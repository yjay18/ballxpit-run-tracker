#!/usr/bin/env python3
"""Check generated search assets, or public production HTTP with --production."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlsplit
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET
from build_search import BASE, OUT, SITE

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(); self.meta = {}; self.canonicals = []; self.links = []; self.ids = set(); self.jsonld = []; self.text = []; self.title = ''; self.in_title = False; self.script = None
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        if tag == 'meta':
            key = a.get('name', a.get('property'))
            if key:
                assert key not in self.meta, f'Duplicate metadata: {key}'
                self.meta[key] = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical': self.canonicals.append(a['href'])
        if tag == 'a': self.links.append(a.get('href', ''))
        if tag == 'title': self.in_title = True
        if tag == 'script': self.script = '' if a.get('type') == 'application/ld+json' else False
    def handle_data(self, data):
        if self.in_title: self.title += data
        if isinstance(self.script, str): self.script += data
        if self.script is None: self.text.append(data)
    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
        if tag == 'script':
            if isinstance(self.script, str): self.jsonld.append(json.loads(self.script))
            self.script = None

BOTS = ['Googlebot', 'bingbot', 'OAI-SearchBot', 'Claude-SearchBot', 'PerplexityBot']
def fetch(url, ua='PitCrewSearchAudit/1.0'):
    with urlopen(Request(url, headers={'User-Agent': ua}), timeout=20) as r:
        assert r.status == 200, (url, r.status)
        return r.read().decode(), dict(r.headers), r.url

def check(production=False, preview=False):
    def read(path):
        if not production: return (OUT / path).read_text()
        text, headers, final = fetch(BASE + ('' if path == 'index.html' else path))
        assert final == BASE + ('' if path == 'index.html' else path), (path, final)
        assert 'noindex' not in headers.get('X-Robots-Tag', '').lower(), headers
        kind = headers.get('Content-Type', '').lower()
        expected = 'html' if path.endswith('.html') else 'xml' if path.endswith('.xml') else 'text/plain'
        assert expected in kind, (path, kind)
        return text
    pages = {p: Page(read(p)) for p in ['index.html', 'guide.html']}
    assert len({p.title for p in pages.values()}) == 2
    assert len({p.meta['description'] for p in pages.values()}) == 2
    for path, p in pages.items():
        url = BASE + ('' if path == 'index.html' else path)
        assert p.canonicals == ([] if preview else [url]), (path, p.canonicals)
        assert ('noindex' in p.meta['robots']) == preview
        for key in ['og:title', 'og:description', 'og:url', 'og:image', 'og:image:alt', 'twitter:title', 'twitter:description', 'twitter:image', 'twitter:card']:
            assert p.meta.get(key), (path, key)
        assert p.meta['og:url'] == url
        if not preview:
            assert len(p.jsonld) == 1
            graph = p.jsonld[0]['@graph']
            assert {g['@type'] for g in graph} == {'WebSite', 'WebPage'}
            assert graph[1]['url'] == url and graph[1]['name'] == p.title
            assert graph[1]['description'] == p.meta['description']
            assert not any(x in json.dumps(graph) for x in ['aggregateRating', 'offers', 'review', 'operatingSystem'])
        for link in p.links:
            target = urlsplit(urljoin(url, link))
            if target.netloc == urlsplit(BASE).netloc and target.path.startswith(urlsplit(BASE).path):
                relative = target.path[len(urlsplit(BASE).path):] or 'index.html'
                assert relative in pages, (path, link)
                if target.fragment: assert target.fragment in pages[relative].ids, link
    guide_text = ' '.join(pages['guide.html'].text)
    for section in SITE['sections']: assert section['text'] in guide_text
    assert 'guide.html' in pages['index.html'].links
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    root = ET.fromstring(read('sitemap.xml'))
    assert root.tag == '{' + ns['s'] + '}urlset'
    urls = [x.text for x in root.findall('s:url/s:loc', ns)]
    assert urls == ([] if preview else [BASE, BASE + 'guide.html']), urls
    for date in root.findall('s:url/s:lastmod', ns):
        from datetime import datetime, timezone
        assert datetime.fromisoformat(date.text) <= datetime.now(timezone.utc)
    if not preview:
        llms = read('llms.txt')
        for section in SITE['sections']: assert section['text'] in llms
    if production:
        origin = urlsplit(BASE).scheme + '://' + urlsplit(BASE).netloc
        try:
            robots, _, _ = fetch(origin + '/robots.txt')
            rp = RobotFileParser(); rp.parse(robots.splitlines())
            for bot in BOTS:
                for url in urls: assert rp.can_fetch(bot, url), (bot, url)
            print('Origin robots policy permits tested search bots.')
        except HTTPError as e:
            if e.code != 404: raise
            print('ACTION REQUIRED: origin /robots.txt is 404; install the supplied policy at the origin root.')
        for bot in BOTS:
            for url in urls:
                source, headers, final = fetch(url, bot)
                assert final == url and 'noindex' not in headers.get('X-Robots-Tag', '').lower()
                assert Page(source).canonicals == [url]
        for alias in [BASE + 'index.html', BASE + '?utm_source=search-audit']:
            source, headers, _ = fetch(alias)
            assert Page(source).canonicals == [BASE], alias
        with urlopen(BASE + 'img/pit-crew-logo.png', timeout=20) as r:
            assert r.status == 200 and 'image/png' in r.headers.get('Content-Type', '')
        try: fetch(BASE + 'does-not-exist-search-audit')
        except HTTPError as e: assert e.code == 404
        else: raise AssertionError('Missing page returned 200: soft 404')
    else:
        error = Page((OUT / '404.html').read_text())
        assert 'noindex' in error.meta['robots'] and not error.canonicals
        rp = RobotFileParser(); rp.parse((OUT / 'robots.txt').read_text().splitlines())
        for bot in BOTS:
            for url in [BASE, BASE + 'guide.html']: assert rp.can_fetch(bot, url)
        assert (OUT / 'LICENSE').exists()
        assert not (OUT / 'README.md').exists() and not (OUT / 'scripts').exists()
        if preview: assert not (OUT / 'llms.txt').exists()
    print('PASS: ' + ('production HTTP' if production else 'local preview' if preview else 'local production') + ' metadata, schema, static content, links, sitemap, and crawl checks')

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--production', action='store_true'); p.add_argument('--preview', action='store_true'); a = p.parse_args()
    try: check(a.production, a.preview)
    except Exception as e: print(f'FAIL: {e}', file=sys.stderr); sys.exit(1)

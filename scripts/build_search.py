#!/usr/bin/env python3
"""Build the public static site using only the Python standard library."""
import argparse
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
SITE = json.loads((ROOT / 'content/site.json').read_text())
BASE = SITE['url']
assert BASE.startswith('https://') and BASE.endswith('/') and not urlsplit(BASE).query

def metadata(title, description, path, preview=False):
    esc = html.escape
    url = BASE + path
    tags = [f'<title>{esc(title)}</title>', f'<meta name="description" content="{esc(description, quote=True)}">',
            f'<meta name="robots" content="{"noindex, nofollow" if preview else "index, follow"}">']
    if not preview:
        tags.append(f'<link rel="canonical" href="{url}">')
    for key, value in {'og:title': title, 'og:description': description, 'og:type': 'website', 'og:url': url,
                       'og:site_name': SITE['name'], 'og:image': BASE + 'img/pit-crew-logo.png',
                       'og:image:alt': 'Pit Crew logo'}.items():
        tags.append(f'<meta property="{key}" content="{esc(value, quote=True)}">')
    for key, value in {'twitter:card': 'summary', 'twitter:title': title, 'twitter:description': description,
                       'twitter:image': BASE + 'img/pit-crew-logo.png', 'twitter:image:alt': 'Pit Crew logo'}.items():
        tags.append(f'<meta name="{key}" content="{esc(value, quote=True)}">')
    if not preview:
        for env, name in [('GOOGLE_SITE_VERIFICATION', 'google-site-verification'), ('BING_SITE_VERIFICATION', 'msvalidate.01')]:
            if os.environ.get(env):
                tags.append(f'<meta name="{name}" content="{esc(os.environ[env], quote=True)}">')
        data = {'@context': 'https://schema.org', '@graph': [
            {'@type': 'WebSite', '@id': BASE + '#website', 'url': BASE, 'name': SITE['name'], 'description': SITE['description']},
            {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': title, 'description': description,
             'isPartOf': {'@id': BASE + '#website'}, 'inLanguage': 'en'}]}
        tags.append('<script type="application/ld+json">' + json.dumps(data).replace('<', '\\u003c') + '</script>')
    return '<!-- SEARCH METADATA START -->\n' + '\n'.join(tags) + '\n<!-- SEARCH METADATA END -->'

def lastmod(paths):
    # Never substitute build time or filesystem mtime. Dirty/untracked sources lack a verified date.
    try:
        status = subprocess.check_output(['git', 'status', '--porcelain', '--', *paths], cwd=ROOT, text=True)
        if status.strip():
            return None
        value = subprocess.check_output(['git', 'log', '-1', '--format=%cI', '--', *paths], cwd=ROOT, text=True).strip()
        return value or None
    except subprocess.CalledProcessError:
        return None

def build(preview=False):
    OUT.mkdir(exist_ok=True)
    # Remove only our own previous output. No source files are published.
    for child in OUT.iterdir():
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    shutil.copytree(ROOT / 'img', OUT / 'img')
    (OUT / '.nojekyll').touch()
    shutil.copyfile(ROOT / 'LICENSE', OUT / 'LICENSE')
    source = (ROOT / 'index.html').read_text()
    assert source.count('<!-- SEARCH METADATA START -->') == 1, 'Missing or duplicate metadata template'
    home = re.sub(r'<!-- SEARCH METADATA START -->.*?<!-- SEARCH METADATA END -->',
                  lambda _: metadata(SITE['title'], SITE['description'], '', preview), source, flags=re.S)
    (OUT / 'index.html').write_text(home)
    esc = html.escape
    nav = ' · '.join(f'<a href="#{s["id"]}">{esc(s["title"])}</a>' for s in SITE['sections'])
    sections = '\n'.join(f'<section id="{s["id"]}"><h2>{esc(s["title"])}</h2><p>{esc(s["text"])}</p></section>' for s in SITE['sections'])
    style = re.search(r'<style>(.*?)</style>', source, re.S).group(1)
    guide = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
{metadata(SITE['guideTitle'], SITE['guideDescription'], 'guide.html', preview)}
<link rel="icon" href="img/pit-crew-logo.svg" type="image/svg+xml"><style>{style}
.guide{{max-width:850px;padding-top:2rem}} .guide p{{line-height:1.8}} .guide nav{{line-height:2}}</style></head>
<body><header><a href="./">PIT CREW — Back to the tracker</a></header><main class="guide">
<h1>How to use Pit Crew</h1><p>{esc(SITE['guideDescription'])}</p><nav aria-label="Guide contents">{nav}</nav>
{sections}<p><a href="./">Open the run tracker</a> · <a href="https://ballxpit.wiki.gg/wiki/Balls">Community ball reference</a> · <a href="https://github.com/cryphixi/ballxpit-tracker">Original tracker</a></p></main></body></html>'''
    (OUT / 'guide.html').write_text(guide)
    (OUT / '404.html').write_text('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, follow"><title>Page not found — Pit Crew</title></head><body><h1>Page not found</h1><p><a href="' + BASE + '">Return to Pit Crew</a></p></body></html>')
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', ns)
    sitemap = ET.Element('{' + ns + '}urlset')
    # Explicit public route registry: utility pages, fragments, and browser run state are never URLs here.
    routes = {'': ['index.html', 'content/site.json', 'scripts/build_search.py'],
              'guide.html': ['content/site.json', 'scripts/build_search.py', 'index.html']}
    if not preview:
        for path, inputs in routes.items():
            entry = ET.SubElement(sitemap, 'url')
            ET.SubElement(entry, 'loc').text = BASE + path
            modified = lastmod(inputs)
            if modified:
                ET.SubElement(entry, 'lastmod').text = modified
    ET.ElementTree(sitemap).write(OUT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    policy = '# Install at the ORIGIN ROOT /robots.txt. A project subdirectory copy is not authoritative.\n'
    if preview:
        # Allow fetching so crawlers can observe noindex. Authentication is a separate hosting requirement.
        policy += 'User-agent: *\nAllow: /\n# Preview HTML has noindex. Protect private previews with authentication.\n'
    else:
        policy += '# Search and user-requested retrieval. Existing training permissions are unchanged.\n'
        for bot in ['*', 'Googlebot', 'bingbot', 'OAI-SearchBot', 'Claude-SearchBot', 'PerplexityBot', 'ChatGPT-User', 'Claude-User', 'Perplexity-User']:
            policy += f'User-agent: {bot}\nAllow: /\n\n'
        policy += '# Training policy is separate: GPTBot, ClaudeBot, and Google-Extended\n# currently inherit the existing unrestricted policy. Change only after an owner decision.\n'
        policy += f'Sitemap: {BASE}sitemap.xml\n'
    (OUT / 'robots.txt').write_text(policy)
    if not preview:
        llms = f'# {SITE["name"]}\n\n> {SITE["description"]}\n\n'
        llms += '\n\n'.join(s['text'] for s in SITE['sections'])
        llms += f'\n\n## Pages\n- [Run tracker]({BASE}): Interactive app; JavaScript required for tracking.\n- [User guide]({BASE}guide.html): Features, usage, saved progress, and credits; readable without JavaScript.\n\nThis file is an experimental discovery supplement, not a crawler permission or indexing guarantee.\n'
        (OUT / 'llms.txt').write_text(llms)
        key = os.environ.get('INDEXNOW_KEY', '')
        if key:
            if not re.fullmatch(r'[a-zA-Z0-9-]{8,128}', key):
                raise ValueError('Invalid IndexNow key')
            (OUT / (key + '.txt')).write_text(key)
    print(f'Built {"preview (noindex)" if preview else "production"} site in {OUT}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--preview', action='store_true')
    build(parser.parse_args().preview)

#!/usr/bin/env python3
"""Explicit post-deployment notification. Does not run during builds."""
import json
import os
import re
import sys
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from build_search import BASE
from check_search import check

if __name__ == '__main__':
    key = os.environ.get('INDEXNOW_KEY', '')
    if not re.fullmatch(r'[a-zA-Z0-9-]{8,128}', key):
        sys.exit('Set INDEXNOW_KEY to the same 8–128 character key used for the deployed build.')
    urls = sys.argv[1:]
    allowed = {BASE, BASE + 'guide.html'}
    if not urls or any(u not in allowed for u in urls):
        sys.exit('Pass only changed canonical public URLs from the sitemap; no previews or fragments.')
    check(production=True)
    location = BASE + key + '.txt'
    with urlopen(location, timeout=20) as r:
        if r.url != location or r.read().decode().strip() != key:
            sys.exit('Deployed key file did not match; no URLs submitted.')
    payload = {'host': urlsplit(BASE).netloc, 'key': key, 'keyLocation': location, 'urlList': list(dict.fromkeys(urls))}
    request = Request('https://api.indexnow.org/indexnow', data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
    with urlopen(request, timeout=20) as response:
        print(f'IndexNow HTTP {response.status}: notification response only; indexing is not confirmed.')

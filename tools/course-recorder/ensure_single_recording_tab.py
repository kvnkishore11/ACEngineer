#!/usr/bin/env python3
from __future__ import annotations

"""Keep the recording Chrome profile as a single-page sandbox.

This tool is intentionally conservative: it operates only on the provided CDP
port, closes extra page targets, and leaves one controlled page for the recorder.
Use before starting a recording queue, not against the user's normal Chrome.
"""

import argparse
import json
import time
import urllib.parse
import urllib.request


def http_json(url: str, timeout: float = 2.0, method: str = 'GET'):
    req = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', type=int, default=9223)
    ap.add_argument('--url', default='about:blank')
    args = ap.parse_args()

    base = f'http://127.0.0.1:{args.port}'
    http_json(base + '/json/version')
    pages = [p for p in http_json(base + '/json/list') if p.get('type') == 'page']

    keep = None
    for p in pages:
        if p.get('url') == args.url or (args.url == 'about:blank' and p.get('url') == 'about:blank'):
            keep = p
            break
    if keep is None and pages:
        keep = pages[0]
    if keep is None:
        keep = http_json(base + '/json/new?' + urllib.parse.quote(args.url, safe=':/?=&'), method='PUT')
        pages = [p for p in http_json(base + '/json/list') if p.get('type') == 'page']

    keep_id = keep.get('id')
    closed = []
    for p in pages:
        pid = p.get('id')
        if not pid or pid == keep_id:
            continue
        try:
            http_json(base + '/json/close/' + pid)
            closed.append({'id': pid, 'url': p.get('url'), 'title': p.get('title')})
        except Exception as e:
            closed.append({'id': pid, 'url': p.get('url'), 'error': repr(e)})

    # Navigate the kept page to requested URL if needed.
    if args.url and keep.get('url') != args.url:
        http_json(base + '/json/activate/' + keep_id)
        # /json/new would create another tab, so use a tiny CDP websocket-free
        # Browser endpoint workaround: leave navigation to record_lesson_cdp.py.

    print(json.dumps({'ok': True, 'kept': {'id': keep_id, 'url': keep.get('url'), 'title': keep.get('title')}, 'closed': closed}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

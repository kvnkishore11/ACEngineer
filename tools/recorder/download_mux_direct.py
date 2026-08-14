#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
from __future__ import annotations

import argparse
import json
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path

from recorder_common import ensure_output_dir, get_lesson, safe_name
from record_lesson_cdp import CDP, find_cdp_base, runtime_eval


def page_tabs(base: str):
    return [p for p in json.loads(urllib.request.urlopen(base + '/json/list', timeout=3).read().decode()) if p.get('type') == 'page']


def main() -> int:
    ap = argparse.ArgumentParser(description='Download current lesson directly from mux-player signed playback URL')
    ap.add_argument('lesson')
    ap.add_argument('--port', type=int, default=9223)
    ap.add_argument('--suffix', default='mux-direct')
    ap.add_argument('--force', action='store_true')
    args = ap.parse_args()

    lesson = get_lesson(args.lesson)
    out_dir = ensure_output_dir(lesson)
    out = out_dir / safe_name(lesson, args.suffix)
    if out.exists() and not args.force:
        raise SystemExit(f'Refusing to overwrite existing file: {out}')
    tmp = out.with_suffix('.recording.mp4')
    if tmp.exists():
        tmp.unlink()

    base = find_cdp_base(args.port)
    tabs = page_tabs(base)
    if not tabs:
        raise SystemExit('No CDP page tabs available')
    tab = tabs[0]
    cdp = CDP(tab['webSocketDebuggerUrl'])
    cdp.cmd('Runtime.enable')
    cdp.cmd('Page.enable')
    if tab.get('url') != lesson['url']:
        cdp.cmd('Page.navigate', {'url': lesson['url']}, timeout=10)
        time.sleep(5)
    attrs = runtime_eval(cdp, """
(() => {
  const m = document.querySelector('mux-player');
  if (!m) return null;
  return Object.fromEntries(Array.from(m.attributes).map(a => [a.name, a.value]));
})()
""", timeout=10)
    if not attrs:
        raise SystemExit('No mux-player found')
    playback_id = attrs.get('playback-id')
    playback_token = attrs.get('playback-token')
    if not playback_id or not playback_token:
        raise SystemExit('Missing mux playback id/token')
    hls = f'https://stream.mux.com/{playback_id}.m3u8?token={urllib.parse.quote(playback_token)}'
    cmd = [
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'warning',
        '-protocol_whitelist', 'file,http,https,tcp,tls,crypto',
        '-i', hls,
        '-map', '0:v:0?', '-map', '0:a:0?',
        '-c', 'copy', '-movflags', '+faststart', str(tmp),
    ]
    proc = subprocess.run(cmd)
    if proc.returncode != 0:
        return proc.returncode
    tmp.rename(out)
    print(out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from recorder_common import ffprobe_json, load_manifest, safe_name, vtt_duration

ROOT = Path('/Users/kvnkishore/WebstormProjects/AgenticEngineer/videos')
REPORT = ROOT / 'RECORDING_REPORT.md'

rows = []
for lesson in load_manifest():
    out_dir = Path(lesson['output_dir'])
    candidates = [
        *sorted(out_dir.glob(f"{lesson['key']}-{lesson['slug']}-cdp-15fps-audio-synced-pause-corrected.mp4")),
        out_dir / safe_name(lesson, 'cdp-15fps-audio-synced'),
        out_dir / safe_name(lesson, 'cdp-15fps-audio-fixed'),
        out_dir / safe_name(lesson, 'mux-direct'),
        out_dir / safe_name(lesson, 'cdp-15fps'),
    ]
    video = next((p for p in candidates if p.exists()), candidates[0])
    validation = out_dir / 'validation.json'
    contact = out_dir / 'contact-sheet.jpg'
    status = 'missing'
    duration = None
    resolution = ''
    audio = 'no'
    notes = ''
    if video.exists():
        try:
            data = ffprobe_json(video)
            duration = float(data.get('format', {}).get('duration') or 0)
            streams = data.get('streams', [])
            vs = next((s for s in streams if s.get('codec_type') == 'video'), None)
            if vs:
                resolution = f"{vs.get('width')}x{vs.get('height')}"
            audio = 'yes' if any(s.get('codec_type') == 'audio' for s in streams) else 'no'
            status = 'recorded'
        except Exception as e:
            notes = f'ffprobe failed: {e}'
            status = 'probe_failed'
    if validation.exists():
        try:
            val = json.loads(validation.read_text())
            status = 'validated' if val.get('ok') else 'validation_failed'
            if val.get('failures'):
                notes = '; '.join(val['failures'][:3])
        except Exception as e:
            notes = f'validation read failed: {e}'
    expected = vtt_duration(lesson.get('transcript', ''))
    rows.append({
        'key': lesson['key'],
        'title': lesson['title'],
        'status': status,
        'duration': duration,
        'expected': expected,
        'resolution': resolution,
        'audio': audio,
        'video': video,
        'validation': validation,
        'contact': contact,
        'notes': notes,
    })

lines = ['# AgenticEngineer Recording Report', '', '| Lesson | Status | Duration | Expected | Resolution | Audio | Notes |', '|---|---:|---:|---:|---:|---:|---|']
for r in rows:
    dur = f"{r['duration']:.1f}s" if r['duration'] else ''
    exp = f"{r['expected']:.1f}s" if r['expected'] else ''
    lines.append(f"| {r['key']} — {r['title']} | {r['status']} | {dur} | {exp} | {r['resolution']} | {r['audio']} | {r['notes']} |")
lines += ['', '## Paths', '']
for r in rows:
    lines += [f"### {r['key']} — {r['title']}", f"- Video: `{r['video']}`", f"- Validation: `{r['validation']}`", f"- Contact sheet: `{r['contact']}`", '']
REPORT.write_text('\n'.join(lines))
print(REPORT)

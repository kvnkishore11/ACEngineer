#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from recorder_common import (
    detect_silence,
    extract_frame,
    ffprobe_json,
    ffprobe_duration,
    get_lesson,
    make_contact_sheet,
    safe_name,
    vtt_duration,
    volume_detect,
    write_json,
)


def fps_value(rate: str | None) -> float | None:
    if not rate or rate == "0/0":
        return None
    if "/" in rate:
        a, b = rate.split("/", 1)
        return float(a) / float(b) if float(b) else None
    return float(rate)


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate a TAC/AgenticEngineer recording")
    ap.add_argument("lesson", help="lesson key/order/slug")
    ap.add_argument("--file", default=None)
    ap.add_argument("--fps", type=float, default=15.0)
    ap.add_argument("--duration-tolerance", type=float, default=120.0)
    ap.add_argument("--skip-duration-check", action="store_true", help="use for short smoke tests")
    ap.add_argument("--require-audio", action="store_true", default=True)
    args = ap.parse_args()

    lesson = get_lesson(args.lesson)
    out_dir = Path(lesson["output_dir"])
    video = Path(args.file) if args.file else out_dir / safe_name(lesson, f"cdp-{int(args.fps)}fps")
    report_path = out_dir / "validation.md"
    json_path = out_dir / "validation.json"
    contact = out_dir / "contact-sheet.jpg"
    first = out_dir / "verify-first.jpg"
    middle = out_dir / "verify-middle.jpg"
    last = out_dir / "verify-last.jpg"

    checks = []
    failures = []
    def check(name: str, ok: bool, detail: str):
        checks.append({"name": name, "ok": ok, "detail": detail})
        if not ok:
            failures.append(f"{name}: {detail}")

    check("file exists", video.exists(), str(video))
    if not video.exists():
        write_json(json_path, {"ok": False, "checks": checks, "failures": failures})
        report_path.write_text("# Validation failed\n\nMissing video file.\n")
        return 2

    data = ffprobe_json(video)
    duration = float(data.get("format", {}).get("duration") or 0)
    expected = vtt_duration(lesson.get("transcript", ""))
    streams = data.get("streams", [])
    video_streams = [s for s in streams if s.get("codec_type") == "video"]
    audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
    check("has video stream", bool(video_streams), f"streams={len(video_streams)}")
    check("has audio stream", bool(audio_streams), f"streams={len(audio_streams)}")
    if args.skip_duration_check:
        check("duration smoke check", duration > 0, f"video={duration:.1f}s transcript={expected:.1f}s duration comparison skipped")
    elif expected:
        check("duration matches transcript", abs(duration - expected) <= args.duration_tolerance, f"video={duration:.1f}s transcript={expected:.1f}s tolerance={args.duration_tolerance}s")
    else:
        check("duration available", duration > 0, f"video={duration:.1f}s")
    if video_streams:
        vs = video_streams[0]
        fps = fps_value(vs.get("avg_frame_rate")) or fps_value(vs.get("r_frame_rate"))
        check("resolution plausible", int(vs.get("width") or 0) >= 1280 and int(vs.get("height") or 0) >= 720, f"{vs.get('width')}x{vs.get('height')}")
        check("fps near target", fps is not None and fps >= max(8, args.fps * 0.75), f"fps={fps}")

    try:
        make_contact_sheet(video, contact)
        check("contact sheet created", contact.exists() and contact.stat().st_size > 0, str(contact))
    except Exception as e:
        check("contact sheet created", False, repr(e))
    try:
        extract_frame(video, first, 5)
        extract_frame(video, middle, max(0, duration / 2))
        extract_frame(video, last, max(0, duration - 10))
        check("checkpoint frames created", all(p.exists() and p.stat().st_size > 0 for p in (first, middle, last)), f"{first}, {middle}, {last}")
    except Exception as e:
        check("checkpoint frames created", False, repr(e))

    silence_summary = "not checked"
    volume_summary = "not checked"
    if audio_streams:
        try:
            samples = [volume_detect(video, start=s, seconds=10) for s in (0, max(0, duration / 2), max(0, duration - 20))]
            max_vols = []
            for sample in samples:
                value = sample.get("max_volume")
                if value is not None:
                    max_vols.append(float(value))
            best_max = max(max_vols) if max_vols else None
            volume_summary = f"sample_max_volumes={max_vols} best_max={best_max}"
            check("audio has audible signal", best_max is not None and best_max > -50.0, volume_summary)
        except Exception as e:
            check("audio has audible signal", False, repr(e))
        try:
            silence = detect_silence(video)
            gaps = re.findall(r"silence_duration: ([0-9.]+)", silence)
            long_gaps = [float(g) for g in gaps if float(g) >= 10]
            silence_summary = f"long_silence_gaps={long_gaps[:10]} total_gaps={len(gaps)}"
            check("audio not mostly silent", len(long_gaps) < 5, silence_summary)
        except Exception as e:
            check("audio not mostly silent", False, repr(e))

    ok = not failures
    report = [
        f"# Validation: {lesson['key']} — {lesson['title']}",
        "",
        f"Output: `{video}`",
        f"Overall: {'PASS' if ok else 'FAIL'}",
        f"Duration: {duration:.1f}s",
        f"Transcript duration: {expected:.1f}s" if expected else "Transcript duration: unavailable",
        f"Contact sheet: `{contact}`",
        f"Checkpoint frames: `{first}`, `{middle}`, `{last}`",
        f"Audio silence: {silence_summary}",
        f"Audio volume: {volume_summary}",
        "",
        "## Checks",
    ]
    for c in checks:
        report.append(f"- [{'x' if c['ok'] else ' '}] {c['name']}: {c['detail']}")
    if failures:
        report += ["", "## Failures"] + [f"- {f}" for f in failures]
    report_path.write_text("\n".join(report) + "\n")
    write_json(json_path, {"ok": ok, "lesson": lesson, "video": str(video), "duration": duration, "expected_duration": expected, "checks": checks, "failures": failures})
    print(report_path)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

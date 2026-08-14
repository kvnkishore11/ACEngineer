#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from recorder_common import get_lesson, load_manifest, safe_name, write_json

ROOT = Path(__file__).resolve().parent
STATUS = ROOT / "queue-status.json"


def run(cmd: list[str], cwd: Path = ROOT) -> int:
    print("RUN", " ".join(cmd), flush=True)
    p = subprocess.Popen(cmd, cwd=str(cwd))
    return p.wait()


def main() -> int:
    ap = argparse.ArgumentParser(description="Sequential AgenticEngineer recorder queue. Lesson 1 gate is enforced.")
    ap.add_argument("--start", default="tac-1")
    ap.add_argument("--only", default=None, help="record only one lesson key/order")
    ap.add_argument("--fps", type=int, default=15)
    ap.add_argument("--quality", type=int, default=88)
    ap.add_argument("--audio-device-index", default="2")
    ap.add_argument("--port", type=int, default=9223)
    ap.add_argument("--seconds", type=float, default=None, help="test duration override")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    manifest = load_manifest()
    if args.only:
        lessons = [get_lesson(args.only, manifest)]
    else:
        start_seen = False
        lessons = []
        for l in manifest:
            if str(l["key"]) == str(args.start) or str(l["order"]) == str(args.start):
                start_seen = True
            if start_seen:
                lessons.append(l)
    if not lessons:
        raise SystemExit("No lessons selected")

    results = []
    for lesson in lessons:
        out_dir = Path(lesson["output_dir"])
        out_dir.mkdir(parents=True, exist_ok=True)
        final = out_dir / safe_name(lesson, f"cdp-{args.fps}fps")
        if final.exists() and not args.force:
            results.append({"lesson": lesson["key"], "status": "skipped", "reason": "exists", "output": str(final)})
            continue
        suffix = f"smoke-{args.fps}fps" if args.seconds is not None else f"cdp-{args.fps}fps"
        rec_cmd = [
            sys.executable, str(ROOT / "record_lesson_cdp.py"), lesson["key"],
            "--port", str(args.port), "--fps", str(args.fps), "--quality", str(args.quality),
            "--audio-device-index", str(args.audio_device_index), "--suffix", suffix, "--attach-existing",
        ]
        if args.seconds is not None:
            rec_cmd += ["--seconds", str(args.seconds)]
        rc = run(rec_cmd)
        if rc != 0:
            results.append({"lesson": lesson["key"], "status": "record_failed", "rc": rc})
            write_json(STATUS, {"updated": time.time(), "results": results})
            return rc
        val_file = out_dir / safe_name(lesson, suffix)
        val_cmd = [sys.executable, str(ROOT / "validate_recording.py"), lesson["key"], "--fps", str(args.fps), "--file", str(val_file)]
        if args.seconds is not None:
            val_cmd.append("--skip-duration-check")
        rc = run(val_cmd)
        if rc != 0:
            results.append({"lesson": lesson["key"], "status": "validation_failed", "rc": rc})
            write_json(STATUS, {"updated": time.time(), "results": results})
            # Lesson 1 gate: never proceed after any validation failure.
            return rc
        results.append({"lesson": lesson["key"], "status": "validated", "output": str(final)})
        write_json(STATUS, {"updated": time.time(), "results": results})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

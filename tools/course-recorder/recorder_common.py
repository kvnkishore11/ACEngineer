#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "lesson_manifest.json"


def load_manifest(path: Path = MANIFEST_PATH) -> list[dict[str, Any]]:
    return json.loads(path.read_text())


def get_lesson(key_or_order: str | int, manifest: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    manifest = manifest or load_manifest()
    s = str(key_or_order)
    for lesson in manifest:
        if str(lesson.get("key")) == s or str(lesson.get("order")) == s or lesson.get("slug") == s:
            return lesson
    raise SystemExit(f"Lesson not found: {key_or_order}")


def ensure_output_dir(lesson: dict[str, Any]) -> Path:
    out = Path(lesson["output_dir"])
    out.mkdir(parents=True, exist_ok=True)
    return out

_TS_RE = re.compile(r"(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})")


def parse_ts(ts: str) -> float:
    m = _TS_RE.search(ts)
    if not m:
        raise ValueError(ts)
    h = int(m.group(1) or 0)
    mn = int(m.group(2))
    sec = int(m.group(3))
    ms = int(m.group(4))
    return h * 3600 + mn * 60 + sec + ms / 1000


def vtt_duration(path: str | Path) -> float | None:
    p = Path(path)
    if not p.exists():
        return None
    last = None
    for line in p.read_text(errors="ignore").splitlines():
        if "-->" in line:
            try:
                last = parse_ts(line.split("-->", 1)[1].strip().split()[0])
            except Exception:
                pass
    return last


def run(cmd: list[str], *, timeout: int | None = None, check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, timeout=timeout, check=check, text=True, stdout=subprocess.PIPE if capture else None, stderr=subprocess.PIPE if capture else None)


def ffprobe_json(path: str | Path) -> dict[str, Any]:
    cp = run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration,size:stream=index,codec_type,codec_name,width,height,avg_frame_rate,r_frame_rate,nb_frames",
        "-of", "json", str(path)
    ], timeout=30)
    return json.loads(cp.stdout or "{}")


def ffprobe_duration(path: str | Path) -> float | None:
    try:
        data = ffprobe_json(path)
        return float(data.get("format", {}).get("duration") or 0)
    except Exception:
        return None


def make_contact_sheet(video: str | Path, output: str | Path, cols: int = 4, rows: int = 3) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    duration = ffprobe_duration(video) or 60.0
    # Pick roughly cols*rows samples across the whole clip. For short smoke clips,
    # one frame per second avoids the old empty-contact-sheet failure.
    interval = max(duration / max(1, cols * rows), 1.0)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(video),
        "-vf", f"fps=1/{interval:.3f},scale=480:-1,tile={cols}x{rows}",
        "-frames:v", "1", str(output)
    ], timeout=180)


def extract_frame(video: str | Path, output: str | Path, seconds: float) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-ss", str(max(0, seconds)), "-i", str(video),
        "-frames:v", "1", "-q:v", "2", str(output)
    ], timeout=60)


def detect_silence(video: str | Path, silence_db: int = -45, min_gap: float = 5.0) -> str:
    cp = subprocess.run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(video),
        "-af", f"silencedetect=noise={silence_db}dB:d={min_gap}",
        "-f", "null", "-"
    ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
    return cp.stderr


def volume_detect(video: str | Path, start: float = 0, seconds: float = 30) -> dict[str, float | None]:
    cp = subprocess.run([
        "ffmpeg", "-hide_banner", "-nostats",
        "-ss", str(start), "-i", str(video), "-t", str(seconds),
        "-af", "volumedetect", "-f", "null", "-"
    ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90)
    out: dict[str, float | None] = {"mean_volume": None, "max_volume": None}
    for name in out:
        m = re.search(rf"{name}:\s*(-?[0-9.]+) dB", cp.stderr)
        if m:
            out[name] = float(m.group(1))
    return out


def safe_name(lesson: dict[str, Any], suffix: str = "cdp-15fps") -> str:
    return f"{lesson['key']}-{lesson['slug']}-{suffix}.mp4"


def write_json(path: str | Path, data: Any) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2, sort_keys=True))

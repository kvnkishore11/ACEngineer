#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Weekly IndyDevDan youtube/ catalog updater.

Idempotent: never re-creates folders for known video IDs.
Discovers new uploads from @IndyDevDan, builds lesson folders
(transcript+metadata), attaches codebases, rebuilds INDEX.

Stdout:
  - non-empty when new videos added or errors → delivered by cron
  - empty when nothing new and healthy → silent (watchdog style)

Usage:
  python3 weekly_update.py
  python3 weekly_update.py --pass primary|doublecheck
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/youtube")
CHANNEL = "https://www.youtube.com/@IndyDevDan/videos"
PY = "/Users/kvnkishore/anaconda3/bin/python3"
YTDLP = "yt-dlp"
# Look at newest N channel videos each run (cheap; weekly cadence)
PLAYLIST_END = 30
# Rolling catalog window (keep inventory coherent)
CUTOFF_DAYS = 400  # ~13 months


def log(msg: str, lines: list[str]) -> None:
    lines.append(msg)


def slugify(title: str, vid: str) -> str:
    s = title.lower()
    s = re.sub(r"[’'`]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    s = s[:60].rstrip("-")
    return s or vid


def known_video_ids() -> set[str]:
    ids: set[str] = set()
    inv_path = ROOT / "_inventory.json"
    if inv_path.exists():
        inv = json.loads(inv_path.read_text())
        for v in inv.get("videos", []):
            if v.get("id"):
                ids.add(v["id"])
    # also scan folders (source of truth for dupes)
    for p in ROOT.glob("yt-*"):
        if not p.is_dir():
            continue
        lj = p / "metadata" / "lesson.json"
        if lj.exists():
            try:
                d = json.loads(lj.read_text())
                if d.get("video_id"):
                    ids.add(d["video_id"])
            except Exception:
                pass
        # STATUS id
        st = p / "STATUS.json"
        if st.exists():
            try:
                d = json.loads(st.read_text())
                if d.get("id"):
                    ids.add(d["id"])
            except Exception:
                pass
    return ids


def max_order() -> int:
    n = 0
    inv_path = ROOT / "_inventory.json"
    if inv_path.exists():
        inv = json.loads(inv_path.read_text())
        for v in inv.get("videos", []):
            n = max(n, int(v.get("order") or 0))
    for p in ROOT.glob("yt-*"):
        m = re.match(r"yt-(\d+)-", p.name)
        if m:
            n = max(n, int(m.group(1)))
    return n


def fetch_recent() -> list[dict]:
    """Return newest videos with real upload dates (list of dicts)."""
    cmd = [
        YTDLP,
        "--skip-download",
        "--lazy-playlist",
        "--playlist-end",
        str(PLAYLIST_END),
        "--print",
        "%(id)s\t%(upload_date)s\t%(duration)s\t%(title)s",
        CHANNEL,
    ]
    env = os.environ.copy()
    # avoid conda noise if any
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300, env=env)
    if r.returncode != 0 and not r.stdout.strip():
        raise RuntimeError(f"yt-dlp failed: {(r.stderr or '')[-500:]}")
    out = []
    for line in r.stdout.splitlines():
        # yt-dlp may emit literal \t or real tabs
        parts = line.split("\t") if "\t" in line else line.split("\\t")
        if len(parts) < 4:
            continue
        vid, date, duration, title = parts[0], parts[1], parts[2], parts[3]
        if not re.fullmatch(r"[\w-]{11}", vid):
            continue
        if not re.fullmatch(r"\d{8}", date or ""):
            continue
        out.append(
            {
                "id": vid,
                "upload_date": date,
                "duration_sec": int(duration) if str(duration).isdigit() else None,
                "title": title,
                "url": f"https://www.youtube.com/watch?v={vid}",
            }
        )
    return out


def append_inventory(new_videos: list[dict]) -> None:
    inv_path = ROOT / "_inventory.json"
    if inv_path.exists():
        inv = json.loads(inv_path.read_text())
    else:
        inv = {
            "name": "IndyDevDan YouTube catalog (1 year)",
            "channel": "https://www.youtube.com/@IndyDevDan",
            "channel_id": "UC_x36zCEGilGpB1m-V4gmjg",
            "cutoff": "2025-07-13",
            "videos": [],
        }
    existing = {v["id"] for v in inv.get("videos", [])}
    for v in new_videos:
        if v["id"] in existing:
            continue
        inv["videos"].append(v)
        existing.add(v["id"])
    inv["videos"].sort(key=lambda x: (x.get("upload_date") or "", x.get("order") or 0))
    # re-number orders strictly chronological if needed? keep stable orders for old; new keep assigned
    inv["count"] = len(inv["videos"])
    inv["generated_at"] = datetime.now(timezone.utc).isoformat()
    inv_path.write_text(json.dumps(inv, indent=2, ensure_ascii=False) + "\n")


def build_new(videos: list[dict], lines: list[str]) -> list[dict]:
    if not videos:
        return []
    batch = ROOT / "_weekly_new_batch.json"
    batch.write_text(json.dumps(videos, indent=2, ensure_ascii=False) + "\n")
    r = subprocess.run(
        [PY, str(ROOT / "build_video_folder.py"), "--batch", str(batch)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=1800,
    )
    log(f"build_video_folder exit={r.returncode}", lines)
    if r.stdout:
        # keep tail
        tail = "\n".join(r.stdout.splitlines()[-40:])
        log(tail, lines)
    if r.returncode not in (0, 2):  # 2 = partial transcript miss
        log(f"build stderr: {(r.stderr or '')[-400:]}", lines)
    return videos


def attach_codebases(lines: list[str]) -> None:
    for script in ("attach_codebases.py", "fill_missing_codebases.py"):
        path = ROOT / script
        if not path.exists():
            continue
        r = subprocess.run(
            [PY, str(path)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=1800,
        )
        log(f"{script} exit={r.returncode}", lines)
        # only keep summary tail
        for ln in (r.stdout or "").splitlines():
            if ln.startswith("===") or "primary:" in ln or "linked" in ln or "SUMMARY" in ln:
                if "primary: NONE" in ln:
                    continue
                log(ln, lines)


def rebuild(lines: list[str]) -> None:
    r = subprocess.run(
        [PY, str(ROOT / "rebuild_index.py")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    log(f"rebuild_index exit={r.returncode}", lines)
    if r.stdout:
        log(r.stdout.strip()[:500], lines)


def main() -> int:
    pass_name = "primary"
    if "--pass" in sys.argv:
        i = sys.argv.index("--pass")
        if i + 1 < len(sys.argv):
            pass_name = sys.argv[i + 1]

    lines: list[str] = []
    started = datetime.now().astimezone().isoformat(timespec="seconds")
    try:
        known = known_video_ids()
        recent = fetch_recent()
        new = [v for v in recent if v["id"] not in known]
        # assign stable orders after current max
        order = max_order()
        prepared = []
        for v in sorted(new, key=lambda x: x["upload_date"]):
            order += 1
            slug = slugify(v["title"], v["id"])
            key = f"yt-{order:02d}-{slug}"
            # hard dupe guard: folder must not exist
            if (ROOT / key).exists():
                # collision on order — bump
                while (ROOT / key).exists():
                    order += 1
                    key = f"yt-{order:02d}-{slug}"
            # also guard by id folder scan already in known
            prepared.append(
                {
                    **v,
                    "order": order,
                    "slug": slug,
                    "key": key,
                }
            )

        if not prepared:
            # silent success unless --verbose
            if "--verbose" in sys.argv:
                print(
                    f"IndyDevDan YT weekly ({pass_name}): no new videos @ {started} "
                    f"(known={len(known)}, scanned={len(recent)})"
                )
            # write heartbeat for ops
            hb = {
                "at": started,
                "pass": pass_name,
                "new": 0,
                "known": len(known),
                "scanned": len(recent),
                "status": "noop",
            }
            (ROOT / "_weekly_last_run.json").write_text(json.dumps(hb, indent=2) + "\n")
            return 0

        log(f"IndyDevDan YT weekly ({pass_name}) @ {started}", lines)
        log(f"known={len(known)} scanned={len(recent)} NEW={len(prepared)}", lines)
        for v in prepared:
            log(f"  + {v['upload_date']} {v['id']} {v['key']}", lines)
            log(f"    {v['title'][:90]}", lines)

        append_inventory(prepared)
        build_new(prepared, lines)
        attach_codebases(lines)
        rebuild(lines)

        hb = {
            "at": started,
            "pass": pass_name,
            "new": len(prepared),
            "new_ids": [v["id"] for v in prepared],
            "new_keys": [v["key"] for v in prepared],
            "known_before": len(known),
            "scanned": len(recent),
            "status": "updated",
        }
        (ROOT / "_weekly_last_run.json").write_text(json.dumps(hb, indent=2) + "\n")
        (ROOT / f"_weekly_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json").write_text(
            json.dumps({"summary": hb, "log": lines}, indent=2) + "\n"
        )
        print("\n".join(lines))
        return 0
    except Exception as e:
        print(f"IndyDevDan YT weekly ({pass_name}) ERROR @ {started}: {e}", file=sys.stderr)
        print(f"IndyDevDan YT weekly ({pass_name}) ERROR: {e}")
        (ROOT / "_weekly_last_run.json").write_text(
            json.dumps(
                {"at": started, "pass": pass_name, "status": "error", "error": str(e)},
                indent=2,
            )
            + "\n"
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

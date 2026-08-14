#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Rebuild youtube/INDEX.json and refresh the table in README.md from folder STATUS + inventory."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = REPO_ROOT / "catalog" / "youtube"
REPOS = REPO_ROOT / "codebases" / "yt"


def main():
    inv = json.loads((ROOT / "_inventory.json").read_text())
    lessons = []
    ok_tx = ok_meta = ok_vid = ok_code = 0
    for v in inv["videos"]:
        key = v["key"]
        folder = ROOT / key
        status_path = folder / "STATUS.json"
        status = {}
        if status_path.exists():
            status = json.loads(status_path.read_text())
        lesson_json = folder / "metadata" / "lesson.json"
        lesson: dict = {}
        if lesson_json.exists():
            lesson = json.loads(lesson_json.read_text())
        tx_md = folder / "transcript" / f"{key}.md"
        tx_body = tx_md.read_text() if tx_md.exists() else ""
        tx = bool(status.get("transcript")) or (
            tx_md.exists()
            and "No transcript available" not in tx_body
            and "unavailable at catalog build time" not in tx_body
            and len(tx_body) > 400
        )
        meta = status.get("metadata") or lesson_json.exists()
        mp4 = folder / "video" / f"{key}.mp4"
        vid = mp4.exists() and mp4.stat().st_size > 1_000_000
        code_link = folder / "codebase"
        code = code_link.exists() and (
            code_link.is_symlink() or any(code_link.iterdir()) if code_link.is_dir() else False
        )
        if not code and status.get("codebase"):
            code = True
        if tx:
            ok_tx += 1
        if meta:
            ok_meta += 1
        if vid:
            ok_vid += 1
        if code:
            ok_code += 1
        lessons.append(
            {
                "order": v["order"],
                "key": key,
                "title": lesson.get("title") or v["title"],
                "video_id": v["id"],
                "url": v["url"],
                "upload_date": lesson.get("upload_date") or v.get("upload_date"),
                "duration_sec": lesson.get("duration_sec") or v.get("duration_sec"),
                "codebase": lesson.get("codebase"),
                "codebase_url": lesson.get("codebase_url"),
                "paths": {
                    "video": f"{key}/video/{key}.mp4",
                    "transcript": {
                        "md": f"{key}/transcript/{key}.md",
                        "txt": f"{key}/transcript/{key}.txt",
                        "vtt": f"{key}/transcript/{key}.vtt",
                    },
                    "metadata": {
                        "lesson_json": f"{key}/metadata/lesson.json",
                        "lesson_html": f"{key}/metadata/lesson.html",
                        "course_page_html": f"{key}/metadata/course-page.html",
                        "video_info": f"{key}/metadata/video-info.json",
                        "repos_json": f"{key}/metadata/repos.json",
                    },
                    "codebase": f"{key}/codebase" if code else None,
                },
                "status": {
                    "transcript": "ok" if tx else "missing",
                    "metadata": "ok" if meta else "missing",
                    "video": "mp4" if vid else "source-only",
                    "codebase": "ok" if code else "none-in-description",
                },
            }
        )

    index = {
        "name": "YouTube video catalog (1 year)",
        # Repo-relative on purpose: an absolute path here breaks the index
        # for everyone whose checkout is not at this machine's path.
        "root": "catalog/youtube",
        "channel": inv.get("channel"),
        "channel_id": inv.get("channel_id"),
        "cutoff": inv.get("cutoff"),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "count": len(lessons),
        "stats": {
            "transcript_ok": ok_tx,
            "metadata_ok": ok_meta,
            "video_mp4": ok_vid,
            "codebase_ok": ok_code,
        },
        "layout": {
            "per_video": ["video/", "transcript/", "metadata/", "codebase/"],
            "folder_naming": "yt-NN-<slug>",
            "notes": (
                "Public YT mirror of course lesson folders. "
                "codebase/ is a symlink into codebases/yt/ when the video description lists a GitHub repo/gist."
            ),
            "repos_cache": "codebases/yt/",
        },
        "videos": lessons,
    }
    (ROOT / "INDEX.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n")

    rows = [
        "| # | Key | Title | Date | TX | Meta | Code | Video |",
        "|--:|-----|-------|------|:--:|:----:|:----:|:-----:|",
    ]
    for L in lessons:
        st = L["status"]
        code_cell = "✓" if st["codebase"] == "ok" else "—"
        rows.append(
            f"| {L['order']} | `{L['key']}` | {L['title'][:60]} | {L.get('upload_date') or ''} | "
            f"{'✓' if st['transcript']=='ok' else '—'} | "
            f"{'✓' if st['metadata']=='ok' else '—'} | "
            f"{code_cell} | "
            f"{'mp4' if st['video']=='mp4' else 'src'} |"
        )
    table = "\n".join(rows)
    readme = ROOT / "README.md"
    text = readme.read_text()
    marker = "## Catalog table\n"
    block = (
        f"{marker}\n{table}\n\n"
        f"_Stats: transcript {ok_tx}/{len(lessons)}, metadata {ok_meta}/{len(lessons)}, "
        f"codebase {ok_code}/{len(lessons)}, mp4 {ok_vid}/{len(lessons)}_\n"
    )
    if marker in text:
        pre, _, rest = text.partition(marker)
        if rest.startswith("\n|"):
            idx = rest.find("\n## ")
            if idx != -1:
                text = pre + block + rest[idx:]
            else:
                text = pre + block
        else:
            text = pre + block + rest
    else:
        if "## Relation to paid courses" in text:
            text = text.replace(
                "## Relation to paid courses",
                block + "\n## Relation to paid courses",
            )
        else:
            text = text.rstrip() + "\n\n" + block
    # keep layout blurb accurate
    text = text.replace(
        "No `codebase/` (public YT has no course repo).",
        "Codebase: `codebase/` → `codebases/yt/<owner>__<repo>` when the YT description lists a GitHub repo/gist "
        "(see `metadata/repos.json`). 19 videos have no public code link in the description.",
    )
    readme.write_text(text)
    print(json.dumps(index["stats"] | {"count": index["count"]}, indent=2))
    print("wrote INDEX.json + README table")


if __name__ == "__main__":
    main()

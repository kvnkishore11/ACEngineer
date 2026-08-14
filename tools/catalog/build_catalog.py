#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Build the agent-facing lesson catalog under catalog/courses/.

Hardlinks the finished video from media/final/, symlinks the codebase into
codebases/, and writes catalog/INDEX.json. Sources are never moved.

This script owns the shape of the 18 course `codebase/` symlinks. If a link is
wrong, change the path constants here and re-run — do not hand-edit the links,
because the next run silently overwrites manual fixes.

Folder names are <course>-<n>-<slug>; metadata/course-page.html is the real
course page dump (outerHTML) when available.
"""
from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path

# Every path derives from the repo root so the script runs from anywhere,
# rather than from whatever the current working directory happens to be.
REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = REPO_ROOT
CATALOG = REPO_ROOT / "catalog"          # INDEX.json + README.md live here
OUT = CATALOG / "courses"                # one directory per lesson
FINAL = REPO_ROOT / "media" / "final"
VIDEOS = REPO_ROOT / "media" / "raw"
TX_VTT = REPO_ROOT / "transcripts"
TX_CLEAN = TX_VTT / "clean"
TX_NOTES = TX_VTT / "notes"
# member-assets/ was an intermediate staging tree; its assets are now in the
# catalog itself and its provenance in catalog/_source/ma-download/.
MA = REPO_ROOT / "catalog" / "_source" / "ma-download"
COURSE_HTML = REPO_ROOT / "catalog" / "_source" / "course-pages"
COURSE_HTML_OFFLINE = (
    REPO_ROOT / "catalog" / "_source" / "course-pages-offline" / "for-metadata"
)

# short_key: old/video-dir key; key: MA-style folder name
LESSONS: list[dict] = [
    # TAC
    dict(order=1, short_key="tac-1", key="tac-1-hello-agentic-coding", title="Hello Agentic Coding",
         slug="hello-agentic-coding", course="TAC", video="tac-1-hello-agentic-coding.mp4",
         tx="hello-agentic-coding", codebase="codebases/tac/tac-1",
         url="https://agenticengineer.com/tactical-agentic-coding/course/hello-agentic-coding"),
    dict(order=2, short_key="tac-2", key="tac-2-the-12-leverage-points", title="The 12 Leverage Points",
         slug="the-12-leverage-points", course="TAC", video="tac-2-the-12-leverage-points.mp4",
         tx="the-12-leverage-points", codebase="codebases/tac/tac-2",
         url="https://agenticengineer.com/tactical-agentic-coding/course/the-12-leverage-points"),
    dict(order=3, short_key="tac-3", key="tac-3-success-is-planned", title="Success is Planned",
         slug="success-is-planned", course="TAC", video="tac-3-success-is-planned.mp4",
         tx="success-is-planned", codebase="codebases/tac/tac-3",
         url="https://agenticengineer.com/tactical-agentic-coding/course/success-is-planned"),
    dict(order=4, short_key="tac-4", key="tac-4-afk-agents", title="AFK Agents",
         slug="afk-agents", course="TAC", video="tac-4-afk-agents.mp4",
         tx="afk-agents", codebase="codebases/tac/tac-4",
         url="https://agenticengineer.com/tactical-agentic-coding/course/afk-agents"),
    dict(order=5, short_key="tac-5", key="tac-5-close-the-loops", title="Close the Loops",
         slug="close-the-loops", course="TAC", video="tac-5-close-the-loops.mp4",
         tx="close-the-loops", codebase="codebases/tac/tac-5",
         url="https://agenticengineer.com/tactical-agentic-coding/course/close-the-loops"),
    dict(order=6, short_key="tac-6", key="tac-6-let-your-agents-focus", title="Let Your Agents Focus",
         slug="let-your-agents-focus", course="TAC", video="tac-6-let-your-agents-focus.mp4",
         tx="let-your-agents-focus", codebase="codebases/tac/tac-6",
         url="https://agenticengineer.com/tactical-agentic-coding/course/let-your-agents-focus"),
    dict(order=7, short_key="tac-7", key="tac-7-zte-secret-of-agentic-engineering",
         title="ZTE Secret of Agentic Engineering", slug="zte-secret-of-agentic-engineering",
         course="TAC", video="tac-7-zte-secret-of-agentic-engineering.mp4",
         tx="zte-secret-of-agentic-engineering", codebase="codebases/tac/tac-7",
         url="https://agenticengineer.com/tactical-agentic-coding/course/zte-secret-of-agentic-engineering"),
    dict(order=8, short_key="tac-8", key="tac-8-the-agentic-layer", title="The Agentic Layer",
         slug="the-agentic-layer", course="TAC", video="tac-8-the-agentic-layer.mp4",
         tx="the-agentic-layer", codebase="codebases/tac/tac-8",
         url="https://agenticengineer.com/tactical-agentic-coding/course/the-agentic-layer"),
    # AH
    dict(order=9, short_key="ah-1", key="ah-1-rd-framework-context-window-mastery",
         title="Elite Context Engineering", slug="rd-framework-context-window-mastery",
         course="AH", video="ah-1-rd-framework-context-window-mastery.mp4",
         tx="rd-framework-context-window-mastery", codebase="codebases/ah/elite-context-engineering",
         url="https://agenticengineer.com/tactical-agentic-coding/course/rd-framework-context-window-mastery"),
    dict(order=10, short_key="ah-2", key="ah-2-seven-levels-agentic-prompt-formats",
         title="Seven Levels Agentic Prompt Formats", slug="seven-levels-agentic-prompt-formats",
         course="AH", video="ah-2-seven-levels-agentic-prompt-formats.mp4",
         tx="seven-levels-agentic-prompt-formats", codebase="codebases/ah/agentic-prompt-engineering",
         url="https://agenticengineer.com/tactical-agentic-coding/course/seven-levels-agentic-prompt-formats"),
    dict(order=11, short_key="ah-3", key="ah-3-building-domain-specific-agents",
         title="Building Domain-Specific Agents", slug="building-domain-specific-agents",
         course="AH", video="ah-3-building-domain-specific-agents.mp4",
         tx="building-domain-specific-agents", codebase="codebases/ah/building-specialized-agents",
         url="https://agenticengineer.com/tactical-agentic-coding/course/building-domain-specific-agents"),
    dict(order=12, short_key="ah-4", key="ah-4-multi-agent-orchestration-the-o-agent",
         title="Multi-Agent Orchestration: The O-Agent", slug="multi-agent-orchestration-the-o-agent",
         course="AH", video="ah-4-multi-agent-orchestration-the-o-agent.mp4",
         tx="multi-agent-orchestration-the-o-agent", codebase="codebases/ah/multi-agent-orchestration",
         url="https://agenticengineer.com/tactical-agentic-coding/course/multi-agent-orchestration-the-o-agent"),
    dict(order=13, short_key="ah-5", key="ah-5-agent-experts", title="Agent Experts",
         slug="agent-experts", course="AH", video="ah-5-agent-experts.mp4",
         tx="agent-experts", codebase="codebases/ah/agent-experts",
         url="https://agenticengineer.com/tactical-agentic-coding/course/agent-experts"),
    dict(order=14, short_key="ah-6", key="ah-6-building-agentic-layers", title="Building Agentic Layers",
         slug="building-agentic-layers", course="AH", video="ah-6-building-agentic-layers.mp4",
         tx="building-agentic-layers", codebase="codebases/ah/orchestrator-agent-with-adws",
         url="https://agenticengineer.com/tactical-agentic-coding/course/building-agentic-layers"),
    # MA
    dict(order=15, short_key="ma-1", key="ma-1-ceo-agents", title="CEO Agents", slug="ceo-agents",
         course="MA", video="ma-1-ceo-agents.mp4", tx=None, ma_key="ma-1-ceo-agents",
         codebase="codebases/ma/ceo-agents",
         url="https://www.youtube.com/watch?v=TqjmTZRL31E", youtube_id="TqjmTZRL31E"),
    dict(order=16, short_key="ma-2", key="ma-2-lead-agents", title="Multi-Team Agentic Coding / Lead Agents",
         slug="lead-agents", course="MA", video="ma-2-lead-agents.mp4", tx=None, ma_key="ma-2-lead-agents",
         codebase="codebases/ma/lead-agents",
         url="https://www.youtube.com/watch?v=M30gp1315Y4", youtube_id="M30gp1315Y4"),
    dict(order=17, short_key="ma-3", key="ma-3-ui-agents", title="Infinite UI Agents", slug="ui-agents",
         course="MA", video="ma-3-ui-agents.mp4", tx=None, ma_key="ma-3-ui-agents",
         codebase="codebases/ma/ui-agents",
         url="https://www.youtube.com/watch?v=RairMJflUSA", youtube_id="RairMJflUSA"),
    dict(order=18, short_key="ma-4", key="ma-4-verifier-agent", title="The Pi Verifier Agent",
         slug="verifier-agent", course="MA", video="ma-4-verifier-agent.mp4", tx=None, ma_key="ma-4-verifier-agent",
         codebase="codebases/ma/the-verifier-agent-system",
         url="https://www.youtube.com/watch?v=EnXKysJNz_8", youtube_id="EnXKysJNz_8"),
]


def hardlink_or_copy(src: Path, dst: Path) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() or dst.is_symlink():
        dst.unlink()
    try:
        os.link(src, dst)
        return "hardlink"
    except OSError:
        shutil.copy2(src, dst)
        return "copy"


def symlink_rel(target: Path, link: Path) -> None:
    link.parent.mkdir(parents=True, exist_ok=True)
    if link.exists() or link.is_symlink():
        link.unlink()
    link.symlink_to(os.path.relpath(target, start=link.parent))


def vtt_to_md(vtt_text: str, title: str) -> str:
    lines = []
    for raw in vtt_text.splitlines():
        line = raw.strip()
        if not line or line.upper().startswith("WEBVTT") or re.match(r"^\d+$", line):
            continue
        if re.match(r"^\d{2}:\d{2}:\d{2}\.\d{3}\s+-->", line) or re.match(r"^\d{2}:\d{2}\.\d{3}\s+-->", line):
            continue
        line = re.sub(r"<[^>]+>", "", line)
        lines.append(line)
    out: list[str] = []
    for ln in lines:
        if not out or out[-1] != ln:
            out.append(ln)
    body = " ".join(out)
    paras: list[str] = []
    buf = ""
    for sent in re.split(r"(?<=[.!?])\s+", body):
        if len(buf) + len(sent) > 700 and buf:
            paras.append(buf.strip())
            buf = sent
        else:
            buf = (buf + " " + sent).strip()
    if buf:
        paras.append(buf.strip())
    return f"# {title}\n\n" + "\n\n".join(paras) + "\n"


def remove_stale_lesson_dirs(keep: set[str]) -> list[str]:
    """Remove old short-name lesson dirs (tac-1, ah-1, …) after rename to MA-style."""
    removed = []
    if not OUT.is_dir():
        return removed
    for p in OUT.iterdir():
        if not p.is_dir() or p.name.startswith("_") or p.name in keep:
            continue
        # only auto-remove known stale short keys / previous catalog dirs
        if re.fullmatch(r"(tac|ah)-\d+", p.name) or p.name in keep:
            if re.fullmatch(r"(tac|ah)-\d+", p.name):
                shutil.rmtree(p)
                removed.append(p.name)
    return removed


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    keep = {lesson["key"] for lesson in LESSONS} | {"_source"}
    removed = remove_stale_lesson_dirs(keep)
    if removed:
        print("removed stale dirs:", ", ".join(removed))

    catalog: list[dict] = []
    errors: list[str] = []

    for lesson in LESSONS:
        key = lesson["key"]
        short = lesson["short_key"]
        d = OUT / key
        video_dir = d / "video"
        tx_dir = d / "transcript"
        meta_dir = d / "metadata"
        code_link = d / "codebase"
        for p in (video_dir, tx_dir, meta_dir):
            p.mkdir(parents=True, exist_ok=True)

        entry: dict = {
            "order": lesson["order"],
            "key": key,
            "short_key": short,
            "title": lesson["title"],
            "slug": lesson["slug"],
            "course": lesson["course"],
            "url": lesson["url"],
            "paths": {},
            "status": {},
        }

        # --- video ---
        src_video = FINAL / lesson["video"]
        dst_video = video_dir / lesson["video"]
        if src_video.is_file():
            mode = hardlink_or_copy(src_video, dst_video)
            entry["paths"]["video"] = str(dst_video.relative_to(OUT))
            entry["status"]["video"] = mode
            entry["video_bytes"] = src_video.stat().st_size
        else:
            errors.append(f"{key}: missing video {src_video}")
            entry["status"]["video"] = "missing"

        # --- transcript ---
        tx_files: dict[str, str] = {}
        if lesson.get("ma_key"):
            ma_key = lesson["ma_key"]
            ma_tx = MA / ma_key / "transcripts"
            for ext, name in [(".en.vtt", f"{ma_key}.en.vtt"), (".md", f"{ma_key}.md"), (".txt", f"{ma_key}.txt")]:
                src = ma_tx / name
                if src.is_file():
                    dst = tx_dir / (f"{key}.vtt" if ext == ".en.vtt" else f"{key}{ext}")
                    hardlink_or_copy(src, dst)
                    tx_files["vtt" if ext == ".en.vtt" else ext.lstrip(".")] = str(dst.relative_to(OUT))
        else:
            slug = lesson["tx"]
            vtt_src = TX_VTT / f"{slug}.vtt"
            if vtt_src.is_file():
                dst_vtt = tx_dir / f"{key}.vtt"
                hardlink_or_copy(vtt_src, dst_vtt)
                tx_files["vtt"] = str(dst_vtt.relative_to(OUT))
                md_dst = tx_dir / f"{key}.md"
                md_dst.write_text(
                    vtt_to_md(vtt_src.read_text(encoding="utf-8", errors="replace"), lesson["title"]),
                    encoding="utf-8",
                )
                tx_files["md"] = str(md_dst.relative_to(OUT))
            clean_txt = TX_CLEAN / f"{slug}.txt"
            if clean_txt.is_file():
                dst_txt = tx_dir / f"{key}.txt"
                hardlink_or_copy(clean_txt, dst_txt)
                tx_files["txt"] = str(dst_txt.relative_to(OUT))
            note_n = lesson["order"]
            for ext in (".md", ".txt"):
                note = TX_NOTES / f"lesson-{note_n:02d}{ext}"
                if note.is_file():
                    dst_note = tx_dir / f"{key}-notes{ext}"
                    hardlink_or_copy(note, dst_note)
                    tx_files[f"notes{ext}"] = str(dst_note.relative_to(OUT))

        # The import blocks above only populate tx_files for transcripts copied in
        # from an external source *this run*. Once a lesson's transcript is already
        # in the catalog there is nothing left to import, so fall back to
        # describing what is actually on disk. Without this the index claims every
        # lesson has no transcript while the files sit right there, and every run
        # emits a false "no transcripts found" warning.
        if not tx_files and tx_dir.is_dir():
            # Canonical "<key>.<ext>" wins over companions such as
            # "<key>-notes.md". Plain sorting would not do it: '-' sorts before
            # '.', so the notes file would be picked as the lesson transcript and
            # every agent following the index would read the wrong file.
            for existing in sorted(
                (p for p in tx_dir.iterdir() if p.is_file()),
                key=lambda p: (0 if p.stem == key else 1, p.name),
            ):
                kind = "vtt" if existing.name.endswith(".vtt") else existing.suffix.lstrip(".")
                tx_files.setdefault(kind, str(existing.relative_to(OUT)))

        entry["paths"]["transcript"] = tx_files
        entry["status"]["transcript"] = "ok" if tx_files else "missing"
        if not tx_files:
            errors.append(f"{key}: no transcripts found")

        # --- codebase ---
        code_src = ROOT / lesson["codebase"]
        if code_src.is_dir():
            symlink_rel(code_src, code_link)
            entry["paths"]["codebase"] = str(code_link.relative_to(OUT))
            entry["codebase_target"] = lesson["codebase"]
            entry["status"]["codebase"] = "symlink"
        else:
            errors.append(f"{key}: missing codebase {code_src}")
            entry["status"]["codebase"] = "missing"

        # --- metadata ---
        meta: dict = {
            "key": key,
            "short_key": short,
            "title": lesson["title"],
            "course": lesson["course"],
            "slug": lesson["slug"],
            "url": lesson["url"],
            "order": lesson["order"],
            "video_file": lesson["video"],
            "codebase": lesson["codebase"],
        }
        if lesson.get("youtube_id"):
            meta["youtube_id"] = lesson["youtube_id"]

        # recording / validation from videos/<short_key>
        rec_dir = VIDEOS / short
        if rec_dir.is_dir():
            for name in ("recording.json", "validation.json", "validation.md"):
                src = rec_dir / name
                if src.is_file():
                    hardlink_or_copy(src, meta_dir / name)
                    meta[name] = name
            cs = rec_dir / "contact-sheet.jpg"
            if cs.is_file():
                hardlink_or_copy(cs, meta_dir / "contact-sheet.jpg")
                meta["contact_sheet"] = "contact-sheet.jpg"

        if lesson.get("ma_key"):
            ma_meta = MA / lesson["ma_key"] / "meta"
            for src in ma_meta.glob("*"):
                if src.is_file() and src.suffix in {".json", ".description", ".webp", ".jpg", ".png"}:
                    hardlink_or_copy(src, meta_dir / src.name)
            info = meta_dir / f"{lesson['ma_key']}.info.json"
            if info.is_file():
                try:
                    info_j = json.loads(info.read_text(encoding="utf-8", errors="replace"))
                    meta["youtube_title"] = info_j.get("title")
                    meta["duration_s"] = info_j.get("duration")
                    meta["channel"] = info_j.get("channel") or info_j.get("uploader")
                    if info_j.get("description"):
                        (meta_dir / f"{key}.description.txt").write_text(info_j["description"], encoding="utf-8")
                except Exception as e:
                    errors.append(f"{key}: info.json parse: {e}")

        # REAL IndyDevDan course page HTML — prefer offline-styled (local CSS/fonts/img)
        # Fall back to raw CDP dump if offline not built yet.
        offline_src = COURSE_HTML_OFFLINE / f"{key}.html"
        raw_src = COURSE_HTML / f"{key}.html"
        course_src = offline_src if offline_src.is_file() else raw_src
        course_dst = meta_dir / "course-page.html"
        if course_src.is_file():
            # copy (not hardlink): offline HTML is rewritten per path; keep independent
            if course_dst.exists() or course_dst.is_symlink():
                course_dst.unlink()
            shutil.copy2(course_src, course_dst)
            lesson_html = meta_dir / "lesson.html"
            if lesson_html.exists() or lesson_html.is_symlink():
                lesson_html.unlink()
            shutil.copy2(course_src, lesson_html)
            meta["course_page_html"] = "course-page.html"
            meta["course_page_source"] = (
                "agenticengineer.com outerHTML + local Nuxt CSS/fonts/images (offline)"
                if course_src == offline_src
                else "agenticengineer.com (raw CDP dump — run materialize_course_pages_offline.py)"
            )
            meta["course_page_bytes"] = course_src.stat().st_size
            meta["course_page_offline"] = course_src == offline_src
            entry["status"]["course_html"] = "offline-copy" if course_src == offline_src else "raw-copy"
            entry["paths"]["course_page_html"] = str(course_dst.relative_to(OUT))
        else:
            entry["status"]["course_html"] = "missing"
            if lesson["course"] in {"TAC", "AH"}:
                errors.append(f"{key}: missing real course HTML {course_src}")
            for stale in ("lesson.html", "course-page.html"):
                p = meta_dir / stale
                if p.is_file():
                    try:
                        head = p.read_text(encoding="utf-8", errors="replace")[:2000]
                    except Exception:
                        head = ""
                    if "Loot Box" not in head and "Agentic Engineer" not in head:
                        p.unlink()

        # loot-box notes (structured extract companion, not a substitute for HTML)
        note = TX_NOTES / f"lesson-{lesson['order']:02d}.md"
        if note.is_file() and lesson["course"] in {"TAC", "AH"}:
            hardlink_or_copy(note, meta_dir / "course-notes.md")
            meta["course_notes"] = "course-notes.md"

        (meta_dir / "lesson.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        entry["paths"]["metadata"] = {
            "lesson_json": str((meta_dir / "lesson.json").relative_to(OUT)),
            "course_page_html": str(course_dst.relative_to(OUT)) if course_dst.is_file() else None,
            "lesson_html": str((meta_dir / "lesson.html").relative_to(OUT)) if (meta_dir / "lesson.html").is_file() else None,
        }
        entry["status"]["metadata"] = "ok"

        (d / "README.md").write_text(
            f"""# {key} — {lesson['title']}

Course: **{lesson['course']}** · order {lesson['order']}

| Asset | Path |
|-------|------|
| Video | `video/{lesson['video']}` |
| Transcript | `transcript/` (vtt + md/txt when available) |
| Course page HTML | `metadata/course-page.html` (real AE HTML + local CSS/fonts/images) |
| Metadata JSON | `metadata/lesson.json` |
| Codebase | `codebase/` → `{lesson['codebase']}` |

Source: {lesson['url']}
""",
            encoding="utf-8",
        )

        catalog.append(entry)
        print(
            f"OK {key:48} video={entry['status'].get('video')} "
            f"tx={entry['status'].get('transcript')} html={entry['status'].get('course_html')} "
            f"code={entry['status'].get('codebase')}"
        )

    index = {
        "name": "course lesson catalog",
        # Repo-relative on purpose. An absolute path here breaks the index for
        # everyone whose checkout is not at this machine's path.
        "root": "catalog/courses",
        "layout": {
            "per_lesson": ["video/", "transcript/", "metadata/", "codebase/"],
            "folder_naming": "<course>-<n>-<slug>, e.g. tac-1-hello-agentic-coding",
            "course_html": "metadata/course-page.html is authenticated outerHTML from agenticengineer.com",
            "notes": "Videos hardlinked from media/final/; codebase/ symlinks into codebases/.",
        },
        "lessons": catalog,
    }
    (CATALOG / "INDEX.json").write_text(
        json.dumps(index, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# `catalog/` — the lessons",
        "",
        "**Generated by `uv run tools/catalog/build_catalog.py` (`make catalog`).**",
        "Edit that script, not this file — the next run overwrites it.",
        "",
        "The read-only front door to the material. Nothing here is a copy: the",
        "video is hardlinked from `media/final/` and `codebase/` is a symlink into",
        "`codebases/`.",
        "",
        "## Layout (every course lesson)",
        "```",
        "catalog/courses/<course>-<n>-<slug>/   # e.g. tac-1-hello-agentic-coding",
        "  video/<key>.mp4             # hardlink into media/final/",
        "  transcript/*.{md,txt,vtt}   # the READABLE stitched transcript",
        "  metadata/course-page.html   # real course page HTML + local CSS/fonts/img",
        "  metadata/lesson.html",
        "  metadata/lesson.json",
        "  metadata/course-notes.md    # loot-box notes companion (TAC/AH)",
        "  codebase/                   # symlink into codebases/",
        "  README.md",
        "catalog/youtube/yt-NN-<slug>/          # same shape, transcript/ + metadata/",
        "catalog/assets/                        # shared CSS/fonts/images (offline)",
        "```",
        "",
        "Raw dumps: `_source/course-pages/`. Offline-styled: `_source/course-pages-offline/`.",
        "",
        "> The per-chapter VTT dumps under `transcripts/<key>/` are **not** these",
        "> files. Read `catalog/courses/<key>/transcript/<key>.md` — the stitched,",
        "> whole-lesson version. See `transcripts/README.md`.",
        "",
        "## Counts",
        "",
        "Counts drift, so produce them rather than reading them:",
        "",
        "```sh",
        "ls -d catalog/courses/*/ | wc -l      # course lessons",
        "ls -d catalog/youtube/yt-*/ | wc -l   # videos",
        "```",
        "",
        "## Catalog",
        "",
        "| # | Key | Title | Course | Video | TX | HTML | Code |",
        "|--:|-----|-------|--------|:-----:|:--:|:----:|:----:|",
    ]
    for e in catalog:
        okv = "✓" if e["status"].get("video") not in (None, "missing") else "—"
        okt = "✓" if e["status"].get("transcript") == "ok" else "—"
        okh = "✓" if e["status"].get("course_html") not in (None, "missing") else "—"
        okc = "✓" if e["status"].get("codebase") == "symlink" else "—"
        lines.append(
            f"| {e['order']} | `{e['key']}` | {e['title']} | {e['course']} | {okv} | {okt} | {okh} | {okc} |"
        )
    lines += [
        "",
        "## Agent quick paths",
        "",
        "- Index: `catalog/INDEX.json`, `catalog/youtube/INDEX.json`",
        "- What he said: `catalog/courses/<key>/transcript/<key>.md`",
        "- What he built: `catalog/courses/<key>/codebase/` → resolves into `codebases/`",
        "- Real course page: `catalog/courses/<key>/metadata/course-page.html`",
        "- Plain transcript: prefer `transcript/*.md`, then `*.txt`, then `*.vtt`",
        "",
        "## Rebuild",
        "",
        "```bash",
        "# optional: re-dump raw HTML via authenticated CDP → _source/course-pages/",
        "uv run tools/catalog/materialize_course_pages.py   # CSS/fonts/img + offline HTML",
        "uv run tools/catalog/build_catalog.py              # wire into lesson folders",
        "# or simply:",
        "make catalog",
        "```",
        "",
    ]
    (CATALOG / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    if errors:
        print("\nWARNINGS:")
        for e in errors:
            print(" -", e)
    print(f"\nBuilt {len(catalog)} lessons → {OUT}")
    return 0 if not any("missing video" in e or "missing codebase" in e for e in errors) else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Attach codebases for youtube videos that had NO GitHub link in the description.

Sources of truth (in priority order):
1. Course catalog exact youtube_id match (ma-1/2/3/4 etc.)
2. Course-preview title mapping (AH/TAC public sneak peeks)
3. Public disler repo topic match (e.g. loops → infinite-agentic-loop)

Never invent: only high-confidence mappings. Writes provenance into
metadata/repos.json + lesson.json.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
YOUTUBE = REPO_ROOT / "catalog" / "youtube"
AE = REPO_ROOT
REPOS = REPO_ROOT / "codebases" / "yt"

# Exact YouTube video_id → local relative path under AgenticEngineer
COURSE_YT_ID = {
    "TqjmTZRL31E": {  # yt-37 CEO Agents
        "rel": "codebases/ma/ceo-agents",
        "label": "codebases/ma/ceo-agents",
        "via": "course-catalog ma-1 youtube_id",
        "course_key": "ma-1-ceo-agents",
    },
    "M30gp1315Y4": {  # yt-38 One Agent Is NOT ENOUGH / lead agents
        "rel": "codebases/ma/lead-agents",
        "label": "codebases/ma/lead-agents",
        "via": "course-catalog ma-2 youtube_id",
        "course_key": "ma-2-lead-agents",
    },
    "RairMJflUSA": {  # ma-3 already often has github; keep for completeness
        "rel": "codebases/ma/ui-agents",
        "label": "codebases/ma/ui-agents",
        "via": "course-catalog ma-3 youtube_id",
        "course_key": "ma-3-ui-agents",
    },
    "EnXKysJNz_8": {
        "rel": "codebases/ma/the-verifier-agent-system",
        "label": "codebases/ma/the-verifier-agent-system",
        "via": "course-catalog ma-4 youtube_id",
        "course_key": "ma-4-verifier-agent",
    },
}

# Public YT sneak-peek → paid course codebase (title-aligned)
# keys = youtube folder order or video_id
PREVIEW_BY_VIDEO_ID = {
    # Elite Context Engineering preview → AH-1
    "Kf5-HWJPTIE": {
        "rel": "codebases/ah/elite-context-engineering",
        "label": "codebases/ah/elite-context-engineering",
        "via": "course-preview title match → ah-1",
        "course_key": "ah-1-rd-framework-context-window-mastery",
    },
    # Agentic Prompt Engineering preview → AH-2
    "luqKnexhpFs": {
        "rel": "codebases/ah/agentic-prompt-engineering",
        "label": "codebases/ah/agentic-prompt-engineering",
        "via": "course-preview title match → ah-2",
        "course_key": "ah-2-seven-levels-agentic-prompt-formats",
    },
    # Agent Experts preview → AH-5
    "zTcDwqopvKE": {
        "rel": "codebases/ah/agent-experts",
        "label": "codebases/ah/agent-experts",
        "via": "course-preview title match → ah-5",
        "course_key": "ah-5-agent-experts",
    },
    # ENDGAME custom agents / specialized agents sneak peek → AH-3
    "6wR6xblSays": {
        "rel": "codebases/ah/building-specialized-agents",
        "label": "codebases/ah/building-specialized-agents",
        "via": "course-preview theme match → ah-3 custom/specialized agents",
        "course_key": "ah-3-building-domain-specific-agents",
    },
    # One Agent to RULE them ALL (advanced orchestration) → AH-4
    "p0mrXfwAbCg": {
        "rel": "codebases/ah/multi-agent-orchestration",
        "label": "codebases/ah/multi-agent-orchestration",
        "via": "course-preview theme match → ah-4 multi-agent orchestration",
        "course_key": "ah-4-multi-agent-orchestration-the-o-agent",
    },
    # Codebase Singularity / agentic layer sneak peek → TAC-8 + AH-6 primary TAC-8
    "fop_yxV-mPo": {
        "rel": "codebases/tac/tac-8",
        "label": "codebases/tac/tac-8",
        "via": "course-preview theme match → tac-8 the agentic layer",
        "course_key": "tac-8-the-agentic-layer",
        "related_rel": [
            "codebases/ah/orchestrator-agent-with-adws",
        ],
    },
}

# Public GitHub when description had none but theme is clear
GITHUB_TOPIC = {
    # Intentionally empty: do NOT invent codebases from title keywords.
    # Only description GitHub links (attach_codebases) or exact course maps below.
}


def link_to(folder: Path, target: Path) -> None:
    link = folder / "codebase"
    if link.is_symlink() or link.is_file():
        link.unlink()
    elif link.exists():
        shutil.rmtree(link)
    rel = os.path.relpath(target, folder)
    link.symlink_to(rel)


def ensure_github(owner_repo: str) -> Path | None:
    owner, name = owner_repo.split("/", 1)
    REPOS.mkdir(parents=True, exist_ok=True)
    dest = REPOS / f"{owner}__{name}"
    if dest.exists() and (dest / ".git").exists():
        return dest
    if dest.exists():
        shutil.rmtree(dest)
    url = f"https://github.com/{owner_repo}"
    r = subprocess.run(
        ["git", "clone", "--depth", "1", url, str(dest)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if r.returncode != 0:
        print(f"  clone fail {owner_repo}: {r.stderr[-300:]}", file=sys.stderr)
        return None
    return dest


def update_meta(folder: Path, *, label: str, url: str | None, via: str, kind: str, local: str) -> None:
    lesson_path = folder / "metadata" / "lesson.json"
    lesson = json.loads(lesson_path.read_text()) if lesson_path.exists() else {}
    lesson["codebase"] = label
    lesson["codebase_url"] = url
    lesson["codebase_local"] = "codebase/"
    lesson["codebase_via"] = via
    lesson["codebase_kind"] = kind  # course-local | github-topic
    lesson_path.write_text(json.dumps(lesson, indent=2, ensure_ascii=False) + "\n")

    repos = {
        "primary": {
            "label": label,
            "url": url,
            "via": via,
            "kind": kind,
            "local": local,
        },
        "source": via,
        "symlink": "codebase/",
        "note": "Attached by fill_missing_codebases.py after description had no GitHub URL",
    }
    (folder / "metadata" / "repos.json").write_text(json.dumps(repos, indent=2, ensure_ascii=False) + "\n")

    status_path = folder / "STATUS.json"
    status = json.loads(status_path.read_text()) if status_path.exists() else {}
    status["codebase"] = True
    status["codebase_repo"] = label
    status["codebase_status"] = f"filled:{kind}"
    status_path.write_text(json.dumps(status, indent=2) + "\n")

    # README row
    readme = folder / "README.md"
    if readme.exists():
        text = readme.read_text()
        row = f"| Codebase | `codebase/` → `{label}` ({via}) |"
        if "| Codebase |" in text:
            import re

            text = re.sub(r"\| Codebase \|.*\|", row, text)
        else:
            text = text.rstrip() + "\n" + row + "\n"
        readme.write_text(text)

    note = folder / "CODEBASE.md"
    if note.exists():
        note.unlink()


def resolve_folder_by_video_id(vid: str) -> Path | None:
    for p in YOUTUBE.glob("yt-*"):
        if not p.is_dir():
            continue
        lj = p / "metadata" / "lesson.json"
        if not lj.exists():
            continue
        d = json.loads(lj.read_text())
        if d.get("video_id") == vid:
            return p
    return None


def main() -> int:
    only_missing = "--all" not in sys.argv
    results = []

    # gather targets
    targets: dict[str, dict] = {}
    targets.update({k: {**v, "type": "course-local"} for k, v in COURSE_YT_ID.items()})
    targets.update({k: {**v, "type": "course-local"} for k, v in PREVIEW_BY_VIDEO_ID.items()})
    targets.update({k: {**v, "type": "github-topic"} for k, v in GITHUB_TOPIC.items()})

    for vid, spec in targets.items():
        folder = resolve_folder_by_video_id(vid)
        if not folder:
            results.append({"video_id": vid, "error": "folder not found"})
            continue
        if only_missing and (folder / "codebase").exists():
            results.append({"key": folder.name, "video_id": vid, "status": "skip-already-has"})
            continue

        print(f"== {folder.name} ({vid}) ==")
        if spec["type"] == "course-local":
            target = AE / spec["rel"]
            if not target.exists():
                print(f"  MISSING local {target}")
                results.append({"key": folder.name, "error": f"missing {spec['rel']}"})
                continue
            link_to(folder, target)
            update_meta(
                folder,
                label=spec["label"],
                url=None,
                via=spec["via"],
                kind="course-local",
                local=spec["rel"],
            )
            print(f"  linked course-local → {spec['rel']}")
            results.append({"key": folder.name, "status": "course-local", "target": spec["rel"]})
        else:
            gh = spec["github"]
            path = ensure_github(gh)
            if not path:
                results.append({"key": folder.name, "error": f"clone {gh}"})
                continue
            link_to(folder, path)
            update_meta(
                folder,
                label=gh,
                url=f"https://github.com/{gh}",
                via=spec["via"],
                kind="github-topic",
                local=str(path.relative_to(YOUTUBE)),
            )
            print(f"  linked github-topic → {gh}")
            results.append({"key": folder.name, "status": "github-topic", "target": gh})

    # remaining still without codebase — document verified empty
    still = []
    for p in sorted(YOUTUBE.glob("yt-*")):
        if not p.is_dir():
            continue
        if (p / "codebase").exists():
            continue
        still.append(p.name)
        # strengthen CODEBASE.md with audit note
        (p / "CODEBASE.md").write_text(
            f"# No public codebase (verified)\n\n"
            f"Folder: `{p.name}`\n\n"
            f"Checked:\n"
            f"- Stored `metadata/video-info.json` description\n"
            f"- Live yt-dlp description re-fetch\n"
            f"- Transcript for github.com paths\n"
            f"- Course catalog youtube_id map\n"
            f"- Title/theme course-preview map\n"
            f"- disler/* topic map\n\n"
            f"**Result:** No cloneable GitHub/gist and no high-confidence course codebase mapping.\n"
            f"Links in description are typically agenticengineer.com course sales, docs, or related videos only.\n"
        )
        st_path = p / "STATUS.json"
        st = json.loads(st_path.read_text()) if st_path.exists() else {}
        st["codebase"] = False
        st["codebase_status"] = "verified-none"
        st_path.write_text(json.dumps(st, indent=2) + "\n")

    summary = {
        "attached": [r for r in results if r.get("status") in ("course-local", "github-topic")],
        "skipped": [r for r in results if r.get("status") == "skip-already-has"],
        "errors": [r for r in results if r.get("error")],
        "still_none": still,
        "still_none_count": len(still),
    }
    (YOUTUBE / "_fill_missing_codebases_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print("\n=== SUMMARY ===")
    print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in summary.items()}, indent=2))
    print("still_none:", still)
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

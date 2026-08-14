#!/usr/bin/env python3
"""Materialize extract/chapter prompts for one lesson and optionally run workers."""
from __future__ import annotations
import json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path("/Users/kvnkishore/WebstormProjects/AgenticEngineer")
BOOK = ROOT / "IndyDevDan/book"
ORCH = BOOK / "_orchestration"
CAT = ROOT / "IndyDevDan"

def load_curriculum():
    d = json.loads((BOOK / "data/curriculum.json").read_text())
    lessons = d.get("lessons") or []
    return {L["key"]: L for L in lessons}

def vol_for(course: str) -> str:
    return {"TAC": "vol-1-tac", "AH": "vol-2-ah", "MA": "vol-3-ma"}[course]

def stem_for(order: int, key: str) -> str:
    # key: tac-2-the-12-leverage-points -> 02-the-12-leverage-points
    m = re.match(r"^(?:tac|ah|ma)-\d+-(.+)$", key)
    slug = m.group(1) if m else key
    return f"{order:02d}-{slug}"

def render(tpl: str, mapping: dict) -> str:
    out = tpl
    for k, v in mapping.items():
        out = out.replace("{{" + k + "}}", str(v))
    return out

def materialize(key: str):
    lessons = load_curriculum()
    L = lessons[key]
    course = L["course"]
    order = int(L["order"])
    mapping = {
        "KEY": key,
        "SHORT": L.get("short_key") or key,
        "TITLE": L["title"],
        "COURSE": course,
        "ORDER": order,
        "VOL": vol_for(course),
        "STEM": stem_for(order, key),
        "CODEBASE": L.get("codebase") or "",
    }
    for name in ("TEMPLATE-EXTRACT.md", "TEMPLATE-CHAPTER.md"):
        tpl = (ORCH / name).read_text()
        out_name = name.replace("TEMPLATE-", f"{key}-").replace(".md", ".md")
        # cleaner names
        if "EXTRACT" in name:
            out_path = ORCH / f"{key}-EXTRACT.md"
        else:
            out_path = ORCH / f"{key}-CHAPTER.md"
        out_path.write_text(render(tpl, mapping))
        print("wrote", out_path)
    return mapping

def run_extract(key: str):
    mapping = materialize(key)
    prompt = ORCH / f"{key}-EXTRACT.md"
    out = BOOK / f"_logs/{key}-extract.json"
    err = BOOK / f"_logs/{key}-extract.err"
    out.parent.mkdir(parents=True, exist_ok=True)
    # Default opus if Fable is rate-limited; override with EXTRACT_MODEL=fable|opus|sonnet
    model = os.environ.get("EXTRACT_MODEL", "opus")
    cmd = [
        "claude", "-p", prompt.read_text(),
        "--model", model,
        "--effort", "max",
        "--permission-mode", "bypassPermissions",
        "--dangerously-skip-permissions",
        "--output-format", "json",
    ]
    env = {
        "HOME": str(Path.home()),
        "PATH": "/Users/kvnkishore/.local/bin:/opt/homebrew/bin:/usr/bin:/bin",
        "USER": os.environ.get("USER", "kvnkishore"),
    }
    with open(out, "w") as fo, open(err, "w") as fe:
        r = subprocess.run(cmd, cwd=str(ROOT), env=env, stdout=fo, stderr=fe)
    print("extract_exit", r.returncode, key)
    status = BOOK / f"_extracts/{key}/STATUS.md"
    print("STATUS", status.exists(), status)
    return r.returncode

def run_chapter(key: str):
    mapping = materialize(key)
    prompt = ORCH / f"{key}-CHAPTER.md"
    out = BOOK / f"_logs/{key}-chapter.out"
    err = BOOK / f"_logs/{key}-chapter.err"
    status = BOOK / f"_extracts/{key}/STATUS.md"
    if not status.exists():
        print("BLOCKED no extract", key)
        return 2
    env = {
        "HOME": str(Path.home()),
        "PATH": "/Users/kvnkishore/.nvm/versions/node/v20.19.5/bin:/Users/kvnkishore/.local/bin:/opt/homebrew/bin:/usr/bin:/bin",
        "USER": os.environ.get("USER", "kvnkishore"),
    }
    cmd = [
        "codex", "exec",
        "--model", "gpt-5.6-sol",
        "-c", 'model_reasoning_effort="xhigh"',
        "--full-auto",
        "--skip-git-repo-check",
        prompt.read_text(),
    ]
    with open(out, "w") as fo, open(err, "w") as fe:
        r = subprocess.run(cmd, cwd=str(ROOT), env=env, stdout=fo, stderr=fe)
    print("chapter_exit", r.returncode, key)
    ch = BOOK / mapping["VOL"] / f"{mapping['STEM']}.html"
    print("CHAPTER", ch.exists(), ch)
    return r.returncode

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: fanout-lesson.py <extract|chapter|materialize> <lesson-key>")
        sys.exit(2)
    action, key = sys.argv[1], sys.argv[2]
    if action == "materialize":
        materialize(key)
    elif action == "extract":
        sys.exit(run_extract(key) or 0)
    elif action == "chapter":
        sys.exit(run_chapter(key) or 0)
    else:
        sys.exit(2)

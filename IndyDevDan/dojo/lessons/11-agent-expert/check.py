#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Closed-loop validator for 11 agent-expert. Deterministic, offline, stdlib only.

Validates the expert's three artifacts: expertise.yaml is a real mental model
of sample_app (structure + true conventions, parsed with stdlib line-parsing —
no yaml import needed), question.md reuses then verifies then cites, and
self-improve.md learns surgically after every task.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LESSON = "11 agent-expert"
EXPERTISE = HERE / "experts" / "database" / "expertise.yaml"
QUESTION = HERE / "experts" / "database" / "question.md"
IMPROVE = HERE / "experts" / "database" / "self-improve.md"


def scan_blanks() -> list[str]:
    """Step zero: no ____ may remain in the starter files."""
    problems = []
    for p in sorted(HERE.rglob("*")):
        if not p.is_file() or "solution" in p.parts or "__pycache__" in p.parts:
            continue
        if p.name in ("check.py", "hints.md", "README.md"):
            continue
        try:
            n = p.read_text(encoding="utf-8").count("____")
        except (UnicodeDecodeError, OSError):
            continue
        if n:
            problems.append(f"{p.relative_to(HERE)} still has {n} blank(s) — fill every ____ (see the YOUR TURN comments)")
    return problems


def parse_yaml_blocks(text: str) -> dict[str, dict]:
    """Minimal stdlib line-parser: top-level 'key:' -> value + indented lines."""
    blocks: dict[str, dict] = {}
    current = None
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):(.*)$", raw)
        if m and not raw[0].isspace():
            current = m.group(1)
            blocks[current] = {"value": m.group(2).split("#")[0].strip(), "lines": []}
        elif current is not None:
            blocks[current]["lines"].append(stripped)
    return blocks


def list_items(block: dict) -> list[str]:
    return [l[1:].strip() for l in block["lines"] if l.startswith("- ")]


def strip_html_comments(md: str) -> str:
    return re.sub(r"<!--.*?-->", "", md, flags=re.S)


def section(md: str, header: str) -> str | None:
    m = re.search(rf"^##\s+{header}\b(.*?)(?=^##\s|\Z)", md, flags=re.S | re.M)
    return m.group(1) if m else None


def check_expertise() -> list[str]:
    fails = []
    blocks = parse_yaml_blocks(EXPERTISE.read_text(encoding="utf-8"))
    for key in ("purpose", "key_files", "conventions", "never"):
        if key not in blocks:
            fails.append(f"expertise.yaml is missing the top-level key {key}: — the mental model needs all four sections")
    if fails:
        return fails
    if not blocks["purpose"]["value"]:
        fails.append("expertise.yaml purpose: must be a one-line mission — an expert without a purpose is just a memory file")
    paths = [m.group(1).split("#")[0].strip()
             for l in blocks["key_files"]["lines"]
             if (m := re.match(r"-\s*path:\s*(.+)$", l))]
    if len(paths) < 2:
        fails.append("key_files needs at least 2 `- path:` entries — the files the expert reaches for without searching")
    for p in paths:
        if p and not (HERE / p).exists():
            fails.append(f"key_files path {p!r} does not exist — paths are relative to the lesson root (try sample_app/...)")
    conventions = list_items(blocks["conventions"])
    if len(conventions) < 2:
        fails.append("conventions needs at least 2 entries — read sample_app/db.py and write down what is actually true")
    if not any("_execute" in c for c in conventions):
        fails.append("one convention must name the real gateway: every query in sample_app/db.py flows through _execute() — "
                     "false expertise is worse than no expertise")
    never = list_items(blocks["never"])
    if not any("hand-edit" in n.lower() for n in never):
        fails.append("never: needs the guardrail 'hand-edit this file — the agent maintains it' — "
                     "don't update the expertise directly, teach your agent to update it")
    return fails


def check_question() -> list[str]:
    fails = []
    text = strip_html_comments(QUESTION.read_text(encoding="utf-8"))
    wf = section(text, "Workflow")
    if wf is None:
        return ["question.md needs a ## Workflow section — the workflow is the S-tier pillar"]
    m_exp = re.search(r"expertise", wf, re.I)
    m_ver = re.search(r"(verify|validate|confirm|prove|check)[\s\S]{0,120}?(code|source of truth)", wf, re.I)
    m_cite = re.search(r"(file:line|citation|cite)", wf, re.I)
    if not m_exp:
        fails.append("question.md workflow must start from the mental model — read EXPERTISE_FILE before anything else")
    if not m_ver:
        fails.append("question.md workflow is missing the verify step: prove the draft against the actual code before "
                     "reporting — the code is the source of truth, expertise is a lens")
    if not m_cite:
        fails.append("question.md workflow must end by citing file:line evidence for every claim")
    if not fails and not (m_exp.start() < m_ver.start() < m_cite.start()):
        fails.append("question.md workflow order must be: load expertise -> verify against code -> cite file:line")
    return fails


def check_improve() -> list[str]:
    fails = []
    text = strip_html_comments(IMPROVE.read_text(encoding="utf-8"))
    wf = section(text, "Workflow")
    if wf is None:
        return ["self-improve.md needs a ## Workflow section — the learn step lives there"]
    if not re.search(r"(update|append|adjust)[\s\S]{0,80}?(yaml|expertise)", wf, re.I):
        fails.append("self-improve.md workflow must UPDATE the yaml — diff what you learned against EXPERTISE_FILE, "
                     "then append new entries and adjust stale ones")
    if not re.search(r"never[\s\S]{0,60}?(wholesale|rewrite)", wf, re.I):
        fails.append("self-improve.md workflow needs the surgical-changes guardrail — never wholesale rewrite the file; "
                     "Dan wants to see surgical changes")
    if not re.search(r"(after every task|every task|mandatory|no human in the loop)", wf, re.I):
        fails.append("self-improve.md workflow must end by making learning mandatory after every task — "
                     "no human in the loop; experts learn by default")
    return fails


def check_sample_app() -> list[str]:
    """The provided data layer must still behave — the expert's facts depend on it."""
    snippet = (
        "import sys; sys.path.insert(0, '.');"
        "from sample_app import db;"
        "db.connect(':memory:');"
        "db.insert_task('learn act-learn-reuse');"
        "tasks = db.list_tasks();"
        "assert len(tasks) == 1 and tasks[0]['title'] == 'learn act-learn-reuse', tasks;"
        "print('ok')"
    )
    proc = subprocess.run([sys.executable, "-c", snippet], cwd=HERE,
                          capture_output=True, text=True, timeout=15, stdin=subprocess.DEVNULL)
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout).strip().splitlines()[-1:]
        return [f"sample_app/db.py smoke test failed — the provided data layer should stay untouched "
                f"(python3 ../../dojo.py reset 11 restores it): {tail[0] if tail else 'no output'}"]
    return []


def cleanup() -> None:
    shutil.rmtree(HERE / "sample_app" / "__pycache__", ignore_errors=True)
    (HERE / "sample_app" / "tasks.db").unlink(missing_ok=True)


def main() -> None:
    cleanup()
    fails = scan_blanks()
    if not fails:
        try:
            for missing, path in ((EXPERTISE, "experts/database/expertise.yaml"),
                                  (QUESTION, "experts/database/question.md"),
                                  (IMPROVE, "experts/database/self-improve.md")):
                if not missing.exists():
                    fails.append(f"{path} is missing — the expert needs all three artifacts")
            if not fails:
                fails += check_expertise()
                fails += check_question()
                fails += check_improve()
                fails += check_sample_app()
        finally:
            cleanup()
    if fails:
        print(f"❌ FAIL — {LESSON}")
        for i, f in enumerate(fails, 1):
            print(f"  {i}. {f}")
        sys.exit(1)
    print(f"✅ PASS — {LESSON}")
    sys.exit(0)


if __name__ == "__main__":
    main()

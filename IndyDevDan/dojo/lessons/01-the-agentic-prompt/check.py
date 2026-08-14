#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Closed-loop validator for 01 · the-agentic-prompt.

Deterministic, offline, stdlib-only. Never calls an LLM — this check IS the
kind of feedback loop the lesson is teaching you to build.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NN, SLUG = "01", "the-agentic-prompt"
STARTERS = ["prompt.md", "run.sh"]


def strip_comments(md: str) -> str:
    return re.sub(r"<!--.*?-->", "", md, flags=re.S)


def section(md: str, name: str) -> str | None:
    m = re.search(rf"^##\s+{re.escape(name)}\b(.*?)(?=^##\s|\Z)", md, re.M | re.S)
    return m.group(1) if m else None


def finish(fails: list[str]) -> None:
    if fails:
        print(f"❌ FAIL — {NN} {SLUG}")
        for i, msg in enumerate(fails, 1):
            print(f"  {i}. {msg}")
        sys.exit(1)
    print(f"✅ PASS — {NN} {SLUG}")
    sys.exit(0)


def main() -> None:
    fails: list[str] = []

    # Step zero: every ____ must be filled before the real checks run.
    blanks: list[str] = []
    for name in STARTERS:
        path = HERE / name
        if not path.exists():
            fails.append(f"{name} is missing — restore the starter: python3 ../../dojo.py reset {NN}")
            continue
        count = path.read_text(encoding="utf-8").count("____")
        if count:
            blanks.append(f"{name}: {count} blank(s)")
    if blanks:
        fails.append("fill every ____ first — " + "; ".join(blanks))
        finish(fails)
    if fails:
        finish(fails)

    prompt = strip_comments((HERE / "prompt.md").read_text(encoding="utf-8"))

    # The three pillars of an agentic prompt.
    for name, why in (
        ("Purpose", "one agent, one prompt, one purpose"),
        ("Workflow", "the numbered chain of tool calls — the S-tier section"),
        ("Report", "the agent must prove its work"),
    ):
        if section(prompt, name) is None:
            fails.append(f"prompt.md: missing `## {name}` section ({why})")

    purpose = section(prompt, "Purpose") or ""
    if not re.search(r"\w{3,}.+\w{3,}", purpose, re.S):
        fails.append("prompt.md: the Purpose section needs a real one-liner stating the mission")

    workflow = section(prompt, "Workflow") or ""
    steps = re.findall(r"^\s*\d+[.)]\s+\S+", workflow, re.M)
    if len(steps) < 4:
        fails.append(
            f"prompt.md: Workflow has {len(steps)} numbered step(s) — needs at least 4 "
            "(list, group+count, sort, verify)"
        )

    report_sec = section(prompt, "Report") or ""
    if not re.search(r"markdown\s+table", report_sec, re.I):
        fails.append(
            "prompt.md: the Report section must pin the output format — say 'markdown table' "
            "explicitly, with extension and count columns and a total row"
        )

    # run.sh must fire the prompt programmatically.
    run_sh = (HERE / "run.sh").read_text(encoding="utf-8")
    live = [
        line for line in run_sh.splitlines()
        if line.strip() and not line.strip().startswith("#") and "claude -p" in line
    ]
    if not live:
        fails.append(
            "run.sh: no live (non-comment) line invokes `claude -p` — the prompt must run "
            "programmatically; the comment above the blank shows the shape"
        )
    elif not any("prompt.md" in line for line in live):
        fails.append(
            'run.sh: the `claude -p` invocation must be fed prompt.md, e.g. '
            'claude -p "$(cat prompt.md)"'
        )

    if shutil.which("bash"):
        proc = subprocess.run(
            ["bash", "-n", str(HERE / "run.sh")], capture_output=True, text=True, timeout=30
        )
        if proc.returncode != 0:
            detail = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "bash -n failed"
            fails.append(f"run.sh: bash syntax error — {detail}")

    finish(fails)


if __name__ == "__main__":
    main()

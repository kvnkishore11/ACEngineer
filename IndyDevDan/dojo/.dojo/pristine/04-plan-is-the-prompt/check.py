#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Closed-loop validator for 04 plan-is-the-prompt.

Deterministic, offline, stdlib-only. Validates the /chore meta prompt template
and the example plan it must be able to produce. Never calls an LLM.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "04 plan-is-the-prompt"

CHORE = HERE / "commands" / "chore.md"
EXAMPLE = HERE / "specs" / "example-chore-rename-config.md"

# The four required plan sections, as tolerant heading patterns.
SECTIONS = {
    "Chore description": r"^#{1,6}\s*chore\s+description",
    "Relevant files": r"^#{1,6}\s*relevant\s+files",
    "Step-by-step tasks": r"^#{1,6}\s*step[-\s]by[-\s]step\s+tasks",
    "Validation commands": r"^#{1,6}\s*validation\s+commands",
}


def strip_comments(text: str) -> str:
    """Drop HTML comments so YOUR TURN guidance can never satisfy a check."""
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def scan_blanks() -> list[str]:
    hits = []
    for p in sorted(HERE.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(HERE)
        if "solution" in rel.parts or p.name in ("check.py", "README.md", "hints.md"):
            continue
        try:
            n = p.read_text(encoding="utf-8").count("____")
        except (UnicodeDecodeError, OSError):
            continue
        if n:
            hits.append(f"{rel}: {n} blank(s) left — fill every `____` (the YOUR TURN comments say what goes where)")
    return hits


def main() -> int:
    failures: list[str] = []

    blanks = scan_blanks()
    if blanks:
        report(blanks)
        return 1

    if not CHORE.exists():
        report([f"commands/chore.md is missing — the meta prompt template must live at {CHORE.relative_to(HERE)}"])
        return 1
    text = strip_comments(CHORE.read_text(encoding="utf-8"))

    if "$ARGUMENTS" not in text:
        failures.append("commands/chore.md never references $ARGUMENTS — the chore description must flow in through the $ARGUMENTS slot")

    for name, pat in SECTIONS.items():
        if not re.search(pat, text, re.I | re.M):
            failures.append(f"commands/chore.md Plan Format is missing the `## {name}` section — every generated plan needs it")

    if not re.search(r"specs/chore-", text):
        failures.append("commands/chore.md never states the output path convention — plans must be written to `specs/chore-<slug>.md`")

    if not re.search(r"(explore|read)[^\n]{0,140}(before|first)", text, re.I):
        failures.append("commands/chore.md has no read-before-write instruction — tell the agent to explore/read the relevant files BEFORE writing the plan")

    if not EXAMPLE.exists():
        failures.append("specs/example-chore-rename-config.md is missing — the example plan shows the target shape; restore it (just reset 04)")
    else:
        example = strip_comments(EXAMPLE.read_text(encoding="utf-8"))
        for name, pat in SECTIONS.items():
            if not re.search(pat, example, re.I | re.M):
                failures.append(f"specs/example-chore-rename-config.md lost its `## {name}` section — the example must match the Plan Format")

    report(failures)
    return 1 if failures else 0


def report(failures: list[str]) -> None:
    if not failures:
        print(f"✅ PASS — {SLUG}")
        print("   your /chore meta prompt writes closed-loop plans. The plan is the prompt.")
        return
    print(f"❌ FAIL — {SLUG}")
    for i, msg in enumerate(failures, 1):
        print(f"  {i}. {msg}")


if __name__ == "__main__":
    sys.exit(main())

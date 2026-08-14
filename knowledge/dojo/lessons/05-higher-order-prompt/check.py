#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Closed-loop validator for 05 higher-order-prompt.

Deterministic, offline, stdlib-only. Validates the /implement HOP: it must read
the plan first, execute in order, gate on validation, and report as a table.
Never calls an LLM.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "05 higher-order-prompt"

IMPLEMENT = HERE / "commands" / "implement.md"
SAMPLE = HERE / "specs" / "sample-plan.md"

READ_PAT = re.compile(r"read[^\n]{0,100}plan", re.I)
ARGS_PAT = re.compile(r"plan[^\n]{0,100}\$ARGUMENTS|\$ARGUMENTS[^\n]{0,100}plan", re.I)
ORDER_PAT = re.compile(r"in order|one (?:task )?at a time|sequentially", re.I)
VALIDATE_PAT = re.compile(r"(?:every|all|each)[^\n]{0,40}validation command", re.I)
FIX_PAT = re.compile(r"(?:fix|resolve)[^\n]{0,160}(?:re-?run|until|before)", re.I)
REPORT_PAT = re.compile(r"^#{1,6}\s*Report", re.I | re.M)
TABLE_PAT = re.compile(r"\|\s*Task\s*\|\s*Status\s*\|", re.I)


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

    if not IMPLEMENT.exists():
        report([f"commands/implement.md is missing — the HOP must live at {IMPLEMENT.relative_to(HERE)}"])
        return 1
    text = strip_comments(IMPLEMENT.read_text(encoding="utf-8"))

    if "$ARGUMENTS" not in text:
        failures.append("commands/implement.md never references $ARGUMENTS — the plan path must flow in through the $ARGUMENTS slot")
    elif not ARGS_PAT.search(text):
        failures.append("commands/implement.md has $ARGUMENTS but never as a *plan path* — say it: read the plan file at $ARGUMENTS")

    read_m = READ_PAT.search(text)
    if not read_m:
        failures.append("commands/implement.md never tells the agent to READ the plan — step 1 of a HOP is reading the prompt it received")

    order_m = ORDER_PAT.search(text)
    if not order_m:
        failures.append("commands/implement.md has no ordered-execution language — tasks run `in order, one task at a time`")

    if not VALIDATE_PAT.search(text):
        failures.append("commands/implement.md has no validation gate — run *every validation command* listed in the plan")
    if not FIX_PAT.search(text):
        failures.append("commands/implement.md never closes the loop on failures — on a failing command: fix, then re-run until all pass")

    report_m = REPORT_PAT.search(text)
    if not report_m:
        failures.append("commands/implement.md is missing a `## Report` section — your agent reports what it did, always")
    if not TABLE_PAT.search(text):
        failures.append("commands/implement.md Report must specify a markdown table with a `| Task | Status |` header row")

    # Sane ordering: read the plan before executing; validate before reporting.
    if read_m and order_m and read_m.start() > order_m.start():
        failures.append("workflow order is wrong — the agent must READ the plan before it EXECUTES tasks")
    val_m = VALIDATE_PAT.search(text)
    if val_m and report_m and val_m.start() > report_m.start():
        failures.append("workflow order is wrong — VALIDATION must happen before the REPORT (never report on unvalidated work)")

    if not SAMPLE.exists():
        failures.append("specs/sample-plan.md is missing — the sample plan is what your HOP runs against; restore it (just reset 05)")
    else:
        sample = strip_comments(SAMPLE.read_text(encoding="utf-8"))
        if not re.search(r"^#{1,6}\s*validation\s+commands", sample, re.I | re.M):
            failures.append("specs/sample-plan.md lost its Validation commands section — a plan without validation is an open loop")

    report(failures)
    return 1 if failures else 0


def report(failures: list[str]) -> None:
    if not failures:
        print(f"✅ PASS — {SLUG}")
        print("   your /implement HOP reads, executes, validates, reports. Plans passed into plans.")
        return
    print(f"❌ FAIL — {SLUG}")
    for i, msg in enumerate(failures, 1):
        print(f"  {i}. {msg}")


if __name__ == "__main__":
    sys.exit(main())

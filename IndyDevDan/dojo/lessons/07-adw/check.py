#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""check.py — closed-loop validator for 07 adw. Deterministic, offline, stdlib-only."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LESSON = "07 adw"
ADW = HERE / "adw.py"
LOG = HERE / "adw_log.jsonl"

STARTER_FILES = [
    ADW,
    *sorted((HERE / "prompts").glob("*.md")),
    *sorted((HERE / "tests").glob("*.py")),
]


def scan_blanks(problems: list[str]) -> None:
    found = []
    for p in STARTER_FILES:
        if p.exists():
            n = p.read_text(encoding="utf-8").count("____")
            if n:
                found.append(f"{p.relative_to(HERE)} ({n})")
    if found:
        problems.append(
            "blanks remain — fill every ____ before the loop can close: " + ", ".join(found)
        )


def check_structure(problems: list[str]) -> None:
    for rel in (
        "adw.py",
        "prompts/plan.md",
        "prompts/build.md",
        "prompts/resolve.md",
        "mock_outputs/plan.txt",
        "mock_outputs/build.txt",
        "mock_outputs/resolve.txt",
        "tests/test_greeting.py",
    ):
        if not (HERE / rel).exists():
            problems.append(f"missing file: {rel} — restore it (just reset 07)")


def run_adw(fail_tests: bool) -> tuple[subprocess.CompletedProcess, list[dict] | None]:
    LOG.unlink(missing_ok=True)
    env = dict(os.environ)
    env["DOJO_MOCK"] = "1"
    env.pop("DOJO_FAIL_TESTS", None)
    if fail_tests:
        env["DOJO_FAIL_TESTS"] = "1"
    proc = subprocess.run(
        [sys.executable, str(ADW), "add greeting"],
        cwd=HERE, env=env, capture_output=True, text=True, timeout=60,
    )
    records = None
    if LOG.exists():
        try:
            records = [
                json.loads(line)
                for line in LOG.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
        except json.JSONDecodeError:
            records = None
    return proc, records


def check_happy_path(problems: list[str]) -> None:
    proc, records = run_adw(fail_tests=False)
    tail = (proc.stdout + proc.stderr).strip().splitlines()[-3:]
    if proc.returncode != 0:
        problems.append(
            f"DOJO_MOCK=1 python3 adw.py \"add greeting\" exited {proc.returncode} — "
            f"the happy path must exit 0. Last output: {' | '.join(tail)}"
        )
        return
    if records is None:
        problems.append(
            "adw_log.jsonl missing or not valid JSONL after the happy-path run — "
            "the report blank must append one json.dumps(...) line"
        )
        return
    if len(records) != 1:
        problems.append(f"adw_log.jsonl has {len(records)} records after one run — append exactly one line per run")
        return
    rec = records[0]
    if rec.get("task") != "add greeting":
        problems.append(f"log record task is {rec.get('task')!r} — it must be the argv task ('add greeting')")
    if rec.get("ok") is not True:
        problems.append(f"log record ok is {rec.get('ok')!r} on the happy path — it must be true (JSON boolean)")
    if rec.get("steps") != ["plan", "build", "validate"]:
        problems.append(
            f"happy-path steps are {rec.get('steps')!r} — the chain is plan → build → validate, "
            "in that order, and resolve must NOT run when validation passes"
        )


def check_resolve_path(problems: list[str]) -> None:
    proc, records = run_adw(fail_tests=True)
    if proc.returncode == 0:
        problems.append(
            "with DOJO_FAIL_TESTS=1 the workflow exited 0 — fail loud: "
            "exit nonzero when the final validation fails"
        )
    if records is None or len(records) != 1:
        problems.append(
            "with DOJO_FAIL_TESTS=1, adw_log.jsonl must still gain exactly one record — "
            "an ADW reports even when it fails (especially when it fails)"
        )
        return
    rec = records[0]
    steps = rec.get("steps") or []
    if steps.count("resolve") != 1:
        problems.append(
            f"with DOJO_FAIL_TESTS=1 the resolve step ran {steps.count('resolve')} time(s) — "
            "the gate is exactly one resolve attempt, then re-validate"
        )
    if steps != ["plan", "build", "validate", "resolve", "validate"]:
        problems.append(
            f"failing-path steps are {steps!r} — expected "
            "['plan', 'build', 'validate', 'resolve', 'validate']"
        )
    if rec.get("ok") is not False:
        problems.append(
            f"failing-path log record ok is {rec.get('ok')!r} — ok must reflect the FINAL "
            "validation (false here); never report success you didn't verify"
        )


def main() -> None:
    problems: list[str] = []
    scan_blanks(problems)
    if not problems:
        check_structure(problems)
    if not problems:
        try:
            check_happy_path(problems)
            check_resolve_path(problems)
        finally:
            LOG.unlink(missing_ok=True)
    if problems:
        print(f"❌ FAIL — {LESSON}")
        for i, p in enumerate(problems, 1):
            print(f"  {i}. {p}")
        sys.exit(1)
    print(f"✅ PASS — {LESSON}")
    sys.exit(0)


if __name__ == "__main__":
    main()

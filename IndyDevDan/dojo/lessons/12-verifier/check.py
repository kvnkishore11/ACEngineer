#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Closed-loop validator for 12 verifier. Deterministic, offline, stdlib only.

Runs the learner's verifier against two fixtures: the dishonest builder report
(one false claim — must exit 1 with evidence citing the observed result) and
the honest report (must exit 0). verification_report.json is cleaned before
and after so reruns are deterministic.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LESSON = "12 verifier"
VERIFIER = HERE / "verifier.py"
REPORT = HERE / "verification_report.json"


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


def cleanup() -> None:
    REPORT.unlink(missing_ok=True)
    shutil.rmtree(HERE / "sample_app" / "__pycache__", ignore_errors=True)


def run_verifier(fixture_name: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(VERIFIER), str(HERE / "fixtures" / fixture_name)],
        cwd=HERE, capture_output=True, text=True, timeout=30,
        stdin=subprocess.DEVNULL,
    )


def stderr_tail(proc: subprocess.CompletedProcess) -> str:
    out = (proc.stderr or proc.stdout or "").strip()
    return out.splitlines()[-1] if out else "no output"


def read_report() -> tuple[dict | None, str | None]:
    if not REPORT.exists():
        return None, "verifier.py did not write verification_report.json — write the report contract in main()"
    try:
        data = json.loads(REPORT.read_text(encoding="utf-8"))
    except ValueError:
        return None, "verification_report.json is not valid JSON — write it with json.dumps(..., indent=2)"
    if not isinstance(data.get("claims"), list):
        return None, 'verification_report.json needs a "claims" list — the schema is {"claims": [...], "all_verified": bool}'
    if not isinstance(data.get("all_verified"), bool):
        return None, 'verification_report.json needs an "all_verified" boolean — the one-glance answer'
    for entry in data["claims"]:
        if not all(k in entry for k in ("claim", "verdict", "evidence")):
            return None, 'every claims[] entry needs {"claim", "verdict", "evidence"} — evidence beats assertion'
    return data, None


def find_claim(data: dict, needle: str) -> dict | None:
    return next((c for c in data["claims"] if needle in str(c["claim"]).lower()), None)


def validate() -> list[str]:
    fails: list[str] = []

    # Round 1 — the dishonest report: one claim is false.
    try:
        proc = run_verifier("builder_report.md")
    except subprocess.TimeoutExpired:
        return ["verifier.py hung — every check here is a file read or a function call; nothing should wait"]
    data, err = read_report()
    if err:
        crash = f" (it crashed: {stderr_tail(proc)})" if proc.returncode != 0 and proc.stderr else ""
        return [err + crash]

    if len(data["claims"]) < 4:
        fails.append(f"extract_claims found {len(data['claims'])} claim(s) but the report makes 4 — "
                     "parse every numbered line with a MULTILINE regex")
        return fails

    mult = find_claim(data, "multiply")
    if mult is None:
        fails.append("no claim about multiply was extracted — claim 3 is the one that matters most")
    else:
        if mult["verdict"] is not False:
            fails.append("the multiply claim must have verdict false — the builder shipped a bug; "
                         "call the function yourself, never trust the report")
        if "9" not in str(mult["evidence"]):
            fails.append("the multiply evidence must cite the ACTUAL observed result (multiply(4, 5) really returns 9) — "
                         "evidence beats assertion")

    for needle, label in (("add(", "add-behavior"), ("created", "file-existence"), ("docstring", "docstring")):
        entry = find_claim(data, needle)
        if entry is None:
            fails.append(f"no {label} claim was extracted from the report")
        elif entry["verdict"] is not True:
            fails.append(f"the {label} claim is TRUE in reality — its verdict must be true "
                         f"(your check returned: {entry['evidence']!r})")

    if data["all_verified"] is not False:
        fails.append("all_verified must be false when any atomic claim fails — "
                     "a single PASS that hides a failed sub-claim is worse than an explicit FAIL")
    if proc.returncode != 1:
        fails.append(f"verifier.py must exit 1 when a claim fails (the signal to re-prompt the builder) — got {proc.returncode}")
    if "multiply" not in proc.stdout:
        fails.append("print each claim's verdict to stdout — stdout is a leverage point")

    # Round 2 — the honest report: every claim verifies.
    REPORT.unlink(missing_ok=True)
    try:
        proc = run_verifier("builder_report_honest.md")
    except subprocess.TimeoutExpired:
        return fails + ["verifier.py hung on the honest report"]
    data, err = read_report()
    if err:
        return fails + [f"honest report run: {err}"]
    if proc.returncode != 0:
        fails.append(f"on the honest report every claim is true — verifier.py must exit 0, got {proc.returncode} "
                     f"({stderr_tail(proc)})")
    if data["all_verified"] is not True:
        fails.append("honest report run: all_verified must be true — a verifier that cries wolf gets deleted")
    if len(data["claims"]) != 3 or not all(c["verdict"] is True for c in data["claims"]):
        fails.append("honest report run: expected exactly 3 claims, all with verdict true")
    return fails


def main() -> None:
    cleanup()
    fails = scan_blanks()
    if not fails:
        try:
            fails = validate()
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

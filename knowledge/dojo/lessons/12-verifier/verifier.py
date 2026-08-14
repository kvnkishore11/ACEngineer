#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""verifier.py — a builder's report goes in, atomic verdicts come out.

Usage: python3 verifier.py <path/to/builder_report.md>

The verifier takes no free-form input — it forces you to template your
engineering. It decomposes the builder's report into atomic claims, proves
or disproves each with READ-ONLY checks (it never edits anything), writes
verification_report.json, and exits 1 when any claim fails — the signal to
re-prompt the builder. Evidence beats assertion: the builder's report is a
CLAIM, never proof.
"""
from __future__ import annotations

import ast
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CALC = ROOT / "sample_app" / "calculator.py"
REPORT_OUT = ROOT / "verification_report.json"


def extract_claims(report_text: str) -> list[str]:
    """Decompose the report into atomic claims — one per numbered line."""
    # YOUR TURN: parse the numbered claim lines ("1. ...", "2. ...") out of
    # the report with re.findall and a MULTILINE regex like
    # r"^\s*\d+\.\s+(.+)$", returning the list of claim strings.
    # Atoms over assertions: one claim, one truth value.
    ____


def load_calculator():
    """Import sample_app/calculator.py fresh — read it, run it, never edit it."""
    spec = importlib.util.spec_from_file_location("calculator", CALC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def verify_claim(claim: str) -> tuple[bool, str]:
    """Dispatch one atomic claim to a read-only check.

    Returns (verdict, evidence). Every verdict must cite what the verifier
    actually OBSERVED — a path check, a call result, an ast scan — never
    what the builder said.
    """
    low = claim.lower()

    if "docstring" in low:
        # YOUR TURN: docstring check via ast — parse CALC.read_text() with
        # ast.parse, collect the names of every ast.FunctionDef node whose
        # ast.get_docstring(node) is empty, then:
        #   return (not missing, f"ast docstring scan of {CALC.name}: missing={missing or 'none'}")
        ____

    m = re.search(r"(\w+)\((-?\d+),\s*(-?\d+)\)\s*returns\s*(-?\d+)", claim)
    if m:
        fn, a, b, want = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
        mod = load_calculator()
        # YOUR TURN: the behavior check — actually call it (read-only!):
        #   actual = getattr(mod, fn)(a, b)
        # then return (actual == want, evidence citing the OBSERVED result,
        # e.g. f"called {fn}({a}, {b}) -> got {actual}, builder claimed {want}")
        ____

    if "created" in low or "exists" in low:
        # YOUR TURN: the file-existence check via pathlib — never trust the
        # report, ask the filesystem:
        #   return (CALC.exists(), f"pathlib: {CALC.relative_to(ROOT)} exists -> {CALC.exists()}")
        ____

    return (False, "no verifier for this claim — the gap is the next thing you template")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: python3 verifier.py <path/to/builder_report.md>")
    report_path = Path(sys.argv[1])
    if not report_path.exists():
        sys.exit(f"no report at {report_path} — the verifier verifies reports, not vibes")

    claims = extract_claims(report_path.read_text(encoding="utf-8"))
    results = []
    for claim in claims:
        verdict, evidence = verify_claim(claim)
        print(f"{'✅' if verdict else '❌'} {claim}")
        print(f"   evidence: {evidence}")
        results.append({"claim": claim, "verdict": verdict, "evidence": evidence})

    all_verified = bool(results) and all(r["verdict"] for r in results)
    # YOUR TURN: the report contract — every agent must produce a concrete
    # asset. Write JSON {"claims": results, "all_verified": all_verified}
    # to REPORT_OUT with json.dumps(..., indent=2).
    ____
    print(f"\n{len(results)} atomic claims · all_verified={all_verified} · wrote {REPORT_OUT.name}")
    # YOUR TURN: close the loop — sys.exit(1) when any claim failed (the
    # caller re-prompts the builder), sys.exit(0) only when every atomic
    # claim verified.
    ____


if __name__ == "__main__":
    main()

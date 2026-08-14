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
    # Atoms over assertions: one claim, one truth value.
    return re.findall(r"^\s*\d+\.\s+(.+)$", report_text, re.MULTILINE)


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
        # Docstring check via ast — static, deterministic, read-only.
        tree = ast.parse(CALC.read_text(encoding="utf-8"))
        missing = [n.name for n in ast.walk(tree)
                   if isinstance(n, ast.FunctionDef) and not ast.get_docstring(n)]
        return (not missing, f"ast docstring scan of {CALC.name}: missing={missing or 'none'}")

    m = re.search(r"(\w+)\((-?\d+),\s*(-?\d+)\)\s*returns\s*(-?\d+)", claim)
    if m:
        fn, a, b, want = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
        mod = load_calculator()
        # The behavior check — actually call it (read-only!).
        actual = getattr(mod, fn)(a, b)
        return (actual == want, f"called {fn}({a}, {b}) -> got {actual}, builder claimed {want}")

    if "created" in low or "exists" in low:
        # The file-existence check — never trust the report, ask the filesystem.
        return (CALC.exists(), f"pathlib: {CALC.relative_to(ROOT)} exists -> {CALC.exists()}")

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
    # The report contract — every agent must produce a concrete asset.
    REPORT_OUT.write_text(
        json.dumps({"claims": results, "all_verified": all_verified}, indent=2),
        encoding="utf-8",
    )
    print(f"\n{len(results)} atomic claims · all_verified={all_verified} · wrote {REPORT_OUT.name}")
    # Close the loop: exit 1 -> re-prompt the builder; exit 0 -> proven work.
    sys.exit(0 if all_verified else 1)


if __name__ == "__main__":
    main()

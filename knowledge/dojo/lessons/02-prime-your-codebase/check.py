#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Closed-loop validator for 02 · prime-your-codebase.

Deterministic, offline, stdlib-only. Verifies the /prime command READs real
paths, RUNs a strictly read-only command, and demands a numbered REPORT.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NN, SLUG = "02", "prime-your-codebase"
PRIME = HERE / "commands" / "prime.md"
STARTERS = [
    "commands/prime.md",
    "sample_app/README.md",
    "sample_app/app.py",
    "sample_app/db.py",
    "sample_app/config.json",
]
WRITE_PATTERNS = [
    (r"\brm\b", "`rm` deletes"),
    (r"\bmv\b", "`mv` moves"),
    (r"\bcp\b", "`cp` writes"),
    (r"\btouch\b", "`touch` creates files"),
    (r"\bmkdir\b", "`mkdir` creates directories"),
    (r"\btee\b", "`tee` writes files"),
    (r"\bdd\b", "`dd` writes raw data"),
    (r"\btruncate\b|\bshred\b", "truncate/shred destroy data"),
    (r"\bchmod\b|\bchown\b", "chmod/chown mutate metadata"),
    (r">", "`>` redirects output into a file"),
    (r"\bsed\b[^\n]*\s-i\b", "`sed -i` edits in place"),
    (r"\bgit\s+(add|commit|push|reset|restore|checkout|clean|rm)\b", "state-changing git command"),
]


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

    prime = strip_comments(PRIME.read_text(encoding="utf-8"))

    for name, why in (
        ("READ", "which files build the agent's picture"),
        ("RUN", "safe stdout the agent can observe"),
        ("REPORT", "the agent must prove the context landed"),
    ):
        if section(prime, name) is None:
            fails.append(f"commands/prime.md: missing `## {name}` section ({why})")

    # READ — every listed path must exist on disk. Stale paths poison the prime.
    read_sec = section(prime, "READ") or ""
    bullets = [b.strip().strip("`") for b in re.findall(r"^\s*[-*]\s+(\S+)", read_sec, re.M)]
    if len(bullets) < 3:
        fails.append(
            f"commands/prime.md: READ lists {len(bullets)} path(s) — needs at least 3 bare "
            "paths, one per bullet (README, entry point, storage layer)"
        )
    for token in bullets:
        if not (HERE / token).exists():
            fails.append(
                f"commands/prime.md: READ path not found on disk: {token!r} — use real paths "
                "relative to this lesson directory, e.g. sample_app/app.py"
            )

    # RUN — one command, strictly read-only.
    run_sec = section(prime, "RUN") or ""
    fence = re.search(r"```[^\n]*\n(.*?)```", run_sec, re.S)
    if not fence:
        fails.append("commands/prime.md: RUN needs its command inside the ```bash fence")
    else:
        cmd = fence.group(1).strip()
        if not cmd:
            fails.append(
                "commands/prime.md: the RUN fence is empty — give the agent one read-only "
                "command that shows the project layout"
            )
        for pattern, why in WRITE_PATTERNS:
            if re.search(pattern, cmd):
                fails.append(
                    f"commands/prime.md: RUN is not read-only ({why}) — a prime observes, "
                    "it never mutates. Try: find sample_app -type f | head -20"
                )
                break

    # REPORT — a numbered contract with at least 3 items.
    report_sec = section(prime, "REPORT") or ""
    items = re.findall(r"^\s*\d+[.)]\s+\S+", report_sec, re.M)
    if len(items) < 3:
        fails.append(
            f"commands/prime.md: REPORT has {len(items)} numbered item(s) — needs at least 3: "
            "what the app is, key modules, suggested next step"
        )

    finish(fails)


if __name__ == "__main__":
    main()

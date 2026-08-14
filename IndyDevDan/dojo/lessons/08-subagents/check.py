#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""check.py — closed-loop validator for 08 subagents. Deterministic, offline, stdlib-only."""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LESSON = "08 subagents"
SCOUT = HERE / "agents" / "file-scout.md"
FANOUT = HERE / "commands" / "fanout.md"

FORBIDDEN_TOOLS = {"write", "edit", "bash", "notebookedit", "websearch", "webfetch"}
REQUIRED_TOOLS = {"read", "glob", "grep"}


def strip_comments(text: str) -> str:
    """Drop <!-- --> comments so the learner's own words carry the checks."""
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str]:
    """Tiny stdlib frontmatter parser: key: value lines between --- markers."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    fm: dict[str, str] = {}
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return fm, "\n".join(lines[i + 1 :])
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue  # YAML comments (the YOUR TURN guidance) are not data
        if ":" in stripped:
            key, value = stripped.split(":", 1)
            fm[key.strip()] = value.strip()
    return None, text  # never saw the closing ---


def scan_blanks(problems: list[str]) -> None:
    found = []
    for p in (SCOUT, FANOUT):
        if p.exists():
            n = p.read_text(encoding="utf-8").count("____")
            if n:
                found.append(f"{p.relative_to(HERE)} ({n})")
    if found:
        problems.append(
            "blanks remain — fill every ____ before the loop can close: " + ", ".join(found)
        )


def check_scout(problems: list[str]) -> None:
    if not SCOUT.exists():
        problems.append("missing file: agents/file-scout.md — restore it (just reset 08)")
        return
    fm, body = parse_frontmatter(SCOUT.read_text(encoding="utf-8"))
    if fm is None:
        problems.append(
            "agents/file-scout.md: frontmatter did not parse — the file must open with "
            "'---', hold 'key: value' lines, and close with '---'"
        )
        return
    if fm.get("name") != "file-scout":
        problems.append(f"agents/file-scout.md: frontmatter name is {fm.get('name')!r} — it must stay 'file-scout'")

    desc = fm.get("description", "")
    if len(desc) < 80:
        problems.append(
            f"agents/file-scout.md: description is {len(desc)} chars — the routing contract "
            "needs at least 80: say WHAT the scout does and WHEN to use it"
        )
    if not re.search(r"(?i)use\s+proactively|proactively|must be used", desc):
        problems.append(
            "agents/file-scout.md: description has no proactive trigger — the primary agent "
            "routes on this field; add an IDK like 'Use PROACTIVELY when ...'"
        )

    tools = {t.strip().lower() for t in fm.get("tools", "").split(",") if t.strip()}
    missing = REQUIRED_TOOLS - tools
    if missing:
        problems.append(
            f"agents/file-scout.md: tools missing {sorted(missing)} — a scout needs Read, Glob, Grep"
        )
    granted_forbidden = sorted(tools & FORBIDDEN_TOOLS)
    if granted_forbidden:
        problems.append(
            f"agents/file-scout.md: tools grant {granted_forbidden} — a scout only looks; "
            "strip everything that writes or executes (no Write, no Edit, no Bash)"
        )

    clean_body = strip_comments(body)
    if not re.search(r"(?i)primary agent", clean_body):
        problems.append(
            "agents/file-scout.md: the body never mentions the primary agent — subagents "
            "respond to the primary agent, not the user; say the final message is a report back"
        )
    if not re.search(r"(?i)\breport\b", clean_body):
        problems.append(
            "agents/file-scout.md: the body needs a Report section that spells out the "
            "report shape sent back to the primary agent"
        )


def check_fanout(problems: list[str]) -> None:
    if not FANOUT.exists():
        problems.append("missing file: commands/fanout.md — restore it (just reset 08)")
        return
    text = strip_comments(FANOUT.read_text(encoding="utf-8"))
    if "$ARGUMENTS" not in text:
        problems.append(
            "commands/fanout.md: no $ARGUMENTS — the three directories arrive as arguments"
        )
    if "file-scout" not in text:
        problems.append(
            "commands/fanout.md: never names the file-scout subagent — the command must "
            "launch the agent you just defined"
        )
    if not re.search(r"(?i)in parallel|single message|at the same time|simultaneously|concurrently", text):
        problems.append(
            "commands/fanout.md: no parallel instruction — say it outright: launch all "
            "three scouts IN PARALLEL, in a single message, never sequentially"
        )
    if not re.search(r"(?i)aggregat|combin|merge", text):
        problems.append(
            "commands/fanout.md: no aggregation step — the scout reports come back to the "
            "primary agent; instruct it to aggregate/combine them into one summary"
        )
    if not re.search(r"(?i)\btable\b", text):
        problems.append(
            "commands/fanout.md: no summary table — the Report must end in ONE markdown "
            "table with a row per directory"
        )


def main() -> None:
    problems: list[str] = []
    scan_blanks(problems)
    if not problems:
        check_scout(problems)
        check_fanout(problems)
    if problems:
        print(f"❌ FAIL — {LESSON}")
        for i, p in enumerate(problems, 1):
            print(f"  {i}. {p}")
        sys.exit(1)
    print(f"✅ PASS — {LESSON}")
    sys.exit(0)


if __name__ == "__main__":
    main()

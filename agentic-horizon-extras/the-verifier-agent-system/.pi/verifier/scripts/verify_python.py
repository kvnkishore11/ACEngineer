#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Verifier-side Python checks. READ-ONLY. JSON output.

Wraps the Astral toolchain (ty + ruff) plus pytest into a single allowlisted
script the verifier's bash policy can pin to. The verifier agent only ever
issues commands of the form:

    uv run --script .pi/verifier/scripts/verify_python.py <subcommand> <args...>

Subcommands:
  type    <path>                        — uvx ty check <path>
  lint    <path>                        — uvx ruff check <path>
  format  <path>                        — uvx ruff format --check --diff <path>
  test    <path>                        — uv run pytest <path> --tb=short -q
  coverage <test_path> --module <name>  — uv run pytest --cov=<name> --cov-report=term-missing <test_path>

Anything else is rejected with a structured JSON error so the agent can
self-correct on the next step.
"""

import argparse
import json
import os
import shlex
import subprocess
import sys
from typing import Any


# ─── Allowlist ───────────────────────────────────────────────────────────────

ALLOWED_SUBCOMMANDS: tuple[str, ...] = (
    "type",
    "lint",
    "format",
    "test",
    "coverage",
)

ALLOWED_FORMS: list[str] = [
    "type <path>                        — uvx ty check <path>",
    "lint <path>                        — uvx ruff check <path>",
    "format <path>                      — uvx ruff format --check --diff <path>",
    "test <path>                        — uv run pytest <path> --tb=short -q",
    "coverage <test_path> --module <m>  — uv run pytest --cov=<m> --cov-report=term-missing <test_path>",
]

# Per-subprocess timeout (seconds). pytest in particular can hang on slow tests
# or a misconfigured environment; we cap so the verifier's max_loops escalation
# isn't gated on a runaway subprocess.
TOOL_TIMEOUT_SEC = 120

# ─── Helpers ─────────────────────────────────────────────────────────────────


def emit(payload: dict[str, Any], *, exit_code: int = 0) -> None:
    """Print one JSON object to stdout and exit with the given code."""
    sys.stdout.write(json.dumps(payload))
    sys.stdout.write("\n")
    sys.stdout.flush()
    sys.exit(exit_code)


def reject(received: str, reason: str, hint: str) -> None:
    """Structured JSON rejection. Mirrors verify_sqlite.py's `reject` so the
    teaching surface is identical across verifier domains. Always exits non-zero."""
    emit(
        {
            "error": "command not permitted in read-only verifier",
            "received": received,
            "reason": reason,
            "allowed": ALLOWED_FORMS,
            "hint": hint,
        },
        exit_code=2,
    )


def run_tool(cmd: list[str], *, label: str) -> dict[str, Any]:
    """Run a subprocess, return a structured payload. Tool-not-found and
    timeout become structured errors with non-zero exit; the agent reads
    the JSON and decides next steps."""
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            timeout=TOOL_TIMEOUT_SEC,
        )
    except FileNotFoundError as e:
        emit(
            {
                "error": "tool not found on PATH",
                "label": label,
                "command": shell_join(cmd),
                "reason": str(e),
                "hint": (
                    "Install the missing tool. For ty/ruff: `uv tool install ty`, "
                    "`uv tool install ruff`. For pytest: add it to the project's "
                    "dev dependencies (pyproject.toml or `uv add --dev pytest`)."
                ),
            },
            exit_code=3,
        )
        return {}  # unreachable
    except subprocess.TimeoutExpired:
        emit(
            {
                "error": "tool timeout",
                "label": label,
                "command": shell_join(cmd),
                "reason": f"exceeded {TOOL_TIMEOUT_SEC}s",
                "hint": (
                    "The tool is hanging or the test scope is too large. "
                    "Narrow the path argument to a single file or a small directory."
                ),
            },
            exit_code=4,
        )
        return {}  # unreachable

    return {
        "label": label,
        "command": shell_join(cmd),
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def shell_join(argv: list[str]) -> str:
    """Render argv as a copy-pasteable shell command for the agent's logs."""
    return " ".join(shlex.quote(a) for a in argv)


def require_existing_path(path: str, *, kind: str) -> None:
    """Reject with a clear hint if the path doesn't exist on disk. Avoids
    surfacing tool-internal errors that are confusing for path typos."""
    if not os.path.exists(path):
        reject(
            received=path,
            reason=f"{kind} '{path}' does not exist on disk",
            hint=(
                f"Confirm the path is correct (relative to the project root). "
                f"List the directory with `ls` first if you're unsure."
            ),
        )


# ─── Routes ──────────────────────────────────────────────────────────────────


def route_type(path: str) -> None:
    """uvx ty check <path>"""
    require_existing_path(path, kind="path")
    emit(run_tool(["uvx", "ty", "check", path], label="type"))


def route_lint(path: str) -> None:
    """uvx ruff check <path>"""
    require_existing_path(path, kind="path")
    emit(run_tool(["uvx", "ruff", "check", path], label="lint"))


def route_format(path: str) -> None:
    """uvx ruff format --check --diff <path>"""
    require_existing_path(path, kind="path")
    emit(run_tool(["uvx", "ruff", "format", "--check", "--diff", path], label="format"))


def route_test(path: str) -> None:
    """uv run pytest <path> --tb=short -q"""
    require_existing_path(path, kind="test path")
    emit(run_tool(["uv", "run", "pytest", path, "--tb=short", "-q"], label="test"))


def route_coverage(test_path: str, module: str) -> None:
    """uv run pytest --cov=<module> --cov-report=term-missing <test_path>"""
    require_existing_path(test_path, kind="test path")
    if not module or "/" in module or module.startswith("-"):
        reject(
            received=f"coverage {test_path} --module {module}",
            reason=f"invalid --module value: {module!r}",
            hint=(
                "--module takes a Python import path (dotted, no slashes), "
                "e.g. `--module my_pkg.users` or `--module foo`."
            ),
        )
    emit(
        run_tool(
            [
                "uv",
                "run",
                "pytest",
                f"--cov={module}",
                "--cov-report=term-missing",
                test_path,
            ],
            label="coverage",
        )
    )


# ─── Main ────────────────────────────────────────────────────────────────────


def main() -> None:
    # Custom argparse so we can route on the first positional. argparse's
    # subparsers would also work, but the verify_sqlite.py shape is
    # "positional first then string args," and we want this script's CLI to
    # feel familiar to anyone who's used the SQLite verifier.
    parser = argparse.ArgumentParser(
        description="Verifier-side Python checks. READ-ONLY. JSON output.",
        add_help=True,
    )
    parser.add_argument(
        "subcommand",
        help=f"One of: {', '.join(ALLOWED_SUBCOMMANDS)}",
    )
    parser.add_argument(
        "args",
        nargs="*",
        help="Subcommand arguments (varies — see --help on each subcommand's persona docs).",
    )
    parser.add_argument(
        "--module",
        help="(coverage only) Python import path of the module under test.",
    )

    try:
        ns = parser.parse_args()
    except SystemExit as e:
        sys.stdout.write(
            json.dumps(
                {
                    "error": "invalid arguments",
                    "hint": (
                        "Usage: verify_python.py <subcommand> <args...>. "
                        f"Subcommands: {', '.join(ALLOWED_SUBCOMMANDS)}."
                    ),
                }
            )
            + "\n"
        )
        sys.stdout.flush()
        raise SystemExit(e.code if isinstance(e.code, int) else 2)

    sub = ns.subcommand.lower()
    rest: list[str] = list(ns.args)

    if sub not in ALLOWED_SUBCOMMANDS:
        reject(
            received=f"{sub} {' '.join(rest)}".strip(),
            reason=f"unknown subcommand '{sub}'",
            hint=(
                f"Valid subcommands: {', '.join(ALLOWED_SUBCOMMANDS)}. "
                "Each takes its own arguments — see the persona's Tool policy section."
            ),
        )

    if sub == "type":
        if len(rest) != 1:
            reject(
                received=f"type {' '.join(rest)}".strip(),
                reason="type expects exactly one argument: <path>",
                hint="e.g. `type src/users.py` or `type src/`",
            )
        route_type(rest[0])

    elif sub == "lint":
        if len(rest) != 1:
            reject(
                received=f"lint {' '.join(rest)}".strip(),
                reason="lint expects exactly one argument: <path>",
                hint="e.g. `lint src/users.py` or `lint src/`",
            )
        route_lint(rest[0])

    elif sub == "format":
        if len(rest) != 1:
            reject(
                received=f"format {' '.join(rest)}".strip(),
                reason="format expects exactly one argument: <path>",
                hint="e.g. `format src/users.py` or `format src/`",
            )
        route_format(rest[0])

    elif sub == "test":
        if len(rest) != 1:
            reject(
                received=f"test {' '.join(rest)}".strip(),
                reason="test expects exactly one argument: <path>",
                hint="e.g. `test tests/test_users.py` or `test tests/`",
            )
        route_test(rest[0])

    elif sub == "coverage":
        if len(rest) != 1 or not ns.module:
            reject(
                received=f"coverage {' '.join(rest)} {('--module ' + ns.module) if ns.module else ''}".strip(),
                reason="coverage expects: <test_path> --module <module>",
                hint="e.g. `coverage tests/test_users.py --module users`",
            )
        route_coverage(rest[0], ns.module)


if __name__ == "__main__":
    main()

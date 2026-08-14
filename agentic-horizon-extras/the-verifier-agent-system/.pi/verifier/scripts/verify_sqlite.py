#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Verifier-side SQLite inspection. READ-ONLY. JSON output."""

import argparse
import json
import re
import sqlite3
import subprocess
import sys
from typing import Any

# ─── Allowlists ──────────────────────────────────────────────────────────────

# PRAGMAs that are read-only / introspective. Anything not in this set is
# rejected, including pragmas like `writable_schema`, `defer_foreign_keys`,
# `journal_mode`, etc., which can mutate database state or behavior.
PRAGMA_ALLOWLIST: set[str] = {
    "integrity_check",
    "foreign_key_list",
    "foreign_key_check",
    "index_list",
    "index_info",
    "table_info",
    "table_xinfo",
    "database_list",
    "schema_version",
    "user_version",
}

# Keywords we recognize as deterministic mutations. Used only to enrich the
# `reason` field of the structured error — actual gating is "not in allowlist".
MUTATION_KEYWORDS: dict[str, str] = {
    "INSERT": "INSERT is a mutation — verifier is read-only",
    "UPDATE": "UPDATE is a mutation — verifier is read-only",
    "DELETE": "DELETE is a mutation — verifier is read-only",
    "DROP": "DROP is a mutation — verifier is read-only",
    "ALTER": "ALTER is a mutation — verifier is read-only",
    "CREATE": "CREATE is a mutation — verifier is read-only",
    "REPLACE": "REPLACE is a mutation — verifier is read-only",
    "TRUNCATE": "TRUNCATE is a mutation — verifier is read-only",
    "REINDEX": "REINDEX rewrites indexes — verifier is read-only",
    "VACUUM": "VACUUM rewrites the database — verifier is read-only",
    "ATTACH": "ATTACH can introduce mutable connections — not permitted",
    "DETACH": "DETACH mutates connection state — not permitted",
    "BEGIN": "transactions are not permitted in the read-only verifier",
    "COMMIT": "transactions are not permitted in the read-only verifier",
    "ROLLBACK": "transactions are not permitted in the read-only verifier",
    "SAVEPOINT": "transactions are not permitted in the read-only verifier",
    "RELEASE": "transactions are not permitted in the read-only verifier",
}

ALLOWED_FORMS: list[str] = [
    "dot-commands (e.g. .schema, .tables, .indexes)",
    "SELECT ...",
    "WITH ... SELECT ...",
    "EXPLAIN <query>",
    "PRAGMA integrity_check | foreign_key_list(<table>) | index_list(<table>) | table_info(<table>) | etc.",
]


# ─── Helpers ─────────────────────────────────────────────────────────────────

def open_ro(path: str) -> sqlite3.Connection:
    """Open the SQLite DB read-only via URI flags. Defense-in-depth: even if
    a mutation string somehow reached this script, SQLite would refuse it."""
    return sqlite3.connect(f"file:{path}?mode=ro&immutable=1", uri=True)


def emit(payload: dict[str, Any], *, exit_code: int = 0) -> None:
    """Print one JSON object to stdout and exit with the given code."""
    sys.stdout.write(json.dumps(payload))
    sys.stdout.write("\n")
    sys.stdout.flush()
    sys.exit(exit_code)


def reject(received: str, reason: str, hint: str) -> None:
    """Structured JSON rejection per PRE_INIT_DECISIONS.md Q5 ("Error
    feedback shape"). Always exits non-zero."""
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


def first_token(s: str) -> str:
    """Return the first whitespace-delimited token, uppercased. Empty string
    if the input is blank."""
    stripped = s.lstrip()
    if not stripped:
        return ""
    # Split on any whitespace; take the first chunk.
    return stripped.split(None, 1)[0].upper()


def extract_pragma_name(cmd: str) -> str | None:
    """Return the pragma name following the `PRAGMA` keyword, lowercased.
    Handles `PRAGMA name`, `PRAGMA name(arg)`, `PRAGMA name = value`."""
    # \bPRAGMA\b followed by whitespace, then the identifier.
    m = re.match(r"\s*PRAGMA\s+([A-Za-z_][A-Za-z0-9_]*)", cmd, re.IGNORECASE)
    if not m:
        return None
    return m.group(1).lower()


# ─── Routes ──────────────────────────────────────────────────────────────────

def route_dot_command(db: str, cmd: str) -> None:
    """Shell out to the sqlite3 CLI in -readonly mode. Print stdout/stderr as
    JSON. Non-zero exit propagates."""
    try:
        proc = subprocess.run(
            ["sqlite3", "-readonly", db, cmd],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        emit(
            {
                "error": "sqlite3 CLI not found on PATH",
                "received": cmd,
                "hint": "Install sqlite3 or use SELECT/PRAGMA via the Python module path.",
            },
            exit_code=3,
        )
        return  # unreachable; emit() exits

    payload: dict[str, Any] = {"stdout": proc.stdout, "stderr": proc.stderr}
    if proc.returncode != 0:
        payload["exit"] = proc.returncode
        emit(payload, exit_code=proc.returncode if proc.returncode != 0 else 1)
    emit(payload, exit_code=0)


def route_query(db: str, cmd: str) -> None:
    """SELECT / WITH / EXPLAIN — execute via the Python sqlite3 module under
    the read-only URI. Return columns + rows JSON."""
    try:
        with open_ro(db) as conn:
            cur = conn.execute(cmd)
            columns = [c[0] for c in cur.description] if cur.description else []
            rows = [list(r) for r in cur.fetchall()]
    except sqlite3.Error as e:
        emit(
            {
                "error": "sqlite error",
                "received": cmd,
                "reason": str(e),
                "hint": "Check the query syntax and that referenced tables/columns exist.",
            },
            exit_code=4,
        )
        return  # unreachable
    emit({"columns": columns, "rows": rows}, exit_code=0)


def route_pragma(db: str, cmd: str) -> None:
    """PRAGMA — validate the name against the allowlist, then execute via the
    Python sqlite3 module."""
    name = extract_pragma_name(cmd)
    if name is None:
        reject(
            received=cmd,
            reason="could not parse PRAGMA name",
            hint="Use the form: PRAGMA <name> or PRAGMA <name>(<arg>).",
        )
        return  # unreachable

    if name not in PRAGMA_ALLOWLIST:
        reject(
            received=cmd,
            reason=(
                f"PRAGMA {name} is not on the read-only allowlist "
                f"(it can mutate state or change connection behavior)"
            ),
            hint=(
                "Allowed PRAGMAs: "
                + ", ".join(sorted(PRAGMA_ALLOWLIST))
                + ". For schema introspection prefer .schema or PRAGMA table_info(<table>)."
            ),
        )
        return  # unreachable

    try:
        with open_ro(db) as conn:
            cur = conn.execute(cmd)
            columns = [c[0] for c in cur.description] if cur.description else []
            rows = [list(r) for r in cur.fetchall()]
    except sqlite3.Error as e:
        emit(
            {
                "error": "sqlite error",
                "received": cmd,
                "reason": str(e),
                "hint": "Check the PRAGMA arguments — e.g. PRAGMA table_info(users) needs a real table name.",
            },
            exit_code=4,
        )
        return  # unreachable
    emit({"columns": columns, "rows": rows}, exit_code=0)


# ─── Main ────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verifier-side SQLite inspection. READ-ONLY. JSON output.",
        add_help=True,
    )
    parser.add_argument("db", help="Path to the SQLite database file.")
    parser.add_argument(
        "command",
        help='A sqlite3 command — dot-command (e.g. ".schema"), SELECT/WITH/EXPLAIN query, or read-only PRAGMA.',
    )

    # argparse errors itself need to come out as JSON, not plain text.
    try:
        args = parser.parse_args()
    except SystemExit as e:
        # argparse already printed to stderr; emit a JSON shim so callers that
        # only read stdout still see something structured.
        sys.stdout.write(
            json.dumps(
                {
                    "error": "invalid arguments",
                    "hint": 'Usage: verify_sqlite.py <db> "<sqlite3 command>"',
                }
            )
            + "\n"
        )
        sys.stdout.flush()
        raise SystemExit(e.code if isinstance(e.code, int) else 2)

    raw_cmd: str = args.command
    cmd = raw_cmd.lstrip()

    if cmd == "":
        reject(
            received=raw_cmd,
            reason="command was empty",
            hint='Pass a sqlite3 command, e.g. ".schema" or "SELECT count(*) FROM users".',
        )
        return  # unreachable

    # 1. Dot-command — shell out to sqlite3 -readonly.
    if cmd.startswith("."):
        route_dot_command(args.db, cmd)
        return  # unreachable

    tok = first_token(cmd)

    # 2. SELECT / WITH / EXPLAIN — Python module read-only.
    if tok in {"SELECT", "WITH", "EXPLAIN"}:
        route_query(args.db, cmd)
        return  # unreachable

    # 3. PRAGMA — validate name then execute read-only.
    if tok == "PRAGMA":
        route_pragma(args.db, cmd)
        return  # unreachable

    # 4. Anything else — structured JSON error.
    reason = MUTATION_KEYWORDS.get(
        tok,
        f"`{tok or '<empty>'}` is not a recognized read-only sqlite3 command",
    )
    # Tailor the hint a bit based on the token.
    if tok == "INSERT":
        hint = "If you want to verify table contents, use: SELECT count(*) FROM <table>"
    elif tok == "UPDATE":
        hint = "If you want to inspect rows, use: SELECT * FROM <table> WHERE <cond>"
    elif tok == "DELETE":
        hint = "If you want to count matching rows, use: SELECT count(*) FROM <table> WHERE <cond>"
    elif tok in {"DROP", "ALTER", "CREATE"}:
        hint = "If you want to inspect schema, use: .schema  or  PRAGMA table_info(<table>)"
    else:
        hint = (
            "Use a dot-command (.schema, .tables), a SELECT/WITH query, EXPLAIN, "
            "or a read-only PRAGMA. The verifier never mutates state."
        )

    reject(received=raw_cmd, reason=reason, hint=hint)


if __name__ == "__main__":
    main()

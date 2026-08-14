"""Thin sqlite3 wrapper for live-bench.

Owns the connection lifecycle, the migration that materialises the spec §4.1
schema (3 tables + 2 indexes), and small row → Pydantic model adapters used by
``store.py``.

Internal storage conventions
----------------------------
* ``benchmarks.config_json`` — full ``BenchmarkConfig`` serialised as JSON.
* ``datapoints.client_ts`` — ISO-8601 UTC microsecond TEXT (lexicographically
  sortable, matches spec §4.1).
* ``datapoints.server_ts`` — Unix epoch milliseconds INTEGER (matches spec
  §4.1). All wire/api boundaries convert this to ``datetime``.
* ``benchmarks.created_at`` / ``updated_at`` — Unix epoch milliseconds INTEGER.
* ``completions.completed_at`` — Unix epoch milliseconds INTEGER.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from live_bench_server.models import DataPointStored


# ── Connection / migration ─────────────────────────────────
def connect(path: str | Path) -> sqlite3.Connection:
    """Open a sqlite3 connection in WAL mode with foreign keys enabled.

    ``check_same_thread=False`` so the FastAPI event loop and uvicorn worker
    threads can share one connection. Writes are still serialised by SQLite's
    own write lock; the broker / store layer holds the connection just long
    enough to execute its statements.
    """
    conn = sqlite3.connect(
        str(path),
        check_same_thread=False,
        isolation_level=None,  # autocommit; we manage transactions explicitly
    )
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


_SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS benchmarks (
        session_id   TEXT PRIMARY KEY,
        title        TEXT NOT NULL,
        subtitle     TEXT,
        better       TEXT NOT NULL,
        config_json  TEXT NOT NULL,
        source_path  TEXT,
        created_at   INTEGER NOT NULL,
        updated_at   INTEGER NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS datapoints (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id   TEXT NOT NULL REFERENCES benchmarks(session_id) ON DELETE CASCADE,
        chart_id     TEXT NOT NULL DEFAULT 'default',
        group_key    TEXT NOT NULL,
        metric_key   TEXT NOT NULL,
        value        REAL NOT NULL,
        seq          INTEGER NOT NULL,
        client_ts    TEXT NOT NULL,
        server_ts    INTEGER NOT NULL
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS ix_datapoints_session_seq
        ON datapoints(session_id, seq)
    """,
    """
    CREATE INDEX IF NOT EXISTS ix_datapoints_cell_client_ts
        ON datapoints(session_id, chart_id, group_key, metric_key, client_ts DESC)
    """,
    """
    CREATE TABLE IF NOT EXISTS completions (
        session_id    TEXT NOT NULL REFERENCES benchmarks(session_id) ON DELETE CASCADE,
        chart_id      TEXT NOT NULL DEFAULT 'default',
        group_key     TEXT NOT NULL,
        completed_at  INTEGER NOT NULL,
        PRIMARY KEY (session_id, chart_id, group_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS metadata (
        session_id   TEXT NOT NULL REFERENCES benchmarks(session_id) ON DELETE CASCADE,
        chart_id     TEXT NOT NULL,
        group_key    TEXT NOT NULL,
        data_json    TEXT NOT NULL DEFAULT '{}',
        updated_at   INTEGER NOT NULL,
        PRIMARY KEY (session_id, chart_id, group_key)
    )
    """,
]


def _ensure_chart_id_columns(conn: sqlite3.Connection) -> None:
    """Idempotent additive migration for the chart_id columns.

    Detects whether the existing dev DB pre-dates the multi-chart schema and
    ALTERs the tables to add chart_id with DEFAULT 'default'. Safe to call
    multiple times; safe on a fresh DB (no-ops because CREATE TABLE already
    included the column).
    """
    # datapoints — simple ADD COLUMN
    cols = {row["name"] for row in conn.execute("PRAGMA table_info(datapoints)")}
    if "chart_id" not in cols:
        conn.execute(
            "ALTER TABLE datapoints ADD COLUMN chart_id TEXT NOT NULL DEFAULT 'default'"
        )

    # completions — needs a table rebuild because the PK includes chart_id
    cols = {row["name"] for row in conn.execute("PRAGMA table_info(completions)")}
    if "chart_id" not in cols:
        conn.execute("BEGIN")
        try:
            conn.execute(
                """
                CREATE TABLE completions_new (
                    session_id    TEXT NOT NULL REFERENCES benchmarks(session_id) ON DELETE CASCADE,
                    chart_id      TEXT NOT NULL DEFAULT 'default',
                    group_key     TEXT NOT NULL,
                    completed_at  INTEGER NOT NULL,
                    PRIMARY KEY (session_id, chart_id, group_key)
                )
                """
            )
            conn.execute(
                """
                INSERT INTO completions_new (session_id, chart_id, group_key, completed_at)
                SELECT session_id, 'default', group_key, completed_at FROM completions
                """
            )
            conn.execute("DROP TABLE completions")
            conn.execute("ALTER TABLE completions_new RENAME TO completions")
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise

    # The cell index also depends on chart_id — drop and recreate.
    conn.execute("DROP INDEX IF EXISTS ix_datapoints_cell_client_ts")
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_datapoints_cell_client_ts
            ON datapoints(session_id, chart_id, group_key, metric_key, client_ts DESC)
        """
    )


def migrate(conn: sqlite3.Connection) -> None:
    """Run the spec §4.1 migration. Idempotent — safe to call on every boot."""
    for stmt in _SCHEMA:
        conn.execute(stmt)
    _ensure_chart_id_columns(conn)


# ── Time helpers ───────────────────────────────────────────
def now_ms() -> int:
    """Current wall-clock time as Unix epoch milliseconds (UTC)."""
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def ms_to_datetime(ms: int) -> datetime:
    """Convert a Unix-ms integer to a timezone-aware UTC datetime."""
    return datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc)


def datetime_to_ms(dt: datetime) -> int:
    """Convert a datetime (assumed UTC if naive) to Unix-ms integer."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)


def parse_client_ts(text: str) -> datetime:
    """Parse the ISO-8601 TEXT representation we store for ``client_ts``."""
    # ``fromisoformat`` handles ``+00:00`` natively in 3.11+; we wrote it that
    # way ourselves so this is a round-trip.
    return datetime.fromisoformat(text)


# ── Row → model adapters ───────────────────────────────────
def row_to_datapoint_stored(row: sqlite3.Row, session_id: str | None = None) -> DataPointStored:
    """Build a ``DataPointStored`` from a ``datapoints`` row.

    ``session_id`` may be supplied explicitly when the SELECT did not include
    that column (some queries select only the cell-relevant fields).
    """
    sid = session_id if session_id is not None else row["session_id"]
    return DataPointStored(
        session_id=sid,
        chart_id=row["chart_id"],
        group_key=row["group_key"],
        metric_key=row["metric_key"],
        value=float(row["value"]),
        client_ts=parse_client_ts(row["client_ts"]),
        server_ts=ms_to_datetime(int(row["server_ts"])),
        seq=int(row["seq"]),
    )


__all__ = [
    "connect",
    "migrate",
    "now_ms",
    "ms_to_datetime",
    "datetime_to_ms",
    "parse_client_ts",
    "row_to_datapoint_stored",
]

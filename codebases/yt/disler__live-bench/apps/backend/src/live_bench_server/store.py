"""Repository layer over ``db.py``.

Every public function takes an explicit ``sqlite3.Connection`` so tests can
spin up an in-memory / tmp_path DB per test. All writes are wrapped in
``BEGIN IMMEDIATE`` → ``COMMIT`` to take SQLite's write lock exactly once per
logical operation (matters for ``insert_points`` where ``seq`` must be
monotonic).
"""

from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime, timezone
from typing import Any

from live_bench_server.db import (
    datetime_to_ms,
    ms_to_datetime,
    now_ms,
    parse_client_ts,
    row_to_datapoint_stored,
)
from live_bench_server.models import (
    BenchmarkConfig,
    CompletionRef,
    DataPoint,
    DataPointStored,
    DatasetState,
    GroupMetadata,
)


# A process-wide write lock. SQLite has its own, but taking this lock in
# Python-land guarantees that ``insert_points`` sees a stable max(seq) even
# under highly concurrent FastAPI request handling.
_WRITE_LOCK = threading.Lock()


# ── Benchmarks ─────────────────────────────────────────────
def upsert_benchmark(
    conn: sqlite3.Connection,
    cfg: BenchmarkConfig,
    source_path: str | None,
) -> None:
    """Insert or update a benchmark row keyed by ``session_id``.

    Serialises the full ``BenchmarkConfig`` into ``config_json``; denormalises
    ``title``, ``subtitle``, ``better`` onto the row so ``GET /benchmarks`` can
    cheaply include them without deserialising the config.

    For multi-chart benchmarks there is no single ``better`` — we denormalise
    the first chart's value for backwards-compat with the DB schema (which
    still has ``better TEXT NOT NULL``). The authoritative source is the
    serialised ``config_json`` column and ``list_benchmarks`` computes the
    correct per-summary ``better`` (nullable) from there.
    """
    config_json = cfg.model_dump_json()
    charts = cfg.all_charts()
    # Denormalised ``better`` for the DB row — falls back to the first chart.
    denorm_better = charts[0].better if charts else "higher"
    now = now_ms()
    with _WRITE_LOCK:
        conn.execute(
            """
            INSERT INTO benchmarks (
                session_id, title, subtitle, better, config_json, source_path,
                created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(session_id) DO UPDATE SET
                title       = excluded.title,
                subtitle    = excluded.subtitle,
                better      = excluded.better,
                config_json = excluded.config_json,
                source_path = excluded.source_path,
                updated_at  = excluded.updated_at
            """,
            (
                cfg.session_id,
                cfg.title,
                cfg.subtitle,
                denorm_better,
                config_json,
                source_path,
                now,
                now,
            ),
        )


def get_benchmark(conn: sqlite3.Connection, session_id: str) -> BenchmarkConfig | None:
    """Load the full ``BenchmarkConfig`` for a session, or ``None`` if missing."""
    row = conn.execute(
        "SELECT config_json FROM benchmarks WHERE session_id = ?",
        (session_id,),
    ).fetchone()
    if row is None:
        return None
    return BenchmarkConfig.model_validate_json(row["config_json"])


def list_benchmarks(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Return one summary dict per benchmark for ``GET /benchmarks``.

    Each dict carries surface fields (``session_id``, ``title``, ``subtitle``,
    ``better``, ``chart_count``) plus derived counts (``completed_count``,
    ``total_count``) and ``last_update`` (ISO-8601 microsecond string or
    ``None``).

    ``better`` is nullable: set to the single chart's ``better`` when the
    benchmark has exactly one chart, otherwise ``None`` (multi-chart
    benchmarks don't have a single answer — each chart has its own).
    """
    rows = conn.execute(
        """
        SELECT session_id, title, subtitle, better, config_json
        FROM benchmarks
        ORDER BY session_id ASC
        """
    ).fetchall()

    out: list[dict[str, Any]] = []
    for row in rows:
        sid = row["session_id"]
        cfg = BenchmarkConfig.model_validate_json(row["config_json"])
        charts = cfg.all_charts()
        chart_count = len(charts)
        total = sum(len(c.groups or []) for c in charts)
        completed_count = conn.execute(
            "SELECT COUNT(*) AS c FROM completions WHERE session_id = ?",
            (sid,),
        ).fetchone()["c"]
        last_update_row = conn.execute(
            "SELECT MAX(client_ts) AS ts FROM datapoints WHERE session_id = ?",
            (sid,),
        ).fetchone()
        last_update = last_update_row["ts"] if last_update_row else None
        # For single-chart benchmarks, ``better`` is the chart's own better.
        # For multi-chart benchmarks, return None — no single answer.
        better = charts[0].better if chart_count == 1 else None
        out.append(
            {
                "session_id": sid,
                "title": row["title"],
                "subtitle": row["subtitle"],
                "better": better,
                "chart_count": chart_count,
                "completed_count": int(completed_count),
                "total_count": total,
                "last_update": last_update,
            }
        )
    return out


def reset(conn: sqlite3.Connection, session_id: str) -> None:
    """Delete all datapoints + completions for a session; bump ``updated_at``.

    The ``benchmarks`` row itself is preserved — config is owned by YAML.
    """
    now = now_ms()
    with _WRITE_LOCK:
        conn.execute("BEGIN IMMEDIATE")
        try:
            conn.execute("DELETE FROM datapoints WHERE session_id = ?", (session_id,))
            conn.execute("DELETE FROM completions WHERE session_id = ?", (session_id,))
            conn.execute("DELETE FROM metadata WHERE session_id = ?", (session_id,))
            conn.execute(
                "UPDATE benchmarks SET updated_at = ? WHERE session_id = ?",
                (now, session_id),
            )
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise


# ── Metadata ──────────────────────────────────────────────

def _deep_merge(existing: dict, new: dict) -> dict:
    """Merge new into existing. For nested dicts (like 'responses'), merge recursively."""
    for k, v in new.items():
        if k in existing and isinstance(existing[k], dict) and isinstance(v, dict):
            existing[k].update(v)
        else:
            existing[k] = v
    return existing


def upsert_metadata(
    conn: sqlite3.Connection,
    session_id: str,
    entries: list[GroupMetadata],
) -> list[tuple[str, str, dict]]:
    """Upsert metadata for one or more (chart, group) pairs.

    Returns a list of ``(chart_id, group_key, merged_data)`` for each entry
    so the caller can broadcast SSE events with the merged result.
    """
    if not entries:
        return []

    now = now_ms()
    results: list[tuple[str, str, dict]] = []

    with _WRITE_LOCK:
        conn.execute("BEGIN IMMEDIATE")
        try:
            for entry in entries:
                # Read existing
                row = conn.execute(
                    "SELECT data_json FROM metadata WHERE session_id = ? AND chart_id = ? AND group_key = ?",
                    (session_id, entry.chart_id, entry.group_key),
                ).fetchone()

                if row:
                    existing = json.loads(row["data_json"])
                    merged = _deep_merge(existing, entry.data)
                else:
                    merged = dict(entry.data)

                conn.execute(
                    """
                    INSERT INTO metadata (session_id, chart_id, group_key, data_json, updated_at)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(session_id, chart_id, group_key)
                    DO UPDATE SET data_json = excluded.data_json, updated_at = excluded.updated_at
                    """,
                    (session_id, entry.chart_id, entry.group_key, json.dumps(merged), now),
                )
                results.append((entry.chart_id, entry.group_key, merged))

            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise

    return results


def get_all_metadata(conn: sqlite3.Connection, session_id: str) -> dict[str, dict]:
    """Return all metadata for a session as ``{"chart_id:group_key": data_dict, ...}``."""
    rows = conn.execute(
        "SELECT chart_id, group_key, data_json FROM metadata WHERE session_id = ?",
        (session_id,),
    ).fetchall()
    return {
        f"{row['chart_id']}:{row['group_key']}": json.loads(row["data_json"])
        for row in rows
    }


# ── Datapoints ─────────────────────────────────────────────
def _client_ts_text(value: datetime) -> str:
    """Render a Pydantic ``client_ts`` field back to its wire TEXT form."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    else:
        value = value.astimezone(timezone.utc)
    return value.isoformat(timespec="microseconds")


def insert_points(
    conn: sqlite3.Connection,
    session_id: str,
    points: list[DataPoint],
) -> list[DataPointStored]:
    """Insert a batch of datapoints and return their stored forms.

    Assigns ``seq`` monotonically as ``current_max + 1, +2, +3, ...`` inside a
    single write lock so concurrent POST /ingest calls cannot interleave and
    end up with duplicate or reversed seqs. Stamps ``server_ts`` once at the
    top of the call — the entire batch shares the same arrival time.
    """
    if not points:
        return []

    server_ts_dt = datetime.now(timezone.utc)
    server_ts_ms = datetime_to_ms(server_ts_dt)

    with _WRITE_LOCK:
        conn.execute("BEGIN IMMEDIATE")
        try:
            row = conn.execute(
                "SELECT COALESCE(MAX(seq), 0) AS m FROM datapoints WHERE session_id = ?",
                (session_id,),
            ).fetchone()
            next_seq = int(row["m"]) + 1

            stored: list[DataPointStored] = []
            rows_to_insert: list[tuple[Any, ...]] = []
            for i, p in enumerate(points):
                seq = next_seq + i
                ct_text = _client_ts_text(p.client_ts)
                rows_to_insert.append(
                    (
                        session_id,
                        p.chart_id,
                        p.group_key,
                        p.metric_key,
                        float(p.value),
                        seq,
                        ct_text,
                        server_ts_ms,
                    )
                )
                stored.append(
                    DataPointStored(
                        session_id=session_id,
                        chart_id=p.chart_id,
                        group_key=p.group_key,
                        metric_key=p.metric_key,
                        value=float(p.value),
                        client_ts=p.client_ts,
                        server_ts=server_ts_dt,
                        seq=seq,
                    )
                )

            conn.executemany(
                """
                INSERT INTO datapoints
                    (session_id, chart_id, group_key, metric_key, value, seq, client_ts, server_ts)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows_to_insert,
            )
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise

    return stored


# ── Completions ────────────────────────────────────────────
def mark_complete(
    conn: sqlite3.Connection,
    session_id: str,
    refs: list[CompletionRef] | list[str],
) -> list[tuple[CompletionRef, datetime]]:
    """UPSERT completion rows; return ``(CompletionRef, completed_at)`` per ref.

    Uses a single server timestamp for the whole batch so all completions
    from one request share the same wall-clock.

    For backward compatibility callers may pass a ``list[str]`` of bare group
    keys — each is coerced to a default-chart ``CompletionRef``.
    """
    if not refs:
        return []

    # Backward compat: coerce bare strings to default-chart CompletionRefs.
    normalized: list[CompletionRef] = []
    for ref in refs:
        if isinstance(ref, str):
            normalized.append(CompletionRef(chart_id="default", group_key=ref))
        else:
            normalized.append(ref)

    completed_at_dt = datetime.now(timezone.utc)
    completed_at_ms = datetime_to_ms(completed_at_dt)

    with _WRITE_LOCK:
        conn.execute("BEGIN IMMEDIATE")
        try:
            for ref in normalized:
                conn.execute(
                    """
                    INSERT INTO completions (session_id, chart_id, group_key, completed_at)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(session_id, chart_id, group_key) DO UPDATE SET
                        completed_at = excluded.completed_at
                    """,
                    (session_id, ref.chart_id, ref.group_key, completed_at_ms),
                )
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise

    return [(ref, completed_at_dt) for ref in normalized]


# ── Derived views ──────────────────────────────────────────
def dataset_states(
    conn: sqlite3.Connection,
    session_id: str,
    cfg: BenchmarkConfig | None = None,
) -> list[DatasetState]:
    """Return one ``DatasetState`` per ``(chart, group)`` pair defined in the config.

    Status derivation (spec §4.1, chart-aware):
      - ``complete``  → a row exists in ``completions`` for that (chart, group).
      - ``running``   → no completion row, at least one datapoint for that
                        (chart, group).
      - ``pending``   → neither a completion row nor any datapoints.

    ``started_at`` = min(``client_ts``) for that (chart, group) triple.
    ``completed_at`` = the completions row's ``completed_at``.

    ``cfg`` is optional — if not supplied it is loaded from the DB. Callers
    that already have the config should pass it in to avoid a second round
    trip.
    """
    if cfg is None:
        cfg = get_benchmark(conn, session_id)
    if cfg is None:
        return []

    completions: dict[tuple[str, str], int] = {
        (row["chart_id"], row["group_key"]): int(row["completed_at"])
        for row in conn.execute(
            "SELECT chart_id, group_key, completed_at FROM completions WHERE session_id = ?",
            (session_id,),
        ).fetchall()
    }

    started_rows = conn.execute(
        """
        SELECT chart_id, group_key, MIN(client_ts) AS started
        FROM datapoints
        WHERE session_id = ?
        GROUP BY chart_id, group_key
        """,
        (session_id,),
    ).fetchall()
    started_map: dict[tuple[str, str], str | None] = {
        (row["chart_id"], row["group_key"]): row["started"] for row in started_rows
    }

    states: list[DatasetState] = []
    for chart in cfg.all_charts():
        cid = chart.chart_id
        for group in (chart.groups or []):
            gk = group.key
            key = (cid, gk)
            started_text = started_map.get(key)
            if key in completions:
                status = "complete"
            elif started_text is not None:
                status = "running"
            else:
                status = "pending"

            started_dt = parse_client_ts(started_text) if started_text else None
            completed_dt = (
                ms_to_datetime(completions[key]) if key in completions else None
            )
            states.append(
                DatasetState(
                    chart_id=cid,
                    group_key=gk,
                    status=status,
                    started_at=started_dt,
                    completed_at=completed_dt,
                )
            )
    return states


def latest_per_cell(conn: sqlite3.Connection, session_id: str) -> list[DataPointStored]:
    """Return the newest-by-``client_ts`` datapoint for each (chart, group, metric) cell.

    Uses the ``ix_datapoints_cell_client_ts`` index. Cells with no data are
    skipped — the snapshot only carries cells that have at least one point.
    Out-of-order ``client_ts`` inserts still produce the newest one per cell.
    """
    rows = conn.execute(
        """
        SELECT d.chart_id, d.group_key, d.metric_key, d.value, d.seq, d.client_ts, d.server_ts
        FROM datapoints d
        WHERE d.session_id = ?
          AND d.id = (
              SELECT d2.id
              FROM datapoints d2
              WHERE d2.session_id = d.session_id
                AND d2.chart_id   = d.chart_id
                AND d2.group_key  = d.group_key
                AND d2.metric_key = d.metric_key
              ORDER BY d2.client_ts DESC, d2.id DESC
              LIMIT 1
          )
        ORDER BY d.chart_id ASC, d.group_key ASC, d.metric_key ASC
        """,
        (session_id,),
    ).fetchall()
    return [row_to_datapoint_stored(r, session_id=session_id) for r in rows]


def max_seq(conn: sqlite3.Connection, session_id: str) -> int:
    """Return the current max ``seq`` for a session, or 0 if empty."""
    row = conn.execute(
        "SELECT COALESCE(MAX(seq), 0) AS m FROM datapoints WHERE session_id = ?",
        (session_id,),
    ).fetchone()
    return int(row["m"]) if row else 0


def points_after_seq(
    conn: sqlite3.Connection,
    session_id: str,
    last_seq: int,
) -> list[DataPointStored]:
    """Return all datapoints for a session with ``seq > last_seq``, in seq order.

    Used by the SSE stream to replay missed events after a ``Last-Event-ID``
    reconnect.
    """
    rows = conn.execute(
        """
        SELECT chart_id, group_key, metric_key, value, seq, client_ts, server_ts
        FROM datapoints
        WHERE session_id = ? AND seq > ?
        ORDER BY seq ASC
        """,
        (session_id, last_seq),
    ).fetchall()
    return [row_to_datapoint_stored(r, session_id=session_id) for r in rows]


__all__ = [
    "upsert_benchmark",
    "get_benchmark",
    "list_benchmarks",
    "reset",
    "insert_points",
    "mark_complete",
    "dataset_states",
    "latest_per_cell",
    "max_seq",
    "points_after_seq",
]

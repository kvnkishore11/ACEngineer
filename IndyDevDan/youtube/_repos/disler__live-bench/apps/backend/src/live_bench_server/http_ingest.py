"""POST /ingest — HTTP ingestion handler.

Validates the incoming batch against the live ``BenchmarkConfig``, stamps
``seq`` + ``server_ts`` on each point via ``store.insert_points``, broadcasts
one ``SseDatapoint`` per stored point, and (if present) marks groups complete
and broadcasts one ``SseDatasetComplete`` per group.

Validation errors return the exact ``{code, message}`` shapes from spec §9.1.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse

from live_bench_server import store
from live_bench_server.logging import get_logger
from live_bench_server.models import (
    IngestRequest,
    IngestResponse,
    SseDatapoint,
    SseDatasetComplete,
    SseMetadata,
)

log = get_logger(__name__)

router = APIRouter()

# Maximum tolerated skew between a point's client_ts and the server clock.
MAX_SKEW_SECONDS = 300  # ±5 minutes, per spec §6


def _err(code: str, message: str, http_status: int) -> JSONResponse:
    return JSONResponse(
        status_code=http_status,
        content={"code": code, "message": message},
    )


@router.post("/ingest")
async def ingest(request: Request, body: IngestRequest) -> JSONResponse:
    """Accept a batch of datapoints and/or group completions for a session."""
    conn = request.app.state.db
    broker = request.app.state.broker

    session_id = body.session_id
    cfg = store.get_benchmark(conn, session_id)
    if cfg is None:
        return _err(
            "unknown_session",
            f"session '{session_id}' not found",
            status.HTTP_404_NOT_FOUND,
        )

    # Build per-chart validation tables. Groups AND metrics are both per-chart,
    # so validation must look up the correct chart for each point/completion.
    charts_by_id = {chart.chart_id: chart for chart in cfg.all_charts()}
    # Per-chart group key set and case-insensitive canonicalization.
    group_keys_by_chart: dict[str, set[str]] = {
        cid: {g.key for g in (chart.groups or [])} for cid, chart in charts_by_id.items()
    }
    group_canon_by_chart: dict[str, dict[str, str]] = {
        cid: {g.key.lower(): g.key for g in (chart.groups or [])} for cid, chart in charts_by_id.items()
    }
    # Per-chart metric key set for chart-scoped metric validation.
    metric_keys_by_chart: dict[str, set[str]] = {
        cid: {m.key for m in chart.metrics} for cid, chart in charts_by_id.items()
    }

    now = datetime.now(timezone.utc)

    # Validate every point against the live config + clock skew.
    for i, p in enumerate(body.points):
        if p.chart_id not in charts_by_id:
            return _err(
                "unknown_chart",
                f"chart '{p.chart_id}' not in session '{session_id}' config",
                status.HTTP_400_BAD_REQUEST,
            )
        # Normalize group key to canonical casing from the chart's config.
        canonical = group_canon_by_chart.get(p.chart_id, {}).get(p.group_key.lower())
        if canonical is None:
            return _err(
                "unknown_group",
                f"group '{p.group_key}' not in session config",
                status.HTTP_400_BAD_REQUEST,
            )
        p.group_key = canonical
        if p.metric_key not in metric_keys_by_chart[p.chart_id]:
            return _err(
                "unknown_metric",
                f"metric '{p.metric_key}' not in chart '{p.chart_id}' config",
                status.HTTP_400_BAD_REQUEST,
            )
        # client_ts presence is already enforced by Pydantic (required field).
        client_ts = p.client_ts
        if client_ts.tzinfo is None:
            client_ts = client_ts.replace(tzinfo=timezone.utc)
        skew = (now - client_ts).total_seconds()
        if abs(skew) > MAX_SKEW_SECONDS:
            minutes = abs(skew) / 60.0
            direction = "behind" if skew > 0 else "ahead of"
            return _err(
                "clock_skew",
                f"point[{i}] client_ts is {minutes:.1f} min {direction} server — check NTP",
                status.HTTP_400_BAD_REQUEST,
            )

    # Validate every complete_groups entry (each entry is a CompletionRef).
    for ref in body.complete_groups:
        if ref.chart_id not in charts_by_id:
            return _err(
                "unknown_chart",
                f"chart '{ref.chart_id}' not in session '{session_id}' config",
                status.HTTP_400_BAD_REQUEST,
            )
        canonical = group_canon_by_chart.get(ref.chart_id, {}).get(ref.group_key.lower())
        if canonical is None:
            return _err(
                "unknown_group",
                f"group '{ref.group_key}' not in chart '{ref.chart_id}' config",
                status.HTTP_400_BAD_REQUEST,
            )
        ref.group_key = canonical

    # Insert and broadcast points.
    stored = store.insert_points(conn, session_id, body.points)
    for sp in stored:
        log.debug(
            "ingest point session=%s chart=%s group=%s metric=%s value=%s seq=%d",
            session_id,
            sp.chart_id,
            sp.group_key,
            sp.metric_key,
            sp.value,
            sp.seq,
        )
        broker.publish(session_id, SseDatapoint(session_id=session_id, point=sp))

    # Mark completions and broadcast.
    completed_pairs = store.mark_complete(conn, session_id, body.complete_groups)
    completed_keys: list[str] = []
    for ref, completed_at in completed_pairs:
        completed_keys.append(ref.group_key)
        broker.publish(
            session_id,
            SseDatasetComplete(
                session_id=session_id,
                chart_id=ref.chart_id,
                group_key=ref.group_key,
                completed_at=completed_at,
            ),
        )

    # Upsert metadata and broadcast.
    if body.metadata:
        # Validate and normalize group keys in metadata entries
        for entry in body.metadata:
            if entry.chart_id not in charts_by_id:
                return _err(
                    "unknown_chart",
                    f"chart '{entry.chart_id}' not in session '{session_id}' config",
                    status.HTTP_400_BAD_REQUEST,
                )
            canonical = group_canon_by_chart.get(entry.chart_id, {}).get(entry.group_key.lower())
            if canonical is None:
                return _err(
                    "unknown_group",
                    f"group '{entry.group_key}' not in session config",
                    status.HTTP_400_BAD_REQUEST,
                )
            entry.group_key = canonical

        merged_results = store.upsert_metadata(conn, session_id, body.metadata)
        for chart_id, group_key, merged_data in merged_results:
            broker.publish(
                session_id,
                SseMetadata(
                    session_id=session_id,
                    chart_id=chart_id,
                    group_key=group_key,
                    data=merged_data,
                ),
            )

    resp = IngestResponse(
        accepted=len(stored),
        seq_from=stored[0].seq if stored else None,
        seq_to=stored[-1].seq if stored else None,
        completed=completed_keys,
        server_ts=datetime.now(timezone.utc),
    )
    return JSONResponse(content=resp.model_dump(mode="json"))


__all__ = ["router", "MAX_SKEW_SECONDS"]

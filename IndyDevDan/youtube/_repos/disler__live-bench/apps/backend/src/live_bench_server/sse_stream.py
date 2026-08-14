"""GET /stream/{session_id} — SSE stream for a single benchmark session.

Emits:
  1. ``snapshot`` — initial full state (config + latest_per_cell + datasets).
  2. Optional replay of ``datapoint`` events if ``Last-Event-ID`` is present.
  3. Live ``datapoint`` / ``dataset_complete`` / ``reset`` / ``config_changed``
     events as they are published via the broker.

Heartbeat comments are emitted every 15 s via sse-starlette's ``ping=15``.

Each SSE frame carries an ``id:`` field set to the most recent datapoint
``seq`` we have seen, so that browsers can resume with ``Last-Event-ID``.
Non-datapoint events reuse the last-seen seq (or 0 if nothing yet).
"""

from __future__ import annotations

import asyncio

from fastapi import APIRouter, HTTPException, Request, status
from sse_starlette.sse import EventSourceResponse

from live_bench_server import store
from live_bench_server.logging import get_logger
from live_bench_server.models import (
    SseDatapoint,
    SseDatasetComplete,
    SseMetadata,
    SseReset,
    SseSnapshot,
)

log = get_logger(__name__)

router = APIRouter()


@router.get("/stream/{session_id}")
async def stream(request: Request, session_id: str):
    """SSE endpoint for a single session."""
    conn = request.app.state.db
    broker = request.app.state.broker

    cfg = store.get_benchmark(conn, session_id)
    if cfg is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "unknown_session", "message": f"session '{session_id}' not found"},
        )

    last_event_id_header = request.headers.get("last-event-id")
    last_seq = 0
    if last_event_id_header:
        try:
            last_seq = int(last_event_id_header)
        except ValueError:
            last_seq = 0

    # Pre-build initial snapshot + replay list under a single read lock.
    snapshot_points = store.latest_per_cell(conn, session_id)
    snapshot_datasets = store.dataset_states(conn, session_id, cfg)
    snapshot_metadata = store.get_all_metadata(conn, session_id)
    current_max_seq = store.max_seq(conn, session_id)
    replay_points = (
        store.points_after_seq(conn, session_id, last_seq) if last_seq > 0 else []
    )

    # Subscribe BEFORE we yield the snapshot so no live events are lost.
    queue = broker.subscribe(session_id)

    async def event_generator():
        last_seq_seen = current_max_seq
        try:
            # 1. Snapshot
            snapshot = SseSnapshot(
                session_id=session_id,
                config=cfg,
                points=snapshot_points,
                datasets=snapshot_datasets,
            )
            yield {
                "event": "snapshot",
                "id": str(last_seq_seen),
                "data": snapshot.model_dump_json(),
            }

            # 1b. Emit existing metadata entries after snapshot.
            for key, data in snapshot_metadata.items():
                chart_id, group_key = key.split(":", 1)
                meta_evt = SseMetadata(
                    session_id=session_id,
                    chart_id=chart_id,
                    group_key=group_key,
                    data=data,
                )
                yield {
                    "event": "metadata",
                    "id": str(last_seq_seen),
                    "data": meta_evt.model_dump_json(),
                }

            # 2. Replay missed datapoints if a Last-Event-ID was supplied.
            for sp in replay_points:
                evt = SseDatapoint(session_id=session_id, point=sp)
                last_seq_seen = max(last_seq_seen, sp.seq)
                yield {
                    "event": "datapoint",
                    "id": str(sp.seq),
                    "data": evt.model_dump_json(),
                }

            # 3. Live events from the broker.
            while True:
                if await request.is_disconnected():
                    break
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=1.0)
                except asyncio.TimeoutError:
                    continue

                if isinstance(event, SseDatapoint):
                    last_seq_seen = max(last_seq_seen, event.point.seq)
                    yield {
                        "event": "datapoint",
                        "id": str(event.point.seq),
                        "data": event.model_dump_json(),
                    }
                elif isinstance(event, SseDatasetComplete):
                    yield {
                        "event": "dataset_complete",
                        "id": str(last_seq_seen),
                        "data": event.model_dump_json(),
                    }
                elif isinstance(event, SseReset):
                    last_seq_seen = 0
                    yield {
                        "event": "reset",
                        "id": "0",
                        "data": event.model_dump_json(),
                    }
                else:
                    # Unknown event — fall back to the declared ``event`` attr.
                    event_name = getattr(event, "event", "message")
                    yield {
                        "event": event_name,
                        "id": str(last_seq_seen),
                        "data": event.model_dump_json(),
                    }
        except asyncio.CancelledError:
            # Client disconnected; fall through to cleanup.
            raise
        finally:
            broker.unsubscribe(session_id, queue)

    return EventSourceResponse(event_generator(), ping=15)


__all__ = ["router"]

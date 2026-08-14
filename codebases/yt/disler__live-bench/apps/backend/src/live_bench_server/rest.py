"""REST endpoints for live-bench.

* ``GET  /benchmarks``                      — list all benchmarks (landing page)
* ``GET  /benchmarks/{session_id}``         — config + latest points + datasets
* ``POST /benchmarks/{session_id}/reset``   — clear datapoints & completions
* ``GET  /healthz``                         — liveness probe

Per spec §13, **no POST /benchmarks** — benchmark creation is YAML-only.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse

from live_bench_server import store
from live_bench_server.logging import get_logger
from live_bench_server.models import SseReset

log = get_logger(__name__)

router = APIRouter()


@router.get("/healthz")
async def healthz() -> dict[str, bool]:
    return {"ok": True}


@router.post("/ping")
async def ping(request: Request) -> dict[str, bool]:
    """Broadcast a ping event to all active SSE subscribers."""
    from live_bench_server.models import SsePing

    broker = request.app.state.broker
    broker.broadcast_all(SsePing())
    return {"ok": True}


@router.get("/benchmarks")
async def list_benchmarks(request: Request) -> dict[str, list[dict]]:
    conn = request.app.state.db
    items = store.list_benchmarks(conn)
    return {"benchmarks": items}


@router.get("/benchmarks/{session_id}")
async def get_benchmark(request: Request, session_id: str) -> JSONResponse:
    conn = request.app.state.db
    cfg = store.get_benchmark(conn, session_id)
    if cfg is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": "unknown_session",
                "message": f"session '{session_id}' not found",
            },
        )
    points = store.latest_per_cell(conn, session_id)
    datasets = store.dataset_states(conn, session_id, cfg)
    metadata = store.get_all_metadata(conn, session_id)
    payload = {
        "config": cfg.model_dump(mode="json"),
        "points": [p.model_dump(mode="json") for p in points],
        "datasets": [d.model_dump(mode="json") for d in datasets],
        "metadata": metadata,
    }
    return JSONResponse(content=payload)


@router.post("/benchmarks/{session_id}/reset")
async def reset_benchmark(request: Request, session_id: str) -> JSONResponse:
    conn = request.app.state.db
    broker = request.app.state.broker

    cfg = store.get_benchmark(conn, session_id)
    if cfg is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": "unknown_session",
                "message": f"session '{session_id}' not found",
            },
        )

    store.reset(conn, session_id)
    broker.publish(session_id, SseReset(session_id=session_id))
    log.info("reset benchmark session_id=%s", session_id)
    return JSONResponse(content={"reset": True, "session_id": session_id})


__all__ = ["router"]

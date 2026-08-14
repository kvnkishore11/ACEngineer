"""FastAPI application factory for live-bench.

Responsibilities:
  * Open the SQLite database (path from ``LIVEBENCH_DB_PATH`` env var, default
    ``./live-bench.db``) and run the spec §4.1 migration.
  * Load every YAML file under ``benchmarks/`` (path from
    ``LIVEBENCH_BENCHMARKS_DIR``, default ``../../benchmarks`` relative to
    ``apps/backend``) and upsert each into the DB.
  * Instantiate the in-process broker and stash it on ``app.state``.
  * Mount the three routers (``rest``, ``sse_stream``, ``http_ingest``).

Entry point:
  ``uvicorn live_bench_server.main:app --port 8787``
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from live_bench_server import config as config_loader
from live_bench_server import db, store
from live_bench_server.broker import LiveBroker
from live_bench_server.http_ingest import router as ingest_router
from live_bench_server.logging import get_logger
from live_bench_server.rest import router as rest_router
from live_bench_server.sse_stream import router as sse_router

log = get_logger("live_bench_server.main")


def _default_benchmarks_dir() -> Path:
    """Resolve the default benchmarks directory relative to apps/backend.

    ``apps/backend/src/live_bench_server/main.py`` → go up 4 parents to reach
    the repo root, then into ``benchmarks/``. Overridable via the
    ``LIVEBENCH_BENCHMARKS_DIR`` env var (used by tests + smoke runs).
    """
    here = Path(__file__).resolve()
    # .../apps/backend/src/live_bench_server/main.py
    # parents: [live_bench_server, src, backend, apps, repo_root]
    repo_root = here.parents[4]
    return repo_root / "benchmarks"


def _resolve_paths() -> tuple[Path, Path]:
    db_path = Path(os.environ.get("LIVEBENCH_DB_PATH", "./live-bench.db")).resolve()
    bm_env = os.environ.get("LIVEBENCH_BENCHMARKS_DIR")
    bm_dir = Path(bm_env).resolve() if bm_env else _default_benchmarks_dir()
    return db_path, bm_dir


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_path, bm_dir = _resolve_paths()
    log.info("opening database at %s", db_path)
    conn = db.connect(db_path)
    db.migrate(conn)

    log.info("loading benchmarks from %s", bm_dir)
    try:
        files = config_loader.load_benchmarks_dir(bm_dir)
    except ValueError as exc:
        log.error("failed to load benchmarks dir: %s", exc)
        files = []

    for parsed, source in files:
        # A YAML file may define one benchmark (`benchmark:`) or many
        # (`benchmarks:`). all_benchmarks() flattens both shapes to a list.
        for cfg in parsed.all_benchmarks():
            store.upsert_benchmark(conn, cfg, source_path=str(source))
            log.info(
                "reconciled benchmark session_id=%s source=%s",
                cfg.session_id,
                source.name,
            )

    broker = LiveBroker()

    app.state.db = conn
    app.state.broker = broker
    app.state.db_path = db_path
    app.state.benchmarks_dir = bm_dir

    try:
        yield
    finally:
        log.info("shutting down live-bench backend")
        await broker.drain()
        try:
            conn.close()
        except Exception:
            pass


def create_app() -> FastAPI:
    app = FastAPI(title="live-bench", lifespan=lifespan)
    app.include_router(rest_router)
    app.include_router(ingest_router)
    app.include_router(sse_router)
    return app


app = create_app()


__all__ = ["app", "create_app", "lifespan"]

"""Shared pytest fixtures for the backend test suite.

Provides:
  * ``tmp_db`` — an isolated sqlite3 connection against a tmp_path DB file.
  * ``sample_config`` — a realistic ``BenchmarkConfig`` for seeding tests.
  * ``seeded_db`` — ``tmp_db`` with the sample config already upserted.
  * ``client`` — a FastAPI ``TestClient`` bound to an isolated DB + broker.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from live_bench_server import db, store
from live_bench_server.broker import LiveBroker
from live_bench_server.models import (
    AxisConfig,
    BenchmarkConfig,
    GroupDef,
    MetricDef,
)


SAMPLE_SESSION_ID = "test-session"


def build_sample_config(session_id: str = SAMPLE_SESSION_ID) -> BenchmarkConfig:
    """Build a compact but complete ``BenchmarkConfig`` for tests."""
    return BenchmarkConfig(
        session_id=session_id,
        title="Test Benchmark",
        subtitle="Two groups · two metrics",
        better="higher",
        direction="BT",
        x=AxisConfig(label="Worker"),
        y=AxisConfig(label="Throughput", unit="req/s", min=0),
        metrics=[
            MetricDef(key="throughput", label="Throughput", color="#10b981"),
            MetricDef(key="latency", label="Latency", color="#f59e0b"),
        ],
        groups=[
            GroupDef(key="alpha", label="Alpha"),
            GroupDef(key="beta", label="Beta"),
        ],
    )


@pytest.fixture()
def tmp_db(tmp_path: Path) -> sqlite3.Connection:
    path = tmp_path / "live-bench.db"
    conn = db.connect(path)
    db.migrate(conn)
    yield conn
    conn.close()


@pytest.fixture()
def sample_config() -> BenchmarkConfig:
    return build_sample_config()


@pytest.fixture()
def seeded_db(tmp_db: sqlite3.Connection, sample_config: BenchmarkConfig) -> sqlite3.Connection:
    store.upsert_benchmark(tmp_db, sample_config, source_path="test://sample.yaml")
    return tmp_db


@pytest.fixture()
def client(tmp_path: Path, monkeypatch):
    """Return a FastAPI TestClient bound to an isolated DB + broker.

    We monkeypatch ``LIVEBENCH_DB_PATH`` so the lifespan opens the temp DB,
    then point the benchmarks dir at an empty tmp dir so no YAMLs are loaded
    on startup — tests seed the DB manually via ``store.upsert_benchmark``
    after the app starts.
    """
    db_path = tmp_path / "live-bench.db"
    empty_bm_dir = tmp_path / "benchmarks"
    empty_bm_dir.mkdir()

    monkeypatch.setenv("LIVEBENCH_DB_PATH", str(db_path))
    monkeypatch.setenv("LIVEBENCH_BENCHMARKS_DIR", str(empty_bm_dir))

    # Import late so env vars are picked up by ``_resolve_paths`` at lifespan
    # time. FastAPI's TestClient runs the lifespan when used as a context
    # manager.
    from live_bench_server.main import create_app

    app = create_app()

    with TestClient(app) as c:
        # Seed a sample benchmark after startup so the lifespan's migrate() has
        # already run against the temp DB.
        store.upsert_benchmark(
            app.state.db,
            build_sample_config(),
            source_path="test://sample.yaml",
        )
        c.app_state = app.state  # type: ignore[attr-defined]
        yield c

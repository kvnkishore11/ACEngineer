"""Integration tests for GET /stream/{session_id}.

These tests spin up a real Uvicorn server on an ephemeral port in a background
thread and use the regular synchronous ``httpx`` client to exercise SSE. This
is more reliable than FastAPI's ``TestClient.stream`` for long-lived
generators with periodic pings — the TestClient tends to buffer the first
chunk and deadlock waiting for more bytes before returning any to the caller.
"""

from __future__ import annotations

import json
import socket
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx
import pytest
import uvicorn

from live_bench_server import store
from live_bench_server.main import create_app
from live_bench_server.models import (
    AxisConfig,
    BenchmarkConfig,
    ChartDef,
    GroupDef,
    MetricDef,
)

from tests.conftest import SAMPLE_SESSION_ID, build_sample_config


MULTI_SESSION_ID = "multi-session"


def _build_multichart_config(session_id: str = MULTI_SESSION_ID) -> BenchmarkConfig:
    groups = [
        GroupDef(key="faiss", label="FAISS"),
        GroupDef(key="qdrant", label="Qdrant"),
    ]
    return BenchmarkConfig(
        session_id=session_id,
        title="Multi Chart Bench",
        subtitle="Two charts, two groups",
        charts=[
            ChartDef(
                chart_id="recall",
                title="Recall@10",
                better="higher",
                direction="BT",
                x=AxisConfig(label="Backend"),
                y=AxisConfig(label="Recall@10", min=0, max=1),
                metrics=[MetricDef(key="recall", label="Recall@10")],
                groups=groups,
            ),
            ChartDef(
                chart_id="latency",
                title="p99 Query Latency",
                better="lower",
                direction="LR",
                x=AxisConfig(label="Latency", unit="ms", min=0),
                y=AxisConfig(label="Backend"),
                metrics=[MetricDef(key="p99_ms", label="p99")],
                groups=groups,
            ),
        ],
    )


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture()
def live_server(tmp_path: Path, monkeypatch):
    """Start a real Uvicorn server in a daemon thread; seed a sample session."""
    db_path = tmp_path / "live-bench.db"
    empty_bm_dir = tmp_path / "benchmarks"
    empty_bm_dir.mkdir()
    monkeypatch.setenv("LIVEBENCH_DB_PATH", str(db_path))
    monkeypatch.setenv("LIVEBENCH_BENCHMARKS_DIR", str(empty_bm_dir))

    app = create_app()
    port = _free_port()
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=port,
        log_level="warning",
        access_log=False,
    )
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    base_url = f"http://127.0.0.1:{port}"

    # Wait for the server to become ready (poll /healthz).
    deadline = time.monotonic() + 10.0
    while time.monotonic() < deadline:
        try:
            r = httpx.get(f"{base_url}/healthz", timeout=0.5)
            if r.status_code == 200:
                break
        except Exception:
            pass
        time.sleep(0.05)
    else:
        raise RuntimeError("uvicorn did not come up in time")

    # Seed a sample session after the lifespan has run.
    store.upsert_benchmark(
        app.state.db,
        build_sample_config(),
        source_path="test://sample.yaml",
    )
    # Also seed a multi-chart session so the chart-aware tests have a target.
    store.upsert_benchmark(
        app.state.db,
        _build_multichart_config(),
        source_path="test://multi.yaml",
    )

    yield base_url

    server.should_exit = True
    thread.join(timeout=5)


def _iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat(timespec="microseconds")


def _parse_events(
    response,
    stop_after: int,
    timeout: float = 5.0,
) -> list[dict]:
    """Read ``stop_after`` SSE frames from an ``httpx`` streaming response.

    Ignores heartbeat comment lines (``: ping``). Returns a list of dicts with
    ``event``, ``id``, and ``data`` (JSON-parsed) keys.
    """
    events: list[dict] = []
    current_event: str | None = None
    current_id: str | None = None
    data_lines: list[str] = []
    deadline = time.monotonic() + timeout

    for raw in response.iter_lines():
        if time.monotonic() > deadline:
            raise AssertionError(
                f"Timed out after {timeout}s; got {len(events)} events so far: {events}"
            )
        line = raw if isinstance(raw, str) else raw.decode("utf-8", errors="replace")
        line = line.rstrip("\r")

        if line == "":
            if current_event is not None and data_lines:
                data_text = "\n".join(data_lines)
                try:
                    parsed = json.loads(data_text)
                except json.JSONDecodeError:
                    parsed = {"_raw": data_text}
                events.append({"event": current_event, "id": current_id, "data": parsed})
            current_event = None
            current_id = None
            data_lines = []
            if len(events) >= stop_after:
                return events
            continue

        if line.startswith(":"):
            continue
        if line.startswith("event:"):
            current_event = line[len("event:") :].strip()
        elif line.startswith("id:"):
            current_id = line[len("id:") :].strip()
        elif line.startswith("data:"):
            data_lines.append(line[len("data:") :].lstrip(" "))

    return events


def test_snapshot_on_connect(live_server):
    with httpx.stream("GET", f"{live_server}/stream/{SAMPLE_SESSION_ID}", timeout=5.0) as r:
        assert r.status_code == 200
        events = _parse_events(r, stop_after=1, timeout=3.0)
    assert len(events) == 1
    assert events[0]["event"] == "snapshot"
    data = events[0]["data"]
    assert data["session_id"] == SAMPLE_SESSION_ID
    assert "config" in data
    assert "points" in data
    assert "datasets" in data
    assert len(data["datasets"]) == 2
    assert {d["group_key"] for d in data["datasets"]} == {"alpha", "beta"}


def test_datapoint_after_ingest(live_server):
    def worker():
        time.sleep(0.25)
        now = datetime.now(timezone.utc)
        httpx.post(
            f"{live_server}/ingest",
            json={
                "session_id": SAMPLE_SESSION_ID,
                "request_ts": _iso(now),
                "points": [
                    {
                        "group_key": "alpha",
                        "metric_key": "throughput",
                        "value": 77.0,
                        "client_ts": _iso(now),
                    }
                ],
            },
            timeout=5.0,
        )

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    try:
        with httpx.stream(
            "GET",
            f"{live_server}/stream/{SAMPLE_SESSION_ID}",
            timeout=5.0,
        ) as r:
            events = _parse_events(r, stop_after=2, timeout=5.0)
    finally:
        t.join(timeout=2)
    assert events[0]["event"] == "snapshot"
    assert events[1]["event"] == "datapoint"
    point = events[1]["data"]["point"]
    assert point["group_key"] == "alpha"
    assert point["value"] == 77.0
    assert point["seq"] == 1


def test_dataset_complete_event(live_server):
    def worker():
        time.sleep(0.25)
        now = datetime.now(timezone.utc)
        httpx.post(
            f"{live_server}/ingest",
            json={
                "session_id": SAMPLE_SESSION_ID,
                "request_ts": _iso(now),
                "points": [
                    {
                        "group_key": "alpha",
                        "metric_key": "throughput",
                        "value": 1.0,
                        "client_ts": _iso(now),
                    }
                ],
                "complete_groups": ["alpha"],
            },
            timeout=5.0,
        )

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    try:
        with httpx.stream(
            "GET",
            f"{live_server}/stream/{SAMPLE_SESSION_ID}",
            timeout=5.0,
        ) as r:
            events = _parse_events(r, stop_after=3, timeout=5.0)
    finally:
        t.join(timeout=2)
    kinds = [e["event"] for e in events]
    assert kinds[0] == "snapshot"
    assert "datapoint" in kinds
    assert "dataset_complete" in kinds
    complete_event = next(e for e in events if e["event"] == "dataset_complete")
    assert complete_event["data"]["group_key"] == "alpha"


def test_reset_event(live_server):
    now = datetime.now(timezone.utc)
    httpx.post(
        f"{live_server}/ingest",
        json={
            "session_id": SAMPLE_SESSION_ID,
            "request_ts": _iso(now),
            "points": [
                {
                    "group_key": "alpha",
                    "metric_key": "throughput",
                    "value": 9.0,
                    "client_ts": _iso(now),
                }
            ],
        },
        timeout=5.0,
    )

    def worker():
        time.sleep(0.25)
        httpx.post(f"{live_server}/benchmarks/{SAMPLE_SESSION_ID}/reset", timeout=5.0)

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    try:
        with httpx.stream(
            "GET",
            f"{live_server}/stream/{SAMPLE_SESSION_ID}",
            timeout=5.0,
        ) as r:
            events = _parse_events(r, stop_after=2, timeout=5.0)
    finally:
        t.join(timeout=2)
    assert events[0]["event"] == "snapshot"
    assert events[1]["event"] == "reset"
    assert events[1]["data"]["session_id"] == SAMPLE_SESSION_ID


def test_last_event_id_resume(live_server):
    now = datetime.now(timezone.utc)
    for v in (10.0, 20.0, 30.0):
        httpx.post(
            f"{live_server}/ingest",
            json={
                "session_id": SAMPLE_SESSION_ID,
                "request_ts": _iso(now),
                "points": [
                    {
                        "group_key": "alpha",
                        "metric_key": "throughput",
                        "value": v,
                        "client_ts": _iso(now),
                    }
                ],
            },
            timeout=5.0,
        )

    with httpx.stream(
        "GET",
        f"{live_server}/stream/{SAMPLE_SESSION_ID}",
        headers={"Last-Event-ID": "1"},
        timeout=5.0,
    ) as r:
        events = _parse_events(r, stop_after=3, timeout=5.0)

    assert events[0]["event"] == "snapshot"
    replayed = [e for e in events[1:] if e["event"] == "datapoint"]
    assert len(replayed) == 2
    seqs = [e["data"]["point"]["seq"] for e in replayed]
    assert seqs == [2, 3]


# ── Chart-aware tests ─────────────────────────────────────────────────────


def test_snapshot_carries_chart_id(live_server):
    """Multi-chart snapshot: every points entry and every datasets entry has chart_id."""
    # Seed one point into each chart so the snapshot has real data to show.
    now = datetime.now(timezone.utc)
    for chart_id, metric_key, value in (
        ("recall", "recall", 0.94),
        ("latency", "p99_ms", 42.0),
    ):
        httpx.post(
            f"{live_server}/ingest",
            json={
                "session_id": MULTI_SESSION_ID,
                "request_ts": _iso(now),
                "points": [
                    {
                        "chart_id": chart_id,
                        "group_key": "faiss",
                        "metric_key": metric_key,
                        "value": value,
                        "client_ts": _iso(now),
                    }
                ],
            },
            timeout=5.0,
        )

    with httpx.stream(
        "GET", f"{live_server}/stream/{MULTI_SESSION_ID}", timeout=5.0
    ) as r:
        events = _parse_events(r, stop_after=1, timeout=3.0)

    assert len(events) == 1
    snap = events[0]
    assert snap["event"] == "snapshot"
    data = snap["data"]

    # Every point carries chart_id.
    assert len(data["points"]) == 2
    chart_ids_in_points = {p["chart_id"] for p in data["points"]}
    assert chart_ids_in_points == {"recall", "latency"}

    # Every dataset carries chart_id; 2 charts × 2 groups = 4 entries.
    assert len(data["datasets"]) == 4
    pairs = {(d["chart_id"], d["group_key"]) for d in data["datasets"]}
    assert pairs == {
        ("recall", "faiss"),
        ("recall", "qdrant"),
        ("latency", "faiss"),
        ("latency", "qdrant"),
    }


def test_datapoint_event_carries_chart_id(live_server):
    """A live datapoint SSE event preserves the point's chart_id."""

    def worker():
        time.sleep(0.25)
        now = datetime.now(timezone.utc)
        httpx.post(
            f"{live_server}/ingest",
            json={
                "session_id": MULTI_SESSION_ID,
                "request_ts": _iso(now),
                "points": [
                    {
                        "chart_id": "recall",
                        "group_key": "qdrant",
                        "metric_key": "recall",
                        "value": 0.91,
                        "client_ts": _iso(now),
                    }
                ],
            },
            timeout=5.0,
        )

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    try:
        with httpx.stream(
            "GET",
            f"{live_server}/stream/{MULTI_SESSION_ID}",
            timeout=5.0,
        ) as r:
            events = _parse_events(r, stop_after=2, timeout=5.0)
    finally:
        t.join(timeout=2)
    assert events[0]["event"] == "snapshot"
    assert events[1]["event"] == "datapoint"
    point = events[1]["data"]["point"]
    assert point["chart_id"] == "recall"
    assert point["group_key"] == "qdrant"
    assert point["metric_key"] == "recall"
    assert point["value"] == 0.91


def test_dataset_complete_event_carries_chart_id(live_server):
    """dataset_complete events preserve chart_id so chart-specific pills flip."""

    def worker():
        time.sleep(0.25)
        now = datetime.now(timezone.utc)
        httpx.post(
            f"{live_server}/ingest",
            json={
                "session_id": MULTI_SESSION_ID,
                "request_ts": _iso(now),
                "points": [],
                "complete_groups": [
                    {"chart_id": "latency", "group_key": "faiss"}
                ],
            },
            timeout=5.0,
        )

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    try:
        with httpx.stream(
            "GET",
            f"{live_server}/stream/{MULTI_SESSION_ID}",
            timeout=5.0,
        ) as r:
            events = _parse_events(r, stop_after=2, timeout=5.0)
    finally:
        t.join(timeout=2)
    assert events[0]["event"] == "snapshot"
    assert events[1]["event"] == "dataset_complete"
    payload = events[1]["data"]
    assert payload["chart_id"] == "latency"
    assert payload["group_key"] == "faiss"

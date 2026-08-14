"""Integration tests for POST /ingest.

Uses a FastAPI TestClient bound to an isolated sqlite DB + an empty
benchmarks dir. ``conftest.client`` seeds one sample session with two groups
(``alpha``, ``beta``) and two metrics (``throughput``, ``latency``).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from live_bench_server import store
from live_bench_server.models import (
    AxisConfig,
    BenchmarkConfig,
    ChartDef,
    GroupDef,
    MetricDef,
)

from tests.conftest import SAMPLE_SESSION_ID


MULTI_SESSION_ID = "multi-session"


def _iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.isoformat(timespec="microseconds")


def _build_multichart_config(session_id: str = MULTI_SESSION_ID) -> BenchmarkConfig:
    """Two-chart × two-group benchmark with DIFFERENT metric keys per chart.

    Chart ``recall`` owns metric ``recall``; chart ``latency`` owns metric
    ``p99_ms``. This asymmetry lets ``test_chart_isolation_in_metric_validation``
    prove per-chart metric validation.
    """
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


def _seed_multichart(client) -> None:
    """Upsert the multi-chart session into the TestClient's DB."""
    store.upsert_benchmark(
        client.app_state.db,
        _build_multichart_config(),
        source_path="test://multi.yaml",
    )


def test_happy_path(client):
    now = datetime.now(timezone.utc)
    body = {
        "session_id": SAMPLE_SESSION_ID,
        "request_ts": _iso(now),
        "points": [
            {
                "group_key": "alpha",
                "metric_key": "throughput",
                "value": 123.4,
                "client_ts": _iso(now),
            }
        ],
    }
    resp = client.post("/ingest", json=body)
    assert resp.status_code == 200, resp.text
    payload = resp.json()
    assert payload["accepted"] == 1
    assert payload["seq_from"] == 1
    assert payload["seq_to"] == 1
    assert payload["completed"] == []
    assert payload["server_ts"]

    # Verify the point landed.
    show = client.get(f"/benchmarks/{SAMPLE_SESSION_ID}")
    assert show.status_code == 200
    data = show.json()
    points = data["points"]
    assert len(points) == 1
    assert points[0]["group_key"] == "alpha"
    assert points[0]["metric_key"] == "throughput"
    assert points[0]["value"] == 123.4


def test_unknown_session(client):
    now = datetime.now(timezone.utc)
    body = {
        "session_id": "does-not-exist",
        "request_ts": _iso(now),
        "points": [
            {
                "group_key": "alpha",
                "metric_key": "throughput",
                "value": 1.0,
                "client_ts": _iso(now),
            }
        ],
    }
    resp = client.post("/ingest", json=body)
    assert resp.status_code == 404
    assert resp.json()["code"] == "unknown_session"


def test_unknown_group(client):
    now = datetime.now(timezone.utc)
    body = {
        "session_id": SAMPLE_SESSION_ID,
        "request_ts": _iso(now),
        "points": [
            {
                "group_key": "nope",
                "metric_key": "throughput",
                "value": 1.0,
                "client_ts": _iso(now),
            }
        ],
    }
    resp = client.post("/ingest", json=body)
    assert resp.status_code == 400
    assert resp.json()["code"] == "unknown_group"


def test_unknown_metric(client):
    now = datetime.now(timezone.utc)
    body = {
        "session_id": SAMPLE_SESSION_ID,
        "request_ts": _iso(now),
        "points": [
            {
                "group_key": "alpha",
                "metric_key": "nope",
                "value": 1.0,
                "client_ts": _iso(now),
            }
        ],
    }
    resp = client.post("/ingest", json=body)
    assert resp.status_code == 400
    assert resp.json()["code"] == "unknown_metric"


def test_missing_client_ts(client):
    """Omitting client_ts should be rejected — Pydantic returns 422."""
    now = datetime.now(timezone.utc)
    body = {
        "session_id": SAMPLE_SESSION_ID,
        "request_ts": _iso(now),
        "points": [
            {
                "group_key": "alpha",
                "metric_key": "throughput",
                "value": 1.0,
                # client_ts intentionally omitted
            }
        ],
    }
    resp = client.post("/ingest", json=body)
    assert resp.status_code in (400, 422)
    # Either Pydantic 422 (field required) or our explicit 400 missing_client_ts
    if resp.status_code == 400:
        assert resp.json().get("code") == "missing_client_ts"


def test_clock_skew(client):
    """A client_ts 10 minutes in the future must be rejected with clock_skew."""
    now = datetime.now(timezone.utc)
    future = now + timedelta(minutes=10)
    body = {
        "session_id": SAMPLE_SESSION_ID,
        "request_ts": _iso(now),
        "points": [
            {
                "group_key": "alpha",
                "metric_key": "throughput",
                "value": 1.0,
                "client_ts": _iso(future),
            }
        ],
    }
    resp = client.post("/ingest", json=body)
    assert resp.status_code == 400
    assert resp.json()["code"] == "clock_skew"


def test_complete_groups(client):
    now = datetime.now(timezone.utc)
    body = {
        "session_id": SAMPLE_SESSION_ID,
        "request_ts": _iso(now),
        "points": [],
        "complete_groups": ["alpha"],
    }
    resp = client.post("/ingest", json=body)
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["accepted"] == 0
    assert payload["completed"] == ["alpha"]

    show = client.get(f"/benchmarks/{SAMPLE_SESSION_ID}")
    data = show.json()
    states = {d["group_key"]: d for d in data["datasets"]}
    assert states["alpha"]["status"] == "complete"
    assert states["beta"]["status"] == "pending"


# ── Chart-aware tests ─────────────────────────────────────────────────────


def test_unknown_chart(client):
    """POST with a chart_id that doesn't exist in the session's config → 400."""
    _seed_multichart(client)
    now = datetime.now(timezone.utc)
    body = {
        "session_id": MULTI_SESSION_ID,
        "request_ts": _iso(now),
        "points": [
            {
                "chart_id": "nonexistent",
                "group_key": "faiss",
                "metric_key": "recall",
                "value": 0.9,
                "client_ts": _iso(now),
            }
        ],
    }
    resp = client.post("/ingest", json=body)
    assert resp.status_code == 400
    payload = resp.json()
    assert payload["code"] == "unknown_chart"
    assert "nonexistent" in payload["message"]


def test_chart_isolation_in_metric_validation(client):
    """Metric ``recall`` exists in chart A, not B. Targeting B with it → 400 unknown_metric."""
    _seed_multichart(client)
    now = datetime.now(timezone.utc)
    body = {
        "session_id": MULTI_SESSION_ID,
        "request_ts": _iso(now),
        "points": [
            {
                # "recall" is valid in chart "recall" but NOT in chart "latency"
                "chart_id": "latency",
                "group_key": "faiss",
                "metric_key": "recall",
                "value": 0.9,
                "client_ts": _iso(now),
            }
        ],
    }
    resp = client.post("/ingest", json=body)
    assert resp.status_code == 400
    assert resp.json()["code"] == "unknown_metric"

    # Sanity check: the SAME metric in its OWN chart should be accepted.
    body["points"][0]["chart_id"] = "recall"
    resp2 = client.post("/ingest", json=body)
    assert resp2.status_code == 200, resp2.text
    assert resp2.json()["accepted"] == 1


def test_complete_groups_with_chart_id(client):
    """complete_groups can carry CompletionRef objects with explicit chart_id."""
    _seed_multichart(client)
    now = datetime.now(timezone.utc)
    body = {
        "session_id": MULTI_SESSION_ID,
        "request_ts": _iso(now),
        "points": [],
        "complete_groups": [{"chart_id": "recall", "group_key": "faiss"}],
    }
    resp = client.post("/ingest", json=body)
    assert resp.status_code == 200, resp.text
    payload = resp.json()
    assert payload["completed"] == ["faiss"]

    # Verify only the (recall, faiss) pair is complete — the (latency, faiss)
    # pair should still be pending even though the group_key matches.
    show = client.get(f"/benchmarks/{MULTI_SESSION_ID}")
    data = show.json()
    states = {
        (d["chart_id"], d["group_key"]): d for d in data["datasets"]
    }
    assert states[("recall", "faiss")]["status"] == "complete"
    assert states[("latency", "faiss")]["status"] == "pending"
    assert states[("recall", "qdrant")]["status"] == "pending"


def test_datapoint_carries_chart_id_through_storage(client):
    """A point with an explicit chart_id persists that chart_id."""
    _seed_multichart(client)
    now = datetime.now(timezone.utc)
    body = {
        "session_id": MULTI_SESSION_ID,
        "request_ts": _iso(now),
        "points": [
            {
                "chart_id": "latency",
                "group_key": "qdrant",
                "metric_key": "p99_ms",
                "value": 42.0,
                "client_ts": _iso(now),
            }
        ],
    }
    resp = client.post("/ingest", json=body)
    assert resp.status_code == 200, resp.text
    show = client.get(f"/benchmarks/{MULTI_SESSION_ID}")
    data = show.json()
    points = data["points"]
    assert len(points) == 1
    assert points[0]["chart_id"] == "latency"
    assert points[0]["group_key"] == "qdrant"
    assert points[0]["metric_key"] == "p99_ms"
    assert points[0]["value"] == 42.0


def test_backward_compat_default_chart_id(client):
    """A point with NO chart_id lands with chart_id="default" on a single-chart session."""
    now = datetime.now(timezone.utc)
    body = {
        "session_id": SAMPLE_SESSION_ID,
        "request_ts": _iso(now),
        "points": [
            {
                # chart_id deliberately omitted
                "group_key": "alpha",
                "metric_key": "throughput",
                "value": 7.5,
                "client_ts": _iso(now),
            }
        ],
    }
    resp = client.post("/ingest", json=body)
    assert resp.status_code == 200, resp.text
    show = client.get(f"/benchmarks/{SAMPLE_SESSION_ID}")
    data = show.json()
    points = data["points"]
    assert len(points) == 1
    assert points[0]["chart_id"] == "default"


def test_reset_endpoint(client):
    now = datetime.now(timezone.utc)
    # ingest a point
    client.post(
        "/ingest",
        json={
            "session_id": SAMPLE_SESSION_ID,
            "request_ts": _iso(now),
            "points": [
                {
                    "group_key": "alpha",
                    "metric_key": "throughput",
                    "value": 50.0,
                    "client_ts": _iso(now),
                }
            ],
        },
    )
    # reset
    resp = client.post(f"/benchmarks/{SAMPLE_SESSION_ID}/reset")
    assert resp.status_code == 200
    assert resp.json() == {"reset": True, "session_id": SAMPLE_SESSION_ID}

    show = client.get(f"/benchmarks/{SAMPLE_SESSION_ID}")
    assert show.json()["points"] == []

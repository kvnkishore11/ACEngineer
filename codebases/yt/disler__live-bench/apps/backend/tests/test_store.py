"""Unit tests for the repository layer (`store.py`)."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from live_bench_server import store
from live_bench_server.models import (
    AxisConfig,
    BenchmarkConfig,
    ChartDef,
    CompletionRef,
    DataPoint,
    GroupDef,
    MetricDef,
)

from tests.conftest import SAMPLE_SESSION_ID


def _make_point(
    group: str,
    metric: str,
    value: float,
    client_ts: datetime,
    chart_id: str = "default",
) -> DataPoint:
    return DataPoint(
        chart_id=chart_id,
        group_key=group,
        metric_key=metric,
        value=value,
        client_ts=client_ts,
    )


def _build_multichart_config(session_id: str = "multi-session") -> BenchmarkConfig:
    """Compact two-chart × two-group BenchmarkConfig for chart-aware tests."""
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


def test_insert_points_assigns_monotonic_seq(seeded_db):
    now = datetime.now(timezone.utc)
    pts = [
        _make_point("alpha", "throughput", 100.0, now),
        _make_point("alpha", "latency", 10.0, now),
        _make_point("beta", "throughput", 200.0, now),
    ]
    stored = store.insert_points(seeded_db, SAMPLE_SESSION_ID, pts)
    assert [s.seq for s in stored] == [1, 2, 3]
    assert store.max_seq(seeded_db, SAMPLE_SESSION_ID) == 3

    # A second batch continues the sequence.
    more = store.insert_points(
        seeded_db,
        SAMPLE_SESSION_ID,
        [_make_point("beta", "latency", 20.0, now)],
    )
    assert more[0].seq == 4


def test_latest_per_cell_handles_out_of_order_client_ts(seeded_db):
    """Out-of-order client_ts: newer-by-client_ts must win even when inserted later."""
    newer = datetime(2030, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    older = datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

    # Insert the newer-by-client_ts point FIRST.
    store.insert_points(
        seeded_db,
        SAMPLE_SESSION_ID,
        [_make_point("alpha", "throughput", 999.0, newer)],
    )
    # Then insert a stale point with an older client_ts for the same cell.
    store.insert_points(
        seeded_db,
        SAMPLE_SESSION_ID,
        [_make_point("alpha", "throughput", 111.0, older)],
    )

    latest = store.latest_per_cell(seeded_db, SAMPLE_SESSION_ID)
    cells = {(p.group_key, p.metric_key): p for p in latest}
    winner = cells[("alpha", "throughput")]
    assert winner.value == 999.0
    assert winner.client_ts.year == 2030


def test_reset_clears_datapoints_and_completions(seeded_db):
    now = datetime.now(timezone.utc)
    store.insert_points(
        seeded_db,
        SAMPLE_SESSION_ID,
        [
            _make_point("alpha", "throughput", 1.0, now),
            _make_point("alpha", "latency", 2.0, now),
        ],
    )
    store.mark_complete(seeded_db, SAMPLE_SESSION_ID, ["alpha"])

    # Pre-conditions
    assert store.max_seq(seeded_db, SAMPLE_SESSION_ID) == 2
    assert len(store.latest_per_cell(seeded_db, SAMPLE_SESSION_ID)) == 2

    store.reset(seeded_db, SAMPLE_SESSION_ID)

    # datapoints + completions gone
    assert store.max_seq(seeded_db, SAMPLE_SESSION_ID) == 0
    assert store.latest_per_cell(seeded_db, SAMPLE_SESSION_ID) == []
    # benchmarks row still exists
    cfg = store.get_benchmark(seeded_db, SAMPLE_SESSION_ID)
    assert cfg is not None
    # after reset, every dataset should be pending again
    states = store.dataset_states(seeded_db, SAMPLE_SESSION_ID)
    assert {s.status for s in states} == {"pending"}


def test_dataset_states_pending_running_complete(seeded_db):
    """Pending when no data; running when data but no completion; complete when completion row exists."""
    # Initial: all pending
    states = {s.group_key: s for s in store.dataset_states(seeded_db, SAMPLE_SESSION_ID)}
    assert states["alpha"].status == "pending"
    assert states["beta"].status == "pending"

    # Insert a point into alpha → alpha is running, beta still pending.
    now = datetime.now(timezone.utc)
    store.insert_points(
        seeded_db,
        SAMPLE_SESSION_ID,
        [_make_point("alpha", "throughput", 42.0, now)],
    )
    states = {s.group_key: s for s in store.dataset_states(seeded_db, SAMPLE_SESSION_ID)}
    assert states["alpha"].status == "running"
    assert states["alpha"].started_at is not None
    assert states["beta"].status == "pending"

    # Mark alpha complete → alpha is complete, beta still pending.
    store.mark_complete(seeded_db, SAMPLE_SESSION_ID, ["alpha"])
    states = {s.group_key: s for s in store.dataset_states(seeded_db, SAMPLE_SESSION_ID)}
    assert states["alpha"].status == "complete"
    assert states["alpha"].completed_at is not None
    assert states["beta"].status == "pending"


def test_list_benchmarks_reports_counts(seeded_db):
    items = store.list_benchmarks(seeded_db)
    assert len(items) == 1
    item = items[0]
    assert item["session_id"] == SAMPLE_SESSION_ID
    assert item["total_count"] == 2
    assert item["completed_count"] == 0
    assert item["last_update"] is None
    assert item["better"] == "higher"
    # Single-chart benchmark should report chart_count=1 and a non-null better.
    assert item["chart_count"] == 1


# ── Chart-aware tests ─────────────────────────────────────────────────────


def test_insert_points_preserves_chart_id(tmp_db):
    """Points inserted with explicit chart_ids round-trip through storage."""
    cfg = _build_multichart_config()
    store.upsert_benchmark(tmp_db, cfg, source_path="test://multi.yaml")

    now = datetime.now(timezone.utc)
    pts = [
        _make_point("faiss", "recall", 0.9, now, chart_id="recall"),
        _make_point("faiss", "p99_ms", 12.0, now, chart_id="latency"),
    ]
    stored = store.insert_points(tmp_db, cfg.session_id, pts)
    assert len(stored) == 2
    assert stored[0].chart_id == "recall"
    assert stored[0].group_key == "faiss"
    assert stored[0].metric_key == "recall"
    assert stored[1].chart_id == "latency"
    assert stored[1].metric_key == "p99_ms"

    # Verify via latest_per_cell that the chart_id is persisted.
    latest = store.latest_per_cell(tmp_db, cfg.session_id)
    assert len(latest) == 2
    cells = {(p.chart_id, p.group_key, p.metric_key): p for p in latest}
    assert ("recall", "faiss", "recall") in cells
    assert ("latency", "faiss", "p99_ms") in cells


def test_latest_per_cell_isolates_charts(tmp_db):
    """Two points with the same (group, metric) but different chart_ids are isolated cells."""
    # Use a synthetic config with the same metric key in both charts so we can
    # prove isolation on the group_key + metric_key axis alone.
    cfg = BenchmarkConfig(
        session_id="chart-iso",
        title="Chart isolation",
        groups=[GroupDef(key="g1", label="G1")],
        charts=[
            ChartDef(
                chart_id="a",
                title="Chart A",
                better="higher",
                x=AxisConfig(label="x"),
                y=AxisConfig(label="y"),
                metrics=[MetricDef(key="m", label="M")],
            ),
            ChartDef(
                chart_id="b",
                title="Chart B",
                better="higher",
                x=AxisConfig(label="x"),
                y=AxisConfig(label="y"),
                metrics=[MetricDef(key="m", label="M")],
            ),
        ],
    )
    store.upsert_benchmark(tmp_db, cfg, source_path="test://iso.yaml")

    now = datetime.now(timezone.utc)
    store.insert_points(
        tmp_db,
        cfg.session_id,
        [_make_point("g1", "m", 1.0, now, chart_id="a")],
    )
    store.insert_points(
        tmp_db,
        cfg.session_id,
        [_make_point("g1", "m", 2.0, now, chart_id="b")],
    )

    latest = store.latest_per_cell(tmp_db, cfg.session_id)
    assert len(latest) == 2
    cells = {(p.chart_id, p.group_key, p.metric_key): p for p in latest}
    assert cells[("a", "g1", "m")].value == 1.0
    assert cells[("b", "g1", "m")].value == 2.0


def test_dataset_states_per_chart(tmp_db):
    """A benchmark with 2 charts × 2 groups yields 4 DatasetState entries."""
    cfg = _build_multichart_config()
    store.upsert_benchmark(tmp_db, cfg, source_path="test://multi.yaml")

    states = store.dataset_states(tmp_db, cfg.session_id, cfg)
    assert len(states) == 4
    pairs = {(s.chart_id, s.group_key) for s in states}
    assert pairs == {
        ("recall", "faiss"),
        ("recall", "qdrant"),
        ("latency", "faiss"),
        ("latency", "qdrant"),
    }
    # Everything should be pending initially.
    assert {s.status for s in states} == {"pending"}

    # Running: insert a point into (recall, faiss) only.
    now = datetime.now(timezone.utc)
    store.insert_points(
        tmp_db,
        cfg.session_id,
        [_make_point("faiss", "recall", 0.91, now, chart_id="recall")],
    )
    states = {
        (s.chart_id, s.group_key): s
        for s in store.dataset_states(tmp_db, cfg.session_id, cfg)
    }
    assert states[("recall", "faiss")].status == "running"
    assert states[("recall", "faiss")].started_at is not None
    # Other pairs must remain pending.
    assert states[("recall", "qdrant")].status == "pending"
    assert states[("latency", "faiss")].status == "pending"
    assert states[("latency", "qdrant")].status == "pending"

    # Complete (recall, faiss) only.
    store.mark_complete(
        tmp_db,
        cfg.session_id,
        [CompletionRef(chart_id="recall", group_key="faiss")],
    )
    states = {
        (s.chart_id, s.group_key): s
        for s in store.dataset_states(tmp_db, cfg.session_id, cfg)
    }
    assert states[("recall", "faiss")].status == "complete"
    assert states[("recall", "faiss")].completed_at is not None
    # The same group on a different chart must remain pending.
    assert states[("latency", "faiss")].status == "pending"


def test_mark_complete_chart_isolation(tmp_db):
    """Marking (chart=a, group=g) complete must not affect (chart=b, group=g)."""
    cfg = _build_multichart_config()
    store.upsert_benchmark(tmp_db, cfg, source_path="test://multi.yaml")

    now = datetime.now(timezone.utc)
    store.insert_points(
        tmp_db,
        cfg.session_id,
        [
            _make_point("faiss", "recall", 0.9, now, chart_id="recall"),
            _make_point("faiss", "p99_ms", 12.0, now, chart_id="latency"),
        ],
    )
    # Mark only (recall, faiss) complete.
    store.mark_complete(
        tmp_db,
        cfg.session_id,
        [CompletionRef(chart_id="recall", group_key="faiss")],
    )

    states = {
        (s.chart_id, s.group_key): s
        for s in store.dataset_states(tmp_db, cfg.session_id, cfg)
    }
    assert states[("recall", "faiss")].status == "complete"
    assert states[("latency", "faiss")].status == "running"


def test_list_benchmarks_multichart_shape(tmp_db):
    """Multi-chart benchmark reports chart_count>1 and better=None."""
    cfg = _build_multichart_config()
    store.upsert_benchmark(tmp_db, cfg, source_path="test://multi.yaml")

    items = store.list_benchmarks(tmp_db)
    assert len(items) == 1
    item = items[0]
    assert item["chart_count"] == 2
    assert item["better"] is None
    assert item["total_count"] == 4  # 2 groups × 2 charts (per-chart groups)


def test_latest_per_cell_out_of_order_chart_aware(tmp_db):
    """Out-of-order client_ts still picks the newest per (chart, group, metric)."""
    cfg = _build_multichart_config()
    store.upsert_benchmark(tmp_db, cfg, source_path="test://multi.yaml")

    newer = datetime(2030, 1, 1, tzinfo=timezone.utc)
    older = datetime(2020, 1, 1, tzinfo=timezone.utc)

    # Insert the newer point first.
    store.insert_points(
        tmp_db,
        cfg.session_id,
        [_make_point("faiss", "recall", 0.99, newer, chart_id="recall")],
    )
    # Then insert a stale point with an older client_ts for the same cell.
    store.insert_points(
        tmp_db,
        cfg.session_id,
        [_make_point("faiss", "recall", 0.10, older, chart_id="recall")],
    )

    latest = store.latest_per_cell(tmp_db, cfg.session_id)
    cell = next(
        p
        for p in latest
        if p.chart_id == "recall" and p.group_key == "faiss" and p.metric_key == "recall"
    )
    assert cell.value == 0.99
    assert cell.client_ts.year == 2030

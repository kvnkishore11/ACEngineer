"""Export JSON fixtures for every public Pydantic model.

Run via:
    uv run python tests/fixtures_export.py

Writes one file per model into ``apps/backend/tests/fixtures/<ModelName>.json``.
The frontend's Zod drift test (``apps/frontend/src/schemas.test.ts``) loads
these files and asserts that each one parses successfully, proving schema
parity across the language boundary.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from live_bench_server.models import (
    AxisConfig,
    BenchmarkConfig,
    BenchmarkFile,
    ChartDef,
    CompletionRef,
    DataPoint,
    DataPointStored,
    DatasetState,
    GroupDef,
    IngestRequest,
    IngestResponse,
    MetricDef,
    SseConfigChanged,
    SseDatapoint,
    SseDatasetComplete,
    SseReset,
    SseSnapshot,
)


def _ts(seconds_offset: float = 0.0) -> datetime:
    base = datetime(2026, 4, 7, 14, 22, 19, 318204, tzinfo=timezone.utc)
    return base.fromtimestamp(base.timestamp() + seconds_offset, tz=timezone.utc)


def build_samples() -> dict[str, object]:
    """Build one realistic instance of every public model."""
    axis_x = AxisConfig(label="Backend")
    axis_y = AxisConfig(label="Recall@10", unit=None, min=0, max=1)
    axis_y_latency = AxisConfig(label="Latency", unit="ms", min=0)

    metric_recall = MetricDef(key="recall", label="Recall@10", color="#6ba368")
    metric_latency = MetricDef(key="p99_ms", label="p99", color="#e86b3a")

    group_faiss = GroupDef(key="faiss", label="FAISS")
    group_qdrant = GroupDef(key="qdrant", label="Qdrant")
    group_lance = GroupDef(key="lance", label="LanceDB")

    groups = [group_faiss, group_qdrant, group_lance]

    chart_recall = ChartDef(
        chart_id="recall",
        title="Recall@10",
        subtitle="higher is better",
        better="higher",
        direction="BT",
        x=axis_x,
        y=axis_y,
        metrics=[metric_recall],
        groups=groups,
    )
    chart_latency = ChartDef(
        chart_id="latency",
        title="p99 Query Latency",
        subtitle="lower is better",
        better="lower",
        direction="LR",
        x=AxisConfig(label="Latency", unit="ms", min=0),
        y=AxisConfig(label="Backend"),
        metrics=[metric_latency],
        groups=groups,
    )

    cfg = BenchmarkConfig(
        session_id="trio",
        title="Vector Search Trio",
        subtitle="FAISS vs Qdrant vs LanceDB",
        charts=[chart_recall, chart_latency],
    )
    file_wrapper = BenchmarkFile(version=1, benchmark=cfg)

    dp = DataPoint(
        chart_id="recall",
        group_key="faiss",
        metric_key="recall",
        value=0.94,
        client_ts=_ts(0.000),
    )
    dp_stored = DataPointStored(
        session_id=cfg.session_id,
        chart_id="recall",
        group_key="faiss",
        metric_key="recall",
        value=0.94,
        client_ts=_ts(0.000),
        server_ts=_ts(0.084),
        seq=43,
    )
    dataset = DatasetState(
        chart_id="recall",
        group_key="faiss",
        status="running",
        started_at=_ts(0.000),
        completed_at=None,
    )

    completion_ref = CompletionRef(chart_id="recall", group_key="faiss")

    ingest_req = IngestRequest(
        session_id=cfg.session_id,
        request_ts=_ts(0.100),
        points=[dp],
        complete_groups=[completion_ref],
    )
    ingest_resp = IngestResponse(
        accepted=1,
        seq_from=43,
        seq_to=43,
        completed=["faiss"],
        server_ts=_ts(0.101),
    )

    snapshot = SseSnapshot(
        session_id=cfg.session_id,
        config=cfg,
        points=[dp_stored],
        datasets=[dataset],
    )
    sse_dp = SseDatapoint(session_id=cfg.session_id, point=dp_stored)
    sse_complete = SseDatasetComplete(
        session_id=cfg.session_id,
        chart_id="recall",
        group_key="faiss",
        completed_at=_ts(0.102),
    )
    sse_reset = SseReset(session_id=cfg.session_id)
    sse_cfg_changed = SseConfigChanged(session_id=cfg.session_id, config=cfg)

    return {
        "AxisConfig": axis_x,
        "MetricDef": metric_recall,
        "GroupDef": group_faiss,
        "ChartDef": chart_recall,
        "BenchmarkConfig": cfg,
        "BenchmarkFile": file_wrapper,
        "DataPoint": dp,
        "DataPointStored": dp_stored,
        "DatasetState": dataset,
        "CompletionRef": completion_ref,
        "IngestRequest": ingest_req,
        "IngestResponse": ingest_resp,
        "SseSnapshot": snapshot,
        "SseDatapoint": sse_dp,
        "SseDatasetComplete": sse_complete,
        "SseReset": sse_reset,
        "SseConfigChanged": sse_cfg_changed,
    }


def main() -> None:
    here = Path(__file__).resolve().parent
    out_dir = here / "fixtures"
    out_dir.mkdir(exist_ok=True)
    samples = build_samples()
    for name, obj in samples.items():
        out_file = out_dir / f"{name}.json"
        out_file.write_text(obj.model_dump_json(indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out_file.relative_to(here.parent)}")
    print(f"exported {len(samples)} fixtures to {out_dir}")


if __name__ == "__main__":
    main()

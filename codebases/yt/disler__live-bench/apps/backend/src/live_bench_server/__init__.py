"""live_bench_server — shared models + (later) FastAPI app.

For now this package only exposes the Pydantic model contract from
``models.py``. Consumers can use either form:

    from live_bench_server.models import DataPoint
    from live_bench_server import DataPoint
"""

from live_bench_server.models import (
    AxisConfig,
    BenchmarkConfig,
    BenchmarkFile,
    Better,
    ChartDef,
    Color,
    CompletionRef,
    DataPoint,
    DataPointStored,
    DatasetState,
    DatasetStatus,
    Direction,
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

__all__ = [
    # type aliases
    "Direction",
    "Better",
    "Color",
    "DatasetStatus",
    # config models
    "AxisConfig",
    "MetricDef",
    "GroupDef",
    "ChartDef",
    "BenchmarkConfig",
    "BenchmarkFile",
    # datapoint models
    "DataPoint",
    "DataPointStored",
    # dataset state
    "DatasetState",
    # ingest wire
    "CompletionRef",
    "IngestRequest",
    "IngestResponse",
    # SSE events
    "SseSnapshot",
    "SseDatapoint",
    "SseDatasetComplete",
    "SseReset",
    "SseConfigChanged",
]

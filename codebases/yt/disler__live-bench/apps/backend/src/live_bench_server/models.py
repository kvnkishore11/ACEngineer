"""Shared Pydantic models for live-bench.

This module is the contract that the FastAPI backend, the click CLI, and the
fixtures the frontend's Zod schemas test against all depend on. Every model in
spec §4.2 lives here verbatim.

Datetime serialisation
----------------------
Every ``datetime`` field is serialised to ISO-8601 UTC with **microsecond**
precision (e.g. ``2026-04-07T14:22:19.318204+00:00``). The format is
fixed-width and lexicographically sortable, which lets the frontend's
newer-wins guard (§14.4) compare ``client_ts`` strings with raw ``<`` / ``>``
on the hot path — no parsing required. See spec §15 for the full rationale.

Naive datetimes are assumed to be UTC and tagged accordingly before
serialisation; aware datetimes are converted to UTC. The serializer is
declared once on a private base class so it applies to every datetime field
across the module (single fields and nested models / lists alike).
"""

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    model_validator,
)


# ── Type aliases ───────────────────────────────────────────
Direction = Literal["LR", "BT"]              # bar growth direction
Better = Literal["higher", "lower"]          # which direction means "good"
Color = str | list[str]                      # "#rrggbb" or ["#a","#b","#c"]
DatasetStatus = Literal["pending", "running", "complete"]


# ── Datetime serialisation helpers ─────────────────────────
def _to_iso_utc_microseconds(dt: datetime) -> str:
    """Render a datetime as fixed-width ISO-8601 UTC with microsecond precision.

    - Naive datetimes are assumed UTC.
    - Aware datetimes are converted to UTC.
    - ``timespec='microseconds'`` guarantees a 6-digit fractional component
      so the resulting strings are lexicographically sortable across all
      timestamps in the system.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.isoformat(timespec="microseconds")


class _LiveBenchModel(BaseModel):
    """Base model that serialises every ``datetime`` field as ISO-8601 UTC μs.

    Subclasses inherit the ``model_config`` and the wildcard
    ``@field_serializer('*')`` hook below; Pydantic only invokes the
    serializer for fields whose runtime value is a ``datetime`` (we
    pass-through everything else), so it is safe to apply universally.
    """

    model_config = ConfigDict(
        # Permit constructing models from datetimes without coercion surprises.
        # We don't want strings auto-parsed in unexpected places, but we do
        # want timezone-aware datetimes to round-trip cleanly.
        validate_assignment=False,
    )

    @field_serializer("*", when_used="json")
    def _serialize_any(self, value):  # type: ignore[no-untyped-def]
        if isinstance(value, datetime):
            return _to_iso_utc_microseconds(value)
        return value


# ── Benchmark configuration ────────────────────────────────
class AxisConfig(_LiveBenchModel):
    label: str
    unit: str | None = None
    min: float | None = None
    max: float | None = None


class MetricDef(_LiveBenchModel):
    key: str
    label: str
    color: Color | None = None
    icon: str | None = None             # optional icon URL (e.g. "/icons/alibaba.svg")


class GroupDef(_LiveBenchModel):
    key: str
    label: str
    icon: str | None = None          # optional icon URL (e.g. "/icons/google.svg")


class ChartDef(_LiveBenchModel):
    """One chart panel inside a benchmark.

    Each chart is fully self-contained: it owns its own groups, metrics,
    axes, direction, and ``better`` indicator. This allows different charts
    in the same benchmark to have different x-axis categories (e.g. prompts
    for speed charts, models for memory charts).
    """

    chart_id: str                              # unique within parent benchmark
    title: str | None = None                   # rendered above this chart panel
    subtitle: str | None = None
    better: Better                             # higher | lower (per-chart)
    direction: Direction = "BT"
    x: AxisConfig
    y: AxisConfig
    metrics: list[MetricDef]
    groups: list[GroupDef] | None = None        # per-chart groups (required for multi-chart, synthesized for legacy)


class TagDef(_LiveBenchModel):
    name: str
    icons: list[str] = Field(default_factory=list)  # URLs to icon SVGs


class BenchmarkConfig(_LiveBenchModel):
    session_id: str
    title: str
    subtitle: str | None = None
    tags: list[TagDef] | None = None

    # ── Multi-chart form ──
    charts: list[ChartDef] | None = None

    # ── Single-chart legacy form (top-level fields, all optional) ──
    # Either set ALL FIVE of these (better/x/y/metrics/groups) and leave `charts` None,
    # OR set `charts` and leave these None. The model_validator below enforces it.
    groups: list[GroupDef] | None = None          # legacy only — multi-chart puts groups on each ChartDef
    better: Better | None = None
    direction: Direction = "BT"
    x: AxisConfig | None = None
    y: AxisConfig | None = None
    metrics: list[MetricDef] | None = None

    @model_validator(mode="after")
    def _normalize_chart_form(self) -> "BenchmarkConfig":
        single_present = (
            self.metrics is not None
            and self.x is not None
            and self.y is not None
            and self.better is not None
        )
        multi_present = self.charts is not None and len(self.charts) > 0

        if single_present and multi_present:
            raise ValueError(
                "BenchmarkConfig must specify EITHER top-level chart fields "
                "(better/x/y/metrics) OR a `charts` list, not both"
            )
        if not single_present and not multi_present:
            raise ValueError(
                "BenchmarkConfig must specify EITHER top-level chart fields "
                "(better/x/y/metrics) OR a `charts` list with at least one entry"
            )
        return self

    def all_charts(self) -> list[ChartDef]:
        """Return every chart in this benchmark as a flat list.

        For the multi-chart form, returns ``self.charts`` directly (each chart
        already carries its own ``groups``).
        For the legacy single-chart form, synthesizes a single ChartDef with
        ``chart_id="default"`` from the top-level fields, including ``groups``.
        """
        if self.charts is not None:
            return self.charts
        # Synthesize default ChartDef from legacy fields.
        assert self.better is not None
        assert self.x is not None
        assert self.y is not None
        assert self.metrics is not None
        assert self.groups is not None
        return [
            ChartDef(
                chart_id="default",
                title=None,
                subtitle=None,
                better=self.better,
                direction=self.direction,
                x=self.x,
                y=self.y,
                metrics=self.metrics,
                groups=self.groups,
            )
        ]


class BenchmarkFile(_LiveBenchModel):
    """One YAML file under ``benchmarks/``.

    Two supported shapes — exactly one of ``benchmark`` or ``benchmarks`` must
    be set:

    1. **Single benchmark** (the original shape, kept for backward compatibility):

       .. code-block:: yaml

           version: 1
           benchmark:
             session_id: my-bench
             ...

    2. **Multiple benchmarks per file** — bundle several related charts into
       one config file:

       .. code-block:: yaml

           version: 1
           benchmarks:
             - session_id: bench-a
               ...
             - session_id: bench-b
               ...

    Use ``BenchmarkFile.all_benchmarks()`` to iterate uniformly over both forms
    in the loader.
    """

    version: Literal[1] = 1
    benchmark: BenchmarkConfig | None = None
    benchmarks: list[BenchmarkConfig] | None = None

    @model_validator(mode="after")
    def _exactly_one_form(self) -> "BenchmarkFile":
        has_single = self.benchmark is not None
        has_multi = self.benchmarks is not None
        if has_single and has_multi:
            raise ValueError(
                "BenchmarkFile must specify either `benchmark` (single) or "
                "`benchmarks` (list), not both"
            )
        if not has_single and not has_multi:
            raise ValueError(
                "BenchmarkFile must specify either `benchmark` (single) or "
                "`benchmarks` (list)"
            )
        if has_multi and len(self.benchmarks or []) == 0:
            raise ValueError("`benchmarks` must contain at least one entry")
        return self

    def all_benchmarks(self) -> list[BenchmarkConfig]:
        """Return every benchmark defined in this file as a flat list.

        Hides the single-vs-multi shape from callers — they always get a list.
        """
        if self.benchmarks is not None:
            return self.benchmarks
        assert self.benchmark is not None  # validator guarantees one of the two
        return [self.benchmark]


# ── Datapoints ─────────────────────────────────────────────
class DataPoint(_LiveBenchModel):
    """A point as it crosses the wire from CLI → backend.

    ``client_ts`` is REQUIRED and set by the CLI at emit time with microsecond
    precision (``datetime.now(timezone.utc)``). It is the ground-truth ordering
    key — the frontend uses it for newer-wins (§14.4).
    """

    chart_id: str = "default"   # which chart inside the benchmark this point targets
    group_key: str
    metric_key: str
    value: float
    client_ts: datetime    # ISO-8601 UTC w/ μs on the wire


class DataPointStored(_LiveBenchModel):
    """A point after the backend has stored it. Adds ``seq`` and ``server_ts``."""

    session_id: str
    chart_id: str = "default"   # which chart inside the benchmark this point targets
    group_key: str
    metric_key: str
    value: float
    client_ts: datetime    # from the CLI, unchanged
    server_ts: datetime    # assigned on insert (arrival time)
    seq: int               # monotonic per session; drives Last-Event-ID


# ── Dataset status ─────────────────────────────────────────
class DatasetState(_LiveBenchModel):
    chart_id: str = "default"   # which chart this dataset status belongs to
    group_key: str
    status: DatasetStatus
    started_at: datetime | None = None
    completed_at: datetime | None = None


# ── Ingest wire (HTTP POST /ingest) ────────────────────────
class GroupMetadata(_LiveBenchModel):
    """Arbitrary key-value metadata for a (chart, group) pair.

    Used to attach qualitative data (prompt text, model responses) alongside
    numeric datapoints. The ``data`` dict is schema-free — the benchmark
    decides what to put there. Upserts merge into existing metadata.
    """

    chart_id: str = "default"
    group_key: str
    data: dict[str, Any] = Field(default_factory=dict)


class CompletionRef(_LiveBenchModel):
    """A (chart, group) pair to mark complete. Used in IngestRequest.complete_groups."""

    chart_id: str = "default"
    group_key: str


class IngestRequest(_LiveBenchModel):
    """The body of POST /ingest.

    ``points`` carry their own ``client_ts`` set by the CLI when each point was
    produced (NOT when the POST was made — batching must not reorder).
    ``request_ts`` is the moment the CLI built the batch, used for operational
    logging only.
    """

    session_id: str
    request_ts: datetime                                          # CLI batch-build time
    points: list[DataPoint] = Field(default_factory=list)
    complete_groups: list[CompletionRef] = Field(default_factory=list)
    metadata: list[GroupMetadata] = Field(default_factory=list)

    @field_validator("complete_groups", mode="before")
    @classmethod
    def _coerce_string_complete_groups(cls, v):
        """Backward compat: bare strings are coerced to default-chart CompletionRefs.

        The original CLI shipped ``complete_groups: ["alpha", "bravo"]``. We keep
        that working: each bare string becomes
        ``{chart_id: "default", group_key: <s>}``.
        """
        if not isinstance(v, list):
            return v
        return [
            {"chart_id": "default", "group_key": item} if isinstance(item, str) else item
            for item in v
        ]


class IngestResponse(_LiveBenchModel):
    accepted: int
    seq_from: int | None = None
    seq_to: int | None = None
    completed: list[str] = Field(default_factory=list)
    server_ts: datetime                                           # receipt time


# ── SSE events ─────────────────────────────────────────────
class SseSnapshot(_LiveBenchModel):
    event: Literal["snapshot"] = "snapshot"
    session_id: str
    config: BenchmarkConfig
    points: list[DataPointStored]
    datasets: list[DatasetState]


class SseDatapoint(_LiveBenchModel):
    event: Literal["datapoint"] = "datapoint"
    session_id: str
    point: DataPointStored


class SseDatasetComplete(_LiveBenchModel):
    event: Literal["dataset_complete"] = "dataset_complete"
    session_id: str
    chart_id: str = "default"
    group_key: str
    completed_at: datetime    # server-assigned on mark_complete


class SseReset(_LiveBenchModel):
    event: Literal["reset"] = "reset"
    session_id: str


class SseConfigChanged(_LiveBenchModel):
    event: Literal["config_changed"] = "config_changed"
    session_id: str
    config: BenchmarkConfig


class SseMetadata(_LiveBenchModel):
    event: Literal["metadata"] = "metadata"
    session_id: str
    chart_id: str
    group_key: str
    data: dict[str, Any]


class SsePing(_LiveBenchModel):
    event: Literal["ping"] = "ping"


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
    "TagDef",
    "ChartDef",
    "BenchmarkConfig",
    "BenchmarkFile",
    # datapoint models
    "DataPoint",
    "DataPointStored",
    # dataset state
    "DatasetState",
    # ingest wire
    "GroupMetadata",
    "CompletionRef",
    "IngestRequest",
    "IngestResponse",
    # SSE events
    "SseSnapshot",
    "SseDatapoint",
    "SseDatasetComplete",
    "SseReset",
    "SseConfigChanged",
    "SseMetadata",
    "SsePing",
]

"""Tests for the click commands.

We stub ``LiveBenchClient`` with a fake that captures every
``IngestRequest`` instead of hitting the network. The invariants we care
about here are:

* ``emit`` (single mode) stamps ``client_ts`` at command entry.
* ``emit --batch`` passes through an explicit ``client_ts`` verbatim.
* ``emit --batch`` stamps lines that omit ``client_ts`` at read time.
* ``stream`` preserves stdin order and stamps in monotonic order.
* ``complete`` builds an empty-points request with ``complete_groups``.
* ``stream`` recognises ``{"complete": "..."}`` control lines.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest
from click.testing import CliRunner

from live_bench_cli import cli as cli_module
from live_bench_cli.cli import cli
from live_bench_cli.commands import (
    complete_cmd,
    emit_cmd,
    stream_cmd,
)
from live_bench_cli.models import CompletionRef, IngestRequest, IngestResponse


# ── fake client ───────────────────────────────────────────────
class FakeClient:
    """Captures every ``IngestRequest`` passed to ``ingest``."""

    instances: list["FakeClient"] = []

    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self.base_url = base_url
        self.requests: list[IngestRequest] = []
        FakeClient.instances.append(self)

    def close(self) -> None:
        pass

    def __enter__(self) -> "FakeClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def ingest(self, req: IngestRequest) -> IngestResponse:
        self.requests.append(req)
        # complete_groups is list[CompletionRef]; extract group keys for the
        # response payload so the CLI's summary printing still works.
        completed = [
            ref.group_key if isinstance(ref, CompletionRef) else str(ref)
            for ref in req.complete_groups
        ]
        return IngestResponse(
            accepted=len(req.points),
            seq_from=1 if req.points else None,
            seq_to=len(req.points) if req.points else None,
            completed=completed,
            server_ts=datetime.now(timezone.utc),
        )


@pytest.fixture(autouse=True)
def _reset_fake_clients():
    FakeClient.instances.clear()
    yield
    FakeClient.instances.clear()


@pytest.fixture
def patch_client(monkeypatch):
    """Patch ``LiveBenchClient`` everywhere the commands import it."""

    monkeypatch.setattr(emit_cmd, "LiveBenchClient", FakeClient)
    monkeypatch.setattr(complete_cmd, "LiveBenchClient", FakeClient)
    monkeypatch.setattr(stream_cmd, "LiveBenchClient", FakeClient)
    yield


# ── emit single ───────────────────────────────────────────────
def test_emit_single_stamps_client_ts_at_read_time(patch_client) -> None:
    runner = CliRunner()
    t0 = datetime.now(timezone.utc)
    result = runner.invoke(
        cli,
        [
            "emit",
            "test-drive-lr",
            "--group",
            "alpha",
            "--metric",
            "latency_ms",
            "--value",
            "42",
        ],
    )
    t1 = datetime.now(timezone.utc)
    assert result.exit_code == 0, result.output

    assert len(FakeClient.instances) == 1
    fc = FakeClient.instances[0]
    assert len(fc.requests) == 1
    req = fc.requests[0]
    assert req.session_id == "test-drive-lr"
    assert len(req.points) == 1
    p = req.points[0]
    assert p.group_key == "alpha"
    assert p.metric_key == "latency_ms"
    assert p.value == 42.0
    # Stamped within the window of the test.
    assert (t0 - timedelta(seconds=1)) <= p.client_ts <= (t1 + timedelta(seconds=1))


def test_emit_single_and_batch_are_mutually_exclusive(patch_client) -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "emit",
            "sess",
            "--group",
            "a",
            "--metric",
            "m",
            "--value",
            "1",
            "--batch",
            "-",
        ],
    )
    assert result.exit_code != 0
    assert "mutually exclusive" in result.output.lower()


# ── emit batch ────────────────────────────────────────────────
def test_emit_batch_passes_through_explicit_client_ts(patch_client) -> None:
    runner = CliRunner()
    line = json.dumps(
        {
            "group": "alpha",
            "metric": "latency_ms",
            "value": 99.0,
            "client_ts": "2030-01-01T00:00:00.000000+00:00",
        }
    )
    result = runner.invoke(cli, ["emit", "sess", "--batch", "-"], input=line + "\n")
    assert result.exit_code == 0, result.output

    req = FakeClient.instances[0].requests[0]
    assert len(req.points) == 1
    p = req.points[0]
    expected = datetime(2030, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)
    assert p.client_ts == expected


def test_emit_batch_stamps_lines_without_client_ts(patch_client) -> None:
    runner = CliRunner()
    t0 = datetime.now(timezone.utc)
    line = json.dumps({"group": "alpha", "metric": "latency_ms", "value": 10.0})
    result = runner.invoke(cli, ["emit", "sess", "--batch", "-"], input=line + "\n")
    t1 = datetime.now(timezone.utc)
    assert result.exit_code == 0, result.output

    req = FakeClient.instances[0].requests[0]
    p = req.points[0]
    assert (t0 - timedelta(seconds=1)) <= p.client_ts <= (t1 + timedelta(seconds=1))


# ── emit --chart flag ─────────────────────────────────────────
def test_emit_single_default_chart(patch_client) -> None:
    """Without --chart, single-mode emits a DataPoint with chart_id='default'."""

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "emit",
            "test-drive-lr",
            "--group",
            "alpha",
            "--metric",
            "latency_ms",
            "--value",
            "42",
        ],
    )
    assert result.exit_code == 0, result.output

    req = FakeClient.instances[0].requests[0]
    assert len(req.points) == 1
    assert req.points[0].chart_id == "default"


def test_emit_single_with_chart_flag(patch_client) -> None:
    """--chart recall stamps chart_id='recall' on the single-mode DataPoint."""

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "emit",
            "test-drive-lr",
            "--chart",
            "recall",
            "--group",
            "alpha",
            "--metric",
            "latency_ms",
            "--value",
            "42",
        ],
    )
    assert result.exit_code == 0, result.output

    req = FakeClient.instances[0].requests[0]
    assert len(req.points) == 1
    assert req.points[0].chart_id == "recall"
    assert req.points[0].group_key == "alpha"
    assert req.points[0].metric_key == "latency_ms"
    assert req.points[0].value == 42.0


def test_emit_batch_passes_through_explicit_chart_id(patch_client) -> None:
    """A JSONL line with its own chart_id wins over --chart and the default."""

    runner = CliRunner()
    line = json.dumps(
        {
            "chart_id": "qps",
            "group_key": "alpha",
            "metric_key": "queries_per_sec",
            "value": 12500.0,
        }
    )
    result = runner.invoke(
        cli,
        ["emit", "sess", "--chart", "recall", "--batch", "-"],
        input=line + "\n",
    )
    assert result.exit_code == 0, result.output

    req = FakeClient.instances[0].requests[0]
    assert len(req.points) == 1
    p = req.points[0]
    assert p.chart_id == "qps"  # explicit chart_id wins over --chart flag
    assert p.group_key == "alpha"
    assert p.value == 12500.0


def test_emit_batch_defaults_to_default_chart(patch_client) -> None:
    """A JSONL line without chart_id and no --chart flag → chart_id='default'."""

    runner = CliRunner()
    line = json.dumps({"group": "alpha", "metric": "latency_ms", "value": 7.0})
    result = runner.invoke(cli, ["emit", "sess", "--batch", "-"], input=line + "\n")
    assert result.exit_code == 0, result.output

    req = FakeClient.instances[0].requests[0]
    assert req.points[0].chart_id == "default"


def test_emit_batch_falls_back_to_chart_flag(patch_client) -> None:
    """A JSONL line without chart_id inherits the --chart flag value."""

    runner = CliRunner()
    line = json.dumps({"group": "alpha", "metric": "latency_ms", "value": 7.0})
    result = runner.invoke(
        cli,
        ["emit", "sess", "--chart", "recall", "--batch", "-"],
        input=line + "\n",
    )
    assert result.exit_code == 0, result.output

    req = FakeClient.instances[0].requests[0]
    assert req.points[0].chart_id == "recall"


# ── complete ──────────────────────────────────────────────────
def test_complete_command_builds_empty_points_request(patch_client) -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["complete", "test-drive-lr", "--group", "alpha", "--group", "bravo"],
    )
    assert result.exit_code == 0, result.output

    req = FakeClient.instances[0].requests[0]
    assert req.session_id == "test-drive-lr"
    assert req.points == []
    # complete_groups is a list[CompletionRef]; without --chart the command
    # defaults to chart_id="default" for every group.
    assert req.complete_groups == [
        CompletionRef(chart_id="default", group_key="alpha"),
        CompletionRef(chart_id="default", group_key="bravo"),
    ]


def test_complete_command_default_chart(patch_client) -> None:
    """Invoking without --chart stamps chart_id='default' on every ref."""

    runner = CliRunner()
    result = runner.invoke(
        cli, ["complete", "sess", "--group", "alpha"]
    )
    assert result.exit_code == 0, result.output

    req = FakeClient.instances[0].requests[0]
    assert len(req.complete_groups) == 1
    ref = req.complete_groups[0]
    assert ref.chart_id == "default"
    assert ref.group_key == "alpha"


def test_complete_command_with_chart_flag(patch_client) -> None:
    """--chart recall applies to ALL --group flags in the same invocation."""

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "complete",
            "test-drive-lr",
            "--chart",
            "recall",
            "--group",
            "alpha",
            "--group",
            "bravo",
        ],
    )
    assert result.exit_code == 0, result.output

    req = FakeClient.instances[0].requests[0]
    assert req.complete_groups == [
        CompletionRef(chart_id="recall", group_key="alpha"),
        CompletionRef(chart_id="recall", group_key="bravo"),
    ]


# ── stream ────────────────────────────────────────────────────
def test_stream_batches_preserve_order(patch_client) -> None:
    runner = CliRunner()
    lines = [
        json.dumps({"group": "alpha", "metric": "latency_ms", "value": float(i)})
        for i in range(5)
    ]
    input_text = "\n".join(lines) + "\n"
    result = runner.invoke(
        cli,
        ["stream", "sess", "--flush-ms", "5", "--max-batch", "100"],
        input=input_text,
    )
    assert result.exit_code == 0, result.output

    # Collect all points across all flushes in order.
    all_points = []
    for req in FakeClient.instances[0].requests:
        all_points.extend(req.points)
    assert len(all_points) == 5
    assert [p.value for p in all_points] == [0.0, 1.0, 2.0, 3.0, 4.0]
    # Non-decreasing client_ts.
    for prev, nxt in zip(all_points, all_points[1:]):
        assert prev.client_ts <= nxt.client_ts


def test_stream_recognises_complete_control_lines(patch_client) -> None:
    runner = CliRunner()
    lines = [
        json.dumps({"complete": "alpha"}),
        json.dumps({"group": "alpha", "metric": "latency_ms", "value": 1.0}),
    ]
    input_text = "\n".join(lines) + "\n"
    result = runner.invoke(
        cli,
        ["stream", "sess", "--flush-ms", "5", "--max-batch", "100"],
        input=input_text,
    )
    assert result.exit_code == 0, result.output

    all_points = []
    all_completes: list[CompletionRef] = []
    for req in FakeClient.instances[0].requests:
        all_points.extend(req.points)
        all_completes.extend(req.complete_groups)
    # Default chart when no --chart flag and no line-level chart.
    assert all_completes == [CompletionRef(chart_id="default", group_key="alpha")]
    assert len(all_points) == 1
    assert all_points[0].value == 1.0
    assert all_points[0].chart_id == "default"


def test_stream_recognises_chart_in_control_line(patch_client) -> None:
    """A control line's own ``chart`` field wins over the --chart flag default."""

    runner = CliRunner()
    line = json.dumps({"complete": "alpha", "chart": "recall"})
    result = runner.invoke(
        cli,
        ["stream", "sess", "--flush-ms", "5", "--max-batch", "100"],
        input=line + "\n",
    )
    assert result.exit_code == 0, result.output

    all_completes: list[CompletionRef] = []
    for req in FakeClient.instances[0].requests:
        all_completes.extend(req.complete_groups)
    assert len(all_completes) == 1
    ref = all_completes[0]
    assert ref.chart_id == "recall"
    assert ref.group_key == "alpha"


def test_stream_chart_flag_applies_to_data_and_control_lines(patch_client) -> None:
    """The --chart flag supplies a default for lines that omit their own chart."""

    runner = CliRunner()
    lines = [
        json.dumps({"group": "alpha", "metric": "latency_ms", "value": 1.0}),
        json.dumps({"complete": "alpha"}),
    ]
    input_text = "\n".join(lines) + "\n"
    result = runner.invoke(
        cli,
        [
            "stream",
            "sess",
            "--chart",
            "qps",
            "--flush-ms",
            "5",
            "--max-batch",
            "100",
        ],
        input=input_text,
    )
    assert result.exit_code == 0, result.output

    all_points = []
    all_completes: list[CompletionRef] = []
    for req in FakeClient.instances[0].requests:
        all_points.extend(req.points)
        all_completes.extend(req.complete_groups)
    assert len(all_points) == 1
    assert all_points[0].chart_id == "qps"
    assert all_completes == [CompletionRef(chart_id="qps", group_key="alpha")]

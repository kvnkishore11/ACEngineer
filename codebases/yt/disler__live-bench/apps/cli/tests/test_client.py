"""Tests for ``live_bench_cli.client``.

Covers:
* ``now_ts()`` is timezone-aware UTC.
* Happy-path ``ingest`` round-trip.
* 5xx → exponential-backoff retry → eventual success.
* Hard failure writes the unsent batch to the outbox preserving its
  original ``client_ts`` (no replay-time overwrites).
* Outbox is drained on the next call before the new request is sent,
  and drained lines preserve their original ``client_ts``.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import httpx
import pytest

from live_bench_cli.client import (
    LiveBenchClient,
    LiveBenchError,
    OUTBOX_FILENAME,
    now_ts,
)
from live_bench_cli.models import IngestRequest
from live_bench_server.models import DataPoint


# ── helpers ───────────────────────────────────────────────────
def _make_request() -> IngestRequest:
    return IngestRequest(
        session_id="test-session",
        request_ts=datetime(2026, 4, 7, 14, 22, 19, 318204, tzinfo=timezone.utc),
        points=[
            DataPoint(
                group_key="alpha",
                metric_key="latency_ms",
                value=42.0,
                client_ts=datetime(
                    2026, 4, 7, 14, 22, 19, 104872, tzinfo=timezone.utc
                ),
            )
        ],
    )


def _ok_response() -> dict:
    return {
        "accepted": 1,
        "seq_from": 1,
        "seq_to": 1,
        "completed": [],
        "server_ts": "2026-04-07T14:22:19.402118+00:00",
    }


def _client_with_transport(transport: httpx.MockTransport) -> LiveBenchClient:
    """Build a ``LiveBenchClient`` whose underlying httpx client uses ``transport``."""

    client = LiveBenchClient("http://test.invalid")
    # Replace the inner httpx.Client with one bound to the mock transport.
    client._client.close()
    client._client = httpx.Client(
        base_url="http://test.invalid",
        transport=transport,
        headers={"Content-Type": "application/json"},
        timeout=5.0,
    )
    return client


# ── now_ts ────────────────────────────────────────────────────
def test_now_ts_is_aware_utc() -> None:
    ts = now_ts()
    assert isinstance(ts, datetime)
    assert ts.tzinfo is not None
    assert ts.utcoffset() == timezone.utc.utcoffset(ts)


# ── happy path ────────────────────────────────────────────────
def test_ingest_happy_path(monkeypatch, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)

    captured: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/ingest"
        captured.append(json.loads(request.content))
        return httpx.Response(200, json=_ok_response())

    transport = httpx.MockTransport(handler)
    with _client_with_transport(transport) as client:
        resp = client.ingest(_make_request())

    assert resp.accepted == 1
    assert resp.seq_from == 1
    assert resp.seq_to == 1
    assert len(captured) == 1
    body = captured[0]
    assert body["session_id"] == "test-session"
    assert body["points"][0]["client_ts"] == "2026-04-07T14:22:19.104872+00:00"


# ── retries ───────────────────────────────────────────────────
def test_ingest_retries_on_5xx(monkeypatch, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)
    # Make sleeps free for the test.
    monkeypatch.setattr("live_bench_cli.client.time.sleep", lambda *_a, **_k: None)

    counter = {"calls": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        counter["calls"] += 1
        if counter["calls"] < 3:
            return httpx.Response(503, json={"code": "boom", "message": "no"})
        return httpx.Response(200, json=_ok_response())

    transport = httpx.MockTransport(handler)
    with _client_with_transport(transport) as client:
        resp = client.ingest(_make_request())

    assert resp.accepted == 1
    assert counter["calls"] == 3


def test_ingest_does_not_retry_on_4xx(monkeypatch, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("live_bench_cli.client.time.sleep", lambda *_a, **_k: None)

    counter = {"calls": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        counter["calls"] += 1
        return httpx.Response(
            400, json={"code": "unknown_group", "message": "no such group"}
        )

    transport = httpx.MockTransport(handler)
    with _client_with_transport(transport) as client:
        with pytest.raises(LiveBenchError) as excinfo:
            client.ingest(_make_request())

    assert counter["calls"] == 1
    assert excinfo.value.status_code == 400
    assert excinfo.value.code == "unknown_group"


# ── outbox on hard failure ────────────────────────────────────
def test_ingest_outbox_on_hard_failure(monkeypatch, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("live_bench_cli.client.time.sleep", lambda *_a, **_k: None)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, json={"code": "down", "message": "off"})

    transport = httpx.MockTransport(handler)
    req = _make_request()
    with _client_with_transport(transport) as client:
        with pytest.raises(LiveBenchError):
            client.ingest(req)

    outbox = Path(tmp_path) / OUTBOX_FILENAME
    assert outbox.exists()
    lines = outbox.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    body = json.loads(lines[0])
    # The original client_ts is preserved verbatim — NOT replaced by retry time.
    assert body["points"][0]["client_ts"] == "2026-04-07T14:22:19.104872+00:00"
    assert body["session_id"] == "test-session"


# ── outbox drains first ───────────────────────────────────────
def test_outbox_drains_first(monkeypatch, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("live_bench_cli.client.time.sleep", lambda *_a, **_k: None)

    # Pre-seed an outbox line with a distinctive original client_ts.
    pre_seeded = {
        "session_id": "test-session",
        "request_ts": "2025-01-01T00:00:00.000000+00:00",
        "points": [
            {
                "group_key": "alpha",
                "metric_key": "latency_ms",
                "value": 7.0,
                "client_ts": "2025-01-01T00:00:00.000000+00:00",
            }
        ],
        "complete_groups": [],
    }
    outbox = Path(tmp_path) / OUTBOX_FILENAME
    outbox.write_text(json.dumps(pre_seeded) + "\n", encoding="utf-8")

    captured_bodies: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured_bodies.append(json.loads(request.content))
        return httpx.Response(200, json=_ok_response())

    transport = httpx.MockTransport(handler)
    with _client_with_transport(transport) as client:
        client.ingest(_make_request())

    # Two POSTs total: drained line first, then the new request.
    assert len(captured_bodies) == 2
    drained = captured_bodies[0]
    fresh = captured_bodies[1]

    # Drained line preserved its client_ts verbatim.
    assert drained["points"][0]["client_ts"] == "2025-01-01T00:00:00.000000+00:00"
    assert drained["points"][0]["value"] == 7.0
    # The fresh request is the one we just built.
    assert fresh["points"][0]["client_ts"] == "2026-04-07T14:22:19.104872+00:00"
    assert fresh["points"][0]["value"] == 42.0
    # Outbox file removed after successful drain.
    assert not outbox.exists()

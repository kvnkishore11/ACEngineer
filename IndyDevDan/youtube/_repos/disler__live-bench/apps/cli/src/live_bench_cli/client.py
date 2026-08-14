"""HTTP client for talking to the live-bench backend.

This module owns the single source of truth for CLI client timestamps —
``now_ts()`` — and the ``LiveBenchClient`` wrapper around ``httpx.Client``
that every command in this package uses to talk to the backend.

Spec references:
    §7  — CLI shape and command list
    §9  — wire protocol (POST /ingest, REST endpoints, error shapes)
    §15 — transport decision; outbox + client_ts rationale
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx

from .models import IngestRequest, IngestResponse


# ── Timestamp source of truth ─────────────────────────────────
def now_ts() -> datetime:
    """Return the current wall-clock instant as an aware UTC ``datetime``.

    This is the **single source of CLI timestamps** for the whole package.
    Every command that needs a ``client_ts`` or ``request_ts`` calls this
    function — never ``datetime.now()`` directly. Tests that need to control
    time can monkeypatch this name.
    """

    return datetime.now(timezone.utc)


# ── Errors ────────────────────────────────────────────────────
class LiveBenchError(Exception):
    """Raised when the backend returns a non-2xx response (after retries).

    ``status_code`` is the HTTP status, ``code`` is the backend's machine
    code (e.g. ``unknown_session``), and ``message`` is a human-readable
    description. Both ``code`` and ``message`` come from the parsed error
    JSON when available.
    """

    def __init__(
        self,
        status_code: int,
        code: str | None = None,
        message: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        parts = [f"HTTP {status_code}"]
        if code:
            parts.append(code)
        if message:
            parts.append(message)
        super().__init__(" — ".join(parts))


# ── Constants ─────────────────────────────────────────────────
OUTBOX_FILENAME = ".live-bench-outbox.jsonl"
RETRY_BACKOFFS_S = (0.1, 0.3, 0.9)  # 100ms, 300ms, 900ms — 3 retries on 5xx


# ── Client ────────────────────────────────────────────────────
class LiveBenchClient:
    """Thin wrapper around ``httpx.Client`` for the live-bench REST API.

    Holds a single keep-alive HTTP/1.1 client for the lifetime of the CLI
    invocation. Methods correspond 1:1 with the backend REST endpoints
    described in spec §9.3.
    """

    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self.base_url = base_url
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers={"Content-Type": "application/json"},
        )

    # ── lifecycle ─────────────────────────────────────────
    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "LiveBenchClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    # ── REST methods ──────────────────────────────────────
    def list_benchmarks(self) -> dict[str, Any]:
        """``GET /benchmarks`` → parsed JSON dict."""

        r = self._client.get("/benchmarks")
        self._raise_for_status(r)
        return r.json()

    def get_benchmark(self, session_id: str) -> dict[str, Any]:
        """``GET /benchmarks/{id}`` → parsed JSON dict."""

        r = self._client.get(f"/benchmarks/{session_id}")
        self._raise_for_status(r)
        return r.json()

    def reset(self, session_id: str) -> dict[str, Any]:
        """``POST /benchmarks/{id}/reset`` → parsed JSON dict."""

        r = self._client.post(f"/benchmarks/{session_id}/reset")
        self._raise_for_status(r)
        return r.json()

    def ingest(self, req: IngestRequest) -> IngestResponse:
        """``POST /ingest`` → ``IngestResponse``.

        Drains any pending outbox first (preserving each line's original
        ``client_ts``), then sends ``req`` with retries on 5xx. On hard
        failure the unsent batch is appended to ``.live-bench-outbox.jsonl``
        in the current working directory and a ``LiveBenchError`` is raised.
        """

        # Drain outbox first — its lines were captured earlier with their own
        # client_ts. Any lines that still fail go back into the outbox; we
        # surface the new request's failure first if both fail.
        self._drain_outbox()

        body = req.model_dump_json()
        try:
            data = self._post_with_retries("/ingest", body)
        except LiveBenchError:
            self._append_outbox(body)
            raise
        return IngestResponse.model_validate(data)

    # ── internals ─────────────────────────────────────────
    def _post_with_retries(self, path: str, body: str) -> dict[str, Any]:
        """POST ``body`` to ``path`` with exponential backoff on 5xx.

        Returns parsed JSON on 2xx. Raises ``LiveBenchError`` immediately on
        4xx (no retry) and after the final attempt on 5xx.
        """

        last_error: LiveBenchError | None = None
        # 1 initial attempt + len(RETRY_BACKOFFS_S) retries.
        for attempt in range(len(RETRY_BACKOFFS_S) + 1):
            try:
                r = self._client.post(path, content=body)
            except httpx.RequestError as exc:
                # Treat connection-level failures as retryable.
                last_error = LiveBenchError(0, "transport_error", str(exc))
                if attempt < len(RETRY_BACKOFFS_S):
                    time.sleep(RETRY_BACKOFFS_S[attempt])
                    continue
                raise last_error

            if 200 <= r.status_code < 300:
                return r.json()

            if 400 <= r.status_code < 500:
                # Client errors are not retried; surface immediately.
                code, message = self._parse_error_body(r)
                raise LiveBenchError(r.status_code, code, message)

            # 5xx — retryable.
            code, message = self._parse_error_body(r)
            last_error = LiveBenchError(r.status_code, code, message)
            if attempt < len(RETRY_BACKOFFS_S):
                time.sleep(RETRY_BACKOFFS_S[attempt])
                continue

        assert last_error is not None
        raise last_error

    @staticmethod
    def _parse_error_body(r: httpx.Response) -> tuple[str | None, str | None]:
        try:
            data = r.json()
        except Exception:
            return None, r.text or None
        if isinstance(data, dict):
            return data.get("code"), data.get("message")
        return None, str(data)

    def _raise_for_status(self, r: httpx.Response) -> None:
        if 200 <= r.status_code < 300:
            return
        code, message = self._parse_error_body(r)
        raise LiveBenchError(r.status_code, code, message)

    # ── outbox ────────────────────────────────────────────
    @staticmethod
    def _outbox_path() -> Path:
        return Path.cwd() / OUTBOX_FILENAME

    def _append_outbox(self, body: str) -> None:
        """Append the raw JSON request body as one line to the outbox.

        ``body`` is the already-serialised ``IngestRequest`` from the caller,
        so the original ``client_ts`` and ``request_ts`` are preserved
        verbatim — replay must not re-stamp anything.
        """

        path = self._outbox_path()
        with path.open("a", encoding="utf-8") as fp:
            fp.write(body)
            fp.write("\n")

    def _drain_outbox(self) -> None:
        """Replay any pending outbox lines through ``/ingest``.

        Each line is a JSON-serialised ``IngestRequest`` from a previous run.
        Lines that succeed are removed; lines that still fail are written
        back to the outbox file. Original ``client_ts`` values are preserved
        — we POST the body verbatim and never re-stamp.
        """

        path = self._outbox_path()
        if not path.exists():
            return

        try:
            raw_lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            return

        lines = [ln for ln in raw_lines if ln.strip()]
        if not lines:
            # Empty file — clean it up.
            try:
                path.unlink()
            except OSError:
                pass
            return

        still_failing: list[str] = []
        for line in lines:
            try:
                self._post_with_retries("/ingest", line)
            except LiveBenchError:
                still_failing.append(line)

        if still_failing:
            with path.open("w", encoding="utf-8") as fp:
                for line in still_failing:
                    fp.write(line)
                    fp.write("\n")
        else:
            try:
                path.unlink()
            except OSError:
                pass


__all__ = ["now_ts", "LiveBenchClient", "LiveBenchError", "OUTBOX_FILENAME"]

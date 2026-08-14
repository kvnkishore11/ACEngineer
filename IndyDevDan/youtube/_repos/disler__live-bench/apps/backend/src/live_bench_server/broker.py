"""In-process pub/sub broker for SSE fan-out.

One ``LiveBroker`` per process (stashed on ``app.state``). SSE handlers call
``subscribe(session_id)`` to get a fresh ``asyncio.Queue``; the ingest handler
calls ``publish(session_id, event)`` which fans out to every subscriber queue
for that session.

Overflow policy: if a queue is at capacity, drop the oldest item (FIFO) to
keep the newest events flowing, and log a WARN with the session id + queue
length. This favours liveness over completeness — SSE reconnect with
``Last-Event-ID`` can recover any dropped ``datapoint`` events from SQLite.
"""

from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Any

from live_bench_server.logging import get_logger

log = get_logger(__name__)


class LiveBroker:
    def __init__(self, queue_cap: int = 1024) -> None:
        self._queue_cap = queue_cap
        # session_id -> list of subscribed queues
        self._subs: dict[str, list[asyncio.Queue[Any]]] = defaultdict(list)
        self._lock = asyncio.Lock()

    def subscribe(self, session_id: str) -> asyncio.Queue[Any]:
        """Create a new queue subscribed to events for ``session_id``."""
        q: asyncio.Queue[Any] = asyncio.Queue(maxsize=self._queue_cap)
        self._subs[session_id].append(q)
        return q

    def unsubscribe(self, session_id: str, queue: asyncio.Queue[Any]) -> None:
        """Remove a previously-subscribed queue. Safe to call repeatedly."""
        subs = self._subs.get(session_id)
        if not subs:
            return
        try:
            subs.remove(queue)
        except ValueError:
            pass
        if not subs:
            self._subs.pop(session_id, None)

    def publish(self, session_id: str, event: Any) -> None:
        """Fan out ``event`` to every subscriber for ``session_id``.

        Synchronous — called from request handlers running inside the asyncio
        loop. If a queue is full, drops the oldest enqueued event to make room
        and logs a WARN.
        """
        subs = self._subs.get(session_id)
        if not subs:
            return
        for q in list(subs):
            try:
                q.put_nowait(event)
            except asyncio.QueueFull:
                # Drop the oldest to make room for the newest. SSE resume via
                # Last-Event-ID will recover from SQLite if the consumer cares.
                try:
                    q.get_nowait()
                except Exception:
                    pass
                log.warning(
                    "broker queue full, dropped oldest event session_id=%s queue_size=%d",
                    session_id,
                    q.qsize(),
                )
                try:
                    q.put_nowait(event)
                except asyncio.QueueFull:
                    # Still full (shouldn't happen). Drop this event too.
                    log.warning(
                        "broker dropped new event after eviction session_id=%s",
                        session_id,
                    )

    def broadcast_all(self, event: Any) -> None:
        """Fan out ``event`` to every subscriber across ALL sessions."""
        for session_id in list(self._subs.keys()):
            self.publish(session_id, event)

    async def drain(self) -> None:
        """Close all subscriptions. Called on app shutdown."""
        async with self._lock:
            self._subs.clear()


__all__ = ["LiveBroker"]

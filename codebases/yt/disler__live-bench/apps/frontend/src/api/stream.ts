// SSE client for /stream/:sessionId.
//
// Wraps EventSource with:
//   - Zod-validated event payloads (parseSseEvent throws on drift)
//   - explicit handlers for each event type
//   - reconnect with exponential backoff (1s → cap 30s)
//   - a connection-state callback so the UI can render a status badge
//
// Returns a `close()` function that tears down the EventSource and stops any
// pending reconnect timer.

import {
  parseSseEvent,
  type SseSnapshot,
  type SseDatapoint,
  type SseDatasetComplete,
  type SseReset,
  type SseConfigChanged,
  type SseMetadata,
} from '../schemas'

export type ConnectionState =
  | 'connecting'
  | 'live'
  | 'ping_received'
  | 'reconnecting'
  | 'disconnected'

export interface StreamHandlers {
  onSnapshot: (event: SseSnapshot) => void
  onDatapoint: (event: SseDatapoint) => void
  onDatasetComplete: (event: SseDatasetComplete) => void
  onReset: (event: SseReset) => void
  onConfigChanged: (event: SseConfigChanged) => void
  onMetadata: (event: SseMetadata) => void
  onConnectionStateChange: (state: ConnectionState) => void
}

export interface StreamHandle {
  close: () => void
}

const RECONNECT_INITIAL_MS = 1000
const RECONNECT_MAX_MS = 30_000

export function connectStream(sessionId: string, handlers: StreamHandlers): StreamHandle {
  let source: EventSource | null = null
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null
  let backoffMs = RECONNECT_INITIAL_MS
  let closed = false

  const setState = (state: ConnectionState) => handlers.onConnectionStateChange(state)

  const safeParse = <T>(raw: unknown, picker: (e: ReturnType<typeof parseSseEvent>) => T | null): T | null => {
    try {
      const parsed = parseSseEvent(raw)
      return picker(parsed)
    } catch (err) {
      console.error('[live-bench] SSE parse error', err, raw)
      return null
    }
  }

  const open = () => {
    if (closed) return
    setState('connecting')
    const url = `/stream/${encodeURIComponent(sessionId)}`
    source = new EventSource(url)

    source.onopen = () => {
      backoffMs = RECONNECT_INITIAL_MS
      setState('live')
    }

    source.addEventListener('snapshot', (ev) => {
      const me = ev as MessageEvent
      const event = safeParse(JSON.parse(me.data), (e) => (e.event === 'snapshot' ? e : null))
      if (event) handlers.onSnapshot(event)
    })

    source.addEventListener('datapoint', (ev) => {
      const me = ev as MessageEvent
      const event = safeParse(JSON.parse(me.data), (e) => (e.event === 'datapoint' ? e : null))
      if (event) handlers.onDatapoint(event)
    })

    source.addEventListener('dataset_complete', (ev) => {
      const me = ev as MessageEvent
      const event = safeParse(JSON.parse(me.data), (e) => (e.event === 'dataset_complete' ? e : null))
      if (event) handlers.onDatasetComplete(event)
    })

    source.addEventListener('reset', (ev) => {
      const me = ev as MessageEvent
      const event = safeParse(JSON.parse(me.data), (e) => (e.event === 'reset' ? e : null))
      if (event) handlers.onReset(event)
    })

    source.addEventListener('config_changed', (ev) => {
      const me = ev as MessageEvent
      const event = safeParse(JSON.parse(me.data), (e) => (e.event === 'config_changed' ? e : null))
      if (event) handlers.onConfigChanged(event)
    })

    source.addEventListener('metadata', (ev) => {
      const me = ev as MessageEvent
      const event = safeParse(JSON.parse(me.data), (e) => (e.event === 'metadata' ? e : null))
      if (event) handlers.onMetadata(event)
    })

    source.addEventListener('ping', () => {
      setState('ping_received')
      setTimeout(() => {
        if (!closed) setState('live')
      }, 3000)
    })

    source.onerror = () => {
      if (closed) return
      // EventSource auto-reconnects on its own, but on some browsers / on
      // total network failure it sticks in CLOSED. Tear it down ourselves and
      // schedule a backoff retry — the browser handles `Last-Event-ID`
      // automatically when we open a fresh EventSource against the same URL,
      // since the backend stamps `id:` on every event.
      try {
        source?.close()
      } catch {
        /* swallow */
      }
      source = null
      setState('reconnecting')
      reconnectTimer = setTimeout(() => {
        reconnectTimer = null
        backoffMs = Math.min(backoffMs * 2, RECONNECT_MAX_MS)
        open()
      }, backoffMs)
    }
  }

  open()

  return {
    close: () => {
      closed = true
      if (reconnectTimer !== null) {
        clearTimeout(reconnectTimer)
        reconnectTimer = null
      }
      try {
        source?.close()
      } catch {
        /* swallow */
      }
      source = null
      setState('disconnected')
    },
  }
}

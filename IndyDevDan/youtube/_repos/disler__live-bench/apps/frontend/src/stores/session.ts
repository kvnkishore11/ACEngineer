// Per-session live state — the heart of the live-bench UI. The chart binds
// directly to this store; SSE handlers in BenchmarkPage call its actions.
//
// Two key invariants:
//
//   1. `latest` is always the most recent value PER
//      (chart_id, group_key, metric_key) cell, ordered by `client_ts` not by
//      arrival time. This is the §14.4 newer-wins guard — late packets
//      (from out-of-order delivery, SSE replay after reconnect, or laggy
//      machines) are silently dropped without ever twitching the bar.
//
//   2. `latestClientTs` is the parallel map used by the guard. ISO-8601 UTC
//      with fixed-width microsecond precision sorts lexicographically, so we
//      compare with `<` / `>` directly — no Date parsing on the hot path.
//
// Maps are mutated in-place but reactivity is preserved by reassigning the
// containing slot via `this.<map> = new Map(this.<map>)` after writes — Pinia
// only deep-tracks Maps via reference replacement.
//
// Key shape
// ---------
// Cell keys are `${chart_id}:${group_key}:${metric_key}` and dataset keys are
// `${chart_id}:${group_key}`. The chart_id prefix isolates state across
// charts inside a multi-chart benchmark — an update on (chart=recall,
// group=faiss, metric=recall) does NOT touch (chart=qps, group=faiss,
// metric=qps). Single-chart legacy benchmarks all use chart_id="default" so
// the prefix is a no-op for them.

import { defineStore } from 'pinia'
import type {
  BenchmarkConfig,
  DataPointStored,
  DatasetState,
  SseSnapshot,
} from '../schemas'

export type CellKey = string // `${chart_id}:${group_key}:${metric_key}`
export type DatasetKey = string // `${chart_id}:${group_key}`

interface SessionStoreState {
  config: BenchmarkConfig | null
  latest: Map<CellKey, number>
  latestClientTs: Map<CellKey, string>
  datasets: Map<DatasetKey, DatasetState>
  lastUpdate: string | null // ISO server_ts of the most recently accepted point
  /** Chart IDs that just received a datapoint — drives the card pulse animation. */
  updatedCharts: Set<string>
  /** Chart IDs that just had a group complete — drives the card green flash. */
  completedCharts: Set<string>
  /** Per-group metadata keyed by `${chart_id}:${group_key}`. */
  metadata: Map<DatasetKey, Record<string, any>>
}

function cellKey(chart_id: string, group_key: string, metric_key: string): CellKey {
  return `${chart_id}:${group_key}:${metric_key}`
}

function datasetKey(chart_id: string, group_key: string): DatasetKey {
  return `${chart_id}:${group_key}`
}

export const useSessionStore = defineStore('session', {
  state: (): SessionStoreState => ({
    config: null,
    latest: new Map(),
    latestClientTs: new Map(),
    datasets: new Map(),
    lastUpdate: null,
    updatedCharts: new Set(),
    completedCharts: new Set(),
    metadata: new Map(),
  }),
  actions: {
    /**
     * Replace all session state from a fresh /stream snapshot. The backend
     * delivers `points` already as latest-per-cell ordered by `client_ts`,
     * so we don't need the guard here — every point unconditionally wins.
     */
    applySnapshot(snapshot: SseSnapshot) {
      this.config = snapshot.config

      const latest = new Map<CellKey, number>()
      const latestTs = new Map<CellKey, string>()
      let mostRecentServerTs: string | null = null

      for (const point of snapshot.points) {
        const key = cellKey(point.chart_id, point.group_key, point.metric_key)
        latest.set(key, point.value)
        latestTs.set(key, point.client_ts)
        if (mostRecentServerTs === null || point.server_ts > mostRecentServerTs) {
          mostRecentServerTs = point.server_ts
        }
      }

      this.latest = latest
      this.latestClientTs = latestTs
      this.datasets = new Map(
        snapshot.datasets.map((d) => [datasetKey(d.chart_id, d.group_key), d]),
      )
      this.lastUpdate = mostRecentServerTs
    },

    /**
     * Apply a single live datapoint with the §14.4 newer-wins guard.
     *
     * Comparison is direct string comparison on the ISO-8601 timestamps — both
     * the CLI and backend always emit fixed-width 6-digit microsecond
     * precision so this is lexicographically safe. The cell key includes
     * `chart_id`, so out-of-order points on one chart cannot regress bars on
     * a different chart even if their group/metric happen to collide.
     */
    applyDatapoint(point: DataPointStored) {
      const key = cellKey(point.chart_id, point.group_key, point.metric_key)
      const prev = this.latestClientTs.get(key)
      if (prev !== undefined && point.client_ts <= prev) {
        // Stale or duplicate replay — drop silently. The bar does not twitch.
        return
      }

      const nextLatest = new Map(this.latest)
      nextLatest.set(key, point.value)
      this.latest = nextLatest

      const nextTs = new Map(this.latestClientTs)
      nextTs.set(key, point.client_ts)
      this.latestClientTs = nextTs

      this.lastUpdate = point.server_ts

      // Signal the card to flash.
      this.updatedCharts = new Set([...this.updatedCharts, point.chart_id])

      // First point in a previously-pending dataset flips the status to
      // running. The §14.4 guard above ensures replay-stale points don't
      // accidentally rewind a running dataset back to pending.
      const dskey = datasetKey(point.chart_id, point.group_key)
      const ds = this.datasets.get(dskey)
      if (ds && ds.status === 'pending') {
        const nextDatasets = new Map(this.datasets)
        nextDatasets.set(dskey, {
          ...ds,
          status: 'running',
          started_at: point.client_ts,
        })
        this.datasets = nextDatasets
      }
    },

    applyDatasetComplete(chart_id: string, group_key: string, completed_at: string) {
      const dskey = datasetKey(chart_id, group_key)
      const ds = this.datasets.get(dskey)
      if (!ds) return
      const nextDatasets = new Map(this.datasets)
      nextDatasets.set(dskey, { ...ds, status: 'complete', completed_at })
      this.datasets = nextDatasets

      // Signal the card to flash green.
      this.completedCharts = new Set([...this.completedCharts, chart_id])
    },

    /**
     * Apply metadata for a (chart, group) pair. Merges into existing —
     * the backend already performs the deep merge, so we just replace.
     */
    applyMetadata(chart_id: string, group_key: string, data: Record<string, any>) {
      const key = datasetKey(chart_id, group_key)
      const next = new Map(this.metadata)
      next.set(key, data)
      this.metadata = next
    },

    /** Clear flash signal for a chart (called by BenchmarkCard after animation). */
    clearUpdated(chartId: string) {
      const next = new Set(this.updatedCharts)
      next.delete(chartId)
      this.updatedCharts = next
    },
    clearCompleted(chartId: string) {
      const next = new Set(this.completedCharts)
      next.delete(chartId)
      this.completedCharts = next
    },

    /**
     * Wipe all live values but keep the dataset list. Each dataset's status
     * is reset to `pending`; this is what the user sees after a `reset`
     * SSE event from the backend (server-side `POST /benchmarks/:id/reset`
     * deletes datapoints + completions but keeps the config row).
     */
    applyReset() {
      this.latest = new Map()
      this.latestClientTs = new Map()
      const next = new Map<DatasetKey, DatasetState>()
      for (const [key, ds] of this.datasets) {
        next.set(key, {
          ...ds,
          status: 'pending',
          started_at: null,
          completed_at: null,
        })
      }
      this.datasets = next
      this.lastUpdate = null
    },

    /** Reset everything — used by BenchmarkPage on unmount before reconnect. */
    clear() {
      this.config = null
      this.latest = new Map()
      this.latestClientTs = new Map()
      this.datasets = new Map()
      this.lastUpdate = null
      this.updatedCharts = new Set()
      this.completedCharts = new Set()
      this.metadata = new Map()
    },
  },
})

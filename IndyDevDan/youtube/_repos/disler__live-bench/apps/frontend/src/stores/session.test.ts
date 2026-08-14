// Exercises the §14.4 newer-wins guard in the session store, plus the
// multi-chart cell-key isolation (a datapoint on chart=A must NOT influence
// chart=B even when the group/metric keys collide).

import { beforeEach, describe, it, expect } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useSessionStore } from './session'
import type {
  BenchmarkConfig,
  ChartDef,
  DataPointStored,
  DatasetState,
  SseSnapshot,
} from '../schemas'

const SESSION_ID = 'test-drive-bt-gradient'

function makeConfig(): BenchmarkConfig {
  return {
    session_id: SESSION_ID,
    title: 'Test Drive',
    subtitle: null,
    better: 'higher',
    direction: 'BT',
    x: { label: 'Backend' },
    y: { label: 'tok/s', unit: 'tok/s', min: 0 },
    metrics: [
      { key: 'prefill', label: 'Prefill', color: ['#e86b3a', '#f2a66b'] },
      { key: 'decode', label: 'Decode', color: ['#4a8fe0', '#6fa5e8'] },
    ],
    groups: [
      { key: 'alpha', label: 'Alpha' },
      { key: 'bravo', label: 'Bravo' },
    ],
  }
}

function makeMultiChartConfig(): BenchmarkConfig {
  const sharedAxis = { label: 'Backend' }
  const sharedY = { label: 'value', unit: null, min: 0, max: 1 }
  const chartA: ChartDef = {
    chart_id: 'a',
    title: 'A',
    subtitle: null,
    better: 'higher',
    direction: 'BT',
    x: sharedAxis,
    y: sharedY,
    metrics: [{ key: 'score', label: 'Score' }],
  }
  const chartB: ChartDef = {
    chart_id: 'b',
    title: 'B',
    subtitle: null,
    better: 'lower',
    direction: 'BT',
    x: sharedAxis,
    y: sharedY,
    metrics: [{ key: 'score', label: 'Score' }],
  }
  return {
    session_id: 'multi-session',
    title: 'Multi',
    subtitle: null,
    direction: 'BT',
    groups: [
      { key: 'alpha', label: 'Alpha' },
      { key: 'bravo', label: 'Bravo' },
    ],
    charts: [chartA, chartB],
  }
}

function makeDatasets(): DatasetState[] {
  return [
    {
      chart_id: 'default',
      group_key: 'alpha',
      status: 'pending',
      started_at: null,
      completed_at: null,
    },
    {
      chart_id: 'default',
      group_key: 'bravo',
      status: 'pending',
      started_at: null,
      completed_at: null,
    },
  ]
}

function makeMultiChartDatasets(): DatasetState[] {
  const states: DatasetState[] = []
  for (const chart of ['a', 'b']) {
    for (const group of ['alpha', 'bravo']) {
      states.push({
        chart_id: chart,
        group_key: group,
        status: 'pending',
        started_at: null,
        completed_at: null,
      })
    }
  }
  return states
}

function makePoint(overrides: Partial<DataPointStored>): DataPointStored {
  return {
    session_id: SESSION_ID,
    chart_id: 'default',
    group_key: 'alpha',
    metric_key: 'prefill',
    value: 100,
    client_ts: '2026-04-07T14:22:19.100000+00:00',
    server_ts: '2026-04-07T14:22:19.400000+00:00',
    seq: 1,
    ...overrides,
  }
}

function snapshotFrom(points: DataPointStored[]): SseSnapshot {
  return {
    event: 'snapshot',
    session_id: SESSION_ID,
    config: makeConfig(),
    points,
    datasets: makeDatasets(),
  }
}

function multiChartSnapshotFrom(points: DataPointStored[]): SseSnapshot {
  return {
    event: 'snapshot',
    session_id: 'multi-session',
    config: makeMultiChartConfig(),
    points,
    datasets: makeMultiChartDatasets(),
  }
}

describe('session store — newer-wins on client_ts (§14.4)', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('keeps the newer value when a stale (older client_ts) point arrives second', () => {
    const store = useSessionStore()
    store.applySnapshot(snapshotFrom([]))

    const newer = makePoint({
      value: 1308,
      client_ts: '2026-04-07T14:22:19.500000+00:00',
      server_ts: '2026-04-07T14:22:19.600000+00:00',
      seq: 10,
    })
    const older = makePoint({
      value: 42,
      client_ts: '2026-04-07T14:22:19.100000+00:00', // older
      server_ts: '2026-04-07T14:22:19.700000+00:00', // arrives later
      seq: 11,
    })

    store.applyDatapoint(newer)
    store.applyDatapoint(older)

    expect(store.latest.get('default:alpha:prefill')).toBe(1308)
    expect(store.latestClientTs.get('default:alpha:prefill')).toBe(
      '2026-04-07T14:22:19.500000+00:00',
    )
    // The stale point must NOT rewind lastUpdate either.
    expect(store.lastUpdate).toBe('2026-04-07T14:22:19.600000+00:00')
  })

  it('updates to the newer value when points arrive in time-order', () => {
    const store = useSessionStore()
    store.applySnapshot(snapshotFrom([]))

    const first = makePoint({
      value: 500,
      client_ts: '2026-04-07T14:22:19.100000+00:00',
      seq: 1,
    })
    const second = makePoint({
      value: 720,
      client_ts: '2026-04-07T14:22:19.200000+00:00',
      server_ts: '2026-04-07T14:22:19.300000+00:00',
      seq: 2,
    })

    store.applyDatapoint(first)
    store.applyDatapoint(second)

    expect(store.latest.get('default:alpha:prefill')).toBe(720)
    expect(store.latestClientTs.get('default:alpha:prefill')).toBe(
      '2026-04-07T14:22:19.200000+00:00',
    )
  })

  it('flips a pending dataset to running when the first real datapoint arrives', () => {
    const store = useSessionStore()
    store.applySnapshot(snapshotFrom([]))

    expect(store.datasets.get('default:alpha')?.status).toBe('pending')

    store.applyDatapoint(makePoint({ value: 100 }))
    expect(store.datasets.get('default:alpha')?.status).toBe('running')
  })

  it('clears latest maps and resets dataset statuses on applyReset', () => {
    const store = useSessionStore()
    store.applySnapshot(snapshotFrom([]))

    store.applyDatapoint(
      makePoint({
        value: 1308,
        client_ts: '2026-04-07T14:22:19.500000+00:00',
      }),
    )
    store.applyDatapoint(
      makePoint({
        group_key: 'bravo',
        value: 42,
        client_ts: '2026-04-07T14:22:19.600000+00:00',
      }),
    )
    store.applyDatasetComplete(
      'default',
      'alpha',
      '2026-04-07T14:22:20.000000+00:00',
    )

    expect(store.latest.size).toBe(2)
    expect(store.datasets.get('default:alpha')?.status).toBe('complete')

    store.applyReset()

    expect(store.latest.size).toBe(0)
    expect(store.latestClientTs.size).toBe(0)
    expect(store.lastUpdate).toBeNull()
    // Dataset statuses should be reset to pending but the keys should survive.
    expect(store.datasets.get('default:alpha')?.status).toBe('pending')
    expect(store.datasets.get('default:alpha')?.started_at).toBeNull()
    expect(store.datasets.get('default:alpha')?.completed_at).toBeNull()
    expect(store.datasets.get('default:bravo')?.status).toBe('pending')
  })

  it('rebuilds latest maps from a fresh snapshot in client_ts order', () => {
    const store = useSessionStore()

    const snapshot = snapshotFrom([
      makePoint({
        value: 100,
        client_ts: '2026-04-07T14:22:19.100000+00:00',
        server_ts: '2026-04-07T14:22:19.200000+00:00',
      }),
      makePoint({
        group_key: 'bravo',
        value: 200,
        client_ts: '2026-04-07T14:22:19.300000+00:00',
        server_ts: '2026-04-07T14:22:19.400000+00:00',
      }),
    ])

    store.applySnapshot(snapshot)

    expect(store.latest.get('default:alpha:prefill')).toBe(100)
    expect(store.latest.get('default:bravo:prefill')).toBe(200)
    expect(store.lastUpdate).toBe('2026-04-07T14:22:19.400000+00:00')
  })
})

describe('session store — multi-chart cell isolation', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('applyDatapoint isolates charts (same group/metric, different chart_id)', () => {
    const store = useSessionStore()
    store.applySnapshot(multiChartSnapshotFrom([]))

    // Apply the same (group=alpha, metric=score) point to TWO different
    // charts. The store must keep them in separate cells.
    store.applyDatapoint({
      session_id: 'multi-session',
      chart_id: 'a',
      group_key: 'alpha',
      metric_key: 'score',
      value: 0.42,
      client_ts: '2026-04-07T14:22:19.100000+00:00',
      server_ts: '2026-04-07T14:22:19.200000+00:00',
      seq: 1,
    })
    store.applyDatapoint({
      session_id: 'multi-session',
      chart_id: 'b',
      group_key: 'alpha',
      metric_key: 'score',
      value: 0.99,
      client_ts: '2026-04-07T14:22:19.300000+00:00',
      server_ts: '2026-04-07T14:22:19.400000+00:00',
      seq: 2,
    })

    expect(store.latest.size).toBe(2)
    expect(store.latest.get('a:alpha:score')).toBe(0.42)
    expect(store.latest.get('b:alpha:score')).toBe(0.99)

    // Updating chart=a must NOT touch chart=b's cell.
    store.applyDatapoint({
      session_id: 'multi-session',
      chart_id: 'a',
      group_key: 'alpha',
      metric_key: 'score',
      value: 0.55,
      client_ts: '2026-04-07T14:22:19.500000+00:00',
      server_ts: '2026-04-07T14:22:19.600000+00:00',
      seq: 3,
    })
    expect(store.latest.get('a:alpha:score')).toBe(0.55)
    expect(store.latest.get('b:alpha:score')).toBe(0.99)

    // Dataset pills are also chart-keyed — promoting chart=a from pending
    // to running must not touch chart=b's pill.
    expect(store.datasets.get('a:alpha')?.status).toBe('running')
    expect(store.datasets.get('b:alpha')?.status).toBe('running')
    expect(store.datasets.get('a:bravo')?.status).toBe('pending')
    expect(store.datasets.get('b:bravo')?.status).toBe('pending')
  })

  it('applyDatapoint newer-wins is chart-scoped (stale point on chart=a does not affect chart=b)', () => {
    const store = useSessionStore()
    store.applySnapshot(multiChartSnapshotFrom([]))

    // Land chart=a with a future timestamp.
    store.applyDatapoint({
      session_id: 'multi-session',
      chart_id: 'a',
      group_key: 'alpha',
      metric_key: 'score',
      value: 0.9,
      client_ts: '2030-01-01T00:00:00.000000+00:00',
      server_ts: '2030-01-01T00:00:00.100000+00:00',
      seq: 1,
    })
    // Land chart=b with an earlier timestamp — it must still land because
    // the newer-wins guard is per-cell, and cells are chart-scoped.
    store.applyDatapoint({
      session_id: 'multi-session',
      chart_id: 'b',
      group_key: 'alpha',
      metric_key: 'score',
      value: 0.1,
      client_ts: '2020-01-01T00:00:00.000000+00:00',
      server_ts: '2030-01-01T00:00:00.200000+00:00',
      seq: 2,
    })

    expect(store.latest.get('a:alpha:score')).toBe(0.9)
    expect(store.latest.get('b:alpha:score')).toBe(0.1)

    // Now apply a stale point on chart=a — older than the chart=a entry.
    // It must be DROPPED, and critically must not touch chart=b's entry.
    store.applyDatapoint({
      session_id: 'multi-session',
      chart_id: 'a',
      group_key: 'alpha',
      metric_key: 'score',
      value: 0.3,
      client_ts: '2020-01-01T00:00:00.000000+00:00',
      server_ts: '2030-01-01T00:00:00.300000+00:00',
      seq: 3,
    })

    expect(store.latest.get('a:alpha:score')).toBe(0.9) // unchanged
    expect(store.latest.get('b:alpha:score')).toBe(0.1) // unchanged
  })

  it('applySnapshot rebuilds chart-keyed maps from multi-chart points', () => {
    const store = useSessionStore()

    // Feed a snapshot with 2 charts × 2 groups × 1 metric = 4 datapoints.
    const points: DataPointStored[] = []
    let ms = 100000
    for (const chart_id of ['a', 'b']) {
      for (const group_key of ['alpha', 'bravo']) {
        points.push({
          session_id: 'multi-session',
          chart_id,
          group_key,
          metric_key: 'score',
          value: ms / 1_000_000,
          client_ts: `2026-04-07T14:22:19.${ms.toString().padStart(6, '0')}+00:00`,
          server_ts: `2026-04-07T14:22:19.${(ms + 50).toString().padStart(6, '0')}+00:00`,
          seq: ms,
        })
        ms += 100
      }
    }

    store.applySnapshot(multiChartSnapshotFrom(points))

    expect(store.latest.size).toBe(4)
    expect(store.latest.get('a:alpha:score')).toBeCloseTo(0.1)
    expect(store.latest.get('a:bravo:score')).toBeCloseTo(0.1001)
    expect(store.latest.get('b:alpha:score')).toBeCloseTo(0.1002)
    expect(store.latest.get('b:bravo:score')).toBeCloseTo(0.1003)
  })

  it('applyReset preserves chart-keyed dataset entries', () => {
    const store = useSessionStore()
    store.applySnapshot(multiChartSnapshotFrom([]))

    // Push a datapoint into every chart × group cell to flip all 4 pills
    // to running.
    let ms = 100000
    for (const chart_id of ['a', 'b']) {
      for (const group_key of ['alpha', 'bravo']) {
        store.applyDatapoint({
          session_id: 'multi-session',
          chart_id,
          group_key,
          metric_key: 'score',
          value: 0.5,
          client_ts: `2026-04-07T14:22:19.${ms.toString().padStart(6, '0')}+00:00`,
          server_ts: `2026-04-07T14:22:19.${(ms + 50).toString().padStart(6, '0')}+00:00`,
          seq: ms,
        })
        ms += 100
      }
    }

    expect(store.datasets.size).toBe(4)
    for (const key of ['a:alpha', 'a:bravo', 'b:alpha', 'b:bravo']) {
      expect(store.datasets.get(key)?.status).toBe('running')
    }

    store.applyReset()

    // All 4 chart-keyed dataset entries must survive the reset — only their
    // status flips back to pending.
    expect(store.latest.size).toBe(0)
    expect(store.latestClientTs.size).toBe(0)
    expect(store.datasets.size).toBe(4)
    for (const key of ['a:alpha', 'a:bravo', 'b:alpha', 'b:bravo']) {
      expect(store.datasets.get(key)?.status).toBe('pending')
      expect(store.datasets.get(key)?.started_at).toBeNull()
      expect(store.datasets.get(key)?.completed_at).toBeNull()
    }
  })

  it('applyDatasetComplete is chart-scoped', () => {
    const store = useSessionStore()
    store.applySnapshot(multiChartSnapshotFrom([]))

    store.applyDatasetComplete('a', 'alpha', '2026-04-07T14:22:20.000000+00:00')

    expect(store.datasets.get('a:alpha')?.status).toBe('complete')
    // Other chart's alpha pill is untouched.
    expect(store.datasets.get('b:alpha')?.status).toBe('pending')
    // Other group in same chart is untouched.
    expect(store.datasets.get('a:bravo')?.status).toBe('pending')
  })
})

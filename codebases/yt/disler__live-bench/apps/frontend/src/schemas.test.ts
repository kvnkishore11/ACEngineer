// Zod drift test — every wire shape defined in
// apps/backend/src/live_bench_server/models.py must parse successfully
// through its Zod mirror. The fixtures under apps/backend/tests/fixtures/
// are the canonical reference (written by tests/fixtures_export.py) — we
// load them directly so any drift in the Pydantic layer immediately
// manifests here as a parse failure.

import { describe, it, expect } from 'vitest'
import { readFileSync } from 'node:fs'
import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import {
  BenchmarkConfigSchema,
  BenchmarkSummarySchema,
  BenchmarksListResponseSchema,
  BenchmarkDetailResponseSchema,
  ChartDefSchema,
  CompletionRefSchema,
  DataPointStoredSchema,
  DatasetStateSchema,
  IngestResponseSchema,
  SseSnapshotSchema,
  SseDatapointSchema,
  SseDatasetCompleteSchema,
  SseResetSchema,
  SseConfigChangedSchema,
  parseSseEvent,
  allCharts,
  type BenchmarkConfig,
} from './schemas'

// Resolve fixture path relative to this test file so the drift check is
// immune to the cwd vitest is invoked from.
const HERE = dirname(fileURLToPath(import.meta.url))
const FIXTURE_ROOT = resolve(HERE, '../../backend/tests/fixtures')

function loadFixture<T = unknown>(name: string): T {
  const raw = readFileSync(resolve(FIXTURE_ROOT, name), 'utf-8')
  return JSON.parse(raw) as T
}

// ── Fixtures from the backend's tests/fixtures/ directory ──
const chartDefFixture = loadFixture('ChartDef.json')
const configFixture = loadFixture('BenchmarkConfig.json')
const pointFixture = loadFixture('DataPointStored.json')
const datasetFixture = loadFixture('DatasetState.json')
const completionRefFixture = loadFixture('CompletionRef.json')
const snapshotFixture = loadFixture('SseSnapshot.json')
const sseDatapointFixture = loadFixture('SseDatapoint.json')
const sseDatasetCompleteFixture = loadFixture('SseDatasetComplete.json')
const ingestResponseFixture = loadFixture('IngestResponse.json')

// A hand-built single-chart legacy config — the backend's fixture is the
// new multi-chart trio shape, so we keep an inline one here to cover the
// legacy synthesis path via `allCharts()`.
const legacyConfigFixture = {
  session_id: 'test-drive-bt-gradient',
  title: 'Test Drive — Gradient Bars (BT)',
  subtitle: '3 groups · 2 metrics · gradient colors',
  better: 'higher' as const,
  direction: 'BT' as const,
  x: { label: 'Backend', unit: null, min: null, max: null },
  y: { label: 'tokens / second', unit: 'tok/s', min: 0, max: null },
  metrics: [
    { key: 'prefill', label: 'Prefill', color: ['#e86b3a', '#f2a66b'] },
    { key: 'decode', label: 'Decode', color: ['#4a8fe0', '#6fa5e8'] },
  ],
  groups: [
    { key: 'alpha', label: 'Alpha' },
    { key: 'bravo', label: 'Bravo' },
    { key: 'charlie', label: 'Charlie' },
  ],
}

describe('ChartDefSchema', () => {
  it('parses the ChartDef fixture', () => {
    const result = ChartDefSchema.parse(chartDefFixture)
    expect(result.chart_id).toBe('recall')
    expect(result.better).toBe('higher')
    expect(result.direction).toBe('BT')
    expect(result.metrics).toHaveLength(1)
    expect(result.x.label).toBe('Backend')
    expect(result.y.max).toBe(1)
  })
})

describe('BenchmarkConfigSchema (multi-chart form)', () => {
  it('parses the multi-chart BenchmarkConfig fixture', () => {
    const result = BenchmarkConfigSchema.parse(configFixture)
    expect(result.session_id).toBe('trio')
    expect(result.charts).toBeDefined()
    expect(result.charts).toHaveLength(2)
    expect(result.charts?.[0].chart_id).toBe('recall')
    expect(result.charts?.[1].chart_id).toBe('latency')
    expect(result.charts?.[1].direction).toBe('LR')
    // Legacy top-level fields are null for the multi-chart form.
    expect(result.better).toBeNull()
    expect(result.metrics).toBeNull()
    // Groups live on each chart, not at config level.
    expect(result.groups).toBeFalsy()
    expect(result.charts?.[0].groups).toHaveLength(3)
  })

  it('allCharts() returns the explicit chart list when present', () => {
    const config = BenchmarkConfigSchema.parse(configFixture)
    const charts = allCharts(config)
    expect(charts).toHaveLength(2)
    expect(charts[0].chart_id).toBe('recall')
    expect(charts[1].chart_id).toBe('latency')
  })
})

describe('BenchmarkConfigSchema (legacy single-chart form)', () => {
  it('parses a legacy top-level-fields config', () => {
    const result = BenchmarkConfigSchema.parse(legacyConfigFixture)
    expect(result.session_id).toBe('test-drive-bt-gradient')
    expect(result.metrics).toHaveLength(2)
    expect(result.groups).toHaveLength(3)
    expect(result.better).toBe('higher')
    expect(result.direction).toBe('BT')
    expect(result.charts).toBeFalsy()
  })

  it('accepts a single-string metric color', () => {
    const result = BenchmarkConfigSchema.parse({
      ...legacyConfigFixture,
      metrics: [{ key: 'single', label: 'Single', color: '#abcdef' }],
    })
    expect(result.metrics?.[0].color).toBe('#abcdef')
  })

  it('accepts a missing metric color', () => {
    const result = BenchmarkConfigSchema.parse({
      ...legacyConfigFixture,
      metrics: [{ key: 'no_color', label: 'No Color' }],
    })
    expect(result.metrics?.[0].color).toBeUndefined()
  })

  it('allCharts() synthesises a single default ChartDef from legacy fields', () => {
    const config = BenchmarkConfigSchema.parse(legacyConfigFixture) as BenchmarkConfig
    const charts = allCharts(config)
    expect(charts).toHaveLength(1)
    expect(charts[0].chart_id).toBe('default')
    expect(charts[0].title).toBeNull()
    expect(charts[0].better).toBe('higher')
    expect(charts[0].direction).toBe('BT')
    expect(charts[0].metrics).toHaveLength(2)
  })
})

describe('DataPointStoredSchema', () => {
  it('parses the fixture (with chart_id)', () => {
    const result = DataPointStoredSchema.parse(pointFixture)
    expect(result.chart_id).toBe('recall')
    expect(result.group_key).toBe('faiss')
    expect(result.value).toBe(0.94)
  })

  it('defaults chart_id to "default" when missing (backward compat)', () => {
    const raw = { ...(pointFixture as Record<string, unknown>) }
    delete raw.chart_id
    const result = DataPointStoredSchema.parse(raw)
    expect(result.chart_id).toBe('default')
  })
})

describe('DatasetStateSchema', () => {
  it('parses the fixture (with chart_id)', () => {
    const result = DatasetStateSchema.parse(datasetFixture)
    expect(result.chart_id).toBe('recall')
    expect(result.group_key).toBe('faiss')
    expect(result.status).toBe('running')
  })

  it('parses a complete dataset', () => {
    const result = DatasetStateSchema.parse({
      chart_id: 'default',
      group_key: 'alpha',
      status: 'complete',
      started_at: '2026-04-07T14:22:18.923000+00:00',
      completed_at: '2026-04-07T14:22:24.110000+00:00',
    })
    expect(result.status).toBe('complete')
  })

  it('parses a pending dataset', () => {
    const result = DatasetStateSchema.parse({
      chart_id: 'default',
      group_key: 'alpha',
      status: 'pending',
      started_at: null,
      completed_at: null,
    })
    expect(result.status).toBe('pending')
  })

  it('defaults chart_id to "default" when missing (backward compat)', () => {
    const result = DatasetStateSchema.parse({
      group_key: 'alpha',
      status: 'pending',
      started_at: null,
      completed_at: null,
    })
    expect(result.chart_id).toBe('default')
  })
})

describe('CompletionRefSchema', () => {
  it('parses the fixture', () => {
    const result = CompletionRefSchema.parse(completionRefFixture)
    expect(result.chart_id).toBe('recall')
    expect(result.group_key).toBe('faiss')
  })

  it('defaults chart_id to "default" when missing', () => {
    const result = CompletionRefSchema.parse({ group_key: 'alpha' })
    expect(result.chart_id).toBe('default')
  })
})

describe('IngestResponseSchema', () => {
  it('parses the fixture', () => {
    const result = IngestResponseSchema.parse(ingestResponseFixture)
    expect(typeof result.accepted).toBe('number')
  })

  it('parses a hand-built response', () => {
    const result = IngestResponseSchema.parse({
      accepted: 2,
      seq_from: 1,
      seq_to: 2,
      completed: ['alpha'],
      server_ts: '2026-04-07T14:22:19.402118+00:00',
    })
    expect(result.accepted).toBe(2)
    expect(result.completed).toEqual(['alpha'])
  })
})

describe('BenchmarkSummarySchema', () => {
  it('parses a single-chart summary with chart_count=1', () => {
    const result = BenchmarkSummarySchema.parse({
      session_id: legacyConfigFixture.session_id,
      title: legacyConfigFixture.title,
      subtitle: legacyConfigFixture.subtitle,
      better: 'higher',
      completed_count: 1,
      total_count: 3,
      last_update: null,
      chart_count: 1,
    })
    expect(result.completed_count).toBe(1)
    expect(result.better).toBe('higher')
    expect(result.chart_count).toBe(1)
  })

  it('parses a multi-chart summary with null better and chart_count>1', () => {
    const result = BenchmarkSummarySchema.parse({
      session_id: 'trio',
      title: 'Trio',
      subtitle: null,
      better: null,
      completed_count: 0,
      total_count: 9,
      last_update: null,
      chart_count: 3,
    })
    expect(result.better).toBeNull()
    expect(result.chart_count).toBe(3)
  })
})

describe('BenchmarksListResponseSchema', () => {
  it('parses a list of benchmarks with mixed chart counts', () => {
    const result = BenchmarksListResponseSchema.parse({
      benchmarks: [
        {
          session_id: 'legacy',
          title: 'Legacy',
          subtitle: null,
          better: 'higher',
          completed_count: 0,
          total_count: 3,
          last_update: null,
          chart_count: 1,
        },
        {
          session_id: 'trio',
          title: 'Trio',
          subtitle: null,
          better: null,
          completed_count: 0,
          total_count: 9,
          last_update: null,
          chart_count: 3,
        },
      ],
    })
    expect(result.benchmarks).toHaveLength(2)
  })
})

describe('BenchmarkDetailResponseSchema', () => {
  it('parses a detail response built from the fixture', () => {
    const result = BenchmarkDetailResponseSchema.parse({
      config: configFixture,
      points: [pointFixture],
      datasets: [datasetFixture],
    })
    expect(result.points).toHaveLength(1)
    expect(result.datasets).toHaveLength(1)
    expect(result.config.charts).toHaveLength(2)
  })
})

describe('SSE events', () => {
  it('parses the snapshot fixture', () => {
    const result = SseSnapshotSchema.parse(snapshotFixture)
    expect(result.event).toBe('snapshot')
    expect(result.config.charts).toHaveLength(2)
    expect(result.points[0].chart_id).toBe('recall')
    expect(result.datasets[0].chart_id).toBe('recall')
  })

  it('parses the datapoint fixture', () => {
    const result = SseDatapointSchema.parse(sseDatapointFixture)
    expect(result.event).toBe('datapoint')
    expect(result.point.chart_id).toBe('recall')
  })

  it('parses the dataset_complete fixture (with chart_id)', () => {
    const result = SseDatasetCompleteSchema.parse(sseDatasetCompleteFixture)
    expect(result.chart_id).toBe('recall')
    expect(result.group_key).toBe('faiss')
  })

  it('defaults dataset_complete chart_id to "default" when missing (legacy)', () => {
    const raw = { ...(sseDatasetCompleteFixture as Record<string, unknown>) }
    delete raw.chart_id
    const result = SseDatasetCompleteSchema.parse(raw)
    expect(result.chart_id).toBe('default')
  })

  it('parses a reset event', () => {
    const result = SseResetSchema.parse({
      event: 'reset',
      session_id: 'trio',
    })
    expect(result.session_id).toBe('trio')
  })

  it('parses a config_changed event', () => {
    const result = SseConfigChangedSchema.parse({
      event: 'config_changed',
      session_id: 'trio',
      config: configFixture,
    })
    expect(result.config.session_id).toBe('trio')
  })
})

describe('parseSseEvent discriminated union', () => {
  it('narrows on the event literal', () => {
    const parsed = parseSseEvent(sseDatapointFixture)
    if (parsed.event === 'datapoint') {
      expect(parsed.point.chart_id).toBe('recall')
    } else {
      throw new Error('expected datapoint event')
    }
  })

  it('rejects an unknown event type', () => {
    expect(() => parseSseEvent({ event: 'bogus' })).toThrow()
  })
})

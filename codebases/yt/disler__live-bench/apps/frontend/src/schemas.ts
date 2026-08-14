// Zod mirrors of the Pydantic models defined in
// apps/backend/src/live_bench_server/models.py.
//
// Field names use snake_case to match the wire shape exactly. Datetimes are
// kept as plain ISO-8601 strings (NOT z.date()) so the §14.4 newer-wins guard
// can compare them with `<` / `>` directly without parsing.

import { z } from 'zod'

// ── Type aliases ───────────────────────────────────────────
export const DirectionSchema = z.enum(['LR', 'BT'])
export const BetterSchema = z.enum(['higher', 'lower'])
export const DatasetStatusSchema = z.enum(['pending', 'running', 'complete'])

// A single hex string OR an array of hex stops (rendered as a gradient).
export const ColorSchema = z.union([z.string(), z.array(z.string())])

// ── Benchmark configuration ────────────────────────────────
export const AxisConfigSchema = z.object({
  label: z.string(),
  unit: z.string().nullish(),
  min: z.number().nullish(),
  max: z.number().nullish(),
})

export const MetricDefSchema = z.object({
  key: z.string(),
  label: z.string(),
  color: ColorSchema.nullish(),
  icon: z.string().nullish(),
})

export const TagDefSchema = z.object({
  name: z.string(),
  icons: z.array(z.string()).default([]),
})

export const GroupDefSchema = z.object({
  key: z.string(),
  label: z.string(),
  icon: z.string().nullish(),
})

// One chart panel inside a multi-chart benchmark. Mirrors the Pydantic
// ChartDef in apps/backend/src/live_bench_server/models.py. A benchmark may
// contain N charts; each chart owns its own title, axes, `better` direction,
// drawing direction, and metrics — but they all share the parent benchmark's
// `groups` (which is what makes the multi-chart grouping meaningful:
// comparing the SAME backends across DIFFERENT metric panels).
export const ChartDefSchema = z.object({
  chart_id: z.string(),
  title: z.string().nullish(),
  subtitle: z.string().nullish(),
  better: BetterSchema,
  direction: DirectionSchema.default('BT'),
  x: AxisConfigSchema,
  y: AxisConfigSchema,
  metrics: z.array(MetricDefSchema),
  groups: z.array(GroupDefSchema).nullish(),
})

// BenchmarkConfig accepts BOTH shapes — the Pydantic model_validator on the
// backend enforces the one-of constraint, so the Zod schema just needs to
// accept either. The legacy top-level fields (`metrics`, `x`, `y`, `better`)
// are nullable/optional; the new multi-chart form uses `charts`.
export const BenchmarkConfigSchema = z.object({
  session_id: z.string(),
  title: z.string(),
  subtitle: z.string().nullish(),
  tags: z.array(TagDefSchema).nullish(),
  groups: z.array(GroupDefSchema).nullish(),
  // Multi-chart form (new). When present, the rest of the system iterates
  // over this list and ignores the legacy top-level fields.
  charts: z.array(ChartDefSchema).nullish(),
  // Legacy single-chart form (top-level fields, all optional). A single
  // default ChartDef is synthesised from these by `allCharts()` below.
  better: BetterSchema.nullish(),
  direction: DirectionSchema.default('BT'),
  x: AxisConfigSchema.nullish(),
  y: AxisConfigSchema.nullish(),
  metrics: z.array(MetricDefSchema).nullish(),
})

// ── Datapoints ─────────────────────────────────────────────
export const DataPointSchema = z.object({
  chart_id: z.string().default('default'),
  group_key: z.string(),
  metric_key: z.string(),
  value: z.number(),
  client_ts: z.string(),
})

export const DataPointStoredSchema = z.object({
  session_id: z.string(),
  chart_id: z.string().default('default'),
  group_key: z.string(),
  metric_key: z.string(),
  value: z.number(),
  client_ts: z.string(),
  server_ts: z.string(),
  seq: z.number().int(),
})

// ── Dataset state ──────────────────────────────────────────
export const DatasetStateSchema = z.object({
  chart_id: z.string().default('default'),
  group_key: z.string(),
  status: DatasetStatusSchema,
  started_at: z.string().nullish(),
  completed_at: z.string().nullish(),
})

// ── Ingest wire ────────────────────────────────────────────
export const CompletionRefSchema = z.object({
  chart_id: z.string().default('default'),
  group_key: z.string(),
})

export const IngestRequestSchema = z.object({
  session_id: z.string(),
  request_ts: z.string(),
  points: z.array(DataPointSchema).default([]),
  complete_groups: z.array(CompletionRefSchema).default([]),
})

export const IngestResponseSchema = z.object({
  accepted: z.number().int(),
  seq_from: z.number().int().nullish(),
  seq_to: z.number().int().nullish(),
  completed: z.array(z.string()).default([]),
  server_ts: z.string(),
})

// ── REST list / show response shapes ───────────────────────
// Mirrors what apps/backend/src/live_bench_server/rest.py returns for
// GET /benchmarks. The landing page shows a lean summary — not the full
// BenchmarkConfig — so the server can cheaply serve the dropdown without
// deserialising every config_json blob.
//
// Multi-chart benchmarks have `better: null` (no single "better" direction
// across a stack of charts) and `chart_count > 1`. Single-chart / legacy
// benchmarks carry `better` populated and `chart_count === 1`.
export const BenchmarkSummarySchema = z.object({
  session_id: z.string(),
  title: z.string(),
  subtitle: z.string().nullish(),
  better: BetterSchema.nullish(),
  completed_count: z.number().int(),
  total_count: z.number().int(),
  last_update: z.string().nullish(),
  chart_count: z.number().int().nullish(),
})

export const BenchmarksListResponseSchema = z.object({
  benchmarks: z.array(BenchmarkSummarySchema),
})

export const BenchmarkDetailResponseSchema = z.object({
  config: BenchmarkConfigSchema,
  points: z.array(DataPointStoredSchema),
  datasets: z.array(DatasetStateSchema),
  metadata: z.record(z.string(), z.record(z.string(), z.any())).optional(),
})

export const ResetResponseSchema = z.object({
  reset: z.boolean(),
  session_id: z.string(),
})

// ── SSE event payloads ─────────────────────────────────────
export const SseSnapshotSchema = z.object({
  event: z.literal('snapshot'),
  session_id: z.string(),
  config: BenchmarkConfigSchema,
  points: z.array(DataPointStoredSchema),
  datasets: z.array(DatasetStateSchema),
})

export const SseDatapointSchema = z.object({
  event: z.literal('datapoint'),
  session_id: z.string(),
  point: DataPointStoredSchema,
})

export const SseDatasetCompleteSchema = z.object({
  event: z.literal('dataset_complete'),
  session_id: z.string(),
  chart_id: z.string().default('default'),
  group_key: z.string(),
  completed_at: z.string(),
})

export const SseResetSchema = z.object({
  event: z.literal('reset'),
  session_id: z.string(),
})

export const SseConfigChangedSchema = z.object({
  event: z.literal('config_changed'),
  session_id: z.string(),
  config: BenchmarkConfigSchema,
})

export const SseMetadataSchema = z.object({
  event: z.literal('metadata'),
  session_id: z.string(),
  chart_id: z.string(),
  group_key: z.string(),
  data: z.record(z.string(), z.any()),
})

export const SseEventSchema = z.discriminatedUnion('event', [
  SseSnapshotSchema,
  SseDatapointSchema,
  SseDatasetCompleteSchema,
  SseResetSchema,
  SseConfigChangedSchema,
  SseMetadataSchema,
])

/**
 * Validate an arbitrary JSON value against the SSE event discriminated union.
 *
 * The session store consumes the result via the `event` literal so callers can
 * narrow safely without re-parsing.
 */
export function parseSseEvent(raw: unknown): SseEvent {
  return SseEventSchema.parse(raw)
}

// ── Inferred TypeScript types ──────────────────────────────
export type Direction = z.infer<typeof DirectionSchema>
export type Better = z.infer<typeof BetterSchema>
export type DatasetStatus = z.infer<typeof DatasetStatusSchema>
export type Color = z.infer<typeof ColorSchema>

export type AxisConfig = z.infer<typeof AxisConfigSchema>
export type MetricDef = z.infer<typeof MetricDefSchema>
export type TagDef = z.infer<typeof TagDefSchema>
export type GroupDef = z.infer<typeof GroupDefSchema>
export type ChartDef = z.infer<typeof ChartDefSchema>
export type BenchmarkConfig = z.infer<typeof BenchmarkConfigSchema>

export type DataPoint = z.infer<typeof DataPointSchema>
export type DataPointStored = z.infer<typeof DataPointStoredSchema>
export type DatasetState = z.infer<typeof DatasetStateSchema>

export type CompletionRef = z.infer<typeof CompletionRefSchema>
export type IngestRequest = z.infer<typeof IngestRequestSchema>
export type IngestResponse = z.infer<typeof IngestResponseSchema>

export type BenchmarkSummary = z.infer<typeof BenchmarkSummarySchema>
export type BenchmarksListResponse = z.infer<typeof BenchmarksListResponseSchema>
export type BenchmarkDetailResponse = z.infer<typeof BenchmarkDetailResponseSchema>
export type ResetResponse = z.infer<typeof ResetResponseSchema>

export type SseSnapshot = z.infer<typeof SseSnapshotSchema>
export type SseDatapoint = z.infer<typeof SseDatapointSchema>
export type SseDatasetComplete = z.infer<typeof SseDatasetCompleteSchema>
export type SseReset = z.infer<typeof SseResetSchema>
export type SseConfigChanged = z.infer<typeof SseConfigChangedSchema>
export type SseMetadata = z.infer<typeof SseMetadataSchema>
export type SseEvent = z.infer<typeof SseEventSchema>

/**
 * Mirrors Pydantic `BenchmarkConfig.all_charts()` — returns the explicit
 * `charts` list when present, otherwise synthesises a single default
 * ChartDef from the legacy top-level fields. Lets the rest of the frontend
 * iterate uniformly regardless of which YAML shape backed the benchmark.
 *
 * The backend's model_validator guarantees exactly one form is present, so
 * a single synthesised chart is always recoverable for legacy configs.
 */
export function allCharts(config: BenchmarkConfig): ChartDef[] {
  if (config.charts && config.charts.length > 0) {
    return config.charts
  }
  if (!config.better || !config.x || !config.y || !config.metrics) {
    throw new Error(
      `BenchmarkConfig ${config.session_id} has neither charts nor legacy fields`,
    )
  }
  return [
    {
      chart_id: 'default',
      title: null,
      subtitle: null,
      better: config.better,
      direction: config.direction ?? 'BT',
      x: config.x,
      y: config.y,
      metrics: config.metrics,
      groups: config.groups,
    },
  ]
}

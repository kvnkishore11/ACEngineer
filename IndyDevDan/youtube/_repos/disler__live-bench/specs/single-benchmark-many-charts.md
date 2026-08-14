# Plan: Single Benchmark, Many Charts

## Task Description

Extend live-bench so a single benchmark can contain **N charts in one view**. Today, one YAML benchmark file produces one card on one page (`/benchmark/:sessionId`). The user wants one YAML benchmark to produce **one landing-table row** that, when clicked, opens a single page rendering **multiple charts stacked together** — each chart with its own title, `better` direction, axes, and metrics, but with the **groups shared** across all charts in the benchmark.

The current `BenchmarkFile` already supports `benchmarks: list[BenchmarkConfig]` (multi-benchmark-per-file), but that produces multiple separate landing rows — the wrong shape for this request. We need a sub-chart concept *inside* a single `BenchmarkConfig`.

After the schema lands, recreate `benchmarks/test-trio.yaml` as **one** benchmark `trio` with three charts (`recall`, `qps`, `latency`), drop the three-separate-benchmark trio, and prove the new shape end-to-end with `/drive` + `playwright-bowser-agent`.

## Objective

A benchmark page (`/benchmark/trio`) renders three live-updating chart cards stacked in the grid. Each card has its own title (`Recall@10` / `Query Throughput` / `p99 Query Latency`), its own `better` direction, its own axes, and its own dataset status pills — but they all share the FAISS / Qdrant / LanceDB groups defined once at the benchmark level. Emitting into any of the three charts via `live-bench emit trio --chart <chart_id> --group <g> --metric <m> --value <v>` smoothly animates exactly that bar without touching the others. The landing table shows **one** `trio` row, not three.

All eight existing single-chart YAMLs continue to work without modification — backward compat is non-negotiable.

## Problem Statement

The current `BenchmarkConfig` defines exactly one chart's worth of state at the top level: one `direction`, one `better`, one `x` axis, one `y` axis, one `metrics` list, one `groups` list. This is fine for "Gemma 4 E4B Audio — Prefill" where the whole benchmark is one chart, but it cannot represent the original reference mockup ("Gemma 4 E4B Audio: GGUF vs MLX" with three distinct chart panels — Prefill, Decode, Wall — each with its own units and `better` direction).

The user discovered this in iteration when a "trio" of related charts was built as three separate benchmarks (three landing rows, three pages) instead of one benchmark with three sub-panels. The fix is a real schema change: introduce a `ChartDef` type and let `BenchmarkConfig` carry a `charts: list[ChartDef]`.

## Solution Approach

A surgical, additive schema extension that preserves backward compatibility:

1. **`ChartDef` type** — a sub-chart inside a benchmark. Owns its own `chart_id`, `title`, `subtitle`, `better`, `direction`, `x`, `y`, `metrics`. Does NOT own `groups` (shared at the benchmark level — that's the whole point of grouping multiple charts under one benchmark).
2. **`BenchmarkConfig` gets `charts: list[ChartDef] | None = None`** — when present, it's a multi-chart benchmark. The legacy top-level `metrics`/`x`/`y`/`better`/`direction` fields become OPTIONAL but still supported. A `model_validator` enforces "exactly one form is present". A new `BenchmarkConfig.all_charts()` method synthesises a single `ChartDef(chart_id="default", ...)` from the legacy top-level fields, so the rest of the system can iterate uniformly over charts whether the YAML used the old or new shape.
3. **`DataPoint` and friends gain `chart_id: str = "default"`** — defaulted for backward compat. Existing CLI calls and existing SSE consumers keep working unchanged when targeting single-chart benchmarks.
4. **SQLite gets `chart_id` columns on `datapoints` and `completions`** — additive, with `DEFAULT 'default'` so the migration is safe to run against an existing dev database. The `(session, group, metric, client_ts DESC)` index becomes `(session, chart, group, metric, client_ts DESC)`.
5. **CLI emit/complete/stream get `--chart` flags** — defaults to `"default"`. JSONL stream lines accept an optional `chart` field, otherwise `"default"`.
6. **Frontend `BenchmarkPage` loops over `config.all_charts`** rendering one `<BenchmarkCard>` per chart inside the existing `<BenchmarkGrid>`. The session store re-keys its `latest` / `latestClientTs` / `datasets` maps to include `chart_id`. Newer-wins (§14.4) still uses `client_ts` strings — only the cell key changes.
7. **Recreate `benchmarks/test-trio.yaml`** as a single benchmark `trio` with three `ChartDef`s (`recall`, `qps`, `latency`). Wipe leftover `trio-recall` / `trio-qps` / `trio-latency` rows from SQLite. Emit data into all three charts and verify in a real browser.

The validator already proved the SQLite + SSE + animation pipeline works end-to-end — all we're doing is widening the cell key from `(group, metric)` to `(chart, group, metric)`.

## Relevant Files

- `spec/init_live_bench.md` — the v1 platform spec; sections §4 (data model), §6 (backend file-by-file), §7 (CLI), §8 (frontend), §9 (wire), §14 (animation + newer-wins). The schema change must respect every contract in there.
- `specs/live-bench-build-plan.md` — the v1 build plan and validation strategy. The Layer 1/2/3 validation pattern is reused here verbatim.
- `apps/backend/src/live_bench_server/models.py` — the contract. ChartDef gets added here, BenchmarkConfig grows the optional `charts` field, DataPoint/DataPointStored/DatasetState gain `chart_id`, IngestRequest's `complete_groups` gains a CompletionRef shape (with backward-compat string coercion).
- `apps/backend/src/live_bench_server/db.py` — schema migration. Add `chart_id TEXT NOT NULL DEFAULT 'default'` to `datapoints` and `completions`. Drop and recreate `ix_datapoints_cell_client_ts` to include `chart_id`. Detect existing column via `PRAGMA table_info` and ALTER TABLE conditionally so the migration is idempotent on the dev DB.
- `apps/backend/src/live_bench_server/store.py` — every helper that touches a cell now keys by `(chart_id, group_key, metric_key)`. `latest_per_cell` returns one row per chart-cell. `mark_complete` takes chart-aware CompletionRef. `dataset_states` enumerates `(chart_id, group_key)` from the iterated `cfg.all_charts()`.
- `apps/backend/src/live_bench_server/http_ingest.py` — validate `chart_id` against `cfg.all_charts()`. New 400 error code: `unknown_chart`. Validate group/metric within the *specific chart*, not the benchmark.
- `apps/backend/src/live_bench_server/sse_stream.py` — no logic changes; events carry `chart_id` automatically because the underlying models do.
- `apps/backend/src/live_bench_server/rest.py` — `GET /benchmarks` summary now includes `chart_count`. `better` becomes nullable in the summary (multi-chart benchmarks don't have a single answer).
- `apps/backend/tests/test_store.py`, `test_http_ingest.py`, `test_sse_stream.py` — extend with chart_id cases. Existing tests must still pass (they use the legacy default `chart_id="default"` path).
- `apps/backend/tests/fixtures_export.py` — export `ChartDef` JSON fixture and update `BenchmarkConfig` / `DataPointStored` / `DatasetState` fixtures with the new field.
- `apps/cli/src/live_bench_cli/commands/emit_cmd.py` — `--chart CHART_ID` flag (default `"default"`). JSONL batch lines accept optional `chart_id`.
- `apps/cli/src/live_bench_cli/commands/complete_cmd.py` — `--chart CHART_ID` flag (default `"default"`); the chart applies to all `--group` flags in the same invocation.
- `apps/cli/src/live_bench_cli/commands/stream_cmd.py` — JSONL data and control lines accept optional `chart` field. Default `"default"`.
- `apps/cli/src/live_bench_cli/commands/show_cmd.py` — render the per-chart matrix instead of a single flat group/metric matrix when the benchmark has multiple charts.
- `apps/cli/tests/test_commands.py` — extend with `--chart` cases and JSONL passthrough.
- `apps/frontend/src/schemas.ts` — `ChartDefSchema`, update `BenchmarkConfigSchema` (charts optional, top-level fields optional), add `chart_id` to `DataPointSchema`/`DataPointStoredSchema`/`DatasetStateSchema`/`SseDatapointSchema`/`SseDatasetCompleteSchema`. Update `BenchmarkSummarySchema` with optional `chart_count` and nullable `better`.
- `apps/frontend/src/stores/session.ts` — cell key changes from `${group}:${metric}` to `${chart}:${group}:${metric}`. `datasets` map keyed by `${chart}:${group}` instead of just `group`. `applySnapshot`, `applyDatapoint`, `applyDatasetComplete`, `applyReset` all updated. The §14.4 newer-wins guard logic is unchanged — only the key derivation changes.
- `apps/frontend/src/stores/session.test.ts` — add tests for chart-keyed updates and the multi-chart snapshot rebuild.
- `apps/frontend/src/pages/BenchmarkPage.vue` — iterate `config.all_charts` (a small client-side helper that mirrors `BenchmarkConfig.all_charts()` from the Pydantic side) and render one `<BenchmarkCard>` per chart inside the `<BenchmarkGrid>`. The grid's column count still comes from `prefs.density` so multi-chart benchmarks naturally fan out across the page in Medium/Small density.
- `apps/frontend/src/components/BenchmarkCard.vue` — refactor: instead of taking the full `BenchmarkConfig`, take a `chart: ChartDef` plus the shared `groups: GroupDef[]`, `betterLabel: string`, plus the chart-scoped slices of `latest` / `latestClientTs` / `datasets`. The header still renders title / subtitle / `Higher/Lower is better` / `<DatasetStatusBar>`, just sourced from the chart not the benchmark.
- `apps/frontend/src/components/GroupedBarChart.vue` — same refactor: takes chart-scoped data instead of the whole config. Internal scale + bar-laying logic unchanged. The cell-key lookup against the session store now uses the `${chart}:${group}:${metric}` key.
- `apps/frontend/src/components/DatasetStatusBar.vue` — receives the chart-scoped dataset list (filtered to the chart's groups, sourced from the `${chart}:${group}` keyed map).
- `apps/frontend/src/pages/LandingPage.vue` — the existing table needs a small tweak: show `chart_count` for multi-chart benchmarks. Either add a new column or fold into the existing "Direction" column (e.g. show `↑ higher` for single-chart and `3 charts` for multi-chart).
- `apps/frontend/src/pages/LandingPage.test.ts` — extend the test with one fixture row that has `chart_count > 1` and `better: null`.
- `benchmarks/test-trio.yaml` — REPLACED. The current shape (3 separate benchmarks via the `benchmarks: list[]` extension) becomes ONE benchmark `trio` with `charts: list[ChartDef]`.
- `apps/backend/live-bench.db` — existing dev database has rows for the now-deleted `trio-recall` / `trio-qps` / `trio-latency` session IDs. The integration validator must wipe these orphans (or the whole db) before the e2e test.

### New Files

- `specs/single-benchmark-many-charts.md` — this plan.
- `specs/single-benchmark-many-charts-validation.md` — the validation report written by `integration-validator` at the end.
- `screenshots/multi-chart-*.png` — playwright screenshots from the e2e validation (landing table with `trio` row, the trio page showing 3 charts, the trio page after live emits, theme cycle, etc.).

## Implementation Phases

### Phase 1: Foundation
Extend `models.py` with `ChartDef`, optional `charts` field on `BenchmarkConfig`, the validator + `all_charts()` helper, and `chart_id` on `DataPoint` / `DataPointStored` / `DatasetState`. Add `CompletionRef` with the string-coerce field validator on `IngestRequest.complete_groups`. Update `tests/fixtures_export.py` to emit a `ChartDef.json` fixture and refresh existing fixtures with the new fields.

This is the contract — no other phase can start until it's done. Run `cd apps/backend && uv sync && uv run python tests/fixtures_export.py` to verify fixtures generate cleanly.

### Phase 2: Core Implementation (parallel)
Three builders run in parallel against the new contract:

- **Backend** writes the `db.py` migration (idempotent ALTER TABLE detection), updates `store.py` (insert_points, latest_per_cell, mark_complete, dataset_states all chart-aware), updates `http_ingest.py` (validate `chart_id` against `cfg.all_charts()`, emit `unknown_chart` 400), updates `rest.py` (`GET /benchmarks` summary includes `chart_count`), and refreshes the three pytest files. **Backend smoke**: launch on smoke port 18787, hit `/healthz`, POST a multi-chart point, GET the snapshot, verify chart_id round-trips.
- **CLI** adds `--chart` to `emit_cmd`, `complete_cmd`, and the stream JSONL parser. Updates `show_cmd` to render the per-chart matrix. Refreshes `test_commands.py` with chart-aware cases. **CLI smoke**: launch a fresh backend on smoke port 18788, run `live-bench emit trio --chart recall --group faiss --metric recall --value 0.94`, verify it round-trips through `live-bench show trio`.
- **Frontend** updates `schemas.ts` (Zod ChartDef + optional fields), `stores/session.ts` (chart-keyed cells + tests), refactors `BenchmarkPage.vue` to loop over charts and render one card per chart, refactors `BenchmarkCard` and `GroupedBarChart` to take chart-scoped props, adjusts `LandingPage` to show `chart_count`. **Frontend smoke**: launch on smoke ports 18789 (backend) + 15787 (vite via `vite.config.smoke.ts`), use `playwright-bowser-agent` to load a multi-chart benchmark and assert N cards render with N independent dataset status bars.

### Phase 3: Integration & Polish
Replace `benchmarks/test-trio.yaml` with the one-benchmark-three-charts shape. Wipe leftover `trio-recall` / `trio-qps` / `trio-latency` rows from the dev SQLite (or `rm` the db). Run `integration-validator` end-to-end against ports 8787 + 5787:

1. Boot backend + frontend via `just serve` (with port-clearing).
2. Verify `GET /benchmarks` returns 9 entries (8 unchanged + the new `trio`); the trio summary shows `chart_count: 3` and `better: null`.
3. Open the landing page in a browser. Confirm exactly one `trio` row (not three).
4. Click "View →" on `trio`. Confirm the page renders **three cards** stacked: `Recall@10`, `Query Throughput`, `p99 Query Latency`. Each card has its own header, "Higher/Lower is better" line, `<DatasetStatusBar>`, and `<GroupedBarChart>`. Empty initial state.
5. Run `just test-drive-trio-fill` (a new recipe) which emits into all three charts via `live-bench emit trio --chart recall ...` etc. Verify all three cards animate to their values simultaneously without bleed-over. Take a screenshot.
6. Run `just test-drive-trio-complete` (a new recipe). Verify each chart's pills flip independently to complete.
7. Restart the backend mid-stream. Verify all three cards retain their values via `latest_per_cell` snapshot + SSE reconnect.
8. Verify all 8 existing single-chart benchmarks still load and render correctly (regression check) — pick `gemma4-e4b-prefill-2026-04-07` and confirm the legacy synthesis path still works.
9. Run all unit test suites (backend pytest, cli pytest, frontend vitest) — must remain green.
10. Write `specs/single-benchmark-many-charts-validation.md` with one row per acceptance criterion + screenshot paths.

## Team Orchestration

- You operate as the team lead and orchestrate the team to execute the plan.
- You're responsible for deploying the right team members with the right context to execute the plan.
- IMPORTANT: You NEVER operate directly on the codebase. You use `Task` and `Task*` tools to deploy team members to to the building, validating, testing, deploying, and other tasks.
  - This is critical. You're job is to act as a high level director of the team, not a builder.
  - You're role is to validate all work is going well and make sure the team is on track to complete the plan.
  - You'll orchestrate this by using the Task* Tools to manage coordination between the team members.
  - Communication is paramount. You'll use the Task* Tools to communicate with the team members and ensure they're on track to complete the plan.
- Take note of the session id of each team member. This is how you'll reference them.

### Team Members

No specialised team agents exist under `.claude/agents/team/`, so every team member uses `general-purpose` with a unique name so the team lead can address each one individually.

- Builder
  - Name: `models-extender`
  - Role: Surgical extension of `apps/backend/src/live_bench_server/models.py` to add `ChartDef`, the optional `charts` field on `BenchmarkConfig` with the one-of validator and `all_charts()` helper, the `chart_id` field on `DataPoint` / `DataPointStored` / `DatasetState`, the new `CompletionRef` with backward-compat string coercion on `IngestRequest.complete_groups`, and the SSE event types that carry `chart_id`. Also updates `apps/backend/tests/fixtures_export.py` to emit a `ChartDef.json` fixture and refresh the affected ones. Verifies all 8 existing benchmark YAMLs still validate against the updated schema.
  - Agent Type: `general-purpose`
  - Resume: true
- Builder
  - Name: `backend-extender`
  - Role: Implements the backend changes — `db.py` idempotent migration adding `chart_id` columns + the new index, `store.py` chart-aware repository methods, `http_ingest.py` `unknown_chart` validation + per-chart group/metric validation, `rest.py` summary now carrying `chart_count` and nullable `better`. Updates the three pytest files with chart-aware cases (existing tests stay green via the `default` chart_id). Runs `uv run pytest -v` and the Layer 2 backend smoke on port **18787**.
  - Agent Type: `general-purpose`
  - Resume: true
- Builder
  - Name: `cli-extender`
  - Role: Adds `--chart CHART_ID` flag (default `"default"`) to `emit_cmd`, `complete_cmd`, and the JSONL passthrough in `stream_cmd`. Updates `show_cmd` to render the per-chart matrix when the benchmark has multiple charts. Extends `test_commands.py` with chart-aware cases. Runs `uv run pytest -v` and the Layer 2 CLI smoke on port **18788**.
  - Agent Type: `general-purpose`
  - Resume: true
- Builder
  - Name: `frontend-extender`
  - Role: Updates `schemas.ts` with `ChartDefSchema` + optional fields on `BenchmarkConfigSchema`, adds `chart_id` to all relevant Zod schemas. Updates `stores/session.ts` to use `${chart}:${group}:${metric}` cell keys and `${chart}:${group}` dataset keys, with the §14.4 newer-wins guard preserved. Refactors `BenchmarkPage.vue` to loop over `config.all_charts` rendering one `<BenchmarkCard>` per chart. Refactors `BenchmarkCard` and `GroupedBarChart` to take chart-scoped props. Updates `LandingPage.vue` to show `chart_count` for multi-chart benchmarks (replacing the single-chart "Direction" column or augmenting it). Extends the existing tests. Runs `pnpm test` and `pnpm build` and the Layer 2 frontend smoke on ports **18789 + 15787**.
  - Agent Type: `general-purpose`
  - Resume: true
- Validator
  - Name: `multi-chart-validator`
  - Role: Phase 3 end-to-end validation. Replaces `benchmarks/test-trio.yaml` with the one-benchmark-three-charts shape, wipes leftover trio rows from the dev SQLite, adds two new `just` recipes (`test-drive-trio-fill` and `test-drive-trio-complete`) and emits data into all three charts. Drives `/drive` for process orchestration on production ports 8787 + 5787, drives `playwright-bowser-agent` for browser DOM/SVG verification, and writes `specs/single-benchmark-many-charts-validation.md` mapping every acceptance criterion to a pass/fail + screenshot path. Also runs a regression check on a legacy single-chart benchmark to confirm the synthesis path still works.
  - Agent Type: `general-purpose`
  - Resume: true

## Step by Step Tasks

- IMPORTANT: Execute every step in order, top to bottom. Each task maps directly to a `TaskCreate` call.
- Before you start, run `TaskCreate` to create the initial task list that all team members can see and execute.

### 1. Extend Pydantic Models for Multi-Chart
- **Task ID**: `models-multichart`
- **Depends On**: none
- **Assigned To**: `models-extender`
- **Agent Type**: `general-purpose`
- **Parallel**: false
- Read `spec/init_live_bench.md` §4 and `specs/single-benchmark-many-charts.md` solution approach.
- Add `ChartDef` class to `apps/backend/src/live_bench_server/models.py`: fields `chart_id: str`, `title: str | None = None`, `subtitle: str | None = None`, `better: Better`, `direction: Direction = "BT"`, `x: AxisConfig`, `y: AxisConfig`, `metrics: list[MetricDef]`.
- Update `BenchmarkConfig`: add `charts: list[ChartDef] | None = None`. Make `metrics`, `x`, `y`, `better` OPTIONAL (with defaults that don't conflict — `None`). Keep `direction: Direction = "BT"` as the default for the legacy single-chart synthesis.
- Add a `@model_validator(mode="after")` named `_normalize_chart_form` that asserts exactly one of {top-level chart fields all set} or {`charts` set with len ≥ 1} is true. Raise a clear ValueError otherwise.
- Add `BenchmarkConfig.all_charts() -> list[ChartDef]`. If `self.charts is not None`, return it. Else synthesize `[ChartDef(chart_id="default", title=None, subtitle=None, better=self.better, direction=self.direction, x=self.x, y=self.y, metrics=self.metrics)]`.
- Add `chart_id: str = "default"` to `DataPoint`, `DataPointStored`, `DatasetState`. **`chart_id` MUST come before `group_key` in field order so the JSON serialization is deterministic.**
- Add `CompletionRef(_LiveBenchModel)` with `chart_id: str = "default"`, `group_key: str`.
- Update `IngestRequest.complete_groups: list[CompletionRef] = Field(default_factory=list)`. Add a `@field_validator("complete_groups", mode="before")` that coerces bare strings to `{"chart_id": "default", "group_key": <str>}` so the existing CLI's string-list shape keeps working unchanged.
- Add `chart_id: str = "default"` to `SseDatasetComplete`.
- Update `apps/backend/tests/fixtures_export.py` to emit a new `ChartDef.json` fixture and refresh `BenchmarkConfig.json`, `DataPointStored.json`, `DatasetState.json`, `SseSnapshot.json`, `SseDatapoint.json`, `SseDatasetComplete.json` with the new `chart_id` field.
- Run: `cd apps/backend && uv sync && uv run python tests/fixtures_export.py && ls tests/fixtures/`. Confirm `ChartDef.json` exists and the refreshed fixtures all carry `chart_id`.
- Run: `uv run python -c "import yaml; from pathlib import Path; from live_bench_server.models import BenchmarkFile; [BenchmarkFile.model_validate(yaml.safe_load(p.read_text())) for p in sorted(Path('../../benchmarks').glob('*.yaml'))]"`. **All 9 existing benchmark YAMLs (8 single + the legacy trio multi-benchmark file) must still validate cleanly via the legacy single-chart synthesis path.** Report any validation failures with the file name.
- Verify the path-dep CLI sync still works: `cd ../cli && uv sync`.
- Report the new fixture filenames + the YAML validation result + any deviations.

### 2. Backend Migration + Store + Ingest + Tests + Smoke
- **Task ID**: `backend-multichart`
- **Depends On**: `models-multichart`
- **Assigned To**: `backend-extender`
- **Agent Type**: `general-purpose`
- **Parallel**: true (with `cli-multichart` and `frontend-multichart`)
- Read `spec/init_live_bench.md` §4.1 + §6 + §9 + the plan's solution approach.
- **`db.py`**: extend `_SCHEMA` with `chart_id` columns on `datapoints` and `completions`. Drop the old `ix_datapoints_cell_client_ts` index and recreate it as `(session_id, chart_id, group_key, metric_key, client_ts DESC)`. Add an idempotent `_ensure_chart_id_columns(conn)` helper called from `migrate(conn)` that checks `PRAGMA table_info(datapoints)` for the `chart_id` column and ALTER TABLE adds it with `DEFAULT 'default'` if missing. Same for `completions`. The `completions` PK rebuild is a recreate-and-copy: `BEGIN; CREATE TABLE completions_new(...); INSERT INTO completions_new SELECT session_id, 'default', group_key, completed_at FROM completions; DROP TABLE completions; ALTER TABLE completions_new RENAME TO completions; COMMIT;` — wrap in a try/except so it's idempotent. Update `row_to_datapoint_stored` to read `row["chart_id"]`.
- **`store.py`**: every helper that currently keys by `(group_key, metric_key)` now keys by `(chart_id, group_key, metric_key)`. Specifically:
  - `insert_points(conn, session_id, points: list[DataPoint])` reads `point.chart_id` and inserts it.
  - `latest_per_cell(session_id) -> list[DataPointStored]` returns one row per `(chart_id, group_key, metric_key)` cell.
  - `mark_complete(conn, session_id, refs: list[CompletionRef]) -> list[tuple[CompletionRef, datetime]]` upserts into completions with the chart_id.
  - `dataset_states(conn, session_id) -> list[DatasetState]` enumerates `(chart_id, group_key)` pairs from `cfg.all_charts()` × `cfg.groups` and computes status. Each chart gets its own pending/running/complete derivation.
  - `reset(conn, session_id)` still wipes everything for the session (no per-chart reset for v1).
- **`http_ingest.py`**: validate `point.chart_id` exists in `cfg.all_charts()` → 400 `{"code": "unknown_chart", "message": "chart 'foo' not in session config"}`. Validate `point.group_key` exists in `cfg.groups` (still benchmark-level). Validate `point.metric_key` exists in **the specific chart's** metrics, not the benchmark — if a metric is on chart A but you target chart B with that metric_key, it must 400 `unknown_metric`. Same chart-aware validation for `complete_groups: list[CompletionRef]`.
- **`sse_stream.py`**: no logic changes needed; events serialize with their `chart_id` automatically. Verify the `SseSnapshot` includes points + datasets with chart_id populated.
- **`rest.py`**: `GET /benchmarks` summary now includes `chart_count: int` (= `len(cfg.all_charts())`). The `better` field becomes `Better | None` — set to `cfg.all_charts()[0].better` if `chart_count == 1`, else `None`. `GET /benchmarks/{id}` returns the full BenchmarkConfig (which carries either the legacy top-level fields OR the new `charts` field — frontend handles both).
- **Tests**: extend `tests/test_store.py` with cases proving chart_id is round-tripped, latest_per_cell isolates cells across charts, mark_complete isolates charts. Extend `tests/test_http_ingest.py` with `test_unknown_chart` and `test_chart_isolation_in_validation` (a metric that exists in chart A but not chart B is rejected when targeting chart B). Extend `tests/test_sse_stream.py` to assert SSE events carry `chart_id`. Existing tests must pass unchanged via the `default` chart_id path.
- Run: `cd apps/backend && uv sync && uv run pytest -v && uv run python tests/fixtures_export.py`.
- **Layer 2 backend smoke (port 18787)**: launch a fresh backend instance against `./live-bench-smoke-multichart.db`, hit `/healthz`, POST a multi-chart point against the legacy `default` chart on `test-drive-lr` to prove backward compat, then POST against an explicit chart_id and assert 400 `unknown_chart` for an invalid chart, then assert 200 with the right values for a valid one. Tear down. Report all outputs.

### 3. CLI Multi-Chart Support + Tests + Smoke
- **Task ID**: `cli-multichart`
- **Depends On**: `models-multichart`
- **Assigned To**: `cli-extender`
- **Agent Type**: `general-purpose`
- **Parallel**: true (with `backend-multichart` and `frontend-multichart`)
- Read `spec/init_live_bench.md` §7 + the plan's CLI bullets in the relevant-files section.
- `commands/emit_cmd.py`: add `--chart CHART_ID` option (default `"default"`). For single mode, stamp it onto the `DataPoint`. For batch mode, each JSONL line may carry its own `chart_id`; if absent, fall back to `--chart`'s value (which itself defaults to `"default"`). Stamping happens at READ TIME just like `client_ts`.
- `commands/complete_cmd.py`: add `--chart CHART_ID` option (default `"default"`). Build `complete_groups` as a list of `CompletionRef(chart_id=<--chart>, group_key=<--group>)` for each `--group` flag.
- `commands/stream_cmd.py`: extend the JSONL reader. Data lines `{"group": "g", "metric": "m", "value": 1.0}` accept an optional `"chart": "c"` field (default `"default"`). Control lines `{"complete": "g"}` accept an optional `"chart": "c"` field. Same READ-TIME stamping rules.
- `commands/show_cmd.py`: when `len(config.all_charts) > 1`, render a per-chart sub-matrix (one labeled section per chart) instead of a flat group/metric matrix. When the count is 1, keep the existing legacy rendering (no behavior change for single-chart benchmarks).
- `commands/list_cmd.py`: add a `Charts` column to the rich table next to `Better` showing `chart_count`. (Mirrors the frontend landing table change.)
- Tests in `tests/test_commands.py`:
  - `test_emit_single_with_chart_flag` — `--chart recall` produces `DataPoint(chart_id="recall", ...)`.
  - `test_emit_batch_passes_through_explicit_chart_id` — JSONL line with `"chart_id": "qps"` is preserved unchanged.
  - `test_emit_batch_defaults_to_default_chart` — JSONL line without `chart_id` produces `chart_id="default"`.
  - `test_complete_command_with_chart_flag` — `--chart recall --group faiss --group qdrant` produces two `CompletionRef(chart_id="recall", ...)`.
  - `test_stream_recognises_chart_in_control_line` — `{"complete": "faiss", "chart": "recall"}` produces a `CompletionRef(chart_id="recall", group_key="faiss")`.
- Run: `cd apps/cli && uv sync && uv run pytest -v && uv run live-bench --help`.
- **Layer 2 CLI smoke (port 18788)**: launch a fresh backend on 18788, run `live-bench emit test-drive-lr --group alpha --metric latency_ms --value 42` to prove backward compat (no `--chart` defaults to `"default"`). Then (this step is optional and only runs if `backend-multichart` has already published the new `trio` benchmark — guard with a conditional check; otherwise skip): `live-bench emit trio --chart recall --group faiss --metric recall --value 0.94` and `live-bench show trio` to verify the chart-aware path. Tear down. Report.

### 4. Frontend Multi-Chart Rendering + Tests + Smoke
- **Task ID**: `frontend-multichart`
- **Depends On**: `models-multichart`
- **Assigned To**: `frontend-extender`
- **Agent Type**: `general-purpose`
- **Parallel**: true (with `backend-multichart` and `cli-multichart`)
- Read `spec/init_live_bench.md` §8 + §14 + the plan's frontend bullets.
- `schemas.ts`: add `ChartDefSchema` with the same shape as the Pydantic ChartDef. Update `BenchmarkConfigSchema`: `charts` becomes `z.array(ChartDefSchema).optional()`, `metrics`/`x`/`y`/`better` become optional. Add a refinement / `superRefine` enforcing the one-of constraint, OR just trust the backend (which already enforces it). Add `chart_id` to `DataPointSchema`, `DataPointStoredSchema`, `DatasetStateSchema`, `SseDatapointSchema`'s `point`, and `SseDatasetCompleteSchema`. Add `CompletionRefSchema`. Update `IngestRequestSchema.complete_groups` to `z.array(CompletionRefSchema)`. Update `BenchmarkSummarySchema` with optional `chart_count` and nullable `better`.
- Add a TS helper `allCharts(config: BenchmarkConfig): ChartDef[]` mirroring `BenchmarkConfig.all_charts()` from Pydantic. Either lives in `schemas.ts` or a new `lib/charts.ts`. Returns the explicit `charts` if set, otherwise synthesizes a single default `ChartDef`.
- `stores/session.ts`: cell key changes from `${group_key}:${metric_key}` to `${chart_id}:${group_key}:${metric_key}`. The `latest`, `latestClientTs` maps use the new key. The `datasets` map keys change from `group_key` to `${chart_id}:${group_key}`. Update `applySnapshot` (rebuild from snapshot.points which now carry chart_id, and snapshot.datasets which now carry chart_id), `applyDatapoint` (preserve §14.4 newer-wins guard with the new key), `applyDatasetComplete` (now takes chart_id), `applyReset` (clears all maps and re-derives pending from `cfg.all_charts() × cfg.groups`).
- `stores/session.test.ts`: extend tests to cover chart-keyed cell isolation. Add a test that proves a datapoint emitted into chart A does NOT appear in chart B's `latest` map (cell isolation across charts).
- `pages/BenchmarkPage.vue`: iterate `allCharts(config)` rendering one `<BenchmarkCard>` per chart inside the existing `<BenchmarkGrid>`. Pass each card the chart's `ChartDef` plus the shared groups plus the chart-scoped slices of the session store.
- `components/BenchmarkCard.vue`: refactor props from `{ config: BenchmarkConfig }` to `{ chart: ChartDef, groups: GroupDef[], latest: Map, latestClientTs: Map, datasets: Map<string, DatasetState>, lastUpdate: string | null }`. Compute "Higher is better" / "Lower is better" from `chart.better`. The body still renders `<DatasetStatusBar>` + `<GroupedBarChart>`, just with chart-scoped data.
- `components/GroupedBarChart.vue`: refactor props from `{ config: BenchmarkConfig, ... }` to `{ chart: ChartDef, groups: GroupDef[], latest: Map, ... }`. Use `chart.x`, `chart.y`, `chart.metrics`, `chart.direction` instead of `config.*`. The §13.2.1 LR cutoff fix from the previous iteration must remain intact.
- `components/DatasetStatusBar.vue`: takes a list of `DatasetState[]` filtered to one chart's groups. Compute `complete_count / total_count` from THIS chart's pills only.
- `pages/LandingPage.vue`: rename "Direction" column to "Charts" (or add a new "Charts" column). For single-chart benchmarks, show `↑ higher` / `↓ lower` (existing behavior). For multi-chart, show `N charts`. The sortable headers stay (Name + Last updated).
- `pages/LandingPage.test.ts`: extend the fixture with one row that has `chart_count: 3` and `better: null`. Add an assertion that the new column renders `3 charts` for that row.
- Run: `cd apps/frontend && PATH="/opt/homebrew/bin:$PATH" pnpm test && PATH="/opt/homebrew/bin:$PATH" pnpm build`.
- **Layer 2 frontend smoke (ports 18789 + 15787)**: launch backend on 18789 and vite via `vite.config.smoke.ts` on 15787, then use `playwright-bowser-agent` to load the frontend, navigate to a single-chart benchmark (e.g. `gemma4-e4b-prefill-2026-04-07`) — confirm it still renders ONE card. Then check if the new `trio` benchmark exists (only present if `multi-chart-validator` has run the YAML replace, which it hasn't yet — so this is conditional). If the trio doesn't exist, the smoke just verifies the legacy single-chart path still works. Take a screenshot to `screenshots/multi-chart-frontend-smoke-legacy.png`. Tear down. Report.

### 5. Recreate Trio + Full E2E Validation
- **Task ID**: `multichart-validate`
- **Depends On**: `backend-multichart`, `cli-multichart`, `frontend-multichart`
- **Assigned To**: `multi-chart-validator`
- **Agent Type**: `general-purpose`
- **Parallel**: false
- Read this plan's Phase 3 + the existing `spec/init_live_bench.md` §10/§17 + `specs/live-bench-build-plan.md` validation strategy.
- **Step 1 — Replace `benchmarks/test-trio.yaml`** with the new shape: ONE benchmark `trio` with `groups` defined once at the benchmark level (FAISS / Qdrant / LanceDB) and `charts: list[ChartDef]` with three entries — `recall` (BT, single emerald metric, `better: higher`, axis 0..1), `qps` (BT, gradient blue→cyan, `better: higher`, axis 0..auto), `latency` (LR, gradient amber→red, `better: lower`, axis 0..auto). Each chart has its own `title` and optionally a `subtitle`. The metric keys can repeat across charts since they're scoped to the chart.
- **Step 2 — Add two new just recipes** to the root `justfile`:
  - `test-drive-trio-fill`: emits 9 values via `live-bench emit trio --chart recall|qps|latency --group faiss|qdrant|lancedb --metric recall|qps|p99_ms --value <v>`. Realistic numbers: recall {faiss=0.94, qdrant=0.91, lancedb=0.88}; qps {faiss=12500, qdrant=8200, lancedb=6400}; p99_ms {faiss=4.2, qdrant=7.8, lancedb=11.5}.
  - `test-drive-trio-complete`: marks all three groups complete on all three charts via `live-bench complete trio --chart recall --group faiss --group qdrant --group lancedb` (and the same for qps + latency).
- **Step 3 — Wipe leftover trio rows from the dev SQLite**. The previous shape created three separate sessions (`trio-recall`, `trio-qps`, `trio-latency`) that are now orphans. Either `mv apps/backend/live-bench.db /tmp/old-pre-multichart.db` (clean slate) or `sqlite3 apps/backend/live-bench.db "DELETE FROM benchmarks WHERE session_id LIKE 'trio-%'"`. Clean slate is simpler.
- **Step 4 — Boot the stack**: `just free-ports && just serve` (or `just backend &` + `just frontend &` if mprocs is unavailable). Poll `/healthz` and `/` for ready.
- **Step 5 — Verify GET /benchmarks**: `curl -s http://127.0.0.1:8787/benchmarks | python3 -m json.tool` returns 9 entries (8 unchanged + new `trio`). The trio summary must have `chart_count: 3` and `better: null`. Each of the 8 legacy summaries must have `chart_count: 1` and a populated `better`.
- **Step 6 — Browser landing check** via `playwright-bowser-agent`: load `http://127.0.0.1:5787/`. Confirm exactly one `trio` row in the landing table (NOT three). Confirm the row's "Charts" column reads `3 charts`. Take screenshot to `screenshots/multi-chart-landing.png`.
- **Step 7 — Empty trio page**: click "View →" on the trio row. URL should become `/benchmark/trio`. Confirm exactly THREE `<BenchmarkCard>` components render, in the order `recall` → `qps` → `latency`. Each card shows its own title (`Recall@10`, `Query Throughput`, `p99 Query Latency`), its own `Higher/Lower is better` line (`higher`, `higher`, `lower`), its own `0 / 3 complete` status bar with 3 pending pills, and an empty chart with the right axis labels and direction. Take screenshot to `screenshots/multi-chart-trio-empty.png`.
- **Step 8 — Live emit**: from a separate shell, run `just test-drive-trio-fill`. Wait 1.5 s. Playwright re-reads the page. Verify each card's bars animated to the expected values:
  - `recall` card: bars at faiss=0.94, qdrant=0.91, lancedb=0.88 (rendered against the 0..1 fixed axis)
  - `qps` card: bars at 12500 / 8200 / 6400 in the blue→cyan gradient
  - `latency` card: bars at 4.2 / 7.8 / 11.5 in the amber→red gradient, with FAISS / Qdrant / LanceDB y-axis labels FULLY VISIBLE (regression check on the previous LR cutoff fix). Take screenshot to `screenshots/multi-chart-trio-filled.png`.
- **Step 9 — Cell isolation check**: emit ONE point into ONLY `chart=recall, group=faiss, metric=recall, value=0.97` via `live-bench emit trio --chart recall --group faiss --metric recall --value 0.97`. Wait 1.5 s. Read playwright SVG: the recall card's faiss bar should now show 0.97; the qps and latency cards must remain at their step-8 values. This proves cell isolation across charts.
- **Step 10 — Per-chart completion**: from a separate shell, `just test-drive-trio-complete`. Verify EACH card's status bar independently flips to `3 / 3 complete` with all three pills green. Take screenshot to `screenshots/multi-chart-trio-complete.png`.
- **Step 11 — Restart resilience**: kill backend, wait 2 s, relaunch. Playwright observes ConnectionBadge cycle amber → green. Re-read SVG: all 9 bar values across all 3 cards must match the step-9 values. Take screenshot to `screenshots/multi-chart-trio-after-restart.png`.
- **Step 12 — Legacy regression check**: navigate to `/benchmark/gemma4-e4b-prefill-2026-04-07` (a single-chart benchmark). Confirm exactly ONE `<BenchmarkCard>` renders with the legacy synthesis path. Take screenshot to `screenshots/multi-chart-legacy-regression.png`. This proves backward compat.
- **Step 13 — Run all unit tests**: `cd apps/backend && uv run pytest -v` (existing 18 + new chart-aware tests, all green); `cd apps/cli && uv run pytest -v` (existing 13 + new --chart tests); `cd apps/frontend && PATH="/opt/homebrew/bin:$PATH" pnpm test` (existing 35 + new chart-keyed store + landing column test); `cd apps/frontend && PATH="/opt/homebrew/bin:$PATH" pnpm build` (clean, zero TS errors). Capture pass counts.
- **Step 14 — Tear down + final port check**: kill backend + frontend + smoke processes. `just free-ports && just ports` → both `free`.
- **Step 15 — Write the validation report**: `specs/single-benchmark-many-charts-validation.md` with one row per acceptance criterion below + the screenshot path that proves it. Append the captured stdout from steps 5-13. Report failures with file:line context for the most likely culprit.

## Acceptance Criteria

- **AC-Schema** — `BenchmarkConfig` accepts both shapes: legacy top-level fields (synthesizing one default chart) AND the new explicit `charts: list[ChartDef]`. The model_validator rejects "neither" and "both". `BenchmarkConfig.all_charts()` returns the right list in both cases.
- **AC-BackwardCompat-YAMLs** — All 8 existing single-chart YAMLs validate against the new schema unchanged. Their landing rows show `1 chart` (or whatever the column label becomes) and a populated `better`.
- **AC-BackwardCompat-CLI** — `live-bench emit test-drive-lr --group alpha --metric latency_ms --value 42` (no `--chart` flag) round-trips through the new schema as `chart_id="default"` and `live-bench show test-drive-lr` displays it correctly.
- **AC-BackwardCompat-DB** — Running the new migration against the existing dev `live-bench.db` succeeds without data loss; existing rows get `chart_id='default'` via the ALTER TABLE / table-rebuild.
- **AC-NewSchema-Trio** — `benchmarks/test-trio.yaml` is now ONE benchmark `trio` with three charts. `GET /benchmarks` returns ONE entry for `trio` (not three). The `trio` row's `chart_count` is 3.
- **AC-MultiCardRender** — `/benchmark/trio` renders exactly three `<BenchmarkCard>` components, one per chart, each with its own header and chart body.
- **AC-PerChart-Better** — Each card's "Higher is better" / "Lower is better" line reflects THAT chart's `better`, not a benchmark-level value. (recall=higher, qps=higher, latency=lower)
- **AC-CellIsolation** — Emitting into `(chart=recall, group=faiss, metric=recall)` updates ONLY that one bar; the qps and latency cards' faiss bars remain unchanged.
- **AC-PerChart-Datasets** — Each card's `<DatasetStatusBar>` reflects only that chart's groups. Marking complete on `chart=recall` does NOT affect the qps or latency dataset pills.
- **AC-NewerWins-MultiChart** — The §14.4 newer-wins guard still holds with chart-keyed cells: an out-of-order client_ts on `(chart=qps, group=faiss)` does not regress that bar.
- **AC-RestartResilience** — After a backend restart, all 9 bar values across all 3 cards survive via `latest_per_cell` snapshot replay.
- **AC-LR-Cutoff-StillFixed** — The trio's `latency` chart (LR direction) renders FAISS / Qdrant / LanceDB y-axis labels fully visible — no clipping (regression check on the previous fix).
- **AC-Tests** — All unit suites green: backend pytest (18 + new), cli pytest (13 + new), frontend vitest (35 + new). `pnpm build` zero TS errors.
- **AC-Errors** — `POST /ingest` with an unknown `chart_id` returns `400 unknown_chart`. With a metric_key that exists in another chart but not the targeted one returns `400 unknown_metric`.

## Validation Commands

Execute these to validate the task is complete:

- `cd apps/backend && uv sync && uv run pytest -v` — backend tests (existing + new) all pass.
- `cd apps/backend && uv run python tests/fixtures_export.py && ls tests/fixtures/` — fixtures regenerate including `ChartDef.json`.
- `cd apps/backend && uv run python -c "import yaml; from pathlib import Path; from live_bench_server.models import BenchmarkFile; [print(f'{p.name}: ok') for p in sorted(Path('../../benchmarks').glob('*.yaml')) for _ in [BenchmarkFile.model_validate(yaml.safe_load(p.read_text()))]]"` — every YAML in `benchmarks/` validates.
- `cd apps/cli && uv sync && uv run pytest -v && uv run live-bench --help` — CLI tests pass and `--chart` flag is in the help output.
- `cd apps/frontend && PATH="/opt/homebrew/bin:$PATH" pnpm test && PATH="/opt/homebrew/bin:$PATH" pnpm build` — frontend tests pass and the production build is clean.
- `just free-ports && just serve` — full stack boots without port conflicts.
- `curl -s http://127.0.0.1:8787/benchmarks | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d[\"benchmarks\"])} benchmarks'); [print(f'  {b[\"session_id\"]:50s} chart_count={b.get(\"chart_count\")} better={b.get(\"better\")}') for b in d['benchmarks']]"` — landing summary returns 9 entries with `trio` having `chart_count=3` and `better=null`.
- `LIVE_BENCH_SERVER=http://127.0.0.1:8787 just test-drive-trio-fill` — exits 0; subsequent `live-bench show trio` displays all 9 cell values.
- `LIVE_BENCH_SERVER=http://127.0.0.1:8787 just test-drive-trio-complete` — exits 0; `live-bench show trio` shows all three charts as 3/3 complete.
- `live-bench emit test-drive-lr --group alpha --metric latency_ms --value 42` — backward-compat path works without a `--chart` flag.
- Browser walk-through via `playwright-bowser-agent`: load `http://127.0.0.1:5787/`, click `trio` row, verify 3 cards, run trio fill, verify all bars animated, run trio complete, verify all 9 pills flip.

## Notes

- **Backward compat is a hard requirement.** The existing 8 YAMLs and any external CLI consumers MUST keep working without modification. Every test added in this iteration MUST be additive — no existing test should need to be modified beyond extending it with new chart-aware cases.
- **No new external dependencies.** Everything still in-process: SQLite, asyncio queues, Pydantic v2.
- **The dev `live-bench.db` will be wiped** by the validator before the e2e run. The integration validator handles this; no manual cleanup needed.
- **Port discipline.** Each builder uses its own dedicated smoke port range (18787 / 18788 / 18789+15787) to avoid collisions when running in parallel. The integration validator uses production ports (8787 / 5787).
- **Schema sharing across languages.** Pydantic remains the source of truth; Zod is hand-mirrored. The frontend's existing drift test (`schemas.test.ts` against `apps/backend/tests/fixtures/`) will catch any divergence — `models-extender` MUST regenerate the fixtures so the frontend test suite picks up the chart_id additions.
- **Out of scope for this iteration**: per-chart reset (`live-bench reset trio --chart recall --yes`), per-chart UI density override, dynamic chart addition/removal at runtime, drag-to-reorder charts inside a benchmark page. These are deferred.
- **Connection store / SSE behavior is unchanged** — one SSE stream per benchmark session; all chart updates flow through that one connection.

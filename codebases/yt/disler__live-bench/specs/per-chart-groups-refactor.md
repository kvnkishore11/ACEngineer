# Plan: Per-Chart Groups Refactor + Memory Charts

## Task Description

Move `groups` from `BenchmarkConfig` (benchmark-level, shared across all charts) into `ChartDef` (per-chart). No fallback, no inheritance — every chart declares its own groups. This unlocks mixing different group shapes in one benchmark (e.g., prompts for speed charts, models for memory charts). Then add 2 memory footprint charts to the qwen35-vs-gemma4 benchmark.

## Objective

When complete:
1. Each `ChartDef` has its own `groups: list[GroupDef]` — fully self-contained
2. `BenchmarkConfig.groups` is removed entirely
3. All YAMLs, backend code, frontend code, and tests updated
4. Two new memory charts (`memory_m4`, `memory_m5`) added to qwen35-vs-gemma4 with model-based groups
5. Benchmark script measures and emits memory via system RAM delta
6. All existing tests pass

## Problem Statement

`BenchmarkConfig.groups` is shared across all charts in a benchmark, preventing charts with different x-axis categories (prompts vs models) from coexisting on the same page. This forces memory charts into a separate benchmark, splitting the presentation across pages.

## Solution Approach

Move `groups` from `BenchmarkConfig` into `ChartDef`. Every chart declares its own groups inline. The backend validation, dataset state tracking, and frontend rendering already receive groups per-chart through props/function params — the refactor mainly changes where the groups are sourced from.

The legacy single-chart form (`BenchmarkConfig` with top-level `better/x/y/metrics/groups`) synthesizes a default `ChartDef` with those groups. The multi-chart form requires `groups` on each chart entry.

## Relevant Files

### Backend
- `apps/backend/src/live_bench_server/models.py` — Move `groups` from `BenchmarkConfig` to `ChartDef`. Update `_normalize_chart_form` validator. Update `all_charts()` to include groups in synthesized default chart.
- `apps/backend/src/live_bench_server/http_ingest.py` — Build per-chart group validation (lines 61-64 currently use `cfg.groups`). Change to look up `charts_by_id[chart_id].groups` per point/completion/metadata.
- `apps/backend/src/live_bench_server/store.py` — `dataset_states()` (line 437) iterates `cfg.groups` — change to `chart.groups`. `list_benchmarks()` (line 130) computes `total = len(cfg.groups)` — change to sum across all charts or use first chart.
- `apps/backend/tests/conftest.py` — Update `build_sample_config()` to put groups in the legacy fields or switch to multi-chart form with per-chart groups.
- `apps/backend/tests/test_store.py` — Update `_build_multichart_config()` to put groups on each chart.
- `apps/backend/tests/fixtures_export.py` — Update fixture generation to put groups on ChartDef, remove from BenchmarkConfig.

### Frontend
- `apps/frontend/src/schemas.ts` — Move `groups` from `BenchmarkConfigSchema` to `ChartDefSchema`. Update `allCharts()` to include groups in synthesized chart. Remove `groups` from config schema (or make optional for backward compat during transition).
- `apps/frontend/src/schemas.test.ts` — Update legacy config fixture and multi-chart test expectations.
- `apps/frontend/src/pages/BenchmarkPage.vue` — Change `session.config.groups` to `chart.groups` in template (lines 135, 152). Update modal group lookup (line 91).
- `apps/frontend/src/components/PromptModal.vue` — Already receives `groups` as prop — no change needed.
- `apps/frontend/src/components/BenchmarkCard.vue` — Already receives `groups` as prop — no change needed.
- `apps/frontend/src/components/GroupedBarChart.vue` — Already receives `groups` as prop — no change needed.

### YAMLs
- `benchmarks/qwen35-vs-gemma4.yaml` — Move groups into each chart. Add 2 memory charts with model-based groups.
- `benchmarks/mock-test.yaml` — Move groups into the chart.

### Benchmark Script
- `apps/benchmarks/qwen35-vs-gemma4/bench.py` — Add memory measurement using `psutil` system RAM delta. Emit to `memory_m4`/`memory_m5` after warmup for each backend. Add `psutil` to script dependencies.

## Implementation Phases

### Phase 1: Backend Schema + Store
Change `models.py` to move groups into `ChartDef`. Update the model validator, `all_charts()`, and the legacy form synthesis. Update `store.py` and `http_ingest.py` to use per-chart groups. Update test fixtures and conftest.

### Phase 2: Frontend Schema + Wiring
Mirror the schema change in Zod. Update `BenchmarkPage.vue` to pass `chart.groups` instead of `session.config.groups`. Update test fixtures and schema tests.

### Phase 3: YAMLs + Memory Charts + Benchmark Script
Update both YAMLs with per-chart groups. Add memory charts to qwen35-vs-gemma4. Update bench.py to measure and emit memory.

### Phase 4: Validation
Run all tests, boot platform, run mock, verify memory charts render.

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

- Builder
  - Name: builder-backend
  - Role: Backend schema refactor — models, store, ingest, tests, fixtures
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-frontend
  - Role: Frontend schema refactor — Zod, BenchmarkPage, schema tests
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-yaml-bench
  - Role: YAML updates + memory charts + bench.py memory measurement
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: validator
  - Role: Run tests, boot platform, verify everything works
  - Agent Type: general-purpose
  - Resume: true

## Step by Step Tasks

### 1. Backend — Move groups to ChartDef in models.py
- **Task ID**: backend-models
- **Depends On**: none
- **Assigned To**: builder-backend
- **Agent Type**: general-purpose
- **Parallel**: false
- In `models.py` `ChartDef`: add `groups: list[GroupDef]` field (required for multi-chart, see below for legacy)
- In `models.py` `BenchmarkConfig`: remove `groups` from the class fields
- BUT keep `groups` as an optional field on `BenchmarkConfig` for the **legacy single-chart form only** — the validator `_normalize_chart_form` needs to read it to synthesize the default ChartDef
- Update `_normalize_chart_form`: when synthesizing the default ChartDef from legacy fields, include `groups=self.groups` in the synthesized chart
- Update `all_charts()`: the synthesized default ChartDef now carries its own groups
- For the multi-chart form: `BenchmarkConfig.groups` should be None/empty — groups live on each chart
- Add a helper `all_groups()` on `BenchmarkConfig` that collects unique groups across all charts (needed by `list_benchmarks` for total count)
- Update `__all__` if needed

### 2. Backend — Update store.py and http_ingest.py
- **Task ID**: backend-store-ingest
- **Depends On**: backend-models
- **Assigned To**: builder-backend
- **Agent Type**: general-purpose
- **Parallel**: false
- `http_ingest.py` line 61-64: currently builds `group_keys` and `group_canon` from `cfg.groups`. Change to build **per-chart** group lookups: `group_keys_by_chart = {cid: {g.key for g in chart.groups} for cid, chart in charts_by_id.items()}` and `group_canon_by_chart` similarly. Validation for points uses `group_keys_by_chart[p.chart_id]`. Validation for completions and metadata uses the same per-chart lookup.
- `store.py` `dataset_states()` line 437: change `for group in cfg.groups` to `for group in chart.groups` (already iterating charts on line 435)
- `store.py` `list_benchmarks()` line 130: change `total = len(cfg.groups)` to count unique groups across all charts, e.g. `total = len(set(g.key for c in charts for g in c.groups))`

### 3. Backend — Update tests and fixtures
- **Task ID**: backend-tests
- **Depends On**: backend-store-ingest
- **Assigned To**: builder-backend
- **Agent Type**: general-purpose
- **Parallel**: false
- `conftest.py` `build_sample_config()`: This uses the legacy single-chart form with `groups=[...]` at config level. Keep this as-is — the validator should still accept legacy form and synthesize groups into the default chart. Verify it works.
- `test_store.py` `_build_multichart_config()`: Move `groups` from `BenchmarkConfig` into each `ChartDef`. Each chart gets `groups=[GroupDef(key="faiss",...), GroupDef(key="qdrant",...)]`.
- `fixtures_export.py`: Move groups from `BenchmarkConfig` constructor into each `ChartDef`. The `BenchmarkConfig` no longer has groups for multi-chart form. Re-export fixtures: `cd apps/backend && uv run python tests/fixtures_export.py`
- Run `just test-backend` to verify

### 4. Frontend — Update Zod schemas
- **Task ID**: frontend-schemas
- **Depends On**: backend-tests (need re-exported fixtures)
- **Assigned To**: builder-frontend
- **Agent Type**: general-purpose
- **Parallel**: false
- `schemas.ts` `ChartDefSchema`: add `groups: z.array(GroupDefSchema).optional()` (optional because legacy synthesized charts get groups added by `allCharts()`)
- `schemas.ts` `BenchmarkConfigSchema`: change `groups` to optional: `groups: z.array(GroupDefSchema).optional()`
- `schemas.ts` `allCharts()`: when synthesizing the default chart from legacy fields, include `groups: config.groups` in the returned ChartDef
- Update type exports if needed
- `schemas.test.ts`: update the legacy config fixture — `groups` stays at config level (legacy form). Multi-chart fixture: groups move to chart level. Update assertions.

### 5. Frontend — Update BenchmarkPage.vue
- **Task ID**: frontend-page
- **Depends On**: frontend-schemas
- **Assigned To**: builder-frontend
- **Agent Type**: general-purpose
- **Parallel**: false
- Line 135: change `:groups="session.config.groups"` to `:groups="chart.groups"` — but `chart` is the loop variable from `v-for="chart in charts"`, and `charts` comes from `allCharts(session.config)` which now includes groups on each chart
- Line 152 (PromptModal): change `:groups="session.config.groups"` to pass groups from the active chart. Need to look up the chart for `activeModal.chartId` and use its groups.
- Line 91: `session.config.groups.find(...)` — change to look up groups from the active chart
- Add computed: `activeChartGroups` that finds the chart matching `activeModal.chartId` and returns its `groups`

### 6. Update YAMLs with per-chart groups
- **Task ID**: update-yamls
- **Depends On**: frontend-page
- **Assigned To**: builder-yaml-bench
- **Agent Type**: general-purpose
- **Parallel**: false
- `benchmarks/qwen35-vs-gemma4.yaml`: remove top-level `groups`. Add `groups:` block to each of the 6 existing charts (copy the 5 prompt groups into each). Then add 2 new memory charts:
  ```yaml
  - chart_id: memory_m4
    title: "Memory (M4 Max)"
    subtitle: "system RAM consumed during inference · lower is better"
    better: lower
    direction: BT
    x: { label: "Model" }
    y: { label: "Memory", unit: "GB", min: 0 }
    groups:
      - { key: qwen_gguf,  label: "Qwen 3.5 GGUF",  icon: "/icons/alibaba.svg" }
      - { key: qwen_mlx,   label: "Qwen 3.5 MLX",   icon: "/icons/alibaba.svg" }
      - { key: gemma4_gguf, label: "Gemma 4 GGUF",   icon: "/icons/google.svg"  }
      - { key: gemma4_mlx,  label: "Gemma 4 MLX",    icon: "/icons/google.svg"  }
    metrics:
      - { key: memory_gb, label: "Peak RAM", color: ["#a855f7", "#c084fc"] }
  - chart_id: memory_m5
    # same structure for M5
  ```
- `benchmarks/mock-test.yaml`: move groups into the chart definition
- Verify YAML loads: start backend, `live-bench list`

### 7. Benchmark script — add memory measurement
- **Task ID**: bench-memory
- **Depends On**: update-yamls
- **Assigned To**: builder-yaml-bench
- **Agent Type**: general-purpose
- **Parallel**: false
- Update `bench.py` script metadata to add `psutil`: `dependencies = ["httpx>=0.27", "psutil>=5.9"]`
- Add memory measurement function using system RAM delta (same as `memory_test.py`):
  - `measure_memory_delta(before_available)` returns GB consumed
  - Before each backend warmup: record `psutil.virtual_memory().available`
  - After warmup (model loaded): compute delta
  - Emit to `memory_m4`/`memory_m5` chart: `live-bench emit qwen35-vs-gemma4 --chart memory_{hw} --group {metric_key} --metric memory_gb --value {delta_gb}`
- Unload previous Ollama model before measuring next one (so baseline is clean): `ollama stop {prev_model}`
- For MLX: measure after MLXRunner boots (model loaded) before running prompts
- Memory is emitted once per backend, not per prompt

### 8. Validation
- **Task ID**: validate-all
- **Depends On**: bench-memory
- **Assigned To**: validator
- **Agent Type**: general-purpose
- **Parallel**: false
- `just test` — all backend + CLI + frontend tests pass
- `just mock` — mock-test works with per-chart groups
- Boot platform, navigate to qwen35-vs-gemma4 benchmark page
- Verify 8 chart cards render (6 existing + 2 memory)
- Verify memory charts have model-based groups (Qwen 3.5 GGUF, etc.) while speed charts have prompt groups (P1-P5)
- Emit test data to a memory chart: `live-bench emit qwen35-vs-gemma4 --chart memory_m4 --group qwen_gguf --metric memory_gb --value 24.7`
- Verify the bar appears on the memory chart

## Acceptance Criteria

1. `ChartDef` has `groups: list[GroupDef]` — every chart is self-contained
2. `BenchmarkConfig.groups` only used in legacy single-chart form (optional, feeds into synthesized default chart)
3. Multi-chart YAMLs declare groups per chart — no benchmark-level groups
4. Speed charts (prefill/decode/wall) have prompt groups (P1-P5)
5. Memory charts (memory_m4/m5) have model groups with icons
6. Ingest validation checks groups per chart, not globally
7. Dataset states computed per chart's own groups
8. `just test` passes — all 107+ tests green
9. `just mock` works with updated mock-test.yaml
10. Memory charts render on the benchmark page alongside speed charts
11. Benchmark script emits memory measurements via system RAM delta

## Validation Commands

- `just test` — all tests pass
- `just mock` — mock benchmark works with per-chart groups
- `cd apps/backend && uv run python tests/fixtures_export.py` — fixtures re-exported
- `live-bench list` — shows qwen35-vs-gemma4 with 8 charts
- `live-bench emit qwen35-vs-gemma4 --chart memory_m4 --group qwen_gguf --metric memory_gb --value 24.7` — emits to memory chart
- Playwright: verify 8 chart cards on benchmark page

## Notes

### Legacy Single-Chart Form

The legacy form (`BenchmarkConfig` with top-level `better/x/y/metrics/groups` and no `charts` list) must continue to work. The `_normalize_chart_form` validator synthesizes a single `ChartDef` with `chart_id="default"` from these fields — it now also passes `groups` through to the synthesized chart.

### Memory Measurement

Uses `psutil.virtual_memory().available` delta — same technique as `apps/benchmarks/memory_test.py`. Measures once per backend after warmup, not per prompt. The system-wide delta captures all memory types (CPU, Metal/GPU, mmap'd) regardless of backend.

### Group Deduplication in list_benchmarks

`list_benchmarks()` currently shows `total_count = len(cfg.groups)`. With per-chart groups, charts may have different groups. The total should represent the number of unique group-chart pairs for completion tracking. Simplest: sum `len(chart.groups)` across all charts.

### psutil Dependency

`bench.py` needs `psutil` — add to the `# /// script` metadata: `dependencies = ["httpx>=0.27", "psutil>=5.9"]`. No changes to the backend or CLI packages.

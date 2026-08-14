# Plan: Qwen 3.6 Trio Benchmarks (Qwen 3.5 vs Qwen 3.6 vs Gemma 4)

## Task Description

Qwen 3.6 (35B-A3B) just shipped on Ollama with direct analogues to every Qwen 3.5 variant we already benchmark. We want to mirror our 3 real benchmarks — `qwen35-vs-gemma4`, `context-scaling`, `pi-coding-agent` — with a new sibling set that pits **Qwen 3.5 35B-A3B**, **Qwen 3.6 35B-A3B**, and **Gemma 4 26B-A4B** against each other on the same M4 Max / M5 Max hardware matrix.

We do NOT modify the existing three benchmarks. They stay as-is as the "2-gen-gap" story. The new three are sibling sessions with their own YAML, their own `apps/benchmarks/<session>/bench.py`, and their own `just` recipes.

Qwen 3.6 variants matched to our existing Qwen 3.5 variants (from <https://ollama.com/library/qwen3.6>):

| Our existing Qwen 3.5 tag          | Size  | New Qwen 3.6 equivalent           | Size  |
| ---------------------------------- | ----- | --------------------------------- | ----- |
| `qwen3.5:35b` (GGUF default)       | 24 GB | `qwen3.6:35b-a3b` (GGUF default)  | 24 GB |
| `qwen3.5:35b-a3b-nvfp4` (MLX-Ollama) | ~22 GB | `qwen3.6:35b-a3b-nvfp4` (MLX-Ollama) | 22 GB |

Both are 35B-A3B, both hit the 256K context window on 3.6, both go through the existing Ollama transport — no new subprocess runner, no new `.mlx-venv`. The only prerequisite is `ollama pull qwen3.6:35b-a3b` + `ollama pull qwen3.6:35b-a3b-nvfp4` on each bench machine.

## Objective

When complete:

1. Three new YAMLs under `benchmarks/`:
   - `benchmarks/qwen36-vs-qwen35-vs-gemma4.yaml` — 6-way raw inference (prefill / decode / wall / memory × M4/M5 = 8 charts)
   - `benchmarks/context-scaling-3way.yaml` — 3-way context scaling (prefill / decode / wall / accuracy × M4/M5 = 8 charts)
   - `benchmarks/pi-coding-agent-3way.yaml` — 5-way coding agent (wall / score / tokens / tools × M4/M5 = 8 charts)
2. Three new benchmark runners under `apps/benchmarks/`:
   - `apps/benchmarks/qwen36-vs-qwen35-vs-gemma4/`
   - `apps/benchmarks/context-scaling-3way/`
   - `apps/benchmarks/pi-coding-agent-3way/`
   Each is a fork of its namesake without the `-3way` / `qwen36-` prefix, with Qwen 3.6 added as a first-class backend.
3. `justfile` recipes for each new benchmark: `bench-qg3-*`, `bench-ctx3-*`, `bench-pi3-*` and a `-reset` variant each, all hooked into `bench-nuke`.
4. `README.md` and `just reset-all` updated to include the three new sessions.
5. `just serve` lists all six benchmarks on the landing page; a smoke run on one fresh machine fills bars in each new benchmark via the UI.

## Problem Statement

The existing qwen3.5-vs-gemma4 benchmarks answer "GGUF vs MLX" and "Qwen vs Gemma". They do not answer the question everyone will ask the moment Qwen 3.6 drops: **does the new generation actually win, and by how much, across the same workload matrix?** We need a sibling set of benchmarks so presenters can switch between "old model cohort" and "new model cohort" on camera without editing YAML mid-stream, and so both datasets live side-by-side on the dashboard.

## Solution Approach

Fork the three existing benchmark directories verbatim and extend each with Qwen 3.6 backends. The YAML schema already supports per-metric icons and colors, so the only deltas are:

- **New session IDs** (new DB rows, isolated from existing data).
- **New metric keys** (`qwen35_gguf` / `qwen35_mlx` / `qwen36_gguf` / `qwen36_mlx` / `gemma4_gguf` / `gemma4_mlx`). Qwen 3.5 gets renamed from `qwen_*` → `qwen35_*` for disambiguation.
- **New backend entries** in each `bench.py`'s model/backend list.
- **Distinct Qwen 3.6 colors** so the old and new generations are visually separable on camera. Proposed palette:
  - Qwen 3.5 GGUF `#f59e0b` / MLX `#fbbf24` (amber — unchanged)
  - **Qwen 3.6 GGUF `#ef4444` / MLX `#f87171` (red) — new**
  - Gemma 4 GGUF `#3b82f6` / MLX `#60a5fa` (blue — unchanged)
- **Memory chart (benchmark 1 only) grows from 4 → 6 bars.** Same shape.

Everything else (CompletionTracker wiring, meta emits, warm-isolated harness, MLX subprocess for Gemma 4 in benchmarks 1 and 2, Ollama transport for every Qwen variant) is unchanged.

## Relevant Files

Use these files to complete the task:

### Reference — existing benchmark YAMLs (copy + extend)
- `benchmarks/qwen35-vs-gemma4.yaml` — 8-chart template with anchors for `&prompt_groups`, `&model_metrics`, `&model_groups`. Target color scheme proven on camera.
- `benchmarks/context-scaling.yaml` — 8-chart template with `&ctx_groups`, `&model_metrics`. 2-model simplicity.
- `benchmarks/pi-coding-agent.yaml` — 8-chart template with `&task_groups`, `&model_metrics`. 3-model shape (incl. GGUF-only Gemma 4).

### Reference — existing benchmark runners (copy + extend)
- `apps/benchmarks/qwen35-vs-gemma4/bench.py` — 6-way expansion target. `OLLAMA_BACKENDS` + `GEMMA4_MLX` + `CompletionTracker(NUM_METRICS)` all need edits.
- `apps/benchmarks/qwen35-vs-gemma4/_harness.py` — unchanged logic; the new `bench.py` imports the same module.
- `apps/benchmarks/qwen35-vs-gemma4/_mlx_runner.py` — unchanged; used by Gemma 4 MLX only.
- `apps/benchmarks/context-scaling/bench.py` — 3-way expansion target. `OLLAMA_BACKEND` (single dict) becomes `OLLAMA_BACKENDS` (list of two dicts).
- `apps/benchmarks/context-scaling/fixtures.json` — copy into new dir unchanged.
- `apps/benchmarks/pi-coding-agent/bench.py` — 5-way expansion target. `MODELS` list grows to include both Qwen 3.6 variants.
- `apps/benchmarks/pi-coding-agent/_pi_runner.py`, `_tasks.py`, `fixtures/` — unchanged; copy verbatim.
- `apps/benchmarks/pi-coding-agent/run_all.py` — copy + rename session reference only.

### Reference — platform contract
- `apps/backend/src/live_bench_server/config.py` — YAML loader (multi-benchmark-per-file supported; single-benchmark is fine for our case).
- `apps/backend/src/live_bench_server/models.py` — `BenchmarkConfig`, `ChartDef`, `MetricDef`, `GroupDef`, tag/icon fields.
- `apps/cli/src/live_bench_cli/commands/emit_cmd.py` + `meta_cmd.py` + `complete_cmd.py` — emit protocol the bench scripts already speak.
- `justfile` — existing `bench-qg-*`, `bench-ctx-*`, `bench-pi-*`, `bench-nuke`, `reset-all` recipes are the template for the new trio.
- `README.md` — existing "qwen35-vs-gemma4 (live inference benchmark)" section is the pattern for the new documentation blocks.

### New Files
- `benchmarks/qwen36-vs-qwen35-vs-gemma4.yaml`
- `benchmarks/context-scaling-3way.yaml`
- `benchmarks/pi-coding-agent-3way.yaml`
- `apps/benchmarks/qwen36-vs-qwen35-vs-gemma4/bench.py`
- `apps/benchmarks/qwen36-vs-qwen35-vs-gemma4/_harness.py` (copy)
- `apps/benchmarks/qwen36-vs-qwen35-vs-gemma4/_mlx_runner.py` (copy)
- `apps/benchmarks/qwen36-vs-qwen35-vs-gemma4/run_all.py` (copy + rename session)
- `apps/benchmarks/context-scaling-3way/bench.py`
- `apps/benchmarks/context-scaling-3way/_harness.py` (copy)
- `apps/benchmarks/context-scaling-3way/_mlx_runner.py` (copy)
- `apps/benchmarks/context-scaling-3way/fixtures.json` (copy)
- `apps/benchmarks/context-scaling-3way/extract_fixtures.py` (copy — defensive)
- `apps/benchmarks/pi-coding-agent-3way/bench.py`
- `apps/benchmarks/pi-coding-agent-3way/_pi_runner.py` (copy)
- `apps/benchmarks/pi-coding-agent-3way/_tasks.py` (copy)
- `apps/benchmarks/pi-coding-agent-3way/fixtures/` (copy recursively)
- `apps/benchmarks/pi-coding-agent-3way/run_all.py` (copy + rename session)

## Implementation Phases

### Phase 1: Foundation

Lock the YAML shape and the session-ID / metric-key conventions before anyone writes runner code. If the YAMLs are wrong, the runners emit into sessions that don't exist.

- Session IDs: `qwen36-vs-qwen35-vs-gemma4`, `context-scaling-3way`, `pi-coding-agent-3way`.
- Metric keys: `qwen35_gguf`, `qwen35_mlx`, `qwen36_gguf`, `qwen36_mlx`, `gemma4_gguf`, `gemma4_mlx` (per-benchmark subset where not all apply — see tables below).
- Chart IDs unchanged from the parents: `prefill_m4|m5`, `decode_m4|m5`, `wall_m4|m5`, plus benchmark-specific (`memory_*`, `accuracy_*`, `score_*`, `tokens_*`, `tools_*`).
- Backend starts cold-loading from the new YAMLs after Phase 1 lands, even before runners exist — the UI will show empty bars in the correct shape, which is itself a validation signal.

Per-benchmark metric layouts:

**qwen36-vs-qwen35-vs-gemma4.yaml** — 6 metrics (bars per prompt):
```
qwen35_gguf  → qwen3.5:35b
qwen35_mlx   → qwen3.5:35b-a3b-nvfp4
qwen36_gguf  → qwen3.6:35b-a3b         ← NEW
qwen36_mlx   → qwen3.6:35b-a3b-nvfp4   ← NEW
gemma4_gguf  → gemma4:26b
gemma4_mlx   → mlx-community/gemma-4-26b-a4b-it-4bit (mlx-vlm)
```

**context-scaling-3way.yaml** — 3 metrics (MLX-only):
```
qwen35_mlx   → qwen3.5:35b-a3b-nvfp4
qwen36_mlx   → qwen3.6:35b-a3b-nvfp4   ← NEW
gemma4_mlx   → mlx-community/gemma-4-26b-a4b-it-4bit (mlx-vlm)
```

**pi-coding-agent-3way.yaml** — 5 metrics (GGUF Gemma 4 only, matching parent):
```
qwen35_gguf  → qwen3.5:35b
qwen35_mlx   → qwen3.5:35b-a3b-nvfp4
qwen36_gguf  → qwen3.6:35b-a3b         ← NEW
qwen36_mlx   → qwen3.6:35b-a3b-nvfp4   ← NEW
gemma4_gguf  → gemma4:26b
```

### Phase 2: Core Implementation

Three independent runner ports, one per benchmark. Each port is ~30 lines of delta against the parent: extend the `OLLAMA_BACKENDS` / `MODELS` list with the two new Qwen 3.6 entries (one in context-scaling-3way since it's MLX-only), rename `qwen_*` → `qwen35_*`, bump `NUM_METRICS`, change the `SESSION` constant. The CompletionTracker is data-driven off the metric count so no further edits needed.

Justfile recipes mirror the existing ones, namespaced with `qg3` / `ctx3` / `pi3`:
```
bench-qg3-m4 / bench-qg3-m5 / bench-qg3-smoke-m4 / bench-qg3-smoke-m5 / bench-qg3-reset
bench-ctx3-m4 / bench-ctx3-m5 / bench-ctx3-smoke-m4 / bench-ctx3-smoke-m5 / bench-ctx3-reset
bench-pi3-m4 / bench-pi3-m5 / bench-pi3-smoke-m4 / bench-pi3-smoke-m5 / bench-pi3-reset
```
`reset-all` gains the three new `-reset` recipes. `bench-nuke` gains `ollama stop qwen3.6:35b-a3b` and `ollama stop qwen3.6:35b-a3b-nvfp4`.

### Phase 3: Integration & Polish

- README: add a "qwen36-vs-qwen35-vs-gemma4", "context-scaling-3way", "pi-coding-agent-3way" section mirroring the existing "qwen35-vs-gemma4" block. Call out the `ollama pull qwen3.6:35b-a3b` + `ollama pull qwen3.6:35b-a3b-nvfp4` prerequisite.
- `.env.sample` does not need changes (same `LIVE_BENCH_SERVER`).
- Smoke validation: `just serve` + `just bench-qg3-smoke-m4` (whichever machine the validator sits on). Open the dashboard, confirm 6 bars animate in prefill_m4 for prompt P1 across all three model families.
- Playwright smoke: script navigates to `/benchmark/qwen36-vs-qwen35-vs-gemma4`, asserts 6 metric legends render with the expected colors and icons.

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
  - Name: builder-yaml
  - Role: Author the three new benchmark YAML files. Lock the session IDs, chart IDs, metric keys, groups, tags, and the Qwen 3.6 color palette so every downstream runner has a stable contract.
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-bench-raw
  - Role: Fork `apps/benchmarks/qwen35-vs-gemma4/` into `apps/benchmarks/qwen36-vs-qwen35-vs-gemma4/` and extend the runner to 6 backends (2 Qwen 3.5 + 2 Qwen 3.6 + 2 Gemma 4). Includes the memory chart's 6-bar variant.
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-bench-ctx
  - Role: Fork `apps/benchmarks/context-scaling/` into `apps/benchmarks/context-scaling-3way/` and extend the runner to 3 MLX backends (Qwen 3.5 MLX + Qwen 3.6 MLX + Gemma 4 MLX). Fixture file is copied verbatim.
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-bench-pi
  - Role: Fork `apps/benchmarks/pi-coding-agent/` into `apps/benchmarks/pi-coding-agent-3way/` and extend the runner to 5 models (Qwen 3.5 GGUF/MLX + Qwen 3.6 GGUF/MLX + Gemma 4 GGUF). Task fixtures are copied verbatim.
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-justfile-readme
  - Role: Add 15 new justfile recipes (`bench-qg3-*`, `bench-ctx3-*`, `bench-pi3-*`), extend `bench-nuke` to stop the two new Qwen 3.6 Ollama models, add the three new sessions to `reset-all`, and add README sections for each new benchmark + the `ollama pull` prerequisite.
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: validator
  - Role: Smoke-test the backend loads all three new YAMLs, confirm the landing page lists them, run one `--smoke-m4` for each and assert bars animate in the UI via a Playwright script. Report any missing icon / color / metric-key drift.
  - Agent Type: playwright-bowser-agent
  - Resume: true

## Step by Step Tasks

- IMPORTANT: Execute every step in order, top to bottom. Each task maps directly to a `TaskCreate` call.
- Before you start, run `TaskCreate` to create the initial task list that all team members can see and execute.

### 1. Author the three benchmark YAMLs
- **Task ID**: create-yamls
- **Depends On**: none
- **Assigned To**: builder-yaml
- **Agent Type**: general-purpose
- **Parallel**: false
- Copy `benchmarks/qwen35-vs-gemma4.yaml` → `benchmarks/qwen36-vs-qwen35-vs-gemma4.yaml`. Change `session_id` to `qwen36-vs-qwen35-vs-gemma4`. Update `title` to `"Qwen 3.6 vs Qwen 3.5 vs Gemma 4 — Raw Inference"`. Update `subtitle` to `"Qwen 3.6 35B-A3B vs Qwen 3.5 35B-A3B vs Gemma 4 26B-A4B · GGUF vs MLX · M4 Max vs M5 Max"`. Rename `tags` to include Qwen 3.6 GGUF + MLX entries (same `/icons/alibaba.svg`). Rename metric keys `qwen_gguf` → `qwen35_gguf`, `qwen_mlx` → `qwen35_mlx`; add `qwen36_gguf` (color `#ef4444`) and `qwen36_mlx` (color `#f87171`) to `&model_metrics`. Memory `&model_groups` gets the same 6 entries.
- Copy `benchmarks/context-scaling.yaml` → `benchmarks/context-scaling-3way.yaml`. Change `session_id` to `context-scaling-3way`. Title becomes `"Context Scaling (3-way) — GraphWalks"`. Subtitle mentions Qwen 3.6 alongside 3.5 + Gemma 4. Rename `qwen_mlx` → `qwen35_mlx`, add `qwen36_mlx` with color `#f87171` and `/icons/alibaba.svg`. Tags list grows by one.
- Copy `benchmarks/pi-coding-agent.yaml` → `benchmarks/pi-coding-agent-3way.yaml`. Change `session_id` to `pi-coding-agent-3way`. Title becomes `"Pi Coding Agent (3-way) — Task Completion"`. Subtitle mentions Qwen 3.6. Rename `qwen_gguf` → `qwen35_gguf`, `qwen_mlx` → `qwen35_mlx`; add `qwen36_gguf` (`#ef4444`) and `qwen36_mlx` (`#f87171`). Keep only `gemma4_gguf` on Gemma side (matching parent).
- Validate each YAML parses with `uv run python -c "from live_bench_server.config import load_benchmarks_dir; load_benchmarks_dir('benchmarks')"` from `apps/backend`.

### 2. Fork raw-inference runner to 6-way
- **Task ID**: port-raw-bench
- **Depends On**: create-yamls
- **Assigned To**: builder-bench-raw
- **Agent Type**: general-purpose
- **Parallel**: true
- Copy `apps/benchmarks/qwen35-vs-gemma4/` → `apps/benchmarks/qwen36-vs-qwen35-vs-gemma4/`. `_harness.py`, `_mlx_runner.py`, `run_all.py` are unchanged beyond session/dir references.
- In `bench.py`: change `SESSION = "qwen36-vs-qwen35-vs-gemma4"`. Rename the `qwen_*` keys in `OLLAMA_BACKENDS` to `qwen35_*`. Insert two new entries into `OLLAMA_BACKENDS` between the Qwen 3.5 MLX and Gemma 4 GGUF lines: `{"metric": "qwen36_gguf", "model": "qwen3.6:35b-a3b", "label": "Qwen 3.6 (GGUF)"}` and `{"metric": "qwen36_mlx", "model": "qwen3.6:35b-a3b-nvfp4", "label": "Qwen 3.6 (MLX)"}`.
- `ALL_METRICS` now has 6 entries; `NUM_METRICS = 6`. `CompletionTracker` is data-driven, no further code changes.
- Memory emits still fire per backend via `emit_memory()`; because `memory_*` charts now have 6 groups, confirm the YAML `&model_groups` block lists all six metric keys as group keys (this is the existing pattern — group key == metric key on the memory chart).
- Smoke: `uv run apps/benchmarks/qwen36-vs-qwen35-vs-gemma4/bench.py --hw m4 --smoke` runs one prompt across all 6 backends and emits valid payloads to a local backend.

### 3. Fork context-scaling runner to 3-way
- **Task ID**: port-ctx-bench
- **Depends On**: create-yamls
- **Assigned To**: builder-bench-ctx
- **Agent Type**: general-purpose
- **Parallel**: true
- Copy `apps/benchmarks/context-scaling/` → `apps/benchmarks/context-scaling-3way/`. `_harness.py`, `_mlx_runner.py`, `fixtures.json`, `extract_fixtures.py` unchanged.
- In `bench.py`: change `SESSION = "context-scaling-3way"`. Convert `OLLAMA_BACKEND` (single dict) to `OLLAMA_BACKENDS` (list). Entries: `{"metric": "qwen35_mlx", "model": "qwen3.5:35b-a3b-nvfp4", "label": "Qwen 3.5 (MLX via Ollama)"}` and `{"metric": "qwen36_mlx", "model": "qwen3.6:35b-a3b-nvfp4", "label": "Qwen 3.6 (MLX via Ollama)"}`.
- Update the Ollama bench loop to iterate `OLLAMA_BACKENDS`, unloading the previous Ollama model between backends with `ollama stop` (match the pattern used in `qwen35-vs-gemma4/bench.py` lines 171-173).
- `ALL_METRICS = ["qwen35_mlx", "qwen36_mlx", "gemma4_mlx"]`; `NUM_METRICS = 3`.
- Smoke: `uv run apps/benchmarks/context-scaling-3way/bench.py --hw m4 --smoke` runs a single context size across all 3 backends and emits valid prefill/decode/wall/accuracy payloads.

### 4. Fork pi-coding-agent runner to 5-way
- **Task ID**: port-pi-bench
- **Depends On**: create-yamls
- **Assigned To**: builder-bench-pi
- **Agent Type**: general-purpose
- **Parallel**: true
- Copy `apps/benchmarks/pi-coding-agent/` → `apps/benchmarks/pi-coding-agent-3way/`. `_pi_runner.py`, `_tasks.py`, `fixtures/` unchanged; `run_all.py` has session references updated.
- In `bench.py`: change `SESSION = "pi-coding-agent-3way"`. Rename `MODELS` keys `qwen_*` → `qwen35_*`. Add two new entries: `{"metric": "qwen36_gguf", "model": "qwen3.6:35b-a3b", "label": "Qwen 3.6 GGUF", "provider": "ollama"}` and `{"metric": "qwen36_mlx", "model": "qwen3.6:35b-a3b-nvfp4", "label": "Qwen 3.6 MLX", "provider": "ollama"}` between the Qwen 3.5 MLX and Gemma 4 GGUF entries.
- `NUM_MODELS = 5`; CompletionTracker tolerates that via the metric-count data driver.
- Smoke: `uv run apps/benchmarks/pi-coding-agent-3way/bench.py --hw m4 --smoke` exercises one task across all 5 models.

### 5. Justfile + README integration
- **Task ID**: justfile-readme
- **Depends On**: port-raw-bench, port-ctx-bench, port-pi-bench
- **Assigned To**: builder-justfile-readme
- **Agent Type**: general-purpose
- **Parallel**: false
- Add to `justfile`:
  - `bench-qg3-m4 *FLAGS: bench-nuke` → `uv run apps/benchmarks/qwen36-vs-qwen35-vs-gemma4/bench.py --hw m4 {{FLAGS}}` (and `-m5`, `-smoke-m4`, `-smoke-m5`, `-reset`).
  - Same shape for `bench-ctx3-*` and `bench-pi3-*`.
  - Extend `bench-nuke` with `ollama stop qwen3.6:35b-a3b 2>/dev/null || true` and `ollama stop qwen3.6:35b-a3b-nvfp4 2>/dev/null || true`.
  - Extend `reset-all: mock-reset bench-qg-reset bench-ctx-reset bench-pi-reset` to add `bench-qg3-reset bench-ctx3-reset bench-pi3-reset`.
- Update `README.md`:
  - Under "CLI commands" add a new section `qwen36-vs-qwen35-vs-gemma4 (6-way live inference benchmark)` with the same table style as the existing `qwen35-vs-gemma4` section.
  - Add matching sections for `context-scaling-3way` and `pi-coding-agent-3way`.
  - Add a "Prerequisites (benchmark machine)" bullet listing `ollama pull qwen3.6:35b-a3b` and `ollama pull qwen3.6:35b-a3b-nvfp4`.
- Sanity: `just --list` shows the 15 new recipes.

### 6. End-to-end validation
- **Task ID**: validate-all
- **Depends On**: create-yamls, port-raw-bench, port-ctx-bench, port-pi-bench, justfile-readme
- **Assigned To**: validator
- **Agent Type**: playwright-bowser-agent
- **Parallel**: false
- `just test` passes (backend pytest, cli pytest, frontend vitest) — no existing tests should regress.
- Boot `just serve`. Hit `GET http://127.0.0.1:8787/benchmarks` and confirm the JSON lists all three new `session_id` values alongside the existing ones.
- Open `http://127.0.0.1:5787/` in Playwright, assert the landing page shows six benchmark cards (three existing + three new) with correct titles and icon tags.
- Navigate to `/benchmark/qwen36-vs-qwen35-vs-gemma4`, assert the 6-metric legend renders with the expected colors (`#f59e0b`, `#fbbf24`, `#ef4444`, `#f87171`, `#3b82f6`, `#60a5fa`) and Alibaba/Google icons in the right rows.
- Navigate to `/benchmark/context-scaling-3way`, assert the 3-metric legend and 8 context-size groups render correctly.
- Navigate to `/benchmark/pi-coding-agent-3way`, assert the 5-metric legend and 6 task groups render correctly.
- Optional deep smoke (any one machine with Ollama + both Qwen 3.6 tags pulled): `just bench-qg3-smoke-m4` → open the benchmark page mid-run → assert at least one bar animates for each of `qwen35_gguf`, `qwen36_gguf`, `qwen36_mlx`.
- Produce a short markdown report with screenshots of each new benchmark page and any drift findings.

## Acceptance Criteria

- `benchmarks/qwen36-vs-qwen35-vs-gemma4.yaml`, `benchmarks/context-scaling-3way.yaml`, `benchmarks/pi-coding-agent-3way.yaml` all exist and validate under `BenchmarkFile` on backend boot.
- The backend boots clean (no YAML errors in the log) and `GET /benchmarks` returns six sessions.
- The landing page lists all six benchmarks with correct titles, subtitles, and tag icons.
- Each new benchmark page renders the expected number of metrics (6 / 3 / 5) with the declared colors and icon mappings.
- `bench.py` smoke runs (`--hw m4 --smoke`) for each new benchmark succeed against a local backend and produce animated bars in the UI.
- `justfile` exposes `bench-qg3-*`, `bench-ctx3-*`, `bench-pi3-*` (5 recipes each × 3 = 15) and `bench-nuke` / `reset-all` cover the new sessions.
- `README.md` documents the three new benchmarks + the `ollama pull qwen3.6:35b-a3b` + `ollama pull qwen3.6:35b-a3b-nvfp4` prerequisite.
- No regression in `just test` (backend + cli + frontend test suites).
- Existing `qwen35-vs-gemma4`, `context-scaling`, `pi-coding-agent` YAMLs and runners are untouched.

## Validation Commands

Execute these commands to validate the task is complete:

- `just test` — backend pytest + cli pytest + frontend vitest must all pass.
- `cd apps/backend && uv run python -c "from live_bench_server.config import load_benchmarks_dir; from pathlib import Path; print([c.session_id for p, _ in load_benchmarks_dir(Path('../../benchmarks')) for c in p.all_benchmarks()])"` — must include `qwen36-vs-qwen35-vs-gemma4`, `context-scaling-3way`, `pi-coding-agent-3way`.
- `just --list | grep -E 'bench-(qg3|ctx3|pi3)'` — must list 15 new recipes.
- `just serve` + `curl -s http://127.0.0.1:8787/benchmarks | jq -r '.benchmarks[].session_id' | sort` — must include all six sessions.
- `just bench-qg3-smoke-m4` (on a machine with Ollama and the two Qwen 3.6 tags pulled) — must run to completion and emit 6 metrics for prompt P1.
- `just bench-ctx3-smoke-m4` — must run to completion and emit 3 metrics for `ctx_200`.
- `just bench-pi3-smoke-m4` — must run to completion and emit 5 metrics for task T1.
- Playwright script navigates to each of the three new benchmark pages and asserts metric count + legend colors match the YAML.

## Notes

- **Prerequisite (bench machine only):** `ollama pull qwen3.6:35b-a3b && ollama pull qwen3.6:35b-a3b-nvfp4` — document in README. The server/frontend machines don't need this.
- **No new Python deps.** Runners reuse the existing `_harness.py` / `_mlx_runner.py` / `_pi_runner.py` modules verbatim; Qwen 3.6 goes over the same Ollama HTTP transport as Qwen 3.5.
- **No frontend code changes.** The chart engine already supports arbitrary metric counts; the 6-bar memory chart is the widest we'll go.
- **Color choice for Qwen 3.6** (`#ef4444` / `#f87171`, red family) is proposed to keep the generations visually distinct; builder-yaml may swap to any hue that isn't already claimed by amber (Qwen 3.5) or blue (Gemma 4). Keep the two stops 1 luminance step apart, matching the existing pattern.
- **Session-ID choice** avoids `-v2` to keep the history readable at a glance — `-3way` and `qwen36-` prefix both say what they mean.
- **Outbox compatibility.** Nothing about the CLI outbox or the ingest wire changes.
- **Future cleanup path:** if Qwen 3.6 fully replaces Qwen 3.5, the existing `qwen35-vs-gemma4` YAMLs and runners can be deleted without touching the `-3way` siblings.

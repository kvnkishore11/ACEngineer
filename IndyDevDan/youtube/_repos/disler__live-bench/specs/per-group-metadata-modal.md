# Plan: Per-Group Metadata with Clickable Prompt/Response Modal

## Task Description

Add a per-group metadata system to live-bench so benchmark scripts can emit arbitrary key-value data (prompt text, model responses) alongside numeric datapoints. The frontend displays this in a modal when the user clicks a group label on the chart, showing the prompt and each model's response side by side.

## Objective

When complete:
1. Benchmark scripts can emit metadata (prompt text + response text) per `(chart_id, group_key)` via the CLI
2. Backend stores metadata in SQLite, merges on upsert, streams via SSE, serves via REST
3. Frontend stores metadata in the session store and updates live
4. Clicking an x-axis group label (e.g., "P1 factual") opens a modal showing the prompt and all model responses
5. The modal populates incrementally — responses appear as each backend completes

## Problem Statement

The current data model only supports numeric values per `(chart_id, group_key, metric_key)`. During a live presentation, the audience sees bars animate but has no way to see *what* was asked or *how* each model responded. Adding per-group metadata enables a drill-down into the qualitative output behind each numeric result.

## Solution Approach

Add a `metadata` table to SQLite keyed by `(session_id, chart_id, group_key)` storing a JSON blob. The ingest pipeline accepts optional `metadata` entries alongside datapoints, merges them into the existing blob (so responses accumulate as backends complete), and broadcasts an SSE event. The frontend listens for metadata events, stores them in the session store, and renders a modal when the user clicks a group label.

The metadata schema is intentionally untyped (`dict[str, Any]`) — the benchmark decides what to put there. For our qwen-vs-gemma4 benchmark, the convention is:
```json
{
  "prompt": "Explain what a hash table is in 2 sentences.",
  "responses": {
    "qwen_gguf": "A hash table is a data structure that...",
    "qwen_mlx": "Hash tables store key-value pairs...",
    "gemma4_gguf": "A hash table is a fundamental...",
    "gemma4_mlx": "Hash tables map keys to values..."
  }
}
```

## Relevant Files

### Existing — Backend
- `apps/backend/src/live_bench_server/models.py` — Add `GroupMetadata`, `SseMetadata` Pydantic models; extend `IngestRequest`
- `apps/backend/src/live_bench_server/db.py` — Add `metadata` table to schema + migration; add `init_db` migration step
- `apps/backend/src/live_bench_server/store.py` — Add `upsert_metadata()`, `get_metadata()` functions; extend `reset()` to clear metadata
- `apps/backend/src/live_bench_server/http_ingest.py` — Process `metadata` from `IngestRequest`, call `upsert_metadata`, broadcast SSE
- `apps/backend/src/live_bench_server/sse_stream.py` — Include metadata in snapshot; handle metadata events in the live stream
- `apps/backend/src/live_bench_server/rest.py` — Include metadata in `GET /benchmarks/{id}` response

### Existing — CLI
- `apps/cli/src/live_bench_cli/cli.py` — Register new `meta` command
- `apps/cli/src/live_bench_cli/commands/` — Directory for command modules
- `apps/cli/src/live_bench_cli/client.py` — No changes needed (uses existing `ingest()` method)

### Existing — Frontend
- `apps/frontend/src/schemas.ts` — Add `GroupMetadataSchema`, `SseMetadataSchema` to Zod schemas
- `apps/frontend/src/stores/session.ts` — Add `metadata: Map<string, any>` to store state
- `apps/frontend/src/api/stream.ts` — Add `metadata` event listener + handler callback
- `apps/frontend/src/components/GroupedBarChart.vue` — Make group labels clickable, emit click event
- `apps/frontend/src/pages/BenchmarkPage.vue` — Wire modal open/close state
- `apps/frontend/src/styles/main.css` — Modal styles

### Existing — Benchmark
- `apps/benchmarks/qwen35-vs-gemma4/bench.py` — Emit metadata (prompt + response text) after each prompt
- `apps/benchmarks/qwen35-vs-gemma4/_harness.py` — Already returns `text` in result dict (line 213) — no changes needed

### New Files
- `apps/cli/src/live_bench_cli/commands/meta_cmd.py` — `live-bench meta` command for emitting metadata
- `apps/frontend/src/components/PromptModal.vue` — Modal component showing prompt + responses

## Implementation Phases

### Phase 1: Foundation (Backend)
Add the metadata table, Pydantic models, store functions, and wire into the ingest pipeline. This is pure backend — no frontend or CLI changes yet.

- SQLite table: `metadata (session_id TEXT, chart_id TEXT, group_key TEXT, data_json TEXT, updated_at INTEGER, PRIMARY KEY (session_id, chart_id, group_key))`
- `upsert_metadata()` — merge semantics: `json_patch(existing, new)` so each emit adds keys without clobbering
- `get_metadata()` — returns `dict[tuple[str,str], dict]` keyed by `(chart_id, group_key)`
- `reset()` — add `DELETE FROM metadata WHERE session_id = ?`
- SSE model: `SseMetadata(event="metadata", session_id, chart_id, group_key, data: dict)`
- Extend `IngestRequest` with `metadata: list[GroupMetadata] = []`
- Ingest handler processes metadata entries, upserts, and broadcasts

### Phase 2: CLI + Benchmark Script
Add the `live-bench meta` command and update `bench.py` to emit metadata.

- `meta_cmd.py` — accepts `--chart`, `--group`, `--json` (string or `-` for stdin)
- POSTs to `/ingest` with `metadata` field populated (reuses existing ingest endpoint)
- `bench.py` — after each `run_warm_isolated()` call, collect `m["text"]` (the model's response) and emit metadata:
  ```python
  # After emitting numeric values for a prompt:
  meta = {"prompt": p["text"]}
  meta.setdefault("responses", {})[cfg["metric"]] = m.get("text", "")[:2000]
  # Emit via CLI or direct POST
  ```
- Use the CLI: `live-bench meta <session> --chart <chart> --group <group> --json '<json>'`

### Phase 3: Frontend (Schema + Store + SSE)
Wire metadata through the frontend data layer.

- Zod: `GroupMetadataSchema = z.object({chart_id, group_key, data: z.record(z.any())})`
- `SseMetadataSchema = z.object({event: z.literal("metadata"), session_id, chart_id, group_key, data: z.record(z.any())})`
- Add to `SseEventSchema` discriminated union
- Session store: `metadata: Map<DatasetKey, Record<string, any>>` — update on SSE metadata events and snapshot
- Stream handler: `onMetadata` callback in `StreamHandlers`
- Snapshot: backend includes metadata in the snapshot response; `applySnapshot` populates the metadata map
- BenchmarkPage: wire the new `onMetadata` handler

### Phase 4: Frontend (Modal UI)
Build the clickable labels and modal.

- `GroupedBarChart.vue`: group label `<text>` elements become clickable — emit a `@group-click` event with `(chartId, groupKey)`
- Add CSS: `cursor: pointer` on hover, subtle underline or highlight
- `PromptModal.vue`:
  - Props: `chartId`, `groupKey`, `metadata` (the data dict), `metrics` (chart metric defs), `latest` (value map), `groups` (for icon lookup)
  - Renders:
    - Header: group label (e.g., "P1 factual") + close button
    - Prompt text block (from `metadata.prompt`)
    - Response cards — one per metric that has a response in `metadata.responses`:
      - Model icon + name + color swatch
      - Metrics row: prefill/decode/wall values pulled from `latest` map
      - Response text (collapsible, scrollable)
  - Close on: X button, Escape key, backdrop click
- `BenchmarkPage.vue`: state for `activeModal: {chartId, groupKey} | null`, pass to modal
- Wire `@group-click` from each `BenchmarkCard` → `GroupedBarChart` → `BenchmarkPage`

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
  - Role: Backend — metadata table, Pydantic models, store functions, ingest handler, SSE, REST
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-cli-bench
  - Role: CLI meta command + benchmark script metadata emission
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-frontend
  - Role: Frontend — Zod schemas, session store, SSE handler, clickable labels, PromptModal component
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: validator
  - Role: End-to-end validation — tests, Playwright browser verification, smoke benchmark with metadata
  - Agent Type: playwright-bowser-agent
  - Resume: true

## Step by Step Tasks

### 1. Backend — Metadata Table + Models
- **Task ID**: backend-models-db
- **Depends On**: none
- **Assigned To**: builder-backend
- **Agent Type**: general-purpose
- **Parallel**: true (can run alongside task 2)
- Add `GroupMetadata` model to `models.py`: `chart_id: str = "default"`, `group_key: str`, `data: dict[str, Any]`
- Add `SseMetadata` model to `models.py`: `event: Literal["metadata"] = "metadata"`, `session_id: str`, `chart_id: str`, `group_key: str`, `data: dict[str, Any]`
- Add `metadata: list[GroupMetadata] = Field(default_factory=list)` to `IngestRequest`
- Add `metadata` table to `db.py` `_SCHEMA`: `(session_id TEXT, chart_id TEXT, group_key TEXT, data_json TEXT NOT NULL, updated_at INTEGER NOT NULL, PRIMARY KEY (session_id, chart_id, group_key))`
- Add migration in `migrate()` — `CREATE TABLE IF NOT EXISTS` so it's idempotent
- Update `__all__` exports

### 2. Backend — Store Functions
- **Task ID**: backend-store
- **Depends On**: backend-models-db
- **Assigned To**: builder-backend
- **Agent Type**: general-purpose
- **Parallel**: false
- Add `upsert_metadata(conn, session_id, entries: list[GroupMetadata])` to `store.py`:
  - For each entry, read existing `data_json`, parse as dict, deep-merge new `data` into it, write back
  - Use `INSERT ... ON CONFLICT ... DO UPDATE` for the upsert
  - Deep merge: `existing.update(new)` for top-level keys, but for nested dicts like `responses`, merge: `existing["responses"].update(new["responses"])`
  - Return list of `(chart_id, group_key)` pairs that were updated
- Add `get_all_metadata(conn, session_id) -> dict[str, dict]` — returns `{f"{chart_id}:{group_key}": data_dict, ...}` 
- Extend `reset()` — add `DELETE FROM metadata WHERE session_id = ?`

### 3. Backend — Ingest + SSE + REST
- **Task ID**: backend-ingest-sse
- **Depends On**: backend-store
- **Assigned To**: builder-backend
- **Agent Type**: general-purpose
- **Parallel**: false
- In `http_ingest.py`: after processing points and completions, process `body.metadata`:
  - Validate each entry's `chart_id` and `group_key` against config (same validation as points)
  - Call `store.upsert_metadata(conn, session_id, body.metadata)`
  - For each updated pair, broadcast `SseMetadata(session_id=session_id, chart_id=..., group_key=..., data=merged_data)`
- In `sse_stream.py`: include metadata in the initial snapshot:
  - After building `snapshot_points` and `snapshot_datasets`, call `store.get_all_metadata(conn, session_id)`
  - Add a `metadata` field to the snapshot yield (or emit separate metadata events after the snapshot)
  - In the live event loop, handle `SseMetadata` events (the `else` branch already handles unknown events via `event.event`)
- In `rest.py`: add `metadata` to `GET /benchmarks/{id}` response payload

### 4. CLI — Meta Command
- **Task ID**: cli-meta-cmd
- **Depends On**: backend-ingest-sse
- **Assigned To**: builder-cli-bench
- **Agent Type**: general-purpose
- **Parallel**: true (can run alongside task 5)
- Create `apps/cli/src/live_bench_cli/commands/meta_cmd.py`:
  - `@click.command()` with args: `session_id`, `--chart` (default "default"), `--group` (required), `--json` (string or `-` for stdin)
  - Parses JSON, builds `IngestRequest` with `metadata=[GroupMetadata(chart_id=chart, group_key=group, data=parsed)]`, empty points
  - POSTs via `LiveBenchClient.ingest()`
- Register in `cli.py`: `cli.add_command(meta_cmd.meta)`
- Reinstall CLI: `just install-cli`
- Test: `live-bench meta --help` exits 0

### 5. Benchmark Script — Emit Metadata
- **Task ID**: bench-emit-meta
- **Depends On**: cli-meta-cmd
- **Assigned To**: builder-cli-bench
- **Agent Type**: general-purpose
- **Parallel**: false
- Update `bench.py` `CompletionTracker.emit_and_track()`:
  - Accept `response_text: str` parameter
  - After emitting numeric values, build metadata: `{"prompt": prompt_text, "responses": {metric_key: response_text}}`
  - Emit via subprocess: `live-bench meta <session> --chart <chart>_<hw> --group <group_key> --json '<json>'`
  - Since metadata merges, each backend's response accumulates into the same group's metadata
- Update `bench_ollama()` and `bench_gemma4_mlx()` — pass `m.get("text", "")[:4000]` (truncate long responses) to the tracker
- Store prompt text in tracker so it's available: `tracker.set_prompt(p["key"], p["text"])`

### 6. Frontend — Schema + Store + SSE
- **Task ID**: frontend-data-layer
- **Depends On**: backend-ingest-sse
- **Assigned To**: builder-frontend
- **Agent Type**: general-purpose
- **Parallel**: true (can run alongside tasks 4-5)
- Add to `schemas.ts`:
  - `GroupMetadataSchema = z.object({chart_id: z.string(), group_key: z.string(), data: z.record(z.string(), z.any())})`
  - `SseMetadataSchema = z.object({event: z.literal("metadata"), session_id: z.string(), chart_id: z.string(), group_key: z.string(), data: z.record(z.string(), z.any())})`
  - Add `SseMetadataSchema` to `SseEventSchema` discriminated union
  - Export types
- Add to `session.ts`:
  - `metadata: Map<DatasetKey, Record<string, any>>` in state
  - `applyMetadata(chart_id, group_key, data)` action — merges into existing entry
  - Include in `applySnapshot()` — read metadata from snapshot
  - Clear in `clear()` and `applyReset()`
- Add to `stream.ts`:
  - `onMetadata` callback in `StreamHandlers`
  - Event listener for `metadata` SSE events
- Wire in `BenchmarkPage.vue`: `onMetadata: (e) => session.applyMetadata(e.chart_id, e.group_key, e.data)`

### 7. Frontend — Clickable Labels + PromptModal
- **Task ID**: frontend-modal
- **Depends On**: frontend-data-layer
- **Assigned To**: builder-frontend
- **Agent Type**: general-purpose
- **Parallel**: false
- In `GroupedBarChart.vue`:
  - Add `const emit = defineEmits<{groupClick: [chartId: string, groupKey: string]}>()` 
  - Make group label `<text>` elements clickable: add `@click`, `style="cursor:pointer"`, hover class
  - Emit `groupClick` with chart_id and group_key on click
- Create `PromptModal.vue`:
  - Props: `chartId: string`, `groupKey: string`, `groupLabel: string`, `metadata: Record<string, any> | null`, `metrics: MetricDef[]`, `latest: Map<string, number>`, `groups: GroupDef[]`, `allChartIds: string[]` (to pull metrics from all 3 charts)
  - Template:
    - Backdrop (semi-transparent, click to close)
    - Modal card with header (group label + X close button)
    - Prompt text block: `metadata?.prompt`
    - Response cards: iterate `metadata?.responses` entries — for each `(metricKey, responseText)`:
      - Find metric def for color/label
      - Find group def for icon
      - Show: icon, metric label (model name), color swatch
      - Show metrics: look up `latest.get(${chartId}:${groupKey}:${metricKey})` for each of the 3 chart types (prefill, decode, wall) — pass all chart IDs so we can pull cross-chart values
      - Show response text (collapsed by default, expand on click)
    - Close on Escape key (global keydown listener)
  - Style: dark overlay, centered card, scrollable body, matches Obsidian theme
- In `BenchmarkCard.vue`: bubble the `@group-click` event from GroupedBarChart
- In `BenchmarkPage.vue`:
  - State: `activeModal: {chartId: string, groupKey: string} | null`
  - Computed: `activeMetadata` — reads from `session.metadata.get(${chartId}:${groupKey})`
  - Computed: `activeGroupLabel` — finds the group label from config
  - Render `PromptModal` when `activeModal` is set
  - Wire close handler to set `activeModal = null`

### 8. End-to-End Validation
- **Task ID**: validate-all
- **Depends On**: bench-emit-meta, frontend-modal
- **Assigned To**: validator
- **Agent Type**: playwright-bowser-agent
- **Parallel**: false
- Run `just test` — all existing tests pass (no regressions)
- Boot platform: `just serve`
- Run smoke: `just bench-qg-smoke-m4` — verify metadata emitted in terminal output
- Playwright browser test:
  1. Navigate to benchmark page
  2. Wait for data
  3. Click a group label (e.g., "P1 factual")
  4. Verify modal appears with prompt text
  5. Verify at least one response card shows model name + response text
  6. Press Escape — modal closes
  7. Screenshot evidence
- Verify `live-bench meta` command works standalone:
  - `live-bench meta qwen35-vs-gemma4 --chart prefill_m4 --group p1 --json '{"prompt": "test", "responses": {"qwen_gguf": "hello"}}'`
  - Verify data appears in `GET /benchmarks/qwen35-vs-gemma4` response

## Acceptance Criteria

1. `live-bench meta <session> --chart <chart> --group <group> --json <data>` emits metadata and returns success
2. Metadata persists in SQLite — survives server restart
3. Metadata merges — emitting `{responses: {qwen_gguf: "..."}}` then `{responses: {gemma4_mlx: "..."}}` results in both responses present
4. `reset` clears metadata alongside datapoints
5. SSE snapshot includes metadata for all groups
6. Live SSE metadata events arrive when new metadata is emitted
7. Clicking a group label on the chart opens the PromptModal
8. Modal shows the prompt text and all available model responses
9. Modal updates live as new responses arrive via SSE
10. Modal closes on X, Escape, or backdrop click
11. `just test` passes — no regressions
12. Benchmark script (`bench.py`) emits prompt + response metadata after each prompt

## Validation Commands

- `just test` — all backend + CLI + frontend tests pass
- `live-bench meta --help` — command registered and shows usage
- `live-bench meta qwen35-vs-gemma4 --chart prefill_m4 --group p1 --json '{"prompt":"test"}'` — returns ok
- `curl http://127.0.0.1:8787/benchmarks/qwen35-vs-gemma4 | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('metadata', 'MISSING'))"` — shows metadata
- `just bench-qg-smoke-m4` — emits metadata (visible in terminal output)
- Playwright: click group label → modal appears with prompt text

## Notes

### Metadata Merge Semantics

The merge is a **shallow merge at top level, deep merge for `responses`**. This means:
- Emitting `{prompt: "new"}` overwrites the entire `prompt` key
- Emitting `{responses: {qwen_gguf: "..."}}` adds/updates just `qwen_gguf` without touching other responses

Implementation: read existing JSON, do `existing_data.update(new_data)` but for the `responses` key specifically, do `existing_data.setdefault("responses", {}).update(new_data.get("responses", {}))` then write back.

### Response Text Truncation

Model responses can be very long (thousands of tokens). The benchmark script should truncate at ~4000 chars to keep SQLite and SSE payloads manageable. The modal UI should show the truncated text with a "..." indicator if truncated.

### Cross-Chart Metric Display

The modal shows metrics from ALL 3 charts (prefill, decode, wall) for the given group/prompt. Since charts have different `chart_id`s (`prefill_m4`, `decode_m4`, `wall_m4`), the modal needs to know the sibling chart IDs to look up values from the session store's `latest` map. Pass the full list of chart IDs to the modal so it can construct the composite keys.

### No New Dependencies

This feature uses only existing dependencies. No `uv add` needed.

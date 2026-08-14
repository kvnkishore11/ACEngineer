# Plan: Build Live Bench Platform

## Task Description

Implement the live benchmarking platform fully described in [`spec/init_live_bench.md`](../spec/init_live_bench.md). This is a from-scratch build of a three-app system in a `apps/{backend,cli,frontend}` layout:

1. **Backend** — FastAPI + SQLite (3 tables) + Pydantic v2 + SSE broadcaster, accepting HTTP POST `/ingest` from CLI clients with client-stamped microsecond timestamps. Loads benchmark definitions from `benchmarks/*.yaml` on boot.
2. **CLI** — astral uv project exposing a `live-bench` click command (`list`, `show`, `reset`, `emit`, `complete`, `stream`, `tail`). Stamps `client_ts` at the moment a point is read from CLI args / stdin and POSTs via httpx with keep-alive.
3. **Frontend** — Vite Vue 3 + TS + Pinia + Zod + vue-router. Two routes: `/` landing dropdown and `/benchmark/:sessionId` chart page. Hand-rolled SVG grouped bar charts with 1-second coalescing animations, gradient bar fills, S/M/L density switcher, 10 themes (default `obsidian`), Play font, presentation-sized type. Newer-wins-by-`client_ts` ordering in the session store.

The spec is the source of truth. This plan does not duplicate it — every task references the spec section that defines what to build.

## Objective

Ship a working `just serve` from a cold checkout in which: a benchmark YAML in `benchmarks/` becomes a chart on screen; a `live-bench emit` from any LAN host smoothly animates a bar to the new value within ~1s; a `live-bench complete` flips a dataset pill to "complete"; and SSE reconnect after a server restart restores bars to the correct latest values without flicker. All six success criteria in §17 of the spec must hold.

## Problem Statement

There is no existing code — only `spec/init_live_bench.md`. The platform spans three apps in two languages with shared schema, a non-trivial wire protocol (HTTP ingest + SSE broadcast with `client_ts` ordering), an in-process pub/sub broker, and a presentation-tuned UI with hand-rolled SVG animations and 10 themes. Building it sequentially in one agent would be slow and would mix unrelated concerns. The backend and frontend are independently buildable against the spec; the CLI depends only on the backend's `models.py` (path dep). This shape is naturally parallelisable into a small team.

## Solution Approach

Build in three phases against `spec/init_live_bench.md` as the single source of truth:

1. **Phase 1 — Foundation.** Scaffold the monorepo (`apps/{backend,cli,frontend}`, `benchmarks/`, root `justfile`, `.gitignore`, README). Drop in the five example YAML files from spec §5 so the backend has data to load on first boot. Then write the shared Pydantic models module — this is the contract every other task depends on.
2. **Phase 2 — Core Implementation (parallel).** Three independent builds run simultaneously: backend (FastAPI + SQLite + SSE + http_ingest), CLI (click + httpx with `client_ts` stamping), frontend (Vue 3 + Pinia + SVG charts + themes + animation). Each builder writes its own unit tests inline. The CLI takes a path dep on the backend package so they share the Pydantic source of truth without a third "shared" package.
3. **Phase 3 — Integration & Polish.** A new cross-cutting `backend-cli-smoke` checkpoint runs as soon as backend + CLI are both done, catching wire-shape drift before the frontend matters. Then the final `integration-validator` agent uses `/drive` (tmux process orchestration) plus `playwright-bowser-agent` (real browser DOM/SVG inspection) to walk a scripted scenario over a dedicated `benchmarks/test-drive-*.yaml` fixture set: 3 charts (1 LR + 2 BT), 3 datasets each, mixed solid/gradient colours. The same scenario is also wired up as `just test-drive-*` recipes so a human can drive the same walkthrough manually on camera.

The team is **six** named agents, all `general-purpose` since no specialised team agents exist in `.claude/agents/team/`. Each agent has a single clear responsibility. Resume is enabled by default so each builder can be brought back to fix issues found in validation without losing context. The `integration-validator` agent owns both the cross-app smoke checkpoint (after backend + CLI) and the final integrated walk-through (after everything).

Validation is **layered**, not back-loaded. See the dedicated *Validation Strategy* section below.

## Validation Strategy

Three layers, each catching a different class of bug. Every layer runs against the same `benchmarks/test-drive-*.yaml` fixture set described in 5.7 below, so the test surface is shared across unit, smoke, and integration.

### Layer 1 — Builder-internal (in-loop, fast)

Each builder writes their own unit tests against their own app, with no other process running. These exist in the per-builder tasks below and run on every save during development.

- **Backend** — `pytest` with FastAPI's `TestClient` (httpx-based). Coverage: `store.insert_points` monotonic seq assignment, `store.latest_per_cell` returns the right newest values when `client_ts` arrives out of order, all 5 `/ingest` 4xx error codes, SSE snapshot+datapoint+`dataset_complete` event flow over `TestClient.stream`, `Last-Event-ID` resume.
- **CLI** — `pytest` with a **mock httpx transport** (no network). Critical invariant test: stamp three points through `stream` with 100 ms sleeps and assert the resulting `client_ts` deltas reflect the sleep deltas, *not* the post-batching flush time.
- **Frontend** — `vitest`. Two pieces:
  1. **Zod drift test** against JSON fixtures exported by `apps/backend/tests/fixtures_export.py` — proves schema parity across the language boundary.
  2. **`AnimatedBar` state machine in pure TS** with fake timers — drives `current/target/pending` through fast successive updates, asserts coalescing drops intermediates and the latest value always wins.
  3. **Session-store newer-wins guard** — feeds `applyDatapoint` two events with reversed `client_ts`, asserts the bar value sticks to the newer one (the §14.4 invariant).

Layer 1 is fast (<10 s per app), runs on every save, and catches most bugs before they cross app boundaries.

### Layer 2 — Per-app smoke against a real running process (`/drive`)

This is the layer that catches "did the app actually boot and round-trip a real request" before handoff. `/drive` is the right tool because each smoke is "spawn a process in a tmux pane, poke it, read output." Each builder runs their own smoke at the end of their task before reporting done.

- **Backend smoke (end of `backend-impl`).** `drive` creates session `lb-backend`, runs `cd apps/backend && uv run uvicorn live_bench_server.main:app --port 8787`, polls for `Application startup complete`. From a separate pane: `curl -s :8787/healthz`, `curl -s :8787/benchmarks` (asserts the test-drive YAMLs were reconciled), POST `/ingest` with a synthetic `client_ts`, GET `/benchmarks/<id>` and assert the point landed. Open `curl -N :8787/stream/<id>` in a third pane and assert the `snapshot` + `datapoint` events arrive. Tear down.
- **CLI smoke (end of `cli-impl`).** Backend left running from the previous smoke (or relaunched). In `lb-cli` pane: every command end-to-end against the real backend — `list`, `emit`, `show`, `complete`, `reset`, `stream` piped from `fake_stream`. In `lb-tail` pane: `live-bench tail` watching the SSE stream, asserts events arrive for each `emit`.
- **Frontend smoke (end of `frontend-impl`).** `drive` runs the backend, runs `pnpm dev` in `lb-frontend`, polls for the `Local: http://` ready signal. **Then `playwright-bowser-agent`** loads `http://localhost:5173/`, asserts the dropdown lists the 3 test-drive sessions + the 5 spec example sessions (8 total), navigates to `/benchmark/test-drive-bt-grouped`, screenshots the empty chart, asserts the title/subtitle/"Higher is better" label render. Saves `screenshots/frontend-smoke-empty.png`.

### Layer 3 — Integrated end-to-end (`/drive` + `playwright-bowser-agent` + `just test-drive-*`)

Run by `integration-validator` after all builds are green. The same scenario is also exposed as `just test-drive-*` recipes so a human can drive it manually on camera — these recipes are the canonical demo.

- `drive` opens 5 tmux sessions: `lb-backend` (uvicorn), `lb-frontend` (vite dev), `lb-tail` (live-bench tail SSE), `lb-emitter` (CLI commands), `lb-watch` (optional pytest log).
- `playwright-bowser-agent` loads `http://localhost:5173/`, navigates to `/benchmark/test-drive-bt-grouped`, screenshots baseline.
- The validator walks the 10-step sequence in §6 task, capturing screenshots at every step. Each step also has a `just test-drive-*` recipe so a presenter can replay it interactively.
- **Out-of-order test (AC-Order).** Use `live-bench emit --batch -` with two JSONL lines whose `client_ts` is explicitly set in reverse order. Read the rendered SVG via playwright and assert the bar shows the value with the *newer* `client_ts*. This is the only test that needs the CLI's "client_ts pass-through" path.
- **Restart-resilience test (AC4).** `drive kill-session lb-backend`, wait 2 s, `drive new-session lb-backend ...`. Playwright observes `<ConnectionBadge>` cycle amber → green and asserts the bars hold their values throughout.
- **Theme + density cycle (AC6).** Playwright clicks the `ThemeSwitcher` through `obsidian → matrix → sunset → obsidian` and the `LayoutSwitcher` through S/M/L, screenshotting each combination. Asserts `<html data-theme>` actually changes and the page does not crash.
- **Final report.** A markdown table in `specs/validation-report.md` listing every AC with pass/fail + screenshot path, returned to the team lead. Failures include the file:line of the most likely culprit so the relevant builder can be resumed for a fix.

### How `/drive` and `playwright-bowser-agent` divide the work

| Concern | Tool | Why |
|---|---|---|
| Spawn long-lived processes (backend, vite, tail) | `/drive` | tmux gives real process control + parallel sessions + readiness polling |
| Send CLI commands and read stdout | `/drive` | one shell per session, `drive read` for output capture |
| Kill + restart the backend mid-test | `/drive` | clean session lifecycle, no `kill -9` shell games |
| Load the page in a real browser | `playwright-bowser-agent` | the only way to actually render Vue + animate SVG |
| Click the dropdown / theme switcher | `playwright-bowser-agent` | DOM-level interactions |
| Assert bar `height` / `width` attributes | `playwright-bowser-agent` | reads the rendered SVG attributes after animation settles |
| Take screenshots for the validation report | `playwright-bowser-agent` | full-page PNGs at deterministic checkpoints |
| Run unit tests | plain shell via `/drive` | pytest / vitest in dedicated panes |

Both tools run in parallel — `/drive` keeps the backend + frontend + CLI panes alive while `playwright-bowser-agent` is interacting with the browser. Neither tool blocks the other.

## Relevant Files

The build is a from-scratch creation. The only existing input is the spec.

- `spec/init_live_bench.md` — **the single source of truth.** Every builder must read the relevant sections before writing code. Section map:
  - §1–§3: scope, architecture diagram, repo layout
  - §4: SQLite schema (3 tables) + Pydantic models + Zod mirrors
  - §5: YAML config schema + 5 example benchmark files
  - §6: backend file-by-file responsibilities
  - §7: CLI file-by-file responsibilities + command list
  - §8: frontend routes, density, card anatomy, file-by-file
  - §9: wire protocol (HTTP request/response shapes, SSE events, REST table)
  - §10: end-to-end example flow
  - §11: cross-language type sharing strategy (path dep + drift test)
  - §12: justfile recipes
  - §13: theming + Play font + 10 theme definitions (`obsidian` default)
  - §14: animation state machine + newer-wins on `client_ts`
  - §15: HTTP POST locked + why client timestamps are non-negotiable
  - §16: open questions (acceptable to defer)
  - §17: success criteria
- `gemma4/bench/bench_gguf_vs_mlx.py` (private sibling repo) — reference for the benchmark CSV/data shapes that will be emitted into live-bench. Read for context only; do not depend on it.
- `pi-agent-playground-v2/bench/` (private sibling repo) — additional reference benchmarks for context-scaling and 4-way comparisons.

### New Files

The complete tree to be created (matching spec §3 exactly):

**Root**
- `.gitignore` — Python (`.venv`, `__pycache__`, `*.pyc`, `.pytest_cache`), node (`node_modules`, `dist`), DB (`*.db`, `*.db-wal`, `*.db-shm`), CLI outbox (`.live-bench-outbox.jsonl`), editor scratch
- `README.md` — one page: what it is, `just serve` quick start, link to spec
- `justfile` — recipes from spec §12 (`serve`, `backend`, `frontend`, `cli`, `list`, `show`, `reset`, `emit`, `complete`, `test`, `build-frontend`, `demo-stream`)
- `benchmarks/gemma4-e4b-prefill.yaml` — spec §5.2
- `benchmarks/gemma4-e4b-decode.yaml` — spec §5.3
- `benchmarks/gemma4-e4b-wall.yaml` — spec §5.4 (`better: lower`)
- `benchmarks/m5-4way-tps.yaml` — spec §5.5
- `benchmarks/m5-pi-agent.yaml` — spec §5.6 (extrapolate from §5.5 shape)
- `benchmarks/test-drive-lr.yaml` — **test fixture.** direction `LR`, 3 groups (`alpha`, `bravo`, `charlie`), 1 metric (`latency_ms`, solid color), `better: lower`. Dedicated to the validation walkthrough — see §5.7 below.
- `benchmarks/test-drive-bt-grouped.yaml` — **test fixture.** direction `BT`, 3 groups (`alpha`, `bravo`, `charlie`), 2 metrics (`throughput`, `latency`, both solid colors), `better: higher`. Exercises BT direction + grouped multi-metric bars + solid colors.
- `benchmarks/test-drive-bt-gradient.yaml` — **test fixture.** direction `BT`, 3 groups (`alpha`, `bravo`, `charlie`), 2 metrics (`prefill`, `decode`, both gradient `["#a","#b"]` arrays), `better: higher`. Exercises BT direction + grouped bars + linear-gradient fills (the §13.2.1 mockup colors).

**Backend — `apps/backend/`**
- `pyproject.toml` (uv project, Python ≥3.12, deps: fastapi, sse-starlette, uvicorn, pydantic≥2, pyyaml, pytest, httpx for tests)
- `uv.lock`
- `README.md`
- `src/live_bench_server/__init__.py`
- `src/live_bench_server/main.py` — FastAPI app, routes, startup/shutdown
- `src/live_bench_server/config.py` — `load_benchmarks_dir(path)`
- `src/live_bench_server/models.py` — all Pydantic models from spec §4.2
- `src/live_bench_server/db.py` — sqlite3 wrapper, `migrate()`, WAL mode
- `src/live_bench_server/store.py` — repository methods incl. `latest_per_cell`, `insert_points`, `mark_complete`, `dataset_states`
- `src/live_bench_server/http_ingest.py` — POST /ingest with client_ts validation
- `src/live_bench_server/sse_stream.py` — GET /stream/{session_id}, Last-Event-ID resume
- `src/live_bench_server/rest.py` — /benchmarks, /benchmarks/{id}, /benchmarks/{id}/reset, /healthz
- `src/live_bench_server/broker.py` — asyncio in-proc pub/sub
- `src/live_bench_server/logging.py`
- `tests/test_store.py` — insert_points + latest_per_cell + reset
- `tests/test_http_ingest.py` — happy path, unknown group, missing client_ts, clock_skew
- `tests/test_sse_stream.py` — snapshot + datapoint + dataset_complete + reset event flow
- `tests/fixtures_export.py` — exports a JSON fixture per Pydantic model into `tests/fixtures/<name>.json` for the frontend Zod drift test
- `tests/fixtures/<name>.json` — generated fixtures (gitignored or committed, builder's choice)

**CLI — `apps/cli/`**
- `pyproject.toml` (uv project; `[project.scripts]` exposes `live-bench`; deps: click, httpx, rich, pydantic; `[tool.uv.sources]` declares `live-bench-server = { path = "../backend", editable = true }`)
- `uv.lock`
- `README.md`
- `src/live_bench_cli/__init__.py`
- `src/live_bench_cli/__main__.py`
- `src/live_bench_cli/cli.py` — click app, global flags
- `src/live_bench_cli/client.py` — `LiveBenchClient` (httpx.Client + retry + outbox), `now_ts()`
- `src/live_bench_cli/models.py` — re-exports `live_bench_server.models`
- `src/live_bench_cli/commands/list_cmd.py`
- `src/live_bench_cli/commands/show_cmd.py`
- `src/live_bench_cli/commands/reset_cmd.py`
- `src/live_bench_cli/commands/emit_cmd.py`
- `src/live_bench_cli/commands/complete_cmd.py`
- `src/live_bench_cli/commands/stream_cmd.py`
- `src/live_bench_cli/commands/tail_cmd.py`
- `src/live_bench_cli/dev/fake_stream.py` — synthetic data emitter for `just demo-stream`
- `tests/test_client.py` — outbox + retry + timestamp stamping
- `tests/test_commands.py` — emit / complete / stream payload shape

**Frontend — `apps/frontend/`**
- `package.json` (vue@3, vue-router@4, pinia, zod, vite, typescript, vitest, @vitejs/plugin-vue, @types/node)
- `pnpm-lock.yaml`
- `tsconfig.json`, `vite.config.ts`
- `index.html` — preload Play font from Google Fonts
- `README.md`
- `src/main.ts`
- `src/App.vue`
- `src/router.ts`
- `src/schemas.ts` — Zod mirrors of spec §4.2
- `src/themes.ts` — 10 theme definitions, names + swatches
- `src/api/rest.ts`
- `src/api/stream.ts` — SSE manager + reconnect, Last-Event-ID
- `src/stores/benchmarks.ts`
- `src/stores/session.ts` — includes `latestClientTs` map for newer-wins (spec §14.4)
- `src/stores/prefs.ts` — theme + density localStorage
- `src/pages/LandingPage.vue`
- `src/pages/BenchmarkPage.vue`
- `src/components/NavBar.vue`
- `src/components/LayoutSwitcher.vue`
- `src/components/ThemeSwitcher.vue`
- `src/components/ConnectionBadge.vue`
- `src/components/BenchmarkGrid.vue`
- `src/components/BenchmarkCard.vue`
- `src/components/DatasetStatusBar.vue`
- `src/components/GroupedBarChart.vue`
- `src/components/BarGradientDefs.vue`
- `src/components/AnimatedBar.vue`
- `src/components/EmptyState.vue`
- `src/styles/main.css` — base, CSS vars, font sizes from spec §13.1
- `src/styles/themes.css` — 10 `[data-theme]` blocks, `obsidian` from spec §13.2.1
- `src/schemas.test.ts` — drift test against backend fixture JSON

## Implementation Phases

### Phase 1: Foundation
1. Scaffold the monorepo: root files (`.gitignore`, `README.md`, `justfile` with **dedicated ports + self-clearing recipes**, see Notes), the `benchmarks/` directory with all five example YAMLs from spec §5 **plus the three `test-drive-*.yaml` fixtures**, and the empty `apps/{backend,cli,frontend}/` directories with their `pyproject.toml` / `package.json` and lockfile placeholders. The justfile also includes the `test-drive-*` recipe set described in 5.7 below. Verify `just --list` and `just ports` work before unblocking Phase 2.
2. Write the shared Pydantic models module (`apps/backend/src/live_bench_server/models.py`) exactly per spec §4.2, including the `client_ts: datetime` field and serialisation config that emits ISO-8601 UTC with microseconds. This is the foundation contract for both backend and CLI; nothing else can start until this exists.

#### 5.7 The `test-drive-*` fixture set + just recipes

Three minimal YAMLs in `benchmarks/` that the validator (and a presenter) walks through to exercise every chart/animation/status code path. Distinct from the five spec-§5 demo YAMLs because the test-drive set is *deliberately small* and *deliberately covers all variants*.

**`benchmarks/test-drive-lr.yaml`** — 1 LR chart, 3 groups, 1 solid-color metric:
```yaml
version: 1
benchmark:
  session_id: test-drive-lr
  title: "Test Drive — Latency (LR)"
  subtitle: "3 groups · 1 metric · solid color"
  better: lower
  direction: LR
  x: { label: "Latency", unit: "ms", min: 0 }
  y: { label: "Probe" }
  metrics:
    - { key: latency_ms, label: "Latency", color: "#f87171" }
  groups:
    - { key: alpha,   label: "Alpha"   }
    - { key: bravo,   label: "Bravo"   }
    - { key: charlie, label: "Charlie" }
```

**`benchmarks/test-drive-bt-grouped.yaml`** — 1 BT chart, 3 groups, 2 solid-color metrics:
```yaml
version: 1
benchmark:
  session_id: test-drive-bt-grouped
  title: "Test Drive — Throughput vs Latency (BT)"
  subtitle: "3 groups · 2 metrics · solid colors"
  better: higher
  direction: BT
  x: { label: "Worker" }
  y: { label: "Throughput", unit: "req/s", min: 0 }
  metrics:
    - { key: throughput, label: "Throughput", color: "#10b981" }
    - { key: latency,    label: "Latency",    color: "#f59e0b" }
  groups:
    - { key: alpha,   label: "Alpha"   }
    - { key: bravo,   label: "Bravo"   }
    - { key: charlie, label: "Charlie" }
```

**`benchmarks/test-drive-bt-gradient.yaml`** — 1 BT chart, 3 groups, 2 gradient-color metrics:
```yaml
version: 1
benchmark:
  session_id: test-drive-bt-gradient
  title: "Test Drive — Gradient Bars (BT)"
  subtitle: "3 groups · 2 metrics · gradient colors"
  better: higher
  direction: BT
  x: { label: "Backend" }
  y: { label: "tokens / second", unit: "tok/s", min: 0 }
  metrics:
    - { key: prefill, label: "Prefill", color: ["#e86b3a", "#f2a66b"] }
    - { key: decode,  label: "Decode",  color: ["#4a8fe0", "#6fa5e8"] }
  groups:
    - { key: alpha,   label: "Alpha"   }
    - { key: bravo,   label: "Bravo"   }
    - { key: charlie, label: "Charlie" }
```

**`just test-drive-*` recipes** (in the root justfile, in addition to spec §12 recipes):

```just
# ── test-drive: scripted walkthrough of the test fixtures ────────
# Resets all three fixtures, then incrementally fills them with values
# that exercise every animation + status code path. Pair this with
# `just serve` in another terminal to watch the bars animate live.
test-drive-reset:
    just cli reset test-drive-lr            --yes
    just cli reset test-drive-bt-grouped    --yes
    just cli reset test-drive-bt-gradient   --yes

test-drive-fill:
    # LR: 3 simple bars
    just cli emit test-drive-lr --group alpha   --metric latency_ms --value 120
    just cli emit test-drive-lr --group bravo   --metric latency_ms --value 240
    just cli emit test-drive-lr --group charlie --metric latency_ms --value 180

    # BT grouped (solid): two metrics per group, slight delay so animation is visible
    just cli emit test-drive-bt-grouped --group alpha   --metric throughput --value 1200
    just cli emit test-drive-bt-grouped --group alpha   --metric latency    --value 45
    sleep 0.3
    just cli emit test-drive-bt-grouped --group bravo   --metric throughput --value 800
    just cli emit test-drive-bt-grouped --group bravo   --metric latency    --value 78
    sleep 0.3
    just cli emit test-drive-bt-grouped --group charlie --metric throughput --value 1500
    just cli emit test-drive-bt-grouped --group charlie --metric latency    --value 52

    # BT gradient: two metrics per group
    just cli emit test-drive-bt-gradient --group alpha   --metric prefill --value 1308
    just cli emit test-drive-bt-gradient --group alpha   --metric decode  --value 76
    sleep 0.3
    just cli emit test-drive-bt-gradient --group bravo   --metric prefill --value 720
    just cli emit test-drive-bt-gradient --group bravo   --metric decode  --value 104
    sleep 0.3
    just cli emit test-drive-bt-gradient --group charlie --metric prefill --value 1100
    just cli emit test-drive-bt-gradient --group charlie --metric decode  --value 92

# Coalesce test: 5 rapid updates → bar should land on the last value (500)
test-drive-coalesce:
    just cli emit test-drive-bt-grouped --group alpha --metric throughput --value 100
    just cli emit test-drive-bt-grouped --group alpha --metric throughput --value 200
    just cli emit test-drive-bt-grouped --group alpha --metric throughput --value 300
    just cli emit test-drive-bt-grouped --group alpha --metric throughput --value 400
    just cli emit test-drive-bt-grouped --group alpha --metric throughput --value 500
    @echo "expected: bar shows 500, no flicker through 100..400 (§14.1 buffering)"

# Newer-wins test: emit two points with REVERSED client_ts.
# Both timestamps must be within ±5 min of NOW (the backend rejects clock skew),
# so we compute them at recipe-run time. We send the NEWER one first then the
# OLDER one second; the bar must end on the value tied to the newer client_ts.
test-drive-newer-wins:
    #!/usr/bin/env bash
    set -euo pipefail
    NEWER=$(python3 -c "from datetime import datetime, timezone; print(datetime.now(timezone.utc).isoformat(timespec='microseconds'))")
    OLDER=$(python3 -c "from datetime import datetime, timezone, timedelta; print((datetime.now(timezone.utc) - timedelta(seconds=60)).isoformat(timespec='microseconds'))")
    echo "{\"group_key\":\"alpha\",\"metric_key\":\"latency_ms\",\"value\":999,\"client_ts\":\"$NEWER\"}" | just cli emit test-drive-lr --batch -
    echo "{\"group_key\":\"alpha\",\"metric_key\":\"latency_ms\",\"value\":111,\"client_ts\":\"$OLDER\"}" | just cli emit test-drive-lr --batch -
    echo "expected: bar shows 999 — newer client_ts wins even though it arrived second (§14.4)"

# Mark groups complete to flip pills
test-drive-complete:
    just cli complete test-drive-lr           --group alpha --group bravo --group charlie
    just cli complete test-drive-bt-grouped   --group alpha --group bravo
    just cli complete test-drive-bt-gradient  --group alpha
    @echo "expected: lr shows 3/3 complete, bt-grouped 2/3, bt-gradient 1/3"

# Full walkthrough = reset + fill + complete (the on-camera demo)
test-drive: test-drive-reset test-drive-fill test-drive-complete
    @echo "test-drive walkthrough complete — check the UI"
```

These recipes exist for two purposes: (a) the `integration-validator` agent invokes them in Layer 3 to drive the scripted scenario; (b) a human presenter can run them manually on camera to demo the platform without typing CLI commands one by one.

### Phase 2: Core Implementation
Three builders run in parallel against the spec, each owning one app end-to-end including its own unit tests:
- **Backend builder** writes db/store/broker/config/http_ingest/sse_stream/rest/main + pytest suites, with focus on the `client_ts` validation path in `http_ingest.py`, the `latest_per_cell` index lookup in `store.py`, and the SSE `Last-Event-ID` replay in `sse_stream.py`.
- **CLI builder** writes the click app, httpx client with `now_ts()` helper, all 7 subcommands, the dev fake-stream emitter, and tests focused on timestamp-stamping at read-time vs POST-time and outbox behaviour.
- **Frontend builder** writes the Vue 3 app: router, two pages, all 12 components, Pinia stores (with `latestClientTs` newer-wins guard), Zod schemas, 10 themes (`obsidian` matching the spec §13.2.1 mockup palette exactly), the hand-rolled SVG `GroupedBarChart` + `AnimatedBar` 1-second coalescing transition, and the gradient-defs emitter.

### Phase 3: Integration & Polish
A validator agent boots the full stack via `just serve` and walks the spec §10 example flow end-to-end: `GET /benchmarks` returns 5 entries, navigating to `/benchmark/gemma4-e4b-prefill-2026-04-07` opens an SSE stream, `live-bench emit` from a separate process produces a `datapoint` SSE event with all three timestamps, `live-bench complete` produces a `dataset_complete` event, restarting the backend mid-stream replays via `Last-Event-ID` without losing the bar's value. Reports any failures back to the team lead with file/line context so the relevant builder can be resumed.

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

No agents exist under `.claude/agents/team/`, so every team member uses the `general-purpose` agent type with a distinct **name** so the team lead can address each one individually and resume them with preserved context.

- Builder
  - Name: `scaffolder`
  - Role: Create the monorepo skeleton — root files (`.gitignore`, `README.md`, `justfile`), the `benchmarks/` directory with all five example YAMLs from spec §5, and the three empty app projects (`apps/backend/pyproject.toml`, `apps/cli/pyproject.toml`, `apps/frontend/package.json`) with their lockfiles initialised. No source code yet — only the project skeletons that the other builders will fill in.
  - Agent Type: `general-purpose`
  - Resume: true
- Builder
  - Name: `builder-models`
  - Role: Author `apps/backend/src/live_bench_server/models.py` (and the package `__init__.py` re-exports) per spec §4.2 verbatim. Includes all wire types, the `client_ts: datetime` field with microsecond ISO-8601 serialisation config, the `Color = str | list[str]` union, the `Better = Literal["higher","lower"]` literal, and the `BenchmarkFile` outer wrapper. This is the contract that backend and CLI will both depend on; no other module touches `models.py` after this task completes (changes are coordinated through this agent only).
  - Agent Type: `general-purpose`
  - Resume: true
- Builder
  - Name: `builder-backend`
  - Role: Implement the entire backend per spec §6 — `db.py`, `store.py`, `broker.py`, `config.py`, `http_ingest.py`, `sse_stream.py`, `rest.py`, `main.py`, `logging.py` — plus the three pytest files. Key correctness targets: (1) `http_ingest.py` validates `client_ts` is present, ISO-8601 parseable, within ±5 min of server clock and returns the right 4xx error codes from spec §9.1; (2) `store.insert_points` stamps `server_ts` + `seq` atomically; (3) `store.latest_per_cell` uses the `(session, group, metric, client_ts DESC)` index; (4) `sse_stream.py` honours `Last-Event-ID` for resume; (5) the in-proc broker fans out without dropping events under concurrent subscribers. Backend must boot cleanly with `uvicorn live_bench_server.main:app --port 8787` and reconcile the five YAMLs from `benchmarks/` into SQLite on startup.
  - Agent Type: `general-purpose`
  - Resume: true
- Builder
  - Name: `builder-cli`
  - Role: Implement the entire CLI per spec §7. Wire the path dep on `live-bench-server` in `pyproject.toml` so `models.py` is the single source of truth across both Python apps. Build all 7 commands (`list`, `show`, `reset`, `emit`, `complete`, `stream`, `tail`) with click. Critical: `client.py` exposes `now_ts() -> datetime` returning `datetime.now(timezone.utc)` with microseconds; `emit_cmd.py` and `stream_cmd.py` stamp `client_ts` at the moment of CLI arg parse / stdin line read, **not** at POST-build time; `client.py` implements 5xx retry with exponential backoff and the `.live-bench-outbox.jsonl` flush-on-failure path that preserves original `client_ts` on replay. Tests must cover the read-time timestamp-stamping invariant explicitly.
  - Agent Type: `general-purpose`
  - Resume: true
- Builder
  - Name: `builder-frontend`
  - Role: Implement the entire frontend per spec §8, §13, §14. Vue 3 + TS + Pinia + Zod + vue-router. Two routes: `/` (LandingPage with dropdown) and `/benchmark/:sessionId` (BenchmarkPage with SSE lifecycle). Hand-rolled SVG `GroupedBarChart` with `BarGradientDefs` (LR-flow `<linearGradient>` for array colours, evenly-spaced stops). `AnimatedBar` implements the §14.1 state machine (current/target/pending coalescing over 1s, `transitionend` flush). Session store implements §14.4 newer-wins on `client_ts`. Ten themes in `themes.css`, `obsidian` is default, palette matches spec §13.2.1 exactly. Play font from Google Fonts. Presentation-tuned font sizes from §13.1. NavBar order: brand on left; ConnectionBadge / LayoutSwitcher / ThemeSwitcher on right. Vitest drift test loads a JSON fixture that the backend builder must export from `apps/backend/tests/fixtures_export.py` (coordinate with builder-backend through the team lead).
  - Agent Type: `general-purpose`
  - Resume: true
- Validator
  - Name: `integration-validator`
  - Role: Owns **both** validation checkpoints. (a) `backend-cli-smoke` — terminal-only cross-app smoke run via `/drive` against the test-drive fixtures (no browser yet) — proves backend↔CLI wire shapes match before frontend matters. (b) `validate-all` — full integrated walk via `/drive` (process orchestration) + `playwright-bowser-agent` (browser DOM/SVG inspection) + `just test-drive-*` recipes, walking the 12-step sequence in task 7 with screenshot artifacts at every step. Writes `specs/validation-report.md` mapping every acceptance criterion to a pass/fail + screenshot path. Reports failures with file:line context so the relevant builder can be resumed for a fix. **Resume between checkpoints** so the second checkpoint inherits the context from the first.
  - Agent Type: `general-purpose`
  - Resume: true

## Step by Step Tasks

- IMPORTANT: Execute every step in order, top to bottom. Each task maps directly to a `TaskCreate` call.
- Before you start, run `TaskCreate` to create the initial task list that all team members can see and execute.

### 1. Scaffold Monorepo
- **Task ID**: `scaffold-monorepo`
- **Depends On**: none
- **Assigned To**: `scaffolder`
- **Agent Type**: `general-purpose`
- **Parallel**: false
- Read spec §3 (repo layout), §5 (YAML examples), §12 (justfile recipes), and 5.7 of this plan (test-drive fixtures + recipes).
- Create root `.gitignore` (Python venvs, `__pycache__`, `*.pyc`, `.pytest_cache`, node `node_modules`, `dist`, `*.db*`, `.live-bench-outbox.jsonl`, `screenshots/*.png`, OS scratch).
- Create root `README.md` with one-paragraph description, a `just serve` quick start, the **dedicated port table** (`backend = 8787`, `frontend dev = 5787`), the `just test-drive` walkthrough section, and a link to `spec/init_live_bench.md`.
- Create root `justfile` with:
  - **Top-of-file variables** declaring dedicated ports: `LB_BACKEND_PORT := "8787"`, `LB_FRONTEND_PORT := "5787"`. These are documented in the README.
  - **Self-clearing `backend` and `frontend` recipes** that kill any process holding their port before booting (see Notes for the exact `lsof | xargs kill -9` snippet). Both recipes pass `--port {{LB_*_PORT}}` to their underlying server.
  - A **`free-ports`** recipe that kills both ports without booting anything (used by `serve` and by the validators).
  - A **`ports`** recipe that prints which PIDs are holding each port (debug helper).
  - The `serve` recipe runs `free-ports` first, then `mprocs "just backend" "just frontend"` (or its fallback equivalent).
  - All other recipes from spec §12 verbatim (`cli`, `list`, `show`, `reset`, `emit`, `complete`, `test`, `build-frontend`, `demo-stream`).
  - The full `test-drive-*` recipe set from 5.7 above (`test-drive-reset`, `test-drive-fill`, `test-drive-coalesce`, `test-drive-newer-wins`, `test-drive-complete`, `test-drive`).
- Create `benchmarks/` directory and write all **8** YAML files: the 5 spec demos (`gemma4-e4b-prefill.yaml`, `gemma4-e4b-decode.yaml`, `gemma4-e4b-wall.yaml`, `m5-4way-tps.yaml`, `m5-pi-agent.yaml`) plus the **3 test-drive fixtures** (`test-drive-lr.yaml`, `test-drive-bt-grouped.yaml`, `test-drive-bt-gradient.yaml`) verbatim from 5.7 above.
- Create `apps/backend/pyproject.toml` (uv project, Python ≥3.12, deps: `fastapi`, `sse-starlette`, `uvicorn[standard]`, `pydantic>=2`, `pyyaml`; dev deps: `pytest`, `httpx`, `pytest-asyncio`). Run `uv sync` to materialise `uv.lock`.
- Create `apps/cli/pyproject.toml` (uv project, deps: `click`, `httpx`, `rich`, `pydantic>=2`; `[tool.uv.sources]` with `live-bench-server = { path = "../backend", editable = true }`; `[project.scripts]` with `live-bench = "live_bench_cli.cli:cli"`; dev deps: `pytest`). Do NOT run `uv sync` here yet — `live_bench_server` package doesn't exist until task 2.
- Create `apps/frontend/package.json` with deps: `vue@^3`, `vue-router@^4`, `pinia`, `zod`; devDeps: `vite`, `typescript`, `@vitejs/plugin-vue`, `vue-tsc`, `vitest`, `@types/node`, `@vue/test-utils`, `jsdom`. Add scripts: `dev` (must accept `--port` from CLI; vite respects the flag), `build`, `test`, `preview`. Run `pnpm install` to materialise the lockfile. Create `vite.config.ts` (with `server.port: 5787`, `server.strictPort: true`, and proxy entries forwarding `/benchmarks`, `/ingest`, `/stream`, `/healthz` → `http://127.0.0.1:8787`), `tsconfig.json`, `index.html` (with Google Fonts Play preconnect/preload from spec §13.1), and an empty `src/` directory.
- Create empty `apps/backend/src/live_bench_server/__init__.py` and `apps/cli/src/live_bench_cli/__init__.py` (placeholders only, real source comes in tasks 2–5).
- Verify `just --list` lists all the test-drive recipes; run `just ports` and confirm both ports report `free`; run `just free-ports` and confirm no error. Report done only after these three checks pass.

### 2. Shared Pydantic Models
- **Task ID**: `shared-models`
- **Depends On**: `scaffold-monorepo`
- **Assigned To**: `builder-models`
- **Agent Type**: `general-purpose`
- **Parallel**: false
- Read spec §4.2 in full and §15 (the why-client-timestamps section).
- Author `apps/backend/src/live_bench_server/models.py` containing every Pydantic model from §4.2 verbatim: `Direction`, `Better`, `Color`, `AxisConfig`, `MetricDef`, `GroupDef`, `BenchmarkConfig`, `BenchmarkFile`, `DataPoint`, `DataPointStored`, `DatasetStatus`, `DatasetState`, `IngestRequest`, `IngestResponse`, all `Sse*` models.
- Configure Pydantic v2 `model_config` so `datetime` fields serialise to ISO-8601 UTC with microsecond precision (e.g. `model_config = ConfigDict(json_encoders={datetime: lambda v: v.astimezone(timezone.utc).isoformat(timespec='microseconds')})` or equivalent v2 idiom). The wire format must be lexicographically sortable across all timestamps.
- Update `apps/backend/src/live_bench_server/__init__.py` to re-export the model names so `from live_bench_server.models import DataPoint` and `from live_bench_server import DataPoint` both work.
- Run `cd apps/backend && uv sync && uv run python -c "from live_bench_server.models import IngestRequest, DataPoint; from datetime import datetime, timezone; r = IngestRequest(session_id='x', request_ts=datetime.now(timezone.utc), points=[DataPoint(group_key='g', metric_key='m', value=1.0, client_ts=datetime.now(timezone.utc))]); print(r.model_dump_json())"` and verify the output has microsecond-precision ISO-8601 timestamps. Report exact JSON to the team lead.
- Now that `live_bench_server` exists, run `cd apps/cli && uv sync` to resolve the path dep and prove it imports.

### 3. Backend Implementation
- **Task ID**: `backend-impl`
- **Depends On**: `shared-models`
- **Assigned To**: `builder-backend`
- **Agent Type**: `general-purpose`
- **Parallel**: true (with `cli-impl` and `frontend-impl`)
- Read spec §1, §2, §4.1, §4.2, §6, §9, §10, §14.4, §15 in full.
- Write `db.py`: thin sqlite3 wrapper, `connect(path)`, `migrate()` runs the spec §4.1 schema (3 tables + 2 indexes), WAL mode on. Row → model helpers.
- Write `store.py`: `upsert_benchmark`, `list_benchmarks`, `get_benchmark`, `reset(session_id)`, `insert_points(session_id, points: list[DataPoint]) -> list[DataPointStored]` (assigns `seq` monotonically inside a write lock and stamps `server_ts = datetime.now(timezone.utc)`), `mark_complete(session_id, group_keys) -> list[tuple[str, datetime]]`, `dataset_states(session_id) -> list[DatasetState]` (derived from datapoints + completions, the `running` state requires `EXISTS (SELECT 1 FROM datapoints WHERE ...)`), `latest_per_cell(session_id) -> list[DataPointStored]` (uses the `ix_datapoints_cell_client_ts` index to fetch the newest stored point per `(group_key, metric_key)` cell — used by the SSE snapshot).
- Write `broker.py`: `LiveBroker` class with `subscribe(session_id) -> asyncio.Queue` and `publish(session_id, event)`. Multiple subscribers per session. Drop events for queues that overflow (configurable cap, default 1024) — log at WARN.
- Write `config.py`: `load_benchmarks_dir(path: Path) -> list[BenchmarkFile]` globs `*.yaml`, validates each via Pydantic, returns or raises `ConfigError(file, message)`.
- Write `http_ingest.py`: FastAPI router with `POST /ingest`. Handler validates session exists (404 `unknown_session`), every group/metric key against the live config (400 `unknown_group` / `unknown_metric`), every `client_ts` is present (400 `missing_client_ts`) and within ±5 min of server clock (400 `clock_skew`). On success: `store.insert_points` → publish one `SseDatapoint` per stored point → if `complete_groups` non-empty: `store.mark_complete` → publish one `SseDatasetComplete` per group → return `IngestResponse` with `seq_from`/`seq_to`/`completed`/`server_ts`. **The handler does not filter out-of-order points** — every insert is broadcast.
- Write `sse_stream.py`: `GET /stream/{session_id}` using `sse-starlette` `EventSourceResponse`. On connect: send `SseSnapshot` (config + `latest_per_cell` points + `dataset_states`); honour `Last-Event-ID` header by replaying `datapoints` with `seq > last`; subscribe to broker queue and forward live events. Each event's SSE `id:` field is the datapoint `seq` (or a synthetic counter for non-datapoint events that still survives reconnect — use the latest datapoint seq seen). Heartbeat comments every 15s.
- Write `rest.py`: `GET /benchmarks` returns `BenchmarkSummary[]` (id, title, subtitle, better, completed_count, total_count, last_update); `GET /benchmarks/{id}` returns `{config, points, datasets}`; `POST /benchmarks/{id}/reset` deletes datapoints + completions, broadcasts `SseReset`, returns `{reset: true, session_id}`; `GET /healthz` returns `{ok: true}`. **No POST /benchmarks** — creation is YAML-only.
- Write `logging.py`: structured logging setup; one DEBUG line per ingested point.
- Write `main.py`: build FastAPI app, mount the three routers (`rest`, `sse_stream`, `http_ingest`), startup hook opens DB at `./live-bench.db`, runs migrations, calls `config.load_benchmarks_dir(Path('../../benchmarks'))` and `store.upsert_benchmark` for each, shutdown hook closes DB. Uvicorn entry: `uvicorn live_bench_server.main:app --port 8787`.
- Write `tests/test_store.py`: insert_points assigns monotonic seqs, latest_per_cell returns the right newest values when client_ts arrives out of order, reset clears datapoints and completions but leaves benchmarks row.
- Write `tests/test_http_ingest.py`: happy-path 200 with correct response shape, 404 unknown_session, 400 unknown_group, 400 unknown_metric, 400 missing_client_ts, 400 clock_skew (point ts ±10 min from server clock).
- Write `tests/test_sse_stream.py`: snapshot on connect contains config + datasets, datapoint event arrives after a /ingest call, dataset_complete event arrives after a /ingest with `complete_groups`, reset event arrives after `/benchmarks/{id}/reset`, Last-Event-ID resume replays missed events.
- Write `tests/fixtures_export.py`: CLI script that imports models, builds one of every Pydantic model, dumps to JSON in `tests/fixtures/<model_name>.json`. The frontend drift test will load these — keep them in sync.
- Run `cd apps/backend && uv sync && uv run pytest -v` and `uv run python tests/fixtures_export.py` (writes `tests/fixtures/`). Report any failures to the team lead before marking complete.
- **Backend smoke (Layer 2, run before reporting done).** Use `/drive` to spawn `lb-backend` tmux session running `just backend` (which clears port 8787 and boots uvicorn). Poll for `Application startup complete`. From a `lb-probe` session: `curl -s http://127.0.0.1:8787/healthz` (expect `{"ok": true}`); `curl -s http://127.0.0.1:8787/benchmarks` (expect 8 entries — the 5 spec demos + 3 test-drive fixtures). POST to `/ingest` with a synthetic `client_ts` against `test-drive-lr` (group `alpha`, metric `latency_ms`, value `42`) and assert 200 with `seq_from=1, seq_to=1, server_ts` populated. `curl -s http://127.0.0.1:8787/benchmarks/test-drive-lr` and assert the new datapoint appears with `client_ts` preserved. Open a 5-second `curl -N http://127.0.0.1:8787/stream/test-drive-lr` in `lb-sse` session and capture the `snapshot` event. Tear down with `drive kill-session lb-backend lb-probe lb-sse`. Report the captured curl outputs in the completion message.

### 4. CLI Implementation
- **Task ID**: `cli-impl`
- **Depends On**: `shared-models`
- **Assigned To**: `builder-cli`
- **Agent Type**: `general-purpose`
- **Parallel**: true (with `backend-impl` and `frontend-impl`)
- Read spec §1, §7, §9, §10, §14.4, §15 in full.
- Write `client.py`: `LiveBenchClient` holds an `httpx.Client(base_url=..., timeout=10.0)` with HTTP/1.1 keep-alive on (default). `now_ts() -> datetime` helper returning `datetime.now(timezone.utc)`. Methods: `list_benchmarks()`, `get_benchmark(id)`, `reset(id)`, `ingest(req: IngestRequest) -> IngestResponse`. Retry on 5xx with exponential backoff (3 attempts, 100/300/900ms). On final failure write the unsent batch as JSONL to `.live-bench-outbox.jsonl` in CWD; on next successful invocation drain the outbox first **preserving each line's original `client_ts`** before sending the new payload.
- Write `cli.py`: click `@click.group()` with global `--server` (env `LIVE_BENCH_SERVER`, default `http://127.0.0.1:8787`) and `--verbose`. Wire all 7 subcommands by registering them from `commands/`.
- Write `commands/list_cmd.py`: `client.list_benchmarks()` → `rich.table.Table` with columns `session_id`, `title`, `subtitle`, `better`, `complete/total`, `last_update`.
- Write `commands/show_cmd.py`: `client.get_benchmark(id)` → printed config + a per-group matrix of latest values + status pills. Optional `--json` for raw output.
- Write `commands/reset_cmd.py`: `--yes` to skip prompt; `client.reset(id)`.
- Write `commands/emit_cmd.py`: two modes. Single: `--group/--metric/--value` → build one `DataPoint(client_ts=now_ts())`. Batch: `--batch <file|->` reads JSONL; for each line stamp `client_ts = now_ts()` **at the moment the line is read** unless the line carries its own `client_ts`. Build `IngestRequest(request_ts=now_ts(), points=[...])` → `client.ingest()`. Print accepted/seq summary.
- Write `commands/complete_cmd.py`: collect `--group` repeatedly → build `IngestRequest(request_ts=now_ts(), complete_groups=[...])` → POST.
- Write `commands/stream_cmd.py`: persistent stdin reader. Loop on `sys.stdin` lines; for each line stamp `client_ts = now_ts()` immediately (unless the line carries its own), append to a buffer. Every `--flush-ms` (default 50) or `--max-batch` (default 100) build an `IngestRequest` and call `client.ingest`. Recognise control lines `{"complete": "<group_key>"}` and route them into `complete_groups` of the next batch. EOF → final flush → exit.
- Write `commands/tail_cmd.py`: open `GET /stream/{id}` with `httpx.stream`, print each `event:` block with `client_ts` and `server_ts` for debugging.
- Write `dev/fake_stream.py`: synthetic data emitter for `just demo-stream`. Picks a random walk for each (group, metric) pair in a session, emits one point every 200ms for 60 seconds, then a `complete` per group. Routes through the same `LiveBenchClient` so it exercises the same code path.
- Write `tests/test_client.py`: `now_ts()` returns timezone-aware UTC; outbox flush on simulated 5xx and drain on next call preserves original `client_ts` (don't overwrite with replay time); retry backoff fires the right number of times.
- Write `tests/test_commands.py`: `emit` single produces one `DataPoint` with `client_ts` at-or-after a baseline `now()`; `stream` batches preserve order and stamps; `complete` produces an `IngestRequest` with empty `points` and the right `complete_groups`. Use a mock httpx transport.
- Run `cd apps/cli && uv sync && uv run pytest -v && uv run live-bench --help` and report results to the team lead.
- **CLI smoke (Layer 2, run before reporting done).** `/drive`: spawn `lb-backend` running `just backend` (kills port 8787 first), poll for ready. In `lb-cli` session: `LIVE_BENCH_SERVER=http://127.0.0.1:8787 uv run live-bench list` (expect 8 sessions); `live-bench emit test-drive-bt-grouped --group alpha --metric throughput --value 1200`; `live-bench show test-drive-bt-grouped` (assert the value landed and the `alpha` dataset shows status `running`); `live-bench complete test-drive-bt-grouped --group alpha`; `live-bench show` again (assert status `complete`); `live-bench reset test-drive-bt-grouped --yes`. In `lb-tail` session: `live-bench tail test-drive-bt-grouped` running concurrently with the emits, capture stdout, assert each emit produces a corresponding `event: datapoint` line with `client_ts` and `server_ts` fields. Tear down. Report captured outputs.

### 5. Frontend Implementation
- **Task ID**: `frontend-impl`
- **Depends On**: `scaffold-monorepo`
- **Assigned To**: `builder-frontend`
- **Agent Type**: `general-purpose`
- **Parallel**: true (with `backend-impl` and `cli-impl`)
- Read spec §1, §8, §9.2, §9.3, §10, §13, §14 in full.
- Set up Vite + Vue 3 + TS scaffolding inside `apps/frontend/src/` (the empty skeleton from task 1 has the config files in place).
- Write `schemas.ts`: Zod mirrors of every Pydantic model from spec §4.2 — `BenchmarkConfig`, `MetricDef`, `GroupDef`, `AxisConfig`, `DataPoint`, `DataPointStored`, `DatasetState`, `IngestResponse`, all `Sse*` event shapes. Export `parseSseEvent(raw: unknown)` returning a discriminated union over the `event` literal field.
- Write `themes.ts`: array of 10 theme entries `{name, label, swatch}` matching spec §13.2.2. Default `'obsidian'`.
- Write `styles/main.css`: import Play font, declare `:root` CSS custom properties from spec §13.1 (font sizes, radii, animation duration, easing).
- Write `styles/themes.css`: 10 `[data-theme="..."]` blocks. `obsidian` MUST match spec §13.2.1 verbatim — every `--bg`, `--bg-card`, `--border-card`, `--fg`, `--accent`, `--success`, `--bar-warm-a/b`, `--bar-cool-a/b`, all the pill colours. The other 9 themes can be derived from the table at the bottom of §13.2.2 (do not invent hex values for vibes you don't recognise — use the listed bg/accent and pick reasonable complements).
- Write `api/rest.ts`: typed fetch wrappers `listBenchmarks()`, `getBenchmark(id)`, `resetBenchmark(id)` returning Zod-parsed types.
- Write `api/stream.ts`: `connectStream(sessionId, handlers)`. Constructs `EventSource('/stream/' + sessionId)`. Handlers for `snapshot`, `datapoint`, `dataset_complete`, `reset`, `config_changed`. Tracks `lastEventId`. On `error`, closes and reconnects after backoff. Pass `Last-Event-ID` automatically (browser handles this if we set `id:` on every event server-side, which we do).
- Write `stores/benchmarks.ts`: Pinia store for the landing page, holds `list: BenchmarkSummary[]`, action `load()` calls `listBenchmarks()`.
- Write `stores/session.ts`: Pinia store for an active benchmark. State: `{config, points: DataPointStored[], latest: Map<string, number>, latestClientTs: Map<string, string>, datasets: Map<string, DatasetState>, lastUpdate: string | null}`. Actions: `applySnapshot(s)`, `applyDatapoint(p)` implementing the §14.4 newer-wins guard (`if (!prev || p.client_ts > prev) update`), `applyDatasetComplete(g, ts)`, `applyReset()` (clears latest/latestClientTs/datasets to pending). On reset, also reset the per-cell maps.
- Write `stores/prefs.ts`: reactive `theme: ThemeName` and `density: 'S'|'M'|'L'`. Defaults `'obsidian'` and `'M'`. Persist to `localStorage` on change. Apply theme by setting `document.documentElement.dataset.theme`.
- Write `router.ts`: `createRouter` with `createWebHistory()`, two routes: `/` → `LandingPage`, `/benchmark/:sessionId` → `BenchmarkPage` (props passed by route).
- Write `pages/LandingPage.vue`: on mount call `benchmarks store.load()`. Render a `<select>` of `{title — subtitle (session_id)}`; on change `router.push('/benchmark/' + id)`. If list is empty render `<EmptyState>` with message "No benchmarks found — drop a YAML file in `benchmarks/` and restart the server." No create UI.
- Write `pages/BenchmarkPage.vue`: on mount call `getBenchmark(id)` to hydrate the session store, then `connectStream(id, handlers)` wired to the store actions. On unmount close the SSE connection. Render a `<header>` with a "← Back" link to `/` and the session title; below it, a `<BenchmarkGrid>` containing one `<BenchmarkCard>` for the current session.
- Write `components/NavBar.vue`: brand "live-bench" on the left; right side in order `<ConnectionBadge/>`, `<LayoutSwitcher/>`, `<ThemeSwitcher/>`. Sticky.
- Write `components/LayoutSwitcher.vue`: 3-button toggle S/M/L bound to `prefs.density`.
- Write `components/ThemeSwitcher.vue`: dropdown showing each theme's swatch + label; updates `prefs.theme` and writes `document.documentElement.dataset.theme`.
- Write `components/ConnectionBadge.vue`: pill with coloured dot + label (`live`, `reconnecting`, `disconnected`) driven by SSE connection state from the session store or stream module.
- Write `components/BenchmarkGrid.vue`: CSS grid `grid-template-columns: repeat(var(--cols), minmax(0, 1fr))`. `--cols` derived from `prefs.density` and viewport width per spec §8.2 table.
- Write `components/BenchmarkCard.vue`: header stack from spec §8.3 — title (fs-large), subtitle (fs-medium dim), `"Higher is better"`/`"Lower is better"` line driven by `config.better`, then `<DatasetStatusBar>`. Body: `<GroupedBarChart>`. Footer: "last update Xs ago" computed from `session.lastUpdate`.
- Write `components/DatasetStatusBar.vue`: aggregate `{complete}/{total} complete` plus a horizontally scrollable row of per-group pills coloured `pending`/`running`/`complete`. Running pills get a subtle CSS pulse animation.
- Write `components/BarGradientDefs.vue`: emits `<defs>` containing one `<linearGradient id="grad-{session}-{metric}">` per metric whose `color` is an array. `x1=0 y1=0 x2=1 y2=0` (LR flow, fixed for v1). Stops evenly spaced across the array.
- Write `components/GroupedBarChart.vue`: receives `{config, latest, latestClientTs}` props from the session store. Computes scales (auto-fit `min(0, minValue)` to `max * 1.1` unless `y.min`/`y.max` set). Renders SVG with `<BarGradientDefs>`, axis lines, group labels, and one `<AnimatedBar>` per `(group, metric)` cell. Honours `direction: BT|LR`.
- Write `components/AnimatedBar.vue`: implements the §14.1 state machine. Local refs `{current, target, pending}`. Watches its prop `value`; on change applies the rules: idle → start animation; animating → set pending. Renders an SVG `<rect>` with CSS `transition: width var(--anim-bar) var(--ease-bar), height var(--anim-bar) var(--ease-bar), y var(--anim-bar) var(--ease-bar)`. Listens for `transitionend`; on fire commits `current = target` and either starts the pending animation or goes idle. The numeric overlay above the bar uses a `requestAnimationFrame` loop to ease from `current` to `target` in lockstep with the bar transition. Test that fast successive updates coalesce to the latest value.
- Write `components/EmptyState.vue`: simple empty-state with icon + message + optional CTA slot.
- Write `App.vue`: `<NavBar />` + `<RouterView />`.
- Write `main.ts`: bootstrap Vue, Pinia, router; on startup apply persisted theme (`document.documentElement.dataset.theme = prefs.theme ?? 'obsidian'`); mount.
- Write `schemas.test.ts`: vitest test that loads each JSON fixture from `apps/backend/tests/fixtures/<model>.json` (coordinate with `builder-backend` via the team lead — request the fixture path) and asserts the corresponding Zod schema's `parse()` succeeds. This is the drift test from spec §11. If fixtures are not yet available, write the test against inline literals matching spec §9.1/§9.2 examples and add a TODO to switch to fixtures once `backend-impl` exports them.
- Confirm `vite.config.ts` declares `server.port: 5787` and `server.strictPort: true`, plus proxy entries for `/benchmarks`, `/ingest`, `/stream`, `/healthz` → `http://127.0.0.1:8787` so the dev server forwards to the backend without CORS.
- Run `cd apps/frontend && pnpm install && pnpm test && pnpm build` and report any failures to the team lead.
- **Frontend smoke (Layer 2, run before reporting done).** `/drive`: spawn `lb-backend` (`just backend`, port 8787) and `lb-frontend` (`just frontend`, port 5787) in parallel. Poll both for ready signals. **Then `playwright-bowser-agent`**: load `http://127.0.0.1:5787/`. Assert the landing page renders with the brand "live-bench" in the nav, the dropdown contains 8 sessions including `test-drive-lr`, `test-drive-bt-grouped`, `test-drive-bt-gradient`. Click `test-drive-bt-gradient` and navigate; assert the URL becomes `/benchmark/test-drive-bt-gradient`; assert the card title reads `"Test Drive — Gradient Bars (BT)"`, the subtitle `"3 groups · 2 metrics · gradient colors"`, and `"Higher is better"` appears under the subtitle. Assert the `<DatasetStatusBar>` shows `0 / 3 complete` and 3 dim pending pills. Take a screenshot to `screenshots/frontend-smoke-empty.png`. Verify the SVG `<defs>` contains `<linearGradient>` elements (gradient defs were emitted). Tear down `drive` sessions. Report screenshot path + DOM assertions to the team lead.

### 6. Backend ↔ CLI Cross-App Smoke
- **Task ID**: `backend-cli-smoke`
- **Depends On**: `backend-impl`, `cli-impl`
- **Assigned To**: `integration-validator`
- **Agent Type**: `general-purpose`
- **Parallel**: false
- Catches wire-shape drift between backend and CLI **before** the frontend matters. Pure terminal — `/drive` only, no browser yet.
- `/drive` create session `lb-backend`, run `just backend` (which clears port 8787 and boots uvicorn), poll for `Application startup complete`. Verify the boot log lists all 8 reconciled benchmarks (5 spec + 3 test-drive).
- In `lb-cli` session: `cd apps/cli && uv run live-bench list` — assert the output table has 8 rows including all 3 `test-drive-*` sessions.
- Run `just test-drive-reset` — assert exit 0 and that all three test-drive sessions report 0 datapoints via `live-bench show`.
- Run `just test-drive-fill` — assert exit 0. For each test-drive session, run `live-bench show` and verify every (group, metric) cell now has a value with a `client_ts` populated, every group's status reads `running`.
- Run `just test-drive-coalesce`. Wait 1.5 s. Run `live-bench show test-drive-bt-grouped` — assert `alpha:throughput` reads `500` (the latest of the rapid 100→500 sequence). Note: this proves the wire shape, not the animation; animation coalescing is verified in the frontend smoke + Layer 3.
- Run `just test-drive-newer-wins`. Run `live-bench show test-drive-lr` — assert `alpha:latency_ms` reads `999` (the entry with the *newer* `client_ts` of `2030-01-01`), not `111` (the older `2020-01-01`). This proves the CLI passes through explicit `client_ts` from JSONL and the backend stores both points but the latest-by-`client_ts` wins.
- Run `just test-drive-complete`. Run `live-bench show` against each test-drive session and assert per-group statuses match expectation: `lr` 3/3 complete, `bt-grouped` 2/3 complete, `bt-gradient` 1/3 complete.
- `/drive` open `lb-sse` session running `live-bench tail test-drive-bt-grouped` — leave it streaming. From `lb-cli`, emit a single new point (`live-bench emit test-drive-bt-grouped --group charlie --metric throughput --value 1700`). Read recent `lb-sse` output via `drive read` — assert a `datapoint` line appeared with `client_ts`, `server_ts`, and `seq` fields populated.
- Kill `lb-backend` (`drive kill-session lb-backend`). Wait 2 s. Restart with `just backend`. Reconnect `lb-sse` with `live-bench tail test-drive-bt-grouped` — assert the snapshot reflects the prior `charlie:throughput=1700` value (proves SQLite persistence + `latest_per_cell` snapshot).
- Run `just free-ports` to clean up. Tear down all `drive` sessions.
- If any assertion fails, report file:line context (`http_ingest.py` for ingest errors, `store.py` for value mismatch, `client.py` for CLI request shape) so the relevant builder can be resumed. If all pass, mark this task complete and unblock `validate-all`.

### 7. Full Integration Validation
- **Task ID**: `validate-all`
- **Depends On**: `backend-impl`, `cli-impl`, `frontend-impl`, `backend-cli-smoke`
- **Assigned To**: `integration-validator`
- **Agent Type**: `general-purpose`
- **Parallel**: false
- Read spec §10 (end-to-end flow) and §17 (success criteria) in full. This task uses **`/drive` for processes** and **`playwright-bowser-agent` for the browser** in parallel.
- **Step 0 — unit-test gate.** Run `cd apps/backend && uv run pytest -v`, `cd apps/cli && uv run pytest -v`, `cd apps/frontend && pnpm test`, `cd apps/frontend && pnpm build`. Capture pass/fail counts. If any fail, halt and report.
- **Step 1 — boot the stack via `/drive`.** Open four sessions in parallel:
  - `lb-backend` running `just backend` (kills port 8787, boots uvicorn). Poll for `Application startup complete`.
  - `lb-frontend` running `just frontend` (kills port 5787, boots vite). Poll for `Local: http://`.
  - `lb-tail` ready to run `live-bench tail` on demand.
  - `lb-emitter` ready to run `live-bench emit / complete / reset` on demand.
- **Step 2 — initial state via `playwright-bowser-agent`.** Load `http://127.0.0.1:5787/`. Assert dropdown lists 8 sessions. Navigate to `/benchmark/test-drive-bt-gradient`. Screenshot baseline → `screenshots/01-empty-bt-gradient.png`. Read the rendered SVG and assert all 6 `<rect>` bar elements have height/width near 0 (empty initial state).
- **Step 3 — first emit (visual).** From `lb-emitter`: `just test-drive-fill` (or just one emit if you want to single-step). Wait 1.5 s for animation to settle. Take screenshot → `02-filled-bt-gradient.png`. Read the SVG `<rect>` height attributes for `alpha:prefill` (expected ~1308 → scaled bar height ≠ 0) and `bravo:decode` (expected ~104). Assert non-zero.
- **Step 4 — coalesce test (visual).** From `lb-emitter`: `just test-drive-coalesce`. Wait 1.5 s. Read the `alpha:throughput` bar value via the numeric overlay text element. Assert it reads `500`. Screenshot → `03-coalesced-bt-grouped.png`.
- **Step 5 — newer-wins test (the AC-Order proof).** From `lb-emitter`: `just test-drive-newer-wins`. Wait 1.5 s. Read the `alpha:latency_ms` bar value on the LR chart. Assert it reads `999`, not `111`. Screenshot → `04-newer-wins-lr.png`.
- **Step 6 — dataset complete (pill flip).** From `lb-emitter`: `just test-drive-complete`. Playwright reads the `<DatasetStatusBar>` for each test-drive session and asserts `aria-label`/text reflects: lr `3 / 3 complete`, bt-grouped `2 / 3 complete`, bt-gradient `1 / 3 complete`. Screenshot the bt-grouped card → `05-pills-mixed-bt-grouped.png`.
- **Step 7 — restart-resilience (the AC4 proof).** Read the current numeric overlay values from the bt-gradient card. `drive kill-session lb-backend`. Wait 2 s. `drive new-session lb-backend just backend`. Poll for ready. Playwright observes the `<ConnectionBadge>` cycling amber (`reconnecting`) → green (`live`). After SSE reconnects, read the numeric overlays again — assert they still match the values from before the kill (proves `latest_per_cell` snapshot + `Last-Event-ID` resume). Screenshot → `06-after-restart.png`.
- **Step 8 — theme cycle (the AC6 proof).** Playwright clicks `ThemeSwitcher` and selects `matrix`. Screenshot → `07-theme-matrix.png`. Assert `document.documentElement.dataset.theme === 'matrix'`. Repeat for `sunset` → `08-theme-sunset.png` and back to `obsidian` → `09-theme-obsidian.png`. Assert page does not crash and bars retain their values across all switches.
- **Step 9 — density cycle.** Playwright clicks `LayoutSwitcher` through S → M → L. Screenshot each → `10-density-S.png`, `11-density-M.png`, `12-density-L.png`. Assert the grid `--cols` CSS variable changes per spec §8.2.
- **Step 10 — reset wipe.** From `lb-emitter`: `just cli reset test-drive-bt-gradient --yes`. Wait 1.5 s. Read the SVG; assert all bars animate back to 0. Read `<DatasetStatusBar>`; assert `0 / 3 complete` and all pills `pending`. Screenshot → `13-after-reset.png`.
- **Step 11 — clean teardown.** `drive kill-session lb-backend lb-frontend lb-tail lb-emitter`. Run `just free-ports` and `just ports`; assert both ports report `free`.
- **Step 12 — write the validation report.** Compose `specs/validation-report.md` containing a markdown table with one row per AC (AC1..AC6 + AC-Schema + AC-Order + AC-Tests), each with pass/fail, the screenshot path that proves it, and a one-line note. Append the captured stdout from the unit test runs and the integration steps. Hand the report path back to the team lead. Any failures must include a file:line pointer to the most likely culprit so the relevant builder can be resumed for a fix.

## Acceptance Criteria

These mirror spec §17 verbatim — the build is done when all six are demonstrably true.

- **AC1.** Cold-start to first bar moving on camera is ≤ 60 seconds. `just serve` → open browser → pick a benchmark from the dropdown → one `live-bench emit` → bar animates smoothly to the new value within 1 second.
- **AC2.** YAML is the only thing the user edits to add a benchmark. Dropping a new file in `benchmarks/` and restarting the server results in the new benchmark appearing in the landing dropdown. No source-code change required.
- **AC3.** The reference mockup (prefill / decode / wall) is faithfully reproducible using the three example YAMLs and the `obsidian` theme. Bars, gradients, status pills, and "Higher/Lower is better" labels render correctly without per-card customisation. Numeric overlays render in the bar's primary colour at `--fs-xlarge`.
- **AC4.** A mid-run server restart is invisible to the camera. SSE reconnects automatically, bars redraw to exactly where they were (driven by `latest_per_cell` snapshot + `Last-Event-ID` resume), new points keep flowing without flicker.
- **AC5.** The CLI fits in one `uv tool install ./apps/cli` and works from any benchmark script on the LAN with `LIVE_BENCH_SERVER=http://<dashboard-host>:8787 live-bench emit ...`. Timestamps are stamped at CLI invocation time, not POST-build time.
- **AC6.** Presenter can flip theme and density mid-stream without dropping a frame. All 10 themes are selectable from the nav bar and persist to localStorage.
- **AC-Schema.** Backend's `client_ts` validation rejects missing timestamps with `400 missing_client_ts` and >±5 min skew with `400 clock_skew`. Verified by `test_http_ingest.py`.
- **AC-Order.** Out-of-order datapoints (older `client_ts` arriving after newer) do NOT regress the bar. Verified two ways: (a) `backend-cli-smoke` runs `just test-drive-newer-wins` and asserts `live-bench show` reports `999`; (b) `validate-all` step 5 has `playwright-bowser-agent` read the rendered SVG numeric overlay and assert it shows `999` not `111`.
- **AC-Tests.** All unit tests pass: `cd apps/backend && uv run pytest`; `cd apps/cli && uv run pytest`; `cd apps/frontend && pnpm test`. Frontend `pnpm build` succeeds with zero TypeScript errors.
- **AC-Ports.** `just backend` and `just frontend` reliably free their port (`8787` and `5787` respectively) before booting; running them twice in a row never fails with `EADDRINUSE`. `just ports` reports both ports with the holding PID or `free`. `just free-ports` is a no-op when nothing is running and a clean kill when something is.
- **AC-TestDrive.** The 8 YAML files in `benchmarks/` (5 spec demos + 3 test-drive fixtures) all reconcile cleanly into SQLite on backend boot. `just test-drive` (which runs reset → fill → complete) completes with exit 0 against a freshly booted server, and the resulting state matches the assertions in task 6.
- **AC-Smoke.** Each builder's per-app smoke (Layer 2 in *Validation Strategy*) passes before that builder reports its task done. `backend-cli-smoke` (task 6) passes before `validate-all` is unblocked.

## Validation Commands

Execute these commands to validate the task is complete. Grouped by layer.

### Layer 1 — unit tests (in each builder's task)
- `cd apps/backend && uv sync && uv run pytest -v` — backend unit tests pass.
- `cd apps/backend && uv run python tests/fixtures_export.py` — fixture JSON files written for the frontend drift test.
- `cd apps/cli && uv sync && uv run pytest -v` — CLI unit tests pass.
- `cd apps/cli && uv run live-bench --help` — CLI binary is wired and click app loads.
- `cd apps/frontend && pnpm install && pnpm test` — frontend vitest passes including Zod drift test, AnimatedBar coalesce test, and store newer-wins test.
- `cd apps/frontend && pnpm build` — production build succeeds with zero TypeScript errors.
- `cd apps/backend && uv run python -c "from live_bench_server.main import app; print(app.routes)"` — backend module imports cleanly.

### Layer 2 — per-app smoke (run via `/drive`)
- `just ports` — reports `free` for both 8787 and 5787 before any boot.
- `just backend` — kills port 8787 first, boots uvicorn, reconciles 8 YAMLs.
- `curl -s http://127.0.0.1:8787/healthz` → `{"ok": true}`.
- `curl -s http://127.0.0.1:8787/benchmarks | python -m json.tool` → 8 entries.
- `cd apps/cli && uv run live-bench list` → 8-row table.
- `cd apps/cli && uv run live-bench emit test-drive-lr --group alpha --metric latency_ms --value 42` → 200 OK with `server_ts`.
- `cd apps/cli && uv run live-bench show test-drive-lr` → shows the value with `client_ts`.
- `just frontend` — kills port 5787 first, boots vite on 5787 (strict).
- `curl -s http://127.0.0.1:5787/` → returns the Vite-served HTML shell.

### Layer 3 — full integration (run by `validate-all`)
- `just free-ports && just serve` from repo root — backend + frontend boot together with no port conflicts.
- `just test-drive-reset` → all 3 test-drive sessions report 0 datapoints.
- `just test-drive-fill` → bars animate to expected values; `live-bench show` matches.
- `just test-drive-coalesce` → `alpha:throughput` reads `500` after settle.
- `just test-drive-newer-wins` → `alpha:latency_ms` reads `999` (newer-wins proof).
- `just test-drive-complete` → status pills flip per task 7 step 6.
- `just test-drive` (the meta-recipe) → reset + fill + complete in one shot, exit 0.
- Restart backend mid-stream via `/drive` (`drive kill-session lb-backend && drive new-session lb-backend just backend`) — bars retain their values after SSE reconnect (verified via playwright SVG read).
- `just free-ports && just ports` — both ports reported `free` after teardown.

## Notes

- **Dedicated ports + self-clearing recipes.** Two long-lived services, two dedicated ports — no other live-bench process binds a port:
  - `LB_BACKEND_PORT  := "8787"` (FastAPI / uvicorn)
  - `LB_FRONTEND_PORT := "5787"` (Vite dev server — overrides Vite's default `5173` so we never collide with another local Vite project)
  - Both `just backend` and `just frontend` MUST kill any process holding their port before booting. Canonical recipe pattern (macOS / Linux, `lsof` available):
    ```just
    LB_BACKEND_PORT  := "8787"
    LB_FRONTEND_PORT := "5787"

    # Kill any process holding either live-bench port. No-op if nothing's listening.
    free-ports:
        @echo "Freeing live-bench ports {{LB_BACKEND_PORT}} and {{LB_FRONTEND_PORT}}..."
        -@lsof -ti:{{LB_BACKEND_PORT}}  2>/dev/null | xargs -r kill -9 2>/dev/null || true
        -@lsof -ti:{{LB_FRONTEND_PORT}} 2>/dev/null | xargs -r kill -9 2>/dev/null || true

    # Show what's holding the live-bench ports (debug helper).
    ports:
        @printf "backend  port {{LB_BACKEND_PORT}}: %s\n" "$$(lsof -ti:{{LB_BACKEND_PORT}}  2>/dev/null || echo free)"
        @printf "frontend port {{LB_FRONTEND_PORT}}: %s\n" "$$(lsof -ti:{{LB_FRONTEND_PORT}} 2>/dev/null || echo free)"

    # Boot the backend; clears its port first so re-running is safe.
    backend:
        -@lsof -ti:{{LB_BACKEND_PORT}} 2>/dev/null | xargs -r kill -9 2>/dev/null || true
        cd apps/backend && uv run uvicorn live_bench_server.main:app --reload --port {{LB_BACKEND_PORT}}

    # Boot the frontend; clears its port first so re-running is safe.
    frontend:
        -@lsof -ti:{{LB_FRONTEND_PORT}} 2>/dev/null | xargs -r kill -9 2>/dev/null || true
        cd apps/frontend && pnpm dev --port {{LB_FRONTEND_PORT}} --strictPort

    serve: free-ports
        mprocs "just backend" "just frontend"
    ```
  - The leading `-` on each command means just ignores a non-zero exit (so missing-process is fine). The `xargs -r` skips when stdin is empty (no PIDs to kill). The `2>/dev/null || true` is defensive in case `lsof` is missing on a non-mac runner.
  - The CLI doesn't bind a port; the test-drive recipes don't need any port management. Only `backend` and `frontend` are long-lived.
  - The README documents the port table prominently so users running multiple projects know where to look.
- **No external services.** Everything is in-process: SQLite for persistence, asyncio queues for the broker, no Redis, no message bus.
- **Python deps to add (backend):** `uv add fastapi sse-starlette 'uvicorn[standard]' 'pydantic>=2' pyyaml` and dev: `uv add --dev pytest pytest-asyncio httpx`.
- **Python deps to add (cli):** `uv add click httpx rich 'pydantic>=2'` and dev: `uv add --dev pytest`. The path dep on `live-bench-server` is declared in `pyproject.toml` directly under `[tool.uv.sources]` rather than via `uv add` to keep it editable.
- **Node deps to add (frontend):** `pnpm add vue@^3 vue-router@^4 pinia zod` and dev: `pnpm add -D vite typescript @vitejs/plugin-vue vue-tsc vitest @types/node @vue/test-utils jsdom`.
- **Path dep gotcha.** The CLI's `[tool.uv.sources]` table needs `live-bench-server = { path = "../backend", editable = true }`. The `[project] dependencies` list must also include `live-bench-server` (without a version) so uv knows to resolve it. `uv sync` in `apps/cli/` will fail until `apps/backend/src/live_bench_server/__init__.py` exists with at least `models.py` importable — this is why task 2 exists between scaffold and the parallel implementation tasks.
- **SQLite path.** Backend uses `./live-bench.db` relative to the working directory the backend was launched from (which is `apps/backend` via `just backend`). Add `live-bench.db*` to root `.gitignore`.
- **`mprocs` is optional.** The `just serve` recipe in spec §12 uses mprocs; if it's not installed, document the fallback in the root README ("`just backend` and `just frontend` in two terminals").
- **Out of scope (per spec §16).** Do not implement: hot YAML reload (`config.watch`), point retention caps, multi-process broker, per-runner deduplication, gradient direction configurability. These are explicitly deferred.
- **Coordination point: backend → frontend fixtures.** `builder-backend` writes JSON fixtures via `tests/fixtures_export.py` that `builder-frontend` consumes in the Zod drift test. The team lead must surface the fixture file paths from `builder-backend` to `builder-frontend` once `backend-impl` reaches that point. If the parallel work race has the frontend ready first, the frontend test starts with inline fixtures and is updated to file-based later — track this with a follow-up nudge to `builder-frontend` after `backend-impl` completes.
- **Reference benchmark scripts** in `experimental/gemma4/bench/` and `experimental/pi-agent-playground-v2/bench/` are read-only context for understanding what data shapes will be emitted. The platform must NOT depend on or import from them.
- **Spec is law.** Any builder that finds the spec ambiguous or contradictory must report back to the team lead with the section number and the specific question — do NOT improvise schema or wire format changes.

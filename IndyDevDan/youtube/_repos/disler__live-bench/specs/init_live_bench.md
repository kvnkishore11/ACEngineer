# Live Bench — Initial Spec

**Status:** draft / planning only (no code yet)
**Owner:** @indydevdan
**Date:** 2026-04-07
**Driving use case:** the M5 Max / M4 × Qwen 3.5 / Gemma 4 × GGUF / MLX matrix from the launch video.
**Related prior art:** earlier `gemma4/bench/` and `pi-agent-playground-v2/bench/` experiments (prefill / decode / wall-time CSV shapes, 4-way and context-scaling benchmarks) — kept in private sibling repos, not part of this codebase.

---

## 1. What we're building

A **general-purpose live benchmarking platform** for devices on the LAN. Benchmark scripts running anywhere on the local network push results to a central server; a Vue UI shows them as live-updating grouped bar charts. The server reads one YAML file per benchmark from a `benchmarks/` directory on boot and registers them in SQLite. The UI lists them on a landing page; clicking one navigates to `/benchmark/:session_id` and attaches to the live stream.

The m5 benchmark is the first user of the platform, but the platform is **not coupled to LLM benchmarks**. Anything that emits `(group, metric, value)` tuples and optional `(group) → complete` signals can drive a chart.

### Concrete ask

- Drop a `benchmarks/gemma4-e4b-prefill.yaml` file in the project. Restart `just serve`.
- Landing page dropdown lists it.
- Click it → `/benchmark/gemma4-e4b-prefill-2026-04-07` opens, empty bars waiting.
- Benchmark scripts on M4 / M5 call `uv run live-bench emit <session_id> --group gguf --metric prefill --value 1308`. The CLI stamps `client_ts` at the instant of the call and POSTs to `/ingest`; the backend stores it, assigns a `seq`, and broadcasts via SSE.
- Bar smoothly animates over 1 s. New values coalesce — only the latest (by `client_ts`, not arrival order) is ever animated toward.
- When that dataset finishes, script calls `live-bench complete <session_id> --group gguf`. Group gets a "complete" pill; card header shows `1 / 2 complete`.
- Card shows "Higher is better" or "Lower is better" under the subtitle, driven by a `better:` field in the YAML.
- Presenter flips density S/M/L and theme from the nav bar. Play font, presentation-sized defaults. Default theme is **obsidian** — the dark slate look from the reference mockup.

### Non-goals

- No auth, no users, no multi-tenant anything.
- No "write your own chart type" framework. **Grouped bar charts only.**
- No remote (WAN) support, no TLS. LAN-only, trust the network.
- No historical analytics / query UI. Current session state is what you see; SQLite exists only to survive a reconnect or crash.
- Not a benchmark *orchestrator*. It does not run the benchmarks — it only receives and displays results.
- **No UI-side creation.** The UI cannot create, rename, or delete benchmarks. YAML files in `benchmarks/` are the only way to introduce a new benchmark. If the DB has zero benchmarks on boot, the landing page shows "No benchmarks found — drop a YAML file in `benchmarks/` and restart."

---

## 2. Architecture at a glance

```
 ┌──────────────┐  HTTP POST    ┌─────────────────────┐   SSE    ┌──────────────┐
 │ live-bench   │──────────────▶│  backend (FastAPI)   │─────────▶│ frontend     │
 │ CLI (uv)     │   /ingest     │  - REST ingest       │  /stream │ (Vite Vue-TS)│
 │              │               │  - REST control      │          │              │
 │ bench script │               │  - SSE broadcast     │          │ / (landing)  │
 │ on M4/M5/... │   GET/POST    │  - SQLite store      │          │ /benchmark/: │
 └──────────────┘──────────────▶│                     │          │    sessionId │
                  /list,/show   │ benchmarks/*.yaml →  │          └──────────────┘
                  /reset,...    │   load on boot       │
                                └──────────┬───────────┘
                                           │
                                     ┌─────▼─────┐
                                     │ SQLite    │
                                     │ 3 tables  │
                                     └───────────┘
```

### Transport decisions

| Direction | Transport | Why |
|---|---|---|
| CLI → backend (ingest) | **HTTP POST** `/ingest` | Stateless, one-shot friendly, httpx keep-alive handles the "socket-per-emit" concern. Batching is a request shape, not a protocol concern. Zero session management. See §15 for the full trade-off vs WebSocket. |
| Backend → frontend (live updates) | **SSE** `/stream/:sessionId` | Fan-out to N browser tabs is trivial; browsers auto-reconnect with `Last-Event-ID`; one-way is exactly what the UI needs. |
| CLI ↔ backend (control) | **REST/JSON** | `list`, `show`, `reset`, `complete` are one-shots, already HTTP. |

> **Transport note:** We originally considered WebSocket for ingest. HTTP POST won because opening/closing sockets for single events is a bad fit for the CLI's primary use case ("bench script emits one metric, exits"). HTTP/1.1 keep-alive + httpx client reuse gives streaming-like throughput without the WS state. **This decision is open — see §15.**

---

## 3. Repo layout

Root stays app-agnostic. Each app is self-contained with its own lockfile.

```
live-bench/
├── .gitignore
├── README.md                       # one-page: what it is, quick start
├── justfile                        # top-level recipes that call into apps/*
├── benchmarks/                     # ← the only source of benchmark definitions
│   ├── gemma4-e4b-prefill.yaml
│   ├── gemma4-e4b-decode.yaml
│   ├── gemma4-e4b-wall.yaml
│   ├── m5-4way-tps.yaml
│   └── m5-pi-agent.yaml
├── spec/
│   └── init_live_bench.md          # this file
└── apps/
    ├── backend/
    │   ├── pyproject.toml          # uv, Python 3.12+
    │   ├── uv.lock
    │   ├── README.md
    │   ├── src/
    │   │   └── live_bench_server/
    │   │       ├── __init__.py
    │   │       ├── main.py         # FastAPI app, routes wired, uvicorn entry
    │   │       ├── config.py       # benchmarks/*.yaml loader
    │   │       ├── models.py       # Pydantic: BenchmarkConfig, DataPoint, ...
    │   │       ├── db.py           # sqlite3 connection, migrations, 3 tables
    │   │       ├── store.py        # repository pattern over db.py
    │   │       ├── http_ingest.py  # POST /ingest handler
    │   │       ├── sse_stream.py   # GET /stream/:session_id SSE handler
    │   │       ├── rest.py         # /list /show /reset /stats /healthz
    │   │       ├── broker.py       # in-proc pub/sub fanout (asyncio.Queue)
    │   │       └── logging.py
    │   └── tests/
    │       ├── test_store.py
    │       ├── test_http_ingest.py
    │       └── test_sse_stream.py
    │
    ├── cli/
    │   ├── pyproject.toml          # uv project, exposes `live-bench` script
    │   ├── uv.lock
    │   ├── README.md
    │   └── src/
    │       └── live_bench_cli/
    │           ├── __init__.py
    │           ├── __main__.py
    │           ├── cli.py          # click app, command dispatch
    │           ├── client.py       # httpx.Client wrapper (reused across calls)
    │           ├── models.py       # re-exports shared Pydantic models
    │           └── commands/
    │               ├── list_cmd.py
    │               ├── show_cmd.py
    │               ├── reset_cmd.py
    │               ├── emit_cmd.py
    │               ├── complete_cmd.py
    │               ├── stream_cmd.py
    │               └── tail_cmd.py
    │
    └── frontend/
        ├── package.json            # vite + vue 3 + ts + pinia + zod + vue-router
        ├── pnpm-lock.yaml
        ├── tsconfig.json
        ├── vite.config.ts
        ├── index.html              # preloads Play font from Google Fonts
        ├── README.md
        └── src/
            ├── main.ts
            ├── App.vue             # <RouterView /> + global NavBar
            ├── router.ts           # 2 routes: / and /benchmark/:sessionId
            ├── schemas.ts          # Zod mirrors of backend Pydantic models
            ├── themes.ts           # 10 themes (obsidian is default)
            ├── api/
            │   ├── rest.ts
            │   └── stream.ts       # SSE manager + reconnect
            ├── stores/
            │   ├── benchmarks.ts   # list of configs (landing page)
            │   ├── session.ts      # per-session live data (benchmark page)
            │   └── prefs.ts        # theme + density, localStorage persisted
            ├── pages/
            │   ├── LandingPage.vue
            │   └── BenchmarkPage.vue
            ├── components/
            │   ├── NavBar.vue
            │   ├── LayoutSwitcher.vue
            │   ├── ThemeSwitcher.vue
            │   ├── ConnectionBadge.vue
            │   ├── BenchmarkGrid.vue
            │   ├── BenchmarkCard.vue
            │   ├── DatasetStatusBar.vue
            │   ├── GroupedBarChart.vue
            │   ├── BarGradientDefs.vue
            │   ├── AnimatedBar.vue
            │   └── EmptyState.vue
            └── styles/
                ├── main.css         # base, CSS vars, Play font, presentation sizes
                └── themes.css       # 10 theme blocks driven by [data-theme]
```

### Why separated apps (not a monorepo package manager)

- Each app gets its own lockfile and CI surface; no cross-contamination between Python and node deps.
- The CLI is a shippable `uv tool install` target, independent of the server.
- Root `justfile` is the only place that knows about all three.

---

## 4. Data model

### 4.1 SQLite — three tables

```sql
-- apps/backend/src/live_bench_server/db.py (migration 001)

CREATE TABLE benchmarks (
    session_id   TEXT PRIMARY KEY,
    title        TEXT NOT NULL,
    subtitle     TEXT,
    better       TEXT NOT NULL,        -- 'higher' | 'lower'
    config_json  TEXT NOT NULL,        -- full BenchmarkConfig serialized
    source_path  TEXT,                  -- benchmarks/<name>.yaml, for diagnostics
    created_at   INTEGER NOT NULL,
    updated_at   INTEGER NOT NULL
);

CREATE TABLE datapoints (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id   TEXT NOT NULL REFERENCES benchmarks(session_id) ON DELETE CASCADE,
    group_key    TEXT NOT NULL,
    metric_key   TEXT NOT NULL,
    value        REAL NOT NULL,
    seq          INTEGER NOT NULL,       -- monotonic per session (SSE Last-Event-ID)
    client_ts    TEXT NOT NULL,           -- ISO-8601 UTC with μs, set by the CLI at emit time
    server_ts    INTEGER NOT NULL         -- unix ms, set by the backend on insert
);
CREATE INDEX ix_datapoints_session_seq   ON datapoints(session_id, seq);
CREATE INDEX ix_datapoints_cell_client_ts ON datapoints(session_id, group_key, metric_key, client_ts DESC);

CREATE TABLE completions (
    session_id    TEXT NOT NULL REFERENCES benchmarks(session_id) ON DELETE CASCADE,
    group_key     TEXT NOT NULL,
    completed_at  INTEGER NOT NULL,
    PRIMARY KEY (session_id, group_key)
);
```

**Dataset status is derived, not stored separately.** Three states per `(session_id, group_key)`:
- `complete` — row exists in `completions`.
- `running` — no completion row, but at least one datapoint row for that group.
- `pending` — no completion row and no datapoints.

`better` is denormalised onto the `benchmarks` row (in addition to living inside `config_json`) so `GET /benchmarks` can cheaply include it in the landing-page list without deserialising the full config.

**Why two timestamps?** `client_ts` is the ground truth for *value ordering* — it's stamped by the CLI at the moment the benchmark runner produced the point, before any batching or network delay. `server_ts` is the arrival time on the backend, used for "last update X seconds ago" footers and operational logging. The bar chart's "newest wins" logic runs off `client_ts`, not arrival order (see §14.4). Clocks are trusted for a LAN (NTP keeps Macs in sync to the millisecond); if drift ever matters we add a handshake-based offset, but v1 trusts the wall clock.

**Reset semantics.** `POST /benchmarks/:id/reset` deletes all rows in `datapoints` and `completions` for that session, bumps `benchmarks.updated_at`, broadcasts a `reset` SSE event. The `benchmarks` row stays (config is owned by YAML).

**YAML → DB reconciliation on boot.** For each file in `benchmarks/*.yaml`:
- Validate against `BenchmarkFile`.
- If `session_id` not in DB → insert, status pending.
- If `session_id` in DB with *identical* `config_json` → no-op.
- If `session_id` in DB with *different* `config_json` → update config, keep datapoints (warn in logs that shapes may mismatch — user can `reset` if needed).

### 4.2 Pydantic models — `apps/backend/src/live_bench_server/models.py`

```python
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

Direction = Literal["LR", "BT"]          # bar growth direction
Better    = Literal["higher", "lower"]    # which direction means "good"
Color     = str | list[str]               # "#rrggbb" or ["#a","#b","#c"]

class AxisConfig(BaseModel):
    label: str
    unit:  str | None = None
    min:   float | None = None
    max:   float | None = None

class MetricDef(BaseModel):
    key:   str
    label: str
    color: Color | None = None

class GroupDef(BaseModel):
    key:   str
    label: str

class BenchmarkConfig(BaseModel):
    session_id: str
    title:      str
    subtitle:   str | None = None
    better:     Better                     # REQUIRED — drives "Higher/Lower is better" label
    direction:  Direction = "LR"
    x:          AxisConfig
    y:          AxisConfig
    metrics:    list[MetricDef]
    groups:     list[GroupDef]

class BenchmarkFile(BaseModel):           # one per YAML file
    version: Literal[1] = 1
    benchmark: BenchmarkConfig

# Datapoints
class DataPoint(BaseModel):
    """A point as it crosses the wire from CLI → backend.
    `client_ts` is REQUIRED and set by the CLI at emit time with microsecond
    precision (datetime.now(timezone.utc)). It is the ground-truth ordering
    key — the frontend uses it for newer-wins (§14.4)."""
    group_key:  str
    metric_key: str
    value:      float
    client_ts:  datetime    # ISO-8601 UTC w/ μs on the wire (e.g. 2026-04-07T14:22:19.123456+00:00)

class DataPointStored(BaseModel):
    """A point after the backend has stored it. Adds seq and server_ts."""
    session_id: str
    group_key:  str
    metric_key: str
    value:      float
    client_ts:  datetime    # from the CLI, unchanged
    server_ts:  datetime    # assigned on insert (arrival time)
    seq:        int         # monotonic per session; drives Last-Event-ID

# Dataset status
DatasetStatus = Literal["pending", "running", "complete"]

class DatasetState(BaseModel):
    group_key:    str
    status:       DatasetStatus
    started_at:   int | None = None
    completed_at: int | None = None

# ── Ingest wire (HTTP POST /ingest) ────────────────────
class IngestRequest(BaseModel):
    """The body of POST /ingest. `points` carry their own client_ts set by
    the CLI when the point was produced (NOT when the POST was made — batching
    must not reorder). `request_ts` is the moment the CLI built the batch,
    used for operational logging only."""
    session_id:      str
    request_ts:      datetime                                  # CLI batch-build time
    points:          list[DataPoint] = Field(default_factory=list)
    complete_groups: list[str]       = Field(default_factory=list)

class IngestResponse(BaseModel):
    accepted:    int
    seq_from:    int | None = None
    seq_to:      int | None = None
    completed:   list[str] = Field(default_factory=list)
    server_ts:   datetime                                       # receipt time

# ── SSE events ─────────────────────────────────────────
class SseSnapshot(BaseModel):
    event: Literal["snapshot"] = "snapshot"
    session_id: str
    config:     BenchmarkConfig
    points:     list[DataPointStored]
    datasets:   list[DatasetState]

class SseDatapoint(BaseModel):
    event: Literal["datapoint"] = "datapoint"
    session_id: str
    point: DataPointStored

class SseDatasetComplete(BaseModel):
    event: Literal["dataset_complete"] = "dataset_complete"
    session_id: str
    group_key: str
    completed_at: datetime   # server-assigned on mark_complete

class SseReset(BaseModel):
    event: Literal["reset"] = "reset"
    session_id: str

class SseConfigChanged(BaseModel):
    event: Literal["config_changed"] = "config_changed"
    session_id: str
    config: BenchmarkConfig
```

### 4.3 Zod mirrors — `apps/frontend/src/schemas.ts`

Hand-written to mirror §4.2 exactly. The SSE stream handler validates every event with Zod before touching Pinia. Drift test in §11.

---

## 5. YAML configuration — one file per benchmark

The server reads every `benchmarks/*.yaml` on boot. Each file is a single `BenchmarkFile` (version + one `benchmark`).

### 5.1 Schema (narrative)

- **`version`** — `1`.
- **`benchmark`** — one entry, containing:
  - **`session_id`** — unique PK. CLI addresses this.
  - **`title`** — shown on the card and in the landing dropdown.
  - **`subtitle`** — optional secondary line under the title and as dropdown hint.
  - **`better`** — `higher` or `lower`. **Required.** Drives the "Higher is better" / "Lower is better" label rendered under the subtitle on every card, and informs delta-colouring (green when values move in the better direction, red otherwise).
  - **`direction`** — `LR` (horizontal bars) or `BT` (vertical bars).
  - **`x`** / **`y`** — axis config: label, unit, optional fixed min/max.
  - **`metrics[]`** — the bars *within each group*. Each metric has `key`, `label`, and optional `color`:
    - single hex string: `"#e86b3a"`, or
    - array of hex stops: `["#e86b3a","#f2a66b"]` — renders as an evenly-spaced linear gradient flowing **left→right** across the bar (fixed LR direction for v1).
  - **`groups[]`** — the x-axis categorical slots.

### 5.2 Example — `benchmarks/gemma4-e4b-prefill.yaml`

Directly mirrors the "Prefill (tok/s)" panel from the reference mockup: two groups (GGUF, MLX), one metric (`prefill`), higher-is-better, vertical bars. GGUF uses the mockup's orange gradient, MLX the mockup's blue. One file, one chart — maps cleanly to one card.

```yaml
version: 1
benchmark:
  session_id: gemma4-e4b-prefill-2026-04-07
  title: "Gemma 4 E4B Audio — Prefill"
  subtitle: "GGUF (Ollama) vs MLX (mlx-vlm)"
  better: higher
  direction: BT
  x:
    label: "Backend"
  y:
    label: "tokens / second"
    unit: "tok/s"
    min: 0
  metrics:
    - key: prefill
      label: "Prefill"
      # Per-group colour is applied by the metric colour's gradient mapped
      # across the bar body; see §8.5 for the solid-vs-gradient logic.
      color: ["#e86b3a", "#f2a66b"]     # warm orange gradient (mockup)
  groups:
    - { key: gguf, label: "GGUF" }
    - { key: mlx,  label: "MLX"  }
```

### 5.3 Example — `benchmarks/gemma4-e4b-decode.yaml`

```yaml
version: 1
benchmark:
  session_id: gemma4-e4b-decode-2026-04-07
  title: "Gemma 4 E4B Audio — Decode"
  subtitle: "GGUF (Ollama) vs MLX (mlx-vlm)"
  better: higher
  direction: BT
  x:
    label: "Backend"
  y:
    label: "tokens / second"
    unit: "tok/s"
    min: 0
  metrics:
    - key: decode
      label: "Decode"
      color: ["#4a8fe0", "#6fa5e8"]     # cool blue gradient (mockup)
  groups:
    - { key: gguf, label: "GGUF" }
    - { key: mlx,  label: "MLX"  }
```

### 5.4 Example — `benchmarks/gemma4-e4b-wall.yaml`

The "Wall Time" panel — identical shape to prefill/decode, but **`better: lower`**. The UI renders "Lower is better" under the subtitle.

```yaml
version: 1
benchmark:
  session_id: gemma4-e4b-wall-2026-04-07
  title: "Gemma 4 E4B Audio — Wall Time"
  subtitle: "Avg end-to-end latency across 5 audio tasks"
  better: lower
  direction: BT
  x:
    label: "Backend"
  y:
    label: "seconds"
    unit: "s"
    min: 0
  metrics:
    - key: wall_s
      label: "Wall time"
      color: ["#e86b3a", "#f2a66b"]
  groups:
    - { key: gguf, label: "GGUF" }
    - { key: mlx,  label: "MLX"  }
```

### 5.5 Example — `benchmarks/m5-4way-tps.yaml`

A richer chart with **two metrics × four groups** for the headline M5 matrix:

```yaml
version: 1
benchmark:
  session_id: m5-4way-tps-2026-04-07
  title: "4-Way Tokens/sec"
  subtitle: "Qwen 3.5 vs Gemma 4 · GGUF vs MLX · M5 Max"
  better: higher
  direction: BT
  x:
    label: "Model × Backend"
  y:
    label: "Throughput"
    unit: "tok/s"
    min: 0
  metrics:
    - key: prefill_tps
      label: "Prefill"
      color: ["#e86b3a", "#f2a66b"]         # warm (mockup orange)
    - key: decode_tps
      label: "Generation"
      color: ["#4a8fe0", "#6fa5e8"]         # cool (mockup blue)
  groups:
    - { key: qwen35_gguf, label: "Qwen 3.5 · GGUF" }
    - { key: qwen35_mlx,  label: "Qwen 3.5 · MLX"  }
    - { key: gemma4_gguf, label: "Gemma 4 · GGUF" }
    - { key: gemma4_mlx,  label: "Gemma 4 · MLX"  }
```

### 5.6 Example — `benchmarks/m5-pi-agent.yaml`

Pi agent P1..P5 wall time per backend. `better: lower`, direction `BT`, two metrics (`qwen35_mlx`, `gemma4_mlx`), five groups (`p1` .. `p5`). Same structural shape as §5.5.

---

## 6. Backend — `apps/backend/`

FastAPI + `sse-starlette` + `sqlite3` (stdlib) + Pydantic v2. uv-managed. Single process, single SQLite file.

### File-by-file

| File | Responsibility |
|---|---|
| `main.py` | Build the FastAPI app. Mount routers (`rest`, `sse_stream`, `http_ingest`). On startup: open DB, run migrations, scan `benchmarks/*.yaml`, reconcile into DB (see §4.1). On shutdown: flush broker, close DB. Uvicorn entry. |
| `config.py` | `load_benchmarks_dir(path) → list[BenchmarkFile]`. Globs `*.yaml`, validates each, returns or raises with a file-accurate error. Optional `watch()` for dev: re-scans on mtime change and broadcasts `SseConfigChanged`. |
| `models.py` | All Pydantic models from §4.2. No logic. |
| `db.py` | Thin sqlite3 wrapper: `connect()`, `migrate()`, row→model helpers. WAL mode on. |
| `store.py` | Repository: `upsert_benchmark`, `list_benchmarks`, `get_benchmark`, `reset`, `insert_points(session_id, points) → list[DataPointStored]`, `mark_complete(session_id, group_keys) → list[(group_key, completed_at)]`, `dataset_states(session_id) → list[DatasetState]` (derived from datapoints + completions), `latest_per_cell(session_id) → dict[(group,metric) → DataPointStored]` (uses the `(session, group, metric, client_ts DESC)` index to cheaply fetch the newest stored point per cell — used to build the `snapshot` SSE event's `points` list). Assigns `seq` monotonically inside a single write lock. `server_ts` is stamped here, not in the handler. |
| `broker.py` | In-proc pub/sub. `subscribe(session_id) → asyncio.Queue`. `publish(event)`. |
| `http_ingest.py` | `POST /ingest`. Body: `IngestRequest`. Flow: validate session exists → validate group/metric keys against config → validate every `client_ts` is present + parseable + within ±5 min of server clock (reject with `400 clock_skew` otherwise) → `store.insert_points` (stamps `server_ts` + `seq`, returns `DataPointStored` list) → publish one `SseDatapoint` per stored point → if any `complete_groups`: `store.mark_complete` → publish `SseDatasetComplete` per group → return `IngestResponse`. 400 on unknown session/group/metric. The handler does **not** filter out-of-order points — every insert is broadcast with its `client_ts`, and the frontend handles newer-wins per cell (§14.4). |
| `sse_stream.py` | `GET /stream/{session_id}`. Headers for SSE. On connect: send `snapshot` with config + points + dataset states; then subscribe to broker and forward events for that session. Honors `Last-Event-ID` to resume. |
| `rest.py` | `GET /benchmarks` (list all with derived `completed_count / total_count` and `better`), `GET /benchmarks/{session_id}` (config + points + datasets), `POST /benchmarks/{session_id}/reset`, `GET /healthz`. **No POST /benchmarks** — creation is yaml-only. |
| `logging.py` | Structured logging; one-line per ingested point at DEBUG. |

### Reconnect story

- **CLI side.** Every request is a standalone HTTP POST. httpx connection pooling handles socket reuse. On 5xx, the CLI retries with exponential backoff. On final failure, the CLI writes the unsent batch to a local `.live-bench-outbox.jsonl` next to the working directory — next invocation drains it before its own payload. Survives a laptop lid close.
- **UI side.** `EventSource` auto-reconnects. On resume the browser passes `Last-Event-ID`; server replays `datapoints` with `seq > last` and re-emits completion events for any groups marked complete since. No flicker, no state reset.
- **Server crash.** SQLite is the persistent truth. On next boot YAML loads, existing sessions reconcile, `/stream` replays from seq 0 on first connect.

---

## 7. CLI — `apps/cli/`

Built with **astral uv** as a standalone uv project that publishes a `live-bench` console script. Uses **`click`**, **`httpx`** for all HTTP, Pydantic models imported from the backend as a path dependency.

### Commands

```
live-bench list
    → GET /benchmarks
    Prints a table: session_id, title, subtitle, better, datasets complete/total

live-bench show <session_id> [--json]
    → GET /benchmarks/<session_id>
    Prints config + current datapoint matrix + per-group status

live-bench reset <session_id> [--yes]
    → POST /benchmarks/<session_id>/reset

live-bench emit <session_id> --group <g> --metric <m> --value <v>
    → POST /ingest  {points: [{...}]}
    Single point, exits after 200

live-bench emit <session_id> --batch <file|->
    → POST /ingest  {points: [...]}
    File or stdin in JSONL; each line: {"group":"...","metric":"...","value":...}

live-bench complete <session_id> --group <g> [--group <g2> ...]
    → POST /ingest  {complete_groups: [...]}

live-bench stream <session_id> [--flush-ms 50] [--max-batch 100]
    → reads stdin JSONL and POSTs batches every <flush-ms> or <max-batch>
    A line may be a point {"group","metric","value"} OR a control
    {"complete": "gguf"} to mark done. Holds one httpx.Client for the whole run.
    Canonical usage:
        python my_bench.py | live-bench stream gemma4-e4b-prefill-2026-04-07

live-bench tail <session_id>
    → dev-only: attaches to SSE and prints events as they arrive
```

Global flags: `--server http://<dashboard-host>:8787` (or env `LIVE_BENCH_SERVER`), `--verbose`.

### File-by-file

| File | Responsibility |
|---|---|
| `cli.py` | Click app, command registration, global flags. |
| `client.py` | `LiveBenchClient`: holds `httpx.Client` with keep-alive and base_url set. Methods: `list()`, `show(id)`, `reset(id)`, `ingest(req: IngestRequest)`. Helper `now_ts() -> datetime` returns `datetime.now(timezone.utc)` with microseconds — this is the single source of client timestamps for the whole CLI. Retries 5xx with exp backoff. Flushes pending batch to `.live-bench-outbox.jsonl` on hard failure (each outbox entry keeps its original `client_ts`, not the replay time). |
| `commands/emit_cmd.py` | Single or batch → stamps `client_ts = now_ts()` at the moment of CLI invocation for single `--value`; for `--batch <file|->` each stdin/file line may include its own `client_ts` (passes through unchanged), otherwise `now_ts()` is filled at the moment the line is read. Builds `IngestRequest{points=[...]}` → one POST. **Timestamps are attached at read time, not POST time**, so a 20 ms batch window never reorders lines from different moments. |
| `commands/stream_cmd.py` | Persistent stdin reader. Reads line-by-line; on each line stamps `client_ts = now_ts()` immediately (unless the line carries its own), then buffers. Every `flush-ms` or `max-batch` builds an `IngestRequest` and calls `client.ingest`. EOF → final flush → exit. This preserves the runner's original emit order even when the network is slow. |
| `models.py` | Re-exports shared Pydantic models from the backend package. |
| `commands/list_cmd.py` | `client.list()` → `rich.table`. |
| `commands/show_cmd.py` | `client.show(id)` → pretty print config + latest values grouped by group, with a per-group status pill. |
| `commands/reset_cmd.py` | Confirm prompt → `client.reset(id)`. |
| `commands/complete_cmd.py` | `IngestRequest{complete_groups=[...]}` → one POST. No points, just a `request_ts`. |
| `commands/tail_cmd.py` | Opens `GET /stream/{id}` via httpx streaming, prints events with both `client_ts` and `server_ts` for debugging. |

---

## 8. Frontend — `apps/frontend/`

Vite + Vue 3 + `<script setup lang="ts">` + Pinia + Zod + vue-router. **No chart library** — hand-rolled SVG. Google Fonts **Play** as the display font. Presentation-sized defaults.

### 8.1 Routes

| Route | Component | Behavior |
|---|---|---|
| `/` | `LandingPage.vue` | On mount: `GET /benchmarks`. Shows a dropdown of benchmarks by `title + subtitle` (with `session_id` as hint). "Go" button (or auto-navigate on select) → `router.push('/benchmark/' + session_id)`. If the list is empty: `EmptyState` "No benchmarks found — drop a YAML file in `benchmarks/` and restart the server." **No create UI.** |
| `/benchmark/:sessionId` | `BenchmarkPage.vue` | On mount: `GET /benchmarks/:sessionId` for initial hydration, then opens SSE `/stream/:sessionId`. Renders `BenchmarkGrid` with a single `BenchmarkCard`. **"← Back"** link in header returns to `/`. On unmount: close SSE. |

Density and theme apply to both routes via the global `NavBar`.

### 8.2 Density — S / M / L

| Density | Columns (≥1400px) | Columns (≥1000px) | Columns (<1000px) | Intent |
|---|---|---|---|---|
| **Large** | 1 | 1 | 1 | Hero shot, maximum chart area. |
| **Medium** | 2 | 2 | 1 | Default working view. |
| **Small** | 4 | 3 | 2 | Dashboard, everything at once. |

### 8.3 Card anatomy (matches the reference mockup)

A `BenchmarkCard` renders the following stack, top to bottom:

```
┌─────────────────────────────────────────────┐ ← rounded rect, border, soft shadow
│ Title (fs-large, white, bold)                │
│ Subtitle (fs-medium, dim)                    │
│ "Higher is better" | "Lower is better"       │ ← from `better`, fs-base, dim
│ ┌─ DatasetStatusBar ─────────────────────┐  │
│ │ 3 / 4 complete · [gguf ✓][mlx ●pulsing]│  │
│ └────────────────────────────────────────┘  │
│                                              │
│        GroupedBarChart (SVG, fills box)      │
│                                              │
└─────────────────────────────────────────────┘
```

The bar numeric value overlay (e.g. `1308`, `720`) renders **above** each bar in the metric's primary colour, at `--fs-xlarge` (or `--fs-mega` in Large density). This matches the mockup exactly.

### 8.4 File-by-file

| File | Responsibility |
|---|---|
| `main.ts` | Vue bootstrap, Pinia, router, mount. Applies persisted theme on startup (`document.documentElement.dataset.theme = prefs.theme ?? 'obsidian'`). |
| `App.vue` | `<NavBar />` + `<RouterView />`. NavBar sticky on both pages. |
| `router.ts` | `createRouter` with routes from 8.1. |
| `schemas.ts` | Zod mirrors of §4.2 + `parseSseEvent(raw)` discriminated union. |
| `themes.ts` | Ten theme definitions (see §13). Exports names, display labels, swatch. |
| `api/rest.ts` | `listBenchmarks()`, `getBenchmark(id)`, `resetBenchmark(id)`. Zod-typed. |
| `api/stream.ts` | `connectStream(sessionId, handlers)`. Tracks `lastEventId`, auto-reconnects. |
| `stores/benchmarks.ts` | Pinia store for landing: `list: BenchmarkSummary[]`. |
| `stores/session.ts` | Pinia store for an active benchmark: `{ config, latest: Map<'g:m', number>, latestClientTs: Map<'g:m', string>, datasets: Map<group_key, DatasetState> }`. Mutations: `applySnapshot`, `applyDatapoint` (with the newer-wins guard from §14.4), `applyDatasetComplete`, `applyReset`. |
| `stores/prefs.ts` | `theme: ThemeName`, `density: 'S'\|'M'\|'L'`. Persisted to localStorage. Defaults: `theme = 'obsidian'`, `density = 'M'`. |
| `pages/LandingPage.vue` | Dropdown + empty state + navigate. |
| `pages/BenchmarkPage.vue` | Fetch + SSE lifecycle + `<BenchmarkGrid>`. "← Back" in header. |
| `components/NavBar.vue` | Brand ("live-bench") on the left. Right side (in order): `<ConnectionBadge/> <LayoutSwitcher/> <ThemeSwitcher/>`. |
| `components/LayoutSwitcher.vue` | 3-way S/M/L → `prefs.density`. |
| `components/ThemeSwitcher.vue` | Dropdown with swatch + name for each of the 10 themes. Writes `prefs.theme` and sets `document.documentElement.dataset.theme`. |
| `components/ConnectionBadge.vue` | Pill with colored dot + label from SSE state. |
| `components/BenchmarkGrid.vue` | CSS grid, `grid-template-columns: repeat(var(--cols), minmax(0, 1fr))`. |
| `components/BenchmarkCard.vue` | Header stack (title / subtitle / better label / status bar), body (chart), footer ("last update Xs ago"). See §8.3. |
| `components/DatasetStatusBar.vue` | Aggregate `n / m complete` + row of per-group pills coloured by status: `pending` (dim), `running` (accent + pulsing dot), `complete` (success + check). |
| `components/GroupedBarChart.vue` | The chart. Computes scales, emits `<BarGradientDefs>`, iterates groups → metrics → `<AnimatedBar>`. Honors `direction`. |
| `components/BarGradientDefs.vue` | Emits one `<linearGradient>` per metric with an array colour. Id pattern: `grad-{session}-{metric}`. Always `x1=0 y1=0 x2=1 y2=0` (LR flow). Stops evenly spaced. Single-colour metrics skip the gradient and use a plain hex. |
| `components/AnimatedBar.vue` | One bar. Owns 1s transition + coalesce buffer (§14). Renders the numeric overlay above itself. |
| `components/EmptyState.vue` | Used in landing and session pages. |

### 8.5 Chart rendering notes

- `latest` is `Map<"group_key:metric_key", number>` — only the latest value per (group, metric) matters. Bar charts are point-in-time snapshots.
- Bar fill resolution order: `metric.color` → if array, gradient ref; if string, plain hex. If missing, fall back to a palette indexed by metric position (and warn once in console).
- Direction:
  - `BT` → bars grow upward; groups are x-axis categories with a small gap between metric sub-bars.
  - `LR` → rotate 90°: groups are y-axis rows, metrics are sub-bars within each row.
- Axis range: if `y.min`/`y.max` set, use them. Otherwise `min(0, minValue)` to `max * 1.1`. Animate `max` changes with the same 1s transition so a new incoming record doesn't snap-rescale jarringly.

---

## 9. Wire protocol — concrete messages

### 9.1 CLI → backend — `POST /ingest`

Every point carries a `client_ts` (ISO-8601 UTC with microsecond precision) stamped by the CLI at the instant it *received* that point from the user or stdin — not at POST-build time. The batch as a whole also carries a `request_ts` for logging.

Request:
```json
{
  "session_id": "gemma4-e4b-prefill-2026-04-07",
  "request_ts": "2026-04-07T14:22:19.318204+00:00",
  "points": [
    {
      "group_key":  "gguf",
      "metric_key": "prefill",
      "value":      1308,
      "client_ts":  "2026-04-07T14:22:19.104872+00:00"
    },
    {
      "group_key":  "mlx",
      "metric_key": "prefill",
      "value":      720,
      "client_ts":  "2026-04-07T14:22:19.291003+00:00"
    }
  ],
  "complete_groups": ["gguf"]
}
```

Response 200:
```json
{
  "accepted":  2,
  "seq_from":  1,
  "seq_to":    2,
  "completed": ["gguf"],
  "server_ts": "2026-04-07T14:22:19.402118+00:00"
}
```

Errors:
- `404 {"code":"unknown_session"}`
- `400 {"code":"unknown_group","message":"group 'foo' not in session config"}`
- `400 {"code":"unknown_metric", ...}`
- `400 {"code":"missing_client_ts","message":"point[1] has no client_ts"}`
- `400 {"code":"clock_skew","message":"point[0] client_ts is 17 min ahead of server — check NTP"}`

Every point is validated against the live `BenchmarkConfig`. Bad data is rejected at the door; `live-bench stream` logs and continues with the next line.

### 9.2 Backend → frontend — SSE `/stream/:sessionId`

Both `client_ts` and `server_ts` are carried on every payload that includes a point, so the frontend can do newer-wins on `client_ts` (§14.4) and the footer "last update Xs ago" can use `server_ts`.

```
event: snapshot
id: 42
data: {
  "session_id": "...",
  "config": {...},
  "points": [ /* latest-per-cell only, ordered by client_ts */ ],
  "datasets": [ {"group_key":"gguf","status":"running","started_at":"2026-04-07T14:22:18.923Z","completed_at":null}, ... ]
}

event: datapoint
id: 43
data: {
  "session_id": "...",
  "point": {
    "group_key":  "gguf",
    "metric_key": "prefill",
    "value":      1308,
    "client_ts":  "2026-04-07T14:22:19.104872+00:00",
    "server_ts":  "2026-04-07T14:22:19.402118+00:00",
    "seq":        43
  }
}

event: dataset_complete
id: 44
data: {"session_id":"...","group_key":"gguf","completed_at":"2026-04-07T14:22:19.402118+00:00"}

event: reset
id: 45
data: {"session_id":"..."}

event: config_changed
id: 46
data: {"session_id":"...","config":{...}}
```

### 9.3 REST endpoints

| Method | Path | Body | Returns |
|---|---|---|---|
| `GET` | `/benchmarks` | — | `{ benchmarks: BenchmarkSummary[] }` (each with `better`, `completed/total`) |
| `GET` | `/benchmarks/{id}` | — | `{ config, points, datasets }` |
| `POST` | `/benchmarks/{id}/reset` | — | `{ reset: true, session_id }` |
| `POST` | `/ingest` | `IngestRequest` | `IngestResponse` |
| `GET` | `/stream/{id}` | — (SSE) | event stream |
| `GET` | `/healthz` | — | `{ ok: true }` |

---

## 10. Example end-to-end flow

1. Drop `benchmarks/gemma4-e4b-prefill.yaml`, `..decode.yaml`, `..wall.yaml` in the repo. Run `just serve`.
2. Backend boots, reconciles 3 YAMLs → SQLite, no datapoints. Frontend boots at `/`.
3. Landing page `GET /benchmarks` → 3 benchmarks. Dropdown shows `"Gemma 4 E4B Audio — Prefill · GGUF vs MLX · Higher is better"`, etc. User selects prefill, navigates to `/benchmark/gemma4-e4b-prefill-2026-04-07`.
4. `BenchmarkPage` hydrates via REST, opens SSE, receives `snapshot`. Card renders title + subtitle + **"Higher is better"** + `0 / 2 complete · [gguf pending][mlx pending]`. Chart shows 2 empty bar slots.
5. On M4, `bench_audio.py` finishes the GGUF run:
   ```
   python bench_audio.py | live-bench stream gemma4-e4b-prefill-2026-04-07
   ```
   Script emits `{"group":"gguf","metric":"prefill","value":1308}` then `{"complete":"gguf"}`. The CLI `stream` reader stamps `client_ts = datetime.now(timezone.utc)` the instant each line arrives on stdin — the point gets `2026-04-07T14:22:19.104872+00:00`, the complete marker gets its own slightly later stamp.
6. Backend validates, `insert_points` stamps seq=1 + server_ts, publishes `SseDatapoint` carrying all three timestamps. `gguf` dataset flips `pending → running`. A moment later `SseDatasetComplete` fires.
7. UI receives `datapoint` → session store compares `client_ts` against any prior value for the `gguf:prefill` cell (none yet) → writes `latest` + `latestClientTs` → `AnimatedBar` smoothly transitions from 0 to 1308 over 1 s; overlay number eases in parallel. Pill flips `pending → running → complete ✓`. Header: `1 / 2 complete`.
8. M5 does the same for `mlx` (720), with its own `client_ts` from M5's clock. Second bar grows. Header: `2 / 2 complete`. If the M5 packet had arrived before the M4 packet (unlikely but possible), the `mlx` and `gguf` cells are independent so there's no reordering issue — and if M4 or M5 had sent a *retry* of an older point, the `client_ts` comparison in the store would drop it silently without the bar ever twitching.
9. Presenter switches `ThemeSwitcher` from `obsidian` → `matrix` mid-take. `<html data-theme>` flips, CSS vars cascade, bars keep the metric gradient but card chrome switches to green-on-black. No reload.
10. User hits `← Back`, picks the wall-time benchmark (`better: lower`). Card now shows **"Lower is better"**. Same cycle runs with `wall_s` values 3.0 and 0.7.

### Benchmark script integration

Same shape as before; at the end of each per-run block in the runner print one JSONL line per metric, then one `{"complete":"<group>"}` at the end. No imports from live-bench into the runner. The runner **does not** need to stamp timestamps itself — the CLI `stream` reader does it the instant each line arrives on stdin, which is the most accurate emit-order signal available without the runner taking a dependency on live-bench. A runner that cares about wall-clock fidelity can include its own `"client_ts"` in each line; if present, the CLI passes it through untouched.

---

## 11. Cross-language type sharing

Two languages, one schema. **Hand-write Pydantic + Zod in parallel**, with a drift test: `apps/frontend/src/schemas.test.ts` loads fixture JSON generated by `apps/backend/tests/fixtures_export.py` and asserts Zod `parse()` succeeds for every model. If drift starts hurting, generate Zod with `datamodel-code-generator`.

Python-side: CLI depends on backend as a path dep in `apps/cli/pyproject.toml`:

```toml
[tool.uv.sources]
live-bench-server = { path = "../backend", editable = true }
```

The CLI imports only `live_bench_server.models`. No vendoring, one source of truth.

---

## 12. justfile — top-level recipes

```just
default:
    @just --list

# ── dev ────────────────────────────────────────────────
serve:           # Start backend (8787) + frontend (5173) together
    mprocs "just backend" "just frontend"

backend:
    cd apps/backend && uv run uvicorn live_bench_server.main:app --reload --port 8787

frontend:
    cd apps/frontend && pnpm dev

# ── cli convenience ────────────────────────────────────
cli *ARGS:
    cd apps/cli && uv run live-bench {{ARGS}}

list:
    just cli list

show SESSION:
    just cli show {{SESSION}}

reset SESSION:
    just cli reset {{SESSION}} --yes

# ── one-shot ingest ────────────────────────────────────
emit SESSION GROUP METRIC VALUE:
    just cli emit {{SESSION}} --group {{GROUP}} --metric {{METRIC}} --value {{VALUE}}

complete SESSION GROUP:
    just cli complete {{SESSION}} --group {{GROUP}}

# ── tests ──────────────────────────────────────────────
test-backend:
    cd apps/backend && uv run pytest

test-cli:
    cd apps/cli && uv run pytest

test-frontend:
    cd apps/frontend && pnpm test

test: test-backend test-cli test-frontend

# ── build ──────────────────────────────────────────────
build-frontend:
    cd apps/frontend && pnpm build

# ── fake data for UI dev ───────────────────────────────
demo-stream SESSION="gemma4-e4b-prefill-2026-04-07":
    cd apps/cli && uv run python -m live_bench_cli.dev.fake_stream {{SESSION}}
```

Note: **no `just load` recipe** — benchmark definitions are loaded from `benchmarks/*.yaml` by the backend on boot.

---

## 13. Theming & typography

### 13.1 Font

Google Fonts **Play** as the sole UI font. Preconnect + preload in `index.html`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Play:wght@400;700&display=swap" rel="stylesheet">
```

Presentation-tuned sizes (base is noticeably larger than typical web apps — readable from 3 m on a 27" display):

```css
:root {
  --font:       'Play', system-ui, sans-serif;
  --fs-base:     18px;   /* body, pill labels */
  --fs-medium:   22px;   /* subtitle, axis labels, group labels, better-label */
  --fs-large:    28px;   /* card title */
  --fs-xlarge:   40px;   /* numeric overlay on bars (Medium/Small) */
  --fs-mega:     56px;   /* numeric overlay on bars (Large density) */
  --radius-card: 16px;
  --radius-pill: 999px;
  --anim-bar:    1000ms;
  --ease-bar:    cubic-bezier(0.22, 1, 0.36, 1);
}
html { font-family: var(--font); font-size: var(--fs-base); }
```

### 13.2 Themes — 10 total, `obsidian` is the default

Themes are applied via `[data-theme="..."]` on `<html>`. Each theme sets a fixed set of CSS custom properties consumed by all chart elements and card chrome. Metric colours from YAML always win for bar fills — themes drive bg, grid, axis text, card chrome, and status pills.

#### 13.2.1 Theme 1 — `obsidian` (DEFAULT, modelled on the reference mockup)

```css
[data-theme="obsidian"] {
  /* surfaces */
  --bg:           #080c17;   /* page background, very dark navy/near-black */
  --bg-card:      #121829;   /* card body */
  --bg-card-hi:   #161d32;   /* card subtle top gradient end */
  --bg-inset:     #0c1322;   /* inset pill / footer strip inside a card */
  --border-card:  #1f2740;   /* soft card border (1px) */
  --border-grid:  #1c2338;   /* chart grid lines (dashed) */
  --shadow-card:  0 4px 24px rgba(0, 0, 0, 0.45);

  /* typography */
  --fg:           #f4f6fc;   /* titles, numeric overlays fallback */
  --fg-medium:    #b7bfd8;   /* body text */
  --fg-dim:       #7b8599;   /* subtitles, axis labels, "higher/lower is better" */
  --fg-dimmer:    #4e5670;   /* grid tick numbers */

  /* accents */
  --accent:       #7c9dff;   /* active UI (selected density, pulsing dot) */
  --accent-bg:    #1a2345;
  --success:      #4ade80;   /* +26%, 4.2x faster delta pills, complete pill */
  --success-bg:   #16331f;
  --warn:         #fbbf24;
  --warn-bg:      #3a2a10;
  --danger:       #f87171;
  --danger-bg:    #3a1716;

  /* chart defaults (overridable via YAML metric.color) */
  --bar-warm-a:   #e86b3a;   /* GGUF/orange gradient stop 1 — matches mockup */
  --bar-warm-b:   #f2a66b;   /* GGUF/orange gradient stop 2 */
  --bar-cool-a:   #4a8fe0;   /* MLX/blue   gradient stop 1 */
  --bar-cool-b:   #6fa5e8;   /* MLX/blue   gradient stop 2 */

  /* status pill palette */
  --pill-pending-bg:  #1a2133;
  --pill-pending-fg:  var(--fg-dim);
  --pill-running-bg:  var(--accent-bg);
  --pill-running-fg:  var(--accent);
  --pill-complete-bg: var(--success-bg);
  --pill-complete-fg: var(--success);

  /* inline info strips (TASKS / MODELS in the mockup) */
  --tag-tasks-border:  #3a5080;
  --tag-tasks-fg:      #8db0ff;
  --tag-models-border: #7d3a5a;
  --tag-models-fg:     #e08dbb;
}
```

Visual notes cross-referenced with the mockup:

- Page background is near-black navy, not pure black — keeps the cards visibly floating.
- Cards have a **1 px soft border** (`--border-card`) plus a generous shadow (`--shadow-card`), rounded `--radius-card` = 16 px.
- Grid lines inside the chart are dashed, one-third-opacity — they're felt, not read.
- Bar gradients flow **LR** even for vertical bars — exactly matching the mockup's subtle left-to-right hue shift on the orange and blue bars.
- Numeric overlay above each bar is drawn in the bar's primary colour (gradient stop 1), bold, at `--fs-xlarge` (Medium/Small) or `--fs-mega` (Large).
- Delta pills (`+26%`, `4.2x faster`, `Higher is better`, `Lower is better` — only the first two are delta badges; the better label is a plain dim line) use `--success` / `--success-bg` for positive, `--danger` / `--danger-bg` for negative.
- The "Tasks" and "Models" chips at the bottom of the reference mockup are a good style target for `DatasetStatusBar` per-group pills — they're pill-shaped, 1 px border in the tag colour, label in the tag colour at `--fs-base`.

#### 13.2.2 Remaining themes

All follow the same CSS var contract. Declared in `themes.css` as `[data-theme="..."]` blocks; `themes.ts` exports the names and swatches for `ThemeSwitcher`.

| # | Name | Vibe | Bg | Accent |
|---|---|---|---|---|
| 1 | `obsidian` | **Default.** Deep navy slate, warm orange + cool blue bars. Mirrors reference mockup. | `#080c17` | `#7c9dff` |
| 2 | `midnight` | Cooler navy, softer cyan accent. | `#0b1020` | `#7c9dff` |
| 3 | `matrix` | Phosphor green on pure black. | `#000000` | `#39ff14` |
| 4 | `vaporwave` | Dark purple + magenta/pink. | `#1a0b2e` | `#ff6ec7` |
| 5 | `tokyo` | Tokyo Night palette. | `#1a1b26` | `#7aa2f7` |
| 6 | `sunset` | Warm dark, orange/pink accents. | `#1f0f1a` | `#ff7a59` |
| 7 | `arctic` | Icy white-blue, navy text. Light theme. | `#eef4ff` | `#2563eb` |
| 8 | `paper` | Warm off-white, dark gray. Light theme. | `#faf8f3` | `#1f2937` |
| 9 | `mono` | Pure black, white, grayscale. | `#000000` | `#ffffff` |
| 10 | `solarized` | Solarized Dark. | `#002b36` | `#268bd2` |

`prefs.theme` defaults to `'obsidian'` on first load and persists to localStorage thereafter.

---

## 14. Animation — smooth, coalescing updates

Every bar animates its length/height over **1 second**. New updates that arrive during an active animation are **buffered** as "pending latest" — only the most recent pending value survives.

### 14.1 Per-bar state machine

```
state:
  current:  number   // what's on screen
  target:   number   // what we're animating toward; = current when idle
  pending:  number | null
```

- **On new value `v` while idle** (`current === target`, no pending):
  `target = v` → CSS transition from `current` to `v` over 1 s.
- **On new value `v` while animating** (`current !== target`):
  `pending = v`. Current animation continues uninterrupted.
- **On `transitionend`**:
  `current = target`. If `pending !== null`: `target = pending; pending = null` (new animation starts). Otherwise idle.

This is exactly the "smoothly incrementing total time" behaviour: a runner emitting `12.1, 12.4, 12.7, ...` every 100 ms sees the bar smoothly grow to the latest value in 1-second bursts.

### 14.2 Implementation notes

- `AnimatedBar.vue` holds the state and renders one SVG `<rect>` (BT) or horizontal rect (LR).
- BT grows from the baseline — both `y` and `height` animate so the illusion is a "bottom-anchored" rise.
- LR: just animate `width`.
- Transition declared via CSS vars: `transition: width var(--anim-bar) var(--ease-bar), height var(--anim-bar) var(--ease-bar), y var(--anim-bar) var(--ease-bar)`.
- Listen for `transitionend`; on fire, check `pending` and either start a new animation or go idle.
- Numeric overlay uses a `requestAnimationFrame` loop that eases from `current` to `target` with the same duration and ease — stays in sync with the bar length. Stops on `transitionend`.

### 14.3 Why 1 s

- Short enough that "live" feels live.
- Long enough to smooth out fast-arriving values into fluid movement — the on-camera dopamine shot from the debrief.
- Matches human reaction time for parsing bar lengths.

### 14.4 Newer-wins on `client_ts`

The 14.1 state machine deliberately swallows mid-animation updates into a `pending` slot — but which update "wins" when two arrive during the same animation? Answer: the one with the **latest `client_ts`**, not the one that arrived last over the wire.

This matters for two scenarios:
- **Out-of-order delivery.** Two httpx POSTs cross in flight, or two runners on M4 and M5 race. The older `client_ts` must not overwrite the newer one just because its packet showed up second.
- **SSE resume.** After a reconnect, `Last-Event-ID` replays historical events in `seq` order. A replay of seq 50 is not "newer" than seq 60 that the UI already processed — `client_ts` is the only reliable ordering key.

The session store (`stores/session.ts`) maintains one tiny extra map alongside `latest`:

```ts
latestClientTs: Map<`${string}:${string}`, string>   // cell → ISO-8601 string
```

On each `datapoint` SSE event:

```ts
const cell = `${point.group_key}:${point.metric_key}`;
const prev = state.latestClientTs.get(cell);
// ISO-8601 UTC with fixed precision is lexicographically sortable.
if (!prev || point.client_ts > prev) {
  state.latest.set(cell, point.value);
  state.latestClientTs.set(cell, point.client_ts);
  // AnimatedBar reactively picks up the new value and applies §14.1.
}
// else: stale point, store in history if we care, but do NOT touch the bar.
```

On `reset`, both maps are cleared for the session. On `snapshot`, both are rebuilt from the snapshot's `points` list (which the backend already delivers as latest-per-cell ordered by `client_ts`).

This is the only ordering logic in the frontend. The backend does not filter — it broadcasts everything with full timestamps and trusts the UI to do the right thing. That keeps the server stateless and makes reconnect replay trivially correct.

---

## 15. Transport decision — HTTP POST (LOCKED) + client timestamps

**Decision:** CLI → backend is **HTTP POST `/ingest`** with httpx connection pooling, and every `DataPoint` carries a CLI-stamped `client_ts` that is the ground-truth ordering key. This section is retained for future reference — the trade-off analysis is still useful if we ever revisit, but the call is made and the spec above is final on this front.

### Why HTTP wins for this use case

1. **The CLI's primary mode is one-shot.** `live-bench emit` is called from a shell script at the end of a run. With WS you pay: `connect → hello → hello_ack → emit → ack → close`. With HTTP POST you pay: `POST → 200`. HTTP is strictly less.
2. **"Opening a socket per event" is mostly a myth at this layer.** `httpx.Client` keeps TCP connections alive across requests. The 2nd, 3rd, and Nth `emit` in a single CLI process reuse the same TCP socket. The CLI `stream` subcommand holds a single `httpx.Client` for its entire lifetime — the hot path *is* one open connection, just wrapped in HTTP semantics.
3. **Stateless servers are easier to reason about.** No hello/ack/resume handshake, no "did this client's seq get desynced", no graceful shutdown of N open sockets.
4. **Validation errors are natural.** HTTP 400 with a JSON body is exactly the right shape for "unknown group". With WS you invent `{type:"error"}` and decide whether to close.
5. **Backpressure for free.** The OS TCP buffer + httpx client pool handle it.

### When I'd choose WebSocket instead

- Truly continuous telemetry (100+ events/s per client) where HTTP/1.1 framing overhead matters.
- Bidirectional control (server pushes commands back to the CLI — we don't do this).

Neither applies.

### Why not a "real" queue (Redis / NATS / etc.)

- Zero functional benefit on a LAN with one consumer; strict ops cost.
- SQLite's single-writer + the in-proc `broker.publish()` fan-out is already a queue — durable (SQLite) plus ephemeral (broker).

### Client-side outbox (the one thing "queue" thinking buys us)

Client-side durability: if the backend is down when the benchmark emits, we don't want to lose the point. The CLI keeps a local `.live-bench-outbox.jsonl` next to the runner; on failed POST it appends; on next successful request it drains. ~30 lines of Python, zero new deps.

### Why client timestamps are non-negotiable once we pick HTTP

The one real weakness of HTTP POST for this use case is that request arrival order is not guaranteed to match emit order: two POSTs from the same process can interleave under connection-pool contention, and two POSTs from *different* machines (M4 and M5 both pushing into the same benchmark) absolutely can arrive out of order over the switch. Without a client-stamped timestamp, the bar would flicker — the server would broadcast the "wrong" latest value whenever a late-arriving packet slipped past a newer one.

`client_ts` closes this hole completely:

- The CLI stamps `client_ts = datetime.now(timezone.utc)` at the instant it receives the point (CLI arg parse for `emit`, stdin line read for `stream`) — *not* at POST-build time. Batching within `stream` cannot reorder anything.
- The backend stores it verbatim, assigns its own `seq` and `server_ts`, and broadcasts all three.
- The frontend's session store does newer-wins per `(group, metric)` cell on `client_ts` (§14.4). Late packets are dropped silently from the bar view even though they're still in SQLite.
- SSE resume via `Last-Event-ID` replays by `seq`, but the frontend still uses `client_ts` to decide whether each replayed point should overwrite the bar — so replay is trivially correct regardless of replay order.

ISO-8601 UTC with microsecond precision is the wire format. It is lexicographically sortable when fixed-width, so the frontend can compare with `<` / `>` directly on the string — no parsing needed for the hot path.

---

## 16. Open questions / deferred decisions

- **Hand-rolled chart scaling edge cases.** Mixed metric scales inside one chart (e.g. tok/s and wall-time s in the same card) look bad on one y-axis. For v1 we assume the YAML author groups same-unit metrics together; no auto-detect or dual-axis.
- **Gradient direction configurability.** Fixed to LR flow for v1 (per the mockup). If a user wants BT gradient flow we'll add `gradient_direction: LR | BT` to `MetricDef` later.
- **`better` at metric level.** v1 puts `better` on the benchmark. If a single card ever needs mixed-direction metrics (e.g. one "higher is better" and one "lower is better" bar side-by-side) we'd move/augment it to `MetricDef.better`. Not needed yet — the reference mockup resolves this by splitting into three cards (one per `better` direction), which our one-yaml-one-benchmark model already encourages.
- **Point retention.** Every point is kept forever in SQLite. Fine for a single session (thousands of rows max).
- **Multi-user drift.** Two runners hammering the same group interleave — last-write-wins, the animation state machine handles coalescing.
- **Hot reload of YAML.** `config.watch()` is drafted but optional for v1.

---

## 17. Success criteria for v1

1. **Cold-start to first bar moving on camera is ≤ 60 seconds.** `just serve` → open browser → pick benchmark → one `live-bench emit` → bar animates.
2. **YAML is the only thing the user edits to add a benchmark.** Drop a file in `benchmarks/`, restart, it's in the dropdown.
3. **The reference mockup (prefill / decode / wall) is faithfully reproducible** using three YAML files and the `obsidian` theme. Bars, gradients, status pills, and "Higher/Lower is better" labels match the mockup without per-card customisation.
4. **A mid-run server restart is invisible to the camera** — SSE reconnects, bars redraw to exactly where they were, new points keep flowing.
5. **The CLI fits in one `uv tool install`** and works from any benchmark script on the LAN with `LIVE_BENCH_SERVER=http://<dashboard-host>:8787 live-bench emit ...`.
6. **Presenter can flip theme and density mid-stream** without dropping a frame. 10 themes, all readable on a 27" display from 3 m.

If those six hold, the tool is done and we ship the video.

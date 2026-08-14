# AH-4 — Outdated vs Current

Course-era detail → 2026 reality, with the book treatment for each. **Good news first, because it flips the AH-3 story:** this lesson's repo is already on the **current Claude Agent SDK** (`claude-agent-sdk` / `ClaudeAgentOptions` / `ClaudeSDKClient`, verified in every import and `pyproject.toml`), and **Dan actually says "the Claude Agent SDK" on camera.** So the single biggest AH-3 correction — the SDK rename — **does not apply here.** What *does* need care: the lesson is a bespoke system (not a product), it names its own biggest missing piece, and there are a few internal staleness bugs in the repo.

---

## 1. The lesson names its OWN biggest gap: no deterministic AI Developer Workflows yet ⭐

**What the lesson shows/says:** A very *agentic* system — the autonomy knob turned up. Dan is explicit about what's missing: *"How does this plug into deterministic code?… We're missing our AI developer workflows. Okay. This is the big missing piece. And this is something that we will be building… in upcoming Agentic Horizon lessons."*

**What's true now:** The O-agent is the **intermediate step** — the thing you use *while* you build an agentic layer, before you have concrete ADWs/triggers wired in. Integrating it with deterministic code (ADWs) is forward-looking, not shipped.

**Book treatment:** Present the O-agent as a **paradigm and a reference implementation**, not a finished agentic layer. Set the expectation Dan sets: this is a critical step, ADW integration comes later, and *"engineering happens in the gray."* Don't let a reader think the codebase is a plug-and-play out-loop machine.

---

## 2. The repo already uses the current SDK — state it, don't "correct" it

**What the lesson shows:** On-screen code and narration both use the **Claude Agent SDK** (`claude_agent_sdk`, `ClaudeAgentOptions`, `ClaudeSDKClient`, `create_sdk_mcp_server`, `@tool`, `HookMatcher`).

**What's true now:** Identical — this is the current SDK. (Contrast AH-3, where Dan said "Claude Code SDK" over already-renamed code.)

**Book treatment:** A one-line reassurance callout: *"The SDK names in this lesson are current — `claude-agent-sdk` / `ClaudeAgentOptions`."* Then teach the durable primitive (options = the core four → mount `ClaudeSDKClient` → `query()` → manage the response stream), and mark specific message/block field names as "current at recording; re-check the SDK reference," since those still drift.

---

## 3. Course-era model IDs — and a real internal inconsistency in the repo

**What the lesson shows:** On-screen badges read **SONNET-4.5** and **HAIKU-4.5**; `config.py` pins `DEFAULT_MODEL = claude-sonnet-4-5-20250929` and `FAST_MODEL = claude-haiku-4-5-20251001`; the meta-agent template uses Opus.

**What's true now / the bug:** The orchestrator **system prompt** (`orchestrator_agent_system_prompt.md`) still documents `haiku`/`fast` → **`claude-3-5-haiku-20241022`** (old 3.5 Haiku), while the code resolves those aliases to **`claude-haiku-4-5-20251001`**. The app README also shows a stale example `ORCHESTRATOR_MODEL=claude-sonnet-4-20250514`. The **code is source of truth.**

**Book treatment:** Keep IDs as period-accurate quotes, but teach the **principle** (Haiku-class for scouts/summaries/high-volume; Sonnet-class for primary work; Opus-class for the meta-agent). Footnote the system-prompt/README staleness so a careful reader trusts the code + the on-screen 4.5 badges, and never hardcode a model ID as a takeaway.

---

## 4. Stale docs & ports inside the repo (use the code/scripts as truth)

**What the lesson/repo shows:** The inner `apps/orchestrator_3_stream/CLAUDE.md` says backend **"port 8002"** and references files that **no longer exist** (`src/data/testData.ts`, a `ThinkingBlockRow`); `types.d.ts`'s `WSMessage` union is vestigial; `src/components/ColorChangeBox/` is an empty dir.

**What's true on disk:** Backend runs on **9403** (README + `.env` + `start_be.sh` + the frontend all agree); frontend on **5175**. `modules/hooks.py` is **legacy/orphan** (no importers) — the active hooks are `command_agent_hooks.py` + `orchestrator_hooks.py`.

**Book treatment:** In the lab, tell students to trust `start_be.sh` / `.env` / the running app over the doc comments (ports **9403 / 5175**). Mention `hooks.py` is dead code so no one studies the wrong file. These are ordinary repo-drift gotchas, not lesson errors.

---

## 5. This is a private, bespoke system — the pattern is the payload, not the app

**What the lesson shows:** A polished custom Vue + FastAPI + Postgres observability app.

**What's true now:** Dan is emphatic it is **not a product you must adopt:** *"I'm not here to tell you how to set up your multi-agent orchestration or even that you need to use this… I don't care what user interface you use."* Big labs are shipping primitive one-agent-at-a-time versions; this is the paradigm ahead of them.

**Book treatment:** Frame the codebase as a **reference implementation to learn the pattern from** (single interface + CRUD-for-agents + observability + out-loop), explicitly transferable to *any* tool — even a plain terminal. Don't teach it as a dependency; teach the three pillars.

---

## 6. Config-path & setup gotchas (lab-relevant)

**What's true on disk:** The backend's `config.py` computes `PROJECT_ROOT` so it loads **`apps/orchestrator_3_stream/.env`**, *not* the repo-root `.env` — and there are two divergent `.env.sample` files. `.mcp.json.sample` must be renamed to `.mcp.json` (three servers: playwright, neon, firecrawl). DB migrations need `psql` on PATH.

**Book treatment:** Call these out in the **lab setup** (copy `.env` into the app dir; rename `.mcp.json`; ensure `psql`), the same way AH-3 flagged the Firecrawl `.sample` rename. Small, real, and otherwise silently confusing.

---

## 7. Features Dan explicitly marks as MISSING / future — don't present them as present

- **Human-in-the-loop decision points** (agents asking *you* questions) — *"That's missing here."*
- **Better orchestration-agent management + multiple codebases through one UI** — the server currently targets **one `--cwd` at a time**.
- **Forking an agent's context window** / duplicating an agent from a point — *"one tool away… a few modules away."*
- **Prompt-engineering autocomplete/tab** (a cheap fast model in the terminal) — *"the highest return on investment."*

**Book treatment:** Keep these in a clearly-labeled "future directions / not-yet-built" box so a reader doesn't go looking for them in the codebase.

---

## What has NOT aged (teach as current, verbatim)

- **The scale framework** — Base → Better → More → Custom → Orchestrated; scale compute to scale impact. Timeless.
- **The three pillars** — Orchestrator + CRUD-for-agents + Observability. Model-agnostic architecture.
- **Observability is a pillar** — "can't measure → can't improve/scale"; results-oriented, filterable, diff-able.
- **Primary agents vs sub-agents** — persistent/re-promptable vs ephemeral; pull a template up a level.
- **Core four at scale + R&D** — read any agent by its core four; keep the orchestrator thin.
- **PITER out-loop (tactic 4), one-agent-one-prompt-one-purpose (tactic 6), prioritize-agentics (tactic 8).** Durable tactics.
- **Template your engineering / defensibility** — specialization is the moat; out-of-the-box tools serve everyone's codebase, not yours.
- **The sleep-check loop as prompt-driven glue; every agent produces a concrete result.** Patterns, not tool trivia.
- **The O-agent is part of, and the key to, the agentic layer** — usable before the layer exists. The most durable claim of the lesson.

---

## Strict YouTube-overlay decision (map-to-lesson / named-gap only)

Two candidates map to *this lesson's* named holes with no topic drift; both `include_in_phase1 = true`, both `verify_before_publish = true` (IDs carried from the tac-1 seed list; no video was fetched, per brief — confirm each resolves and re-check the title before shipping the link):

| video_id | title | maps_to | why it's allowed |
|----------|-------|---------|------------------|
| `fop_yxV-mPo` | Codebase Singularity | named hole (Gap 1/5) | The O-agent is *"the key to unlocking how to best organize, create, and use your agentic layer"* and the self-operating-codebase end-state. Deferred from tac-1 as "too much scale for lesson 1" — AH-4 **is** the scale chapter, so it's now on-topic. |
| `6fCqj4xFCZI` | How Claude Code CHANGED Engineering Forever | named hole (Gap 2/5) | The whole system rests on *"the Claude Agent SDK and the ecosystem… far ahead of the pack… the extensibility of this tool."* Bridges that claim to the current state of the SDK/ecosystem. |

**Deferred (do not surface on this chapter):** `X2ciJedw2vU` (ZERO to Agent SKILL) — the lesson confirms "orchestrator and agents can use skills," so a Skills primer *maps*, but Skills are the heart of the AH-3/skills lessons, not the orchestration chapter. Keep it in the volume map (`include_in_phase1 = false`). Broader "AI-labs multi-agent product" videos would drift into speculation — Dan makes the "big labs will build this" point himself; no overlay needed.

# MA-1 — Outdated vs Current (recording era → book build)

MA-1 was recorded ~March 2026 (briefs are dated 2026-03-17…22) and teaches primitives that age well, but it is closer to the frontier than the TAC lessons, so more of its *specifics* drift. For each item: what the lesson shows, what current practice is, and whether the book needs an overlay or a callout. Two of these are not "aging" at all — they are **spec-vs-implementation gaps** a technical reader must know regardless of date.

---

## 1. Model versions: near-future placeholders that already drift  ⟵ period detail

**Recording era:** CEO on **Opus 4.6**, board on **Sonnet 4.6**; the retrieval chart benchmarks **Sonnet 4.5, GPT-5.4, Gemini 3.1 Pro**; the multimodel config wires Qwen 3.5, Kimi K2.5, MiniMax M2.7, Xiaomi MiMo v2 Pro, Gemini 3 Flash.
**Current (book baseline):** the Claude line is newer (Opus 4.8 / Sonnet 5 / Haiku 4.5 / Fable 5). The exact strings — and the harness's `/claude-.*-4-6/` regex that stamps the "1M" TUI badge — are frozen at record time.
**Book treatment:** margin note on model-bearing frames ("version strings are period detail; the tactic is model-agnostic — 'the models must be able to maintain long context'"). Update the roster strings if reproducing.
**Overlay:** none.

## 2. 1M true context: headliner → table stakes

**Recording era:** framed as a fresh, singular unlock — "no model lab has been able to do this while maintaining a model that's actually useful"; flat price, no post-200K surcharge.
**Current:** long context at flat(ish) pricing is broadly available across labs by publish time; the "only Anthropic can do this" framing is a snapshot. The *pedagogy* holds — long context is what lets an agent hold a whole business + compounding expertise in one session.
**Book treatment:** "current practice" callout — keep the teaching (why long context enables the pattern), date-stamp the competitive claim, and re-check the retrieval-benchmark landscape before repeating "no one else can do this."
**Overlay:** none required (the on-screen MRCR chart, frame `t0076`, carries the point).

## 3. Two spec-vs-implementation gaps in the v1 harness  ⟵ not aging; verify against shipping code

**a. converse is PARALLEL, not "sequential."** `ceo.md` documents converse as "sequential — later members see earlier responses from the same round." The extension runs targets with `Promise.allSettled` (parallel), matching Dan's narration. **Within a round, members respond blind to each other;** cross-pollination only happens across rounds via the shared `conversation.jsonl` (their prompts say "reread the entire conversation").
**b. "Contrarian speaks last" is not enforced.** README, `ceo.md`, and `contrarian.md` all claim it; `end_deliberation` collects final statements in **config order** (Contrarian is 4th of 8) with no reordering.
**Book treatment:** teach both explicitly as "what the docs say vs what v1 does." A later version may implement sequential rounds or true ordering — **re-check the shipping code before presenting either as a guarantee.**
**Overlay:** none.

## 4. Custom harness (Pi) vs. the moving extensibility landscape

**Recording era:** Pi-specific — TypeScript extensions, `pi` subprocess spawn, custom TUI, `.pi/` structures; positioned as "one of the only true Claude Code competitors" because of the customization.
**Current:** Pi's API and Claude Code's own extensibility (plugins, hooks, subagents, background tasks, the Agent SDK) all move fast. The **transferable claim is durable**: customize your harness down to the primitives (tool registration + subprocess/session control) and you leave the normal distribution.
**Book treatment:** sidebar — "this pattern can be built on any harness that exposes custom tools + subprocess/session control; Pi is the vehicle, not the point." Keep the `converse`/`end_deliberation` design as the reusable shape.
**Overlay:** the **Pi coding agent vs Claude Code** video Dan links on-screen (source the ID from the channel and verify).

## 5. Single-vendor demo vs the model-diversity ideal

**Recording era:** Dan says "agent model diversity is super super important," then runs the demo **all-Claude** because other labs lacked true 1M context. A parallel `agents-multimodel.yaml` already wires cross-vendor models via OpenRouter.
**Current:** as more labs ship true long-context models, the diversity path (different model families per seat) becomes the natural default — the config is already there.
**Book treatment:** present the all-Claude demo as the teaching baseline and the multimodel config as the "here's the diversity upgrade" — update the recommendation as long-context parity spreads.
**Overlay:** none.

---

## What has NOT aged (teach with full confidence)

- **Uncertainty in, decision out** as the design discipline: know inputs and outputs, then build the workflow.
- **Adversarial specialists** > one strong generalist agent — controlled biases and opposing time horizons expose blind spots.
- **Real constraints (time + budget)** on an agent run — the min/max engine is a durable pattern for *any* long-running agentic system.
- **Template your engineering** — validated, required-section inputs force good prompt engineering and make agents repeat your work.
- **Observability first** — log the whole deliberation (conversation + tool use); measure to improve.
- **Compounding expertise files** — persistent, domain-specific scratch pads as a distinct concept from vague "memory."
- **Specialization beats the normal distribution** — change more than one of the core four; go up a level to the harness.
- **The one-shot / locked-input design** — a deliberation tool is not a chat; constrain the interaction surface.
- **"Prompt engineering is very much still alive."**
- **Agentic engineering > agentic coding** — decisions are higher-leverage than code; "coding is just the beginning."

## Phase-1 overlay decision (strict, per brief: max 1–3)

| # | Video | Maps to | Include |
|---|---|---|---|
| — | `TqjmTZRL31E` — *Pi CEO Agents. Claude 1M Context. Multi-Agent Teams.* | the lesson's own public video (provenance, not an overlay) | n/a |
| 1 | **Pi coding agent vs Claude Code** (Dan links it on-screen) | named hole — customizable agent harness (innovation 2) | ✅ (verify ID) |
| 2 | Agent Experts / expertise-file pattern (Agentic Horizon) | named hole — agent expertise (innovation 3) → map to internal ch. `ah-5-agent-experts` first | ❌ defer |

*Caveat (per brief, no video fetching performed): only the lesson's own ID (`TqjmTZRL31E`) is confirmed. The overlay IDs must be sourced from the IndyDevDan channel and verified — and content-checked against the title — before publishing links. Do not fabricate IDs.*

---

## Reproduction / accuracy caveats for the chapter builder

- The codebase is **member-exclusive** (Tactical Agentic Coding + Agentic Horizon). The lab must not assume public cloning; frame it as "inside the course codebase."
- The lesson author's note "2K lines is not a great design pattern here — I need to break this up" applies to `ceo-and-board.ts`; treat the current module split (`modules/*.ts`) as the tidied state.
- Frames `t0076` (small burned-in caption) and `t1672` (composited over desk B-roll) are legible but not pristine slides; clean SVG sources exist in `images/main/` if the chapter wants crisp vector versions.

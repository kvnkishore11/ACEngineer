# AH-5 — Outdated vs Current (course era → mid-2026)

Agent Experts ages well because it teaches a **pattern over primitives** (Act/Learn/Reuse over an expertise file, all reducing to the core four), and Dan repeatedly says to break the rules and use whatever abstraction fits. Six things have moved since recording. For each: what the course shows, current practice, and whether the book needs an overlay.

---

## 1. Agent memory: a detached expertise file vs Claude Code's memory features  ⟵ the design conversation to have

**Course era:** Dan deliberately rejects always-loaded **memory files** (CLAUDE.md-style) for experts because "expertise requires breaking rules when the time is right" and forced global context can't detach when it should. Instead he uses a **dedicated, topic-scoped, agent-maintained** expertise file loaded on demand by the expert prompt.
**Current:** Claude Code's memory surface has grown — CLAUDE.md imports/hierarchy, and an Anthropic **memory tool / pattern** for cross-session state. These make "give the agent memory" easier, but they don't decide *what shape* that memory should take.
**Book treatment:** overlay-as-contrast, not correction. Teach Dan's argument — **topic-scoped, self-maintained, on-demand** memory beats always-on memory for experts — then map it onto today's memory features so the reader chooses deliberately. Note: he explicitly says you *can* use memory files with auto-update if you like; he just prefers a detached file.
**Overlay:** best served by a memory/self-improving-agents video (see decision table #1 — ID needs sourcing).

## 2. Packaging: raw prompt-file expert → Agent Skills (and the Agent SDK)

**Course era:** experts are raw slash-command prompt files under `.claude/commands/experts/<domain>/` plus a YAML expertise file, orchestrated with in-Claude-Code primitives (`SlashCommand` inside `Task`, `TaskOutput`).
**Current:** **Agent Skills** (`SKILL.md` + progressive disclosure) are the first-class, discoverable, on-demand encoding — a natural home for an expert (a skill that loads its expertise file and a self-improve routine). Dan half-predicts this on camera (*"skills boil down to prompts"*), and the repo's **meta-skill already scaffolds Skills**. For production, the **Claude Agent SDK** (Python/TS) wraps Act/Learn/Reuse outside an interactive session — and the Nile product expert *already uses it* (`ClaudeSDKClient`, `@tool`, `create_sdk_mcp_server`).
**Book treatment:** teach the raw prompt-file expert first (pedagogically perfect — no magic), then show the same expert as a Skill and note the SDK path for non-interactive/production use.
**Overlay:** `X2ciJedw2vU` — *RAW Agentic Coding: ZERO to Agent SKILL* (include_in_phase1: **yes**, pending ID re-verification).

## 3. Orchestration: slash-command chaining → SDK subagents/hooks

**Course era:** `plan_build_improve.md` chains three fresh sub-agents via the `Task` tool, each running a slash command; context is protected by spawning fresh agents.
**Current:** the same "isolate each step in a fresh subagent" idea is a supported SDK pattern (structured output, hooks, permission modes, subagents). The concept — **context delegation** — is unchanged; the machinery is richer and works headlessly.
**Book treatment:** sidebar ("the `Task`-chaining you see has a grown-up SDK form"); concept identical.
**Overlay:** none required.

## 4. Models & speed: course-era Claude 4.5 family, Opus→Haiku swap

**Course era:** on-screen model IDs are `claude-opus-4-5-20251101`, `claude-sonnet-4-5-20250929`, `claude-haiku-4-5-20251001`; Dan drops Opus→Haiku live "just for speed."
**Current:** newer families (Opus 4.x → 5, etc.) change **nothing** about the pattern. "More compute = more confidence" and "as models improve, false-expertise error rates drop" are the durable claims; specific IDs are period detail.
**Book treatment:** one-line margin note on affected frames ("model IDs are period detail; the pattern is identical today").
**Overlay:** none.

## 5. False expertise → evaluation, drift-control, and review gates

**Course era:** Dan names **false expertise** as inherent ("I have false expertise... expect this") and predicts "great sophisticated models to fact check things," but the lesson's control is mostly the self-improve validation loop (line limit + YAML compile + validate-against-code).
**Current:** for high-stakes experts, teams add **evals**, periodic **re-seeding**, and **diff-review gates** on the expertise file — treat each self-improve output like a pull request, especially in billing/security. This is the missing playbook the book should supply.
**Book treatment:** "current practice" callout after the challenges section; frame the expertise diff as a reviewable artifact.
**Overlay:** none identified (topic-anchored; source if a good one exists).

## 6. Product/generative-UI experts: still latency-bound, more viable

**Course era:** the Nile per-user expert streams generated UI sections; Dan is explicit it's a **seed, not production** — agents too slow for real-time recommendations — and calls for "UI hacks" (loading bars, streamed sections) to mask latency.
**Current:** streaming component protocols, tool-driven UI, and faster small models make adaptive/generative UI more practical than at recording, but it remains latency-sensitive. Still an *emerging class*, not a ship-today recipe.
**Book treatment:** frame as "a class of product to watch/prototype," carry Dan's caveat forward verbatim.
**Overlay:** none required.

---

## What has NOT aged (teach with full confidence)

- The core thesis: agents forget → don't learn, and the fix is a **stored, self-maintained mental model**. More consensus now than at recording.
- **Act · Learn · Reuse** as the minimal anatomy of a learning agent.
- **Expertise file = mental model, not a source of truth**; the code is the only source of truth and the file is re-validated against it.
- **Never hand-edit the expertise file — fix the self-improve step.** ("Build the system that builds the system.")
- The **partial vs complete** distinction (the missing Act step).
- **Seeding loosely** + **hard line limits** + **expect false expertise**.
- **When-to / when-not** judgment (high-risk/complexity/error-rate/evolving vs static/simple/new/no-mental-model).
- **Everything reduces to the core four** — pick the abstraction (skill/subagent/MCP) by ergonomics.
- **More compute = more confidence** (parallel experts, composed).

## Phase-1 overlay decision (strict, per brief: max 1–3)

| # | Video | Maps to | Include | ID status |
|---|---|---|---|---|
| 1 | *(IndyDevDan video on agent memory / self-improving agents / "agents that learn")* | operationalizes tactic (the exact thesis) | ✅ | **NEEDS LOOKUP — no verified ID; source before publishing** |
| 2 | `X2ciJedw2vU` — RAW Agentic Coding: ZERO to Agent SKILL | named hole (packaging an expert as a Skill) | ✅ | inherited from TAC-1 seed list — verify resolves & matches |
| 3 | `fop_yxV-mPo` — Codebase Singularity | named hole (build-the-system / agentic layer) | ❌ defer to **AH-6** | inherited from TAC-1 seed list — verify |

*Caveat (fail-loud): only #2 and #3 carry inherited IDs (from the TAC-1 orchestration seed list) and even those must be re-verified for topical match to THIS lesson. #1 is the strongest match by topic but has **no confirmed video ID** — it is intentionally left `video_id: null` in extract.json and must be sourced before any overlay link is published. No video fetching was performed in this pass, per brief.*

## A note for the chapter author

The single best "current practice" upgrade to weave through this chapter is the **memory-vs-expertise-file** contrast (gap #1) and the **Skill/SDK packaging** (gap #2) — both are things Dan *gestures at himself*, so they read as "here's where this went," not "here's what Dan got wrong." Keep the raw prompt-file expert as the primary teaching form; the modern encodings are the "grown-up form" sidebars.

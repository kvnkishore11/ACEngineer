# AH-2 — Outdated vs Current (mid-2026)

The **concepts** in this lesson — the trifecta, the seven levels, the composable sections, input→workflow→output, system-vs-user — have aged extremely well. What drifts is **packaging and tooling**. Treat course-era specifics as period detail; treat the tactics as current.

Rule of thumb: the tier list is timeless; the model ids and MCP dependencies are not.

---

## 1. Reusable expertise now ships as first-class **Agent Skills** (SKILL.md)

- **Course-era:** reusable prompts live as `.claude/commands/*.md` slash commands; reusable behavior lives as sub-agents in `.claude/agents/*.md`.
- **Now:** Claude Code has **Agent Skills** — `SKILL.md` with frontmatter, progressive disclosure, and on-demand discovery — as the current idiom for packaging reusable engineering so it's discoverable, composable, and shareable. The seven-levels vocabulary maps 1:1 onto a Skill body; the packaging upgraded. The Level-7 "self-improving Expertise" idea also overlaps with today's memory/knowledge-file patterns.
- **Book treatment:** teach the levels/sections exactly as filmed (they're the substance), then add a margin note: "today you'd often package a Level 2–4 workflow prompt as a Skill." Do **not** rewrite the labs onto Skills — the slash-command form is the clearest teaching vehicle.

## 2. Pinned course-era model ids (`claude-opus-4-1-20250805`)

- **Course-era:** `quick-plan.md` and `background.md` hard-code `model: claude-opus-4-1-20250805`; the README aliases and metaprompt default to generic `sonnet`/`opus`.
- **Now:** model families have moved on (Opus 4.8, Sonnet 5, Haiku 4.5, Fable 5). The **Metadata `model:` field is exactly where you swap these.**
- **Book treatment:** annotate the two frames that show the pinned id (`t0765` quick-plan, `t2020` background) with a "period detail — pick the current best model" callout. This axis moves fastest; flag it for re-check at publish time.

## 3. Background/headless delegation → the **Claude Agent SDK** + richer headless flags

- **Course-era:** `background.md` shells out to `claude --print --append-system-prompt … --dangerously-skip-permissions --output-format text` with `run_in_background`.
- **Now:** that still works and is the clearest teaching form, but production delegation uses the **Claude Agent SDK** (Python/TS), structured `--output-format json/stream-json`, session resume, permission modes, and typed hooks — which is precisely what **AH-3 (Claude Code SDK)** builds toward. Same concept (agent as callable component; append vs overwrite system prompt), richer machinery.
- **Book treatment:** keep the CLI demo; add a forward-link box to AH-3 for "the grown-up version."

## 4. Parallel delegation → **worktree isolation** + first-class background tasks

- **Course-era:** `parallel_subagents.md` fires N `Task` sub-agents in a single batch.
- **Now:** still valid, but current practice adds **git-worktree isolation** for agents that mutate files concurrently, plus background-task orchestration and multi-agent workflow tooling. The delegation ceiling is far higher (dozens of isolated agents) than the single Task fan-out shown. **AH-4 (the O-agent)** scales exactly this.
- **Book treatment:** note the ceiling is higher than one terminal; cross-link AH-4.

## 5. Firecrawl-MCP doc scraping is **one** context-loading option

- **Course-era:** `load_ai_docs.md` depends on the Firecrawl MCP server (WebFetch fallback), with a 24-hour TTL.
- **Now:** broader native web tooling and MCP options exist; the "load docs into `ai_docs/` for agents to read" pattern is one instance of the **R&D (Reduce/Delegate)** context engineering from **AH-1**. Concept is durable; the specific MCP dependency and TTL are implementation detail.
- **Book treatment:** teach the pattern; footnote the specific MCP as swappable.

---

## What has NOT aged (teach verbatim)

- **The stakeholder trifecta** — you/your team/your agents. More true now, not less.
- **The seven levels and the ~13 composable sections** — the entire tier list. The definitive artifact of the lesson.
- **Workflow is the pillar** (S useful / C skill) — still the highest-ROI section to master.
- **Input → Workflow → Output** and **static vs dynamic variables** — pure design wisdom, tool-agnostic.
- **System vs user prompts** — scope & persistence; the framing is timeless and leads straight into agent-building.
- **Consistency is king / "be bored of your format"** — the cultural core; unchanged.
- **"Three times marks a pattern"** and the **coworker test** — durable heuristics.

---

## Overlay decision (strict: map-to-lesson / named-gap only)

Per the fan-out brief, **max 1–3** overlays with `include_in_phase1: true`. This brief supplied **no seed ID list** (unlike TAC-1), so video IDs are intentionally left `null` with `needs_id_verification: true` — Codex/Hermes must source and verify real IDs from the IndyDevDan channel before publishing links. **Do not fabricate IDs.**

| Overlay (topic) | Maps to | Phase 1? | Why |
|---|---|:--:|---|
| **Agent Skills** (Zero → Agent Skill) | corrects outdated / named gap | ✅ | Upgrades slash-command packaging to SKILL.md — the single biggest current-practice gap (§1). |
| **Claude Code SDK** (build your own agent w/ custom system prompt) | named gap / lesson's own "next lesson" pointer | ✅ | Direct continuation of the system-vs-user section; Dan explicitly forwards here (AH-3). |
| **Context Engineering** (R&D framework: priming vs memory files) | map-to-lesson (prerequisite) | ⛔ hold | Repeatedly cited (AH-1) as the basis for delegate/prime; better as a linked prerequisite than a phase-1 overlay. |

Everything else (general prompt-engineering hype, unrelated build demos) is **out** — topic drift.

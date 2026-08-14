# AH-1 — Outdated vs Current (course era → mid-2026)

AH-1 ages well because it teaches *principles of context* (measure, reduce, delegate, own your window) on top of tool features that keep evolving. Dan future-proofs on camera repeatedly: *"You might have a model in the future... context management is still critically important"* and *"these techniques are all the same across models. Don't get stuck up on any one individual model."* Six things have moved. For each: what the course shows, what current practice is, and whether the book needs an overlay.

---

## 1. Reusable expertise: hand-rolled Agent Experts → first-class Agent Skills  ⟵ the big named gap

**Course era:** Technique #12 encodes reusable expertise as a plan/build/improve slash-command triad with a hand-maintained `## Expertise` section, self-updated by an `improve` meta-command reading the `git diff`. Brilliant, but discovery, loading, and sharing are all hand-rolled.
**Current:** Agent Skills (`SKILL.md` with frontmatter — name, description, trigger guidance) are the first-class encoding: discovered and loaded on demand, shareable across projects/teams, composable. They're the modern answer to "how do I package what my agent knows about this subsystem?" — exactly what the expert triad answers primitively.
**Book treatment:** overlay + sidebar. Teach the codebase's plan/build/improve triad first (no magic, and the self-updating loop is genuinely additive), then show the same idea as a Skill.
**Overlay:** an IndyDevDan Skills/hooks video (`corrects outdated`; include_in_phase1: **yes**) — ID needs sourcing (see note).

## 2. Embedding: bare `--append-system-prompt`/`--print` → headless mode + Claude Agent SDK

**Course era:** Techniques #10–11 use CLI flags — `--append-system-prompt`, `--print`, `--output-format text`, `--dangerously-skip-permissions`, `run_in_background=true` — and `scripts/bg_claude_code_test.sh` as the raw shell form.
**Current:** the pattern survives verbatim (and remains the clearest teaching form), but production embedding adds richer headless flags (`--output-format json|stream-json`, `--allowedTools`, `--permission-mode`, session resume) and the **Claude Agent SDK** (Python/TS): structured output, hooks, subagents, multi-turn control. The lesson itself points you to the "Claude Code SDK Mastery" extended lesson for this.
**Book treatment:** sidebar ("the flag you just used has a grown-up SDK form"), not a rewrite — the concept (agent as callable, steerable component) is unchanged.
**Overlay:** a Claude Code / Agent SDK video (`named hole`; include_in_phase1: **yes**) — ID needs sourcing.

## 3. Output styles → a broader customization surface

**Course era:** Technique #4 teaches output styles that "hot-swap the output-style block in the system prompt" (One Word Output, Ultra Concise, TTS, Bullet Points, YAML Structured), selected via `/output-style` or `settings.local.*.json`.
**Current:** output styles still exist, but Claude Code's customization surface has broadened (plugins, settings layering, and Skills sit alongside output styles). Dan explicitly names *hot-swapping the system-prompt block* as a trend to watch — and it broadly played out.
**Book treatment:** footnote + "current practice" callout; the durable point is "control the response layer to cap your most expensive (output) tokens."
**Overlay:** none required.

## 4. Models & the on-screen numbers: period detail, pre-handled by Dan

**Course era:** `/context` shows `claude-opus-4-1-20250805` and `claude-sonnet-4-20250514`; `quick-plan.md` pins `model: claude-opus-4-1-20250805`; token breakdowns (63k boot, 24.1k MCP, 23.7k memory, 6.5k firecrawl, 2,650 README) are record-time exact.
**Current:** newer model families (Claude 5 / Opus 4.x era); token accounting shifts with model and tool changes. None of it invalidates a technique — the demo is about *proportions and habits*, not specific counts.
**Book treatment:** one-line margin note on affected frames ("model ids and counts are period detail; the technique is identical today"). Update the pinned model id when adapting the codebase. No overlay.

## 5. Repo state on camera ≠ shipped repo (MCP sample filenames)

**Course era:** the on-screen file tree shows `.mcp.json.all_22k`, `.mcp.json.firecrawl_4k`, and `.mcp.json.empty`.
**Current/shipped:** the repo ships `.mcp.json.all_16k.sample`, `.mcp.json.firecrawl_7k.sample`, and `.mcp.json.sample` (no `.empty`). The self-fixed token counts baked into filenames (4k/7k/16k/22k) reflect the MCP surface at record time vs ship time.
**Book treatment:** teach from the *shipped* filenames; footnote the on-screen names/numbers as record-time detail. Not a defect — a snapshot difference.
**Overlay:** none.

## 6. `/compact` vs reset-and-prime: a stance, and compaction keeps improving

**Course era:** Technique #7 is deliberately opinionated — avoid `/compact`, `/clear` + `/prime` instead, because after compaction you don't know your exact state.
**Current:** `/compact` remains a legitimate built-in and has grown (custom summarization instructions, auto-compact). The *durable* lesson is "know and own your exact window state, especially out-loop"; the specific avoidance is a tunable practice as compaction gets more controllable.
**Book treatment:** present as Dan's reasoned stance with the "own your window" principle foregrounded; note that compaction tooling has improved. No overlay.

---

## What has NOT aged (teach with full confidence)

- **The R&D framework.** Reduce and Delegate is a complete, model-agnostic taxonomy for context management.
- **A focused agent is a performant agent.** More true as fleets scale, not less.
- **Measure to manage.** `/context` + a tokenizer remain the two right instruments; the "you can't manage what you don't measure" logic is timeless.
- **The context sweet spot / attention-vs-length problem.** Models still lose capability as windows grow — the reason context engineering is "a safe bet."
- **Own your context window.** Don't delegate its control to a memory file or a compactor. Unchanged.
- **Sub-agents as partially forked (system-prompt-isolated) windows; primary delegation as independent instances.** The distinction and its token economics hold.
- **Architect/editor split; one agent, one purpose; compose into ADWs.** The pipeline logic is the backbone of current multi-agent practice.
- **Self-improving experts (plan/build/improve, update only the Expertise section).** The *loop* is current even as Skills become the packaging.
- **Spend tokens properly, not minimally.** The reliability framing (avoid re-work, one-shot out-loop) is exactly today's cost logic.

## Phase-1 overlay decision (strict, per brief: max 1–3 include_in_phase1)

| # | Candidate (topic) | Maps to | Include | ID status |
|---|---|---|---|---|
| 1 | IndyDevDan — context engineering / context-window management | operationalizes tactic (whole thesis) | ✅ | needs sourcing + oembed-verify |
| 2 | IndyDevDan — Claude Code sub-agents / delegation | named hole (T5/T11 current practice) | ✅ | needs sourcing + oembed-verify |
| 3 | IndyDevDan — hooks / Agent Skills / Agent SDK | corrects outdated (T8/T10/T12 → Skills+SDK) | ✅ | needs sourcing + oembed-verify |
| 4 | IndyDevDan — AI Developer Workflows / multi-agent orchestration | named hole (T9 → ADW at scale) | ❌ defer | needs sourcing |

**Critical caveat (per brief + no-fabrication rule):** AH-1 had **no seeded overlay list** in `data/curriculum.json` (`overlays: []`) and the chapter brief provided none. I have **not invented YouTube IDs**. Each phase-1 candidate is a *topic to source*: the chapter build/review stage must find the real IndyDevDan video, confirm the ID resolves via oembed, and verify the content matches the mapped role before publishing the overlay link (exactly as TAC-1's cross-review did for its seeded IDs). Keep `include_in_phase1` to at most 3.

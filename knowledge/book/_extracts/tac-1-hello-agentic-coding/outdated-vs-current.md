# TAC-1 — Outdated vs Current (course era → mid-2026)

TAC-1 ages unusually well because it teaches primitives, and Dan future-proofs on camera: *"Your Claude Code UI might look different. You might be using newer models. That's all great... Don't let that distract you from the value embedded in each lesson."* Still, five things have moved. For each: what the course shows, what current practice is, and whether the book needs an overlay.

---

## 1. Reusable agent behavior: prompt files → Agent Skills  ⟵ the big named gap

**Course era:** reusable behavior is encoded as a raw prompt file (`programmable/prompt.md`) plus launcher scripts. Works, but discovery, triggering, and composition are all manual.
**Current:** Agent Skills are the first-class encoding — `SKILL.md` files with frontmatter (name, description, trigger guidance), loaded on demand by Claude Code and shareable across projects/teams. Skills are the modern answer to "how do I package the thing my agent knows how to do?" — exactly the question `programmable/` answers primitively.
**Book treatment:** overlay REQUIRED. This is the course's most-cited gap ("Skills as modern encoding of engineering"). Teach prompt.md first (pedagogically perfect: no magic), then show the same workflow as a Skill.
**Overlay:** `X2ciJedw2vU` — *RAW Agentic Coding: ZERO to Agent SKILL* (include_in_phase1: **yes**).

## 2. Embedding: bare `claude -p` → headless mode + Claude Agent SDK

**Course era:** `claude -p "<prompt>"` via subprocess from sh/ts/py; output captured as plain text; REPORT requested inside the prompt itself.
**Current:** the pattern survives verbatim (and remains the best teaching form), but production embedding now uses headless flags — `--output-format json|stream-json`, `--allowedTools`, `--permission-mode`, session resume — and, for real systems, the Claude Agent SDK (Python/TS): structured outputs, hooks, subagents, multi-turn control. What TAC-1 calls "programmable agentic coding" grew into a supported product surface.
**Book treatment:** sidebar ("the 3-line script you just wrote has a grown-up form"), not a rewrite — concept unchanged: agent as callable component.
**Overlay:** `6fCqj4xFCZI` — *How Claude Code CHANGED Engineering Forever* (include_in_phase1: **yes**).

## 3. Permissions: flat allowlist → modes, hooks, sandboxing

**Course era:** `.claude/settings.json` with a flat `permissions.allow` list (`Read`, `Write`, `Edit`, `Bash(uv run:*)`, four git patterns, `WebSearch`).
**Current:** that syntax still works, but the surface grew: permission modes (plan/accept-edits/etc.), pre/post tool-use hooks, sandboxed bash, deny rules, and settings layering (user/project/local). Teams gate agents with hooks, not just allowlists.
**Book treatment:** footnote + "current practice" callout. The lesson's HABIT — always read what the agent may do before running it — transfers unchanged and is the actual teaching point.
**Overlay:** none needed.

## 4. Models & UI: period detail, pre-handled by Dan

**Course era:** course-era Claude models and TUI; Aider cited as the phase-1 analogue.
**Current:** newer model families (Claude 4.x → Claude 5 era), richer TUI, plan modes, background tasks. None of it invalidates a frame of the lesson — the demo is deliberately primitive-level.
**Book treatment:** one-line margin note on affected screenshots ("UI is period detail; the flow is identical today"). No overlay.

## 5. Scale: one serial loop → fleets, subagents, parallel worktrees

**Course era:** one agent, one workflow, serially, in one terminal — deliberately, since it's lesson 1 of 8.
**Current:** the same agentic prompt is routinely fanned out: subagents, background tasks, git-worktree-isolated parallel runs, orchestrated pipelines. "Systems that build systems" now has industrial-strength machinery.
**Book treatment:** forward-pointer only ("the course scales this in later lessons; today's ceiling is higher still"). Overlaying scale content on lesson 1 would front-run the pedagogy.
**Overlay candidates (deferred to later chapters):** `fop_yxV-mPo` — *Codebase Singularity*; `hGg3nWp7afg` — *3 Codebase Folders* (both include_in_phase1: **no**).

---

## What has NOT aged (teach with full confidence)

- The phase-1/phase-2 frame and "AI coding is not enough" — if anything, more consensus now than at recording.
- The core four. Context/model/prompt/tools remains the complete diagnostic vocabulary for agentic failures.
- The agentic prompt as workflow-specification (RUN/CREATE/RUN/REPORT) — this shape is now everywhere (slash commands, skills, CI prompts).
- "Scale and performance, not novelty" as the right lens on tool calling.
- The three-essential-elements checklist for evaluating agentic tools.
- Terminal ubiquity as the embedding superpower.
- Report-back as the first closed-loop habit.
- The economics: token spend as pay-to-play. (Costs shifted; the logic didn't.)

## Phase-1 overlay decision (strict, per brief: max 1–3)

| # | Video | Maps to | Include |
|---|---|---|---|
| 1 | `2TIXl2rlA6Q` — AI Coding is NOT ENOUGH | operationalizes tactic (lesson thesis, phase model) | ✅ |
| 2 | `6fCqj4xFCZI` — How Claude Code CHANGED Engineering Forever | named hole (form factor + programmable embedding, current state) | ✅ |
| 3 | `X2ciJedw2vU` — RAW Agentic Coding: ZERO to Agent SKILL | corrects outdated (skills gap) | ✅ |
| 4 | `fop_yxV-mPo` — Codebase Singularity | self-operating vision → later lessons | ❌ defer |
| 5 | `hGg3nWp7afg` — 3 Codebase Folders | context engineering → later lessons | ❌ defer |

*Caveat: IDs/titles from the orchestration brief's seed list; verify each resolves and content matches title before publishing overlay links (no video fetching was performed in this extract pass, per brief).*

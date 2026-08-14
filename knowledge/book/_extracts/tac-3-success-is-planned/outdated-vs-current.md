# TAC-3 — Outdated vs Current (course era → mid-2026)

> The demo is pinned to its era by one JSONL line: `"model":"claude-opus-4-20250514"` (frame t2270). Everything below maps course-era mechanics to current practice; the tactic itself has not aged a day.

## 1. Slash-command templates: plain markdown → frontmatter + dynamic context

**Then:** `.claude/commands/*.md` are bare markdown bodies with one `$ARGUMENTS` slot; all context arrives via the agent's own research ("Start your research by reading the README.md file").
**Now:** commands support YAML frontmatter (`description`, `argument-hint`, `allowed-tools`, `model`), positional `$1`/`$2`, inline `` !`bash` `` output injection, and `@file` references — a 2026 chore.md could inject `git ls-files` itself and pin a planning model.
**Book treatment:** teach Dan's plain form first (it still runs verbatim), then show the same chore.md upgraded with frontmatter as a sidebar. The anatomy (purpose/instructions/relevant-files/format/parameter) transfers unchanged.

## 2. Templates were proto-Skills  ⟵ the big named gap

**Then:** reusable encoded engineering lives as repo-local command files you copy between projects by hand.
**Now:** Agent Skills (SKILL.md + frontmatter, auto-discovery, on-demand loading, bundled scripts) are the first-class packaging for exactly what this lesson calls "templating your engineering" — discoverable, composable, shareable across repos and teams.
**Book treatment:** map template → skill explicitly; keep slash-command templates as the lightweight repo-local tool for plan generation, skills as the team-scale/reusable-expertise tier. Overlay video: X2ciJedw2vU.

## 3. THINK HARD: magic words → first-class thinking controls

**Then:** literal phrases (think < think hard < ultrathink) mapped to escalating extended-thinking budgets; Dan calls it an "information dense keyword" Anthropic encoded.
**Now:** thinking is a first-class toggle/config in Claude Code and newer models manage reasoning budgets more autonomously; the literal words still nudge but are no longer the primary interface.
**Book treatment:** date the mechanism ("course-era trigger"), keep the principle (deliberately buy reasoning compute for planning-grade work) as current.

## 4. Headless posture: --dangerously-skip-permissions → scoped alternatives

**Then:** the demo bypasses permissions wholesale for a planning-only run; Dan scopes it honestly ("very low risk... for now").
**Now:** `--allowedTools` allowlists, permission modes, hooks as pre/post-tool gates, sandboxed bash, and the Claude Agent SDK (Python/TS) are the production embedding path; `--output-format stream-json` remains exactly how harnesses consume agents.
**Book treatment:** quote Dan's scoping as the lesson (risk is scoped, not ignored); show the modern equivalent invocation in a current-practice box. Overlay video: 6fCqj4xFCZI.

## 5. Native plan mode now exists — and does NOT replace specs/

**Then:** planning is hand-rolled: template → markdown plan in `specs/` → committed to the repo.
**Now:** Claude Code ships a built-in plan mode (plan-then-approve inside a session).
**Book treatment:** the sharpest current-practice point in this chapter — in-session plans are ephemeral; Dan's `specs/` plans are durable, committable, team-visible, agent-reusable artifacts ("staging environments for code"). Modern best practice combines them: plan mode to draft, specs/ to persist. Do not let students read "plan mode exists" as "this lesson is obsolete."

## 6. Fresh-agents doctrine → today's context-engineering tooling

**Then:** manual discipline — new terminal, new instance per phase; Dan name-drops coming tricks ("parallel agents... isolated sub agent context windows").
**Now:** /clear, /compact, subagents with isolated contexts, background tasks, worktree-parallel fleets automate what Dan did by hand.
**Book treatment:** the doctrine (one agent one task; known context at boot; zero-dependency assets; presence → 0) is verbatim-current; only mechanics got easier. Deferred overlay: fop_yxV-mPo (whole-arc payoff, hold for a later chapter).

## What has NOT aged (teach with full confidence)

- Plan = prompt scaled up; great planning is great prompting.
- Template anatomy: purpose / instructions / relevant files / plan format / parameter — and per-class specialization (chore vs bug vs feature).
- Meta prompts and HOPs as composition primitives (prompts building prompts; prompts consuming prompts).
- Plans in `specs/` as committed, improvable codebase artifacts with embedded Validation Commands.
- The two-phase, two-agent split (plan → implement) and the three fresh-agent reasons.
- One-shot successes / decoupling from the conversational context window / presence-KPI framing.
- The security demo's engineering content: keyword blocklists are not SQL-injection protection; parameterize + centralize execution (the shipped code's flaws are real and still instructive).
- "Do not wait" — run one small /chore on a real repo to get the aha moment.

## Phase-1 overlay decision (strict, per brief: max 1–3)

**Include (2):** X2ciJedw2vU (templates → Skills; corrects outdated) · 6fCqj4xFCZI (headless/programmable Claude Code today; fills the claude -p named hole).
**Defer (1):** fop_yxV-mPo (Codebase Singularity — self-operating end state; belongs to a later chapter after ADWs land).
**Caveat:** no tac-3-specific seed list was provided; these IDs come from the tac-1 orchestration seed list (oembed-verified there) and are mapped only where genuine. If the orchestrator supplies a dedicated planning/spec-prompting video for tac-3, slot it ahead of these.

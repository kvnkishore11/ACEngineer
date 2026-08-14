# TAC-2 — Outdated vs Current (course era → mid-2026)

TAC-2 is built to age well on purpose — its opening argument is "bet on the aspects that never change" (the SDLC), and the 12 leverage points are tool-agnostic primitives. What HAS moved is the machinery around four of them: templates, tools, the run-server-inside-the-agent trick, and permissions/docs conventions. For each: what the course shows, what current practice is, and the book treatment.

---

## 1. Templates: bare .claude/commands → Agent Skills + richer commands  ⟵ the big named gap

**Course era:** the templates leverage point = markdown prompt files in `.claude/commands/` (install/prime/tools, plus `/start` minted on camera). No arguments, no frontmatter, no discovery — fire by name, and compose by having one prompt read-and-execute another.
**Current:** slash commands gained `$ARGUMENTS`, frontmatter (`allowed-tools`, descriptions), and user/project scoping; and the concept graduated into **Agent Skills** — `SKILL.md` packages with trigger descriptions, on-demand loading, bundled scripts/resources, shareable across projects and teams. Dan's definition ("reusable, embeddable, agentic prompts") describes Skills almost verbatim, three years early.
**Book treatment:** overlay REQUIRED. Teach the lesson's raw form first (it's transparent — you can read all 16 lines of install+prime+tools), then show the same `/start` workflow as a Skill.
**Overlay:** `X2ciJedw2vU` — *RAW Agentic Coding: ZERO to Agent SKILL* (include_in_phase1: **yes**; note — also used in chapter 1; drop here first if the stitcher wants zero reuse).

## 2. The /tools roster: period snapshot of Claude Code's toolset

**Course era:** the on-screen list — `Task` (subagent for keyword/file searches), `Bash(command, description?, timeout?)`, Glob/Grep/LS/Read/Edit/MultiEdit/Write, NotebookRead/NotebookEdit, WebFetch/WebSearch, TodoRead/TodoWrite, exit_plan_mode.
**Current:** the roster has churned: typed subagents replace bare Task-as-search, todo tools became richer task systems, background Bash + output polling exist, plan mode reshaped, giant stdout auto-truncates, MCP tools mount dynamically. Several names on Dan's screen no longer exist as shown.
**Book treatment:** margin note on the t0630 frame ("period roster; run /tools-style introspection yourself — the habit is the lesson"). The transferable core — tools live in the system prompt, ask for them, read parameter definitions, exploit details like `timeout` — is unchanged.
**Overlay:** none needed.

## 3. Running the app inside the agent: fixed Bash timeout → background tasks

**Course era:** the lesson's cleverest move — `sh ./scripts/start.sh, 300s` — blocks one foreground Bash call for up to five minutes so server stdout lands in context. Hard ceiling: when the timeout expires (or you interrupt), the server dies with it.
**Current:** long-lived processes run as background tasks; the agent starts the server, keeps working, and polls its output on demand — no five-minute ceiling, no blocking. Same leverage point (agent sees runtime stdout), industrial machinery.
**Book treatment:** sidebar on the t0965 frame: "today you'd background this — the 300s trick is the concept in its rawest form." Concept unchanged: get runtime output into the context window.
**Overlay:** none needed.

## 4. Agent docs: verbal CLAUDE.md nod, none committed → standardized conventions

**Course era:** Dan credits "/prime in combination with the claude.md" for fast ramp-up — but tac-2 ships **no CLAUDE.md**; README.md + prime carry the role. The docs leverage point is taught via `ai_docs/` (vendored third-party quickstarts) and "spread agent-facing markdown through your tree."
**Current:** root CLAUDE.md auto-loaded each session (bootstrapped by `/init`), nested CLAUDE.mds for subsystems, AGENTS.md interop, settings layering — the distributed-agent-docs idea is now paved road. `ai_docs/`-style local vendoring remains a best practice (context7-style MCP servers notwithstanding, local = drift-free and token-cheap).
**Book treatment:** teach the absence honestly (it's a great retrieval question: "where would this repo's CLAUDE.md go and what belongs in it?"), then the current convention.
**Overlay:** `hGg3nWp7afg` — *3 Codebase Folders* (include_in_phase1: **yes**) — the current-practice answer to organizing agentic assets (ai_docs/specs/commands), and the payoff of Dan's "don't refactor yet — future lessons organize agentic assets" promise.

## 5. YOLO mode & permissions: a toggle and a flat list → modes, hooks, sandboxes

**Course era:** auto-accept edits ("yolo mode") plus a `settings.json` that is already ahead of tac-1: allow-list of nine Bash patterns + Write, and a **deny list** (`git push --force`, `git push -f`, `rm -rf`).
**Current:** permission modes (plan / acceptEdits / bypassPermissions), pre/post tool-use hooks, sandboxed execution, org/user/project/local settings layering. The repo's deny-list instinct is exactly where the ecosystem went — policy over vibes.
**Book treatment:** footnote + callout on the settings read-aloud lab step. The habit (know what the agent may do; forbid the catastrophic) transfers unchanged.
**Overlay:** none needed.

## 6. KPIs: markdown + mental tracking → measurable proxies

**Course era:** size/attempts/streak/presence tracked in a scratch markdown file and "floating around your mind"; systematize "inside GitHub or Jira or whatever you wanna use."
**Current:** session logs, OTEL metrics, cost/usage dashboards, and PR-per-agent-run workflows give real numbers: run duration ≈ size, retry counts ≈ attempts, consecutive green runs ≈ streak, human-interaction counts ≈ presence. The definitions were ahead of their tooling and hold up unmodified.
**Book treatment:** keep Dan's four definitions canonical; one sidebar mapping each to a modern measurable.
**Overlay (deferred):** `fop_yxV-mPo` — *Codebase Singularity* (include_in_phase1: **no**) — the presence→0 / self-running-codebase end-state; reserve for the ADW lessons.

## Bonus period details (mention only if the chapter touches them)

- `llm_processor.py` pins `gpt-4.1-mini` and `claude-3-haiku-20240307` — course-era model IDs; the app runs fine with current IDs swapped in (a nice stretch drill, agent-performed).
- Dan's status bar shows CPython 3.12.8 while the README says both "3.10+" (prerequisites) and "3.12+" (troubleshooting) — internal README inconsistency, pyproject says `>=3.10`.
- Claude Code shows "Read 154 lines" for the 153-line README (trailing newline) — not a discrepancy.

---

## What has NOT aged (teach with full confidence)

- The 12 leverage points as a taxonomy and, more importantly, as a **failure diagnostic**.
- Tactic #2 and the litmus question — if anything, MORE true now that agents run longer and further from supervision.
- "Your agent can only see what you let it see" — stdout/observability as the first lever; silent failure = bad agentic code.
- Fix-the-system-not-the-bug: engineering the conditions so agents resolve issues.
- Types as IDKs and the type-flow trace prompt — works verbatim in any current agent.
- The agent navigation problem; consistency as the antidote; "if it's hard for you, it's hard for your agent."
- Tests as closed-loop structures; "if you're not writing tests, you're probably vibe coding."
- Plans-are-prompts and the abstraction ladder (plans → templates → ADWs) — this IS the modern agentic stack's shape.
- The four KPIs and the streak diagnostic.
- The three-time rule.

## Phase-1 overlay decision (strict, per brief: max 1–3)

| # | Video | Maps to | Include |
|---|---|---|---|
| 1 | `hGg3nWp7afg` — 3 Codebase Folders | operationalizes tactic (agentic-asset organization: ai_docs/specs/commands) | ✅ |
| 2 | `X2ciJedw2vU` — RAW Agentic Coding: ZERO to Agent SKILL | corrects outdated (templates → Skills) | ✅ (reused from ch.1 — drop first if needed) |
| 3 | `fop_yxV-mPo` — Codebase Singularity | named hole (ADW / presence→0 end-state) | ❌ defer to ADW lessons |

*Caveat: IDs/titles come exclusively from the tac-1-era vetted seed list — no new IDs searched or invented, no videos fetched in this pass, per brief. Oembed-verify at review time.*

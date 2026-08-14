# TAC-8 — Outdated vs Current (course era → mid-2026)

TAC-8 ages well for the same reason TAC-1 does: it teaches an allocation decision and a set of primitives, not a toolchain. Dan future-proofs it on camera — *"keep your eyes on the primitives… Claude Code represents the first viable engineering tool that unlocks agentic engineering, but it won't be the last."* The **concepts** (two layers, MVAL, template meta prompts, ADWs, triggers, PITER→PITE, the guiding question) are unchanged. What has moved is the **packaging** of each primitive — every hand-rolled mechanism in the five apps now has a first-class successor. Seven gaps; for each: what the course shows, what current practice is, and whether the book needs an overlay.

---

## 1. Reusable behavior: `.claude/commands/*.md` libraries → Agent Skills  ⟵ the big named gap

**Course era:** every reusable behavior is a slash-command prompt file (`.claude/commands/chore.md`, `plan_uv_mcp.md`, `process_tasks.md`…) invoked by name from ADWs. This is "template your engineering" done primitively — and pedagogically perfect, because there's no magic to hide behind.
**Current:** Claude Code packages reusable expertise as **Agent Skills** — `SKILL.md` with frontmatter (name, description, trigger guidance), loaded on demand, shareable across repos and teams. The lesson's meta-prompt concept maps 1:1; discovery, triggering, and composition all upgraded.
**Book treatment:** overlay + sidebar. Teach the `.claude/commands` form first (it's the load-bearing concept), then show the same template as a Skill.
**Overlay:** `X2ciJedw2vU` — *RAW Agentic Coding: ZERO to Agent SKILL* (already anchors the TAC-1 chapter; **defer** here to avoid double-placement — see table).

## 2. The agent call: hand-rolled subprocess `agent.py` → Claude Agent SDK

**Course era:** every app copies a ~630-line `agent.py` that shells out to `claude -p "<prompt>" --output-format stream-json --model <m> --dangerously-skip-permissions`, with retry logic, a filtered subprocess env, and hand-parsed JSONL landing under `agents/{adw_id}/{agent}/`. Dan drives the CLI deliberately, "to have full control over how the agent is called."
**Current:** Dan already plants the successor on camera — app1 ships `agent_sdk.py` + `adw_sdk_prompt.py`, "a Python version and a bun version." That matured into the **Claude Agent SDK** (Python/TS): typed messages, sessions, hooks, subagents, structured outputs. Production ADWs start there; the subprocess form remains the clearest *teaching* form.
**Book treatment:** sidebar ("the ~630-line wrapper you're reading has a supported grown-up form"), not a rewrite — the concept (agent as a callable, observable component) is unchanged.
**Overlay:** none needed.

## 3. Permissions: `--dangerously-skip-permissions` everywhere → modes, sandboxing, hooks

**Course era:** all tac-8 ADWs bypass permissions entirely — fine for isolated throwaway demo repos, dangerous as a default habit.
**Current:** headless agents are gated with allowlists, **permission modes** (plan/accept-edits/…), sandboxed bash, deny rules, and pre/post tool-use **hooks**. The lesson's *isolation* instinct — git worktrees + sparse checkout, "double isolation" — is exactly right and is now complemented by first-class sandboxing; the blanket bypass flag is the dated part.
**Book treatment:** "current practice" callout on every `--dangerously-skip-permissions` screenshot. Teach the isolation habit as timeless; flag the flag.
**Overlay:** none needed.

## 4. Triggers: DIY cron/polling loops → native background agents, scheduled runs, CI hooks

**Course era:** app2/app4 poll with `schedule` loops inside long-running terminal processes (5s / 15s); app5 hand-rolls a FastAPI server. The trigger CONCEPT — the mechanism that fires ADWs without you — is the durable idea.
**Current:** map "trigger" to headless CI invocation, background tasks, scheduled cloud agents, and webhook-native integrations that ship out of the box. A modern reader should not assume a hand-rolled poller is required.
**Book treatment:** footnote + "current practice" callout. Keep the hand-rolled poller as the transparent teaching version; point to managed triggers as the production target.
**Overlay:** none needed (the trigger primitive is covered in-lesson).

## 5. Parallelism: one serial agent per task → first-class parallel subagents and orchestration

**Course era:** parallelism is achieved at the OS level — detached `subprocess.Popen(start_new_session=True)` per task, one Claude instance each, coordinated by markdown (`tasks.md`) or Notion state. Impressive, and deliberately transparent.
**Current:** in-band multi-agent primitives — subagents, parallel tool fan-out, worktree-isolated background agents, orchestration frameworks — express the same patterns inside the agent runtime, with less scaffolding. Same architecture, less glue.
**Book treatment:** forward-pointer + "current practice" note. The lesson's OS-level version is the best way to *understand* the architecture; note that the runtime now offers it natively.
**Overlay:** `fop_yxV-mPo` — *Codebase Singularity* (include_in_phase1: **yes** — this IS the lesson's end-state).

## 6. Models, paths & MCP wiring: period detail, pre-handled by Dan

**Course era:** scripts toggle `sonnet|opus` of the course era; app5's start script hard-codes Dan's local `claude` path; the Notion MCP server and `.mcp.json` format are course-era versions.
**Current:** newer model families and MCP server versions; all incidental. Swap in current model names/paths and everything runs. Dan future-proofs this explicitly ("tools will change and models will improve — we can't fixate").
**Book treatment:** one-line margin note on affected screenshots ("model names / local paths are period detail; the flow is identical today"). No overlay.

## 7. AEA: a hand-built preview of in-product agents → standard architecture

**Course era:** app5's agent-embedded application (SQLite session store + `--resume` + in-app chat windows behind a Cmd+P console) is a from-scratch demo of a product agent.
**Current:** the Agent SDK supports embedding long-lived, session-resuming agents into products directly. "Outside the loop is inside the application" has gone from clever demo to a recognized pattern.
**Book treatment:** "this was ahead of its time" callout; the mechanism (persist `cc_session_id`, pass it with `--resume`) is exactly what the SDK now formalizes.
**Overlay:** none needed.

---

## What has NOT aged (teach with full confidence)

- **The two layers.** Application layer vs agentic layer is the complete diagnostic frame for "where is my time going?" — more true now, not less.
- **The guiding question.** *Am I working on the agentic layer or in the application layer?* — and the three (only three) acceptable reasons to be in the app layer: a deadline, testing by hand, or running prompts in-loop to verify they'll work out-loop.
- **The ≥50% allocation rule** and the parabolic-ROI argument ("10 minutes in, two hours out").
- **The MVAL:** `adws/` + `.claude/commands/` + `specs/`, with the single rule — compose code, reference files, stay isolated from the app layer; language is free choice.
- **Template meta prompts and the Plan Format** — a prompt that generates a self-verifying plan (step-by-step tasks + validation commands). The self-checking loop is the timeless part.
- **Problem classes, not one-offs** — the unit of agentic-layer work ("I have solved the problem class… it's done").
- **The gateway/observability contract** — one agent call, managed state, four output files. Every later system assumes it.
- **Composed ADWs coupled by explicit report contracts** — deterministic glue + non-deterministic prompt, joined by a machine-parseable Report section.
- **Worktree + sparse-checkout isolation** ("double isolation") for safe parallel agents.
- **One agent, one prompt, one purpose** — and the discipline of breaking it exactly once, knowingly, with the mechanism (DB-persisted session id) engineered for it.
- **PITER → PITE** — drop the R only after encoded feedback loops + reliability streaks prove review is the bottleneck.
- **The economics thesis** — commoditization of implementation; value moves up the stack (system design, domain encoding, quality control) which you then encode in your ADWs.

## Phase-1 overlay decision (strict, per brief: max 1–3)

| # | Video | Maps to | Include |
|---|---|---|---|
| 1 | `fop_yxV-mPo` — Codebase Singularity | operationalizes tactic (the self-operating codebase = this lesson's end-state; explicitly deferred *to* this chapter from TAC-1) | ✅ |
| 2 | `hGg3nWp7afg` — 3 Codebase Folders | named hole (slows down on the MVAL folder-level reasoning the lesson races past) | ✅ |
| 3 | `X2ciJedw2vU` — RAW Agentic Coding: ZERO to Agent SKILL | corrects outdated (commands → Skills, gap #1) — but already anchors the TAC-1 chapter | ❌ defer (no double-placement) |

*Two included — within the 1–3 limit. Caveat: IDs/titles from the orchestration brief's seed list; verify each resolves and its content matches the title before publishing overlay links (no video fetching was performed in this extract pass, per brief).*

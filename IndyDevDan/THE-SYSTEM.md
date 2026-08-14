# THE SYSTEM
### IndyDevDan's Unified Agentic Engineering Method — one fixed procedure, applied identically to every unit of work

> Naming note: everything below keeps his exact names. Where eras conflict, the later code artifacts win (e.g. `/build` with `$1` supersedes `/implement` with `$ARGUMENTS`, though both shapes are canonical and interchangeable).

---

## 1. THE CORE MODEL

Five principles. Everything else in the system is a consequence of one of these.

1. **The Core Four** — every agent, tool, and multi-agent system reduces to **Context, Model, Prompt, Tools** (the earlier "Big Three" — context, model, prompt — plus tools, which is what makes coding *agentic*). Debug and design everything by asking which of the four is wrong or missing. Expanded for diagnosis into **The 12 Leverage Points**: Context, Model, Prompt, Tools (in-agent) + Standard Out, Types, Documentation, Tests, Architecture, Plans, Templates, ADWs (through-agent).

2. **The Plan is the Prompt** — the prompt is the fundamental unit of engineering; a plan is a prompt scaled up. "Great planning is great prompting." You define **What > How**; the spec file is the staging environment for code and the context handoff between agents.

3. **Build the System That Builds the System** — never fix agent output by hand; fix the template/prompt/ADW that produced it. **Template your engineering**: encode how YOU solve each problem class into reusable meta-prompts so a solved class stays solved. "Three times marks a pattern" is the trigger; ">50% of engineering time on the agentic layer" is the budget. Governing economics: **Compute Advantage** = (Compute Scaling × Autonomy) / (Time + Effort + Cost); "scale your compute to scale your impact"; "spend tokens to save time."

4. **One Agent, One Prompt, One Purpose** — "a focused agent is a performant agent." Every task gets a fresh, memoryless agent instance; context is managed by exactly two operations, the **R&D Framework**: **Reduce** what enters the window, **Delegate** work to other windows. **Adopt your agent's perspective**: give it exactly what you would use to solve the problem, and nothing more (Minimum Context Principle).

5. **Close Every Loop** — every unit of work carries validation commands the agent runs itself until feedback is positive; claims are never proof, only deterministic tool output is (**"Agents plus code beats agents alone"** — agents propose, code disposes). Progress is measured by four **Agentic KPIs**: **Size ↑, Attempts ↓ (target 1), Streak ↑, Presence ↓** (out-loop best = 2 touchpoints: prompt + review; ZTE = 1: prompt only — "zero presence" is the directional slogan, not a literal target). More compute must equal more trust; trust is the metric — the length of correct tool-call chains you allow — and the North Star is **ZTE (Zero-Touch Engineering)**: your codebase ships itself.

---

## 2. ONE-TIME SETUP — installing the agentic layer

Build order derived from what appears in early vs. late codebases (TAC-1/2 → TAC-3 → TAC-4 → TAC-5/6/7 → AH → MA). The agentic layer is **physically isolated** from application code — it operates ON the app, never mixes with it.

### Step 0 — Directory skeleton (create empty, all at once)
```
repo/
├── .claude/
│   ├── commands/        # every reusable prompt, as markdown (the atomic unit of the system)
│   ├── agents/          # subagent system-prompt files
│   ├── hooks/           # uv single-file Python scripts, one per lifecycle event
│   ├── settings.json    # permission allow/deny lists + hook wiring + status line
│   ├── output-styles/   # (later) response-format contracts
│   └── skills/          # (later) on-demand capability packages
├── ai_docs/             # curated third-party docs pulled local ("don't make agents web-request every lookup")
├── specs/               # ALL generated plans (+ specs/patch/ later)
├── adws/                # AI Developer Workflow scripts (Python, uv single-file, PEP 723)
├── agents/              # runtime output: <adw-id>/ logs, background/, context_bundles/
├── app_docs/            # agent-generated feature docs
├── scripts/             # start/stop/copy_env; a justfile launchpad for humans AND agents
├── trees/               # git worktrees for parallel agents (later)
└── app/ or apps/        # application layer — NEVER mixed with the above
```

### Step 1 — Permissions & context hygiene (TAC-1/2 era)
1. `.claude/settings.json`: allow list (`Bash(uv:*)`, `Write`, …), deny list (`git push --force`, `rm -rf`, …).
2. **Delete the default `.mcp.json`.** Ship servers as `.mcp.json.<name>_<tokencost>.sample` (token cost in the filename); activate per-task via `claude --mcp-config <file> --strict-mcp-config`.
3. Shrink `CLAUDE.md` to ~40 lines of things you are 100% sure you want loaded 100% of the time. Everything else moves to prime commands.

### Step 2 — Priming & visibility commands
4. `/prime` — Purpose → Run (`git ls-files`) → Read (README + key files) → Report (summarize understanding). Add variants per area of focus later (`/prime_bug`, `/prime_cc`, …).
5. `/start` — runs the app inside the agent with a timeout (`sh ./scripts/start.sh 300s`) so stdout flows into context. `/tools` — lists the agent's tool definitions. `/install` — primes then installs deps (the prompt-in-prompt pattern).
6. **Standard-Out Enablement**: make the codebase talk to the agent — every exception AND every success prints to stdout before returning.

### Step 3 — The plan/build command pair (TAC-3 era; the heart of the system)
7. Template meta-prompts, one per problem class: `/feature`, `/bug`, `/chore`. Fixed anatomy (late-era Specified Format — the original TAC-3 template had no frontmatter; frontmatter arrives in the AH era and wins as the later artifact): frontmatter → Title → Purpose → Variables → Instructions (`IMPORTANT: Replace every <placeholder>`; `THINK HARD`) → Relevant Files ("Ignore all other files") → **Plan Format** (fenced template with `<placeholder>` micro-prompts) → the user's one-liner as the argument. Output: `specs/<kebab-name>.md`, always ending in **Validation Commands** ("zero regressions").
8. `/build` (earlier `/implement`) — the **Higher-Order Prompt (HOP)**: takes `PATH_TO_PLAN: $1`; if missing, STOP and ask. Read plan → think hard → execute every step top to bottom → run Validation Commands → Report with `git diff --stat`.

### Step 4 — Feedback infrastructure
9. Tests (mirror test folders to source structure — "tests are the rule of law"), linter, type check, build — the raw material of **Closed Loop Prompts** (Request → Validate → Resolve, rerun ALL validations top-to-bottom after any fix).
10. **Agent-ready architecture pass** (do it WITH your agent): verbose Information-Dense-Keyword names everywhere, types over dicts, ~1000-line file max, one responsibility per file, client/server split, README/CLAUDE.md spread through the codebase.

### Step 5 — Meta layer (install early — "every codebase must have meta agentics")
11. `/meta_prompt` (generates slash commands in the Specified Format), `meta-agent` (generates subagent files), `meta-skill`. Each embeds the exact output template and forbids extra sections.

### Step 6 — Hooks & observability (TAC-4 era)
12. `.claude/hooks/<event>.py` — uv single-file scripts named exactly after their lifecycle event, JSON from stdin, exit 2 blocks (PreToolUse guardrails), registered in settings.json with `uv run … || true`. Add the observability pipeline (events → server → dashboard): "without observability, you're vibe coding at scale."
13. Context-bundle hook: append-only JSONL trail of prompts + reads, enabling `/load_bundle` recovery to ~70% of a dead agent's state.

### Step 7 — The ADW layer (TAC-4→7 era)
14. `adws/adw_prompt.py` — a UV single-file script that calls ONE agent with ONE prompt via the `claude` CLI (`claude -p "<prompt>" --output-format stream-json …`, logged to JSONL). **"This script is the gateway into agentic coding."**
15. Chain into pipelines: `adw_plan_build.py` (classify issue → branch → plan agent → build agent, progress comments between steps), then composable `adw_{plan,build,test,review,document,ship}_iso.py` chained by `adw_sdlc_iso.py` (`_iso` = isolated git worktree), with `ADWState`/`adw_state.json` passed between scripts and a health-check ADW run first in any new environment.
16. **PITER** wiring: **P**rompt input (GitHub issues), **T**rigger (webhook or cron), **E**nvironment (worktree/container/dedicated device), **R**eview (PR + issue-comment feed with screenshot proof).

### Step 8 — Specialization layer (AH era)
17. Subagents (`.claude/agents/*.md`, minimal tools; thin agents fat prompts: body can be "Read and Execute: .claude/commands/<x>.md"), `/background` delegation (report file created BEFORE launch, renamed `*.complete.md`/`*.failed.md`), output styles, skills.
18. **Agent Experts** for high-risk domains: `.claude/commands/experts/<domain>/` = `expertise.yaml` (mental model, ≤ MAX_LINES) + `question.md` + `plan.md` + `self-improve.md` + `plan_build_improve.md`.

### Step 9 — Multi-agent layer (MA era; only when earned)
19. **Builder + Verifier** pair first (verifier: read-only tools, decomposes claims into atomic propositions, demands deterministic evidence, `verifier_prompt()` sends fixes back to the builder).
20. Then the **three-tier architecture** (orchestrator → leads → workers) composed from a YAML config + per-agent markdown files with front matter (model, expertise, skills, tools, domain locks); constraints enforced by the harness, not prompts; every session writes an append-only JSONL conversation log. Custom harness convention: `.pi/<system>/`, launched via justfile.

---

## 3. THE LOOP — the identical per-task procedure

This is **The Two-Prompt Loop** (plan phase + build phase). Run it for EVERY unit of work — chore, bug, or feature. In-loop at first; the same loop runs out-loop via ADW/PITER unchanged.

| # | Step | Artifact produced |
|---|------|-------------------|
| 1 | **Boot a FRESH agent** (never reuse a window; `/clear`, never `/compact`) and run `/prime` (or the area-specific prime). Check `/context` — target ~90% free. | Context summary in-window |
| 2 | **Fire the matching template meta-prompt** with a one-line description: `/feature "…"` (you pick chore/bug/feature yourself in-loop; a `/classify_issue` step exists only in the out-loop ADW pipeline, where it returns exactly `/chore`\|`/bug`\|`/feature`). Agent researches the codebase in reasoning mode ("think hard") and fills the Plan Format. | `specs/<kebab-name>.md` — the plan, ending in Validation Commands |
| 3 | **Review the plan** (human-in-the-loop planning scales with feature size; delete anything not needed for the build — "go overboard, then delete"). This is one of your only two touchpoints. | Edited spec |
| 4 | **Commit the spec** and current changes before implementing. | Git commit |
| 5 | **Boot a SECOND fresh agent** and run `/build specs/<name>.md`. The HOP reads the plan, thinks hard, executes every step in order, top to bottom. No priming needed — everything the builder needs is in the plan. | Code changes on a branch |
| 6 | **Agent closes its own loop**: runs every Validation Command; on any failure, fixes immediately and reruns ALL validations from the top until one clean pass. | Passing validation output |
| 7 | **Agent reports**: concise bullet summary + `git diff --stat`. | Report block |
| 8 | **Review the diff** (touchpoint two). Optionally verify via the plan's Steps to Reproduce / e2e markdown tests / screenshot proof. In multi-agent maturity, the **Verifier** does this step for you. | Approved diff (or verifier Report: STATUS + CONFIDENCE + atomic-claim counts) |
| 9 | **Commit** (each SDLC step commits its own changes). Out-loop: PR created, review/document/ship phases run as chained ADWs; `/document` writes `app_docs/` and updates the conditional-docs prompt. | Commit / PR / feature doc |
| 10 | **Improve the system, not the output**: if attempts > 1, diagnose which of the 12 Leverage Points was missing and install it; if this was the third time running a similar prompt, extract a slash command; if the work touched an expert's domain, run `self-improve` with `check_git_diff=true`. | Upgraded template / new command / synced `expertise.yaml` |

**Failure rule inside the loop:** the target is one shot (Attempts = 1). Hitting 3–6 attempts on the same task is the diagnosis trigger: stop prompting and fix a leverage point: confused by dicts → Types; can't navigate → Architecture; you're reading errors → Standard Out; "success" but bugs → Tests; short iterative prompts → Plans; repeated workflow → Templates.

---

## 4. DECISION RULES

| When… | Do… |
|---|---|
| You've done anything three times | Extract it to a `.claude/commands/` slash command (Level 1, bare minimum; enrich later). "Three times marks a pattern." |
| Writing any reusable prompt | Use the one fixed skeleton: frontmatter → Title → Purpose → **Variables** ($1/$2 dynamic first, static literals second) → Instructions (critical bullets prefixed `IMPORTANT:`) → **Workflow** (numbered) → **Report** (exact format). Omit unneeded sections. |
| Choosing a prompt level (Seven Levels: 1 high-level → 2 workflow → 3 control-flow → 4 delegation → 5 HOP → 6 template meta → 7 self-improving) | Start at 1; graduate only when you need the capability. **Levels 3–4 cover 80–90% of real work.** 5–7 are meta territory. |
| A required variable is missing | STOP immediately and ask — never guess. |
| A prompt's output feeds code | Return ONLY the parseable value (single `/command` token or raw JSON) — zero prose. |
| A step is deterministic (tests, lint, git, transforms, routing, retries) | Give it to code, not an agent — otherwise you pay a token tax. Behavior that must be *guaranteed* goes in hooks (block at PreToolUse; PostToolUse is feedback-only). |
| Context window fills mid-task | `/clear` → `/prime` → rebuild (or `/load_bundle`). **Never `/compact`.** Task too big for 200K → chop the task. |
| Tempted to add to CLAUDE.md | Test: "am I 100% sure I want this loaded 100% of the time?" No → put it in a prime command. |
| Choosing models | Strongest model (Opus-class) + "think hard" for planning, orchestration, meta-prompts; workhorse (Sonnet-class) default for building/workers; lightweight (Haiku-class) only for trivial tasks. Expose a `model_set heavy` IDK on the prompt input. Stack models across vendors — "it's an and, not an or." |
| Considering subagents | Only if you need specialization AND parallelization; otherwise a reusable prompt in the primary agent. Can't track one agent's Core Four → not ready for many. |
| Considering an MCP wrapper / full app | MCP only to combine services or fix an interface; app only with product vision. Always escalate the Five Agent Interaction Patterns left→right; "complexity should be earned, not assumed." |
| An area is high-risk/high-complexity (billing, DB, security) or agents keep erring there | Build an **Agent Expert** (Act-Learn-Reuse). Static problem / no mental model yet → plain prompt or skill instead. |
| Expert knowledge is wrong | Never edit `expertise.yaml` — fix `self-improve.md` (teach it HOW to learn) and rerun. |
| Going multi-agent | Only on mid-to-large production codebases where results outweigh tokens. Build **Builder + Verifier first**; three-tier orchestrator/leads/workers only to operate a whole domain. Cost min-maxing or small codebase → stay single-agent. |
| Acting as a leader agent (orchestrator/lead) | Read, delegate, synthesize, decide — NEVER write/edit/bash (exceptions: own expertise file; and if a worker/model fails mid-run, the lead does that work itself as fallback while the orchestrator reroutes to a healthy team). Default-route to ONE team; parallel round-robin only for independent work. |
| A domain is dangerous (DevOps, migrations, config) | Domain-lock it to exactly one agent via harness-enforced path permissions; lock bash to a single allowed script. |
| A high-leverage/irreversible decision (pricing, acquisition, career) | Don't chat with one agent — write a structured brief (Situation/Stakes/Constraints/Key Question) and run **CEO & Board** deliberation ("uncertainty in, decisions out": brief in → ranked memo with stances + dissent out); reject briefs missing sections. |
| Verifying work | Testing ≠ reviewing. Verifier claims need deterministic tool-output evidence; no evidence → "unsure", never "verified". Verification gap → template the missing rule/fixture/script, never a one-off prompt. |
| Rolling out autonomy | Trust Ladder: chores → bugs → features. Battle-test every prompt in-loop before it runs out-loop. |
| A problem class ships reliably (~5+ consecutive clean ships / ~90%) and your review catches nothing | Drop the R off PITER (**PETE**): remove review, add a Ship step — ZTE for that class. |
| Deciding what to work on at all | Ask "am I on the agentic layer or the application layer?" — ≥50% of time on the agentic layer; being on the app layer requires a stated reason. |
| A new tool/model drops | Evaluate against the Core Four and your private benchmarks (HOP/LOP eval: grade performance, speed, AND cost in an identical harness) — never leaderboards or hype. |
| Needing confidence / prototyping | Fusion thread: same prompt to N sandboxed agents across models, best-of-N, merge only the winner. |

---

## 5. THE LADDER — maturity levels and graduation criteria

Maps his three overlays onto one ladder: the **Velocity Scale** (in-loop → out-loop → ZTE), the **Agentic Layer Classes & Grades**, and the **Agent Evolution Path** (base → better → more → custom → orchestrated).

**Level 0 — AI Coder (in-loop, base agent).** Ad hoc back-and-forth prompting; knows the Big Three.
*Graduate when:* you run `/context` habitually, you can name the Core Four of your session, and you have stopped typing code.

**Level 1 — Reusable Prompter (Class 1, Grades 1–2).** `/prime` installed, slim CLAUDE.md, first slash commands, plan prompts writing to `specs/`, `ai_docs/`.
*Graduate when:* the Two-Prompt Loop (plan agent → fresh build agent) one-shots small chores; you never carry context across SDLC steps.

**Level 2 — Templated Engineer (Class 1, Grades 3–5).** `/feature` `/bug` `/chore` templates with embedded Plan Formats and Validation Commands; Closed Loop Prompts; custom tools/skills; standard-out wired; meta-prompts installed.
*Graduate when:* Attempts ≈ 1 across a multi-task Streak; agents self-validate with zero regressions; you diagnose every failure as a missing leverage point rather than re-prompting.

**Level 3 — ADW Operator (Class 1 Grade 6 → Class 2; out-loop).** `adw_prompt.py` gateway, chained plan→build→test→review→document pipelines, PITER wired (issues in, PRs out), worktree isolation, health checks, observability dashboard.
*Graduate when:* Presence = 2 touchpoints (prompt + review) for whole classes of work; Size measured in hours of agent runtime; prompts proven in-loop run out-loop unchanged.

**Level 4 — Orchestrated Specialist (Class 1 Grade 7 → Class 3; more/custom agents).** Agent Experts with self-improving mental models; Builder+Verifier pair live; custom SDK agents where needed; orchestrator commanding teams (leaders never execute, workers never improvise, every agent produces a concrete file artifact); harness-enforced constraints.
*Graduate when:* your cognitive input no longer scales with agent count (you talk to one orchestrator); verifier evidence replaces your review; expertise files compound across sessions untouched by you.

**Level 5 — ZTE / Codebase Singularity (Class 3 Grade 3; Z-threads).** PETE for trusted classes: prompt to production, no review. The codebase ships itself; nothing ships without your teams of agents; "to become irreplaceable, you replace yourself."
*Standing criterion:* trust — the length of correct tool-call chains you allow — keeps growing on all four KPI axes: more threads, longer threads, thicker threads, fewer human checkpoints.

---

## 6. SELF-IMPROVEMENT — how the system upgrades itself

The system improves through five closed loops, all governed by one law: **you don't fix the issue, you fix the system that caused the issue.**

1. **KPI diagnosis loop (every task).** Any broken streak or attempts > 1 → identify the missing leverage point of the 12 → install it → rerun. Because every run was a fresh agent on committed assets, you know 100% what was in context when it failed.
2. **Template extraction & specialization loop (weekly rhythm).** Three repetitions → new slash command. A generic template repeatedly missing a problem class → specialize it (front-end bug template, migration chore template). Solidified prompt chains → promote to ADWs (deterministic code + retries + logging). Mature ADWs → hand to the orchestrator. The meta layer (`/meta_prompt`, `meta-agent`, `meta-skill`) makes each extraction cheap.
3. **Expert Act-Learn-Reuse loop (per domain).** After any build in an expert's domain, `self-improve check_git_diff=true` diffs the mental model against the real code, remedies discrepancies, trims to MAX_LINES, validates the YAML compiles. Humans never edit `expertise.yaml`; if it learns wrong, you improve `self-improve.md`. "You have to let go. You have to teach your agents to operate as you would."
4. **Documentation feedback loop (per feature).** `/document` writes `app_docs/` AND appends to the conditional-docs prompt, so every future plan/bug/chore/patch/prime agent knows when to pull that doc — the SDLC's own closing loop.
5. **Verifier flywheel (per turn, at maturity).** Every "What could you not verify?" in a verifier Report becomes the next templated rule, fixture, or deterministic script in the harness — the harness deliberately removes the ability to answer with a one-off prompt. Each cycle converts a human-review gap into machine-enforced trust, which is what eventually earns each problem class its promotion to ZTE.

Prompts are the unit of all of this: because every prompt is a versioned file (no ad hoc prompts, ever), every improvement is a diff, every prompt is effectively an eval, and the whole agentic layer compounds — "build the system that builds the system."

---

## APPENDIX A — Full named-framework glossary

Frameworks he names that aren't already expanded above, one line each:

- **The 80/20 Three Tactics** — Tactic #1 Stop Coding; Tactic #2 Adopt Your Agent's Perspective; Tactic #3 Template Your Engineering.
- **Three Constraints of Agentic Engineers** — context window, codebase/problem complexity, your own abilities. Model intelligence is explicitly NOT a constraint.
- **SDLC as Questions** — Plan: what are we building? Build: did we make it real? Test: does it work? Review: is it what we planned? Document: how does it work?
- **Prompt Composition Hierarchy** (distinct from the Seven Levels of *formats*) — prompt → agentic prompt → reusable prompt → meta-prompt → plan → HOP → ADW. One primitive, composed upward.
- **Thread-Based Engineering taxonomy** — base thread (prompt → tool calls → review) plus P-thread (parallel), C-thread (chained w/ checkpoints), F-thread (fusion best-of-N), B-thread (big/meta: orchestrators spawning threads), L-thread (long-running high-autonomy), Z-thread (zero-touch). Improve on four axes: more threads, longer threads, thicker threads, fewer human checkpoints.
- **Five Pillars + Tokenomics** — own the agent harness; build factories not features; write extensible software; agentic access everywhere (CLIs/APIs/webhooks — agents only command what they can reach); always-on agents ONLY after climbing tokenomics: use more tokens → make tokens useful → capture value (else "token maxing").
- **Five Agent Interaction Patterns** — ad-hoc prompt → reusable prompt → subagents → workflow/MCP wrapper → full app. Escalate left→right only; "complexity should be earned, not assumed."
- **Infinite Agentic Loop** — Spec Analysis → Directory Recon → Parallel Coordination → QA → Wave Management, in waves of ~5 agents until context limits.
- **Scout → Build** — read-only scout investigates, builder implements from its findings; named `scout-<keyword>`/`build-<keyword>`; keep finished agents for inspection.
- **Type-Flow Tracing** — copy a type to a fresh zero-context agent: "show me how this type flows through the codebase."
- **HOP/LOP Evals** — private benchmarking: a LOP defines the test (prompt, agents, expected output, rubric); a HOP runs all agents in an identical harness and grades performance + speed + cost.
- **The Agentic Path** — base agent → better agent → more agents → custom agents → orchestrator agent.
- **CRUD for agents** — orchestrators create, command, read-status, and delete agents as temporary resources.
- **Stdout-overflow fallback ladder** — per-session log file → clean up logs → last resort: warnings/errors only.
- **Guiding preferences** — "Agent > Code > Manual Input"; prefer creation and reading over updates and deletions.
- **Hooks specifics** — 13 lifecycle events; UserPromptSubmit is "the first line of defense"; a Stop hook returning `decision: block` forces continuation.
- **Critical-build rule** — anything that will run hundreds of times: write the raw spec (`raw.md`) BY HAND first, then let agents expand it.

## APPENDIX B — Honest footnotes (genuinely unresolved in his material)

1. **Finished agents:** latest code says keep them for inspection/debugging/continuation; earlier AH orchestration says delete them as temporary resources. This manual follows the code (keep).
2. **ZTE promotion bar:** "~90% reliability" and "~5 consecutive clean ships" both appear; no single canonical number. Use the stricter.
3. **Expertise-file caps:** MAX_LINES 1000 for `.claude` experts, 10000 in the multi-team harness — treat as per-harness config; the invariant rule is "trim before you bloat."
4. **Naming drift:** `/implement` vs `/build`, `$ARGUMENTS` vs `$1` coexist even in late repos. Pick one per project; consistency itself is the rule.

---

*Provenance: distilled from TAC 1–8, Agentic Horizon 1–6, Multi-Agent 1–4 (transcripts + notes + course codebases), 53 public YouTube videos, agenticengineer.com and github.com/disler — by 7 parallel mining agents, one synthesizer, and one adversarial completeness critic. Compiled by Fable (Claude Fable 5), 2026-08-04.*


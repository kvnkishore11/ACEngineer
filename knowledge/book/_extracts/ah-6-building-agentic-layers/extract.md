# AH-6 — Building Agentic Layers · Master Teaching Notes

> **Lesson:** Agentic Horizon #6 (course order #14, Advanced) · **Course:** AH · **Runtime:** 1:06:24 (3984s @ native 1920×1080)
> **URL:** https://agenticengineer.com/tactical-agentic-coding/course/building-agentic-layers
> **Codebase:** `agentic-horizon/orchestrator-agent-with-adws` (Dan's "final gift"; his local copy is `o-agent-with-adws`) — a Class-3-Grade-3 agentic layer wrapping a bundled `apps/` application layer.
> **Meta-tactic:** *Prioritize Agentics* (Tactic 08) — build the system that builds the system; prioritize your agentic layer.

This is the technical-accuracy extract for the **capstone** lesson of the whole 14-lesson arc (TAC 1–8 + AH 1–6). It exists so the chapter author and a weak student can trust every claim, name, number, and file path. Each major idea follows the teaching model: **Hook → Picture → Worked example → Name → Failure → Retrieval.**

---

## The one-sentence thesis

**Your codebase now has two layers — the application layer (the code that serves users) and the _agentic layer_ (the ring of agentic primitives that lets agents operate that code on your behalf) — and building/leveling the agentic layer is the highest-ROI action any engineer can take.** The lesson gives you a ruler for that layer (three **Classes**, each with **Grades 1..N**), a concrete build order, and a destination: the **codebase singularity**, the moment your agents can run your codebase better than you can.

Everything you learned across TAC and AH is a component of this one buildable object.

---

## The spine of the lesson: the Class/Grade ladder

Three classes, each defined by a **unique element**. Grades within a class each add a **new dimension**. Everything **stacks** — Class 3 still contains Class 1 and Class 2. You (1) locate your class+grade, (2) raise your grade, (3) jump classes.

| Class | Unique element | Grades | The two hard "jumps" |
|---|---|---|---|
| **Class 1 — In-loop** | Agentic primitives you run in the terminal | G1 prime+memory · G2 sub-agents · G3 custom tools · G4 closed loops · G5 templates · G6 prompt chains · G7 agent experts | — |
| **Class 2 — Out-loop** | A system that runs agents **without you** (webhooks/triggers; the "PITER framework") | G1 out-loop fabric (webhook→Agent SDK) · G2 full AI Developer Workflows | **in-loop → out-loop** |
| **Class 3 — Orchestrated** | An **orchestrator agent** that CRUDs other agents | G1 the orchestrator · G2 orchestrator dev workflows · G3 orchestrator runs ADWs | **out-loop → orchestrated** |

> The goal is **not** to sprint to Class 3. It is to recognize where you are, name the missing piece, build it, and feel it move you forward. "A lot of engineers are probably missing agent experts."

---

## Idea 1 — The agentic layer (the new ring around your codebase)

**Hook.** After 13 lessons of tactics, Dan says there is ONE framework at the center that, if you capture it, changes how you engineer forever.

**Picture.** [Frame `t0382`] Green squares form a ring — the **agentic layer** — around dark inner squares — the **application layer**. Three progressively larger rings are Class 1, 2, 3. The application layer bundles *everything*: DB, front/back end, scripts, DevOps, notebooks — and **multiple apps** under one `apps/` directory (git submodules for related repos) so agents can see the whole product at once.

**Worked example.** In the repo, the agentic layer is the root `.claude/` (24 commands, 7 sub-agents, 2 skills, 3 experts, 9 hooks) plus `adws/`; the application layer is `apps/*` (a Vue markdown-preview SPA, a Python Pomodoro CLI, a static HTML page, the Nile shopping demo, and the orchestrator apps themselves) — heterogeneous apps operated by **one shared, specialized** agentic layer.

**Name it.** *The agentic layer.* "The new ring around your codebase where you teach your agents to operate your application on your behalf as well and even better than you and your team ever could."

**Failure mode.** Thinking the agentic layer is "just my `.claude` folder" or "just prompts." It is a graded, specialized system you invest in and maintain like a first-class product, wrapping all your related apps.

**Retrieval.** *What two layers should every codebase now have, and which squares are which in Dan's diagram?* → Application (inner/dark: DB, front/back, scripts, DevOps, notebooks, multiple bundled apps) and agentic (outer/green: the primitive ring).

---

## Idea 2 — The codebase singularity (the destination)

**Hook.** "Once you've built a sufficiently powerful agentic layer, something will happen." It sounds crazy, Dan admits, far out.

**Picture.** You, the engineer, realizing: my agents can now run my codebase better than I can. Nothing ships to production without my teams of agents.

**Worked example.** Dan says he uses working versions of this in production codebases and it is "like nothing else." The lesson makes it *buildable* by walking the ladder to Class-3-Grade-3, where an orchestrator runs observable AI Developer Workflows end to end.

**Name it.** *The codebase singularity* — reached via *zero-touch engineering* (Tactic 7), the North Star of TAC and AH.

**Failure mode.** Reading it as fear or hype about full autonomy tomorrow. "This is not something to fear, it's something to run toward." It is a threshold you build toward incrementally and can attain in a real configuration today.

**Retrieval.** *Define the codebase singularity.* → The moment your agents can run your codebase better than you can and you trust them to ship more than you trust yourself or your team.

---

## Idea 3 — Class 1, the in-loop ladder (Grades 1→7)

This is the concrete build order for a brand-new codebase. Each grade adds exactly one dimension.

| Grade | Unique element | Real files in the repo | Frame |
|---|---|---|---|
| **G1** | Prime prompt + memory files (thinnest layer) | `.claude/commands/prime.md`, `CLAUDE.md`, `AGENTS.md` | t0382 (smallest ring) |
| **G2** | Sub-agents (+ `specs/`, `ai_docs/`) | `.claude/agents/docs-scraper.md` (fetch-docs), `scout-report-suggest*.md`, `planner.md` | t0812 |
| **G3** | Custom tools: skills, MCP servers, prime-with-tools | `.claude/skills/start-orchestrator/`, `.mcp.json.sample` (postgres/firecrawl/notion) | t0895 |
| **G4** | Closed-loop prompts (request→validate→resolve) | `.claude/commands/review.md`, `fix.md`; `app_review/`, `app_fix_reports/` | t1088 |
| **G5** | Templates (bug/feature/chore) | `.claude/commands/plan.md` (task_type switch), `plan_w_scouters.md` | t1288 |
| **G6** | Prompt chains / agentic workflows | `orch_scout_and_build.md`, `build_in_parallel.md`, `adws/adw_workflows/adw_plan_build.py` | t1768 |
| **G7** | Agent experts (mental models) | `.claude/commands/experts/{adw,database,websocket}/` | t2015 |

**Worked example — Grade 3 (the "interesting" jump).** [Frame `t0895`] A real `.mcp.json` wires postgres, firecrawl, atlassian, and notion MCP servers. But Dan's key move: *skills and MCP servers can both be replaced by a simple prompt.* `prime_db` teaches an agent to run PSQL directly — no MCP needed, no token bloat. "You can bypass everything by just understanding how the core four works."

**Worked example — Grade 4 (feedback loops = TAC-5).** [Frame `t1088`] `review.md` (model: opus, analysis-only) reads git diffs, sorts issues into 4 risk tiers (Blocker/High/Medium/Low), ends PASS/FAIL, and writes `app_review/review_<timestamp>.md`; `fix.md` resolves them. Evidence lands on disk. *"More compute should equal more trust, not less. If it's less, you're doing something wrong."*

**Worked example — Grade 5 (templates).** [Frame `t1288`] The layer annotated with `bug.md`, `feature.md`, `chore.md`, `new_api_endpoint.md`… In the repo this is consolidated into `plan.md`, which classifies `task_type (chore|feature|refactor|fix|enhancement)` and emits a conditional plan format. *"This is where you can truly template your engineering and teach your agents to build like you do."*

**Worked example — Grade 6 (prompt chains).** [Frame `t1768`] `scout_then_plan.md`: "Launch Parallel Scouts → collect → synthesize → plan," spawning scouts via the `Task` tool. **The rule:** never build a plan-build-review chain you *can't* run piece-by-piece — otherwise you can't isolate the one step that breaks, and you can't scale pieces into parallel sub-agents.

**Worked example — Grade 7 (agent experts = AH-5).** [Frame `t2015`] `.claude/commands/experts/adw/` holds `expertise.yaml` (a **mental model**, not a source of truth — the code is) plus the ACT→LEARN→REUSE trio: `question.md` (REUSE: read expertise, validate vs code, answer with file/line cites), `plan.md` (ACT), `self-improve.md` (LEARN: diff expertise vs code, enforce `MAX_LINES 1000`, validate YAML). *This is where Dan first sees agents solving problems end to end without you.*

**Name it.** *The Class-1 ladder.* Sub-agent models are deliberately right-sized (scout-fast = Haiku, docs-scraper = Sonnet, heavy build/plan/review = Opus) — a live echo of AH-3's "match the model to the task."

**Failure modes (per rung).** Getting stuck at G3 with too many bad, token-heavy tools; skipping G4 feedback loops; confusing a plan and a template at G5; building an un-decomposable chain at G6; treating `expertise.yaml` as a source of truth at G7.

**Retrieval.** *List the seven Class-1 grades in order.* → prime+memory · sub-agents · custom tools · closed loops · templates · prompt chains · experts.

---

## Idea 4 — Class 2, getting out of the loop (the first big jump)

**Hook.** "That small chore, that small bug — you absolutely are wasting your time" sitting in the loop for it.

**Picture.** [Frames `t2258`, `t2464`] The agentic ring now wraps a "Class 1 Agentics" inner ring around **FE + BE apps**, with outer nodes = the out-loop machinery.
- **G1 (fabric only):** a webhook/HTTP endpoint (Slack/Jira/Discord/GitHub) fires a prompt through a **core Agent SDK** that fires custom agents (planner, builder). Nodes: `adw_webhook.py`, `adw_agent_core.py`, `prompt.py`. **No full ADW yet.**
- **G2 (the payoff):** full **AI Developer Workflows**. Nodes become `adw_plan_build.py`, `adw_chore_test_merge.py`, `adw_plan_w_scouts.py`…

**Worked example.** `adws/adw_workflows/adw_plan_build.py` sets `TOTAL_STEPS = 2`; `run_plan_step` invokes `/plan <prompt>` (via the Skill tool) and `run_build_step` invokes `/build <path>`. Deterministic Python owns step order, logging hooks, `StepStart/StepEnd`, DB writes, and WebSocket broadcasts; the Claude agent owns the reasoning. Triggering is out-loop: `adw_manual_trigger.py` (CLI) or the orchestrator's `start_adw` tool both write an `ai_developer_workflows` DB row, then `adw_scripts.py` spawns a **detached** `uv run adw_<type>.py --adw-id <uuid>` process.

**Name it.** *The AI Developer Workflow (ADW)* — "the highest leverage point of agentic coding," because you get **deterministic code + non-deterministic agents**: full control (logging, validation, retries) between every step, with frontier-agent capability inside each step. "Raw agents are unreliable. Raw code is inflexible. Combined, they're unstoppable."

**Failure mode.** Refusing to leave the terminal (never making the in-loop→out-loop jump), so the layer never scales; or just adopting a big-lab cloud tool and losing the control advantage of your own ADWs.

**Retrieval.** *Why is the ADW the highest leverage point, and how does an ADW differ from a prompt chain?* → Deterministic code + non-deterministic agents = best of both worlds; an ADW wraps agent steps in deterministic code so each transition is loggable/validatable/retryable (a prompt chain is agent-driven end to end).

---

## Idea 5 — Class 3, the orchestrator (the second big jump)

**Hook.** "This is the orchestrator agent, the one agent to rule them all."

**Picture.** [Frames `t2776`, `t3124`] The real orchestrator UI (`localhost:5175`). One system panel lists the whole agentic layer: six live agents (fix/review/build/plan), ~30 slash commands, 7 agent templates, 3 ADW workflows, and all **10 orchestrator tools**. The center panel toggles between the **LOGS** view and the **ADW's (swimlane)** view — the exact "two views" Dan names.
- **G1:** the orchestrator agent itself — a custom lead engineer that runs CRUD on other agents.
- **G2:** *orchestrator developer workflows* — it conducts multi-team workflows via `orch_scout_and_build.md`, `orch_plan_w_scouts_build_review.md`, spinning up teams and summarizing every event.
- **G3 (final):** the orchestrator **runs AI Developer Workflows** (raw code) so its biggest jobs are trackable and trustworthy.

**Worked example.** `orchestrator_service.py` runs a Claude Agent SDK client (default `claude-opus-4-5-20251101`) whose system prompt ("You are the conductor of this multi-agent orchestra") exposes 10 MCP tools from `create_management_tools()`: **8 agent-management** (`create_agent`, `list_agents`, `command_agent`, `check_agent_status`, `delete_agent`, `interrupt_agent`, `read_system_logs`, `report_cost`) **+ `start_adw` + `check_adw`**. Those last two are the exact bridge that lets **Class 3 run Class 2's ADWs** — the orchestrator LLM emits a `start_adw` tool call (there is no literal "start adw:" text parser), which spawns the background workflow.

**Name it.** *The orchestrator agent* — the top of the pipeline every engineer walks: base → better → more → custom → orchestrator.

**Failure mode.** Trying to start at Class 3 without the lower rungs ("we don't start at class three"), then drowning in an unmaintainable, non-deterministic mess with no observability.

**Retrieval.** *What exact tool does the orchestrator call to run an ADW, and what does it spawn?* → `start_adw`; it writes a DB record and spawns a detached `uv run adws/adw_workflows/adw_<type>.py --adw-id <uuid>` process.

---

## Idea 6 — Specialize, don't genericize (the most-repeated warning)

**Hook.** "Engineers go wrong here too. They think they need to build a generic one-size-fits-all agentic layer. That is not what we're doing here at all."

**Picture.** Five related apps under `apps/`, one specialized agentic layer wrapping them — templates, experts, and prompts all tuned to *this* product's exact problems.

**Name it.** *Specialize your agentic layer.* "Your codebase is literally a specialized solution to solve a problem… build to win for the use cases you care about." If agents don't need to see multiple codebases, it's fine to duplicate and specialize a separate layer per repo.

**Failure mode.** Chasing reuse/DRY and building a generic layer that wins nowhere.

**Retrieval.** *What is Dan's single most-repeated warning about building the layer?* → Specialize it to one codebase and use case; do not build for reuse.

---

## Idea 7 — Everything reduces to the core four

**Hook.** "It doesn't matter what it's called. It can be called a skill. It can be called a prompt chain, agentic workflow."

**Name it.** *The core four* (context, model, prompt, tools) — the invariant. A prompt, a sub-agent, a skill, an ADW, and an orchestrator all resolve to the same four primitives. "Everything eventually becomes a core four." The composite **form factor doesn't matter**; increasing your **compute advantage** does.

**Retrieval.** *An expert can be a set of prompts, a sub-agent, a skill, or a prime prompt — why doesn't the form matter?* → Because all of them reduce to context/model/prompt/tools; choose the form that maximizes compute advantage for your codebase.

---

## The closing recap (the whole course in one breath)

The lesson ends by boiling TAC + AH into the tactics that build the layer:

1. **Stop coding** — agents are the best tool; hand-typing caps your agentic layer.
2. **Adopt your agent's perspective** — could *you* solve it with exactly this context? (AH-1)
3. **Template your engineering** — encode how you build; models drift, templates don't.
4. **Stay out the loop** — scale chains, then leave the terminal (Class 2).
5. **Always add feedback loops** — request, validate, resolve; more compute = more trust.
6. **One agent, one prompt, one purpose** — a focused agent is a performant agent.
7. **Target zero-touch engineering** — the doorstep of the singularity.
8. **Prioritize agentics (meta-tactic)** — [Frame `t3518`] build the system that builds the system.

AH arc: context engineering (AH-1) → agentic prompt engineering (AH-2) → custom agents (AH-3) → multi-agent orchestration (AH-4) → agent experts (AH-5) → **agentic layers (AH-6, this)**.

Closing line: *"When the agents arrived, something changed. We weren't just AI Coding anymore. We started orchestrating intelligence."* Dan's stated next move: build a four-to-five-figure/month agent-run business on camera to prove what one engineer can do.

---

## VTT-verified timeline map (approx, ~10s accuracy)

| Time | Beat | Frame |
|---|---|---|
| 0:44 | "The agentic layer" named as the central framework | — |
| 4:24 | Codebase singularity defined ("run my codebase better than I can") | render as pull-quote |
| 6:12 | Green vs dark squares — agentic vs application layer; three classes | **t0382** |
| 8:00–9:36 | Class-3 destination demo: orchestrator kicks off ADWs; LOGS/ADWS views | **t0558** |
| 10:35 | Class 1 Grade 1 — thinnest layer (prime + memory) | — |
| 13:24 | Class 1 Grade 2 — sub-agents (fetch-docs, test-writer) | **t0812** |
| 14:48 | Class 1 Grade 3 — `.mcp.json` (postgres/firecrawl/jira/notion) + skills | **t0895** |
| 18:00 | Class 1 Grade 4 — closed-loop prompts, `app_review/` | **t1088** |
| 21:24 | Class 1 Grade 5 — bug/feature/chore templates | **t1288** |
| 24:24 | Winning multi-app structure: `apps/` + git submodules; specialize | — |
| 29:24 | Class 1 Grade 6 — `scout_then_plan` prompt chain | **t1768** |
| 33:12 | Class 1 Grade 7 — agent experts + `expertise.yaml` | **t2015** |
| 36:33 | Class 2 Grade 1 — out-loop system (PITER framework), webhook | **t2258** |
| 41:00 | Class 2 Grade 2 — AI Developer Workflows (highest leverage point) | **t2464** |
| 44:24 | Class 3 — orchestrator agent, "one to rule them all"; fixer/reviewer/builder + tools | **t2776** |
| 49:00 | Class 3 Grade 2 — orchestrator developer workflows | — |
| 51:48–52:12 | Class 3 Grade 3 — orchestrator runs ADWs; "final gift"; LOGS + ADW views | **t3124** |
| 55:00–58:36 | Tactic recap culminating in Tactic 08 "Prioritize Agentics" | **t3518** |
| 63:54 | "We started orchestrating intelligence"; Dan's next-year plan | — |

---

## Glossary / auto-transcript corrections

- **PITER framework** — the out-loop framework (TAC-4). Auto-transcribed "Peter framework."
- **core Agent SDK / Agent expert** — auto-transcribed "core Asian SDK / Asian expert."
- **agentic coding** — auto-transcribed "agenda coding."
- **grade** — occasionally auto-capitalized as "Great" ("the final Great" = the final grade).
- **AGENTS.md / agent declaration** — auto-transcribed "agent declare."
- **ADW** — AI Developer Workflow. **Core four** — context, model, prompt, tools.
- **Expertise file (`expertise.yaml`)** — an agent expert's *mental model / working memory*, validated against the code (which is the source of truth).

---

## Facts the chapter must not get wrong (verified this session)

1. **10 orchestrator tools, not 8** — `create_management_tools()` returns 8 agent-management tools **plus `start_adw` and `check_adw`** (a stale docstring says 8).
2. **7 database tables, not 6** — migration `9_ai_developer_workflows.sql` adds `ai_developer_workflows`; `models.py` has 7 Pydantic models.
3. **Backend port 9403** is canonical (config.py/README/start_be.sh/api.ts). The `8002` in the app CLAUDE.md and start-orchestrator skill is stale.
4. **Orchestrator default model = `claude-opus-4-5-20251101`** (the README env-var example showing sonnet-4-5 is illustrative). Model era dates the codebase to ~Nov 2025.
5. **No literal "start adw:" parser** — ADWs launch via the `start_adw` MCP tool call, not host string-matching.
6. **The per-grade "example project structures" are teaching diagrams** — the working repo consolidates some rungs (templates inside `plan.md`; out-loop via `start_adw`/`adw_manual_trigger.py` rather than a literal inbound webhook).
7. **Video is native 1920×1080** (recording.json's 2880×1620 is the capture surface); all 13 frames extracted with no upscaling.

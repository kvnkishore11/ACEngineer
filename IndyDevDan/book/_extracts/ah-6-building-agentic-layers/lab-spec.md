# AH-6 Lab — Build & Climb the Agentic Layer

**Codebase (only):** `agentic-horizon/orchestrator-agent-with-adws` (Dan's "final gift"). No PiCanvas, no external repos.
**Goal:** Prove you can (1) *locate* every class/grade in a real agentic layer, (2) *drive* an ADW from both the CLI (Class 2) and the orchestrator (Class 3), (3) *operate* an agent expert (Grade 7), and (4) *name your own* codebase's class/grade and next rung.
**Rule of the house:** type zero application code by hand — everything through agents/prompts (editing prompt/spec files via Claude Code is allowed).

Time: ~90–120 min. Cost: budget a few dollars of Anthropic tokens (real agents + real DB). Every part has **gradable checkpoints** and a **pass bar**.

---

## Part 0 — Setup (10 min)

1. Open the repo. `cp .env.sample .env` and set `ANTHROPIC_API_KEY` + `DATABASE_URL` (a free NeonDB Postgres works).
2. `uv run apps/orchestrator_db/run_migrations.py` — creates the schema.
3. Confirm tooling: `uv --version`, `bun --version`, `claude --version`.

**Checkpoint 0 (gradable).**
- [ ] Migrations succeeded and created **7** tables. Verify: `psql "$DATABASE_URL" -c "\dt"` shows `orchestrator_agents, agents, prompts, agent_logs, system_logs, orchestrator_chat, ai_developer_workflows`.
- [ ] You can state that migrations 5/6/7 are indexes/functions/triggers (not tables).

---

## Part 1 — Locate every rung (the layer audit) (20 min)

Without running agents, produce a one-page **layer map** of this repo. For each rung, cite one real file/dir.

| Rung | Find at least one real path | Your citation |
|---|---|---|
| C1 G1 prime + memory | `.claude/commands/prime.md`, `CLAUDE.md` | |
| C1 G2 sub-agents (+ specs/, ai_docs/) | `.claude/agents/*.md`, `specs/`, `ai_docs/` | |
| C1 G3 custom tools | `.claude/skills/*/SKILL.md`, `.mcp.json.sample` | |
| C1 G4 closed loops | `.claude/commands/review.md`, `fix.md`, `app_review/` | |
| C1 G5 templates | `.claude/commands/plan.md` (task_type switch) | |
| C1 G6 prompt chains | `.claude/commands/orch_scout_and_build.md`, `adws/adw_workflows/adw_plan_build.py` | |
| C1 G7 agent experts | `.claude/commands/experts/{adw,database,websocket}/` | |
| C2 G1 out-loop fabric | `adws/adw_triggers/adw_manual_trigger.py`, `adw_scripts.py`, `adws/adw_modules/adw_agent_sdk.py` | |
| C2 G2 full ADWs | `adws/adw_workflows/adw_plan_build{,_review,_review_fix}.py` | |
| C3 G1 orchestrator | `apps/orchestrator_3_stream/backend/modules/orchestrator_service.py`, `agent_manager.py` | |
| C3 G2 orch dev workflows | `apps/orchestrator_3_stream/.claude/commands/orch_*` | |
| C3 G3 orchestrator runs ADWs | `agent_manager.py` (`start_adw`/`check_adw`), `frontend/src/components/AdwSwimlanes.vue` | |

**Checkpoint 1 (gradable).**
- [ ] Every rung has a real, on-disk citation (verify each `ls`/open).
- [ ] You identified the **application layer** (`apps/*`: markdown_preview, nile, interactive_file_tree, pomodoro_timer, simple-html-file, + orchestrator apps) vs the **agentic layer** (root `.claude/` + `adws/`).
- [ ] You can name the sub-agent model choices (`scout-report-suggest-fast` = haiku, `docs-scraper` = sonnet, `build-agent`/`planner`/`review-agent` = opus) and explain why (match model to task).

**Pass bar:** a filled table with 11 verified citations + the app/agentic split named.

---

## Part 2 — Read the ADW (Class 2 comprehension) (10 min)

Open `adws/adw_workflows/adw_plan_build.py` (read it in chunks — it's ~976 lines).

**Checkpoint 2 (gradable).** Find and quote the line/identifier for each:
- [ ] `TOTAL_STEPS = 2`.
- [ ] `run_plan_step` invoking `/plan <prompt>` (via the Skill tool) and `run_build_step` invoking `/build <path>`.
- [ ] `create_logging_hooks` + `create_message_handlers` logging `TextBlock`/`ThinkingBlock`/`ToolUseBlock` and `StepStart`/`StepEnd`.
- [ ] In `adws/adw_triggers/adw_scripts.py`: the `subprocess.Popen([... "uv","run", ..., "--adw-id", adw_id ...], start_new_session=True)` spawn.

**Pass bar:** you can explain, in one sentence, why this is "deterministic code orchestrating non-deterministic agents."

---

## Part 3 — Run an ADW from the CLI (Class 2 in action) (15 min)

Trigger an ADW **without** the orchestrator, exactly as `adw_manual_trigger.py`'s docstring shows.

```bash
uv run adws/adw_triggers/adw_manual_trigger.py \
  "lab-feature" \
  "plan_build" \
  "Add a word-count badge to the markdown_preview app footer" \
  "$(pwd)"
```

**Checkpoint 3 (gradable).**
- [ ] A row appeared in `ai_developer_workflows` (verify: `psql "$DATABASE_URL" -c "select adw_name, workflow_type, status from ai_developer_workflows order by created_at desc limit 1;"`).
- [ ] A plan file was written under `specs/`.
- [ ] The `apps/markdown_preview` change was made by the agent (you typed no app code).
- [ ] Re-run with `"plan_build_review"` and confirm an `app_review/` report with a PASS/FAIL verdict is produced.

**Pass bar:** at least one ADW completed end to end from the CLI, with a `specs/` plan and (for the review variant) an `app_review/` artifact.

---

## Part 4 — Run an ADW from the orchestrator (Class 3 in action) (20 min)

1. Start the stack (uses the Grade-3 `start-orchestrator` skill pattern):
   ```bash
   cd apps/orchestrator_3_stream && ./start_be.sh &   # backend (port 9403)
   ./start_fe.sh &                                     # frontend (port 5175)
   open "http://127.0.0.1:5175"
   ```
2. In the orchestrator chat, ask it to start an ADW, e.g.:
   *"Start a plan_build_review ADW named 'lab-orch' to add a copy-to-clipboard button to the markdown preview app."*
3. Toggle the center panel between the **LOGS** view and the **ADWS** (swimlane) view.

**Checkpoint 4 (gradable).**
- [ ] The orchestrator invoked its `start_adw` tool (visible in the event stream / tool-use blocks) and returned an `adw_id` — confirm there was **no** literal "start adw:" string parsing; it's a tool call.
- [ ] You watched the ADW progress in the **ADWS swimlane** view and the **LOGS** view.
- [ ] Using the orchestrator, you asked it to `check_adw <adw_id>` and it reported step status.
- [ ] You can list the orchestrator's **10** tools from `agent_manager.py` (`create_agent, list_agents, command_agent, check_agent_status, delete_agent, interrupt_agent, read_system_logs, report_cost, start_adw, check_adw`).

**Pass bar:** an orchestrator-launched ADW ran to completion, observed in both UI views, and you named the exact class-3→class-2 bridge tool (`start_adw`).

---

## Part 5 — Operate an agent expert (Grade 7 + ACT/LEARN/REUSE) (15 min)

Use the ADW expert.

1. **REUSE:** `/experts:adw:question "How does start_adw spawn a workflow, and where is the swimlane UI rendered?"` — confirm the answer cites real files/lines.
2. **LEARN:** make a tiny change to an ADW file (e.g. add a comment in `adw_plan_build.py`), then run `/experts:adw:self-improve true` and watch it validate `expertise.yaml` against the code.

**Checkpoint 5 (gradable).**
- [ ] The question answer includes file+line citations (proof it validated against code, not memory).
- [ ] After self-improve, `.claude/commands/experts/adw/expertise.yaml` is still valid YAML and ≤ 1000 lines (verify: `python3 -c "import yaml; yaml.safe_load(open('.claude/commands/experts/adw/expertise.yaml'))"` and `wc -l`).
- [ ] You can explain why `expertise.yaml` is a **mental model**, not a source of truth (the code is).

**Pass bar:** you ran REUSE + LEARN and can articulate ACT→LEARN→REUSE.

---

## Part 6 — Grade yourself + your own codebase (10 min)

Write two short paragraphs:
1. **This repo:** its class/grade (it's a Class-3-Grade-3 exemplar) and *which rungs it consolidates* vs the idealized diagrams (e.g. templates inside `plan.md`; out-loop via `start_adw`/CLI trigger, not a literal webhook).
2. **Your real codebase:** its current class + grade, the single next element you'd add, and a one-paragraph justification.

**Checkpoint 6 (gradable).**
- [ ] You proved Grade-6's rule: you ran `/plan` and `/build` individually **and** as a chain, and can say how you'd isolate a failure to one step.
- [ ] Your own-codebase class/grade + next-rung plan is written down.

**Pass bar:** both paragraphs written; the individual-vs-chain runs demonstrated.

---

## Overall pass criteria (all must be true)

1. You cited a real file for **every** rung C1G2–G7, C2G1–G2, C3G1–G3 (Part 1).
2. An ADW ran end to end from **both** the CLI trigger **and** the orchestrator, producing a `specs/` plan and (for review/fix variants) an `app_review/`/`app_fix_reports/` artifact.
3. You can state the exact tool the orchestrator calls to run an ADW (`start_adw`) and what it spawns (a detached `uv run adw_<type>.py --adw-id` process).
4. You ran an agent-expert `question` + `self-improve` and can explain ACT/LEARN/REUSE and why `expertise.yaml` is not a source of truth.
5. You named your **own** codebase's class/grade and its next rung — without notes.
6. You typed **zero** application code by hand.

---

## Instructor / self-grader notes

- **Common failure:** trying to jump straight to Part 4 (orchestrator) without Part 1's audit — students then can't explain what the UI is showing. Enforce Part 1 first ("we don't start at class three").
- **Cost control:** use `plan_build` (2 steps) for first runs; only use `plan_build_review_fix` (4 steps) once the flow works.
- **Port gotcha:** if the frontend can't reach the backend, confirm the backend is on **9403** (canonical); ignore the stale `8002` in some docs.
- **DB hygiene:** these runs write real rows; clean up test ADWs afterward if reusing a shared DB (the repo's CLAUDE.md requires ephemeral, self-cleaning tests).
- **Stretch (optional, still course-codebase only):** using Claude Code, add a `plan_build_test` workflow by copying `adw_plan_build.py` and swapping the build step's follow-up for a `/test` command; prove the orchestrator can discover and run it (it maps to `adws/adw_workflows/adw_<type>.py`). Then run `/experts:adw:self-improve true` and confirm the expert notices the new workflow.

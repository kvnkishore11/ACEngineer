# AH-4 Lab Spec — Multi-Agent Orchestration: The O-Agent

**Scope rule:** every drill runs inside the course codebase only — `agentic-horizon/multi-agent-orchestration` (resolve the lesson symlink `.../ah-4-multi-agent-orchestration-the-o-agent/codebase`, or clone from the loot box: `git clone https://github.com/disler/multi-agent-orchestration.git`). No external repos. The app points at its own codebase (`--cwd apps/orchestrator_3_stream`), so you are literally using the system to build the system.
**Prime directive (graded throughout):** you command the fleet **through the Orchestrator** (Cmd+K) — you never hop into a side terminal to hand-run an agent, and you never hand-edit an agent to "fix" it. You're learning to conduct, not to babysit.
**Reading skill graded above all:** for every agent you touch — the orchestrator and each spawned agent — you must be able to point at its **core four** (context, model, prompt, tools) and name how each is set.
**Time box:** 120–180 minutes (advanced; real infra: Postgres + backend + frontend). **Token/cost note:** fan-out burns real tokens — the fast scouts are Haiku (cheap), but plan→build→review with Sonnet agents adds up. Budget for it, and **delete your agents** when done (it's also the lesson).

---

## 0 · Setup (25–35 min) — real infrastructure

1. Enter the codebase and read the top-level `README.md` (the 8 tools + the architecture diagram) and root `CLAUDE.md` (engineering rules: no-mock tests, UV only, keep `models.py` in sync).
2. **Toolbelt:** `uv --version`, `claude --version`, `node --version`, `bun --version`, and **`psql --version`** (needed for migrations).
3. **Database:** create a **Neon** serverless Postgres (recommended) *or* a local/Docker Postgres. Put its DSN in `DATABASE_URL`.
4. **Env:** `cp .env.sample .env`; set `ANTHROPIC_API_KEY` + `DATABASE_URL`. **Copy the root `.env` into both app dirs** (`apps/orchestrator_3_stream/.env` and `apps/orchestrator_db/.env`) — the backend loads the app-dir `.env`, *not* the repo root.
5. **Migrations:** `uv run apps/orchestrator_db/run_migrations.py` → confirm 6 tables (`orchestrator_agents`, `agents`, `prompts`, `agent_logs`, `system_logs`, `orchestrator_chat`).
6. **Backend:** `cd apps/orchestrator_3_stream && ./start_be.sh` → serves **http://127.0.0.1:9403** (ignore the inner `CLAUDE.md`'s stale "8002").
7. **Frontend:** `bun install` then `./start_fe.sh` → open **http://127.0.0.1:5175**. You should see the empty shell: `AGENTS 0 Total`, `Active/Running/Logs 0`, `Cost $0.00`, and *"Start a conversation."*
8. **SDK sanity:** open `backend/pyproject.toml` + any backend module — confirm `claude-agent-sdk` / `from claude_agent_sdk import … ClaudeAgentOptions, ClaudeSDKClient`. (Unlike AH-3, the names here are already current — Dan even says "Claude Agent SDK.")

**Checkpoint 0:** the app is live at :5175, connected (green dot), 6 tables exist, and you can state the backend port (**9403**) and the SDK name (**claude-agent-sdk**) without looking.

---

## 1 · Reading drill — the O-agent's core four + the 8 tools (20 min)

Open `backend/prompts/orchestrator_agent_system_prompt.md` and `backend/modules/agent_manager.py`. Write down:
- The **first line** of the system prompt (what IS the orchestrator?).
- The **8 management tools** and, for each, its params — then label each **C/R/U/D**.
- How the orchestrator's **core four** is set in `orchestrator_service.py`: model (`ORCHESTRATOR_MODEL`), system_prompt (overwritten), tools (`create_sdk_mcp_server('mgmt')` + `Bash, Read, SlashCommand, Skill`), context (200k window, R&D).

**Checkpoint 1:** your list has all 8 tools with correct CRUD labels (create_agent=C; list_agents/check_agent_status/read_system_logs/report_cost=R; command_agent=U/task; delete_agent+interrupt_agent=D), and you can say why the orchestrator's system prompt is a **full overwrite** (it's a custom meta-agent, not Claude Code).

---

## 2 · Run the fleet & feel the "3× compute" (20 min)

1. Cmd+K → ping the orchestrator (`ping`). Confirm a quick response and that **no agents** were created (it answered directly).
2. Cmd+K → *"Create three agents to summarize this codebase: one for the frontend, one for the backend, and a primary QA agent to summarize both into a full-stack architecture doc with a Mermaid diagram."*
3. Watch the EventStream: count the orchestrator's tool calls (**expect 6** — 3× `create_agent` + 3× `command_agent`). In the left rail, read each agent's **model badge** (2× Haiku fast + 1× Sonnet primary), cost, and context bar.

**Checkpoint 2:** you can point at the 6 tool calls and say, in one sentence, why this is *"three times the compute an engineer in a terminal has"* — and identify which agents are fast (Haiku) vs primary (Sonnet).

---

## 3 · Observability drill — the pillar in action (20 min) ⭐

This is the money drill.
1. Use the filter tabs: **RESPONSE / TOOL / THINKING / HOOK**. Then filter to a **single agent** via its chip. Then run a **regex** search over events.
2. When the QA agent finishes, open its **Consumed vs Produced** panel: click **Show Diff** on a produced `.md`, then **one-click into your editor** (that's `POST /api/open-file`). Read the produced architecture doc — trace the mermaid: browser → FastAPI → Orchestrator Service → Orchestrator Agent (Sonnet 4.5) → Management Tools MCP Server / Agent Manager (8 tools).
3. Read each agent card's **core four** (context bar `x/200k`, model, cost, tool/hook/response/thinking counts).

**Checkpoint 3 (write it down):** *observability is why you can (a) see every agent's core four at a glance, (b) diff and open produced files, and (c) debug "which agent did what."* State the couplet: **"if you can't measure it, you can't improve it — and you can't scale it."**

---

## 4 · CRUD drill — create, command, check, delete (15 min)

1. Ask the orchestrator to **list agents and check their status** — watch it run `list_agents` / `check_agent_status`. Note it does **not** dump every log (it protects its own context).
2. Re-command one existing agent with a follow-up (proves **update / re-prompt** with memory).
3. Cmd+K → **"delete all agents."** Watch N× `delete_agent` + *"✅ All agents deleted successfully."* Confirm `AGENTS 0 Total` and that the **produced docs still exist** in `app_docs/`.

**Checkpoint 4:** you can explain "treat your agents as deletable temporary resources that serve a single purpose" — the work (artifacts) persisted, the agents did not. You can also explain why the orchestrator *shouldn't* keep reading all logs (protect its context / R&D).

---

## 5 · Ecosystem + templates — primary vs sub-agent (25 min)

1. **Slash-command interop:** Cmd+K → *"Create an agent and command it to run `/question`: can the orchestrator and its agents use skills?"* Read the produced answer (**yes**). Then have an agent run **`/prime`** and note the context it loads.
2. **Template creation:** Cmd+K → *"Create an agent with the `scout-report-suggest-fast` template and command it to summarize which fields our regex search looks at."* Open `.claude/agents/scout-report-suggest-fast.md` and confirm its frontmatter (**model haiku; tools Read, Glob, Grep**). Note that `create_agent(subagent_template=…)` turned that sub-agent template into a **primary** agent (its own card, re-promptable).

**Checkpoint 5:** you can state, in your own words, why this is a **primary agent, not a sub-agent** ("pulled up a level" — own session, re-promptable, runs slash commands/skills), and confirm from `meta-prompt/SKILL.md` that commands are kept model-invocable ("DO NOT use `disable-model-invocation`") so agents can trigger them.

---

## 6 · The ADW workflow + the sleep-check glue (25 min)

Pick **one** orchestration workflow and run it end-to-end via Cmd+K.

**A. Scout + Build** (`/orch_scout_and_build`): a small UI tweak (e.g. "add simple flat gray info pills to the app header"). Watch the orchestrator create a **scout** (`scout-report-suggest-fast`) + a **builder** (`build-agent`), then **sleep + `check_agent_status`** while they work.

**B. Plan → Build → Review** (`/orch_plan_w_scouts_build_review`): a responsive-UI change (e.g. "collapse the agent list and shrink the orchestrator chat under 650px"). Watch all three agents get created up front — a **dynamic planner** (custom prompt, *no* template), a **`build-agent`** builder, a **`review-agent`** reviewer — and the three phases run with a **final report**; the reviewer verifies the vite build.

Then open the workflow command file (`apps/orchestrator_3_stream/.claude/commands/orch_plan_w_scouts_build_review.md`) and find `SLEEP_INTERVAL: 15 seconds` + the `Bash(sleep …)` + `check_agent_status` loop.

**Checkpoint 6:** you can (a) name the three phases and each agent's template (planner=none/dynamic, builder=`build-agent`, reviewer=`review-agent`), (b) show that the ~15s monitor is **prompt-driven** (not hidden Python), and (c) point at the completion signal (a `response` event_category followed by a `hook` `Stop`).

---

## 7 · Judgment drill — orchestrate, or not? (10 min)

Write two short lists from your own work:
1. Three jobs that are **orchestration-shaped** (multiple specialized agents, repeatable multi-phase workflow, worth out-loop review with observability).
2. Three jobs that should stay a **single agent / in-loop** (exploratory, one-off, generic, tight back-and-forth).
Then map ONE orchestration-shaped job onto **PITER**: what's the Prompt input, the Trigger, the Environment, and how would you Review it?

**Checkpoint 7:** your first orchestration pick genuinely needs a *fleet* (not one focused agent) — and you can articulate the out-loop review, not just "more agents."

---

## Stretch (optional, +30–60 min) — change the fleet *through* the system

Type zero application code by hand; make changes through the orchestrator/agents or through config.
1. **New template:** add a new `.claude/agents/<name>.md` template (frontmatter + body) and have the orchestrator `create_agent(subagent_template="<name>")`; prove it runs.
2. **New tool:** have Claude Code add a 9th management tool to `agent_manager.py` (e.g. `archive_agent`), register it in `create_sdk_mcp_server`, add it to `allowed_tools`, and prove the orchestrator can call it.
3. **New orchestration prompt:** write a new `.claude/commands/orch_*.md` workflow (use the `meta-prompt` skill) and run it.
4. **Fix a staleness bug:** update the orchestrator system prompt's stale `claude-3-5-haiku-20241022` doc line to match the code (`claude-haiku-4-5-20251001`), and/or the inner `CLAUDE.md` port (8002 → 9403). Verify the app still runs.

**Stretch checkpoint:** every change went through the agent/config surface, and you can point at the `ClaudeAgentOptions` (orchestrator or spawned agent) affected by your change.

---

## Pass criteria (all must hold)

- [ ] The app is live (backend :9403, frontend :5175), connected, with 6 Postgres tables.
- [ ] You can point at the orchestrator's `ClaudeAgentOptions` and name how each of the **core four** is set (incl. its 8-tool `mgmt` MCP server).
- [ ] You created ≥3 agents from ONE prompt and can explain the "3× compute" moment.
- [ ] You used the observability UI (filters + Consumed/Produced + Show Diff + one-click-open) and stated the "can't measure → can't scale" couplet (Checkpoint 3).
- [ ] You demonstrated all four CRUD verbs and deleted the fleet (Checkpoint 4), and can explain "deletable temporary resources."
- [ ] You created an agent from the `scout-report-suggest-fast` template and can explain **primary vs sub-agent** (Checkpoint 5).
- [ ] You ran an orchestration workflow (scout+build **or** plan→build→review) and showed the **sleep-check is prompt-driven** (Checkpoint 6).
- [ ] You produced your orchestrate-vs-single-agent lists and mapped one job onto **PITER** (Checkpoint 7).

---

## Instructor / self-grader notes

- **Highest-value single drill is #3 (observability).** If a student "gets" only one thing, it must be that observability is a *pillar* — measurement is what makes a fleet controllable and scalable, not a nicety.
- **Watch for the "just sub-agents" trap.** A student who can't articulate why a *primary* agent (persistent, re-promptable, runs its own commands/skills, keeps artifacts) beats a Task sub-agent hasn't got the differentiator (Checkpoint 5).
- **Grade the orchestrator's context.** A strong student notices the orchestrator's context bar stays tiny (~4–41k/200k) even after big runs, and can explain R&D (Reduce + Delegate) as the reason.
- **The sleep-check is a common misconception.** Many assume a hidden Python poll loop. Make them open the workflow command and find `Bash(sleep 15)` + `check_agent_status` (Checkpoint 6). It's prompt-driven glue.
- **Setup will bite.** If Postgres/`psql` or the app-dir `.env` copy is missed, nothing runs — don't fail a student for the infra gotchas; treat them as the intended "operating in the gray" lesson. Trust code/scripts over the stale doc comments (ports 9403/5175; ignore `hooks.py`).
- **Cost hygiene is part of the grade.** A student who leaves a fleet running (especially Sonnet plan→build→review) burns tokens; deleting agents when done is both cost control and the lesson ("let the agents go home").
- **Don't let a student treat this app as a required product.** The transferable payload is the pattern (single interface + CRUD + observability + out-loop) — they could rebuild a thinner version in any tool.

# AH-4 — Multi-Agent Orchestration: The O-Agent — Master Teaching Notes

**Lesson:** Agentic Horizon #4 (course order 12, Advanced) · **Runtime:** 56:08 · **Codebase:** `agentic-horizon/multi-agent-orchestration`
**Tactic:** *Orchestrate Your Agents* — put one custom Orchestrator Agent in front of your whole fleet, give it CRUD-for-agents + observability, and command agents at scale through a single interface.

> One-sentence spine: *You've scaled better → more → custom agents; the interface itself is now your bottleneck, so you build **one agent to rule them all** — the Orchestrator — and combine three pillars (Orchestrator + CRUD-for-agents + Observability) to command a fleet out of the loop.*

Every major idea below is built for a struggling learner: **Hook → Picture → Worked example → Name → Failure → Retrieval.**

---

## 0. The frame that anchors everything

The lesson is one continuous screen recording of a **custom dark-theme web app** (`MULTI-AGENT ORCHESTRATION`, `127.0.0.1:5175`) with three columns: **AgentList** (left, per-agent cards) · **EventStream** (center, filterable logs) · **OrchestratorChat** (right, the O-agent). A **Cmd+K palette** exposes the whole capability surface. Keep the [architecture frame `t0636`] and the [capability palette `t0300`] open while you read — between them they show *what the system is* and *what it can do*.

---

## 1. Multi-agent orchestration is the next rung — because the interface is the wall

- **Hook.** You got better agents, then more agents, then custom agents. So why do you still feel slow? Because *"you can't scale by hopping into one terminal at a time, writing one prompt at a time."*
- **Picture.** A ladder: **Base → Better → More → Custom → Orchestrated.** Each rung: *"scale your compute to scale your impact."* You're stuck one rung too low — running agents by hand.
- **Worked example.** In the generative-AI age, *"the rate at which you can create and command your agents becomes the constraint of your engineering output. When your agents are slow, you're slow. When your agents have a problem, you have a problem."* One human clicking between terminals cannot command a fleet.
- **Name it.** **The agent-scale framework**, and the new top rung: **Multi-Agent Orchestration.** It is *"an advanced agentic coding concept. It comes last after custom agents"* — you can only orchestrate what you can already build (custom) and measure (observability).
- **Failure to avoid.** Scaling agent *count* without an interface — opening 10 tabs. *"If you have 10 agents doing the wrong thing, does it matter that you have 10? Of course not."*
- **Retrieval.** *Recite the five rungs. Why does orchestration come last?* (Base→Better→More→Custom→Orchestrated; you can't orchestrate what you can't build or measure.)

---

## 2. The Orchestrator Agent (O-agent): the single interface pattern, applied to agents

- **Hook.** *Where is our input field?* This isn't an app for normal users; it's for the agentic engineer. You talk to exactly **one** agent — and it commands all the others.
- **Picture.** [Frame `t0258`]: the empty shell, three title cards fading in — **AGENT ORCHESTRATION / OBSERVABILITY / AGENTS AT SCALE** — and a right panel: *"Start a conversation — Ask the orchestrator to create, manage, or command agents."*
- **Worked example.** The orchestrator is a **custom agent**: its system prompt is *fully overwritten* — verbatim in `orchestrator_agent_system_prompt.md`: *"You are the **Orchestrator Agent** — a meta-agent that manages other Agents in a multi-agent system."* Its tools are **8 specialized management tools** (an in-memory MCP server), not the Claude Code engineering toolset. You say *"create three agents to summarize the codebase…"* → it emits **6 tool calls** (3× `create_agent` + 3× `command_agent`) and the fleet does the work.
- **Name it.** **The single interface pattern** — *"an existing engineering paradigm that great engineers have used for decades,"* now pointed at agents. The **O-agent** / **OA**.
- **Failure to avoid.** Letting the orchestrator do the engineering. It must not: *"we don't want our orchestrator agent getting involved in the actual work. It is just here to orchestrate."*
- **Retrieval.** *What kind of agent is the orchestrator, and what does it deliberately NOT do?* (A custom agent, system prompt overwritten, 8 tools; it orchestrates — it never does the heavy lifting, so its context stays tiny.)

---

## 3. The three pillars: Orchestrator + CRUD-for-agents + Observability

- **Hook.** *"But it's not just the Orchestrator Agent that matters. We're combining three pillars."*
- **Picture.** Three cards over the empty UI (`t0258`): **Orchestrator Agent** (unified interface) · **CRUD** for agents (agents at scale) · **Observability** (performance, cost, results).
- **Worked example.** Fire one prompt → three agents appear in the left rail, each with a live status, model, cost, and context bar; the center EventStream shows every response/tool/thinking/hook; the right panel shows the orchestrator's dispatch summary. That's all three pillars in one screen ([`t0402`]).
- **Name it.** **The three pillars of multi-agent orchestration.** *"When you combine these three, you get a powerful solution… This is you controlling your compute at scale."*
- **Failure to avoid.** Treating observability as a nice dashboard, or forgetting CRUD. Drop a pillar and you either fly blind or can't manage the fleet.
- **Retrieval.** *Name the three pillars and what each unlocks.* (Orchestrator = single interface; CRUD = agents at scale; Observability = control at scale.)

---

## 4. Observability is key — *measure it or you can't scale it*

- **Hook.** Why build a whole observability UI instead of just reading terminal output? *"Observability is a key component of a successful multi-agent system."*
- **Picture.** [`t0690`] the Consumed-vs-Produced ledger with inline **Show Diff** and an **Export File Activity** button; filter tabs **RESPONSE / TOOL / THINKING / HOOK**; per-agent chips; regex search; Auto-Follow.
- **Worked example.** *"If something went wrong, I could dial in right here and understand why, when, and where, and who. What agent messed up? Was it our planner? Was it our builder?"* You can one-click into any produced file and read the diff — in the loop only as long as you need.
- **Name it.** **Observability as a pillar** — *"If you can't measure it, you can't improve it. And if you can't measure it, you can't scale it."*
- **Failure to avoid.** Ten agents doing the wrong thing feels productive and isn't. Without measurement you can't tell.
- **Retrieval.** *Complete the couplet and give the pipeline.* ("can't measure → can't improve/scale"; SDK/hook event → Postgres (`agent_logs`) → WebSocket → Pinia store → UI, + a Haiku one-sentence summary.)

---

## 5. Primary agents, not sub-agents (the differentiator)

- **Hook.** Every engineer's first objection: *"Aren't these just sub-agents? Why aren't you just using sub-agents?"*
- **Picture.** An agent card that stays put with a template badge, a running cost, and a re-promptable session — versus a Task sub-agent that fires once and vanishes.
- **Worked example.** *"Instead of just using a sub-agent here, we can turn this into a full-on primary agent by blowing away the system prompt and by giving it custom tools… You can't do all this with a sub-agent. You're locked in, it's too narrow."* In code: `create_agent(subagent_template="scout-report-suggest-fast")` resolves the `.claude/agents/*.md` template into a **fresh `ClaudeSDKClient`** (its own session), and `command_agent` re-mounts it with `resume=session_id` so it remembers.
- **Name it.** **Primary agents** (re-promptable, persistent, produce results, can themselves run slash commands/skills/sub-agents) vs **sub-agents** (ephemeral, narrow, context blown away). Building one = **pull a sub-agent template up a level** (overwrite prompt + custom tools).
- **Failure to avoid.** Dismissing the whole system as "just sub-agents" and missing what persistence + re-prompting + concrete results buys you.
- **Retrieval.** *Give two concrete things a primary agent can do that a Task sub-agent can't.* (Be re-commanded with memory via `resume=`; run its own slash commands/skills/sub-agents; produce an inspectable artifact you keep.)

---

## 6. Manage the core four of every agent — and protect the orchestrator's context (R&D)

- **Hook.** All the UI, all the features — what are you actually looking at? *"It's all just the core four."*
- **Picture.** [`t0528`] the **CONTEXT / MODEL / PROMPT / TOOLS** Venn over the live per-agent cards (context bar `x/200k`, model badge, cost).
- **Worked example.** *"We're managing the core four of every single agent we spin up. If you do not adopt your agent's perspective… you do not know what you can do."* The orchestrator keeps *its own* context minimal by **Reducing** and **Delegating** (the R&D framework from AH-1): *"it is not always observing the logs. It cannot be. We have to protect its context window."* Even after conducting huge work, the orchestrator card shows ~4–41k/200k because context is reduced + delegated.
- **Name it.** **Core four at scale** + **R&D (Reduce & Delegate)**. The system prompt even sets `COMMAND_LEVEL_COMPACT_PERCENTAGE: 80%` — at ~80% it suggests `command_agent(agent, '/compact')`.
- **Failure to avoid.** Making the orchestrator read every agent log to "stay informed" — that blows up the one context window you most need thin.
- **Retrieval.** *Why does the orchestrator's context window stay small? Which two R&D verbs?* (It never does the work or reads all logs — it Reduces its own context and Delegates to focused agents.)

---

## 7. Stay out the loop — the PITER system (tactic 4)

- **Hook.** *"This is quite literally a prompt input…"* Why a database and WebSockets instead of a chat window?
- **Picture.** A 4-stage out-loop pipeline: **P**rompt input → **T**rigger (HTTP) → **E**nvironment → **R**eview (observability). (Render as a diagram; see frame-plan `unframed_beats`.)
- **Worked example.** Prompt = your Cmd+K message (`POST /send_chat`). Trigger = the HTTP request to the FastAPI server (fired as a background task). Environment = the working directory the agents operate in (here, the app's own codebase — *"we are using the system to build the system"*). Review = observability. *"We are observing work from our agents outside the loop… Remember tactic four, stay out the loop."*
- **Name it.** **PITER** (out-loop system). ⚠️ The auto-transcript renders it **"Peter"**; the loot-box notes spell it out; it is **not** a string in the repo — it's a lesson concept mapped onto real mechanics.
- **Failure to avoid.** Reading "out of the loop" as "unsupervised and hoping." The **R** is Review — you still inspect results; you just don't type back-and-forth prompts.
- **Retrieval.** *Expand PITER and name the tactic.* (Prompt input → Trigger (HTTP) → Environment → Review; tactic 4, stay out the loop.)

---

## 8. One agent, one prompt, one purpose — then delete (tactic 6)

- **Hook.** *"There's a journey every engineer goes through… you learn that the best code is no code at all. You learn to delete."*
- **Picture.** [`t1143`] three `delete_agent{agent_name}` calls, then **"✅ All agents deleted successfully!"** — the fleet cleared, ready for the next task.
- **Worked example.** Focus each agent on a single task with a protected window, let it produce its result, then delete it. *"You must treat your agents as deletable temporary resources that serve a single purpose."* A 200K window is plenty — *"you're just stuffing a single agent with too much work, just like your boss did to you at your last job."* Sidesteps context rot / pollution / toxic context.
- **Name it.** **One agent, one prompt, one purpose** (TAC lesson 6, *Let Your Agents Focus*).
- **Failure to avoid.** Hoarding stale, context-polluted agents. The *produced artifacts* persist; the agent is disposable — *"let the agents go home… delete it, back to the data center."*
- **Retrieval.** *State the three-word rule and the 200K claim.* (One agent, one prompt, one purpose; 200K is plenty — overloading one agent, not window size, is the problem.)

---

## 9. Every agent produces a concrete result — and you template YOUR engineering into it

- **Hook.** *"Every agent should produce some concrete result. Otherwise, what was the point in the first place?"*
- **Picture.** [`t2148`] a **✅ Scout Report Complete** with a produced `app_docs/header-pills-scout-report.md (+363)` and its consumed files — a durable artifact you can review after the agent is gone.
- **Worked example.** The scout agent reports in *your* dedicated structure because you **templated your engineering** into its system prompt. *"We've templated our engineering… a dedicated scout report, a dedicated structure."* That embedded specialization is your **defensibility**: *"If it's just one, two, three, four prompts away with zero effort… how defensible is your work really?"* Out-of-the-box tools are built for everyone's codebase, not yours.
- **Name it.** **Results-oriented engineering** + **templating your engineering** (the moat).
- **Failure to avoid.** Shipping the orchestrator app with none of *your* specialized prompts/tools/agents inside it — an undifferentiated tool with no edge.
- **Retrieval.** *Why must every agent produce an artifact, and where does defensibility come from?* (So work is inspectable/handed-off and outlives the agent; defensibility comes from the specialized engineering you template in, not the app shell.)

---

## 10. The orchestrator is glue — ecosystem interop + orchestration prompts (ADWs)

- **Hook.** *"It is interoperable with the entire Claude Code ecosystem."*
- **Picture.** [`t1445`] the orchestrator spins up a `codebase-questioner` (Haiku) and commands it to run **`/question`** → *"Yes, both your orchestrator and agents can use Skills."* A **`/prime`** is mid-type. Slash commands, skills, agent templates, hooks — all plug in.
- **Worked example.** Because you can specialize prompts for a custom agent, you get **orchestration prompts**: `/orch_plan_w_scouts_build_review` is a **plan → build → review → report** three-phase **ADW**. [`t2625`] all three agents up front — a *dynamic* planner (custom prompt, no template), a `build-agent` builder, a `review-agent` reviewer; the planner consumes real Vue files and produces `specs/responsive-ui-plan.md`. The orchestrator is the **glue**: *"I think this is vastly superior to agent hand-offs… more superior to blind sub-agents."* Its **sleep-check** monitoring — [`t3215`] `Bash{command:"sleep 20"}` + `check_agent_status` — is **prompt-driven** (the workflow file sets `SLEEP_INTERVAL: 15 seconds`), *not* hidden Python.
- **Name it.** **Ecosystem interoperability** + **orchestration prompts / ADWs** + **the orchestrator as glue** (the sleep-check loop).
- **Failure to avoid.** Assuming the ~15s monitor is machinery you can't change. It lives in the workflow command — read it, edit it.
- **Retrieval.** *What are the three phases of the demo workflow, and how does the ~15s loop work?* (Plan → Build → Review (+ report); the orchestrator runs Bash(sleep 15) + check_agent_status until a `response` is followed by a `hook` `Stop`.)

---

## 11. The agentic layer, prioritize agentics (tactic 8), and operating in the gray

- **Hook.** *"Make no mistake, the multi-agent orchestration, your O-agent, it is a part of your agentic layer."*
- **Picture.** The O-agent as both a piece of the agentic layer **and** *"the key to unlocking how to best organize, create, and use your agentic layer"* — usable **before** you have a full layer.
- **Worked example.** Prioritize agentics (TAC lesson 8): *"More than 50% of your time, as a rough guideline, should be spent investing into your agentic layer, into the system that builds the system."* But be honest — this costs upfront investment and ongoing maintenance (orchestrator, Postgres, WebSockets): *"another piece of your agentic layer you'll have to maintain."* And the big missing piece is deterministic **AI Developer Workflows**: *"How does this plug into deterministic code?… We're missing our AI developer workflows. This is the big missing piece."*
- **Name it.** **Prioritize agentics** + **operating in the gray**. *"Engineering happens in the gray. It happens in the messiness of it all."*
- **Failure to avoid.** Waiting for a "finished" out-loop utopia, or selling one. Dan explicitly refuses that: it works in **and** out of the loop, and you step between modes.
- **Retrieval.** *What's the >50% guideline, and the single biggest missing piece?* (Spend >50% of your time on the agentic layer; the missing piece is deterministic-code / ADW integration — a future lesson.)

---

## The fleet at a glance

**The 8 orchestrator (management) tools — the "CRUD":**

| Tool | CRUD | Signature (verified in `agent_manager.py` + palette frame `t0300`) |
|---|---|---|
| `create_agent` | **C** | `create_agent(name, system_prompt?, model?, subagent_template?)` |
| `list_agents` | R | `list_agents()` |
| `command_agent` | C-task / **U** | `command_agent(agent_name, command)` — also `/compact` at 80% |
| `check_agent_status` | R | `check_agent_status(agent_name, tail_count=10, offset=0, verbose_logs=false)` — the sleep-check poll |
| `delete_agent` | **D** | `delete_agent(agent_name)` |
| `interrupt_agent` | D/U | `interrupt_agent(agent_name)` |
| `read_system_logs` | R | `read_system_logs(offset=0, limit=50, message_contains?, level?)` |
| `report_cost` | R | `report_cost()` — orchestrator tokens/cost/context%/session id |

**The agent templates (`.claude/agents/*.md`):**

| Template | Model | Tools | Job |
|---|---|---|---|
| `scout-report-suggest-fast` | Haiku | Read, Glob, Grep | read-only "scout fast" → SCOUT REPORT (demoed by name) |
| `scout-report-suggest` | Sonnet | Read, Glob, Grep | deeper read-only scout |
| `build-agent` | Sonnet | Write, Read, Edit, Grep, Glob, Bash, TodoWrite | implement one file from a spec (the builder) |
| `review-agent` | Sonnet | Write, Read, Bash, Grep, Glob | diff-review → Blocker/High/Med/Low → PASS/FAIL |
| `meta-agent` | Opus | Write, WebFetch, firecrawl, MultiEdit | agent architect (generates sub-agents) |
| `docs-scraper` | Haiku | firecrawl, WebFetch, Write, Edit | scrape URL → `ai_docs/` markdown |
| `playwright-validator` | Sonnet | 19× `mcp__playwright__browser_*` + Write/Edit | drive browser, screenshot, validate |

*The **planner** has no static template — it's created dynamically (custom prompt, no template) by the plan→build→review workflow. Frame `t2625` shows the planner card with no template badge.*

**Models (from `config.py`):** Sonnet `claude-sonnet-4-5-20250929` (orchestrator + primary/build/review) · Haiku `claude-haiku-4-5-20251001` (scouts, docs-scraper, AI summaries) · Opus (meta-agent). On-screen badges: **SONNET-4.5 / HAIKU-4.5**.

---

## VTT-verified timeline map (mm:ss)

| Time | Beat | Frame |
|---|---|---|
| 0:07 | Welcome to Agentic Horizon, Lesson 4 | — |
| 2:15 | "when your agents are slow, you're slow" | — |
| 3:01 | "teach your agents to do for you" | — |
| 3:40 | **The Orchestrator Agent — one agent to rule them all** | — |
| 4:01 | **Three pillars** (orchestrator + CRUD + observability) | t0258 (4:18) |
| 4:56 | **Cmd+K** prompt input + capability metadata | **t0300 (5:00)** |
| 6:03–6:15 | multi-agent observability; **"can't measure → can't scale"** | **t0402 (6:42)** |
| 8:42 | **managing the core four of every agent** | **t0528 (8:48)** |
| 10:17 | **"using the system to build the system"**; architecture mermaid | **t0636 (10:36)** |
| 11:28–11:55 | **PITER out-loop system; tactic 4**; produced assets | t0690 (11:30) |
| 18:57 | **"deletable temporary resources"**; delete all agents | **t1143 (19:03)** |
| 19:19–19:46 | **one agent, one prompt, one purpose** (tactic 6) | — |
| 20:35 | "200K context window is plenty" | — |
| 21:28 | **"orchestrator is a custom agent… system prompt completely overwritten"** | — |
| 22:08 | **"Base, better, more, custom, orchestrator"** | — |
| 22:22–24:05 | **interoperable ecosystem**; `/question`, `/prime` | t1445 (24:05) |
| 27:05 | **scout-report-suggest-fast template** ("scout fast") | — |
| 28:37 | "every agent should produce a concrete result" | — |
| 32:12 | "how defensible is your work?" (templating/defensibility) | — |
| 35:48 | **sleep-check** loop; `check_agent_status` (scout + build) | **t2148 (35:48)** |
| 42:08–43:45 | **plan → build → review ADW**; planner ~21K tokens | **t2625 (43:45)** |
| 48:37–48:40 | **prioritize agentics; >50% of your time** (tactic 8) | — |
| 49:10–50:19 | missing pieces: human-in-loop, fork context, autocomplete | — |
| 53:35 | reviewer verifies vite build; `sleep 20` + check_agent_status | **t3215 (53:35)** |
| 54:39 | "first pattern… observability, customizability, agents at scale" | — |
| 55:35 | "remember where you saw this first" | — |
| 56:02 | codebase link in the loot box | — |

---

## Glossary

- **O-agent / OA / Orchestrator Agent** — the single custom agent that manages the fleet; system prompt overwritten; 8 management tools.
- **Single interface pattern** — one interface in front of many; here, one agent commanding a fleet.
- **Three pillars** — Orchestrator + CRUD-for-agents + Observability.
- **CRUD for agents** — create/command(+read status)/update/delete over agents.
- **Primary agent** — a persistent, re-promptable spawned `ClaudeSDKClient` (own session), vs an ephemeral Task **sub-agent**.
- **Agent template** — a `.claude/agents/*.md` sub-agent definition resolved into a primary agent via `create_agent(subagent_template=...)`.
- **PITER** — out-loop system: Prompt input → Trigger (HTTP) → Environment → Review (observability). *(Transcribed "Peter"; not in the repo.)*
- **Sleep-check loop** — prompt-driven `Bash(sleep 15)` + `check_agent_status` monitoring in the workflow commands.
- **ADW** — AI Developer Workflow (plan → build → review → report), here as an orchestration prompt.
- **R&D framework** — Reduce (context) & Delegate (work) — from AH-1.
- **Consumed vs Produced** — files an agent Read vs Wrote/Edited (via `file_tracker.py`), shown with inline diffs.
- **The agentic layer** — the system that builds the system; the O-agent is part of it and the key to organizing it.

## Transcript-artifact key (auto-generated VTT)

- "Peter" → **PITER**; "Cloud Code" / "clog code" → **Claude Code**; "O agent" / "OA" → **Orchestrator Agent**; "ultra thinking" → **ultrathink**; "agent decoding" → **agentic coding**; "Oracle Shure agent" → **orchestrator agent**; "Agenta Horizon" → **Agentic Horizon**; "PITER/Peter framework" is the out-loop review system (tactic 4).

## Cross-references

- **AH-1 (R&D framework / context window mastery):** the Reduce-and-Delegate engine that keeps the orchestrator thin.
- **AH-2 (agentic prompt formats):** the shape of the orchestration prompts and workflow commands.
- **AH-3 (building custom agents):** the O-agent IS a custom agent — same Claude Agent SDK, same "system prompt is the law," same core-four-in-code, same in-memory MCP custom tools, now used to build a fleet-manager. Orchestration is the rung after custom.
- **TAC 4 (AFK / stay out the loop):** PITER = the out-loop system.
- **TAC 6 (let your agents focus):** one agent, one prompt, one purpose.
- **TAC 8 (the agentic layer / prioritize agentics):** the O-agent is part of and the key to the agentic layer; >50% of your time.
- **Forward:** AH-5/AH-6 and future lessons wire this to deterministic AI Developer Workflows — the acknowledged missing piece.

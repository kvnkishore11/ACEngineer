# AH-4 Nuggets — ranked for the struggling learner

Ordering rule: how much of *multi-agent-orchestration competence* collapses if this nugget is missing. **Tier 1** is the paradigm you must not miss; **Tier 2** is the working machinery of the O-agent (the SDK, the tools, observability); **Tier 3** is judgment — how to run a fleet well and when it's worth building.

---

## Tier 1 — If you remember nothing else

**1. The interface is the wall; orchestration is the next rung.**
Better → more → custom agents got you here, but *"you can't scale by hopping into one terminal at a time, writing one prompt at a time."* The full ladder is **Base → Better → More → Custom → Orchestrated**, and *"the rate at which you can create and command your agents becomes the constraint of your engineering output."*
*Say it Dan's way:* "When your agents are slow, you're slow. When your agents have a problem, you have a problem."

**2. Multi-agent orchestration = three pillars, not one.**
**Orchestrator Agent** (single interface) + **CRUD-for-agents** (agents at scale) + **Observability** (performance, cost, results). *"When you combine these three, you get a powerful solution… This is you controlling your compute at scale."* Drop a pillar and you fly blind or can't manage the fleet.

**3. The Orchestrator is a custom agent — and it must NOT do the work.**
*"The orchestrator agent is a custom agent… Its system prompt is completely overwritten. Its tools are specialized. It's designed to manage other agents."* Its whole job is to orchestrate; *"we don't want our orchestrator agent getting involved in the actual work."* That's why its context window stays tiny.
*Why weak learners lose it:* they think orchestration means one big smart agent doing everything. It's the opposite — a thin conductor delegating to focused agents.

**4. Observability is a pillar, not a dashboard.**
*"If you can't measure it, you can't improve it. And if you can't measure it, you can't scale it. If you have 10 agents doing the wrong thing, does it matter that you have 10? Of course not."* You must see and filter every response/tool/thinking/hook, per agent, plus consumed-vs-produced files with diffs.

**5. Command PRIMARY agents, not blind sub-agents.**
Primary agents persist (own session, `resume=`), are re-promptable until done, produce inspectable results, and can run slash commands/skills/their own sub-agents. You build one by pulling a sub-agent template **up a level** — overwrite its system prompt + give it custom tools. *"You can't do all this with a sub-agent. You're locked in, it's too narrow."*

---

## Tier 2 — The working machinery (the O-agent)

**6. The 8 management tools ARE the CRUD.**
`create_agent(name, system_prompt?, model?, subagent_template?)` (C) · `list_agents()` / `check_agent_status(agent_name, tail_count, offset, verbose_logs)` / `read_system_logs(...)` / `report_cost()` (R) · `command_agent(agent_name, command)` (create-a-task/U) · `delete_agent` + `interrupt_agent` (D). They're an **in-memory MCP server** (`create_sdk_mcp_server('mgmt')`) — the same custom-tool pattern from AH-3, now for managing agents. The mermaid diagram labels them *"Agent Manager — 8 Management Tools."*

**7. Agent templates spawn primary agents.**
`.claude/agents/*.md` files (name/description/tools/model/color + body) are resolved by `create_agent(subagent_template=...)` into a fresh `ClaudeSDKClient`. Demoed: **scout-report-suggest-fast** (Haiku, read-only Read/Glob/Grep), **build-agent** (Sonnet, can write), **review-agent** (Sonnet, diff→PASS/FAIL). The **planner** has *no* template — it's created dynamically with a custom prompt.

**8. Same Claude Agent SDK, used twice.**
Universal loop — **options (core four) → mount `ClaudeSDKClient` → `query()` → manage the response stream** — runs for the orchestrator AND every spawned agent. This repo already uses the current names (`claude-agent-sdk` / `ClaudeAgentOptions` / `ClaudeSDKClient`), and Dan *says* "Claude Agent SDK" on camera. Blocks: `TextBlock`/`ThinkingBlock`/`ToolUseBlock`; `ResultMessage` carries session id + cost.

**9. Match the model to the job — at fleet scale.**
Orchestrator + primary/build/review = **Sonnet** (`claude-sonnet-4-5-20250929`); fast scouts + docs-scraper + AI summaries = **Haiku** (`claude-haiku-4-5-20251001`); the meta-agent template = **Opus**. On-screen: **SONNET-4.5 / HAIKU-4.5**. *(The system prompt's doc string still says the old `claude-3-5-haiku-20241022` — the code wins.)*

**10. Protect the context window — of every agent, especially the orchestrator (R&D).**
*"We're managing the core four of every single agent."* The orchestrator stays thin by **Reduce + Delegate**: *"it is not always observing the logs. It cannot be. We have to protect its context window."* At 80% it suggests `command_agent(agent, '/compact')`.

**11. The observability pipeline is real plumbing.**
SDK/hook event → Postgres (`agent_logs`/`system_logs`/`orchestrator_chat`) → WebSocket (~14 event types) → Pinia store → live UI, with a **Haiku one-sentence summary** per event and `file_tracker.py` splitting **Consumed (Read)** vs **Produced (Write/Edit/Bash)**. DB = **Neon/Postgres via asyncpg**. Backend **FastAPI :9403**, frontend **Vite :5175**.

**12. The sleep-check loop is PROMPT-driven, not hidden Python.**
The orchestrator monitors an agent by running `Bash(sleep 15)` + `check_agent_status` — because the workflow command says so (`SLEEP_INTERVAL: 15 seconds`). Completion = an `agent_logs` `response` event_category followed by a `hook` with a `Stop` event_type. *"The orchestrator is now a part of connecting the workflow. It's glue."*

---

## Tier 3 — Judgment (running a fleet well)

**13. One agent, one prompt, one purpose — then delete (tactic 6).**
Focus each agent on a single task with a protected window, then delete it. *"Treat your agents as deletable temporary resources… the best code is no code at all. You learn to delete."* A 200K window is plenty — overloading one agent, not window size, causes context rot. The produced artifacts persist; the agent is disposable.

**14. Every agent produces a concrete result — otherwise, what was the point?**
A plan, scout report, diff, or doc you can hand off, inspect, and keep after the agent is deleted. This is what makes out-loop review possible.

**15. Stay out the loop — PITER (tactic 4).**
**P**rompt input → **T**rigger (HTTP) → **E**nvironment → **R**eview (observability). You review results outside the loop and hop in only when you need to (one click into a file, then back out). *(Transcribed "Peter"; not a string in the repo.)*

**16. Template your engineering in — that's your moat.**
*"You need to be putting your engineering into your agents. This is what makes them special."* If your work is *"one, two, three, four prompts away with zero effort"* on an out-of-the-box tool, it isn't defensible. Specialization — your prompts, tools, agents, structures — is.

**17. Everything plugs in — reuse the whole ecosystem.**
Built on the Claude Agent SDK, the orchestrator and its agents can use slash commands (`/question`, `/prime`), skills, agent templates, and hooks — and the orchestrator can command an agent to run a slash command. *"Cloud code and the agent SDK and the ecosystem is far ahead of the pack."*

**18. Build it honestly — it's the gray, and it's worth it.**
Real upfront cost + maintenance (orchestrator, Postgres, WebSockets), and it's imperfect — the biggest missing piece is deterministic **ADW** integration (future). But *"you want to have some type of out-loop agentic coding system… I think the answer is a very clear yes."* It works in **and** out of the loop. Prioritize agentics (tactic 8): **>50%** of your time on the system that builds the system.

---

## Micro-quiz (self-check before the lab)

1. Name the five rungs of the scale framework and where the orchestrator sits. *(Base → Better → More → Custom → Orchestrated; last, after custom.)*
2. What are the three pillars? *(Orchestrator Agent, CRUD-for-agents, Observability.)*
3. Give two things a primary agent can do that a Task sub-agent can't. *(Be re-commanded with memory via `resume=`; run its own slash commands/skills/sub-agents; produce a kept artifact.)*
4. Name the 8 orchestrator tools and their CRUD roles. *(create_agent=C; list_agents/check_agent_status/read_system_logs/report_cost=R; command_agent=U/task; delete_agent+interrupt_agent=D.)*
5. How does the ~15-second monitor loop actually work? *(Prompt-driven: `Bash(sleep 15)` + `check_agent_status` in the workflow command, until a `response` → `hook`/`Stop`.)*
6. Why does the orchestrator's context stay tiny? *(It never does the work or reads all logs — Reduce + Delegate.)*
7. Expand PITER and name its tactic. *(Prompt input → Trigger (HTTP) → Environment → Review; tactic 4, stay out the loop.)*
8. Where does defensibility come from — the app or something else? *(Not the app shell; the specialized engineering you template into your agents/prompts/tools.)*

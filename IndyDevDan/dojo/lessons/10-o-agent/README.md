# 10 · The O-Agent

One interface, many agents — the orchestrator is "the one agent to rule them all... the single interface pattern applied to your fleet of agents."

## The Idea

Once you have better agents, more agents, and custom agents, you hit the wall of the interface: you can't scale one terminal and one prompt at a time. "The rate at which you can create and command your agents becomes the constraint of your engineering output. When your agents are slow, you're slow." The answer is the Orchestrator Agent — a custom agent whose only job is to manage other agents. "We don't want our orchestrator agent getting involved in the actual work. It is just here to orchestrate."

Multi-agent orchestration stands on three pillars: (1) the **Orchestrator Agent** — your unified interface; (2) **CRUD for your agents** — agents at scale; (3) **Observability** — real-time monitoring of status, costs, and results. "At scale, if you lose track of your agents, you lose control of your results." And: "If you can't measure it, you can't improve it. And if you can't measure it, you can't scale it."

The last pillar of the mindset is the delete: "You must treat your agents as deleteable temporary resources that serve a single purpose." An agent gets created with a purpose, commanded, observed — and then it goes. "Force it to focus and then let it go home back to the data center. Delete it." The best code is no code at all; you learn to delete.

One more discipline hides in the status function: the orchestrator reads the **tail** of each agent's trail, never the raw logs. Dan's orchestrator "used check-status tools (agent name + tail of response logs) rather than reading raw logs, protecting its own window." R&D applies to the orchestrator too — reduce and delegate.

## What Dan Did

In AH-4 (`multi-agent-orchestration`) Dan built an O-Agent — a custom agent with a completely overwritten system prompt whose tools are exactly create/command/status/delete over primary agents. From one Command-K prompt bar he fired a single prompt that spun up three agents (front-end, back-end, QA) — six tool calls: 3× create_agent, 3× command_agent. He walked an observability UI showing per-agent name, status, context window, model, and cost. "List agents and check status" hit status tools that return the log *tail*. "Delete all agents" closed the CRUD loop with three delete calls. "With a single prompt, I've deployed three times the compute an engineer working in the terminal has."

This lesson is the minimum viable version of that system: `worker.py` is your background agent, `oagent.py` is your orchestrator, `fleet/` is your registry, and `status.jsonl` is your observability trail.

## Your Mission

`worker.py` is complete — read it first (adopt your agent's perspective). Then fill the blanks in `oagent.py`, one per pillar:

1. **`create_agent(name, purpose)`** — two blanks: spawn `worker.py` via `subprocess.Popen` (streams detached to `DEVNULL`), then write the manifest `{"name", "purpose", "pid"}` to `fleet/<name>/manifest.json`. Every agent must have a purpose.
2. **`command_agent(name, text)`** — one blank: write the command to `fleet/<name>/inbox.txt`. That file is the whole command channel.
3. **`status(name?)`** — one blank: read the **last** event of `fleet/<name>/status.jsonl` and print a one-line summary per agent. Tail, not full log.
4. **`delete_agent(name)`** — two blanks: send `shutdown` through the inbox and poll `pid_alive` for ~2s, then remove the whole `fleet/<name>` directory. Agents are deletable resources.

The argv CLI dispatch at the bottom is already wired — don't touch it.

## The Loop

```bash
just check 10          # or: python3 ../../dojo.py check 10
```

The check runs the real sequence — create alpha → command alpha "do work" → status → delete alpha — against a live worker process, with timeouts everywhere. Pass looks like:

```
✅ PASS — 10 o-agent
```

Fail prints a numbered list telling you exactly which pillar leaks.

## Done-when

- `oagent.py create alpha <purpose>` spawns a live worker and writes `fleet/alpha/manifest.json` with `name`, `purpose`, and a real `pid`.
- `oagent.py command alpha "do work"` lands in the inbox and `status.jsonl` gains `working`/`finished` events.
- `oagent.py status` prints one summary line per agent, built from the last trail event.
- `oagent.py delete alpha` leaves no live process and no `fleet/alpha` directory.
- No `____` blanks remain.

## Level-up

Add `command all <text>` (broadcast to every agent in the fleet) and `oagent.py logs <name>` that prints only the last 3 trail events. Then add agent templates: let `create_agent` take an optional template file whose contents become the worker's first command — that's how Dan promoted `.claude/agents/` sub-agent definitions into full primary agents.

## Run It Live

Once the check passes, swap the worker for the real thing: in `create_agent`, replace the `worker.py` Popen with a background Claude instance —

```python
subprocess.Popen(["claude", "-p", purpose,
                  "--append-system-prompt",
                  f"write your report to fleet/{name}/result.txt"], ...)
```

— and you have Dan's `/background` pattern under your own CRUD interface. Compute orchestrating compute, agents orchestrating agents. Never required for passing.

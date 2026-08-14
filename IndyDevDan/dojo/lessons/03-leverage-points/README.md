# 03 · Leverage Points

Adopt your agent's perspective: your agent can only see what you let it see — open the two
highest-leverage channels, standard out and types, on a tiny app.

## The Idea

Tactic #2 comes with the 12 Leverage Points of Agentic Coding: the Core Four in-agent
(context, model, prompt, tools) and eight through-agent levers that flow through the context
window — standard out, types, documentation, tests, architecture, plans, templates, ADWs.
This lesson drills the first two, because they are the cheapest to open and the most ignored.

Standard out first. Dan: "Your agent can only see what you let it see." A CLI that mutates a
JSON file in silence is fine for a human who can open the file — it is invisible to an agent
watching stdout. That is bad agentic code: "Not only do we have bad code, we have bad
agentic code" — code that hides what happened, and hides errors, from agents. Every artifact
reports what it did. And once it does: "Stop looking at error messages… give them to your
agent. Only when your agent fails do you take your precious time and dig in."

Types second. "Types are IDKs" — Information Dense Keywords. "They point to exact locations
in your codebase and represent the flow of a specific type of information." An untyped
signature makes your agent guess; a typed one tells a story — "Types tell a story about how
information travels throughout your codebase." Every channel you open is context your agent
no longer burns tokens rediscovering. That is how the Attempts KPI falls toward one-shot and
your Streak grows: "Your agent will make mistakes, just like you. The only question is: does
it have the leverage it needs to correct them?"

## What Dan Did

In TAC-2 Dan dragged a CSV into the tac-2 natural-language→SQL app and hit an error the
server swallowed — endpoints returned raw responses with zero logging. His fix was a prompt,
not a patch: with `@app/server/server.py` referenced, "make sure every exception logs all
exception details, and every successful response before returning." Then he booted a fresh
agent, ran the start script inside it with a 300-second bash timeout so the agent could
watch stdout live, reproduced the bug, and asked "any issues with the server?" — the agent
diagnosed unescaped special characters from stdout alone and fixed it. For types, he copied
the `DatabaseSchemaResponse` model into a fresh instance and asked how it flows through the
application: the agent fired a search sub-agent and produced a top-to-bottom trace — 26K
tokens, 7 tool uses. Both demos are the same move: give the agent your perspective.

## Your Mission

`sample_app/tasks.py` is a working task-tracker CLI — add, list, done, JSON storage — that
runs in total silence and carries zero type hints on its core functions. Six sites are
marked with `____` inside comments:

- 3 stdout sites — print a confirmation after `add`, one line per task for `list`, a
  completion confirmation for `done`.
- 3 type sites — annotate every parameter and the return on `add_task`, `list_tasks`,
  and `complete_task`.

The starter runs as-is; keep it running. Open the channels without changing behavior.

## The Loop

```bash
just check 03          # or: python3 ../../dojo.py check 03
```

The check executes your CLI (add → list → done) in a temp copy and reads its stdout —
exactly the way an agent would — then AST-parses your signatures for the type hints.

## Done-when

- No `____` markers remain in `sample_app/tasks.py`.
- `add "…"` prints a confirmation naming the task.
- `list` prints each task with its id and text.
- `done 1` prints a completion confirmation with the id.
- `add_task`, `list_tasks`, and `complete_task` each have every parameter and the return
  annotated.

## Level-up

Fail loud: when `done <id>` matches nothing, print exactly which id was missing — silent
failure is the worst class of bug. Then type the rest of the file (`load_tasks`,
`save_tasks`, `main`) and paste one signature into a fresh `claude` session asking: "show me
how this type flows through the file — functions, purpose" — Dan's exact move.

## Run It Live

Boot `claude` in this lesson directory and prompt: "Run sample_app/tasks.py — add two
tasks, list them, complete one — then tell me, from stdout alone, what state the tracker is
in." A blind agent can answer only because you opened the channel.

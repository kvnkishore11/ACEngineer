# 11 · Agent Expert

"The difference between a generic agent and an agent expert is simple. One executes and forgets, the other executes and learns."

## The Idea

The massive problem with agents is that they forget — and that means they don't learn. "Traditional software improves as it's used... Agents of today don't. Your agents forget." An agent expert fixes this with three concrete steps — **Act, Learn, Reuse**: take a useful action, store what you learned, and apply that expertise on the next execution. Formally, "the agent expert is a concrete form of a self-improving template meta prompt."

The heart of the pattern is the expertise file — and what it is NOT. "This is not a source of truth... You have a working memory file. You have a mental model, a data structure that you constantly update." The true source of truth is always the code. That's why the question prompt must verify against the code before answering, and why the self-improve prompt diffs reality against belief and updates the yaml. "Real experts don't relearn their craft every time they have a new task" — the expert reads its key_files list and goes straight there: "It didn't need to go search or find these files. It knew where they were. This is the differentiated factor of an agent expert."

Two guardrails keep the mental model honest. First, changes are surgical: "I get super hyped when agents change just the right things... I wanna see surgical changes" — append and adjust, never wholesale rewrite. Second, hands off: "Don't directly update this expertise file. Teach your agents how to directly update it." If the expertise comes out wrong, you fix the self-improve prompt, not the yaml.

## What Dan Did

In AH-5 (`agent-experts`) Dan built a database expert at `.claude/commands/experts/database/`: an `expertise.yaml` (overview, core implementation with file paths and line numbers, query patterns), a `question.md`, and a `self-improve.md`. Running `/experts:database:question "how does information flow between our database tables"`, the agent read expertise.yaml FIRST, validated it against the code, and reported with file/line citations and a mermaid ER diagram. Running `/experts:database:self-improve`, the agent diffed its beliefs against the codebase, made surgical updates, then ran two closed loops on its own memory: a line-count check against MAX_LINES and a YAML validation. His websocket expert chained `plan → build → self-improve` and one-shotted a feature — the expertise diff afterward showed only accurate, surgical updates.

## Your Mission

`sample_app/` is the codebase this expert owns — `db.py` and `schema.sql` are complete; read `db.py` before filling anything (you need your own mental model first). Then fill:

1. **`experts/database/expertise.yaml`** — the mental model: the `purpose:` one-liner; 2 `key_files` entries (paths relative to the lesson root — they must exist); 2 `conventions` that are REALLY true in `db.py` (one must name the `_execute()` gateway); and the missing `never:` guardrail ("hand-edit this file — the agent maintains it").
2. **`experts/database/question.md`** — one blank: the verify step. Load expertise → answer from the mental model → **verify against the code** → cite file:line. The code is the source of truth; expertise is a lens.
3. **`experts/database/self-improve.md`** — two blanks: the learn step (diff findings vs the yaml, then UPDATE it — append/adjust, never wholesale rewrite) and the final step making self-improve mandatory after every task (no human in the loop).

## The Loop

```bash
just check 11          # or: python3 ../../dojo.py check 11
```

The check parses your yaml with stdlib line-parsing, verifies the key_files exist and the conventions match the real code, and checks both prompts' workflow language and ordering. Pass looks like:

```
✅ PASS — 11 agent-expert
```

## Done-when

- `expertise.yaml` has `purpose`, `key_files`, `conventions`, `never` — and the key_files paths exist on disk.
- At least one convention names the `_execute()` gateway (it's really in `db.py` — false expertise is worse than none).
- `question.md`'s workflow order is: load expertise → verify against the code → cite file:line.
- `self-improve.md` updates the yaml surgically (never wholesale rewrite) and makes learning mandatory after every task.
- No `____` blanks remain.

## Level-up

Add `plan.md` (reads expertise before planning) and a `plan_build_improve.md` chain — Step 1 plan, Step 2 build, Step 3 self-improve — "DO NOT STOP between steps." Then try seeding: empty out your expertise.yaml and rewrite self-improve.md so the agent can invent the structure from blank; "rerun it until your agent stops finding new things."

## Run It Live

Copy `experts/` into a real repo under `.claude/commands/` and run `/experts:database:question "how do inserts flow through this data layer?"` in Claude Code. Watch whether it reads expertise.yaml first and skips searching — that's the differentiated factor. Then change something in the data layer and run `/experts:database:self-improve`; inspect the diff with `git diff` — you want surgical changes. Never required for passing.

# 05 · The Higher Order Prompt

A Higher Order Prompt takes another prompt as its argument — `/implement <path-to-plan>` is the second half of the two-prompt engineering pipeline.

## The Idea

In TAC-3 Dan names the pattern: a **Higher Order Prompt (HOP)** is "a prompt that takes another prompt as an argument… plans getting passed into plans, like passing functions into functions." The meta prompt (`/chore`, lesson 04) writes the plan; the HOP (`/implement`) executes it. Two prompts, one shipped chore. "The plan is the prompt — and that means great planning is great prompting."

The HOP itself stays tiny — Dan's real `implement.md` is about 12 lines — because all the detail lives in the plan it receives. But those few lines carry the discipline: read the plan first and think hard; execute the tasks in order, one at a time; run every validation command the plan carries and fix failures before moving on; then report. The validation gate matters most: "It's not good enough to resolve once if that resolution causes something else to break — rerun every validation step top to bottom."

Why a separate prompt in a separate agent instead of continuing the planning session? Dan gives three reasons to always run fresh agents: free the context window — "one agent, one task, one mission"; force your prompts, plans, and templates to be "isolated, reusable, improvable assets with zero dependencies"; and "prepare for true off-device agentic coding" — decouple performance from the conversational context window. "When I boot up this agent, I know 100% what the agent's perspective is."

## What Dan Did

In TAC-3, after `/chore` generated the logging plan, Dan opened a **new terminal and a fresh Claude** and ran `/implement specs/<plan>.md`. He dissected `implement.md` on camera: "Read the plan, Think hard, implement, then report: summarize work + files changed." The agent executed every task, ran pytest for regressions, and reported. He then manually validated — restarted the server, confirmed the new logging format, regex-searched for zero remaining `print(` calls — and the whole chore had "been completed agentically with two prompts."

## Your Mission

Fill the four blanks in `commands/implement.md`:

1. **Workflow step 1** — read the plan at `$ARGUMENTS` top to bottom before touching anything; think hard.
2. **Workflow step 2** — execute the plan's tasks in order, one task at a time; finish each before starting the next.
3. **Workflow step 3** — the validation gate: run every validation command from the plan; if any fails, fix it and re-run them all until green.
4. **The Report section** — a markdown table mapping each Task to its Status, then the files changed.

`specs/sample-plan.md` is a real plan (three tasks, two validation commands) your finished HOP can be run against live.

## The Loop

```
just check 05        # or: python3 ../../dojo.py check 05
```

Fill, check, read the failure, fix, repeat. Pass looks like:

```
✅ PASS — 05 higher-order-prompt
```

## Done-when

- `commands/implement.md` has zero `____` blanks left.
- `$ARGUMENTS` is referenced as the path to a plan.
- The workflow reads the plan before executing, and executes tasks in order, one at a time.
- The validation gate runs every validation command and fixes failures before proceeding.
- The Report section specifies a markdown table with `| Task | Status |`.
- The steps land in a sane order: read before execute, validate before report.

## Level-up

Give the HOP a loop of its own: make step 3 re-run the *entire* validation list from the top after every fix, with a maximum retry count, and report each attempt in the table. Then write a second HOP — `/test_e2e <path-to-test-file>` — that executes markdown e2e test files the same way.

## Run It Live

Copy `commands/implement.md` into a scratch repo's `.claude/commands/`, copy `specs/sample-plan.md` into its `specs/`, boot `claude`, and run:

```
/implement specs/sample-plan.md
```

The agent should create `greet.py`, run both validation commands, and hand you the task table. Headless: `claude -p "/implement specs/sample-plan.md" --output-format stream-json --verbose`.

# 01 · The Agentic Prompt

An agentic prompt is a prompt that reliably executes a long chain of tool calls —
purpose, workflow, report. It is the fundamental unit of phase-two engineering.

## The Idea

AI coding ran on the Big Three: context, model, prompt. You asked, the model wrote a file,
you babysat. Agentic coding adds the fourth element — tools — and that upgrade changes the
unit of work entirely. Dan: "with the right context, model, prompt, and now tools, these
prompts are now more capable than ever before." The Core Four turn a prompt from a request
into a program.

A well-built agentic prompt has three pillars. **Purpose** states the one thing this prompt
exists to do — one agent, one prompt, one purpose. **Workflow** is the numbered chain of
tool-executing steps — the S-tier section, where the agent does engineering work instead of
just writing code. **Report** closes the loop back to you: an agent that doesn't report is
an agent you can't verify, and "it doesn't matter if our agent can solve every problem if we
don't know that it's solved."

And because Claude Code is a programmable agentic coding tool, the same prompt runs
headlessly from any script: `claude -p`. "It's not just about the agentic prompt. It's about
where we can use the agentic prompt." A prompt you can fire from code is a prompt you can
chain, schedule, and scale — that's how you push the Size KPI up (more work handed off per
prompt) while driving Attempts toward one-shot.

## What Dan Did

In TAC-1 Dan cloned `tac-1` and ran the AI coding prompt from the README — Claude created a
single `main` file with a print. "This is phase one." Then he ran the ~35-line agentic
coding prompt: Claude checked out a `demo-agentic-coding` branch, wrote `main_tac`, ran both
files, committed with a clear message, maintained a to-do list, and reported the work. "This
is engineering work, not just writing code." Then the kicker: the `programmable/` directory —
shell, Bun, and Python scripts each firing that same prompt through `claude -p`. He deleted
the demo branch and watched the Python runner recreate everything headlessly, full report at
the end, while he typed nothing. "To become an irreplaceable engineer, you will replace
yourself."

## Your Mission

- `prompt.md` — an agentic prompt that inventories this lesson directory. Fill:
  - the **Purpose** one-liner (the single mission of this prompt),
  - Workflow steps **2** and **3** (group files by extension and count; sort most-common first),
  - the **Report** output spec (a markdown table: extension, count, total row).
- `run.sh` — the programmable runner. Fill the `claude -p "$(cat prompt.md)"` invocation.

## The Loop

```bash
just check 01          # or: python3 ../../dojo.py check 01
```

Pass looks like `✅ PASS — 01 the-agentic-prompt`. Fail lists exactly what is missing —
read it, fix it, run again. That closed loop is the lesson.

## Done-when

- No `____` blanks remain in `prompt.md` or `run.sh`.
- `prompt.md` has `## Purpose`, `## Workflow`, and `## Report` sections.
- The Purpose section states the mission in real words.
- The Workflow has at least 4 numbered steps.
- The Report section explicitly specifies a markdown table as the output format.
- `run.sh` is valid bash and invokes `claude -p` fed with `prompt.md` on a live
  (non-comment) line.

## Level-up

Add a fifth Workflow step that flags the largest file in the directory, and re-run the
check. Then swap `--output-format text` for `--output-format stream-json --verbose` in
`run.sh` and watch the tool calls stream by — that JSONL stream is the raw material of ADWs.

## Run It Live

```bash
./run.sh
```

With the `claude` CLI installed, the agent inventories this directory and prints the
markdown table. Without it, the script says so and exits cleanly — the offline check never
needs it.

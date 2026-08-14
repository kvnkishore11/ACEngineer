# THE BUILD LOOP
### What IndyDevDan actually does when building a feature — reconstructed from code, commits, and uncut video

> Companion to `THE-SYSTEM.md`. That file is **doctrine** — the principles and the vocabulary.
> This file is **procedure** — what to type, in what order, and what to do when it breaks.
> Where the two disagree, this file wins: it is sourced from artifacts, not from talks.

**Provenance.** Eight parallel mining agents over: 29 cloned `disler/*` repos with full git history, the 8 TAC + 6 AH + 4 MA course codebases, 255 `.claude/commands/*.md` files, 52 committed specs, 18 lesson transcripts, and 53 public videos. Every claim below carries a count or a path.

---

## PART 0 — Four corrections before you start

Most write-ups of this method are wrong on these points. All four are load-bearing.

**0.1 — Git shows you his publishes, not his builds.**
46 of 78 commits in the traced repos are literally the word `progress`. 25 of 95 are the single character `🚀`. Nine of ten repos open with one commit dumping a finished project. Zero merges, zero branches, zero PRs, zero tags across all of them. **Do not try to learn the loop from his commit history** — it records distribution. Exactly one repo leaked a live session (`infinite-agentic-loop`, 2025-06-06, 94 minutes), and the uncut videos are the real evidence.

**0.2 — There is no `/feature` and no `/bug` command.**
Searched all 255 command files: they do not exist. TAC-3 teaches three templates (chore 53 lines, bug 69, feature 91) but every production repo converged on **one parameterized `/plan`** whose first instruction is:

```
- Determine the task type (chore|feature|refactor|fix|enhancement) and complexity (simple|medium|complex)
```

Task type then gates sections conditionally. Build one `/plan`, not three files that drift.

**0.3 — `prime.md` is the first file, not `CLAUDE.md`.**
`prime.md`: 24 of 30 repos. `CLAUDE.md`: 10 of 30, median 9.5 lines, two of them empty. In the one repo where git caught the real sequence, `CLAUDE.md` arrives at **commit 15 of 18, four days in**, and it is a *retrospective summary* of a system that already worked.

**0.4 — He calls his own framework arbitrary.**
> *"I'm saying that this arrangement of ADWs is completely arbitrary. There is no one way to do this. The one way is the way that ships in your code base."* — TAC-7

Take the loop. Leave the ceremony until it earns its place.

---

## PART 1 — Day one: install the layer

Ordered by **how often each file actually appears in his repos**, which is the only honest evidence of what comes first.

### 1.1 `.claude/commands/prime.md` — 24/30 repos

The irreducible version, verbatim from `disler__nano-agent`:

```md
# Prime
Execute the `Run`, `Read` and `Report` sections to understand the codebase then summarize your understanding.

## Run
git ls-files

## Read
README.md

## Report
Summarize your understanding of the codebase.
```

**Write it backwards.** In the traced repo it was born as one line (`RUN: git ls-files`) and only gained `READ: README.md` three days later — *after* the README existed. Point it at artifacts once they are real, never before.

Add a `## Focus` block and tiered read-lists (`### Core (always)`, `### Backend (if working on backend)`) only when the repo is big enough to need them.

### 1.2 `ai_docs/` — 13/30 repos

Vendor docs pulled local so agents never web-request a lookup. `ai_docs/README.md` is a manifest of `- filename.md: URL`. In the one live-traced session this landed **in the very first commit, alongside the first slash command, before any application code**.

### 1.3 `specs/` — 15/30 repos

Empty directory. Every generated plan lands here. Specs **fork rather than get edited**: `invent_new_ui.md` → `_v2` → `_v3` → `_v4`.

### 1.4 `.claude/commands/plan.md` — the planner

Verbatim from `orchestrator-agent-with-adws` (byte-identical in `agent-experts`):

```md
---
description: Creates a concise engineering implementation plan based on user requirements and saves it to specs directory
argument-hint: [user prompt]
---

# Quick Plan

Create a detailed implementation plan based on the user's requirements provided through the `USER_PROMPT` variable. Analyze the request, think through the implementation approach, and save a comprehensive specification document to `PLAN_OUTPUT_DIRECTORY/<name-of-plan>.md` that can be used as a blueprint for actual development work. Follow the `Instructions` and work through the `Workflow` to create the plan.

## Variables

USER_PROMPT: $1
PLAN_OUTPUT_DIRECTORY: `specs/`

## Instructions

- IMPORTANT: If no `USER_PROMPT` is provided, stop and ask the user to provide it.
- Carefully analyze the user's requirements provided in the USER_PROMPT variable
- Determine the task type (chore|feature|refactor|fix|enhancement) and complexity (simple|medium|complex)
- Think deeply (ultrathink) about the best approach to implement the requested functionality or solve the problem
- Explore the codebase to understand existing patterns and architecture
- Follow the Plan Format below to create a comprehensive implementation plan
- Generate a descriptive, kebab-case filename based on the main topic of the plan
- Save the complete implementation plan to `PLAN_OUTPUT_DIRECTORY/<descriptive-name>.md`
- Ensure the plan is detailed enough that another developer could follow it to implement the solution
- Consider edge cases, error handling, and scalability concerns

## Workflow

1. Analyze Requirements - THINK HARD and parse the USER_PROMPT to understand the core problem and desired outcome
2. Explore Codebase - Understand existing patterns, architecture, and relevant files
3. Design Solution - Develop technical approach including architecture decisions and implementation strategy
4. Document Plan - Structure a comprehensive markdown document with problem statement, implementation steps, and testing approach
5. Generate Filename - Create a descriptive kebab-case filename based on the plan's main topic
6. Save & Report - Follow the `Report` section to write the plan and provide a summary of key components

## Plan Format

<the fenced Plan Format block — see 1.4b>

## Report

After creating and saving the implementation plan, provide a concise report:

✅ Implementation Plan Created
File: PLAN_OUTPUT_DIRECTORY/<filename>.md
Topic: <brief description>
Key Components:
- <main component 1>
```

### 1.4b The Plan Format — the six sections that matter

The full skeleton is 11 sections, and they are **atomic**: all 14 specs that use any of them use all of them. But a natural experiment in the corpus (the same plan prompt run through Claude, Gemini, and Codex) shows weaker models shed sections in a fixed order. **Six survive every model — these are the irreducible core:**

```md
# Plan: <task name>

## Task Description
<describe the task in detail based on the prompt>

## Objective
<clearly state what will be accomplished when this plan is complete>

## Relevant Files
<list files relevant to the task with bullet points explaining why.
 Include new files under an h3 'New Files' section if needed>

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.
<h3 headers with bullet points. Start with foundational changes then move to
 specific changes. Last step should validate the work>

## Acceptance Criteria
<specific, measurable criteria that must be met>

## Validation Commands
Execute these commands to validate the task is complete:
<list specific commands. Be precise about what to run>
```

Conditionally add, per the template's own gates:
- `## Problem Statement` + `## Solution Approach` — *if task_type is feature OR complexity is medium/complex*
- `## Implementation Phases` (Foundation / Core Implementation / Integration & Polish) — *if complexity is medium/complex*
- `## Testing Strategy` — *if task_type is feature OR complexity is medium/complex*
- `## Notes` — optional, always last

**Two non-negotiables**, in his own words from the dojo template:

> *"Explore before you plan… **Never write a plan against code you have not read.**"*
> *"Every plan must end with Validation commands… **A plan without validation is an open loop.**"*

And the validation format is never bare commands — it's `` `<command>` — <what passing looks like> ``:

```md
- `just test` — all tests pass
- `cd apps/backend && uv run pytest -v` — backend tests (existing + new) all pass
- `live-bench list` — shows qwen35-vs-gemma4 with 8 charts
```

### 1.5 `.claude/commands/build.md` — the HOP, 11/30 repos

Verbatim. This is the whole file:

```md
---
description: Build the codebase based on the plan
argument-hint: [path-to-plan]
---

# Build

Follow the `Workflow` to implement the `PATH_TO_PLAN` then `Report` the completed work.

## Instructions

- IMPORTANT: Implement the plan top to bottom, in order. Do not skip any steps. Do not stop in between steps. Complete every step in the plan before stopping.
  - Make your best guess judgement based on the plan, everything will be detailed there.
  - If you have not run any validation commands throughout your implementation, DO NOT STOP until you have validated the work.
  - Your implementation should end with executing the validation commands to validate the work, if there are issues, fix them before stopping.

## Variables

PATH_TO_PLAN: $ARGUMENTS

## Workflow

- If no `PATH_TO_PLAN` is provided, STOP immediately and ask the user to provide it.
- Read the plan at `PATH_TO_PLAN`. Ultrathink about the plan and IMPLEMENT it into the codebase.
  - Implement the entire plan top to bottom before stopping.

## Report

- Summarize the work you've just done in a concise bullet point list.
- Report the files and total lines changed with `git diff --stat`
```

That is the entire build layer. **No priming needed** — everything the builder requires is inside the plan.

### 1.6 `CLAUDE.md` — optional, and later than you think

Write it **only when you have a rule an agent keeps breaking**. Every section is a rule, never a description; architecture and file tours belong in `/prime`. His canonical 43-line file is nine rules, e.g.:

```md
## IMPORTANT: Actually read the file
- IMPORTANT: When asked to read a file, read all of it - don't just read the first N lines.
- Read the file in chunks. If that's too large, cut in half and try again.

## Git Commits
- IMPORTANT: Do NOT commit any changes to the git repository unless you are explicitly asked to do so.
```

The test: *am I 100% sure I want this loaded 100% of the time?* If no, it goes in a prime command.

### 1.7 What to skip on day one

`.claude/settings.json` (arrives 8th in the traced repo), hooks, subagents, ADWs, worktrees, observability. `adws/` appears in **2 of 30 repos**. That is the top of the ladder, not the base.

---

## PART 2 — The feature loop

This is the per-unit-of-work procedure. Run it identically for a chore, a bug, or a feature.

### Step 0 — Push the laptop away

> *"Before I even start touching the computer... I think and I plan."*
> *"we never start by just blasting out prompts."*

Open `raw.md` by hand. Write three things: **purpose, problem, solution.** Then write the **literal output file tree** — what will exist when this is done that doesn't exist now.

> *"Beginning with the end in mind for engineering work, that often means defining the concrete output structures... At the end, what will you have that you didn't have before? What is your deliverable?"*

This step has no agent in it. Skipping it is the single most common failure.

### Step 1 — Fresh agent, `/prime`

New terminal. New instance. Run `/prime`. Check `/context` — you want ~90% free.

### Step 2 — Fire `/plan` with a *high-level* prompt

```
/plan "replace all server print statements with proper python logging, log levels, make sure all output is written to standard out"
```

Deliberately void of detail:

> *"We're writing a high level prompt, which is a prompt that's void of detail."*
> *"You want these to mostly be high level prompts because we've templated our engineering already inside of our planning prompts."*

Output: `specs/<kebab-name>.md`.

### Step 3 — Read the plan. Delete things.

This is **touchpoint one of two**.

> *"When you're engineering, when you're writing plans, you always go overboard. By the end of your planning phase, you should be deleting information that isn't relevant... You should go overboard, then delete."*

Check the Validation Commands section exists and is real. If it isn't, the loop is open and the rest will not work.

### Step 4 — Commit the spec

Before any code exists to blur it.

### Step 5 — **NEW terminal. NEW agent.** `/build specs/<name>.md`

Never continue the planner. This is the rule that survives every contradiction in the corpus.

> *"I keep opening new terminals and starting fresh agent instances that have no memory of what just happened. Why am I doing that? Don't we want to keep rolling the important context between planning, building, and really the entire software development lifecycle? **No.**"*

The three reasons, verbatim:

1. *"We free up our context. Focus every available token on the task at hand"*
2. *"we force our prompts, plans, and templates to be isolated, reusable, and improvable assets with zero dependencies"* — *"We have a trail of success or a trail of things we can improve."*
3. *"when we use fresh agents… we prepare for true off device agentic coding."*

And the payoff: **"It's easy to know what your agent has seen when it's seen nothing."** You cannot root-cause a failure in a polluted window.

### Step 6 — Watch it close its own loop

The agent runs every Validation Command, fixes failures, and **reruns all validations from the top**. Not just the one that failed.

> *"Run in order top to bottom. If you want to take any issues, stop and resolve them immediately. Then rerun every validation step... It's not good enough to resolve this once and that resolution causes something to break. You need them all to run from start to finish."*

The closed-loop prompt anatomy is three parts: **Request → Validate → Resolve.**

### Step 7 — Review the diff

**Touchpoint two.** `git diff --stat`, then spot-check by hand — refresh the browser, run one query.

> *"Many engineers get super hyped when an agent changes a million things. I get super hyped when agents change just the right things... I wanna see surgical changes like this. Five lines, 17 lines, nine lines, four lines."*

Note the distinction that matters: **testing ≠ reviewing.**
> *"Remember what the review step answers. It's not, does it work? It's is what we built, what we asked for."*

### Step 8 — Commit

---

## PART 3 — When it fails

### 3.1 Blame order — strict, and in this order

> *"Don't assume that it's the model's fault. First assume it's your fault, and then if you really prompt engineer properly, then you can assume it's the tooling's fault."*

1. Your wording
2. Your tooling
3. The model

### 3.2 Never fix the output by hand

> *"you don't fix the issue. you fix the system that caused the issue. You fix your templates, you fix your ADW."*
> *"Why didn't you just do that by hand? You're missing the point."*

### 3.3 Attempts > 1 means a missing leverage point

Target is one shot. At 3–6 attempts on the same task, stop prompting and install what's missing:

| Symptom | Missing leverage point |
|---|---|
| Agent confused by data shapes | **Types** (over dicts) |
| Agent can't navigate the codebase | **Architecture** (verbose names, 1-file-1-responsibility) |
| *You* are reading the error messages | **Standard Out** (make the code talk to the agent) |
| "Success" but the behavior is wrong | **Tests** |
| You're firing short iterative prompts | **Plans** |
| You've done this three times | **Templates** |

> *"Are you still manually looking at error messages? Stop. Stop... Give them to your agent. And only when your agent fails do you take your precious time and dig into the error."*

### 3.4 Live recovery moves, in his actual order

1. Kill a wrong-direction run — *"So I'm going to stop it. Ignore the skill. Just run this directly."*
2. Re-prompt more explicitly — add `IMPORTANT:` — *"I'm going to go ahead and use the important information dense keyword so that the agent really respects this"*
3. Escape / rewind history / Ctrl-Z
4. Full `/clear` and restart — *"Never be afraid to just start fresh."*

**Never `/compact`.** If the window fills mid-task, the task was too big — chop it.

---

## PART 4 — Escalate only when earned

### 4.1 The rule of three

> *"Three time makes a pattern. Three time should trigger your engineering brain. Automate."*

And when you do, **start ugly**:

> *"copy this and literally tell your agent create dot claude slash command slash start and then as a string, just give it exactly what you want in there. Then you can reformat it later. **Start with the bare minimum.**"*

Do it by hand once in a throwaway agent first, watch what actually works, *then* encode it.

### 4.2 Subagents — the gate

> *"Only use sub agents when you need specialization **and** parallelization. If you don't need to parallelize and you don't need to specialize, just create a reusable prompt... You want to do the least amount to get the greatest value."*
> *"If you're losing track of a single agent... you probably aren't yet ready for sub-agents."*

### 4.3 The prompt skeleton — his, written down, not inferred

Every reusable prompt uses this, and it lives inside `meta_prompt.md` as a literal `Specified Format` block:

```
---
allowed-tools: <comma separated>
description: <how we id this prompt>
argument-hint: [<first dynamic var>], [<second>]
model: <or default to 'opus'>
---

# Purpose
## Variables      ← dynamic ($1, $2) FIRST, then static
## Instructions   ← guardrails; "aid the workflow but are not part of the workflow itself"
## Workflow       ← numbered procedure
## Report         ← a fenced output template, not prose
```

60 of 255 files match exactly; 35 more match minus the optional `Purpose`. The order `Variables → Workflow → Report` holds at **100%**.

Rules he states explicitly: *"Prefer the `$1`, `$2`, ... over the `$ARGUMENTS` notation."* · *"if no variables are requested or mentioned, do not create a Variables section."* · *"Do not create any additional sections or headers that are not in the `Specified Format`."*

### 4.4 The self-improvement loop — Agent Experts

Build one only when *"you keep trying to deploy an agent and they keep getting it wrong"* in a specific domain. Not for static problems.

Four files per domain under `.claude/commands/experts/<domain>/`:

| File | Role |
|---|---|
| `expertise.yaml` | The mental model. Cap it (`MAX_LINES: 1000`). |
| `question.md` | Read-only Q&A. Validates the yaml against the code before answering. |
| `plan.md` | HOP — loads expertise, then delegates to `/plan`. |
| `self-improve.md` | Diffs the yaml against reality and repairs it. |

The loop:
```
expertise.yaml ──read──▶ /plan ──▶ /build ──▶ code changes
      ▲                                            │
      └────── /self-improve true ◀───git diff──────┘
              · validate yaml against code
              · surgical add / adjust / remove
              · wc -l > MAX_LINES ? trim, repeat
              · python3 -c "yaml.safe_load(...)"
```

Four invariants keep it from degenerating:

1. **Code is truth, the yaml is a lens.** *"validate the information from `EXPERTISE_PATH` against the codebase before answering."*
2. **Bounded memory.** Repeat-until-under-cap, or you rebuild the CLAUDE.md problem.
3. **Surgical edits only.** *"Don't include 'summaries' of work done in your expertise."*
4. **Permission to no-op.** *"there may be nothing to be done - this is perfectly acceptable. If there's nothing to be done, report that and stop."*

And the governing rule:

> **"Don't directly update this expertise file. Teach your agents how to directly update it."**

If the expertise comes out wrong, you fix `self-improve.md` — never the yaml.

### 4.5 Multi-agent — the later design wins

His systems split into two eras that disagree:

| | Mar–Apr 2026 | **Aug 2026** |
|---|---|---|
| Who routes | an LLM calls `delegate()` | **a Python script owns sequencing** |
| Agents message each other | yes | **never** |
| Principle | — | **"Agent proposes, code disposes"** |

The later factory also **deleted its tester agent**, on this rule:

> *"A known command is code, not an agent — if you can write the invocation down (`bun test`, `ruff check`), it belongs in a code phase."*

Five invariants worth carrying regardless of which shape you pick:

1. **Tier = tool list.** Leads get `delegate`, no `bash`. Workers get `bash`, no `delegate`. Topology enforced by capability, not by asking nicely.
2. **`tools:` is a capability list; a separate mechanism is the boundary.** `bash` runs `git checkout` and `write` reaches any path — you need a `writes:` allowlist enforced in code.
3. **The agent's final message is a claim; a gate is the proof.** Failures return to the *same session* as a correction, never a cold restart.
4. **An agent must not be able to edit the machinery that grades it.**
5. **One shared append-only log, written by code.** Agents read a record; they never message each other.

---

## PART 5 — The honest version

When the camera doesn't cut, the procedure is smaller and scrappier than the framework:

> Paper first → write the literal output file tree → agent scaffolds **empty files only** → do the risky thing once **by hand** in a throwaway agent → encode the smallest working version → test in a fresh instance → commit the moment it works → new instance for the next problem → build `/prime` only when a new agent needs onboarding → on failure blame your wording, then your tooling, then the model → escape / rewind / Ctrl-Z → add `IMPORTANT` → re-run → at "good enough," ship and say the debt out loud.

Things he admits on camera, which you should hear before building the full stack:

- *"I could have done all this with a single agent, but this is just good practice"*
- *"This probably isn't the scale."* — about his own multi-agent system
- *"I'll be honest, I haven't seen anyone doing zero-touch work yet."*
- *"many of the ideas I share with you here are experiments. Many of the ideas are trial and error."*
- In MA-3 the demo **failed live**; four agents bombed and the lead agents broke the system's own "leads never write files" rule to recover: *"this is not how the system is supposed to work, by the way."*

His defense of the machinery, which is fair: *"Think about the thousandth run, not the first, not the tenth."*

Build for the thousandth run only once you've done the first ten by hand.

---

## APPENDIX — Day-one checklist

```
[ ] .claude/commands/prime.md        # 8 lines. Run / Read / Report.
[ ] ai_docs/                         # + README.md manifest of "- file.md: URL"
[ ] specs/                           # empty
[ ] .claude/commands/plan.md         # one parameterized planner
[ ] .claude/commands/build.md        # the HOP, ~25 lines
[ ] raw.md                           # hand-written, per feature

Then run the loop. Add nothing else until something breaks three times.

Later, in this order, each only when earned:
[ ] .claude/settings.json            # hooks first; deny-lists are theater
[ ] .claude/commands/meta_prompt.md  # once you have 3+ commands to maintain
[ ] .claude/hooks/pre_tool_use.py    # real guardrails: sys.exit(2) blocks
[ ] .claude/commands/review.md       # "is what we built what we asked for"
[ ] experts/<domain>/                # only where agents keep getting it wrong
[ ] adws/                            # 2 of 30 repos. The top of the ladder.
```

---

*Compiled by Fable (Claude Opus 5) from 8 parallel mining agents over the IndyDevDan corpus, 2026-08-12. Every quote verbatim; every count reproducible from the paths cited in `THE-SYSTEM.md`'s provenance note.*

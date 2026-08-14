# 04 · The Plan Is the Prompt

Encode how you solve an entire class of problems into a template meta prompt — a prompt that writes plans — and let your agent do the planning for you.

## The Idea

"The plan is the prompt." Dan means that literally: "Plans are prompts scaled up for high impact… great planning is great prompting." A one-line request is a low-level prompt. A plan — a chore spec, a bug spec, a PRD — is the same prompt with the detail dialed all the way up, and detail is what one-shots work.

But planning by hand is slow, and "planning alone is expensive… there's always something to miss." So Dan goes one level higher: the **meta prompt** — "a prompt that builds a prompt." `/chore` is the canonical one. You hand it a chore description; it explores your codebase, thinks hard, and writes a complete plan into `specs/` — "staging environments for code that will be generated." You encode your problem solving once, into a template, and "you, your team, and your agents can see, use, and importantly, improve" it.

The template is where your standards live. Every plan it emits names the relevant files (so the implementing agent doesn't re-explore blind), breaks the work into step-by-step tasks, and — non-negotiable — ends with validation commands. That last section is what makes the plan a closed loop instead of a wish. This is Tactic #3, Template Your Engineering, and together with Stop Coding and Adopt Your Agent's Perspective it is "the Pareto 80/20 of agentic engineering."

## What Dan Did

In TAC-3, on the natural-language-to-SQL app, Dan booted a fresh Claude and ran `/chore "replace all server print statements proper python logging log levels make sure all output is written to standard out"`. The meta prompt researched the codebase in thinking mode and generated a plan in `specs/` with sections for the chore description, relevant files, step-by-step tasks, and validation commands.

Then he opened `.claude/commands/chore.md` and dissected the template: Purpose → Instructions → Relevant Files → Plan Format → `Chore: $ARGUMENTS`. A fresh agent ran `/implement` on the generated plan, and the whole chore shipped "agentically with two prompts — one for the planning phase and one for the coding/building phase."

## Your Mission

Fill the four blanks in `commands/chore.md`, the meta prompt:

1. **The explore instruction** — the read-before-write rule. The agent must explore and read the relevant files *before* it writes a word of the plan.
2. **The Plan Format section list** — the embedded template every plan follows: `Chore description`, `Relevant files`, `Step-by-step tasks`, `Validation commands`, as headings.
3. **The validation rule** — every plan must end with validation commands. No validation, no plan.
4. **The output path convention** — plans land at `specs/chore-<slug>.md`.

Study `specs/example-chore-rename-config.md` first — it is a real plan in the exact shape your template must produce.

## The Loop

```
just check 04        # or: python3 ../../dojo.py check 04
```

Fill a blank, run the check, read the failure, fix, repeat. Pass looks like:

```
✅ PASS — 04 plan-is-the-prompt
```

## Done-when

- `commands/chore.md` has zero `____` blanks left.
- The template takes the chore via `$ARGUMENTS`.
- The Plan Format contains all four sections as headings: Chore description, Relevant files, Step-by-step tasks, Validation commands.
- The template tells the agent to explore/read relevant files before writing the plan.
- The output path convention `specs/chore-<slug>.md` is spelled out.
- `specs/example-chore-rename-config.md` still carries the same four sections.

## Level-up

Build `/bug` — the next template up the ladder. Same skeleton, but the Plan Format grows `Steps to Reproduce` and `Root Cause Analysis` sections. Then specialize: "the more custom your templates are, the more unique your engineering gets."

## Run It Live

Copy `commands/chore.md` into any repo's `.claude/commands/`, boot `claude`, and run:

```
/chore "rename the config module and update every import"
```

Watch it write `specs/chore-<slug>.md`. Or stay out the loop entirely:

```
claude -p '/chore "your chore here"' --output-format stream-json --verbose
```

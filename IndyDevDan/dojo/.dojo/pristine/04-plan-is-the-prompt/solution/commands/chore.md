# Chore

Create a step-by-step plan in `specs/` that resolves the chore described below. This is a meta prompt — you are writing the prompt (the plan) that a fresh agent will execute. Plan, do not build.

## Purpose

Turn a one-line chore description into a complete, self-validating plan file. The plan is the prompt: everything the implementing agent needs must be inside the file you write.

## Instructions

- Explore before you plan: run `git ls-files`, then read every relevant file the chore touches. Never write a plan against code you have not read.
- Think hard about the smallest sequence of steps that completes the chore end to end.
- Fill in every section of the Plan Format below. No placeholders, no TODOs.
- Every plan must end with Validation commands — concrete commands the implementing agent runs to prove the chore is done. A plan without validation is an open loop.
- Write the finished plan to `specs/chore-<slug>.md`, where `<slug>` is a short kebab-case name for the chore (e.g. `specs/chore-rename-config.md`).
- Report the path of the plan file you wrote.

## Plan Format

```md
# Chore: <name>

## Chore description
<one paragraph: what changes and why>

## Relevant files
<every file the implementing agent must read or touch, with a one-line reason each>

## Step-by-step tasks
<numbered tasks, smallest first — each one independently completable>

## Validation commands
<commands that prove the chore is done — every plan ends with these>
```

## Chore

$ARGUMENTS

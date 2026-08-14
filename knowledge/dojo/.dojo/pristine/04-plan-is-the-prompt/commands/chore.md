# Chore

Create a step-by-step plan in `specs/` that resolves the chore described below. This is a meta prompt — you are writing the prompt (the plan) that a fresh agent will execute. Plan, do not build.

## Purpose

Turn a one-line chore description into a complete, self-validating plan file. The plan is the prompt: everything the implementing agent needs must be inside the file you write.

## Instructions

<!-- YOUR TURN: the read-before-write rule. Instruct the agent to explore the
     codebase and read every relevant file BEFORE writing the plan — e.g. start
     from `git ls-files`, read each file the chore touches. Never plan against
     code you have not read. -->
- ____
- Think hard about the smallest sequence of steps that completes the chore end to end.
- Fill in every section of the Plan Format below. No placeholders, no TODOs.
<!-- YOUR TURN: the non-negotiable — every plan must END with validation
     commands the implementing agent can run to prove the chore is done.
     A plan without validation is an open loop. -->
- ____
<!-- YOUR TURN: the output path convention — plans are written to the specs/
     directory as chore-, then a short kebab-case slug, then .md
     (like the example plan sitting in specs/ right now). -->
- Write the finished plan to `____`
- Report the path of the plan file you wrote.

## Plan Format

```md
# Chore: <name>

<!-- YOUR TURN: the embedded template — exactly four sections, each a `## ` heading:
     Chore description, Relevant files, Step-by-step tasks, Validation commands.
     Under each heading, leave a one-line note describing what belongs there.
     Match specs/example-chore-rename-config.md. -->
____
```

## Chore

$ARGUMENTS

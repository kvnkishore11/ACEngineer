# Hints — 04 plan-is-the-prompt

## Hint 1

The template you are filling in produces plans, it never touches code. So every blank answers one question: what does a *planning* agent need to be told? Open `specs/example-chore-rename-config.md` — it is the exact output shape your Plan Format blank must describe. The four headings in that file are the four headings you need.

## Hint 2

Blank by blank:
- The first Instructions blank is Dan's read-before-write rule — tell the agent to explore (e.g. `git ls-files`) and read every relevant file *before* writing the plan.
- The second is the closed-loop rule — every plan must *end with* validation commands that prove the chore is done.
- The path blank follows the convention `specs/chore-` + short kebab-case slug + `.md`.
- The Plan Format blank lists four `## ` headings: Chore description, Relevant files, Step-by-step tasks, Validation commands.

## Hint 3

Near-answers you can adapt:

```
- Explore before you plan: run `git ls-files`, then read every relevant file the chore touches. Never write a plan against code you have not read.
- Every plan must end with Validation commands — concrete commands the implementing agent runs to prove the chore is done.
- Write the finished plan to `specs/chore-<slug>.md`
```

And inside the Plan Format fence:

```md
## Chore description
## Relevant files
## Step-by-step tasks
## Validation commands
```

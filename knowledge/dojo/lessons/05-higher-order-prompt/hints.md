# Hints — 05 higher-order-prompt

## Hint 1

Dan's real `implement.md` is about 12 lines: "Read the plan, Think hard, implement, then report." Each blank is one of those moves. The order is the message: you cannot execute what you have not read, and you cannot report what you have not validated. `$ARGUMENTS` is the plan's path — that is the whole trick that makes this a *higher order* prompt.

## Hint 2

Blank by blank:
- Step 1 must mention reading the plan at `$ARGUMENTS` before doing anything, plus "think hard" (Anthropic's encoded IDK for more reasoning compute).
- Step 2 is execution discipline: tasks run *in order, one task at a time*.
- Step 3 is the validation gate: run *every validation command* from the plan; on failure, *fix and re-run until all pass* — never proceed past a red command.
- The Report blank specifies a markdown table with a `| Task | Status |` header row, then the files changed.

## Hint 3

Near-answers you can adapt:

```
1. Read the plan file at `$ARGUMENTS` top to bottom before touching anything. Think hard.
2. Execute the plan's Step-by-step tasks in order, one task at a time. Complete each task fully before starting the next.
3. Run every validation command listed in the plan. If any command fails, fix the failure and re-run every validation command from the top until all pass.
```

And for the Report section:

```
| Task | Status |
|------|--------|
| <task from the plan> | ✅ done / ❌ blocked (why) |

Then list every file you changed.
```

# Implement

Execute the plan at the path passed in below. This is a Higher Order Prompt (HOP): it takes another prompt — the plan — as its argument. One agent, one prompt, one purpose: build exactly what the plan says.

## Purpose

Turn a plan file from `specs/` into working, validated code. The plan carries the detail; your job is to execute it faithfully and prove it worked.

## Workflow

1. Read the plan file at `$ARGUMENTS` top to bottom before touching anything. Think hard.
2. Execute the plan's Step-by-step tasks in order, one task at a time. Complete each task fully before starting the next.
3. Run every validation command listed in the plan. If any command fails, fix the failure and re-run every validation command from the top until all pass. Do not report on unvalidated work.

## Report

When every task is complete and every validation command is green, report your work as a markdown table:

| Task | Status |
|------|--------|
| <task from the plan> | ✅ done / ❌ blocked (why) |

Then list every file you changed.

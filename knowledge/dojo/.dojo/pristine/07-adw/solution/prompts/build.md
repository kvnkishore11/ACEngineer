# Build

## Purpose

Implement a plan. This is a higher order prompt — the plan path is the argument,
a prompt passed into a prompt.

## Variables

PATH_TO_PLAN: $ARGUMENTS

## Workflow

1. IMPORTANT: If no PATH_TO_PLAN is provided, stop immediately and ask for it.
2. Read the plan at PATH_TO_PLAN. Think hard.
3. Implement every step in order.
4. Run the plan's Validation Commands before you finish.

## Report

Summarize the work done and list every file changed.

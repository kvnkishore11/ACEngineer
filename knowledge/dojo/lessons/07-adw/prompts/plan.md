# Plan

## Purpose

Turn a one-line task into a step-by-step plan the build agent can execute
without asking a single question. The plan is the prompt.

## Variables

TASK: $ARGUMENTS

## Workflow

1. Run `git ls-files` and read the README to ground the plan in this codebase.
2. Think hard. Write a step-by-step plan for TASK into `specs/adw_plan.md` with
   sections: Task, Relevant Files, Step-by-Step Tasks, Validation Commands.
3. Keep every step small enough for a single agent to one-shot.

## Report

Summarize the plan in one line, then print the plan location on its own line,
exactly in this format:

PLAN_PATH: <path to the plan you wrote>

# Resolve

## Purpose

The validation gate failed. Diagnose the failing tests and fix the build with
minimal targeted changes — you fix the system, not the symptom.

## Workflow

1. Run `python3 -m unittest discover tests` and read the failure output.
2. Find the root cause. The tests are the rule of law in this codebase —
   never edit a test to make it pass.
3. Apply the smallest fix that addresses the root cause.
4. Re-run the tests to confirm the fix.

## Report

State what failed, the root cause, and exactly what you changed.

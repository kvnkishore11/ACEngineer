# Database Expert — Self-Improve

The LEARN step of Act–Learn–Reuse: after work happens on the data layer,
bring the mental model back in sync with reality. No human in the loop —
you don't tell an expert to learn, it's in their DNA.

## Variables

EXPERTISE_FILE: experts/database/expertise.yaml
MAX_LINES: 100

## Instructions

- Think of EXPERTISE_FILE as your mental model, not a source of truth.
- Prioritize actionable, high value expertise over verbose documentation.
- After a thorough search there may be nothing to do — this is perfectly acceptable.

## Workflow

1. Read EXPERTISE_FILE — know what you currently believe.
2. Read sample_app/ — what is actually true in the code right now.
3. Diff what you found in the code against EXPERTISE_FILE and update the
   yaml: append new entries, adjust stale ones, remove what the code
   contradicts. Surgical changes only — never wholesale rewrite the file.
4. Enforce MAX_LINES and confirm the file still parses as valid yaml —
   closed loops on your own memory.
5. Run this prompt after EVERY task that touches the data layer — it is
   mandatory, with no human in the loop. Agents forget; experts learn
   by default.

## Report

- List each expertise entry you added or adjusted (or "nothing to do").
- Confirm the line count is within MAX_LINES and the yaml is valid.

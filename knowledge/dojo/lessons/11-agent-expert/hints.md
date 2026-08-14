# Hints — 11 agent-expert

## Hint 1

Everything you need for `expertise.yaml` is inside `sample_app/db.py` — including its module docstring, which literally lists the house conventions. Read the code, then write down only what is true: which two files matter, and which two rules the code actually enforces. For the prompts, ask yourself where each of Act–Learn–Reuse lives: question.md is Reuse, self-improve.md is Learn.

## Hint 2

- `key_files`: the two files in `sample_app/` — paths relative to the lesson root, so `sample_app/...`. The check verifies they exist.
- `conventions`: one entry must mention `_execute` (the single gateway every query flows through); the second is the parameterized-`?`-placeholders rule.
- `never`: the exact guardrail is in the YOUR TURN comment: hand-edit this file — the agent maintains it.
- `question.md` step 3: a sentence that verifies/validates the draft **against the code** — the checker wants a verify-verb near "code", positioned after the expertise read and before the citation step.
- `self-improve.md` step 3 needs "update the yaml... append/adjust... never wholesale rewrite"; step 5 needs "after every task... no human in the loop".

## Hint 3

Near-answer — fill the yaml like this:

```yaml
purpose: answer, plan, and ship work on the sample_app data layer from a maintained mental model

key_files:
  - path: sample_app/db.py
    role: the data layer — connect, insert_task, list_tasks
  - path: sample_app/schema.sql
    role: the schema — table definitions applied by connect()

conventions:
  - every query flows through the _execute() gateway in sample_app/db.py — never call conn.execute() directly
  - SQL is always parameterized with ? placeholders — values are never interpolated into the SQL string

never:
  - guess when the code can answer — validate this mental model against the code
  - hand-edit this file — the agent maintains it
```

question.md step 3: "Verify the draft against the code: open every key_file the draft leaned on and confirm each fact — the code is the source of truth, expertise is only a lens."

self-improve.md step 3: "Diff what you found in the code against EXPERTISE_FILE and update the yaml: append new entries, adjust stale ones. Surgical changes only — never wholesale rewrite the file."
self-improve.md step 5: "Run this prompt after EVERY task that touches the data layer — mandatory, no human in the loop. Agents forget; experts learn by default."

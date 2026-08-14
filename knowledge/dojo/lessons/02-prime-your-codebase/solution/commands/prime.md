# /prime — Context Priming for sample_app

Your agent is brilliant, but blind: every session starts as a blank instance with no
context and no memories. This command gives a fresh agent your perspective on this
codebase — READ the right files, RUN a safe command, REPORT back what it learned.

## Purpose

Prime a fresh agent on the `sample_app/` codebase so it can start real work with zero
prior memory.

## READ

Read each of these files:

- sample_app/README.md
- sample_app/app.py
- sample_app/db.py

## RUN

Run this safe, read-only command and observe the output:

```bash
find sample_app -type f | head -20
```

## REPORT

After reading and running, report back exactly this structure:

1. What this app is: one sentence naming the app and its job.
2. Key modules: app.py (CLI entry point), db.py (JSON storage layer), config.json (settings).
3. Suggested next step: the single highest-value improvement you would make first.

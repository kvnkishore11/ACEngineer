# Hints — 02 · prime-your-codebase

## Hint 1

READ wants bare file paths, one per bullet, relative to this lesson directory — everything
worth reading lives under `sample_app/`. RUN must only look, never touch: if the command
could change a single byte on disk, it does not belong in a prime. REPORT is a numbered
contract — write each item as an instruction the agent fills in after priming.

## Hint 2

- READ: the README first (the map before the territory), then the entry point, then the
  storage layer. `ls sample_app/` shows you the candidates.
- RUN: `find sample_app -type f | head -20` is the canonical move — pipes are fine;
  `>` redirects, rm, mv, cp, touch, mkdir are not. Put it inside the ```bash fence.
- REPORT: phrase the three items as instructions, e.g. "1. What this app is, in one sentence."

## Hint 3

Near-answer:

- READ bullets: `sample_app/README.md`, `sample_app/app.py`, `sample_app/db.py`
- RUN (inside the fence): `find sample_app -type f | head -20`
- REPORT:
  1. What this app is: one sentence naming the app and its job.
  2. Key modules: app.py (CLI entry point), db.py (JSON storage layer), config.json (settings).
  3. Suggested next step: the single highest-value improvement to make first.

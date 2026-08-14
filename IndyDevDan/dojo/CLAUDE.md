# The Agentic Dojo

A fill-in-the-blanks training repo teaching IndyDevDan's agentic engineering patterns.
Lessons live in `lessons/NN-slug/`; each has starter files with `____` blanks, a
`check.py` closed-loop validator, `hints.md`, and a reference `solution/`.
`LESSON_SPEC.md` is the contract. `python3 dojo.py status|check|hint|diff|reset` runs everything.

## You are the sensei, not the solver

The human is here to LEARN. When they ask for help with a lesson:

- Give guidance the way `hints.md` does — nudge first, reveal last.
- NEVER paste solution files or fill blanks for them unless they explicitly say
  "just give me the answer" or ask you to run `dojo.py diff`.
- Prefer pointing at the failing check output: run `python3 dojo.py check NN`,
  read it with them, and explain WHY the check wants what it wants.
- Quote Dan's principles when they explain a design choice (the vocabulary is in
  `ai_docs/` and `LESSON_SPEC.md`).

## Working on the dojo itself

- Keep `check.py` files deterministic, offline, stdlib-only — never call an LLM from a check.
- A checker must fail on the pristine starter and pass on `solution/`. Test both before shipping.
- Blanks are `____` with a `YOUR TURN:` comment. Keep the house style (uv single-file
  scripts, PEP 723 headers, stdout reporting).
- `ai_docs/` holds the distilled source material from Dan's courses, videos, and repos —
  read it before writing lesson content; do not invent teachings he never gave.

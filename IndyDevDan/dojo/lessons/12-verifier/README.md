# 12 · The Verifier

"Quite literally spending 5x tokens to make sure that I spend less of my time... Tokens are cheap. Your time is not."

## The Idea

Agentic coding has two binding constraints: **how much you can plan** and **how much you can review**. Most engineers stall on review — hand-checking every "✅ done" a builder agent prints. The verifier attacks that constraint with the simplest, highest-value multi-agent system there is: a builder + verifier pair. One builds; the other proves. **Spend tokens to save time.**

The verifier's job is decomposition. "Everything you prompt into your agents — they're all small axioms... units of information that can be proven true or proven false." The builder's final message "is a CLAIM, never proof." So you pull every report apart into **atomic claims** — the smallest units that can each be independently proven or disproven — and verify each against actual state. "A single PASS that hides three unverified sub-claims is worse than three explicit FAILs." Evidence beats assertion: every verdict cites what the verifier actually observed, never what the builder said.

Two disciplines make it trustworthy. First, **read-only verification**: the verifier reads files, calls functions, scans ASTs — it never writes, never edits, never fixes. A verifier that fixes things is just a second builder you now have to verify. Second, it is **un-promptable by design**: "the verifier takes no input — it forces you to template your engineering." You can't type at it; when it misses something, you improve the persona, the script, or the dispatch — and the improvement solves the whole problem class. "I am increasing the trust I have in my agent system by having this verifier agent validate the atomic claims." Most agents increase trust or scale — the verifier does both.

## What Dan Did

In MA-4 (`disler/the-verifier-agent`) Dan ran two side-by-side Pi agents: a **builder** (Opus 4.7) and a **verifier** (GPT 5.5) — AND, not OR; stack intelligence. The verifier auto-spawns in its own tmux window with the input bar locked, fires on the builder's stop event over a unix socket, reads the builder's session JSONL, decomposes the turn into atomic claims (script ran, file exists, right size, right content), and re-proves each with read-only tools — domain personas pin bash to a single allowlisted script, "blocked, fully blocked" otherwise. When a claim fails, it calls its one tool that touches the builder — `verifier_prompt` — sending the corrective feedback you'd have written yourself, up to `max_loops: 3`, then escalates to the human. Every Report grades a confidence ladder (PERFECT → VERIFIED → PARTIAL → FEEDBACK → FAILED) and ends with "What could you not verify?" — the gap becomes the next thing you template. "This is a compounding system."

This lesson is that pattern in one file: the fixture reports are the builder's session, `verify_claim` is the read-only tool surface, `verification_report.json` is the report contract, and exit 1 is `verifier_prompt`.

## Your Mission

`sample_app/calculator.py` was "built" by a builder agent — it shipped a bug (do NOT fix it). `fixtures/builder_report.md` is the builder's claim bundle: four numbered claims, one of them false. Fill the blanks in `verifier.py`:

1. **`extract_claims(report_text)`** — parse the numbered claims out of the report. Decomposition first.
2. **`verify_claim(claim)`** — three read-only checks in the dispatch: docstring check via `ast`, behavior check by importing `sample_app/calculator.py` and actually calling the function, file-existence check via `pathlib`. Never edit anything.
3. **The report contract** — write `verification_report.json`: `{"claims": [{claim, verdict, evidence}, ...], "all_verified": bool}`.
4. **The exit code** — exit 1 when any claim fails (re-prompt the builder), exit 0 only when every atomic claim verified.

`fixtures/builder_report_honest.md` is the same report minus the lie — your verifier must pass it clean.

## The Loop

```bash
just check 12          # or: python3 ../../dojo.py check 12
```

The check runs your verifier on both fixtures: the dishonest report must exit 1 with the multiply claim false and evidence citing the observed result; the honest report must exit 0. Pass looks like:

```
✅ PASS — 12 verifier
```

## Done-when

- `python3 verifier.py fixtures/builder_report.md` extracts all 4 claims.
- The multiply claim's verdict is false and its evidence cites the actual observed result (multiply(4, 5) really returns 9).
- The file-existence, add-behavior, and docstring claims verify true.
- `verification_report.json` matches the contract and `all_verified` is false; exit code is 1.
- `python3 verifier.py fixtures/builder_report_honest.md` exits 0 with `all_verified` true.
- No `____` blanks remain.

## Level-up

Give unverifiable claims their own lane: instead of `verdict: false`, collect them into a `"could_not_verify"` list in the report — the flywheel section that teaches you what to template next. Then wrap builder + verifier in a loop script: when the verifier exits 1, feed its evidence lines back to the builder as a corrective prompt, cap it at `max_loops = 3`, then escalate to the human. That's Dan's `verifier_prompt` cycle in twenty lines of deterministic code.

## Run It Live

Ask a real builder for a report and verify it: in any repo, run `claude -p "add a tiny feature X; then write a numbered claim list of what you did to builder_report.md"`, point your verifier's dispatch at the real files, and run it. Or wire it as a Claude Code Stop hook that runs the verifier on every turn's report — the un-promptable observer, on your own harness. Never required for passing.

# TAC-5 Nuggets — ranked for the struggling learner

Ordering rule: how much of the rest of the course breaks if this nugget is missing. Tier 1 is non-negotiable; Tier 2 is the working machinery; Tier 3 is framing that keeps you honest when the loops feel like overhead.

---

## Tier 1 — If you remember nothing else

**1. One question runs the whole lesson.**
*"Given a unit of valuable work that's production ready, how would you, the engineer, test and validate this work?"* Answer it for every class of work your codebase handles, then **encode each answer into a command or tool call**. That encoded list is the leverage point — "you will fly while other engineers run."
*Why weak learners lose it:* they nod at the question and never write the list. The deliverable is literal commands, not agreement.

**2. Closed-loop prompt = Request → Validate → Resolve.**
The lesson's first one is three lines: change `sql_processor.py` / validate with `cd app/server && uv run ruff check .` / "If there are errors at all, resolve them." The feedback channel is just stdout entering the agent's context window. No validation block in your prompt = you volunteered to be the validator.

**3. Tactic #5 is a prompt-structure rule, not a testing philosophy.**
**Always add feedback loops** means the prompt you fire *today* carries validators. Not "stop testing or stop reviewing" — hand the responsibility off and teach your agents to test, so they "execute, validate, and reflect... in a loop until the job is done."

**4. Tests are the rule of law.**
Decide once, architecturally: when code and tests disagree, **the tests win**. If a test is genuinely wrong, agents fix the *test*, visibly — never route around red. The moment a failing validator is negotiable, every loop in the repo stops closing.

**5. The debate is over because the math changed.**
"The value of tests are multiplied by the number of agent executions that occur in your codebase." Same suite, dozens of unseen runs a day inside loops. That's why "engineers that test with their agents win. Full stop, zero exceptions."

---

## Tier 2 — The working machinery

**6. Stack loops across failure classes — six in this lesson.**
ruff (lint) → pytest (units, "one bucket") → `python -m py_compile` (syntax) → `bun tsc --noEmit` (types) → `bun run build` (production build) → Playwright e2e (does the button actually work). Each catches what the others can't. One validator is a start; disjoint coverage is confidence.

**7. The sabotage catch is the proof moment.**
Demo 1 comments out `validate_sql_query`; demo 2 — after `/clear`, a fresh agent, zero memory — runs pytest, finds it, uncomments it, restores the import. "Without knowing what we previously did... it fixed this issue." Validators carry your standards **across context windows**. That's why fresh agents are safe.

**8. The browser is just another tool call.**
Playwright MCP (`npx @playwright/mcp@latest` in `.mcp.json`) opens the app, screenshots before, runs 'select newest 7 products sort by price desc', screenshots after, and the agent **reads both images and confirms 7 results**. Your click-through ritual, encoded — pointable at staging or a production test account. Determinism rule: `scripts/reset_db.sh` first, or the precise assertion means nothing.

**9. Rerun everything after every fix.**
The reusable `# Validation` prompt's standing order: run validators top to bottom; on any error stop, resolve immediately, **then rerun every validation step** — a resolution can break an earlier check. Loops close on green sweeps, not one-off passes.

**10. Template the tactic so 'always' survives Tuesday.**
`/bug` and `/feature` are meta prompts (prompts that create prompts) whose Plan Format bakes in `## Validation Commands` (pytest, `tsc --noEmit`, build + reproduce-before/after) and **forces a new `.claude/commands/e2e/test_<name>.md` task whenever UI is affected**. Discipline decays; templates don't. "Validation commands baked in by default."

**11. adw_test is testing as its own SDLC node.**
Fetch issue → `/test` returns ONLY a JSON array (`test_name, passed, execution_command, test_purpose, error?`) → each failure goes to a fresh `/resolve_failed_test` agent that must reproduce via the given command → ≤4 rounds (stop early if nothing resolved) → e2e only if units are green: per-file `/test_e2e`, stop at first failure, `/resolve_failed_e2e_test`, ≤2 rounds → 📊 summary comment → commit → push → PR → honest exit code. Deterministic code owns retries; agents own judgment.

**12. Leave trails or every failure becomes archaeology.**
Every run persists `agents/{adw_id}/{agent}/prompts/*.txt` + `raw_output.jsonl`, and every issue comment is prefixed `{adw_id}_{agent_name}`. That's how the on-camera FAILED status traced to an **Anthropic API error 500** in ninety seconds — infrastructure, not product, honestly reported. "Adopt our agent's perspective: know what's inside of every agent at any time."

---

## Tier 3 — Framing that keeps you going

**13. Your most valuable contribution is the user's experience.**
Code, architecture, plans — means, not ends. Verifying the experience works is not the boring tax after engineering; it IS the value-securing act. The ultimate test is your users; the next best is now an army of agents.

**14. Everything is one tool call away.**
Linter, Datadog logs, Sentry, custom evals, LLM-as-judge, a browser: "tools are just functions and functions can do anything." Whatever you check today is encodable — the lesson's menu is a starter list, not a ceiling.

**15. Start tiny, move outward, stay on top.**
"Everything starts with a single prompt... in the loop, and then slowly move it out the loop. Get yourself a dedicated environment." And when the pipeline ships a PR, your job returns at the end: review — "the test on top of the test." The KPIs say why: attempts↓, size↑, streak↑, presence↓.

---

## Micro-quiz (close the book first)

1. Recite the core validation question. What's the *deliverable* after answering it?
2. Write a minimum viable closed-loop prompt for any repo you know (three parts, label them).
3. Name the six loops the lesson stacks, in escalation order, and what class each catches.
4. A red test is wrong. What happens next under the rule of law — and what must never happen?
5. Why did `/clear` before demo 2 make the pytest catch *more* impressive, not less?
6. adw_test: what are the two retry bounds, what gates e2e, and why does e2e stop at the first failing file?
7. The out-loop run said FAILED. Trace the diagnosis path from the issue page to the verdict.
8. What does the /bug template guarantee even if the engineer forgets everything from this lesson?

*(Answers: extract.md ideas 1, 4, 5, 5, 5/7, 8, 9, 7.)*

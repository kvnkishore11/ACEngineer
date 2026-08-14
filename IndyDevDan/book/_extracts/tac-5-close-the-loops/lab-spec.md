# TAC-5 Lab Spec — Close the Loops

**Scope rule:** every drill runs inside the course codebase only (`codebase/` → the tac-5 NL→SQL app; students: `git clone https://github.com/disler/tac-5.git`, then re-origin to your OWN GitHub repo so you control the issues/PRs the out-loop drills create). No external repos.
**Prime directive (graded throughout):** you type **zero** lines of application code by hand. Every mutation flows through a prompt — scratch-buffer prompt files are allowed and encouraged; opening the editor to "just fix it" is a failed lab.
**Second directive:** every prompt you fire carries a validation block. A request without a `validate` section is you volunteering to be the validator — the exact job this lesson exists to hand off.
**Time box:** 90–150 minutes (53:52 lesson, six reproduce drills + five stretch). Token cost: a long lesson of real agent runs — several in-loop closed loops plus at least one full `adw_test.py` node (plan/test/e2e agents). Pay to play; budget for it.

---

## 0 · Setup (15 min)

1. Clone and take ownership: `git clone https://github.com/disler/tac-5.git && cd tac-5`, create your own GitHub repo, `git remote set-url origin <yours>` (you need issues/PRs you control).
2. Verify the toolbelt: `claude --version`, `uv --version`, `bun --version`, `gh auth status`. Playwright MCP deps resolve on first use via `.mcp.json` (`npx @playwright/mcp@latest`).
3. Configure env: `cp .env.sample .env` (`ANTHROPIC_API_KEY` required for programmatic Claude Code) and `cp app/server/.env.sample app/server/.env` (OpenAI and/or Anthropic key for the NL→SQL feature).
4. **Permissions & control audit (do not skip):** open `.claude/settings.json` and answer in writing — name the deny rules (e.g. `git push --force`, `rm -rf`) and the five lifecycle hook events. Then read `.claude/commands/install.md` **before** you run it. Dan's rule: *"always review these slash commands... they have massive control."*
5. Boot: run `/install` in Claude Code (or manually: `uv sync --all-extras` in `app/server`, `bun install` in `app/client`, `sh scripts/reset_db.sh`, `sh scripts/start.sh`). Confirm `http://localhost:5173` renders with the sample tables. If the port is taken, use the stop/start scripts (Dan hits this on camera).

**Checkpoint 0:** you can state, without looking, what the agent may NOT do (deny rules) and which slash commands can mutate your repo. If you can't, re-read the files — reviewing the agentic layer before running it is a graded habit.

## 1 · The simplest closed loop (10 min)

In a scratch markdown buffer write the three-part prompt **exactly**:
- **Request:** comment out validation in `@app/server/core/sql_processor.py`
- **Validate:** `` cd app/server && uv run ruff check . ``
- **Resolve:** "If there are errors at all, resolve them."

Fire it. Watch ruff's stdout enter the agent's context window (the unused-import error from the now-dangling import), then watch the agent fix it and re-run ruff to green. Verify independently: `uv run ruff check .` → clean.

**Checkpoint 1:** name the three parts of what you just fired, and name the feedback channel. *(Request / Validate / Resolve; the channel is ordinary stdout landing in the context window — "everything is one tool call away.")*

## 2 · Three loops + the sabotage catch (15 min)

**`/clear` FIRST — this is the entire point of the drill.** New prompt: remove the `/api/insights` endpoint from `@app/server/server.py` and move `load_dotenv()` right below its import; validate with ruff, `uv run pytest`, and `uv run python -m py_compile server.py`; resolve everything found.

Watch three disjoint loops fire: ruff catches the E402 import-order issue (the agent may briefly add duplicate imports — "this happens" — and re-run); **pytest catches Drill 1's commented-out `validate_sql_query`** — an agent with zero memory of Drill 1 un-comments it and restores the `SQLSecurityError` import; py_compile seals syntax.

**Checkpoint 2 (write it down):** one sentence on why `/clear` made the pytest catch *more* impressive, not less. *(A fresh agent with no memory of the sabotage still caught and fixed it — proof that validators carry your standards across context windows, which is what makes fresh agents safe.)*

## 3 · The full stack incl. the browser (20 min)

`/clear`. Reproduce the `# Validation` reusable prompt from frame t1200:
- **Backend:** ruff, `uv run pytest`, `uv run python -m py_compile server.py`
- **Frontend:** `cd app/client && bun tsc --noEmit`, `bun run build`
- **E2E (Playwright MCP):** open `localhost:5173`, screenshot before, run `select newest 7 products sort by price desc`, click Query, screenshot after, **read both images and confirm exactly 7 results.**

Run it. Then do Dan's ultimate spot-check yourself: open the after-screenshot, copy the generated query into the real app, confirm the identical 7 rows. Count your loops.

**Checkpoint 3:** you counted **six** (ruff, pytest, py_compile, tsc --noEmit, bun run build, Playwright e2e), and you can state what makes the "confirm 7 results" assertion trustworthy. *(`scripts/reset_db.sh` restored a known DB state first; without determinism the precise assertion means nothing.)*

## 4 · Templated loops — validation by default (20 min)

Run `/bug 111 adw111` with Dan's junk-data description: *tests write junk tables to the production SQLite DB; they should run against in-memory DBs instead.* **Do NOT implement yet.** Open the generated `specs/issue-111-adw-adw111-sdlc_planner-*.md` and verify three things:
1. a `## Validation Commands` section exists,
2. it includes reproduce-before / reproduce-after commands (table diffs, targeted pytest),
3. there is **no** e2e task — this is a backend-only bug, so the template's "IMPORTANT: if the bug affects the UI..." conditional correctly did NOT fire.

Then `/clear` and `/implement` the plan. Confirm all its validation commands pass and that `git status` shows no junk tables after `uv run pytest`.

**Checkpoint 4:** state what the `/bug` meta prompt guarantees about every plan it emits, and the exact condition that forces a new `.claude/commands/e2e/test_<name>.md` task. *(Every plan ends with a Validation Commands section; a new e2e file is forced whenever the bug affects UI or user interactions.)*

## 5 · The test node, out-loop-shaped (25 min)

Restore a clean state (commit or revert). Create a real issue on **your** repo — e.g. the debounce bug: *"disable the query input while a query is running, add a debounce."* Run the test node directly:

```
cd adws && uv run adw_test.py <issue-number>
```

Verify the full trail: `{adw_id}_`-prefixed issue comments, the 📊 **Test Run Summary** comment, a `test-issue-*` (or reused) branch, a commit with the sdlc-formatted message, a PR, and `agents/{adw_id}/` containing `test_runner/raw_output.jsonl` (plus `e2e_test_runner_*` dirs with `img/` screenshots if e2e ran).

**Checkpoint 5:** the run left a complete audit trail (prefixed comments, summary, commit, PR, per-agent prompts + `raw_output.jsonl`). If it failed, you can point to *where* the failure was reported, not guess at it.

## 6 · Read the trail like Dan (10 min)

From Drill 5's run, open `agents/{adw_id}/test_runner/prompts/test.txt` and `raw_output.jsonl`. Find the JSON array `/test` returned; confirm each entry carries an `execution_command` you could paste straight into a terminal. If anything failed, open the matching `test_resolver_iter*/` or `e2e_test_resolver_iter*/` directory and read the exact payload the resolver received.

**Checkpoint 6:** you diagnosed a real (or simulated) failure from saved artifacts alone — the on-camera skill that turned an out-loop FAILED status into "Anthropic API 500, infrastructure not product" in ninety seconds.

## Stretch drills (still zero hand-typing)

**S1 — New e2e spec.** Via Claude Code, create `.claude/commands/e2e/test_hide_button.md` modeled on `test_basic_query.md`: User Story → Test Steps (with `**Verify**` markers) → Success Criteria incl. a screenshot count. Execute via `/test_e2e` (pass an adw_id, agent name, the file); verify JSON output + screenshots under `agents/<id>/<agent>/img/hide_button/`.

**S2 — Break a loop on purpose.** Have Claude Code flip an assertion in `tests/core/test_sql_processor.py`, commit to a scratch branch, run `uv run adw_test.py <issue>`, and watch `resolve_failed_test` reproduce → fix → rerun. Then answer: what stopped the system from "fixing" it by deleting the test? *(Your review + the resolver's minimal-change instructions — rule of law is a human-enforced architecture decision, not a model behavior.)*

**S3 — Bound the loops.** Re-run Drill 5 with `--skip-e2e`; explain when that flag is correct (e2e too slow/flaky for this iteration) and what confidence you gave up. Then read `MAX_TEST_RETRY_ATTEMPTS` (4) and `MAX_E2E_TEST_RETRY_ATTEMPTS` (2) in `adw_test.py` and state why unbounded resolution would be worse than honest failure.

**S4 — Add a seventh loop.** Pick a validator the lesson didn't use (`uv run ruff format --check .`, a coverage threshold, `npm audit`) and thread it through all three altitudes: the `# Validation` reusable prompt, the `/bug` Plan Format defaults, and `test.md`'s sequence (with `test_name` / `test_purpose` / `execution_command`). One loop, three altitudes — that IS "templating your engineering."

**S5 — Answer the core question for YOUR codebase.** Write the validation menu for the repo you actually work on: for each class of work (bug / feature / chore / data), the exact commands that would prove it production-ready. Mark which are encodable today vs. which need architecture work first (the net-new advantage, inverted). This list is your next month of leverage.

## Pass criteria (all required)

- [ ] Zero application code typed by hand; every edit flowed through a prompt (scratch prompt files allowed)
- [ ] Drill 1's ruff loop closed autonomously: sabotage introduced, flagged, resolved, re-validated green with no human edits
- [ ] Drill 2 performed **after** `/clear`, and you can articulate why the pytest catch proves validators enforce standards across fresh context windows
- [ ] Drill 3 stacked all six loops and produced before/after screenshots whose result you independently reproduced in the browser (7 rows)
- [ ] Drill 4's generated plan contains a Validation Commands section with reproduce-before/after commands and correctly omits the e2e task for a backend-only bug
- [ ] Drill 5 left a complete audit trail: prefixed issue comments, 📊 summary, commit, PR, and `agents/{adw_id}/` with per-agent prompts and `raw_output.jsonl`
- [ ] Oral check, no notes: the core validation question verbatim; request→validate→resolve; the six loops; the rule of law (and what to do when a test is genuinely wrong); `adw_test`'s retry bounds (4 unit / 2 e2e, e2e gated on green units, stop at first e2e failure); why `/test` returns JSON with `execution_command`

## Instructor / self-check notes

- **The single most common failure:** skipping `/clear` before Drill 2. If the agent still remembers Drill 1, the cross-context catch is fake and the whole lesson about validators-carry-standards evaporates. Enforce the clear.
- **Port conflict on boot** (Drill 0/5): a stale server holds `:5173`/the API port. Use the stop-then-start scripts; Dan hits exactly this at ~13:00. Teaches why runbooks state their starting state.
- **Determinism stall (Drill 3):** if a student skips `scripts/reset_db.sh`, "confirm 7 results" becomes noise and they wrongly distrust their strongest loop. The DB reset is not optional decoration — it's what makes the precise assertion an assertion.
- **One in-loop agent per repo (Drills 1–4):** this lesson does no worktrees — only one repo-mutating agent runs on your device at a time. That constraint is exactly what the out-loop architecture (Drill 5) removes; name it so students don't think it's a bug.
- **Honest failure is success (Drill 5/6):** if `adw_test` reports FAILED because of an Anthropic API 500, the system is *working* — it surfaced an infrastructure failure it genuinely can't resolve. Reward the accurate report; a loop that can't fail loudly can't be trusted to pass quietly.
- **Cost anxiety:** a full `adw_test.py` node spins several agents across fresh contexts — it is the most expensive drill. If budget is tight, S3's `--skip-e2e` is a legitimate way to see the node work for less; the pay-to-play conversation is itself part of the lesson.
- **What this lab intentionally does NOT cover:** the review and document SDLC steps (TAC-6), full webhook/tunnel out-loop infrastructure (optional, TAC-4 territory), and multi-agent worktree parallelism. Deflect scope creep to keep the closed-loop primitive crisp.

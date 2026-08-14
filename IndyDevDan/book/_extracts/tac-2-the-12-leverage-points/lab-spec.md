# TAC-2 Lab Spec — The 12 Leverage Points

**Scope rule:** every drill runs inside the course codebase only (`codebase/` → `tac/tac-2`; students: `git clone https://github.com/disler/tac-2.git`). No external repos. New dependency: the demo app itself calls LLM APIs, so an OpenAI **and/or** Anthropic API key goes in `app/server/.env` (either one suffices — the router prefers OpenAI if both exist).
**Prime directive (graded throughout):** you type **zero** lines of application code by hand. Every code change — the stdout prints, the sanitizer, even editing prompt files — goes through your agent.
**Second directive (this lesson's own rule):** you do not read errors to your agent. The agent must SEE failures through stdout it observes itself. If you catch yourself pasting an error message, you've skipped the leverage point this lab installs.
**Time box:** 75–120 minutes. Token cost: one install/prime cycle + ~6–10 short agentic prompts + one subagent trace (the trace alone ran ~27k tokens for Dan; budget accordingly — pay to play).

---

## 0 · Setup (15 min)

1. `git clone https://github.com/disler/tac-2.git && cd tac-2`
2. **Permissions audit (do not skip):** open `.claude/settings.json` and answer in writing:
   - Which nine Bash patterns plus which file tool are allowed?
   - Which three commands are **denied**? (`git push --force`, `git push -f`, `rm -rf`) — first TAC repo with a deny list; why these three?
   - Unlike tac-1, no git commit/checkout allowance appears — what does that tell you about this lesson's focus?
3. `cd app/server && cp .env.sample .env` → add `OPENAI_API_KEY` and/or `ANTHROPIC_API_KEY`. Don't leak keys on stream.
4. Boot `claude` at repo root → run `/install`. Watch it read-and-execute `prime.md` (prompts inside prompts) and install FE+BE deps. Open `.claude/commands/install.md` (7 lines) and `prime.md` (7 lines) and say out loud what each line does.
5. `./scripts/start.sh` from a fresh terminal (WSL on Windows). Verify: frontend `localhost:5173`, backend `localhost:8000` (`/docs` for the API), then Upload Data → sample `products.csv` → query **"list top 5 products by price"** → SQL + results render.

**Checkpoint 0:** you can state without looking: the three shipped slash commands, what `/prime` runs (`git ls-files` + read `README.md` + summarize), and the app's five API endpoints (upload, query, schema, insights, health — plus the delete-table route).

## 1 · See like your agent: tools + the planted bug (15 min)

1. In Claude Code run `/tools`. Read the whole list. Write down: (a) what `Task` does, (b) the Bash tool's three parameters, (c) which tools can modify files.
2. Drag `app/client/public/sample-data/orders_(32).csv` into Upload Data. Capture both facts:
   - Browser: `Error converting CSV to SQLite: near "(": syntax error`
   - Server terminal: **nothing printed at all**
3. Open `app/server/server.py` and confirm the committed repo has zero `print()` calls — every endpoint swallows exceptions into a response `error` field. Predict (in one sentence) why the filename `orders_(32).csv` breaks table creation before you look at `core/file_processor.py`.

**Checkpoint 1 (write it down):** define *bad agentic code* in your own words, and name the exact failing statement (`PRAGMA table_info({table_name})` at `core/file_processor.py:26` receiving `orders_(32)`).

## 2 · Reproduce Dan — install the stdout lever, let the agent fix the bug (25 min)

1. New agent → `/prime` → prompt (reference the file with `@`):
   `@app/server/server.py make sure every exception prints all exception details, and make sure every successful response prints before returning`
   Turn auto-accept on (Dan's "YOLO mode"). Review the resulting `[ERROR]`/`[SUCCESS]` diff — do not edit it by hand.
2. Restart services (`Ctrl+C` → `./scripts/start.sh`), re-upload the bad CSV, and verify the SQLite error now traces to the server's stdout.
3. Kill the outside server. Fresh agent → `/prime` → prompt **exactly**: `sh ./scripts/start.sh, 300s` — the app now runs *inside* the agent (this is the Bash `timeout` parameter you read about in drill 1).
4. In the browser, re-upload `orders_(32).csv` to reproduce the failure *while the agent watches*.
5. Stop the run, then ask: **`any issues with the server?`** — expect a diagnosis naming `file_processor.py:26` and unescaped special characters. If the agent can't answer, a lever is missing: check your prints survived the restart and the server really ran inside the agent.
6. Then: **`resolve: replace bad chars and escape`** — review the `sanitize_table_name()` diff (strip extension, replace bad chars with underscores, leading-letter guard, non-empty guard).
7. Close the loop: relaunch inside the agent, delete the old `db/database.db`, re-upload → success; query **"latest delivery"** → sensible rows.

**Checkpoint 2:** two short prompts fixed a real bug. List the three system conditions that made that possible *(stdout prints existed; the server ran inside the agent's context; the agent had CRUD tools per settings.json)*. This list IS Tactic #2 operationalized.

## 3 · Types, tests, templates, ADW seed (20 min)

**A. Type-flow trace (IDKs).** Copy `DatabaseSchemaResponse` from `core/data_models.py`. Open a **brand-new** `claude` instance (zero context — that's the point). Prompt: `show me how this type flows throughout the application, detail functions, files, and purpose` plus a format sketch (`file:\n  function: purpose\n...`). While it runs, note the `Task(...)` subagent line. Verify its answer with your own `grep -rn DatabaseSchemaResponse` — expect exactly five locations: `core/data_models.py`, `server.py`, `client/src/types.d.ts`, `client/src/api/client.ts`, `specs/init_nlq_to_sql_to_table.md`.

**B. Closed loop (tests).** Inside the agent: `!` → `cd app/server && uv run pytest`. All tests pass, output lands in context. Then prompt the agent to *write a test for `sanitize_table_name` covering parenthesized filenames* and run pytest again itself. Green = your first closed loop.

**C. Three-time rule (templates).** You've started the server at least three times by now. Do what Dan does: tell the agent to create `.claude/commands/start.md` containing exactly `sh ./scripts/start.sh 300s`. Restart `claude`; run `/start`; verify both services boot inside the agent.

**D. ADW seed (programmable mode).** Exit the agent. From the plain shell: `claude -p "/tools"`. The reusable prompt runs headlessly and returns to your prompt. Say Dan's ADW formula out loud while it runs: *agentic prompts + arbitrary code + a trigger.*

**Checkpoint 3:** grep confirmed all five type locations; pytest ran INSIDE the agent twice (before/after the new test); `/start` works from a cold session; `claude -p` returned the tool list to your shell.

## 4 · Stretch drills (20–40 min, still zero hand-typing)

**S1 — Prime upgrade (context lever).** Via the agent, extend `prime.md` to also read `core/data_models.py`. Boot a fresh agent, `/prime`, and ask a type question — compare how much less exploration it needs. One sentence: which leverage point did you just move?

**S2 — Leverage-point ablation (the diagnostic, experienced).** `git checkout app/server/server.py app/server/core/file_processor.py` (reverting the agent's fixes — allowed: it's config/reset, not application code). Now ask a fresh agent, with the server running OUTSIDE it and no stdout: `fix the CSV upload bug`. Document the flailing. Restore the levers (re-run drill 2 quickly or `git stash pop` your diff) and repeat. Write one sentence naming the exact levers whose absence caused the failure. *(This drill is the KPI section's "figure out which leverage point you were missing" made physical.)*

**S3 — KPI journal.** For your next three agentic prompts in this repo, log: size (minutes the agent ran), attempts (post-completion corrections), streak (consecutive one-shots), presence (times you intervened). When anything breaks the streak, write the missing-lever diagnosis before re-prompting.

**S4 — IDK rename.** Find the weakest type name in the repo (Dan nominates `QueryRequest`/`QueryResponse` as "not that good"). Have the agent rename one to something information-dense (e.g. `NaturalLanguageQueryRequest`) across all its locations, run pytest inside the agent, and re-run the type-flow trace on the new name.

**S5 — Architecture audit (read-only).** Score `tac-2` against all nine checklist items: clear entry points / constant files / types / verbose IDK names / ≤1000-line files / distributed agent docs / separated services / one responsibility per file / mirrored tests. Then score a repo you own. **Do not refactor** — Dan's explicit instruction; write the gap list for the later lessons that do it with your agent.

## Pass criteria (all required)

- [ ] Zero application code typed by hand; zero error messages pasted to the agent
- [ ] Permissions audit answers correct, including the three denied commands (checkpoint 0)
- [ ] Bad-agentic-code definition + exact failing line identified (checkpoint 1)
- [ ] `orders_(32).csv` upload fails before / succeeds after, with `[ERROR]`/`[SUCCESS]` traces you can point to in server stdout
- [ ] The agent's diagnosis cited `file_processor.py`'s PRAGMA call from stdout it observed itself — no human relay
- [ ] Type-flow answer matched your grep exactly (five locations)
- [ ] pytest ran inside the agent, including one new agent-written sanitizer test, all green
- [ ] `/start` works from a cold session; `claude -p "/tools"` returned headlessly
- [ ] Closing oral check, no notes: the 12 points in two families; Tactic #2 + its litmus question; the four KPIs with directions; which two levers you install first in any codebase (stdout, then tests)

## Instructor / self-check notes

- **Most common stall:** running `sh ./scripts/start.sh, 300s` while the *outside* `start.sh` still holds ports 5173/8000 — the inside run dies instantly. Fix: `./scripts/stop_apps.sh` (or Ctrl+C the outer terminal) first. Teaches why runbooks state their starting state.
- **Second stall:** re-uploading the bad CSV after the sanitizer fix but before deleting the stale `db/database.db` — mixed old/new tables confuse the verify step. Dan deletes the db file mid-demo; make it explicit.
- **Timeout expiry confusion:** the 300s Bash timeout kills the in-agent server after five minutes; students think something broke. It's the documented parameter doing its job — re-run the prompt (or `/start` once minted).
- **`.env` misses:** `start.sh` exits early with instructions if `app/server/.env` is absent — that error message is itself a stdout-lever example worth pointing at.
- **Both keys absent → the app boots but every query errors** (router raises on missing keys); at least one key is genuinely required.
- **Model pins are period details:** `llm_processor.py` hard-codes `gpt-4.1-mini` / `claude-3-haiku-20240307`; if a student's account lacks one, swapping the ID (via the agent) is a legitimate micro-drill, not a detour.
- **Cost anxiety:** the type trace alone was ~27k tokens on camera; the full lab is a few hundred k. If that's a blocker, the pay-to-play conversation from lesson 1 is surfacing again.
- **What this lab intentionally does NOT cover:** MCP servers, meta-prompting/plan generation (lesson 3), frontend agent testing, real ADW construction (`adws/` stays empty), and any refactoring of architecture — deflect scope creep to keep the twelve levers crisp.

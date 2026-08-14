# TAC-3 Lab Spec — Success is Planned

> Course codebase only (`tac/tac-3` · clone: https://github.com/disler/tac-3.git). Prime directive carried from TAC-1: **zero application code typed by hand.** New discipline this lesson: **plan in one fresh agent, implement in another** — no rolling conversations.
> Scope contract: work only inside the cloned tac-3 repo (stretch S3 excepted); do not improvise destructive Git commands; note the repo's own deny list (`git push --force`, `git push -f`, `rm -rf`) and leave it intact.

## 0 · Setup (10–15 min)

1. `git clone https://github.com/disler/tac-3.git && cd tac-3`
2. Read `.claude/settings.json` **aloud** — allow list (12 entries) AND the deny list (the course's first explicit guardrails). Say what the agent may do without asking.
3. API keys — pick one path:
   - **On-camera path:** tac-2 cloned as a sibling with `app/server/.env` populated → `/install`'s `copy_dot_env.sh` step works as filmed.
   - **Fallback:** `cd app/server && cp .env.sample .env` and add `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` (the copy script will report an error; that's expected and fine).
4. `claude` → `/install`. Read its report: prime ran (git ls-files + README), FE + BE deps installed, .env in place.
5. New terminal: `sh ./scripts/start.sh` → backend :8000 + frontend :5173. Upload `users.json` (sample button), run **"Show users with age between 20 and 40"**. App works = setup passes. Note the raw `print` output in the server terminal — that's the chore target.

## 1 · Reproduce Dan — the chore, two prompts, two agents (20 min)

**Checkpoint 1a — meta prompt (planning phase).** In a FRESH Claude Code instance:
`/chore "Replace all server print statements with proper python logging. Use proper log levels. Preserve the exact same log output. Make sure all output is written to standard out"`
Pass when: a new plan exists in `specs/` with all six sections of chore.md's Plan Format (Chore / Chore Description / Relevant Files / Step by Step Tasks / Validation Commands / Notes), and its inventory identifies the prints in `app/server/server.py` and `app/server/main.py` (19 on disk; the plan's prose count may vary — the line list is what matters). While it runs: open `.claude/commands/chore.md` and locate all five template parts, including `$ARGUMENTS`.

**Checkpoint 1b — HOP (building phase).** Open a NEW instance:
`/implement specs/<your-chore-plan>.md`
Watch the todo list mirror the plan's steps. Pass when ALL of:
- `cd app/server && uv run pytest` green (37 pre-existing tests, zero regressions)
- `grep -rn "print(" app/server --include="*.py"` → no hits in `server.py` outside tests (main.py's `if __name__` stub may legitimately become a logger call — accept either)
- restart `scripts/start.sh`, run **"get users id name sorted by signup date descending"**, and confirm the same `[SUCCESS]`/`[ERROR]` message shapes now flow through logging to stdout
- the agent's Report ended with a bullet summary + `git diff --stat`

**Reset note:** commit now (`specs/` + code). If a run goes sideways: `git status` → `git checkout -- .` on unwanted tracked changes (never `rm -rf`, it's denied anyway) and re-fire the phase from its file — that reproducibility is the lesson.

## 2 · Reproduce Dan — the bug, root cause and all (25 min)

**Checkpoint 2a — bug template.** Fresh instance:
`/bug "Resolve major issue: our SQL statements are not being escaped — user input flows into SQL"`
Pass when the generated plan has non-empty **Steps to Reproduce** and **Root Cause Analysis** naming (at minimum) the keyword-blocklist weakness and f-string identifier interpolation — both really on disk: raw `cursor.execute(sql_query)` behind a 10-keyword substring blocklist in `core/sql_processor.py`, and `cursor.execute(f"DROP TABLE IF EXISTS {table_name}")` at `server.py:243`. Expect a `### New Files` section (Dan's run: `app/server/core/sql_security.py`).

**Checkpoint 2b — implement + verify like an engineer.** Commit, then in a NEW instance `/implement <bug plan path>`. Pass when ALL of:
- pytest green with **new** injection-focused tests added (Dan's run: 18 new, 52 total — your counts WILL differ; require ≥1 new test file + zero regressions)
- follow the plan's own Steps to Reproduce: through the UI, request something injection-shaped (concatenated fields; a `'); DROP TABLE users;--`-style query) → safe result or clean error, never a schema change
- you ran `cd app/server && uv run pytest` yourself, not just trusted the report

## 3 · Reproduce Dan — headless planning (15 min)

**Checkpoint 3 — claude -p + stream-json.** From a PLAIN terminal (not inside Claude Code), fire your own `/feature` one-liner (or Dan's query-history-panel prompt) exactly in the video's shape:

```sh
claude -p "/feature \"<your feature description>\"" \
  --output-format stream-json \
  --dangerously-skip-permissions \
  --model <your-best-model> \
  --verbose \
  > feature_plan_raw_agent_logs.jsonl
```

`tail -f` the JSONL while it runs. Pass when: the file contains a `system`/`init` event plus assistant/tool events; a new feature plan appears in `specs/` with User Story, phased Implementation Plan, Testing Strategy, and Acceptance Criteria; and you never touched an interactive session. **Do not implement it** (matching Dan) unless taking S4. Safety framing: permission-skipping was acceptable here because the run only *plans* in a demo repo — say that out loud before firing.

## 4 · Stretch drills (20–40 min, still zero hand-typed app code)

- **S1 · Specialize a template:** copy `bug.md` → `.claude/commands/bug-frontend.md`; restrict Relevant Files to `app/client/**` and adjust instructions. Run both `/bug` variants on the same UI-shaped symptom; diff the two plans — that's encoding, visible.
- **S2 · Write a HOP variant:** create `implement-and-review.md` (implement the plan, then review completed work against the plan and report deviations before the summary). Run it on a fresh branch against your chore plan; compare reports with 1b.
- **S3 · Port the pattern home (the lesson's real CTA):** copy `chore.md` into a repo you own; rewrite ONLY Relevant Files + the Validation Commands seed; run one real small chore end-to-end (fresh plan agent → fresh implement agent).
- **S4 · Chain the phases:** shell script that runs the claude -p planning command, extracts the new spec path (glob `specs/` or parse the JSONL), then launches a second `claude -p` with `/implement` on it. You just hand-rolled a two-node ADW — lesson 4's on-ramp.

## Pass criteria (all required)

- Zero application code typed by hand anywhere (template/HOP files are prompts and may be created via the agent or by hand — they are the one sanctioned writing surface)
- Every plan was generated in one fresh instance and implemented in a different fresh instance
- `specs/` holds ≥3 generated plans (chore, bug, feature), each following its template's exact section skeleton
- pytest green after each implement run; new injection tests exist after §2; no-print grep clean after §1
- `feature_plan_raw_agent_logs.jsonl` exists, parses line-by-line as JSON, and corresponds to a spec you never interactively created
- Stated from memory: meta prompt vs HOP; the five template parts; the three fresh-agent reasons; the four KPIs the doctrine serves

## Instructor / self-check notes

- **Counts that may trip students:** on-disk = 18 prints in server.py + 1 in main.py (19); the video agent's prose says 19/20 (its own inventory totals 18+1). Video reports 52 tests / 18 new post-bug-fix; the shipped repo has 37 test functions. Grade on invariants (zero regressions, new coverage, empty grep), never on matching Dan's numbers.
- **implement.md line count:** displays as 12 lines; `wc -l` says 11 (no trailing newline). Both true.
- **copy_dot_env.sh** hard-fails without a sibling `../tac-2/app/server/.env` — the fallback in Setup 3 is expected for most readers.
- **Injection reality check:** sqlite3's `cursor.execute` won't run stacked statements, so the drama is in UNION/subquery reads and the `delete_table`/PRAGMA identifier interpolation — if a student's plan says "multiple statements", have them test it and refine the plan (template improvement in action).
- **Model drift:** `--model opus` on camera = claude-opus-4-20250514 (visible in the JSONL frame). Students substitute their era's best model; behavior equivalence, not output equality.
- **If a student's generated plan is thin:** the fix is upstream — improve the template (add detail to Instructions/Relevant Files), regenerate, re-implement. Never patch downstream code by hand; that's the whole tactic.

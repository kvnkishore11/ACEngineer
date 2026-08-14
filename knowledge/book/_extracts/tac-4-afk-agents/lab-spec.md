# TAC-4 Lab Spec — AFK Agents

**Scope rule:** every drill runs inside the course codebase only (`codebase/` → `tac/tac-4`; students: `git clone https://github.com/disler/tac-4.git`) — pushed to a GitHub repo the student owns (mandatory: the ADW needs YOUR issues and PRs). No external repos; no dependencies beyond the lesson's prerequisites.
**Prime directive (graded throughout):** you type **zero** lines of application code by hand. Template and config edits go through Claude Code. The AGENT builds the feature; you build the system.
**Time box:** 90–150 minutes (two full ADW runs ≈ 5–20 min each of agent time — use it to do the trace drills). Token cost: two+ full ADW runs, each ~8 agent invocations, plus health checks — noticeably more than tac-1's lab; pay to play.
**Safety note:** ADW template runs use `--dangerously-skip-permissions` by design. Run this lab in a checkout you can afford to lose (a dedicated machine or at minimum a dedicated directory + repo), exactly per the lesson's E-element argument. Never with production credentials in the environment.

---

## 0 · Setup — build your PITER perimeter (25 min)

1. Fresh directory → `git clone https://github.com/disler/tac-4.git && cd tac-4`
2. Open Claude Code. **Read `.claude/commands/install.md` before running it** — say out loud what it will do (remove course remote, git init, cp .env.sample, install FE+BE deps, attempt tac-2 env copy). Then run `/install`.
3. Follow the install report's *action required*: create a new empty GitHub repo you own; `git remote add origin <your-repo-url>`; `git push -u origin main`.
4. Fill **root** `.env` via the samples: `ANTHROPIC_API_KEY` (programmatic mode runs on the API key in this course build), `CLAUDE_CODE_PATH` (paste `which claude` output if the bare name fails). Fill `app/server/.env` (OpenAI and/or Anthropic key) for the app itself.
5. **Permissions audit (do not skip):** open `.claude/settings.json` and answer in writing:
   - Which Bash commands are pre-approved for interactive sessions? Which THREE things are denied? (force-push ×2 forms, `rm -rf`)
   - Which five hook events are wired, and where do their logs land? (`logs/{session_id}/`)
   - Separately: why does the ADW **not** rely on this file at run time? (`execute_template` → `dangerously_skip_permissions=True`; the environment is the boundary)
6. Create a warm-up issue on YOUR repo (any title). **Pre-flight:** `uv run adws/health_check.py <n>`.

**Checkpoint 0 (gate — do not proceed until):** health check prints `Overall Status: HEALTHY`, shows **no** "still points to 'disler'" warning, Claude Code live-test passed (`response: 4`), and a ✅ comment appeared on your issue.

## 1 · Chore ADW — your first out-loop run (25 min)

1. Create **issue A** — title `ADW Documentation`, body exactly in Dan's shape: `/chore` + "we need to document the adw/ directory. Read everything in adw/ then update README.md with information about how it works."
2. Fire the manual trigger: `uv run adws/adw_plan_build.py <A>`. (Running it from the repo root gives `Failed to spawn` — Dan hits this too; the script lives under `adws/`. Diagnose, don't panic.)
3. **Hands off.** While it runs, open the issue and narrate the live feed as it drains: `{adw_id}_ops: ✅ Starting ADW workflow` → `✅ Issue classified as: /chore` → `✅ Working on branch: chore-<A>-<adw_id>-<slug>` → planner → plan file → commit → implementor → commit → PR.
4. Verify like a grader (all from evidence):
   - branch name matches `<class>-<issue>-<adw_id>-<slug>`
   - a `specs/*-plan.md` exists **on the branch**, and its shape matches `chore.md`'s Plan Format
   - `git log` on the branch shows two commits in the `<agent_name>: <issue_class>: <message>` format
   - the PR body contains: plan link, changes checklist, `Closes #<A>`, and the ADW tracking ID
5. **Audit the PR content against reality** (the lesson's own PR mislabeled "ADW" and described files that don't exist). Write down every inaccuracy — or explicitly "none found" — and, for each, WHICH file owns the fix (`chore.md`? `pull_request.md`? the README the agent wrote?).

**Checkpoint 1 (write it down):** the audit list + the ADW ID traced through all five surfaces: issue comments → branch name → `agents/<adw_id>/` → commit messages → PR body.

## 2 · Feature ADW — reproduce the JSONL run (35 min)

1. Confirm the gap first: `sh scripts/start.sh`, open `localhost:5173`, try uploading a `.jsonl` → the UI/API only accept `.csv`/`.json` (`app/server/server.py` rejects the rest). The feature you're about to ship does **not** exist in the repo — that's the exercise.
2. Create **issue B** — title `Jsonl Support`, body with Dan's constraints (verbatim is fine): add support for uploading jsonl files; look through the entire jsonl first to get all possible fields; std lib only — no new libraries; one jsonl file → one new table just like csv/json uploads; concat nested fields (and nested lists) with `__`, stored as an updatable delimiter in a constants file; use `_0` to denote list items; update the UI so users know jsonl is allowed; create a couple of test .jsonl files in the test dir.
3. Pre-flight again: `uv run adws/health_check.py <B>` → HEALTHY.
4. Fire: `uv run adws/adw_plan_build.py <B>`. Expect ~15–20 minutes of agent time.
5. **Trace drill while it runs** (this is the lab's core learning): in a second terminal —
   - `tail -f agents/<adw_id>/adw_plan_build/execution.log`
   - after each step completes, open `agents/<adw_id>/<agent>/prompts/*.txt` (the EXACT prompt sent) and `raw_output.json`; find the `result` line: note `num_turns`, `duration_ms`, `total_cost_usd`
   - connect each issue comment to the artifact that produced it
6. Review the PR like you'd merge it: read the committed plan FIRST (Dan's was 170 lines), then files changed, then validate: `git checkout <feature-branch>`, `cd app/server && uv run pytest` (green, including new tests), `sh scripts/start.sh`, regression-test an old query, drag-drop the agent-created `.jsonl` fixture, and confirm the resulting table honors `__` and `_0` from your issue.

**Checkpoint 2:** feature verified live in the app + pytest green + one sentence: what did YOU contribute to this feature after clicking Create on the issue? *(Target answer: the prompt input and the review — nothing else.)*

## 3 · Trigger drills — the T is interchangeable (20 min)

1. **Cron:** `uv run adws/trigger_cron.py` → comment exactly `adw` on issue A → watch it re-process within ~20 seconds → Ctrl+C. State the two conditions that make cron fire. *(New issue with no comments; latest comment exactly 'adw'.)*
2. **Webhook (optional infra — attempt, and record the outcome either way):** `uv run adws/trigger_webhook.py` (port 8001) → expose via `scripts/expose_webhook.sh` (needs `CLOUDFLARED_TUNNEL_TOKEN`) or ngrok → GitHub repo → Settings → Webhooks → payload URL `<public-url>/gh-webhook`, events: Issues + Issue comments → create a tiny chore issue **from your phone** → watch a PR appear. Hit `GET /health` on the trigger and read its embedded health-check summary.
3. Kill everything when done: `scripts/kill_trigger_webhook.sh`, `scripts/stop_apps.sh`. State why leaving a trigger listening is a cost bug. *(Every new issue / 'adw' comment = a full ADW run = tokens.)*
4. Reset utilities for re-runs: `scripts/clear_issue_comments.sh <n>`, `scripts/delete_pr.sh <n> [--delete-branch]`.

**Checkpoint 3:** same ADW, three triggers (manual, cron, webhook-or-documented-attempt) — in your own words, which PITER element changed and which didn't.

## 4 · Stretch drills (30–45 min, still zero hand-typing)

**S1 — New problem class.** Via Claude Code: add `/docs` (or `/test`) as a first-class issue class — new `.claude/commands/docs.md` meta-prompt cloned from `chore.md`'s shape, extend `IssueClassSlashCommand` + `SlashCommand` Literals in `adws/data_types.py`, add the mapping line in `classify_issue.md`. Prove it: an issue classified `/docs` runs end-to-end. *(This is the exact extension path Dan names: "you just add them here in your classify issue step, and then you update your data types.")*

**S2 — Fix the system.** Take the worst inaccuracy from your Checkpoint-1 audit and encode the fix into the owning template (e.g., `pull_request.md`: "ADW always expands to *AI Developer Workflow*; describe only files that exist"). `scripts/clear_issue_comments.sh` + `scripts/delete_pr.sh`, rerun issue A, and diff the two PRs to demonstrate a class-level fix. Bonus target: the shipped `adws/README.md` claims model selection lives at "agent.py line 129" — find where model choice REALLY lives (`data_types.py` Literals/defaults; per-step args in `adw_plan_build.py`) and fix the doc via a chore run.

**S3 — Break the pre-flight.** Temporarily unset `ANTHROPIC_API_KEY` (or point the remote back at disler/tac-4). Run: the health check, the webhook's `GET /health`, then an actual ADW run. Record where each layer catches it and what lands on the issue (`❌ ...`). Restore. One sentence: why do pre-flights belong INSIDE the workflow layer?

**S4 — Model policy.** Via Claude Code, switch `sdlc_planner` and `sdlc_implementor` requests to `"opus"` in `adw_plan_build.py`. Rerun a feature-class issue; compare plan depth, `num_turns`, `duration_ms`, `total_cost_usd` against the Sonnet run from your saved `raw_output.json` result lines. Verdict in two sentences, referencing Dan's policy (top models on plan/build).

**S5 — KPI scorecard.** Score your two main runs on the lesson-2 KPIs — presence (times you intervened), size (operations completed by agents), attempts (prompts before completion), streak (consecutive one-shot successes). Worst number → name the system change (template? trigger? environment? review?) that would move it.

**S6 — Transfer map.** For your real job: name your four PITER elements (tracker / trigger / environment / review surface) and the first three chores you'd hand off this week. Circle one. Dan: "take action on this now... the ROI here is insane."

## Pass criteria (all required)

- [ ] Zero application code typed by hand anywhere in the lab (template/config edits via Claude Code included)
- [ ] Checkpoint 0: HEALTHY health check against YOUR repo, no disler warning, ✅ comment posted
- [ ] Chore ADW end-to-end with zero mid-run intervention: live feed, spec-format branch name, committed plan, two `<agent>: <class>: <msg>` commits, complete PR
- [ ] Written PR audit exists (≥1 real inaccuracy found, or explicit "none found"), each item mapped to the template that owns the fix
- [ ] Feature ADW (JSONL) completed: pytest green on the branch; live verification — a `.jsonl` upload creates a table honoring `__` and `_0` from the issue
- [ ] ADW ID traced through all five surfaces without notes (comments → branch → agents/ → commits → PR)
- [ ] Cron trigger demonstrated; webhook demonstrated or its attempt explicitly documented
- [ ] All triggers/apps stopped at lab end (no listener left burning tokens)
- [ ] Closing oral check, no notes: PITER (with your own stack's mapping); the ADW definition; the classifier contract; why dangerous-skip was safe HERE and what would make it unsafe; "fix the system, not the issue" stated as policy

## Instructor / self-check notes

- **Most common stall:** remote still pointing at `disler/tac-4` — comments/PRs fail or land nowhere. The health check names it; students who skip Checkpoint 0 rediscover it the hard way. Fix: `git remote set-url origin <yours>` + push.
- **Second stall:** running `uv run adw_plan_build.py` from the repo root (Dan does it on camera at ~25:11) — `Failed to spawn`. It's a path, not a bug: `uv run adws/adw_plan_build.py <n>`.
- **Third stall:** `CLAUDE_CODE_PATH` unset when `claude` isn't on the subprocess PATH — health check's Claude Code test catches it; fix via `which claude`.
- **Cost surprise:** a feature ADW is ~8 agent invocations, one of which implements a whole feature. Budget accordingly; the chore run is the cheap rehearsal.
- **Cleanup between reruns matters:** cron/webhook both treat "latest comment == adw" as a trigger; stale listeners + leftover comments = surprise runs. `stop_apps.sh` + `kill_trigger_webhook.sh` are part of the lab, not appendix.
- **If the classifier returns 0** (contract working as designed): the issue body lacked a recognizable class — improve the issue, or extend the classes (S1). This failure is a feature; grade the diagnosis, not the rerun.
- **What this lab intentionally does NOT cover:** self-validating agents and review velocity (lesson 5), scaling/parallel ADWs, additional SDLC steps (later lessons). Deflect scope creep; the composable unit must stay crisp.

# TAC-6 Lab Spec — Let Your Agents Focus

**Scope rule:** every drill runs inside the course codebase only (`codebase/` → `tac/tac-6`; students: `git clone https://github.com/disler/tac-6.git`). You additionally need a GitHub repo YOU control — issues and PRs are the review system. No external repos, no new machinery beyond the lesson's tools.
**Prime directive (graded throughout):** you type **zero** lines of application code by hand. The misplaced button, the docs, the patch — all of it flows through an ADW or Claude Code. If your fingers touch `app/client/src/main.ts`, you've quit the lesson.
**Time box:** 90–120 minutes. Token cost: real, and higher than earlier labs — a full plan→build→review run plus a patch run and a document run, with `/review` on opus. Pay to play; budget for it or you'll stall mid-review and blame the tactic.

---

## 0 · Setup (15 min)

1. Clone the lesson repo: `git clone https://github.com/disler/tac-6.git && cd tac-6`
2. **Own the review surface:** create your own GitHub repo and point origin at it — `git remote remove origin && git remote add origin <your-repo> && git push -u origin main`. ADW review/patch/document need issues and PRs you control. `gh auth status` must be green.
3. Boot `claude`, run `/install`. Fill `.env` from `.env.sample`: `ANTHROPIC_API_KEY` (required — this is the headless billing path), `CLAUDE_CODE_PATH`, and `export GITHUB_REPO_URL`. Fill `app/server/.env` for the app's own NL→SQL key.
4. **Optional but demo-faithful:** set the four Cloudflare R2 vars (`CLOUDFLARE_ACCOUNT_ID` + R2 access key / secret / bucket) so review screenshots render as images on GitHub. Without them you get local file paths in comments — **that is not an error**; the uploader disables silently by design.
5. Sanity: `uv --version`; `/start`; the app serves at `localhost:5173`; run the five-users query to confirm the NL→SQL app works.

**Checkpoint 0:** you can state what makes review/patch/document different from plan/build/test — they need a repo you own, because their output IS issue comments and PR updates.

## 1 · Reproduce Dan — plan → build → review (25 min)

1. Create GitHub issue **"One Click Table Exports"** in Dan's shape: one-click CSV export for tables AND for query results; two new endpoints; the download button **directly LEFT of the tables' "x" icon** and **directly LEFT of the query results' "hide" button**; an appropriate download icon. (This mid-level detail is deliberate — placement is exactly what review will check.)
2. Fire it and hands off: `uv run adws/adw_plan_build_review.py <issue#>` (no adw-id — one gets created). "Our agents have now taken over this repository. We shouldn't be doing anything alongside them." Do NOT touch the repo while it runs.
3. Watch the machinery, don't interrupt it: `agents/{adw_id}/` fills with per-agent folders; `adw_state.json` carries adw_id / issue_number / branch_name / plan_file / issue_class; most of what scrolls by is the workflow REPORTING to the issue.

**Checkpoint 1:** the run posts a review comment. Read it as a contract, not prose — success flag, `review_summary` (standup-style), 1–5 numbered screenshots (R2 URLs or local paths), severity-grouped issues, and the raw JSON payload at the bottom.

## 2 · Read the review contract (15 min)

1. Open `.claude/commands/review.md` beside `adws/adw_modules/data_types.py`. Confirm the prompt's Output Structure and the `ReviewResult` / `ReviewIssue` pydantic types are the same shape; find the severity `Literal['skippable','tech_debt','blocker']`.
2. Answer in writing, no notes:
   - Which severities set `success=false`? Which get auto-resolved? *(blockers; both.)*
   - What caps the resolution loop? *(`MAX_REVIEW_RETRY_ATTEMPTS = 3`.)*
   - What happens if the review output fails to parse? *(a synthetic blocker-severity `ReviewResult` — the pipeline fails LOUD.)*
   - What does review use the `e2e/test_*.md` files for? *(navigation guides for WHERE to screenshot — only. It is not testing.)*
3. Spot the on-disk quirk: `review.md` has a `./claude/commands/e2e` path typo (missing the leading dot on `.claude`). Agents tolerate it because the intent is clear; a literal grep won't.

**Checkpoint 2:** you can recite the triage contract and the loud-failure behavior from memory.

## 3 · The patch loop, run out-loop (20 min)

1. Inspect the placement in the running app. If your agent nailed the button position, **plant Dan's deviation deliberately** (via Claude Code, not your editor) so you have a blocker to resolve — the point is to run the loop, not to get lucky.
2. Do NOT open the CSS. Comment on the issue with the literal keyword `adw_patch` + one line: "make sure the download button is just to the left of our hide button."
3. Run it like you're out-loop: `uv run adws/adw_patch.py <issue#> <adw-id>`. **Pass the issue number, not the PR number** — Dan fumbled 15-vs-14 on camera; the state echo in the comments is your check.
4. Verify the receipts: a plan under `specs/patch/patch-adw-{adw_id}-*.md`, the fix visible in the app, the commit, and the existing PR updated.

**Checkpoint 3 (write one sentence):** why run a whole workflow for a one-line CSS nudge you could hand-fix in 10 seconds? *(You're building the system that builds the system; a hand-fix leaves the system as fallible as before and isn't reproducible.)*

## 4 · Document, and watch the loop close (15 min)

1. On the SAME state: `uv run adws/adw_document.py <issue#> <adw-id>`.
2. Verify all three outputs: `app_docs/feature-{adw_id}-*.md`, copied images under `app_docs/assets/`, and a NEW entry appended to `.claude/commands/conditional_docs.md` (the committed file ships with exactly 4; yours makes 5).
3. Prove the loop: search `conditional_docs` — it's referenced in bug, chore, feature, patch, and prime. The planners read what your documenter just wrote.

**Checkpoint 4:** state the plan↔document cycle in one breath — document APPENDS the conditional entry; five planning prompts READ it; the next feature you plan pulls this doc only when its condition matches.

## 5 · Stretch drills (15–40 min, still zero hand-typing)

**S1 — The winning workflow.** Rerun the whole feature on a fresh issue with `adw_plan_build_test_review.py`. Note which phase catches your planted deviation — Dan: "the UI test very likely would have caught this... this is probably the winning workflow."
**S2 — Dan's named improvement (vision).** Via Claude Code, add "For every image you take, be sure to read it in during the review process" to `review.md`. Re-run `adw_review.py` on the same adw-id; compare `ReviewResult`s. Note where the fix does NOT belong: the global `.mcp.json --vision` ("this is outside of the ADW").
**S3 — Evals in practice.** Flip `/review` to a different model in `SLASH_COMMAND_MODEL_MAP`, `git checkout` the pre-review state, rerun, diff the two review JSONs. You just built an eval from git.
**S4 — One-one-one census.** `ls agents/{adw_id}/` after a full run; map every agent folder to its single slash command and one purpose. Confirm no agent ran two prompts.
**S5 — Trigger-drift hunt.** From `classify_adw.md` vs `data_types.ADWWorkflow` / `workflow_ops.AVAILABLE_ADW_WORKFLOWS`, prove why a webhook can never launch `adw_plan_build_review`. This is prompt↔code contract drift — exactly the failure class a review step exists to catch. (Optional: fix it via an `adw_patch` issue.)

## Pass criteria (all required)

- [ ] Zero application code typed by hand anywhere — every change flowed through an ADW or Claude Code
- [ ] `agents/{adw_id}/adw_state.json` shows adw_id / issue_number / branch_name / plan_file / issue_class populated across phases
- [ ] Review posted a JSON-backed report with 1–5 screenshots and severity-classified issues
- [ ] You can state which severities block and what caps the resolution loop (3), no notes
- [ ] A patch plan exists under `specs/patch/` and its fix is visible in the app + PR
- [ ] An `app_docs/feature-*.md` exists with copied assets AND `conditional_docs.md` gained its entry **agentically**, not by hand
- [ ] Oral, no notes: five SDLC questions; testing-vs-review distinction; three constraints + which two the tactic bypasses; why compact is a band-aid; ideal presence count and its two moments

## Instructor / self-check notes

- **Most common stall:** running `adw_review.py` / `adw_document.py` without the adw-id — they hard-exit demanding prior state. Remind students the ADW ID chains everything; copy it from the plan-phase output.
- **Second stall (Dan's own):** passing the PR number instead of the issue number to `adw_patch.py` (15 vs 14). Teach reading the state echo in the issue comments before blaming the tool.
- **"My screenshots are just file paths — it's broken."** No — the R2 uploader disables silently without the four Cloudflare vars. Local paths are the expected fallback; set the vars only if you want images to render on GitHub.
- **"Review passed but the button's wrong — the model failed."** Reframe it exactly as Dan does: blame the ADWs and skills, not the model. Two causes (test skipped; screenshots never read), one fix location (the review prompt). This is the lesson's most important teaching moment — don't let it slide into model-blaming.
- **Cost anxiety:** this lab spends more than TAC-1 (opus review + multiple full ADW runs). If the budget conversation surfaces, that IS the pay-to-play lesson arriving on schedule.
- **What this lab intentionally does NOT cover:** webhook/cron out-loop triggering at scale, dangerous-mode production ADWs, the fleet-of-agents endgame — those are lesson 7+. Keep the five-question SDLC crisp and deflect scope creep.

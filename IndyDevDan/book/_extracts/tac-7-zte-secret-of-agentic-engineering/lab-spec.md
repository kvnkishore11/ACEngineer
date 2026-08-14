# TAC-7 Lab Spec — ZTE: The Secret of Agentic Engineering

**Scope rule:** every drill runs inside the course codebase only (`codebase/` → `tac/tac-7`; students: `git clone https://github.com/disler/tac-7.git`). You additionally need a GitHub repo **you control** — the ADW pipeline IS issues, comments, and PRs. No external repos, no new machinery; every workflow in tac-7 is already `_iso`.
**Prime directive (graded throughout):** you type **zero** lines of application code by hand, AND you record your **presence** honestly for every run (how many times you touched it: prompt only = 1, prompt + review = 2, anything more = you were in-loop). The point of this lab is to *watch your own presence fall per problem class* — not to reach ZTE on run one.
**Time box:** 2–3 hours (the capstone lab). Token cost is real and the highest of the course: multiple full plan→build→test→review→document runs, one on `model_set heavy` (opus), plus a ship. Budget for it; running out mid-ship and blaming ZTE is the failure the pay-to-play lesson is designed to surface.

---

## 0 · Setup (20 min)

1. Clone the lesson repo: `git clone https://github.com/disler/tac-7.git && cd tac-7`. **Own the review surface:** create your own GitHub repo, `git remote remove origin && git remote add origin <your-repo> && git push -u origin main` (Dan does the equivalent on-video by resetting origin). `gh auth status` must be green.
2. Copy `.env.sample` → `.env`; set `ANTHROPIC_API_KEY` (the headless billing path) and `export GITHUB_REPO_URL`. Fill `app/server/.env` for the NL→SQL app's own key. **Optional but demo-faithful:** the four Cloudflare R2 vars so review screenshots render as images on the issue — without them you get local file paths, and **that is not an error** (the uploader disables silently).
3. Verify the toolchain: `claude --version`, `gh auth status`, `uv --version`, `bun --version`, `git --version` (must support worktrees).
4. Boot the app once yourself: `./scripts/start.sh` → `http://localhost:5173`; upload sample data; run one NL query; `./scripts/stop_apps.sh`. You need to know what "working" looks like before an agent ships to it.
5. Read `.claude/settings.json` and `adws/README.md`. Say out loud, before you run anything: what may a workflow do, and where will its evidence land? *(Answer you're building toward: `agents/<adw_id>/` for state + logs, `trees/<adw_id>/` for the isolated app copy, and the issue thread for every human-visible report.)*

**Checkpoint 0:** you can name the three places evidence lands and state why review/patch/ship need a repo you own — their output *is* issue comments, PR updates, and a merge.

## 1 · One issue → a production-shaped run (30 min)

1. File a GitHub issue in Dan's shape: `Add a footer showing the current table count. adw_sdlc_iso`. Run it manually first (webhook comes later): `cd adws && uv run adw_sdlc_iso.py <issue#>`. Hands off the repo the moment it starts.
2. While it runs, **prove the isolation with your own eyes:** `git worktree list` shows `trees/<adw_id>`; `cat trees/<adw_id>/.ports.env` shows the deterministic 9100-/9200-range pair; `cat agents/<adw_id>/adw_state.json` — name all **ten** fields aloud.
3. Jump into the agent's environment mid-run, like Dan: `code trees/<adw_id>` and watch the branch in the status bar. You are a guest in the agent's world, not a co-editor — do not touch files.
4. When it finishes, audit the evidence chain top-to-bottom on the issue: classification → state JSON → plan path → test summary → review summary **with ≥1 screenshot** → documentation → the PR. Open the PR diff.

**Checkpoint 1:** the issue thread reads as a complete paper trail, and you can point at where each of the ten state fields got populated. Record your presence for this run.

## 2 · Go in-loop on purpose (15 min)

1. This is the beat most students skip. In `claude`, run `/in_loop_review <branch-name>`; it fetches + checks out the branch, resets/starts the app, and opens `localhost` for hands-on inspection.
2. Exercise the footer feature yourself in the browser. Write one sentence: **what did your review catch?** (Be honest — on a clean run, likely nothing.)

**Checkpoint 2:** you can explain Dan's "in loop moving toward out loop" from experience — you *chose* to add a touchpoint, and you can say whether it added value. When it stops adding value for this class, that's the signal to drop it.

## 3 · Turn the compute knob (20 min)

1. New issue, heavier work: `Generate random rows for a selected table. adw_sdlc_iso model_set heavy`. Run it.
2. **Prove the knob actually turned:** find which model the implementor ran — `agents/<adw_id>/sdlc_implementor/raw_output.jsonl` (the `model` field) or the "Model Set" line in the issue thread. Confirm the implementor escalated to **opus** while classification/branch/test stayed on **sonnet**.

**Checkpoint 3:** you can state that `model_set` is one IDK read by `/classify_adw`, stored in `adw_state.json`, and that exactly **8 of 18** commands escalate on heavy — and you have on-disk evidence that yours did.

## 4 · Patch class vs full SDLC (15 min)

1. Small, surgical change: `Rename the Query button to Run. adw_patch_iso`. Run it.
2. Compare its footprint to the full SDLC runs: the plan lives under `specs/patch/`, and only a subset of phases ran (worktree → targeted patch plan → implement → PR — no full plan/test/review/document ceremony).

**Checkpoint 4 (one sentence):** why is the CSV/text-rename class routed to `patch` instead of `sdlc`? *(It's "just changing one thing" — a different composition of the same primitives, not a smaller SDLC. This is the secret in miniature.)*

## 5 · The ZTE ceremony and the uppercase interlock (30 min)

1. The low-stakes class ZTE is earned on first: `/chore adw_sdlc_ZTE_iso - change the background color to light green` (**ZTE uppercase**). Watch all six phases; note the initiation comment's auto-merge warning.
2. Confirm the merge landed **with no human step**: `git pull && git log --oneline -3` shows a merge commit `...via ADW Ship workflow`, and the app served from `main` shows the change.
3. **Prove the interlock is real, not a bug:** repeat with lowercase `adw_sdlc_zte_iso`. `/classify_adw` downgrades it to reviewed `adw_sdlc_iso` — no auto-merge. Typing lowercase and mistaking the working safety for a defect is the trap; you just disarmed it.

**Checkpoint 5:** you can list the ship gates in order (8 non-null state fields → three-way worktree validation → fetch/checkout main/pull/`merge --no-ff`/push, original branch restored on any failure) and explain what a lowercase `zte` does and why.

## 6 · Read the KPIs, close the loop, clean up (15 min)

1. Open `app_docs/agentic_kpis.md` after your runs. Recompute **attempts** (count entries in `all_adws`) and **streak** by hand and confirm the table agrees — the KPI command forces its arithmetic through `python -c` for exactly this reason.
2. **Clean up every run:** `./scripts/purge_tree.sh <adw_id>` for each; confirm `git worktree list` is clean. Each worktree is a full repo copy — skipping this is how a laptop fills up silently.

**Checkpoint 6:** your KPI table matches your hand-computed numbers, your worktrees are purged, and you can state the presence you recorded for each run in sections 1, 3, 4, and 5 — and which class you'd trust to ZTE next.

## 7 · Stretch drills (30–60 min, still zero hand-typing)

**S1 — Parallel proof.** File two independent chores; launch both ADWs back to back. Capture `git worktree list` and both `.ports.env` while both run; explain in one line why they can't collide (disjoint worktree, branch, ports, state).
**S2 — Port-collision drill.** Occupy a run's deterministic port (`python3 -m http.server 9107`) before launching; find in the logs where `find_next_available_ports` picked the fallback slot.
**S3 — Break ship's gate on purpose.** Run `adw_plan_iso` only, then `adw_ship_iso <issue#> <adw-id>`. Screenshot the missing-fields abort and read off exactly which of the eight required state fields were null.
**S4 — Docs-vs-code audit (technical-accuracy drill).** `adws/README.md` says ship "approves the PR and merges using squash." Read `adw_ship_iso.py` and write three sentences on what it *actually* does (`--no-ff` manual merge + push) and how `git log` would reveal the difference. Dan's narration matches the code, not the README.
**S5 — Latent-bug hunt.** Find the bug in `worktree_ops.remove_worktree` (a `shutil.rmtree` fallback with no `import shutil`); explain the failure path and why `validate_worktree`'s three-way check still keeps pipelines honest.
**S6 — E2E honesty check.** Prove from `adw_sdlc_zte_iso.py` that E2E is *always* skipped in SDLC/ZTE (`--skip-e2e`), then run it yourself standalone: `uv run adw_test_iso.py <issue#> <adw-id>` (no `--skip-e2e`) with Playwright MCP configured.
**S7 — Extend the review one step toward video.** `playwright-mcp-config.json` already records 1920×1080 video per run. After a review, locate the worktree's `videos/` dir and post the file path (or an uploaded URL) back to the issue — Dan's named "next most obvious" review upgrade.
**S8 — Wire the real trigger.** `uv run adw_triggers/trigger_webhook.py` (port 8001) + `scripts/expose_webhook.sh` (cloudflared) + a repo webhook for Issues/Issue-comments. File an issue from your phone and stay fully out of the loop. (Cron alternative: `trigger_cron.py`, 20s poll.)

## Pass criteria (all required)

- [ ] One `adw_sdlc_iso` run completed end-to-end from a GitHub issue with **zero hand-typed application code**; the issue thread shows classification, state, plan, test, review (with ≥1 screenshot), documentation, and a PR
- [ ] You can print `agents/<adw_id>/adw_state.json` and explain every one of the ten fields, including why ship refuses to run when any of its **eight** required fields is null
- [ ] A `model_set heavy` run demonstrably used **opus** for implementation while classification stayed on **sonnet** (evidence from `raw_output.jsonl` or the issue thread)
- [ ] One **uppercase-ZTE** run merged to main with a `via ADW Ship workflow` merge commit, AND one lowercase `zte` attempt visibly downgraded to reviewed SDLC
- [ ] Two ADW runs executed concurrently with disjoint worktrees, branches, and port pairs (evidence captured)
- [ ] `app_docs/agentic_kpis.md` was updated by your runs; you recomputed attempts/streak/presence by hand and they match
- [ ] All worktrees purged; `git worktree list` clean
- [ ] Oral, no notes: Tactic #7; the three velocity-scale levels with presence numbers; PITER→PITE; the secret (composable agentic primitives, SDLC = one arrangement)

## Instructor / self-check notes

- **The presence log is the real assessment.** A student who reaches ZTE on the background-color chore but records honest presence for the heavier runs has learned the lesson. A student who declares "ZTE for everything" has missed it entirely — push back exactly as Dan does at 32:37.
- **Most common stall:** running a dependent workflow (`adw_ship_iso`, `adw_review_iso`, `adw_document_iso`) without the adw-id — they hard-exit demanding prior state. The ADW ID chains everything; copy it from the plan-phase output.
- **"It merged to main automatically — is that safe?"** That IS ZTE, and it's gated (8-field state validation → three-way worktree check → `--no-ff` merge with branch-restore on failure → the uppercase interlock upstream). Have them count the gates before they panic; then discuss the *deterministic* controls current practice layers on top (branch protection, required CI, merge queues) — see `outdated-vs-current.md`.
- **"My screenshots are just file paths — it's broken."** No — the R2 uploader disables silently without the four Cloudflare vars. Local paths are the expected fallback.
- **Cost anxiety is on-schedule.** This lab spends the most in the course (opus on heavy + a full ship). If the budget conversation surfaces, that's the pay-to-play lesson arriving; ZTE's whole premise is that the layer's compounding payoff justifies the spend.
- **Don't let doc-blaming slide into tool-blaming.** S4 (README says squash, code does `--no-ff`) is the transferable habit: verify countable claims against source. Reward the student who reads `adw_ship_iso.py` over the one who quotes the README.
- **What this lab intentionally does NOT cover:** production-grade deploy guardrails (canaries, deterministic deploy checks, three-agent review fusion), the full fleet-of-agents endgame, and lesson 8's atoms-and-compositions map. Keep ZTE framed as a *targeted* North Star per problem class and deflect scope creep into "delete your whole SDLC."

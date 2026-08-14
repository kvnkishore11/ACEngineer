# TAC-8 Lab Spec — The Agentic Layer

**Scope rule:** every drill runs inside the course codebase only (`codebase/` → `tac/tac-8`; students: `git clone https://github.com/disler/tac-8.git`). Five sibling apps live inside it; you touch four (app3 is skipped on camera and here). No external repos.
**Prime directive (graded throughout):** you type **zero** lines of application code by hand. Agents write `main.sh`, the enhanced datasets, the prototypes, and the MCP server. You write only prompts, plans, tasks, and ADW glue. Even edits go through Claude Code.
**The one question (asked at every checkpoint):** *am I working on the agentic layer or in the application layer?* This lab is 100% agentic-layer work by construction — that is the point.
**Time box:** core reproduction 90–150 min; with stretch drills 3–5 hours. Token cost: real and non-trivial — app2 alone kicks off ~7 agents, app4 spawns detached prototypers. Pay to play; budget API funds or a plan before you start.
**Safety note (do not skip):** every tac-8 ADW runs Claude with `--dangerously-skip-permissions`. Stay inside the cloned repo, and **read each prompt/ADW file before you fire it**. This is a graded habit, not a formality.

---

## 0 · Setup (15 min)

1. Fresh directory for TAC codebases → `git clone https://github.com/disler/tac-8.git && cd tac-8` (catalog mirror: `tac/tac-8`).
2. Verify the toolbelt: `claude --version`, `uv --version`, `bun --version`, `git --version`. Windows: run everything inside WSL. Confirm `git worktree` works (`git worktree list`).
3. In `tac8_app1__agent_layer_primitives`: `cp .env.sample .env` and set `ANTHROPIC_API_KEY` (plus `CLAUDE_CODE_PATH` if `claude` isn't on your PATH).
4. **Read app1's `README.md` end to end.** Before running anything, answer in writing:
   - Name the **three MVAL pieces** and the **two layers**.
   - Which directory is the application layer here, and which directories form the ring?

**Checkpoint 0:** you can state, without looking, the two layers and the MVAL's three pieces (`adws/` + `.claude/commands/` + `specs/`). If you can't, re-read the README — this vocabulary carries the whole lesson.

## 1 · Reproduce Dan — app1, the primitives (30–40 min)

**A. In-loop warm-up.** Run `claude`, then `/prime`. Confirm it runs `git ls-files`, reads both READMEs, and reports. Then `/start`; confirm both hello-world outputs. *(This is the "set your agent up" baseline before any out-loop machinery.)*

**B. The gateway script.** `./adws/adw_prompt.py "list all files in the adws directory and a concise output of their purpose"` — Dan's exact run. Read the **Inputs** panel (ADW ID, agent `oneoff`, prompt, model, working dir, output path), then inspect all four files under `agents/<adw_id>/oneoff/`.

**Checkpoint 1B (write it down):** in one line each, what does `cc_raw_output.jsonl` vs `cc_raw_output.json` vs `cc_final_object.json` vs `custom_summary_output.json` contain? This observability tree is assumed by every later system.

**C. Slash, out of the loop.** `./adws/adw_slash_command.py /start` — same behavior as the in-loop `/start`, zero conversation. Note: you just ran a prompt with no chat window. That is "moving out the loop" in one command.

**D. Composed ADW (Dan's exact run).** `./adws/adw_chore_implement.py "create a .sh version of main in apps/*"`. Verify: `specs/chore-<id>-*.md` exists; `apps/main.sh` exists and runs (`sh apps/main.sh`); `agents/<adw_id>/` contains `planner/` + `builder/` + `workflow_summary.json`.

**Checkpoint 1D:** trace the plan path in one sentence — `/chore` writes `specs/chore-{id}-*.md` and *reports the path per its Report contract*; the script regex-extracts it; `/implement` receives it as its argument. Say why editing `/chore`'s Report section would break the pipeline. *(The deterministic script and the non-deterministic prompt are coupled by an explicit machine-parseable contract.)*

## 2 · Reproduce Dan — app2 Todone, multi-agent (30–45 min)

1. **Author a board.** Replace `tasks.md` content with your own `# ATL` list: two worktrees, three tasks each; mark the last task of one worktree `[⏰]`; tag one task `{opus}` and one `{sonnet, adw_plan_implement_update_task}`.
2. **Trigger once (dry first).** `./adws/adw_triggers/adw_trigger_cron_todone.py --once --dry-run` (read what WOULD happen), then `--once` for real. Watch worktree creation and `🟡` markers appear in `tasks.md`.
3. **Let it drain.** Run the trigger with defaults (5s poll). Verify `✅` lines carry real commit hashes (`git -C trees/<name> log --oneline`) and that the `⏰` task started **only after** everything above it in its worktree succeeded.
4. **Validation pass (Dan's move).** `code trees/<worktree>` — confirm the sparse checkout contains **only** `tac8_app2__multi_agent_todone`. Validate one agent's artifact by hand exactly like Dan validated `tweets_positive_only.csv` (open it, grep for what must NOT be there, confirm zero hits) — only then trust the `✅`.

**Checkpoint 2:** recite the tasks.md state machine — `[]` → `[🟡, adw_id]` → `[✅ commit_hash, adw_id]` | `[❌, adw_id] // Failed: reason`; `[⏰]` eligible only when every task above it is `✅` — and say what each tag does (`{opus}` = model tier, `{adw_plan_implement_update_task}` = workflow tier).

## 3 · Reproduce Dan — app4 prototyping, no Notion required (15–25 min)

1. Read `adw_trigger_cron_notion_tasks.py`'s **claim → route → spawn** flow and `.claude/commands/plan_uv_mcp.md`.
2. Run the specialized meta prompt in-loop: `claude` → `/plan_uv_mcp test0001 "Create a concise and minimal MCP server that provides system information: memory, cpu, disk"`. Read the generated `specs/plan-*-uv-mcp.md` and check it against the **Plan Format** contract (metadata, chore description, relevant files, step-by-step tasks, **validation commands**).
3. Confirm the routing table maps `{{prototype: uv_mcp}}` → `/plan_uv_mcp` and `continue - <prompt>` → HIL iteration (README §How It Works).

**Checkpoint 3:** map PITER onto app4 out loud — Prompt input = Notion card; Trigger = 15s cron; Environment = `trees/` worktrees; Review = board columns + live status. Name the mechanism that prevents two triggers grabbing the same card. *(Instant status flip to In progress + adw_id on claim.)*

## 4 · Reproduce Dan — app5 AEA, agents in the product (15–25 min)

1. `cp app/server/.env.sample app/server/.env` (add keys); `./scripts/start.sh`; in a second terminal `./scripts/aea_server_start.sh` (edit `CLAUDE_CODE_PATH` for your machine).
2. Open `http://localhost:5173`, press **Cmd+P**, run `/aea`; ask *"what is this codebase about?"*.
3. Open a **second** agent with `/aea` and give it a small UI change. Refresh the page and verify **both** agents reconnect with history.

**Checkpoint 4:** state the rule and its one exception — *one agent, one prompt, one purpose* (focused, reproducible, testable context windows); the AEA server is the sanctioned break because a conversational product agent needs continuity, achieved via a DB-persisted `cc_session_id` passed back with `--resume`.

## 5 · Stretch drills (still zero hand-typing)

- **S1 — New problem class (app1).** Copy `chore.md` to a new template meta prompt (e.g. `/bugfix` or `/docs`) with its own Plan Format; wire a composed ADW that chains it into `/implement`; run end to end. **Pass =** your team-specific standards appear in the generated plan (you templated a *class*, not an instance).
- **S2 — Blocked-chain proof (app2).** Craft a worktree where task 2 is `[⏰]` and task 1 is designed to FAIL (impossible validation). Run the trigger; verify task 2 never starts and task 1 records `[❌, adw_id] … // Failed: <reason>`.
- **S3 — Trigger surgery (app2).** Change the polling interval and `--max-tasks`, then add a third workflow tag of your own design routed in `delegate_task()` — one new `elif`, one new ADW script.
- **S4 — Real Notion factory (app4).** Create a Notion DB, wire `.mcp.json` from `.mcp.sample.json` + `NOTION_AGENTIC_TASK_TABLE_ID`, run the trigger with `--once`, and ship one `{{prototype: uv_script}}` task from board to Done.
- **S5 — AEA to your codebase (app5).** Point the AEA server pattern at any repo of yours — the server + patch script + dev console are self-contained; verify session resume across a **server restart**.
- **S6 — The audit (capstone).** For one real workweek, keep a two-column log answering the guiding question each work block. Compute your agentic-layer percentage; if under 50%, pick the problem class you did most often by hand and template it.

## Pass criteria (all required)

- [ ] Zero application code typed by hand anywhere in the lab (agents wrote `main.sh`, datasets, prototypes; you wrote prompts, plans, tasks, ADW glue)
- [ ] `agents/<adw_id>/` observability tree produced **and explained**: you can say what the JSONL stream, JSON array, final object, and custom summary each contain
- [ ] `adw_chore_implement.py` run complete: plan file in `specs/`, `apps/main.sh` exists and runs, `workflow_summary.json` shows both phases succeeded
- [ ] app2 board drained: every task reached `✅` (with a verifiable commit hash in its worktree) or `❌` (with reason); the `⏰` dependency provably held; sparse checkout verified (worktree contains only the app2 directory)
- [ ] app4: a Plan-Format-conformant `specs/plan-*-uv-mcp.md` generated from one concise prompt (in-loop acceptable; Notion path is stretch)
- [ ] app5: two concurrent AEA agents — one Q&A, one code change — both surviving a page refresh via session resume
- [ ] Closing oral check, no notes: the two layers and the ≥50% rule; the MVAL's three pieces; the tasks.md state machine incl. tags; PITER→PITE and its prerequisite; the one-agent rule + its exception; and the final guiding question with its **three** acceptable application-layer reasons

## Instructor / self-check notes

- **Most common stall — the `⏰` dependency looks broken.** A blocked task legitimately does nothing until everything above it in its worktree is `✅`. Students read "stuck" as "failed." Fix: check the worktree above it first; a `❌` above blocks forever by design (that's S2's whole lesson).
- **Second stall — reading instead of running.** The lesson's payoff is watching a trigger pick up work you never dispatched ("I'm not doing this, by the way"). A student who only reads the code will conclude multi-agent is "just cron." Make them run the trigger and *watch the markers change*.
- **Third stall — mixing layers.** Agent scripts placed inside `apps/`, or an agent writing to `main` without a worktree, then parallel edits collide and the student blames multi-agent. The separation IS the feature.
- **Cost anxiety is a real teaching moment.** app2 fires ~7 agents; app4 spawns detached prototypers. If a student can't afford a full drain, cap with `--max-tasks` / `--once` and still hit every checkpoint. The budget conversation (pay to play, parabolic ROI) is on-topic, not a distraction.
- **The `--dangerously-skip-permissions` habit.** Fine inside these throwaway repos; call out explicitly that it is NOT the pattern for real code (see `outdated-vs-current.md` §3). The isolation instinct (worktrees) is what transfers; the bypass flag does not.
- **What this lab intentionally does NOT cover:** app3 (skipped on camera), a from-scratch agentic layer, and production hardening (permission modes, the Agent SDK, native background agents). Deflect scope creep — the invariants to internalize are isolation, composability, observability, and feedback loops, not Dan's exact directory names.

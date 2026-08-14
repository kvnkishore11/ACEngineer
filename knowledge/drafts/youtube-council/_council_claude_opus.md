# Becoming IndyDevDan: A Personal Operating Plan

*Claude Opus — strategy council seat. Written for kvnkishore, grounded in the corpus already on disk under `IndyDevDan/`.*

## 1. Thesis

"Think/create/write like Dan" is not a coding-speed upgrade — it is a **change of job**. You stop being the person who types diffs and become the **commander of compute**: the engineer who plans work to a spec, dispatches a stack of agents at it, and reviews outputs instead of keystrokes. "Thinking like Dan" means you reason in **closed loops and control surfaces** (a hook, a skill, a verifier, a task queue), not files and functions. "Creating like Dan" means every codebase you author is an **agent operating system** — a repo an agent can run end-to-end from one command while you are AFK. "Writing like Dan" means each repo teaches or exposes **exactly one** control surface, in the canonical `CLAUDE.md + .claude/ + ai_docs/ + specs/ + justfile` shape you can see repeated across `youtube/_repos/disler__*`. The models are swappable; the **harness is the asset**.

## 2. Anti-goals (what NOT to copy)

- **Thumbnail hype / model-of-the-week identity.** `yt-05` (GPT-5), `yt-14` (Big-3), `yt-41` (Gemma/MLX), `yt-51` (GLM vs MiniMax) are *content* about swappable backends. Learn the harness they run inside; do not make "which model won" your personality.
- **Bake-off busywork.** You have `disler__live-bench` and `disler__nano-agent` — benchmarking is a tool, not a curriculum. One bake-off per quarter, max.
- **Cargo-cult repo names.** Naming something `the-library` or `nano-agent` without the meta-skill/loop behind it is theater. Structure follows a working loop, never the reverse.
- **Rebranding your existing scripts as "the agentic layer."** TAC-8 is a real architecture, not a label for cron jobs. `yt-53` ("forget loop engineering") is Dan explicitly rejecting exactly this move.
- **Binging all 53 videos.** Consumption is the trap. Transfer beats views.
- **Inventing a product (PiCanvas) as the lab.** This phase builds the operating *system*, not an app. Labs run on course codebases and `disler/*` repos only.

## 3. Mental model — Dan's operating system (three layers)

Leverage flows **downward**: you author the code layer so the agent layer can operate it while you sleep.

| Layer | Who/what | Your job here | Corpus anchor |
|---|---|---|---|
| **Engineer** (you) | Judgment only: plan, ZTE cut/keep calls, taste, verification criteria | Decide *what* good looks like; never hand-type what an agent can | `tac-3`, `tac-7-zte-secret-of-agentic-engineering` |
| **Agent** | Hermes, Claude Code (Opus), Codex, local Gemma/MLX — orchestrated as CEO → lead → worker → verifier → UI | Orchestrate and route; close loops between agents | `ma-1-ceo-agents` … `ma-4-verifier-agent`, `ah-4-multi-agent-orchestration-the-o-agent` |
| **Code** | The repo as agent OS: `CLAUDE.md`, `.claude/{commands,agents,hooks,skills}`, `ai_docs/`, `specs/`, `justfile`, observability | Author the control surfaces the agent layer operates | `youtube/_repos/disler__claude-code-hooks-mastery`, `…__the-verifier-agent` |

The **TAC stack** is the operating discipline that binds the layers: *planned success* (TAC-3) → *AFK agents* (TAC-4) → *close the loops* (TAC-5) → *focus* (TAC-6) → *ZTE* (TAC-7) → *agentic layer* (TAC-8), all sitting on the *12 leverage points* (TAC-2). Read this as a **stack you install into your day**, not a playlist.

## 4. Curriculum path for THIS user (Phases 0–4, 8 weeks)

You are **not a beginner**. `IndyDevDan/book/` proves it: you already built a fan-out pipeline (`book/_orchestration/`, `book/.claude/`, `book/_extracts/<module>/`) that turns course modules into HTML chapters. That is ADW competence. So we skip "hello agentic coding" as *learning* and use it as *reference*. Daily cadence: **~90 min** = one study ritual (§5) + one build rep + log metrics.

- **Phase 0 — Instrument & baseline (Days 1–3).** Stand up your canonical template repo and metrics ledger. Wire observability + hooks from `yt-01` and `disler__claude-code-hooks-mastery`. You can't improve AFK hours you don't measure.
- **Phase 1 — Tactics stack (Week 1–2).** Run `tac-1` … `tac-8` as **drills, not watches**. Each module must produce *one change to your operating loop* (a hook, a spec habit, a ZTE rule). Anchor codebases: `tac-3-success-is-planned/codebase/`, `tac-5-close-the-loops/codebase/`, `tac-8-the-agentic-layer/codebase/`.
- **Phase 2 — Context & prompt formats (Week 3–4).** `ah-1-rd-framework-context-window-mastery`, `ah-2-seven-levels-agentic-prompt-formats`. Rebuild your `.claude/commands/` and skills to the highest *useful* format level. Context is your primary leverage; treat the window as a budget.
- **Phase 3 — Specialized & multi-agent (Week 5–6).** `ah-3-building-domain-specific-agents`, `ah-5-agent-experts`, then `ma-1-ceo-agents` → `ma-4-verifier-agent`. Build one domain agent and one verifier; wire CEO→lead→worker routing over your book pipeline.
- **Phase 4 — Agentic layer & software factory (Week 7–8).** `tac-8`, `ah-6-building-agentic-layers`, plus `yt-25` (codebase singularity), `yt-48` (Cloudflare software factory), `yt-53` (ADW ≠ loop engineering). Turn `IndyDevDan/book/` into a genuinely agent-run factory: agents open, verify, and merge chapter work.

## 5. How to study a Dan codebase (repeatable 60–90 min ritual)

Operate agents *around* the repo. Do **not** read every file — that is the archaeology trap the brief warns against.

1. **(5m) Frame.** Read `README.md` + `CLAUDE.md` only. Write one sentence: *"This repo's ONE control surface is ___."* If you can't, it's the wrong repo for today.
2. **(10m) Map the OS.** `ls` the `.claude/{commands,agents,hooks,skills}`, `ai_docs/`, `specs/`, `justfile`. Identify the single entry command.
3. **(10m) Delegate the read.** Point Opus **and** Codex at it in parallel: *"Summarize this repo's one control surface and the loop it closes. Output a 15-line spec."* You review both; you do not read source.
4. **(15m) Run the loop once.** Execute the `justfile` target / primary slash command. Watch it work — this is the point.
5. **(20m) Fork one surface.** Copy *only* that control surface into your template repo (§6). Strip everything else. Make it run.
6. **(10m) Transfer note.** 5 lines to your ledger: which tactic, what it replaces in *your* loop, which metric it moves. A study session with no wired change **did not happen**.
7. **(10m) Verify.** Run a verifier agent over your fork: does it actually run from one command?

## 6. How to *author* a Dan-style codebase (checklist + minimum viable agent OS)

The canonical shape is not aesthetic — it's what lets an agent operate the repo unattended. It recurs in `disler__claude-code-hooks-mastery` and `disler__the-verifier-agent`:

```
your-repo/
  README.md            # teaches the ONE surface; images/ of it running
  CLAUDE.md            # operating instructions FOR the agent
  .claude/
    commands/          # entry loops (slash commands) — the "how to run"
    agents/            # specialized subagents
    hooks/             # close-the-loop enforcement: lint / verify / notify
    skills/            # packaged, distributable capabilities
  ai_docs/             # curated context the agent reads (not the whole internet)
  specs/               # plans that drive AFK runs
  justfile             # ONE command runs the whole loop
```

**Ship checklist — a repo is Dan-shaped when:**

- [ ] It exposes **exactly one** control surface (name it in the README's first line).
- [ ] **One command** (`just <x>` or `/command`) runs the whole loop.
- [ ] The loop is **closed** — a hook or verifier agent gates success, so it can *fail loud* (per your global `CLAUDE.md`).
- [ ] It is **AFK-runnable**: queue a spec, walk away, come back to a verified result.
- [ ] `CLAUDE.md` + `ai_docs/` give an agent enough context to operate it cold.
- [ ] It is **small** — if a newcomer can't grasp the surface in 5 minutes, it's teaching two things.

## 7. First 4 personal projects (one control surface each)

Each is weekend-scoped, canonical-shaped, and runs on corpus you own — no invented product.

1. **`hooks-obs-starter`** — Fork `yt-01`/`disler__claude-code-hooks-multi-agent-observability` + `hooks-mastery`. Wire every agent action to a local dashboard. **Surface: observability.** *Done = you can see agent actions live from one `just` target.*
2. **`verify-gate`** — A verifier agent (`ma-4-verifier-agent/codebase/`, `disler__the-verifier-agent`) that gates PRs in `IndyDevDan/book/`. **Surface: close-the-loop / verification.** *Done = no book chapter merges without an agent's pass.*
3. **`plan-skill`** — Rebuild TAC-3 *success-is-planned* + `yt-50` (plan skill for Fable-5) as a reusable `/plan` that emits `specs/` your agents run AFK. **Surface: planned success.** *Done = one prompt → a spec your agents execute unattended.*
4. **`my-library`** — Package projects 2 and 3 for distribution via the meta-skill pattern in `yt-36`/`disler__the-library` (`SKILL.md` + `library.yaml` + `cookbook/`). **Surface: skill distribution / agentic layer.** *Done = you install your own skills into a fresh repo in one command.*

## 8. Weekly operating loop (Mon–Sun)

Built around your **Hermes weekly YT cron** (`youtube/weekly_update.py`, state in `youtube/_weekly_last_run.json`) and the 18 course modules.

- **Mon — Intake.** Cron drops the new `yt-NN` + attached codebase. Run a **20-min** study ritual (§5) on *that codebase only*. Extract one tactic to the ledger.
- **Tue — Module drill.** One TAC/AH/MA module (rotate through all 18). Produce one wired change.
- **Wed — Build rep.** Advance the current project of the four in §7.
- **Thu — Fork day.** Pull one control surface from a `youtube/_repos/disler__*` repo into your template.
- **Fri — Verifier day.** Run `verify-gate` over the week's work. Close every loop you opened.
- **Sat — AFK day.** Queue a `specs/` file; let Opus + Codex (+ Gemma for cheap passes) run. Review **outputs, not keystrokes**. Log AFK hours.
- **Sun — Ledger.** Metrics review (§9); pick next week's module + project. 30 min, no building.

## 9. Metrics of becoming like Dan (not vanity)

Track in `_lab/LEDGER.md`. None of these is "videos watched."

| Metric | Definition | Direction |
|---|---|---|
| **AFK hours** | Agent-hours run with you away from the keyboard / week | ↑ |
| **Closed loops** | Count of self-verifying loops (hook- or verifier-gated) across your repos | ↑ |
| **Agent-operable surfaces** | # of your repos an agent runs end-to-end from one command | ↑ |
| **Transfer ratio** | Tactics *wired into your loop* ÷ tactics noted | → 1.0 |
| **Keystroke share** | % of shipped diff you typed by hand | ↓ |
| **Time-to-first-agent-action** | Minutes from opening a new codebase to an agent operating it | ↓ |

## 10. Risks & failure modes

- **Content binging** (53 videos in, 0 tactics out). *Guard:* every study session must produce a ledger row with a wired change, or it didn't count.
- **Model-bake-off rabbit hole.** *Guard:* models are backends; if a week's work is "compare models," it's a wasted week unless it changes routing in a real loop.
- **Cargo-culting structure.** *Guard:* the ship checklist — one command closes one loop — or it doesn't ship.
- **Building a product instead of the OS.** *Guard:* Phase-0–4 output is *operating surfaces*, not an app. Re-read the brief's constraint.
- **Over-engineering the agent OS** (10 agents, nothing shipped). *Guard:* minimum viable agent OS; small beats clever.
- **Silent AFK failure.** Agents that run unattended without a gate violate your own *fail loud* rule. *Guard:* no AFK loop ships without a verifier gate (project 2).

## 11. Immediate next 7 days (day-by-day)

- **Day 1 — Baseline.** Create `IndyDevDan/_lab/` as the canonical template (§6): `README.md`, `CLAUDE.md`, `.claude/{commands,agents,hooks,skills}`, `ai_docs/`, `specs/`, `justfile`. Create `_lab/LEDGER.md` and record today's **keystroke share** honestly.
- **Day 2 — Observability.** Study ritual on `yt-01-.../codebase/` + `disler__claude-code-hooks-mastery`. Fork the observability hook into `_lab`. Dashboard runs from one command. *(Project 1 started.)*
- **Day 3 — Plan.** TAC-3 drill (`tac-3-success-is-planned/`). Turn one real task into `_lab/specs/`. Run it AFK once; log the AFK minutes.
- **Day 4 — Verify.** Study `ma-4-verifier-agent/` + `disler__the-verifier-agent`. Wire a verifier as a hook gate on `_lab`. *(Project 2 started.)*
- **Day 5 — Prompt formats.** `ah-2-seven-levels-agentic-prompt-formats`. Rewrite your best slash command up to the highest *useful* format level; measure the difference.
- **Day 6 — AFK rep.** Saturday: queue a `specs/` file, let Opus + Codex run, review outputs only. Log AFK hours + closed loops.
- **Day 7 — Ledger.** Review metrics. Draft `plan-skill` (project 3) from what worked. Set Week-2 module (`ah-1-rd-framework`) and next project. Update `_council_*` if the plan needs sharpening.

---

**One line to keep:** *You are not learning to code faster — you are learning to not code. Author surfaces, dispatch agents, verify loops, repeat.*

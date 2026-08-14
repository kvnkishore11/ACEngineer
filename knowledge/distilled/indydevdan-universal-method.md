# IndyDevDan’s Universal Method
## The Agent Layer Algorithm (ALA)

**One procedure. Every problem class. No ad-hoc religion.**

TAC 1–8 collapse into this algorithm. Tactics are *invariants* and *steps*, not separate systems.  
The secret (TAC-7): engineering is **composable agentic primitives**, not “the SDLC.”  
The meta-rule (TAC-8): **≥50% of time on the agentic layer** (prompts + plans + ADWs).  
Daily question: *Am I working on the agentic layer or in the application layer?*

**KPIs (always):** Size↑ · Attempts↓ · Streak↑ · Presence↓

**Invariants (never violate):**
1. **Stop coding** — agents write application code; you write the system that writes.
2. **Core Four** — every agent run has deliberate Context, Model, Prompt, Tools.
3. **One agent · one prompt · one purpose** — fresh agent per phase; no context pollution.
4. **Plan is the prompt** — high-impact work is a written plan in `specs/`.
5. **Request → Validate → Resolve** — no “done” without a checkable loop.
6. **Fix the system, not the symptom** — failure upgrades templates/ADWs, not only the app.
7. **3× rule** — once novel, twice maybe, three times → template/command/ADW.
8. **R&D** — manage context only by **Reduce** or **Delegate**.

---

## Part A — Universal Method (any work unit)

**Name: Classify → Plan → Build → Prove → Promote (CPBPP)**

Applies to: chore, bug, feature, decision, research, refactor, ops task.

### Step 0 — Gate (10 seconds)
- [ ] Can an agent do this with the right Core Four? → **Yes (default).**  
- [ ] Only you do: novel strategy, irreversible prod risk, undefined success.  
- [ ] Write one sentence: **Done when ____ (observable).**

**Fail:** No done-when → stop. Don’t start.

### Step 1 — CLASSIFY
Pick **exactly one** problem class:

| Class | Template | Signal |
|-------|----------|--------|
| **chore** | `/chore` | Cleanup, logging, rename, docs, config |
| **bug** | `/bug` | Broken behavior; needs repro + root cause |
| **feature** | `/feature` | New user-visible behavior |
| **patch** | `/patch` | Surgical fix to one failed review/test |
| **research** | ad-hoc plan | Answer/decision; output = memo/notes, not code |
| **decision** | brief→memo (MA-1) | Strategy; adversarial multi-perspective |

- [ ] Class chosen.  
- [ ] Size estimate: S (≤15m) / M (≤1h) / L (>1h).  
- [ ] L → split into S/M units (one purpose each).

**Branch:** No template for this class yet → Step 1b: run once **in-loop**, log steps, then Step 7 promotes.

### Step 2 — LEVERAGE CHECK (agent’s perspective)
Before any agent runs, verify the agent can succeed:

- [ ] **Stdout/logs** exist for the touched surface (no swallowed errors).  
- [ ] **Types/names/entry points** legible; files <~1000 lines preferred.  
- [ ] **Validation commands** known (lint, test, build, e2e).  
- [ ] **Minimal context**: prime or plan path — not dump whole repo.  
- [ ] **Model**: plan/review = heavy; implement/simple = base.  
- [ ] **Tools**: only what the purpose needs (MCP on demand).

**Fail:** Agent is blind → fix leverage (logging, types, tests, docs) *before* the work unit. That fix is itself a chore through CPBPP.

### Step 3 — PLAN (template meta-prompt → `specs/`)
- [ ] Fresh agent.  
- [ ] Run template: `/chore|bug|feature|patch "<request>"` (or research brief).  
- [ ] Plan written under `specs/` with **mandatory sections**:
  - Description / problem  
  - Relevant files (+ New Files if any)  
  - Step-by-step tasks (ordered)  
  - **Validation commands** (copy-pasteable)  
  - Notes / risks  
- [ ] Human scan (≤5 min): would *you* execute this top-to-bottom? Gaps → edit plan or re-plan, not babble-prompt.

**Fail:** Plan vague or unvalidated → reject plan. Attempts+1. Fix template if plan shape is wrong.

### Step 4 — BUILD (higher-order implement)
- [ ] **New** fresh agent (new terminal / new ADW step).  
- [ ] `/implement specs/<plan>.md` (or ADW builder).  
- [ ] Agent executes steps **in order**.  
- [ ] Agent runs **all** validation commands; on fail → fix → **re-run every validation top-to-bottom**.  
- [ ] Report: summary + `git diff --stat`.

**Fail:** Loop doesn’t close in ≤N retries (default 3) → stop agent. Human diagnoses **which leverage/template** failed. Do not keep chatting the same polluted context. `/clear` + re-prime, or fix system.

### Step 5 — PROVE (review answers “is this what we asked?”)
Not the same as “tests pass.”

- [ ] Diff vs plan: every plan step done or explicitly waived.  
- [ ] If UI: screenshot (or e2e) **read back** into context.  
- [ ] Issues classed: `skippable` | `tech_debt` | `blocker`.  
- [ ] Blockers → `/patch` → Step 4 again (same ADW id if chained).  
- [ ] Optional: verifier (MA-4) — atomic claims, evidence not assertion.

**Fail:** Blocker after max patches → Presence required; log miss into template/review prompt.

### Step 6 — CAPTURE (close the knowledge loop)
- [ ] Commit specs + code (or PR).  
- [ ] If user-facing or multi-session: `/document` → `app_docs/` + update `conditional_docs.md`.  
- [ ] Score KPIs for this unit: Size, Attempts, Streak, Presence (1=prompt only … high=babysitting).

### Step 7 — PROMOTE (thicken the agentic layer)
Answer: *what should never be manual again?*

| Trigger | Action |
|---------|--------|
| Same manual step **3×** | New `.claude/commands/*.md` |
| Plan→build repeated | `adw_*` chain (plan then implement) |
| Validation ritual stable | Bake Validation Commands into templates; add `/test` |
| UI verify by hand | e2e prompt or Playwright MCP loop |
| Review catches same miss | Fix `/review` (e.g. must read images) |
| Streak ≥~5–10 one-shots on class | Allow **ZTE** for that class only (PITE: drop Review) |
| Domain complexity high-risk | Agent expert (expertise.yaml + self-improve) |
| Parallel collisions | git worktrees (`trees/`) |
| Many agents / many tasks | Orchestrator (CRUD agents) or trigger (issue/cron) |

- [ ] One concrete file changed in **agentic layer** when a gap appeared.  
- [ ] Guiding question answered for the session.

**Exit:** Work unit closed when Prove is green **and** any system gap is filed as the next chore (or fixed now if 3×).

---

## Part B — Bootstrap Method (empty repo → MVAL)

**Goal:** Minimum Viable Agentic Layer in one sitting.

### B1. Scaffold (files only, zero app logic)
```
repo/
├── apps/                    # application layer only
├── specs/                   # plans (generated)
├── adws/
│   ├── adw_modules/agent.py # wraps `claude -p`
│   ├── adw_prompt.py        # GATEWAY
│   ├── adw_slash_command.py
│   └── adw_chore_implement.py
├── agents/                  # runtime logs per run id
├── .claude/commands/
│   ├── prime.md
│   ├── start.md
│   ├── chore.md
│   ├── feature.md
│   └── implement.md
└── README.md
```
- [ ] Agentic dirs **never** mixed into `apps/`.

### B2. First commands (in this order)
1. **`prime.md`** — Run: `git ls-files` · Read: README · Report: summary.  
2. **`start.md`** — how to boot/run the app (exact commands).  
3. **`chore.md`** — template meta-prompt → Plan Format → `specs/chore-{id}-{name}.md` with Validation Commands.  
4. **`feature.md`** — same skeleton; user story + phases if needed.  
5. **`implement.md`** — HOP: read plan → think hard → implement → validate → report + `git diff --stat`.

### B3. First ADWs
1. **`adw_prompt.py`** (gateway): `claude -p "<prompt>" --output-format stream-json` → log under `agents/<id>/`.  
2. **`adw_slash_command.py`**: run `/prime` or `/start` headlessly.  
3. **`adw_chore_implement.py`**: agent1 `/chore` → parse plan path → agent2 `/implement <path>` (two fresh agents).

### B4. First validation (definition of MVAL done)
- [ ] `uv run adws/adw_prompt.py "list files in adws/ and one-line purpose each"` succeeds + logs exist.  
- [ ] In-loop: `/prime` then `/start` work.  
- [ ] One **real** backlog chore: `uv run adws/adw_chore_implement.py "<chore>"`.  
- [ ] Plan in `specs/`, code change, validations green, you typed **zero** application code.  
- [ ] Write % of day agentic vs application.

### B5. App-legibility minimum (if agents fail)
- [ ] Exceptions/success log to stdout.  
- [ ] One test or compile command.  
- [ ] Clear entrypoint + README.

---

## Part C — Growth Method (layer thickens)

Climb **only the next grade**. Don’t skip to orchestrators.

| When this happens | Add this |
|-------------------|----------|
| Boot context bloated | Trim CLAUDE.md; MCP on demand; `/prime` over memory |
| Same chore/bug/feature shape 3× | Dedicated template (`/bug` with RCA, `/feature` with AC) |
| You re-verify by hand | Validation section + closed-loop prompt |
| UI clicks are the real test | Playwright MCP + e2e markdown tests |
| Plan-build works but you babysit | Issue/file/cron **trigger** + PR as review surface (PITER) |
| Pipeline steps tangle in one agent | Split ADWs: plan, build, test, review, document; chain by ADW id |
| Agents collide on disk | Worktrees under `trees/` + per-tree ports |
| Review misses intent | `/review` + severity classes + patch loop |
| Docs never feed next plans | `app_docs/` + `conditional_docs.md` in templates |
| Domain keeps getting relearned | Expert: `expertise.yaml` + question/plan/self-improve |
| Single terminal is the bottleneck | O-agent: create/command/status/delete |
| Claims ≠ truth | Verifier agent (atomic claims, read-only tools) |
| Class one-shots for a streak | ZTE ship for **that class only** (PITE) |

**Growth rule:** After every failure, change **one** agentic-layer file. After every third success of the same shape, **promote** it (Step 7).

---

## Part D — Daily Operating Method (same every day)

### Morning (15–25 min)
- [ ] Guiding question intent: today **≥50% agentic layer**.  
- [ ] Pick **problem class** queue: chores first, then bugs, then features.  
- [ ] Health: env keys, `claude`, tests/start still work (or `health_check`).  
- [ ] Open/create issues or task lines as **prompt inputs** (P of PITER).  
- [ ] Fire **out-loop** work first (ADW/issue); save in-loop for hard/novel only.

### During
- [ ] For each unit: **CPBPP** — no freeform coding session.  
- [ ] Fresh agent per phase. Prefer `claude -p` / ADW over long chats.  
- [ ] If agent fails: give it stdout/tests first; dig in only if agent fails twice.  
- [ ] Context unhealthy → `/clear` + `/prime` (never trust `/compact` as strategy).  
- [ ] Log KPI ticks (attempts, presence) per unit.  
- [ ] Midday: *Am I on agentic or application layer?* Rebalance.

### Evening (10–15 min)
- [ ] Merge/review only PRs that need human R (Presence endpoint).  
- [ ] Streak check: any class ready to loosen review / ZTE?  
- [ ] 3× list: what repeated → new command tomorrow.  
- [ ] One template/ADW improvement committed.  
- [ ] KPI day score: Size / Attempts / Streak / Presence.  
- [ ] Tomorrow’s first issue pre-written as a prompt.

**Weekly:** parallelize (worktrees), expert self-improve on hottest domain, kill dead prompts.

---

## Part E — Decision table

| Situation | Method step / artifact |
|-----------|------------------------|
| Empty or greenfield repo | Part B full bootstrap |
| Tiny cleanup | CLASSIFY=chore → `/chore` → `/implement` |
| Broken behavior | `/bug` (repro + RCA) → implement → tests |
| New capability | `/feature` plan (AC + phases) → implement → e2e if UI |
| Review found one miss | `/patch` only — no full feature replan |
| “Just ask Claude in chat” | Reject if class has template; force plan path |
| Agent needs codebase map | `/prime` (or scoped `prime_*`) then task |
| Context fat / confused | Reduce MCP/memory; Delegate sub-agent; reset+prime |
| Same task 3rd time | Promote to command (Step 7) |
| Want AFK | PITER: issue/board + trigger + env + PR review |
| Multiple independent issues | Worktrees + parallel ADWs |
| “Does it work?” | Test step (validators) |
| “Is it what we asked?” | Review step (diff+proof) |
| “How does it work later?” | Document + conditional_docs |
| Chore streak flawless | ZTE workflow for chores only |
| High-risk domain (billing/DB) | Agent expert before more freestyle |
| Strategic fork (not code) | Brief → multi-agent memo (MA-1) |
| Don’t trust builder claims | Verifier / atomic claims |
| Too many agents to drive | O-agent CRUD + observability |
| Model too weak on plan | `model_set: heavy` / Opus on plan+review |
| You’re typing app code | Stop. Return Step 0. You’re on wrong layer |

---

## Part F — Anti-methods (what breaks the system)

1. **Hands on application code as default** — Presence stuck high; layer never compounds.  
2. **In-loop forever** — chat babysitting instead of plans/ADWs.  
3. **One god agent / one mega prompt** — context pollution; violates one-one-one.  
4. **No plan file** — “vibe implement”; unreproducible, unimprovable.  
5. **No validation commands** — green theater; can’t close loops.  
6. **Swallow errors / silent failures** — blind agents (leverage #5 dead).  
7. **Fix the bug, not the template** — same failure forever.  
8. **3× ignored** — perpetual manual tax.  
9. **Tangled layers** — app code inside `adws/` or prompts inside `apps/`.  
10. **Always-on fat CLAUDE.md + all MCPs** — context rot from boot.  
11. **Trust `/compact`** — unknown window; prefer clear+prime.  
12. **Outsource your agentic pipeline** generically — not *your* templates on *your* classes.  
13. **ZTE before streak** — auto-merge without proven class competence.  
14. **Review without proof** — screenshots not read; claims as evidence.  
15. **Parallel without isolation** — worktree-less collisions.  
16. **Edit expertise.yaml by hand** — teach self-improve instead.  
17. **Orchestrator does the work** — must only create/command/observe/delete.  
18. **Measuring nothing** — no KPI → no improvement.  
19. **Problem instances over problem classes** — one-offs that never template.  
20. **Application-layer day** — majority time in app code = wrong game.

---

## Pocket card (print this)

```
DONE-WHEN? → CLASSIFY → LEVERAGE → PLAN(specs) → FRESH BUILD →
VALIDATE ALL → PROVE → CAPTURE → PROMOTE(3×/streak)
IF FAIL: fix system (template/ADW/leverage), not just app
LAYER ≥ 50% · Size↑ Attempts↓ Streak↑ Presence↓
```

**That’s the whole method.** Everything else is a thicker ring of the same loop.

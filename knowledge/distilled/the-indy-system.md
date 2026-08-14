# THE INDY SYSTEM
## One method. Every problem. Follow the steps → get the answer.

> Like JEE Physics: **one fixed method** for a class of problems — not a different trick for every question.
>
> You do not invent a new approach for each ticket. You run **CPBPP**. Every time.

---

## The pocket card (memorize this)

```
0  DONE-WHEN?     (observable proof of success)
1  CLASSIFY       (chore | bug | feature | patch | …)
2  LEVERAGE       (can the agent see? stdout/types/context)
3  PLAN           (fresh agent → specs/*.md with Validation Commands)
4  BUILD          (fresh agent → /implement plan → validators green)
5  PROVE          (diff vs plan · tests · screenshots read back)
6  CAPTURE        (commit/PR · optional docs · score KPIs)
7  PROMOTE        (3× → template · streak → ADW/ZTE for that class)

IF FAIL: fix the SYSTEM (template/ADW/validator), not only the app.
DAILY FILTER: agentic layer or application layer? (≥50% agentics)
```

**Name of the method:** **CPBPP** — Classify → Plan → Build → Prove → Promote

---

## Invariants (laws — never break)

| # | Law | Meaning |
|---|-----|---------|
| 1 | Stop coding | Agents write app code. You write the system that writes. |
| 2 | Core Four | Every run: Context · Model · Prompt · Tools — deliberate. |
| 3 | 1·1·1 | One agent · one prompt · one purpose. Fresh agent per phase. |
| 4 | Plan is the prompt | High-impact work lives as a written plan in `specs/`. |
| 5 | Closed loop | Request → Validate → Resolve. No “done” without a check. |
| 6 | Fix the system | Failure upgrades templates/ADWs, not only the symptom. |
| 7 | 3× rule | Once novel, twice maybe, three times → command/ADW now. |
| 8 | R&D | Context only by **Reduce** or **Delegate**. |
| 9 | Own the layer | Your templates on your codebase — not generic cloud agents. |
| 10 | Layer filter | ≥50% time on agentic layer. Daily: agentic or application? |

**KPIs (score every run):** Size↑ · Attempts↓ · Streak↑ · Presence↓

---

## Part 1 — Universal method (any work unit)

### Step 0 — Done-when gate
Write one sentence: **Done when ________ (observable).**  
If you cannot write it → stop. You do not have a problem yet.

### Step 1 — CLASSIFY
Pick **exactly one** problem class:

| Class | Use when |
|-------|----------|
| **chore** | Mechanical. No design debate. Rename, logging, deps, cleanup. |
| **bug** | Expected ≠ actual. Need root cause + minimal fix. |
| **feature** | New user value. Needs story, phases, acceptance. |
| **patch** | Review found a small miss. Surgical. Not a new feature. |
| **document** | Code shipped; teach future agents via `app_docs/`. |
| **research** | Explore; findings + claims that can be checked. |
| **decision** | Strategy (MA brief), not code. |

**If none fit:** run once in-loop as discovery → after success, **PROMOTE** a new class template (3× rule).

### Step 2 — LEVERAGE
Before planning: can a blind agent solve this?
- stdout logs errors?
- types / entry points clear?
- `/prime` gives enough map?
- right model + tools?

If blind → **chore** the leverage fix first. Do not plan a blind agent.

### Step 3 — PLAN (fresh agent)
Run the class template only:
```
/chore  "…"   →  specs/chore-{slug}.md
/bug    "…"   →  specs/bug-{slug}.md
/feature "…"  →  specs/feature-{slug}.md
```
Plan **must** include:
- Description
- Relevant Files
- Step-by-step Tasks
- **Validation Commands** (specific, runnable, no vague “test it”)

**Reject** vague plans. Fix the **template** if plan shape is wrong.

### Step 4 — BUILD (fresh agent — new session)
```
/implement specs/<plan>.md
```
- Execute steps top to bottom
- Run **all** Validation Commands
- On fail: fix → re-run **all** validators until green
- Report: task table + `git diff --stat`

**>3 retries without green:** STOP. Fix system (template / leverage / validators). Do not chat longer.

### Step 5 — PROVE
- Diff matches plan intent?
- Validators green?
- UI? Screenshots **read back** by agent
- Review severities: skippable | tech_debt | **blocker**
- Blocker → `/patch` → BUILD again

### Step 6 — CAPTURE
- Commit / PR
- Optional `/document` → `app_docs/` + conditional_docs
- Score KPIs for this run

### Step 7 — PROMOTE (this is how the layer grows)
| Signal | Action |
|--------|--------|
| Same step done **3×** | Create/update `.claude/commands/*.md` |
| Plan→build babysitting | Write `adws/adw_*.py` chain |
| Hand verification every time | Encode validators into plan format / hooks |
| Class one-shots 5–10× in a row | That class is ZTE-eligible (drop human review) |
| Domain re-learned every session | Add `experts/<domain>/` Act–Learn–Reuse |

**Always:** if a gap appeared, change **one agentic-layer file** today.

---

## Part 2 — Bootstrap (empty → Dan’s minimum layer)

Do in order. Do not skip.

### Day 0 structure
```
your-repo/
├── apps/                         # application ONLY
├── specs/                        # plans live here
├── agents/                       # run logs
├── adws/
│   ├── adw_modules/agent.py      # shells claude -p
│   ├── adw_prompt.py             # gateway
│   └── adw_chore_implement.py    # first chain
└── .claude/commands/
    ├── prime.md
    ├── chore.md
    ├── bug.md
    ├── feature.md
    └── implement.md
```

### Ordered build
1. Create dirs (agentic never inside `apps/src`)
2. Write `prime.md` (RUN / READ / REPORT)
3. Write `chore.md` + `bug.md` + `feature.md` (Plan Format + Validation Commands)
4. Write `implement.md` (HOP: read plan → do steps → validate → report)
5. Write gateway `adw_prompt.py` (one prompt → log under `agents/`)
6. Write `adw_chore_implement.py` (plan agent → parse path → implement agent)
7. **Done-when:** one real chore ships via two prompts (or ADW), plan in `specs/`, **zero hand-typed app code**

Copy skeletons from: `tac/tac-8/tac8_app1__agent_layer_primitives/`  
Practice offline: `IndyDevDan/dojo/lessons/01` → `07`

---

## Part 3 — The only ladder (climb; don’t collect)

| Rung | Add | Pass test | Forbidden until pass |
|------|-----|-----------|----------------------|
| **R1 Prime** | `/prime` + thin CLAUDE.md | Fresh agent orients without free wander | BFC, ADWs, MCP pile |
| **R2 BFC+HOP** | chore/bug/feature + implement + specs/ | Real chore: 2 prompts, zero hand code | Hooks, ADWs, multi-agent |
| **R3 Closed loop** | Validators in every plan; optional hooks | Agent self-heals from test failure | Out-loop, worktrees |
| **R4 ADW+PITER** | `adws/` plan→build→validate→log | `adw_*.py "task"` AFK → honest log | Worktrees, experts, O-agent |
| **R5 Isolation** | worktrees / `*_iso` | 2 tickets parallel, main clean | Orchestrator theater |
| **R6 Review+docs** | review + document gates | Ship path includes review proof | Experts, fleets |
| **R7 Expert** | one domain expertise.yaml + self-improve | Expert cites file:line; you never hand-edit expertise | Multi-agent fleets |
| **R8 Fleet (optional)** | O-agent CRUD | ≥2 agents produce files; orchestrator doesn’t code | — |

**Rule:** highest solid rung only. ADWs without closed loops = vibe automation.

**Timebox (60–90 min/day on a real repo):** R1–R2 ~1–2 weeks · R3–R4 ~2 weeks · R5–R7 ~2–3 weeks · **~5–7 weeks to Dan-grade without fleet theater.**

---

## Part 4 — “I got work today” (same protocol every day)

```
1. Write DONE-WHEN
2. CLASSIFY (chore|bug|feature|…)
3. /prime if new session
4. PLAN via class template → specs/
5. BUILD via /implement (fresh) OR adw_*.py if R4+
6. PROVE (validators + review if R6+)
7. CAPTURE
8. PROMOTE one layer improvement if anything hurt
```

You do **not** open the IDE and “just fix it.”  
You run the method. The method produces the fix.

---

## Part 5 — Daily operating loop (identical every day)

### Morning
- [ ] Set agentic-time intention (≥50%)
- [ ] Queue work as **problem classes** (chores first)
- [ ] Health check if ADW exists
- [ ] Fire out-loop / ADW before in-loop chat

### During
- [ ] Only CPBPP
- [ ] Fresh agent per phase
- [ ] Stdout/tests before you dig in
- [ ] Failures → template/ADW fix, not endless chat

### Evening
- [ ] Review only what still needs R
- [ ] Score KPIs · update streak per class
- [ ] 3× list → tomorrow’s new command
- [ ] Commit **one** agentic-layer improvement
- [ ] Ask: agentic layer or application layer today?

---

## Part 6 — Decision table (situation → action)

| Situation | Do this |
|-----------|---------|
| Empty / no layer | Part 2 Bootstrap R1→R2 |
| Cleanup / rename / logging | `/chore` → implement |
| Broken behavior | `/bug` → implement |
| New capability | `/feature` → implement |
| Review miss | `/patch` only |
| Urge to freeform chat | Reject if class has template |
| Fat confused context | Reduce + Delegate; clear + prime |
| Want AFK | Finish R3 then R4 ADW |
| Parallel tickets | R5 worktrees |
| “Does it work?” | Validators / test loop |
| “Did we build what we asked?” | Review + proof |
| Flawless chore streak | ZTE that class only |
| Strategy not code | Decision brief (MA), not BFC |
| Don’t trust claims | Verifier (R7+) |
| You’re typing app code | **STOP. Step 0.** |

---

## Part 7 — Anti-methods (system killers)

1. Hands on app code as default  
2. Infinite in-loop babysitting  
3. God-agent / mega-prompt / no plan file  
4. No validation commands  
5. Swallowed errors (blind agents)  
6. Fix bug, not template  
7. Ignore 3× rule  
8. Tangled agentic + app layers  
9. Fat CLAUDE.md + all MCPs always on  
10. Trust `/compact` as strategy  
11. Generic cloud agents over your templates  
12. ZTE before streak proof  
13. Review without reading proof  
14. Parallel without isolation  
15. Majority day in application layer  

---

## Part 8 — What “I have Dan’s agentic layer” means

- [ ] `apps/` = product; agentic ring wraps it  
- [ ] `/prime` + thin memory  
- [ ] BFC + `/implement` + `specs/`  
- [ ] Closed-loop validation  
- [ ] `adws/` plan→build→validate + honest log  
- [ ] Isolation for parallel work  
- [ ] Review (+ docs) on ship path  
- [ ] ≥1 living expert domain  
- [ ] ≥3 real changes shipped with zero keyboard between invoke and review  
- [ ] Failures report `ok: false` — no fake green  
- [ ] Weekly: more work via layer than by hand  

**Not required:** orchestrator UI, five MCP servers, Class-3 fleets.

---

## Start tomorrow (first 7 days)

| Day | Action | Pass |
|-----|--------|------|
| 1 | Scaffold MVAL dirs on **your** real repo | tree exists |
| 2 | Write `/prime`; run it | agent map matches repo |
| 3 | Write `/chore` + `/implement` | plan format complete |
| 4 | Ship one real chore via 2 prompts | zero hand app code |
| 5 | Add Validation Commands + force a self-heal | agent fixes from test fail |
| 6 | Gateway `adw_prompt.py` then `adw_chore_implement.py` | one AFK chore |
| 7 | Log KPIs; list 3× items; promote one command | layer file committed |

Then climb R3→R7 using Part 3. Same method. Thicker ring.

---

## Sources (this system is extracted from)

- TAC 1–8 (tactics collapsed into CPBPP + invariants)
- AH-6 class/grade ladder
- TAC-8 app1 MVAL + app5 full factory
- Dojo lessons 01–12
- Problem-class templates (chore/bug/feature/patch/review/document)
- Fleet synthesis agents (method, classes, ladder)

**That’s the whole system.**  
Everything else in the course is a thicker ring of the same loop:

> **Classify the class → template the plan → fresh build with closed loops → prove → promote the layer.**

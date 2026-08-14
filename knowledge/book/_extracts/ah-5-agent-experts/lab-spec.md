# AH-5 Lab Spec — Agent Experts

**Scope rule:** every drill runs inside the course codebase only (`codebase/` → `agentic-horizon/agent-experts`; students: `git clone https://github.com/disler/agent-experts.git`). No external repos.
**Prime directive (graded throughout):** you **never hand-edit an expertise file**. Every change to a mental model must come from running a self-improve prompt. If you open `expertise.yaml` and type into it, you've failed the core discipline of the lesson.
**Time box:** 60–90 minutes. Token cost: several multi-agent runs across Opus/Sonnet/Haiku — real money; pay to play.
**Repo rules to honor (from CLAUDE.md):** use `uv`, never raw `python`; keep `apps/orchestrator_db/models.py` in sync with migrations; prefer Pydantic over dicts; **do not commit unless asked**.

---

## 0 · Setup & orientation (12 min)

1. `git clone https://github.com/disler/agent-experts.git && cd agent-experts`
2. Verify the toolbelt: `claude --version`, `uv --version`, `git --version`, `node --version`; ensure **PostgreSQL** is running (the orchestrator's data layer).
3. **Read both experts end to end** and label each file **Act / Learn / Reuse** in writing:
   - `.claude/commands/experts/database/` → `question.md`, `self-improve.md`, `expertise.yaml`
   - `.claude/commands/experts/websocket/` → `plan_build_improve.md`, `plan.md`, `question.md`, `self-improve.md`, `expertise.yaml`
4. Start the app the codebase experts operate on. Easiest: use the **start-orchestrator skill**, or run `apps/orchestrator_3_stream/start_be.sh` and `start_fe.sh`.

**Checkpoint 0 (write it down):** for the *database* expert, which step is missing and why? (Answer: Act — no prompt changes code.) For the *websocket* expert, which file supplies Act, which supplies Learn, which supplies Reuse?

## 1 · Meta-agentics — act without learn (12 min)

1. Run the **meta prompt** to build a new prompt (e.g. ask it for a "summarize-open-prs" question prompt). Confirm it wrote a real `.claude/commands/<name>.md` in the Specified Format.
2. Run the **meta agent** to build a new sub-agent. Confirm `.claude/agents/<name>.md` exists with real YAML frontmatter and exactly 4 sections.
3. Run the **meta skill** to build a new skill. Confirm `.claude/skills/<name>/SKILL.md` exists.

**Checkpoint 1:** in one sentence, why are these three **not** agent experts? (Answer: they act but never learn — nothing about them updates automatically.)

## 2 · Reproduce Dan — the partial (database) expert (15 min)

**Reuse.** Run `/experts:database:question "does information flow between our database tables? write your report to a temp file."`
- Verify the **first** tool call is `Read(.../database/expertise.yaml)`, *then* it reads `apps/orchestrator_db/models.py` and migrations to validate.
- Verify the report cites **exact files and line numbers** and includes a mermaid ER diagram.
- Verify it wrote **no** code (question mode is read-only).

**Learn.** Run `/experts:database:self-improve`.
- Verify it validates top-to-bottom, runs `wc -l` against `MAX_LINES` (1000), and compiles the YAML (`python3 -c "import yaml; yaml.safe_load(...)"`).
- Verify it reports discrepancies **or** cleanly reports "nothing to do" and stops.

**Checkpoint 2 (write it down):** quote the two lines in `question.md` that make Reuse safe — the one that reads the expertise and the one that validates it against the codebase.

## 3 · Reproduce Dan — the complete (websocket) expert (20 min)

1. Run the full loop:
   `/experts:websocket:plan_build_improve "Add a session-based counter to the app nav bar that displays the total number of WebSocket events."`
2. Watch the three sub-agents in order: **plan → build → self-improve (true)**. Note each is a fresh `Task` (context delegation) and record the token/tool stats per step.
3. **Verify the Act:** the counter appears in the app nav bar and increments on WebSocket events.
4. **Verify the Learn:** `git diff .claude/commands/experts/websocket/expertise.yaml` shows a real, accurate mental-model update (e.g. a `websocketEventCount` / `session_state` entry with correct line references).
5. **Scale compute:** in the orchestrator UI, fire the same websocket **question** at **three** agents. Compare the three answers.

**Checkpoint 3:** (a) which sub-agent step is Act, which is Learn, which is Reuse? (b) Did all three parallel experts agree? Did any fail or surface something the others missed? Why is that the *point* of scaling compute?

## 4 · Stretch drills (20–30 min — still zero hand-edited expertise)

**S1 — Seed a NEW expert from blank.** Pick a real subsystem (e.g. the orchestrator's cost tracking, or Nile's cart). Create `.claude/commands/experts/<domain>/` with an **empty** `expertise.yaml` and copied-and-edited `question.md` + `self-improve.md` pointing at the right files. Run self-improve **repeatedly** until it stops finding new things. The agent — not you — writes every line of the expertise.

**S2 — Break-then-heal.** Corrupt one line-number reference in an existing `expertise.yaml`, then run its self-improve with `check_git_diff=false`. Confirm it detects and repairs the drift.

**S3 — Never-edit discipline (graded).** Find something you dislike in an expertise file. Instead of editing it, add a prescriptive line to the **self-improve** prompt (e.g. "always record `reset_on` connect/disconnect line numbers"), rerun, and confirm the agent produces your change itself.

**S4 — Line-limit stress.** Temporarily lower `MAX_LINES` in a self-improve prompt to a small number. Rerun and watch the agent trim least-critical content while preserving key operations. Report what it dropped and whether the expert still answers well.

**S5 — Product expert (Nile).** Start Nile (`apps/nile` FE+BE). Browse → add to cart → checkout as a user. Open the **Control-K** expertise panel and correlate your actions with `expertise_data` (viewed/added/checked-out) and the regenerated personalized sections. Change `SECTIONS_RANGE` / `PRODUCTS_PER_SECTION_RANGE` in `shopping_expert_streaming_system_prompt.md` and observe the UI change.

**S6 — When-NOT-to-use judgment.** Pick a static/simple part of the repo. Argue in writing why an expert would *not* help there, then solve the same task with a plain generic agent for comparison.

## Pass criteria (all required)

- [ ] Zero hand-edited expertise files anywhere in the lab (every mental-model change came from a self-improve run).
- [ ] Each expert file correctly labeled Act / Learn / Reuse; you can explain why the database expert is "partial" (Checkpoint 0).
- [ ] Database question ran read-only, read `expertise.yaml` **first**, and validated against the codebase with cited files/lines (Checkpoint 2).
- [ ] `plan_build_improve` completed all three steps; the nav-bar counter works **and** the `expertise.yaml` git diff shows a real, accurate update (Checkpoint 3).
- [ ] You seeded at least one **new** expertise file entirely via self-improve (S1) and it stabilized ("nothing to do").
- [ ] You demonstrated the never-edit discipline (S3): a change you wanted appeared by editing the self-improve prompt, not the file.
- [ ] Closing oral check, no notes: Act/Learn/Reuse + keyword; why the expertise file is a mental model not a source of truth; two systems you'd build an expert for and one you wouldn't, with reasons.

## Instructor / self-check notes

- **Most common failure:** hand-editing `expertise.yaml` "just this once." Catch it early — it defeats the entire lesson. If the file needs to change, the *self-improve prompt* is what changes.
- **Second failure:** building a partial expert (Reuse + Learn) and expecting it to improve. Without an **Act** step there's no useful action to learn from. Have students point at the exact missing prompt.
- **Third failure:** trusting the expertise file blindly. Make them show the "validate against the codebase" step actually reading real files.
- **Seeding stall:** students over-specify the structure up front. Push them to start **blank** and let self-improve define it; then tweak the prompt and rerun.
- **Cost anxiety:** the websocket full loop plus three parallel experts is the token-heavy part. If a student can't afford to run it, the pay-to-play conversation is the lesson surfacing early — have them at least run the read-only database question + one self-improve.
- **What this lab intentionally does NOT cover:** routers/reminders for "too many experts," full production Skill/SDK packaging, and generative-UI latency engineering — flagged in outdated-vs-current.md and deferred to keep the Act/Learn/Reuse primitive crisp.

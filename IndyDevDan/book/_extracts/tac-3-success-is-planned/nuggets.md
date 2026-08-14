# TAC-3 Nuggets — ranked for the struggling learner

> 15 nuggets in three tiers. Tier 1 is the exam. Tier 2 is the machinery. Tier 3 keeps you going.
> Source: VTT-verified transcript + the tac-3 codebase on disk + 12 verified frames.

## Tier 1 — If you remember nothing else

1. **The plan IS the prompt.** A plan/spec/PRD is just a prompt scaled up for high impact — so great planning is literally great prompting. (1:46–1:56; the on-screen equation: Great Planning === Great Prompting.)
2. **Tactic #3: Template Your Engineering.** Encode how you solve each CLASS of work (chores, bugs, features) into reusable template files; the template's output is always a plan in `specs/`, never code. (3:20 slide; loot box: "reusable, scalable units of agentic success.")
3. **Meta prompt = a prompt that builds a prompt.** `/chore "one sentence"` → the agent researches the codebase and writes a 64-line plan (`specs/replace-print-with-logging.md`) from your one line. (8:04; frame t0585.)
4. **HOP = a prompt that takes prompts as input.** `/implement specs/<plan>.md` — 12 lines that run ANY plan: "plans getting passed into plans," like higher-order functions. (13:34 slide, quoted verbatim in the extract.)
5. **Fresh agent, every phase.** Plan in one instance, implement in a NEW one — three reasons: context focus; zero-dependency reusable assets; preparing for off-device runs. "Decouple our performance from the conversational context window." (23:02–26:35.)

## Tier 2 — The working machinery

6. **Template anatomy (five parts):** purpose line → ## Instructions (THINK HARD; start at README.md) → ## Relevant Files ("Ignore all other files") → ## Plan Format (exact ```md skeleton) → final H2 holding `$ARGUMENTS`. (9:58–11:58; frame t0660.)
7. **Different work, different encoded process:** bug.md adds Problem/Solution Statements + Steps to Reproduce + Root Cause Analysis + "surgical, minimal changes"; feature.md adds User Story + 3-phase Implementation Plan + Testing Strategy + Acceptance Criteria.
8. **Plans self-validate:** every Plan Format ends in Validation Commands (`cd app/server && uv run pytest`, zero regressions) and the agent's last task is running them; the bug agent even diffed its own work, found 2 issues, and fixed them unprompted. (30:13–30:25.)
9. **THINK HARD is a switch, not a pep talk** — course-era Claude Code's information-dense keyword for the reasoning model; the durable principle is buying more reasoning compute for planning-grade work. (13:07; one of the 12 leverage points.)
10. **You should know 100% of your agent's context at boot** — implement.md + the plan file and nothing else. That certainty is what makes failures diagnosable and templates improvable ("a trail of success"). (27:00–27:40.)
11. **The headless bridge:** `claude -p "/feature \"...\"" --output-format stream-json --dangerously-skip-permissions --model opus --verbose > feature_plan_raw_agent_logs.jsonl` — the same template, no visible agent, a live-appending JSONL, and a finished `specs/query-history-panel.md`. (36:27–37:44; frames t2205/t2270/t2575.)
12. **Two prompts completed the whole chore:** `/chore` (planning phase) + `/implement` (building phase). Separate phases, separate fresh agents — that's the pattern to burn in. (16:55: "completed agentically with two prompts.")

## Tier 3 — Framing that keeps you going

13. **Planning alone is expensive — that's WHY templates exist.** Time scales with problem difficulty and codebase size, and "there's always something to miss"; templates amortize the cost across every future run. (4:00–4:30.)
14. **Custom templates are differentiation.** Off-the-shelf agents "don't understand your codebase like you do"; specialize per system (front-end features, DB-migration chores, notebook bugs) — "the more custom your templates are, the more unique your engineering gets." (4:54; 41:58.)
15. **"My codebase is too big" is a limiting belief — and the CTA is NOW.** Run one small `/chore` today from the tac-3 repo; don't wait to finish the course. Also the warning label: "agents run loose... without structure is a plan for failure." (43:49–44:30; 30:58.)

## Micro-quiz (close the book first)

1. Complete: prompt → ______ → ______, and state both Dan equalities. *(plan/spec/PRD → template; the plan is the prompt; great planning is great prompting)*
2. Meta prompt vs HOP — one sentence each, one example each from `.claude/commands/`. *(Prompt that builds a prompt: /chore. Prompt that takes a prompt as input: /implement.)*
3. Where do generated plans live, and what three landed there in the demo? *(specs/; replace-print-with-logging.md, fix-sql-injection-vulnerabilities.md, query-history-panel.md)*
4. The three fresh-agent reasons, ten words or fewer each. *(Focus every token; zero-dependency reusable assets; prepare for off-device.)*
5. Which four flags followed `claude -p`, and where did output go? *(--output-format stream-json, --dangerously-skip-permissions, --model opus, --verbose; > feature_plan_raw_agent_logs.jsonl)*
6. What must every plan's last step do? *(Run the Validation Commands — zero regressions, e.g. uv run pytest.)*

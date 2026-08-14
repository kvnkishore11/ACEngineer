# TAC-3 · Success is Planned — Master Teaching Notes

> Source of truth for the expanded chapter. Video 46:32 · Intermediate · Tactic #3: **Template Your Engineering**
> Lesson artifact: eight slash-command files in `.claude/commands/` — four of them (chore/bug/feature/implement) are the entire tactic. The app underneath (the lesson-2 NL→SQL client/server) is deliberately just a workbench.

**Lesson thesis in one sentence:** A plan is a prompt scaled up — so encode HOW you plan each class of work (chores, bugs, features) into reusable templates that agents fill out, execute the resulting plans with fresh memory-less agents via a higher-order `/implement`, and you've templated your engineering into a system that can eventually run without you.

**The chapter must land ten ideas.** Each below follows: Hook → Picture → Worked example (course codebase) → Dan's term → Failure mode → Retrieval Q.

---

## Idea 1 — The prompt is everything, and a plan is a prompt scaled up

**Hook.** "What was once a complete joke is now the most valuable skill any engineer can have." Prompting got laughed at; then it became the medium through which all work flows to agents. So ask the question the lesson opens with: *what does a scaled prompt look like?* It's a plan. It's a specification. It's a PRD.

**Picture.** Frame t0116 (1:56): the on-screen equation **Great Planning === Great Prompting** overlaid on the keyboard shot — the thesis as one image.

**Worked example.** `specs/init_nlq_to_sql_to_table.md` ships in the repo: the 749-line plan that *built the entire application* in lesson 2. The proof that plans are executable prompts is sitting on disk before you type anything.

**Dan's term.** *Plans are prompts scaled up for high impact. The plan is the prompt.* Corollary later in the lesson: plans are *"staging environments for code"* — engineering work compressed into natural language that the agent expands.

**Failure mode.** Treating plans as documentation (write-once, goes stale in a wiki) instead of as the actual instruction fired into an agent. The tell: a student who "writes a plan" and then re-explains everything to the agent in chat has not connected plan=prompt.

**Retrieval Q.** Complete the ladder: prompt → ? → ? — and state the two Dan equalities. *(Prompt → plan/spec/PRD → template; the plan is the prompt; great planning is great prompting.)*

---

## Idea 2 — Tactic #3: Template Your Engineering

**Hook.** Planning alone is expensive: it's time-consuming, there's always something to miss, and the cost scales with problem difficulty and codebase size. You could write every plan by hand forever — or you could encode *how you plan* once, and let agents write the plans.

**Picture.** Frame t0200 (3:20): the full Tactic 03 slide — definition, the 01–08 tactic dot grid (this is tactic three of eight), and the **Daily Actions** sidebar (use meta-prompts for problem classes; create specialized templates; build HOPs that pass plans into plans; review and refine templates from outcomes; document domain-specific patterns; convert successful prompts into meta-prompts).

**Worked example.** The whole of `.claude/commands/`: chore.md (53 lines), bug.md (69), feature.md (91), implement.md (12). Zero application code — pure encoded process. Also the sleeper example: `/install` runs `scripts/copy_dot_env.sh` agentically ("we're having an agent with a reusable prompt do this work for us") — reuse all the way down.

**Dan's term.** *Template your engineering* — "you encode your problem solving into reusable units that you, your team, and your agents can see, use, and importantly, improve." Solves problem **classes**, not problems; explicitly "one of many solutions to the my-codebase-is-too-big problem" and one of the 12 leverage points.

**Failure mode.** Hearing "template" as code boilerplate/snippets. These templates contain no code — the output of a template is a *plan*. Second failure: copying the templates into your repo without rewriting `Relevant Files`, so the agent researches files that don't exist and produces mush.

**Retrieval Q.** What does a template output, and for whom (three audiences)? *(A plan in specs/; for you, your team, and your agents — to see, use, and improve.)*

---

## Idea 3 — The meta prompt: one sentence in, a 64-line plan out

**Hook.** Dan types one sentence — *"Replace all server print statements with proper python logging. Use proper log levels. Preserve the exact same log output. Make sure all output is written standard out"* (as typed on screen) — and walks away. The agent reads the README, researches the codebase with its reasoning model, and writes a complete plan.

**Picture.** Frame t0470 (7:50): the `/chore` prompt being typed (with install.md's 11 lines above it). Frame t0585 (9:45): the payoff — `Write(specs/replace-print-with-logging.md)`, "Wrote 64 lines", the plan excerpt inventorying prints by line number, and the one-sentence prompt circled underneath.

**Worked example.** The generated plan (not committed; regenerate it in the lab) inventories the codebase's actual print statements — 18 lines in `app/server/server.py` plus 1 in `app/server/main.py` = 19, each with its line number and message type. (Accuracy note for the chapter: the on-camera agent's *prose summary* says "19 in server.py / 20 across 2 files" while its own line inventory totals 18+1 — quote the inventory, not the prose.)

**Dan's term.** *Meta prompt* — "a prompt that builds a prompt. More specifically, this agentic prompt builds a plan based on a template that our agent fills out." Your input is a *high-level prompt* — "a prompt that's void of detail."

**Failure mode.** Expecting `/chore` to fix the code. It plans only; nothing in the app changes until `/implement` runs. Students who "finish" after the plan generated have done half the workflow; students who tell the same session "now do it" have skipped the fresh-agent discipline (Idea 7).

**Retrieval Q.** Define meta prompt, and name the demo's input and output artifacts. *(A prompt that builds a prompt; input: one-sentence chore string into $ARGUMENTS; output: specs/replace-print-with-logging.md, a 64-line plan.)*

---

## Idea 4 — Template anatomy: five parts, three specializations, one home

**Hook.** Open `chore.md` expecting something exotic; find "a reusable prompt that looks ordinary" — yet "the instructions in this prompt completely change your engineering impact."

**Picture.** Frame t0660 (11:00): chore.md lines 1–34 fully legible — purpose sentence, Instructions (with `THINK HARD`), Relevant Files, and the opening of Plan Format.

**Worked example.** The shared skeleton across chore/bug/feature: (1) **purpose line** at top ("Create a new plan in specs/*.md to resolve the `Chore` using the exact specified markdown `Plan Format`..."); (2) **## Instructions** — thorough-but-precise, name the file appropriately, "IMPORTANT: Replace every <placeholder>", "Use your reasoning model: THINK HARD", "Start your research by reading the `README.md` file"; (3) **## Relevant Files** — README.md, app/**, scripts/** and "Ignore all other files in the codebase."; (4) **## Plan Format** — the exact markdown skeleton in a ```md fence; (5) the final H2 (## Chore / ## Bug / ## Feature) holding **$ARGUMENTS**. The specializations encode different engineering: bug.md adds Problem/Solution Statements, Steps to Reproduce, Root Cause Analysis and demands a surgical minimal fix ("Don't use decorators. Keep it simple."); feature.md adds a User Story, a 3-phase Implementation Plan, Testing Strategy, and Acceptance Criteria. All plans land in `specs/`.

**Dan's term.** *Plan format* / *giving our agent a template*; the `$ARGUMENTS` slot is "the Claude Code argument parameter that just takes whatever we passed in."

**Failure mode.** One-format-fits-all thinking — flattening bug and feature planning into the chore shape and losing exactly the sections (repro, root cause, acceptance criteria) that make those work classes safe. Also: deleting the seeded validation line (`cd app/server && uv run pytest`) when porting, which silently removes the plan's self-check floor.

**Retrieval Q.** Name the five structural parts every template shares, and two sections bug.md adds that chore.md lacks. *(Purpose, Instructions, Relevant Files, Plan Format, $ARGUMENTS slot; Steps to Reproduce + Root Cause Analysis — also Problem/Solution Statements.)*

---

## Idea 5 — The Higher Order Prompt: /implement runs any plan

**Hook.** The build phase needs a prompt too — and it's 12 lines. "It doesn't take a lot to do a lot, but you need the right information."

**Picture.** Frame t0815 (13:35): the HOP definition slide — verbatim: *"A prompt that accepts other prompts as input parameters, enabling composable agentic workflows. Higher order prompts (HOPs) allow you to pass plans, templates, or other prompts into reusable execution frameworks - like passing functions into functions in programming languages, but for agentic systems."* — with implement.md's `## Plan` / `$ARGUMENTS` visible behind it and the logging diff already flowing.

**Worked example.** `.claude/commands/implement.md` in full: purpose ("Follow the `Instructions` to implement the `Plan` then `Report` the completed work."), one instruction ("Read the plan, think hard about the plan and implement the plan."), `## Plan` → `$ARGUMENTS`, `## Report` → bullet summary + "Report the files and total lines changed with `git diff --stat`". Invocation: `/implement specs/replace-print-with-logging.md`. The same 12 lines later run the bug plan unchanged — and Dan sketches HOP variants: "read your plan, implemented it... after you implement, review the work completed against the plan."

**Dan's term.** *Higher order prompt, AKA a hop* — "plans getting passed into plans"; like higher-order functions. The chore completes "agentically with two prompts, one for the planning phase and one for the coding building phase."

**Failure mode.** Bloating the executor. Students stuff plan-specific detail into implement.md, coupling it to one plan and killing its universality — detail belongs in the plan (or template), the HOP stays generic. Also: forgetting the Report block exists, then complaining the run "ended silently."

**Retrieval Q.** What are implement.md's four sections, and why does its smallness matter? *(Purpose/Instructions/Plan($ARGUMENTS)/Report; because it's a universal executor — the power flows through it from the plan, so it must stay generic.)*

---

## Idea 6 — THINK HARD: buying reasoning compute on purpose

**Hook.** Both the templates and the executor contain a strange all-caps phrase: THINK HARD. It's not motivation — it's a switch.

**Picture.** Frame t0660 shows it in chore.md's instructions ("Use your reasoning model: THINK HARD about the plan..."); the implement run banner shows thinking-mode workings ("Schlepping… / Philosophising…" with token counts).

**Worked example.** implement.md line 5: "Read the plan, think hard about the plan and implement the plan." Dan: "We're activating Claude Code's information dense keyword to activate the reasoning model... If you just search for think, you'll be able to find this. This is an information dense keyword that Anthropic has encoded into this word here. Think."

**Dan's term.** *Information dense keyword*; framed as one of the *12 leverage points* — "We always wanna throw more compute at the problem, right? Especially as we start to scale this up."

**Failure mode.** Cargo-culting the words without the principle (sprinkling "think hard" on trivial work), or the reverse — running planning-grade work with reasoning off to save tokens and getting shallow plans. The durable principle: match reasoning budget to problem difficulty; planning is where it pays.

**Retrieval Q.** What does "think hard" do in course-era Claude Code, and what's the transferable principle? *(Activates the reasoning model via an information-dense keyword; deliberately allocate more reasoning compute to planning-grade work.)*

---

## Idea 7 — Fresh agents every time: three reasons, four KPIs, one certainty

**Hook.** "Why do I keep opening up new Claude Code instances? Look at all these terminals... fresh agent instances that have no memory of what just happened. Why am I doing that? Don't we want to keep rolling the important context...? **No.**"

**Picture.** Frame t1390 (23:10): implement.md on screen, the agent's todo checklist mirroring the bug plan's steps 1:1, and a right rail stacked with eight terminal sessions.

**Worked example.** Six separate agent boots in one lesson: /install; /chore; /implement (chore); /bug; /implement (bug); the headless /feature run. Between phases Dan commits specs + code ("you want each one of these steps to commit their changes" — full Git discipline promised for later lessons).

**Dan's term.** The three reasons, verbatim targets: (1) *"we free up our context — focus every available token on the task at hand"* (agents have context windows; so do overloaded humans); (2) *"we force our prompts, plans, and templates to be isolated, reusable, and improvable assets with zero dependencies"* — creating "a trail of success or a trail of things we can improve"; (3) *"we prepare for true off-device agentic coding."* KPI linkage (from lesson 2): size ↑, attempts ↓, streak ↑, presence → 0 — *"we need to decouple our performance from the conversational context window"*; *"we want one shot successes"*; *"we're not here to babysit a single agent."* And the certainty: booting from implement.md + a plan file means "I know 100%... what the agent's perspective is."

**Failure mode.** The comfort of the rolling conversation. It feels safer ("the agent remembers!") but it builds assets that secretly depend on chat history — irreproducible by teammates, unimprovable, and impossible off-device. The tell: "it worked yesterday in my session" with no way to say what the agent knew.

**Retrieval Q.** Recite the three reasons and the KPI the pattern ultimately drives to zero. *(Context focus; isolated/reusable/improvable zero-dependency assets; preparing for off-device — presence → 0.)*

---

## Idea 8 — Plans that check themselves (and the human who still checks)

**Hook.** Near the end of the bug implement, the agent runs a diff over its own work, announces two issues, and fixes them — unprompted. "This is the power of templating your engineering. I still haven't lifted a finger."

**Picture.** Frame t0945 (15:45): the logging diff — red `print(f"[SUCCESS]...")` → green `logger.info(...)` under the plan's step list with exact line numbers. Frame t1285 (21:25): the bug plan's Root Cause Analysis (keyword blocklist insufficient; identifiers trusted from uploads; SQLite params don't cover identifiers; no centralized SQL layer), Relevant Files, and `### New Files` → `app/server/core/sql_security.py`.

**Worked example.** Every Plan Format ends with **## Validation Commands** ("Execute every command to validate... with zero regressions", seeded with `cd app/server && uv run pytest`; chore.md adds "Don't validate with curl commands."), and the last step of every Step-by-Step Tasks list is running them. The bug plan adds Steps to Reproduce so a human can verify independently — which Dan does: restarts the app, tries an injection-shaped concat query, re-runs pytest by hand. All four Relevant-Files claims in the generated bug plan are literally true of the shipped code (raw `cursor.execute(sql_query)` behind a substring blocklist in sql_processor.py; f-string identifiers in file_processor.py and insights.py; `cursor.execute(f"DROP TABLE IF EXISTS {table_name}")` at server.py:243).

**Dan's term.** *Self-validating loops with tests*; "it's checking its own work — self validation." Flagged as "a huge, huge leverage point... it has its own dedicated lesson."

**Failure mode.** Both extremes: trusting self-validation totally (skipping the manual repro, letting a subtly wrong fix land), or ignoring it (deleting Validation Commands when porting templates, so plans stop being closed-loop). The video's own numbers teach calibration: Dan's run reports 52 tests / 18 new — your regenerated run will differ; the invariant is zero regressions + new coverage, not magic numbers.

**Retrieval Q.** Name the two self-validation mechanisms in the demo and the one human step Dan still performs. *(Embedded Validation Commands (pytest + running the apps) and the agent's own git-diff review-and-fix; Dan still manually reproduces — browser query + pytest.)*

---

## Idea 9 — The off-device preview: claude -p, stream-json, and an invisible agent

**Hook.** "We won't be able to open up the terminal" — if features are to ship end-to-end without us, the agent must run where we aren't. So Dan fires the /feature template with no visible agent at all, and watches a file grow.

**Picture.** Frame t2205 (36:45): the complete command — `claude -p "/feature \"Create a new query history side panel...\"" --output-format stream-json --dangerously-skip-permissions --model opus --verbose > feature_plan_raw_agent_logs.jsonl`. Frame t2270 (37:50): the JSONL appending live — system init, assistant events with `claude-opus-4-20250514`, tool results. Frame t2575 (42:55): the deliverable — `specs/query-history-panel.md` rendered (Feature Description, User Story, Problem Statement...), written by an agent nobody watched.

**Worked example.** The exact same `.claude/commands/feature.md` template runs interactively and headlessly — that symmetry is the entire bridge to lesson 4. Dan's scoping on the scary flag: "running in dangerously skip permissions. This is going to work just fine for now. It's very low risk" — a planning-only run in a demo repo. The output redirect is the composition hook: "we can chain these agents together. We can check their output."

**Dan's term.** *Claude Code in its programmatic form*; "this prompt here represents the planning phase" of the SDLC → *agentic software development lifecycle*; destination named: *AI developer workflows* — "the highest composition level and the greatest leverage point of agentic coding" (lesson 4: "let your product ship itself").

**Failure mode.** Two: treating `--dangerously-skip-permissions` as the default posture everywhere (it was scoped risk, not habit — modern practice uses allowlists/sandboxes/hooks); and dismissing the JSONL as "just logs" when it's the machine-readable interface another program or agent consumes.

**Retrieval Q.** Which template ran headlessly, with which four flags, into which file — and what appeared in specs/? *(/feature; --output-format stream-json, --dangerously-skip-permissions, --model opus, --verbose; > feature_plan_raw_agent_logs.jsonl; specs/query-history-panel.md.)*

---

## Idea 10 — Specialize, share, start now: templates as differentiation

**Hook.** Codex, Copilot, Devin, Jules, Gemini CLI "and whatever comes next" — great tools, but "no matter how great AI gets, they don't understand your codebase like you do." The granularity you need lives in templates you write.

**Picture.** Frame t2575 doubles here: a comprehensive feature plan produced by *your* encoded process is the differentiation argument made visible.

**Worked example.** The specialization ladder Dan sketches over the generic trio: a front-end feature template for specific page sets; a chore template for your database migration system; a bug resolver for your research-notebook system. Team leverage: templates are time savers "not just for you, but for your entire team" — see/use/improve. And the improvement loop: as your size-KPI grows, templates get bigger or more precise — "we get this self-improving loop inside of your codebase."

**Dan's term.** *"The more custom your templates are, the more unique your engineering gets"* — and the standing order: *"You want to be building the system that builds the system."* Anti-pattern named: *"Having agents run loose on your codebase without structure, without knowing how you do things is a plan for failure."* Objection pre-handled: "my codebase is too big" is *a limiting belief*.

**Failure mode.** Waiting. The lesson's explicit CTA is to run one small `/chore` today ("Do not wait... Don't wait to complete this course. You'll miss out on getting ahead now") — the aha moment is engineered to be cheap. The meta-failure is perfectionism: polishing a mega-template before ever firing one.

**Retrieval Q.** Why do custom templates beat out-of-the-box agent tools, per Dan — and what is the lesson's call to action? *(Tools don't know your codebase or give SDLC-granular control; encode YOUR practice. CTA: run one small /chore now.)*

---

## Timeline map (VTT-verified)

| t | beat |
|---|---|
| 0:18 | "Complete joke → most valuable skill. The prompt is everything." |
| 1:46–1:56 | Plan/spec/PRD; plans are prompts scaled up; Great Planning === Great Prompting |
| 2:46–3:02 | "Those who plan the future tend to create it"; Pareto 80/20; three tactics |
| 3:20 | Tactic 03 slide: Template Your Engineering (+ Daily Actions) |
| 4:39–4:57 | Templates = one of 12 leverage points; Codex/Copilot/Devin/Jules/Gemini CLI limits |
| 5:47–6:20 | /install (runs prime + copy_dot_env.sh from tac-2) |
| 6:46–7:45 | scripts/start.sh; browser demo ("age between 20 and 40"); stdout foreshadow |
| 7:47–8:06 | /chore fired; meta prompt defined |
| 9:02–9:58 | Plan written to specs/ (64 lines); plan reviewed in preview |
| 9:58–11:58 | chore.md dissected: purpose→instructions→relevant files→plan format→$ARGUMENTS |
| 12:30–12:44 | /implement + plan path (new instance); "doesn't take a lot to do a lot" |
| 13:07–13:40 | implement.md (12 lines); think hard; yolo mode; **HOP slide** |
| 14:00–15:45 | Todos mirror plan steps; Report: summary + git diff --stat |
| 15:25–17:20 | Validation: pytest, git diff review, browser re-test, no-prints grep |
| 17:44–19:09 | /bug fired (SQL injection, high-level prompt) |
| 19:25–22:20 | Thinking mode; leverage-points recap; bug plan reviewed (root cause, New Files); commit; /implement |
| 23:02–28:10 | **Fresh agents: three reasons; KPIs; one-shot successes; known perspective** |
| 29:40–30:30 | HOP variants; agent self-fixes 2 issues; "haven't lifted a finger" |
| 30:58 | "Agents run loose without structure... a plan for failure" |
| 32:55–35:20 | /feature prompt drafted; bug run finishes (52 tests, 18 new); manual injection tests |
| 36:27–37:44 | claude -p + stream-json fired; JSONL appends live |
| 38:05–39:55 | feature.md purpose; "system that builds the system"; plans as staging environments |
| 41:00–43:20 | Headless plan lands: specs/query-history-panel.md reviewed (not implemented) |
| 43:49–44:30 | CTA: run one /chore now; limiting beliefs |
| 44:30–46:32 | 8-tactics stack recap; lesson-4 teaser: ADWs, "let your product ship itself" |

## Terminology glossary (Dan-isms, canonical spellings)

- **Meta prompt** — a prompt that builds a prompt (template → plan). Transcript sometimes renders "/chore" as "slash tour / this tour" — always *chore*.
- **Higher order prompt (HOP)** — a prompt accepting prompts as input ($ARGUMENTS = a plan path). "AKA a hop."
- **Template** — reusable meta-prompt file in `.claude/commands/` encoding one class of work.
- **Plan / spec / PRD** — the scaled prompt; generated into `specs/`.
- **High-level prompt** — deliberately detail-free one-liner passed to a template.
- **THINK HARD / information dense keyword** — course-era reasoning-model trigger.
- **Fresh agents / one-shot successes / presence KPI** — the context-decoupling doctrine.
- **Programmatic form** — `claude -p` headless invocation ("claw code" in the auto-transcript = Claude Code).
- **copy_dot_env.sh** — transcript's "copy.m / scripts copy" ; **tac-2** — transcript's "tack to".
- **Root Cause Analysis** — transcript's "root calls analysis".
- **Loot box** — per-lesson resource notes (22 for this lesson).

## Bridge to the rest of TAC (as trailed in-lesson)

- **Backward:** assumes lesson 1's Stop Coding + core four, and lesson 2's KPIs (size/attempts/streak/presence), agent-perspective tactic, and the NL→SQL codebase this repo carries forward (including `/prime`, `/tools`, `/start` and the 749-line init spec).
- **Forward (lesson 4):** triggers and agents running in their own environments — AI developer workflows as "the highest composition level and the greatest leverage point"; the empty `adws/` and `agents/` directories in this repo are the reserved parking spaces. Git discipline for step-wise commits "in upcoming lessons"; closing the loop / self-validation "has its own dedicated lesson."
- **Whole-arc:** the 8-tactics stack (dot grid on the Tactic 03 slide; T1–T5 pyramid in the outro) — this lesson completes the Pareto trio (stop coding → adopt your agent's perspective → template your engineering).

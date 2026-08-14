# TAC-8 · The Agentic Layer — Master Teaching Notes

> Source of truth for the expanded chapter. Video 63:19 · Advanced · Tactic #8: **Prioritize Agentics** — the final lesson and the compression of the whole course.
> Lesson artifact: five sibling codebases, each a working agentic layer at a different scale — from three near-empty directories (app1) to an agent living inside the product (app5).
> ⚠️ Capture note: the lesson video's screen content is live only to ~34:30; everything after (MCP demo payoff, the AEA demo, the recap, the final question) is audio-verified against the VTT, not frame-verified. Five lost beats are `diagram_instead` in the frame plan.

**Lesson thesis in one sentence:** Your codebase now has two layers — the application layer and the agentic layer (deterministic ADW code fused with non-deterministic agentic prompts) — and the irreplaceable engineer spends most of their time thickening the second so it operates the first, guided daily by one question: *am I working on the agentic layer or the application layer?*

**The chapter must land ten ideas.** Each below follows: Hook → Picture → Worked example (course codebase) → Dan's term → Failure mode → Retrieval Q.

---

## Idea 1 — Tactic #8: Prioritize Agentics (the tactic that contains all tactics)

**Hook.** Seven lessons, seven tactics — and the last one has "been staring us in the face the entire time." It isn't new machinery. It's an allocation decision you make every single day, and it decides whether you compound or plateau.

**Picture.** No usable tactic-card frame exists (spoken over B-roll); render the reveal as a designed card. Support with frame t0385 (6:25) — the `ls` of five app directories — as the "here's where we practice it" shot.

**Worked example.** The repo itself: five codebases where the application layer is deliberately boring (hello-world scripts, a tweets CSV, a demo SQL app) and every interesting file is agentic-layer. The lesson's time allocation mirrors the tactic's.

**Dan's term.** *Prioritize agentics — prioritize your agentic layer.* The ratio: "at least half" of engineering time, more when bootstrapping. The compression claim: "This tactic represents all others, from target zero-touch engineering all the way back to stop coding."

**Failure mode.** Agreeing in principle and then spending the week entirely in the application layer "because deadline." The tactic is behavioral, not attitudinal: if your calendar doesn't show agentic-layer hours, you don't practice it. (Dan's guardrail: deadlines are one of only three acceptable reasons — see Idea 9.)

**Retrieval Q.** What is Tactic #8, what time split does it prescribe, and what does Dan say it compresses? *(Prioritize agentics; ≥50% on the agentic layer; all other tactics, ZTE back to stop coding.)*

---

## Idea 2 — The two layers and the ring

**Hook.** Imagine a ring around your codebase. Thin at first. Every prompt you template, every workflow you script, thickens it — until machines that operate with your judgment are shipping your way, autonomously, in your product.

**Picture.** The ring exists on screen only as a green pixel animation over B-roll (~1:10) — `diagram_instead`: draw the two-layer ring (application core; agentic ring of prompts/plans/ADWs; triggers piercing the ring from outside).

**Worked example.** Every app in tac-8 enforces the split physically: `apps/` (or `app/`) is the application layer; `.claude/commands/` + `specs/` + `adws/` are the ring. app1's README states it as doctrine: "The Agentic Layer wraps your Application Layer, providing a programmatic interface for AI-driven development workflows."

**Dan's term.** *The agentic layer* vs *the application layer* — and he's deliberately vague about the second: DevOps, infrastructure, database, raw app — "it all goes under there." The definition (~50:20, audio): "the combination of traditional deterministic code stored in your ADWs directory… with the new non-deterministic agentic technology… the old world of deterministic code and the new world of agentic prompts."

**Failure mode.** Mixing layers: agent scripts inside the app, agents editing main without isolation. The separation isn't aesthetics — it's what lets the same ring shape wrap ANY application layer (Jupyter notebook in app2, Vue dashboard in app3, FastAPI product in app5), and what keeps the ring reusable while the app churns.

**Retrieval Q.** Give Dan's two-ingredient definition of the agentic layer and name what lives under "application layer." *(Deterministic ADW code + non-deterministic agentic prompts/LM; DevOps, infra, database, raw application.)*

---

## Idea 3 — The Minimum Viable Agentic Layer (app1)

**Hook.** What's the smallest agentic layer that's real? Three directories. Not a framework, not a platform — three directories and one rule.

**Picture.** Frame t0430 (7:10): app1's README with the MVAL tree — `specs/` (plans), `.claude/commands/` (prompts), `adws/` (workflows) — each line commented. Frame t0515 (8:35): the in-loop warm-up, /prime running.

**Worked example.** `tac8_app1__agent_layer_primitives`: five prompts (prime, start, chore, feature, implement), four ADW scripts over one core module, two hello-world app files. The one rule, verbatim: "The only thing that matters is that you can compose code and reference other files and have this be isolated from your application layer." Scripting language is explicitly free choice — UV Python (used all course), Bun TS, shell.

**Dan's term.** *Minimum viable agentic layer.* Also the pieces' roles: prompts are the atoms ("none of this works without the prompts"); ADWs "combine the old world of deterministic guaranteed code execution with the new world of agents"; plans are what planning prompts emit and building prompts consume.

**Failure mode.** Cargo-culting the scaled tree (hooks, triggers, state, worktrees, observability — app1's README shows it too) on day one. The lesson's growth model is thin-ring-first; the scaled tree is where you END after value compounds, not where you start.

**Retrieval Q.** Name the MVAL's three pieces and the single scripting-layer rule. *(adws/ + .claude/commands/ + specs/; any language that composes code, references files, and stays isolated from the app layer.)*

---

## Idea 4 — The gateway script (adw_prompt.py) and the observability contract

**Hook.** Somewhere in your codebase there's about to be a script that is categorically different from every other script you've ever written: it doesn't compute a result — it hires an intelligence and files a report about what happened.

**Picture.** Frame t0810 (13:30): adw_prompt.py's UV header + the rich **Inputs** panel (ADW ID `d2c20425`, agent `oneoff`, prompt, model `sonnet`, working dir, output path) for Dan's live run: *"list all files in the adws directory and a concise output of their purpose."*

**Worked example.** `adws/adw_prompt.py` → `adw_modules/agent.py`: builds `claude -p "<prompt>" --output-format stream-json --model sonnet --dangerously-skip-permissions`, with retry logic and a filtered subprocess env. Everything lands under `agents/{adw_id}/{agent_name}/`: `cc_raw_output.jsonl` (stream) → `cc_raw_output.json` (array) → `cc_final_object.json` (final message) → `custom_summary_output.json` (your own metadata view). Dan: "this layer of control is really important."

**Dan's term.** *The gateway into agentic coding.* "This ADW is calling an agent — this is distinctly different from any other type of code." Plus the forward pointer: the same call is available via the Claude Code SDK (Python/Bun) — app1 ships `agent_sdk.py` + `adw_sdk_prompt.py` — but TAC drives the CLI "to have full control over how the agent is called."

**Failure mode.** Dismissing it as a wrapper and skipping the output tour. The four output files are the debugging/observability substrate every later system (task boards, Notion factory, AEA) assumes. If you can't say what's in `cc_final_object.json` vs the summary, the multi-agent lessons will feel like magic instead of engineering.

**Retrieval Q.** What state does the gateway script manage around one agent call? *(Unique adw_id, retries, and agents/{adw_id}/{agent}/ outputs: JSONL stream, JSON array, final object, custom summary.)*

---

## Idea 5 — Template meta prompts: templating your engineering

**Hook.** The most leveraged file in tac-8 isn't code. It's a markdown file that writes markdown files — your engineering standards compiled into a form compute can execute.

**Picture.** Frame t0610 (10:10): chore.md open — Variables (adw_id, prompt), Instructions ("research the codebase starting with README.md"), and the **Plan Format** block. Frame t2065 (34:25): the specialized cousin, plan_uv_mcp.md, with its Workflow (`uv init --package --python 3.10`) and `ai_docs/mcp-python-sdk.md` reference.

**Worked example.** The Plan Format is the load-bearing part: metadata, chore description, relevant files, **step-by-step tasks executed top to bottom**, and **validation commands** — the plan ends by checking itself (feedback loops, encoded). /implement is a *higher-order prompt*: it takes the plan as `$ARGUMENTS`. Specialization ladder: generic `/plan` → `/chore`, `/feature` → app4's `/plan_uv_mcp`, `/plan_vite_vue`, `/plan_uv_script`, `/plan_bun_scripts` ("You will be able to outperform these by going more specific").

**Dan's term.** *Template meta prompts* — "prompts that output prompts in specific formats with specific rules, guidelines, files to read, conditional documentation." The design stance: "while you're building out your meta prompts, you want to be thinking from your agent's perspective — is this the engineering workflow you would use to solve the problem set at hand?" And the target: *problem classes, not one-off fixes.*

**Failure mode.** Writing prompts so specific they solve today's task once. The class test: at ~38:50 one concise prompt produces an entire working MCP server, and Dan declares "I have solved the problem class of building Astral UV model context protocol servers. I've solved it. It's done." If your template can't absorb a request you didn't anticipate, you templated an instance, not a class.

**Retrieval Q.** What makes a template meta prompt different from a good prompt, and what two sections make the Plan Format self-verifying? *(It generates another prompt (a plan) in a rigid format encoding your standards; step-by-step tasks + validation commands.)*

---

## Idea 6 — Composed ADWs: the chore→implement pipeline

**Hook.** Two prompts and forty lines of glue: that's your first real AI developer workflow — and the glue is where the guarantees live.

**Picture.** Frame t1131 (18:51): the money shot — **Planning Success** panel with the plan path, **Phase 2: Implementation** consuming that exact path as its argument, the generated spec (`chore-eae01d83-create-sh-version-main.md`) open in the editor, and `apps/main.sh` newly present in the tree.

**Worked example.** `adws/adw_chore_implement.py`: Phase 1 `execute_template(/chore [adw_id, prompt])` as agent **planner** → `extract_plan_path()` regex-parses `specs/chore-*.md` from the agent's report (the /chore prompt's Report section is a CONTRACT: "Return the path to the plan file created") → Phase 2 `execute_template(/implement [plan_path])` as agent **builder** → per-phase summaries + `workflow_summary.json`. Dan's on-camera run: "create a .sh version of main in apps/*" — deliberately overkill ("we don't need this much compute for a simple task") to demonstrate *complete control* over the workflow.

**Dan's term.** ADWs are "the highest abstraction level," the fusion of prompts with "the deterministic world of raw code," and "this begins infinite combinations and composables." He prefers the "nice explicit version" over clever chainable configs — "more readable, understandable for yourself, for your engineers, and most importantly for agents that you work with." Naming the pattern at scale (app2's variant): *an architect and an editor — ultra powerful pattern.*

**Failure mode.** Missing that the pipeline works ONLY because the meta prompt's report format is machine-parseable. Change /chore's Report section and the regex breaks — the deterministic and non-deterministic halves are coupled by explicit contracts. (Also: the composed ADW that can't fail loudly — app1's version exits nonzero and aborts phase 2 if planning fails.)

**Retrieval Q.** Trace the plan path through adw_chore_implement.py. *(/chore writes specs/chore-{adw_id}-{name}.md and reports the path per its Report contract; the script regex-extracts it; /implement receives it as its argument; both phases log under agents/{adw_id}/planner|builder.)*

---

## Idea 7 — Todone: a multi-agent system in a markdown file (app2)

**Hook.** No queue, no database, no framework: a markdown file and a 5-second cron loop — and suddenly seven agents are doing data-science chores in parallel while Dan narrates, hands off: "I'm not doing this, by the way."

**Picture.** Frame t1320 (22:00): tasks.md above the trigger's **Starting 7 Tasks** panel + "Creating Worktree". Frame t1400 (23:20): `[🟡, adw_id]` markers + one agent's Build Inputs panel. Frame t1540 (25:40): the full state vocabulary — ✅ with commit hashes, 🟡 in flight, ⏰ blocked. Frame t1720 (28:40): the sparse-checkout worktree opened as its own editor window.

**Worked example.** The state machine (README + update_task.md): `[]` pending → `[🟡, adw_id]` → `[✅ commit_hash, adw_id]` | `[❌, adw_id] … // Failed: reason`; `[⏰]` eligible only when EVERY task above it in its worktree is ✅ (a ❌ above blocks forever). Tags are per-task config parsed from `{…}`: `{opus}` upgrades the model; `{adw_plan_implement_update_task}` upgrades the workflow (build-update → plan-implement-update). The trigger (`adw_trigger_cron_todone.py`, default 5s, max 5 concurrent) does a cheap regex pre-check, then delegates PARSING to an agent — `/process_tasks` returns eligible worktree groups as strict JSON. Worktrees: `/init_worktree` = `git worktree add --no-checkout trees/<name> -b <name>` + cone sparse-checkout of only the app2 directory + `.env` copy + empty initial commit — "double isolation."

**Dan's term.** *Todone* (to-do → to-DONE), the *two-way task list* ("we're pushing past the overkilled chat-based UI"), *dedicated environments*, and the growth observation: your adws/ + prompts become "its own kind of micro codebase — a wrangle layer around your codebase," so engineer it properly and keep it out of apps/.

**Failure mode.** Writing one giant task and never touching tags or ⏰ — you get a to-do list with extra steps instead of an orchestrator with dependencies, model routing, and workflow routing. Second failure: skipping the validation pass; Dan physically opens `trees/enhance-training-data`, greps `tweets_positive_only.csv` for `negative` (zero hits), and only then trusts the ✅.

**Retrieval Q.** Full state machine of tasks.md including blocking, and what the two tags do. *(See above; {opus}=model, {adw_plan_implement_update_task}=workflow tier.)*

---

## Idea 8 — Out-loop factories: PITER on a Notion board (app4)

**Hook.** The prompt input for your next application doesn't have to live in a terminal. Dan's lives in a Notion card — and a cron job builds the app while he's on his phone.

**Picture.** Frame t1835 (30:35): the **Agentic Prototyper** board — four prototype tasks, one card open showing `workflow:plan prototype:vite_vue` + `execute`. Frame t2065 (34:25): the /plan_uv_mcp specialized template. (The board's five-column zoom-out and the MCP payoff are in the frozen-video region — design cards for them.)

**Worked example.** `adw_trigger_cron_notion_tasks.py` polls every 15s (`--once` for testing — Dan uses it on camera): eligible = status *Not started* or *HIL Review* + trigger word `execute` (or `continue - <prompt>` for iteration); claims instantly (status→In progress + adw_id) to prevent double-pickup; `{{prototype: uv_script|vite_vue|bun_scripts|uv_mcp}}` routes to the matching specialized planner; `/make_worktree_name` (a one-purpose agent with a strict output contract: ONLY the name) → `/init_worktree` → plan → implement → `/update_notion_task` writes results + commit hash back. Agents spawn as `subprocess.Popen(start_new_session=True)` — detached, parallel, monitor-restart-proof. Payoff (audio region): the system-info MCP server — `.mcp.json` wired, `get_memory_info`/`get_cpu`/`get_disk` called live from Claude Code — from ONE concise prompt.

**Dan's term.** *PITER, applied*: "Prompt input — for us, it's this Notion page. Environment — the trees directory… And then we have the review system" (the board's Not started / In progress / **Human in the loop review** / Failed / Done columns + live status updates). Plus the velocity claim: "Look at our velocity. Our velocity is absolutely mind-blowing."

**Failure mode.** Assuming the review column is bureaucracy. HIL Review + `continue - <prompt>` is the iteration loop — the mechanism that lets you steer a factory without entering the loop. Skip it and your out-loop system is fire-and-forget, which is fire-and-regret at scale. Second failure: vague prototype cards ("build me a website") — the README's own anti-patterns.

**Retrieval Q.** Map PITER onto app4 and name the claim mechanism that prevents duplicate work. *(Prompt input=Notion card; Trigger=15s cron; Environment=trees/ worktrees; Review=board columns+updates. Instant status flip to In progress with adw_id.)*

---

## Idea 9 — One agent, one prompt, one purpose — and the AEA exception (app5)

**Hook.** The most controversial rule in TAC ends with a confession: Dan breaks it exactly once, on purpose, inside his own product — to put an agent IN the app.

**Picture.** Both AEA frames are lost to the capture freeze — design a mock: the NLQ-to-SQL app with two chat windows ("Nexus", "Roon"), the Cmd+P dev console (`/aea`, `/list`, `/toggle-view`, `/close-all`), annotated with the flow client → AEA server (port 8743) → SQLite (agent_id, cc_session_id, conversation) → `adw_aea_patch.py` → `claude -p … --resume <cc_session_id>`.

**Worked example.** Every other agent in the whole course is one Claude instance, one prompt, one purpose — "focused agents, focused context windows, that are reproducible and easily testable, validatable, and improvable." app5's AEA server is the sanctioned exception: it persists `cc_session_id` and passes it back with `--resume`, because a conversational product agent NEEDS continuity across prompts, refreshes, and server restarts. The demo (audio region): `/aea` → Nexus answers "what is this codebase about?" while a second agent Roon renames the Generate-Random-Query button — parallel, in-product. "The power of agents isn't in one, it's in many."

**Dan's term.** *One agent, one prompt, one purpose*; *AEA — agent embedded application*; and the reframe: "we have a dedicated agent-embedded application server so that we can access this outside the loop. In this case, outside the loop is inside the application." Rule-breaking is explicit: "We broke one of our rules."

**Failure mode.** Two symmetric ones: treating the rule as optional (sprawling multi-topic mega-agents whose context windows can't be reproduced or tested) — or treating it as absolute (refusing session continuity even where the use case demands it). The lesson models the discipline: break the rule once, knowingly, with the mechanism (DB-persisted session id) engineered for it.

**Retrieval Q.** State the rule, why it exists, and the single exception with its mechanism. *(Focused/reproducible/testable context windows; app5 AEA resumes conversations via stored cc_session_id + --resume.)*

---

## Idea 10 — The compression: KPIs → PITE → one question

**Hook.** The course ends by deleting itself: eight tactics, twelve leverage points, four KPIs — compressed into one question you ask every day, and one letter you eventually drop.

**Picture.** All in the frozen-video region — design three cards: the KPI quad (attempts ↓, size ↑, streak ↑, presence → 0); PITER→PITE with the R crossed out and replaced by encoded feedback loops; and the full-bleed final question.

**Worked example.** The recap runs the whole stack against the codebases you just used: feedback loops = the validation commands in every Plan Format ("There is a validation, a set of validations in your codebase that once run ensures everything works perfectly — the only question is, do you know what it is?"); ZTE = ship a dialed-in ADW until "the time you spend reviewing the work will be useless… you realize you're the bottleneck," then PITER→PITE. The final question (~52:39): **"Am I working on the agentic layer or am I working in the application layer?"** — with exactly three acceptable reasons to answer "application": a deadline, testing something, or running prompts in-loop to verify they'll work out-loop. Anything else is "moving sideways while other engineers move up." Closing frame of the whole course: "When the agents arrived, something changed. We weren't just AI coding anymore. We started orchestrating intelligence."

**Dan's term.** *The final question / final meta tactic*, teased at ~2:14 as "the oil of this course." Plus the economic stakes: *the commoditization of implementation* ("with agentic coding, not only is code a commodity, but the implementation as well"), value moving up the stack (system design, domain encoding, quality control, creative problem decomposition — "which you'll then encode in your ADWs"), and the identity: "An agentic engineer operates on living pieces of software that work while they sleep."

**Failure mode.** Answering the question once, at course end, instead of daily at sit-down. And the ego failure Dan names twice: believing you can outperform "your team's best engineering practices encoded into a template metaprompt that runs in an ADW that kicks off five to ten agents per problem… don't try to compete with that — your place of competition is now net new innovation."

**Retrieval Q.** The final question, the three exemptions, and the PITE prerequisite. *(See above; drop the R only after feedback loops + reliability streaks prove review is the bottleneck.)*

---

## Timeline map (VTT-verified; ⚠ = audio-only in this capture)

| Time | Beat |
|---|---|
| 0:00–3:00 | Cold open: final lesson; ring metaphor (~1:05); build-the-system-that-builds-the-system = agentic layer; guiding-question teaser ("the oil of this course," 2:14) |
| 3:00–4:31 | **Tactic #8: Prioritize Agentics** (3:01, 3:16); ≥50% time; agentic vs application layer |
| 4:31–6:07 | Primitives over tools; Claude Code first-not-last; "not a Claude Code course" |
| 6:07–6:39 | Clone tac-8; `ls` → five apps (6:21) |
| 6:39–9:36 | app1: README MVAL (7:00); /prime (8:29); /start; V1 prompt set |
| 9:36–11:54 | /implement higher-order prompt (9:36); templates=meta prompts (9:49); Plan Format (10:02); agent's perspective; problem classes; chore vs feature; 12 leverage points (11:38) |
| 11:54–16:00 | ADWs = highest abstraction (11:54–12:32); adw_prompt.py gateway (13:13–13:39); SDK aside; success output; adw_slash_command /start (14:46); moving out the loop (15:01); "terrible place to stay"; parabolic ROI (15:38) |
| 16:00–16:38 | Feedback loops mention (16:00); extraction-logs tour (JSONL/array/final/summary) |
| 16:38–19:30 | adw_chore_implement (16:38); run "create a .sh version of main in apps/*"; plan → main.sh (18:51) |
| 19:47–21:23 | app2 Todone: Jupyter sentiment app layer; tasks.md; paste 5-worktree task set |
| 21:23–23:30 | Trigger = how you stay out the loop (21:23); 5s poll (21:48); **Starting 7 Tasks** (21:55); worktrees; tags {opus}/{adw_plan_implement_update_task} (22:34–22:50); two-way task list; 🟡+hash markers (23:16) |
| 23:30–28:14 | Work rolls in; ✅/⏰ semantics (~25:40); /build quick patch vs plan-implement (architect+editor, ~27:10); micro-codebase/wrangle layer (27:45) |
| 28:14–29:50 | Validate: trees/ sparse checkout (28:37); tweets_positive_only; stacked work |
| 29:50–31:43 | Skip app3 (29:50); app4 agentic prototyping (30:03); Notion board (30:19–30:31); PITER mapped (30:54); 15s notion cron (31:26–31:38); --once (31:43) |
| 31:43–34:30 | Find prompts by "/"; notion task claimed agentically (32:17); primitives recap; /plan_uv_mcp specialized meta prompt + ai_docs (34:11) |
| ⚠ 34:30–39:50 | Board columns zoom-out (~35:30); MCP sysinfo done (36:40); trees/feat-mcp-sysinfo; .mcp.json; get_memory_info/cpu/disk live (38:01); "solved the problem class" (38:50); loot box pointer (39:29) |
| ⚠ 39:50–43:00 | app5: start.sh + aea_server_start.sh; Cmd+P /aea → Nexus (40:27–40:32); "power of agents isn't in one, it's in many" (40:38); Roon (40:45); parallel Q&A + button rename; "broke one of our rules"; AEA server; outside the loop is inside the application |
| ⚠ 43:00–50:15 | Recap: stop coding (43:34); core four; 12 leverage points; template your engineering; KPIs (attempts/size/streak/presence); stay out the loop (46:19); always add feedback loops (46:27–47:50); one agent one prompt one purpose (47:53) + the exception (48:20); ZTE (48:56); PITER→PITE (49:21) |
| ⚠ 50:15–53:57 | Agentic layer defined (~50:20); don't compete with your templated practices (51:30); **the final question** (52:39); orchestrating intelligence (53:16); "no competing with an agentic engineer" (53:40) |
| ⚠ 53:57–63:19 | Daily thought pattern; aha moments (teammate runs your ADW); users/product/company constant; living software (55:34); commoditization of implementation (56:39–56:57); value up the stack; manifesto/codex (57:45–57:52); share ask (58:37); YT cadence; the closing line (1:02:20, repeated 1:03:07) |

## Terminology glossary (Dan-isms, canonical spellings)

- **The agentic layer** — deterministic ADW code + non-deterministic agentic prompts, wrapped as a ring around the application layer
- **The application layer** — everything classical: app, database, infra, DevOps
- **MVAL (minimum viable agentic layer)** — adws/ + .claude/commands/ + specs/
- **Template meta prompt** — a prompt that generates a prompt (a plan) in a rigid format; *plan format* is its load-bearing section
- **Higher-order prompt** — a prompt that takes another prompt/plan as an argument (/implement)
- **The gateway script** — adw_prompt.py; the smallest ADW: one prompt, managed state
- **ADW** — AI Developer Workflow; "the highest level of composition — code plus agentics"
- **Todone** — app2's to-do→to-DONE multi-agent task system; tasks.md is a *two-way task list*
- **Trigger** — the mechanism that fires ADWs without you (cron over tasks.md, Notion poller, webhook, AEA server)
- **PITER / PITE** — Prompt input, Trigger, Environment, Review — until you drop the R (ZTE)
- **One agent, one prompt, one purpose** — the reliability rule; exception: AEA session resume
- **AEA** — Agent Embedded Application (app5); agents living inside the product
- **Problem class** — the unit of agentic-layer work (vs one-off fixes)
- **Agentic KPIs** — attempts ↓, size ↑, streak ↑, presence → 0
- **ATL** — the header of app2's tasks.md (Agentic Task List)
- Transcript corrections: "Cloud/clog code"→Claude Code; "bond run"→bun run; "Prong trigger"→cron trigger; "sjson array"→JSON array; "feet MCP"→feat-mcp-sysinfo; "agents to glare"→agentic layer; "Peter/Pete"→PITER/PITE

## Bridge out of TAC (as stated in-lesson)

- The guiding question is the durable takeaway: ask it daily; ≥50% agentic layer
- Every codebase is a starting point, not a framework: "these are all example starting points… build it any way you want" — invariants are isolation, composability, observability, feedback loops
- Post-course: share-the-course ask; course-completion survey steers Dan's next builds; Monday YouTube cadence for current-generation ideas
- The era claim to carry forward: implementation is commoditizing; encode your judgment in ADWs and compete on net-new innovation

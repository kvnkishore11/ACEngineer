# TAC-2 · The 12 Leverage Points — Master Teaching Notes

> Source of truth for the expanded chapter. Video 47:14 · Beginner (exit ramp to intermediate) · Tactic #2: **Adopt Your Agent's Perspective**
> Lesson artifact: a real two-service app (FastAPI + Vite/TS natural-language→SQL interface) with a planted bug, three slash commands, a 749-line spec, mirrored tests, and empty `adws/` + `agents/` placeholder dirs waiting for the rest of the course.

**Lesson thesis in one sentence:** Agentic coding success is not luck — it is the stacked effect of 12 nameable leverage points (the core four *in* the agent + eight levers that flow *through* it), applied by an engineer who consistently adopts the agent's perspective and measures improvement with four KPIs: size up, attempts down, streak up, presence down.

**The chapter must land twelve ideas.** Each below follows: Hook → Picture → Worked example (course codebase) → Dan's term → Failure mode → Retrieval Q.

---

## Idea 1 — The framework bet: a compressed SDLC for phase two

**Hook.** Tools churn weekly; models leapfrog monthly. What do you bet a career on? Dan's answer: the things that *don't* change. "When there are massive trend shifts and revolutions in the tech industry… you can see the aspects that never change and you can place big bets on them." The aspect resurfacing in a big way is the oldest one in the book: the software development lifecycle.

**Picture.** ~1:56 — the five-circle SDLC slide: 1 Plan → 2 Code → 3 Test → 4 Review → 5 Document. (Simple enough to re-render as a designed diagram; see frame plan `diagram_instead`.)

**Worked example.** The lesson repo already embodies the five steps: `specs/init_nlq_to_sql_to_table.md` (plan) generated `app/` (code), which is checked by `app/server/tests/` (test), inspected live in the demo (review), and explained by `README.md` + `ai_docs/` (document).

**Dan's term.** The *phase two SDLC*: **plan, code, test, review, document** — "this compressed, focused version of the software development lifecycle is built for phase two of the generative AI age." Over the next seven lessons TAC augments and automates its steps "so that your agent ships on your behalf… We're here to dial up the autonomy knob all the way to 11."

**Failure mode.** Treating the SDLC framing as filler and skipping to the leverage points. The 12 points only cohere because several of them (plans, tests, documentation, review-ish stdout) *are* SDLC nodes — Dan says exactly this at the end: "notice how some of the leverage points are the node in the software developer lifecycle." Students who miss the mapping memorize a flat list instead of a system.

**Retrieval Q.** Name the five steps of the phase-two SDLC and the reason Dan bets on it. *(Plan, code, test, review, document; it's an aspect of engineering that never changes, so it survives tool and model churn.)*

---

## Idea 2 — Tactic #2: Adopt Your Agent's Perspective

**Hook.** Your agent is *brilliant, but blind*. Every new session boots a blank instance: no context, no memories, no awareness beyond what you hand it — and when the work is done it resets to zero. If you want it to perform like you across your codebase, it needs *your* perspective.

**Picture.** Frame t0183 (3:03): the official tactic card — "Adopt Your Agent's Perspective" — with its Daily Actions sidebar: give the agent the context/model/prompt/tools it needs; ensure clear logging and standard output; use types and consistent architecture; write tests so it can self-validate; equip it with what YOU would need to do the job.

**Worked example.** The tactic's litmus question (from the slide): *"Whenever you launch your agent, ask yourself: With my agent's core four (context, model, prompt, tools), is it possible to complete the task I've given it?"* The whole stdout demo (Ideas 5–6) is this question failing and then being made to pass.

**Dan's term.** *Adopt your agent's perspective* — "Your agent needs your context, your model, your prompt, and your tools — the core four… By consistently adopting your agent's perspective you close the gap between what you can do and what your agent can do." And the promotion this unlocks: "It's not about what you can do anymore. It's about what you can teach your agents to do."

**Failure mode.** Anthropomorphizing continuity: assuming the agent "remembers" yesterday's session, the open browser tab, or the error you can see on your screen. Agents are ephemeral; anything not in the context window does not exist. The `/prime` command exists precisely because of this — weak students skip priming and then blame the model.

**Retrieval Q.** State Tactic #2, the three-word diagnosis that motivates it, and the litmus question. *(Adopt your agent's perspective; "brilliant, but blind"; with my agent's core four, is it possible to complete the task I've given it?)*

---

## Idea 3 — The 12 leverage points: in-agent vs through-agent

**Hook.** "How can you give your agent everything it needs to succeed?" Not by vibes — by a checklist of exactly 12 levers. Stack them and "agentic coding success becomes inevitable." Skip them and you'll be iterating forever.

**Picture.** Frame t0345 (5:45): the money slide — **12 Leverage Points of Agentic Coding**. Top row, *In-Agent (Core Four)*: Context (system prompts and conversation history) · Model (LLM selection and configuration) · Prompt (user instructions and queries) · Tools (available functions and capabilities). Bottom rows, *Through-Agent*: Standard Out (response from commands and logging) · Types (types, schemas, classes, errors, and structures) · Documentation (3rd party and internal) · Tests (self-validating feedback loops) · Architecture (codebase structure) · Plans (detailed prompts for massive work) · Templates (reusable, embeddable, agentic prompts) · ADWs (AI Developer Workflows).

**Worked example.** Every through-agent lever has a concrete artifact in `tac-2`: stdout → the missing-then-added `print()`s in `app/server/server.py`; types → `core/data_models.py` mirrored by `client/src/types.d.ts`; documentation → `README.md` + `ai_docs/`; tests → `app/server/tests/`; architecture → the `app/client` / `app/server` split; plans → `specs/init_nlq_to_sql_to_table.md`; templates → `.claude/commands/`; ADWs → the empty `adws/` dir (and `claude -p`), deliberately left as the course's destination.

**Dan's term.** *In-agent* leverage points "are in the agent because they're always with your agent — context, model, prompt, tools." *Through-agent* leverage points are "external levers that eventually interact with your agent that have massive impact on your success. They typically flow through the context window."

**Failure mode.** Learning the list as trivia instead of as a *diagnostic*. The KPI section closes the loop: when a one-shot fails, the assignment is to name which leverage point was missing (dictionaries instead of types? no stdout? no tests? no plan?). A student who can't run that diagnosis hasn't learned the lesson, however well they recite the twelve.

**Retrieval Q.** Name the two families and all 12 points. *(In-agent: context, model, prompt, tools. Through-agent: standard out, types, documentation, tests, architecture, plans, templates, ADWs.)*

---

## Idea 4 — Tools you can't name are leverage you can't use

**Hook.** Did you know Claude Code's Bash tool takes a timeout parameter? Dan did — and twenty minutes later that one fact is what lets him run a live server *inside* the agent for five minutes. "There are many little hidden kind of secrets inside of every single tool."

**Picture.** Frame t0630 (10:30): the `/tools` output as a Core Tools list — `Task` (launch agent for keyword/file searches), `Bash(command, description?, timeout?)`, `Glob`, `Grep`, `LS`, `Read`, `Edit`, `MultiEdit`, `Write`, then Specialized (NotebookRead/NotebookEdit, WebFetch, WebSearch), Task Management (TodoRead/TodoWrite), Workflow Control (exit_plan_mode).

**Worked example.** `.claude/commands/tools.md` is two lines: *"List all core, built-in non-mcp development tools available to you. Display in bullet format. Use typescript function syntax with parameters."* Because the tools live in the agent's system prompt, the agent itself is the documentation — you just have to ask. Dan reads the list like an engineer reading an API: delegation tools, bash tools, reading, writing, web tools — "notice how these represent the essential engineering commands. They can CRUD — create, read, update, delete — a codebase just like you and I can." MCP servers get a one-line teaser: arbitrary tools, "several mission critical MCP servers in future lessons."

**Dan's term.** "We need to see what our agents can see. We need to know what they can do… if you don't know the tools your agent can use, you can't maximize your agent to its highest capability."

**Failure mode.** Never reading the tool definitions, then (a) under-using the agent (babysitting a terminal outside it because you didn't know Bash had a timeout) or (b) being surprised by what it does (Task fires a subagent — students who don't know that misread the type-trace demo entirely).

**Retrieval Q.** What does the `Task` tool do, what hidden Bash parameter did Dan exploit, and where do Claude Code's tools live? *(Task launches a subagent for keyword/file searches; Bash's `timeout` — used as 300s to run the start script inside the agent; the tools are embedded in the system prompt, so you can ask the agent to list them.)*

---

## Idea 5 — Standard out: your agent can only see what you let it see

**Hook.** Dan drags `orders_(32).csv` into the app. The browser flashes "Error converting CSV to SQLite: near "(": syntax error." A human can read that. Now the only question that matters: *can the agent?* Flip to the server terminal: nothing. Silence. "Not only do we have bad code, we have bad agentic code."

**Picture.** Frame t0715 (11:55): the browser error with the syntax fragment highlighted. Frame t0835 (13:55): the after — green diff lines adding `print(f"[ERROR] …")` and `print(f"[SUCCESS] Table deleted: …")` across every endpoint, with the agent's summary: "Updated server.py to print detailed exception information and successful response details for all endpoints."

**Worked example.** The committed repo really is the before-state: `app/server/server.py` contains **zero** `print()` calls; every endpoint catches exceptions and stuffs `error=str(e)` into the response model, so failures surface only in the browser. The planted trap is real too: line 60 derives `table_name` from the filename replacing only spaces, so `orders_(32).csv` → table `orders_(32)`, and `core/file_processor.py:26` runs `PRAGMA table_info(orders_(32))` — an SQLite syntax error. Sample data ships all three files (`products.csv`, `users.json`, `orders_(32).csv`); the third one *is* the lesson.

**Dan's term.** *Standard out* — "the response from any command you run… it's all standard out. This means that clear logging throughout your applications, your commands and your scripts can guide your agent to success." Plus the overload escape hatches for real codebases: a per-session log file the agent reads after the fact; cleaned-up logs; or warn/error-only levels — with the caveat that "warnings and errors are only part of the story," and the payoff that top-level visibility "drastically reduces the state space" the agent must search.

**Failure mode.** Logging for humans instead of agents: pretty UI toasts, dashboards, or a logging service the agent process can't read. If the text never reaches a stream the agent sees (its terminal, a file it can open), it's invisible. Corollary weak-student move: skipping the re-upload that *proves* the error now traces to stdout.

**Retrieval Q.** What made the server "bad agentic code," and what exactly is the planted bug? *(Endpoints swallowed exceptions into response fields with no stdout trace, so the agent couldn't see failures; the upload path only replaces spaces in filenames, so `orders_(32).csv` becomes table name `orders_(32)`, which breaks `PRAGMA table_info` at file_processor.py:26.)*

---

## Idea 6 — Fix the system, not the bug

**Hook.** Here's the twist that separates this from every debugging tutorial you've seen: Dan *knows* the bug. He could fix it in thirty seconds. He deliberately doesn't. "I'm not actually fixing the issue. I'm setting up my codebase so that my agent can resolve the issue."

**Picture.** Frame t0965 (16:05): the agent, having watched the server's stdout, answers "any issues with the server?" with a precise diagnosis — SQL syntax error in `app/server/core/file_processor.py:26`, `PRAGMA table_info({table_name})`, table names with unsanitized parentheses. Companion moment (17:50–18:15, unframed): Dan re-runs everything and the fixed app answers "latest delivery."

**Worked example.** The full closed loop, step by step: (1) new agent, `/prime`; (2) `@app/server/server.py` + "make sure every exception prints all exception details, make sure every successful response prints before returning" — YOLO/auto-accept mode on, "we don't want to be constantly watching"; (3) restart services, re-upload, error now traces to stdout; (4) fresh agent, `/prime`, then `sh ./scripts/start.sh, 300s` — the server now runs *inside* the agent (the Bash-timeout secret from Idea 4), so its stdout lands directly in the context window; (5) reproduce the error in the browser; (6) prompt: "any issues with the server?" → exact diagnosis; (7) prompt: "resolve: replace bad chars and escape" → the agent writes `sanitize_table_name()` into `file_processor.py` (21 additions: strip extension, `re.sub` bad chars to underscores, ensure leading letter/underscore, never empty); (8) rerun, re-upload — table lands as `orders__32_`-style sanitized name, queries work. Two short prompts fixed the bug — *because the system had been set up first*.

**Dan's term.** "We're building up a system for our agent to solve problems… We're updating our codebase to communicate information to our agent." And the mindset shift stated at KPI time: "Are you still manually looking at error messages? Stop… Give them to your agent. And only when your agent fails do you take your precious time and dig into the error."

**Failure mode.** Two: (a) hand-fixing the planted bug — you get a working app and learn nothing; (b) prompting "fix the CSV upload bug" *before* stdout exists — the agent flails, and the student concludes agents can't debug, when the actual failure was a missing leverage point (exactly the diagnosis drill from Idea 3).

**Retrieval Q.** Reproduce Dan's two prompts and explain why they worked. *("Any issues with the server?" then "resolve: replace bad chars and escape." They worked because the server ran inside the agent with full stdout visibility — the fix to the SYSTEM (logging + agent-run server) preceded the fix to the bug.)*

---

## Idea 7 — Types are IDKs: information dense keywords

**Hook.** You've done this by hand a hundred times: copy a class name, search the repo, follow the hits to understand a feature. Dan's reframe: that search trail is a *story about how information travels* — and now your agent can read it too.

**Picture.** Frame t1220 (20:20): the clean-instance demo's final answer — `DatabaseSchemaResponse` traced through `app/server/core/data_models.py` (Pydantic definition) → `app/server/server.py` (FastAPI endpoint) → `app/client/src/types.d.ts` (mirrored TS interface) → `app/client/src/api/client.ts` (`getSchema()`) → `specs/init_nlq_to_sql_to_table.md` (spec reference), capped by the one-line flow summary — produced by a `Task` subagent in 7 tool uses / 26.7k tokens / 59.2s.

**Worked example.** All five locations are literally true on disk (grep confirms: `data_models.py:47`, `server.py:121–150`, `types.d.ts:43`, `client.ts:60–61`, spec lines 169/251/308). The client file even opens with the comment "These must match the Pydantic models exactly" — the type contract crossing the language boundary. Dan runs this from a *brand-new* Claude instance on purpose: zero conversational context, pure codebase leverage. Prompt shape worth copying: "show me how this type flows throughout the application, detail functions, files, and purpose" + an output format sketch (`file: function: purpose…`) the model can continue.

**Dan's term.** *Types are IDKs — information dense keywords.* "They point to exact locations in your codebase and represent the flow of a specific type of information." Scope note: "when I say types, I'm talking about classes, exceptions, interfaces, and all typing structures that represent a concrete piece of information." Contrast names Dan mocks on camera: `QueryRequest`/`QueryResponse` — "not that good"; a hypothetical `DataRequest` — "terrible, terrible name… If your agent ever wants to search for data or just request, it's cooked."

**Failure mode.** Generic naming that destroys searchability (the agent greps `data` and drowns), and dict-passing codebases where no type exists to trace at all — Dan's first KPI-section example: "does your agent get confused because your codebase is using dictionaries instead of types? Leverage types."

**Retrieval Q.** What does IDK stand for, and through which five files does `DatabaseSchemaResponse` flow? *(Information dense keywords; data_models.py → server.py → types.d.ts → api/client.ts → specs/init_nlq_to_sql_to_table.md.)*

---

## Idea 8 — Architecture and the agent navigation problem

**Hook.** Open `app/`. Two folders: `client`, `server`. Dan: there's an architectural decision "looking right at us" that "cuts all possibilities in half for our agent." One directory boundary = half the search space gone before a single file is read.

**Picture.** Frame t1552 (25:52): the explorer with `server/core` (data_models, file_processor, insights, llm_processor, sql_processor) and `tests/core` (test_file_processor, test_llm_processor, test_sql_processor) side by side — the mirrored structure circled.

**Worked example.** Dan's consistency checklist, each item auditable against this repo: clear entry points (`server.py`, `main.ts`); constant files for unchanging information; types/classes/structures (`data_models.py`); meaningful, verbose IDK names; files under ~1000 lines (biggest file here: `main.ts` at 415); agent-facing markdown spread through the tree (READMEs / CLAUDE.mds "whatever the agent specific documentation file is"); separated services (`client` | `server`); one responsibility per file (`file_processor` / `sql_processor` / `llm_processor` / `insights`); tests mirroring source structure. The checklist ships as a loot-box note.

**Dan's term.** *The agent navigation problem* — "Every time you boot up a new agent, it has to explore the codebase… Your architecture stacks up very, very quickly for you or against you." The principle: "If it's hard for you, you should assume it'll be hard for your agent," and the antidote: "consistency is a powerful actor against complexity for both humans and for agents." Plus the economic frame: agents boot "hundreds and thousands of times," so navigation cost is a multiplier on everything; build codebases that are "token efficient."

**Failure mode.** Two opposite ones: (a) ignoring architecture because "the agent will figure it out" — it will, expensively, every single boot; (b) hearing the sermon and immediately launching a hand-refactor — Dan explicitly says **"don't refactor yet"**: future lessons organize agentic assets *with* your agent. The drill for now is awareness, not surgery.

**Retrieval Q.** What is the agent navigation problem, which single decision halves this repo's search space, and what is Dan's stated antidote to complexity? *(Every fresh agent must re-navigate the codebase from zero; the client/server split; consistency — same patterns, folder structures, names, comment structure.)*

---

## Idea 9 — Documentation: two kinds, and a folder just for agents

**Hook.** Why does this repo vendored-copy two API quickstarts (`ai_docs/anthropic_quick_start.md`, `ai_docs/openai_quick_start.md`) that are one web search away? Because "you don't want them making web requests every time they have to look something up. Just get it local."

**Picture.** No dedicated frame (talking-head + brief tree glances); the chapter should render a small two-column internal/external doc diagram. `ai_docs/` contents are visible in the t0400 tree.

**Worked example.** Internal documentation: `README.md` (153 lines — setup, commands, structure, endpoints, security, troubleshooting) is what `/prime` reads to ramp any fresh agent. External documentation: `ai_docs/` holds third-party knowledge (OpenAI + Anthropic quickstarts, 311 + 180 lines) pre-fetched for offline, in-context use when writing plans or code against those APIs. Related tools get a namecheck: RepoMix and git tools for pulling open-source codebases in; Claude Code's own WebFetch/WebSearch ("this is just a critical tool for engineering, which is why they baked it in").

**Dan's term.** "There are two types: internal documentation and external documentation. AI docs is a dedicated folder specifically for our agents." Docs get a whole later lesson ("we have an entire lesson dedicated to docs, tests, and plans"), and the `/prime` + "claude.md" combo is named as how agents ramp up fast.

**Failure mode.** Note the accuracy trap: Dan *mentions* the CLAUDE.md convention on camera, but tac-2 ships **no CLAUDE.md file** — the README + prime command carry that role here. Weak students go looking for a file that isn't there (or worse, assume docs = whatever's in the model's training data and keep nothing local, paying web-fetch latency and drift on every plan).

**Retrieval Q.** What are the two types of documentation, and what is `ai_docs/` for? *(Internal — README/CLAUDE.md-style codebase docs; external — third-party docs; ai_docs is the local, agent-dedicated folder of external docs so agents don't need web requests mid-task.)*

---

## Idea 10 — Tests: the self-validation leverage point

**Hook.** "Your agent will make mistakes, okay — just like you. The only question is: does it have the right leverage it needs to correct the mistakes?" Tests aren't quality theater anymore; they're the agent's error-correction machinery.

**Picture.** ~28:25 (unframed; terminal moment): Dan types `!` to drop into bash mode, `cd app/server`, `uv run pytest` — the whole test run's output streams straight into the agent's context.

**Worked example.** `app/server/tests/` ships 621 lines across `test_file_processor.py`, `test_llm_processor.py`, `test_sql_processor.py`, mirroring `core/`'s layout, with an `assets/` folder of fixture files (including `invalid.csv` — malformed rows for failure-path testing). Tests print to stdout, so "all the output just ran and fed right into our agent" — pass or fail, the agent sees it. Chain it with Idea 6: after the agent adds new functionality, it can run the tests and improve immediately.

**Dan's term.** *Self-validating loops* / *closed loop structures* — "This is where we let our agent write the code itself by getting a concrete feedback loop." The era-defining line: "This used to be a negotiable… That time has completely passed. **If you're not writing tests, you're probably vibe coding.**" Priority guidance: backends are the easiest, highest-leverage place to start; tests are "probably the first leverage point you should go after right next to standard out"; frontend testing (agents clicking buttons, seeing results) is promised for later lessons.

**Failure mode.** Running tests yourself, reading the output yourself, then telling the agent what failed — a human-in-the-middle loop that throws away the leverage. The loop closes only when the *agent* runs the tests and reads the results. Also: skipping tests "because it's a demo app" — which is precisely the vibe-coding Dan is calling out.

**Retrieval Q.** What are closed-loop structures, and what's Dan's one-liner about engineers who skip tests? *(Structures where the agent validates its own work via concrete feedback — e.g. running tests and reading stdout; "if you're not writing tests, you're probably vibe coding.")*

---

## Idea 11 — Plans → Templates → ADWs: the abstraction ladder

**Hook.** Three leverage points left, and they're a ladder. A plan communicates one big batch of work. A template makes a prompt reusable. An ADW wraps prompts in code and a trigger so the work runs *without you*. Top of the ladder = "your codebase literally runs itself."

**Picture.** Frame t1812 (30:12): `specs/init_nlq_to_sql_to_table.md` open — project overview, tech stack, MVP core flow, architecture tree. Frame t1980 (33:00): the terminal after `claude -p "/tools"` — the full tool list printed and control returned to the shell prompt. Companion beat (42:50, unframed): `claude` then `/start` booting the server from a student-created command.

**Worked example.** *Plans:* the spec is 749 lines (Dan: "some 750 lines long… there is no way that I sat here and typed out 700 lines of a plan") — code examples, front/back-end types, architecture. It bootstrapped this entire codebase, and lesson 3 teaches planning *with* your agent (meta-prompting, higher-order prompts). *Templates:* `.claude/commands/` ships three — `install.md` (7 lines, whose body reads-and-executes `prime.md`: "running prompts inside of prompts… no different than passing a function inside of a function"), `prime.md` (run `git ls-files`, read `README.md`, summarize), `tools.md` (2 lines). The three-time rule mints new ones: Dan copies `sh ./scripts/start.sh 300s` into a new `.claude/commands/start.md` on camera, then `/start` just works. *ADWs:* "created when you combine one or more agentic prompts right out of the commands directory, and then you wrap it in arbitrary code, and then you kick it off autonomously with a trigger." Demo seed: `claude -p "/tools"` — programmable mode, "do this work, call this command, whatever happens, return the result." The `adws/` and `agents/` dirs sit empty in the repo — scaffolding for where the course is going.

**Dan's term.** "Put simply, plans are just prompts. Put accurately, plans are how you communicate massive amounts of work to your agent." · "The plan is the prompt… great planning is great prompting." · Templates "are just reusable prompts… to use our precise language, these are agentic prompts." · "Three time makes a pattern. Three time should trigger your engineering brain. Automate." · ADWs are "the highest level of abstraction… This is where real engineering work can happen autonomously."

**Failure mode.** Ladder inversions: hand-typing plans (the point is agent-drafted plans you review); hoarding one-off prompts in a notes app instead of committing commands to the repo where every future agent (and teammate) can fire them; or chasing ADWs before the primitives work — "we must know how to fire off a single powerful agent running a single prompt… Master the primitives and you'll master the compositions."

**Retrieval Q.** Define an ADW precisely, and give the two formulations of "plans." *(ADW = one or more agentic prompts + arbitrary code wrapper + an autonomous trigger; plans are "just prompts" (simply) and "how you communicate massive amounts of work to your agent" (accurately).)*

---

## Idea 12 — Four KPIs, and the confession that reframes the whole lesson

**Hook.** "It's not enough to vibe code and randomly ship a feature… If you don't measure it, you can't improve it." Then, at the very end, the twist: everything you just watched — all that back-and-forth prompting — was Dan using Claude Code in *phase one mode*. "This tanks our presence KPI."

**Picture.** Frame t2072 (34:32): the KPI file — "# How do we know we're improving as agentic engineers? / ## Four KPIs / Size / Attempts / Streak / Presence."

**Worked example.** The four, with directions and thresholds from the lesson: **Size ↑** — hand off bigger work; five-minute agent runs are fine, push toward 10/20/30 minutes, an hour, three hours. **Attempts ↓** — corrections after the prompt completes cost "your most important engineering resource: your time"; sitting at 5–10 (even 3–6) means a leverage point is missing — find it. **Streak ↑** — back-to-back one-shots; streaks of 3, 5, 10; the engineer who one-shots five features "drastically outperforms an engineer that runs five prompts but had to fix three issues per prompt — that's 3x slower"; when the streak breaks, name the missing lever. **Presence ↓** — how much you must sit, guide, and correct; the industry thinks prompting back-and-forth is the end game, "this is not the end game. This is the early game"; target zero. Then the problem→lever mapping drill: dictionaries confusing your agent → types; unnavigable structure → architecture; manually reading errors → stop, stdout; short iterative prompts → plans; "successful" runs with hidden bugs → tests; same workflow three times → template it (`/start`).

**Dan's term.** *The agentic coding KPIs* — "size, attempts, streak, presence. This is it. This is all we need to track to win." The tactic's closing tie-in: adopting your agent's perspective "sends the size of your agentic prompts up… your attempts down to one per prompt… increases your streak… so you can drop your presence down to zero." And the era line for the road ahead: programmable mode from here on; "this will be uncomfortable. As engineers, we love control and visibility, but it's time for us to let that go… What does stay is architecture… direction… planning… thinking… engineering." "English is the new programming language."

**Failure mode.** Tracking nothing (can't tell improvement from luck) — or misreading "iteration is bad" as an absolute: Dan explicitly allows exploratory iteration and expects attempts to rise temporarily whenever you scale size; the sin isn't iterating, it's *accepting* iteration as the permanent workflow instead of diagnosing the missing leverage point. Also: mistaking presence for productivity — feeling productive *because* you're watching every token is the early-game trap.

**Retrieval Q.** Name the four KPIs with target directions, and Dan's streak math. *(Size ↑, attempts ↓ (toward one per prompt), streak ↑, presence ↓ (toward zero); five one-shots vs five prompts needing three fixes each = the fixer is 3x slower.)*

---

## Timeline map (VTT-verified, 10s buckets)

| Time | Beat |
|---|---|
| 0:13–0:55 | Cold open: lesson 1 set the stage, lesson 2 performs; framework + tactic; easy to start, hard to master; smart work for asymmetric returns |
| 0:55–1:56 | Bet on what never changes → the SDLC; five steps: plan, code, test, review, document |
| 1:56–2:45 | Autonomy knob to 11; agent ships on your behalf; three topics: tactic, 12 points, measuring success |
| 2:45–4:15 | **Tactic #2: Adopt your agent's perspective**; brilliant but blind; ephemeral agents; the core four is what it needs; teach your agents |
| 4:15–5:50 | The 12 leverage points; longest hot streak; in-agent vs through-agent; the money slide |
| 5:50–7:25 | Demo setup: clone tac-2 (loot box), VS Code, Claude Code; `/install`; prompts inside prompts (`install.md` → `prime.md`, 7 lines) |
| 7:25–8:50 | README step 2: `.env` from sample (OpenAI + Anthropic keys); `./scripts/start.sh`; WSL note; app tour: upload products.csv, "list top 5 products by price" |
| 8:50–10:50 | In-agent points recap; **tools deep-dive**: `/tools`, Bash timeout secret, CRUD toolset, delegation tools, MCP teaser |
| 10:50–12:30 | **Standard out**: agent sees only what you let it see; drag `orders_(32).csv` → browser error; server silent → "bad agentic code" |
| 12:30–14:30 | New agent, `/prime`, `@server.py` add error+success prints; YOLO mode; restart; error now traces to stdout |
| 14:30–16:30 | Fresh agent; `sh ./scripts/start.sh, 300s` runs server **inside** agent; reproduce error; "any issues with the server?" → file_processor.py:26 diagnosis; "resolve: replace bad chars and escape" → `sanitize_table_name` |
| 16:30–18:15 | Stdout overload options (session log file / cleanup / warn+error levels); state-space reduction; rerun, delete db, re-upload works; "latest delivery" query |
| 18:15–20:55 | **Types**: types tell a story; copy `DatabaseSchemaResponse`; clean instance; flow-trace prompt + format; Task subagent (7 tool uses, 26.7k tokens); 5-file flow; types are IDKs |
| 20:55–23:10 | **Architecture**: client/server halves the space; consistency vs complexity; the agent navigation problem; prime is just a starting point |
| 23:10–26:30 | The architecture checklist (entry points, constants, types, verbose IDK names, ≤1000-line files, distributed agent docs, separated services, one responsibility/file, mirrored tests); "don't refactor yet" |
| 26:30–27:40 | **Documentation**: internal vs external; `ai_docs/` local-first; RepoMix; WebFetch/WebSearch baked in |
| 27:40–29:50 | **Tests**: agents make mistakes; backend easiest; `!` bash mode `uv run pytest` feeds agent; closed-loop structures; "not writing tests = probably vibe coding"; frontend tests later |
| 29:50–31:30 | **Plans**: 749-line spec; "no way I typed 700 lines"; plans are prompts / massive work; planning = SDLC step 1; lesson 3 teaser |
| 31:30–33:30 | **Templates**: reusable agentic prompts; want many commands; **ADWs**: prompts + code + trigger; `claude -p "/tools"` programmable mode |
| 33:30–40:30 | **KPIs**: size ↑ (5 min → hours), attempts ↓ (5–10 means missing lever), streak ↑ (don't break it; 3x-slower math), presence ↓ (early game vs end game); systematize later (GitHub/Jira) |
| 40:30–43:50 | Problem→lever mapping drill (dicts→types, structure→architecture, errors→stdout, iterative prompts→plans, "successful" bugs→tests, repeated workflow→`/start` template; three-time rule); tactic summary: all four KPIs move |
| 43:50–47:14 | The confession: phase-one mode all lesson; programmable mode ahead; letting go of control; what stays (architecture, direction, planning, thinking); English is the new programming language; master primitives → compositions; lesson 3 teaser (the plan, meta-prompting); sign-off |

## Terminology glossary (Dan-isms, canonical spellings)

- **Tactic #2: Adopt Your Agent's Perspective** — give the agent the information, tools, and resources you'd use; litmus: "with my agent's core four, can it complete the task?"
- **Brilliant, but blind** — the agent's condition: capable, ephemeral, context-free until you provide it
- **In-agent leverage points** — the core four: context, model, prompt, tools (always with the agent)
- **Through-agent leverage points** — standard out, types, documentation, tests, architecture, plans, templates, ADWs (external levers flowing through the context window)
- **Phase two SDLC** — plan, code, test, review, document
- **Bad agentic code** — code whose failures are invisible to agents (no stdout trace)
- **IDK (information dense keyword)** — a name that points to exact codebase locations; types are the canonical IDKs
- **Agent navigation problem** — every fresh agent must re-explore the codebase; consistency is the antidote
- **Closed loop structures / self-validating loops** — agent validates its own work (tests → stdout → correction)
- **The plan is the prompt** — plans communicate massive work; great planning = great prompting
- **Three-time rule** — "three time makes a pattern… automate" → mint a slash command
- **ADW (AI Developer Workflow)** — agentic prompt(s) + arbitrary code + autonomous trigger; highest abstraction
- **Programmable mode** — `claude -p "…"`: run a prompt/command headlessly, return the result
- **YOLO mode** — auto-accept edits; not watching every step (transcribed as "yellow mode")
- **Agentic coding KPIs** — size ↑, attempts ↓, streak ↑, presence ↓
- Transcript corrections: "clog code"/"Cloud Code"/"ClawedCode" → Claude Code; "Clawed-P" → `claude -p`; "loop box" → loot box; "get else files"/"Git LS" → `git ls-files`; "claw.md" → CLAUDE.md; "agent decoding" → agentic coding; "standard in" (~41:50) → standard out; "right test" → write tests

## Bridge to the rest of TAC (as trailed in-lesson)

- Lesson 3: **the plan** — meta-prompting, higher-order prompts, reusable plans; "plans so clear success becomes inevitable"; plan with your agent from its perspective
- Docs, tests, and plans each get dedicated lessons; frontend + backend agent testing coming
- "Several mission critical MCP servers in future lessons"
- Organizing agentic assets in your codebase — without and *with* your agent (hence: don't refactor yet)
- Empty `adws/` and `agents/` dirs foreshadow the ADW lessons; programmable mode becomes the default posture
- Constant thread: KPIs measure every lesson's payoff; the 12 leverage points recur "over and over"

# TAC-5 · Close the Loops — Master Teaching Notes

> Source of truth for the expanded chapter. Video 53:52 · Intermediate · Tactic #5: **Always Add Feedback Loops**
> Lesson artifact: the tac-5 codebase — a real NL→SQL app (FastAPI + Vite/TS) wrapped in a full agentic layer: 21 command templates (incl. `/test`, `/test_e2e`, 3 e2e specs, 2 resolvers), Playwright MCP, five ADW scripts, and the 1,106-line `adw_test.py` test node.
> Subtitle: "More Compute, More Confidence" (course page; the in-video slide footer says "Higher Confidence").

**Lesson thesis in one sentence:** Your work is useless until it's validated, so encode how you would test every class of work into commands and tool calls, attach those validators to every agentic prompt (request → validate → resolve), and stack them — linter to unit tests to builds to browser-driving e2e — until agents execute, validate, and resolve in loops and 'the code writes itself,' first in-loop where you can watch, then out-loop where you can't.

**The chapter must land ten ideas.** Each below follows: Hook → Picture → Worked example (course codebase) → Dan's term → Failure mode → Retrieval Q.

---

## Idea 1 — The most valuable thing you make is not code, and the question that follows

**Hook.** Lesson 5 opens with a confession demand: "Let's be brutally honest with ourselves." Engineers rank code, architecture, systems, plans, features as their most valuable assets — and they're wrong. The valuable thing is the *experience in your users' hands*, which means the highest-value engineering act is proving the stuff does what it's meant to do. Then the ambush: you probably verify by opening the browser and clicking around. "What a waste of time."

**Picture.** Frame t0105 (1:45): the two-line question slide — "Given a unit of **valuable work** that's production ready / How would you, the engineer, **test and validate this work?**" This is the lesson's load-bearing artifact; everything else is answers to it.

**Worked example.** The lesson's own answer menu (2:28–3:00, narrated over an on-screen checklist): run your linter, execute unit tests, UI tests, CI/CD integration tests, build/compile, look for Datadog log lines, check Sentry for the *absence* of errors, run custom evals or LLM-as-a-judge for ML work — and the big one, clicking through the feature yourself. Every item is a feedback loop, and every one of them is encodable as a command or tool call. In tac-5 those encodings literally exist as files: `uv run ruff check .`, `uv run pytest`, `bun tsc --noEmit`, `bun run build`, `.claude/commands/e2e/*.md`.

**Dan's term.** *The core validation question.* And the payoff clause: answer it "for every class of work that your codebase handles and then encode the answers into a command or tool call, [and] you will fly while other engineers run." Plus the architecture rider: *codebase architecture is a massive critical leverage point* here — "net new codebases have a massive advantage."

**Failure mode.** Treating the question as rhetorical instead of operational. The deliverable is a literal list: per class of work, the exact commands that would prove it production-ready. If you can't write the command, you haven't answered the question — and your agent has no loop to close. (Lab S5 makes students produce this list for their own repo.)

**Retrieval Q.** Recite the core validation question and state what you do with the answer. *(Given a unit of valuable work that's production ready, how would you, the engineer, test and validate this work? — answer it per class of work, encode each answer into a command or tool call.)*

---

## Idea 2 — Tactic #5: Always Add Feedback Loops (the testing debate is over)

**Hook.** One of engineering's most heated debates — how much testing is worth it — "has come to an end." Not by argument, by arithmetic: the value of a test used to amortize over *your* runs of it; now it multiplies by the number of *agent executions* in your codebase, and that number is exploding.

**Picture.** Frame t0230 (3:50): the official Tactic card — "Always Add Feedback Loops" with the Daily Actions sidebar: add validation commands to every agentic prompt; create closed-loop prompts (request, validate, resolve); set up e2e tests for high-ROI self-validation; chain feedback mechanisms; spend compute on testing to buy confidence in agent work.

**Worked example.** The lesson's KPI logic (7:28, recap of the TAC-2 scoreboard): attempts down, size up, streak up, presence down. Every one moves the right way when agents self-validate: fewer re-prompts (attempts), bigger units of handed-off work (size), more consecutive one-shots (streak), fewer moments where you must be present (presence). Testing is "one of the highest through-agent leverage points" because it converts compute into confidence without you.

**Dan's term.** *Always add feedback loops* — with both halves said explicitly: "I'm not saying stop testing or stop reviewing. I'm saying start handing off this responsibility and start teaching your agents to test." The hierarchy: "The ultimate test will always be your users. The next best test... used to be you. Now, the next best test is an army of agents validating your entire codebase with regression tests and most importantly with end-to-end tests." And the verdict: "engineers that test with their agents win. Full stop, zero exceptions."

**Failure mode.** Hearing 'add feedback loops' as a someday-testing-strategy instead of a *prompt-structure rule for today*. The test of the tactic is brutal and immediate: does the prompt you are about to fire contain a validation block? If not, you just volunteered to be the validator — the exact job the lesson exists to hand off. Second failure: judging test ROI with human-era math ("tests slow me down"), which silently converts every agent run from self-validating to unverified.

**Retrieval Q.** Why is the testing debate over, and what are the two things the tactic does NOT mean? *(Test value multiplies by agent executions, so engineers who test with agents win — full stop; it doesn't mean stop testing/reviewing yourself entirely, and it doesn't mean 'later' — it means every agentic prompt carries validators now.)*

---

## Idea 3 — Three loops that sound alike: in-loop, out-loop, closing the loop

**Hook.** Three phrases, one word apart, and mixing them up costs you the lesson: being *in* the loop, being *out* of the loop, and *closing* the loop. You can be out-loop with zero closed loops — that's an unsupervised agent shipping unverified junk. The lesson's whole strategy is: close the loops in-loop where you can watch, so you can trust them out-loop where you can't.

**Picture.** No slide exists (spoken over B-roll, 4:54–5:30) — the chapter should draw the three-loop diagram: (1) you ↔ agent chat cycle (in-loop), (2) the PITER pipeline running on a separate machine (out-loop), (3) the micro-loop inside any single step: agent → command → feedback → agent (closing the loop). Frames t0700/t0725 (11:40/12:05) supply the out-loop half in the real world: the GitHub issue whose body is `adw_plan_build_test` + `/feature` + a mid-level prompt, and the Mac mini running `trigger_webhook.py` that catches it.

**Worked example.** The lesson performs all three simultaneously: at 10:13 Dan fires the out-loop pipeline (issue #28 → webhook → plan→build→test on the agent box), then spends thirty minutes in-loop demonstrating the closed-loop primitives that pipeline is built from, then returns at 46:32 to find a PR waiting. The demo's structure IS the concept.

**Dan's term.** *In-loop* ("you sitting right here, prompting with your agent back and forth"), *out-loop* ("a high level prompt running through the PITER system that fires off on your isolated device" — PITER from TAC-4: Prompt input, Trigger, Environment, Review; the transcript's 'Peter system' and 'PIDA framework' are mishearings), and *closing the loop*: "letting your agent operate on work, calling a command or a tool to get feedback on the success of the work... your agent continues to build until the feedback is positive. When you do this, you let the code write itself."

**Failure mode.** Conflating out-loop with closed-loop and scaling autonomy before feedback: firing AFK agents on a codebase with no validators. Autonomy without feedback is unsupervised risk; feedback is what makes autonomy safe to scale. Reverse failure: staying in-loop forever polishing validators and never installing a trigger + environment — the KPI gains (presence↓, size↑) only materialize out-loop.

**Retrieval Q.** Define the three terms so they can't be confused. *(In-loop: you at the keyboard trading prompts. Out-loop: a high-level prompt running via PITER on an isolated machine. Closing the loop: the agent calling commands/tools for feedback on its own work and iterating until positive.)*

---

## Idea 4 — The closed-loop prompt: Request → Validate → Resolve

**Hook.** The lesson's first artifact is three lines long, and one of the lines is an order to sabotage the codebase. That's the point: the prompt plants a defect *and* carries the loop that catches it. If a three-line prompt can self-correct, "I don't have time for feedback loops" is dead on arrival.

**Picture.** Frame t0860 (14:20): the scratch buffer, verbatim — `Update @app/server/core/sql_processor.py comment out validation.` / `Validate your work with `cd app/server && uv run ruff check .``. If there are errors at all, resolve them.` Frame t0985 (16:25): the next-level version actually closing — ruff's E402 in the terminal, and the agent's own sentence: "I need to fix the ruff errors. The issue is that load_dotenv() is being called before all imports are complete. I need to move it after all the imports."

**Worked example.** Demo 1 (13:38–14:50): commenting out `validate_sql_query(sql_query)` in `core/sql_processor.py` leaves its import dangling; `uv run ruff check .` prints the unused-import error to stdout; that stdout lands in the agent's context window; the agent fixes and reruns ruff to green. "Ruff is looking at that change. It's going to provide input back to our agent via standard out." The feedback channel is embarrassingly ordinary — and that's why it works everywhere: *everything is one tool call away; tools are just functions and functions can do anything* (9:49).

**Dan's term.** *Closed loop prompt*, with its *anatomy*: "There's a request — usually a large spec or task or feature you want built — and then you're going to have validations... validators, and then give some direction with your resolution. Request, validate, resolve." Plus the execution rule from the scaled version: run validators in order, top to bottom; on any issue, stop, resolve immediately, then "rerun every validation step. It's not good enough to resolve this once and [have] that resolution cause something to break."

**Failure mode.** Writing the request and skipping the validation block because the change is 'simple.' An open-loop prompt doesn't fail loudly — it silently reassigns the validator job to you, later, when you least expect it. Second failure: believing the magic is in the model. The magic is in the plumbing: no validator in the prompt → no stdout in context → no self-correction, however smart the agent.

**Retrieval Q.** Write the lesson's smallest closed-loop prompt from memory and name its three parts. *(Request: comment out validation in sql_processor.py. Validate: cd app/server && uv run ruff check . Resolve: if there are errors at all, resolve them.)*

---

## Idea 5 — Stack the loops; make tests the rule of law

**Hook.** The best moment of the lesson is a trap paying off: demo 1 deliberately left a landmine (validation commented out), and demo 2 — run by a *fresh agent with a cleared context window* — steps on it. Pytest fails, and an agent that never saw the sabotage un-comments the line and restores the import. Nobody remembered the defect. The validator did.

**Picture.** Frame t1030 (17:10): the diff restoring `validate_sql_query(sql_query)` and the `SQLSecurityError` import, with "Now let's run pytest again" beneath — the cross-context catch on camera.

**Worked example.** Demo 2 (15:15–17:40): request = remove the `/api/insights` endpoint from `server.py`, move `load_dotenv()` right below its import; validate = ruff, `uv run pytest`, `uv run python -m py_compile server.py`; resolve = fix everything found. Ruff catches the E402 import-order issue; the agent briefly adds duplicate imports ("This happens.") and re-runs; pytest catches demo 1's sabotage "without knowing what we previously did, thanks to the context window clearing"; py_compile seals syntax. Three loops, each covering a failure class the others can't see. By 25:20 the full stack counts six: ruff, pytest ("a crap ton more than one, but one bucket"), py_compile, `bun tsc --noEmit`, `bun run build`, Playwright e2e.

**Dan's term.** *Stacking the confidence* ("We know a little bit more, a little bit better that things are going to work") and the architecture decree: "You have to make a rule inside of your codebase architecture. What's more important, the code or your tests? The answer should be your tests. **Your tests should be the rule of law in your codebase.**" With the corollary: if the tests aren't right, have your agents update the *tests* so testing commands keep their weight. And the forward-looking reason: "as the agents progress, as the models improve, **we will be the ones prompting the errors**" — loops guard against your prompts, not just the model's slips.

**Failure mode.** Two. (a) Stopping at one validator: the linter can't catch a failing business rule; nothing but an e2e run catches 'the button doesn't work.' Confidence is coverage of *disjoint failure classes*. (b) The rule-of-law inversion: letting an agent (or yourself) weaken a red test to get to green. The moment a failing validator is negotiable, every loop in the repo stops meaning anything — feedback becomes advisory, and self-validation quietly dies.

**Retrieval Q.** Name the six loops of the lesson and state the rule of law with its corollary. *(ruff, pytest, py_compile, tsc --noEmit, bun run build, Playwright e2e; tests outrank code — red means stop and fix, and a wrong test gets visibly fixed as a test, never routed around.)*

---

## Idea 6 — The browser is a tool call: end-to-end via Playwright MCP

**Hook.** The QA ritual the lesson called a waste of your time at minute three comes back at minute twenty — automated. Open the browser, type the query, click, screenshot, read the result. Same ritual, zero of your minutes: "browser control is another tool that you can use to validate work."

**Picture.** Frame t1200 (20:00): the full `# Validation` reusable prompt — Backend Validation (ruff, pytest, py_compile), Frontend Validation (`bun tsc --noEmit`, `bun run build`), and E2E Validation: six numbered Playwright steps ending in "Read both images and verify our natural language query was executed correctly. Confirm 7 results are returned."

**Worked example.** The run (21:00–24:30): tsc passes, vite build compiles for production, then Playwright (registered in `.mcp.json` as `npx @playwright/mcp@latest --isolated --headless --viewport-size 1920,1080`) opens localhost:5173, screenshots `e2e_before.png`, types 'select newest 7 products sort by price desc', queries, screenshots `e2e_after.png`, and the agent reads both images to confirm the 7 rows. Dan then does the ultimate spot-check: copies the generated query from the screenshot into the real app and gets the identical rows. Bonus discovery inside `e2e_before.png`: junk tables (`test`, `data___DROP_TABLE_users___`) — the tests are polluting the real DB. Bookmarked; becomes `/bug` fodder (Idea 7). The codebase carries three permanent e2e specs in `.claude/commands/e2e/` — basic query, complex query, SQL injection — each structured User Story → Test Steps (with `**Verify**` markers) → Success Criteria.

**Dan's term.** *End-to-end tests* as the "most importantly" class; the specificity mandate — "It validates a precise result from our codebase given the state of our codebase" (which is why `scripts/reset_db.sh` restores `backup.db` before every run); and the deployment pointer: point the same loop "at a staging system or even a production test account."

**Failure mode.** Dismissing the demo because the app is small — Dan pre-handles it: "I know this application is super simple... there's like five actions you can take on this page, but don't let that scare you away." The pattern (drive UI, capture evidence, verify a precise expectation) is complexity-invariant; only the specs get longer. Second failure: e2e without determinism — skipping the DB reset makes 'confirm 7 results' meaningless, teaching students to distrust their strongest loop.

**Retrieval Q.** What exactly does the e2e block of the `# Validation` prompt make the agent do, and what makes the assertion trustworthy? *(Open localhost:5173, screenshot before, run 'select newest 7 products sort by price desc', screenshot after, read both images, confirm exactly 7 results — trustworthy because reset_db.sh restored a known DB state first, and the screenshots remain as evidence.)*

---

## Idea 7 — Template your engineering: validation by default

**Hook.** "Always add feedback loops" has an enemy: your discipline on a busy Tuesday. The lesson's answer is to take 'always' away from the human entirely — bake the loops into the templates that generate all future work, so forgetting is no longer an available action.

**Picture.** Frame t1760 (29:20): `bug.md`'s Plan Format — the `## Validation Commands` block ("Execute every command to validate the bug is fixed with zero regressions"), the reproduce-before/after placeholder, the three default commands (`uv run pytest`, `bun tsc --noEmit`, `bun run build`), and the conditional e2e machinery. Frame t0700 (11:40) shows where these plans come from out-loop: the issue body itself.

**Worked example.** `/bug` is a *meta prompt* — "a prompt that creates a prompt": (issue_number, adw_id, issue_json) → a plan in `specs/issue-{n}-adw-{id}-sdlc_planner-{slug}.md`. Fired in-loop on camera: `/bug 111 adw111` for the junk-data bug (tests writing to the production SQLite DB — "our tests shouldn't be operating in our quote-unquote live production database"; fix: in-memory DBs). The generated plan arrives with reproduce steps, root-cause analysis, and validation commands (sqlite3 table checks, targeted pytest, before/after table diffs) — and correctly *omits* an e2e task because the bug is backend-only: the template's "IMPORTANT: If the bug affects the UI or user interactions..." conditional didn't fire. A second agent runs `/bug 222 adw222` (disable query input while running + debounce — "a common UI thing... not something that you or I need to solve ever again"), whose plan DOES include creating `.claude/commands/e2e/test_<name>.md`. Then `/implement <plan>` (a higher-order prompt whose `think hard` is an information-dense keyword activating extended thinking) executes plan 111, finishing with its validation commands. "Plan velocity is through the roof... Great planning is indeed great prompting."

**Dan's term.** *Templating our engineering* — "you encode it, you template your engineering into your reusable prompts so that your agents can pick up on the work and build the way you want to build over and over and over. And the way you want to build is with high confidence." Also *fresh agents*: "/clear... we always want fresh agent instances. We don't want any context pollution" — plus the in-loop constraint noted on camera: one repo-mutating agent at a time on your device (no worktrees in this lesson), a limitation the out-loop architecture removes.

**Failure mode.** Hand-adding validation commands to individual prompts and calling it a system — hand-added loops disappear the week you're busy; templated loops are structural. Subtler failure: not auditing the conditional — a UI bug whose plan lacks an e2e task means the template misfired, and rubber-stamping it erodes the guarantee the template exists to provide.

**Retrieval Q.** What does the /bug meta prompt guarantee about every plan it generates, and when does it force a new e2e test file? *(Every plan ends with a Validation Commands section — pytest/tsc/build defaults plus reproduce-before/after commands; a new .claude/commands/e2e/test_<name>.md task is forced whenever the bug affects UI or user interactions.)*

---

## Idea 8 — adw_test: the test step becomes an isolated ADW node

**Hook.** Everything so far ran where you could watch it. The last move is packaging the whole testing discipline into a machine you *don't* watch: a script that runs every test you have, tries to fix what fails, reports everything, and ships its results — as its own node of the SDLC, separate from plan and build.

**Picture.** Frame t2460 (41:00): `adw_test.py`'s `run_tests_with_resolution` — `max_attempts: int = MAX_TEST_RETRY_ATTEMPTS`, `while attempt < max_attempts:`, the circled `run_tests(adw_id, logger)` — deterministic Python wrapped around agentic judgment, with the `adws/` module tree and the freshly-generated issue-111/222 specs in the explorer.

**Worked example.** The pipeline, verified against the 1,106-line source: fetch issue → checkout the state branch (or create `test-issue-{n}-adw-{id}`) → `/test` runs the five-check suite and must return ONLY a JSON array of `{test_name, passed, execution_command, test_purpose, error?}`, failures first ("we'll immediately run JSON.parse() on the output") → each failure fans out to a fresh `/resolve_failed_test` agent (`test_resolver_iter{attempt}_{idx}`) that must *reproduce via the provided execution_command* before fixing, minimally, and re-run only that command → up to `MAX_TEST_RETRY_ATTEMPTS = 4` rounds, stopping early if a round resolves nothing → e2e gate: only if unit tests are green and `--skip-e2e` absent → glob `.claude/commands/e2e/*.md`, run each via `/test_e2e` (agents `e2e_test_runner_{attempt-1}_{idx}`), **stop at the first e2e failure**, resolve via `/resolve_failed_e2e_test`, `MAX_E2E_TEST_RETRY_ATTEMPTS = 2` → post the 📊 Test Run Summary to the issue → `/commit` → push + create/update PR → exit 1 if failures remain. "What do you think the failed tests do? Of course, they do one thing. They run a template."

**Dan's term.** *AI Developer Workflow* (the highest leverage point, "the highest composition level"), *isolated nodes*: "It's isolated. It's not part of the build. It's not part of the plan. This runs on its own with its own set of agents in its own context windows... we want to be able to tap into one node of the software developer lifecycle and improve that one node." Plus the composition move: `adw_plan_build_test.py` subprocesses plan → build → test sharing one ADW ID and `agents/{id}/adw_state.json` — "isolated reusable scripts" via astral uv ("you can use anything you want — classic shell scripts, bun scripts").

**Failure mode.** Wiring test-running into the build agent 'to keep it simple' — you lose all three isolations at once: fresh context per failure, an independently improvable node, and the JSON boundary where *code* (not vibes) decides what happens next. Second failure: reading the retry constants as arbitrary. Bounded loops (4/2, stop-on-nothing-resolved, e2e-stop-on-first-failure) are what separate a self-correcting system from a token-burning one that thrashes on an unfixable failure.

**Retrieval Q.** Walk adw_test.py's control flow with its bounds. *(/test → JSON parse → per-failure resolver agents, ≤4 rounds, early-stop if nothing resolved; e2e only on green units and no --skip-e2e: per-file /test_e2e, stop at first failure, /resolve_failed_e2e_test, ≤2 rounds; summary → commit → push/PR; non-zero exit on remaining failures.)*

---

## Idea 9 — Observability: adopt your agent's perspective (the API-500 story)

**Hook.** The out-loop run comes back with "Overall Status: FAILED" — the demo gods deliver. And the failure is the best thing in the lesson, because finding its cause takes ninety seconds, not an interrogation: the answer was written down before anyone asked, by a system built to be traced.

**Picture.** Frame t2925 (48:45): inside the agent sandbox, `agents/ce364af1/` — every agent that ran (adw_build, adw_plan, adw_test, e2e_test_runner_0_0/0_1/0_2, e2e_test_resolver_iter1_0, issue_classifier, plan_finder, pr_creator, sdlc_planner, sdlc_implementor...) with the resolver's saved prompt open: `test_complex_query`, status failed, "Test execution error: Claude Code error". Frame t2990 (49:50): the payoff view — PR #29 plus the agent machine's own browser running the new Generate Random Query feature.

**Worked example.** Trace as performed (46:50–48:50): issue #28's summary shows unit checks green, e2e 2/3 — `test_complex_query` failed with a Claude Code error. Copy the ADW ID from the log header → search `agents/ce364af1/` → `e2e_test_resolver_iter1_0/prompts/resolve_failed_e2e_test.txt` shows exactly what the resolver was asked; its raw output shows **API error 500** — Anthropic overload. Infrastructure failure, not product failure; unresolvable by the resolver ("tried to resolve cloud code failing, which it just can't"), honestly reported instead of hidden. Every issue comment is prefixed `{adw_id}_{agent_name}` — GitHub itself is a trace viewer. Then the human close: on the agent box's browser, the feature works (complex CTE query, correct rows; a loading-state nit noted as future test material) — "now you and I, the human engineer, comes in here at the end... It's the test on top of the test."

**Dan's term.** *Observability and tracing* ("You wanna be able to trace everything right down to the nose"), *adopt our agent's perspective* ("We want to know what's inside of every agent at any time"), and the closing posture: human review as the final validator, not the first.

**Failure mode.** Reading FAILED as 'the system is broken' and re-running blind — or worse, treating an honest failure report as a reason to distrust the pipeline. An accurately-reported infrastructure 500 is the system *working*: loops that can't fail loudly can't be trusted to pass quietly. Also: skipping the trails (not saving prompts/outputs per agent) — without them, every out-loop failure becomes archaeology.

**Retrieval Q.** The e2e suite reported one failure. Reconstruct the diagnosis path and the verdict. *(Issue summary → ADW ID ce364af1 → agents/{id}/e2e_test_resolver_iter1_0 saved prompt + raw output → API error 500, Anthropic overload: infrastructure, honestly reported; product itself verified fine.)*

---

## Idea 10 — The arc: single prompt → in-loop loops → out-loop pipeline → you, on top

**Hook.** The lesson opened by firing a GitHub issue and walked away; it closes by collecting a PR, a new e2e test written by the pipeline itself, and a working feature — then asks what your job was in between. Answer: designing the loops, and judging the result. Everything in the middle validated itself.

**Picture.** Frames t0700 → t2990 as bookends: the 40-word issue that started it; the PR + running feature that ended it. Between them, every other frame is a loop being added.

**Worked example.** The composition recap (50:23–51:00): plans from meta prompts, testing embedded into daily work (bugs, features, chores), then pushed into ADWs, then stacked across the SDLC — "we're composing the 12 leverage points of agentic coding step by step by step." The trajectory instruction is explicit and beginner-safe: "They don't have to be complex or intricate. **Everything starts with a single prompt.** And everything starts in the loop and then slowly move it out the loop. Get yourself a dedicated environment so that you can operate out the loop."

**Dan's term.** *The agentic layer* — "lesson by lesson, we're improving the agentic layer around our codebase" (`.claude/commands` + `adws/` + `scripts/` + hooks as its directories here); *the system that builds the system*; and the TAC-6 bridge: two SDLC steps remain — **review** and **document** — "in lesson six... our agents will nearly be operating our entire codebase themselves."

**Failure mode.** Trying to build lesson 5's endgame on day one (a full webhook'd pipeline) instead of the prescribed gradient: one three-line closed-loop prompt today, a reusable validation prompt this week, templated plans this month, the ADW when the loops have earned trust. The gradient isn't slower — it's how the loops get correct enough to be worth automating.

**Retrieval Q.** What's the prescribed adoption path, in Dan's own sequence? *(Single prompt → in-loop closed loops → reusable/templated prompts → ADWs off your device with a dedicated environment — then you review on top: the test on top of the tests.)*

---

## Timeline map (VTT-verified)

| Time | Beat |
|---|---|
| 0:11–1:35 | Cold open: brutal honesty — user experience is the real asset; agents test at scales you never will; gift of generative AI |
| 1:35–2:28 | The core validation question; encode answers into commands/tool calls; architecture as leverage; net-new advantage |
| 2:28–3:42 | The validation menu (linter → LLM-as-judge); browser click-through called a waste of time; all of it = feedback loops to hand off |
| 3:42–4:35 | **Tactic #5: Always Add Feedback Loops**; useless-unless-tested; army of agents; execute-validate-reflect loops; autonomy dial; agentic layer |
| 4:54–5:40 | Terminology: in-loop / out-loop (PITER) / closing the loop; "let the code write itself" |
| 5:40–7:15 | Testing debate over; tests × agent executions; auth/UI/staging confidence ladder; free your context window; "did it do what you designed it to do?" |
| 7:15–8:04 | KPIs recap (attempts↓ size↑ streak↑ presence↓); end-to-end agents, not babysitting |
| 8:04–9:35 | Clone tac-5; YOLO mode; review slash commands ("massive control"); /install runs and self-validates |
| 9:36–10:13 | Many ways to test; "everything is one tool call away"; in-loop is presentational — stay out the loop |
| 10:13–12:30 | Fire the out-loop pipeline: issue #28 (`adw_plan_build_test` + `/feature` + prompt) → webhook on the Mac mini → chained agents start |
| 13:00–13:38 | Housekeeping: port conflict (stop/start scripts); reset remote to your own repo |
| 13:38–14:50 | **Closed loop #1**: 3-line prompt; ruff via stdout; simplest imaginable loop; request/validate/resolve named |
| 15:15–17:40 | **Closed loops #2–3**: insights endpoint + load_dotenv; ruff E402; duplicate-imports wobble; pytest catches prior sabotage cross-context; **tests = rule of law**; py_compile |
| 18:19–19:39 | Missing classes (frontend, e2e); the three-step framework formalized; toy → mid-level reusable prompt |
| 19:39–21:55 | The `# Validation` reusable prompt: backend + frontend (tsc, build) + E2E via Playwright MCP; loot box for links |
| 21:55–24:30 | Playwright drives the browser; before/after screenshots; manual cross-check of the 7 rows; junk-tables discovery bookmarked |
| 24:30–26:12 | "More agency with self-validating loops"; don't ignore testing; six loops counted; hand off more, not less |
| 26:12–29:40 | Templating: .claude/commands tour; /bug meta prompt; Validation Commands baked into Plan Format; conditional e2e task; demo mutations reverted |
| 27:55–31:40 | /bug 111 adw111 (junk data → in-memory); /bug 222 adw222 (debounce); plan review: templated validations, no e2e for backend-only; "great planning is indeed great prompting" |
| 33:14–37:40 | /implement (HOP; think-hard IDK); fresh agents / context pollution; one-in-loop-agent limitation (no worktrees); issue-111 validation commands execute |
| 39:11–45:45 | adws/ deep dive: adw_test pipeline; /test JSON contract; resolve_failed_test fan-out; e2e runner + resolver; retry parameters; isolated SDLC nodes; compositions |
| 46:32–48:50 | Out-loop results: issue trail + PR #29; one e2e failure; trace ADW ce364af1 → API error 500; observability and tracing |
| 48:56–50:30 | PR review (new e2e test authored by the pipeline); feature works on the agent box; human = test on top of the test |
| 50:30–53:52 | Recap: composing the 12 leverage points; main-branch junk-data fix confirmed; lesson-6 teaser (review + document); "everything starts with a single prompt"; get a dedicated environment |

## Terminology glossary (Dan-isms, canonical spellings)

- **Tactic #5: Always Add Feedback Loops** — every agentic prompt carries validators
- **The core validation question** — "Given a unit of valuable work that's production ready, how would you, the engineer, test and validate this work?"
- **Closed loop prompt** — request → validate → resolve; the agent tests itself
- **Closing the loop** — agent calls a command/tool for feedback and iterates until positive; "let the code write itself"
- **In-loop / out-loop** — you at the keyboard vs. a PITER-driven pipeline on an isolated machine
- **PITER** — Prompt input, Trigger, Environment, Review (TAC-4; mishearings: 'Peter system', 'PIDA framework')
- **Rule of law** — tests outrank code; wrong tests get fixed as tests
- **Stacking the confidence** — adding validators across disjoint failure classes (six in this lesson)
- **Meta prompt** — a prompt that creates a prompt (/bug, /feature, /chore → plans)
- **Higher order prompt (HOP)** — a prompt taking another prompt/file as argument (/implement, /test_e2e)
- **Information dense keyword (IDK)** — special-effect words, e.g. `think hard` (extended thinking)
- **ADW / AI Developer Workflow** — deterministic script composing agents into an SDLC node (adw_plan, adw_build, adw_test + compositions)
- **ADW ID** — 8-char run key; prefixes issue comments ({adw_id}_{agent_name}), names agents/{id}/ trails
- **Agentic layer** — the codebase's agent-facing directories: .claude/commands, adws/, scripts/, hooks
- **Fresh agents / context pollution** — /clear between tasks; validators must not depend on chat memory
- **Test on top of the test** — human review as the final validator
- **Agentic KPIs** — size↑ attempts↓ streak↑ presence↓ (TAC-2 scoreboard)
- Transcript corrections: "rough"→ruff, "pie test"→pytest, "Outlook/Outloop system"→out-loop, "copy.inv"→copy_dot_env.sh, "VITES"→Vitest, "Bunrun"→bun run, "tack four"→tac-4

## Bridge to the rest of TAC (as trailed in-lesson)

- Lesson 6: the review and document steps — "we conclude our epic journey to automate the software developer lifecycle"; agents nearly operating the codebase
- Standing thread: compose the 12 leverage points; improve one SDLC node at a time; stack ADWs
- Constant instruction: start with a single prompt, in-loop; move out-loop; dedicated environment
- Carried forward from TAC-4: PITER, the issue-as-prompt, micro-agents with isolated context windows, structured return contracts

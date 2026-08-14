# Tactical Agentic Coding (TAC) — Complete Learning Distillate

IndyDevDan's 8-lesson course on becoming an "irreplaceable engineer" in phase two of the generative AI age. Source of truth: full lesson transcripts under `tac-1` … `tac-8`.

The 8 tactics, in order: **(1) Stop Coding → (2) Adopt Your Agent's Perspective → (3) Template Your Engineering → (4) Stay Out The Loop → (5) Always Add Feedback Loops → (6) One Agent, One Prompt, One Purpose → (7) Target Zero Touch Engineering → (8) Prioritize Agentics.**

---

## TAC-1: Hello Agentic Coding

**Thesis:** AI coding (phase one) is not enough — engineering was never about writing code, it's about building systems of leverage. The first, foundational move into phase two is to stop coding entirely and use agentic tools (the Core Four wrapped in Claude Code) to build systems that build systems.

**Named frameworks & mnemonics:**
- **Tactic #1: Stop Coding.** "Your hands and your mind are no longer the best tool for the job of writing code. Full stop." Throughout TAC, not a single line of code is typed by hand.
- **Phase One vs Phase Two:** Phase one = AI coding (birth of VibeCoders, "complete commoditization of code"). Phase two = agentic coding — "where real engineers strike back" and turn codebases into "increasingly self-operating machines."
- **The Big Three** (AI coding): **context, model, prompt.**
- **The Core Four** (agentic coding): **context, model, prompt, tools.** "Agentic Coding is a superset of AI coding" — the new dimension is "prompts that can reliably execute long chains of tools."
- **The Agentic (Coding) Prompt:** a prompt containing a sequence of tool calls — "with the right context, model, prompt, and now tools, these prompts are now more capable than ever before."
- **Commander of Compute:** the phase-two role — "you take this compute and you use it to build systems that build systems."
- **The Irreplaceable Engineer:** the mission of TAC — "transform you into an engineer they can't replace. You know who they are. It's your boss. It's the company. It's the industry. It's AI."
- **Programmable agentic coding tool:** Claude Code can be run from any language with terminal access (shell, TypeScript/Bun, Python/uv) — the key differentiator enabling embedded agents across the SDLC.
- **Claude Code's three essential elements:** "a powerful language model that can reason when needed, the ability to consistently call long chains of tools, and the right agent architecture."
- **ADW (AI developer workflow)** — teased: "long running end-to-end AI developer workflows that run for minutes to hours with and without your oversight."

**Nuggets:**
- "AI coding is not enough. Engineering is about much more than just writing code."
- "Engineering was never about writing code. It's about building systems of leverage that produce valuable outcomes for your users and your customers."
- "You're an engineer, not a coder. The difference is massive."
- "We move up the stack once again. We become a commander of compute."
- "Powerful language models called the Agentic Loops running on powerful supercomputers are now vastly superior coders than you and I are."
- "Don't be the engineer that can't let go of the past."
- The 10x engineer opportunity: "not by spending 10x the time or effort, but by achieving 10x the leverage… it's 2x, it's 10x, it's 100x — it all depends on the leverage points you can find."
- "80% of life is noise, boring repetition and wasted time — but every once in a while an opportunity presents itself that can change everything if you focus."
- "If you're still typing code, you have no chance of keeping up."
- Phase-two engineering cycles go to "planning, reviewing, and creating closed loop structures."
- "It's not a question of new. It's a question of scale and performance." (on tool calling)
- "Reliable Agentic Coding at scale was not possible before Claude Code."
- "It's not just about the agentic prompt. It's about where we can use the agentic prompt." (terminal = everywhere)
- "We're going to be using millions and millions of tokens… we have to pay to play."
- "Tools will change and models will improve. Don't get stuck on any one tool."
- "Always check out the settings so you know what Claude Code has access to."
- "The contradicting truth: to become an irreplaceable engineer, you will replace yourself."
- "In the tech industry, this is where all the alpha lies. It's in the future… your asymmetric engineering advantage."
- "Big things are just two or more small things put together" (set up in L2 but seeded here via primitives-first framing).

**What Dan actually did/built:**
1. Listed the essential tool stack (Claude Code, git, gh CLI, Python + Astral uv, Node/npm/Bun, etc. — links in the loot box).
2. `git clone https://github.com/disler/tac-1.git`, `cd tac-1`, opened VS Code (`code .`), opened terminal (Cmd+J), ran `claude`.
3. Inspected `.claude/settings` (permissions) — "always check what Claude Code has access to."
4. Ran the **AI coding prompt** from the README: Claude just creates a `main` file with a print — "this is phase one."
5. Ran the **Agentic coding prompt** from the README (~35 lines): Claude checked out a `demo-agentic-coding` branch, wrote `main_tac` with prints, ran both files, `git add`/`git commit`, maintained a to-do list, and reported the work. "This is engineering work, not just writing code."
6. Opened the `programmable/` directory: three scripts (shell, Bun/TypeScript, Python/uv) each firing Claude Code programmatically with the same prompt.
7. Deleted the demo branch (`git branch -D …`), then ran the Python/uv version — watched the whole workflow re-run headlessly with a full report of outputs at the end.

**Workout module:**
- **Goal:** Feel the difference between an AI coding prompt and an agentic prompt, then run an agent programmatically.
- **Prerequisites:** Claude Code installed and authenticated, git, Python + uv (or Bun), any empty repo.
- **Steps:**
  1. In a fresh repo, run `claude` and prompt: "Create hello.py that prints 'goodbye AI coding'. Do nothing else." (AI coding baseline.)
  2. Now run an agentic prompt: "Check out a new branch demo-agentic. Create main_tac.py printing 'hello agentic coding world' and a one-line description of AI agents. Run hello.py and main_tac.py and show outputs. git add and commit with a clear message. Report all work done as a checklist."
  3. Inspect the branch, commit, and files it created.
  4. Write `run_agent.py` (uv single-file script) that shells out `claude -p "<the same agentic prompt>" --output-format stream-json --verbose` and writes output to a file.
  5. Delete the branch and run `uv run run_agent.py` — verify the agent reproduces everything with zero interaction.
- **Done-when:** The branch, files, commit, and final report are recreated entirely by the programmatic run and you never typed a line of code.
- **Level-up:** Write the same runner in a second language (shell or Bun) and have the agent's prompt also open a PR via `gh`.

**Quote of the lesson:** "To become an irreplaceable engineer, you will replace yourself."

---

## TAC-2: The 12 Leverage Points

**Thesis:** Your agent is brilliant but blind — it starts every session from zero, so success depends on giving it your perspective (context, model, prompt, tools) plus eight external leverage points that flow through its context window. Bet on what never changes: the software development lifecycle, compressed to five steps.

**Named frameworks & mnemonics:**
- **Tactic #2: Adopt Your Agent's Perspective.** "Your agent is brilliant, but blind. With every new session, it starts as a blank instance… no context, no memories, and no awareness outside of what you give it."
- **The Phase-Two SDLC (5 steps):** **Plan, Code, Test, Review, Document** — "our framework for success," the aspect of engineering that never changes.
- **The 12 Leverage Points of Agentic Coding**, in two types:
  - **In-agent (the Core Four):** Context, Model, Prompt, Tools — "always with your agent."
  - **Through-agent (8):** **Standard Out, Types, Documentation, Tests, Architecture, Plans, Templates, ADWs** — "external levers… that typically flow through the context window."
- **The Agentic Coding KPIs (4):** **Size ↑, Attempts ↓, Streak ↑, Presence ↓.** Size = amount of work handed off per prompt; Attempts = prompts needed to finish (target one-shot); Streak = back-to-back one-shot successes; Presence = "how much you the engineer have to sit, guide and correct your AI agent" (target zero).
- **IDKs — Information Dense Keywords:** "Types are IDKs. They point to exact locations in your codebase and represent the flow of a specific type of information." Everything you name can be an IDK.
- **The Agent Navigation Problem:** every new agent must re-explore your codebase; architecture and consistency stack up "for you or against you."
- **Closed loop structures:** self-validating loops — "we let our agent write the code itself by getting a concrete feedback loop."
- **"The plan is the prompt"** — "plans are just prompts… great planning is great prompting."
- **Templates:** reusable prompts (custom slash commands); **ADWs:** "one or more agentic prompts wrapped in arbitrary code, kicked off autonomously with a trigger" — the highest level of abstraction.
- **"Three time makes a pattern"** — the trigger for automating anything into a slash command.
- **Codebase-architecture checklist (build for agents):** clear entry points; constants files; types/classes/structures; meaningful, verbose names; files under ~1000 lines; agent docs (README/CLAUDE.md) spread through the tree; separated services; one responsibility per file; test tree mirroring source tree.

**Nuggets:**
- "It's not about what you can do anymore. It's about what you can teach your agents to do."
- "Agentic coding is easy to start, hard to master. All the low hanging fruit is getting chewed up."
- "Do the smart work, not the hard work, to get asymmetric return on your engineering."
- "We're here to dial up the autonomy knob all the way to 11."
- "Your agent can only see what you let it see" — standard out is a top leverage point.
- "Not only do we have bad code, we have bad agentic code" — code that hides errors from agents.
- "Stop looking at error messages… give them to your agent. Only when your agent fails do you take your precious time and dig in."
- "Types tell a story about how information travels throughout your codebase."
- "One simple decision (client/server split) cuts all possibilities in half for your agent."
- "If it's hard for you, you should assume it'll be hard for your agent."
- "Consistency is a powerful actor against complexity for both humans and for agents."
- "We want our codebases to be token efficient."
- "Your agent will make mistakes, just like you. The only question is: does it have the leverage it needs to correct them?"
- "If you're not writing tests, you're probably vibe coding."
- "Most engineers don't spend enough time communicating what they want done."
- "Plans are how you communicate massive amounts of work to your agent."
- "Counterintuitively, iterating is not good… We're not aiming to become a babysitter for AI agents. We're looking for one-shot solutions."
- "Once you start one-shotting, don't break the streak. And when you break it, figure out exactly which leverage point you were missing."
- "This is not the end game. This is the early game." (on back-and-forth prompting)
- "If you don't measure it, you can't improve it."
- "Master the primitives and you'll master the compositions."
- "English is the new programming language and we're taking it where it's going before it gets there."

**What Dan actually did/built:**
1. `git clone https://github.com/disler/tac-2.git` — a natural-language→SQL app (Vue-ish frontend + Python backend + in-memory SQLite).
2. Ran `/install` (a 7-line reusable prompt that reads and executes `/prime`, then installs frontend + backend deps) — "prompts inside of prompts… no different than passing a function into a function."
3. Set up `.env` (OpenAI + Anthropic keys), ran `scripts/start.sh` to boot client+server; uploaded sample CSV data and ran NL queries.
4. Ran `/tools` (a baked-in prompt template) to dump every tool definition Claude Code has — noting hidden capabilities like the bash tool's timeout parameter.
5. **Standard out demo:** dragged in a CSV that errored; showed server endpoints returning raw responses with no logging ("bad agentic code"). Prompted with `@app/server/server.py`: "make sure every exception logs all exception details, and every successful response before returning." Restarted, confirmed errors now trace to stdout.
6. Booted a fresh agent, `/prime`, then ran the start script *inside* the agent (`scripts/start.sh` with a 300s bash timeout) so the agent could watch stdout live; reproduced the upload error; prompted "any issues with the server?" — agent diagnosed unescaped special characters; prompted "resolve: replace bad chars and escape" and let it fix + re-verify in YOLO mode.
7. **Types demo:** copied the `DatabaseSchemaResponse` data model into a fresh Claude instance: "show me how this type flows throughout the application; detail functions, files, and purpose" — agent fired a search sub-agent (Task tool) and produced a top-to-bottom information-flow trace (26K tokens, 7 tool uses).
8. **Architecture walkthrough:** client/server split, mirrored test tree, the agent-facing docs, `specs/` with a 750-line initialize-codebase plan ("no way I typed that — we plan with our agent").
9. Ran `uv run pytest` from within the agent (bang/bash mode) so all test output landed in its context.
10. Demonstrated turning a repeated workflow into a command: "create `.claude/commands/start.md`" then `claude` → `/start`.
11. Ran `claude -p "/tools"` — programmable mode as the bridge to ADWs.
12. Walked the 4 KPIs in a markdown file and mapped each failure mode to the leverage point that fixes it.

**Workout module:**
- **Goal:** Make one real codebase legible to agents via stdout, types, and a `/prime` command — and verify with a one-shot fix.
- **Prerequisites:** Claude Code; a small client/server project (or clone `disler/tac-2`).
- **Steps:**
  1. Create `.claude/commands/prime.md`: run `git ls-files`, read README, summarize the codebase. Boot `claude`, run `/prime`.
  2. Create `.claude/commands/tools.md` that asks the agent to list all its tool definitions; read the output and note 2 capabilities you didn't know.
  3. Audit one API endpoint: if it swallows errors, prompt the agent (with `@file` references) to log every exception and success to stdout.
  4. Run your app's start script inside the agent with a long bash timeout; trigger a known error in the UI; ask "any issues with the server?" then "resolve".
  5. Copy one core type into a fresh agent and ask for the full flow trace (file → function → purpose format).
  6. Track KPIs for the session: size of task, attempts, streak, presence — write them down.
- **Done-when:** The agent detects and fixes a runtime bug in one attempt purely from stdout, and your type-trace covers every layer of the app.
- **Level-up:** Refactor one confusing directory using the architecture checklist (entry points, verbose names, <1000-line files, mirrored tests) and re-measure attempts on a similar bug.

**Quote of the lesson:** "It's not about you anymore. It's about what you can do for your agent so they can work for you."

---

## TAC-3: Success is Planned

**Thesis:** The prompt is everything, and a plan is just a prompt scaled up — so encode how you solve whole classes of problems (chores, bugs, features) into template meta prompts that let your agent write the plans, then implement them with fresh, single-purpose agent instances.

**Named frameworks & mnemonics:**
- **Tactic #3: Template Your Engineering.** "You encode your problem solving into reusable units that you, your team, and your agents can see, use, and importantly, improve."
- **"The plan is the prompt."** "Plans are prompts scaled up for high impact… great planning is great prompting." A scaled prompt = "a plan, a specification, a PRD."
- **Meta prompt:** "a prompt that builds a prompt" — e.g. `/chore` generates a plan from a template.
- **Higher Order Prompt (HOP):** a prompt that takes another prompt as an argument — e.g. `/implement <path-to-plan>` ("plans getting passed into plans," like passing functions into functions).
- **Template:** a reusable prompt containing Purpose, Instructions, Relevant Files, Plan Format, and an `$ARGUMENTS` slot.
- **The Pareto 80/20 of agentic engineering:** the first three tactics together — Stop Coding, Adopt Your Agent's Perspective, Template Your Engineering.
- **High-level vs low-level prompts:** a high-level prompt is "a prompt void of detail" that templates expand into detailed plans.
- **Three reasons to always run fresh agents:** (1) free the context window — "one agent, one task, one mission"; (2) force prompts/plans/templates to be "isolated, reusable, improvable assets with zero dependencies"; (3) "prepare for true off-device agentic coding" — decouple performance from the conversational context window.
- **"Think hard"** — Anthropic's encoded IDK that activates the reasoning model ("throw more compute at the problem").
- **specs/ directory:** all generated plans are written here — "staging environments for code that will be generated."

**Nuggets:**
- "What was once a complete joke is now the most valuable skill any engineer can have. The prompt is everything."
- "There's a reason they're called Vibe Coders, not Vibe Engineers. They're just coding. We're doing it all."
- "Those who plan the future tend to create it. Success is planned."
- "Planning alone is expensive… there's always something to miss."
- Templates are "one of many solutions to the 'my codebase is too big' problem."
- Out-of-the-box tools (Codex, Copilot, Devin, Jules, Gemini CLI) "don't understand your codebase like you do… they're limited by nature."
- "It doesn't take a lot to do a lot, but you need the right information."
- "Not only should we stop coding, we should also lean into and leverage our agent to write plans with us and for us."
- "Chores, bugs, features, front end, back end, research notebooks, data analytics, code optimization, net new codebases — all of it can be templated. Don't limit yourself."
- "Don't make the mistake in thinking that Gen AI can't solve your problem… tools will change, models will improve. We know this for a fact."
- "We need to decouple our performance from the conversational context window."
- "When I boot up this agent, I know 100% what the agent's perspective is."
- "The more code, the more complexity in your codebase, the more you'll want to dial in your reusable templates to solve specific problems really well."
- "Having agents run loose on your codebase without structure, without knowing how you do things, is a plan for failure."
- "The more custom your templates are, the more unique your engineering gets."
- "You want to get to that first aha moment as fast as possible… run one of these. Don't wait to complete this course."
- "Be very careful thinking that these tactics can't work for your codebase. That is a limiting belief."
- "You want to be building the system that builds the system."
- This chore "has been completed agentically with two prompts — one for the planning phase and one for the coding/building phase."

**What Dan actually did/built:**
1. `git clone https://github.com/disler/tac-3.git`; `/install` (now also runs `scripts/copy.env` to copy the `.env` from tac-2 — agentic resource reuse); `scripts/start` to boot the NL-SQL app.
2. **Chore flow:** fresh Claude → `/chore "replace all server print statements proper python logging log levels make sure all output is written to standard out"` — the meta prompt researched the codebase (thinking mode) and generated a plan in `specs/` with sections: Chore, Description, Relevant Files, Step-by-Step Tasks, Validation Commands, Notes.
3. Opened `.claude/commands/chore.md` and dissected the template: Purpose → Instructions → Relevant Files → Plan Format → `Chore: $ARGUMENTS`.
4. **New terminal, fresh Claude** → `/implement specs/<plan>.md`. Dissected `implement.md`: 12 lines — "Read the plan, Think hard, implement, then report: summarize work + files changed." Watched it execute, run pytest for regressions, and report.
5. Manually validated: restarted server, ran queries, confirmed new logging format, regex-searched to confirm zero `print(` remained.
6. **Bug flow:** fresh instance → `/bug "resolve major issue our SQL statements not being escaped, user input into SQL"` — generated a plan with Problem Statement, Solution Statement, Steps to Reproduce, Root Cause Analysis, Relevant Files, New Files (`sql_security`), Step-by-Step Tasks, Validation, Notes. Committed specs + changes, then `/implement <plan>` in a fresh instance; watched self-validation catch and fix 2 issues, generating 18 new SQL-injection tests (52 total).
7. Explained the fresh-agents rationale (3 reasons above).
8. **Feature flow, out-of-loop preview:** wrote `/feature "create a new query history side panel…"` but ran it via programmable mode: `claude -p "/feature '…'" --output-format stream-json --dangerously-skip-permissions --model <best> --verbose > output.jsonl` — watched the JSONL stream append live while the agent produced a comprehensive feature plan (user story, problem/solution statement, implementation phases, testing, acceptance criteria).

**Workout module:**
- **Goal:** Build a chore→plan→implement pipeline from templates and ship one chore with exactly two prompts.
- **Prerequisites:** Claude Code; a repo with at least one test command (or `disler/tac-3`).
- **Steps:**
  1. Create `.claude/commands/chore.md`: Purpose ("create a plan in specs/ to resolve the chore"), Instructions, Relevant Files, a Plan Format (Chore / Description / Relevant Files / Step-by-Step Tasks / Validation Commands / Notes), ending with `Chore: $ARGUMENTS`.
  2. Create `.claude/commands/implement.md`: "Read the plan at $ARGUMENTS. Think hard. Implement every step in order. Run the validation commands. Report: summary + files changed."
  3. Run `/chore "<one real small task in your repo>"` and read the generated plan in `specs/`.
  4. Open a NEW terminal + fresh Claude instance; run `/implement specs/<plan>.md`.
  5. Verify via the plan's validation commands yourself; commit specs + code.
  6. Repeat headlessly: `claude -p "/chore '<another chore>'" --output-format stream-json --verbose > run.jsonl` and watch the stream.
- **Done-when:** One chore ships end-to-end with two prompts, the plan file exists in `specs/`, and validation commands pass on rerun.
- **Level-up:** Add `/bug` (with Steps to Reproduce + Root Cause Analysis sections) and `/feature` (with user story + phased implementation) templates; specialize one template to a specific subsystem of your codebase.

**Quote of the lesson:** "The plan is the prompt — and that means great planning is great prompting."

---

## TAC-4: AFK Agents

**Thesis:** Move from in-loop prompting to out-loop systems: with the four PITER elements (prompt input, trigger, environment, review), your templated engineering chains into AI Developer Workflows that go from GitHub issue to pull request while you're away from the keyboard — outperforming generic cloud agents because they run *your* templates on *your* problems.

**Named frameworks & mnemonics:**
- **Tactic #4: Stay Out The Loop.** In-loop = "sitting on their device, prompting back and forth"; out-loop = "off-device agentic coding… you write high-to-low-level prompts that you pass off to your agentic pipeline, then you go AFK."
- **AFK Agents:** "agents that run while we're away from the keyboard."
- **The four elements of AFK agents — PITER ("Peter"):** **P**rompt input, **T**rigger, **E**nvironment, **R**eview. Dan's defaults: GitHub issues (P), GitHub webhooks via Cloudflared tunnel (T), a dedicated Mac mini the agent fully controls (E), GitHub pull requests (R).
- **ADW (AI Developer Workflow) — full definition:** "a reusable agentic workflow that combines code, agentic prompts, and agents to deliver results autonomously… the synthesis of previous-generation deterministic code and new-generation non-deterministic language models, prompt chains, and now agents." Highest leverage point and highest composition level. "In the future these will just be known as scripts."
- **The agentic layer (first named here):** "a net new agentic layer around your codebase" formed by two directories: `.claude/commands` (prompts) + `adws/` (workflows).
- **Issue classification pattern:** an agent classifies each issue as chore/bug/feature and routes to the right template — "you need to be able to target specific classes of problems."
- **Health check pattern:** a pre-flight ADW validating env vars, repo access, and Claude Code before running workflows.
- **adw_plan_build (the first full ADW):** fetch GitHub issue → classify → create branch → planner agent (runs `/chore` / `/bug` / `/feature`) → builder agent (runs `/implement` on the generated plan) → create PR — with issue comments as a live feed throughout.

**Nuggets:**
- "Your agentic pipeline is too valuable to outsource to a third party tool… You want to own your agentic pipelines."
- Cloud tools "are literally designed for everyone's codebases, not yours."
- "There are increasingly more chores, bugs, and features that don't require your expertise at all."
- "Stay out the loop… models will improve and tools will change. When you stay out the loop, you leverage this fact."
- "If you are not wrong now, you will be. It's only a matter of time."
- "We're not playing today's game, we're playing tomorrow's."
- "Chores are the simplest unit of engineering work that your agent should be taking off your plate with no debate at all."
- "It doesn't matter if our agent can solve every problem if we don't know that it's solved. We need to observe, we need to report, we need to log and monitor."
- "No ad hoc prompts as strings inside of the codebase. Everything's isolated so that we can improve it."
- "Every time you miss something… you don't fix the issue, you fix the system that caused the issue. You fix your templates, you fix your ADW."
- "The details are everything. There's a reason why a lot of agentic coding tools don't work — they don't understand your codebase."
- "Success is absolutely planned. You can plan success into your codebase by templating your engineering."
- "For your build and implement steps, use the most powerful model you can."
- "In-loop agentic coding is great for experimentation, exploring new territory, and very hard specific problems. But let's be real — most of engineering is not that."
- "Start with low hanging fruit… template the chore, then move up to bugs, and eventually the feature level."
- "These four elements can be anything… Don't read into how this is configured too much. Focus on the composable units."
- "The ROI here is insane. I want you to get to the aha lightbulb moment you'll get when you run one of these end to end."
- "Your ADWs can operate on your ADWs. So, you know, don't get too meta."
- "We're focusing on the what, not the how. The how is already encoded in the codebase."

**What Dan actually did/built:**
1. **End-to-end demo first:** created GitHub issue "ADW documentation — /chore document the ADW directory, read everything in adws, update README" → webhook fired → Mac mini agent environment picked it up (screen-shared live) → classified as chore → new branch → planner agent wrote the spec → implementer agent built it → PR posted back — total 5 minutes, with live GitHub issue comments the whole way.
2. Disabled the webhook, then `git clone https://github.com/disler/tac-4.git` locally; ran `/install` (unsets remote origin, walks you through creating your own repo, copies `.env` files, installs deps, reports "action required" items).
3. Set root-level `.env`: `ANTHROPIC_API_KEY` and `CLAUDE_CODE_PATH` (via `which claude`) — "the agent SDK currently only runs with the API key."
4. Created issue #33: "JSONL support" — mid-level prompt with constraints (stdlib only, concat nested fields, handle arrays, update the UI).
5. Ran the health check: `uv run adws/health_check.py 33` — verified env, repo, Claude Code, and posted a health comment to the issue.
6. Ran `uv run adws/adw_plan_build.py 33` with a local trigger — watched: unique ADW ID assigned, `jsonl-support` branch created, issue classified as feature, `/feature` planner ran, `/implement` builder ran, PR created (~17 min).
7. Walked the ADW code: `classify_issue` (maps to slash commands), branch creation, `build_plan` (template request: agent name, slash command, args, model), `execute` → Claude Code in programmable mode with `--dangerously-skip-permissions` (safe in its own environment); per-session log files via Claude Code hooks; per-ADW agent directories (planner, implementer, branch generator, issue classifier, PR creator, committers).
8. Reviewed and manually tested the PR: JSONL upload option in UI, sample data files, comprehensive tests; regression-tested existing queries.

**Workout module:**
- **Goal:** Ship one GitHub issue to PR with zero keyboard time between prompt and review.
- **Prerequisites:** TAC-3-style templates (`/chore`, `/feature`, `/implement`); a GitHub repo you own; `gh` CLI; `ANTHROPIC_API_KEY`.
- **Steps:**
  1. Write `adws/adw_plan_build.py` (uv single-file script): parse issue number → `gh issue view` for title/body → agent 1 classifies chore/bug/feature (its own prompt file) → create branch → agent 2 runs the matching template via `claude -p "/feature '<issue body>'" --output-format stream-json` → agent 3 runs `claude -p "/implement <plan path>"` → commit → `gh pr create`. Post `gh issue comment` progress updates between every step.
  2. Write `adws/health_check.py` that validates env vars, repo remote, and a trivial `claude -p "respond OK"` call.
  3. File a real chore as a GitHub issue; run the health check, then the ADW with the issue number.
  4. Review only the PR — do not touch the branch.
  5. (Trigger upgrade) Add a webhook: expose a tiny listener via `cloudflared tunnel` or ngrok that runs the ADW on `issues.opened`.
- **Done-when:** An issue you wrote from the GitHub UI (or your phone) results in a merged-quality PR with live issue comments, and you never opened the working branch locally.
- **Level-up:** Move the environment off your machine — a spare box, VM, or container that listens for webhooks 24/7 — and run a feature-class issue through it.

**Quote of the lesson:** "You don't fix the issue — you fix the system that caused the issue."

---

## TAC-5: Close the Loops

**Thesis:** Your work is useless unless it's tested, and testing is now your agents' job: encode every way you'd validate production-ready work into commands and tools (linters, unit tests, builds, Playwright browser tests), structure prompts as request→validate→resolve, and your agents self-correct until the work is provably done.

**Named frameworks & mnemonics:**
- **Tactic #5: Always Add Feedback Loops.** "Your work, my work, any engineer's work is useless unless it's tested."
- **The core validation question:** "Given a unit of valuable work that's production ready, how would you, the engineer, test and validate this work? If you can answer this for every class of work and encode the answers into a command or tool call, you will fly while other engineers run."
- **Closed loop prompt anatomy (3 parts):** **Request → Validation → Resolution.** "This prompt instructs the agent to validate itself."
- **Closing the loop (definition):** "letting your agent operate on work, calling a command or tool to get feedback on the success of the work… your agent continues to build until the feedback is positive. When you do this, you let the code write itself."
- **In-loop / Out-loop / Closing-the-loop terminology:** in-loop = you prompting back and forth; out-loop = high-level prompt through the PITER system on an isolated machine; closing the loop = the agent's own execute-validate-reflect cycle.
- **Testing hierarchy of trust:** "The ultimate test will always be your users. The next best test used to be you. Now the next best test is an army of agents validating your entire codebase with regression tests and, most importantly, end-to-end tests."
- **Tests as rule of law:** "What's more important, the code or your tests? The answer should be your tests. Your tests should be the rule of law in your codebase."
- **Playwright MCP:** browser control as a validation tool — open browser, type, click, screenshot, read images, verify results.
- **adw_test (the testing ADW):** fetch issue → run full test suite (`/test` prompt returning standardized JSON) → parse results → per-failure isolated **resolver agents** (`/resolve_failed_test`) in a retry loop → run e2e tests (`/test_e2e` HOP looping over e2e test files) → report → commit → push/PR.
- **E2E test file format:** test name, test steps, `verify` IDK statements, success criteria — stored as markdown prompts, run through a HOP with preconditions (reset DB, ports, screenshot directory) and a JSON output format.
- **Validation commands templated into every plan:** the chore/bug/feature plan formats include a Validation Commands section by default, plus "if this bug affects UI or user interactions, create an end-to-end test."

**Nuggets:**
- "Our most valuable contribution is the experience we create for our users."
- "Have your agents test on your behalf like you never could, at scales you never will achieve. This is the gift of generative AI."
- "You probably opened the browser and clicked through your new feature. What a waste of time."
- "Engineers that test with their agents win. Full stop, zero exceptions."
- "The value of tests is multiplied by the number of agent executions that occur in your codebase."
- "With every passing set of tests, you free your context window and you stop second-guessing."
- "Test, let your agents scale your success. Same game, different day, new tools, exponential impact."
- "Testing at its core is simple: did it do what you designed it to do, and did it break anything else along the way?"
- "Everything is one tool call away. Tools are just functions and functions can do anything."
- "We will be the ones prompting the errors" — as models improve, your validators catch *your* mistakes.
- "It's not good enough to resolve once if that resolution causes something else to break — rerun every validation step top to bottom."
- "We're stacking the confidence" — each loop (ruff → pytest → compile → tsc → build → e2e) adds certainty.
- "Your agent has more agency with self-validating loops."
- "Hand off more responsibility to your agents, not less."
- "Lean into the future. Don't lean into the present, don't lean into the past."
- "We want end-to-end agents, not in-loop agents… we don't want to be babysitting."
- "Always run fresh agents… no context pollution."
- "When you're setting up your ADW to test, you might point this at staging or even a production test account."
- "Everything starts with a single prompt. Everything starts in the loop, and then slowly move it out the loop."
- "One agent running here, one agent running there" — parallel issue-fixing is normal once loops are closed.
- In-loop limitation: "You're pretty much limited to one agent unless you're conscious about everything that you're changing" (no worktrees yet).

**What Dan actually did/built:**
1. `git clone https://github.com/disler/tac-5.git`; `/install` (now resets the SQLite DB and copies both app and tac-4 `.env` files).
2. **Fired the big one first:** GitHub issue "adw_plan_build_test feature — create a new button (generate random NL query)" → webhook → dedicated agent box began the full plan-build-test pipeline in the background for the whole lesson.
3. **Closed loop v1 (linter):** prompt = update `@sql_processor` to comment out validation + "validate your work with: ruff check" — ruff flagged the unused import via stdout; the agent fixed and re-ran until clean.
4. **Closed loop v2 (3 validators):** remove insights endpoint + move `load_dotenv`; validate with `ruff`, `uv run pytest`, and `python -m py_compile`. Watched the agent: ruff caught import-order, pytest caught the previously commented-out validation (fixed without any memory of the prior session), all three loops closed.
5. **Closed loop v3 (full-stack + browser):** a reusable validation prompt — backend checks, frontend checks (`tsc --noEmit`, `bun run build`), then **Playwright MCP**: open the local URL, screenshot before, type a query, screenshot after, read both images, verify the NL query returned exactly 7 results. Verified the screenshots himself by re-running the query manually.
6. Caught a side effect via git status — tests had written junk tables to the "production" SQLite DB — bookmarked it as the next bug.
7. **Templated feedback loops:** showed the `/bug` meta prompt now bakes "Validation Commands" into every generated plan plus the conditional e2e-test instruction; ran `/bug 111 adw-111 "tests are writing junk data to the live database — run tests in memory"` → plan with sqlite3 checks, targeted pytest, before/after table diffs. `/implement` in a fresh agent.
8. Ran a second bug in parallel: `/bug 222 …"disable the input query while running and add a debounce"` → plan included a new e2e test file (clean user store: test steps, `verify` statements, success criteria); implemented it.
9. Walked `adws/adw_test.py`: `/test` prompt returning standardized JSON so failures fan out to isolated resolver agents; retry parameters; `/test_e2e` HOP looping every e2e file with preconditions and screenshot output.
10. Traced a failed run on the agent box by ADW ID through `agents/` + `logs/` directories → found the root cause was an Anthropic API 500, not the workflow.
11. Reviewed the finished plan-build-test PR: new "generate random query" button working in the agent's environment, with a noted UI nit — motivation for the review step in TAC-6.

**Workout module:**
- **Goal:** Convert your manual verification ritual into closed loops an agent runs, including one browser-level e2e test.
- **Prerequisites:** TAC-3/4 setup; a linter, a test runner, and a build command in your repo; Playwright MCP configured in `.mcp.json`.
- **Steps:**
  1. Write down every step you personally take to verify a change ships (lint, tests, build, click-through). This is your validation inventory.
  2. Write a closed-loop prompt: Request (one small refactor) + Validation (`ruff check` or equivalent) + Resolution ("if any issues, fix and re-run until clean"). Run it; watch the loop close.
  3. Scale to three validators: linter + unit tests + compile/build, with the instruction "run in order top to bottom; if any step fails, stop, resolve immediately, then rerun EVERY validation step."
  4. Add the browser: a validation prompt that starts your app, opens it via Playwright MCP, screenshots before/after a scripted interaction, and verifies a precise expected result.
  5. Bake a "Validation Commands" section into your `/chore` `/bug` `/feature` plan formats, plus "if this affects UI, create an e2e test file" with a test-steps/verify/success-criteria format.
  6. Run one `/bug` through plan→implement and confirm the generated plan carries its own validators.
- **Done-when:** An intentionally broken change gets fully repaired by the agent with zero human diagnosis, and one e2e screenshot pair proves a UI behavior.
- **Level-up:** Build `adw_test.py` — run all tests, emit JSON results, spawn one fresh resolver agent per failure with a retry cap, then commit and PR the fixes.

**Quote of the lesson:** "Now engineers that test with their agents win. Full stop, zero exceptions."

---

## TAC-6: Let Your Agents Focus

**Thesis:** Complete the SDLC with dedicated review agents (is what we built what we planned? — with screenshot proof) and document agents (including conditional docs that feed future agents), all governed by the tactic that sidesteps context pollution: one agent, one prompt, one purpose.

**Named frameworks & mnemonics:**
- **Tactic #6: One Agent, One Prompt, One Purpose.** "Use specialized agents with focused prompts to achieve a single purpose. No agent runs more than a single prompt."
- **The SDLC as questions and answers:** Plan asks "what are we building?" · Build asks "did we make it real?" · Test asks "does it work?" · **Review asks "is what we built what we planned?"** · Document asks "how does it work?" — "Testing answers does it work, but review answers is what we built what we asked for. Now prove it."
- **Context pollution / context overloading / toxic context:** "Massive context windows often lead to a distracted, confused agent."
- **The three constraints of agentic engineers:** (1) the context window, (2) the complexity of your codebase + problem, (3) your abilities. "Specialized agents bypass two out of three. Model intelligence is not a constraint — don't use it as an excuse."
- **Four advantages of one-one-one:** free up the context window; let your agent focus; every prompt is committed → reproducible and improvable; you "effectively create evals for the agentic layer of your codebase."
- **Minimum context principle:** "You want to context engineer as little as possible — the minimum context in your prompt required to solve the problem."
- **Review issue severity classes:** **skippable, tech_debt, blocker** — only blockers stop the pipeline; "if you ask them to find something, they'll find something," so give agents the tools to delineate what matters.
- **adw_review:** find spec from branch → review implementation against spec via `/review` (git diff + Playwright screenshots) → upload screenshots to a Cloudflare R2 bucket → if blockers, loop `create_and_implement_patch` (max retries) → post results + update PR.
- **adw_patch / the patch prompt:** "create a focused patch plan to resolve a specific issue with minimal targeted changes" — a surgical template meta prompt, distinct from chore/bug/feature.
- **adw_document / the `/document` prompt:** generate concise markdown docs into `app_docs/` from git diff vs main + the spec; **`app_docs/` (your app) vs `ai_docs/` (third-party docs)**.
- **Conditional documentation (`conditional_docs.md`):** "read this to check if your task requires additional documentation; if your task matches any conditions listed, include those documentation files" — referenced inside `/bug`, `/chore`, `/feature`, `/patch`, and `/prime`, creating "a complete software developer lifecycle feedback loop" from documenting back into planning.
- **State object (`state.json`):** ADW ID, branch name, plan file, issue class — meta info that travels along every workflow so composed ADWs can chain.
- **Composable ADWs:** `adw_plan_build_review`, `adw_plan_build_document`, `adw_plan_build_test_review` ("probably the winning workflow"), each a standalone uv script chained by ADW ID.
- **Optimal presence = 2:** "one at the beginning for your prompt input, one at the end for your review and PR merge."

**Nuggets:**
- "Isn't more context better for your agent? This is not true."
- "Big tech is chasing the all-in-one god model, the super agent that can do it all. That's not what we're doing here. Real engineering requires real developer workflows, not some pie-in-the-sky god model."
- "Every step of engineering requires a different set of information, a different approach, a different perspective, a different set of tools and context."
- "A focused engineer working on a single task is a productive engineer. Agents are the same."
- "When your agent's performance drops, your performance drops."
- "Every piece of context you add increases the number of variables your agent has to reason about."
- "If your agent is running compact, it is losing information." (compaction is a band-aid)
- "While other companies run big context windows blown away at the end, you'll run single focused prompts you can pinpoint and improve."
- "Everything comes down to the prompt level. All the ADW surrounding deterministic code is just support for the agents doing the real work."
- "There's no excuse for having poor documentation" (every ADW script self-documents its workflow at the top).
- "You want your agents communicating proof — a hard asset that proves what was built is what you asked for. Screenshots, reports, ideally video."
- "Even when your agent is wrong, when it presents you with proof that it thinks it's right, you can quickly say yes or no."
- "Whatever you would do to review that the thing is what you asked for — that's what you embed into your review step."
- "Why didn't you just do that by hand? You're missing the point… This isn't about you anymore. It's about teaching your agents to build on your behalf, so that it can be about you again."
- "Do you want to be an agentic engineer, or an engineer of the past?"
- "I'm not blaming the model for this. I'm blaming my skills. I'm blaming the ADWs."
- "The value in your ADWs isn't in a single workflow — it's the power of combining workflows: isolated, reviewable, improvable."
- "Reduce the number of human-in-the-loop points in your workflow."
- "It's a good practice to encode the agent names as constants right at the top of the file."
- Documentation timing: "how you document and when to include your documentation is the tricky part."

**What Dan actually did/built:**
1. `git clone https://github.com/disler/tac-6.git`; `/install` in Opus + YOLO mode (adds Cloudflare R2 env vars for image upload).
2. Toured the new ADWs: `adw_review`, `adw_patch`, `adw_document`, plus composed `adw_plan_build_review` and `adw_plan_build_document` (standalone uv scripts chained by ADW ID).
3. Created issue #14: one-click table export + result export as CSV (two new endpoints, download icon placement "directly to the left of the hide button").
4. Ran `uv run adws/adw_plan_build_review.py 14` on his own machine (to inspect in real time; agents own the repo — "we shouldn't be doing anything alongside them").
5. Walked the review internals while it ran: `state.json`, branch validation, R2 uploader init, `run_review` → `/review` prompt (collapse-first reading: "review work against spec, use git diff, capture screenshots, report issues or success"), prompt-level variables as on-the-fly IDKs, JSON `ReviewResult`/`ReviewIssue` Pydantic types, skippable/tech_debt/blocker classes, patch-resolution loop with max retries.
6. Reviewed the posted screenshots: feature worked, but the export button was misplaced (agent missed "left of the hide button") — a blocker the review agent failed to flag.
7. Filed a patch: issue comment "make sure download button for query results is just to the left of the hide button," then `uv run adws/adw_patch.py <issue> --adw-id <same ADW ID>` (after first passing the wrong issue number — state file caught it). Patch plan generated into `specs/patch/`, implemented, UI verified fixed.
8. Post-mortemed the miss: the `/review` prompt captured screenshots but never read them back into context (fix: "for every image you take, read it in during the review process"); Playwright MCP wasn't in `--vision` mode; and the **test step had been skipped entirely** — `adw_plan_build_test_review` would likely have caught it.
9. Ran `uv run adws/adw_document.py <issue> <same ADW ID>`: generated `app_docs/` feature doc (screenshots, what changed, files touched, how to use) from git diff + spec, AND agentically updated `conditional_docs.md`.
10. Showed `conditional_docs` referenced in `/bug`, `/chore`, `/feature`, `/patch`, `/prime` — the planning↔documentation loop closed.
11. Scored the run against KPIs: attempts 2 (patch needed), streak broken, presence ~3 vs the optimal 2.

**Workout module:**
- **Goal:** Add review and document agents to your pipeline, with image proof and conditional docs.
- **Prerequisites:** TAC-5 pipeline; Playwright MCP; any public bucket (R2/S3) or GitHub image upload for screenshots.
- **Steps:**
  1. Write `/review.md`: variables at top (ADW ID, spec file, agent name, screenshot dir); instructions to git-diff against main, compare against the spec, capture screenshots of critical functionality, READ each screenshot back in, and output JSON `{success, review_summary, issues[{class: skippable|tech_debt|blocker, …}], screenshots}`.
  2. Write `/patch.md`: "create a focused patch plan resolving one specific issue with minimal targeted changes" → plan into `specs/patch/`.
  3. Write `adw_review.py`: load state → run `/review` → upload screenshots → for each blocker, fresh patch-plan agent + fresh `/implement` agent (max 3 retries) → post results with image links.
  4. Write `/document.md`: template meta prompt generating a doc in `app_docs/` from git diff + spec, then updating `conditional_docs.md` with when-to-read conditions.
  5. Reference `conditional_docs.md` in the Relevant Files section of `/chore`, `/bug`, `/feature`, and `/prime`.
  6. Run plan→build→test→review→document on one feature; deliberately give a precise UI placement instruction and check whether review catches deviations.
- **Done-when:** The review step posts screenshot proof with a severity-classified JSON verdict; a follow-up plan automatically pulls in the new documentation via conditional docs.
- **Level-up:** Make review self-healing — auto-run the patch loop on blockers without your involvement — and upgrade proof from screenshots to screen-recorded video.

**Quote of the lesson:** "One agent, one prompt, one purpose."

---

## TAC-7: ZTE — Secret of Agentic Engineering

**Thesis:** With a full agentic layer, you fire five issues in parallel (git worktrees, model-set knobs) and agents ship end to end — and once your streak proves you add no value reviewing a problem class, you drop the R off PITER and target Zero Touch Engineering. The secret: TAC was never about the SDLC — it's about composable agentic primitives that solve any problem class.

**Named frameworks & mnemonics:**
- **Tactic #7: Target Zero Touch Engineering.** "Just like you've stopped coding, you'll stop reviewing… This is YOLO mode for your AI developer workflows. Maximum confidence mode for agentic engineering."
- **The Agentic Engineering Velocity Scale (3 levels):** **In loop → Out loop → ZTE (Zero Touch Engineering).**
- **PITER → PITE:** "You'll drop yourself off the end of the Outloop Peter framework and it becomes Pete, not Peter. You'll drop off the review."
- **The ZTE realization:** "This human in the loop model is a bottleneck. I'm not catching any bugs anymore. I'm not adding any value outside of the agentic layer. I'm going to remove the human review for this class of problems." Threshold intuition: ~90% confidence, rising with every model/tool/template improvement.
- **The Secret of Tactical Agentic Coding:** "It's not about the software developer lifecycle at all. It's about composable agentic primitives you can use to solve any engineering problem class." The SDLC "is powerful, but it's a remnant of the past… a package for me to deliver a message to you."
- **ISO workflows (git worktree isolation):** `adw_sdlc_iso` (plan→build→test→review→document, isolated), `adw_sdlc_zte_iso` (SDLC + ship), `adw_patch_iso`, `adw_ship_iso`. Every workflow creates its own worktree under `trees/` with its own ports, env, and install (`/install_worktree`) — "the easiest way to parallelize your workflows." Docker/VMs work too; "it only matters that you can."
- **Model sets (base | heavy):** an encoded IDK passed in the issue body; `agents.py` maps each slash command to a base or heavy (Opus-class) model; parsed by `/classify_adw` at workflow start. "A knob to turn to increase the compute that your workflow uses."
- **The ship step:** checkout main outside the tree → merge the feature branch → post success — "approve and merge the PR agentically… deploy, ship."
- **Presence math:** best out-loop coders have presence 2 (prompt + review); ZTE has presence 1 (prompt only).
- **The four postures toward the future:** run away · stand still · walk toward it · **sprint** ("beat everyone else there").

**Nuggets:**
- "You'll witness something most engineers dismiss as impossible: a codebase that nearly runs itself."
- "We can scale our impact as easily as copying a file" — engineering digitized into the agentic layer.
- "Think in the gray. We're not jumping to out-loop. We're progressively handing off more and more work."
- "It's not in loop versus out loop. It's in loop moving toward out loop, one day at a time."
- "We're not solving the problem directly anymore… the rate at which you can solve your specific problem is drastically scaled up when you put your effort into your agentic layer."
- "You can encode any information dense keyword you want that changes your workflows."
- "You do want to stay on the review system as much as possible… a comprehensive review system is a massive edge for increasing your review velocity."
- "Agents took images and gave us proof that the feature has shipped… Remember what review answers: not 'does it work?' but 'is what we built what we asked for?'"
- "Engineering is not black and white. It's gray. You progress toward agentic engineering one day at a time."
- "You can't vibe code this stuff. Your agent is operating as you would."
- "I parallelized myself across five features."
- "When the agents arrived, something changed. We weren't just AI coding anymore. We started orchestrating intelligence."
- "I'm giving you an information arbitrage… the question is, are you going to use it?"
- "First, go after chores, then bugs, then features. Solve the stupid, simple problems that waste your time, then scale up."
- "If you don't invest in the agentic layer, how will you know when agents can solve your problem class end to end with no oversight?"
- "I can guarantee you right now, you are doing engineering work you do not have to do."
- "Everything starts small and then it compounds… they'll do it five times in a row, and you'll realize you add no value by reviewing. In fact, you slowed things down."
- "It's not about being right. It's about being prepared to win."
- "If you don't believe your agents can run your codebase, you're cooked."
- "The agentic layer is where 1x input becomes 10x output, and 10x input becomes 100x."
- "You must update your beliefs. This is a belief change you must make for 10-100x scaled engineering with agents."
- "The primitives are the atoms of agentic engineering. Master them and you can build any molecular structure you need."
- "It's you, the engineer with their boots on the ground… That's where the big AI gains come from. Not AGI, not ASI."

**What Dan actually did/built:**
1. With the dedicated agent box listening to webhooks, fired **five GitHub issues back to back**: (1) increase drag-and-drop surface area (feature, `adw_sdlc_iso`); (2) JSON export (feature); (3) generate random synthetic data from a table's schema (mid-level feature, `model_set heavy`); (4) upgrade query-generation model to o4-mini (chore); (5) CSV label mismatch (bug via `adw_patch_iso`). All ran **in parallel** on one machine via git worktrees, live-commenting on their issues.
2. `git clone https://github.com/disler/tac-7.git` locally; `/install`; toured the new ADWs (`adw_sdlc_iso`, `adw_sdlc_zte_iso`, `adw_ship_iso`) — SDLC composed from the same lower-level pieces, plus worktree setup (`/install_worktree` with assigned ports and tree path).
3. Jumped inside a live agent's environment mid-run: `code trees/<adw-id>` — full sparse copy of the app on its own branch; showed `state.json` tracking meta info.
4. Explained model sets: `agents.py` maps slash commands → base/heavy models; `/classify_adw` parses the model set + workflow from the issue at kickoff; `think hard` IDK still active inside prompts.
5. Reviewed completions as they landed: o4-mini chore PR (~100 lines, conditional docs auto-updated, docs + spec both attached); patch bug done; drag-and-drop review posted **screenshot proof** of the new overlay ("Drop to create a table").
6. Did deliberate in-loop verification of the drag-drop branch via a `/in_loop_review` prompt (pull branch, reset DB, restart app, open browser) and manually exercised drag-and-drop and JSON export.
7. Watched the JSON-export agent hit a blocker in review and self-patch; the heavy-model random-data feature ran ~27 min on Opus.
8. **ZTE demo:** issue "update background color to light green — `adw_sdlc_zte_iso`" → plan, build, test, review (screenshot proof of green background), document, then **ship**: agent checked out main, merged the branch, closed the issue. `git pull origin main` locally showed the change live. "This is zero touch engineering."
9. Delivered the secret-of-TAC monologue: composable agentic primitives over SDLC; the ADW arrangement "is completely arbitrary — the one way is the way that ships in your codebase."

**Workout module:**
- **Goal:** Run two ADWs in parallel via git worktrees, then take one trivial problem class to zero-touch (auto-merge).
- **Prerequisites:** TAC-6 composed pipeline; webhook or local trigger; a repo where auto-merging to main is safe.
- **Steps:**
  1. Add worktree isolation to your ADW: at start, `git worktree add trees/<adw-id> -b <branch>`, run `/install_worktree` (copy envs, install deps, assign unique ports), and run all agents with `cwd` inside the tree.
  2. Add a model-set knob: a `classify_adw` step that parses `model_set: base|heavy` from the issue body and a map from each slash command to a model.
  3. File two issues simultaneously (one chore, one small feature) and confirm both worktrees run concurrently without collisions.
  4. Write `adw_ship.py`: from the root repo, checkout main, merge the ADW branch, push, close the issue with a success comment.
  5. Compose `adw_sdlc_zte.py` = plan→build→test→review→document→ship. Pick a genuinely trivial class (style tweak, copy change) and run it end to end with zero review.
  6. Verify by pulling main — the change should already be there.
- **Done-when:** Two parallel worktree runs complete cleanly, and one issue goes prompt→production merge with your presence = 1 (the prompt).
- **Level-up:** Harden the ZTE gate: require N consecutive one-shot successes on a problem class (tracked in a log) before ship is allowed; add a parallel double-review (two review agents must both pass) as the merge condition.

**Quote of the lesson:** "The secret of tactical agentic coding is that it's not about the software developer lifecycle at all. It's about composable agentic primitives you can use to solve any engineering problem class."

---

## TAC-8: The Agentic Layer

**Thesis:** All eight tactics compress into one: prioritize agentics — spend the majority of your engineering time on the agentic layer (adws/ + prompts + plans) that rings your codebase, because you can teach compute to engineer your way. The daily guiding question: am I working on the agentic layer or in the application layer?

**Named frameworks & mnemonics:**
- **Tactic #8: Prioritize Agentics** ("prioritize your agentic layer"). "Agentics refer to systems or entities capable of autonomous action and decision-making. This tactic represents all others… all tactics are compressed into this tactic."
- **The Agentic Layer (full definition):** "the combination of traditional deterministic code stored in your ADWs directory as a scriptable layer, with the new non-deterministic agentic technology — the language model, the agent, Claude Code and whatever comes next… the old world of deterministic code and the new world of agentic prompts." Visual: "a ring around your codebase — at first thin, then thicker as you scale agentics in."
- **Agentic layer vs Application layer:** application layer = DevOps + infrastructure + database + raw app. Rule of thumb: **at least half your engineering time on the agentic layer.**
- **The Minimum Viable Agentic Layer (3 pieces):** an **ADWs directory** (any scripting layer — uv, bun, shell), **prompts** (`.claude/commands`), and **plans** (`specs/`) — kept strictly isolated from the application.
- **The Gateway Script (`adw_prompt`):** the thinnest ADW — a script that calls one Claude Code agent with one prompt and manages surrounding state/logging. "This script is the gateway into agentic coding."
- **The Final Guiding Question (the meta-tactic):** **"Am I working on the agentic layer or am I working in the application layer?"** — "if you forget everything else, this is the only question you need."
- **The eight-tactic recap (canonical order):** Stop Coding → Adopt Your Agent's Perspective → Template Your Engineering → Stay Out The Loop → Always Add Feedback Loops → One Agent, One Prompt, One Purpose → Target Zero Touch Engineering → Prioritize Agentics.
- **Commoditization of implementation:** "with agentic coding, not only is code a commodity, but the implementation as well" — early signs of "the commoditization of engineering." Value moves up to "system design, system architecture, encoding your domain expertise, quality control, and most importantly creative problem decomposition."
- **Four example agentic layers (tac-8 apps):** (1) **agentic layer primitives** (empty starter: prime/start/implement/chore/feature + adw_prompt, adw_slash_command, adw_chore_implement); (2) **multi-agent "to-done"** (tasks.md as two-way prompt UI, cron trigger every 5s, per-task git worktrees, tags like `opus` and `adw_plan_implement_update_task` as inline IDKs, status emojis + commit hashes); (3) **agentic prototyping** (Notion board as prompt input + review system, cron trigger, template meta prompts that build entire uv MCP servers from one card); (4) **agents-in-app** (in-app `/aea` agents "Nexus" and "Roon" — the one sanctioned exception to one-agent-one-prompt, continuing a session by passing the session ID back).

**Nuggets:**
- "Build the system that builds the system — we're talking about the new agentic layer of your codebase."
- "Machines that operate with your judgment, shipping your way, getting work done autonomously in your product."
- "This course is an opportunity to pull the future into the present."
- "This is not a Claude Code course… Claude Code represents the first viable tool that unlocks agentic engineering, but it won't be the last."
- "Keep your eyes on the primitives. Focus on the pieces that make the whole."
- "Building an agentic layer is parabolic. Put 10 minutes in, get two hours of value out or more."
- "In-loop is a great place to start, a great place to do deep work, and a terrible place to stay."
- "The power of agents isn't in one, it's in many."
- "Focus on problem classes, not one-off fixes."
- "I have solved the problem class of building Astral UV MCP servers. It's done." (one prompt → full MCP server)
- "The big labs are all doing this right now — insane feedback loops where agents iterate against some validation function. If they can do it for world-changing problems, you can do it on your codebase."
- "There is a set of validations in your codebase that once run ensures everything works perfectly. The only question is: do you know what it is?"
- "You will become a bottleneck in the process… then you'll convert the Outloop framework from Peter to Pete."
- "Not only will you stay out the loop — getting in the loop will be harmful."
- "Don't make the mistake of thinking you can outperform your team's best engineering practices encoded into a template meta prompt that kicks off five to ten agents per problem."
- "Your place of competition is now net new innovation."
- "An agentic engineer operates on living pieces of software that work while they sleep."
- "There is no competing with an agentic engineer. You must have fleets of agents operating on your behalf to compete with an agentic engineer."
- "Command your agentic layer to run and control your application layer."
- "Never forget who this is all for: customers, users, team, company, you."
- "You are here very early. It might not feel like it, but you're here early."
- "In this phase there are two things that matter more than ever: focus and signal."
- "You only need to catch one wave to change everything."

**What Dan actually did/built:**
1. `git clone https://github.com/disler/tac-8.git` — five distinct example apps, each with its own agentic layer.
2. **App 1 — agentic layer primitives:** walked the minimum viable layer (adws/ + `.claude/commands` + specs). Ran `/prime`, `/start`; showed `/implement` (HOP) and `/chore` + `/feature` template meta prompts. Ran the gateway script: `uv run adws/adw_prompt.py "list all files in the ADWs directory and a concise output of their purpose"`; then `adw_slash_command.py` firing `/start`; then `adw_chore_implement.py` — two agents chained (chore plan → path passed into implement), noting the Claude Code SDK (Python/Bun) exists but TAC uses the CLI directly "to have full control."
3. **App 2 — multi-agent to-done (data science/Jupyter):** pasted ~10 tasks into `tasks.md`; ran the cron trigger ADW (`uv run adws/adw_trigger_cron.py`, 5s polling); watched tasks fan out into five git worktrees, statuses updating in-file (sun emoji + commit hash while running, check when done, timer emoji for blocked-on tasks), `opus` and `adw_plan_implement_update_task` tags routing work to heavier workflows; opened `code trees/<name>` to verify a filtered tweets-positive-only dataset and follow-on augmented-training tasks stacking on completed work.
4. **App 3:** skipped on camera ("open that up on your own").
5. **App 4 — agentic prototyping via Notion:** a Notion board (Not Started / In Progress / Human-in-the-loop Review / Failed / Done) as prompt input + review system; ran `uv run adws/adw_trigger_cron_notion_tasks.py --once`; agents picked up cards, moved them agentically, created worktrees, and built prototypes — including a complete **uv MCP server for system info** from one card via the `uv_mcp` template meta prompt + `ai_docs/`; verified by adding the generated `.mcp.json` and calling `get_memory_info`, `get_cpu`, `get_disk` from Claude Code.
6. **App 5 — agents in the app:** the NL-SQL app with an embedded agent server (`sh scripts/start` + `sh scripts/ae_server_start`); Cmd+P → `/aea` spun up in-app agents "Nexus" and "Roon"; asked one about the codebase while the other renamed the "generate random query" button — the sole session-continuation exception to one-one-one.
7. Recapped all 8 tactics, the 12 leverage points, and the KPIs; compressed everything into the final guiding question; closed with the commoditization-of-implementation thesis and the "orchestrating intelligence" epilogue.

**Workout module:**
- **Goal:** Bootstrap a minimum viable agentic layer on YOUR real codebase and prove it with one gateway run and one chained ADW.
- **Prerequisites:** Any real project you maintain; Claude Code; uv (or bun/shell).
- **Steps:**
  1. Create the three pieces: `adws/`, `.claude/commands/`, `specs/` — strictly outside your app directories.
  2. Write `/prime.md` and `/start.md` for this codebase; verify in-loop.
  3. Write `adws/adw_prompt.py`: takes a prompt string, calls `claude -p` with stream-json output, logs raw + parsed output to `agents/<id>/`. Run it with a read-only question about your repo.
  4. Port your `/chore` + `/implement` templates from TAC-3 with THIS codebase's plan format and validation commands.
  5. Write `adws/adw_chore_implement.py` chaining the two prompts (plan path parsed from agent 1's output, passed to agent 2).
  6. Run one real chore from your backlog through it. Then answer, in writing, today's guiding question: what % of your day was agentic layer vs application layer?
  7. Schedule the layer's growth: pick the next problem class (bugs), and the trigger you'll add (cron file-watcher, GitHub webhook, or a task board).
- **Done-when:** A real chore in your real repo ships via the chained ADW with logs under `agents/`, and your agentic layer directories contain zero application code.
- **Level-up:** Build one of the alternative shapes: a `tasks.md` + cron trigger multi-agent worktree system, or a Notion/issue-board prototyper — whichever matches how work actually arrives in your life.

**Quote of the lesson:** "When the agents arrived, something changed. We weren't just AI coding anymore. We started orchestrating intelligence."

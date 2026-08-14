# Agentic Horizon (AH) — Complete Learning Distillate

IndyDevDan's six-lesson "Agentic Horizon" extended-lesson series (lessons #9–#14 of the Tactical Agentic Coding ecosystem). Source of truth: full lesson transcripts. Companion repos: `elite-context-engineering`, `agentic-prompt-engineering`, `building-specialized-agents`, `multi-agent-orchestration`, `agent-experts`, `orchestrator-agent-with-adws`.

---

## AH-1: R&D Framework — Context Window Mastery (Elite Context Engineering)

**Thesis:** The context window is your agent's most precious, ephemeral, limited temporal resource, and there are only two ways to manage it — Reduce and Delegate. A focused agent is a performant agent; obsessively measuring and managing context is what separates agentic engineering from vibe coding.

**Named frameworks & mnemonics:**
- **The R&D Framework** — "There are only two ways to manage your context window, R and D: **reduce and delegate**. Every technique fits into one or both of these buckets."
- **Four levels of context engineering** — "There are three levels of context engineering and a fourth hidden level if you're on the bleeding edge": Beginner → Intermediate → Advanced → **Agentic**.
- **The Core Four** — context, model, prompt, tools. "When aligned with the right model, prompt, tools and the right range of context, we can hit the core four bullseye over and over."
- **Context sweet spot** — "a range of context where your agent performs to its maximum possible capability for the task at hand." Hitting it consistently matters more as you scale to hundreds/thousands of executions.
- **Context rot / context bloat** — what accumulates when context isn't laser-focused; "search and destroy is the real skill in context engineering."
- **The 12 context engineering techniques** (as demoed, beginner → agentic):
  1. **Measure your context** — `/context` + an IDE token counter ("your most important tool for measuring and therefore managing your context window").
  2. **Be purposeful with MCP servers** — delete the default `.mcp.json`; load servers by hand with `claude --mcp-config <file>` (+ `--strict-mcp-config` to override globals).
  3. **Context priming over memory files** — "Context priming is when you use a dedicated reusable prompt, AKA a custom slash command, to set up your agent's initial context window specifically for the task type at hand." Prime, don't default.
  4. **Control output tokens with output styles** — output tokens cost 3–5x input; a "concise done" output style cut a 150-token response to 2 tokens (~99% reduction). Output styles hot-swap the output-style block of the system prompt.
  5. **Sub-agent delegation** — sub-agents are *system prompts* creating a "partially forked context window"; work happens in *their* windows, not your primary's. Sub-agents respond to your primary agent, not to you.
  6. **Planner/builder split** — "One agent plans, the other agent executes the plan. You have a planner and a builder, an architect and an editor." Classic prompt chaining across two context windows.
  7. **Reset and prime instead of /compact** — "After compact runs, do you know exactly what's in your context window every single time? No." Run `/clear`, then `/prime`. "Stop guessing and start knowing."
  8. **Context bundles** — hook-generated append-only logs of prompts/reads per session (`agents/context-bundles/`); `/load_bundle <path>` remounts a fresh agent to ~70% of the previous agent's state without the writes.
  9. **One agent for one purpose** — "There's no better way to control and manage your context window than to ship one thing at a time."
  10. **System prompt control** — `claude --append-system-prompt "<rules>" -p "<prompt>"` (print/programmatic mode only); SDK `custom_system_prompt` blows the whole system prompt away — "use this with caution."
  11. **Primary multi-agent delegation** — a `/background` slash command that boots a *full* background Claude Code instance with its own prompt, model, and report file. "Compute orchestrating compute, agents orchestrating agents."
  12. **Agent experts** (preview of AH-5) — "fire off specialized agents that are experts at specific parts of your codebase. And here's the kicker: you have them auto update their own knowledge." Three-prompt flow: plan → build → improve.
- **Future trends to bet on:** larger context windows, better *effective* context windows, hot-swapped context (system prompt, tools, messages), multi-agent architectures for delegation, specialized agents everywhere.

**Nuggets:**
- "A focused agent is a performant agent." (the lesson's mantra)
- "Context engineering is the name of the game for high value engineering in the age of agents."
- "Your agent's context window is a precious, renewable, but limited temporal resource."
- "What gets measured gets managed. So measure your context window."
- "If you aren't actively paying attention to the state of your agent's context, you're just vibe coding — and you'll only be able to tackle the lowest hanging fruit."
- "Adding the right context is usually the easy part. The real trick is finding the context agentically and then removing and delegating it."
- Default MCP config ate 24.1K tokens = ~12% of a 200K window; a bloated CLAUDE.md ate another 23K (~10%). "Boot up five agents over an hour, that's 25% of a context window completely wasted."
- "The claude.md file is incredible for one reason: it's a reusable memory file that's always loaded. Simultaneously it's terrible for the exact same reason."
- "The problem with always-on context is that it's not dynamic or controllable... the claude.md file only grows." Worst case: contradictory information in the window.
- Shrink your memory file "to contain only the absolute universal essentials that you're 100% sure you want loaded 100% of the time."
- "There are many places to be wasteful as an engineer... The context window of your agents is not one of them."
- "One write costs you up to five times more" — output tokens burn compute and wallet fastest.
- "The flow of information in these multi-agent systems is critical" — if you lose track of a single agent's core four, you're not ready for sub-agents.
- "By the end of your planning phase you should be deleting information that isn't relevant... go overboard, then delete."
- "The context window of your agents should not be handed off to any tool or team." /compact "is a bandaid fix for the true problem."
- "No single agent should overflow their 200K tokens and trigger a compact. If it does, you should chop up the task."
- "You want your agentic layer operating your codebase and you operate the agentic layer."
- "The focus should always be: better agents or more agents?"
- "It's not necessarily about saving tokens. It's about spending them properly."
- "What's better than a prompt? A prompt chain. What's better than a prompt chain? An agent. What's better than an agent? Many focused, specialized agents."
- "If it's easy, a vibe coder is probably doing it — and that isn't irreplaceable."

**What Dan actually did/built** (in `disler/elite-context-engineering`):
1. Ran `/context` on boot: 63K tokens (31%) already gone — diagnosed MCP tools (24.1K) and CLAUDE.md (23K).
2. Deleted the default `.mcp.json`; relaunched with `claude --mcp-config .mcp.firecrawl.json --strict-mcp-config` to load only Firecrawl (~4–6K tokens, suffix-labeled in the filename).
3. Swapped the bloated `claude.large.md` for a 43-line `claude.concise.md` (350 tokens, 0.2%) → 92% free window on boot.
4. Ran `/prime` and `/prime_cc` — stacked prime commands (prime_cc runs base prime + reads Claude-Code-layer files) with purpose/run/read/report structure.
5. Side-by-side Sonnet instances: one with `--settings settings.local.concise.json` (output style: "done"), one default; same "what does this codebase do" + AI-docs task; 150 output tokens vs 2.
6. Ran `/load_ai_docs` — primary agent fired ~10 `doc-scraper` sub-agents (system-prompt agents) to refresh `ai_docs/` after a 24-hour staleness check; primary window stayed at ~9K.
7. Planner/builder: `/quick_plan` (Opus) wrote a spec for a 3-file Claude Code TypeScript SDK wrapper in `app/`; fresh instance ran `/build <spec path>` with zero priming; ran the built app with bun.
8. Demoed `/clear` + re-prime instead of `/compact` (Ctrl+R to inspect the compact summary first).
9. Inspected `agents/context-bundles/` (per day/hour/session-id JSONL from hooks) and ran `/load_bundle <path>` in a fresh agent to replay prior state.
10. Ran `claude -p` with `--append-system-prompt` forcing "read in increments of 100 lines" + prefix final message with check/X — verified obedience in the context bundle (read 100, read 100...).
11. Ran `/background` — background Claude instance wrote a Python (uv/Pydantic) SDK-wrapper plan to a report file, renamed on completion; monitored via its context bundle.
12. Agent experts: `.claude/commands/experts/` Claude Code hooks expert — ran expert **plan** (with dedicated `Expertise` section) to spec a universal hook logger (`agents/hook_logs/<session_id>/<hook_name>.jsonl`), **build** in a fresh instance (one-shot), then **improve** (no params — reads git diff, updates the expertise sections of the plan and build prompts).

**Workout module:**
- **Goal:** Cut your Claude Code boot context by >50% and replace always-on memory with priming, then delegate one job to a background context window.
- **Prerequisites:** Claude Code installed; any repo with a `.mcp.json` and/or CLAUDE.md; an IDE token counter extension.
- **Steps:**
  1. Run `claude` then `/context`. Record: total %, MCP tokens, memory-file tokens. This is your baseline.
  2. Move `.mcp.json` to `.mcp.firecrawl.json` (or per-server files). Relaunch with `claude --mcp-config .mcp.firecrawl.json --strict-mcp-config`; re-run `/context` and confirm the drop.
  3. Trim CLAUDE.md to <50 lines of universal essentials. Move everything else into `.claude/commands/prime.md` (sections: Purpose / Run / Read / Report) and a second scoped `prime_<area>.md` that references files for one area of the codebase.
  4. Create `.claude/output-styles/concise-done.md` that instructs "respond only with 'done' on success; explain only on failure or questions." Set it in a `settings` file and compare output tokens on the same prompt vs default.
  5. Planner/builder: write `.claude/commands/quick_plan.md` (writes specs to `specs/`) and `.claude/commands/build.md` (takes `$1` = path to plan, early-returns if missing). Run plan in one terminal, `/clear`, build in a second.
  6. Write `.claude/commands/background.md` that shells out `claude -p "<prompt>" --append-system-prompt "report progress to <report file>; rename file with -complete suffix when done" &`. Fire one plan job through it.
  7. Instead of `/compact` on your next long session: `/clear` then `/prime`. Note the difference in confidence about window contents.
- **Done-when:** `/context` on boot shows ≥50% reduction vs baseline; the planner/builder pair one-shots a small feature with the builder receiving *only* the spec path; the background agent writes and renames its report file with zero babysitting.
- **Level-up:** Add a PostToolUse hook that appends prompt/read events to `agents/context-bundles/<session>.jsonl`, plus a `/load_bundle` command that deduplicates reads and re-mounts a fresh agent from the trail.

**Quote of the lesson:** "There are only two ways to manage your context window, R and D: reduce and delegate."

---

## AH-2: Seven Levels of Agentic Prompt Formats

**Thesis:** The prompt is now the fundamental unit of engineering, and every prompt is a force multiplier for three audiences at once — you, your team, and your agents. Master seven escalating prompt formats built from consistent, swappable Lego-block sections, with the workflow section as the S-tier pillar.

**Named frameworks & mnemonics:**
- **The Stakeholder Trifecta** — "We're now engineering for three audiences: you, your team, your agents. This is the stakeholder trifecta for the age of agents."
- **The Seven Levels of Agentic Prompt Formats:**
  1. **High Level Prompt** — "the reusable ad hoc static prompt"; the one-off you throw into a file when you start repeating work. 1–3 sections: Title, High Level Prompt, Purpose.
  2. **Workflow Prompt** — "easily the most important one"; a sequential list of tasks the agent executes. Adds Metadata, Variables, Workflow, Report. Workflow section = S-tier usefulness.
  3. **Control Flow Prompt** — the workflow gains "conditions, loops, and early returns" (e.g., "if no path to plan is provided, immediately stop and ask").
  4. **Delegation Prompt** — "a prompt that kicks off other agents to do work"; "our primary agent is the prompt engineer for our sub agents." S-tier useful, A-tier skill.
  5. **Higher Order Prompt** — "we are passing prompts into prompts"; stable top-level scaffold, swappable payload (e.g., `/build <path_to_plan>`).
  6. **Template Meta Prompt** — "a prompt used to create another prompt in a specific format... the most powerful prompt you can write. It's the prompt that creates your other prompts." Adds a template/Specified Format section the agent fills in.
  7. **Self-Improving Prompt** — "we're having our agents update our agents... by having our prompts update our prompts," via a dynamic **Expertise** section. "Expert level" — A usefulness, S skill.
- **The composable sections (swappable Lego blocks)** with Dan's tier grades: Title (C use/D skill), Purpose (B/D), Metadata (C/C), Workflow (**S**/C), Report (the output/format section), Instructions ("auxiliary information on the individual steps in the workflow"), Variables (A/B — dynamic `$1`/`$ARGUMENTS` vs static in-prompt constants), Codebase Structure aka **context map** (C/C), Examples (A — "can drastically increase your agent's performance"), Relevant Files (C/C), Expertise (level 7).
- **Input → Workflow → Output** — "a very consistent three-step pattern you can use to think about how to design and build your prompts."
- **System prompts vs user prompts** — "the big idea is scope and level of persistence. System prompts are rules for all conversations... mistakes scale to every user prompt you run." Key system-prompt sections: Purpose, Instructions, Examples (Workflow only when you're sure — "workflows reduce agency to increase determinism").
- **Information dense keywords (IDKs)** — words like IMPORTANT that carry extra weight for models.

**Nuggets:**
- "The prompt is now the fundamental unit of engineering."
- "One well-crafted prompt can generate tens and hundreds of hours of productive work. One bad prompt compounds failure at the same rate."
- "The winners here are building libraries of reusable battle-tested agentic prompts with composable sections that work like Lego blocks."
- "Three times marks a pattern — copy whatever you're doing and just write it as a high level prompt, then move up the levels."
- "The high level prompt is a great place to start. It's a terrible place to end."
- "The workflow is the step-by-step play of exactly what you want your agent to do."
- "You can call these sections whatever you want. I'm using the most consistent, most information dense keywords to represent every section."
- "Great prompting is great communicating."
- "This is a dynamic variable in contrast to a static variable" — static variables save you from re-referencing paths everywhere.
- "Consistency is the greatest weapon against confusion for both you and your agent."
- "If I handed this to a coworker, could they complete this work top to bottom? If that's true, you've probably written a high quality prompt."
- "Consistency beats complexity. Consistency makes you faster."
- "Only add what you need — these are composable pieces of your agentic prompts."
- "Every prompt format is about the capability that it offers you and your agent."
- "We're writing prompts that write prompts" (delegation) — "design agent prompts: create detailed self-contained prompts for each agent."
- "Levels one through four will be 80 or 90% of all of your prompts... usually level three, level four is all you need."
- "Engineers creating more and better prompts at scale are the winners here."
- "Workflows reduce agency to increase determinism."
- "A bad system prompt is bad instructions for the whole job." The system prompt is "one order of magnitude — really more like two or three" — more important than a user prompt.
- "You're gonna be creating, reading, updating and deleting your prompts at light speed."
- "The prompt is the fundamental unit of engineering. Invest in your prompts for the trifecta to achieve asymmetric engineering in the age of agents."

**What Dan actually did/built** (in the `agentic-prompt-engineering` codebase, graded live on a tier-list app):
1. Level 1: `all_tools.md` (title + high level prompt: list your tools from the system prompt) and `start.md` (adds Purpose; cd/bun install/bun dev).
2. Level 2: `prime.md` (metadata description, purpose, workflow, report); `build.md` (allowed-tools Read/Write/Bash, argument-hint, `PATH_TO_PLAN` variable referenced throughout); `quick-plan.md` (dynamic `USER_PROMPT` + static `PLAN_OUTPUT_DIRECTORY = specs/`, Instructions section); `prime_tier_list.md` (Codebase Structure/context map + "read these files exclusively" with IMPORTANT keyword).
3. Level 3: `build.md`'s early return (no plan path → stop and ask, demoed live); `create_image.md` (positional `$1`/`$2` args, static vars for output dir/model/aspect ratio, an XML-wrapped `image_loop`, Replicate MCP) and `edit_image.md` (loop + exit-immediately conditionals, no Report section on purpose).
4. Level 4: `parallel_subagents.md` (prompt_request + count; fired 5 agents to extract CLAUDE.md-worthy essentials); `load_ai_docs.md` (24-hour delete rule, loop calling the doc-scraper sub-agent directly, strict report format); `background.md` (delegation + control flow + appended system prompt, spinning a background Claude instance reporting to a file).
5. Level 5: `build.md` reframed as higher-order prompt — plans from `/quick_plan` (or chore/feature builders) passed in as the lower-order prompt.
6. Level 6: `meta_prompt.md` — the prompt that builds prompts (variables: user's prompt request; workflow reads slash-command docs first; Specified Format template the agent fills in) and `plan_vue_view` rapid-prototype planner with a Plan Format template section.
7. Level 7: `experts/` hook expert with its dedicated `Expertise` section — "we're basically updating the context inside of our prompts in a live way."
8. Distinguished system vs user prompts using `doc-scraper` sub-agent (system prompt with purpose, static output dir, workflow) and the background prompt's `--append-system-prompt`.

**Workout module:**
- **Goal:** Build a seven-level prompt ladder in one repo, one prompt per level, all sharing the same section format.
- **Prerequisites:** Claude Code; a small app repo; AH-1 workout done (you have `prime.md`).
- **Steps:**
  1. Level 1 — `.claude/commands/all_tools.md`: Title + one high-level line ("List all tools available to you from your system prompt in a bullet list").
  2. Level 2 — `.claude/commands/prime.md` with exactly: metadata (description, allowed-tools), `# Title`, `## Purpose`, `## Workflow` (numbered reads), `## Report`. Run it; confirm the agent's todo list mirrors your workflow steps.
  3. Level 2.5 — `.claude/commands/plan.md`: dynamic `USER_PROMPT: $1`, static `PLAN_OUTPUT_DIRECTORY: specs/`; reference both variables at least twice in the workflow.
  4. Level 3 — `.claude/commands/build.md`: `PATH_TO_PLAN: $1`; first workflow line: "IMPORTANT: If no PATH_TO_PLAN is provided, immediately stop and ask the user for it." Test by running `/build` with no args.
  5. Level 4 — `.claude/commands/parallel_subagents.md`: `PROMPT_REQUEST: $1`, `COUNT: $2`; workflow step "design agent prompts — create detailed self-contained prompts for each agent, define clear output expectations." Run with count 3 on a research question.
  6. Level 5 — chain them: `/plan "add X"` → copy spec path → `/build specs/<file>.md`.
  7. Level 6 — `.claude/commands/meta_prompt.md`: takes a request, reads the slash-command docs, emits a new command file matching your exact level-2 Specified Format. Use it to generate a `/test.md` prompt.
  8. Level 7 — add an `## Expertise` section to one prompt plus a `self_improve.md` that reads git diff and updates only that section.
- **Done-when:** All seven commands exist, collapse to the same header skeleton, and: `/build` early-returns without args; the meta prompt generates a working new command in your format; the self-improve run edits only the Expertise section.
- **Level-up:** Grade each of your sections on Dan's usefulness/skill tier list, then delete every section that isn't earning its tokens ("only add what you need").

**Quote of the lesson:** "The prompt is the fundamental unit of engineering."

---

## AH-3: Building Domain-Specific Agents

**Thesis:** Every engineer's path is better agents → more agents → custom agents, because out-of-the-box agents "are built for everyone's codebase, not yours." The Claude Code (Agent) SDK lets you control the Core Four at bare metal — and the system prompt is the most important element of a custom agent, with zero exceptions.

**Named frameworks & mnemonics:**
- **The agent evolution path:** "Better agents, more agents, and then custom agents."
- **The Core Four** — context, model, prompt, tools. "Whenever you see ClaudeCodeOptions, isolate the core four."
- **The SDK loop:** "You set up your options, you set up your agent, you run your prompt, you then manage the responses." (options → agent → query → handle messages: assistant/system/result; text/tool-use/tool-result/thinking blocks.)
- **`query()` vs `ClaudeSDKClient`** — "query is for one-off prompts and the Claude SDK client is for continuous conversations" (with `resume`/session-id for continuation).
- **Extension agents vs complete custom agents** — append the system prompt to *extend* Claude Code; overwrite the system prompt (and add custom tools) and "this is not Claude Code anymore... you change the product."
- **The system prompt is the law** — "Your system prompt is the law for your agent"; embed a workflow in it only when you want that exact flow every single time.
- **When to build custom agents:** programmatic agents; repeat workflows; domain-specific problems; costs down/performance up; permission checks & safety (hooks); "most importantly... you build custom agents when you want to stay out of the loop."
- **When to use out-of-the-box agents:** operating in-loop; generic workflows the SDK covers; exploring/prototyping; a balanced generalist that works in 80% of situations; short-lived, lightweight, non-repeat, non-domain tasks.
- **One agent, one prompt, one purpose** — pushed to its limit by custom agents.

**Nuggets:**
- "They're built for everyone's codebase, not yours. This mismatch can cost you hundreds of hours and millions of tokens."
- "This is where all the alpha is in engineering. It's in the hard specific problems that most engineers and most agents can't solve out of the box."
- "The system prompt is the most important element of your custom agents. With zero exceptions."
- "The system prompt affects every single user prompt the agent runs. All of your work is multiplied by your system prompt."
- "The system prompt is truly what builds the agent."
- "Everything that's going into your agent winds up in the context window at some point" — 15 default tools "consume space in your agent's mind."
- "Always look for the system prompt and then look for the custom tools."
- "The description of your tool tells your agent how to use it."
- "In your tools, you're back in traditional deterministic code... do whatever you want, but respond in the proper format."
- "If an error occurs, can our agent pivot?" — give agents information so they can reflect and correct.
- "Don't start with big things, start with small things. Everything large is a few small things that you understand fundamentally first."
- "It's not the models that are the limitation anymore. It's you and I — our ability to wield better agents, more agents, and now custom agents."
- "You can embed workflows in your system prompt if you're sure that is what you want to happen every single time your agent executes."
- "This agent cannot write. It's a QA agent. Why would it need to write anything?"
- Hooks = "essential for governance, for control, for permissions in all of your agents."
- "Whatever response format you return from your agents... create a concrete object" (Pydantic / Zod).
- "Don't try to reproduce your own engineering agent. Claude Code is that." / "In no way do I think you should try to compete with Claude Code."
- "You can solve your problems better than any agent can. Out of the box is a great place to start — don't end there."
- The SDK "has built-in prompt caching. You will be saving money by using this out of the box."
- "Agentic coding is not so much about what we can do anymore. It's about what we can teach our agents to do."

**What Dan actually did/built** (eight agents in `building-specialized-agents/apps/`, all Python + `uv run`):
1. **Pong agent** — overwrote the system prompt ("You are a Pong agent, always respond exactly with Pong"); every prompt → "Pong". ~150 lines, mostly logging. Lesson: total system prompt control.
2. **Echo agent** — custom `@tool` (reverse/uppercase/repeat) in an in-memory MCP server via `create_sdk_mcp_server`; downgraded to Haiku; `ClaudeSDKClient` for a follow-up query; discovered 15 leftover Claude Code tools still in context.
3. **Calc agent** — terminal-UI form factor; only two tools (calculate expression via eval, unit converter); big `disallowed_tools` block ("these tools do not end up in its context window"); `resume` session id for continuous chat.
4. **Social hype agent** — Bluesky firehose WebSocket stream handler; deterministic keyword match → queue → agent sentiment analysis (`submit_analysis` tool) → conditional `notify` tool (AppleScript notification + TTS); workflow embedded in the system prompt; a runtime-locked "static variable dynamically set" notification prompt; max 3 turns.
5. **QA agent** — codebase question-answering expert; external Firecrawl MCP via `mcp_config` path; read-only allowed tools (Task, Bash, Glob, Grep, Read, web/Firecrawl search); PreToolUse/PostToolUse hooks — blocked reads of `.env` files live; thinking blocks parsed; system prompt with Instructions + working directory + agent examples.
6. **Tri copywriter** — agent in a web UI; ALL tools disallowed ("tool calling is useless for this use case"); `NUMBER_OF_VERSIONS` templated into the system prompt; JSON responses validated by a Pydantic `MultiVersionCopyResponse`; drag-and-drop file context; 6 variations per prompt.
7. **Custom seven micro SDLC** — multi-agent kanban (plan → build → review → ship) over WebSockets; planner has a write-hook restricting writes to the plans directory; builder uses the stock Claude Code system prompt untouched; reviewer *appends* to the system prompt; shipped a title change end-to-end from a dragged ticket ("a perfect example of an out-loop review system using the PITER framework").
8. **UltraStream agent** — two agents on a 42K-token log stream: a stream agent with fine-grained tools (read stream file in 5-line chunks, produce summarized log, create alert) that manages its own context window, and an inspector agent consuming the stream agent's produced logs (list issues, find logs per user, notify support). "You cannot do this without serious prompt engineering with an out-of-the-box agent."

**Workout module:**
- **Goal:** Build three custom agents of increasing capability on the Claude Agent SDK: a Pong agent, a tool-wielding Echo agent, and a read-only codebase QA agent with a security hook.
- **Prerequisites:** Python + `uv` (or TS + bun), `claude-agent-sdk` installed, ANTHROPIC_API_KEY.
- **Steps:**
  1. Scaffold `apps/pong_agent/` with `pong_agent.py` + `prompts/pong_system_prompt.md` ("You are a Pong agent. Always respond exactly with 'Pong'."). Use `query()` with options `{model: haiku, system_prompt: <loaded file>}`. Prove that "summarize this codebase" returns "Pong".
  2. Scaffold `apps/echo_agent/`: define an `@tool` echo(text, reverse, uppercase, repeat); wrap it with `create_sdk_mcp_server`; use `ClaudeSDKClient` and send a follow-up "summarize our conversation" query. Then ask "list your available tools" and count the stock tools leaking in.
  3. Add `disallowed_tools` for every stock tool your echo agent doesn't need; re-ask for tools and confirm only yours remain.
  4. Scaffold `apps/qa_agent/`: overwrite system prompt (Purpose/Instructions/Examples), allow only Task/Bash/Glob/Grep/Read, add a PreToolUse hook that blocks any Read whose path matches `.env` and returns a concise "blocked: environment file" reason.
  5. Test the hook: prompt "read the .env file" → expect a block; prompt "summarize the key modules, think hard" → expect thinking blocks + a real answer.
  6. Log every message type (system/assistant/result; text/tool_use/tool_result/thinking) with clean panels — "if you don't know what your agent is doing... it will be hard to improve them."
- **Done-when:** Pong always pongs; the echo agent's tool list contains only your tool; the QA agent answers a codebase question with citations, refuses `.env`, and reports session cost from the result message.
- **Level-up:** Bolt the QA agent onto a stream: pipe a growing log file through a stream agent with a read-in-chunks tool, and have a second agent answer questions against its produced summaries (the UltraStream pattern).

**Quote of the lesson:** "Agentic coding is not so much about what we can do anymore. It's about what we can teach our agents to do."

---

## AH-4: Multi-Agent Orchestration — The O-Agent

**Thesis:** Once you have better, more, and custom agents you hit the wall of the interface — you can't scale one terminal and one prompt at a time. The Orchestrator Agent (O-Agent) applies the single interface pattern to your fleet: one custom agent that CRUDs, commands, and observes all your other agents.

**Named frameworks & mnemonics:**
- **The Orchestrator Agent (O-Agent)** — "the one agent to rule them all... the single interface pattern applied to your fleet of agents." "The orchestrator agent is a custom agent — its system prompt is completely overwritten, its tools are specialized, it's designed to manage other agents."
- **The Three Pillars of multi-agent orchestration:** (1) the Orchestrator Agent — your unified interface; (2) **CRUD for your agents** — agents at scale; (3) **Observability** — real-time monitoring of performance, costs, and results.
- **The agent scale framework:** "Base agents, better agents, more agents, custom agents" → orchestrated agents. "At each step, you scale your compute to scale your impact."
- **PITER out-loop system** — the orchestrator UI is "an out-loop PITER system": Prompt input, Trigger (HTTP), Environment, Review (observability) — "remember tactic four, stay out the loop."
- **Consumed vs produced assets** — "Every agent should produce some concrete result. Otherwise, what was the point in the first place?"
- **Agents as deletable resources:** "You must treat your agents as deleteable temporary resources that serve a single purpose." Read → create → update → delete: "the best code is no code at all. You learn to delete."
- **One agent, one prompt, one purpose** (tactic six) applied to fleets; **R&D framework** at scale — orchestrator context reduced, work delegated to primary agents.
- **Agent templates** — sub-agent definitions in `.claude/agents/` promoted into full primary agents ("we've just pulled it up a level... you can't do all this with a sub-agent. You're locked in, it's too narrow.").

**Nuggets:**
- "At scale, if you lose track of your agents, you lose control of your results."
- "The rate at which you can create and command your agents becomes the constraint of your engineering output. When your agents are slow, you're slow."
- "If you can't measure it, you can't improve it. And if you can't measure it, you can't scale it."
- "If you have 10 agents doing the wrong thing, does it matter that you have 10?"
- "With a single prompt, I've deployed three times the compute an engineer working in the terminal has."
- "Our orchestrator agent takes our high-level prompt and then writes out in much more detail the actual concrete work" — "it is doing some serious prompt engineering."
- "We don't want our orchestrator agent getting involved in the actual work. It is just here to orchestrate."
- "If you do not adopt your agent's perspective, if you do not know what they can do, you do not know what you can do."
- "On top of every feature any lab builds, any UI you see — it's all just the core four. Don't let anyone confuse you."
- "These aren't just one-off sub-agents where the context is blown away... These are primary agents that we can tap into over and over until that specific job is done."
- "200K context window is plenty. You're just stuffing a single agent with too much work, just like your boss did to you at your last job."
- "Force it to focus and then let it go home back to the data center. Delete it."
- "Once you build a custom agent, you can then write prompts specialized for that custom agent." (the orchestration prompt: plan-with-scouts → build → review)
- "The orchestrator is now glue for the workflow. I think this is vastly superior to agent handoffs... superior to blind sub-agents."
- "If you can do your job with an out-of-the-box agentic coding tool, how defensible is your product really?"
- "If you can deploy a little bit more compute to have more confidence and more trust in your agents, why wouldn't you?"
- "Specialized tools like this are more powerful than some out-of-the-box cloud tool... designed for everyone's codebase, not yours."
- "One time I had 16 agents operating, completing work at absurd scales."
- "More than 50% of your time as a rough guideline should be spent investing into your agentic layer" (tactic eight).
- Missing pieces he names: human-in-the-loop decision points, better orchestrator management (multi-codebase), context-window/agent forking ("one tool away"), prompt autocomplete, and ADW integration ("the big missing piece... deterministic code").

**What Dan actually did/built** (the `multi-agent-orchestration` codebase — Vue/Pinia front end, HTTP + WebSocket services, Claude Agent SDK orchestrator service, Postgres/Neon data layer; the system pointed at itself):
1. Command-K prompt bar → `ping` → orchestrator replies; then one prompt spun up 3 agents (front-end, back-end, QA) to write an app-structure summary with mermaid diagrams — 6 tool calls: 3× create_agent, 3× command_agent.
2. Walked the observability UI: per-agent name/status/context window/model/cost; responses, tool calls, hooks, thinking filters; consumed vs produced assets with one-click diffs into the editor.
3. `list agents and check status` — orchestrator used check-status tools (agent name + tail of response logs) rather than reading raw logs, protecting its own window.
4. `command all agents...` with thinking enabled — reprompted existing primary agents (not ephemeral sub-agents).
5. `delete all agents` — three delete tool calls; the CRUD loop complete.
6. Ecosystem interop: created an agent to run the `/question` slash command ("can our orchestrator and agents use skills?" → yes); ran `/prime` for the orchestrator (with the caveat: it loads the orchestrator's context).
7. Created a primary agent from the `scout-report-suggest-fast` sub-agent template in `.claude/agents/`, commanded a regex-field summary; produced a report doc.
8. "Scout and build" prompt — orchestrator thought, created a scout + builder, slept in a 15-second check-status loop, then wrote a detailed builder prompt from the scout's report; shipped gray stat pills to the app header.
9. Final demo: an orchestration prompt (`plan_w_scouters` → build → review, three phases + final report) shipping a responsive-UI feature (collapse agent list under 650px) — planner 21K tokens, builder, reviewer, all observable end-to-end.

**Workout module:**
- **Goal:** Build a minimum viable O-Agent: a custom agent whose only tools are create/command/status/delete over background Claude instances, with a file-based observability trail.
- **Prerequisites:** AH-3 workout done (you can build a custom agent with custom tools); Claude Agent SDK; a target repo.
- **Steps:**
  1. Create `apps/orchestrator/` with an overwritten system prompt: "You are an orchestrator. You never do engineering work yourself. You create, command, monitor, and delete agents. Every agent must produce a concrete file result."
  2. Implement four tools: `create_agent(name, model, system_prompt)` (registers a row in `agents/registry.json`), `command_agent(name, prompt)` (spawns `claude -p` with that agent's config, streaming output to `agents/logs/<name>.jsonl` and a produced-files list), `check_agent_status(name)` (returns status + log tail — tail, not full log), `delete_agent(name)`.
  3. Disallow all stock tools on the orchestrator except your four (plus TodoWrite).
  4. Run the ping test, then: "Create two agents, one to summarize the backend and one for the frontend, into docs/*.md; check on them until done; report consumed vs produced files."
  5. Add an agent-template option: `create_agent` can read a `.claude/agents/<template>.md` file as the new agent's system prompt.
  6. Write one orchestration prompt for your O-agent (scout → build → review, phases + final report format) and run a small real feature through it.
  7. Finish every session with "delete all agents" and verify the registry is empty.
- **Done-when:** One high-level prompt yields ≥2 concurrently-working agents, each producing a concrete file; the orchestrator's own context stays small (verify it never reads full logs); agents are deleted after the job.
- **Level-up:** Swap the JSON registry for Postgres + a WebSocket UI showing per-agent status, cost, and produced assets — the three pillars in full (orchestrator, CRUD, observability).

**Quote of the lesson:** "You must treat your agents as deleteable temporary resources that serve a single purpose."

---

## AH-5: Agent Experts

**Thesis:** The massive problem with agents is that they forget — and that means they don't learn. An agent expert is "a concrete form of a self-improving template meta prompt": an agent that acts, learns, and reuses its own expertise at runtime by maintaining a mental-model data structure (an expertise file) with no human in the loop.

**Named frameworks & mnemonics:**
- **Agent Expert** — "The difference between a generic agent and an agent expert is simple. One executes and forgets, the other executes and learns." Formally: "The agent expert is a concrete form of a self-improving template meta prompt."
- **Act, Learn, Reuse** — the three concrete steps of an agent expert. **Act**: take a *useful* action (e.g., the build step). **Learn**: store new information (the self-improve prompt updating expertise). **Reuse**: apply that expertise on the next execution (plan/question prompts read the expertise file first).
- **The expertise file = mental model, NOT a source of truth** — "This is not a source of truth... You have a working memory file. You have a mental model, a data structure that you constantly update." "The true source of truth is always the code." Dan uses YAML with a MAX_LINES cap (1000) enforced by the agent on itself.
- **Meta-agentics** — "meta prompts, meta agents and meta skills... they help you build elements of the system that builds the system." "Every codebase must have meta agentics." Meta-agentics act but don't learn, so they are *not* agent experts.
- **Self-improve prompt anatomy** (the learn step): check git diff (conditional) → read current expertise → validate against codebase → identify discrepancies → update expertise → enforce line limit + validate YAML (closed loops). Key line in the prompt: "Prioritize actionable, high value expertise over verbose documentation" and "after your thorough search, there may be nothing to do — this is perfectly acceptable."
- **Seeding** — creating the first version of the expertise: "Ideally you run your self-improve prompt and it creates the expertise from blank... rerun it until your agent stops finding new things."
- **Expert file structure** — `.claude/commands/experts/<domain>/` containing `expertise.yaml`, `question.md`, `plan.md`, `self-improve.md`, and a `plan_build_improve.md` chain.
- **Where to deploy codebase experts:** billing (his #1 — "literally saved me money"), database, DevOps, integrations (3–4 way), ML/data science, API (front/back sync), data types/models across microservices. Rule: "the higher the risk, the higher the intensity, experts are really great here."
- **Product agent experts** — per-user expertise files powering adaptive/generative UI ("personalization to the max").
- **When NOT to build one:** the problem doesn't evolve; simple/new codebases; and "if you yourself do not have a mental model in place... you will build an expert that can't solve the problem because you can't."
- **Challenges/trade-offs named:** seeding, "another source of truth" objection, finite context, false expertise, too-granular expertise, too many experts.

**Nuggets:**
- "Traditional software improves as it's used... Agents of today don't. Your agents forget. And that means your agents don't learn."
- "You don't need to tell an expert to learn. It's in their DNA."
- "Real experts don't relearn their craft every time they have a new task."
- "This mental model is simply put a data structure that evolves over time."
- "Memory files are global forced context that always loads... expertise requires breaking rules when the time is right."
- "There is no codebase I create that does not have meta agentics."
- "It first reads this expertise file... It didn't need to go search or find these files. It knew where they were. This is the differentiated factor of an agent expert."
- "You don't have a source of truth in your mind. You have a working memory file."
- "Give your agents a mental model by giving them an expertise file."
- "Three times marks a pattern" — hence the meta expert that generates expert prompt sets.
- "More compute equals more confidence" — three parallel experts on one question; "sometimes if you throw five agents at the problem... you compose that together, you get a better result."
- "I get super hyped when agents change just the right things... I wanna see surgical changes."
- "If there's something we don't like, we're not going to update the expertise file... you wanna update the self-improve step that operates your expertise." / "Don't directly update this expertise file. Teach your agents how to directly update it."
- "My agentic experts have caught revenue changing details in these systems."
- "If your product is successful, it will grow in complexity and speciality. As that happens, agent experts become more and more valuable."
- "It's their mental model, not yours" — steer toward autonomy over prescription.
- "Your mental model doesn't infinitely grow... once you get to a certain level, you just forget. That is okay."
- "Prompt first so that you can execute it by hand manually... then scale it into whatever abstraction you want" (skill, sub-agent, custom agent — "everything becomes the core four").
- "Build the system that builds the system. Do not work on the application layer. You're wasting your time."
- "Do you want a generalist working on your codebase that forgets every time they work? Or do you want an expert that remembers?"

**What Dan actually did/built** (the `agent-experts` codebase; local copy of the code lives at `/Users/kvnkishore/WebstormProjects/AgenticEngineer/agent-experts/.claude/` in git):
1. **Meta-agentics demo:** `/meta_prompt` generated `question-w-mermaid-diagrams.md`; the **meta-agent** (`.claude/agents/meta-agent.md`, an agent that writes new sub-agent files to `.claude/agents/<name>.md`) generated a `planner` agent that reads and executes the plan prompt; a **meta skill** generated a `start-orchestrator` skill (boots the AH-4 app's front end + back end, opens Chrome).
2. **Database expert** (`.claude/commands/experts/database/`): ran `/experts:database:question "how does information flow between our database tables"` — agent read `expertise.yaml` first, validated against code, wrote a report with an ER mermaid diagram. Walked `expertise.yaml` (overview: "lightweight pydantic models over raw SQL, no heavy ORM"; core implementation with file paths, line numbers, query patterns, migrations). Ran `/experts:database:self-improve` — validation confirmed the mental model in sync (line-count check + YAML compile as closed loops). Noted: this expert has Reuse + Learn but **no Act step — a partial expert**.
3. **WebSocket expert** (`.claude/commands/experts/websocket/`: `expertise.yaml`, `plan.md`, `question.md`, `self-improve.md`, `plan_build_improve.md`): ran `/experts:websocket:plan_build_improve "add a session-based counter to the app nav bar that displays total WebSocket events"` — three sub-agents chained via Task tool: plan (80K tokens, expertise-informed), build (61K tokens, 41 tool uses), self-improve with CHECK_GIT_DIFF=true (updated expertise with the new counter event, session state, line numbers). Feature one-shotted.
4. Scaled experts through the AH-4 orchestrator: "create three agents and run /experts:websocket:question 'what WebSocket events exist'" — three parallel experts, non-deterministic consumed-file sets, one failed, orchestrator synthesized the answer (21 event types); offered "create three more experts using the Opus model... to ultra validate."
5. **Product expert demo ("Niall" shopping app):** per-user `expertise` data structure (viewed products, cart adds, checkouts) updated on every action; agent regenerates personalized landing-page sections (generative UI) on return; expertise + dynamic variables embedded in the shopping agent's system prompt; Opus for generation quality, dropped to Haiku for speed.

**Workout module:**
- **Goal:** Stand up one complete agent expert (Act–Learn–Reuse) for a real domain in your codebase — e.g., your database layer.
- **Prerequisites:** AH-2 prompt formats internalized; a codebase with a non-trivial subsystem you understand well (you need your own mental model first).
- **Steps:**
  1. Create `.claude/commands/experts/database/` with four files: `expertise.yaml` (empty), `question.md`, `plan.md`, `self-improve.md`.
  2. Write `self-improve.md` (this is the heart): frontmatter allowed-tools `Read, Grep, Glob, Bash, Edit, Write, TodoWrite`; Variables `CHECK_GIT_DIFF: $1 (default false)`, `FOCUS_AREA: $2`, `EXPERTISE_FILE: .claude/commands/experts/database/expertise.yaml`, `MAX_LINES: 1000`; Instructions including "think of the expertise file as your mental model, not a source of truth", "prioritize actionable, high value expertise over verbose documentation", "there may be nothing to do — this is perfectly acceptable"; Workflow: git diff (conditional) → read expertise → validate against codebase → identify discrepancies → update → `wc -l` line-limit check + YAML validation.
  3. **Seed:** run `/experts:database:self-improve` on the empty file. Let the agent invent the structure. Rerun until it reports "nothing to be done."
  4. Write `question.md`: Variables `USER_QUESTION: $1`, `EXPERTISE_PATH`; Instructions "IMPORTANT: question-answering only — DO NOT write/edit files" and "validate the information from EXPERTISE_PATH against the codebase before answering"; Report: direct answer + file/line evidence + mermaid where useful. Ask it a hard question; confirm it reads expertise *first* and skips searching.
  5. Write `plan.md` that reads expertise before planning, and a `plan_build_improve.md` chain: Step 1 Task→`/experts:database:plan`, Step 2 Task→`/build <plan path>`, Step 3 Task→`/experts:database:self-improve true`. ("DO NOT STOP between steps.")
  6. Run one real change through the chain, then `git diff .claude/commands/experts/database/expertise.yaml` to inspect what the agent learned.
  7. If the expertise is wrong or too verbose, do NOT edit the YAML — edit `self-improve.md` and rerun.
- **Done-when:** The question prompt answers from the mental model with correct file/line citations; a plan→build→improve run ships a change AND the expertise diff shows only accurate, surgical updates; expertise stays under MAX_LINES with valid YAML.
- **Level-up:** Build a meta expert (a template meta prompt that scaffolds `question/plan/self-improve/expertise` for any new domain), then add a second expert for your highest-risk system (billing/security) and wire both into your O-agent as agent templates.

**Quote of the lesson:** "The difference between a generic agent and an agent expert is simple. One executes and forgets, the other executes and learns."

---

## AH-6: Building Agentic Layers (The Codebase Singularity)

**Thesis:** Everything in TAC and AH builds toward one moment — the codebase singularity: "My agents can now run my codebase better than I can. I trust them to ship more than I trust myself or my team." The path there is building your agentic layer through three classes and their grades, from a lone prime prompt to an orchestrator running AI developer workflows.

**Named frameworks & mnemonics:**
- **The Agentic Layer** — "the new ring around your codebase where you teach your agents to operate your application on your behalf as well and even better than you and your team ever could." The application layer bundles *everything* app-side (front end, back end, DB, scripts, DevOps, multiple repos as git submodules under `apps/`).
- **The Codebase Singularity** — the moment you realize "my agents can now run my codebase better than I can... Nothing ships to production without my teams of agents." "There is an agentic layer that could exist inside your codebase so powerful that your codebase runs itself."
- **The three classes and grades of the agentic layer:**
  - **Class 1 (in-loop agentics):**
    - **Grade 1** — prime prompt and/or memory files. "The thinnest possible agentic layer you can have."
    - **Grade 2** — plan prompts, sub-agents (fetch-docs, test-writer), `specs/` for plans, `ai_docs/` for pulled documentation.
    - **Grade 3** — custom tools: skills, MCP servers, prime commands with tool access. "All three give us the same thing: custom tools that enhance our agent's core four." (Many engineers get stuck here with terrible, token-heavy tools.)
    - **Grade 4** — closed-loop prompts / feedback loops: code review, reproduce bug, test backend/front end. "Request, validate, resolve." "You're effectively adding more compute to get more confidence in your agent's results."
    - **Grade 5** — **templates** (bug, feature, chore, new-API-endpoint): "structured plans with specific output formats for different types of work... where you truly template your engineering and teach your agents to build like you do."
    - **Grade 6** — prompt chains / agentic workflows: "one prompt now references many prompts and/or sub-agents" (plan_build, scout-then-plan). Context engineering "becomes a requirement" here.
    - **Grade 7** — **agent experts** with mental models. "This is where we start to see your agents solving problems end to end without you" — the doorstep of the singularity.
  - **Class 2 (out-loop):**
    - **Grade 1** — webhooks/triggers + a core agent SDK layer: "you can execute prompts against your codebase from an external service" (Slack, Jira, GitHub, Discord). The PITER framework realized.
    - **Grade 2** — **AI Developer Workflows (ADWs)**: "deterministic code plus non-deterministic agents. You get the best of both worlds" — logging, validation, retries between agent steps. "Once you find yourself deleting your prompt chains and replacing them with concrete AI developer workflows... you will be at class two, grade two."
  - **Class 3 (orchestrated):**
    - **Grade 1** — the **Orchestrator Agent**: "a custom agent that is a lead engineer that can CRUD, command and manage other agents."
    - **Grade 2** — **Orchestrator Developer Workflows**: the orchestrator conducts entire multi-team workflows with open streams of communication ("we can talk to any one of these agents from this workflow at any time").
    - **Grade 3** — the orchestrator runs **ADWs**: agentic autonomy on top, deterministic raw code underneath. The final grade.
- **The TAC tactics recap (as the closing framework):** stop coding (use agents); adopt your agent's perspective; template your engineering; stay out the loop; always add feedback loops (request/validate/resolve — "more compute should equal more trust, not less"); one agent, one prompt, one purpose; target zero-touch engineering (ZTE); and the meta tactic — **prioritize agentics**: "build the system that builds the system."

**Nuggets:**
- "Compute in its most useful form is in a prompt and a loop with tools — the agent. This transformed the big three into the core four."
- "If you have this [a prime prompt], you technically have an agentic layer."
- "Skills and MCP servers can both be replaced with just a simple prompt."
- "MCPs are very token heavy and we can just prompt engineer properly to get our agents the tools they need."
- "A lot of engineers do get stuck at grade three... their tools are terrible and they won't scale and they're chewing up tokens."
- "Designing tools is an entire game on its own."
- "Always add feedback loops... More compute should equal more trust, not less. If it's less, you're doing something wrong."
- "When you start building templates, your agent starts operating more like you would — the way you solve a bug is very different from the way you solve a chore."
- "You want all of the actual application layer code to run under `apps/`, and if they're coming from a different git repository, set up git submodules. This is the winning codebase structure."
- "Your agentic layer should be specialized to fit and wrap your codebase... Don't focus on reuse. Focus on making these prompts great for that one codebase."
- "I would absolutely never build a plan, build, review workflow that cannot be run individually" — composability + isolation for debugging and parallelization.
- "You can't write a five agent long prompt chain without knowing the context that every agent will have at every step."
- "Everything is just a context, model, prompt [and tools]. It doesn't matter what it's called... everything eventually becomes the core four."
- "The composite type doesn't matter" (expert as prompt set, skill, sub-agent, custom agent) — "do you have a specialized agent that can operate specific parts of your codebase better than you can?"
- "By this point you have to have adopted your agent's perspective. There's no way around that."
- "That small chore, that small bug — you absolutely are wasting your time [doing it in-loop]. I guarantee you that."
- "Imagine you are your agent right before you hit enter... could you solve the problem you're going to ask your agent to solve?"
- "If you cannot encode what you would do into your prompts... you will not get repeated agentic success."
- "You will not scale your agentic layer if you are stuck in the terminal prompting back and forth."
- "There are two problems in there and the chance they accomplish both go down" — one agent, one prompt, one purpose.
- "The goal here is not to try to climb to the highest class... The goal is to recognize where you are, what pieces you have, what pieces you're missing."
- "You're building the machine that builds your product now."
- "Target zero-touch engineering... This is not a dream anymore. It's not a meme."
- "We are now commanders of compute."

**What Dan actually did/built** (the `orchestrator-agent-with-adws` codebase + a graded tour of mock codebase structures):
1. Opened the Class 3 system: prompted the orchestrator to kick off a **plan_build_review_fix ADW** in a target directory; ran a second ADW building a markdown-preview app end-to-end; showed the new ADWs view UI alongside the log-stream view.
2. Walked a concrete codebase per grade: G1 `.claude/commands/prime.md` + `CLAUDE.md` (agents.md referencing it); G2 `specs/`, `ai_docs/`, `.claude/agents/fetch-docs.md`, `test-writer.md`, `plan.md`; G3 `.mcp.json` (Postgres/Firecrawl/Jira/Notion), skills `migrate-database` and `start-stop-application` (teaching the agent scripts), `prime_db` teaching raw `psql`; G4 `app_reviews/`, `code_review.md`, `reproduce_bug.md`, `test_backend.md`/`test_frontend.md` with request-validate-resolve closed loops, review sub-agent; G5 templates `bug.md`/`feature.md`/`chore.md`, new/update/test API endpoint templates; G6 `plan_build.md` ("create a plan and then build it — run our plan prompt, capture the path, execute build on it") and `scout_then_plan.md` (parallel scouts → synthesize → plan); G7 `experts/` directory with expertise files; Class 2 `adw/` webhook + `core agent SDK` module + full ADWs; Class 3 orchestrator directory (nested app or inside `adws/`) with fixer/reviewer/builder command-level agents and orchestrator tools.
3. Demonstrated the application layer splitting (client/server → two git-submodule codebases under `apps/`) while one agentic layer wraps them all.
4. Closed with the full TAC recap and announced his next project: building a 4–5 figure/month business run by agents, recorded end to end.

**Workout module:**
- **Goal:** Grade your own codebase against the class/grade rubric and climb exactly one grade this week.
- **Prerequisites:** A real repo you work in daily; workouts AH-1..AH-5 give you the pieces for grades 1–7.
- **Steps:**
  1. Audit: create `agentic_layer_audit.md` with a checklist row per grade (C1G1 prime/memory → C3G3 orchestrator+ADW). For each: have it / partial / missing, with file paths as evidence.
  2. Identify your current grade = highest grade where everything below is solid. (Most engineers: C1G3–G4; "a lot of engineers are probably missing agent experts.")
  3. Pick the next grade and build its distinguishing artifact:
     - → G4: write one closed-loop prompt (`test_backend.md`) with explicit request → validate → resolve steps that loops until tests pass.
     - → G5: write `bug.md` — a template with your exact debugging steps, relevant-files section, and a mandatory validation step; have your agent fill it in for a real bug.
     - → G6: write `plan_build.md` that chains your existing `/plan` and `/build` — and verify each piece still runs standalone.
     - → G7: build the AH-5 database expert.
     - → C2G1: expose one HTTP webhook that fires `claude -p "/plan_build <task>"` against your repo from outside the terminal.
     - → C2G2: wrap that chain in a script (deterministic code) with logging, a validation gate between plan and build, and one retry.
  4. Run one real task end-to-end at the new grade; keep the produced artifacts (spec, review file, expertise diff) as your trail of success.
  5. Re-grade. Update the audit file. Schedule the next climb.
- **Done-when:** The audit file exists with evidence paths; one real work item shipped through the new grade's mechanism without you editing code by hand; you can state your class/grade in one sentence.
- **Level-up:** Convert your most-used prompt chain into a true ADW (deterministic script + agent SDK calls + logging/validation/retries), then put your O-agent in front of it — Class 3, Grade 3, knocking on the codebase singularity.

**Quote of the lesson:** "When the agents arrived, something changed. We weren't just AI coding anymore. We started orchestrating intelligence."

# AH-1 · Elite Context Engineering — Master Teaching Notes

> Source of truth for the expanded chapter. Video 73:20 · Lesson #9 · Intermediate · Framework: **R&D — Reduce & Delegate**
> Lesson artifact: a 301-line README that enumerates 12 techniques across 4 levels, plus a full `.claude/` agentic layer (commands, sub-agents, hooks, output styles, an expert triad) and a two-app `apps/` playground. The whole codebase is a context-engineering exhibit.

**Lesson thesis in one sentence:** A focused agent is a performant agent, and there are only two ways to keep an agent focused — **Reduce** context out of your primary agent and **Delegate** context onto other agents — so master the 12 R&D techniques and you can measure, own, and scale your agents' most precious resource: the context window.

**The chapter must land the framework + 12 techniques + the future.** The framework and each technique below follow: Hook → Picture → Worked example (course codebase) → Dan's term → Failure mode → Retrieval Q. Techniques are grouped by their four levels. Two beats (Technique 9 and the future recap) are rendered as diagrams, not frames.

---

## Idea 0 — The frame: a focused agent is a performant agent (R&D)

**Hook.** You've been told models are getting smarter. True — and irrelevant if you keep drowning them. The bottleneck on a modern agent isn't intelligence; it's the state you cram into its context window. "How good are your context engineering skills? Do you have a skill issue? Let's find out and fix it."

**Picture.** Frame t0176 (2:56): the full-screen **REDUCE AND DELEGATE** title card. Frame t0266 (4:26) is the counter-image: a `/context` readout already at 63k/200k (31%) on boot, with MCP at 24.1k and a bloated memory file at 23.7k — the mess R&D exists to clean up.

**Worked example.** The entire `elite-context-engineering` repo is the framework in miniature: the README lists all 12 techniques tagged by Level (Beginner→Agentic) and Framework (Reduce/Delegate/R&D); the `.claude/` tree is the machinery (priming commands, sub-agents, hooks, output styles, an expert triad). Nothing here is application code for its own sake — it's context-engineering apparatus.

**Dan's term.** *The R&D framework — Reduce and Delegate.* Also: *a focused agent is a performant agent*, *context sweet spot*, *search and destroy*, *core four bullseye*, *context rot / context bloat*.

**Failure mode.** Hearing "context engineering" as "write a good prompt and dump in some files." The weak student never measures, never adopts the agent's perspective, and treats the window as free background plumbing — then blames the model when a bloated window underperforms.

**Retrieval Q.** What are the only two ways to manage a context window, and what's the one-line law behind them? *(Reduce and Delegate; a focused agent is a performant agent.)*

---

# LEVEL 1 — BEGINNER

## Idea 1 — Technique #1: Measure to Manage

**Hook.** You cannot manage what you cannot see. Boot a fresh Claude Code and you might already be a third full — and you'd never know it.

**Picture.** Frame t0266 (4:26): `/context` shows `claude-opus-4-1-20250805 · 63k/200k tokens (31%)`, broken down (System prompt 3.1k, System tools 11.7k, MCP tools 24.1k, Custom agents 122, Memory files 23.7k, Free 137.3k), with the IDE token counter reading `Tokens: 2650` for the README.

**Worked example.** Run `claude`, then `/context`. Install a tokenizer in your IDE so the README's ~2,650 tokens are visible *before* an agent reads it (the README is a high-touch file). Every later technique depends on this one number: how full is the window, and with what?

**Dan's term.** *"What gets measured gets managed. So measure your context window."* Tools: `/context` (what's in the window) and a token counter (what you're about to add).

**Failure mode.** Never running `/context` — "vibe coding," in Dan's words. You optimize a prompt while sitting in a 31%-full, MCP-and-memory-bloated window and can't understand why results wander.

**Retrieval Q.** Name the two measurement tools and what each tells you. *(/context = exact breakdown already in the window; a token counter = a file's cost before it enters context.)*

---

## Idea 2 — Technique #2: Avoid MCP Servers (when you don't need them)

**Hook.** The most expensive thing in your window might be tools you never call.

**Picture.** In t0266, MCP tools = 24.1k (12.1%). Frame t0505 (8:25) is the fix: after `--mcp-config` with firecrawl only, MCP drops to 6.5k (3.2%); the file tree shows the `.mcp.json.*` options.

**Worked example.** Delete the default project `.mcp.json`; avoid global (user/local) servers. Start with none, then load exactly what you need: `claude --mcp-config .mcp.json.firecrawl_7k.sample` (add `--strict-mcp-config` to override globals for that one instance). The repo ships pre-scoped configs and self-fixes the token cost in the filename so you know it up front.

**Dan's term.** *"Do not load MCP servers unless you need them."* The math: ~24k wasted per agent × five agents/hour ≈ 25% of a whole window gone.

**Failure mode.** Keeping a default `.mcp.json` "just in case," silently paying 10–12% of every agent's window for tools you don't use this session.

**Retrieval Q.** How do you load only the MCP server you need, and what flag overrides global servers? *(`claude --mcp-config <file>`; `--strict-mcp-config`.)*

---

## Idea 3 — Technique #3: More Prime, Less CLAUDE.md

**Hook.** The convenience of an always-loaded memory file is exactly what rots your window.

**Picture.** t0266 shows the `⚠ Large CLAUDE.md will impact performance (79.7k chars > 40.0k)` warning with memory files at 23.7k (11.8%). Frame t0786 (13:06): after swapping to the 43-line concise `CLAUDE.md`, memory files fall to 358 tokens (0.2%) and free space is 92.4%.

**Worked example.** `CLAUDE.large.md` (2,978 lines; header literally reads "an example of a BLOATED CLAUDE.md file... the anti-pattern of over-contextualization") vs the 43-line `CLAUDE.md`/`CLAUDE.concise.md`. Instead of a growing memory file, **prime**: `/prime` runs `git ls-files`, reads the README, reports; `/prime_cc` stacks on top to load the `.claude/` layer. Different task → different prime, so the window is always task-scoped.

**Dan's term.** *"The CLAUDE.md file is incredible for one reason: it's a reusable memory file that's always loaded. Simultaneously, it's terrible for the exact same reason."* And: *"Prime, don't default."*

**Failure mode.** Letting CLAUDE.md grow forever into a contradictory 3,000-line glob, and reading the performance warning as noise. Contradictory context is the worst case — it actively steers the agent wrong.

**Retrieval Q.** Why is CLAUDE.md "incredible and terrible for the same reason," and what replaces it? *(It's always loaded; great for guaranteed universals, terrible because it only grows toward irrelevance/contradiction. Replace with context priming + a tiny universals-only CLAUDE.md.)*

---

# LEVEL 2 — INTERMEDIATE

## Idea 4 — Technique #4: Control Output Tokens

**Hook.** Your most expensive tokens are the ones the agent talks back to you with — and they re-enter the window.

**Picture.** Frame t1085 (18:05): left terminal `> hi` → `● Done.`; right terminal the `/output-style` menu (Default, Explanatory, Learning, Ultra Concise, One Word Output, TTS Summary, Bullet Points, YAML Structured).

**Worked example.** Output tokens cost ~3–5× input tokens. You can't cut the tokens spent *writing files*, but you can cut the *response*. The `concise-done.md` "One Word Output" style turns a ~150-token status reply into a 2-token "Done." (~99% off). Output styles hot-swap the output-style block in Claude Code's system prompt. Exceptions: questions and errors still get concise real answers.

**Dan's term.** *"Output tokens are priced anywhere from three to five X the price of your input tokens... a massive 99% reduction."* Note the trend teaser: *hot-swapping the system-prompt block.*

**Failure mode.** Dismissing this as trivial at one-agent scale and missing the compounding: 150 vs 2 tokens across hundreds of prompts and agents is a large, recurring drain on your most expensive tokens.

**Retrieval Q.** Why do output styles matter and roughly what was the effect shown? *(Output tokens cost 3–5×; a one-word style cut a ~150-token reply to 2 tokens, ~99%, by hot-swapping the output-style block.)*

---

## Idea 5 — Technique #5: Use Sub-Agents — Properly

**Hook.** What if you could run a big, token-hungry job and have almost none of it touch your main agent?

**Picture.** Frame t1492 (24:52): `load_ai_docs.md` (allowed-tools `Task`, firecrawl) above a terminal reading "Found 10 files... Launching docs-scraper agents…". In `/context`, Custom agents = 122 tokens (0.1%).

**Worked example.** A sub-agent's definition is a **system** prompt, so custom agents cost ~122 tokens in your primary window even though the sub-agent burns thousands doing work. `/load_ai_docs` reads `ai_docs/README.md`, deletes stale docs, and fires `docs-scraper` sub-agents in parallel via the `Task` tool — each scrape (~3k tokens) stays *off* your primary window and returns a concise report to your *primary agent* (not to you).

**Dan's term.** *"When you use Claude Code sub-agents, you are effectively creating a partially forked context window."* This is the D — delegation.

**Failure mode.** Spawning sub-agents before you can track one agent's context; losing the flow of information (who prompts whom, who reports to whom). "If you're losing track of a single agent, you probably aren't ready for sub-agents."

**Retrieval Q.** Why do custom sub-agents cost only ~122 tokens in the primary window? *(They're system prompts, not user prompts, so they aren't added to the primary window; the sub-agent burns its own window and reports back to the primary agent.)*

---

## Idea 6 — Technique #6: Architect / Editor (Planner / Builder)

**Hook.** Your best code comes from an agent that never had to *find* anything — it was handed a perfect plan.

**Picture.** Frame t1790 (29:50): split screen — LEFT the planner thinking through the 3-file wrapper spec ("1. A types file... 2. A low-level file that wraps the SDK... 3. A CLI file"), RIGHT a fresh agent at `/clear` then `/build`.

**Worked example.** `/quick-plan` (the architect; `allowed-tools` Read/Write/Edit/Glob/Grep; writes `specs/<name>.md`) over-gathers context — *that's its job* — then a separate `/build` agent reads only the spec and implements with a clean window. The demo builds `apps/cc_ts_wrapper` (types.ts, core.ts, cli.ts), a Claude Code TypeScript SDK wrapper, from the plan. "You go overboard planning, then delete."

**Dan's term.** *Architect and editor / planner and builder.* Shout-out to legacy AI-coding tools (Aider) that separated planning from building.

**Failure mode.** Prompt-chaining inside one chat window instead of splitting responsibilities, causing context rot with every non-focused prompt and denying the builder a clean window for surgical edits.

**Retrieval Q.** In the architect/editor split, whose job is it to "waste" tokens, and why? *(The planner's — it over-gathers to write a complete spec; you then delete the irrelevant parts so the builder gets a focused window.)*

---

# LEVEL 3 — ADVANCED

## Idea 7 — Technique #7: Avoid /compact — Reset and Prime

**Hook.** After `/compact`, quick — what's in your window right now? You don't know. Neither does Dan.

**Picture.** Frame t2050 (34:10): the builder's finished `cc_ts_wrapper` report (types.ts/core.ts/cli.ts + "Git diff stats: 1 file changed") followed by `> /compact` → "Compacting conversation…".

**Worked example.** `/compact` is a bandaid: it summarizes and leaves an *unknown* state you must Ctrl-R to reread. Instead, `/clear` (blow the window away completely) then `/prime` (reload exactly what you want). You trade a little work for certainty — and it prepares you for out-loop coding, where no single agent should overflow 200k and trigger a compaction you can't predict. If it would, chop up the task.

**Dan's term.** *"When you get to advanced agentic coding, it's time to stop guessing and start knowing... I avoid compact and I recommend that you reset and prime."* And: *"You don't want to delegate the control of your context window."*

**Failure mode.** Reaching for `/compact` reflexively and never knowing the exact window — fine in-loop, fatal the moment you try to scale out-of-loop where predictability is everything.

**Retrieval Q.** Why does Dan avoid `/compact`, and what does he do instead? *(You don't know exactly what's retained; `/clear` then `/prime` so you own and know your exact state.)*

---

## Idea 8 — Technique #8: Use Context Bundles

**Hook.** When an agent's window finally explodes, you don't have to start from zero — you can hand its replacement the story so far.

**Picture.** Frame t2345 (39:05): the `agents/context_bundles/` directory full of `SAT_<hour>_<session>.jsonl` files; one open shows `{"operation":"prompt","prompt":"/prime_cc"}`, `{"operation":"read","file_path":".claude/settings.json"}`, ...; the terminal replays deduped reads.

**Worked example.** A `PostToolUse` hook (`context_bundle_builder.py`) writes an append-only JSONL log of prompts/reads (with limit/offset)/writes to `agents/context_bundles/<DAY_HOUR>_<session_id>.jsonl`. A fresh agent runs `/load_bundle <path>`, which dedups reads (full file if any entry lacks a limit) and replays ~60–70% of the prior agent's state and story — without every detail. Use it selectively.

**Dan's term.** *Context bundle* — *"a simple append-only log of the work that our Claude Code instances are doing... this gets us 70% of where the previous agent was."*

**Failure mode.** Logging every operation and reloading the whole thing — which just overflows the next agent. The trimmed, deduped replay is the point.

**Retrieval Q.** What produces a context bundle and what reloads it? *(A Claude Code hook, `context_bundle_builder.py`, writes per-session JSONL; `/load_bundle` dedups and replays it.)*

---

## Idea 9 — Technique #9: Use One Agent for One Purpose  *(render as diagram)*

**Hook.** The simplest, most powerful rule, and the one that turns techniques into a system: ship one thing at a time.

**Picture.** No unique UI — render as a designed **agent-pipeline (ADW) diagram**: a high-level prompt fanning into single-purpose agents (plan → build → improve → commit).

**Worked example.** It summarizes everything before it. Two-step problem solving: (1) plan the work with *no regard for technology* (users/customers first), then (2) plan how to delegate it across single-purpose agents — an agentic pipeline / AI Developer Workflow (the highest leverage in agentic coding, and the key idea of TAC Lesson 6).

**Dan's term.** *"Use one agent for one purpose so that your context windows are focused."* The pipeline is the *ADW*.

**Failure mode.** Making one capable agent own a whole feature; its window rots and you can't tell which part failed. Single-purpose agents localize both focus and debugging.

**Retrieval Q.** What two planning steps does "one agent, one purpose" force? *(Plan the work without regard for technology; then plan the agent pipeline / ADW to deliver it.)*

---

# LEVEL 4 — AGENTIC (the hidden level)

> "Many engineers will not get to this level. Many engineers don't need this level." Here your patterns scale into your ADWs — powerful and dangerous.

## Idea 10 — Technique #10: Modify the System Prompt

**Hook.** Beneath output styles is the real control surface: the system prompt itself.

**Picture.** Frame t2705 (45:05): one command line — `claude --dangerously-skip-permissions --model sonnet --append-system-prompt "IMPORTANT: When using the Read tool, ALWAYS read in increments of 100 lines... prefix your last message with ✅ or ❌..." -p "what is CLAUDE.large.md for?"`.

**Worked example.** Two knobs: `--append-system-prompt` (adds to Claude Code's crafted default) and the SDK's `customSystemPrompt` (a full *overwrite* — dangerous). Appending must run in **print mode** (`-p`, out-loop). The demo forces the read tool into 100-line increments and a ✅/❌ final-message prefix; the run's context bundle proves obedience — `Read(100)`, `Read(100)` — reducing lines read (and tokens). Points to the Claude Code SDK Mastery extended lesson.

**Dan's term.** *"When you control the behavior, you control the context window."* And the warning: *"Do not use [customSystemPrompt] unless you know what you're doing."*

**Failure mode.** Grabbing `customSystemPrompt` and blowing away the carefully crafted default system prompt. Use `--append-system-prompt` unless you truly need a replacement.

**Retrieval Q.** Which flag appends to the system prompt, what mode is required, and what's the dangerous SDK alternative? *(`--append-system-prompt`; print mode (`-p`); the SDK's `customSystemPrompt`, which overwrites the default.)*

---

## Idea 11 — Technique #11: Primary Multi-Agent Delegation

**Hook.** Sub-agents report back to you. What if you fire off a *fully independent* agent that just… goes and does the job while you keep working?

**Picture.** Frame t3195 (53:15): a background Claude Code kicked off — `REPORT_FILE: ./agents/background/background-report-Sat_13_02_53.md`, "Running in the background", "When it completes it will rename the file to ...complete.md on success or ...failed.md if it fails", "1 background task" — beside the run's context bundle.

**Worked example.** Primary agents are independent Claude Code instances (own context/model/settings/keys). The lightweight version is `/background`, which builds `claude --model <m> --output-format text --dangerously-skip-permissions --append-system-prompt "<report structure + rename logic>" --print "<prompt>"` and runs it detached, writing a live report file. `scripts/bg_claude_code_test.sh` is the raw shell version. Compute orchestrating compute — out of loop, no babysitting.

**Dan's term.** *"Compute orchestrating compute, agents orchestrating agents... Better agents, and then more agents."*

**Failure mode.** Conflating background/primary delegation with sub-agents. Primary delegation gives full control (and runs on your API keys) — more power, more responsibility.

**Retrieval Q.** How is primary delegation different from sub-agents? *(Primary agents are fully independent instances with their own context/model/settings/keys and report via files; sub-agents are partially forked windows that report back to the primary agent.)*

---

## Idea 12 — Technique #12: Agent Experts

**Hook.** Encode the one engineer who knows that gnarly subsystem better than anyone — then let it maintain itself.

**Picture.** Frame t3485 (58:05): `experts/cc_hook_expert/` expanded to its three files — `cc_hook_expert_build.md`, `cc_hook_expert_improve.md`, `cc_hook_expert_plan.md` — the plan/build/improve triad that *is* the technique.

**Worked example.** A three-step expert: **plan** (writes a spec to `specs/experts/cc_hook_expert/`), **build** (implements from the spec — the demo builds `universal_hook_logger.py`), **improve** (reads the `git diff`/`git log` and updates *only* the dedicated `## Expertise` sections of the plan and build experts, never the Workflow). Evidence it works: the plan expert already carries a "Discovered Patterns from Universal Logger Implementation" block — the improve step has run. Wrap plan→build→improve→commit and you have an ADW.

**Dan's term.** *"You fire off specialized agents that are experts at specific parts of your codebase, and here's the kicker, you have them auto-update their own knowledge."* And the craft note: *"We're not conflating our headers"* — Expertise is its own section, distinct from Purpose/Instructions/Workflow.

**Failure mode.** Building an "expert" as a static mega-prompt and skipping the improve step, so it never self-updates and rots like any other memory file.

**Retrieval Q.** What are the three steps of an agent expert, and what makes it self-improving? *(Plan → Build → Improve; the improve step reads the git diff and updates only the dedicated `## Expertise` sections.)*

---

## Idea 13 — The future you can bet on  *(render as diagram)*

**Hook.** The reason context engineering is a *safe* bet: the models fight you as the window grows, and that won't change soon.

**Picture.** No slide — narrated over B-roll; render as a **five-card future diagram**.

**Worked example / Dan's term.** Five trends: (1) **larger** context windows (get around `/compact`); (2) **better/effective** context windows (attention-mechanism problem — capability drops as length grows); (3) **hot-swapped** context (tools/context/system-prompt, like output styles already do); (4) **multi-agent architectures** for delegation; (5) **specialized agents everywhere** (plug into the Claude Code SDK and specialize context/model/prompt/tools). Closer: *"It's not about saving tokens. It's about spending them properly"* — one-shot out-loop streaks so you can drop your presence. And don't forget prompt engineering (see the Agentic Prompt Engineering and Claude Code SDK Mastery extended lessons).

**Failure mode.** Assuming bigger future windows make this obsolete. Bigger helps; *effective* is the frontier — context engineering keeps paying off.

**Retrieval Q.** Name two future trends and the reason context engineering stays a safe bet. *(Any two of: larger / better-effective / hot-swapped context, multi-agent architectures, specialized agents; models lose capability as context grows.)*

---

## Timeline map (VTT-verified)

| Time | Beat |
|---|---|
| 0:16–3:00 | Cold open: focused agent = performant agent; context sweet spot; adopt the agent's perspective; search and destroy; **R&D — reduce and delegate** |
| 3:33–5:29 | **T1 Measure:** /context (63k/31% on boot); token counter (README ~2,650); "what gets measured gets managed" |
| 5:50–9:26 | **T2 Avoid MCP:** MCP 24.1k (12%); delete default .mcp.json; `--mcp-config` + `--strict-mcp-config` (firecrawl → 6.5k) |
| 9:26–16:12 | **T3 Prime > CLAUDE.md:** bloated CLAUDE.large.md warning (23.7k); concise 43-line file (0.2%, 92% free); /prime, /prime_cc; experts/ teaser |
| 16:27–22:24 | **T4 Output tokens:** 3–5× cost; One Word "Done." (2 vs ~150); output styles hot-swap the system-prompt block |
| 22:41–28:08 | **T5 Sub-agents:** partially forked; custom agents 122 tokens; /load_ai_docs fires docs-scraper in parallel (delegation) |
| 28:46–33:00 | **T6 Architect/Editor:** /quick-plan (Opus) → spec; fresh /build; go overboard then delete; builds cc_ts_wrapper |
| 33:47–36:33 | **T7 Avoid /compact:** unknown state after compact; /clear + /prime; own your window; prep for out-loop |
| 37:11–41:00 | **T8 Context bundles:** hook-built append-only JSONL; /load_bundle dedups + replays ~70% |
| 41:28–43:01 | **T9 One agent, one purpose:** plan work sans tech, then the agent pipeline (ADW) |
| 43:01–48:07 | **T10 System prompt:** `--append-system-prompt` (print mode); read-in-100s + ✅/❌; bundle shows Read(100) |
| 48:55–56:39 | **T11 Primary delegation:** /background independent instance; report file + rename; compute orchestrating compute |
| 56:39–68:00 | **T12 Agent experts:** cc_hook_expert plan/build/improve; improve updates only ## Expertise; builds universal_hook_logger |
| 68:00–73:13 | Recap: spend tokens properly; future trends (larger/better/hot-swap/multi-agent/specialized); prompt engineering; sign-off |

## Terminology glossary (Dan-isms, canonical spellings)

- **R&D framework** — Reduce and Delegate; the only two ways to manage a context window
- **A focused agent is a performant agent** — the lesson's central law (paired with "a focused engineer is a performant engineer")
- **Context sweet spot** — the range of context where an agent performs at maximum capability
- **Core four bullseye** — right model + prompt + tools aligned with the right *range* of context
- **Search and destroy** — find context agentically, then remove/delegate it to prevent rot/bloat
- **Context rot / context bloat** — stale/contradictory context (rot) and irrelevant filler (bloat) degrading the agent
- **Context priming** — a reusable slash command that sets a task-scoped initial window (vs an always-on CLAUDE.md)
- **Output styles** — reusable response styles that hot-swap the output-style block in Claude Code's system prompt
- **Sub-agent** — a partially forked, system-prompt-isolated context window that reports to the primary agent
- **Architect/editor** (planner/builder) — split planning and implementation across two agents
- **Context bundle** — an append-only per-session JSONL trail of prompts/reads/writes (built by a hook) for remounting
- **Primary (multi-agent) delegation** — firing independent Claude Code instances (e.g. /background)
- **Agent expert** — a plan/build/improve triad that owns a codebase area and self-updates its ## Expertise
- **ADW** — AI Developer Workflow; the agentic pipeline that single-purpose agents compose into
- **In-loop / out-of-loop / ZTE** — you present / agents run without you / zero-touch engineering
- Transcript corrections: "CloudCode/Cloud Code"→Claude Code, "claw.md/flaw.concise"→CLAUDE.md/CLAUDE.concise.md, "ADER"→Aider, "Bunn"→Bun, "agent decoding"→agentic coding, "Outloop"→out-of-loop, "loot/loop box"→loot box

## Bridge to the rest of the curriculum (as trailed in-lesson)

- **TAC Lesson 6** — "one agent for one purpose" in full (the ADW model this lesson borrows)
- **TAC Lesson 8** — multi-agent workflows, systems, and UIs (primary delegation at scale)
- **Agentic Prompt Engineering (AH-2)** — the powerful prompt structures used in every command/agent here ("if you're writing bad prompts, your context doesn't matter")
- **Claude Code SDK Mastery** — `customSystemPrompt`, headless/print mode, and building domain-specific agents (the machinery behind Techniques 10–12)
- Constant thread: measure → reduce → delegate → one agent, one purpose → compose into ADWs → drop your presence

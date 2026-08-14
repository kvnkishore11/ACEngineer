# AH-3 — Building Domain-Specific Agents · Master Teaching Notes

> **Lesson:** Agentic Horizon #11 (Advanced) · **Course:** AH · **Runtime:** 1:07:10 (4030s @ 1920×1080)
> **URL:** https://agenticengineer.com/tactical-agentic-coding/course/building-domain-specific-agents
> **Codebase:** `agentic-horizon/building-specialized-agents` — 8 custom agents in `apps/custom_1..8_*`
> **Tactic:** *Build Custom Agents* — take programmatic control of the core four so your compute serves **your** domain.

This is the technical-accuracy extract. It exists so the chapter author (and a weak student) can trust every claim, name, and number. Each major idea below follows the teaching model: **Hook → Picture → Worked example → Name → Failure → Retrieval.**

---

## The one-sentence thesis

**Agentic engineering leads every engineer down one single path: _better agents → more agents → custom agents_.** You master a single agent (prompt + context engineering), then scale to many agents, and finally — when out-of-the-box tools stop fitting your domain — you go to the bare metal and build **custom agents** whose context, model, prompt, and tools you control in code. The reason: *the out-of-the-box agents are built for everyone's codebase, not yours*, and that mismatch costs hundreds of hours and millions of tokens as your codebase grows.

The lesson teaches this by building **eight custom agents on the Claude Agent SDK**, simple → complex, so you learn the primitives before the products.

---

## The 8-agent ladder (the spine of the lesson)

| # | Agent | Form factor | New primitive it teaches | Model | Prompt strategy |
|---|-------|-------------|--------------------------|-------|-----------------|
| 1 | **Pong** | CLI script | System prompt = the whole product | Sonnet 4 | overwrite (3 lines) |
| 2 | **Echo** | CLI script | Custom `@tool` + in-memory MCP; query vs client; model downgrade | Haiku 3.5 | overwrite (1 line) |
| 3 | **Calc** | Terminal REPL | `disallowed_tools` (de-context built-ins); `resume` continuity | Sonnet 4 | overwrite |
| 4 | **Social Hype** | CLI stream handler | Data-stream agent; static system-prompt variable; workflow-in-prompt | Sonnet 4 | overwrite + `{VAR}` |
| 5 | **QA** | Terminal REPL | Hooks (governance/`.env` block); Firecrawl MCP; parallel `Task` | Sonnet 4 | overwrite + examples |
| 6 | **Tri-Copy-Writer** | Vue + FastAPI | Agent as backend method; 1 prompt → N variations; Pydantic response | Sonnet 4 | overwrite + `{VAR}` |
| 7 | **Micro SDLC** | Vue kanban + FastAPI | Multi-agent hand-off; **extend vs overwrite**; write-path hooks | Sonnet 4 / Opus 4.1 | preset+append (planner/reviewer), pure preset (builder) |
| 8 | **Ultra Stream** | Vue dual-panel + FastAPI | One agent produces → another consumes; token-efficient chunked read; self-managed context | Sonnet 4 | overwrite (both) |

> The ladder is deliberate: *"Everything large is a few small things that you understand fundamentally first."* Don't skip to agent 8.

---

## Major idea 1 — The system prompt is the law of the agent

- **Hook:** You type "hello." It says "pong." You type "summarize this codebase." It says "pong." You type "king." It says "pong." What on earth builds an agent this stubborn?
- **Picture:** `t0225` (terminal: `hello` → **Agent Response: pong** + Session ID / 1483ms / $0.003629) and `t0300` (the entire `PONG_AGENT_SYSTEM_PROMPT.md` — three lines).
- **Worked example:** The Pong agent is ~150 lines, and *most of it is logging*. The only thing that defines its behavior is a 3-line markdown system prompt loaded into `ClaudeAgentOptions(system_prompt=..., model=...)`. Two changes to the SDK config — model + system prompt — and the world's best coding agent becomes a pong machine.
- **Name it:** *The system prompt.* It is injected before **every** user prompt, so **all of your work is multiplied by your system prompt** — "the most important element of your custom agents, with zero exceptions." Overwrite it and *"this is not Claude Code anymore… it might be using the same model, but the system prompt is truly what builds the agent."*
- **Failure mode:** Believing a "custom agent" needs a mountain of code. The leverage is in the prompt; the Python is plumbing.
- **Retrieval:** *What two things does Pong change to become a new product, and why does the system prompt matter more than any single user prompt?* → model + system prompt; the system prompt runs before every user prompt, so it governs every run.

---

## Major idea 2 — Control the core four in code (and everything costs context)

- **Hook:** Ask the Echo agent to "list your available tools." You added exactly **one** tool. It lists **sixteen**. Where did the other fifteen come from — and who's paying for them?
- **Picture:** `t0565` (Echo: `create_sdk_mcp_server`, `allowed_tools=["mcp__echo__echo"]`, `model="claude-3-5-haiku-20241022"`) and `t1040` (Calc: the full `disallowed_tools` block — Read, Write, Edit, … Bash, KillShell).
- **Worked example:** Echo adds one custom tool but the ~15 built-in Claude Code tools are **still loaded into context** — 15 extra options the model must weigh, and tokens you pay on every call. Calc fixes it: an explicit `disallowed_tools=[...]` list removes those built-ins entirely — *"These tools do not end up in its context window. This is not an option… they can't see this."*
- **Name it:** *The core four* — context, model, prompt, tools — set explicitly via `ClaudeAgentOptions`. `allowed_tools` gates what **can** be called; `disallowed_tools` removes definitions from **context**. `model=` right-sizes intelligence (Echo drops to **Haiku** — cheap, fast, less smart, and correct for a trivial transform). *"Whenever you see Claude Code options, isolate the core four."*
- **Failure mode:** Thinking `allowed_tools` alone keeps context lean. It doesn't — the built-in tool **definitions** still load unless you disallow them. Run `/context`; adopt your agent's perspective.
- **Retrieval:** *Why isn't `allowed_tools` enough to keep context small, and what does `disallowed_tools` actually do?* → `allowed_tools` only gates calls; `disallowed_tools` unloads the tool definitions so they never reach the window.

---

## Major idea 3 — `query()` for one-off, `ClaudeSDKClient` for conversation

- **Hook:** Pong used `query()`. Echo *can't* — it needs `ClaudeSDKClient`. What changed?
- **Picture:** `t0565` — `async with ClaudeSDKClient(options=options) as client:`.
- **Worked example:** `query(prompt, options)` fires a single one-off request and cannot use custom tools. `ClaudeSDKClient` maintains a continuous conversation and is **required** for custom tools; call `client.query()` multiple times and it remembers. Calc's REPL keeps memory across turns by capturing `ResultMessage.session_id` and passing it back as `resume=` next loop.
- **Name it:** *query vs client; resume-based session continuity.* *"Query is for one-off prompts and the Claude SDK client is for continuous conversations."*
- **Failure mode:** Reaching for `query()` with a custom tool (the tool never fires), or losing memory because you never captured/passed the `session_id`.
- **Retrieval:** *When must you use `ClaudeSDKClient`, and how do you keep a conversation alive across calls?* → for custom tools and multi-turn; capture `ResultMessage.session_id`, pass as `resume=`.

---

## Major idea 4 — Custom tools + MCP, and "manage the responses"

- **Hook:** How do you *give* an agent a new power — and how do you *see* what it's doing?
- **Picture:** `t0565` (the `@tool` echo + `create_sdk_mcp_server`) and `t1360` (Social Hype's live stream: Agent Response → **Tool Called: submit_analysis** → **Tool Called: notify**).
- **Worked example:** A tool is the `@tool("name", "description", {param: type})` decorator over an async function; mount it with `create_sdk_mcp_server(...)` — *"this builds an entire MCP server in memory for our agent."* The **description** tells the agent when/how to use it; inside, you're back in deterministic code — do anything, return `{"content": [...]}`, and on failure return the error so the agent can **pivot** (the "stdout + tools" leverage point). The universal loop is **options → agent → query → manage the responses**: parse `TextBlock` / `ThinkingBlock` / `ToolUseBlock` / `ToolResultBlock` and `ResultMessage` (session/cost). Custom agents can also load *existing* MCP servers (QA uses **Firecrawl**, ~6k tokens).
- **Name it:** *Custom tools, in-memory MCP, response-stream primitives.* *"If you don't adopt your agent's perspective, it will be hard to improve them"* — build observability in.
- **Failure mode:** Treating tools as magic. A tool is deterministic code with a good name/description; the model only decides **when** to call it. Also: over-indexing on the exact block-type names (Dan: *"these might change… understand the primitives"*).
- **Retrieval:** *What does a tool's description do, and what should a tool return on error?* → tells the agent when/how to call it; return the error content so the agent can pivot.

---

## Major idea 5 — System-prompt variables: static (locked) vs dynamic (per-call)

- **Hook:** The Social Hype agent takes a `-n "notify me when…"` flag and bakes it into the **system** prompt. How can a "variable" live in the law of the agent?
- **Picture:** `SOCIAL_HYPE_AGENT_SYSTEM_PROMPT.md` — `NOTIFICATION_CRITERIA: {NOTIFICATION_CRITERIA}` (substituted at boot).
- **Worked example:** The value is injected once when the agent starts and then **frozen for its life** — *"a static variable that is dynamically updated… as long as this agent runs, I just want it to look for this."* That's exactly right for a single-boot agent. Contrast a true dynamic **user-prompt** variable (`$1` / `$ARGUMENTS`) which updates every turn. Tri-Copy-Writer does the same with `{NUMBER_OF_VERSIONS}` set by its `-v` flag.
- **Name it:** *Static (runtime-locked) system-prompt variable vs dynamic user-prompt variable.*
- **Failure mode:** Expecting a system-prompt variable to change per call — it won't; only user-prompt variables do.
- **Retrieval:** *Where is `{NOTIFICATION_CRITERIA}` set, and when does it change?* → in the system prompt, once at boot; it never changes for that run.

*(Related — idea 5b, workflow-in-system-prompt:* the Social Hype and Ultra Stream agents put a fixed **workflow** in the system prompt. That's correct **because they're domain-specific** — you know what should happen every time, so you encode it as law. The generic Claude Code prompt has no workflow because it must stay multi-purpose.)*

---

## Major idea 6 — Hooks give custom agents governance and permissions

- **Hook:** You ask the QA agent to read the `.env.sample` file. It refuses — *"blocked reading .env in the file path"* — and tells you why. Who taught it to say no?
- **Picture:** `t2170` — `block_env_files`: `if ".env" in file_path:` → 🔒 SECURITY HOOK → `return {"hookSpecificOutput": {"permissionDecision": "deny", …}}`.
- **Worked example:** The SDK exposes Claude Code's hook system in code (`HookMatcher` / `HookContext` on `PreToolUse` / `PostToolUse`). QA registers a hook that denies any `Read` touching `.env` and a `log_tool_usage` audit hook. The Micro SDLC agents go further: the **planner** can write **only** to `specs/`, the **reviewer** only to `reviews/` — enforced by path-checking write hooks (`t2825` shows a live *Write Request → Write Allowed to specs/ → Tool Allowed* trace).
- **Name it:** *Hooks for governance/permissions.* *"This is essential for governance, for control, for permissions in all of your agents"* — and, crucially, **hooks cover subagents too**.
- **Failure mode:** Shipping an agent to teammates with no permission checks — letting compute read secrets or write outside its lane.
- **Retrieval:** *What does the QA hook return to block a read, and does it protect subagents?* → `permissionDecision: "deny"` in `hookSpecificOutput`; yes, it covers subagents.

---

## Major idea 7 — Extend vs overwrite (and use the engineering agent for engineering)

- **Hook:** In the Micro SDLC app, the **builder** agent has no custom system prompt at all. Isn't this a lesson about *custom* agents?
- **Picture:** `t2565` (the Plan→Build→Review→Ship kanban board) and `t2825` (`agent_orchestrator.py` → `planner_write_hook`).
- **Worked example:** Three agents, three strategies:
  - **Planner** — `{"type":"preset","preset":"claude_code","append": …}` → **extends** Claude Code + a write-hook to `specs/`.
  - **Builder** — `{"type":"preset","preset":"claude_code"}` → the **pure** Claude Code engineering agent, `bypassPermissions`. *"This is software work. That's what Claude Code is for."*
  - **Reviewer** — preset + **append** + write-hook to `reviews/`.
- **Name it:** *Extension agents vs complete custom agents.* Extension = keep the preset, **append**, tweak. Custom = **overwrite** the system prompt (and further still when you add your own tools). *"You don't always need to blow away the Claude Code system prompt."*
- **Failure mode:** Overwriting the system prompt for ordinary engineering — throwing away a world-class generalist to hand-roll a worse one. And the meta-warning: *never try to compete with Claude Code at general engineering — "they own agentic coding."*
- **Retrieval:** *Why does the builder use the pure `claude_code` preset with no append?* → building software is exactly what Claude Code is for; no overwrite needed.

---

## Major idea 8 — Agents deploy everywhere; one agent's output is another's input

- **Hook:** What if one agent watched an endless log firehose and *summarized* it, while a second agent let you *interrogate* those summaries and page the right team?
- **Picture:** `t3060` — the Ultra Stream dual-panel UI: **Inspector Agent** (left, red HIGH-severity ALERT) beside the **Stream Agent** (right, live severity-tagged feed, Logs:7 / Index:7).
- **Worked example:** The **Stream agent** reads a JSONL log file in **3–5 line chunks** (via a `sed` subprocess), caches raw lines by index, summarizes **one log per tool call** with a severity, raises alerts, and calls `clear_context` to reset its own window — so it runs on a file *far larger than its context window*, indefinitely, cheaply. The **Inspector agent** **consumes** those produced logs (`find_logs_for_user`, `read_produced_log_entries`) and notifies engineering/support. *"You cannot do this without serious prompt engineering with an out-of-the-box agent."*
- **Name it:** *Form-factor freedom + producer/consumer multi-agent + token-efficient domain tools + self-managed context.* This is Dan's favorite combination.
- **Failure mode:** Believing bigger context windows make this obsolete. Chunked streaming + self-managed context handle an *unbounded* stream no single window could hold.
- **Retrieval:** *How does the Stream agent process a file bigger than its context window?* → chunked `sed` reads (3–5 lines), one summary per log, `clear_context` to reset — token-efficient, infinite.

---

## Major idea 9 — When to build a custom agent (and when NOT to)

- **Hook:** After eight dazzling agents, Dan spends the finale telling you *not* to build them.
- **Picture:** narrated over B-roll — render as a **decision box** in the chapter (`frame-plan.json` marks this beat unframed by design).
- **Worked example / Name it:**
  - **Build custom** when you need: **programmatic** agents · **repeat workflows** · **domain-specific** wins others can't get · **cost-down while performance-up** · **permission checks** (safe for teams) · to stay **out of the loop**.
  - **Use out-of-the-box / extended** when: you're **in the loop** prompting back and forth · the workflow is **generic** · you're **exploring/prototyping** · you need an **80%-case generalist** · tasks are **short-lived / lightweight / non-repeatable / non-domain**.
  - **Never** try to reproduce Claude Code as a general engineering agent.
- **Failure mode:** Building a custom agent for an in-loop, generic, or one-off task — spending effort where the generalist already wins.
- **Retrieval:** *Name one reason to build custom and one reason not to.* → build: stay out of the loop / domain-specific / permissions; don't: in-loop, generic, prototyping, one-off.

---

## VTT-verified timeline map

| Time | Beat | Frame |
|------|------|-------|
| 0:07 | Thesis: better → more → custom agents | `t0018` |
| 0:47–1:10 | The mismatch problem; where the alpha is | — |
| 3:24 | **Agent 1 Pong** — run; always "pong" | `t0225` |
| 5:03 | System prompt is the law ("zero exceptions") | `t0300` |
| 6:49 | **Agent 2 Echo** — custom tool + MCP | `t0565` |
| 9:21 | Model downgrade to Haiku | `t0565` |
| ~11:30 | Echo "list tools" → 15 built-ins still loaded | — |
| 13:30 | **Agent 3 Calc** — REPL | — |
| 17:10 | `disallowed_tools` block | `t1040` |
| 19:42 | "It's not the models that are the bottleneck… it's you and I" | — |
| 21:38 | **Agent 4 Social Hype** — run | — |
| 22:03 | Bluesky firehose + sentiment | `t1360` |
| 27:38 | Workflow embedded in the system prompt | — |
| 29:49 | **Agent 5 QA** — codebase Q&A REPL | — |
| 30:43 | Firecrawl MCP; 13 tools | `t1852` (arch) |
| 35:41–36:10 | Hook blocks reading `.env` | `t2170` |
| 37:08 | **Agent 6 Tri-Copy-Writer** — Vue UI | `t2265` |
| 37:18–38:47 | One prompt → six variations | `t2265` |
| 42:29 | **Agent 7 Micro SDLC** — kanban board | `t2565` |
| 43:44 | Planner thinking; hooks intercept | `t2825` |
| ~46–48 | Planner write-hook → `specs/`; builder pure preset; reviewer append | `t2825` |
| 49:57 | "You don't always need to blow away the Claude Code system prompt" | — |
| 50:11 | **Agent 8 Ultra Stream** — dual panel | `t3060` |
| 51:08 | Inspector agent | `t3060` |
| 55:33 | "operate on a file in a token efficient way" | — |
| 58:20 | "You cannot do this… with an out-of-the-box agent" | — |
| 1:00:20 | "You build custom agents when you want to stay out of the loop" | — (decision box) |
| 1:02:40 | "Don't try to compete with Claude Code" | — |
| 1:06:52 | "It's about what we can teach our agents to do" | — |
| 1:07:04 | Closing: better, more, then custom agents | `t0018` (bookend) |

---

## Glossary / transcript-artifact key

- **Claude Agent SDK** — the SDK these agents run on. Dan *says* "Claude Code SDK" and the on-screen code reads `ClaudeCodeOptions`, but the shipped repo imports `claude_agent_sdk` / `ClaudeAgentOptions`. The package was renamed (see `outdated-vs-current.md`).
- **Core four** — context · model · prompt · tools (subset of the 12 leverage points).
- **query() vs ClaudeSDKClient** — one-off vs continuous conversation (client is required for custom tools).
- **allowed_tools / disallowed_tools** — whitelist calls / remove tool definitions from context.
- **Static vs dynamic variable** — system-prompt value locked at boot vs user-prompt `$1`/`$ARGUMENTS` per call.
- **Extension vs custom agent** — append to the `claude_code` preset vs overwrite the system prompt.
- **Hook** — `PreToolUse`/`PostToolUse` gate; returns `permissionDecision: deny` to block; covers subagents.
- **Peter framework** — the out-loop review pattern (tickets = prompt input + review system) referenced in the SDLC agent.
- Auto-transcript garbles: "Claude Code SDK" (code says Agent SDK) · "fire call/fire crawl" = **Firecrawl** · "clog code / cloud code" = **Claude Code** · "UVR" = `uv run` · "ADW" = AI Developer Workflow.

---

## Cross-references

- Builds on **AH-1** (RD framework / context-window mastery — why context is precious) and **AH-2** (agentic prompt formats — the purpose/variables/instructions/workflow structure visible in every system prompt here).
- Points forward to **AH-4** (multi-agent orchestration / the O-agent), **AH-5** (agent experts — the QA agent is a "simple version of an agent expert"), **AH-6** (building agentic layers). The SDLC + Ultra Stream apps are the seed of the agentic layer.
- Assumes **TAC 1–8** finished (Dan: *"if you haven't finished the TAC lessons… stop watching this video immediately and finish TAC"* — for in-loop → out-loop → ZTE).

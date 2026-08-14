# AH-3 Nuggets — ranked for the struggling learner

Ordering rule: how much of custom-agent competence collapses if this nugget is missing. **Tier 1** is non-negotiable; **Tier 2** is the working machinery of the Claude Agent SDK; **Tier 3** is judgment — when to reach for a custom agent at all.

---

## Tier 1 — If you remember nothing else

**1. The path is fixed: better → more → custom agents.**
You don't decide to build custom agents; you *arrive* at them by pushing compute to its limits on a domain problem the out-of-the-box tools can't clear. Master one agent, then scale to many, then — only when the mismatch bites — go to the bare metal.
*Say it Dan's way:* "Agentic engineering leads every engineer down one single path. Better agents, more agents, and then custom agents."

**2. The system prompt is the law of the agent — with zero exceptions.**
It runs before *every* user prompt, so all the agent's work is multiplied by it. Pong proves it: a 3-line system prompt turns the best coding agent on earth into a thing that says "pong" to anything. Change the system prompt and *"this is not Claude Code anymore."*
*Why weak learners lose it:* they think "custom agent" means lots of code. Pong is ~150 lines and most of it is logging.

**3. A custom agent is just the core four set in code.**
Context, model, prompt, tools — declared explicitly in `ClaudeAgentOptions` so the agent behaves the same way every run. When you open any agent, find the options block and ask: *how is each of the core four being managed here?* That single habit lets you read any agent.

**4. Everything you give an agent ends up in its context window — and costs tokens.**
Tools, MCP configs, system prompt, user prompt: all of it. Echo's gut-punch: add ONE custom tool and the ~15 built-in Claude Code tools are *still* loaded. `allowed_tools` gates what can be **called**; only `disallowed_tools` removes the definitions from **context**.

---

## Tier 2 — The working machinery (Claude Agent SDK)

**5. `query()` is one-off; `ClaudeSDKClient` is a conversation — and the only path to custom tools.**
If your agent needs a custom tool or memory across turns, you need the client. Keep memory alive by capturing `ResultMessage.session_id` and passing it back as `resume=` on the next call.

**6. A tool is deterministic code with a great description.**
`@tool("name","description",{param:type})` + `create_sdk_mcp_server(...)` = an MCP server built in memory. The **description** tells the agent *when* to call it; inside you do anything and return `{"content":[...]}`. On failure, return the error so the agent can **pivot** (the "stdout + tools" leverage point). Custom agents can also load *existing* MCP servers (QA → Firecrawl).

**7. Manage the responses, or you're flying blind.**
The loop is always **options → agent → query → manage responses**. Parse `TextBlock` (answer), `ThinkingBlock` (reasoning), `ToolUseBlock` (a call), `ToolResultBlock` (a return), and `ResultMessage` (session/cost). Log everything — *"if you don't adopt your agent's perspective, it will be hard to improve them."*

**8. Match the model to the task.**
Echo drops to **Haiku** (cheap, fast, less smart — perfect for a trivial transform); most agents use **Sonnet**; the SDLC agent offers **Opus** for heavy planning. *"It's not the models that are the bottleneck anymore. It's you and I."*

**9. Static system-prompt variable ≠ dynamic user variable.**
`{NOTIFICATION_CRITERIA}` / `{NUMBER_OF_VERSIONS}` are set once at boot and **frozen** — right for a single-purpose agent. A true dynamic variable (`$1` / `$ARGUMENTS`) changes every user prompt. Don't confuse them.

**10. Hooks are how custom agents get governance.**
`PreToolUse`/`PostToolUse` hooks can **deny** a tool call (QA blocks reading `.env`; the SDLC planner can write only to `specs/`). Return `permissionDecision: "deny"`. Hooks cover **subagents** too — the security boundary holds when the agent spawns `Task` agents.

**11. Extend before you overwrite.**
`{"type":"preset","preset":"claude_code","append": …}` extends Claude Code; a bare string overwrites it. The SDLC **builder** uses the *pure* preset — building software is exactly what Claude Code is for. *"You don't always need to blow away the Claude Code system prompt."*

**12. Domain tools beat insurmountable problems cheaply.**
Ultra Stream's Stream agent reads a log file *bigger than its context window* by pulling 3–5 lines at a time (`sed` subprocess), summarizing one log per call, and calling `clear_context` to reset itself — infinite, token-efficient. *"You cannot do this without serious prompt engineering with an out-of-the-box agent."*

**13. Agents deploy in every form factor — and can feed each other.**
Script → REPL → stream handler → backend method → full UI. And one agent's output can be another's input: Ultra Stream's Stream agent **produces** summaries the Inspector agent **consumes**.

---

## Tier 3 — Judgment (the part most people skip)

**14. Build custom only when you need to.**
Build custom for: programmatic agents · repeat workflows · domain-specific wins · cost-down/performance-up · permission checks · staying **out of the loop**. Otherwise use out-of-the-box or lightly extended agents.

**15. Do NOT try to out-build Claude Code.**
For in-loop, generic, exploratory, or one-off work, just use Claude Code. And never try to reproduce it as a general engineering agent — *"they own agentic coding… this space is totally oversaturated."* Custom agents are a scalpel for the last mile, not a replacement for the generalist.

**16. Consistent codebase architecture is a leverage point.**
Every agent shares the same shape (`prompts/`, `agent.py`, same layout). *"It's easy for us to read, easy for our team to read, and most importantly, easy for our agents to read."* Consistency is compute you get back later.

**17. The real destination.**
*"Agentic coding is not so much about what we can do anymore. It's about what we can teach our agents to do."* Custom agents are how you teach compute your domain.

---

## Micro-quiz (self-check before the lab)

1. What two things does the Pong agent change to become a new product? *(model + system prompt)*
2. You add one custom tool; how many tools does the agent now see, and how do you fix it? *(all the built-ins are still loaded; use `disallowed_tools`)*
3. Which SDK entrypoint do custom tools require? *(`ClaudeSDKClient`)*
4. Where is `{NOTIFICATION_CRITERIA}` set and when does it change? *(system prompt, at boot; never during the run)*
5. What does the QA hook return to block a `.env` read? *(`permissionDecision: "deny"`)*
6. Why does the SDLC builder use the pure `claude_code` preset? *(engineering work → use the engineering agent; no overwrite needed)*
7. How does the Stream agent handle a file bigger than its context window? *(chunked `sed` reads + one summary per log + `clear_context`)*
8. Name one reason to build custom and one reason not to. *(build: out-of-loop/domain/permissions; don't: in-loop/generic/one-off)*

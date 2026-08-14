# AH-3 Lab Spec — Building Domain-Specific Agents

**Scope rule:** every drill runs inside the course codebase only — `agentic-horizon/building-specialized-agents` (resolve the lesson symlink `.../ah-3-building-domain-specific-agents/codebase`, or clone the lesson repo from the loot box). No external repos.
**Prime directive (graded throughout):** you never hand-edit an agent to "fix" it — you either configure it via `ClaudeAgentOptions` or, in the stretch drills, change it *through* Claude Code. You're learning to command custom agents, not to babysit them.
**Time box:** 90–150 minutes (it's an advanced, 8-agent lesson). **Token/cost note:** the CLI agents (1–5) are cheap; the UI agents (6–8) and the Social Hype firehose can burn real tokens — budget for it, and stop streams when done.
**Reading skill graded above all:** for every agent you touch, you must be able to point at its `ClaudeAgentOptions` and name how each of the **core four** (context, model, prompt, tools) is set.

---

## 0 · Setup (15 min)

1. Enter the codebase: `cd agentic-horizon/building-specialized-agents` (or your clone). Skim `README.md` — it lists all eight agents with run commands.
2. Verify the toolbelt: `uv --version`, `claude --version`, `node --version` (+ `bun --version` for the Vue frontends).
3. `cp .env.sample .env` and set `ANTHROPIC_API_KEY` (or use a Claude plan). Optional: `FIRECRAWL_API_KEY` (QA agent), `ELEVENLABS_API_KEY` (Social Hype TTS). macOS is assumed for Social Hype `osascript` alerts.
4. **SDK sanity check:** open any agent's `pyproject.toml`. Confirm the dependency reads **`claude-agent-sdk`** and the `.py` imports **`ClaudeAgentOptions`** — *not* `ClaudeCodeOptions`. (This is the recorded-vs-current rename; the video/frames say the old name.)

**Checkpoint 0:** you can state the package name (`claude-agent-sdk`) and the options class (`ClaudeAgentOptions`) without looking, and you know why the video says "Claude Code SDK."

---

## 1 · The reading drill — find the core four (20 min)

Open, in order, `custom_1_pong_agent/pong_agent.py`, `custom_2_echo_agent/echo_agent.py`, `custom_3_calc_agent/calc_agent.py`. For **each**, locate the `ClaudeAgentOptions(...)` block and fill this table (write it down):

| Agent | context (allowed/disallowed/MCP) | model | prompt (overwrite/append; any `{VAR}`) | tools (custom? which?) |
|-------|----------------------------------|-------|----------------------------------------|------------------------|

**Checkpoint 1:** your table shows Pong (no tools, Sonnet, overwrite), Echo (1 custom `echo` tool via in-memory MCP, **Haiku**, overwrite), Calc (2 custom tools, **explicit `disallowed_tools`**, Sonnet, `resume=`). You can explain why Pong uses `query()` while Echo/Calc use `ClaudeSDKClient`.

---

## 2 · Run the ladder & prove the system prompt is the law (20 min)

1. `uv run python apps/custom_1_pong_agent/pong_agent.py --prompt "summarize this codebase"` → it replies **pong**. Open `prompts/PONG_AGENT_SYSTEM_PROMPT.md` and confirm the 3-line prompt is the *only* thing defining that behavior.
2. `uv run python apps/custom_2_echo_agent/echo_agent.py "echo 'custom agents' in reverse uppercase repeat 2"` → watch the **Tool Called** block, then the transformed result.
3. `uv run python apps/custom_3_calc_agent/calc_agent.py` → ask "convert 55 fahrenheit to celsius", then "what was my last calculation?" (proves `resume=` memory). Type `quit`.

**Checkpoint 2:** you can state, in one sentence, why changing *only* the system prompt turns Claude Code into a "pong machine" — and that overwriting it means "this is not Claude Code anymore."

---

## 3 · The context experiment — allowed vs disallowed (15 min) ⭐

This is the money drill.
1. In the Echo agent, ask it: `uv run python apps/custom_2_echo_agent/echo_agent.py "list your available tools"`. Count them. You added **one** tool — how many does it list?
2. Now run the Calc agent and ask "list all your tools, names only." Count again.
3. Explain the difference by reading the two options blocks: Echo sets `allowed_tools` but **not** `disallowed_tools`; Calc sets a full `disallowed_tools` list.

**Checkpoint 3 (write it down):** *`allowed_tools` gates what can be **called**; the ~15 built-in tools are still **loaded into context** unless you **disallow** them.* State which agent proves each half of that sentence.

---

## 4 · Governance — hooks that say no (20 min)

1. Launch the QA agent: `uv run python apps/custom_5_qa_agent/qa_agent.py`.
2. Ask it: `read the .env.sample file`. Watch the **🔒 SECURITY HOOK** panel deny the read and explain why.
3. Open `qa_agent.py` → `block_env_files`. Trace the return value: `hookSpecificOutput.permissionDecision == "deny"`. Note the second hook, `log_tool_usage` (audit).
4. Run the shipped hook test: `uv run python apps/custom_5_qa_agent/test_inline_hooks.py`. Confirm it exercises the `.env` block.
5. Ask QA a real question ("how does the QA agent handle security hooks? think hard") and watch the **Thinking** block + any parallel `Task` subagents.

**Checkpoint 4:** you can explain what the hook returns to block a call, and confirm (from Dan's claim + the code) that hooks also cover **subagents**. Bonus: note that the agent gracefully fell back to WebSearch/WebFetch if you didn't rename `.mcp.json.firecrawl_6k.sample`.

---

## 5 · Agents in UIs (25 min)

Pick **at least two** of the three UI agents (do Ultra Stream — it's the flagship).

**A. Tri-Copy-Writer (one prompt → N variations).**
- Backend: `cd apps/custom_6_tri_copy_writer/backend && uv sync && uv run python main.py -v 6`
- Frontend: `cd ../frontend && npm install && npm run dev` → open http://127.0.0.1:5173
- Prompt "write a blog post title for a productivity app." Confirm **6** variations. In `backend/main.py`, find `disallowed_tools` (ALL tools off) and the `CopyResponse` **Pydantic** model; in the system prompt, find `{NUMBER_OF_VERSIONS}`.

**B. Micro SDLC (multi-agent hand-off).**
- Start backend + frontend per README; open the kanban board.
- Create a ticket, e.g. "update the HTML title and header to 'Plan, Build, Review, Ship Agents'"; drag it to **Plan** and watch it flow Plan → Build → Review → Shipped over the WebSocket log.
- In `backend/modules/agent_orchestrator.py`, confirm: **planner** = preset+`append`+write-hook to `specs/`; **builder** = *pure* `claude_code` preset (no append); **reviewer** = preset+`append`+write-hook to `reviews/`.

**C. Ultra Stream (dual producer/consumer agents).**
- `cd apps/custom_8_ultra_stream_agent && uv sync && uv run python backend/main.py --reset` (+ frontend). Watch the **Stream** agent summarize the log feed with severities and raise a HIGH alert.
- Ask the **Inspector** agent "list issues 1–3, log summary only" and "find logs for user <id>, summary only."
- In `backend/main.py`, read `read_stream_file` (note the `sed` subprocess + `raw_log_cache`) and `clear_context`.

**Checkpoint 5:** for each UI agent you ran, name the SDK surface (custom tools? disallowed all? preset+append? `resume`?) and state what problem the UI solves that a script couldn't.

---

## 6 · Judgment drill — when custom, when not (10 min)

Write two short lists from your own work:
1. Three tasks that are **custom-agent-shaped** (programmatic / repeat / domain-specific / permission-gated / out-of-loop).
2. Three tasks that should stay on the **out-of-the-box or extended** agent (in-loop / generic / prototyping / one-off).
Then pick the **one** custom-agent-shaped task you'd build first, and name which of the eight lesson agents is its closest template.

**Checkpoint 6:** your first pick is genuinely out-of-loop or domain-specific — not something Claude Code already does well in-loop.

---

## Stretch (optional, +30–45 min) — change agents *through* Claude Code

Type zero lines of application code by hand for these.
1. **Model swap:** have Claude Code change the Echo agent's model line to a current Haiku-class ID and rerun; confirm it still echoes.
2. **New tool:** have Claude Code add a third tool to the Calc agent (e.g. `custom_percentage`), register it in `create_sdk_mcp_server`, add it to `allowed_tools`, and prove it fires.
3. **Tighten governance:** extend the QA hook to also **deny** reads of `*.pem`/`*.key` (today they only warn). Test with a fake key file, then delete it.
4. **Extend, don't overwrite:** in the Micro SDLC agent, add one line to the planner's *appended* instructions and confirm via the run log that the builder (pure preset) is unaffected.
5. **Harden a tool:** replace Calc's `eval()` with an `ast`-based evaluator; verify the same conversions still work and that `import os` in an expression is rejected.

**Stretch checkpoint:** every change went through the agent or through `ClaudeAgentOptions` — you never hand-patched behavior the config should own.

---

## Pass criteria (all must hold)

- [ ] You can point at any agent's `ClaudeAgentOptions` and name how each of the **core four** is set.
- [ ] You state the SDK's real name (`claude-agent-sdk` / `ClaudeAgentOptions`) and why the video says "Claude Code SDK."
- [ ] You demonstrated the **allowed vs disallowed** context lesson from the Echo→Calc contrast (Checkpoint 3), in your own words.
- [ ] You triggered the QA `.env` **deny** hook and can explain the returned `permissionDecision` (Checkpoint 4).
- [ ] You ran ≥2 UI agents including **Ultra Stream**, and can explain how its Stream agent processes a file bigger than its context window.
- [ ] You can articulate the **extend vs overwrite** distinction using the SDLC builder (pure preset) as evidence.
- [ ] You produced your custom-vs-generalist lists and named your first build + its template agent.

---

## Instructor / self-grader notes

- The **highest-value single drill is #3** (context experiment). If a student only "gets" one thing, it must be that `disallowed_tools` — not `allowed_tools` — is what keeps the context window lean.
- Common stumble: students conflate a **system-prompt** static variable (`{NOTIFICATION_CRITERIA}`, `{NUMBER_OF_VERSIONS}`, locked at boot) with a **user-prompt** dynamic variable (`$1`/`$ARGUMENTS`). Probe for this in Part 5A.
- If Firecrawl isn't configured, the QA agent still passes (it falls back to WebSearch). Don't fail a student for the `.mcp.json.firecrawl_6k.sample` rename gotcha — flag it as the intended setup lesson.
- Watch for the anti-pattern the whole lesson warns against: a student building a custom agent for in-loop generic work. Redirect them to "just use Claude Code" — that judgment IS the lesson's finale.
- Stop the Social Hype firehose and the UI backends when done; they hold WebSocket connections and can quietly accrue tokens.

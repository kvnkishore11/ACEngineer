# AH-3 — Outdated vs Current

Course-era detail → 2026 reality, with the book treatment for each. This lesson is SDK-heavy, so the accuracy stakes are higher than a concept lesson: names and IDs *have* moved. The good news — verified against the shipped repo — is that **the codebase itself is already updated**; it's mostly the *spoken track and on-screen frames* that are period detail.

---

## 1. The SDK was renamed: "Claude Code SDK" → **Claude Agent SDK** ⭐ (biggest gap)

**What the lesson shows/says:** Dan says "Claude Code SDK" throughout, and the on-screen code (frames `t0565`, `t1040`) reads `options = ClaudeCodeOptions(...)`.

**What's true now (verified in the repo this session):** Every `pyproject.toml` depends on **`claude-agent-sdk`**, and every `.py` file imports `from claude_agent_sdk import ... ClaudeAgentOptions`. The package was renamed from `claude_code_sdk` → `claude-agent-sdk` and `ClaudeCodeOptions` → `ClaudeAgentOptions` (circa late 2025). The **migration guide is even linked** in `ai_docs/README.md` (`.../claude-code/sdk/migration-guide`).

**Book treatment:** State this up front in the chapter and normalize it in a callout: *"When Dan says 'Claude Code SDK,' read 'Claude Agent SDK.' Install `pip install claude-agent-sdk`; import `ClaudeAgentOptions`."* Use `ClaudeAgentOptions` in all book code samples (matching the repo), and add a one-line footnote on the two frames that still show `ClaudeCodeOptions` so a sharp reader isn't confused. **This is the single most important correction in the chapter.**

---

## 2. Course-era model IDs are stale

**What the lesson shows:** Pinned strings — `claude-sonnet-4-20250514` (default, 23 refs), `claude-3-5-haiku-20241022` (Echo), `claude-opus-4-1-20250805` (SDLC `AVAILABLE_MODELS`).

**What's true now:** Newer families exist with different IDs (e.g. Opus 4.x, Sonnet 5, Haiku 4.5, Fable 5). Dan future-proofs in-lesson: *"If you're operating in the future, hopefully you have something more powerful… don't let these models fool you."*

**Book treatment:** Keep the IDs as period-accurate quotes of the code, but add a "swap the model string" note and teach the **principle**, which is unchanged: Haiku-class for trivial/high-volume/latency-sensitive tools, Sonnet-class as the balanced default, Opus-class for the hardest planning/review. Never hardcode a model ID as a lesson takeaway.

---

## 3. SDK message/block shapes may drift

**What the lesson shows:** Parsing `AssistantMessage` / `ResultMessage` / `SystemMessage` and `TextBlock` / `ThinkingBlock` / `ToolUseBlock` / `ToolResultBlock`; hook payloads with `hookSpecificOutput.permissionDecision`.

**What's true now:** These are stable enough to teach, but exact field/class names can change between SDK versions. Dan pre-empts this: *"These might change in the future… The key idea is that you understand how to manage the primitives of your custom agent."*

**Book treatment:** Teach the **primitive** (options → agent → query → manage the response stream) as durable, and mark the specific class names as "current at recording; check the SDK reference." Don't build a retrieval question on an exact field name.

---

## 4. `eval()`-based math tool is a teaching simplification

**What the lesson shows:** Calc's `custom_math_evaluator` runs `eval(expr, {"__builtins__": {}}, math_funcs)` — restricted, but still `eval`.

**What's true now / better practice:** For production, prefer a real expression parser (`ast.literal_eval` or a small math grammar) to avoid `eval` risk. Dan's own framing invites it: *"you're back in deterministic world — do whatever you want, just set up the input and output properly."*

**Book treatment:** Present the code as shipped, then add a "harden this" margin note (parser instead of `eval`) as a stretch idea. Not a correction of the lesson's point — a maturation of one tool.

---

## 5. Reusable-expertise-as-prompt-files vs first-class **Agent Skills**

**What the lesson shows:** Reusable expertise encoded as `system_prompts/*.md` / `prompts/*.md` loaded by Python.

**What's true now:** Modern Claude Code also ships **Agent Skills** (`SKILL.md` with discovery + on-demand loading) as the first-class way to package reusable expertise for the *in-loop* agent.

**Book treatment:** Frame them as **complementary, not competing**: Skills package expertise for the interactive agent; the **SDK** is the right tool exactly when you need *programmatic* control — custom tools, hooks, explicit models, deployment as a script/stream/UI — which is this lesson's entire reason to exist. This is the cleanest hook for the phase-1 YouTube overlay (see below).

---

## 6. QA agent's MCP config path expects a rename (setup gotcha)

**What the lesson shows:** `qa_agent.py` calls `load_mcp_config()` looking for `.mcp.json.firecrawl_6k`.

**What's true on disk:** the shipped file is `.mcp.json.firecrawl_6k.sample`. Out of the box the config isn't found and the agent **gracefully falls back** to `WebSearch`/`WebFetch` (Dan added both "as fallbacks… if you don't have the firecrawl MCP server set up").

**Book treatment:** Call this out in the **lab** setup: to enable Firecrawl, drop the `.sample` suffix and set `FIRECRAWL_API_KEY`; otherwise the agent still works via web search. A small, real gotcha that will otherwise confuse a careful student.

---

## What has NOT aged (teach as current, verbatim)

- **The system prompt is the law** — injected before every user prompt; overwrite = new product; append = extension. Timeless.
- **The core four in code** — context/model/prompt/tools as the lens for reading and building any agent.
- **Everything costs context; `allowed_tools` gates, `disallowed_tools` unloads.** The Echo→Calc contrast is model-agnostic and permanent.
- **`query()` vs `ClaudeSDKClient`; `resume=` for continuity.** Core SDK shape.
- **Hooks for governance/permissions, covering subagents.** The security model is unchanged.
- **Extend vs overwrite; use the engineering agent for engineering.** Judgment that only gets more relevant.
- **Static vs dynamic prompt variables; workflow-in-system-prompt for domain agents.** Prompt-engineering fundamentals.
- **Form-factor freedom + producer/consumer multi-agent + token-efficient domain tools + self-managed context.** Architecture patterns, not tool trivia.
- **When to build custom (and when NOT to); don't compete with Claude Code.** The most durable part of the lesson.
- **Consistent codebase architecture as a leverage point** for humans *and* agents.

---

## Strict YouTube-overlay decision (map-to-lesson / named-gap only)

Two candidates map to *this lesson's* named gaps with zero topic drift; both `include_in_phase1 = true`, both `verify_before_publish = true` (IDs carried from the tac-1 seed list; no video was fetched, per brief — confirm each resolves and re-check the title before shipping the link):

| video_id | title | maps_to | why it's allowed |
|----------|-------|---------|------------------|
| `6fCqj4xFCZI` | How Claude Code CHANGED Engineering Forever | named hole (Gap 1) | Bridges the recording's course-era "Claude Code SDK"/`ClaudeCodeOptions` to the current **Claude Agent SDK** and programmable embedding — the chapter's single biggest correction. |
| `X2ciJedw2vU` | RAW Agentic Coding: ZERO to Agent SKILL | corrects outdated (Gap 5) | Covers **Agent Skills**, the modern first-class reusable-expertise encoding that complements the `system_prompts/*.md` pattern used throughout. |

**Deferred (do not surface on this chapter):** general multi-agent / agentic-layer videos — they belong with AH-4/AH-6, not here. Overlaying broad "codebase singularity"-style content on a build-focused lesson front-runs scale before the reader has the primitives.

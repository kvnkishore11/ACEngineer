# 09 · The Custom Agent — System Prompt, Stripped Tools, Governance Hook

"The system prompt is the most important element of your custom agents. With zero exceptions." — build one at bare metal and prove the governance works.

## The Idea

The agent evolution path is "better agents, more agents, and then custom agents." Out-of-the-box agents "are built for everyone's codebase, not yours. This mismatch can cost you hundreds of hours and millions of tokens." A custom agent is where you take the Core Four — context, model, prompt, tools — into your own hands. And the moment you overwrite the system prompt and pick the tools yourself, something changes: "this is not Claude Code anymore — you've built a new product."

Three elements carry the whole design. First, **the system prompt is the law**: "the system prompt affects every single user prompt the agent runs. All of your work is multiplied by your system prompt." The role line and the output-format rule you write here shape every response the agent will ever give. Second, **strip the tools**: "This agent cannot write. It's a QA agent. Why would it need to write anything?" Every tool in the registry "consumes space in your agent's mind" — and every tool left out is a failure mode deleted. `run_bash` sits right there in this file, tempting and dangerous, and the correct amount of it in your registry is zero. Third, **hooks**: "essential for governance, for control, for permissions in all of your agents." The registry decides *which* tools exist; the PreToolUse hook decides *when* a call is acceptable — like denying any path that escapes the workspace.

This harness has no SDK dependency on purpose. The run loop, the registry lookup, the hook gate, the transcript — that's everything an agent framework does, laid bare in 40 lines of stdlib, so you can see exactly where the Core Four live. The model is mocked; the governance is real.

## What Dan Did

In AH-3 Dan built eight custom agents on the Claude Agent SDK (`building-specialized-agents`), climbing from a Pong agent (system prompt overwritten — every prompt returns "Pong") to the **QA agent**: a codebase question-answering expert with read-only allowed tools (Task, Bash, Glob, Grep, Read) and PreToolUse/PostToolUse hooks that blocked reads of `.env` files live on camera. He parsed thinking blocks, logged every message type, and kept repeating the design question: "Always look for the system prompt and then look for the custom tools." This lesson is that QA agent's skeleton with the SDK swapped for a deterministic mock loop.

## Your Mission

Four blanks in `agent.py`:

1. **The role line** in `SYSTEM_PROMPT` — state it plainly: a read-only codebase QA agent that answers questions about `workspace/` and never modifies anything.
2. **The output-format rule** in `SYSTEM_PROMPT` — cite every workspace file path read; final line starts with `ANSWER:`.
3. **The `TOOLS` registry** — register exactly `read_file` and `list_files`. `run_bash` stays out.
4. **The hook** in `pre_tool_hook()` — resolve the target path and return `False` for anything outside `workspace/`.

Then `DOJO_MOCK=1 python3 agent.py` replays `fixtures/session.jsonl` — four scripted tool calls: an allowed read, an allowed listing, a `../../etc/passwd`-style escape, and a `run_bash` attempt. The last two must be denied, and `transcript.jsonl` is your proof.

## The Loop

```
just check 09          # or: python3 ../../dojo.py check 09
```

The check imports your definitions, probes the hook directly, runs the mock session, and reads the transcript like an auditor. Pass looks like:

```
✅ PASS — 09 custom-agent
```

## Done-when

- `SYSTEM_PROMPT` carries the read-only QA role line and the cite-paths / `ANSWER:` format rule.
- `TOOLS` registers exactly `read_file` and `list_files`; `run_bash` is not in the registry.
- `pre_tool_hook` allows workspace reads and denies any path resolving outside `workspace/`.
- `DOJO_MOCK=1 python3 agent.py` exits 0 and `transcript.jsonl` shows: two `ok` calls, the escape `denied` (blocked by hook), `run_bash` `denied` (not in registry).

## Level-up

Add a PostToolUse hook that redacts anything matching `API_KEY|SECRET|PASSWORD` from tool output before it would reach the model — then add a `max_tool_calls` budget to the loop that stops the session and logs `budget exhausted` honestly. Governance is not one gate; it's layers.

## Run It Live

Optional, never required to pass. The same agent on the real Claude Agent SDK (Python) is about ten lines — `uv add claude-agent-sdk`, export `ANTHROPIC_API_KEY`:

```python
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions
from agent import SYSTEM_PROMPT  # the law you just wrote

async def main():
    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,               # overwrite: not Claude Code anymore
        allowed_tools=["Read", "Glob", "Grep"],    # strip: read-only, like your registry
        disallowed_tools=["Write", "Edit", "Bash"],
        cwd="workspace",
    )
    async for message in query(prompt="What does app.py do?", options=options):
        print(message)

anyio.run(main)
```

Same Core Four, real model. The harness you filled in is what this SDK is doing under the hood.

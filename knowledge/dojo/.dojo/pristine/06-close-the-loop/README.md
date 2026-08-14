# 06 · Close the Loop

A PostToolUse hook is a closed loop wired straight into your agent: request → validate → resolve, with exit code 2 feeding the error back to the agent that caused it.

## The Idea

"Engineers that test with their agents win. Full stop, zero exceptions." Tactic #5 — Always Add Feedback Loops — starts from one question: "Given a unit of valuable work that's production ready, how would you, the engineer, test and validate this work? If you can answer this for every class of work and encode the answers into a command or tool call, you will fly while other engineers run."

Closing the loop means "letting your agent operate on work, calling a command or tool to get feedback on the success of the work… your agent continues to build until the feedback is positive. When you do this, you let the code write itself." Every closed-loop prompt has the same three-part anatomy: **Request → Validation → Resolution**.

A Claude Code hook is that anatomy made automatic. A `PostToolUse` hook fires after every tool call; Claude Code pipes the event payload (`tool_name`, `tool_input`, `tool_response`) to your script's stdin. Your script is the validator. Two exit codes carry the whole protocol: **exit 0** means the work passed (or was not yours to judge) — stay silent. **Exit 2** means block — everything you printed to stderr is fed *back to the agent* as feedback, and it resolves the problem itself. You never fix the file by hand; "you don't fix the issue — you fix the system that caused the issue." The hook IS the system.

## What Dan Did

In TAC-5, Dan closed loops by hand first — a prompt that told the agent to validate with `ruff check`, then three stacked validators (ruff, pytest, py_compile), then a full-stack loop with Playwright screenshots — watching the agent fix its own mistakes each time until every validator went green: "we're stacking the confidence."

In his `claude-code-hooks-mastery` repo, he moved the pattern into the harness itself: uv single-file stdlib scripts in `.claude/hooks/`, registered per event in `.claude/settings.json` (`"PostToolUse": [{"matcher": "", "hooks": [{"type": "command", "command": "uv run .claude/hooks/post_tool_use.py"}]}]`). Each hook reads the JSON payload from stdin — `json.load(sys.stdin)`, then `tool_name`, `tool_input.get('file_path')` — and decides: let it ride, or block with feedback. This lesson's validator is that exact shape, pointed at a real class of work: JSON config files under `data/`.

## Your Mission

Fill the blanks in two files:

1. `hooks/validate_json.py` — the validator:
   - extract `file_path` from the payload (it nests at `tool_input.file_path`),
   - the applicability test (only judge `.json` files under `data/` — everything else exits 0 silently),
   - the validation (require the keys `name` and `version`),
   - the two blocking exit codes (exit 2 = block + feed stderr back to the agent).
2. `settings.sample.json` — one blank: the hook event name that fires *after* a tool call completes.

The fixtures are your test bench: `fixtures/payload_good.json` and `fixtures/payload_bad.json` are realistic PostToolUse payloads pointing at `data/config_good.json` (valid) and `data/config_bad.json` (missing `version`). Real payloads carry absolute paths; the fixtures use lesson-relative paths so the check runs anywhere.

## The Loop

```
just check 06        # or: python3 ../../dojo.py check 06
```

The check literally runs your hook, piping each fixture payload to its stdin — the same closed loop Claude Code runs. Pass looks like:

```
✅ PASS — 06 close-the-loop
```

## Done-when

- Zero `____` blanks left in `hooks/validate_json.py` and `settings.sample.json`.
- Fed `fixtures/payload_good.json`, the hook exits 0 and stays silent.
- Fed `fixtures/payload_bad.json`, the hook exits 2 with an actionable message on stderr.
- Fed a payload for a non-`data/` file, the hook exits 0 — not our class of work, not our problem.
- `settings.sample.json` registers the hook under the `PostToolUse` event.
- The hook keeps its PEP 723 header — it stays a uv single-file, stdlib-only script.

## Level-up

Harden the class of work: validate that `version` is semver (`X.Y.Z`) and block on that too. Then add a second loop: a `PreToolUse` hook that blocks any edit to `.env` files before it happens (exit 2 *prevents* the tool call there), like Dan's `pre_tool_use.py` guard.

## Run It Live

Copy the hook into a scratch repo as `.claude/hooks/validate_json.py`, merge the `hooks` block from `settings.sample.json` into that repo's `.claude/settings.json`, create a `data/` directory, and boot `claude`. Ask the agent to create `data/config.json` *without* a version field — then watch the hook block, the stderr feedback land in the agent's context, and the agent fix its own file. Request → validate → resolve, with you nowhere in the loop.

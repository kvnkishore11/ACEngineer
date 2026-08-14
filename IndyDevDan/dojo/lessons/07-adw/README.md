# 07 · The AFK Developer Workflow

Deterministic code chaining agentic prompts — the ADW is the highest level of composition in the agentic layer, and it runs while you're away from the keyboard.

## The Idea

Tactic #4 is Stay Out The Loop. In-loop is you "sitting on their device, prompting back and forth." Out-loop is different: "you write high-to-low-level prompts that you pass off to your agentic pipeline, then you go AFK." The vehicle is the **ADW — the AI Developer Workflow**: "a reusable agentic workflow that combines code, agentic prompts, and agents to deliver results autonomously… the synthesis of previous-generation deterministic code and new-generation non-deterministic language models, prompt chains, and now agents." Dan's kicker: "In the future these will just be known as scripts."

Notice the split. The Python in `adw.py` is boring on purpose — routing, chaining, gating, logging. That's the R&D-era rule from your own CLAUDE.md instincts: if code can answer, code answers. The judgment calls — what to plan, how to build, how to fix — live in the prompts. The workflow chains them: plan → build → validate → resolve → report. The build step is a **higher order prompt** in action: the planner's report carries a plan path, and that path becomes the build prompt's argument. Prompts passed into prompts, like functions passed into functions.

Around the ADW sits **PITER**: **P**rompt input, **T**rigger, **E**nvironment, **R**eview. Here your prompt input is argv, your trigger is you (for now), your environment is this lesson directory, and your review is `adw_log.jsonl`. "It doesn't matter if our agent can solve every problem if we don't know that it's solved. We need to observe, we need to report, we need to log and monitor." And when a run fails: "you don't fix the issue, you fix the system that caused the issue. You fix your templates, you fix your ADW."

## What Dan Did

In TAC-4 Dan opened with the end-to-end demo: a GitHub issue ("document the ADW directory") fired a webhook, a Mac mini picked it up, an agent classified it as a chore, cut a branch, a planner agent wrote the spec, an implementer agent built it, and a PR came back — five minutes, live issue comments the whole way. Then he walked `adws/adw_plan_build.py`: fetch issue → classify → branch → planner runs `/chore`/`/bug`/`/feature` → builder runs `/implement` on the generated plan → PR. Every agent got its own prompt file — "no ad hoc prompts as strings inside of the codebase. Everything's isolated so that we can improve it."

This lesson is that ADW shrunk to its skeleton: one uv single-file script, three prompt files, a validation gate, and an honest log.

## Your Mission

Fill the blanks in `adw.py` (the prompts are already written — the Python is the exercise):

1. **`validate()`** — run the test suite via subprocess (`python3 -m unittest discover tests`) and return True only on returncode 0. The gate is binary.
2. **The chain in `main()`** — run `prompts/plan.md` first with the task, then make the HOP move: pass the parsed `PLAN_PATH` into `prompts/build.md` as its argument.
3. **The resolve gate** — if validation fails, run `prompts/resolve.md` exactly once, record the step, re-validate. One attempt, no loops, honest result.
4. **The report** — append one JSON line `{"task": ..., "steps": ..., "ok": ...}` to `adw_log.jsonl`.

`mock_outputs/` holds the canned agent reports used when `DOJO_MOCK=1`, so the loop closes offline. `tests/` is the rule of law; `DOJO_FAIL_TESTS=1` simulates a broken build so the resolve gate can be exercised.

## The Loop

```
just check 07          # or: python3 ../../dojo.py check 07
```

The check runs your ADW twice — once green, once with a simulated failing build — and reads `adw_log.jsonl` like a reviewer would. Pass looks like:

```
✅ PASS — 07 adw
```

## Done-when

- `DOJO_MOCK=1 python3 adw.py "add greeting"` exits 0.
- `adw_log.jsonl` gains exactly one record: `{"task": "add greeting", "steps": ["plan", "build", "validate"], "ok": true}`.
- With `DOJO_FAIL_TESTS=1`: the resolve step appears in the log exactly once, steps are `["plan", "build", "validate", "resolve", "validate"]`, `ok` is `false`, and the script exits nonzero. The workflow reports honestly.

## Level-up

Give the ADW a real trigger: a `watch.py` that polls a `tasks.md` file every 5 seconds and fires `adw.py` for each unchecked line (Dan's "to-done" pattern from TAC-8). Then add a retry knob: allow N resolve attempts, logged as `resolve×N` — and decide what N should be before you'd stop trusting the run.

## Run It Live

Optional, never required to pass. With Claude Code installed and authenticated, drop the mock:

```
python3 adw.py "add a --shout flag to the greeting"
```

`run_agent()` now shells out to `claude -p` with each prompt file. Watch the same chain run with real agents — and check `adw_log.jsonl` for the same honest record. That's the whole point: the workflow doesn't change, only the compute behind it does.

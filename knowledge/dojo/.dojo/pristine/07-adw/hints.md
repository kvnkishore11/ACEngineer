# Hints — 07 adw

## Hint 1

Read `run_agent()` and `parse_plan_path()` before touching a blank — the workflow is already telling you its shape. The chain order is the same one Dan named the script after: `adw_plan_build`. Plan first. And the planner's mock report (`mock_outputs/plan.txt`) ends with a `PLAN_PATH:` line — that line exists so a later step can consume it. Which step wants a plan path as its argument?

## Hint 2

Three of the blanks are file names or step names: the planner prompt is `plan.md`, the fixer prompt is `resolve.md`, and the step you append after running the fixer should say what actually happened — `"resolve"`. In `validate()`, the discover directory is just `"tests"`, and a subprocess tells you it succeeded through `proc.returncode` — the gate returns `proc.returncode == 0`.

## Hint 3

Near-answer. The HOP move: `run_agent(PROMPTS / "build.md", plan_path)` — the plan path parsed from the planner's report is the build prompt's argument. The report line:

```python
f.write(json.dumps({"task": task, "steps": steps, "ok": ok}) + "\n")
```

Keys exactly `task`, `steps`, `ok`; `ok` is the final validation result, so on the DOJO_FAIL_TESTS run it must be `false`. One JSON object, one line, appended.

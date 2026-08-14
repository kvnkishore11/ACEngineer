# CLAUDE.md

Project-specific guidance for Claude working in this repo. Read once; apply to every task.

## Rules

### Benchmarks must never auto-reset

**A `live-bench reset` call deletes ALL datapoints for a session — every chart, every hardware tag, every metric key.** It is not scoped to `chart_id`, `group_key`, or `metric_key`.

Benchmark runs are expensive (minutes to hours of real inference on local hardware, sometimes on a different machine than the dashboard). The session is shared across M4 and M5, and across multiple model variants — an M5 run appends `*_m5` chart points while the M4 run's `*_m4` points live in the same SQLite session. A reset between runs wipes the other machine's work.

**Rules for any recipe, script, or instruction that runs a real-inference benchmark:**

- Never call `live-bench reset` inside a recipe or script that also runs inference. Runs must be additive.
- The only recipes/flags allowed to call reset are explicit ones named `*-reset` (e.g. `bench-qg3-reset`) or explicit opt-in flags named `--reset` (e.g. `uv run run_all.py --reset`).
- Combined recipes (e.g. `bench-3way-m4`, `bench-3way-m5`) must NOT chain a reset. If someone wants a clean slate they call `bench-3way-reset` first, then the runner.
- When writing a new benchmark recipe, model it on `bench-qg3-m5` (additive, `bench-nuke` dep only) — not on anything that references reset.

Mock/demo fixtures in `apps/benchmarks/mock-test/` are outside this rule — they're UI smoke tests, not measurement runs.

## Stack reminders

- Backend reads `benchmarks/*.yaml` only on startup. After editing a YAML, restart the backend (`just backend` re-bind is clean because ports are freed first).
- Adding a Qwen variant requires both `ollama pull <tag>` on the bench machine AND an update to `bench-nuke` in the justfile so it unloads the new tag between phases.
- `*_m4` and `*_m5` chart IDs within one session are independent — you can run one machine without the other present. Bars for the missing hardware stay empty.

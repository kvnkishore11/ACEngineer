# AH-6 — Outdated vs Current (course-era → mid-2026)

The tactics in this capstone are durable — the agentic layer, the class/grade ladder, the ADW, the orchestrator, and "prioritize agentics" are not going stale. What ages is (a) the gap between the lesson's idealized on-screen diagrams and the actual repo, (b) specific model IDs / ports / tool counts, and (c) the fast-moving Claude Code surface (Skills, Agent SDK, permissions). Each gap below has a recommended **book treatment** so the chapter neither overclaims nor under-teaches.

---

## Gap 1 — The per-grade "example project structures" are teaching diagrams, not the repo's literal file layout

**Course-era framing.** Each grade gets a crisp on-screen "EXAMPLE PROJECT STRUCTURE": separate `bug.md` / `feature.md` / `chore.md` at Grade 5; an `adw_trigger/adw_webhook.py` at Class 2 Grade 1; `adw_modules/adw_agent_core.py`.

**Repo reality (verified).** The working `orchestrator-agent-with-adws` consolidates several rungs:
- Grade-5 templates live inside `.claude/commands/plan.md`'s `task_type (chore|feature|refactor|fix|enhancement)` switch (+ `plan_w_scouters.md`), not as separate `bug.md`/`feature.md`/`chore.md` files.
- The out-loop entry is the orchestrator's `start_adw` MCP tool + the CLI `adws/adw_triggers/adw_manual_trigger.py`, both of which write an `ai_developer_workflows` DB row and spawn a detached `uv run adw_<type>.py --adw-id` process via `adw_scripts.py`. There is no `adw_webhook.py`; a literal inbound GitHub/Slack webhook is described conceptually.

**Book treatment.** Teach the ladder as a **maturity model** and use the on-screen frames as idealized diagrams; then show the repo as *one real, consolidated instantiation* and explicitly note where a rung is consolidated. Do not print the idealized filenames as if they exist verbatim in the repo. (Flagged in `extract.json` → `current_practice_gaps[0]` and the grade-5/class-2 `codebase_note` fields.)

---

## Gap 2 — "start adw:" is illustrative chat syntax; the real trigger is a typed tool call

**Course-era framing.** The repo README shows `start adw: plan_build_review: Create a markdown preview app…` as if you type it in chat.

**Current reality (verified).** `grep -rniE "start adw:"` returns zero hits. The orchestrator LLM emits a `start_adw` **MCP tool call**; the host does not string-match chat text. This matches current Claude Code / Agent SDK practice: agents act by calling typed tools, not by the host parsing prose.

**Book treatment.** Present the orchestrator→ADW handoff as a tool call (`start_adw(name_of_adw, workflow_type, prompt, description)` → returns `adw_id`), and note the README's chat string is a human-readable illustration of the intent.

---

## Gap 3 — Skills, headless mode, and the Agent SDK have matured since recording

**Course-era framing.** Grade 3 "skills," Class 2 "core Agent SDK," and the general "programmable agent" idea.

**Current reality.** These map 1:1 to today's first-class **Agent Skills** (`SKILL.md` with frontmatter + progressive disclosure; the repo already ships `meta-skill`, `start-orchestrator`) and the **Claude Agent SDK** (Python/TypeScript) with headless flags, structured outputs, hooks, and session resume (the repo already wraps it in a typed Pydantic layer, `adws/adw_modules/adw_agent_sdk.py`). So the *concepts* are current; specific flags/APIs drift.

**Book treatment.** Note that the lesson's "skill/MCP/prime-with-tools are interchangeable, and all reducible to a prompt" insight is *more* true today. Re-verify SDK flags and Skill frontmatter fields at publish; keep the teaching at the concept level.

---

## Gap 4 — Model IDs, the orchestrator's default model, ports, and tool/table counts

**Course-era specifics (verified in-repo, ~Nov 2025 era).**
- Models: `opus = claude-opus-4-5-20251101`, `sonnet = claude-sonnet-4-5-20250929`, `haiku = claude-haiku-4-5-20251001`.
- Orchestrator default model = **opus-4-5** (`config.ORCHESTRATOR_MODEL`); the README env-var example showing `sonnet-4-5` is illustrative.
- Canonical backend port = **9403** (config.py, README, `start_be.sh`, `api.ts`). The `8002` in the app `CLAUDE.md` and the `start-orchestrator` skill is **stale**.
- Orchestrator exposes **10 tools** (not 8): the stale module docstring says 8; `create_management_tools()` actually returns 8 agent-management + `start_adw` + `check_adw`.
- **7** database tables (not 6): migration `9_ai_developer_workflows.sql` adds `ai_developer_workflows`.

**Book treatment.** Print the verified numbers (10 tools, 7 tables, port 9403, opus-4-5 default) and treat contradicting doc strings as errata. Apply Dan's standing rule for model/UI: newer families and TUIs will differ — treat specifics as period detail, tactics as current. The orchestrator's model is a one-line config change.

---

## Gap 5 — Observability, hooks, and permissions are deliberately under-emphasized in-lesson

**Course-era framing.** Dan explicitly scopes the lesson to **raw impact, not observability or security**: "logging, not observability; it's just impact… We're talking about raw capability here, not security."

**Current reality.** Production agentic layers now lean on **hooks** (pre/post tool-use gates), **permission modes**, sandboxed bash, and org/user/project settings layering. The repo ships a rich hooks/observability spine — `.claude/hooks/` (9 scripts) firing `send_event.py --source-app agent-experts` to a multi-agent observability server (`localhost:4000/events`) — but, unlike TAC-1, this `.claude/settings.json` has **no permission allowlist** (it is hooks-only). Two wiring gaps also exist: `session_start.py` is unregistered, and `PreCompact` only calls `send_event.py`.

**Book treatment.** Present observability/permissions as the deliberately-deferred "next investment" once impact is proven, and point production readers to add a permission allowlist + pre-tool-use gates. This is where a "current practice" overlay adds the most value on top of the lesson.

---

## What has NOT aged (print with confidence)

- **The agentic layer** as the central framework and highest-ROI action.
- **The class/grade ladder** as a self-location + next-step tool (the exact rung filenames are illustrative; the progression is durable).
- **The two class-jumps:** in-loop → out-loop, out-loop → orchestrated.
- **The AI Developer Workflow** = deterministic code + non-deterministic agents = the highest leverage point.
- **The orchestrator agent** as a custom lead engineer (CRUD on agents) that can also run ADWs.
- **Specialize, don't genericize** and **bundle related apps under `apps/` (git submodules)**.
- **Everything reduces to the core four**; form factor doesn't matter.
- **The codebase singularity / zero-touch engineering** as the North Star.
- The tactic recap (TAC 1–8) and the AH arc synthesis.

---

## Strict overlay decision (map-to-lesson / named-gap only)

Per the phase-1 rule, **1** YouTube overlay is marked `include_in_phase1: true`:

- ✅ **`fop_yxV-mPo` — "Codebase Singularity"** — maps 1:1 to this lesson's central concept; AH-6 is where the singularity becomes buildable. *Verify the ID resolves before publishing.*

Deferred (listed, not phase-1):
- **`hGg3nWp7afg` — "3 Codebase Folders"** — structural companion (application/agentic split, `apps/` bundling). *Verify ID.*
- **(topic slot, ID null)** — a public "AI Developer Workflows / out-loop agents" video would reinforce Class 2; no verified ID from a seed list, so left null rather than fabricated. Populate + verify before publishing.

No seed ID list was provided in this brief, so IDs are proposed conservatively and all are flagged `verify: true`. Do not publish overlay links until the IDs are confirmed.

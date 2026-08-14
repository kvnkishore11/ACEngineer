# IndyDevDan (disler) Repo Distillate

Source: 24 disler repos + 1 gist cloned at `youtube/_repos/` (all unshallowed to full history), plus the `agent-experts` course codebase (recovered from git history of the AgenticEngineer repo — its working-tree copy is currently deleted). `pvolok__mprocs` is third-party (the terminal multiplexer Dan uses in `just serve` recipes) and is excluded from the catalog.

A note on Dan's git style: he ships whole ideas per commit and labels them `🚀` (initial drop) or `progress`. Repos are video artifacts — the initial commit usually contains the entire working system, and later commits are README/demo polish plus occasional real feature drops with meaningful messages (`UserPromptSubmit`, `subagents`, `genui`, `HIL + Haiku 4.5 Enhancements + Swim Lanes`, `pi 2 pi coms and net coms`). Where history is one commit, the rebuild paths in Part 3 decompose the system's internal structure instead.

---

# Part 1: Repo catalog

*(chronological by first commit)*

**infinite-agentic-loop** — Two-prompt system: a `/project:infinite <spec> <out_dir> <count>` slash command orchestrates waves of parallel sub-agents that generate evolving, unique UI-component iterations from a spec file. The command does spec analysis → directory reconnaissance → parallel sub-agent deployment → wave management. Tech: pure Claude Code (commands + specs + settings.json permissions), generated HTML/CSS/JS. 18 commits, 122 files, 2025-06-06 → 2026-03-09. Signature ideas: (1) spec-driven generation with versioned specs (`invent_new_ui.md` v1→v4), (2) slash command as orchestrator with `$ARGUMENTS`, (3) parallel sub-agent batching + "infinite mode" waves with progressive sophistication, (4) directory reconnaissance so agents never duplicate prior output, (5) `ai_docs/` primed context.

**claude-code-hooks-mastery** — The canonical hooks reference: all 13 Claude Code lifecycle hooks implemented as uv single-file Python scripts, plus sub-agents (including the meta-agent that writes new agents), 8 output styles, 9 status-line versions, and a builder/validator team. Tech: Python + uv, ElevenLabs/OpenAI/pyttsx3 TTS fallback chain, Anthropic/OpenAI/Ollama LLM utils. 10 commits, 130 files, 2025-07-02 → 2026-02-01. Signature ideas: (1) hook exit-code flow control (0 allow / 2 block / JSON), (2) uv single-file scripts with inline deps for zero-setup hooks, (3) meta-agent (agent that generates agents), (4) model-tier agent variants (crypto analyzer in haiku/sonnet/opus), (5) output styles + status lines as personality/observability layers.

**claude-code-hooks-multi-agent-observability** — Real-time monitoring for Claude Code agents: every hook POSTs JSON via `send_event.py` to a Bun server that persists to SQLite and broadcasts over WebSocket to a Vue 3 client with filtering, swim lanes, and theming. Tech: Python uv hooks, Bun + TypeScript, SQLite, Vue 3. 16 commits, 171 files, 2025-07-10 → 2026-02-08. Signature ideas: (1) hooks as a telemetry bus (`--source-app` + `session_id` identifies each agent), (2) event summarization with a cheap model (Haiku) before display, (3) human-in-the-loop (HIL) hooks, (4) swim-lane multi-agent comparison, (5) `apps/demo-cc-agent` as a self-test agent.

**nano-agent** — An MCP server wrapping a minimal internal agent loop (OpenAI SDK abstraction over GPT-5, Claude, and local Ollama models) so Claude Code can delegate the same task to 9 models in parallel and grade them on performance/speed/cost. Tech: Python + uv, MCP, typer CLI (`nano-cli`), Ollama. 7 commits, 92 files, 2025-08-08 → 2025-08-10. Signature ideas: (1) HOP/LOP — Higher Order Prompt orchestrating Lower Order Prompt evals (`.claude/commands/perf/`), (2) per-model sub-agent wrappers in `.claude/agents/`, (3) the perf/speed/cost "trade-off trifecta" with committed eval-result grades, (4) building an agent from scratch (loop + tools + provider abstraction), (5) agents-as-MCP-tools.

**agentic-drop-zones** — Directory-watching automation: drop a file into a zone and a configured agent (Claude Code, Gemini CLI) fires with a prompt template against it. Tech: single-file uv Python script (`sfs_agentic_drop_zone.py`, watchdog + rich streaming), `drops.yaml` config. 8 commits, 28 files, 2025-08-28 → 2025-08-31. Signature ideas: (1) "sfs" single-file-script architecture, (2) declarative zones in YAML (pattern, prompt, agent, model, MCP config per zone), (3) reusable prompts in `.claude/commands/` doubling as templates with `FILE_PATH` substitution, (4) `bypassPermissions` full autonomy with explicit risk acknowledgment, (5) agent-agnostic dispatch.

**big-3-super-agent** — A voice-controlled super-agent: OpenAI Realtime API orchestrates Claude Code coding agents and Gemini computer-use browser agents via tools (`create_agent`, `command_agent`, `list_agents`, `browser_use`). Tech: single-file Python (`big_three_realtime_agents.py`), Playwright, plus a full hooks/output-styles/status-lines stack. 1 commit, 104 files, 2025-10-10. Signature ideas: (1) voice as orchestration layer, (2) agent registry with resumable sessions on disk, (3) cross-provider trio (OpenAI + Anthropic + Google), (4) `apps/content-gen` as the agents' working directory, (5) status-line versions v1→v4 evolution.

**beyond-mcp** — One domain (Kalshi prediction-market data) implemented four ways — MCP server, CLI, file-system scripts, and a skill — to expose the real trade-offs (context cost, discoverability, reusability) of each agent-tool interface. Tech: Python + uv per app. 1 commit, 51 files, 2025-11-09. Signature ideas: (1) numbered `apps/1_mcp_server` … `apps/4_skill` comparison layout, (2) "MCP's cost is instant context loss", (3) `/prime_*` commands per approach instead of always-loaded tools, (4) uv single-file scripts as agent tools, (5) same-prompt benchmarking across interfaces.

**agent-sandboxes** — E2B sandbox exploration monorepo: 13 numbered fundamentals scripts, a Click CLI, an MCP wrapper, "obox" parallel agent-fork workflows, and Claude Code running *inside* a sandbox ("ibox"). Tech: Python + uv, E2B SDK, MCP. 1 commit, 79 files, 2025-11-16. Signature ideas: (1) Isolation/Scale/Agency value framing, (2) atoms-to-workflow learning ladder (fundamentals → CLI → MCP → workflows), (3) numbered example scripts `01_…13_`, (4) agent forks — N isolated copies of the same task, (5) full autonomy justified by isolation.

**agent-sandbox-skill** — The productized version of agent-sandboxes: one portable skill (`.claude/skills/agent-sandboxes/`) with an embedded `sandbox_cli` uv app, prompts (`sandbox`, `plan-build-host-test`, `host`, `browse`…), cookbook, and examples; works in Claude Code, Gemini CLI, and Codex. 2 commits, 129 files, 2025-11-22 → 2025-11-29. Signature ideas: (1) skill-with-embedded-CLI (skill ships its own tooling), (2) cross-agent portability via CLAUDE.md + AGENTS.md + GEMINI.md, (3) `\prompt` nested-prompt dispatch convention in CLAUDE.md, (4) difficulty-graded starter prompts per agent, (5) Playwright browser validation inside the sandbox (2nd commit: "browser tools").

**fork-repository-skill** (Fork Terminal Skill) — A skill that spawns new terminal windows running Claude Code, Codex, Gemini, or raw CLI commands, optionally handing off conversation context via a summary. Tech: Python tool + osascript, SKILL.md + cookbook per tool. 1 commit, 13 files, 2025-12-07. Signature ideas: (1) forking as delegation/parallelization primitive, (2) cookbook progressive disclosure (one md per target tool), (3) model modifiers ("fast"/"heavy") mapping to model tiers, (4) context handoff prompt template.

**claude-code-damage-control** — Defense-in-depth PreToolUse hooks for Bash/Edit/Write driven by `patterns.yaml` with three protection levels (zeroAccessPaths, readOnlyPaths, noDeletePaths), shipped as a skill with interactive install/modify cookbooks. Tech: parallel Python and TypeScript hook implementations. 1 commit, 34 files, 2026-01-04. Signature ideas: (1) exit-code contract (0 allow / 2 block / JSON ask), (2) config-not-code security (patterns.yaml), (3) `sentient*.md` adversarial test prompts to attack your own guardrails, (4) AskUserQuestion-guided install workflows, (5) dual-language implementation as a porting lesson.

**agentic-finance-review** — "Specialized Self-Validating Agents": a multi-agent pipeline (normalize → categorize → merge → accumulate → graph → dashboard) over bank CSVs, where each sub-agent carries its own embedded validation hooks running deterministic Python validators. 2 commits, 92 files, 2026-01-18. Signature ideas: (1) hooks embedded in prompts/subagents/skills instead of global settings.json, (2) `Focused Agent + Specialized Validation = Trusted Automation`, (3) deterministic validator scripts (`csv-validator.py`, `html-validator.py`, ruff/ty validators), (4) orchestrator command (`/review-finances`) fanning out to stage agents, (5) mock input data for reproducible demos.

**install-and-maintain** — The "living document that executes" pattern: one deterministic setup script exposed three ways — SessionStart hook flags (`claude --init`), agentic prompts (`/install`, `/maintenance`), and interactive prompts (`/install true` with AskUserQuestion). Tech: Python uv hooks, justfile (`cldi`/`cldii`/`cldit`). 1 commit, 33 files, 2026-01-25. Signature ideas: (1) deterministic/agentic/interactive ladder, (2) script as single source of truth, hooks and prompts both call it, (3) CI-friendly `--init-only`, (4) agents+code beats agents or code alone.

**claude-code-hooks-mastery gist** (`gist__disler__c7719b79a107`) — Single file: the `observable-tools-diffs-tts` output style shared as a gist; the distribution vehicle for one of the output styles from hooks-mastery/big-3.

**bowser** — Agentic browser automation and UI testing built as a four-layer composable stack: Skill (claude-bowser via Chrome MCP, playwright-bowser via playwright-cli) → Subagent (parallel isolated sessions, QA agent) → Command (`/ui-review`, `/bowser:hop-automate`) → justfile recipes. 3 commits, 30 files, 2026-02-15 → 2026-02-22. Signature ideas: (1) "enter at any layer" composability, (2) headed (observable) vs headless duality, (3) YAML user stories driving parallel QA fan-out into `ai_review/`, (4) a `just` skill teaching the agent the task runner itself.

**pi-vs-claude-code** — A playground of ~19 TypeScript extensions for the Pi coding agent that rebuild (and extend) Claude Code's feature set: custom footers/widgets/themes, subagent spawning, agent teams, sequential agent chains, damage control, purpose gates, and pi-to-pi communications over unix sockets and a networked HTTP/SSE hub. Tech: Bun, TypeScript, pi extension API. 8 commits, 82 files, 2026-02-22 → 2026-07-10. Signature ideas: (1) harness hacking — owning the agent runtime, (2) agent-to-agent comms (`coms`, `coms-net`), (3) `cross-agent.ts` reusing `.claude/`/`.gemini/`/`.codex/` assets in Pi, (4) damage-control with "continue" variant (blocked calls return feedback instead of aborting), (5) hedging against vendor lock-in.

**mac-mini-agent** — macOS computer-use toolkit: Steer (Swift CLI: screenshots, OCR, click, type, hotkeys, windows) + Drive (Python tmux orchestration CLI) + listen (voice), each wrapped as a skill so agents can operate the machine. 4 commits, 87 files, 2026-03-08 → 2026-03-09. Signature ideas: (1) OCR as the equalizer for Electron apps with empty accessibility trees, (2) skills wrapping native CLIs, (3) spec-then-build within history (`specs/process_control.md` lands with the `process control` commit), (4) deploy agents to dedicated hardware.

**the-library** — A pure-agent meta-skill for private distribution of agentics: `library.yaml` catalogs skills/agents/prompts by local path or GitHub URL with typed dependencies (`skill:`, `agent:`, `prompt:`); cookbook instructions teach the agent to list/pull/sync. No code, no CLI — "the agent IS the runtime." 1 commit, 20 files, 2026-03-15. Signature ideas: (1) package.json-for-agentics, (2) pointers-not-copies with on-demand pull, (3) typed dependency resolution, (4) markdown-only application, (5) private-first distribution.

**live-bench** — LAN-only live benchmarking platform for local models: YAML-defined benchmarks, a `live-bench` CLI POSTing `(group, metric, value)` datapoints, FastAPI backend + SQLite, Vue 3 dashboard animating bars over SSE. Built for the M4 vs M5 / MLX vs GGUF video. 1 commit, 179 files, 2026-04-19. Signature ideas: (1) charts-as-YAML, model-agnostic ingest, (2) CLAUDE.md encoding hard operational rules ("benchmarks must never auto-reset"), (3) embedded `drive` skill for tmux orchestration of bench machines, (4) wall-clock over tokens/sec, (5) `/install` agentic onboarding.

**max-your-cc-sub** — An educational repo answering "can I use my Claude subscription instead of an API key?" with a green/gray/red usage-tier framework and runnable scripts that diff OAuth vs API-key auth signals. 1 commit, 13 files, 2026-04-26. Signature ideas: (1) policy-as-repo (runnable compliance demo), (2) `just oauth / just api / just compare`, (3) interactive `/install` command.

**the-verifier-agent** — Two-agent observer system on Pi: an interactive Builder plus an input-locked Verifier in its own tmux window that re-verifies every builder turn with read-only tools, prompting corrections back via a single `verifier_prompt` tool (max 3 loops, then human escalation). 1 commit, 55 files, 2026-05-03. Signature ideas: (1) verification as first-class (not human-in-the-loop), (2) un-promptable agents — fixes must be templated into personas, (3) top-down observer via unix socket + session JSONL, (4) read-only tool surface / bash pinned to allowlisted scripts, (5) "spend tokens to save time."

**bash-damage-from-within** — Five runnable security levels around the bash tool — safe-mode skill, `--append-system-prompt`, blacklist hook, whitelist hook, no-bash-custom-tools-only — implemented side-by-side for Claude Code and Pi, each attacked with the same catalog against a fake `target/` production directory. 1 commit, 64 files, 2026-05-10. Signature ideas: (1) the security ladder (L1/L2 trust the model, L3 imagination, L4 discipline, L5 only what you built), (2) attack-prompts as test suite, (3) target-template reset harness, (4) dual-harness parity, (5) `/install` + justfile bootstrapping.

**pi-agent-observability** — The observability system rebuilt for Pi: a drop-in extension streams lifecycle events to a Bun+SQLite server with three views (single, swimlane, race), validated by a real "Steelman" product agent, plus four spec-format skills (`/spec`, `/htmlspec`, `/htmlvspec`, `/vspec`) to A/B plan formats under measurement. 1 commit, 70 files, 2026-05-31. Signature ideas: (1) measure the perf/speed/cost trifecta, (2) race view (who finished which step first), (3) spec-format A/B testing, (4) product agent as telemetry proof, (5) extension-based (zero agent changes) instrumentation.

**planf3** — A Mythos-class planning meta-skill: `/planf3 "<prompt>"` emits a single self-contained HTML plan into `specs/` from a rigid template (`{{PLACEHOLDER}}` + `<!-- repeat -->` blocks) with one gpt-image-2 diagram per section, plus workflows to build from and update plans. 1 commit, 31 files, 2026-06-21. Signature ideas: (1) templated engineering — you encode *how you engineer* once, (2) plans as living artifacts (append-only metadata: commits, sessions, references), (3) HTML-first specs (spend tokens/cost for performance), (4) meta-skill = skill that produces artifacts, (5) `questionable` flag surfacing assumptions as Q&A.

**learning-cmux-with-agents** — 31 natural-language prompts proving an orchestrator agent can stand up, prompt, observe, and tear down a fleet of agents inside cmux (native macOS terminal) via its CLI/socket; includes a lead/plan/build-fe/build-be/test agent team, a `/spawn-fs-team` command, a demo app, and a self-contained visual guide. 1 commit, 169 files, 2026-06-29. Signature ideas: (1) prompts/ as the product, (2) four-verb control loop over addressable terminal surfaces, (3) 3-tier agent teams with visual identity per pane, (4) layouts-as-code declarative team boot, (5) single-page HTML guide (`just guide`).

**agent-experts** (Agentic Horizon course codebase, `AgenticEngineer/agent-experts/` in git history) — "Agents that actually learn": the ACT → LEARN → REUSE pattern where each domain expert owns an `expertise.yaml` mental model plus `question.md` / `plan.md` / `self-improve.md` / `plan_build_improve.md` prompts under `.claude/commands/experts/<domain>/`; includes orchestrator apps (`orchestrator_3_stream` with a Claude-Agent-SDK autocomplete expert) and the Nile adaptive-shopping product-expert demo. Signature ideas: (1) expertise files as agent working memory (code stays the source of truth), (2) self-improve prompts that sync the mental model against the codebase until stable, (3) codebase experts vs product experts, (4) scout/planner/build sub-agents + full hooks stack, (5) composite prompt chains (plan → build → self-improve).

---

# Part 2: Recurring patterns across repos

1. **`/prime` context-priming command** — `.claude/commands/prime.md` (read README, `git ls-files`, key dirs; report understanding) exists in virtually every repo; variants `prime_cc`, `prime_obox`, `prime_kalshi_cli_tools`, `prime_tts`. Shown in: all 24 disler repos + agent-experts. Dan never lets an agent start cold.

2. **uv single-file Python scripts (PEP 723 inline deps)** — every hook, validator, and tool is a standalone `uv run`-able script; whole apps ship as one file (`sfs_agentic_drop_zone.py`, `big_three_realtime_agents.py`). Repos: hooks-mastery, observability, drop-zones, nano-agent, big-3, finance-review, install-and-maintain, agent-experts.

3. **The copied hooks stack** — `pre_tool_use.py`, `post_tool_use.py`, `stop.py`, `notification.py`, `subagent_stop.py`, `user_prompt_submit.py` + `utils/llm/{anth,oai,ollama}.py` + `utils/tts/{elevenlabs,openai,pyttsx3}.py` with graceful fallback chains, logging every payload to `logs/*.json`. Repos: hooks-mastery, observability, nano-agent, big-3, agent-experts (near-identical files — the stack is a portable artifact).

4. **`send_event.py` observability bus** — hooks POST summarized events (`--source-app X --event-type Y --summarize`) to a local server; SQLite + WebSocket/SSE + Vue dashboard. Repos: observability, nano-agent, big-3, agent-experts; rebuilt for Pi in pi-agent-observability.

5. **`apps/` monorepo layout** — every runnable codebase lives at `apps/<name>` with its own `pyproject.toml`/`package.json`; the repo root is the agentic layer (.claude, specs, ai_docs, justfile). Repos: nano-agent, observability, big-3, agent-sandboxes, beyond-mcp, live-bench, pi-agent-observability, the-verifier-agent, finance-review, install-and-maintain, damage-control, mac-mini-agent, agent-experts.

6. **`ai_docs/` curated third-party documentation** — scraped/condensed docs (Claude Code hooks, agent SDK, E2B, OpenAI Realtime) checked into the repo for context loading via `/load_ai_docs`, often maintained by a `docs-scraper` sub-agent. Repos: infinite-loop, hooks-mastery, observability, nano-agent, drop-zones, agent-sandboxes, beyond-mcp, damage-control, install-and-maintain, the-verifier-agent, big-3, learning-cmux, agent-experts.

7. **`specs/` plan-first directory** — plans/specs as markdown (later HTML) that drive generation; "great planning is great engineering." Repos: infinite-loop (versioned specs v1→v4), nano-agent, agent-sandboxes, bowser, live-bench, mac-mini-agent (spec lands in same commit as feature), pi-agent-observability, planf3 (the spec system itself), hooks-mastery, observability.

8. **justfile as the launch pad + agentic `/install`** — `just` recipes for humans, agents, and CI; an `/install` slash command (`.claude/commands/install.md`) does toolchain checks and setup interactively. Repos: bowser, live-bench, verifier, pi-agent-observability, bash-damage, max-your-cc-sub, install-and-maintain (the pattern's own repo), learning-cmux, pi-vs-cc, observability, the-library, mac-mini-agent. mprocs appears inside `just serve` recipes.

9. **HOP/LOP — higher-order prompts orchestrating lower-order prompts** — one orchestrator prompt fans out to N parameterized worker prompts and aggregates results. Repos: nano-agent (`perf/hop_evaluate_nano_agents.md` over 5 LOP evals), infinite-loop (`/infinite` over spec), bowser (`hop-automate` over saved workflows), finance-review (`/review-finances` over stage agents), agent-experts (`plan_build_improve` chains).

10. **Skills that ship their own tooling** — SKILL.md + `cookbook/` (per-scenario workflows) + `prompts/` + an embedded CLI/app/scripts dir; progressive disclosure so the agent only reads what it needs. Repos: agent-sandbox-skill (embedded sandbox_cli), damage-control (hooks in 2 languages + cookbook + test-prompts), fork-terminal, live-bench & mac-mini-agent (`drive`, `steer`), planf3 (workflows + image scripts), the-library (cookbook only — pure agent), bowser (3 skills incl. a `just` skill).

11. **Meta-agents and meta-skills** — things that generate the things: `meta-agent.md` (writes new sub-agents; hooks-mastery, observability), planf3 (writes plans), the-library (manages skills), `pi-pi` extension (builds Pi agents), agent-experts `meta_prompt.md`.

12. **Model-tier variants of the same agent** — identical prompt at haiku/sonnet/opus (crypto agents in hooks-mastery), 9 per-model nano-agent wrappers, fork-terminal "fast"/"heavy" modifiers, fetch-docs-haiku45 vs -sonnet45 (observability). Always framed as the performance/speed/cost trade-off trifecta.

13. **The safety ladder / autonomy-isolation matching** — full `bypassPermissions` only inside sandboxes or watched zones; otherwise deterministic guardrails: blacklist → whitelist → no-bash custom tools; adversarial "sentient" attack prompts test the guardrails. Repos: drop-zones, agent-sandboxes, damage-control, bash-damage-from-within, verifier, pi-vs-cc (damage-control ext), big-3.

14. **Deterministic validation closes the loop** — agents validate their own work with scripts, not vibes: validator hooks per agent (finance-review), a whole verifier agent, `test-prompts/`, eval_results committed to the repo (nano-agent), QA stories → `ai_review/` reports (bowser).

15. **Cross-agent portability** — CLAUDE.md + AGENTS.md + GEMINI.md triplets; `.mcp.json.sample` + `.gemini/settings.json.sample`; Pi's `cross-agent.ts` reading `.claude/.gemini/.codex` dirs; agent-agnostic dispatch in drop-zones. Dan builds for the category, not one vendor.

16. **TTS + personalization everywhere** — completion announcements, "your agent needs your input", `ENGINEER_NAME` env var injected into hooks for personalized speech; TTS fallback chain ElevenLabs → OpenAI → pyttsx3. Repos: hooks-mastery, observability, big-3, nano-agent, agent-experts, gist output style.

17. **Output styles + status lines as an observability UI** — versioned status lines (`status_line.py` … `status_line_v9.py`) and a portable set of output styles (genui, tts-summary, table-based, yaml-structured, observable-tools-diffs-tts). Repos: hooks-mastery, big-3, observability, bash-damage (minimal.py), pi-vs-cc, verifier.

18. **README as video companion** — one-line hook + blockquote, YouTube link in the first 5 lines, hero image in `images/`, mermaid/GIF architecture diagram, value-prop triad (e.g. Isolation/Scale/Agency), Quick Start with copy-paste blocks, and a "Master AI Coding" footer linking Principled AI Coding / agenticengineer.com / the channel.

19. **Team agent patterns** — builder + validator team dirs (`.claude/agents/team/`), `plan_w_team.md` command, lead/worker 3-tier cmux teams, dispatcher-only `agent-team` extension, two-agent verifier. Repos: hooks-mastery, observability, pi-vs-cc, learning-cmux, verifier, live-bench (`plan-w-team`).

20. **Emoji/terse commit style** — `🚀` initial commit containing the entire working system, `progress` for iteration, meaningful messages reserved for real feature drops. Every repo; a byproduct of building in public for video.

---

# Part 3: Rebuild-worthy repos

Selection criteria: density of transferable patterns, real commit history to follow, and how much of Dan's stack the rebuild forces you to internalize.

## 1. claude-code-hooks-mastery (10 commits, 2025-07 → 2026-02)

**Why it teaches the most:** This is the foundation layer every other repo copies from — the hooks stack, TTS/LLM utils, sub-agents, meta-agent, output styles, and status lines all originate or mature here. It also has the cleanest real history: each commit is a named capability.

**Rebuild path:**
- **M1 — Core hooks + flow control** (`🚀`, 2025-07-02): `.claude/settings.json` wiring `pre_tool_use.py`, `post_tool_use.py`, `stop.py`, `notification.py`, `subagent_stop.py` as uv single-file scripts; block `rm -rf` and `.env` reads in PreToolUse; log every payload to `logs/`; add `utils/tts/` (elevenlabs → openai → pyttsx3 fallback) and `utils/llm/{anth,oai}.py`; commands `prime.md`, `all_tools.md`, `git_status.md`, `sentient.md`. *Learn: hook payloads, exit-code contract (0/2/JSON), uv inline deps, deterministic control over a nondeterministic agent.*
- **M2 — Prompt-level control** (`UserPromptSubmit`, 2025-07-18): add `user_prompt_submit.py` for validation/context injection; document payloads in `ai_docs/`. *Learn: intercepting before the model even sees the prompt.*
- **M3 — Sub-agents + the meta-agent** (`subagents`, 2025-07-27): `.claude/agents/` with hello-world, work-completion-summary (TTS), research agents, crypto analyzers, and `meta-agent.md` that generates new agent files from a description. *Learn: agent frontmatter (tools, model, description-driven delegation), agents that build agents.*
- **M4 — Lifecycle completeness** (`add PreCompact and SessionStart`, 2025-07-29): cover session boundaries; inject dev context at SessionStart. *Learn: the full 13-event lifecycle map.*
- **M5 — Model-tier engineering** (`ccmodels`, 2025-08-03): restructure crypto agents into `crypto/*-{haiku,sonnet,opus}.md` variants. *Learn: the performance/speed/cost trifecta as a file-naming discipline.*
- **M6 — Output styles + status lines + local LLMs** (`genui`, 2025-08-17): 8 output styles including genui (HTML-generating) and tts-summary; `status_line_v1→v9` pulling session data; `utils/llm/ollama.py`. *Learn: response formatting as a programmable layer; local-model fallbacks.*
- **M7 — Teams + new hooks** (`Update Hooks`, 2026-02-01): `permission_request.py`, `subagent_start.py`, `post_tool_use_failure.py`, `session_end.py`, `setup.py`; `agents/team/{builder,validator}.md`, `plan.md`/`build.md`/`plan_w_team.md` commands; `tts_queue.py`. *Learn: builder/validator team orchestration, failure-path hooks.*

**Done when:** every one of the 13 hooks logs its JSON payload; a dangerous `rm -rf` is blocked with exit 2; `/plan_w_team` runs builder then validator; the meta-agent generates a working new agent file; TTS announces completion with your name.

## 2. claude-code-hooks-multi-agent-observability (16 commits, 2025-07 → 2026-02)

**Why:** Takes M1's hooks and turns them into a product — the single best full-stack exercise in the catalog (Python hooks → Bun/SQLite server → WebSocket → Vue client), and the direct ancestor of pi-agent-observability.

**Rebuild path:**
- **M1 — Event pipeline end-to-end** (`🚀`, 2025-07-10): hooks + `send_event.py` (HTTP POST with `--source-app`/`--event-type`), Bun server with SQLite insert + WebSocket broadcast, minimal Vue client with live event rows; `apps/demo-cc-agent` to generate traffic. *Learn: hooks as telemetry, `source_app:session_id` agent identity (per CLAUDE.md).*
- **M2 — Visualization polish** (six `progress` commits, 2025-07-13): filtering, emoji per event type, pulse charts, README arch diagrams. *Learn: making event streams legible.*
- **M3 — Prompt observability** (`add UserPromptSubmit`, 2025-07-18): new hook + client rendering of prompts; `.claude/commands/start.md` (2025-07-19) to boot the system. *Learn: extending a live schema across all four layers.*
- **M4 — Session lifecycle + SDK docs** (`QOL Improvements`, 2025-10-10): `session_start.py`, `session_end.py`, `pre_compact.py`; swap in `claude_agent_sdk_python.md` ai_docs; client App.vue upgrades. *Learn: keeping an agentic repo current as the platform evolves.*
- **M5 — HIL + swim lanes** (`HIL + Haiku 4.5 Enhancements + Swim Lanes`, 2025-10-19): human-in-the-loop example hooks (`hitl_example.py`, `test_hitl.py`), Haiku-4.5 summarization in `send_event.py`, swim-lane view comparing agents, bench commands. *Learn: pausing agents for human decisions; cheap-model summarization at the edge.*
- **M6 — Agentic layer maturity** (`Add multi-agent observability system with hooks, agents, and skills…`, 2025-10-26): meta-agent, scout-report-suggest agents, worktree commands + skills, output styles, client filtering/theming. *Learn: the repo eating its own dogfood — agents maintaining the observability repo.*
- **M7 — Task/team era** (`update for task/team tools & new hooks`, 2026-02-08): team builder/validator agents, `plan_w_team.md`, `permission_request.py` + `post_tool_use_failure.py` events flowing to the dashboard. *Learn: observing multi-agent teams, not just single sessions.*

**Done when:** two projects with different `--source-app` values stream simultaneously into one dashboard; events are summarized; swim lanes show a team run; killing the server never breaks the agent (hooks fail silent).

## 3. infinite-agentic-loop (18 commits, 2025-06)

**Why:** The purest lesson in spec-driven parallel sub-agent orchestration — the whole system is two markdown files. Its history is a visible iteration loop on a spec (v1 → v4) — you literally watch Dan learn what makes agent-facing specs work.

**Rebuild path:**
- **M1 — The command** (`progress`, 2025-06-06, adds `.claude/commands/infinite.md` + `ai_docs/claude_code_fresh_tutorials.md`): write the orchestrator prompt: parse `$ARGUMENTS` (spec, out_dir, count), analyze spec, reconnoiter directory, deploy sub-agents. *Learn: slash commands as programs; args parsing in prompts.*
- **M2 — First spec + first outputs** (`progress` ×2: `specs/invent_new_ui.md`, `src/ui_innovation_1..10.html`): single and small-batch runs. *Learn: uniqueness via directory reconnaissance.*
- **M3 — Spec iteration** (`progress`: `invent_new_ui_v2.md` + `src_enhanced/`; then `invent_new_ui_v3.md` + `themed_hybrids/`): tighten naming patterns, design dimensions, quality bars; `broader` commit widens v3. *Learn: the spec is the product — output quality tracks spec quality, not prompt cleverness.*
- **M4 — Repo hygiene + permissions** (`progress` commits 2025-06-07: `prime.md`, `.claude/settings.json`, move old outputs to `legacy/`): permission allowlists for Write/Edit/Bash. *Learn: settings.json permissioning for autonomous loops.*
- **M5 — Scale run + README** (`progress`: README + `src/ui_hybrid_10..18+`): 20-iteration batched waves; infinite mode until context exhaustion. *Learn: wave management and progressive sophistication under a finite context budget.*
- **M6 — Multi-file generations** (`progress`, 2025-06-10: `specs/invent_new_ui_v4.md` + `src_group/ui_hybrid_N/{index.html,script.js,styles.css}`): upgrade the spec so each agent emits a file *set*. *Learn: structuring specs for compound artifacts.*

**Done when:** `/infinite specs/your_spec.md out 5` yields 5 genuinely distinct spec-compliant artifacts with correct sequential naming, and infinite mode runs at least two waves with rising sophistication.

## 4. nano-agent (7 commits, 2025-08)

**Why:** The only repo where you build the agent itself — loop, tools, provider abstraction — then expose it through MCP and evaluate models scientifically. Demystifies what Claude Code is under the hood.

**Rebuild path** (initial `🚀` contains the system; decompose it):
- **M1 — Agent core:** typed file-system tools + an OpenAI-SDK agent loop in `apps/nano_agent_mcp_server` (modules: tools, agent, provider config). *Learn: the tool-call loop that all agents share.*
- **M2 — Provider abstraction:** route `gpt-5*` / `claude-*` / `gpt-oss:*` (Ollama) through one interface. *Learn: OpenAI-compat as lingua franca; local models as first-class.*
- **M3 — CLI:** `nano-cli run "<prompt>" --model X --provider Y`, `test-tools`. *Learn: testing the agent without any MCP client.*
- **M4 — MCP server:** expose `prompt_nano_agent` via MCP; `.mcp.json.sample`; `uv tool install`. *Learn: agents-as-MCP-tools; delegation from Claude Code.*
- **M5 — Per-model sub-agent wrappers:** `.claude/agents/nano-agent-{gpt-5,gpt-5-mini,claude-opus-4-1,gpt-oss-20b,…}.md` all calling the same MCP tool with a pinned model. *Learn: fan-out parallelism via sub-agents.*
- **M6 — LOP evals:** `.claude/commands/perf/lop_eval_1__dummy_test.md` … `5__complex_engineering_test.md` with expected outputs and grading rubrics. *Learn: writing evaluations as prompts.*
- **M7 — HOP + results** (`progress` commits 2025-08-10 = eval runs + README + eval GIFs): `hop_evaluate_nano_agents.md` runs all agents in parallel on a LOP and grades performance/speed/cost; commit `eval_results_*.md`. *Learn: the trifecta; cheap models often win.*

**Done when:** one HOP invocation runs ≥3 models in parallel on the same task and produces a graded comparison table with token counts, wall-clock, and cost — including a $0.00 local model row.

## 5. agentic-drop-zones (8 commits, 2025-08)

**Why:** Minimal agentic infrastructure — one file, one YAML, huge leverage. The best first rebuild: teaches triggers, templates, streaming, and autonomy trade-offs without any web stack.

**Rebuild path** (the `init` commit contains everything; the seven `progress` commits are README/arch polish — decompose `init`):
- **M1 — Watcher skeleton:** `sfs_agentic_drop_zone.py` with watchdog observers, rich console; detect created files matching patterns. *Learn: single-file uv apps ("sfs" naming), event-driven triggers.*
- **M2 — Declarative zones:** `drops.yaml` (name, file_patterns, reusable_prompt, zone_dirs, events, agent, model, mcp_server_file, create_zone_dir_if_not_exists). *Learn: config-not-code extensibility.*
- **M3 — Prompt templating + agent dispatch:** load `.claude/commands/<x>.md`, substitute `FILE_PATH`, shell out to `claude -p` with `bypassPermissions` and stream JSON to styled panels. *Learn: prompts as reusable templates; full-autonomy risk framing.*
- **M4 — Multi-agent + MCP:** gemini_cli branch (`yolo --sandbox`), per-zone `.mcp.json`; `.gemini/settings.json.sample`. *Learn: agent-agnostic dispatch, per-zone tool scoping.*
- **M5 — Real zones:** `echo.md` (hello world), `create_image.md`/`edit_image.md` (MCP image gen), `finance_categorizer.md`, `morning_debrief.md`, `more_training_data.md`; `example_input_files/`. *Learn: one pattern, many workflows — the zone catalog is the product.*

**Done when:** dropping `echo.txt` streams a response within seconds; an image-prompt file produces a generated image in the zone; a malformed file fails loudly, not silently.

## 6. beyond-mcp (1 commit, 2025-11)

**Why:** The clearest architectural-judgment lesson: the same domain built four ways forces you to *feel* the context-cost/discoverability/reusability trade-offs everyone argues about abstractly. The numbered apps are a built-in rebuild order.

**Rebuild path** (structure-derived):
- **M1 — Domain client:** shared Kalshi API access (status, events, markets).
- **M2 — `apps/1_mcp_server`:** FastMCP server + `.mcp.json`; measure the context the tool schemas consume at session start. *Learn: MCP mechanics and their "instant context loss."*
- **M3 — `apps/2_cli`:** typer/click CLI + `/prime_kalshi_cli_tools` command that teaches the agent the CLI on demand. *Learn: prime-on-demand beats always-loaded.*
- **M4 — `apps/3_file_system_scripts`:** one uv script per operation; `/prime_file_system_scripts`. *Learn: scripts as the zero-infrastructure tool surface agents read and edit.*
- **M5 — `apps/4_skill`:** SKILL.md wrapping the capability with trigger description + progressive disclosure. *Learn: skills as auto-discovered, context-cheap packaging.*
- **M6 — Bake-off:** run the same prompt set against all four; compare tokens at startup, tokens per task, latency, and failure modes. *Learn: writing the trade-off table yourself.*

**Done when:** you can answer "MCP, CLI, scripts, or skill?" for a new toolset in one sentence, backed by your own measured token numbers.

## 7. bowser (3 commits, 2026-02)

**Why:** The best single artifact for Dan's composition philosophy — Skill → Subagent → Command → justfile, each layer independently testable. Small (30 files) but the architecture generalizes to any capability, not just browsers.

**Rebuild path** (initial `🚀` has the full stack; build it layer by layer):
- **M1 — Layer 1, skills:** `claude-bowser` (Chrome MCP, headed/observable) and `playwright-bowser` (playwright-cli, headless) SKILL.md files; test directly with `just test-playwright-skill`. *Learn: dual observable/headless capability design; a `just` skill teaching the runner itself.*
- **M2 — Layer 2, subagents:** `playwright-bowser-agent`, `claude-bowser-agent`, `bowser-qa-agent` wrapping skills for isolated parallel sessions with structured report output. *Learn: subagent = capability + isolation + report contract.*
- **M3 — Layer 3, commands:** `/bowser:hop-automate` (run saved workflow), `/ui-review` (discover YAML stories in `specs/`, fan out QA agents, collect into `ai_review/`), saved workflows `amazon-add-to-cart.md`, `blog-summarizer.md`. *Learn: HOP orchestration over subagents.*
- **M4 — Layer 4, justfile:** one-liners per layer (`just hop …`, `just ui-review`); README with the four-layer table (the two `progress` commits). *Learn: reusability for you, your team, and other agents.*

**Done when:** you can enter at every layer — skill directly, one agent, full `/ui-review` fan-out, and a `just` one-liner — and parallel QA produces per-story reports in `ai_review/`.

## 8. agentic-finance-review (2 commits, 2026-01)

**Why:** The capstone of the trust theme: specialized self-validating agents whose hooks live *inside* the agent definitions, validated by deterministic scripts. It composes nearly everything above (commands + subagents + hooks + orchestration) into an autonomous pipeline with a checkable output.

**Rebuild path** (single `🚀` + `progress`; decompose the pipeline):
- **M1 — Mock data + one validated stage:** `mock-input-data/raw_*.csv`; `normalize-csv-agent.md` with an embedded PostToolUse hook running `csv-single-validator.py`. *Learn: agent-scoped hooks (vs global settings.json); validation as part of the agent, not the harness.*
- **M2 — Stage agents:** `categorize-csv-agent`, `merge-accounts-agent`, `csv-edit-agent`, each with matching validators (`csv-validator.py`, `normalized-balance-validator.py`). *Learn: one agent = one job = one validator.*
- **M3 — Visualization stages:** `graph-agent` + `scripts/generate_graphs.py` (8 plots) with `graph-validator.py`; `generative-ui-agent` producing `index.html` dashboards with `html-validator.py`; Stop-hook validation on `/build` (ruff/ty validators). *Learn: validating generated UI and code deterministically.*
- **M4 — Orchestrator:** `/review-finances` chaining normalize → categorize → merge → accumulate → graph → dashboard over `ROOT_OPERATIONS_DIR` (CLAUDE.md variable); monthly + year-to-date cumulative outputs. *Learn: `Focused Agent + Specialized Validation = Trusted Automation` — autonomy earned through verification.*

**Done when:** dropping a new month of raw CSVs and running one command produces normalized/merged CSVs, 8 graphs, and monthly + yearly dashboards — with every stage's validator green and any failure loudly halting the pipeline.

### Honorable mentions
- **the-verifier-agent** — rebuild after #8 if you use Pi: verification moved from hooks into a dedicated observer agent (unix socket + session JSONL, un-promptable by design).
- **claude-code-damage-control / bash-damage-from-within** — the security pair: rebuild patterns.yaml hooks, then attack them with the 5-level ladder's prompt catalog.
- **agent-experts** (course codebase) — the learning-agents capstone: expertise.yaml + self-improve prompts (ACT → LEARN → REUSE); rebuild one codebase expert for a repo you own after finishing #1 and #8.

---

## Suggested rebuild order for a learner

1. **agentic-drop-zones** (smallest; triggers + templates + autonomy)
2. **claude-code-hooks-mastery** (the foundation stack, richest history)
3. **infinite-agentic-loop** (spec-driven parallel orchestration)
4. **beyond-mcp** (tool-interface judgment)
5. **bowser** (layered composition)
6. **nano-agent** (build the agent itself + evaluation)
7. **claude-code-hooks-multi-agent-observability** (full-stack product)
8. **agentic-finance-review** (self-validating autonomous pipeline)

The arc: *trigger an agent → control an agent → parallelize agents → choose tool interfaces → compose layers → build and measure the agent itself → observe fleets → trust autonomous pipelines.* That is, in order, how Dan thinks.

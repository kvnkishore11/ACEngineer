# TAC-5 — Outdated vs Current (course era → mid-2026)

TAC-5 ages well because it teaches a *mental model* — request → validate → resolve, stacked across disjoint failure classes — not a toolchain. The concept is dead-on for 2026; what moved is **packaging and enforcement**. The lesson wires every loop by hand inside prompt text and Python; current Claude Code can package those loops as Skills and enforce them as hooks. Six things shifted. For each: what the course shows, what current practice is, and whether the book needs an overlay. Dan pre-handles the cosmetic drift himself — the YOLO "Bypassing Permissions" banner and `think hard` IDK are period detail; *"we will be the ones prompting the errors"* is the timeless part.

---

## 1. Enforcement: closed loops in prompt text → hooks as rails  ⟵ the one config step short

**Course era:** the loop lives INSIDE the prompt (request/validate/resolve), and that remains the right mental model for judgment-bearing work. tac-5 already ships five lifecycle hooks — but uses them for logging and notification, not validation.
**Current:** Claude Code (mid-2026) can enforce loops mechanically — `PostToolUse` hooks that run ruff/pytest after every edit and feed failures straight back, `Stop` hooks that gate completion on a green suite. The rule of law stops being a prompt the agent *should* honor and becomes a rail it *cannot* cross. tac-5 is literally one config step short of this pattern.
**Book treatment:** overlay + "current practice" callout. Teach the prompt-level loop first (pedagogically perfect — you can watch the stdout land in context), then show the same non-negotiable moved into a hook. Split rule: **prompt-level loops for judgment, hook-level loops for non-negotiables.**
**Overlay:** `6fCqj4xFCZI` — *How Claude Code CHANGED Engineering Forever* (include_in_phase1: **yes**).

## 2. Packaging: reusable validation prompts → Agent Skills

**Course era:** the `# Validation` reusable prompt and the `.claude/commands` templates are the encoding — discovery, triggering, and composition all manual.
**Current:** Agent Skills (`SKILL.md` with frontmatter, on-demand discovery, composition, shareable across projects/teams) are the first-class form of exactly this. A "validate this repo" skill with embedded commands, e2e specs, and evidence rules is the modern shape of what this lesson builds by hand. Concept maps 1:1; packaging upgraded.
**Book treatment:** overlay REQUIRED — this is the named packaging gap for every prompt artifact in the chapter. Teach the templates first (no magic), then show the same workflow as a Skill.
**Overlay:** `X2ciJedw2vU` — *RAW Agentic Coding: ZERO to Agent SKILL* (include_in_phase1: **yes**).

## 3. Contracts: text-parsed JSON → structured outputs + Agent SDK

**Course era:** `adw_test.py` asks `/test` to "return ONLY JSON" and then `parse_json()`s markdown-wrapped output — period-accurate, instructive, and a little fragile.
**Current:** the Claude Agent SDK (Python/TS) gives schema-validated structured outputs, session management, hooks, and subagents natively; `claude -p --output-format stream-json` (which `agent.py` already uses) grew into a full product surface. The CONTRACT idea — **code decides, agents judge** — is completely unchanged and is the transferable lesson.
**Book treatment:** sidebar ("the JSON-you-hope-parses has a grown-up form"), not a rewrite. The boundary where deterministic code owns retries and agents own judgment is the point; the SDK just makes that boundary type-safe.
**Overlay:** none needed.

## 4. Browser loop: Playwright MCP → wider computer-use menu

**Course era:** Playwright MCP as the browser validator (`--isolated --headless --viewport-size 1920,1080` in `.mcp.json`).
**Current:** Playwright MCP is still a standard, current choice and the config holds up — but browser validation now has more first-party routes: Claude's computer-use tooling, Chrome-DevTools MCP for performance/a11y loops, hosted browser sandboxes. The principle *"browser control is another tool for validating work"* aged perfectly; only the menu widened.
**Book treatment:** footnote listing the current options; keep Playwright as the worked example. No overlay.

## 5. Environment: Mac mini + cloudflared → managed out-loop

**Course era:** the PITER environment is a physical Mac mini running `trigger_webhook.py` behind a cloudflared tunnel.
**Current:** managed options now dominate the E in PITER — `claude-code-action` on GitHub Actions (issue/PR-triggered agents with the repo checkout as the environment), cloud sandboxes (E2B is literally teased in `.env.sample`), and Claude Code on the web for kicked-off background runs. The four PITER elements are invariant; the **E is now often rented**.
**Book treatment:** "current practice" box next to the webhook demo. The self-operating end state this builds toward is owned by later chapters (below), so keep this chapter's overlays testing-specific.
**Overlay candidate (deferred):** `fop_yxV-mPo` — *Codebase Singularity* (include_in_phase1: **no**; TAC-4/7/8 own that vision).

## 6. Models & UI: period detail, pre-handled

**Course era:** `agent.py` pins model strings (`'sonnet'|'opus'`), the demo shows course-era TUI, the YOLO "Bypassing Permissions" banner, and `think hard` as an IDK.
**Current:** newer model families and richer permission modes exist; none of it changes a single loop. Treat every screenshot as period detail.
**Book treatment:** one-line margin note on affected frames ("UI is period detail; the loop is identical today"). No overlay.

---

## What has NOT aged (teach with full confidence)

- **The core validation question** — "Given a unit of valuable work that's production ready, how would you, the engineer, test and validate this work?" — and its operational payoff: encode each answer into a command or tool call.
- **Request → validate → resolve** as the anatomy of a closed-loop prompt. More common now (slash commands, skills, CI prompts), not less.
- **Tests as the rule of law**, with the corollary (a wrong test gets fixed *as a test*, never routed around). If anything, more enforceable now via hooks.
- **Stacking confidence across disjoint failure classes** — the six loops each catch what the others structurally can't. Timeless.
- **The browser is a tool call** — drive UI, capture evidence, verify a precise expectation. Complexity-invariant.
- **Code decides, agents judge** — the JSON contract at the `/test` boundary. The SDK hardens it; the idea is the lesson.
- **Isolated SDLC nodes** — test as its own node with its own agents and context windows, independently improvable. This is *more* true with subagents.
- **Observability / adopt your agent's perspective** — per-agent saved prompts + `raw_output.jsonl`, ADW-ID-prefixed comments as a trace viewer. The reason an out-loop FAILED became a 90-second diagnosis.
- **Bounded loops** — 4 unit / 2 e2e retries, stop-on-nothing-resolved, e2e-stop-on-first-failure. The difference between self-correction and token-burning thrash.
- **The adoption gradient** — single prompt → in-loop closed loops → templated prompts → ADWs off your device → you, the test on top of the test. Beginner-safe and still exactly right.

## Phase-1 overlay decision (strict, per brief: max 1–3)

| # | Video | Maps to | Include |
|---|---|---|---|
| 1 | `X2ciJedw2vU` — RAW Agentic Coding: ZERO to Agent SKILL | corrects outdated (templates → Skills packaging) | ✅ |
| 2 | `6fCqj4xFCZI` — How Claude Code CHANGED Engineering Forever | named hole (hooks as enforcement rails; headless/programmatic surface) | ✅ |
| 3 | `fop_yxV-mPo` — Codebase Singularity | self-operating end state → owned by TAC-4/7/8 | ❌ defer |

*Caveat: IDs/titles from the orchestration brief's seed list; verify each resolves and content matches title before publishing overlay links (no video fetching was performed in this extract pass, per brief). `current_practice_gaps` written against mid-2026 Claude Code (Skills, Agent SDK, hooks, computer-use, managed sandboxes); re-check at publish time.*

# TAC-4 — Outdated vs Current (course era → mid-2026)

TAC-4 teaches an architecture (PITER + ADW + agentic layer), and architectures age slower than tools. Dan future-proofs in-lesson twice: "these four elements can be anything... don't read into how this is configured too much — focus on the composable units," and "tools will change and models will improve." Still, seven things have moved. For each: what the course shows, what current practice is, and the book treatment.

---

## 1. Hand-rolled subprocess wrapper → Claude Agent SDK  ⟵ the big named gap

**Course era:** `adws/agent.py` builds the `claude -p ... --output-format stream-json` command by hand, pipes stdout to a JSONL file, parses the `result` message itself, and manages an env allowlist. Dan even dates it on camera: "the agent SDK currently only runs with the API key. This may change in the future — keep your eye out for that." (`ai_docs/claude_code_sdk.md` pins the era's SDK docs.)
**Current:** the Claude Agent SDK (Python/TypeScript) IS this file, productized: typed message streams, structured outputs, session management, hooks, subagents, permission control — and auth options beyond a raw API key have shipped since. What TAC-4 calls "programmable mode" is now a supported product surface, not a subprocess trick.
**Book treatment:** overlay/sidebar — teach `agent.py` first (every moving part visible: the pedagogically perfect form), then one page: "here is this exact file rewritten on the SDK." The concept — Claude Code as a pipeline primitive — is unchanged.
**Overlay:** `6fCqj4xFCZI` — *How Claude Code CHANGED Engineering Forever* (listed; **deferred** from phase-1 to avoid duplicating chapter 1's overlay set).

## 2. DIY issue→PR pipelines now have first-party competitors — and first-party HOSTS

**Course era:** the lesson's framing is "replace and outperform Copilot, Devin, Jules, Codex" with a webhook + Mac mini + your templates.
**Current:** GitHub-native coding agents matured (Copilot's coding agent takes issue assignments; Claude Code runs inside GitHub Actions and responds to @-mentions). Two consequences: (a) the convenience bar Dan is competing against is higher; (b) more interestingly, CI runners became a mainstream **Environment** choice — you can host YOUR pipeline (templates, ADWs, standards intact) on their infrastructure. The four elements map cleanly onto Actions: issue → workflow trigger → runner → PR.
**Book treatment:** reframe, don't retract: the ownership argument ("they're not running your templates... one size does not fit all") has aged WELL — it's now the differentiator between you and everyone whose agent PRs look identical. Add a margin note: "E can be a GitHub Actions runner; the Mac mini is one instantiation."
**Overlay:** none needed.

## 3. `--dangerously-skip-permissions` → sandboxes, permission modes, scoped headless flags

**Course era:** every template run skips permissions entirely; safety comes from the dedicated environment ("running dangerously, but... in its own environment, this is going to be safe"). Interactive sessions rely on `.claude/settings.json` allow/deny lists plus pre-tool-use hook blocking (rm -rf patterns, .env access).
**Current:** the menu grew — sandboxed bash, permission modes, `--allowedTools`/`--disallowedTools` for headless runs, hook-based gates, container/worktree isolation. Teams now typically run headless agents with *scoped* allowlists inside sandboxes rather than full skip, even in dedicated environments.
**Book treatment:** keep the lesson's principle front and center (move the permission boundary to the environment — it's correct and current), then a "current practice" callout: today you'd add a second boundary (scoped tools/sandbox) so a prompt-injected agent can't, e.g., exfiltrate the GH token that lives in its env.
**Overlay:** none needed.

## 4. Flat `.claude/commands/*.md` → Agent Skills and richer command surfaces

**Course era:** reusable behavior = 13 flat markdown slash commands with `$ARGUMENTS`/`$1..$n`, hand-invoked by the ADW.
**Current:** Agent Skills (`SKILL.md` with frontmatter, model-invoked discovery, bundled resources) are the first-class packaging for exactly this "no ad hoc prompts — isolate to improve" doctrine; slash commands themselves gained features. The lesson's prompt-library discipline transfers 1:1; only the packaging upgraded.
**Book treatment:** sidebar on the upgrade path (command file → skill), same as the TAC-1 chapter's treatment — by this point in the volume the reader has seen it once, so one paragraph suffices.
**Overlay:** `X2ciJedw2vU` covers this but already anchors chapter 1; do not repeat — cross-reference chapter 1's overlay instead.

## 5. Model names and per-step model policy

**Course era:** `health_check.py` hardcodes `claude-3-5-haiku-20241022` for its live test; ADW steps pass `"sonnet"` aliases (Literal allows `sonnet|opus`); Dan: use top models on plan/build, faster ones elsewhere.
**Current:** the model families moved (Claude 4.x → Claude 5 era); aliases still resolve but the pinned haiku ID is period detail. The *policy* — cheapest model that clears each step, strongest on plan/build — is the durable content and is now standard practice (often with per-step structured-output modes replacing whole-agent calls for glue steps like classification).
**Book treatment:** one-line margin note on the screenshot; keep the policy as a highlighted rule.
**Overlay:** none needed.

## 6. One serial ADW in one checkout → fleets, queues, worktree isolation

**Course era:** `adw_plan_build.py` processes one issue in the repo's single working copy; the branch generator does `git checkout main && git pull && git checkout -b` in place. Two webhook fires at once would collide mid-run. (Deliberate scope: "obviously, we're gonna take this a lot further.")
**Current:** parallel ADWs are routine — git worktrees or containers per run, queues/locks on the trigger side, fleets of runs with per-run isolation. The lesson's own `trees/` gitignore entry hints where the course goes next.
**Book treatment:** forward-pointer only ("the ceiling is much higher; don't productionize the demo as-is — serialize your triggers or isolate your checkouts"). Belongs to later lessons' chapters in depth.
**Overlay:** `fop_yxV-mPo` — *Codebase Singularity* (include_in_phase1: **yes**) — the where-this-goes vision, now teachable since the reader has templates + ADWs.

## 7. Issue-comment live feed → structured run telemetry

**Course era:** observability = ✅/❌ issue comments with `{adw_id}_{agent}` prefixes, per-run `agents/` artifacts, hook session logs.
**Current:** still an excellent zero-infra pattern (and the comment-feed UX is genuinely good); production stacks add structured run views — Actions job summaries, Checks API, trace-style step telemetry — on top of the same four layers.
**Book treatment:** none required beyond a sentence; the lesson's rule ("observe, report, log, monitor — or you can't improve") is timeless.
**Overlay:** none needed.

---

## What has NOT aged (teach with full confidence)

- **PITER.** The four-element decomposition of autonomous coding systems is, if anything, MORE legible now that every vendor ships a variant of it. Tool-agnostic by construction.
- **The ADW composition rule:** deterministic code for sequencing/errors/reporting; non-deterministic agents for judgment; templates as the interface between them.
- **Micro-agent decomposition** with fresh context per step and per-step model policy.
- **Structured return contracts** ("Return ONLY..." / "0 if not found") + loud failure to the review surface — this is exactly how current agent pipelines are still built.
- **The issue-as-prompt pattern** (what + constraints, not plans) and the committed plan as an improvable artifact.
- **Fix the system, not the issue** — the compounding rule, and the demo's own imperfect PR (plus the agent-written `adws/README.md` inaccuracies shipped in the repo) as honest evidence that review is mandatory.
- **The trust ladder** (chores → bugs → features) and the KPI scoreboard (presence↓ size↑ streak↑ attempts↓).
- **Own-your-pipeline economics.** Stronger today than at recording: as generic agents commoditize, the encoded house style IS the moat.
- **Health-check-before-run** as a pattern built into the workflow layer.

## Phase-1 overlay decision (strict, per brief: max 1–3)

| # | Video | Maps to | Include |
|---|---|---|---|
| 1 | `hGg3nWp7afg` — 3 Codebase Folders | operationalizes tactic (the agentic layer's directories: ai_docs/ + specs/ + .claude/) | ✅ |
| 2 | `fop_yxV-mPo` — Codebase Singularity | named hole (the "product builds itself" end-state, now teachable) | ✅ |
| 3 | `6fCqj4xFCZI` — How Claude Code CHANGED Engineering Forever | corrects outdated (agent.py → headless/Agent SDK) | ❌ defer — already anchors chapter 1; cross-reference instead |

*Caveat: IDs come exclusively from the tac-1 orchestration seed list (titles oembed-verified during the TAC-1 cross-review). Mapping to TAC-4 gaps is by title/known topic — verify each resolves and content matches before publishing overlay links; no video fetching was performed in this extract pass, per brief. No new IDs were invented.*

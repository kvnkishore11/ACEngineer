# TAC-6 — Outdated vs Current (course era → mid-2026)

TAC-6 ages well because its spine is primitives — the five SDLC questions, one-agent-one-prompt-one-purpose, typed review contracts, conditional-doc feedback loops — and Dan pre-empts the churn on camera ("model intelligence is not a constraint"). But it's an Advanced lesson wired to a specific tooling moment, and seven things have moved. For each: what the course shows, what current practice is, and whether the book needs an overlay.

---

## 1. One-purpose orchestration: hand-rolled `claude -p` processes → native subagents  ⟵ the big named gap

**Course era:** one-agent-one-prompt-one-purpose is implemented as separate headless `claude -p` processes orchestrated by Python (`execute_template` → stream-json → per-agent folders). Works, and it's pedagogically perfect: nothing is hidden.
**Current:** Claude Code productizes the same tactic — subagents with their own context windows, tools, and system prompts (`.claude/agents/*.md`), spawnable in parallel from a main loop, plus background tasks. The rationale (fresh focused window per purpose) is unchanged and is now the OFFICIAL mental model for subagent design. External ADW-style orchestration still wins for deterministic CI/webhook pipelines; native subagents win for interactive fan-out.
**Book treatment:** overlay REQUIRED. Teach the hand-rolled version first (you see every moving part), then show the same tactic as native subagents / Skills.
**Overlay:** `X2ciJedw2vU` — *RAW Agentic Coding: ZERO to Agent SKILL* (include_in_phase1: **yes**) — the committed one-purpose prompt becomes a `SKILL.md`.

## 2. "Context pollution" → mainstream context engineering

**Course era:** Dan's vocabulary — context pollution / overloading / toxic context, the minimum context principle — predates the industry's "context engineering" wave, and the only lever shown is a fresh window per step.
**Current:** Claude Code adds machinery TAC-6 lacked: auto-compaction control, context editing, `/context` inspection, CLAUDE.md layering, and explicit long-session-degradation guidance. Dan's "compact is a band-aid — if your agent is compacting it is losing information" is now the consensus position, and the durable answer is still exactly what he teaches: fresh one-purpose contexts.
**Book treatment:** "current practice" callout naming the vocabulary alignment; no rewrite. The principle transfers unchanged.
**Overlay:** none required.

## 3. The screenshot-blind reviewer is solved tooling today

**Course era:** the lesson's sharpest self-critique — the review agent captures screenshots it never reads ("the tokens aren't flowing through the vision capabilities"), so a misplaced button sails through. Dan's fix is an in-prompt instruction to read every image.
**Current:** agents read images natively — Claude Code's Read renders PNGs into context, Playwright MCP has vision modes, computer-use agents screenshot-and-look by default. Dan's proposed one-liner is now standard practice.
**Book treatment:** teach the read-your-images instruction as the DEFAULT review-prompt line, not an optional improvement — but keep the whole failure story, because "blame the layer, encode the fix" is the transferable lesson, not the specific gap.
**Overlay:** none required.

## 4. R2 public bucket → one of several proof-hosting paths

**Course era:** review screenshots go to a public Cloudflare R2 bucket (S3-compatible boto3 + public domain, default `tac-public-imgs.iddagents.com`) so GitHub renders them inline.
**Current:** that path still works verbatim; alternatives now include `gh` CLI/API attachment uploads, inline images in PR review comments, CI-runner artifacts, and Agent SDK structured outputs carrying artifacts. The principle — proof lands IN the review system, publicly viewable, zero clicks to verify — transfers unchanged.
**Book treatment:** footnote listing the alternatives; keep R2 as the worked example.
**Overlay:** none required.

## 5. Model routing map: drifted names, now a first-class feature

**Course era:** `SLASH_COMMAND_MODEL_MAP` hardcodes `sonnet` / `opus` aliases (course-era Claude 4-class models) in a hand-rolled dict.
**Current:** the aliases still resolve, but current model families (Claude 4.x → Claude 5 era) and per-agent `model:` frontmatter in subagent definitions make per-purpose model routing a supported feature, not a dict you maintain. The lesson's deeper insight — committed one-purpose prompts let you tune model/thinking per step and rerun as evals — is now also served by real eval harnesses and session resume/checkpointing.
**Book treatment:** margin note on the model-map frame ("aliases are period detail; per-purpose routing is now first-class"); teach the eval idea as durable.
**Overlay:** `6fCqj4xFCZI` — *How Claude Code CHANGED Engineering Forever* (include_in_phase1: **no** — already carried in phase 1 by TAC-1/TAC-3; volume-map reference only).

## 6. app_docs / ai_docs / specs → Dan's full 3-folder taxonomy

**Course era:** TAC-6 introduces `app_docs` (your codebase's docs) alongside `ai_docs` (third-party docs) and `specs` (plans), but the split gets one line: "AI docs for third party, app docs is for your codebase."
**Current:** Dan's public "3 codebase folders" treatment develops the taxonomy fully — the natural overlay for the documentation half of this lesson, including WHY conditional loading (not bulk loading) is the whole point.
**Book treatment:** overlay for the document / conditional-docs section.
**Overlay:** `hGg3nWp7afg` — *3 Codebase Folders* (include_in_phase1: **yes**).

## 7. Repo drift: the two new composers are invisible to triggers (accuracy flag, not an ecosystem shift)

**Course era / on disk today:** `classify_adw.md` lists `/adw_plan_build_review` and `/adw_plan_build_document` as valid, but `data_types.ADWWorkflow` and `workflow_ops.AVAILABLE_ADW_WORKFLOWS` omit both, so `extract_adw_info()` filters them out — webhook/cron classification can select every workflow EXCEPT those two composers. They're manual-entry-only.
**Book treatment:** carry it as a live worked example of prompt↔code contract drift — precisely the failure class a review step is supposed to catch. Not a dated feature; a permanent teaching artifact.
**Overlay:** none.

---

## What has NOT aged (teach with full confidence)

- One agent, one prompt, one purpose — more consensus now (native subagents) than at recording.
- Review ≠ testing. The two-question distinction is the load-bearing idea and is timeless.
- The typed review contract: strict JSON → pydantic `ReviewResult`, severity triage, blockers-only resolution, a hard retry cap, loud parse-failure.
- Severity triage for agreeable agents — skippable / tech_debt / blocker is templated judgment that still keeps nitpicks from blocking releases.
- The conditional-documentation feedback loop — document writes it, planners read it — is the lesson's crown jewel and has no expiry.
- The three constraints, and "model intelligence is not a constraint."
- "Compact is a band-aid." Truer now that we can actually measure context degradation.
- Minimum context principle; adopt your agent's perspective.
- Proof / the live-asset principle; review velocity; ideal presence = 2.
- Out-loop bias: fix the end-to-end portion, not the thing that went wrong. Blame the layer, not the model.
- Committed prompts become evals — git IS the eval infrastructure.

## Phase-1 overlay decision (strict, per brief: max 1–3)

| # | Video | Maps to | Include |
|---|---|---|---|
| 1 | `X2ciJedw2vU` — RAW Agentic Coding: ZERO to Agent SKILL | corrects outdated (one-purpose prompt → Skill/subagent) | ✅ |
| 2 | `hGg3nWp7afg` — 3 Codebase Folders | operationalizes tactic (the document half's home) | ✅ |
| 3 | `6fCqj4xFCZI` — How Claude Code CHANGED Engineering Forever | named hole (tool surface / SDK) — already in phase 1 elsewhere | ❌ defer |
| 4 | `fop_yxV-mPo` — Codebase Singularity | fleet-of-agents endgame → lesson 7 (ZTE) | ❌ defer |

Exactly 2 included (within the 1–3 cap), matching `extract.json`.

*Caveat: IDs/titles from the orchestration seed pool (oembed-verified in the TAC-1 cross-review); re-verify each resolves and the content matches its title before publishing overlay links — no video fetching was performed in this extract pass, per brief.*

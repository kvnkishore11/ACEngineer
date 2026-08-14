# TAC-7 — Outdated vs Current (course era → mid-2026)

TAC-7 ages unusually well because its payload is a *North Star and a set of primitives*, not a toolchain: the velocity scale (in-loop → out-loop → ZTE), the presence KPI, and "the secret is composable agentic primitives, not the SDLC" are timeless, and Dan pre-empts the churn on camera ("I don't care how you scale up your agent environments, it only matters that you can"). But it's the Advanced, second-to-last lesson, wired to a specific mid-2025 tooling moment, and six things have moved. For each: what the course shows, what current practice is, and whether the book needs an overlay. Every gap below narrows the *plumbing*; none touches the doctrine.

---

## 1. Hand-rolled worktree orchestration → isolation as a first-class platform feature  ⟵ the big named gap

**Course era:** parallel isolation is built from raw materials — `git worktree add -b` from `origin/main`, base-36-hash port arithmetic (9100–9114 / 9200–9214), an agent-run `/install_worktree` prompt, and `scripts/purge_tree.sh` to reclaim the full-repo copies. Pedagogically perfect: every moving part is visible.
**Current:** Claude Code (mid-2026) exposes the same tactic natively — worktree-isolated subagents/tasks, sandboxed bash, and cloud/remote agent execution; multi-agent fan-out over isolated environments is a standard orchestration pattern rather than custom scripting. The CONCEPT — isolated, parallel, disposable agent environments with per-run state — transfers unchanged; the code you'd write today is smaller.
**Book treatment:** overlay REQUIRED. Teach the hand-rolled worktree version first (you see the ports, the state, the install), then show the same isolation as native worktree-isolated agents.
**Overlay:** `fop_yxV-mPo` — *Codebase Singularity* (include_in_phase1: **yes**) — TAC-7 is the lesson where "the codebase runs itself" stops being a vision and becomes a demo; this video develops that self-operating end-state. (Deferred out of TAC-1 explicitly *to* this lesson.)

## 2. `subprocess claude -p` pipelines → the Claude Agent SDK

**Course era:** `adws/adw_modules/agent.py` is a subprocess wrapper — `claude -p --model X --output-format stream-json --verbose --dangerously-skip-permissions`, JSONL parsing, a `[1,3,5]s` retry ladder, per-agent session capture.
**Current:** that layer is exactly what the Claude Agent SDK (Python/TS) now provides first-class — structured outputs, hooks, session management, and error semantics. The ADW architecture maps 1:1; a 2026 rebuild swaps `agent.py` for the SDK and keeps every workflow script's shape.
**Book treatment:** margin note on the `agent.py` walkthrough — "this is the SDK, hand-rolled"; teach the ADW composition idea as durable, the subprocess plumbing as period detail.
**Overlay:** `6fCqj4xFCZI` — *How Claude Code CHANGED Engineering Forever* (include_in_phase1: **yes**) — bridges the ADW plumbing the student just read to how the same embedding is done today.

## 3. Reusable engineering as `.claude/commands` prompt files → Agent Skills

**Course era:** engineering is templated into 33 command prompts discovered by convention, plus the `conditional_docs.md` routing table — which is essentially hand-rolled skill discovery / progressive disclosure ("this lets our agents scale with the size of our codebase").
**Current:** Agent Skills (`SKILL.md` with frontmatter, on-demand loading, composability) are the first-class packaging for the same idea; the conditional-docs pattern is precisely what Skills' progressive disclosure does natively.
**Book treatment:** overlay for the "template your engineering" section; teach the committed-prompt encoding, then show its current form as a Skill.
**Overlay:** `X2ciJedw2vU` — *RAW Agentic Coding: ZERO to Agent SKILL* (include_in_phase1: **yes**) — the committed one-purpose prompt becomes a `SKILL.md`.

## 4. Model names and model-set economics are period detail

**Course era:** `SLASH_COMMAND_MODEL_MAP` hardcodes `sonnet` / `opus` aliases circa mid-2025, and the demo app bumps `gpt-4.1` → `o4-mini` as its worked chore.
**Current:** model families have turned over since (Claude 4-class → Claude 5 era); the specific ids are dated the day they ship. The durable idea is the **base/heavy KNOB** — per-command compute allocation via an IDK stored in state — not any model name. Update the map's *values*, keep its *shape*.
**Book treatment:** "period detail" callout on the model-map frame (t1010); teach the knob and the 8-of-18 selectivity as the transferable lesson.
**Overlay:** none required.

## 5. ZTE guardrails have matured beyond an uppercase check

**Course era:** the auto-merge safety is charming prompt-level engineering — `/classify_adw` refuses `adw_sdlc_ZTE_iso` unless "ZTE" is literally uppercase — plus the pipeline's own gates (test/review abort, 8-field state validation, three-way worktree check, `--no-ff` merge with branch-restore).
**Current:** production practice layers *deterministic* controls around auto-merge: branch protection + required CI checks, permission modes and hooks gating tool use, environment-scoped credentials, staged deploys / canaries, and merge queues. Dan hints at exactly this evolution in-lesson — "add that key deploy check step, a bunch of deterministic deploy checks... parallelize the review step so three agents have to agree — run the fusion chain on agents."
**Book treatment:** teach the in-repo gates as the *concept* (a pipeline that refuses to merge in N places), then a "current practice" callout naming the deterministic controls a real deploy would add. Keep the uppercase interlock as a teaching artifact of prompt-level safety, not a recommendation.
**Overlay:** none required (Dan's own "deterministic deploy checks / three-agent fusion" line carries it).

## 6. Review evidence: screenshots → video and richer review products

**Course era:** the review step's proof is 1–5 numbered screenshots uploaded to R2 and posted to the issue.
**Current:** the lesson names its own next step — "the next most obvious one to build out is video. Have your agents take video, upload it to a cloud bucket, and post the URLs." The repo's `playwright-mcp-config.json` *already records* 1920×1080 video per run, and Dan calls comprehensive review systems "an entire product category that is important to build out" — which is precisely what agent-review tooling became.
**Book treatment:** footnote the video path as the intended evolution (the config is already there — see lab stretch S7); keep screenshots as the worked example. The principle — proof lands IN the review system, zero clicks to verify — transfers unchanged.
**Overlay:** none required.

---

## What has NOT aged (teach with full confidence)

- The **Agentic Engineering Velocity Scale** — in-loop → out-loop → ZTE — and that it's a per-problem-class gradient, not a switch.
- **Presence** as the KPI under the whole course arc: TAC-1 removed typing, TAC-7 removes reviewing, presence tracks both.
- **The secret: composable agentic primitives**, with the SDLC demoted to one arbitrary arrangement ("a package to deliver a message"). This is the course's thesis and has no expiry.
- **Review = proof of value** ("is what we built what we asked for?", proved), distinct from testing; blockers-only resolution.
- The **ADW state object** as pipeline memory outside the context window — the thing that lets single-purpose agents chain.
- **Isolation, parallelism, disposability** as the requirement (worktrees are one implementation of it).
- The **base/heavy compute knob** — encode the allocation once, invoke with one word.
- **Evidence-gated, per-class** decisions to drop review — KPIs, not vibes; "how else will you know unless you're trying?"
- **"Target" ZTE**: chores → bugs → features; a North Star you earn, not a day-one state.
- The **belief section** — "if you don't believe your agents can run your codebase, you're cooked"; "prepared to win, not right."
- **Verify countable claims against source, not docs** — the README-says-squash / code-does-`--no-ff` drift is a permanent teaching artifact, not a dated feature.

## Phase-1 overlay decision (strict, per brief: max 1–3)

| # | Video | Maps to | Include |
|---|---|---|---|
| 1 | `fop_yxV-mPo` — Codebase Singularity | operationalizes tactic (the self-operating codebase this lesson demos) | ✅ |
| 2 | `6fCqj4xFCZI` — How Claude Code CHANGED Engineering Forever | named hole (`agent.py` subprocess → Agent SDK) | ✅ |
| 3 | `X2ciJedw2vU` — RAW Agentic Coding: ZERO to Agent SKILL | corrects outdated (command prompts / conditional_docs → Skills) | ✅ |
| 4 | `hGg3nWp7afg` — 3 Codebase Folders | ai_docs/specs/app_docs get only passing reference here | ❌ defer to the context lessons / volume map |

Exactly **3** included (within the 1–3 cap), matching `extract.json`'s `yt_overlay_candidates`. TAC-7 uses all three because its three biggest plumbing gaps (worktree orchestration, subprocess pipelines, prompt-file packaging) each have a clean, on-topic current-practice video.

*Caveat: IDs/titles come from the orchestration seed pool (oembed-verified in the TAC-1 cross-review — `fop_yxV-mPo`, `6fCqj4xFCZI`, `X2ciJedw2vU`); re-verify each resolves and its content matches its title before publishing overlay links — no video fetching was performed in this extract pass, per brief.*

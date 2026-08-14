# Outdated vs Current — Multi-Team Agentic Coding / Lead Agents (`ma-2-lead-agents`)

What in this lesson is **period detail** (a specific tool/model/UI state at recording time) versus what is **timeless** (the tactic). Dan future-proofs the model/UI drift himself in-lesson — treat specifics as a snapshot, tactics as current. Written against the ecosystem as of **mid-2026**; the model-name and harness-capability axes move fast, so re-verify at publish.

Two kinds of drift are documented here:
- **A. Recording-vs-shipped drift** — where the video shows an *earlier* state than the checked-in repo (verified by reading both).
- **B. Ecosystem drift** — where the wider tooling has moved since recording.

---

## A. Recording-vs-shipped drift (verify against the shipped files, not the video)

### A1. The on-screen `orchestrator.md` predates the TillDone integration
- **In the video** (frame **t0768**), `orchestrator.md` shows `tools: read, grep, find, ls, delegate` and only **two** domain entries (`.pi/multi-team/`, `.`).
- **In the shipped file**, the orchestrator has `tools: write, edit, read, grep, find, ls, delegate, **tilldone**` and **three** domain entries (adds `.pi/multi-team/expertise/` with `upsert: true`).
- **Why:** `tilldone` was added *after* this recording — `specs/tilldone-multi-team-integration.md` is the plan that added it (orchestrator + the three leads gained the tool; workers deliberately did not). The video captures a mid-development state.
- **Teaching guidance:** teach from the **shipped** files. If you show frame t0768, caption it as "an earlier build — the shipped orchestrator also has `write/edit/tilldone` and can write its own expertise."

### A2. The front-end/back-end domain SPLIT is a live demo edit, not the shipped default
- **In the video** (frame **t1290**), Dan edits `frontend-dev.md` so its domain scopes writes to `apps/frontend/` (read+upsert+delete) while only **reading** the rest of `apps` — the "read the back-end, never touch it" rule — and shows the mirror-image edit for `backend-dev.md`.
- **In the shipped files**, `frontend-dev.md` and `backend-dev.md` have **identical** app-domain: `apps/` with read+upsert+delete. There is no `apps/frontend/` / `apps/backend/` split checked in.
- **Why:** the shipped repo is a "simple example" (a data-science, backend-focused target; Dan even notes the front-end dev isn't really needed for prompt-routing). The split is Dan demonstrating *what you would do* on a real front/back codebase.
- **Teaching guidance:** present the split as the *pattern to apply*, and be explicit that the shipped default is unsplit. Great "you try" lab step (see `lab-spec.md` S3).

### A3. The mental-model (expertise) files ship EMPTY
- **In the video**, the back-end dev's mental model is ~5,000 tokens of rich, structured notes (specs, missing infra, key risks, backend patterns, security, testing).
- **In the shipped repo**, all **10** expertise files are **0 lines** (verified with `wc -l`).
- **Why:** that on-screen model was Dan's *working copy from a previous codebase* — he says on camera, "I actually need to get rid of this and tune the mental model… it's got information stored about its previous codebase." `/install-into-codebase` creates **empty** expertise; agents grow their own per codebase.
- **Teaching guidance:** the compounding is the point, not the starter file. Weak students who open an empty file and think "it's broken" are missing that these are meant to fill in over sessions.

### A4. Dan's own description says "2 teams" — the shipped default is 3
- The video description says "9 specialized agents across 3 teams" in one place and "2 teams, 3 members each, 9 agents" in another.
- The shipped `multi-team-config.yaml` and the footer both show **3 teams / 10 agents** (1 orchestrator + 3 leads + 6 workers).
- **Teaching guidance:** use the code's numbers (3 teams, 10 agents). The "2 teams" line is a description inconsistency, not the system.

---

## B. Ecosystem drift (period detail vs timeless tactic)

### B1. Model names (`claude-opus-4-6`, `claude-sonnet-4-6`, "Haiku")
- **Period detail:** the agent frontmatter pins `anthropic/claude-opus-4-6` (orchestrator + leads) and `anthropic/claude-sonnet-4-6` (workers); the transcript names "Opus 4.6," "Sonnet 4.6," and "Claude Haiku." The `opensource` config names then-current third-party models (qwen3.5, kimi-k2.5, gemini-3-flash-preview, gpt-5.4/-mini, minimax-m2.7, mimo-v2-pro).
- **Timeless tactic:** **tier your models** — best intelligence where coordination happens (orchestrator + leads), cheaper where you just execute (workers) — or go all-Opus if you're maxing out. Dan blesses drift directly: models will improve; that's great; don't let it distract you.
- **Action at publish:** update model ids to the current tier equivalents; keep the tiering principle verbatim.

### B2. Sequential delegation only; parallel is the roadmap
- **Now:** the orchestrator delegates **one team at a time** (plan → engineer → validate). Dependent work is exactly right for this.
- **Coming:** `OPUS.md` names **parallel delegation** as the next direction — `Promise.allSettled` already wraps the delegation loop; the hard part is teaching the orchestrator *when* work is parallel-safe vs dependent ("review this PR" → Engineering + Validation at once). Independent cross-team requests are the near-term unlock, not the current default.
- **Teaching guidance:** tell the reader the ceiling is higher than what the video shows; don't imply parallel fan-out is already the behavior.

### B3. Two orchestration models coexist — don't conflate them
- **The Pi RUNTIME** (the lesson's subject) uses custom `delegate` / `tilldone` tools and spawns `pi` subprocesses. This is what runs when you type in the chat room.
- **The Claude Code BUILD harness**: the `.claude/` tooling — `plan-w-team.md`, `meta-pi-agent.md`, and the "Team Orchestration / Task*" sections of both specs — uses Claude Code's **Task\*** tools (`TaskCreate`/`TaskUpdate`/`Task`/`TaskOutput`) to *build and extend* the system. Claude Code is the **bootloader** (`/install`, `/install-into-codebase`).
- **Ecosystem drift:** Claude Code's own subagent/Task/background-task and Agent-Skills capabilities have grown since recording, which makes it *easier* to conflate the build harness with the runtime. Keep the two layers distinct in the chapter.

### B4. "Beyond Claude Code" — harness customization is less exotic now
- **The lesson's premise:** the Pi harness is customizable down to files/folders/tools/hooks/**UI** ("the nuclear UI pattern"), which is what lets Dan build a multi-team chat room. He notes you *can* build a more limited version in Claude Code via subagents + hooks ("Pi has the exact same system" of hooks).
- **Drift:** since recording, Claude Code and peers have expanded their own customization surfaces (Agent Skills with `SKILL.md`, hooks, output styles, plugins, settings layering). The **ideas** — teams, leads, domain locking, compounding memory, a single chat-room interface — now have more than one viable home.
- **Timeless tactic:** don't marry the tool. Dan: "More tools like this will emerge, but the ideas will be there." Anchor the chapter on the transferable architecture, not on Pi specifically.

### B5. Multi-agent tooling landscape
- The description name-drops **CMUX** alongside Claude Code as multi-agent tooling "here now." The specific tool roster will keep changing; the point ("multi-agent orchestration is the frontier right now, and the engineers who build these patterns get the asymmetric advantage") is durable.

---

## What is fully timeless (state these plainly)

- **One agent is a ceiling; teams of agent experts break it.**
- **Depth-2 delegation** (User → Orchestrator → Leads → Workers) with a **single orchestrator interface**.
- **Leads delegate, never execute**, enforced both softly (skill) and structurally (domain rules).
- **Domain ownership** (per-path read/upsert/delete) as the unlock for safe autonomy at scale.
- **Agent experts > generalists**, powered by **compounding, domain-scoped mental models** you let the agents self-maintain.
- **Composable skills** as the fleet-wide control surface.
- **Configuration-driven teams** — the whole roster in one file.
- **Model tiering + spend-to-win**, and the **2026 game of trust then scale.**

---

## Current-practice overlays (YouTube)

Both phase-1 overlays are sourced **directly from the lesson's own description** (real IDs, oembed-verify before publishing):
- **`f8cfH5XX-XU` — "Pi vs Claude Code"** → the named "beyond Claude Code / customizable harness / hooks" gap (Dan references it in-lesson).
- **`TqjmTZRL31E` — "CEO Agents"** → the immediately-prior lesson this one builds on (context / 1M window / multi-agent foundation).

See `extract.json` → `yt_overlay_candidates` for the full list and rationale (plus the phase-2 candidates).

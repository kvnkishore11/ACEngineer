# Extract — Multi-Team Agentic Coding / Lead Agents (`ma-2-lead-agents`)

> **Course:** MA (Agentic Horizon multi-agent series) · **Order:** 16 · **Volume:** vol-3-ma · **Chapter stem:** `16-lead-agents`
> **Video:** 34:56, native 4K (3840×2160). Public cut: `youtu.be/M30gp1315Y4` — "One Agent Is NOT ENOUGH: Agentic Coding BEYOND Claude Code."
> **Codebase:** members-only `lead-agents` (the multi-team-chat TOOL built on the **Pi coding agent** harness).

This file is the human-readable companion to `extract.json`. It carries the teaching scaffold (Hook → Picture → Worked example → Name → Failure → Retrieval) that the chapter is built from. Every technical claim is verified against the shipped codebase and the transcript; see `extract.json` → `confidence_notes` and `outdated-vs-current.md` for the version-drift flags.

---

## 0. The one-liner and the mission

**Tactic:** *One agent is not enough — build teams of agent experts.* Stop being the orchestrator. Replace the single, endlessly re-prompted agent with a **config-driven hierarchy of specialized, domain-locked, memory-compounding agent experts** that you command through **one** chat interface.

**Mission:** Move up the stack again — from *single-agent operator* to *commander of agent teams*. Dan's prediction: by the end of 2026 the engineer still re-prompting one agent in a terminal is the bottleneck (they **are** the orchestrator). You become irreplaceable by building a multi-team system where you type one message and 9 specialized agents across 3 teams decompose → build → validate while you watch. No babysitting. The endgame of TAC/Agentic Horizon: **systems that build systems**, so your codebase increasingly runs itself.

**Why it's uncomfortable:** it asks you to spend real money on coordination that *looks* wasteful. "Ping each team" is 7+ API calls; a full plan→engineer→validate cycle can cost ~$8 across Opus leads and Sonnet workers. Cost-min-maxers see the footer tick and call it waste. Dan's counter is the whole mindset of the lesson: *you are not thinking far enough into the future.* Intelligence-per-token rises while token cost falls, so the engineer who learns to **spend** those tokens on specialized teams **now** gets the asymmetric advantage.

> "One agent is not enough… today I want to show you a system that pushes beyond Claude Code. This is multi-team agentic coding. Here we use specialized teams of agents to outperform the normal distribution of results." — 0:06 / 1:02

---

## 1. Dan's spine: the 6 pillars

Dan frames the whole system as **6 pillars of multi-agent team orchestration** (from his own description). Use these as the chapter's backbone — every concept hangs off one:

1. **Team Leads & Workers** — a 3-tier hierarchy that removes YOU as the bottleneck.
2. **Expertise & Specialization** — specialized agents make expert decisions; generalists make mediocre ones.
3. **Agent Memory** — persistent per-agent mental models that compound session over session.
4. **Domain Ownership** — per-path boundary enforcement that makes full autonomy *safe* (blast radius ≈ zero).
5. **Chat Room Interface** — the coordination primitive; you talk only to the orchestrator.
6. **Configuration-Driven Harness** — the entire setup in one YAML, on the customizable Pi harness.

---

## 2. The architecture — depth-2 delegation

```
User
  │  (you type one message; you only ever talk to the Orchestrator)
  ▼
Orchestrator            model: claude-opus-4-6
  │  classify → tilldone list → delegate(team, question) → synthesize
  ├─▶ Planning Team
  │     ├─ Planning Lead      (opus) — routes to members, synthesizes; NEVER executes
  │     ├─ Product Manager    (sonnet)
  │     └─ UX Researcher      (sonnet)
  ├─▶ Engineering Team
  │     ├─ Engineering Lead   (opus)
  │     ├─ Frontend Dev       (sonnet)
  │     └─ Backend Dev        (sonnet)
  └─▶ Validation Team
        ├─ Validation Lead    (opus)
        ├─ QA Engineer        (sonnet)
        └─ Security Reviewer  (sonnet)
```

**10 agents total** = 1 orchestrator + 3 leads + 6 workers. (Dan's description says "2 teams, 3 members each, 9 agents" in one line — that's inconsistent with the shipped **3-team** default; the footer visibly renders 10 rows. Trust the code.)

**Delegation flow:** you → orchestrator → lead → worker; results bubble back up into one answer. Multi-team work chains **sequentially** (plan → engineer → validate), not in parallel — parallel delegation is the roadmap (see `outdated-vs-current.md`).

**Tier job matrix (the thing to memorize):**

| Tier | Model | Tools | Can run bash / mutate code? | Domain | Key skills |
|---|---|---|---|---|---|
| Orchestrator | opus-4-6 | write, edit, read, grep, find, ls, **delegate**, **tilldone** | No | read all, write only its own expertise | conversational-response, zero-micro-management, active-listener, mental-model, **high-autonomy** |
| Team Lead | opus-4-6 | same as orchestrator | No | read all, write only its own mental-model file | conversational-response, zero-micro-management, active-listener, mental-model |
| Worker | sonnet-4-6 | read, write, edit, **bash**, grep, find, ls (no delegate/tilldone) | **Yes** | scoped per role | mental-model, active-listener, **precise-worker** |

The tier boundary is enforced *twice*: a **soft** layer (the `zero-micro-management` skill in the prompt) and a **hard** layer (domain rules + the `domain-enforcer` extension that structurally blocks out-of-domain tool calls). Both exist on purpose.

---

## 3. Teach each idea (weak-student scaffold)

### 3.1 One agent is a ceiling → teams of agents
- **Hook:** "If you're still re-prompting one agent over and over, YOU are the orchestrator, and that's the problem." You are doing the classify/route/synthesize work by hand.
- **Picture:** the ping demo (frame **t0118**) — you type `ping`, and only the Orchestrator answers: *"Pong. Teams are online — Planning, Engineering, Validation standing by."*
- **Worked example:** `ping each team lead` → the orchestrator fans out to all three leads and composes one reply; the footer sums Orchestrator + leads + context + total cost.
- **Name:** **multi-team agentic coding** — specialized *teams* (not just specialized agents) behind one interface.
- **Failure:** thinking this is "Claude Code subagents renamed." The unit here is the specialized **team** plus a single orchestrator; your cognitive load stays flat as you add specialists.
- **Retrieval:** *What makes you the bottleneck in single-agent coding, and what removes it?* (You are the orchestrator; a real orchestrator agent + team hierarchy removes it.)

### 3.2 The three tiers (depth-2 delegation)
- **Hook:** watch a lead try to do the work itself — and get *rejected*.
- **Picture:** frame **t0185** — the Engineering Lead's file tool calls show **red ✗** (domain-blocked); it says *"I have restricted tool access as a lead — let me delegate this to my team members who have the right tools,"* then `@Backend Dev` takes over. Three tiers visible in one screen.
- **Worked example:** "have engineering present a tree of the most important files" → Eng Lead blocked → delegates to Frontend + Backend Dev → they read the codebase → lead synthesizes → orchestrator reports.
- **Name:** **depth-2 delegation** — User → Orchestrator → Leads → Workers.
- **Failure:** assuming "deeper = better." Two levels is the sweet spot (OPUS.md); depth is hard-capped in code (a lead's `delegate` tool self-disables inside worker subprocesses).
- **Retrieval:** *Which tier runs bash and mutates code?* (Only workers.)

### 3.3 Leads delegate, never execute (zero micro-management)
- **Hook:** the lead is a *thinker*, not a *builder*.
- **Picture:** the `zero-micro-management` skill: "If you catch yourself about to use `write`, `edit`, or `bash` — stop and delegate instead."
- **Worked example:** `run head-to-head` → orchestrator can't do it → delegates to Engineering → the lead can't execute → passes to Backend Dev, who actually runs the eval.
- **Name:** **zero micro-management.**
- **Failure:** reading the lead's block as waste. It's the mechanism that routes work to the specialist with the right tools **and** the compounding domain memory.
- **Retrieval:** *Name the soft and hard enforcement of "leads don't execute."* (Soft: the skill. Hard: domain rules + the enforcer extension.)

### 3.4 Domain ownership / domain locking
- **Hook:** "No one should be touching the DevOps files except the DevOps agent."
- **Picture:** frame **t1290** — `frontend-dev.md` with a `domain:` block that lets it write to `apps/frontend/` but only **read** the rest of `apps` — the exact "read the back-end, never touch it" rule Dan types live.
- **Worked example:** each agent declares per-path `read` / `upsert` / `delete`. Planning leads read everything and write nothing but their own memory; QA/Security read code but never mutate it; backend/frontend devs write only their directories.
- **Name:** **domain locking** — "the holy grail of operating mid-to-large codebases."
- **Failure:** believing it's just a prompt instruction the model might ignore. It's a Pi extension (`domain-enforcer.ts`) that structurally blocks out-of-domain read/write/delete tool calls **and** heuristically blocks bash write/delete commands.
- **Retrieval:** *What three permissions does a domain rule grant, and is it prompt-only?* (read / upsert / delete; not prompt-only — structurally enforced.)

### 3.5 Agent experts + compounding memory
- **Hook:** "Agent experts will always outperform a generic agent."
- **Picture:** frames **t0232** (the specialized 10-agent roster) and **t1420** (the session log where the team wrote `head-to-head-results.md`).
- **Worked example:** each agent has an **expertise** YAML — its mental model. It reads it on boot, updates it after work, and the knowledge **compounds** every session (backend dev remembers backend patterns; QA remembers failure modes). You add read-only expertise (`updatable: false`) for billing / migrations / DevOps that nobody can corrupt.
- **Name:** **mental models / agent experts.**
- **Failure:** (1) thinking it's Claude-style "remember everything I ever said" — no, it's narrow, domain-specific, per-agent. (2) Micro-curating the files — Dan says *let go*; the `mental-model` skill is ~76 lines of guidance, and agents self-maintain within a `max-lines` cap.
- **Retrieval:** *In the shipped repo, what state are the expertise files in?* (Empty — 0 lines; agents build them per codebase. Dan's on-screen 5,000-token model was from a previous codebase.)

### 3.6 Composable skills
- **Hook:** change one line, change many agents.
- **Picture:** frame **t1180** — searching for `active-listener.md` returns **"10 results in 10 files"** — every agent shares that one skill.
- **Worked example:** `active-listener` (read the conversation log before every response) is shared by all 10; `conversational-response` (Slack-concise) is given to leads/orchestrator but withheld from workers so workers stay verbose; `zero-micro-management` goes only to leads/orchestrator.
- **Name:** **skills composition** — the control surface.
- **Failure:** treating skills as inert prompt snippets. They're how you retune the whole fleet cheaply: "There could be an agent somewhere that we don't want to always active-listen. We want it to be independent."
- **Retrieval:** *Which skill do all 10 agents share, and which is withheld from workers (and why)?* (Shared: active-listener. Withheld: conversational-response — workers stay verbose/detailed.)

### 3.7 Configuration-driven teams
- **Hook:** "Really is as simple as updating the configuration file."
- **Picture:** the `multi-team-config.yaml` roster + the file tree (`.pi/multi-team/agents|expertise|skills|sessions`).
- **Worked example:** kill the app, edit the config to drop the Validation team, relaunch → "now it's just planning and engineering." Add a DevOps team by copying the pattern.
- **Name:** **config-driven teams** on the **customizable Pi harness** (`.pi` vs `.claude`).
- **Failure:** assuming domain/skills/expertise live in the YAML. They **don't** — the YAML holds only the roster + `consult-when` routing; each agent's model/tools/skills/expertise/domain live in that agent's `.md` frontmatter. The repo ships 5 preset configs (default, engineering-only, planning+engineering, plan + 3× scaled engineering, and an open-source multi-provider config).
- **Retrieval:** *Where does an agent's domain live — the config or the agent file?* (The agent `.md` frontmatter.)

### 3.8 Model tiering + spend to win
- **Hook:** "$8 for this agent team?!"
- **Picture:** frame **t1610** — real ML results delivered by the team, footer showing **Orch $8.280** total, Opus leads / Sonnet workers.
- **Worked example:** leads/orchestrator on Opus (coordination needs the best intelligence), workers on Sonnet (follow instructions + execute). Overridable per agent via config `model:` (the `opensource` config points 9 agents at 9 different provider models).
- **Name:** **model tiering + spend-to-win.**
- **Failure:** fixating on cost. Dan: *"You're thinking about right now. You're not thinking far enough into the future… I am not spending enough tokens, you are not spending enough tokens, and you are wasting time doing things the old way."*
- **Retrieval:** *What's Dan's answer to "this is expensive"?* (Spend more; cost/intelligence is moving in your favor; the old single-agent way is finished.)

### 3.9 Conversation awareness + session workspace
- **Hook:** "Every agent is aware of the conversation happening."
- **Picture:** frame **t1420** — the actual `conversation.jsonl` (rows with `from`/`message`/`to`/`type`/`timestamp`) plus the per-session directory with per-team folders and the artifacts the team wrote.
- **Worked example:** copy the session ID → open `sessions/<id>/conversation.jsonl` → read the entire multi-agent exchange. The `active-listener` skill makes every agent load recent history before responding.
- **Name:** **conversation awareness** + the **session directory** as shared workspace.
- **Failure:** thinking each agent is a private black box. The shared log is what keeps the team coordinated and observable.
- **Retrieval:** *What file makes the whole team's exchange observable, and what skill uses it?* (`conversation.jsonl`; the active-listener skill.)

### 3.10 Trust and scale (the 2026 close)
- **Hook:** "The name of the game in 2026 is trust and scale."
- **Picture:** frame **t0955** — the validation team autonomously reviews and returns "Ship it. No blocking issues."
- **Worked example:** raise trust until you *know* the team ships on enter; then scale — how big, how surgical. Compounding, domain-locked agent experts drive both.
- **Name:** **trust → scale.**
- **Failure:** thinking trust comes from watching more closely. It comes from building specialized, domain-locked, memory-compounding experiences and then letting go.
- **Retrieval:** *What are the two moves of 2026, in order?* (Trust, then scale.)

---

## 4. The worked demo (the classifier)

The teams operate **on** a separate **prompt-routing / prompt-complexity-classifier** codebase (data-science / scikit-learn). **It is NOT shipped** in the lead-agents repo — Dan deploys the multi-team tool *into* it via the `teams` alias. The classifier's job: predict whether a prompt needs a **low / mid / high** intelligence model so you "don't pay for intelligence you don't need."

The thread you can point at, frame by frame:
1. `just predict "summarize this codebase"` → **Label: MID**, confidences `{high 0.35, low 0.19, mid 0.45}`, routes to `claude-sonnet-4-6` (frame **t0337**).
2. "Ask all teams: two more scikit-learn classifiers to benchmark" → the orchestrator writes the **same** domain-tailored prompt to all 3 teams → consensus (LinearSVC, CalibratedClassifierCV; Engineering adds SGDClassifier; ComplementNB as challenger) (frame **t0408**).
3. "plan, engineer, then validate" → Planning drafts → Backend Dev implements the benchmark → QA + Security review → Security "ship it," QA finds extra items (frame **t0955**).
4. `run head-to-head` → LR owns LOW (80% vs 67%), ComplementNB owns MID (86% vs 76%), both perfect on HIGH; "LR stays as default, CNB a credible challenger"; results written to `sessions/<id>/head-to-head-results.md` (frame **t1610**).

Design nuance worth teaching: the classifier is deliberately **biased toward predicting HIGH** as a safe default — mispredicting LOW/MID when you truly needed HIGH is the costly, user-hurting error.

---

## 5. How it actually works (the harness internals)

For the chapter's "under the hood" box — all read from source (`apps/multi-team-chat/extensions/`), corroborated by the two specs:

- **The nuclear UI pattern.** `multi-team-chat.ts` (1,432 lines) doesn't theme Pi — it *replaces* Pi's display layer: inside `session_start` it reassigns `tui.children[1] = chatView` (custom chat) and blanks `[2]`/`[3]`. The agent brain stays; the whole UI is Dan's.
- **Delegation = subprocesses.** Each tier is the *same* `pi` binary spawned as a subprocess: `callAgent()` runs `pi --mode json -p --no-extensions -e domain-enforcer -e lead-delegate -e tilldone-lead --no-skills --no-prompt-templates --no-themes --session <file>` (and, first run only, `--system-prompt`/`--model`). Sessions are persistent JSONL — the system prompt is set once and resumed after.
- **The env-var handshake caps depth.** Three extensions load on *every* subprocess and each self-exits unless its trigger env var is present: `domain-enforcer` (`AGENT_DOMAIN_RULES`), `lead-delegate` (`LEAD_MEMBERS_JSON`), `tilldone-lead` (`TILLDONE_TASKS`). A lead deletes `LEAD_MEMBERS_JSON` before spawning members → members can't re-delegate. That's the hard depth cap.
- **`delegate` and `tilldone` are custom Pi tools.** The orchestrator's `delegate(teams, question)` accepts a team name, a list, or `"all"`; it runs `Promise.allSettled` over the targets and streams each lead's output into a live chat bubble. `tilldone` gives the orchestrator a visible task list; leads get a reduced `start`/`done`/`list` variant.
- **The domain enforcer is structural.** `domain-enforcer.ts` blocks `tool_call`s: an allowlist (`AGENT_ALLOWED_TOOLS`), per-path `isAllowed(path, read|upsert)` (expertise files first, then directory rules; `.` root is special; *no matching rule = deny*), and bash write/delete regex heuristics. On `tool_result` it re-reads expertise files and warns if over `max-lines`.
- **Runtime variable injection.** `config.ts`/`prompt.ts` fill `{{SESSION_DIR}}`, `{{CONVERSATION_LOG}}`, `{{TEAMS_BLOCK}}`/`{{MEMBERS_BLOCK}}`, `{{EXPERTISE_BLOCK}}`, `{{SKILLS_BLOCK}}` into each system prompt at startup — this is the "controlling the core four down to the system-prompt level" Dan describes.
- **Two orchestration models coexist — don't conflate them.** The Pi **runtime** uses `delegate`/`tilldone` + `pi` subprocesses (the lesson's subject). The `.claude` tooling (`plan-w-team.md`, `meta-pi-agent.md`, and the specs' "Team Orchestration / Task*" sections) uses the **Claude Code Task\*** tools to *build* the system. Claude Code is the **bootloader** (`/install`, `/install-into-codebase`); Pi is the runtime.

Two real engineering artifacts make excellent "this is real, not a demo" material:
- `specs/fix-worker-cost-tracking.md` — a real bug: worker costs were silently dropped, so the footer showed **$8.79 vs a real $34.28** (~25% of spend). Three-layer fix. Perfect "spend to win, *but track your spend*" tension.
- `specs/tilldone-multi-team-integration.md` — the full plan for adding the task-tracking system (parent canonical state, lead mutations via `onToolUpdate`, two-column footer, `agent_end` nudge).

---

## 6. Codebase orientation (what the student is looking at)

The shipped repo **is the tool.** Highest-value files to read, in order:
1. `README.md` — the definitive written companion (why multi-team, setup, architecture, memory, domain, skills, config, tilldone, conversation awareness, emoji legend).
2. `.pi/multi-team/multi-team-config.yaml` — the roster.
3. `.pi/multi-team/agents/orchestrator.md` → `planning-lead.md` → `backend-dev.md` — read one of each tier and diff the frontmatter (model / tools / skills / domain).
4. `.pi/multi-team/skills/*.md` — the 6 composable behaviors.
5. `OPUS.md` — architecture reflections + roadmap (parallel delegation).
6. `apps/multi-team-chat/extensions/` — the harness internals (see §5).
7. `justfile` — how to launch (`just team`, `team-eng`, `team-pe`, `team-scale`, `team-oss`).

Full file-by-file map in `extract.json` → `codebase_map`.

---

## 7. Pointers
- **Quotable insights & distilled ideas:** `nuggets.md`
- **Version drift + current-practice notes:** `outdated-vs-current.md`
- **Gradable lab (course codebase only):** `lab-spec.md`
- **Frames (11, all 4K, verified on disk):** `frame-plan.json` and `media/frames/ma-2-lead-agents/`
- **YouTube overlays (2 phase-1, real IDs from the lesson's own description):** `extract.json` → `yt_overlay_candidates`

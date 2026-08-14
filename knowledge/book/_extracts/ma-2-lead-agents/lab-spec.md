# Lab — Multi-Team Agentic Coding / Lead Agents (`ma-2-lead-agents`)

**Goal:** operate, inspect, and reconfigure the multi-team system until you can explain the 3-tier architecture, domain locking, skills composition, and model tiering **without notes** — and prove each with evidence you produced.

## Scope contract (read first)
- **Course codebase only.** The shipped `lead-agents` repo **is the tool** (a Pi extension + `.pi/multi-team/` team definitions). The scikit-learn *prompt-routing classifier* codebase Dan operates on in the video is **NOT shipped** — so this lab runs the tool **against its own source repo** (exactly what `README.md` → "Step 2: Test Locally" prescribes). Do not try to reproduce the classifier benchmark.
- **No PiCanvas. No destructive Git/`rm` improvisation.** Restore any file you edit.
- **This costs tokens.** Even a light session can run several dollars. Have `ANTHROPIC_API_KEY` funded or a Claude plan. Keep test prompts small.
- Every checkpoint below is **gradable** — it has an explicit, checkable pass condition.

---

## Setup

1. **Prereqs on PATH:** Claude Code (`claude`), Pi (`pi` or `ipi`), `bun`, `node`, `just`. Confirm: `claude --version`, `pi --version` (or `ipi --version`), `bun --version`, `just --version`.
2. **`.env`:** create `.env` from `.env.sample`; set `ANTHROPIC_API_KEY=...` (required). Optional provider keys only if you'll run the multi-provider config.
3. **Install:** from the repo root run `/install` inside Claude Code (or `just install`). It checks prereqs, verifies `.env`, runs `bun install`, validates the config + agent files, and adds a shell alias (default `teams`) to your profile. Reload your shell.
4. **Say the permissions out loud before launching:** open `.pi/multi-team/agents/orchestrator.md` and read its `domain:` block. What can the orchestrator read? What can it write? (Answer: read everything; write only its own expertise.)

---

## Checkpoint 0 — Launch + ping (the single interface)
- Run `just team` (default 3-team config against this repo). Wait for the chat room to boot.
- Type `ping`.
- **Pass:** only the **Orchestrator** responds (a pong-style message confirming Planning/Engineering/Validation are online), and the footer shows an Orchestrator line with cost + context tokens. You did **not** talk to any worker directly. *(Matches frame t0118.)*

## Checkpoint 1 — Three-tier delegation + a domain block
- Type: `ping each team lead`. Observe the two-layer fan-out (Orchestrator → 3 leads) and the footer summing lead costs.
- Then type: `have engineering present a tree structure of the most important files in this repo`.
- **Pass:** you observe the **Engineering Lead** attempt file access, get **domain-blocked** (visible ✗ / "restricted tool access as a lead"), and **delegate to a worker** (Backend/Frontend Dev) that actually reads the tree — three tiers in one exchange, results synthesized back up. *(Matches frame t0185.)*
- **Record:** one sentence — *why* did the lead delegate instead of reading the files itself?

## Checkpoint 2 — Reveal the full team (cost + model tiering)
- Type `/toggle-workers`.
- **Pass:** the footer/tree shows **all 10 agents** (Orch + 3 leads + 6 workers), each with its own **cost** and **model**; you can point to **Opus for orchestrator+leads** and **Sonnet for workers**. *(Matches frames t0232 / t1610.)*
- **Record:** the per-agent model tier and the total (orchestrator) cost at this moment.

## Checkpoint 3 — Multi-perspective (consistent fan-out)
- Ask a repo-relevant question of all teams, e.g.: `ask all teams: what is the single biggest risk in this codebase's architecture, and why?`
- **Pass:** the Orchestrator delegates the **same** (domain-tailored) question to all three teams and returns **one** synthesized answer noting consensus/splits — you never addressed a team directly. *(Matches frame t0408.)*

## Checkpoint 4 — Read the anatomy (where the config lives)
- Open and compare `orchestrator.md`, `planning-lead.md`, and `backend-dev.md` frontmatter, plus `.pi/multi-team/multi-team-config.yaml` and two skills (`zero-micro-management.md`, `active-listener.md`).
- **Pass:** you can answer, from the files:
  1. Which tier has `bash` and which does not? *(Workers do; leads/orchestrator don't.)*
  2. Where does an agent's **model / tools / skills / domain** live — the YAML or the agent `.md`? *(The agent `.md` frontmatter; the YAML holds only the roster + `consult-when`.)*
  3. Which skill is shared by **all 10** agents, and which is **withheld from workers** (and why)? *(Shared: `active-listener`. Withheld: `conversational-response` — workers stay verbose.)*

## Checkpoint 5 — Conversation awareness (the shared log)
- Find the current session's directory under `.pi/multi-team/sessions/<session-id>/` and open `conversation.jsonl`.
- **Pass:** you can see rows from **every tier** (user, orchestrator, leads, members) with `from`/`message`/`type`, proving every agent can load the shared conversation. *(Matches frame t1420.)*

---

## Stretch drills

### S1 — Prune a team (config-driven)
Kill the app. Either run `just team-pe` (Planning + Engineering preset) **or** copy `multi-team-config.yaml`, delete the Validation team block, and launch it with `just teamc <your-config>`. **Pass:** the relaunched roster shows **only** the remaining teams (no Validation lead/workers in the tree).

### S2 — Add a team (config-driven)
In a copy of the config, add a new team block (e.g. a "DevOps" team) pointing its lead/members at existing agent `.md` files (reuse engineering-lead + backend-dev is fine for the drill), give it a distinct color and `consult-when`. Launch with `just teamc <your-config>`. **Pass:** the Orchestrator lists/uses the new team when you ask something in its domain.

### S3 — Domain-lock experiment (the hard gate)
Edit `frontend-dev.md`'s `domain:` to scope writes to `apps/frontend/` only (read-only on the rest of `apps/`), mirroring the video (frame t1290). Relaunch, then via the Orchestrator ask Engineering to have the **Frontend Dev** write a file **outside** `apps/frontend/`. **Pass:** the `domain-enforcer` **blocks** the write (you see a refusal/blocked tool call), demonstrating the hard gate is structural, not prompt-only. **Restore** `frontend-dev.md` afterward.

### S4 — Model override precedence
Run `just team-oss` (multi-provider preset) **or** add a config-level `model:` to one agent in a config copy. **Pass:** that agent runs on the **overridden** model (visible in the tree), proving config `model:` beats the agent's frontmatter `model:`. *(Requires the relevant provider key in `.env` for `team-oss`.)*

### S5 — Read-only expertise
Add a second expertise entry to one worker with `updatable: false` (e.g. a "deploy-checklist.yaml" with a couple of lines) and reference it in `use-when`. Ask that agent to modify that file. **Pass:** the agent can **read** it but is **blocked from writing** it (read-only expertise is enforced by the enforcer's expertise check). Alternatively, observe `max-lines` enforcement by inspecting the `mental-model` skill's line-limit rule. Restore afterward.

### S6 — Scale horizontally (advanced)
Run `just team-scale` (Planning + **3 parallel Engineering teams**). **Pass:** the tree shows Engineering1/2/3, each with its own lead + FE + BE — team count is a config knob. (Watch the cost; keep the prompt trivial.)

### S7 — Meta build (advanced, optional)
Boot the meta agent with `just metacc` (Claude Code) or `just metapi` (Pi) and ask it to scaffold one new specialized agent + wire it into a config. **Pass:** a new agent `.md` + config entry that launches. *(This exercises the Claude Code build harness — distinct from the Pi runtime.)*

---

## Pass criteria (final sheet — all must be true)
1. The system is installed and launches (`just team` / your `teams` alias); `ping` returns an **Orchestrator-only** response with cost in the footer.
2. You **witnessed a lead get domain-blocked and delegate to a worker** (the three-tier cascade) and can explain why in one sentence.
3. `/toggle-workers` showed **all 10 agents** with per-agent cost and the **Opus-leads / Sonnet-workers** tiering; you recorded the tiers and total cost.
4. You **reconfigured the roster via YAML** (pruned S1 or added S2 a team) and relaunched successfully.
5. You **triggered a `domain-enforcer` block** (S3) by asking an agent to write outside its domain, then **restored** the file.
6. You opened `conversation.jsonl` and confirmed **every tier's** messages are logged.
7. Without notes you can state: the **3 tiers + what each may/may not do**; **where** model/tools/skills/domain live (agent frontmatter, not the config); the **soft vs hard** enforcement of "leads don't execute"; and **Dan's answer to the cost objection** (spend more; cost/intelligence trends favor you).

---

## Troubleshooting (keyed to the real mechanics)
| Symptom | Likely cause | Fix |
|---|---|---|
| "Ghost" / duplicate messages when re-testing | Reused a live Pi/tmux session | Per `CLAUDE.md`: fully kill + recreate the session between runs; wait for the orchestrator to go idle before sending the next prompt. Prefer bun over npm. |
| Launch dies immediately | Missing `.env` or `ANTHROPIC_API_KEY` | `config.ts` `loadDotEnv` **throws** if `.env` is absent. Create it from `.env.sample` and set the key. |
| "FATAL"/crash naming an agent file | An agent `.md` referenced by the config is missing/renamed | `loadAgentConfig` throws on a missing agent file. Fix the path in your config or restore the `.md`. |
| A worker "refuses" / a write silently doesn't happen | The `domain-enforcer` blocked an out-of-domain tool call | Check that agent's `domain:` block. This is the feature (S3), not a bug. |
| Footer cost looks suspiciously low | Worker-cost propagation edge (see `specs/fix-worker-cost-tracking.md`) | Costs are captured across three layers; if a build predates that fix, worker costs can under-report (~25%). Cross-check against your API dashboard. |
| A lead tries to write code and stalls | Working as designed | Leads have no execution domain — they must `delegate`. This is the three-tier boundary. |
| Provider agent (team-oss) errors | Missing provider key | Add the relevant `OPENROUTER_/OPENAI_/GEMINI_` key to `.env`, or use the default Anthropic config. |

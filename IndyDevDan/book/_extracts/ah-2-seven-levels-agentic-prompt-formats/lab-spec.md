# AH-2 Lab Spec — Seven Levels of Agentic Prompt Formats

**Scope rule:** every drill runs inside the course codebase only (`codebase/` → `agentic-horizon/agentic-prompt-engineering`, from the lesson loot box). No external repos. Some prompts need external services (Replicate/Firecrawl MCP) — those are **read-and-analyze only** unless you already have the keys; nothing in the pass criteria requires them.
**Prime directive (graded throughout):** you reason about every prompt as a stack of **composable sections** and a **level**, and you keep the format **consistent** — no novel structure per prompt.
**Time box:** 60–90 minutes. Token cost: booting the app is free; a handful of small agent runs (prime, build, parallel at count=3, one metaprompt generation).

---

## 0 · Setup (10 min)

1. Open the lesson codebase in your IDE; open the terminal; run `claude`.
2. Verify the toolbelt: `claude --version`, `bun --version`, `git --version`.
3. **Boot the tier-list app** (this is the app Dan grades on screen): run the Level-1 prompt `/start` — or by hand: `cd apps/prompt_tier_list && bun install && bun run dev`, then open `http://localhost:5173/`.
4. **Prime the codebase:** run `/prime` (general) then `/prime_tier_list` (the app specifically). Read the summaries the agent returns.

**Checkpoint 0:** the tier-list grid is open in your browser, and you can name — from the primed summary — the two axes (X = Beginner→Expert skill; Y = Useful→Useless usefulness) without looking.

---

## 1 · Grade the tier list yourself, then check Dan (15 min)

In the app, drag **all 13 sections and all 7 formats** from the SECTIONS & FORMATS pool onto the grid where *you* think they belong. Then compare against the answer key (`extract.json → tier_list`, verified from frame `t2740`).

**Answer key — pillar positions you must get right:**

| Entity | Useful | Skill |
|---|:--:|:--:|
| `## Workflow` | S | C |
| `## Template` | S | S |
| `## Variables` | A | B |
| `## Expertise` | A | A |
| `## Report` | B | C |
| `# Title` | C | D |
| `workflow_prompt.md` | A | C |
| `control_flow_prompt.md` | A | B |
| `delegate_prompt.md` | S | A |
| `higher_order_prompt.md` | B | A |
| `template_metaprompt.md` | S | S |
| `self_improving_prompt.md` | A | S |

**Checkpoint 1 (write it down):** explain in one sentence why `## Workflow` (S useful / C skill) is the *bargain* of the whole grid, and why `## Template` sits alone in the S/S cell.

---

## 2 · Classify every prompt by level (codebase audit) (15 min)

Open each `.claude/commands/*.md` prompt, **collapse to its H2s**, and fill in this table. Use `README.md` (§ "The 7 Levels") as the answer key.

| Prompt | Level(s) | Key section that sets the level |
|---|---|---|
| `all_tools.md` | 1 | (title + high-level prompt only) |
| `start.md` | 1 | + Purpose |
| `prime.md` | 2 | Workflow |
| `prime_tier_list.md` | 2 | Workflow + Codebase Structure |
| `quick-plan.md` | 2 | Workflow + Variables + Instructions |
| `build.md` | 2 → 3 → 5 | Workflow; line-17 early return; plan passed in |
| `create_image.md` | 3 | Workflow with `<image-loop>` + STOP conditionals |
| `edit_image.md` | 3 | loop + conditionals, **no Report** |
| `parallel_subagents.md` | 4 | designs sub-agent prompts, Task fan-out |
| `load_ai_docs.md` | 4 | calls `@agent-docs-scraper` per URL |
| `background.md` | 4 | fires a background `claude` CLI + `--append-system-prompt` |
| `load_bundle.md` | 5 | accepts a bundle file as input |
| `t_metaprompt_workflow.md` | 6 | `## Specified Format` template |
| `plan_vite_vue.md` | 6 | large `## Plan Format` template |
| `experts/cc_hook_expert/cc_hook_expert_plan.md` | 7 | dynamic `## Expertise` |

**Checkpoint 2:** for `build.md`, name the exact line that makes it a Level-3 control-flow prompt, and the thing you pass in that makes it Level-5. *(Line 17 STOP/early-return; a plan file as `PATH_TO_PLAN`.)*

---

## 3 · Static vs dynamic variables (10 min)

Open `quick-plan.md` and `create_image.md`. For every variable, label it **static** or **dynamic**:
- `quick-plan.md`: `USER_PROMPT: $1` → dynamic; `PLAN_OUTPUT_DIRECTORY: \`specs/\`` → static.
- `create_image.md`: `IMAGE_GENERATION_PROMPT: $1`, `NUMBER_OF_IMAGES: $2` → dynamic; `IMAGE_OUTPUT_DIR`, `MODEL: google/nano-banana`, `ASPECT_RATIO: 16:9` → static.

Then, **via Claude Code (not by hand)**, change `quick-plan.md`'s static `PLAN_OUTPUT_DIRECTORY` from `specs/` to `prd/`. Confirm the plan now writes to `prd/` and that you only had to edit **one line**.

**Checkpoint 3:** state the one-sentence payoff of a static variable. *(Change it in one place and every reference updates — for you, your team, and your agent.)*

---

## 4 · Run one prompt at each of Levels 1–4 (20 min)

1. **L1** — `/all_tools`. Verify the agent lists its tools in TypeScript-signature format. *(Runs in any agent; this is your "what can it see" probe.)*
2. **L2** — `/prime`. Verify it runs `git ls-files`, reads `README.md`, and returns a codebase summary — exactly the two workflow steps, nothing more.
3. **L3** — `/build` **with no argument**. Verify the early return fires: the agent STOPs and asks you for a `PATH_TO_PLAN` instead of guessing. *(This is control flow you can trigger on purpose.)*
4. **L4** — `/parallel_subagents "audit .claude/commands and report each prompt's level" 3`. Verify **three** sub-agents launch in one batch, each gets a self-contained prompt, and the primary agent synthesizes their results.

**Checkpoint 4:** in the L4 run, quote one sentence the primary agent wrote *as a prompt for its sub-agents.* *(Proves the primary agent is the prompt engineer for its sub-agents.)*

---

## 5 · Level 6 — make the agent write a prompt (15 min)

Run the Template Metaprompt to generate a **new Level-2 workflow prompt**:

`/t_metaprompt_workflow "a prompt that lists every TODO comment in the codebase and writes them to todos.md"`

Verify the generated file:
- lands in `.claude/commands/` with a sensible name;
- follows the `## Specified Format` **exactly** (metadata → title → purpose → Variables → Workflow → Report), with no extra sections;
- has dynamic variables before static, `$1/$2` preferred over `$ARGUMENTS`.

**Checkpoint 5:** confirm the generated prompt is a valid Level-2 workflow prompt (has a real `## Workflow`) and that its format matches your other prompts. *This is the peak-leverage move: a prompt that builds prompts.*

---

## 6 · Stretch drills (still consistent, still composable)

**S1 — Promote L2 → L3.** Take `prime.md` (Level 2) and, via Claude Code, add a conditional to its Workflow (e.g. "If `README.md` is missing, STOP and report"). Confirm it's now a control-flow prompt without changing any other section.

**S2 — Touch the self-improving loop (read-first).** Open the `cc_hook_expert` triplet. Trace how `cc_hook_expert_improve.md` updates **only** the `## Expertise` sections of `_plan`/`_build` and leaves their Workflows stable. Write one sentence on why "only Expertise changes" is the safety rule of Level 7.

**S3 — Find the system prompts.** Open `.claude/agents/docs-scraper.md` (a sub-agent = a system prompt). List which sections it uses (Purpose, static Variables, Workflow, Report). Then, from `README.md § System Prompts vs User Prompts`, name three sections you would **avoid** in a primary-agent system prompt (Variables, Report, Expertise/Templates, Metadata) and why.

**S4 — Transfer to your job.** Pick a task you do ≥3×. Write it as a **Level-1** high-level prompt. Then rewrite it as a **Level-2** workflow prompt (add Variables + Workflow + Report). Save both; note which sections you *didn't* need.

---

## Pass criteria (all required)

- [ ] Tier-list pillar cells match the answer key (Checkpoint 1)
- [ ] Prompt-level audit table correct for all listed prompts (Checkpoint 2)
- [ ] Every variable in the two prompts correctly labeled static/dynamic; static-var edit propagated from one line (Checkpoint 3)
- [ ] `/all_tools`, `/prime`, `/build` (early-return), and `/parallel_subagents 3` each produced the expected observable behavior (Checkpoint 4)
- [ ] `/t_metaprompt_workflow` generated a valid Level-2 workflow prompt in the exact Specified Format (Checkpoint 5)
- [ ] Oral check, no notes: name the seven levels + the one capability each adds; state why Workflow is most-useful/mid-skill; explain why the tier grades apply to **user** prompts only

---

## Instructor / self-check notes

- **Most common stall:** confusing the **Workflow** section (executed play-by-play) with **Instructions** (auxiliary notes), or **Codebase Structure** (a map you do NOT read) with **Relevant Files** (you do read). Force the distinction in Checkpoint 2.
- **Second stall:** trying to *run* `create_image.md`/`edit_image.md`/`load_ai_docs.md` without Replicate/Firecrawl configured. These are analyze-only; don't put them on the critical path.
- **Model drift:** `quick-plan.md`/`background.md` pin `claude-opus-4-1-20250805`. If a student's Claude Code rejects the id, that's the "period detail — swap the model in Metadata" lesson surfacing (see outdated-vs-current §2).
- **Capture-vs-code gotcha:** the video shows `t_metaprompt_workflow.md`'s purpose saying "Instructions"; the shipped file says "Workflow." If a sharp student notices, that's Dan's live correction — reward it.
- **What this lab intentionally does NOT cover:** the Claude Code SDK / system-prompt overwrite (AH-3), worktree-isolated parallel agents (AH-4), and Agent Skills packaging — later material. Keep the seven levels crisp; deflect scope creep.

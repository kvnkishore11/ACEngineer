# Extract — AH-2 · Seven Levels Agentic Prompt Formats

> **Course:** Agentic Horizon (AH) · order 10 · `agentic-horizon/agentic-prompt-engineering`
> **Runtime:** 57:21 · 1920×1080 · **Tactic:** *Master the seven agentic prompt formats.*
> **One line:** The prompt is the fundamental unit of engineering — so stop writing one-off prompts and start building a library of reusable, consistently-structured agentic prompts assembled from a fixed set of swappable "Lego-block" sections, scaled level by level from a one-line ad-hoc prompt up to a prompt that writes and improves your other prompts.

This extract is the **technical-accuracy source** for the chapter. Every claim is cross-checked against the transcript, the codebase, and the on-screen tier list. Teaching prose/HTML is written downstream (Codex); here the goal is *correctness + weak-student scaffolding*.

---

## 0. The frame: who are you writing prompts for?

**Hook.** You already know prompt engineering was mocked as a joke. Here's the reversal: with agents, *every line of a prompt can fire tens to hundreds of tool calls and run for minutes to hours.* One well-crafted prompt can generate hundreds of hours of productive work — and one bad prompt compounds failure at the same rate. That leverage makes agentic prompt engineering one of the most important engineering skills of the age of agents.

**Picture.** `t0052-stakeholder-trifecta.jpg` — a slide with three nodes: **You**, **Your Team**, **Your Agents**.

**Worked example.** When Dan writes `prime.md`, three readers must understand it instantly: *future Dan* (collapse to the H2s, read the top, know what it does), *a teammate* (could they run it top to bottom cold?), and *the agent* (does the Workflow map cleanly onto its todo list?).

**Name it — the Stakeholder Trifecta.** *"We're now engineering for three audiences, you, your team, your agents. This is the stakeholder trifecta for the age of agents."* The agent is the newest — and most important — consumer of your work.

**Failure mode.** Treating prompts as private scratch work. In the age of agents a prompt is shared infrastructure; write it like an interface, not a sticky note.

**Retrieval.** *Who are the three stakeholders, and which matters most?* → You, your team, your agents; the agents (they execute), with clear communication to all three.

---

## 1. The two ideas the whole lesson rests on

### 1a. The prompt is the fundamental unit of engineering
- **Name:** *the prompt is the fundamental unit of engineering.*
- **Why it's true now:** agentic prompts drive long tool chains, so the prompt (not the function or file) is the atom of engineering work.
- **Quote:** *"The prompt is now the fundamental unit of engineering. And with agents, every prompt you create becomes a force multiplier."*
- **Consequence:** engineers who create more and better prompts at scale are the winners.

### 1b. Composable sections = swappable Lego blocks
- **Hook:** what if every prompt you ever wrote was built from the *same* ~13 named parts, and you just swapped parts in and out?
- **Picture:** `t0765-quick-plan-collapsed-sections.jpg` — a prompt collapsed to its H2 headers: `## Variables`, `## Instructions`, `## Workflow`, `## Report`. A stack of blocks, not a wall of text.
- **Name:** *composable sections.* There are 13 (from `entities.ts`): `# Title`, `## High Level Prompt`, `## Metadata`, `## Purpose`, `## Variables`, `## Instructions`, `## Relevant Files`, `## Codebase Structure`, `## Workflow`, `## Expertise`, `## Template`, `## Examples`, `## Report`.
- **Rule:** *only add the sections you need.* You can name them anything; Dan uses "the most consistent, the most information dense keywords."
- **Failure mode:** believing you must use every section, or that section names are law. The discipline is *composability + consistency*, not completeness.
- **Retrieval:** *Do you have to use every section?* → No — add only what you need; drop Report if you don't care about output, drop Variables if nothing comes in.

---

## 2. The seven levels (each adds exactly one capability)

The levels **stack**: every level inherits the sections below it and adds one new capability. Reach for the **lowest level that does the job** — "usually level three, level four is all you need." Levels 1–4 are 80–90% of real work; 5–7 are "meta" territory.

| Lv | Format | New capability | Example prompts | Tier (useful / skill) |
|----|--------|----------------|-----------------|----------------------|
| 1 | **High Level Prompt** | Reusable ad-hoc one-off | `all_tools.md`, `start.md` | B / D |
| 2 | **Workflow Prompt** | Sequential input→work→output | `prime.md`, `build.md`, `quick-plan.md`, `prime_tier_list.md` | A / C |
| 3 | **Control Flow Prompt** | Conditions, loops, early returns | `build.md`, `create_image.md`, `edit_image.md` | A / B |
| 4 | **Delegate Prompt** | Fires other agents | `parallel_subagents.md`, `load_ai_docs.md`, `background.md` | S / A |
| 5 | **Higher Order Prompt** | Accepts another prompt/file as input | `build.md`, `load_bundle.md` | B / A |
| 6 | **Template Metaprompt** | Writes a new prompt in a set format | `t_metaprompt_workflow.md`, `plan_vite_vue.md` | S / S |
| 7 | **Self-Improving Prompt** | Updates its own Expertise | `experts/cc_hook_expert/*.md` | A / S |

> Tier axes: **usefulness** S(top)→D(bottom); **skill** D=Beginner(left)→S=Expert(right). Verified against `t2740-final-tier-list.jpg`.

### Level 1 — High Level Prompt
**Hook:** the moment you do something a third time, stop retyping it. **Picture:** `t0250-l1-all-tools-prompt.jpg` — `# List All Tools` + one paragraph. **Worked example:** `all_tools.md` asks the agent to read its own system prompt and list every tool in TypeScript-signature format; runs in *any* chat interface. `start.md` adds a Purpose line + steps (`cd apps/prompt_tier_list; bun install; bun run dev`). **Name:** reusable, ad-hoc, static prompt (1–3 sections: Title, high-level prompt [required], Purpose). **Failure:** ending here — "a great place to start, a terrible place to end." **Retrieval:** *When do you write a Level-1 prompt?* → When you notice repeat work an agent can do cleanly ("three times marks a pattern").

### Level 2 — Workflow Prompt (the pillar)
**Hook:** "a huge milestone… easily the most important one." **Picture:** `t0456-l2-prime-workflow-report.jpg` — `prime.md` with `## Workflow` (git ls-files; read README.md) and `## Report`. **Worked example:** every Level-2 prompt is **Input → Workflow → Output**. `prime.md` is the minimal case; `quick-plan.md` adds Metadata + Variables + Instructions; `prime_tier_list.md` adds a Codebase Structure map. **Name:** the **Workflow section** — a sequential, numbered play that maps directly onto the agent's todo/plan list. Graded **S usefulness / C skill** — max value, low cost. **Failure:** skipping straight to meta levels; 90% of the time all you need is a great workflow. **Retrieval:** *Most useful section, and its skill grade?* → Workflow; S useful, only C skill.

### Level 3 — Control Flow Prompt
**Hook:** what if the workflow could branch and loop? **Picture (conditionals):** `t1245-l3-build-line17-control-flow.jpg` — `build.md` line 17: *"If no `PATH_TO_PLAN` is provided, STOP immediately and ask the user."* That's an early return. **Picture (loops):** `t1450-l3-create-image-loop.jpg` — `create_image.md` with an `<image-loop> … </image-loop>` block repeated `NUMBER_OF_IMAGES` times, plus prerequisite STOP checks. `edit_image.md` shows a loop + conditionals and **no Report** (output format intentionally dropped). **Name:** control flow (conditions, loops, early returns) — all living *inside* the Workflow. Graded **A / B**. **Failure:** hiding branching in prose so neither teammate nor agent can see where the loop starts and stops (use clear XML blocks / numbered steps). **Retrieval:** *Where does control flow live?* → Inside the Workflow section.

### Level 4 — Delegate Prompt
**Hook:** the biggest unlock — a prompt that fires *other* agents. **Picture:** `t1935-l4-load-ai-docs-scrapers.jpg` — `load_ai_docs.md` loops URLs and calls `@agent-docs-scraper` (five doc scrapers run in parallel); `t2020-l4-background-append-system-prompt.jpg` — `background.md` launches a whole background Claude Code CLI instance. **Worked example:** `parallel_subagents.md` (PROMPT_REQUEST `$1`, COUNT `$2`) makes the primary agent *design self-contained prompts* for N sub-agents and launch them in one Task batch — Dan runs it live at count=5. Because LLMs are non-deterministic, the five agents return diverse results. This is the **D (Delegate)** of the R&D context framework (AH-1). **Name:** the delegate prompt — your primary agent is the **prompt engineer for its sub-agents.** Graded **S usefulness / A skill.** **Failure:** handing a stateless sub-agent an under-specified prompt; you must manage the flow of information between agents. **Retrieval:** *What role does the primary agent play?* → Prompt engineer for its sub-agents (writes their self-contained prompts + output expectations).

### Level 5 — Higher Order Prompt
**Hook:** what if the thing you pass in is *another prompt*? **Picture:** reuse `t1245` (build.md) — the plan file is the input. **Worked example:** `/build specs/thing.md` — the top-level structure of `build.md` stays constant while the plan you pass in changes each run; the plan comes from `/quick-plan` or an expert. `load_bundle.md` similarly takes a context-bundle path and reconstructs a prior agent's context. **Name:** higher-order prompt (accepts a reusable prompt/file as input). Graded **B usefulness / A skill.** **Failure:** embedding all logic inline instead of scaffolding a stable wrapper you can feed different plans. **Retrieval:** *What does a higher-order prompt accept as input?* → Another reusable prompt/plan file.

### Level 6 — Template Metaprompt (the peak)
**Hook:** the prompt that builds your other prompts. **Picture:** `t2280-l6-metaprompt-specified-format.jpg` — `t_metaprompt_workflow.md` with `HIGH_LEVEL_PROMPT: $ARGUMENTS`, a `## Documentation` context map (web-fetched first), and a `## Specified Format` template the agent fills in. **Worked example:** you pass a high-level idea; the metaprompt emits a well-formed Level-2 workflow prompt in your house style. `plan_vite_vue.md` is a rapid-prototyping variant with a big Plan Format template + conditional `<if…>` blocks. **Name:** Template Metaprompt; its **Template (Specified Format)** section is graded **S / S** — the only max-usefulness *and* max-skill cell. **Failure:** dismissing meta-prompting as novelty — it's the highest-ROI investment; "this will pay you back massive dividends." **Retrieval:** *L6 vs L5?* → L5 *consumes* a prompt/plan; L6 *generates* a new prompt in a specified format.

> ⚠️ **Capture detail:** on video the metaprompt's purpose reads "follow the `Instructions`"; Dan says on camera *"this should be follow the workflow,"* and the shipped file on disk reads **`Workflow`.** The codebase is the corrected version.

### Level 7 — Self-Improving Prompt (expert level)
**Hook:** the agent that updates the agent. **Picture:** `t2565-l7-expert-expertise-section.jpg` — `cc_hook_expert_plan.md` with a large dynamic `## Expertise` section (Claude Code hook file structure, events, execution model, security). **Worked example:** the `cc_hook_expert` triplet — `_plan` (uses expertise), `_build` (implements), and **`_improve`** which reviews recent hook changes and rewrites **ONLY** the `## Expertise` sections, *leaving the Workflow stable.* **Name:** self-improving prompt via a live-updated Expertise section — "updating the context inside our prompts in a live way." Graded **A usefulness / S skill.** **Failure:** letting the improve step rewrite the Workflow, or building a self-improving prompt with no real domain to specialize in ("it's unlikely you even have a use case"). **Retrieval:** *What must `_improve` never touch?* → The Workflow — only the Expertise section changes.

---

## 3. The composable sections, graded (the tier list)

**Picture:** `t2740-final-tier-list.jpg` — the completed "AGENTIC PROMPT TIER LIST." This grid *is* the chapter's centerpiece. Every position below was reconciled against it.

**Sections (13), by tier:**

| Section | Useful | Skill | What it does |
|---|:--:|:--:|---|
| `## Workflow` | **S** | C | The sequential step-by-step play; maps to the agent's todo list; hosts control flow/loops/delegation. **The pillar.** |
| `## Template` | **S** | S | The exact output structure (Specified Format) with `<placeholder>` blocks; heart of L6. |
| `## Variables` | A | B | Dynamic (`$1/$2/$ARGUMENTS`) + static values in `NAME: value` syntax, referenced throughout. |
| `## Examples` | A | B | Concrete output demos; can drastically raise agent performance. |
| `## Expertise` | A | A | Embedded domain knowledge; the section that makes a prompt self-improving (L7). |
| `## High Level Prompt` | B | D | Detail-void description of what you want; required core of L1. |
| `## Purpose` | B | D | 1–2 sentences of direct, agent-directed intent. |
| `## Report` | B | C | The output/format section (JSON/YAML/structure/required fields). |
| `## Instructions` | B | C | Auxiliary guardrail bullets that aid the Workflow (more valuable in system prompts). |
| `# Title` | C | D | Clear, action-oriented H1 name. |
| `## Metadata` | C | C | YAML frontmatter: allowed-tools, description, argument-hint, model. |
| `## Codebase Structure` | C | C | A *context map* (tree of where files are) — you do NOT tell the agent to read them. |
| `## Relevant Files` | C | C | A specific file set to reference; speeds the agent up. |

**Headline reading:** the most useful section (Workflow) costs only C-tier skill — high value, low cost. The peak cell (S/S) holds `## Template` and `template_metaprompt.md`.

**Two easily-confused pairs (call these out for weak students):**
- **Workflow vs Instructions** — Workflow is the *play-by-play* the agent executes; Instructions are *surrounding auxiliary notes* about the steps. You can often fold Instructions into nested Workflow bullets.
- **Codebase Structure vs Relevant Files** — Codebase Structure is a *map you do not read* (find files fast, save tokens); Relevant Files is a set you *do* read.

---

## 4. Two design frameworks to carry away

**Input → Workflow → Output.** Every prompt reads as Variables (in) → Workflow (work) → Report (out). Input and output are especially for you and your team; the workflow is where the agent does the engineering. Drop any of the three you don't need.

**Static vs dynamic variables.**
- *Dynamic* — runtime input via `$1/$2/$ARGUMENTS`, changes each run. Example: `USER_PROMPT: $1` (quick-plan), `PATH_TO_PLAN: $ARGUMENTS` (build).
- *Static* — fixed value referenced throughout, changed in one place. Example: `PLAN_OUTPUT_DIRECTORY: \`specs/\``. Change it to `prd/` once and every reference updates.
- Convention (from the metaprompt): dynamic variables first, static second; prefer `$1/$2` over `$ARGUMENTS` for multiple args.

---

## 5. System prompts vs user prompts

**Everything graded above is for USER prompts** — all your slash commands enter the context window as user prompts.

**System prompts are a different game** — *scope and persistence.* They set the rules for **every** conversation, can't change mid-conversation, must handle many scenarios, and their mistakes scale to every user prompt. *"A bad system prompt is bad instructions for the whole job."* Written once, run many times — 1–3 orders of magnitude more consequential.

- **Where you touch them:** rarely. You **append** (`background.md` uses `--append-system-prompt`) or **overwrite** (Claude Code SDK, AH-3) only when building your own specialized agents. Sub-agents (`docs-scraper.md`) *are* system prompts. Only ~4 exist in the whole repo.
- **Good system-prompt sections:** Purpose (identity/role), Instructions (behavioral rules), Examples (behavior patterns), and a **loose** Workflow — because *"workflows reduce agency to increase determinism"* and a system prompt should keep agency.
- **Avoid in system prompts:** Variables, Report, Expertise/Templates, Metadata/Relevant Files/Codebase Structure.

**Retrieval:** *The tier-list grades apply to which kind of prompt?* → User prompts only.

---

## 6. The through-line: consistency is king

*"Consistency is the greatest weapon against confusion for both you and your agent."* Dan wants you **bored** of the workflow — the sameness is the feature. A predictable format lets you CRUD reusable prompts at light speed and hand work off to compute without friction. His quality test: *"If I handed this to a coworker, could they complete this work top to bottom?"*

This is how you move from inside-the-loop → outside-the-loop → **ZTE** (the TAC North Star), building AFK agents and ADW pipelines. It all traces back to one skill: **agentic prompt engineering.** *"Invest in your prompts for the trifecta to achieve asymmetric engineering in the age of agents."*

---

## 7. What "done" looks like for the student

A student has this chapter if they can, without notes: name the seven levels and the one capability each adds; state why Workflow is most-useful/mid-skill; give a real static and dynamic variable from the codebase; distinguish L6 (writes prompts) from L7 (updates its own Expertise); and explain why every grade is for user, not system, prompts — finishing by explaining why being *bored* by their own consistent format means they're doing it right.

**Next move (Dan's):** finish TAC first (ZTE/AFK/ADWs), then AH-3 (Claude Code SDK — build domain-specific agents with custom system prompts). Start at Level 1; scale to the Workflow Prompt; stack up to the Template Metaprompt.

---

*Cross-references: AH-1 (R&D framework / elite context engineering — the R and D behind prime and delegate), AH-3 (Claude Code SDK — system-prompt overwrite / domain agents), AH-4 (the O-agent — scaling parallel delegation), TAC-7 (ZTE), TAC-4 (AFK agents).*

# Infinite UI Agents — Lab Spec

**Codebase:** `agentic-horizon-extras/ui-agents` (Agentic Horizon member asset) — the only codebase for this lab. Do **not** use PiCanvas or any other repo.

**Prime directive (the tac ethos):** you don't hand-edit product code. Every change to the system — components, brand, even prompts — is made *by the agents / through the harness*, not by you typing into `index.vue`. Editing **harness config** (front matter, `brand.yaml`, `settings.json`) by hand is allowed and expected; editing generated **product** code by hand is a fail.

### Prerequisites & the two tracks

The full system requires the **Pi coding agent**, the **`teams`** shell alias (from the Multi-Team Agentic Coding member asset), plus `bun`, `node`, `just`, `uv`, and API keys (`ANTHROPIC_API_KEY`; OpenRouter/provider keys only if you attempt the open-source stretch). Because that's member-gated and token-costing, the lab is split:

- **Track A — Read the Harness (Lab 0–1):** fully gradable from the committed files. **No Pi, no `teams`, no API cost.** Everyone can complete and self-grade this from the repo alone.
- **Track B — Run & Specialize the Harness (Lab 2–4):** requires the full member setup and spends tokens. Do this if you have access.

---

## Lab 0 — Setup & orientation (Track A)

1. Open `ui-agents` in your IDE. Run `/install` (via Claude Code) and read what it verifies (Pi + `teams` alias, Bun/Node/just/uv, `ANTHROPIC_API_KEY`, Vue deps, team config, dev-server readiness). You do **not** need every prerequisite to pass Track A.
2. Read `README.md` end to end. Say out loud where you are in the trilogy (**ceo-agents → lead-agents → ui-agents**) and what the tagline demands ("build systems that solve entire problem classes").
3. Read `.pi/settings.json` and state, in one sentence, everything the Pi harness is configured to control here.

**Checkpoint 0 (gradable):** you can name the 4 keys in `settings.json` and what each does (`thinking`, `autoCompact`, `compactThreshold`, `prompts`), and you can state the 5-level hierarchy Brand → Product → Tree → Branch → Leaf without looking.

---

## Lab 1 — Map the harness (Track A, no API cost)

Answer each from the committed files; write your answers down — they are the graded artifact.

**1.1 Count the system.** From `.pi/multi-team/multi-team-config.yaml`: how many teams? How many *unique* agent files in `.pi/multi-team/agents/`? How many total agent *slots* (count A/B/C duplicates)?
> Expected: **8 teams**, **12 unique agent files**, **24 slots** (1 orchestrator + Setup 3 + Brand 2 + UI Gen ×3 + Validation ×3).

**1.2 Prove the tiers.** For `orchestrator.md`, one lead (e.g. `ui-generation-lead.md`), one worker (`vue-generator.md`), and one validator (`hard-validator.md`), record the `tools:` list and the `domain:` permissions.
> Expected: leads/orchestrator have `delegate` + `tilldone`; workers have `write`/`edit`/`bash` (no delegate); validators have neither `write`/`edit` nor `delegate`. Leads' `domain` sets `upsert: false` on `apps/infinite-ui/`; workers set `upsert: true`.

**1.3 Find the enforced rule.** Quote the two lines in `CLAUDE.md` that say leads don't write files and workers do. Explain in one sentence how `tools` + `domain` enforce it structurally.

**1.4 Read the learning loop.** Read `skills/mental-model.md`. In three bullets, state when an agent reads its expertise file, when it updates it, and what it must do after every write (line-count trim + YAML validation).

**1.5 Inspect a mental model.** Open any file in `.pi/multi-team/expertise/`. What's in it? Reconcile with the "7K-token mental model" from the video.
> Expected: a **one-line stub** (`# Mental model — auto-maintained by agent`); the 7,753-token file is runtime state, capped by `max-lines: 10000`.

**1.6 Trace the workflow.** Read `.pi/prompts/multi-team/generate.md`. List its 5 `Variables` and summarize the 8 `Workflow` steps. Where is the "till-done" list in this file?
> Expected: BRAND/PRODUCT/TREE/COUNT/PROMPT; the 8-step Setup→Brand→UIGen→round-robin gen→Setup→round-robin validate→fix→Setup pipeline; **there is no till-done list here** — it's the orchestrator's `tilldone` tool.

**1.7 Prove zero-hardcoded-values.** Open `brands/aegis/products/app/trees/agent-stream/timeline-stack/index.vue`. Find 3 CSS custom properties it uses and locate their source values in `brands/aegis/brand.yaml`. Confirm the leaf uses tokens, not raw hex.

**1.8 Find the preview mechanism.** In `src/canvas/PreviewBranchNode.vue` and `src/gallery/BranchPreview.vue`, identify how a leaf renders. Is it Vue `Teleport`?
> Expected: a real `<iframe>` (1280×720, CSS `transform: scale()`, `pointer-events:none`) → gallery route → `import.meta.glob` + dynamic `<component :is>`. **Not** Teleport (that's only in `Sidebar.vue`).

**Checkpoint 1 (gradable — pass = 7/8 correct):** answers to 1.1–1.8 match the expected values above. This checkpoint requires **no** API spend and certifies you understand the harness before you run it.

---

## Lab 2 — Run the pipeline (Track B, members)

1. `just dev` (starts the Vue app on :5173). `just team` (opens the multi-team chat — you're talking to the Orchestrator).
2. Pick an existing brand/product (`aegis` / `app`) and generate a **new** tree of 3 variants:
   `/generate aegis app pricing 3 "Three pricing-page layouts: a classic 3-tier table, a bold single-plan hero, and a comparison-grid. Use Aegis brand tokens only."`
   (Or use `just generate aegis app pricing 3 "<brief>"`.)
3. Watch the orchestrator delegate: Setup scaffolds → Brand loads context → UI Gen Lead writes 3 briefs → round-robin across UI Generation A/B/C → Validation A/B/C → Setup finalizes. Note the TillDone list appear and advance.
4. When it reports done, `just list-branches aegis app pricing` and browse the results at `/aegis/app` (canvas) and `/aegis/app/gallery/pricing`.

**Checkpoint 2 (gradable) — pass criteria:**
- `trees.yaml` for `aegis/app` shows a `pricing` tree with 3 branches at `status: validated` (or documented `failed` with the reason).
- 3 real `index.vue` leaves exist on disk under `.../pricing/*/index.vue`, each non-stub (> 100 lines) and using **only** brand CSS custom properties (grep for raw `#` hex in `<style>` → none outside `:root`/token declarations).
- All 3 render in the browser gallery and are visually on-brand for Aegis.
- **You typed zero lines of Vue by hand.** Every component came from the team.

---

## Lab 3 — Specialize the harness (Track B, members)

1. **Retarget an agent (edit front matter, not code).** In `vue-generator.md`, tighten `domain` to a single product path (e.g. `apps/infinite-ui/src/brands/aegis/products/site/`) and re-run a generation scoped there. Observe that the agent stays in its lane.
2. **Live rebrand (through the Brand team).** Run `/rebrand aegis "shift the accent from crimson to amber; keep everything else"` (or edit `aegis/brand.yaml` by hand — harness config edit, allowed) and watch every rendered component update live via CSS custom properties. Do **not** edit any `index.vue`.
3. **Watch a mental model grow.** Before and after a generation run, `wc -l` an agent's `expertise/*.yaml`. Confirm it moved from the 1-line stub toward populated, self-authored entries.

**Checkpoint 3 (gradable) — pass criteria:**
- The retargeted agent wrote **only** inside its narrowed `domain` (verify via `git status` / paths touched).
- The rebrand changed the rendered UI **without** any hand-edit to a leaf (`git diff` shows changes only in `brand.yaml`, not in `index.vue` files).
- At least one `expertise/*.yaml` is no longer a 1-line stub after your run.

---

## Lab 4 — Stretch (Track B, members)

- **S1 — Reproduce the reliability lesson.** Assign an open-source model to one team's worker in front matter (e.g. `model: openrouter/minimax/minimax-m2.7` on a `vue-generator` instance) and re-run `/generate`. Observe whether the worker underperforms or fails — and whether its lead / another team picks up the work. Then restore Sonnet and rerun. Write 3 sentences on what this teaches about model choice and redundancy.
- **S2 — Compose a new command against the team.** Add a reusable prompt in `.pi/prompts/multi-team/` (follow the `generate.md` shape: frontmatter → Purpose → Variables → Instructions → Workflow → Report). E.g. `/audit <brand> <product>` that delegates a brand-compliance sweep to the Brand + Validation teams. Prove it runs from `just`/`teams`.
- **S3 — Fork a leaf.** `/fork-leaf aegis app agent-stream compact-dashboard 2 "one denser, one calmer"`. Confirm the 2 forks carry `forkedFrom` in `trees.yaml` and attach to their parent branch on the canvas.
- **S4 — Read the meta-layer.** In `.claude/skills/drive/`, read how the tmux `drive` skill (`session`/`run`/`poll`/`fanout`/`screenshot`) is used to script and record the `teams` chat. In one paragraph, explain how Dan drove/recorded the demo — the Claude-Code-as-meta-agent layer.

---

## Final pass sheet

You pass the lab if:

- **[Track A]** Checkpoint 0 and Checkpoint 1 are complete (≥7/8 on Lab 1), with written answers matching the expected values — **achieved with zero API spend.**
- **[Track A]** You can state, without notes: the six harness components; the three tiers and who writes files; the four front-matter specialization fields (and why `domain` matters); and the committed-vs-demo divergence (all-Sonnet, empty stubs, one brand).
- **[Track B, if attempted]** Checkpoint 2 met: 3 validated, on-brand, browseable leaves generated **by the team**, zero hand-written Vue.
- **[Track B, if attempted]** Checkpoint 3 met: a retargeted agent stayed in its `domain`, a rebrand changed the UI without touching any leaf, and a mental model grew past its stub.
- **Prime directive honored throughout:** no hand-edited product code; all product changes came from the agents.

---

## Instructor notes & guardrails

- **Grade Track A from artifacts, not vibes.** The Lab 1 answers are objective (counts, tool lists, file contents) and checkable against the repo. This is the equalizer for readers without member access or API budget.
- **Token economics (Track B).** A single `/generate ... 3` run drives ~8–11 delegated tasks across up to 6 teams — it is not cheap. Budget for it; watch the per-agent cost/token telemetry in the `teams` chat (the demo hit ~$6.70 / 29 min for one 3-variant run at full scale).
- **Expect failures, and grade them as data.** If a worker stalls, the correct behavior is the lead covering or a sibling team completing the branch — that *is* the reliability lesson. Document failures with their reason rather than treating them as a lab-breaking error.
- **Don't hunt for Teleport.** Steer students to the real preview path (`iframe` + `import.meta.glob`); it's a deliberate "read the code, not the narration" beat.
- **Guardrails.** Don't improvise destructive git commands. Keep generation scoped to `aegis` (or a fresh `/new-brand`) so runs stay reproducible. Restore any front-matter/model edits after stretch exercises so the base config is clean for the next reader.

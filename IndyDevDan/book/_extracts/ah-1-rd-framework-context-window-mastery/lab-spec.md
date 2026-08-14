# AH-1 Lab Spec — Elite Context Engineering (the R&D Framework)

**Scope rule:** every drill runs inside the course codebase only (`codebase/` → `agentic-horizon/elite-context-engineering`; students: `git clone https://github.com/disler/elite-context-engineering.git`). No external repos.
**Prime directive (graded throughout):** you MEASURE with `/context` before and after every reduce/delegate move, and you can cite the numbers. The graded outcome is that you can *see, own, and move* your window — not just run commands. Corollary: zero application code typed by hand (the wrapper and the hook come from planner/builder/expert agents).
**Time box:** 75–120 minutes (12 techniques). Token cost: real but modest at beginner/intermediate; the agentic-level drills (10–12) bill directly on your API key — budget for it.

---

## 0 · Setup + baseline measurement (10 min)

1. `git clone https://github.com/disler/elite-context-engineering.git && cd elite-context-engineering`
2. Open in an IDE with a **token-counter extension** in the status bar (Dan uses VS Code). Copy `.env.sample` → `.env` and set `ANTHROPIC_API_KEY` (ELEVENLABS/OPENAI optional, only for the TTS/util demos).
3. Read `README.md`: note all 12 techniques with their **Level** (Beginner→Agentic) and **Framework** (Reduce/Delegate/R&D) tags, and the bash aliases at the bottom (`cld`, `cldys`, `cldyo`, `lfg`, …).
4. Boot `claude`, run `/context`, and **write down the boot state**: total %, System tools, MCP tools, Custom agents, Memory files, Free space.

**Checkpoint 0:** you can state your boot-state numbers and what each `/context` line means. If you can't read the window, you can't manage it.

## 1 · REDUCE — beginner level (Techniques 1–3, 20 min)

**T1 Measure.** With the README open, watch the IDE token counter (~2,650 tokens). Re-run `/context`; identify the two biggest consumers (on Dan's machine: MCP tools 24.1k and Memory files 23.7k).

**T2 Avoid MCP.** Confirm the default MCP cost. Then relaunch loading only what you need:
`claude --mcp-config .mcp.json.firecrawl_7k.sample --strict-mcp-config`
Re-run `/context`; verify MCP tokens dropped (Dan's went 24.1k → 6.5k). Say out loud why `--strict-mcp-config` matters (it overrides global user/local servers).

**T3 Prime > CLAUDE.md.** Point the project at the bloated memory file (`CLAUDE.large.md`, 2,978 lines) and observe the `⚠ Large CLAUDE.md will impact performance` warning + Memory-files %. Restore the 43-line `CLAUDE.md`/`CLAUDE.concise.md`; confirm Memory files fall to ~0.2% and Free space ~90%+. Then `/prime` (git ls-files → read README → report) and inspect `/prime_cc`.

**Checkpoint 1 (write it down):** MCP tokens AND memory-file tokens both measurably dropped, verified in `/context`. State which lever (delete/scope MCP; shrink+prime) reduced each, and which R it is (all Reduce).

## 2 · REDUCE + DELEGATE — intermediate level (Techniques 4–6, 20 min)

**T4 Output tokens.** Open two terminals. Set one to the **One Word Output** style (via `settings.local.concise.json` or `/output-style` → "One Word Output"); leave the other default. Send the same prompt to both (start with `hi`, then "What does this codebase do?"). Compare the response token counts — the concise one should say roughly "Done." (a few tokens) vs a full paragraph.

**T5 Sub-agents.** In `/context`, note **Custom agents ≈ 122 tokens** (they're system prompts). Run `/load_ai_docs`; watch it read `ai_docs/README.md`, delete docs >24h old, and fire `docs-scraper` sub-agents in parallel. Confirm the scrape tokens did **not** land on your primary window (`/context` afterward).

**T6 Architect/Editor.** `/quick-plan "add a tiny helper to apps/cc_ts_wrapper"` (writes `specs/<name>.md`). Open a **fresh** agent and `/build <path-to-spec>`. Confirm the builder needed no priming — everything was in the plan.

**Checkpoint 2:** (a) the concise style produced a measurably smaller response than default; (b) `/load_ai_docs` kept scrape work off your primary window; (c) a fresh `/build` agent implemented from the spec alone. State which technique is Reduce, which is Delegate, and which is both.

## 3 · Advanced level (Techniques 7–9, 20 min)

**T7 Avoid /compact.** After some work, run `/compact`, then `Ctrl-R` to read the summary — notice you had to *look* to know your state. Now do the alternative: `/clear` then `/prime`. Write one sentence on which leaves you *knowing* your exact window.

**T8 Context bundles.** Inspect `agents/context_bundles/<DAY_HOUR>_<session>.jsonl` (built by the `PostToolUse`/`UserPromptSubmit` hook `context_bundle_builder.py`). Re-run `/prime` and watch entries append. In a fresh agent, `/load_bundle <path>` and confirm deduped replay of the prior agent's reads.

**T9 One agent, one purpose.** On paper, take one real task and split it into a pipeline of single-purpose agents (plan → build → improve → commit). No code — just the pipeline. This is the ADW you'll automate in later lessons.

**Checkpoint 3:** you can explain why `/clear`+`/prime` leaves a known state and `/compact` doesn't, and a fresh agent successfully remounted prior state via `/load_bundle`.

## 4 · Agentic level (Techniques 10–12, 25 min — bills on your API key)

**T10 System prompt.** Run in print mode:
`claude --dangerously-skip-permissions --model sonnet --append-system-prompt "ALWAYS read files in 100-line increments (offset=0 limit=100, then offset=100 limit=100); if you have enough, stop and proceed; prefix your final message with ✅ or ❌" -p "what is CLAUDE.large.md for?"`
Open the resulting context bundle and confirm `Read(..., limit:100)` operations — the append-system-prompt steered the read tool itself.

**T11 Primary delegation.** From a primary agent: `/background "/quick-plan add a second helper to the wrapper" sonnet`. Watch `agents/background/background-report-*.md` get written and renamed to `.complete.md` (or `.failed.md`). You did not sit in the loop.

**T12 Agent experts.** Run the triad on a tiny hook feature:
`/experts:cc_hook_expert:cc_hook_expert_plan "log SessionStart events to a JSONL file"` → `/experts:cc_hook_expert:cc_hook_expert_build <spec-path>` → `/experts:cc_hook_expert:cc_hook_expert_improve`.
Confirm via `git diff` that **improve** edited **only** the `## Expertise` sections of the plan/build experts (never the Workflow).

**Checkpoint 4:** (a) the context bundle shows 100-line reads; (b) a `/background` agent wrote and renamed its report without you; (c) the improve step updated only the Expertise section (git diff proves Workflow untouched).

## Stretch drills (still zero hand-typing)

- **S1 — New prime area.** Author `/prime_bug` (or `/prime_feature`) that primes a different focus; prove via `/context` it loads a different, task-scoped window than `/prime`.
- **S2 — New self-fixed MCP config.** Add a `.mcp.json.<server>_<Nk>.sample` for a server you actually use; load it with `--strict-mcp-config` and confirm the token cost matches the filename.
- **S3 — New output style.** Create a style between "One Word Output" and default (one line + a status emoji); measure the response-token delta on a fixed prompt.
- **S4 — Second expert.** Create a new expert triad (plan/build/improve) for another codebase concern; run improve after a change and verify it updates only the Expertise section.
- **S5 — Wrap an ADW.** Chain plan → build → improve → `git commit` as a single background workflow, using a context bundle to remount if a step overflows.

## Pass criteria (all required)

- [ ] You measured with `/context` before and after every reduce/delegate move and can cite the numbers (Checkpoints 0–4).
- [ ] MCP-tool and memory-file token usage measurably dropped (Reduce), verified in `/context`.
- [ ] You delegated at least twice — sub-agents via `/load_ai_docs` and a primary `/background` agent — keeping work off your primary window.
- [ ] You ran the architect/editor split and the agent-experts plan/build/improve loop end to end.
- [ ] Zero application code typed by hand (the wrapper and the hook came from planner/builder/expert agents).
- [ ] Closing oral check, no notes: name the R&D framework; sort all 12 techniques into their Level and into Reduce vs Delegate; state the central law ("a focused agent is a performant agent"); and explain the paradox — how spending MORE effort on context (reset-and-prime, plan-then-build, maintain experts) lets you do LESS babysitting and drop your presence.

## Instructor / self-check notes

- **Most common stall — not measuring.** Students run the commands but never open `/context`, so they can't see the payoff. Make every checkpoint a *number*, not a vibe.
- **Second stall — model/count drift.** The recording shows `claude-opus-4-1-20250805`, MCP `24.1k`, README `2,650`, and on-screen `.mcp.json.all_22k`/`.firecrawl_4k`. The shipped repo uses `.mcp.json.all_16k.sample`/`.firecrawl_7k.sample`, and your models/counts will differ. That's expected — grade the *direction and proportion* of the change, not exact figures.
- **Third stall — quick-plan model pin.** `quick-plan.md` pins a course-era Opus id (`claude-opus-4-1-20250805`); if that model isn't available, update the frontmatter to a current model before running T6/T11.
- **Cost anxiety.** Beginner/intermediate drills are cheap; the agentic-level drills (10–12) and any background/expert runs bill on your API key. If a student can't run them, the pay-to-play conversation is the lesson surfacing early — do the read-only inspection of the codebase files instead.
- **Guardrails.** `--dangerously-skip-permissions` and `/background` run with reduced safety and on your keys; keep them scoped to this repo and small prompts. Do not point background/expert agents at unrelated directories.
- **What this lab intentionally does NOT cover:** full ADW orchestration at scale, worktree-parallel fleets, and the Claude Agent SDK — those are later TAC/AH lessons and the Claude Code SDK Mastery extended lesson. Keep the 12 primitives crisp; deflect scope creep.

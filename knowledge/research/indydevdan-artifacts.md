# IndyDevDan artifact panel: the recurring execution system

Research date: 2026-08-04  
Panel remit: concrete public artifacts, not a summary of rhetoric.

## Bottom line

The recurring system is **not one giant prompt and not one permanent set of tools**. It is a stable control loop whose roles and artifacts survive repeated tool changes:

> **request → bounded context → executable plan → specialized worker(s) → deterministic checks → independent semantic verification → bounded correction → accepted artifact → trace/documentation → reusable capability**

The clearest current expression is the Super Simple Software Factory (SSSF): deterministic Python owns sequencing, retries, and acceptance; agents operate only inside named phases; typed envelopes cross phase boundaries; and SQLite records the trace. IndyDevDan states that design explicitly in the [SSSF README](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/README.md#L16-L18) and contrasts it with an agent owning the whole SDLC in the [control-plane rationale](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/README.md#L25-L47).

The deepest stable principle is therefore:

> **Keep judgment in agents; move repeatable control, state transitions, permissions, and proof into code and durable artifacts.**

That conclusion is an inference from the evolution of his repositories. Early work embeds the whole loop in a prompt passed to a coding agent ([programmable Notion workflow](https://github.com/disler/claude-code-is-programmable/blob/388926529ccdf78b7090ee221157e85953f739aa/claude_code_is_programmable_3.py#L79-L140)); the newest work explicitly moves that loop into Python and relegates agents to bounded nodes ([SSSF rationale](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/README.md#L31-L43)).

## Scope and inventory method

I queried IndyDevDan's first-party GitHub account with `gh api users/disler/repos`, shallow-cloned all **52 public repositories** visible on 2026-08-04, and searched their tracked files. This is an artifact inventory, not an independent benchmark of the systems' quality. Repository descriptions, claimed costs, and claimed performance remain the author's claims unless the repository contains the underlying run artifacts. The public corpus is visible on the [disler repository index](https://github.com/disler?tab=repositories).

Across those 52 default-branch snapshots, I found:

| Artifact | Repositories containing it | What the prevalence suggests |
|---|---:|---|
| `.claude/` agentic layer | 33 | The agent layer lives beside the application, not inside `src/`. |
| prompt/command Markdown | 32 | Workflows are named and replayable rather than remembered ad hoc. |
| `prime` or `context_prime` command | 29 | Deliberate session intake is one of the most stable habits. |
| `ai_docs/` | 25 | External documentation is frozen locally for grounded agent use. |
| `specs/` | 22 | Plans/specifications are treated as implementation inputs. |
| `SKILL.md` | 16 | Capabilities are increasingly packaged as portable, progressively disclosed skills. |
| `justfile` | 15 | Human/CI/agent entry points collapse to reproducible one-line recipes. |
| explicit agent definitions | 11 | Specialization is encoded as files with distinct tools and purposes. |
| hooks | 7 | Automation, validation, safety, and observability attach to lifecycle events. |
| deterministic `adws/` workflow code | 2 | Code-owned orchestration is the newest culmination, not yet an old convention. |

These counts are my direct scan of the public repositories, so they should be read as a snapshot rather than a timeless statistic. The representative implementations below provide the exact first-party file evidence.

## Concrete artifact stack

### 1. Context files orient the agent

Common artifacts are `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, and a `/prime` command. A representative `prime.md` permits only Bash/Read, runs `git ls-files`, reads the README and selected `ai_docs`, then reports its understanding ([hooks-mastery `prime.md`](https://github.com/disler/claude-code-hooks-mastery/blob/052ad1cbd5aeb1ec4a1def22012d1293c6225625/.claude/commands/prime.md)). This is not generic “read everything”; it is a deterministic intake bundle.

The latest SSSF tightens this into **lazy context loading**: startup reads only the overview plus the phase summaries, prints available workflows, and waits; the roster, database schema, and handoff contract are loaded only when the request routes there ([SSSF `SKILL.md`](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/.claude/skills/sssf/SKILL.md#L11-L34)). Stable pattern: prime deliberately. New refinement: do not spend context before the task selects it.

### 2. `ai_docs/` and `app_docs/` separate reference knowledge from outcome knowledge

The corpus repeatedly checks in vendor/API material under `ai_docs/`, so agents can use a task-relevant, versioned reference rather than reconstructing an API from memory. Planf3's create workflow explicitly explores the codebase and reads `AI_DOCS` and `APP_DOCS` to ground a plan ([create workflow](https://github.com/disler/planf3/blob/f34b7ba5ff8167ef6283791763f4b578bfb3a2c0/.claude/skills/planf3/workflows/create-plan.md#L1-L10)).

In SSSF's real Inkwell reference implementation, the documenter operates only after tests and review pass, receives a diff captured against the run's pinned baseline, writes the result to `app_docs/`, and commits documentation separately ([`adw_simple_sdlc.py`](https://github.com/disler/inkwell-agent-sandboxes-and-software-factory/blob/86b8dceb5a81a1bbdbaa84c644b058d262a394c3/adws/adw_simple_sdlc.py#L140-L171)). Stable pattern: reference material enters through `ai_docs`; verified change knowledge exits through `app_docs`/documentation.

### 3. `specs/` is the durable contract between intent and implementation

Planf3 makes planning a reusable meta-skill rather than an improvised model mode. It emits a self-contained plan into `specs/` and standardizes purpose, problem, solution, relevant files, phased tasks, testing strategy, validation loop, metadata, and amendments ([plan anatomy](https://github.com/disler/planf3/blob/f34b7ba5ff8167ef6283791763f4b578bfb3a2c0/README.md#L88-L106)). The plan is explicitly a living artifact with create, update, reference-update, build, and image workflows ([workflow table](https://github.com/disler/planf3/blob/f34b7ba5ff8167ef6283791763f4b578bfb3a2c0/README.md#L110-L126)).

The build workflow requires the next agent to absorb the full plan and back-references, process phases top-to-bottom, mark `[wip]`/`[x]`/`[f]`, loop on each phase's tests, run final validation, and append session/commit metadata ([`build-plan.md`](https://github.com/disler/planf3/blob/f34b7ba5ff8167ef6283791763f4b578bfb3a2c0/.claude/skills/planf3/workflows/build-plan.md#L1-L16)). SSSF goes further: it commits the plan before code exists, preserving the request even when verification later fails ([Inkwell SDLC](https://github.com/disler/inkwell-agent-sandboxes-and-software-factory/blob/86b8dceb5a81a1bbdbaa84c644b058d262a394c3/adws/adw_simple_sdlc.py#L78-L94)).

### 4. Skills, agents, commands, and `just` form a reusable hierarchy

Bowser provides the cleanest explicit decomposition:

1. **Skill** = raw capability.
2. **Subagent** = isolated specialized worker and scale.
3. **Command** = workflow orchestration and result collection.
4. **Justfile** = reusable one-line entry point for humans, CI, or other agents.

This four-layer stack is documented with exact locations in the [Bowser README](https://github.com/disler/bowser/blob/26541acddc0626e97e8f4398e47b288e97f97ebd/README.md#L9-L26). Bowser's UI review command then makes the abstraction concrete: YAML stories are discovered, one QA agent is assigned per story, all independent stories launch in parallel, structured results are collected, and the team is torn down ([`ui-review.md`](https://github.com/disler/bowser/blob/26541acddc0626e97e8f4398e47b288e97f97ebd/.claude/commands/ui-review.md#L40-L51), [`ui-review.md`](https://github.com/disler/bowser/blob/26541acddc0626e97e8f4398e47b288e97f97ebd/.claude/commands/ui-review.md#L77-L118)).

The Library packages distribution of this layer: the normal lifecycle is **build → catalog → distribute → use**, with a reference catalog for skills, agents, and prompts rather than a public marketplace ([Library workflow](https://github.com/disler/the-library/blob/47f455cd139b0e8498e13ce0d91de9741ebddf99/README.md#L154-L188)). Its README explicitly names the stack as skills → agents → prompts → justfile → distribution ([agentic stack](https://github.com/disler/the-library/blob/47f455cd139b0e8498e13ce0d91de9741ebddf99/README.md#L261-L272)).

### 5. Agent identity is a role contract, not a model name

In the Pi comparison project, the actual agent files make the recurring split explicit: planner and reviewer have read-only tool lists, builder can mutate, documenter can edit documentation, and red-team is adversarial/read-only ([planner](https://github.com/disler/pi-vs-claude-code/blob/0ed11f44932fdef29bd98467700019762298f50d/.pi/agents/planner.md), [builder](https://github.com/disler/pi-vs-claude-code/blob/0ed11f44932fdef29bd98467700019762298f50d/.pi/agents/builder.md), [reviewer](https://github.com/disler/pi-vs-claude-code/blob/0ed11f44932fdef29bd98467700019762298f50d/.pi/agents/reviewer.md), [red-team](https://github.com/disler/pi-vs-claude-code/blob/0ed11f44932fdef29bd98467700019762298f50d/.pi/agents/red-team.md)). Its chain definitions include `plan-build-review`, `plan-review-plan`, and `scout → plan → build → review` flows ([`agent-chain.yaml`](https://github.com/disler/pi-vs-claude-code/blob/0ed11f44932fdef29bd98467700019762298f50d/.pi/agents/agent-chain.yaml)).

SSSF generalizes the same idea into YAML: one agent, one prompt, one purpose; model, thinking, prompts, harness, tools, and allowed writes are configured per role, while workflow scripts name roles instead of models ([agent roster](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/README.md#L145-L181)). Fusion Harness makes the model interchangeability explicit: architect, builder, fusion, and validator are roles; the provider/model occupying each slot is configurable ([three commands](https://github.com/disler/fusion-harness/blob/5852f2ed4f5f064a368d83d2dabad84fe6bfa0b4/README.md#L70-L92)).

### 6. Parallelism is used only after work is partitioned

The Infinite Agentic Loop is an early prompt-only example: it analyzes a specification and existing outputs, assigns a distinct iteration number and creative direction per subagent, and launches bounded waves of independent generators ([phases 1–4](https://github.com/disler/infinite-agentic-loop/blob/6e9a012f81ef2291faf174d67176f7e69832cc0a/.claude/commands/infinite.md#L17-L85)). Infinite mode uses fresh waves and progressive summaries to avoid main-context accumulation ([phase 5](https://github.com/disler/infinite-agentic-loop/blob/6e9a012f81ef2291faf174d67176f7e69832cc0a/.claude/commands/infinite.md#L87-L121)).

Bowser follows the same partition-before-fan-out rule for test stories. Fusion Harness follows it for independent model opinions, then gives a third agent the explicit merge task; it keeps provenance and disagreements rather than concatenating the answers ([fusion flow](https://github.com/disler/fusion-harness/blob/5852f2ed4f5f064a368d83d2dabad84fe6bfa0b4/README.md#L102-L116)). Stable pattern: parallelize independent searches, alternatives, or stories. Do not let multiple workers silently share one canonical output path.

### 7. Deterministic code owns known operations

The newest and most important implementation rule is: if the exact invocation is known, it is a code phase, not an agent. SSSF calls out `bun test` and `ruff check` as deterministic operations that should not consume a context window ([rationale](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/README.md#L35-L45)) and makes this an enforced skill rule ([SSSF hard rule 8](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/.claude/skills/sssf/SKILL.md#L60-L72)).

The reference SDLC proves the intended split: the planner and builder are agent phases; `quality.run_inkwell_tests()` is a code phase; failures are converted into envelopes and returned verbatim to the builder; the fix loop is bounded at three attempts ([Inkwell test/fix loop](https://github.com/disler/inkwell-agent-sandboxes-and-software-factory/blob/86b8dceb5a81a1bbdbaa84c644b058d262a394c3/adws/adw_simple_sdlc.py#L91-L112)). Git commits are also code phases rather than agent side effects ([same workflow](https://github.com/disler/inkwell-agent-sandboxes-and-software-factory/blob/86b8dceb5a81a1bbdbaa84c644b058d262a394c3/adws/adw_simple_sdlc.py#L67-L89)).

### 8. Testing and reviewing answer different questions

In the current SDLC, the test suite asks whether the code runs; the reviewer asks whether the result matches the request/plan. A revision after review invalidates the old test result and therefore triggers a retest ([workflow rationale](https://github.com/disler/inkwell-agent-sandboxes-and-software-factory/blob/86b8dceb5a81a1bbdbaa84c644b058d262a394c3/adws/adw_simple_sdlc.py#L22-L37), [retest implementation](https://github.com/disler/inkwell-agent-sandboxes-and-software-factory/blob/86b8dceb5a81a1bbdbaa84c644b058d262a394c3/adws/adw_simple_sdlc.py#L114-L148)). This separation is stable across earlier artifacts but is most enforceable here.

The Verifier Agent adds an independent observer. It reads the builder's session slice, decomposes the request and claims into atomic propositions, proves each with deterministic tool output, feeds concrete corrections back, and escalates after a bounded number of loops ([two-agent design](https://github.com/disler/the-verifier-agent/blob/aa18d68bcf886fb2a061ca5a76c6d2e1f3516501/README.md#L9-L13), [verifier workflow](https://github.com/disler/the-verifier-agent/blob/aa18d68bcf886fb2a061ca5a76c6d2e1f3516501/.pi/verifier/agents/verifier.md#L49-L58)). Its core epistemic rule is that the builder's answer is a claim, not proof; verified findings require command/file/query evidence ([verifier persona](https://github.com/disler/the-verifier-agent/blob/aa18d68bcf886fb2a061ca5a76c6d2e1f3516501/.pi/verifier/agents/verifier.md#L18-L36)).

Fusion Harness pushes this further with **gate-first validation**: the validator writes an executable acceptance gate before the builder works, each explicit user requirement must map to an objective check, and a baseline run must be red so a vacuous gate is visible ([validator contract](https://github.com/disler/fusion-harness/blob/5852f2ed4f5f064a368d83d2dabad84fe6bfa0b4/extensions/fusion-harness/SYSTEM_PROMPT_VALIDATOR.md#L1-L30), [auto-validation loop](https://github.com/disler/fusion-harness/blob/5852f2ed4f5f064a368d83d2dabad84fe6bfa0b4/README.md#L138-L154)).

### 9. Correction loops preserve context and always have a cap

SSSF uses typed envelopes for handoff and re-prompts the **same session** when parsing or gates fail, preserving what the worker learned ([envelopes and gates](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/README.md#L221-L247)). The reference SDLC caps test fixes at three and review revisions at two ([loop constants and implementation](https://github.com/disler/inkwell-agent-sandboxes-and-software-factory/blob/86b8dceb5a81a1bbdbaa84c644b058d262a394c3/adws/adw_simple_sdlc.py#L52-L54), [`adw_simple_sdlc.py`](https://github.com/disler/inkwell-agent-sandboxes-and-software-factory/blob/86b8dceb5a81a1bbdbaa84c644b058d262a394c3/adws/adw_simple_sdlc.py#L96-L129)). Fusion Harness similarly halts after a configured number of gate failures and escalates to validator triage rather than running forever ([bounded gate loop](https://github.com/disler/fusion-harness/blob/5852f2ed4f5f064a368d83d2dabad84fe6bfa0b4/README.md#L144-L154)).

### 10. Permissions are checked as outcomes, not trusted as prompts

Tool lists express capability but do not securely express write scope because Bash and Write can reach beyond a nominal role. SSSF snapshots the git change set before and after an agent call, rejects paths outside `writes`, protects the workflow/grader machinery, and rolls back unauthorized new changes ([permission design](https://github.com/disler/inkwell-agent-sandboxes-and-software-factory/blob/86b8dceb5a81a1bbdbaa84c644b058d262a394c3/adws/adw_modules/permissions.py#L1-L27), [enforcement](https://github.com/disler/inkwell-agent-sandboxes-and-software-factory/blob/86b8dceb5a81a1bbdbaa84c644b058d262a394c3/adws/adw_modules/permissions.py#L128-L157)). This is a more mature form of the earlier “planner/reviewer get read-only tools” convention.

For risky or parallel work, isolation is another layer. Agent Sandbox's complete workflow creates an isolated environment, writes a plan, builds inside the sandbox, exposes it, validates it internally and externally, and loops until the full-stack/browser checks pass ([workflow definition](https://github.com/disler/agent-sandbox-skill/blob/ac460eea626bd11a68960b0b8f2dcefc25bfce5c/.claude/skills/agent-sandboxes/prompts/plan-build-host-test.md#L21-L41), [steps](https://github.com/disler/agent-sandbox-skill/blob/ac460eea626bd11a68960b0b8f2dcefc25bfce5c/.claude/skills/agent-sandboxes/prompts/plan-build-host-test.md#L50-L95)). Inkwell's later sandbox layer strengthens this by running the coding agents inside a throwaway VM and stripping host orchestration code from the mounted guest ([Inkwell sandbox architecture](https://github.com/disler/inkwell-agent-sandboxes-and-software-factory/blob/86b8dceb5a81a1bbdbaa84c644b058d262a394c3/README.md#L12-L39)).

### 11. Observability and memory are products, not transcript archaeology

The 2025/early-2026 observability system captures agent lifecycle hooks through HTTP into SQLite, broadcasts via WebSocket, and renders a live Vue UI ([architecture](https://github.com/disler/claude-code-hooks-multi-agent-observability/blob/8a6e5cf795df50767cea7123703751282a819697/README.md#L1-L17), [data flow](https://github.com/disler/claude-code-hooks-multi-agent-observability/blob/8a6e5cf795df50767cea7123703751282a819697/README.md#L294-L306)). SSSF simplifies the transport but preserves the principle: JSONL remains the raw record, SQLite is the queryable mirror, and the UI polls a single cursor query ([SSSF trace](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/README.md#L251-L271)).

There are three distinct memory forms in the artifact set:

- **Run memory:** session JSONL, envelopes, gate results, phase status, and SQLite traces ([SSSF trace](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/README.md#L257-L269)).
- **Project memory:** specs, commits, diffs, `app_docs`, and append-only plan metadata ([Planf3 plan anatomy](https://github.com/disler/planf3/blob/f34b7ba5ff8167ef6283791763f4b578bfb3a2c0/README.md#L94-L106)).
- **Reusable personal/team memory:** Pocket Pick stores searchable snippets/ideas in a portable SQLite knowledge base ([Pocket Pick](https://github.com/disler/pocket-pick/blob/d8243d35036cb4b3c934180fce30952bc4a73365/README.md#L1-L16)); The Library distributes reusable skills, agents, and prompts by reference ([Library](https://github.com/disler/the-library/blob/47f455cd139b0e8498e13ce0d91de9741ebddf99/README.md#L21-L45)).

## The actual recurring execution stack

This is the most faithful artifact-backed methodology to extract from the repositories.

| Stage | Fixed rule | Durable artifact / proof |
|---|---|---|
| 1. Intake | Capture the request verbatim; enumerate explicit outcomes and unknowns. | Request event or prompt file. |
| 2. Context | Prime only the repository map and relevant docs; lazy-load deeper references after routing. | `CLAUDE.md`/`AGENTS.md`, `/prime`, `ai_docs/`. |
| 3. Definition of done | Turn every explicit requirement into an objective acceptance check; for important work, run the gate before building and expect red. | Validation commands or executable `gate.py`. |
| 4. Plan | Produce an executable plan with purpose, relevant files, ordered phases, tests, and measurable acceptance criteria; record it before implementation. | `specs/<plan>`, preferably committed. |
| 5. Role assignment | One agent, one purpose, one output contract. Name roles, not models. Give only the required tools and write paths. | Agent roster YAML/frontmatter + typed envelope. |
| 6. Scheduling | Run dependent phases sequentially. Fan out only independent stories, searches, or alternatives; assign collision-free outputs. | ADW graph/task DAG/run directory. |
| 7. Build | Only the builder mutates product code. Code, not the agent, performs known commands and git transitions. | Working-tree diff + build envelope. |
| 8. Mechanical verification | Run tests, lint, typecheck, builds, migrations, and smoke checks as deterministic code. | Exit codes and command logs. |
| 9. Semantic verification | A separate reviewer/verifier checks the implementation against the request/plan and cites evidence. | Atomic claim report / review envelope. |
| 10. Correction | Return exact failures to the same responsible session; retest after every corrective mutation; stop/escalate at a fixed cap. | Failure envelope + attempt counter. |
| 11. Acceptance and shipping | Accept only when mechanical checks and semantic review are both green; commit code after verification. | `run.finish(accepted=...)`, commit SHA. |
| 12. Capture and improve | Document the verified diff, retain the trace, and turn repeated gaps into a better skill, prompt, gate, fixture, or harness. | `app_docs/`, trace DB, Library/Pocket Pick entry. |

The first-party reference implementation follows almost exactly this sequence—request, plan, plan commit, build, bounded test/fix, bounded review/revise, retest, code commit, diff capture, documentation, docs commit, final acceptance—in [`adw_simple_sdlc.py`](https://github.com/disler/inkwell-agent-sandboxes-and-software-factory/blob/86b8dceb5a81a1bbdbaa84c644b058d262a394c3/adws/adw_simple_sdlc.py#L5-L41) and its executable phases ([lines 78–174](https://github.com/disler/inkwell-agent-sandboxes-and-software-factory/blob/86b8dceb5a81a1bbdbaa84c644b058d262a394c3/adws/adw_simple_sdlc.py#L78-L174)).

## Stable patterns versus tool-specific details

| Stable and transferable | Currently tool-specific / replaceable |
|---|---|
| Externalize context, plan, handoff, verification, and trace. | `.claude/`, `.pi/`, `SKILL.md` discovery conventions. |
| One role, one purpose, least privilege, structured output. | Claude Task/Team tools, Pi subprocess flags and extensions. |
| Code owns known commands and workflow state transitions. | Python + `uv`, `just`, Bun, Pydantic, YAML. |
| Independent checks before “done”; evidence beats self-report. | Playwright CLI, exact lint/test commands, verifier Unix socket. |
| Bounded corrections reuse the responsible session. | Pi `--session-id`, Claude resume handles, tmux windows. |
| Parallelize independent work; isolate writers and output paths. | E2B/exe.dev sandboxes, worktrees, named browser sessions. |
| Store raw events plus a queryable projection. | JSONL + SQLite + Vue, HTTP/WebSocket versus direct polling. |
| Package improvements so the next run inherits them. | The Library catalog, Pocket Pick MCP, current folder names. |
| Roles outlive models; select models per role. | The current provider/model IDs and thinking-level flags. |

Do not copy current model names, exact ports, or vendor-specific commands and mistake them for the methodology. SSSF itself labels Pi-only execution and its default model as a v1 limitation ([scope](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/.claude/skills/sssf/SKILL.md#L74-L76)); the role, phase, envelope, gate, and trace concepts are the portable parts.

## Evolution: what became more systematic over time

1. **Programmable agent (2025):** code launches a single agent with a detailed natural-language loop and an allowed-tool list; the agent still owns sequencing ([Notion agent prompt](https://github.com/disler/claude-code-is-programmable/blob/388926529ccdf78b7090ee221157e85953f739aa/claude_code_is_programmable_3.py#L79-L140)).
2. **Prompt orchestrator (2025):** a specification plus directory reconnaissance drives parallel generation waves; coordination is still encoded almost entirely in Markdown ([Infinite loop](https://github.com/disler/infinite-agentic-loop/blob/6e9a012f81ef2291faf174d67176f7e69832cc0a/.claude/commands/infinite.md#L17-L108)).
3. **Full workflow and isolation (late 2025):** plan → sandbox build → host → internal/external/UI validation becomes a replayable command chain ([Agent Sandbox workflow](https://github.com/disler/agent-sandbox-skill/blob/ac460eea626bd11a68960b0b8f2dcefc25bfce5c/.claude/skills/agent-sandboxes/prompts/plan-build-host-test.md#L39-L98)).
4. **Composable agentic layer (early 2026):** capability, worker, orchestration, and entry-point layers become independently testable ([Bowser](https://github.com/disler/bowser/blob/26541acddc0626e97e8f4398e47b288e97f97ebd/README.md#L15-L26)).
5. **Independent verification and living plans (spring/summer 2026):** verifier and Planf3 make reviewing and planning explicit, stateful products rather than chat steps ([Verifier](https://github.com/disler/the-verifier-agent/blob/aa18d68bcf886fb2a061ca5a76c6d2e1f3516501/README.md#L59-L77), [Planf3](https://github.com/disler/planf3/blob/f34b7ba5ff8167ef6283791763f4b578bfb3a2c0/README.md#L53-L71)).
6. **Gate-first, multi-model harness (July 2026):** acceptance is executable and designed before implementation; model diversity is assigned by role ([Fusion Harness](https://github.com/disler/fusion-harness/blob/5852f2ed4f5f064a368d83d2dabad84fe6bfa0b4/README.md#L138-L154)).
7. **Code-owned factory (August 2026):** deterministic code owns the graph, typed handoffs, write enforcement, bounded retries, acceptance, and tracing ([SSSF](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/README.md#L16-L18), [hard rules](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/.claude/skills/sssf/SKILL.md#L60-L72)).

## What not to copy literally

- **Do not equate “more agents” with a better system.** The current factory explicitly says the point is choosing correctly among engineer, code, and agent, not merely increasing agent count ([SSSF principles](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/README.md#L106-L116)).
- **Do not leave acceptance inside a reviewer prompt alone.** The recent artifacts use executable gates, deterministic commands, and independent evidence ([Fusion validator](https://github.com/disler/fusion-harness/blob/5852f2ed4f5f064a368d83d2dabad84fe6bfa0b4/extensions/fusion-harness/SYSTEM_PROMPT_VALIDATOR.md#L17-L30)).
- **Do not treat a green test suite as request fidelity.** Tests and semantic review are separate stages ([Inkwell SDLC](https://github.com/disler/inkwell-agent-sandboxes-and-software-factory/blob/86b8dceb5a81a1bbdbaa84c644b058d262a394c3/adws/adw_simple_sdlc.py#L27-L37)).
- **Do not run unbounded “Ralph” loops for implementation.** The artifact-backed implementation loops have explicit caps and escalation ([SSSF loop constants](https://github.com/disler/inkwell-agent-sandboxes-and-software-factory/blob/86b8dceb5a81a1bbdbaa84c644b058d262a394c3/adws/adw_simple_sdlc.py#L52-L54), [Fusion halt](https://github.com/disler/fusion-harness/blob/5852f2ed4f5f064a368d83d2dabad84fe6bfa0b4/README.md#L146-L154)).
- **Do not regard prompt-only read-only rules as security.** The Verifier README admits its read-only Bash policy is not a sandbox ([verifier limitations](https://github.com/disler/the-verifier-agent/blob/aa18d68bcf886fb2a061ca5a76c6d2e1f3516501/README.md#L167-L174)); the later factory verifies actual working-tree changes and rolls back breaches.

## Confidence and limitations

High confidence: the workflow/artifact pattern above appears repeatedly and culminates in executable first-party code. Medium confidence: prevalence counts can change as repositories are added or branches change. Low confidence in any claim that a specific model, token budget, or vendor stack is universally optimal; the repositories themselves increasingly treat those as replaceable configuration.

The most important distinction for the final system design is this: **copy the contracts and feedback loops, not the current tools.**

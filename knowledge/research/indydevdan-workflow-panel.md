# IndyDevDan workflow panel: from idea to verified deliverable

_Panel role: adversarial systems designer_  
_Research date: 2026-08-04_

## Bottom line

IndyDevDan does have a repeatable method, but it is not “use this one agent/tool for every problem.” His fixed layer is the **outer engineering workflow**:

> Pick valuable work → perform and observe it once → write a contract/plan → assign each step to the right actor → execute in isolation → validate with independent evidence → review against the original intent → ship an auditable artifact → improve the reusable system.

The variable layer is the implementation: which model, agent harness, skill, CLI, number of agents, and amount of autonomy. His tool choices change rapidly; the outer method does not. The current expression is a “software factory” in which **the engineer supplies intent and judgment, agents handle ambiguous reading/deciding, and deterministic code owns sequencing, retries, and acceptance** ([Super Simple Software Factory](https://github.com/disler/super-simple-software-factory#why-this-exists), [latest walkthrough](https://www.youtube.com/watch?v=haUfb1ievTE)).

The most important adversarial finding is that a learner should **not** copy the finished factory first. Dan's latest advice is to walk the workflow end to end, step into every node, and only then encode it as agents plus code; start with a simple skill and extract deterministic code when the workflow becomes serious or production-facing ([“Forget Loop Engineering,” 29:03–30:26](https://www.youtube.com/watch?v=VQy50fuxI34)).

## Evidence base and limits

I inspected the workspace before researching externally. It contains 18 first-party course lesson transcripts/artifacts, 56 public YouTube videos from 2025-07-14 through 2026-08-03, and 27 locally materialized public repositories. I also enumerated 208 channel videos and 52 non-fork repositories through the public YouTube and GitHub surfaces, then concentrated close reading on the artifacts that define or change the operating method.

External retrieval used Agent Reach's active YouTube (`yt-dlp`), GitHub (`gh`), Twitter (`twitter-cli`), and general-web backends. Exa was unavailable. X is a weak current source by Dan's own profile—its bio says he is “not really on twitter” and points people to YouTube—so X mainly provides historical evidence. I found no separate first-party conference/talk archive; the YouTube channel is the public long-form talk corpus. The site/course, channel, old blog, X profile, and public repositories are all Dan's first-party material.

High-signal first-party sources include:

- The current canonical implementation: [Super Simple Software Factory](https://github.com/disler/super-simple-software-factory), its [walkthrough](https://www.youtube.com/watch?v=haUfb1ievTE), and the newly isolated [Inkwell sandbox example](https://github.com/disler/inkwell-agent-sandboxes-and-software-factory).
- The conceptual transition from “loops” to full developer workflows: [Forget Loop Engineering](https://www.youtube.com/watch?v=VQy50fuxI34).
- The earlier codification: [Success Is Planned](https://agenticengineer.com/tactical-agentic-coding/course/success-is-planned), [Close the Loops](https://agenticengineer.com/tactical-agentic-coding/course/close-the-loops), [Let Your Agents Focus](https://agenticengineer.com/tactical-agentic-coding/course/let-your-agents-focus), [ZTE](https://agenticengineer.com/tactical-agentic-coding/course/zte-secret-of-agentic-engineering), and [The Agentic Layer](https://agenticengineer.com/tactical-agentic-coding/course/the-agentic-layer).
- The public mental models: [Thinking in Threads](https://agenticengineer.com/thinking-in-threads), [Top 2% Agentic Engineering](https://agenticengineer.com/top-2-percent-agentic-engineering), and [Engineering with Exponentials](https://agenticengineer.com/state-of-ai-coding/engineering-with-exponentials).
- Concrete controls: [Agentic Finance Review](https://github.com/disler/agentic-finance-review), [Pi Verifier Agent](https://github.com/disler/the-verifier-agent), [Bash: Damage From Within](https://github.com/disler/bash-damage-from-within), [Planf3](https://github.com/disler/planf3), [Fusion Harness](https://github.com/disler/fusion-harness), and [Agent Sandbox Skill](https://github.com/disler/agent-sandbox-skill).
- Historical operating beliefs: his 2022 [retrospective](https://danisler.com/blogs/solopreneur-2022-reflection), [Think Bigger](https://danisler.com/blogs/think-bigger), [No-ish and Yes-ish](https://danisler.com/blogs/noish-and-yesish), and X posts on [decide–execute–learn–iterate](https://x.com/IndyDevDan/status/1626016126965633026) and [low-cost/high-impact actions](https://x.com/IndyDevDan/status/1631504710149578756).

## How the method evolved

### 2022–2023: value, time boxes, feedback, and metaprocess

Before “agentic engineering,” the durable pattern was already visible. Dan wrote about Pareto actions, meta-processes that force him to slow down and question actions, deep blocks for MVPs, user/product KPIs, and a “Fill or Kill” rule that time-boxed product work and required evidence to continue ([2022 retrospective](https://danisler.com/blogs/solopreneur-2022-reflection)). His product advice was probabilistic, not dogmatic: rank decisions by expected outcomes and direction rather than pretend there is a universal yes/no answer ([No-ish and Yes-ish](https://danisler.com/blogs/noish-and-yesish)).

The early engineering artifacts follow the same shape: `diffbro` made review a reusable command; `multi-agent-postgres-data-analytics` composed specialized agents; `llm-prompt-testing-quick-start` treated prompts as testable artifacts. The seed was not “more AI.” It was **turn judgment into a repeatable, measurable system**.

### 2024–mid-2025: reusable prompts, evals, and programmable agents

The artifacts moved from one-off AI assistance toward prompt libraries, benchmarks, single-purpose agents, MCP/CLI interfaces, and programmable Claude Code. In public writing he framed “Compute Advantage” as more useful compute and autonomy divided by time, effort, and monetary cost—not raw token volume ([Engineering with Exponentials](https://agenticengineer.com/state-of-ai-coding/engineering-with-exponentials)).

His five interaction patterns made the escalation rule explicit: start with an ad-hoc prompt; when repetition appears (“three times marks a pattern”), make it reusable; add subagents for specialization/parallelism; add deterministic interfaces/code when control is required; build a full application only when its leverage repays its maintenance cost ([Five Agent Patterns](https://www.youtube.com/watch?v=XojxD7hfaD4)).

### Mid-2025–early 2026: the agentic layer and complete lifecycle

Tactical Agentic Coding codified eight tactics: stop hand-coding, adopt the agent's perspective, template engineering, move out of the loop, add feedback loops, give every agent one purpose, target zero-touch execution, and prioritize the agentic layer. The lifecycle became:

> Plan → Build → Test → Review → Document/Generate → Ship.

The crucial distinction is that **test and review answer different questions**: testing asks whether it works; review asks whether what was built is what was requested ([Let Your Agents Focus](https://agenticengineer.com/tactical-agentic-coding/course/let-your-agents-focus)). Plans became scaled prompts containing relevant files, phased work, implementation notes, and validation commands ([Success Is Planned](https://agenticengineer.com/tactical-agentic-coding/course/success-is-planned)).

At the same time, the system acquired context discipline (reduce and delegate), specialization (“one agent, one prompt, one purpose”), typed or file-based handoffs, observability, branches/worktrees/sandboxes, and out-of-loop triggers. Zero-touch engineering was always stated as a **destination reached after evidence**, not a starting mode ([Thinking in Threads](https://agenticengineer.com/thinking-in-threads#z-thread), [ZTE lesson](https://agenticengineer.com/tactical-agentic-coding/course/zte-secret-of-agentic-engineering)).

### 2026: trust, security, verification, model stacks, and factories

The 2026 thesis is “earned trust.” Specialized self-validating agents attach deterministic checks to a narrow task ([Agentic Finance Review](https://github.com/disler/agentic-finance-review)). An independent verifier decomposes every builder claim into atomic, provable units and loops concrete failures back, with a bounded retry cap and human escalation ([Pi Verifier](https://github.com/disler/the-verifier-agent#how-it-works)). Security moved from prompt-based restraint to enforced capabilities: allowlist specific commands or remove Bash entirely for production work ([Bash: Damage From Within](https://github.com/disler/bash-damage-from-within#the-5-levels)).

Planning also became a maintained executable artifact rather than a disposable preamble: Planf3 routes create, update, reference, build, and image workflows through one living plan with phase checklists and validation loops ([Planf3](https://github.com/disler/planf3#the-plan-template)). Fusion work separates independent perspectives, merges them with attribution, and creates the acceptance gate before building; a baseline that is already green is treated as a suspicious/weak gate ([Fusion Harness](https://github.com/disler/fusion-harness#the-auto-validation-loop)).

The latest consolidation rejects “loop engineering” as too narrow. A software factory is a collection of AI Developer Workflows that place three actors—engineer, agents, deterministic code—at the correct nodes. The current implementation uses Python as the control plane, agents as bounded phases, typed JSON envelopes for handoffs, gates as definitions of done, SQLite traces for observability, and a skill for installation/operation ([SSSF README](https://github.com/disler/super-simple-software-factory)). The next-day Inkwell artifact closes a known gap by putting the factory and agents inside a disposable VM, then harvesting commits back to the host ([Inkwell sandbox example](https://github.com/disler/inkwell-agent-sandboxes-and-software-factory)).

## Reconstructed end-to-end operating loop

This is the recurring structure underneath the changing vocabulary and tools.

1. **Choose a valuable problem class.** Start from a real user/engineer pain, preferably one you experience. Ask whether this is a one-off or likely repetition. Time-box discovery and define the evidence that justifies continued investment.
2. **Perform one legible run.** Work in-loop and observe how the result is actually produced. Agents may perform the actions, but the engineer walks through every node, sees the pass/fail conditions, and learns where judgment is required. Do not automate a process you cannot explain.
3. **Write the contract before the build.** Record purpose, outcome, non-goals, assumptions/open questions, relevant files, blast radius, phases, and an executable definition of done. The plan is an artifact for engineer, team, and agents—not private model reasoning.
4. **Route every step to one of three actors.** The engineer owns intent, tradeoffs, and irreversible decisions. Deterministic code owns known commands, sequencing, gates, state, retries, and acceptance. A focused agent owns reading, synthesis, diagnosis, generation, or judgment that cannot be reduced to a known command.
5. **Configure each agent's Core Four.** Give it the minimum sufficient context, the appropriate model/cost tier, one focused prompt, and the least-powerful tools/write boundary that can finish its phase. Do not give every agent the whole codebase and every tool.
6. **Execute through explicit seams in isolation.** Use one agent/prompt/purpose per phase; move context through plans, files, or typed envelopes rather than a giant shared conversation. Use a branch/worktree for low-risk local work and a sandbox/throwaway VM when parallelism, long runtime, credentials, or blast radius demand it. Trace tool calls, cost, timing, outputs, and state.
7. **Close deterministic feedback paths first.** Run lint, type-check, build, unit/integration/E2E tests, schema checks, or domain validators as code. Feed exact failures back into the same builder session. Cap retries; escalate rather than loop forever.
8. **Review independently against the contract.** A different agent or human asks “is this what we asked for?” and checks claims against actual state. Security review and diff inspection are separate from functional tests. Human approval remains at high-risk seams until the system has earned evidence-based autonomy.
9. **Package and ship evidence.** Produce a diff, test/gate reports, review verdict, docs for future agents, commits, and a PR or harvested branch. The deliverable is not “agent said done”; it is the artifact plus the evidence chain.
10. **Compound the agentic layer.** Inspect the trace and every unverifiable gap. Fix the prompt, template, validator, capability boundary, handoff type, or workflow—not merely the current output. Benchmark the changed system on real recurring tasks. Promote it to an out-of-loop workflow only after repeated green runs.

## A compact fixed methodology a learner can execute

Call it **TRACE**. It preserves Dan's stable method without copying any surface tool.

### T — Target the class and the proof

- State the valuable outcome in one sentence.
- Name the recurring problem class and beneficiary.
- Write non-goals and blast radius.
- Define proof before work: commands, observable behavior, review rubric, rollback.
- If no objective proof exists, the first deliverable is a validator/fixture—not the feature.

### R — Run it once and record the real workflow

- Complete one in-loop run with an agent while observing every step.
- Draw the nodes and handoffs: scout → plan → build → test → review → document → ship, deleting nodes that do not add value.
- Mark each node `E` (engineer judgment), `C` (deterministic code), or `A` (agent judgment).
- Record failure cases and what information the next node actually needs.

### A — Artifactize the contract and configure the Core Four

- Save one plan/spec containing purpose, relevant files, phases, checklists, and validation commands.
- For each `A` node: one purpose, minimal context, appropriate model, least tools/writes.
- For every seam: declare an output schema or named file. No handoff by vague chat summary.
- Put repeated knowledge in version-controlled prompts/templates/skills, not personal memory.

### C — Compose, contain, and close feedback

- Run in a branch/worktree/sandbox appropriate to risk.
- Let code own sequencing and known checks; let agents propose/diagnose/build.
- Run gates after every material phase; on failure, return exact evidence to the responsible agent in the same session.
- Use an independent reviewer against the original contract.
- Set explicit retry, cost, time, and permission limits; escalate at the cap.

### E — Evidence, export, and evolve

- Ship only with: artifact/diff + validation output + review verdict + documentation + rollback path.
- Merge manually until repeated evidence makes human review the bottleneck.
- After each run, classify every failure as prompt, context, tool, model, gate, architecture, or environment.
- Improve the reusable primitive, rerun a representative task, and track the trend.

TRACE's fixed rule is: **never advance on an assertion when you can advance on evidence**.

### Routing rules inside TRACE

| Situation | Use |
|---|---|
| Novel, low-risk, one-off work | One in-loop agent thread |
| Same instruction has appeared roughly three times | Reusable prompt/skill/template |
| A step has distinct context or expertise | A specialized agent |
| Alternatives are independent and value exceeds cost | Parallel isolated attempts, then explicit fusion/selection |
| Invocation and expected result are already known | Deterministic code, not an agent |
| The same multi-step path repeats | An AI Developer Workflow with typed handoffs and gates |
| Long-running, parallel, or risky work | Sandbox/throwaway environment with harvested output |
| High-impact or irreversible action | Human checkpoint plus architectural permission boundary |
| Repeated green evidence and review is the bottleneck | Gradually reduce checkpoints; only then consider zero-touch |

## Tensions and contradictions that matter

| Apparent contradiction | Adversarial resolution |
|---|---|
| **“Stop coding” vs “code owns the graph.”** | “Stop coding” means stop spending scarce human attention typing routine application code. The mature system deliberately writes and reads deterministic control code because agents alone are variable, expensive, and hard to audit. |
| **One agent is not enough vs one agent/one prompt/one purpose.** | Scale the number of narrow roles only when decomposition, independent verification, or parallel exploration creates value. A simple feature may still be a single-agent task; the latest walkthrough says so explicitly. |
| **More compute creates trust vs risk compounds with runtime.** | More agents/tokens create more candidate work and verification opportunities, not automatic trust. Trust rises only when independent evidence, isolation, least privilege, and bounded retries rise with compute. The security repo warns that even small per-turn failure probabilities compound over long runs. |
| **Zero-touch shipping vs review is especially important.** | ZTE is the destination after the system proves itself; it is dangerous as a default. The current SSSF openly says its base version lacks sandbox, branch-per-run, merge, and human approval, and its sample tests are placeholders until customized. |
| **Closed loops vs “forget loop engineering.”** | He has not abandoned feedback loops. He rejects treating the loop as the whole system. The unit is the complete developer workflow; retries are merely one control-flow primitive inside it. |
| **MCP/custom agents/Claude Code/Pi/software factories as the “next level.”** | The favored surface changes. His durable abstraction is the Core Four plus explicit interfaces, ownership, and evidence. Tool loyalty is tactical; by 2026 he argues for model stacks and “AND, not OR.” |
| **A fixed method vs thinking in probabilities.** | Dan's old writing explicitly rejects universal yes/no answers. The fixed element must therefore be the evidence-seeking outer process, not a predetermined technical answer. TRACE always follows the same steps while allowing evidence to change the route. |
| **Maximum autonomy vs “do it by hand first.”** | He means execute and inspect the workflow end to end before automating it, not necessarily type every line manually. Automation without process knowledge produces fast, opaque failure. |

## Hidden prerequisites

The polished demos obscure what must already exist:

1. **Domain judgment.** Someone must know what a good plan, implementation, review, and user experience look like. Templates encode expertise; they do not create it.
2. **Oracles.** Real tests, fixtures, validators, rubrics, staging signals, or user metrics must distinguish good from bad. Placeholder commands that exit zero create validation theater; SSSF calls this its first customization requirement.
3. **Legible architecture.** Types, modular boundaries, documentation, deterministic setup, and executable commands let agents navigate and self-correct.
4. **Version control and recovery.** Branches, commits, rollback, artifact harvesting, and reproducible environments are prerequisites for autonomy.
5. **Security boundaries.** Prompts are not enforcement. Production-capable systems need least privilege, allowlists/custom tools, secrets isolation, and sandboxing.
6. **Observability.** Without traces of prompts, tool calls, cost, state, outputs, gates, and failures, improvement is storytelling rather than engineering.
7. **A recurrence threshold.** A factory has a maintenance cost. One-offs should usually remain simple; the system earns its complexity across the hundredth and thousandth run.
8. **Budget and caps.** Parallel/fusion/verifier systems exchange tokens and latency for confidence. Their retry, cost, and runtime ceilings must be designed up front.

## Failure modes and countermeasures

| Failure mode | Countermeasure |
|---|---|
| Automating a process nobody has completed or understood | Run one legible end-to-end execution; draw it before encoding it. |
| Starting with the complete factory | Begin with a prompt/skill and one real gate; add machinery only when a repeated failure justifies it. |
| “Green” placeholder or weak tests | Require the gate to fail on the pre-change baseline; verify every explicit requirement maps to a concrete check. |
| Builder grades its own work | Separate deterministic tests and an independent reviewer/verifier from the builder. |
| Plan is polished but not executable | Every phase needs files, commands, acceptance criteria, and a handoff contract; visuals are optional. |
| Context pollution or stale assumptions | Minimum sufficient context, specialized phases, fresh sessions when needed, typed/file handoffs, deliberate reference loading. |
| Shared working directory races | One branch/worktree/sandbox per writer; fuse or harvest after workers finish. |
| Broad Bash/tools turn a mistake into catastrophe | Allowlist exact operations, pin scripts, or remove general execution tools; isolate production credentials. |
| Infinite self-correction burns time/tokens | Bounded retry count, cost/time caps, diagnostic escalation, then human decision. |
| Multi-agent theater | Add an agent only for independent evidence, distinct expertise/context, parallel alternatives, or a measurable bottleneck. |
| Premature zero-touch | Track repeated green streaks and severity-weighted escapes; remove human checkpoints gradually. |
| Tool/model churn rewrites the whole system | Keep roles and contracts independent of model IDs/harness; evaluate on private, real workflows. |
| Fixing one output instead of the class | Every incident updates a prompt, template, gate, permission, or workflow and is followed by a regression task. |
| Factory activity loses sight of user value | Preserve product/user acceptance and post-ship metrics; internal gate success is not market success. |

## Metrics that reflect the method

Dan's earlier agentic KPIs are **attempts down, work size up, green streak up, human presence down**; Thinking in Threads reframes scaling as width, duration, depth, and fewer checkpoints. The latest artifacts add tokens, latency, cost, and phase-level acceptance. A learner should track only this compact scorecard per problem class:

- First-pass acceptance rate and attempts to green.
- Severity-weighted defects escaping gates/review.
- Human minutes and checkpoints per accepted deliverable.
- Median work size and autonomous runtime per run.
- Cost and latency per accepted deliverable, not per prompt.
- Green streak across representative repeated tasks.
- Unverifiable claims/gaps reported by the reviewer.
- User/production outcome after shipping.

Do not optimize “number of agents,” raw tokens, or tool calls in isolation. They are inputs. Accepted value with bounded risk is the outcome.

## Recommended learner starting point

For the first recurring workflow, create only:

```text
specs/                  # the work contract and definition of done
prompts/                # one focused prompt per role
scripts/validate.*      # real deterministic checks
adws/                   # one thin script: plan → build → validate → review
runs/ or trace db       # prompt/config/output/gate evidence
```

Start with one planner/builder if the work is simple, one deterministic validator, and one independent review pass. Run it manually three times. Only after the same route and failures repeat should it become an out-of-loop, sandboxed workflow. This captures the same agentic layer logic without inheriting Dan's current toolchain, model assumptions, or maintenance burden.

## Final panel judgment

The reproducible “IndyDevDan advantage” is not a prompt library, Claude/Pi configuration, agent roster, or repository layout. It is a discipline:

1. Find leverage in a real recurring problem.
2. Convert tacit judgment into an explicit plan, routing, and evidence contract.
3. Put deterministic behavior in code and ambiguous work in narrowly configured agents.
4. Make every claim earn passage through an independent gate.
5. Feed each failure back into the reusable agentic layer.

Follow that discipline and the layer compounds. Copy only the visible tools and it decays as soon as the next model or harness arrives.

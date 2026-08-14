# IndyDevDan's core philosophy and repeatable mental models

_Research date: 2026-08-04_

## Scope and evidence standard

This note reconstructs IndyDevDan's philosophy from first-party material only: his official blog, Agentic Engineer course pages and transcripts, his YouTube channel and transcripts, and repositories published under `disler`. I searched the full course and recent-channel corpus mirrored in this repository, then used the recurring sources below as anchors. I found no substantive first-party podcast or external interview that added a distinct framework, so I did not pad the evidence with third-party summaries.

This is a reconstruction, not a claim that every slogan is a formal definition. I distinguish direct recurring positions from my synthesis. Short phrases are retained where they function as named concepts; everything else is paraphrased.

## Executive reconstruction

IndyDevDan's central idea is: an engineer should stop treating AI as an interactive code generator and instead design a reusable, observable, self-validating system in which humans, agents, and deterministic code each do the work they are best suited to do. The engineer's leverage comes from the system around the agents—the agentic layer or software factory—not from any single prompt or model. [Hello Agentic Coding](https://agenticengineer.com/tactical-agentic-coding/course/hello-agentic-coding), [Top #1 Opportunity for Senior Engineers](https://www.youtube.com/watch?v=2KcITKKJikA), [Forget Loop Engineering](https://www.youtube.com/watch?v=VQy50fuxI34), [Super Simple Software Factory](https://github.com/disler/super-simple-software-factory)

The human moves up the abstraction stack. Instead of spending most cycles implementing, the human defines valuable outcomes, supplies domain judgment, plans, creates acceptance tests, owns the harness, observes behavior, and improves the reusable workflow after failures. Hands-on human presence should fall only as evidence and confidence rise; visibility should not fall with it. [The 12 Leverage Points](https://agenticengineer.com/tactical-agentic-coding/course/the-12-leverage-points), [PLANS For Fable 5](https://www.youtube.com/watch?v=DzbqeO_diOQ), [The Verifier Agent](https://github.com/disler/the-verifier-agent), [SEE CMUX SOLVE Multi-Agent Orchestration](https://www.youtube.com/watch?v=WAFUMBLOjHo)

His deepest invariant predates the current agent vocabulary: maximize useful impact per unit of scarce human time. In 2022 he described this as finding force multipliers and building processes whose outputs greatly exceed their inputs; his current agentic layer is the same leverage thesis applied to generative compute. [Reflecting on 2021](https://indydevdan.com/blogs/reflecting-on-2021), [Stop Wasting Time and Automate](https://indydevdan.com/blogs/stop-wasting-time-and-automate), [IndyDevDan's Blog](https://indydevdan.com/)

## The philosophy beneath the tooling

### 1. Start with human value, not automation

His earlier product writing centers people and user value. He recommends identifying a “critical hypothesis”: the one question that must be true for a product or feature to succeed, and then gathering evidence for or against it. The modern agentic system is therefore not an automation goal by itself; it is a force multiplier for producing valuable outcomes. [Reflecting on 2021](https://indydevdan.com/blogs/reflecting-on-2021), [Hello Agentic Coding](https://agenticengineer.com/tactical-agentic-coding/course/hello-agentic-coding)

The most stable decision rule across his work is to choose tools that reduce the distance between the engineer and the goal, rather than chasing every new tool. This is why his frameworks are intentionally more durable than any particular model or coding agent. [You Can't Keep Up](https://indydevdan.com/blogs/you-cant-keep-up), [The 12 Leverage Points](https://agenticengineer.com/tactical-agentic-coding/course/the-12-leverage-points)

### 2. Leverage is the objective function

He defines leverage as an asymmetric input/output relationship: invest once in a tool, process, template, or system and receive repeated output. Automation is valuable because it preserves future human time, and meta-work is valuable because it improves the schedule or system that produces all subsequent work. [Reflecting on 2021](https://indydevdan.com/blogs/reflecting-on-2021), [Stop Wasting Time and Automate](https://indydevdan.com/blogs/stop-wasting-time-and-automate)

The modern version is “build the system that builds the system.” The unit of engineering investment moves from a feature to the factory that can repeatedly produce that class of feature on-spec. [Top #1 Opportunity for Senior Engineers](https://www.youtube.com/watch?v=2KcITKKJikA), [The Agentic Layer](https://agenticengineer.com/tactical-agentic-coding/course/the-agentic-layer), [Forget Loop Engineering](https://www.youtube.com/watch?v=VQy50fuxI34)

### 3. Think before compressing work into a system

His older “Think – Plan – Build” motif matters. He argues that dedicated thought makes apparent complexity resolve into a series of smaller steps and that requirements become simpler after the problem has been mentally modeled. The newer planning material preserves that sequence: first think and exercise domain judgment, then use an agent to encode that judgment into a reusable plan format. [To Simplify: Think](https://indydevdan.com/blogs/to-simplify-think), [PLANS For Fable 5](https://www.youtube.com/watch?v=DzbqeO_diOQ)

This means his system is not “outsource thinking to the model.” The model scales a human's engineering formula; it should not invent the formula in a black box. His recent plan skill explicitly treats domain knowledge as the differentiator and the plan template as a way to teach agents how the team engineers. [PLANS For Fable 5](https://www.youtube.com/watch?v=DzbqeO_diOQ), [Planf3](https://github.com/disler/planf3)

### 4. Master primitives, then compose them

He repeatedly works from small, inspectable primitives—prompts, tool calls, tests, plans, agents, scripts—and composes them into higher-order workflows. His claim is not that one fixed software-development sequence fits every task; it is that arbitrary problem classes can be handled by different compositions of a stable set of primitives. [ZTE: The Secret of Agentic Engineering](https://agenticengineer.com/tactical-agentic-coding/course/zte-secret-of-agentic-engineering), [The Agentic Layer](https://agenticengineer.com/tactical-agentic-coding/course/the-agentic-layer), [Forget Loop Engineering](https://www.youtube.com/watch?v=VQy50fuxI34)

That is the important answer to the desire for a single IIT-JEE-like method: the universal part is a meta-method for constructing and improving workflows; the execution graph changes by problem class. A bug, feature, research task, deployment, and UI review should share a design discipline without being forced through an identical sequence. [Success Is Planned](https://agenticengineer.com/tactical-agentic-coding/course/success-is-planned), [ZTE: The Secret of Agentic Engineering](https://agenticengineer.com/tactical-agentic-coding/course/zte-secret-of-agentic-engineering)

## Core definitions

| Term | Reconstructed definition | First-party evidence |
|---|---|---|
| **AI coding** | A model generates code from context and a prompt. It accelerates implementation, but it does not by itself perform the full engineering workflow. | [Hello Agentic Coding](https://agenticengineer.com/tactical-agentic-coding/course/hello-agentic-coding) |
| **Agentic coding / agentic engineering** | Engineering with systems that can reliably execute long tool-call sequences and complete real workflows. In its mature form, the engineer designs a software factory that places engineers, agents, and deterministic code at the appropriate nodes. | [Hello Agentic Coding](https://agenticengineer.com/tactical-agentic-coding/course/hello-agentic-coding), [Forget Loop Engineering](https://www.youtube.com/watch?v=VQy50fuxI34) |
| **Core Four** | The four variables inside an agent execution: context, model, prompt, and tools. Mastering the agent means deliberately controlling all four rather than relying on defaults. | [The 12 Leverage Points](https://agenticengineer.com/tactical-agentic-coding/course/the-12-leverage-points), [Super Simple Software Factory](https://github.com/disler/super-simple-software-factory) |
| **Agentic layer** | A separable ring around the application containing agent-oriented prompts, specs, tools, workflows, tests, observability, and orchestration. It teaches agents how to operate the application on the team's behalf. | [The Agentic Layer](https://agenticengineer.com/tactical-agentic-coding/course/the-agentic-layer), [The Codebase Singularity](https://www.youtube.com/watch?v=fop_yxV-mPo) |
| **AI Developer Workflow (ADW)** | A reusable workflow in which deterministic code sequences one or more agentic prompts, passes context, handles triggers, logging, gates, and retries, and produces an engineering result. | [AFK Agents](https://agenticengineer.com/tactical-agentic-coding/course/afk-agents), [Forget Loop Engineering](https://www.youtube.com/watch?v=VQy50fuxI34), [Super Simple Software Factory](https://github.com/disler/super-simple-software-factory) |
| **Software factory** | The higher-level system of agents plus code that routes a request through the appropriate workflow and can operate repeatedly with minimal human intervention. Its value is reproducible leverage, not merely more agents. | [Top #1 Opportunity for Senior Engineers](https://www.youtube.com/watch?v=2KcITKKJikA), [Forget Loop Engineering](https://www.youtube.com/watch?v=VQy50fuxI34), [My Super Simple Software Factory](https://www.youtube.com/watch?v=haUfb1ievTE) |
| **Specification / plan** | A scaled prompt and executable contract: purpose, relevant context and files, phased tasks, acceptance criteria, and validation commands. It is a living artifact shared by the engineer, team, and agents, not a disposable preamble. | [Success Is Planned](https://agenticengineer.com/tactical-agentic-coding/course/success-is-planned), [PLANS For Fable 5](https://www.youtube.com/watch?v=DzbqeO_diOQ), [Planf3](https://github.com/disler/planf3) |
| **Context engineering** | Selecting the minimum sufficient, task-relevant information that puts an agent in the performance sweet spot. The two control operations are Reduce and Delegate. | [Elite Context Engineering](https://agenticengineer.com/tactical-agentic-coding/course/rd-framework-context-window-mastery), [Elite Context Engineering with Claude Code](https://www.youtube.com/watch?v=Kf5-HWJPTIE) |
| **Closed loop** | A request–validate–resolve cycle in which an agent performs work, receives concrete feedback from a test or verifier, corrects the failure, and repeats until the gate passes or escalation is required. | [Close the Loops](https://agenticengineer.com/tactical-agentic-coding/course/close-the-loops), [The Verifier Agent](https://github.com/disler/the-verifier-agent) |
| **Agent Expert** | A specialized agent with a topic-specific external mental model that follows Act–Learn–Reuse: perform useful work, store validated learning, and apply it on the next execution. | [Agent Experts](https://agenticengineer.com/tactical-agentic-coding/course/agent-experts), [Agent Experts video](https://www.youtube.com/watch?v=zTcDwqopvKE) |
| **Zero-Touch Engineering (ZTE)** | A north-star maturity state where a trusted workflow can plan, build, test, review, document, and ship from one initiating touch. It is approached incrementally after review and validation systems create sufficient confidence. | [ZTE: The Secret of Agentic Engineering](https://agenticengineer.com/tactical-agentic-coding/course/zte-secret-of-agentic-engineering), [The Verifier Agent](https://github.com/disler/the-verifier-agent) |
| **Codebase singularity** | The point at which the agentic layer operates the codebase more reliably or effectively than the human or team can directly. | [Building Agentic Layers](https://agenticengineer.com/tactical-agentic-coding/course/building-agentic-layers), [The Codebase Singularity](https://www.youtube.com/watch?v=fop_yxV-mPo) |

## Named repeatable mental models

### The 12 leverage points

The first four are internal to every agent: **context, model, prompt, tools**. The other eight are external structures that the agent can use: **standard output, types, documentation, tests, architecture, plans, templates, and ADWs**. His diagnostic question is not “why is the model bad?” but “which leverage point did the system fail to provide?” [The 12 Leverage Points](https://agenticengineer.com/tactical-agentic-coding/course/the-12-leverage-points)

The governing tactic is to adopt the agent's perspective. A fresh agent is capable but context-poor; the engineer must provide the information, resources, affordances, and feedback they would need to solve the task. That perspective also motivates agent-readable architecture, clear names, standard output, local documentation, and executable tests. [The 12 Leverage Points](https://agenticengineer.com/tactical-agentic-coding/course/the-12-leverage-points)

### The agentic KPIs

He proposes four directional measures:

- **Size up:** increase the amount and duration of meaningful work a system can accept in one handoff.
- **Attempts down:** reduce human re-prompts or correction cycles for a result.
- **Streak up:** increase consecutive one-shot successes.
- **Presence down:** reduce the number of points at which a human must sit with, guide, or correct the system.

These are explicitly meant to replace the feeling of “it shipped once” with a measurable trajectory of autonomous reliability. [The 12 Leverage Points](https://agenticengineer.com/tactical-agentic-coding/course/the-12-leverage-points), [Close the Loops](https://agenticengineer.com/tactical-agentic-coding/course/close-the-loops)

The KPIs must be read together. Increasing task size while attempts explode is not progress; lowering presence by removing review without evidence is not trust. The intended movement is larger work, fewer corrections, longer success streaks, and less hands-on intervention as the agentic layer improves. [The 12 Leverage Points](https://agenticengineer.com/tactical-agentic-coding/course/the-12-leverage-points), [ZTE: The Secret of Agentic Engineering](https://agenticengineer.com/tactical-agentic-coding/course/zte-secret-of-agentic-engineering)

### PITER for out-of-loop systems

PITER names the four requirements for an AFK workflow: **Prompt input, Trigger, Environment, Review**. His examples use an issue as the input, a webhook as the trigger, an isolated worktree or sandbox as the environment, and a pull request as the review surface. The concrete technologies are replaceable; the four functions are the durable pattern. [AFK Agents](https://agenticengineer.com/tactical-agentic-coding/course/afk-agents)

### Request–Validate–Resolve

A closed-loop prompt requests work, validates the result with a concrete oracle, and gives failures back to an agent for resolution. Oracles can include linting, compilation, unit tests, end-to-end browser tests, logs, external monitoring, evaluations, or a specialized verifier. [Close the Loops](https://agenticengineer.com/tactical-agentic-coding/course/close-the-loops), [The Verifier Agent](https://github.com/disler/the-verifier-agent)

The loop is not “keep prompting until it looks right.” Its power comes from explicit pass/fail information that is independent of the builder's own assertion. [Close the Loops](https://agenticengineer.com/tactical-agentic-coding/course/close-the-loops), [The Verifier Agent](https://github.com/disler/the-verifier-agent)

### One agent, one prompt, one purpose

Different phases require different context, tools, and questions. A planning agent asks what should be built; a test agent asks whether it works; a review agent asks whether the result matches the specification; a documentation agent explains how it works. Fresh, specialized contexts reduce pollution and make each step reproducible and evaluable. [Let Your Agents Focus](https://agenticengineer.com/tactical-agentic-coding/course/let-your-agents-focus)

This is specialization, not agent-count maximalism. Multiple agents create value when they supply independent focus, perspective, context windows, or verification—not merely because many instances ran. [The Verifier Agent](https://github.com/disler/the-verifier-agent), [My Super Simple Software Factory](https://www.youtube.com/watch?v=haUfb1ievTE)

### Act–Learn–Reuse

Ordinary agents repeatedly start from zero. An Agent Expert performs a useful action, extracts and validates new domain knowledge, stores it in a topic-specific expertise file, and reuses that mental model on later executions. The code remains the source of truth, and the learning procedure—not ad hoc human edits—should govern expertise updates. [Agent Experts video](https://www.youtube.com/watch?v=zTcDwqopvKE), [Agent Experts](https://agenticengineer.com/tactical-agentic-coding/course/agent-experts)

### The five compounding pillars

His 2026 umbrella framework is:

1. **Own the agent harness** so prompts, tools, policies, and specializations are under your control.
2. **Build a software factory** that produces result classes, not individual features.
3. **Build extensible software** so models, tools, and workflow nodes can be swapped.
4. **Turn on always-on agents only after useful token economics are proven.**
5. **Provide agentic access** through APIs, CLIs, webhooks, or RPC so agents can operate systems directly.

These pillars relocate advantage from picking a model to engineering the environment and interfaces around the model. [Top #1 Opportunity for Senior Engineers](https://www.youtube.com/watch?v=2KcITKKJikA)

## Specifications and planning

### What a specification is for

The plan is the primary communication artifact between intent and execution. It should tell a fresh agent why the work exists, what is in scope, which files and systems matter, how work is phased, and exactly how completion will be proven. [Success Is Planned](https://agenticengineer.com/tactical-agentic-coding/course/success-is-planned), [Planf3](https://github.com/disler/planf3)

A strong plan is also a review oracle. Testing determines whether the implementation functions; review compares the implementation to the original requested outcome. Without a sufficiently explicit spec, that second question cannot be answered reliably. [Let Your Agents Focus](https://agenticengineer.com/tactical-agentic-coding/course/let-your-agents-focus), [The Verifier Agent](https://github.com/disler/the-verifier-agent)

### His current plan anatomy

The current Planf3 artifact includes:

- Purpose, problem, and proposed solution.
- Relevant existing files and expected new files.
- Phases with ordered tasks and live status markers.
- A testing strategy and concrete validation commands for each phase.
- Metadata, session/commit references, amendments, and related-plan links.
- A validation loop that blocks completion until all required checks pass.

The exact HTML and image-rich format is a current implementation choice; the durable principle is a rich, inspectable, executable artifact serving the engineer, team, and agents together. [Planf3](https://github.com/disler/planf3), [PLANS For Fable 5](https://www.youtube.com/watch?v=DzbqeO_diOQ)

### Planning is a reusable skill, not a one-off document

The template encodes the team's engineering judgment once and reproduces it across problem instances. Plan creation, plan update, reference maintenance, build execution, and visual generation are separate workflows around the same living artifact. [Planf3](https://github.com/disler/planf3)

The principle is to invest more before implementation to reduce review cost later. This is deliberately a performance-versus-speed/cost trade: important work can justify more tokens and slower planning if it raises execution precision. [PLANS For Fable 5](https://www.youtube.com/watch?v=DzbqeO_diOQ), [Planf3](https://github.com/disler/planf3)

## Context engineering

Context is a limited, temporal working resource. Performance is not monotonically improved by adding information; there is a task-dependent sweet spot, and irrelevant or contradictory material creates context rot. [Elite Context Engineering](https://agenticengineer.com/tactical-agentic-coding/course/rd-framework-context-window-mastery), [Elite Context Engineering with Claude Code](https://www.youtube.com/watch?v=Kf5-HWJPTIE)

His R&D framework says every context action is one of two things:

- **Reduce:** remove irrelevant always-on instructions, unused tool schemas, duplicate material, and noise; prime only for the current task.
- **Delegate:** move a subproblem and its context into a fresh specialized agent, then return only the useful result.

[Elite Context Engineering](https://agenticengineer.com/tactical-agentic-coding/course/rd-framework-context-window-mastery), [Elite Context Engineering with Claude Code](https://www.youtube.com/watch?v=Kf5-HWJPTIE)

The practical corollary is “minimum sufficient context,” not “maximum context.” Every phase receives the context appropriate to its purpose, and typed handoff envelopes or artifacts carry only the information needed across seams. [Let Your Agents Focus](https://agenticengineer.com/tactical-agentic-coding/course/let-your-agents-focus), [Super Simple Software Factory](https://github.com/disler/super-simple-software-factory)

## Verification and trust

### Testing and review are different gates

Testing asks whether the system works and whether regressions occurred. Review asks whether the system built what the specification requested. A mature workflow needs both, because a functional implementation can still be off-spec. [Let Your Agents Focus](https://agenticengineer.com/tactical-agentic-coding/course/let-your-agents-focus)

### Deterministic code should own what is deterministic

His newest factory design explicitly assigns sequencing, retries, and acceptance to code, while bounding agents inside phases that require reading and judgment. A known command such as a linter or test runner should execute directly; there is no reason to spend an agent turn rediscovering it. [Super Simple Software Factory](https://github.com/disler/super-simple-software-factory), [My Super Simple Software Factory](https://www.youtube.com/watch?v=haUfb1ievTE)

This updates, rather than contradicts, his earlier agent-centric language. The goal was never “agents everywhere”; the goal is the most reliable and leveraged combination of the three actors: human, agent, and code. [Forget Loop Engineering](https://www.youtube.com/watch?v=VQy50fuxI34), [My Super Simple Software Factory](https://www.youtube.com/watch?v=haUfb1ievTE)

### Independent verification breaks the review bottleneck

His verifier pattern gives a second, read-only agent the builder's claims and session evidence. The verifier decomposes claims into atomic propositions, checks them against actual state with deterministic tools where possible, and sends corrective feedback only when necessary. After a bounded number of failed loops, it escalates to the human. [The Verifier Agent](https://github.com/disler/the-verifier-agent), [GPT-5.5 VERIFIED Opus 4.7](https://www.youtube.com/watch?v=EnXKysJNz_8)

Trust is therefore earned through observability, independent evidence, bounded feedback loops, safety policies, and escalation—not through the builder saying it is finished. [The Verifier Agent](https://github.com/disler/the-verifier-agent), [SEE CMUX SOLVE Multi-Agent Orchestration](https://www.youtube.com/watch?v=WAFUMBLOjHo)

## Learning and improvement loops

There are three distinct loops in his system and they should not be conflated:

1. **Execution loop:** request → validate → resolve until a gate passes or escalation occurs. [Close the Loops](https://agenticengineer.com/tactical-agentic-coding/course/close-the-loops)
2. **Expertise loop:** act → learn → reuse validated domain knowledge on the next run. [Agent Experts](https://agenticengineer.com/tactical-agentic-coding/course/agent-experts), [Agent Experts video](https://www.youtube.com/watch?v=zTcDwqopvKE)
3. **Factory improvement loop:** observe failures and unverifiable claims, then improve the version-controlled prompt, test, persona, tool, or workflow so the whole problem class benefits. [The Verifier Agent](https://github.com/disler/the-verifier-agent), [Let Your Agents Focus](https://agenticengineer.com/tactical-agentic-coding/course/let-your-agents-focus)

This third loop is the essence of “template your engineering.” A one-off correction fixes one run; an edit to the reusable system prevents or detects the same class of failure in future runs. [Success Is Planned](https://agenticengineer.com/tactical-agentic-coding/course/success-is-planned), [The Verifier Agent](https://github.com/disler/the-verifier-agent)

Observability is a prerequisite for learning. If prompts, tool calls, costs, failures, and results are opaque, the engineer cannot identify which leverage point or workflow node needs improvement. [SEE CMUX SOLVE Multi-Agent Orchestration](https://www.youtube.com/watch?v=WAFUMBLOjHo), [My Super Simple Software Factory](https://www.youtube.com/watch?v=haUfb1ievTE)

## The role of the human

### What the human retains

The human retains responsibility for valuable intent, architecture, direction, domain judgment, trade-offs, safety boundaries, and the definition of done. His “stop coding” position reallocates engineering attention; it does not make code understanding, architecture, or responsibility optional. [Hello Agentic Coding](https://agenticengineer.com/tactical-agentic-coding/course/hello-agentic-coding), [The 12 Leverage Points](https://agenticengineer.com/tactical-agentic-coding/course/the-12-leverage-points)

At the ordinary out-of-loop level, the human appears at the two constraints: planning at the beginning and reviewing at the end. The factory handles the work between those boundaries. As verification matures, some review can move to specialized agents and code, but unresolved or high-risk conditions still escalate. [Forget Loop Engineering](https://www.youtube.com/watch?v=VQy50fuxI34), [The Verifier Agent](https://github.com/disler/the-verifier-agent)

The human also owns the agent harness and the factory. Whoever controls the prompts, tools, policies, context, model roster, routing, and acceptance logic controls the result. Outsourcing that layer caps specialization and makes improvement harder. [Top #1 Opportunity for Senior Engineers](https://www.youtube.com/watch?v=2KcITKKJikA), [The Verifier Agent](https://github.com/disler/the-verifier-agent)

### What the human should progressively relinquish

The human should stop manually performing repeatable implementation, test execution, routine review, environment operation, and correction work once those activities can be expressed as reliable prompts, code, or gates. The trigger in his earlier course is simple: when a workflow repeats enough to reveal a pattern, automate and template it. [Stop Wasting Time and Automate](https://indydevdan.com/blogs/stop-wasting-time-and-automate), [The 12 Leverage Points](https://agenticengineer.com/tactical-agentic-coding/course/the-12-leverage-points), [AFK Agents](https://agenticengineer.com/tactical-agentic-coding/course/afk-agents)

Presence should fall in stages: in-loop work, then out-of-loop prompt plus human review, then zero-touch only for workflows whose gates and evidence make human review the bottleneck rather than the safety mechanism. [ZTE: The Secret of Agentic Engineering](https://agenticengineer.com/tactical-agentic-coding/course/zte-secret-of-agentic-engineering)

## A synthesized canonical method

The following is my synthesis of his repeated principles, not a verbatim IndyDevDan checklist. It is the closest faithful version of a universal method:

1. **Name the valuable outcome and critical hypothesis.** State who benefits, what must change, and what must be true for the work to be valuable. [Reflecting on 2021](https://indydevdan.com/blogs/reflecting-on-2021)
2. **Think and model the domain before automating it.** Reduce apparent complexity to decisions, constraints, and small steps; do not outsource the core judgment. [To Simplify: Think](https://indydevdan.com/blogs/to-simplify-think), [PLANS For Fable 5](https://www.youtube.com/watch?v=DzbqeO_diOQ)
3. **Classify the problem class.** Decide whether this is a bug, feature, research task, review, deployment, or another repeatable class; choose or create the workflow for that class. [Success Is Planned](https://agenticengineer.com/tactical-agentic-coding/course/success-is-planned), [ZTE: The Secret of Agentic Engineering](https://agenticengineer.com/tactical-agentic-coding/course/zte-secret-of-agentic-engineering)
4. **Write the specification and acceptance evidence.** Include purpose, scope, relevant artifacts, ordered phases, constraints, tests, and review criteria before implementation starts. [Planf3](https://github.com/disler/planf3), [Let Your Agents Focus](https://agenticengineer.com/tactical-agentic-coding/course/let-your-agents-focus)
5. **Design the Core Four and check all 12 leverage points.** Give the agent the minimum sufficient context, suitable model, explicit prompt, necessary tools, and external affordances such as logs, types, docs, tests, architecture, plans, templates, and ADWs. [The 12 Leverage Points](https://agenticengineer.com/tactical-agentic-coding/course/the-12-leverage-points), [Elite Context Engineering](https://agenticengineer.com/tactical-agentic-coding/course/rd-framework-context-window-mastery)
6. **Place each actor deliberately.** Use deterministic code for known sequencing and checks, specialized agents for reading and judgment, and humans for goals, novel trade-offs, safety, and escalation. [Forget Loop Engineering](https://www.youtube.com/watch?v=VQy50fuxI34), [Super Simple Software Factory](https://github.com/disler/super-simple-software-factory)
7. **Isolate phases and agent contexts.** Give each agent one purpose, its own focused context, and a safe environment; move information across seams through explicit artifacts or typed envelopes. [Let Your Agents Focus](https://agenticengineer.com/tactical-agentic-coding/course/let-your-agents-focus), [Super Simple Software Factory](https://github.com/disler/super-simple-software-factory)
8. **Close every important loop.** Run deterministic tests and independent review; route failures back to the responsible builder; bound retries and escalate unresolved uncertainty. [Close the Loops](https://agenticengineer.com/tactical-agentic-coding/course/close-the-loops), [The Verifier Agent](https://github.com/disler/the-verifier-agent)
9. **Observe the complete run.** Record prompts, context, tool calls, costs, outputs, gate results, retries, and human interventions so failures are diagnosable. [SEE CMUX SOLVE Multi-Agent Orchestration](https://www.youtube.com/watch?v=WAFUMBLOjHo), [My Super Simple Software Factory](https://www.youtube.com/watch?v=haUfb1ievTE)
10. **Improve the reusable system, not only the output.** Convert each recurring miss into a stronger template, test, tool, verifier rule, architecture affordance, or expertise update. [The Verifier Agent](https://github.com/disler/the-verifier-agent), [Agent Experts video](https://www.youtube.com/watch?v=zTcDwqopvKE)
11. **Measure and expand trust.** Track size, attempts, streak, and presence; widen task scope and autonomy only when the evidence improves. [The 12 Leverage Points](https://agenticengineer.com/tactical-agentic-coding/course/the-12-leverage-points), [ZTE: The Secret of Agentic Engineering](https://agenticengineer.com/tactical-agentic-coding/course/zte-secret-of-agentic-engineering)
12. **Package the workflow for reuse.** Version it, make models and tools swappable, and install it wherever that problem class recurs. [Top #1 Opportunity for Senior Engineers](https://www.youtube.com/watch?v=2KcITKKJikA), [My Super Simple Software Factory](https://www.youtube.com/watch?v=haUfb1ievTE)

## Important tensions and guardrails

### “Stop coding” does not mean “remove code”

His earlier rhetoric tells humans to stop spending their scarce time hand-writing implementation. His newest factory makes deterministic code the workflow control plane because code is cheap, fast, repeatable, and owned. The consistent principle is allocation: humans should not do repetitive implementation, agents should not do deterministic work that code can perform, and code should not be asked to make judgment calls. [Hello Agentic Coding](https://agenticengineer.com/tactical-agentic-coding/course/hello-agentic-coding), [My Super Simple Software Factory](https://www.youtube.com/watch?v=haUfb1ievTE), [Super Simple Software Factory](https://github.com/disler/super-simple-software-factory)

### Lower presence does not mean lower observability

He wants hands off the keyboard, not eyes closed. The less often a human intervenes, the more important traces, deterministic gates, read-only verification, safety controls, and escalation become. [SEE CMUX SOLVE Multi-Agent Orchestration](https://www.youtube.com/watch?v=WAFUMBLOjHo), [The Verifier Agent](https://github.com/disler/the-verifier-agent)

### More agents are not automatically better

More compute increases confidence only when it adds focused expertise, independent perspective, or verification. A swarm without observability and acceptance criteria is token gambling, not engineering. [GPT-5.5 VERIFIED Opus 4.7](https://www.youtube.com/watch?v=EnXKysJNz_8), [SEE CMUX SOLVE Multi-Agent Orchestration](https://www.youtube.com/watch?v=WAFUMBLOjHo)

### Zero touch is a target, not a starting permission setting

The course presents ZTE as the north star, but the concrete verifier implementation uses bounded retries and human escalation. A faithful implementation should therefore move autonomy outward from safe, low-risk, well-tested problem classes rather than begin with unrestricted production shipping. [ZTE: The Secret of Agentic Engineering](https://agenticengineer.com/tactical-agentic-coding/course/zte-secret-of-agentic-engineering), [The Verifier Agent](https://github.com/disler/the-verifier-agent)

### You cannot copy his advantage without encoding your own domain judgment

His artifacts can supply the architecture and mental models, but the differentiator is the user's problem-solving formula, product context, standards, and validation oracles. The system must be adapted by observing how _you_ solve a problem class and templating that expertise. [PLANS For Fable 5](https://www.youtube.com/watch?v=DzbqeO_diOQ), [Planf3](https://github.com/disler/planf3)

## Bottom line for the parent system

The faithful system should not be a giant universal prompt or a mandatory multi-agent swarm. It should be a small factory-building discipline:

**value → think → specify → place human/agent/code → execute in focused phases → validate independently → observe → encode the lesson → measure → expand autonomy.**

That loop is stable. The agents, models, tools, and exact phase graph are replaceable. [You Can't Keep Up](https://indydevdan.com/blogs/you-cant-keep-up), [The 12 Leverage Points](https://agenticengineer.com/tactical-agentic-coding/course/the-12-leverage-points), [Forget Loop Engineering](https://www.youtube.com/watch?v=VQy50fuxI34), [My Super Simple Software Factory](https://www.youtube.com/watch?v=haUfb1ievTE)


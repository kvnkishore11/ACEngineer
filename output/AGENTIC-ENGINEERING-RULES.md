# Agentic Engineering Rules & Instructions

> **The Complete Reference for Building Agentic Systems**
> *Everything learned from TAC 1-8 + Agentic Horizon consolidated into actionable rules*

---

## Table of Contents

1. [Foundational Mindset](#1-foundational-mindset)
2. [The 8 Core Tactics](#2-the-8-core-tactics)
3. [Project Structure Rules](#3-project-structure-rules)
4. [Prompt Engineering Rules](#4-prompt-engineering-rules)
5. [The 7 Prompt Levels](#5-the-7-prompt-levels)
6. [Information Dense Keywords (IDKs)](#6-information-dense-keywords-idks)
7. [Workflow Rules](#7-workflow-rules)
8. [Context Management Rules](#8-context-management-rules)
9. [Agent Design Rules](#9-agent-design-rules)
10. [Multi-Agent Orchestration Rules](#10-multi-agent-orchestration-rules)
11. [Testing & Validation Rules](#11-testing--validation-rules)
12. [The 28 Antipatterns to AVOID](#12-the-28-antipatterns-to-avoid)
13. [KPIs for Measuring Success](#13-kpis-for-measuring-success)
14. [Production Deployment Checklist](#14-production-deployment-checklist)
15. [Quick Reference Checklists](#15-quick-reference-checklists)

---

## 1. Foundational Mindset

### The Paradigm Shift

**RULE 1.1**: You are no longer a code writer. You are an **orchestrator of compute**.

> "In a world where code is a commodity... you move up the stack. You become a commander of compute."

**RULE 1.2**: Engineering is about building **systems of leverage**, not writing code.

**RULE 1.3**: The irreplaceable engineer **replaces themselves** by building systems that build systems.

**RULE 1.4**: Ask "**Who should handle this?**" instead of "How do I code this?"

### The Evolution Model

```
Phase 1 (AI Coding):     Context + Prompt → Generated Code
Phase 2 (Agentic Coding): Context + Prompt + Tools → Long Chains + Autonomy
```

**RULE 1.5**: Your target state is agents operating your codebase **24/7 without your presence**.

### The Role Transformation

| Before (Coder)  | After (Orchestrator)    |
|-----------------|-------------------------|
| Code Writer     | System Designer         |
| Debugger        | Architect               |
| Tester          | Strategic Oversight     |
| Documenter      | Innovation Enabler      |

---

## 2. The 8 Core Tactics

### TACTIC 1: Stop Coding

**RULE 2.1**: Let agents do the writing. Your job is to orchestrate, not implement.

### TACTIC 2: Adopt Your Agent's Perspective

**RULE 2.2**: Your agent is brilliant but blind. Give it:
- The **context** you would need
- The **model** appropriate for the task
- The **prompt** with clear instructions
- The **tools** to accomplish the work

> "Adopting your agent's perspective means: give them what you'd need to solve the problem."

### TACTIC 3: Template Your Engineering

**RULE 2.3**: The **three times rule**: Once = novel task, Twice = might repeat, Three times = pattern confirmed → **automate immediately**.

**RULE 2.4**: Encode solutions into reusable prompts. Plans are prompts scaled up.

### TACTIC 4: Stay Out of the Loop

**RULE 2.5**: Move from **in-loop** (prompting back and forth) to **out-loop** (fire and forget).

**RULE 2.6**: If you can't let agents run AFK (Away From Keyboard), delegation isn't working.

### TACTIC 5: Always Add Feedback Loops

**RULE 2.7**: Every agent needs validation to know if work succeeded:
- **Backend**: Linting → Unit tests → Compilation
- **Frontend**: TypeScript check → Build → E2E tests
- **Full Stack**: All above + Browser automation

### TACTIC 6: One Agent, One Prompt, One Purpose

**RULE 2.8**: Each lifecycle phase gets a **fresh agent**. Don't carry context between Plan/Build/Test/Review/Document.

**RULE 2.9**: This approach:
- Frees context window per task
- Forces prompts to be isolated, reusable, improvable
- Prepares for true off-device agentic coding

### TACTIC 7: Target Zero-Touch Engineering

**RULE 2.10**: The ultimate goal is **no human intervention**:
```
Trigger → Orchestrator → Pipeline → Agents → Validation → Integration → Learning
```

### TACTIC 8: Prioritize Agentics

**RULE 2.11**: Ask yourself: "Am I working on the **agentic layer** or the **application layer**?"

**RULE 2.12**: Spend **50-70% of your time** on the agentic layer (`.claude/`, `adws/`, templates, prompts).

---

## 3. Project Structure Rules

### Directory Architecture

**RULE 3.1**: Maintain **clean separation** between agentic and application layers:

```
project/
├── .claude/                 # AGENTIC LAYER
│   ├── commands/           # Reusable prompts
│   │   ├── plan.md
│   │   ├── implement.md
│   │   ├── test.md
│   │   ├── review.md
│   │   ├── document.md
│   │   ├── bug.md          # Meta-prompt for bugs
│   │   ├── feature.md      # Meta-prompt for features
│   │   └── chore.md        # Meta-prompt for chores
│   ├── agents/             # Agent configurations
│   ├── skills/             # Composable skill units
│   └── settings.json       # Project settings
│
├── app/                    # APPLICATION LAYER
│   ├── src/
│   ├── tests/
│   └── config/
│
├── specs/                  # Generated plans live here
│   └── features/
│
├── adws/                   # Agentic Developer Workflows
│   ├── plan_build.py
│   └── test_deploy.py
│
├── agents/                 # ADW execution tracking
│   └── [adw-id-YYYYMMDD-HHMMSS]/
│       ├── planner/
│       ├── implementor/
│       └── reviewer/
│
├── app_docs/               # Documentation
│
└── task.md                 # Human-readable task tracking
```

### Codebase Architecture for Agents

**RULE 3.2**: Use **clear entry points** (main.py, index.ts).

**RULE 3.3**: Use **constant files** for unchanging info.

**RULE 3.4**: Use **types/classes/structures** - tells data flow story.

**RULE 3.5**: Use **verbose naming** (information dense keywords).

**RULE 3.6**: Keep **files under 1000 lines**.

**RULE 3.7**: Include **README/CLAUDE.md** throughout codebase.

**RULE 3.8**: **Mirror test structure** to source structure.

**RULE 3.9**: Use **consistent patterns** - this compounds against complexity.

**RULE 3.10**: **Separate concerns** by directory (client/, server/, etc.).

> "If it's hard for you to navigate, assume it's hard for your agent."

---

## 4. Prompt Engineering Rules

### The Three Audiences

**RULE 4.1**: Every prompt must work for three distinct audiences:
1. **You** (future self): Quick understanding when revisiting
2. **Your Team**: Clear communication of intent and patterns
3. **Your Agents**: Unambiguous execution instructions

> Optimization for only one audience fails the entire system.

### Consistency Principles

**RULE 4.2**: **Consistency beats complexity** - same structural pattern for all prompts.

**RULE 4.3**: Don't change format every time - cognitive overload and agent confusion.

**RULE 4.4**: Use standard structure: Title → Purpose → Variables → Workflow → Report

### The Three-Step Framework (INPUT → WORKFLOW → OUTPUT)

**RULE 4.5**: Every prompt follows this pattern:

```markdown
## Variables          # INPUT - What comes in
USER_REQUEST: $1

## Workflow          # WORK - What the agent does
1. Parse request
2. Execute tasks
3. Validate results

## Report            # OUTPUT - What comes out
- Summary of changes
- Metrics and statistics
```

### Communication Style

**RULE 4.6**: Use **imperative, direct language** (not conversational).

**RULE 4.7**: No politeness required for agents.

**RULE 4.8**: **Explicit constraints** better than implicit assumptions.

**RULE 4.9**: **Examples beat vague descriptions**.

**RULE 4.10**: **Boundary definition essential** - tell agents what NOT to do.

### Token Optimization

**RULE 4.11**: Every token must **earn its place**.

**RULE 4.12**: Verbose prompts waste 3x tokens.

**RULE 4.13**: Compress without losing clarity.

**RULE 4.14**: Measure and eliminate waste.

### Essential Prompt Sections

| Section | Purpose | Required? |
|---------|---------|-----------|
| **Title** | What this does | Yes |
| **Purpose** | 1 sentence to agent | Yes |
| **Metadata** | Model, tools, timeout specs | Optional |
| **Variables** | Inputs (dynamic `@plan_path`, static `output_dir`) | Yes |
| **Workflow** | Numbered list of steps | **CRITICAL** |
| **Report/Output** | Format for results | Yes |
| **Instructions** | Auxiliary info | Optional |
| **Codebase Structure** | Context map of relevant files | Optional |
| **Examples** | Show expected output/format | Recommended |
| **Template/Format** | Exact structure agent outputs | For meta-prompts |
| **Expertise** | For self-improving prompts | Advanced |

---

## 5. The 7 Prompt Levels

### Level 1: High-Level Prompt (Static, Reusable, Ad-Hoc)

- Simple, one-shot instructions
- **Skill Tier**: D | **Usefulness**: D
- **Use**: Quick ad-hoc prompts (mostly for debugging)

```markdown
# All Tools
Look at your system prompt and list all tools
```

### Level 2: Workflow Prompt (Structured Instructions) ⭐ MOST IMPORTANT

- Adds **sequential workflow** (step-by-step list)
- Adds **report section** (output format)
- **Skill Tier**: C | **Usefulness**: A
- **Use**: 80%+ of your prompts

```markdown
# Implement Feature

## Purpose
Implement the requested feature with clean code.

## Variables
- FEATURE: $1

## Workflow
1. Understand the requirements
2. Create necessary files
3. Implement with clean code
4. Add error handling
5. Create basic tests

## Report
- Files created/modified
- Key decisions made
```

### Level 3: Control Flow Prompt

- Adds **conditionals, loops, early returns**
- If/else logic within workflow
- **Skill Tier**: B | **Usefulness**: A
- **Use**: ~10% of prompts when you need conditionals

### Level 4: Delegation Prompt

- **Spins up sub-agents** to do work
- Parallel processing, D&R pattern (Distribute → Reduce)
- **Skill Tier**: A | **Usefulness**: S
- **Use**: ~5% for complex parallel work

### Level 5: Higher-Order Prompt (HOP)

- **Takes other prompts as arguments**
- Template infrastructure stays same, content changes
- **Skill Tier**: A | **Usefulness**: B

### Level 6: Template Meta-Prompt ⭐ HIGHEST LEVERAGE

- **Prompt that generates prompts**
- Includes **plan format** section showing exact output structure
- **Skill Tier**: S | **Usefulness**: S
- **Critical**: Agents fill in blanks of specified format

```markdown
# Feature Planner (Meta-Prompt)

## Purpose
Create a detailed implementation plan for the given feature.

## Variables
- FEATURE_REQUEST: $1
- OUTPUT_DIR: specs/

## Instructions
Think hard about the implementation approach.
Consider edge cases and error handling.

## Plan Format
Generate a plan file with this EXACT structure:
---
# Feature: [Feature Name]

## Overview
[1-2 sentences describing what we're building]

## Implementation Steps
1. [Step with specific file and function]
2. [Next step...]

## Validation Commands
- `ruff check app/`
- `uv run pytest`

## Success Criteria
- [ ] Feature works as described
- [ ] All tests pass
---

## Workflow
1. Analyze the feature request
2. Think through the implementation approach
3. Generate plan following the Plan Format exactly
4. Save to {OUTPUT_DIR}/feature-[name].md

## Report
- Path to generated plan
- Summary of approach
```

### Level 7: Self-Improving Prompt

- **Updates its own expertise section** over time
- Prompts that improve themselves
- **Skill Tier**: S | **Usefulness**: A
- **Use**: Rare, most advanced pattern

---

## 6. Information Dense Keywords (IDKs)

### How They Work

**RULE 6.1**: IDKs are already in Claude's training - they **trigger specific behaviors** by modifying attention weights.

### Tier 1: Absolute Controllers (98%+ compliance)

| Keyword | Effect | Attention Weight |
|---------|--------|------------------|
| **ALWAYS / NEVER** | Non-negotiable requirements | 3.5x |
| **MUST / MUST NOT** | Critical requirements (slight flexibility) | 3.0x |
| **CRITICAL** | Overrides everything, failure points | 4.0x (highest) |

### Tier 2: Strong Modifiers (85% priority boost)

| Keyword | Effect | Attention Weight |
|---------|--------|------------------|
| **IMPORTANT** | High-priority tasks | 2.5x |
| **ESSENTIAL** | Core requirements for success | 2.8x |
| **REQUIRED** | Creates validation checkpoints | 2.3x |

### Tier 3: Behavioral Modifiers

| Keyword | Effect | Attention Weight |
|---------|--------|------------------|
| **CAREFULLY** | +40% validation steps | 1.8x |
| **THOROUGHLY** | +60% completeness | 2.0x |
| **STRICTLY** | Reduces flexibility 70%, literal interpretation | 2.2x |

### Tier 4: Scope Controllers

| Keyword | Effect | Attention Weight |
|---------|--------|------------------|
| **ONLY / EXCLUSIVELY** | 90% scope reduction | 2.5x |
| **SPECIFICALLY** | Narrows interpretation | 1.9x |
| **EXACTLY** | Zero-tolerance matching | 2.1x |

### Special Keywords

**RULE 6.2**: **"Think"** or **"Think Hard"** activates extended reasoning mode:
- Uses more compute
- Better results for complex planning/architecture
- **Use on planning steps, not simple tasks**

---

## 7. Workflow Rules

### The Software Development Lifecycle for Agentic Coding

**RULE 7.1**: Five core steps with **fresh agents** for each:

1. **Plan** - Create detailed specs (meta-prompts generate these)
2. **Build** - Implement plans with agents
3. **Test** - Validate with closed-loop feedback
4. **Review** - Confirm work matches requirements
5. **Document** - Update docs for future agents

### The 12 Leverage Points

#### In-Agent Leverage Points (Core Four)

1. **Context** - What the agent knows
2. **Model** - Which LLM to use (spend compute on complex steps)
3. **Prompt** - How you ask for work
4. **Tools** - What the agent can do

#### Through-Agent Leverage Points (External)

5. **Standard Out** - Clear logging so agents see errors/output
6. **Types** - Classes, interfaces track data flow
7. **Documentation** - AI docs folder (don't make agents web fetch every time)
8. **Tests** - Unit, integration, E2E validate work
9. **Architecture** - Clean separation reduces agent search space
10. **Plans** - Detailed specs agents execute (prompt scaled up)
11. **Templates** - Meta-prompts that generate prompts
12. **ADWs** - Agentic Developer Workflows (composable units)

### The Peter Framework (4 Elements of AFK Agents)

**RULE 7.2**: Every autonomous workflow needs:

| Element | Description | Example |
|---------|-------------|---------|
| **P**rompt Input | Where work description comes from | GitHub Issues, Notion, Slack |
| **E**nvironment | Where agent runs | Local machine, Cloud VM, Docker |
| **T**rigger | What kicks off the workflow | Webhook, Cron, Manual script |
| **E**xit/Review | How to check results | GitHub PRs, Email, Notion status |

```
GitHub Issue (input) → Webhook (trigger) → Mac Mini (environment) → PR submitted (review)
```

### The ISO Workflow Pattern

**RULE 7.3**: **Issue-Solution-Outcome** for modular, composable workflow units:

- **Issue**: Clear problem definition
- **Solution**: Specific implementation approach
- **Outcome**: Measurable results

**Benefits**:
- Each unit maintains isolation (no context pollution)
- Can be combined into complex pipelines
- Enables composable development

### Closed-Loop Testing Pattern

**RULE 7.4**: Every agent output must be validated:

```markdown
## Validation Commands
- `ruff check app/`           # Linting
- `uv run pytest`             # Unit tests
- `npm run build`             # Compilation
- `npx playwright test`       # E2E tests
```

**RULE 7.5**: If validation fails, agent must fix and rerun until all pass.

---

## 8. Context Management Rules

### The R&D Framework (Reduce & Delegate)

**RULE 8.1**: Most systems carry **70% waste context** that can be eliminated.

### REDUCE: Eliminate Junk Context

**RULE 8.2**: Minimize CLAUDE.md files (~350 tokens max, not ~23K).

**RULE 8.3**: Control output tokens (concise response styles).

**RULE 8.4**: Load MCP servers **on demand**, not at startup.

**RULE 8.5**: **Reset and Prime** instead of compact - rebuild with only essential state.

**RULE 8.6**: Measure constantly to identify waste.

### DELEGATE: Distribute Cognition

**RULE 8.7**: Use **sub-agent delegation** (partially forked context).

**RULE 8.8**: Use **primary agent delegation** (completely independent).

**RULE 8.9**: Use **expert agent systems** (self-improving specialists).

**RULE 8.10**: Use **Architect/Editor pattern** (planner → builder separation).

**RULE 8.11**: Use **background agents** (out-of-loop execution).

### Context Priming

**RULE 8.12**: Use `.claude/commands/prime.md` instead of memory files:
- Faster than memory
- More flexible
- Scannable for specific sections

**RULE 8.13**: Prime specific sections of codebase for focused tasks.

### Reset-Prime Strategy

**RULE 8.14**: Rather than compacting growing context:
1. Save everything to history
2. Reset context window completely
3. Load only essential current state
4. Prime agent with minimal context

---

## 9. Agent Design Rules

### The "One Agent, One Purpose" Philosophy

**RULE 9.1**: Out-of-box agents are built for everyone's codebase, not yours.

**RULE 9.2**: Specialization solves:
- Context window constraints ✅
- Codebase complexity ✅
- (Human abilities remain the bottleneck)

**RULE 9.3**: Each specialized agent gets **full token allocation**.

**RULE 9.4**: Every prompt should be **versioned, measurable, and improvable**.

### Core Agent Design Principles

#### Principle 1: Complete System Prompt Override

**RULE 9.5**: System prompt affects EVERY user prompt - override default to specialize.

**RULE 9.6**: One clear responsibility, no mission creep.

**RULE 9.7**: Explicit boundaries: "What You MUST Do" and "What You MUST NOT Do".

#### Principle 2: Tool Minimization

**RULE 9.8**:
- Generic agents: 15+ tools
- Specialized agents: **Only tools needed for purpose**

**RULE 9.9**: Custom tools for domain-specific needs.

**RULE 9.10**: Agents can choose without analysis paralysis.

#### Principle 3: Domain Knowledge Injection

**RULE 9.11**: Embed your patterns and conventions.

**RULE 9.12**: Encode rules unique to your codebase.

**RULE 9.13**: Specify common edge cases.

**RULE 9.14**: Teach agent your shortcuts.

### Agent Interface Types

| Interface | Use Case |
|-----------|----------|
| **Script** | One-shot execution in automated pipelines |
| **REPL** | Maintains conversation state for interactive work |
| **Web** | Backend for UI-driven workflows |
| **Stream** | Processes data streams |

### Model Selection Strategy

**RULE 9.15**: Match model to task complexity:

| Step | Model |
|------|-------|
| Planning (complex) | Most powerful (Opus) |
| Implementation | Powerful (Sonnet) |
| Testing/Simple | Can use faster model |

**RULE 9.16**: Use latest available models - never stay behind.

---

## 10. Multi-Agent Orchestration Rules

### When You Need Orchestration

**RULE 10.1**: You've hit the "Orchestration Wall" when:
- **Context Explosion**: Single agents drowning in information
- **Coordination Chaos**: Agents working in isolation
- **Observability Blindness**: Can't see what agents are doing
- **Management Overhead**: Manual creation and monitoring

### The Orchestrator Pattern

**RULE 10.2**: The Orchestrator interprets intent and manages workers:

```python
class OrchestratorAgent:
    """One Agent to Rule Them All"""
    tools = [
        "create_agent",
        "command_agent",
        "check_agent_status",
        "list_agents",
        "delete_agent",
        "read_agent_logs",
        "interrupt_agent",
        "report_cost"
    ]
```

### Key Orchestration Principles

**RULE 10.3**: **Separation of Concerns** - Orchestrator does planning, agents do execution.

**RULE 10.4**: **Context Protection** - Minimal context for orchestrator, isolated for agents.

**RULE 10.5**: **Coordination Layer** - Central management and status tracking.

**RULE 10.6**: **Observation Layer** - Event logs, database, WebSocket streams.

### Orchestration Architecture

```
Input → Orchestrator → Decompose → Agent Fleet → Coordinate → Synthesize → Output
         (interpret)    (plan)      (execute)     (manage)     (aggregate)
```

### The Evolution Journey

```
Base Agents (2x) → Better Agents (5x) → More Agents (10x) → Custom Agents (20x) → Orchestrated (100x+)
```

---

## 11. Testing & Validation Rules

### Closed Loop Testing Anatomy

**RULE 11.1**: Every agent needs feedback to validate work.

| Codebase Type | Validation Chain |
|---------------|------------------|
| Backend (Python/Node) | Linting → Unit tests → Compilation |
| Frontend (React/Vue) | TypeScript check → Build → Playwright E2E |
| Full Stack | All above + actual browser testing |
| Data Science | Custom evaluation + regression tests |

### Validation Commands in Plans

**RULE 11.2**: Template meta-prompts MUST include validation section:

```markdown
## Validation Commands
- `ruff check app/`
- `uv run pytest`
- Run e2e test: `npx playwright test`
```

### Testing Strategy

**RULE 11.3**: Make tests **pass/fail deterministically** so agents know if work is done.

**RULE 11.4**: If validation fails:
1. Agent analyzes the failure
2. Agent fixes the issue
3. Agent reruns ALL validations
4. Only succeed when ALL pass

### Request-Validate-Resolve Pattern

**RULE 11.5**: Every agent workflow follows:

```
REQUEST:  What needs to be done
VALIDATE: Run commands to check it worked
RESOLVE:  Fix issues found by validation
```

---

## 12. The 28 Antipatterns to AVOID

### Architectural Antipatterns

| # | Antipattern | Problem | Solution |
|---|-------------|---------|----------|
| 1 | **Monolithic Agent** | One giant agent doing everything | Use specialized agents |
| 2 | **Tangled Layer** | Mixing agentic and application code | Maintain `.claude/` separation |
| 3 | **Infinite Loop** | Agents calling agents without termination | Add exit conditions and depth limits |
| 4 | **Stateless Maze** | No state management between calls | Implement persistence |

### Prompting Antipatterns

| # | Antipattern | Problem | Solution |
|---|-------------|---------|----------|
| 5 | **Vague Instruction** | Unclear, ambiguous prompts | Be specific with constraints |
| 6 | **Context Dump** | Providing entire codebase | Curate carefully (R&D pattern) |
| 7 | **Rigid Template** | Over-constraining output | Allow flexibility |
| 8 | **Prompt Spaghetti** | Massive, unstructured prompts | Use clear organization |

### Workflow Antipatterns

| # | Antipattern | Problem | Solution |
|---|-------------|---------|----------|
| 9 | **Sequential Bottleneck** | Forcing sequential when parallel possible | Parallelize independent tasks |
| 10 | **Missing Rollback** | No recovery mechanism | Implement rollbacks |
| 11 | **Premature Optimization** | Over-engineering before understanding | Start simple, evolve |
| 12 | **Manual Bridge** | Human intervention in automated flow | Full automation with quality gates |

### Context Antipatterns

| # | Antipattern | Problem | Solution |
|---|-------------|---------|----------|
| 13 | **Stale Context** | Using outdated information | Refresh constantly |
| 14 | **Context Black Hole** | Loading context but not using it | Load only what's needed |
| 15 | **Split Brain** | Agents with conflicting context | Coordinate context, version it |

### Integration Antipatterns

| # | Antipattern | Problem | Solution |
|---|-------------|---------|----------|
| 16 | **Brittle Integration** | Hard-coded dependencies | Use abstractions |
| 17 | **Synchronous Trap** | Blocking on slow calls | Use async patterns |
| 18 | **Credential Leak** | Exposing secrets | Use environment variables |

### Testing Antipatterns

| # | Antipattern | Problem | Solution |
|---|-------------|---------|----------|
| 19 | **Untested Agent** | No validation of outputs | Implement testing |
| 20 | **Flaky Test** | Tests that randomly fail | Make deterministic |
| 21 | **Test Theater** | Tests that don't test anything | Meaningful assertions |

### Production Antipatterns

| # | Antipattern | Problem | Solution |
|---|-------------|---------|----------|
| 22 | **Silent Failure** | Failures without notification | Implement alerting |
| 23 | **Runaway Agent** | Unlimited resource consumption | Set limits and circuit breakers |
| 24 | **Unobservable System** | No visibility into behavior | Implement observability |
| 25 | **Configuration Chaos** | Hard-coded configuration | Centralize config |

### Meta-Antipatterns

| # | Antipattern | Problem | Solution |
|---|-------------|---------|----------|
| 26 | **Pattern Zealotry** | Using patterns regardless of fit | Use judiciously |
| 27 | **NIH Syndrome** | Rebuilding everything | Use existing tools |
| 28 | **Premature Abstraction** | Creating abstractions too early | Wait for patterns (Rule of Three) |

### Deadly Combinations

```
Death Spiral:     Monolithic Agent + Context Dump + No Testing + Silent Failures
Complexity Trap:  Premature Optimization + Pattern Zealotry + NIH Syndrome
Performance Kill: Sequential Bottleneck + Synchronous Trap + Context Dump
Debug Nightmare:  Unobservable System + Silent Failures + Split Brain
```

---

## 13. KPIs for Measuring Success

### The Four Metrics

| KPI | Direction | Meaning |
|-----|-----------|---------|
| **Size** | ↑ Increase | Larger chunks of work per prompt (5min → 30min → 1hr+) |
| **Attempts** | ↓ Decrease | Fewer re-prompts needed (target: 1-shot success) |
| **Streak** | ↑ Increase | Consecutive successful runs without issues |
| **Presence** | ↓ Decrease | Time you spend babysitting agent (goal: zero) |

### The Golden Formula

```
Presence DOWN + Streak UP + Size UP + Attempts DOWN = Agentic Engineering Win
```

### Progression Benchmarks

| Stage | Size | Attempts | Streak | Presence |
|-------|------|----------|--------|----------|
| Beginner | 5 min tasks | 3-5 | 1-2 | High |
| Intermediate | 30 min tasks | 2 | 3-5 | Medium |
| Advanced | 1+ hr tasks | 1 | 10+ | Low |
| Master | Full features | 1 | Unlimited | Zero (AFK) |

---

## 14. Production Deployment Checklist

### Pre-Deployment

- [ ] Context limits tested
- [ ] Error handling implemented
- [ ] Fallbacks configured
- [ ] Monitoring setup
- [ ] Rate limits configured
- [ ] All tests passing
- [ ] Security review completed
- [ ] Performance tested
- [ ] Cost analysis done
- [ ] Rollback plan ready
- [ ] Caching implemented

### Security

- [ ] Input validation (length, injection attempts)
- [ ] Output sanitization (remove PII, escape special chars)
- [ ] Environment variables for secrets
- [ ] Encryption at rest
- [ ] Audit logging
- [ ] Access controls

### Post-Deployment

- [ ] Monitor metrics 24 hours
- [ ] Check error rates
- [ ] Verify costs align with estimates
- [ ] Gather feedback
- [ ] Document lessons learned
- [ ] Plan improvements

### Cost Optimization

**DO**:
- Implement caching for expensive operations
- Batch processing when possible
- Model selection by task complexity
- Monitor token usage
- Compress prompts
- Parallelize independent tasks

**DON'T**:
- Make redundant API calls
- Skip token optimization
- Ignore free tiers
- Process one-at-a-time when batching possible
- Allow wasteful context management

---

## 15. Quick Reference Checklists

### Starting a New Project

1. [ ] Create `.claude/commands/` directory
2. [ ] Add `prime.md` - ramped-up agent primer
3. [ ] Add `implement.md` - takes plan as input
4. [ ] Create `specs/` directory for generated plans
5. [ ] Add `/bug`, `/feature`, `/chore` meta-prompts
6. [ ] Create `adws/` directory with basic workflow
7. [ ] Set up GitHub integration for issue input
8. [ ] Test one workflow end-to-end

### Writing a Template Meta-Prompt

1. [ ] Title + Purpose (direct language)
2. [ ] Variables defined (dynamic `@var`, static `var = value`)
3. [ ] Instructions (auxiliary info)
4. [ ] **Plan Format section** (exact structure for output)
5. [ ] Workflow (numbered steps)
6. [ ] Validation commands included
7. [ ] Report format defined
8. [ ] Tested with one example

### Converting In-Loop to Out-Loop

1. [ ] Get prompt working manually
2. [ ] Create Python/Bash wrapper script
3. [ ] Set up trigger (webhook, cron)
4. [ ] Set up environment (dedicated machine)
5. [ ] Set up review (PRs, email, dashboard)
6. [ ] Disable verbose output
7. [ ] Check results asynchronously

### Creating Closed-Loop Tests

1. [ ] Identify manual testing steps
2. [ ] Convert to shell commands (pass/fail output)
3. [ ] Add to plan template in Validation Commands section
4. [ ] Configure agent to run all, report results
5. [ ] If fail → fix → rerun validation
6. [ ] Only succeed when ALL pass
7. [ ] Add regression test for future

### Debugging Failed Workflows

1. [ ] Check logs in `agents/` directory
2. [ ] Find exact ADW ID that failed
3. [ ] Find `.jsonl` output with agent thought process
4. [ ] Identify which step failed (planning? building? testing?)
5. [ ] Fix the template meta-prompt for that step
6. [ ] Re-run workflow
7. [ ] **Don't iterate with agent** - fix templates permanently

---

## Red Flags to Watch For

### In Code
- Functions over 100 lines
- Deeply nested conditions
- No error handling
- Hard-coded values
- No tests
- Circular dependencies

### In Prompts
- Over 1000 tokens
- No structure
- Vague instructions
- No examples
- Conflicting requirements

### In Architecture
- Single point of failure
- No state management
- No rollback capability
- Synchronous everything
- No monitoring

### In Process
- No documentation
- No code reviews
- Direct production deployment
- No testing strategy
- Manual steps in automation

---

## Key Quotes to Remember

> "In a world where code is a commodity... you move up the stack. You become a commander of compute."

> "Engineering was never about writing code. It's about building systems of leverage."

> "Your agent is brilliant but blind. Give it your perspective."

> "Template your engineering. Encode your solutions into reusable units."

> "Plans are prompts scaled up. Great planning is great prompting."

> "Presence KPI to zero. You walk away from keyboard. Your product ships itself."

> "Ask yourself: am I working on the agentic layer or the application layer?"

> "If it's hard for you to navigate, assume it's hard for your agent."

> "The three times rule: Once = novel, Twice = might repeat, Three times = pattern → automate."

> "Consistency beats complexity."

---

## The Ultimate Guiding Questions

1. **Am I working on the agentic layer or the application layer?**
   - Majority time should be on agentic layer

2. **Who should handle this?**
   - Think delegation, not implementation

3. **Can this run AFK (Away From Keyboard)?**
   - If not, delegation isn't working

4. **Is this the third time I'm doing this?**
   - If yes, template it immediately

5. **Does my agent have what I would need?**
   - Context, model, prompt, tools

---

**Version 1.0 | Compiled from TAC 1-8 + Agentic Horizon**

*This document is your single source of truth for agentic engineering. Bookmark it. Print it. Live by it.*

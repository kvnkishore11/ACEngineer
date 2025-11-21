---
name: agentic-prompt-engineering
description: Expert framework for designing high-quality prompts for autonomous agents. Use when creating slash commands, agent instructions, or multi-agent workflows. Based on comprehensive analysis of Tactical Agentic Coding course materials.
---

# Agentic Prompt Engineering Skill

## Core Philosophy

> "The prompt is THE fundamental unit of engineering in the age of agents. Every prompt you write has the ability to generate tens or hundreds of hours of productive work through tool calls."

This skill helps you craft prompts for **three distinct audiences**:
1. **You** - Quick understanding when revisiting
2. **Your Team** - Clear communication of intent
3. **Your Agents** - Unambiguous execution instructions

## When to Use This Skill

Claude automatically applies this skill when you:
- Create new `.claude/commands/*.md` slash commands
- Design system prompts for autonomous agents
- Build multi-agent workflows or orchestration
- Debug agent misbehavior through prompt refinement
- Optimize existing prompts for better performance
- Create meta-prompts (prompts that generate prompts)

## The 7 Levels of Agentic Prompt Formats

### Level 1: High Level Prompt (Tier: D)
**Purpose**: Static, reusable, ad-hoc prompts for simple tasks

**Structure**:
```markdown
# Title

High-level description of what to do

## Purpose (optional)
One-line clarification of intent
```

**When to Use**: One-off tasks, simple queries, quick utilities

---

### Level 2: Workflow Prompt ⭐ (Tier: S - MOST COMMON)
**Purpose**: Sequential workflow with INPUT → WORKFLOW → OUTPUT structure

**Structure**:
```markdown
---
description: Brief description
---

# Title

## Purpose
Execute the `Workflow` and `Report` sections to accomplish X

## Variables
DYNAMIC_VAR: $1
STATIC_VAR: /fixed/path

## Workflow
1. Step one with clear action
2. Step two with tool usage
3. Step three with validation

## Report
- Format for output
- Required information
```

**When to Use**: 80% of prompts - multi-step processes, reusable workflows

**CRITICAL**: This is your workhorse format. Use it by default.

---

### Level 3: Control Flow Prompt (Tier: A)
**Purpose**: Adds conditions and loops to workflows

**Structure**:
```markdown
## Workflow
1. Check condition
   - IF condition: take action A
   - ELSE: take action B
2. LOOP for each item:
   - Process item
   - Validate result
3. Continue workflow
```

**When to Use**: Dynamic workflows, batch processing, conditional execution

---

### Level 4: Delegate Prompt (Tier: S)
**Purpose**: Orchestrates multiple agents for parallel work

**Structure**:
```markdown
## Variables
AGENT_COUNT: 5
AGENT_MODEL: sonnet
AGENT_TOOLS: Read, Write, WebSearch

## Workflow
1. Parse requirements
2. Design agent prompts
   - Create self-contained prompts
   - Define clear output expectations
3. Launch {{AGENT_COUNT}} parallel agents
4. Collect and summarize results
```

**When to Use**: Parallel processing, diverse perspectives, large-scale operations

---

### Level 5: Higher Order Prompt (Tier: A)
**Purpose**: Accepts other prompts as input for dynamic execution

**Structure**:
```markdown
## Variables
PATH_TO_PROMPT: $1

## Workflow
1. Read prompt at {{PATH_TO_PROMPT}}
2. Parse prompt structure
3. Execute embedded workflow
4. Report according to prompt specification
```

**When to Use**: Executing generated plans, dynamic workflows

---

### Level 6: Template Metaprompt (Tier: S)
**Purpose**: Prompts that generate prompts - force multiplier

**Structure**:
```markdown
## Purpose
Generate a complete agentic prompt for {{TASK_TYPE}}

## Template Structure to Generate
- Title and description
- Variables section
- Workflow steps (numbered, specific)
- Report format (structured output)
- Error handling

## Validation
The generated prompt must:
- Follow Level 2 Workflow format
- Be self-contained
- Include success criteria
```

**When to Use**: Building prompt libraries, automating prompt creation, systematizing workflows

**IMPORTANT**: Template metaprompts are MASSIVE leverage - they create exponential returns

---

### Level 7: Self-Improving Prompt (Tier: Future)
**Purpose**: Prompts that monitor, evaluate, and improve themselves

**Structure**:
```markdown
## Workflow
1. Execute primary task
2. Collect performance metrics
3. Evaluate against success criteria
4. IF performance < threshold:
   - Analyze failure patterns
   - Propose prompt modifications
   - Test modified version
5. Update prompt template with learnings
```

**When to Use**: Production systems, continuous improvement, advanced automation

---

## The Three-Step Pattern (Universal)

EVERY agentic prompt follows: **INPUT → WORKFLOW → OUTPUT**

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

**ALWAYS use this pattern for consistency.**

---

## Information Dense Keywords (IDKs)

Certain keywords carry special weight with agents and dramatically alter behavior.

### Tier 1: Absolute Controllers (Maximum Impact)

**ALWAYS / NEVER**
- Impact: 98%+ compliance rate
- Attention Weight: ~3.5x baseline
- Example: `ALWAYS validate user input before processing`

**MUST / MUST NOT**
- Impact: 95%+ compliance rate
- Attention Weight: ~3.0x baseline
- Example: `You MUST check database connectivity before queries`

**CRITICAL**
- Impact: Overrides other instructions
- Attention Weight: ~4.0x baseline
- Example: `CRITICAL: Verify backup exists before deletion`

### Tier 2: Strong Modifiers

**IMPORTANT**
- Impact: 85% priority boost
- Attention Weight: ~2.5x baseline
- Example: `IMPORTANT: Generate comprehensive test coverage`

**ESSENTIAL**
- Impact: Marks for required completion
- Attention Weight: ~2.8x baseline
- Example: `ESSENTIAL: All API endpoints must return JSON`

**REQUIRED**
- Impact: Creates validation checkpoints
- Attention Weight: ~2.3x baseline
- Example: `REQUIRED: Authentication token in all requests`

### Tier 3: Behavioral Modifiers

**CAREFULLY**
- Impact: +40% validation steps
- Example: `CAREFULLY parse the configuration file`

**THOROUGHLY**
- Impact: +60% completeness
- Example: `THOROUGHLY test all edge cases`

**STRICTLY**
- Impact: Reduces flexibility by 70%
- Example: `STRICTLY follow the coding style guide`

### Tier 4: Scope Controllers

**ONLY / EXCLUSIVELY**
- Impact: 90% reduction in scope
- Example: `ONLY modify files in the src/ directory`

**SPECIFICALLY**
- Impact: Narrows interpretation
- Example: `SPECIFICALLY test the login endpoint`

**EXACTLY**
- Impact: Zero-tolerance matching
- Example: `Return EXACTLY this format: {"status": "ok"}`

---

## Core Principles

### Principle 1: Consistency Beats Complexity
Every prompt should follow the same structural pattern. Consistency is the greatest weapon against confusion for both you and your agent.

### Principle 2: Direct Communication
Use imperative, direct language:
- **Bad**: "Could you please analyze the codebase?"
- **Good**: "Execute the workflow to analyze the codebase and identify all critical issues."

### Principle 3: Composable Sections
Build prompts from swappable, optional sections. Use only what you need.

### Principle 4: The Stakeholder Trifecta
Write for three audiences simultaneously:
- **You**: Quick understanding 6 months from now
- **Your Team**: Clear communication of intent and requirements
- **Your Agents**: Unambiguous execution instructions

---

## Prompt Engineering Workflow

### Phase 1: Intent Definition
```markdown
**Agent Purpose**: [What does this agent do?]
**Input Format**: [What does it receive?]
**Output Format**: [What should it produce?]
**Success Criteria**: [How do we measure success?]
**Failure Modes**: [What can go wrong?]
```

### Phase 2: Choose Format Level
- Simple task → Level 1
- Standard workflow → Level 2 (80% of cases)
- Conditional logic → Level 3
- Multi-agent → Level 4
- Dynamic execution → Level 5
- Prompt generation → Level 6
- Self-improvement → Level 7

### Phase 3: Apply Pattern
Use templates from `/templates/` directory

### Phase 4: Add IDKs
Strategically place Information Dense Keywords for critical sections

### Phase 5: Validate
Use validation checklist from `/templates/validation-checklist.md`

---

## Common Patterns Quick Reference

### REQUEST → VALIDATE → RESOLVE (Closed-Loop)
```markdown
## Workflow
1. REQUEST: Perform the task
2. VALIDATE: Check results meet criteria
   - IF validation passes: Continue
   - ELSE: RESOLVE issues and retry
3. Report final status
```

### Pipeline Pattern (Sequential Agents)
```markdown
Agent 1 → Agent 2 → Agent 3 → Agent 4
(Plan)   (Build)   (Test)    (Review)
```

### Fork-Join Pattern (Parallel Processing)
```markdown
        ┌→ Agent A →┐
Main → ─┼→ Agent B →┼→ Aggregator → Output
        └→ Agent C →┘
```

### Fresh Agent Handoff
```markdown
# Agent 1: Do task A, save state to state.json
# Agent 2: Load state.json, do task B (clean context)
```

---

## Advanced Techniques

### Meta-Prompt Architecture
Create prompts that generate domain-specific prompts:

```markdown
# Generate Test Prompt

Create a testing prompt for {{FEATURE_NAME}}

## Generated Prompt Must Include
1. Test setup instructions
2. Test cases (happy path + edge cases)
3. Validation criteria
4. Cleanup procedures

## Output
Write the complete prompt to .claude/commands/test-{{FEATURE_NAME}}.md
```

### Context Optimization
Integrate with Elite Context Engineering:
- Use R&D framework (Reduce & Delegate)
- REDUCE: Remove unnecessary context
- DELEGATE: Offload to specialized agents

### Specialized Agent Integration
One Agent, One Prompt, One Purpose:
- Create focused prompts for single responsibilities
- Avoid multi-purpose agents
- Use fresh agents for clean context

---

## Validation Checklist (Quick)

Before finalizing any prompt:
- [ ] Follows one of the 7 levels consistently
- [ ] Has clear INPUT → WORKFLOW → OUTPUT structure
- [ ] Uses appropriate IDKs for critical sections
- [ ] Written for all three audiences (You, Team, Agents)
- [ ] Includes error handling
- [ ] Specifies exact output format
- [ ] Has examples or test cases
- [ ] Is self-contained (no assumed context)

---

## Anti-Patterns to Avoid

❌ **Vague Instructions**: "Do a good job"
✅ **Specific Criteria**: "Achieve 90%+ test coverage with edge cases"

❌ **Assumed Context**: "Follow standard practices"
✅ **Explicit Specification**: "Use Python PEP 8 style guide with max line length 88"

❌ **Ambiguous Success**: "Make it better"
✅ **Measurable Outcomes**: "Reduce execution time by 50% while maintaining accuracy"

❌ **Human-style Prompting**: "Could you please..."
✅ **Agent-style Commands**: "Execute the workflow to..."

---

## Integration with TAC System

This skill integrates with:
- **TAC-1**: Programmable prompts foundation
- **TAC-3**: Meta-prompts and templates
- **TAC-4**: ADW (AI Developer Workflow) automation
- **TAC-5**: Closed-loop testing patterns
- **TAC-6**: One Agent, One Prompt, One Purpose
- **TAC-7**: Composable agentic primitives

---

## Examples Directory

See `/examples/` for:
- `plan-pattern.md` - Feature planning prompt
- `build-pattern.md` - Implementation prompt
- `test-pattern.md` - Testing automation prompt
- `review-pattern.md` - Code review prompt
- `document-pattern.md` - Documentation generation
- `meta-prompt-pattern.md` - Prompt generation prompt
- `orchestrator-pattern.md` - Multi-agent coordination

---

## Key Takeaways

1. **Level 2 (Workflow) is your workhorse** - use it for 80% of prompts
2. **IDKs are force multipliers** - strategic placement of CRITICAL, ALWAYS, IMPORTANT
3. **Consistency beats complexity** - same structure across all prompts
4. **INPUT → WORKFLOW → OUTPUT** - universal pattern
5. **Template metaprompts = exponential leverage** - prompts that generate prompts
6. **Write for three audiences** - You, Team, Agents

---

## Quick Start Guide

Creating a new slash command? Follow this:

1. **Identify the level**: Most likely Level 2 (Workflow)
2. **Use template**: Copy from `/templates/workflow-prompt-template.md`
3. **Fill in sections**:
   - Title and description
   - Variables (inputs)
   - Workflow steps (numbered, specific actions)
   - Report format (structured output)
4. **Add IDKs**: Place CRITICAL, IMPORTANT where needed
5. **Validate**: Quick checklist above
6. **Test**: Run with sample input
7. **Iterate**: Refine based on results

**Remember**: The prompt is THE fundamental unit. Invest in making it excellent.

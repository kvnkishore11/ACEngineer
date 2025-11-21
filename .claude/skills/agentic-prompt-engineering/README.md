# Agentic Prompt Engineering Skill

> "The prompt is THE fundamental unit of engineering in the age of agents."

Complete framework for designing high-quality prompts for autonomous agents, based on comprehensive analysis of the Tactical Agentic Coding course.

---

## Quick Start

### Creating a New Slash Command

1. **Choose your level** (most likely Level 2 - Workflow)
2. **Copy the template**: `templates/workflow-prompt-template.md`
3. **Fill in the sections**:
   - Title and description
   - Variables (what inputs does it need?)
   - Workflow (what steps does it take?)
   - Report (what output does it produce?)
4. **Add IDKs**: Place CRITICAL, IMPORTANT where needed
5. **Test**: Run it with real input
6. **Iterate**: Refine based on results

### When Claude Uses This Skill

This skill activates automatically when you:
- Type "create a slash command for..."
- Say "help me design a prompt for..."
- Ask "how do I build an agent that..."
- Request "optimize this prompt..."

---

## Core Concepts

### The 7 Levels (Know Your Format)

1. **Level 1: High Level** → Simple, ad-hoc tasks
2. **Level 2: Workflow** ⭐ → **80% of your prompts - the workhorse**
3. **Level 3: Control Flow** → Conditions and loops
4. **Level 4: Delegate** → Multi-agent orchestration
5. **Level 5: Higher Order** → Dynamic prompt execution
6. **Level 6: Template Metaprompt** → Prompts that generate prompts (massive leverage)
7. **Level 7: Self-Improving** → Future: self-optimizing prompts

### The Three-Step Pattern (Universal)

**Every prompt follows**: INPUT → WORKFLOW → OUTPUT

```markdown
## Variables      # INPUT
## Workflow       # WORK
## Report         # OUTPUT
```

### The Stakeholder Trifecta

Write for three audiences:
1. **You** (6 months from now)
2. **Your Team** (clear communication)
3. **Your Agents** (unambiguous execution)

### Information Dense Keywords (IDKs)

Strategic word placement that changes agent behavior:

| Tier | Keywords | Impact | When to Use |
|------|----------|--------|-------------|
| 1 | CRITICAL, ALWAYS, NEVER, MUST | 4x attention | Safety, security, data loss prevention |
| 2 | IMPORTANT, ESSENTIAL, REQUIRED | 2.5x attention | Quality requirements, key features |
| 3 | CAREFULLY, THOROUGHLY, STRICTLY | 2x attention | Increased validation, completeness |
| 4 | ONLY, EXCLUSIVELY, EXACTLY, SPECIFICALLY | 2x attention | Scope control, precision matching |

---

## Directory Structure

```
agentic-prompt-engineering/
├── SKILL.md                              # Main skill definition
├── README.md                             # This file
├── templates/
│   ├── workflow-prompt-template.md       # Level 2 template (most common)
│   ├── metaprompt-template.md           # Level 6 template
│   └── validation-checklist.md          # Quality checklist
├── examples/
│   ├── plan-pattern.md                  # Implementation planning
│   ├── build-pattern.md                 # Code execution
│   ├── test-pattern.md                  # Testing automation
│   ├── review-pattern.md                # Code review
│   └── meta-prompt-example.md           # Prompt generation
└── reference/
    ├── idk-catalog.md                   # Complete IDK reference
    ├── common-mistakes.md               # Anti-patterns
    └── integration-guide.md             # Works with TAC system
```

---

## Usage Guide

### Creating Your First Prompt

**Task**: Create a slash command that generates API documentation

**Step 1**: Choose Level 2 (Workflow) - standard multi-step task

**Step 2**: Copy template
```bash
cp .claude/skills/agentic-prompt-engineering/templates/workflow-prompt-template.md \
   .claude/commands/document-api.md
```

**Step 3**: Fill in sections

```markdown
---
description: Generate API documentation from code
---

# Document API

Generate comprehensive API documentation by analyzing code

## Purpose
Execute the `Workflow` and `Report` sections to create API documentation

## Variables
API_DIR: $1  # Directory containing API code
OUTPUT_FILE: ./docs/api.md
DOC_FORMAT: markdown

## Workflow
1. VALIDATE input:
   - REQUIRED: {{API_DIR}} exists
   - IF not: Exit with error
2. Scan for API endpoints:
   ```bash
   grep -r "app\\.get\\|app\\.post\\|app\\.put\\|app\\.delete" {{API_DIR}}
   ```
3. IMPORTANT: For each endpoint found:
   - Extract route path
   - Identify request parameters
   - Determine response format
   - Find related code comments
4. Generate documentation with:
   - Endpoint description
   - HTTP method and path
   - Request parameters (type, required/optional)
   - Response format with example
   - Error codes
5. Write to {{OUTPUT_FILE}}
6. CRITICAL: Validate generated documentation:
   - All endpoints documented
   - Examples are valid JSON
   - No placeholder text

## Report
```yaml
status: success|failure
endpoints_documented: [count]
output_file: [path]
missing_docs: [list if any]
```
```

**Step 4**: Test
```bash
/document-api ./src/api
```

**Step 5**: Iterate based on results

---

## Common Patterns

### Plan → Build → Test → Review (SDLC)

```markdown
# Complete workflow
/plan "feature description"
/build ./specs/plan-*.md
/test
/review
```

### Request → Validate → Resolve (Closed-Loop)

```markdown
## Workflow
1. REQUEST: Perform task
2. VALIDATE: Check results
   - IF valid: Continue
   - ELSE: RESOLVE issues and retry
3. Report status
```

### Fork-Join (Parallel Agents)

```markdown
## Workflow
1. Split work into tasks
2. FOR each task:
   - Spawn fresh agent
   - Execute independently
3. Aggregate results
4. Validate combined output
```

---

## Integration with TAC System

This skill is the foundation for:

| TAC Module | How It Uses Prompts |
|------------|---------------------|
| TAC-1 | Programmable prompts as code |
| TAC-3 | Meta-prompts and templates |
| TAC-4 | ADW (AI Developer Workflows) - chains prompts |
| TAC-5 | Closed-loop validation patterns |
| TAC-6 | One Agent, One Prompt, One Purpose |
| TAC-7 | Composable agentic primitives |
| TAC-8 | Orchestration and the Agentic Layer |

**Plus Agentic Horizon modules**:
- Elite Context Engineering → R&D framework for prompt optimization
- Building Specialized Agents → One prompt per agent
- Multi-Agent Orchestration → Prompts that coordinate agents

---

## Best Practices

### ✅ DO

- **Use Level 2 (Workflow) for most prompts**
- **Be explicit and specific** in every instruction
- **Include validation steps** after critical operations
- **Specify exact output formats** with examples
- **Add error handling** for common failures
- **Use IDKs strategically** (CRITICAL, IMPORTANT, ALWAYS)
- **Test with real inputs** before deploying
- **Write for three audiences** (You, Team, Agents)

### ❌ DON'T

- **Don't be vague**: "Do a good job" → Specify criteria
- **Don't assume context**: "Follow best practices" → List specific practices
- **Don't use human-style language**: "Please try to..." → "Execute the workflow to..."
- **Don't skip validation**: Always validate critical operations
- **Don't mix concerns**: One prompt, one purpose
- **Don't forget examples**: Show expected usage
- **Don't use placeholders**: TBD, TODO in production prompts

---

## Examples Library

### Example 1: Simple Task (Level 1)
```markdown
# List Tools

Show all available tools from your system prompt

## Purpose
Quick reference for available capabilities
```

### Example 2: Standard Workflow (Level 2)
See `examples/plan-pattern.md` for complete example

### Example 3: Conditional Logic (Level 3)
```markdown
## Workflow
1. Check file size:
   - IF size < 1MB: Process normally
   - ELSE IF size < 10MB: Process with streaming
   - ELSE: Split into chunks
```

### Example 4: Meta-prompt (Level 6)
```markdown
# Generate Test Prompt

Create a testing prompt for {{FEATURE_NAME}}

## Output
Write complete prompt to .claude/commands/test-{{FEATURE_NAME}}.md
following Level 2 Workflow format
```

---

## Quick Reference

### IDK Cheat Sheet

```markdown
CRITICAL: [data loss, security, irreversible actions]
ALWAYS: [non-negotiable requirements]
NEVER: [absolute prohibitions]
IMPORTANT: [quality requirements]
ESSENTIAL: [must-have features]
CAREFULLY: [needs extra validation]
THOROUGHLY: [needs completeness]
ONLY: [scope restriction]
EXACTLY: [precision matching]
```

### Validation Checklist

Before deploying any prompt:
- [ ] Follows one of the 7 levels
- [ ] Has INPUT → WORKFLOW → OUTPUT structure
- [ ] Uses IDKs for critical sections
- [ ] Includes error handling
- [ ] Specifies exact output format
- [ ] Has at least one example
- [ ] No assumed context

### Common Workflow Patterns

```markdown
# Read → Process → Write
1. Read input
2. Process/transform
3. Write output
4. Validate

# Validate → Execute → Verify
1. Check preconditions
2. Execute main task
3. Verify results

# Try → Catch → Retry
1. Attempt operation
2. IF fails: Handle error
3. Retry with different approach
```

---

## Advanced Topics

### Meta-Prompts (Level 6)

Prompts that generate prompts = **exponential leverage**

**Use cases**:
- Building prompt libraries for domains
- Automating prompt creation for repetitive tasks
- Systematizing prompt patterns

**Example**: Generate CRUD prompts for any data model

### Context Optimization

Integrate with Elite Context Engineering:
- **REDUCE**: Remove unnecessary context from prompts
- **DELEGATE**: Split work across specialized agents

Aim for **70% context reduction** while improving performance.

### Multi-Agent Orchestration

Design prompts that coordinate multiple agents:
- Orchestrator prompt (coordinates, never executes)
- Specialist prompts (focused, single-purpose)
- Aggregator prompt (combines results)

---

## Troubleshooting

### Problem: Agent doesn't follow instructions

**Diagnosis**: Vague or ambiguous language
**Solution**: Be more explicit, add specific validation steps, use IDKs

### Problem: Agent outputs wrong format

**Diagnosis**: Output format not clearly specified
**Solution**: Show exact format with code block example, validate in workflow

### Problem: Agent skips important steps

**Diagnosis**: Steps buried in paragraphs or not numbered
**Solution**: Use numbered lists, place IMPORTANT/CRITICAL IDKs

### Problem: Agent makes assumptions

**Diagnosis**: Context not explicitly provided
**Solution**: Remove all assumed knowledge, make everything explicit

### Problem: Inconsistent results

**Diagnosis**: Non-deterministic logic or missing constraints
**Solution**: Add specific decision rules, use IF/THEN explicitly

---

## Learning Path

### Beginner (First Week)
1. Read SKILL.md completely
2. Study examples/plan-pattern.md
3. Create 3 simple Level 1 prompts
4. Create 2 Level 2 (Workflow) prompts
5. Test all prompts with real inputs

### Intermediate (Second Week)
1. Master Level 2 (Workflow) format
2. Learn IDK strategic placement
3. Create prompts with error handling
4. Build a meta-prompt (Level 6)
5. Integrate prompts into workflow chain

### Advanced (Third Week)
1. Design multi-agent orchestration
2. Create self-improving prompts (Level 7)
3. Build domain-specific prompt libraries
4. Optimize prompts with Elite Context Engineering
5. Systematize with template metaprompts

---

## Success Metrics

You've mastered agentic prompt engineering when:
- [ ] 80%+ of your prompts use Level 2 (Workflow) format
- [ ] You use IDKs strategically, not randomly
- [ ] Your prompts have >90% success rate on first run
- [ ] You can create a new prompt in <15 minutes
- [ ] Your team can understand and use your prompts
- [ ] You've built meta-prompts that generate prompts
- [ ] You think in terms of composable prompt primitives

---

## Resources

### In This Skill
- `SKILL.md` - Complete framework and reference
- `templates/` - Ready-to-use templates
- `examples/` - Working examples with explanations
- `reference/` - Deep dives into concepts

### Related TAC Modules
- TAC-1: Programmable Prompts foundation
- TAC-3: Meta-prompts and templates
- TAC-4: AI Developer Workflows (ADW)
- TAC-6: One Agent, One Prompt, One Purpose
- TAC-7: Composable Agentic Primitives

### Related Agentic Horizon
- Elite Context Engineering (R&D framework)
- Building Specialized Agents (one prompt per agent)
- Multi-Agent Orchestration (coordinating prompts)

---

## Contributing

As you build prompts, capture learnings:
1. Add new patterns to `examples/`
2. Document mistakes in `reference/common-mistakes.md`
3. Update templates based on what works
4. Share meta-prompts that generate useful prompts

---

## Quick Help

**"I need a simple command"** → Use Level 1, see examples/simple-task.md
**"I need a standard workflow"** → Use Level 2, copy templates/workflow-prompt-template.md
**"I need conditional logic"** → Use Level 3, add IF/ELSE to workflow
**"I need multiple agents"** → Use Level 4, see examples/orchestrator-pattern.md
**"I need to generate prompts"** → Use Level 6, see examples/meta-prompt-example.md

**"My agent isn't working"** → Check validation-checklist.md, add IDKs, be more explicit
**"How do I...?"** → Ask Claude - this skill will activate automatically

---

**Remember**: The prompt is THE fundamental unit. Invest in making it excellent.

Every hour spent perfecting a prompt returns 10x in reliable agent execution.

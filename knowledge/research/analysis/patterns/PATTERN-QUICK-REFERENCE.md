# Agentic Engineering Pattern Quick Reference

## Essential Patterns Cheat Sheet

### 🏗️ Architectural Patterns

| Pattern | When to Use | Key Structure | TAC Level |
|---------|------------|---------------|-----------|
| **Agentic Layer** | Starting any project | `.claude/` separated from `app/` | TAC-1+ |
| **Command Component** | Reusable agent tasks | Markdown commands in `.claude/commands/` | TAC-2+ |
| **Agent Pipeline** | Multi-step workflows | Input → Agent₁ → Agent₂ → Output | TAC-4+ |
| **Worktree Isolation** | Parallel development | Separate Git worktrees per task | TAC-7+ |
| **Multi-Architecture** | Different use cases | MVP/Minimal/Standard/Scaled/Advanced | TAC-8 |

### 💬 Prompting Patterns

| Pattern | When to Use | Key Feature | Level |
|---------|------------|-------------|-------|
| **Structured Template** | Consistent outputs | Sections: Instructions/Variables/Process/Report | TAC-3+ |
| **Variable Injection** | Dynamic prompts | `$VARIABLE_NAME` substitution | TAC-3+ |
| **Delegation Prompt** | Multi-agent tasks | Spawn specialized sub-agents | Horizon L4 |
| **Metaprompt** | Generate prompts | Prompts creating prompts | Horizon L6 |
| **Self-Improving** | Repetitive tasks | Accumulates expertise over time | Horizon L7 |

### 🔄 Workflow Patterns

| Pattern | When to Use | Pipeline | TAC Level |
|---------|------------|----------|-----------|
| **Plan-Build-Test-Ship** | Feature development | Plan → Build → Test → Review → Doc → Ship | TAC-7 |
| **Issue-to-PR** | GitHub workflow | Issue → Classify → Plan → Build → PR | TAC-4+ |
| **Fail-Fast-Fix-Fast** | Error recovery | Try → Fail → Analyze → Fix → Retry | TAC-5+ |
| **Progressive Enhancement** | New features | MVP → Basic → Advanced → Optimized | All |
| **Zero-Touch Engineering** | Full automation | Trigger → Plan → Execute → Validate → Deploy | TAC-7 |

### 📚 Context Patterns

| Pattern | When to Use | Strategy | Level |
|---------|------------|----------|-------|
| **Context Bundling** | Reusable context | Package related files together | Horizon |
| **Reduce & Delegate** | Large codebases | Minimize context per agent | Horizon |
| **Conditional Docs** | Just-in-time info | Load docs based on current task | TAC-6+ |
| **Reset-Prime** | Context pollution | Clear and rebuild context | Horizon |
| **Context Measurement** | Optimization | Track token usage and relevance | Horizon |

### 🔌 Integration Patterns

| Pattern | When to Use | Integration Type | TAC Level |
|---------|------------|------------------|-----------|
| **GitHub Integration** | Dev workflow | Issues, PRs, branches | TAC-4+ |
| **Tool Abstraction** | Multiple services | Common interface for tools | Horizon |
| **Webhook Trigger** | Real-time response | React to external events | TAC-4+ |
| **Model Selection** | Task optimization | Choose model by requirements | TAC-4+ |
| **State Persistence** | Continuity | Database-backed state | Horizon |

### ✅ Testing Patterns

| Pattern | When to Use | Test Type | TAC Level |
|---------|------------|-----------|-----------|
| **E2E Browser Testing** | Web apps | Playwright automation | TAC-5+ |
| **Test Failure Resolution** | Failed tests | Auto-fix test failures | TAC-5+ |
| **Visual Testing** | UI consistency | Screenshot comparison | TAC-6+ |
| **Test Generation** | Coverage | Generate from specs | TAC-5+ |
| **Continuous Validation** | Early detection | Test at each step | TAC-7 |

### 🚀 Production Patterns

| Pattern | When to Use | Purpose | TAC Level |
|---------|------------|---------|-----------|
| **ADW ID Tracking** | Traceability | Unique ID for workflow tracking | TAC-4+ |
| **Multi-Agent Orchestration** | Complex workflows | Coordinate agent teams | Horizon |
| **Observability** | Monitoring | Track metrics and performance | TAC-7+ |
| **Quality Gates** | Standards | Enforce quality at each stage | TAC-7 |
| **Self-Healing** | High availability | Detect and fix own issues | Horizon |

---

## Quick Decision Trees

### Starting a New Project
```
Small/Personal? → Agentic Layer + Commands
Team/Medium? → + Agent Pipeline + GitHub
Enterprise? → + Orchestration + Observability
```

### Choosing a Workflow
```
Simple task? → Single command
Multi-step? → Plan-Build pattern
Need testing? → Plan-Build-Test-Ship
Full auto? → Zero-Touch Engineering
```

### Optimizing Performance
```
Token limits? → Reduce & Delegate
Repeated context? → Context Bundling
Slow execution? → Parallel agents
High costs? → Model selection
```

### Handling Failures
```
Test failures? → Test Failure Resolution
System errors? → Self-Healing
Quality issues? → Quality Gates
Debug needs? → Observability
```

---

## Pattern Combinations

### 🎯 The Starter Pack
```
Agentic Layer + Command Component + Structured Templates
```
**Use for**: Getting started with agentic development

### 🔧 The Developer Suite
```
GitHub Integration + Issue-to-PR + Plan-Build-Test-Ship
```
**Use for**: Automating development workflow

### 🛡️ The Quality Shield
```
E2E Testing + Test Resolution + Visual Testing + Quality Gates
```
**Use for**: Ensuring code quality

### 🏭 The Production System
```
Multi-Agent Orchestration + State Persistence + Observability + Self-Healing
```
**Use for**: Production agent systems

### ⚡ The Performance Pack
```
Context Measurement + Context Bundling + Reduce & Delegate + Model Selection
```
**Use for**: Optimizing agent performance

---

## Command Structure Templates

### Basic Command
```markdown
# Command Name
## Instructions
What to do
## Process
1. Step one
2. Step two
## Report
Output format
```

### Variable Command
```markdown
# Task: $TASK_NAME
## Variables
- $INPUT_VAR
- $CONFIG_VAR
## Process
Use $INPUT_VAR to...
```

### Delegation Command
```yaml
delegate:
  agent: specialized-agent
  model: claude-3-opus
  tools: [Tool1, Tool2]
```

---

## Workflow Templates

### Simple Workflow
```python
def workflow():
    plan = create_plan()
    result = implement(plan)
    return result
```

### Pipeline Workflow
```python
async def pipeline():
    tasks = [
        classify_task(),
        generate_plan(),
        implement_solution(),
        create_tests(),
        document_code()
    ]
    return await execute_pipeline(tasks)
```

### Error-Handling Workflow
```python
def resilient_workflow():
    try:
        result = execute_task()
    except Error as e:
        fix = generate_fix(e)
        result = retry_with_fix(fix)
    return result
```

---

## Common Configurations

### Project Structure
```
project/
├── .claude/
│   ├── commands/      # Reusable prompts
│   ├── agents/        # Agent configs
│   └── settings.json  # Project settings
├── app/               # Application code
├── specs/             # Specifications
├── adws/              # Workflows
└── tests/             # Test files
```

### ADW Tracking Structure
```
agents/
└── [adw-id]/
    ├── planner/
    │   ├── prompt.md
    │   └── output.json
    ├── implementor/
    │   ├── prompt.md
    │   └── output.json
    └── reviewer/
        ├── prompt.md
        └── output.json
```

### Settings Configuration
```json
{
  "model": "claude-3-opus",
  "temperature": 0.7,
  "max_tokens": 4000,
  "tools": ["WebSearch", "Calculator"],
  "context_strategy": "reduce_delegate"
}
```

---

## Evolution Path Quick Guide

### Beginner → Intermediate
1. Learn structured templates
2. Add GitHub integration
3. Implement agent pipelines
4. Add automated testing

### Intermediate → Advanced
1. Implement quality gates
2. Add multi-agent coordination
3. Optimize context management
4. Build observability

### Advanced → Master
1. Create self-improving prompts
2. Build meta-agents
3. Implement orchestration
4. Design new patterns

---

## Red Flags to Avoid

### ❌ DON'T
- Mix agent and app code
- Dump entire codebase as context
- Create synchronous bottlenecks
- Skip error handling
- Ignore testing
- Hard-code configurations

### ✅ DO
- Separate concerns cleanly
- Curate context carefully
- Parallelize when possible
- Handle failures gracefully
- Test everything
- Use configuration files

---

## Performance Tips

### Token Optimization
- Measure context usage
- Bundle related files
- Use Reduce & Delegate
- Clear stale context

### Speed Optimization
- Parallelize independent tasks
- Use appropriate models
- Cache reusable results
- Implement circuit breakers

### Cost Optimization
- Use Sonnet for simple tasks
- Use Opus for complex tasks
- Monitor token usage
- Set resource limits

---

## Debugging Checklist

### When Things Go Wrong
- [ ] Check logs and outputs
- [ ] Verify context is current
- [ ] Confirm agent has needed tools
- [ ] Test with simpler input
- [ ] Check for circular dependencies
- [ ] Verify API keys and permissions
- [ ] Review rate limits
- [ ] Check state persistence

---

## Quick Commands

### Initialize Project
```bash
mkdir -p .claude/commands
echo "# Prime\nLoad project context" > .claude/commands/prime.md
```

### Run Command
```bash
claude run .claude/commands/implement.md
```

### Execute Workflow
```bash
uv run adws/adw_plan_build.py --issue 123
```

### Check Status
```bash
cat agents/adw-*/status.json
```

---

## Pattern Maturity Levels

### Level 1: Basic (TAC 1-3)
- Commands, Templates, Variables

### Level 2: Automated (TAC 4-6)
- Pipelines, GitHub, Testing

### Level 3: Production (TAC 7-8)
- Zero-Touch, Quality, Architecture

### Level 4: Mastery (Horizon)
- Self-Improving, Orchestration, Meta-Agents

---

## Emergency Patterns

### System Down
→ Self-Healing + Rollback + Alerting

### Performance Crisis
→ Context Reduction + Parallel Execution + Caching

### Quality Emergency
→ Quality Gates + Test Resolution + Review

### Debugging Nightmare
→ Observability + ADW Tracking + Logging

---

## The Golden Rules

1. **Start Simple**: Don't over-engineer
2. **Test Early**: Validate as you go
3. **Monitor Always**: Observe everything
4. **Document Well**: Future you will thank you
5. **Evolve Gradually**: Patterns emerge from use

---

## Final Quick Reference

### Most Used Patterns
1. Agentic Layer (Foundation)
2. Command Component (Reusability)
3. Agent Pipeline (Workflow)
4. GitHub Integration (Development)
5. Plan-Build-Test-Ship (Quality)

### Most Powerful Patterns
1. Zero-Touch Engineering (Automation)
2. Self-Improving Prompts (Evolution)
3. Multi-Agent Orchestration (Scale)
4. Reduce & Delegate (Performance)
5. Self-Healing (Resilience)

### Quick Win Patterns
1. Structured Templates (Immediate improvement)
2. Variable Injection (Dynamic prompts)
3. Context Bundling (Performance boost)
4. Test Failure Resolution (Time saver)
5. ADW Tracking (Debugging aid)
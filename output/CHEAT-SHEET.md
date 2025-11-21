# 🎯 Agentic Engineering Cheat Sheet

> **Everything You Need on One Page**

## ⚡ Essential Commands

### Claude CLI Basics
```bash
# Initialize agent
claude agent init --type specialist --name my-agent

# Run with context
claude run --context window.yaml --prompt "task"

# Test agent
claude test --agent my-agent --scenario production

# Deploy
claude deploy --env production --scale auto
```

### Quick Patterns
```bash
# BFC (Brief-Focused-Clear)
claude prompt --pattern bfc --task "analyze logs"

# ISO (Input-Structure-Output)
claude prompt --pattern iso --format json

# ADW (Analyze-Design-Write)
claude generate --pattern adw --complexity high
```

## 🏗️ Top 10 Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| **BFC** | Clear prompting | `Brief: Analyze / Focused: errors / Clear: list` |
| **ISO** | Structured I/O | `Input: CSV / Structure: parse / Output: JSON` |
| **Chain-of-Thought** | Complex reasoning | `Let's think step-by-step...` |
| **Few-Shot** | Examples | `Example 1:... Example 2:... Now:...` |
| **Tool Augmentation** | External tools | `@search query @calculate formula` |
| **Context Window** | Memory mgmt | `window: sliding, size: 4000` |
| **Reflexion Loop** | Self-improvement | `try → evaluate → refine → retry` |
| **Mixture-of-Experts** | Specialization | `router → expert1, expert2 → aggregate` |
| **Constitutional AI** | Safety | `principles: [...] → critique → revise` |
| **RLHF** | Alignment | `generate → rank → train → improve` |

## 🔄 Core Workflows

### BFC Workflow (Brief-Focused-Clear)
```yaml
1. Brief: State objective (1 line)
2. Focused: Add constraints (2-3 points)
3. Clear: Specify output format
```

### ISO Workflow (Input-Structure-Output)
```yaml
1. Input: Define data source
2. Structure: Process/transform
3. Output: Format result
```

### ADW Workflow (Analyze-Design-Write)
```yaml
1. Analyze: Understand requirements
2. Design: Plan architecture
3. Write: Implement solution
```

## 🤖 Agent Templates

### Specialist Agent
```yaml
type: specialist
capabilities:
  - domain_expertise
  - tool_use
  - memory_management
config:
  model: claude-3
  temperature: 0.3
  max_tokens: 4000
```

### Orchestrator Agent
```yaml
type: orchestrator
agents:
  - researcher
  - analyzer
  - writer
routing: dynamic
consensus: weighted_vote
```

### Tool Agent
```yaml
type: tool_augmented
tools:
  - web_search
  - calculator
  - code_executor
fallback: reasoning_only
```

## 🐛 Top 10 Issues & Fixes

| Issue | Quick Fix |
|-------|-----------|
| **Context overflow** | Use sliding window or compression |
| **Hallucination** | Add grounding with tools/retrieval |
| **Inconsistent output** | Lower temperature, add examples |
| **Slow response** | Optimize prompt, use caching |
| **Token limit** | Implement chunking strategy |
| **Poor reasoning** | Add CoT prompting |
| **Format errors** | Use structured output (JSON mode) |
| **Memory loss** | Implement state management |
| **Tool failures** | Add fallback mechanisms |
| **Scale issues** | Use load balancing, queue systems |

## ⌨️ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Run agent | `Ctrl+R` |
| Test prompt | `Ctrl+T` |
| View context | `Ctrl+W` |
| Debug mode | `Ctrl+D` |
| Stop execution | `Ctrl+C` |
| Clear context | `Ctrl+K` |
| Save state | `Ctrl+S` |
| Load template | `Ctrl+L` |

## 🧠 Critical Concepts

### Context Management
- **Window Types**: Fixed, Sliding, Expanding
- **Compression**: Summarization, Extraction, Pruning
- **State**: Persistent, Session, Ephemeral

### Agent Types
- **Reactive**: Simple stimulus-response
- **Deliberative**: Planning and reasoning
- **Hybrid**: Combines reactive + deliberative
- **Learning**: Adapts from experience

### Orchestration Patterns
- **Sequential**: A → B → C
- **Parallel**: A + B + C → Merge
- **Hierarchical**: Manager → Workers
- **Consensus**: Vote/Debate/Merge

### Performance Optimization
- **Caching**: Response, embedding, tool results
- **Batching**: Group similar requests
- **Streaming**: Progressive output
- **Pruning**: Remove redundant context

## 📊 Quick Decision Matrix

### Choose Your Pattern
| Need | Use |
|------|-----|
| Clear instructions | BFC |
| Structured data | ISO |
| Complex logic | Chain-of-Thought |
| Examples | Few-Shot |
| External data | Tool Augmentation |

### Choose Your Agent
| Task | Agent Type |
|------|------------|
| Single domain | Specialist |
| Multiple tasks | Orchestrator |
| Tool integration | Tool-Augmented |
| Learning/Adapting | RLHF Agent |

### Choose Your Architecture
| Scale | Architecture |
|-------|--------------|
| Small | Single agent |
| Medium | Pipeline |
| Large | Multi-agent |
| Enterprise | Microservices |

## 🚀 Production Checklist

### Pre-Deployment
- [ ] Context limits tested
- [ ] Error handling implemented
- [ ] Fallbacks configured
- [ ] Monitoring setup
- [ ] Rate limits configured

### Security
- [ ] Input validation
- [ ] Output sanitization
- [ ] API keys secured
- [ ] Audit logging enabled
- [ ] Access controls configured

### Performance
- [ ] Response time < 2s
- [ ] Token usage optimized
- [ ] Caching implemented
- [ ] Load testing passed
- [ ] Scaling strategy defined

## 📈 TAC Module Progression

```
TAC-1: Prompting → TAC-2: Reasoning → TAC-3: Tools
       ↓                    ↓                ↓
TAC-4: Architecture → TAC-5: Dialogue → TAC-6: Enterprise
       ↓                    ↓                ↓
TAC-7: Optimization ←──── TAC-8: Advanced Systems
```

## 🎓 Horizon Courses at a Glance

| Course | Core Skill | Output |
|--------|------------|--------|
| **Prompt Engineering** | Template mastery | Optimized prompts |
| **Specialized Agents** | Agent building | Production agents |
| **Context Engineering** | Memory management | Efficient systems |
| **Multi-Agent** | Orchestration | Scalable platforms |

## 🔗 Quick Links

**Documentation**
- [Master Index](./README.md)
- [Pattern Library](./analysis/patterns/PATTERN-LIBRARY.md)
- [FAQ](./FAQ.md)

**Learning**
- [Quick Start](./QUICK-START.md)
- [Learning Path](./LEARNING-PATH.md)
- [Best Practices](./BEST-PRACTICES.md)

**Reference**
- [Glossary](./GLOSSARY.md)
- [Comparison Matrix](./COMPARISON-MATRIX.md)
- [Roadmap](./ROADMAP.md)

---

## 💡 Remember

1. **Start simple** - BFC before complex patterns
2. **Test early** - Validate before scaling
3. **Monitor always** - Track performance/costs
4. **Document patterns** - Reuse what works
5. **Iterate constantly** - Improve incrementally

---

*Keep this handy! Print it, bookmark it, share it.*

**Version 1.0 | November 2024**
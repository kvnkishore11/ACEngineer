# TAC-2 Ultimate Guide: The Complete Deep Dive

## Executive Summary

TAC-2 transforms engineers from AI-assisted coders into Agentic Engineers who build self-operating systems. Through 12 concrete leverage points and 4 measurable KPIs, it provides a systematic framework for maximizing agent autonomy while minimizing human presence.

**Core Thesis:** "Stop coding, start building systems that operate on your behalf."

## Part 1: The Philosophical Foundation

### The Paradigm Shift

The author opens with a revolutionary declaration:

> "In order to become an irreplaceable engineer, we have to stop coding and learn to build systems that can operate on our behalf."

This isn't about using AI to code faster - it's about transcending coding entirely.

### The "Brilliant but Blind" Mental Model

The central insight that drives all of TAC-2:

> "Your agent is brilliant, but blind. With every new session, it starts as a blank instance. Agents are ephemeral, no context, no memories, and no awareness outside of what you give it."

This understanding shapes every pattern, practice, and principle in TAC-2.

### The Central Tactic: Adopt Your Agent's Perspective

> "Your agent needs the information, the tools, and the resources you would use to solve the problem at hand."

This means thinking not "What do I need to do?" but "What does my agent need to succeed?"

## Part 2: The 12 Leverage Points Framework

### In-Agent Leverage Points (The Core Four)

#### 1. Context
- What the agent knows about the current situation
- Provided through conversation history and file content

#### 2. Model
- The underlying LLM (Claude, GPT-4, etc.)
- Capabilities and limitations of the chosen model

#### 3. Prompt
- The instructions and questions you provide
- Now organized as reusable commands in `.claude/commands/`

#### 4. Tools
- The actions available to the agent
- Critical insight: "Did you know that the bash tool here has a timeout?"

**Implementation Example:**
```markdown
# .claude/commands/tools.md
List the tools available to you
```

### Through-Agent Leverage Points

#### 5. Standard Out
**Video Teaching:** "Your agent can only see what you let it see."

**Bad Pattern:**
```python
except Exception as e:
    return {"error": str(e)}  # Agent can't see this!
```

**Good Pattern:**
```python
except Exception as e:
    print(f"Error: {e}")  # Agent visibility!
    return {"error": str(e)}
```

#### 6. Types
**Concept:** "Types are IDKs - Information Dense Keywords"

**Purpose:** Track information flow through your codebase

**Example from TAC-2:**
```python
# data_models.py
class DatabaseSchemaResponse:
    # This type can be traced throughout the application
```

#### 7. Documentation
**Structure:**
- Internal: `.claude/`, `README.md`, inline comments
- External: `ai_docs/` for LLM provider documentation

**The Prime Pattern:**
```markdown
# .claude/commands/prime.md
## Run
git ls-files
## Read
README.md
```

#### 8. Tests
**Philosophy:** "Your agent will make mistakes... The only question is, does it have the right leverage it needs to correct the mistakes?"

**Integration:**
```bash
uv run pytest  # Output feeds directly to agent
```

#### 9. Architecture
**Key Principle:** "This one simple decision makes it easy for our agent to cut all of its work in half."

**TAC-2 Structure:**
```
app/
├── client/  # Clear separation
├── server/  # Reduces search space
tests/       # Mirrors source structure
```

#### 10. Plans
**Scale:** "Plans are how you communicate massive amounts of work to your agent."

**Location:** `specs/init_nlq_to_sql_to_table.md` (700+ lines)

**Revelation:** "We are going to be planning with our agent."

#### 11. Templates (Slash Commands)
**Innovation:** "We're using a powerful pattern of running prompts inside of prompts."

**Example Commands:**
- `/prime` - Understand codebase
- `/install` - Setup dependencies
- `/tools` - List capabilities

#### 12. ADWs (AI Developer Workflows)
**Definition:** "Combine one or more agentic prompts... wrap it in arbitrary code... kick it off autonomously with a trigger."

**Vision:** "Your code base literally runs itself."

## Part 3: The KPI System

### Four Metrics That Matter

#### 1. Size ↑
**Goal:** Increase work handed to agents
**Progression:** "5 minutes → 10 → 20 → 30 → an hour → three hours"

#### 2. Attempts ↓
**Goal:** Achieve one-shot success
**Warning:** "Attempts cost your most important engineering resource: your time"

#### 3. Streak ↑
**Goal:** Chain successful one-shot prompts
**Target:** "Streaks of three, five, ten"

#### 4. Presence ↓
**Goal:** Zero human intervention
**Challenge:** "We love control and visibility, but it's time for us to let that go"

### The Success Formula

> "An engineer that can run five one-shot agent prompts that ship entire features... drastically outperforms an engineer that runs five prompts but had to fix three issues per prompt."

## Part 4: The TAC-2 Application

### The Natural Language to SQL System

**Purpose:** "A great playground to showcase the leverage points"

**Components:**
```
Frontend (Vite + TypeScript):
- Drag-and-drop file upload
- Natural language query interface
- Real-time results display

Backend (FastAPI + Python):
- LLM integration (OpenAI/Anthropic)
- SQL generation and execution
- Security and validation

Database (SQLite):
- In-memory operations
- SQL injection protection
- Dynamic table creation
```

### Demonstration Flow

1. **Prime the Agent:**
   ```bash
   claude /prime
   ```

2. **Install Dependencies:**
   ```bash
   claude /install
   ```

3. **Start with Monitoring:**
   ```bash
   scripts/start.sh 300s  # 5-minute timeout
   ```

4. **Fix Issues Agentically:**
   - Agent sees errors in stdout
   - Agent traces types through codebase
   - Agent runs tests for validation

## Part 5: Key Patterns and Practices

### The Prime Pattern
**Always start with understanding:**
1. List files (`git ls-files`)
2. Read documentation
3. Summarize understanding

### The Command Composition Pattern
```markdown
# install.md calls prime.md
## Read and Execute
.claude/commands/prime.md
## Run
Install FE and BE dependencies
```

### The Three-Time Rule
> "Three time makes a pattern. Three time should trigger your engineering brain. Automate."

### The Agent Navigation Problem
**Challenge:** "Every time you boot up a new agent, it has to explore the codebase."

**Solutions:**
- Consistent architecture
- Clear entry points
- Information-dense naming
- Mirror test structure

### Token Efficiency Principles
- Avoid generic names ("data_request" ❌)
- Use verbose but meaningful names ✓
- Keep files under 1000 lines
- One responsibility per file

## Part 6: Practical Implementation

### Setting Up TAC-2

1. **Clone the Repository:**
   ```bash
   git clone [tac-2-repo]
   cd tac-2
   ```

2. **Prime Your Agent:**
   ```bash
   claude /prime
   ```

3. **Install Dependencies:**
   ```bash
   claude /install
   ```

4. **Configure Environment:**
   ```bash
   # app/server/.env
   OPENAI_API_KEY=your_key
   ANTHROPIC_API_KEY=your_key
   ```

5. **Start the Application:**
   ```bash
   scripts/start.sh
   ```

### Creating Custom Commands

1. **Create Command File:**
   ```bash
   .claude/commands/my-command.md
   ```

2. **Define Command Structure:**
   ```markdown
   # My Command
   > Description of what this does

   ## Run
   [bash commands]

   ## Read
   [files to read]
   ```

3. **Use the Command:**
   ```bash
   claude /my-command
   ```

### Implementing Leverage Points

#### For Better Standard Out:
```python
# Always print before returning
print(f"Success: {operation} completed")
print(f"Error: {error_details}")
```

#### For Better Architecture:
```
service/
├── core/       # Business logic
├── api/        # Endpoints
├── tests/      # Mirror structure
└── types/      # Shared types
```

#### For Better Types:
```python
class SpecificWorkflowRequest:  # Not "DataRequest"
    """Traces through: api → core → database"""
```

## Part 7: Advanced Concepts

### Programmable vs Interactive Mode

**Phase 1 (Interactive):**
```bash
claude
# Back and forth conversation
```

**Phase 2 (Programmable):**
```bash
claude -p "/command"
# One-shot execution
```

### The Autonomy Spectrum

Level 1: Manual coding
Level 2: AI-assisted coding (TAC-1)
Level 3: Command-driven development (TAC-2)
Level 4: Workflow automation (Future)
Level 11: "Autonomy knob all the way to 11"

### The Engineering Evolution

**What Changes:**
- No more manual coding
- No more debugging
- No more iteration

**What Remains:**
- Architecture decisions
- Planning and direction
- User value focus

> "What does stay is architecture. What does stay is direction. It's planning. It's thinking. It's engineering."

## Part 8: Common Pitfalls and Solutions

### Pitfall 1: Low Leverage Output
**Problem:** No stdout, agent is blind
**Solution:** Print everything important

### Pitfall 2: Generic Naming
**Problem:** Types like "DataModel" provide no context
**Solution:** Use information-dense keywords

### Pitfall 3: Inconsistent Structure
**Problem:** Agent wastes time navigating
**Solution:** Consistent patterns everywhere

### Pitfall 4: Missing Tests
**Problem:** No validation loop
**Solution:** Tests that output to stdout

### Pitfall 5: High Presence
**Problem:** Constant human intervention
**Solution:** Better plans, more leverage points

## Part 9: The Vision and Future

### The End Goal

> "We're here to dial up the autonomy knob all the way to 11. We're here to become Agentic Engineers."

### The Market Context

> "All the low hanging fruit is getting chewed up. It's time to do the smart work, not the hard work to get asymmetric return on your engineering."

### The Career Implication

> "How well you do this determines your progression as an engineer in phase two of the generative AI age."

### The Ultimate Achievement

> "When I say your codebase will literally run itself, I mean that."

## Part 10: Quick Reference

### Essential Commands

```bash
# Understand codebase
claude /prime

# Install dependencies
claude /install

# List available tools
claude /tools

# Start with monitoring
claude -p "scripts/start.sh 300s"
```

### KPI Tracking

| Metric | Direction | Current | Target |
|--------|-----------|---------|--------|
| Size | ↑ | 5 min | 3 hours |
| Attempts | ↓ | 3-5 | 1 |
| Streak | ↑ | 1-2 | 10+ |
| Presence | ↓ | High | Zero |

### Leverage Point Checklist

- [ ] Standard out visible to agent
- [ ] Types tracking information flow
- [ ] Documentation in `.claude/`
- [ ] Tests with stdout feedback
- [ ] Consistent architecture
- [ ] Clear entry points
- [ ] Commands for repeated tasks
- [ ] Plans for complex work
- [ ] ADWs for automation (future)

## Part 11: Key Takeaways

### Technical Takeaways

1. **Commands are Functions:** Reusable, composable prompt templates
2. **Prime First:** Always understand before acting
3. **Stdout is Communication:** Agent visibility is crucial
4. **Types are Navigation:** Information flow tracking
5. **Tests are Validation:** Self-correcting systems

### Philosophical Takeaways

1. **Stop Coding:** Build systems instead
2. **Think Like Agent:** Adopt their perspective
3. **Measure Progress:** KPIs drive improvement
4. **Embrace Autonomy:** Let go of control
5. **Focus on Value:** Users, not code

### Strategic Takeaways

1. **Phase 2 is Here:** Agentic > AI-assisted
2. **Irreplaceable Skills:** System design > coding
3. **Leverage Compounds:** Stack the 12 points
4. **One-Shot Goals:** Iteration is failure
5. **Scale Ambition:** Hours, not minutes

## Conclusion

TAC-2 isn't just an evolution of TAC-1 - it's a revolution in how we think about engineering. It provides:

1. **A Framework:** The 12 leverage points
2. **A Measurement System:** The 4 KPIs
3. **A Practical Application:** The NLQ-to-SQL system
4. **A Philosophy:** Agentic Engineering
5. **A Vision:** Self-operating codebases

The author's closing wisdom:

> "Master the primitives and you'll master the compositions. Big things are just two or more small things put together."

TAC-2 teaches us to build the small things (commands, leverage points) that compose into big things (autonomous systems). It's not about writing better prompts - it's about building better systems that eliminate the need for prompts entirely.

The future isn't AI-assisted coding. The future is codebases that run themselves. TAC-2 shows us how to build that future today.

> "English is the new programming language and we're just digging into that fact and we're taking it where it's going before it gets there."

Welcome to Agentic Engineering. Welcome to TAC-2.
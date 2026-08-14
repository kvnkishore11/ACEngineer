# TAC-2 Concept Mapping: Video to Code

## Core Concepts Map

### 1. Slash Commands (`/install`, `/prime`, `/tools`)

**Video Teaching:**
> "Out of the gate, we're using a custom slash command. This is a reusable prompt."

**Code Location:** `.claude/commands/`

**Implementation Details:**
```markdown
# .claude/commands/prime.md
> Execute the following sections to understand the codebase then summarize your understanding.
## Run
git ls-files
## Read
README.md
```

**Author's Explanation:**
> "We're using a powerful pattern of running prompts inside of prompts. This is no different than passing a function inside of a function."

### 2. The Prime Pattern

**Video Teaching:**
> "The prime custom slash command is super, super important. This in combination with the claude.md lets your agent quickly get ramped up with information about your codebase."

**Code Implementation:**
- Location: `.claude/commands/prime.md`
- Purpose: Codebase comprehension
- Method: List files → Read documentation → Summarize

**Author's Mental Model:**
> "Your agent still has to look through files, figure out where things are, and navigate your codebase."

### 3. Standard Out as Leverage Point

**Video Teaching:**
> "Your agent can only see what you let it see. Standard out is the response from any command you run."

**Code Example from Video:**
The author demonstrates this with the CSV upload error:

**Bad Code (Before):**
```python
# Server doesn't print errors - agent is blind
except Exception as e:
    return {"error": str(e)}  # No print!
```

**Good Code (After):**
```python
# Server prints to stdout - agent can see
except Exception as e:
    print(f"Error: {e}")  # Agent can see this!
    return {"error": str(e)}
```

**Author's Emphasis:**
> "Making sure agent can read standard out is a massive leverage point."

### 4. Types as Information Flow

**Video Teaching:**
> "Types tell a story about how information travels throughout your codebase."

**Code Location:** `app/server/core/data_models.py`

**Demonstration from Video:**
```python
# DatabaseSchemaResponse type
# Author copies this and asks agent to trace it
```

**Author's Insight:**
> "Types are IDKs - information dense keywords. They point to exact locations in your code base."

### 5. Architecture for Agents

**Video Teaching:**
> "Code-based architecture is a critical leverage point for agentic coding."

**Code Structure:**
```
app/
├── client/  # Clear separation
└── server/  # Cuts possibilities in half
```

**Author's Example:**
> "Because we have these separated, this one simple decision makes it easy for our agent to cut all of its work in half."

**Key Principles from Video:**
- Clear entry points (`server.py`)
- Consistent file structure
- Mirror test structure to source
- 1000 line file limit
- One responsibility per file

### 6. The Core Four

**Video Teaching:**
> "Your agent needs your context, your model, your prompt, and your tools, the core four."

**Tool Discovery Pattern:**
```markdown
# .claude/commands/tools.md
List the tools available to you
```

**Author's Emphasis:**
> "In order to really use tactic to adopt your agent's perspective, We need to see what our agents can see."

### 7. Tests as Self-Validation

**Video Teaching:**
> "Your agent will make mistakes, okay, just like you. The only question is, does it have the right leverage it needs to correct the mistakes?"

**Code Location:** `app/server/tests/`

**Integration Pattern from Video:**
```bash
# Running tests feeds output to agent
uv run pytest
# Agent sees results and can fix issues
```

**Author's Strong Opinion:**
> "If you're not writing tests, you're probably vibe coding."

### 8. Plans as Scaled Prompts

**Video Teaching:**
> "Plans are just prompts. Put accurately, plans are how you communicate massive amounts of work to your agent."

**Code Location:** `specs/init_nlq_to_sql_to_table.md`

**Author's Revelation:**
> "There is no way that I sat here and typed out 700 lines of a plan. We are going to be planning with our agent."

### 9. ADWs (AI Developer Workflows)

**Video Teaching:**
> "ADWs are created when you combine one or more agentic prompts... wrap it in arbitrary code and then you kick it off autonomously with a trigger."

**Code Placeholder:** `adws/` directory

**Author's Vision:**
> "This is the leverage point we'll use to automate the software development lifecycle so well that your code base literally runs itself."

### 10. Programmable vs Interactive Mode

**Video Teaching:**
> "We've been using Claude Code in phase one mode... As we progress throughout TAC, we'll be using programmable mode."

**Command Line Usage:**
```bash
# Interactive (Phase 1)
claude

# Programmable (Phase 2)
claude -p "command"
```

**Author's Challenge:**
> "This will be uncomfortable. As us engineers, we love control and visibility, but it's time for us to let that go."

## KPIs Implementation

### Size
**Video:** "Increase the size of work we can hand off"
**Code:** Plans in `specs/` demonstrate large work handoffs

### Attempts
**Video:** "We don't want to have to go back in after the prompt completes"
**Code:** Tests provide validation to reduce attempts

### Streak
**Video:** "We want back to back to back one shot successes"
**Code:** Commands enable repeatable success

### Presence
**Video:** "Drop your presence to zero"
**Code:** Programmable mode enables zero presence

## The NLQ-to-SQL Application

**Purpose in TAC-2:**
> "This code base will make a great playground we can use to showcase the leverage points of agentic coding."

**Components:**
1. **Frontend:** `app/client/` - Vite + TypeScript
2. **Backend:** `app/server/` - FastAPI + LLM integration
3. **Database:** SQLite with injection protection
4. **Tests:** Comprehensive test suite

**Teaching Vehicle Features:**
- File upload (CSV/JSON)
- Natural language queries
- SQL generation
- Error handling
- Security patterns

## Hidden Patterns from Video

### 1. The "Three Times" Rule
> "Three time makes a pattern. Three time should trigger your engineering brain. Automate."

### 2. The Agent Navigation Problem
> "Every time you boot up a new agent, it has to explore the codebase."

### 3. Token Efficiency
> "We want our codebases to be token efficient."

### 4. Information Dense Keywords
> "Everything you name can be an information dense keyword."

### 5. The Blank Instance Problem
> "With every new session, it starts as a blank instance."

## File Structure Teaches Architecture

**Video Emphasis:**
```
app/
├── client/          # Clear separation
│   └── public/
│       └── sample-data/  # Test data location
├── server/
│   ├── core/        # Business logic
│   └── tests/       # Mirrors core structure
```

**Author's Teaching:**
> "Your architecture stacks up very, very quickly for you or against you."

## Command Composition Pattern

**Video Demonstration:**

1. **Base Command:** `prime.md`
2. **Composite Command:** `install.md` calls `prime.md`
3. **Pattern:** Commands calling commands

**Author's Insight:**
> "This is no different than passing a function inside of a function."

## Evolution Points from TAC-1

### What's New:
1. **Slash Commands** - Not present in TAC-1
2. **Programmable Mode** - Evolution from interactive
3. **12 Leverage Points** - Systematic framework
4. **KPIs** - Measurable success metrics
5. **Real Application** - Beyond toy examples

### What's Reinforced:
1. **Context is King** - Still fundamental
2. **Tools Matter** - Extended from TAC-1
3. **Prompts as Code** - Now organized in commands
4. **Agent Limitations** - Still "brilliant but blind"

## Key Takeaways

The code perfectly demonstrates the concepts taught in the videos:

1. **Commands Directory** = Reusable prompt templates
2. **Prime Pattern** = Standard codebase understanding
3. **Test Structure** = Mirrors source for easy navigation
4. **Clear Architecture** = Reduces agent confusion
5. **Standard Out** = Agent visibility into execution
6. **Types** = Information flow tracking
7. **Plans** = Large-scale work communication

The author uses the NLQ-to-SQL application not just as an example, but as a teaching vehicle that embodies all 12 leverage points in a real, working system.
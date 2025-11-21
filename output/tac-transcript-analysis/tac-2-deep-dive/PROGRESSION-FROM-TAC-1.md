# TAC-2 Progression from TAC-1

## Overview: From Foundation to Framework

TAC-1 established the basics: "Make your codebase Claude-friendly"
TAC-2 transforms this into: "Build systems that operate on your behalf"

The author explicitly states:
> "In lesson one, we set the stage. In lesson two, we start performing."

## Core Evolution Points

### 1. From Simple Prompts to Slash Commands

**TAC-1:**
- Single `prompt.md` file
- Basic Claude configuration
- Manual prompt entry

**TAC-2:**
- `.claude/commands/` directory
- Multiple reusable commands
- Command composition patterns

**Video Insight:**
> "We're using a powerful pattern of running prompts inside of prompts. This is no different than passing a function inside of a function."

### 2. From Toy Examples to Real Applications

**TAC-1:**
- "Hello, Claw!" simple examples
- Basic file operations
- Learning-focused code

**TAC-2:**
- Full NLQ-to-SQL application
- Frontend + Backend + Database
- Production-ready patterns

**Author's Justification:**
> "This code base will make a great playground we can use to showcase the leverage points of agentic coding."

### 3. From Awareness to Systematic Leverage

**TAC-1 Concepts:**
- Claude can read files
- Claude can execute commands
- Context matters

**TAC-2 Framework - The 12 Leverage Points:**

**In-Agent (Core Four):**
1. Context
2. Model
3. Prompt
4. Tools

**Through-Agent:**
5. Standard Out
6. Types
7. Documentation
8. Tests
9. Architecture
10. Plans
11. Templates
12. ADWs

**Author's Promise:**
> "When you stack up these leverage points, Agentic Coding success becomes inevitable."

### 4. From Iteration to Automation

**TAC-1 Workflow:**
```
Human → Prompt → Claude → Response → Human Review → Repeat
```

**TAC-2 Vision:**
```
Human → Command → Agent → Autonomous Execution → Validation
```

**Paradigm Shift:**
> "We've been using Claude Code in phase one mode... This tanks our presence KPI."

### 5. From Qualitative to Quantitative

**TAC-1:**
- "Does it work?"
- "Is it helpful?"
- Subjective success

**TAC-2 KPIs:**
1. **Size** - How much work per prompt
2. **Attempts** - How many tries needed
3. **Streak** - Consecutive successes
4. **Presence** - Human involvement required

**Author's Emphasis:**
> "If you don't measure it, you can't improve it."

## Conceptual Progressions

### The Agent's Perspective

**TAC-1:** Think about what Claude needs
**TAC-2:** "Adopt your agent's perspective"

**Evolution:**
> "Your agent is brilliant, but blind. With every new session, it starts as a blank instance."

This deeper understanding drives all TAC-2 patterns.

### The Role of the Engineer

**TAC-1:** Engineer who uses AI tools
**TAC-2:** "Agentic Engineer" who builds self-operating systems

**Transformation:**
> "In order to become an irreplaceable engineer, we have to stop coding and learn to build systems."

### Error Handling Philosophy

**TAC-1:** Fix errors when they occur
**TAC-2:** Build systems that self-correct

**New Approach:**
> "Your agent will make mistakes... The only question is, does it have the right leverage it needs to correct the mistakes?"

## Technical Progressions

### 1. Directory Structure

**TAC-1:**
```
project/
├── .claude/
│   └── prompt.md
└── src/
```

**TAC-2:**
```
project/
├── .claude/
│   ├── commands/
│   │   ├── install.md
│   │   ├── prime.md
│   │   └── tools.md
│   └── settings.json
├── app/
│   ├── client/
│   └── server/
├── specs/
├── ai_docs/
├── adws/
└── agents/
```

### 2. Command Patterns

**TAC-1:** Single prompts
**TAC-2:** Composable commands

Example from video:
```markdown
# install.md
## Read and Execute
.claude/commands/prime.md  # Command calling command
## Run
Install FE and BE dependencies
```

### 3. Testing Integration

**TAC-1:** Tests exist (maybe)
**TAC-2:** Tests as leverage points

**Video Teaching:**
> "If you're not writing tests, you're leaving massive leverage on the table."

### 4. Documentation Evolution

**TAC-1:** Basic README
**TAC-2:** Multi-layered documentation
- `README.md` - Setup instructions
- `ai_docs/` - LLM provider docs
- `specs/` - Feature specifications
- Command self-documentation

## Mindset Shifts

### 1. From Helper to Partner

**TAC-1:** Claude helps you code
**TAC-2:** Agent does the coding

**Quote:**
> "It's not about what you can do anymore. It's about what you can teach your agents to do."

### 2. From Iteration to One-Shot

**TAC-1:** Iterate until it works
**TAC-2:** Aim for one-shot success

**Strong Statement:**
> "We're not aiming to become a babysitter for AI agents. We're looking for one shot solutions."

### 3. From Control to Trust

**TAC-1:** Maintain control, review everything
**TAC-2:** Build systems, let them run

**Challenge:**
> "This will be uncomfortable. As us engineers, we love control and visibility, but it's time for us to let that go."

## New Concepts in TAC-2

### 1. The Prime Pattern
Not in TAC-1, fundamental in TAC-2:
- List files
- Read documentation
- Summarize understanding

### 2. Standard Out as Communication
**New Insight:**
> "Your agent can only see what you let it see."

### 3. Types as Navigation
**Novel Concept:**
> "Types are IDKs - information dense keywords."

### 4. The Agent Navigation Problem
**Newly Identified:**
> "Every time you boot up a new agent, it has to explore the codebase."

### 5. Programmable Mode
**Game Changer:**
```bash
# TAC-1 style
claude

# TAC-2 evolution
claude -p "/command"
```

## What Remains from TAC-1

### Still Critical:
1. **Context is King** - Even more important now
2. **Clear File Structure** - Enhanced for agent navigation
3. **Good Documentation** - Now systematic
4. **Tool Awareness** - Expanded understanding

### Enhanced Versions:
- **Settings.json** - More permissions in TAC-2
- **Project Structure** - More intentional organization
- **Error Messages** - Now designed for agents

## The Bigger Picture

### TAC-1 Achievement:
"Claude can work with your codebase"

### TAC-2 Achievement:
"Your codebase can run itself through agents"

### The Journey:
1. TAC-1: Learn to communicate with AI
2. TAC-2: Build systems for autonomous operation
3. Future (TAC-3+): Full SDLC automation

## Key Quotes on Progression

**On Evolution:**
> "Just like with AI coding, Agentic Coding is easy to start, hard to master."

**On Urgency:**
> "All the low hanging fruit is getting chewed up. It's time to do the smart work, not the hard work."

**On Transformation:**
> "The new age phase two engineering looks less and less of what it used to look like."

**On Focus:**
> "Master the primitives and you'll master the compositions."

## Practical Differences

### Writing Code:
- **TAC-1:** You write code, Claude helps
- **TAC-2:** Agent writes code, you guide

### Debugging:
- **TAC-1:** You debug with Claude's help
- **TAC-2:** Agent debugs with test feedback

### Planning:
- **TAC-1:** Simple prompts
- **TAC-2:** 700-line specifications

### Success Metrics:
- **TAC-1:** "It works!"
- **TAC-2:** Size ↑, Attempts ↓, Streak ↑, Presence ↓

## Conclusion

TAC-2 represents a fundamental shift from TAC-1:

**TAC-1** taught us to work WITH AI
**TAC-2** teaches us to work THROUGH agents

The progression is:
1. **Awareness** (TAC-1) → **Framework** (TAC-2)
2. **Helper** (TAC-1) → **Partner** (TAC-2)
3. **Iteration** (TAC-1) → **Automation** (TAC-2)
4. **Coding** (TAC-1) → **Engineering** (TAC-2)

The author's vision is clear:
> "We're here to dial up the autonomy knob all the way to 11."

TAC-2 doesn't replace TAC-1; it builds upon it, taking the foundational understanding of Claude-friendly codebases and transforming it into a systematic approach for building self-operating systems through the 12 leverage points and measurable KPIs.
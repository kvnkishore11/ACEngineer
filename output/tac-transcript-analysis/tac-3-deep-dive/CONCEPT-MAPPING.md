# TAC-3 Concept Mapping: Video Teaching to Code Implementation

## Overview
This document maps the concepts taught in the TAC-3 videos directly to their code implementations, showing exactly how the author's teachings manifest in the actual codebase.

## Core Concept Mappings

### 1. Meta-Prompts: "A Prompt That Generates a Prompt"

**Video Teaching** (Video 21-22):
> "What is a meta prompt? It's a prompt that builds a prompt. More specifically, this agentic prompt builds a plan based on a template that our agent fills out."

**Code Implementation**:
```markdown
# Location: tac-3/.claude/commands/chore.md
## Purpose
Create a new plan in specs/*.md to resolve the `Chore`...

## Plan Format
# Chore: [NAME]
## Chore Description
## Relevant Files
## Step by Step Tasks
```

**Video Reference** (Video 23):
> "We are giving our agent a template... This was our plan that was generated from our chore template meta prompt."

### 2. Template Engineering Pattern

**Video Teaching** (Video 22):
> "Not only should we stop coding, we should also lean into and leverage our agent to write plans with us and for us."

**Code Structure**:
```
tac-3/.claude/commands/
├── bug.md       # Bug template → generates bug fix plan
├── chore.md     # Chore template → generates maintenance plan
├── feature.md   # Feature template → generates feature plan
└── implement.md # Execution template → implements any plan
```

### 3. The "Fresh Agent" Pattern

**Video Teaching** (Videos 46-48):
> "Why do I keep opening up new cloud code instances? You know, look at all these terminals. I keep opening new terminals and starting fresh agent instances that have no memory of what just happened."

**Code Evidence**:
- No session state management in commands
- Each command is self-contained
- Plans include all necessary context

**Three Reasons from Transcript**:
1. **Context Window Management**: "Focus every available token on the task at hand"
2. **Asset Independence**: "Force our prompts, plans, and templates to be isolated, reusable, and improvable assets"
3. **Off-Device Preparation**: "Prepare for true off device agentic coding"

### 4. Higher-Order Prompts (HOPs)

**Video Teaching** (Video 27):
> "This is a higher order prompt, AKA a hop... There are a lot of advanced concepts here."

**Code Implementation** (`implement.md`):
```markdown
## Plan
$ARGUMENTS  # The plan file path is passed as an argument

## Instructions
- Read the plan, think hard about the plan and implement
```

### 5. The "Think Hard" Information Dense Keyword

**Video Teaching** (Videos 26, 40):
> "Think hard. We're activating Claude Code's information dense keyword to activate the reasoning model. We're using one of the 12 leverage points of Agentic Coding by turning on the reasoning model."

**Code Occurrences**:
```markdown
# bug.md
- You must use your reasoning model by including: THINK HARD

# feature.md
- Always use your reasoning model, THINK HARD about the feature

# implement.md
- Read the plan, think hard about the plan and implement
```

### 6. Plan Format Standardization

**Video Teaching** (Video 22-23):
> "We have the plan format. Okay. So we requested this agent creates a new plan in the specified markdown format. We are giving our agent a template."

**Chore Template Format**:
```markdown
# Chore: [NAME]
## Chore Description
## Relevant Files
## Step by Step Tasks
## Validation Commands
## Notes
```

**Bug Template Format**:
```markdown
# Bug: [NAME]
## Problem Statement
## Solution Statement
## Steps to Reproduce
## Root Cause Analysis
## Relevant Files
## Step by Step Tasks
## Validation Commands
## Notes
```

**Feature Template Format**:
```markdown
# Feature: [NAME]
## User Story
## Acceptance Criteria
## Technical Implementation
## Relevant Files
## Step by Step Tasks
## Validation Commands
## Notes
```

### 7. Validation Loops

**Video Teaching** (Videos 30-31):
> "We're embedding another lever of agentic coding. We have several self validating loops with tests... So not only did it run all of our PI tests to prevent regressions, it also ran server and main just to make sure that it works."

**Code Pattern** (All templates):
```markdown
## Validation Commands
List all commands that should be run to validate this work...
```

**Actual Generated Example**:
```markdown
## Validation Commands
- Run tests: `pytest`
- Test server startup: `python app/server/main.py`
- Verify no print statements remain: search for "print(" in server files
```

### 8. The SDLC Framework

**Video Teaching** (Video Segments 3-4):
> "Throughout tactical Agentic Coding, we'll break down the software development lifecycle into five concrete steps... Plan, code, test, review, document."

**Code Manifestation**:
1. **Plan**: `bug.md`, `feature.md`, `chore.md` → Generate specs
2. **Code**: `implement.md` → Execute the plan
3. **Test**: Validation commands in every template
4. **Review**: Git diff reporting in implement.md
5. **Document**: Plans themselves serve as documentation

### 9. The Core Four Enhancement

**Video Teaching** (Videos 2, 7):
> "Agentic Coding and the Core 4 takes it all to the next level with the addition of tools, our prompts have become exponentially more powerful."

**TAC Evolution in Code**:
- **TAC-1**: Basic permissions in settings.json
- **TAC-2**: Added commands directory structure
- **TAC-3**: Templates + meta-prompts + fresh agents

### 10. Git Integration for Reporting

**Video Teaching** (Videos 29-30):
> "Report files change... this is going to be super, super important once we really start getting into true off device agentic coding."

**Code Implementation** (`implement.md`):
```markdown
## Report
When you've completed the work:
- Summarize what you did in bullet points
- Report files and lines changed: `git diff --stat`
```

### 11. One-Shot Success Pattern

**Video Teaching** (Videos 52-53):
> "We want one shot successes... Size goes up, but it does mean that our plans are prompts scaled up contains everything an agent needs to get started."

**Code Design**:
- Templates include ALL necessary sections
- Plans are comprehensive and self-contained
- No back-and-forth iteration expected

### 12. Specialization for Scale

**Video Teaching** (Video 50):
> "The more code, the more complexity in your code base, the more you'll want to dial in your reusable templates to solve specific problems really well."

**Code Guidance** (bug.md):
```markdown
## Instructions
- Be surgical with your bug fix
- Aim for the minimal number of changes necessary
- Fix the root cause and prevent similar issues
```

## Hidden Implementation Details

### 1. The `scripts/copy_dot_env.sh` Integration
**Not explicitly mentioned in videos but present in code**:
- Automatically copies .env files during install
- Shows automation beyond what's discussed

### 2. The `main.py` Entry Point Addition
**Added in TAC-3 but not discussed**:
- Located at `app/server/main.py`
- Provides cleaner server startup

### 3. The specs/ Directory Convention
**Briefly shown but not explained**:
- All generated plans go to `specs/*.md`
- Creates audit trail of all work planned

## Video-to-Code Quick Reference

| Video Segment | Concept Taught | Code Location | Implementation |
|--------------|----------------|---------------|----------------|
| 21-23 | Meta-prompts | `.claude/commands/*.md` | Templates that generate plans |
| 26-27 | "Think hard" keyword | All templates | Activates reasoning model |
| 29-30 | Git reporting | `implement.md` | `git diff --stat` requirement |
| 46-48 | Fresh agents | Command design | No session dependencies |
| 50-51 | Template specialization | Multiple templates | bug/feature/chore variants |
| 52-54 | One-shot execution | Plan structure | Self-contained specifications |

## Key Insights from Mapping

1. **Every video concept has concrete implementation** - The author practices what they teach
2. **Code is simpler than explanation** - The templates are surprisingly concise
3. **Progressive complexity** - TAC-3 builds directly on TAC-1 and TAC-2 foundations
4. **Hidden sophistication** - Simple markdown files enable complex workflows
5. **Extensibility built-in** - Template pattern allows infinite customization

## What's Taught vs What's Built

### Explicitly Taught:
- Meta-prompts concept
- Fresh agent pattern
- Template engineering
- SDLC automation
- 12 leverage points (partially)

### Present but Not Emphasized:
- Specific markdown formatting requirements
- Directory structure conventions
- Environment setup automation
- The power of `$ARGUMENTS` parameter passing
- Git integration depth

### Mentioned but Not Implemented:
- Full 12 leverage points enumeration
- Parallel agent execution
- Off-device agent deployment
- Team collaboration features
- Advanced codebase handling techniques

This mapping reveals that TAC-3's code is both a complete implementation of the core concepts AND a foundation for the advanced techniques mentioned but not yet built.
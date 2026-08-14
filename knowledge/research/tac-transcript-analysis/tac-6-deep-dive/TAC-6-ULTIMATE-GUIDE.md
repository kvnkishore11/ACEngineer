# TAC-6 Ultimate Guide: The Complete SDLC Automation System

*The definitive guide combining video transcripts, code analysis, and implementation patterns for mastering TAC-6*

## Executive Summary

TAC-6 represents the **completion of the Software Developer Lifecycle automation** vision. It introduces the final two steps—**Review** and **Documentation**—creating a complete feedback loop where agents not only build and test but also validate their work against specifications and document it for future agent intelligence.

The core philosophy: **"One Agent, One Prompt, One Purpose"**—a controversial but powerful stance against the industry's pursuit of "god models" in favor of specialized, focused agents that excel at singular tasks.

## Core Innovation: Complete SDLC Automation

### The Five Questions of Engineering

TAC-6 completes the SDLC by framing each step as a question:

1. **Plan**: What are we building? *(TAC-3)*
2. **Build**: Did we make it real? *(TAC-4)*
3. **Test**: Does it work? *(TAC-5)*
4. **Review**: Is what we built what we planned? *(TAC-6)*
5. **Document**: How does it work? *(TAC-6)*

### The Critical Distinction: Testing vs. Reviewing

> "Testing answers the question, does it work? But review answers the question, is what we built what we asked for?"

This distinction is crucial:
- **Testing**: Validates functionality
- **Reviewing**: Validates intent alignment

## The Central Tactic: One Agent, One Prompt, One Purpose

### Why This Matters

1. **Free the Context Window**: Each agent gets full token allocation
2. **Agent Focus**: No context pollution or confusion
3. **Improvability**: Every prompt is versioned and improvable
4. **Evaluability**: Create implicit evals for your agentic layer

### Implementation Pattern

```python
# Each ADW is single-purpose
adw_plan.py      # Only planning
adw_build.py     # Only building
adw_test.py      # Only testing
adw_review.py    # Only reviewing
adw_document.py  # Only documenting
adw_patch.py     # Only patching
```

## System Architecture

### Directory Structure
```
tac-6/
├── .claude/commands/       # Single-purpose prompts
│   ├── review.md          # Review implementation
│   ├── document.md        # Generate documentation
│   ├── patch.md           # Surgical fixes
│   └── conditional_docs.md # Dynamic documentation index
├── adws/                  # AI Developer Workflows
│   ├── adw_review.py      # Review workflow
│   ├── adw_document.py    # Documentation workflow
│   ├── adw_patch.py       # Patch workflow
│   └── adw_modules/       # Shared components
├── app_docs/              # Generated documentation
│   └── assets/           # Screenshots
├── agents/{adw_id}/       # Agent work directories
│   ├── state.json        # Workflow state
│   ├── review_img/       # Review screenshots
│   └── {agent_name}/     # Agent-specific logs
└── specs/                # Plans and patches
    └── patches/          # Surgical fix plans
```

## Key Workflows

### 1. The Review Workflow

**Purpose**: Validate that implementation matches specification

**Process**:
1. Read specification file
2. Analyze git diff against main
3. Capture 1-5 critical screenshots
4. Classify issues (blocker/tech_debt/skippable)
5. Upload screenshots to public bucket
6. If blockers exist, trigger patch workflow

**Key Innovation**: Visual Proof
```python
# Screenshots provide undeniable evidence
review_result = {
    "success": True,  # No blockers
    "screenshots": [
        "/path/to/01_feature_working.png",
        "/path/to/02_ui_correct.png"
    ],
    "review_issues": []
}
```

### 2. The Documentation Workflow

**Purpose**: Create self-updating documentation system

**Two-Part System**:

#### Part 1: Generate Documentation
```markdown
# Feature Documentation
**ADW ID**: adw-123
**Date**: 2024-01-15
**Specification**: specs/feature.md

## Overview
[Auto-generated from git diff and spec]

## Screenshots
![Feature](assets/01_feature.png)

## Technical Implementation
[Extracted from code changes]

## How to Use
[User-focused instructions]
```

#### Part 2: Conditional Documentation
```markdown
# conditional_docs.md
- app_docs/feature-auth.md
  - Conditions:
    - When working with authentication
    - When implementing user sessions
```

**The Magic**: Future agents read conditional_docs.md and automatically include relevant documentation in their context when planning new work.

### 3. The Patch Workflow

**Purpose**: Surgical fixes without full rebuild

**When to Use**:
- Review finds blocker issues
- Small UI adjustments needed
- Quick bug fixes

**Process**:
1. Create focused patch plan
2. Implement minimal changes
3. Validate fix
4. Update documentation

## Advanced Patterns

### State Management System

```python
class ADWState:
    """Travels between workflows"""
    adw_id: str        # Unique workflow ID
    branch_name: str   # Git branch
    plan_file: str     # Specification
    issue_class: str   # bug/feature/chore
```

State persists across workflow steps:
- `agents/{adw_id}/state.json`

### Issue Severity Classification

```python
class ReviewIssue:
    severity: Literal["blocker", "tech_debt", "skippable"]
```

- **Blocker**: Must fix before merge
- **Tech Debt**: Should fix but not blocking
- **Skippable**: Minor, can ignore

### Composed Workflows

Chain base workflows for complete automation:
```bash
# Complete development cycle
uv run adw_plan_build_test_review.py

# Quick iteration
uv run adw_plan_build_review.py

# Documentation after success
uv run adw_document.py
```

## Implementation Checklist

### Environment Setup
- [ ] Install Claude Code CLI
- [ ] Configure Anthropic API key
- [ ] Set up Cloudflare R2 or S3 bucket
- [ ] Configure GitHub access token
- [ ] Install uv package manager

### Workflow Implementation
- [ ] Create `.claude/commands/` directory
- [ ] Implement review.md command
- [ ] Implement document.md command
- [ ] Implement patch.md command
- [ ] Set up conditional_docs.md
- [ ] Create ADW Python scripts
- [ ] Configure state management

### Integration Points
- [ ] GitHub Issues for prompt source
- [ ] Pull Requests for review
- [ ] R2/S3 for screenshot storage
- [ ] MCP for Playwright automation

## Mental Models & Philosophy

### The System That Builds The System

> "We are putting in the effort to build the system that builds the system... This isn't about you anymore. It's about your agents."

**Mindset Shift Required**:
- Stop doing, start teaching
- Stop coding, start orchestrating
- Stop fixing, start systematizing

### Context Minimalism

> "You want the minimum context in your prompt required to solve the problem."

**Why Less Is More**:
- Focused agents perform better
- No context pollution
- Clearer debugging
- Faster iteration

### The Three Constraints

As agentic engineers, we face:
1. **Context window** ✓ (solved by specialization)
2. **Codebase complexity** ✓ (solved by specialization)
3. **Our abilities** ✗ (remaining bottleneck)

Specialized agents eliminate 2/3 constraints.

## Agentic KPIs

Track your system's performance:

### Attempts ↓
- Ideal: 1 attempt per feature
- Reality: 1-3 with patches

### Streak ↑
- Consecutive successful workflows
- Broken by patches or failures

### Size ↑
- Scope of work per attempt
- Larger features in single workflows

### Presence ↓
- Ideal: 2 touches (start + review)
- TAC-7 promises even less

## Common Patterns & Best Practices

### 1. Always Review Before Document
```bash
# Correct order
uv run adw_review.py
uv run adw_document.py

# Not recommended
uv run adw_document.py  # Without review
```

### 2. Skip Test at Your Peril
> "We did completely skip the test step... testing very likely would have caught this issue"

### 3. Vision Mode Enhancement
```markdown
# Add to review.md
"For every image you take, be sure to read it in during the review process"
```

### 4. Background Process Management
```bash
# In install scripts
npm start &  # Background
# Not: npm start (blocks agent)
```

## Troubleshooting Guide

### Issue: Agent Context Overflow
**Symptom**: Compact command running
**Solution**: Split into multiple single-purpose agents

### Issue: Review Missing UI Issues
**Symptom**: Visual bugs not caught
**Solution**: Enable vision mode, add image reading instructions

### Issue: Documentation Not Found by Agents
**Symptom**: Agents missing relevant docs
**Solution**: Update conditional_docs.md with better conditions

### Issue: Patch Loops
**Symptom**: Multiple patch attempts
**Solution**: Improve review criteria, add better specs

## Advanced Techniques

### 1. Webhook-Triggered Automation
```python
# GitHub webhook → ADW trigger
# Comment "!review" → Run review workflow
# Comment "!patch: fix button" → Run patch
```

### 2. Severity-Based Automation
```python
if issue.severity == "skippable":
    auto_merge = True
elif issue.severity == "tech_debt":
    create_future_issue = True
else:  # blocker
    require_human_review = True
```

### 3. Documentation Intelligence
```python
# Future agents read past documentation
if "authentication" in task_description:
    include_docs = ["app_docs/auth-feature.md"]
```

## The Hidden Power: Feedback Loops

### The Complete Circle
```
Plan (reads docs) → Build → Test → Review (validates) → Document (updates docs)
                                                                     ↓
                                                                     ↓
Future Plans ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
```

Each cycle makes the system smarter.

## What's Coming: TAC-7 Preview

The author teases:
- **"Dangerous Mode"**: Direct to production
- **"The Secret"**: Hidden throughout TAC
- **"Wacky"**: Beyond traditional engineering
- **Presence → 0**: Full automation

## Action Steps

### Immediate (Today)
1. Set up review workflow
2. Configure screenshot uploads
3. Create first conditional_docs.md

### Short Term (This Week)
1. Implement patch workflow
2. Add documentation generation
3. Create composed workflows

### Long Term (This Month)
1. Achieve single-attempt features
2. Build documentation library
3. Optimize agent specialization

## Key Takeaways

1. **Review ≠ Testing**: Different questions, different value
2. **Documentation = Future Intelligence**: Not just records
3. **Specialization > Generalization**: Focused agents win
4. **Visual Proof > Text Reports**: Screenshots convince
5. **Patches > Rebuilds**: Surgical fixes save time

## The Ultimate Message

> "Do you want to be an agentic engineer or do you want to be an engineer of the past?"

TAC-6 completes the transformation from manual engineer to **commander of compute**. With review and documentation, you have a complete system that:

- Plans intelligently
- Builds accurately
- Tests thoroughly
- Reviews visually
- Documents automatically
- Patches surgically
- Improves continuously

The future isn't about writing code—it's about building systems that build systems. TAC-6 gives you that system.

## Resources & References

### Required Tools
- Claude Code CLI
- Python with uv
- Git & GitHub
- Cloudflare R2 / AWS S3
- Playwright (via MCP)

### File References
- Complete Transcript: `COMPLETE-TRANSCRIPT.md`
- Author Analysis: `AUTHOR-VOICE-ANALYSIS.md`
- Concept Mapping: `CONCEPT-MAPPING.md`
- Hidden Insights: `HIDDEN-INSIGHTS.md`
- TAC Progression: `PROGRESSION-FROM-TAC-5.md`

### Community & Support
- TAC Course Materials
- GitHub Issues for questions
- Community Discord (if available)

---

*"Great work here. Do not wait to start putting this stuff in your codebase. Set up basic ADWs, set up basic agentic prompts, get your advantage, start rolling this into your code bases. The value here is immense."* - TAC-6 Author
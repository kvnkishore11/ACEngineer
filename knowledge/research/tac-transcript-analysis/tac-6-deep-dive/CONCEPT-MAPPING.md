# TAC-6 Concept Mapping: Video Teaching to Code Implementation

*Mapping the author's spoken concepts to concrete code implementations in the TAC-6 codebase*

## Core Tactic: One Agent, One Prompt, One Purpose

### Video Teaching (Segment 9-13)
> "The tactic is one agent one prompt one purpose. This unlocks massive Agentic Coding capabilities throughout the new agentic layer of your code base."

### Code Implementation

#### ADW Structure
Each ADW file represents a single workflow with one purpose:
- `adw_plan.py` - Planning only
- `adw_build.py` - Building only
- `adw_review.py` - Review only
- `adw_document.py` - Documentation only
- `adw_patch.py` - Patching only

#### Agent Name Constants
```python
# From adw_review.py
AGENT_REVIEWER = "reviewer"
AGENT_REVIEW_PATCH_PLANNER = "review_patch_planner"
AGENT_REVIEW_PATCH_IMPLEMENTOR = "review_patch_implementor"
```

#### Single Command Execution
Each prompt in `.claude/commands/` does ONE thing:
- `/review` - Reviews against spec
- `/document` - Creates documentation
- `/patch` - Creates surgical fixes
- `/implement` - Implements a plan

## The Software Developer Lifecycle as Q&A

### Video Teaching (Segment 4-5)
> "Every step of the software developer lifecycle can be represented as a question and an answer:
> - Plan: What are we building?
> - Build: Did we make it real?
> - Test: Does it work?
> - Review: Is what we built what we planned?
> - Document: How does it work?"

### Code Implementation

#### Composed ADW Workflows
The author creates composed workflows that chain these questions:
- `adw_plan_build_review.py` - Plan → Build → Review
- `adw_plan_build_document.py` - Plan → Build → Document
- `adw_plan_build_test_review.py` - Full cycle

#### State Management Between Steps
```python
# From adw_modules/state.py
class ADWState:
    """State that travels between AI Developer Workflows"""
    adw_id: str
    branch_name: str
    plan_file: str
    issue_class: str
```

## Review vs Testing: The Critical Distinction

### Video Teaching (Segment 3-5)
> "Testing answers the question, does it work? But review answers the question, is what we built what we asked for?"

### Code Implementation

#### Review Command (`review.md`)
```markdown
# Key distinction in instructions:
- IMPORTANT: To be clear, we're not testing. We know the functionality works.
  We're reviewing the implementation against the spec to make sure it matches
  what was requested.
```

#### Review Output Structure
```json
{
    "success": "true if NO BLOCKING issues",
    "review_summary": "What was built and whether it matches spec",
    "review_issues": [{
        "issue_severity": "skippable | tech_debt | blocker"
    }],
    "screenshots": ["proof of implementation"]
}
```

## Visual Proof & Review Velocity

### Video Teaching (Segment 62-63, 101-103)
> "We have images uploaded... Our agents are presenting the work to us. This is super critical for agentic engineering work."

### Code Implementation

#### R2 Upload Integration
```python
# From adw_review.py
from adw_modules.r2_uploader import R2Uploader

# Upload screenshots to public bucket
uploader = R2Uploader()
uploaded_urls = uploader.upload_screenshots(screenshots)
```

#### Screenshot Capture Instructions
```markdown
# From review.md
- IMPORTANT: Aim for 1-5 screenshots to showcase functionality
- Number screenshots: 01_<descriptive>.png, 02_<descriptive>.png
- Store in review_image_dir with absolute paths
- Focus only on critical functionality paths
```

## The Patch Workflow: Surgical Fixes

### Video Teaching (Segment 66-69)
> "This is the whole point of the patch workflow... We want a simple quick fix."

### Code Implementation

#### Patch Command (`patch.md`)
```markdown
# Create a focused patch plan to resolve a specific issue
Follow instructions to create concise plan with minimal targeted changes
```

#### Patch Plan Structure
```markdown
specs/patches/{adw_id}/patch_{number}.md
- Issue Summary
- Solution Approach
- Minimal Implementation
```

## Documentation as Future Agent Intelligence

### Video Teaching (Segment 7-8, 90-96)
> "Documentation provides feedback on work done for future agents to reference in their work."

### Code Implementation

#### Conditional Documentation System
```markdown
# conditional_docs.md - Self-updating index
- app_docs/feature-xyz.md
  - Conditions:
    - When working with authentication
    - When implementing user sessions
    - When troubleshooting login issues
```

#### Documentation Auto-Update in Prompts
```markdown
# From bug.md, feature.md, chore.md
## Relevant Files
Read .claude/commands/conditional_docs.md to check if your task
requires additional documentation
```

## The Feedback Loop Architecture

### Video Teaching (Segment 94-96)
> "This creates a very powerful end-to-end full feedback cycle between the beginning of the software developer lifecycle with the planning and the end with the documenting."

### Code Implementation

#### Documentation Updates Conditional Docs
```python
# From document.md instructions
### 5. Update Conditional Documentation
- After creating documentation file, read conditional_docs.md
- Add entry for new documentation with appropriate conditions
- Entry helps future developers know when to read this
```

#### Planning Reads Conditional Docs
```markdown
# From feature.md, bug.md, patch.md
Check conditional_docs.md for relevant documentation
If task matches conditions, include those docs in the plan
```

## Context Window Management

### Video Teaching (Segment 14-17)
> "You free up the context window. You give your agent the full 200K, 500K, 1 million tokens... You want the minimum context in your prompt required to solve the problem."

### Code Implementation

#### Focused Agent Templates
Each command has minimal required context:
```python
# From execute_template in agent.py
request = AgentTemplateRequest(
    agent_name=AGENT_REVIEWER,  # Single agent
    slash_command="/review",     # Single command
    args=[adw_id, spec_file],    # Minimal args
    adw_id=adw_id
)
```

#### No Context Stacking
```python
# Each ADW runs fresh
def run_review(spec_file, adw_id, logger):
    # Fresh context for review
    request = AgentTemplateRequest(...)

def run_patch(issue_desc, adw_id, logger):
    # Fresh context for patch
    request = AgentTemplateRequest(...)
```

## Issue Severity Classification

### Video Teaching (Segment 43-44)
> "We have skippable, tech debt, and blocker. You want to make sure you're accounting for things that your agents are going to find."

### Code Implementation

#### ReviewIssue Type Definition
```python
# From data_types.py
class ReviewIssue:
    review_issue_number: int
    screenshot_path: str
    issue_description: str
    issue_resolution: str
    issue_severity: Literal["skippable", "tech_debt", "blocker"]
```

#### Review Logic
```python
# From adw_review.py
blocking_issues = [
    issue for issue in review_result.review_issues
    if issue.issue_severity == "blocker"
]
if blocking_issues:
    resolve_review_issues(blocking_issues, ...)
```

## Improvable Prompts Philosophy

### Video Teaching (Segment 18-21)
> "We get to commit every one of our prompts... we can easily reproduce and more importantly, improve every single step down to the prompt level."

### Code Implementation

#### All Prompts in Version Control
```
.claude/commands/
├── bug.md          # Improvable bug planning
├── feature.md      # Improvable feature planning
├── review.md       # Improvable review process
├── document.md     # Improvable documentation
└── patch.md        # Improvable patch creation
```

#### Searchable Command Pattern
```python
# Easy to find and improve
"search for: slash_command='/review'"
"search for: execute_template"
"search for: template_request"
```

## The "System That Builds The System"

### Video Teaching (Segment 74-76)
> "The whole point here is that we are putting in the effort to build the system that builds the system."

### Code Implementation

#### ADW Module Structure
```python
adw_modules/
├── state.py          # State management system
├── git_ops.py        # Git operation system
├── github.py         # GitHub integration system
├── workflow_ops.py   # Workflow composition system
├── agent.py          # Agent execution system
└── r2_uploader.py    # Asset management system
```

#### Composed Workflows Build on Base Workflows
```python
# adw_plan_build_review.py
subprocess.run(["uv", "run", "adw_plan.py", ...])
subprocess.run(["uv", "run", "adw_build.py", ...])
subprocess.run(["uv", "run", "adw_review.py", ...])
```

## Hidden Implementation Details from Video

### The Compact Warning (Segment 16)
> "The compact command inside of Claude Code... this is a bandaid fix. If your agent is running compact, it is losing information."

**Not directly in code but influences design:**
- Single-purpose agents avoid context overflow
- No need for compaction with focused prompts

### Vision Mode Consideration (Segment 70-71)
> "We don't have this dash dash vision. We're not operating in vision mode."

**Suggested improvement in video:**
```markdown
# Potential addition to review.md
"For every image you take, be sure to read it in during the review process"
```

### The Three Constraints (Segment 15)
> "We have three constraints: the context window, the complexity of our codebase, and our abilities. Specialized agents bypass two out of three."

**Architectural impact:**
- ADWs handle complexity through specialization
- Context window freed by single-purpose design
- Only "our abilities" remain as constraint

## State Persistence Across Workflows

### Video Teaching (Segment 35-36)
> "We have state meta information that travels along every one of our AI developer workflows."

### Code Implementation

```python
# State file location pattern
agents/{adw_id}/state.json

# State validation
def validate_state(state: ADWState):
    if not state.branch_name:
        raise ValueError("Branch name required")
    if not state.plan_file:
        raise ValueError("Plan file required")
```

## The Evolution Path

### From Manual to Agentic (Segment 77-78)
> "Do you want to be an agentic engineer or do you want to be an engineer of the past?"

**Code manifestation:**
- `/install` command replaces manual setup
- ADW workflows replace manual SDLC steps
- Patch workflows replace manual fixes
- Review automation replaces manual PR review

This mapping shows how every philosophical point and mental model the author teaches in the video has a concrete implementation in the TAC-6 codebase, creating a complete system where theory meets practice.
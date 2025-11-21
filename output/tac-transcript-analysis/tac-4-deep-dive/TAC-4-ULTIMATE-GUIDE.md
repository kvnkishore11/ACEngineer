# TAC-4 Ultimate Guide: The Complete ADW System Mastery

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [The TAC-4 Revolution](#the-tac-4-revolution)
3. [Core Concepts](#core-concepts)
4. [The ADW System Architecture](#the-adw-system-architecture)
5. [Implementation Guide](#implementation-guide)
6. [Advanced Patterns](#advanced-patterns)
7. [Production Deployment](#production-deployment)
8. [Troubleshooting](#troubleshooting)
9. [Future Roadmap](#future-roadmap)
10. [Quick Start Checklist](#quick-start-checklist)

## Executive Summary

TAC-4 introduces the **Agentic Development Workflow (ADW)** system - a revolutionary approach that transforms GitHub issues into completed pull requests autonomously. This isn't incremental improvement; it's a paradigm shift from "AI-assisted coding" to "autonomous engineering systems."

**The Core Promise**: "Stay out the loop and let your product build itself."

**The Key Innovation**: ADW - a reusable agentic pipeline that combines deterministic code with non-deterministic AI to create self-operating development systems.

**The Outcome**: 10x+ velocity improvement with engineers focusing on system design rather than implementation.

## The TAC-4 Revolution

### What Makes TAC-4 Different

| Aspect | Traditional | TAC-3 | TAC-4 |
|--------|------------|-------|-------|
| **Execution** | Manual | Semi-automated | Fully autonomous |
| **Trigger** | Human initiated | Command-based | Event-driven |
| **Environment** | Local only | Local with templates | Dedicated + isolated |
| **Workflow** | Ad-hoc | Templated | Pipeline-based |
| **Integration** | None | File-based | GitHub-native |
| **Observability** | Console | Logs | Multi-layer tracking |

### The Philosophical Shift

> "In order to become an irreplaceable engineer, we have to stop coding and learn to build systems that can operate on our behalf."

This isn't about working faster - it's about working at a different level entirely.

## Core Concepts

### 1. The PETER Framework
**Four Elements of AFK (Away From Keyboard) Agents**

```
P - Prompt Input    → GitHub Issues
E - Environment     → Dedicated agent sandbox
T - Trigger        → Webhook/Cron/Manual
E - (Environment)  → (Redundant but memorable)
R - Review         → Pull Requests
```

### 2. The ADW (AI Developer Workflow)

**Definition**: A reusable agentic workflow that combines code, agentic prompts, and agents to deliver results autonomously.

**Components**:
```python
ADW = {
    "Triggers": ["webhook", "cron", "manual"],
    "Pipeline": ["classify", "plan", "implement", "commit", "pr"],
    "Agents": ["classifier", "planner", "implementor", "pr_creator"],
    "Outputs": ["plan.md", "implementation", "pull_request"]
}
```

### 3. The Agent Specialization Principle

> "By separating our agents, we're able to isolate the big three context model in prompt to solve one problem and solve one problem well."

Each agent is a specialist:
- **issue_classifier**: Expert at categorization
- **sdlc_planner**: Master of planning
- **sdlc_implementor**: Implementation specialist
- **pr_creator**: PR crafting expert

### 4. The ADW ID System

Every workflow gets a unique 8-character identifier:
```python
adw_id = "5f2e861e"  # Tracks everything in this workflow
```

This ID:
- Links all artifacts
- Enables debugging
- Provides audit trail
- Isolates agent outputs

## The ADW System Architecture

### System Overview
```
GitHub Issue
    ↓
[Trigger System]
    ↓
ADW Pipeline
    ├── Classify Issue (bug/feature/chore)
    ├── Generate Branch
    ├── Create Plan
    ├── Implement Solution
    ├── Commit Changes
    └── Create PR
    ↓
GitHub Pull Request
```

### Directory Structure
```
tac-4/
├── .claude/commands/       # Templates & Meta-prompts
│   ├── classify_issue.md
│   ├── feature.md
│   ├── bug.md
│   ├── chore.md
│   ├── implement.md
│   └── pull_request.md
├── adws/                   # ADW System Core
│   ├── adw_plan_build.py  # Main orchestrator
│   ├── agent.py           # Claude CLI wrapper
│   ├── github.py          # GitHub integration
│   ├── trigger_webhook.py # Event-driven trigger
│   ├── trigger_cron.py    # Polling trigger
│   └── data_types.py      # System models
├── agents/[adw_id]/        # Execution artifacts
├── logs/                   # Detailed logging
└── specs/                  # Generated plans
```

### Data Flow
```python
# 1. Issue arrives
issue = fetch_issue(number=123)

# 2. ADW starts
adw_id = make_adw_id()  # "5f2e861e"

# 3. Classification
type = classify_issue(issue)  # "feature"

# 4. Planning
plan = generate_plan(issue, type)

# 5. Implementation
code = implement_solution(plan)

# 6. Delivery
pr = create_pull_request(code)
```

## Implementation Guide

### Step 1: Environment Setup

```bash
# Clone the repository
git clone [tac-4-repo]
cd tac-4

# Create your own GitHub repo
gh repo create my-tac-4 --private
git remote set-url origin https://github.com/YOU/my-tac-4

# Install dependencies
uv run install
```

### Step 2: Configuration

**.env file**:
```bash
# Required
ANTHROPIC_API_KEY=sk-ant-xxxxx
CLAUDE_CODE_PATH=/usr/local/bin/claude

# Optional but recommended
GITHUB_PAT=ghp_xxxxx
```

### Step 3: Test the System

```bash
# Health check
uv run adws/health_check.py 1

# Create a test issue on GitHub
# Title: "Add JSON-L support"
# Body: "Support uploading .jsonl files"

# Run the ADW
cd adws
uv run adw_plan_build.py 1
```

### Step 4: Set Up Triggers

**Option A: Manual Trigger**
```bash
uv run adw_plan_build.py <issue-number>
```

**Option B: Webhook Trigger**
```python
# adws/trigger_webhook.py
# Set up GitHub webhook to your endpoint
```

**Option C: Cron Trigger**
```python
# adws/trigger_cron.py
# Polls for new issues every N minutes
```

### Step 5: Progressive Implementation

1. **Start with Chores** (Low risk, high confidence)
   ```markdown
   Issue: "Add logging to API endpoints"
   Type: Chore
   Complexity: Low
   ```

2. **Move to Bugs** (Focused, testable)
   ```markdown
   Issue: "Fix SQL injection in user query"
   Type: Bug
   Complexity: Medium
   ```

3. **Graduate to Features** (Creative, complex)
   ```markdown
   Issue: "Add OAuth authentication"
   Type: Feature
   Complexity: High
   ```

## Advanced Patterns

### 1. Multi-Model Strategy
```python
# Use different models for different complexity
MODELS = {
    "classify": "claude-3-haiku",      # Fast, cheap
    "plan": "claude-3-5-sonnet",       # Balanced
    "implement": "claude-3-opus"        # Powerful
}
```

### 2. Custom Agent Pipeline
```python
# Extend the pipeline with custom agents
CUSTOM_PIPELINE = [
    "classify_issue",
    "security_review",  # Custom
    "generate_plan",
    "code_review",      # Custom
    "implement",
    "test_generation",  # Custom
    "create_pr"
]
```

### 3. Parallel ADW Execution
```python
# Run multiple ADWs simultaneously
issues = [101, 102, 103, 104]
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(run_adw, issue) for issue in issues]
```

### 4. ADW Composition
```python
# ADWs that trigger other ADWs
def meta_adw(epic_issue):
    subtasks = decompose_epic(epic_issue)
    for task in subtasks:
        create_issue(task)
        run_adw(task.number)
```

### 5. Self-Improving Templates
```python
# Track success rates and improve prompts
def track_and_improve():
    success_rate = calculate_success_rate()
    if success_rate < 0.8:
        improve_prompt = generate_improvement_prompt()
        update_template(improve_prompt)
```

## Production Deployment

### Infrastructure Setup

#### Option 1: Dedicated Mac Mini
```bash
# Author's recommended approach
- Mac Mini M2: $599
- Always on, dedicated environment
- Full control, no cloud limitations
```

#### Option 2: Cloud VM
```bash
# AWS EC2 / Google Cloud / Azure
- t3.medium instance
- Ubuntu 22.04
- Docker containerization
```

#### Option 3: GitHub Actions
```yaml
name: ADW Pipeline
on:
  issues:
    types: [opened, edited]
jobs:
  run-adw:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: uv run adw_plan_build.py ${{ github.event.issue.number }}
```

### Security Considerations

1. **API Key Management**
   ```python
   # Use environment variables, never hardcode
   os.getenv("ANTHROPIC_API_KEY")
   ```

2. **Permission Boundaries**
   ```python
   # Limit agent permissions
   ALLOWED_OPERATIONS = ["read", "write", "commit"]
   FORBIDDEN_OPERATIONS = ["delete", "force-push"]
   ```

3. **Branch Protection**
   ```yaml
   # GitHub branch protection rules
   - Require PR reviews
   - Dismiss stale reviews
   - Require status checks
   ```

### Monitoring & Observability

```python
# Multi-layer observability
OBSERVABILITY = {
    "GitHub Comments": "User-facing progress",
    "File Logs": "Detailed debugging",
    "Metrics": "Success rates, timing",
    "Alerts": "Failure notifications"
}
```

## Troubleshooting

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "No module named 'claude'" | CLI not installed | Install Claude CLI |
| "GitHub API rate limit" | Too many requests | Add GITHUB_PAT |
| "Agent timeout" | Complex task | Increase timeout, use stronger model |
| "Permission denied" | Branch protection | Configure bot permissions |
| "Classification wrong" | Ambiguous issue | Improve classify_issue.md template |

### Debugging Workflow

1. **Check ADW ID outputs**
   ```bash
   ls agents/[adw_id]/*/
   cat agents/[adw_id]/*/raw_output.json
   ```

2. **Review logs**
   ```bash
   tail -f logs/[adw_id]/*.log
   ```

3. **Inspect GitHub comments**
   - Check issue comments for progress updates
   - Look for error messages

4. **Validate templates**
   ```bash
   claude --command /classify_issue --arg "issue_title=Test"
   ```

## Future Roadmap

### Near Term (Next Module - TAC-5)
- **Testing Integration**: Automated test generation and execution
- **Review Automation**: AI-powered code review
- **Documentation Generation**: Automatic docs from code

### Medium Term
- **Self-Improving ADWs**: ADWs that optimize themselves
- **Multi-Repository Support**: ADWs that work across repos
- **Team Collaboration**: Multiple agents working together

### Long Term Vision
> "In the future these will just be known as scripts and will fully expect agentic behavior by default."

- **Recursive ADWs**: ADWs building ADWs
- **Natural Language Infrastructure**: "Create a microservice for user authentication"
- **Self-Evolving Codebases**: Code that improves itself based on metrics

## Quick Start Checklist

### Essential Setup ✅
- [ ] Clone TAC-4 repository
- [ ] Create your own GitHub repo
- [ ] Install Claude CLI
- [ ] Set up .env file with API keys
- [ ] Run health check successfully
- [ ] Create first test issue
- [ ] Execute first ADW successfully

### Progressive Mastery Path 📈
1. **Week 1**: Run existing ADWs on simple chores
2. **Week 2**: Customize templates for your codebase
3. **Week 3**: Implement webhook triggers
4. **Week 4**: Build custom agent pipelines
5. **Month 2**: Deploy production ADW system
6. **Month 3**: Create self-improving templates

### Key Metrics to Track 📊
- **Success Rate**: % of ADWs that produce mergeable PRs
- **Time Savings**: Human hours saved per week
- **Velocity Increase**: Features shipped per sprint
- **Quality Metrics**: Bugs introduced vs prevented

## Essential Commands Reference

```bash
# Run ADW on issue
uv run adws/adw_plan_build.py 123

# Run with specific ADW ID
uv run adws/adw_plan_build.py 123 abc12345

# Health check
uv run adws/health_check.py 123

# Start webhook server
uv run adws/trigger_webhook.py

# Start cron monitor
uv run adws/trigger_cron.py

# View agent outputs
cat agents/*/sdlc_implementor/raw_output.json

# Check logs
tail -f logs/*/*.log
```

## The TAC-4 Mindset

### Remember These Principles

1. **"Your agent is brilliant, but blind"**
   - Always provide complete context
   - Never assume prior knowledge

2. **"Stay out the loop"**
   - Build systems, not solutions
   - Automate decisions, not just actions

3. **"Template your engineering"**
   - Encode patterns, not instances
   - Solve classes of problems, not individual problems

4. **"Fix the system, not the issue"**
   - Errors improve templates
   - Failures improve workflows

5. **"Success is absolutely planned"**
   - Invest in templates upfront
   - ROI compounds over time

## Conclusion

TAC-4 represents a fundamental shift in software development. By mastering the ADW system, you're not just automating coding - you're building self-operating engineering systems that compound in value over time.

The author's urgent message is clear: **"I recommend you take action on this now. Like don't wait, the ROI here is insane."**

This isn't about the future of coding. This is about the present reality that early adopters are already leveraging. The question isn't whether to adopt these systems, but how quickly you can implement them before your competition does.

**Your Next Step**: Create your first GitHub issue, run your first ADW, and experience the paradigm shift from "writing code" to "teaching machines to write code."

Welcome to the age of Agentic Engineering. Stay out the loop. Let your product build itself.
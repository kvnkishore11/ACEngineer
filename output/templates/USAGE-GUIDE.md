# 📘 Template Usage Guide

Complete guide for using the Agentic Engineering templates effectively.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Template Types](#template-types)
3. [Implementation Steps](#implementation-steps)
4. [Real-World Examples](#real-world-examples)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Patterns](#advanced-patterns)

## Getting Started

### Prerequisites
```bash
# Required tools
- Claude CLI or Claude Code
- Git
- Node.js (for JavaScript examples)
- Python 3.8+ (for Python examples)

# Optional but recommended
- Docker (for containerized deployments)
- GitHub CLI (for PR automation)
```

### Initial Setup
```bash
# 1. Clone or download templates
git clone [templates-repo] templates/
cd templates/

# 2. Choose your project type
ls projects/  # View available project scaffolds

# 3. Copy to your workspace
cp -r projects/minimal-agentic-layer/ ~/my-project/
cd ~/my-project/

# 4. Initialize
claude /hello  # Test setup
```

## Template Types

### 1. Agent Templates

#### Purpose
Agents are specialized workers that handle specific types of tasks.

#### Usage Pattern
```bash
# Step 1: Copy agent template
cp templates/agents/implementation-agent.md .claude/agents/my-impl-agent.md

# Step 2: Customize the agent
edit .claude/agents/my-impl-agent.md
# - Change name to "my-impl-agent"
# - Adjust tools list
# - Modify workflow steps
# - Update output format

# Step 3: Use in a command
cat > .claude/commands/build-feature.md << 'EOF'
# Build Feature
Use agent: my-impl-agent
Task: $ARGUMENTS
EOF

# Step 4: Execute
claude /build-feature "Add user authentication"
```

#### Agent Selection Matrix
| Task Type | Recommended Agent | Key Strength |
|-----------|------------------|--------------|
| Investigation | research-agent | Deep analysis, pattern finding |
| Code writing | implementation-agent | Clean code, best practices |
| Quality check | review-agent | Security, performance, standards |
| Coordination | orchestrator-agent | Multi-agent management |
| Domain-specific | specialist-agent | Expert knowledge |

### 2. Command Templates

#### Basic Command Usage
```markdown
# .claude/commands/analyze-deps.md
# Analyze Dependencies

## Task
Analyze all npm dependencies for security and updates.

## Process
1. Read package.json
2. Check each dependency version
3. Identify security issues with `npm audit`
4. Find available updates
5. Generate report

## Output
Markdown report with:
- Security vulnerabilities
- Outdated packages
- Recommended updates
```

#### Workflow Command Example
```markdown
# .claude/commands/complete-feature.md
# Complete Feature Workflow

## Stages

### 1. Research
/agent research-agent "Analyze existing $1 implementation"

### 2. Plan
/agent planning-agent "Design improvements for $1"

### 3. Implement
/agent implementation-agent "Build $1 based on plan"

### 4. Test
/test "$1"

### 5. Review
/agent review-agent "Review $1 implementation"

### 6. Document
/document "$1"

## Usage
/complete-feature "payment processing"
```

### 3. Workflow Templates

#### Simple Sequential Workflow
```yaml
name: code-review-workflow
stages:
  - analyze:
      agent: research-agent
      task: "Analyze code in $PATH"
  - review:
      agent: review-agent
      task: "Review findings"
      depends_on: analyze
  - fix:
      agent: implementation-agent
      task: "Fix identified issues"
      depends_on: review
```

#### Parallel Processing Workflow
```yaml
name: multi-file-processor
stages:
  parallel:
    - process_js:
        agent: implementation-agent
        task: "Process all .js files"
    - process_css:
        agent: style-agent
        task: "Process all .css files"
    - process_tests:
        agent: test-agent
        task: "Update test files"
  merge:
    agent: orchestrator-agent
    task: "Merge all changes"
    depends_on: [process_js, process_css, process_tests]
```

### 4. Skill Templates

#### Defining a Custom Skill
```markdown
---
title: "API Integration"
tags: ["integration", "api", "networking"]
---

# API Integration Skill

## When to Use
- Connecting to external services
- Building API clients
- Handling authentication flows

## Core Workflow
1. Analyze API documentation
2. Design client interface
3. Implement with error handling
4. Add retry logic
5. Create comprehensive tests

## Implementation
[Detailed steps and code examples]
```

## Implementation Steps

### Step 1: Assess Your Needs
```python
# Assessment checklist
needs_assessment = {
    "complexity": "simple|moderate|complex",
    "team_size": 1-50,
    "automation_level": "basic|intermediate|advanced",
    "integration_requirements": ["github", "jira", "slack"],
    "performance_requirements": "low|medium|high"
}

# Based on assessment, choose:
if needs_assessment["complexity"] == "simple":
    start_with = "minimal-agentic-layer"
elif needs_assessment["complexity"] == "moderate":
    start_with = "basic agents + workflow commands"
else:
    start_with = "full orchestration system"
```

### Step 2: Build Incrementally
```bash
# Week 1: Basic setup
cp templates/projects/minimal-agentic-layer/ project/
# Test basic commands

# Week 2: Add specialized agents
cp templates/agents/research-agent.md .claude/agents/
cp templates/agents/implementation-agent.md .claude/agents/
# Test agent interactions

# Week 3: Create workflows
cp templates/workflows/bfc-workflow.yaml .claude/workflows/
# Customize for your process

# Week 4: Add automation
cp templates/commands/pipeline-command.md .claude/commands/
# Connect to CI/CD
```

### Step 3: Customize Templates
```javascript
// Before customization
const template = {
  name: "[PROJECT_NAME]",
  description: "[DESCRIPTION]",
  tasks: ["[TASK_1]", "[TASK_2]"]
};

// After customization
const myProject = {
  name: "E-Commerce Platform",
  description: "Automated development for online store",
  tasks: [
    "Generate product catalog API",
    "Create checkout flow",
    "Implement payment processing"
  ]
};
```

### Step 4: Test Thoroughly
```bash
# Test individual components
claude /test-agent research-agent
claude /test-command workflow-command

# Test integration
claude /run-workflow complete-feature-test

# Test error handling
claude /test-error-recovery

# Performance test
claude /benchmark-workflow
```

### Step 5: Deploy to Production
```yaml
# Production deployment checklist
deployment:
  - backup_existing_system
  - deploy_to_staging
  - run_smoke_tests
  - gradual_rollout:
      - 5% traffic for 1 hour
      - 25% traffic for 4 hours
      - 50% traffic for 12 hours
      - 100% traffic
  - monitor_metrics
  - setup_alerts
```

## Real-World Examples

### Example 1: Automated PR Review System
```bash
# Setup
cp templates/agents/review-agent.md .claude/agents/
cp templates/workflows/bfc-workflow.yaml .claude/workflows/pr-review.yaml

# Customize pr-review.yaml
# - Add security scanning
# - Include performance checks
# - Add style validation

# Create GitHub Action
cat > .github/workflows/auto-review.yml << 'EOF'
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Claude Review
        run: claude /workflow pr-review --pr=${{ github.event.number }}
EOF
```

### Example 2: Documentation Generator
```python
# .claude/commands/generate-docs.md
"""
# Generate Documentation

## Process
1. Scan all source files
2. Extract JSDoc/docstrings
3. Analyze code structure
4. Generate markdown docs
5. Create API reference
6. Build examples

## Implementation
"""

def generate_documentation():
    # Use research-agent to analyze
    analysis = claude.agent("research-agent", "Analyze codebase structure")

    # Use implementation-agent to generate
    docs = claude.agent("implementation-agent", f"Generate docs from {analysis}")

    # Use review-agent to validate
    review = claude.agent("review-agent", f"Review documentation {docs}")

    return docs if review.approved else regenerate(review.feedback)
```

### Example 3: Multi-Agent Feature Development
```yaml
# Complete feature development workflow
workflow:
  name: develop-feature
  input:
    issue_number: 123
    feature_name: "OAuth Integration"

  stages:
    - research:
        parallel:
          - agent: research-agent
            task: "Research OAuth 2.0 best practices"
          - agent: research-agent
            task: "Analyze existing auth system"

    - planning:
        agent: specialist-agent
        task: "Create OAuth implementation plan"
        context: research.outputs

    - implementation:
        parallel:
          - agent: implementation-agent
            task: "Implement OAuth provider"
          - agent: implementation-agent
            task: "Create OAuth middleware"
          - agent: implementation-agent
            task: "Build OAuth UI components"

    - integration:
        agent: orchestrator-agent
        task: "Integrate all OAuth components"

    - testing:
        parallel:
          - unit_tests
          - integration_tests
          - security_tests

    - deployment:
        agent: specialist-agent
        task: "Deploy with feature flags"
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: Agent Not Found
```bash
Error: Agent 'my-agent' not found

# Solution 1: Check file location
ls .claude/agents/

# Solution 2: Verify file extension
# Must be .md

# Solution 3: Check agent name in file
grep "name:" .claude/agents/my-agent.md
```

#### Issue: Workflow Fails Midway
```yaml
# Add recovery mechanisms
error_handling:
  on_failure:
    - save_state
    - rollback_changes
    - notify_team
    - create_debug_log

  recovery:
    - restore_from_checkpoint
    - retry_failed_stage
    - continue_with_manual_intervention
```

#### Issue: Command Not Executing
```bash
# Debug steps
1. Check command file exists
ls .claude/commands/

2. Verify syntax
claude /validate-command my-command

3. Test with simple input
claude /my-command "test"

4. Check logs
cat .claude/logs/commands.log
```

## Advanced Patterns

### Pattern 1: Dynamic Agent Selection
```python
def select_agent(task_type, complexity):
    """Dynamically select best agent for task."""
    agent_matrix = {
        ("analysis", "low"): "basic-agent",
        ("analysis", "high"): "research-agent",
        ("coding", "low"): "basic-agent",
        ("coding", "high"): "implementation-agent",
        ("review", "*"): "review-agent"
    }

    return agent_matrix.get((task_type, complexity), "basic-agent")

# Usage
agent = select_agent("coding", "high")
result = claude.agent(agent, task)
```

### Pattern 2: Conditional Workflows
```yaml
workflow:
  stages:
    - analyze:
        agent: research-agent
        task: "Analyze codebase"

    - decision:
        condition: "analyze.complexity > threshold"
        if_true:
          agent: orchestrator-agent
          task: "Complex refactoring"
        if_false:
          agent: implementation-agent
          task: "Simple fix"
```

### Pattern 3: Learning Loop
```python
class AdaptiveWorkflow:
    def __init__(self):
        self.history = []
        self.optimizations = {}

    def execute(self, task):
        # Learn from history
        similar_tasks = self.find_similar(task)
        if similar_tasks:
            approach = self.best_approach(similar_tasks)
        else:
            approach = self.default_approach()

        # Execute with monitoring
        result = self.run_with_monitoring(approach, task)

        # Store for learning
        self.history.append({
            "task": task,
            "approach": approach,
            "result": result,
            "metrics": self.collect_metrics()
        })

        # Optimize for next time
        self.optimize_approach(task, result)

        return result
```

### Pattern 4: Parallel Pipeline Processing
```python
async def parallel_pipeline(items):
    """Process multiple items through pipeline stages in parallel."""

    # Stage 1: Process all items in parallel
    stage1_results = await asyncio.gather(*[
        process_stage1(item) for item in items
    ])

    # Stage 2: Batch process results
    batches = chunk(stage1_results, batch_size=10)
    stage2_results = []
    for batch in batches:
        results = await asyncio.gather(*[
            process_stage2(item) for item in batch
        ])
        stage2_results.extend(results)

    # Stage 3: Aggregate and finalize
    final_result = await aggregate_results(stage2_results)

    return final_result
```

## Best Practices Summary

### DO ✅
- Start with simple templates and iterate
- Test each component independently
- Document your customizations
- Version control your templates
- Monitor performance metrics
- Implement proper error handling
- Use parallel processing where possible
- Create reusable components

### DON'T ❌
- Over-engineer from the start
- Skip testing phases
- Ignore error cases
- Hardcode sensitive data
- Create overly complex workflows initially
- Forget about rollback strategies
- Neglect documentation
- Skip security considerations

## Next Steps

1. **Choose your starting template** based on complexity needs
2. **Set up your development environment** with the minimal scaffold
3. **Customize one component** at a time
4. **Test thoroughly** before moving to the next component
5. **Document your customizations** for team members
6. **Share your improvements** with the community

Remember: These templates are meant to accelerate your development, not constrain it. Feel free to modify, extend, and improve them based on your specific needs!
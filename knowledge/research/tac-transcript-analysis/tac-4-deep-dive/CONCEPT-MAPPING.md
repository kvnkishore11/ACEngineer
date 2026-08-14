# TAC-4 Concept Mapping: Video to Code

## Overview
This document maps the concepts taught in the TAC-4 video transcripts to their actual implementations in the codebase, showing exactly how the author's spoken teachings translate to production code.

## Core Concept Map

### 1. "Your Agent is Brilliant, But Blind"

#### Video Teaching:
> "With every new session, it starts as a blank instance. Agents are ephemeral, no context, no memories, and no awareness outside of what you give it."

#### Code Implementation:
```python
# adws/agent.py - Fresh agent pattern in action
def execute_template(request: AgentTemplateRequest) -> AgentPromptResponse:
    """Execute a Claude command with a template."""
    # Every execution starts fresh
    template_vars = request.template_variables or {}

    # Agent gets context through template variables
    for key, value in template_vars.items():
        cmd_args.extend(["--arg", f"{key}={value}"])
```

### 2. The PETER Framework (Four Elements of AFK Agents)

#### Video Teaching:
> "The four elements are prompt input, the trigger, you'll need an environment, and then a review system. These four elements can be remembered with Peter."

#### Code Mapping:

**P - Prompt Input**: GitHub Issues
```python
# adws/github.py
def fetch_issue(issue_number: int) -> GitHubIssue:
    """Fetch issue details from GitHub."""
    # Issues become the prompt source
```

**E - Environment**: Agent execution environment
```python
# .env configuration
CLAUDE_CODE_PATH=/usr/local/bin/claude
ANTHROPIC_API_KEY=your-key-here
```

**T - Trigger**: Multiple trigger mechanisms
```python
# adws/trigger_webhook.py - GitHub webhook trigger
# adws/trigger_cron.py - Polling trigger
# adws/adw_plan_build.py - Manual trigger
```

**R - Review**: Pull Request system
```python
# adws/github.py
def create_pull_request(title: str, body: str, branch: str)
```

### 3. The ADW (AI Developer Workflow) Architecture

#### Video Teaching:
> "An ADW is a reusable agentic workflow that combines code, agentic prompts, and agents to deliver results autonomously."

#### Code Structure:
```
adws/
├── adw_plan_build.py      # Main workflow orchestrator
├── agent.py               # Claude CLI integration
├── data_types.py          # Workflow data models
├── github.py              # GitHub operations
└── utils.py               # Support utilities
```

#### Workflow Implementation:
```python
# adws/adw_plan_build.py - The complete workflow
"""
Workflow:
1. Fetch GitHub issue details
2. Create feature branch: feature/issue-{number}-{slug}
3. Plan Agent: Generate implementation plan
4. Build Agent: Implement the solution
5. Create PR with full context
"""
```

### 4. Agent Specialization Pattern

#### Video Teaching:
> "By separating our agents, we're able to isolate the big three context model in prompt to solve one problem and solve one problem well."

#### Code Implementation:
```python
# adws/adw_plan_build.py - Specialized agents
AGENT_PLANNER = "sdlc_planner"
AGENT_IMPLEMENTOR = "sdlc_implementor"
AGENT_CLASSIFIER = "issue_classifier"
AGENT_PLAN_FINDER = "plan_finder"
AGENT_BRANCH_GENERATOR = "branch_generator"
AGENT_PR_CREATOR = "pr_creator"
```

Each agent has a dedicated purpose:
- **issue_classifier**: Determines bug/feature/chore
- **sdlc_planner**: Creates detailed implementation plans
- **sdlc_implementor**: Executes the plans
- **branch_generator**: Creates semantic branch names
- **pr_creator**: Generates comprehensive PRs

### 5. The ADW ID System

#### Video Teaching:
> "It has its own unique ADW ID to identify this AI developer workflow."

#### Code Implementation:
```python
# adws/utils.py
def make_adw_id() -> str:
    """Generate a unique 8-character ADW ID."""
    return str(uuid4())[:8]

# Used throughout the workflow
adw_id = make_adw_id()
logger.info(f"ADW ID: {adw_id}")
```

#### Tracking Structure:
```
agents/
└── [adw_id]/              # Unique per workflow
    ├── issue_classifier/
    ├── sdlc_planner/
    ├── sdlc_implementor/
    └── pr_creator/
```

### 6. Classification-Driven Workflow

#### Video Teaching:
> "We can target specific classes of problems with this switch, right? With this feature inside of our ADW that classifies is this a chore bug feature."

#### Code Implementation:
```python
# .claude/commands/classify_issue.md
def classify_issue(issue: GitHubIssue) -> IssueClassSlashCommand:
    # Returns: bug, feature, or chore

# adws/adw_plan_build.py
if classification == IssueClassSlashCommand.FEATURE:
    slash_command = "/feature"
elif classification == IssueClassSlashCommand.BUG:
    slash_command = "/bug"
else:
    slash_command = "/chore"
```

### 7. Template and Meta-Prompt System

#### Video Teaching:
> "By encoding them into our templates and then chaining our templates, our meta prompts and our reusable prompts together, we get an ADW that can do work like this."

#### Command Structure:
```
.claude/commands/
├── classify_issue.md      # Classification template
├── feature.md             # Feature meta-prompt
├── bug.md                 # Bug meta-prompt
├── chore.md               # Chore meta-prompt
├── implement.md           # Implementation template
└── pull_request.md        # PR creation template
```

### 8. Observability and Logging

#### Video Teaching:
> "It doesn't matter if our agent can solve every problem if we don't know that it's solved. We need to observe, we need to report, we need to log and monitor."

#### Code Implementation:
```python
# adws/utils.py - Comprehensive logging
def setup_logger(name: str, adw_id: str) -> logging.Logger:
    log_dir = Path("logs") / adw_id
    log_dir.mkdir(parents=True, exist_ok=True)

# adws/adw_plan_build.py - GitHub comment reporting
make_issue_comment(
    issue_number,
    f"🤖 **ADW Plan Build Started** (ID: `{adw_id}`)\n"
    f"Creating feature branch and planning implementation..."
)
```

### 9. The Software Development Lifecycle Automation

#### Video Teaching:
> "We'll break down the software development lifecycle into five concrete steps: Plan, code, test, review, document."

#### TAC-4 Focus (Plan & Build):
```python
# Plan Step
def build_plan(issue: GitHubIssue, classification: IssueClassSlashCommand):
    """Plan Agent: Generate implementation plan"""

# Build/Code Step
def build_implementation(plan_file: str):
    """Build Agent: Implement the solution"""
```

### 10. Progressive Error Handling

#### Video Teaching:
> "Every time you miss something, what do you do? You don't fix the issue, you fix the system that caused the issue."

#### Code Pattern:
```python
def check_error(
    result: Union[AgentPromptResponse, subprocess.CompletedProcess],
    step_name: str
) -> None:
    """Check for errors and provide detailed logging."""
    if hasattr(result, "success") and not result.success:
        logger.error(f"Error in {step_name}")
        make_issue_comment(issue_number, f"❌ Error in {step_name}")
        sys.exit(1)
```

## Concept Evolution from TAC-3 to TAC-4

### TAC-3 Concepts Still Present:
1. **Templates**: `.claude/commands/` directory
2. **Meta-prompts**: `/feature`, `/bug`, `/chore`
3. **Fresh Agent Pattern**: Each execution starts clean
4. **Slash Commands**: Core interaction method

### New TAC-4 Concepts:
1. **ADW System**: Complete workflow orchestration
2. **GitHub Integration**: Direct issue/PR integration
3. **Multi-Agent Pipeline**: Specialized agent chain
4. **ADW ID Tracking**: Unique workflow identification
5. **Trigger Mechanisms**: Webhook, cron, manual
6. **Environment Isolation**: Dedicated agent environments

## Hidden Implementation Details

### 1. Agent Output Management
```python
# Not explicitly mentioned in videos but crucial
agents/[adw_id]/[agent_name]/
├── prompts/           # Input prompts sent
├── raw_output.json    # Structured response
└── raw_output.jsonl   # Streaming output
```

### 2. Model Selection Strategy
```python
# High-complexity tasks use stronger models
model = "claude-3-5-sonnet-latest"  # For implementation
# vs
model = "claude-3-haiku"  # For classification
```

### 3. Git Operations Integration
```python
# Direct git operations within workflow
subprocess.run(["git", "checkout", "-b", branch_name])
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", commit_message])
```

## Key Patterns in Code

### 1. Pipeline Pattern
```python
# Sequential execution with error checking
result = classify_issue(issue)
check_error(result, "classification")

result = generate_plan(issue, classification)
check_error(result, "planning")

result = implement_solution(plan)
check_error(result, "implementation")
```

### 2. Template Variable Pattern
```python
template_vars = {
    "issue_title": issue.title,
    "issue_body": issue.body,
    "issue_number": issue.number,
    "adw_id": adw_id
}
```

### 3. Reporting Pattern
```python
# Every major step reports to GitHub
make_issue_comment(
    issue_number,
    f"✅ **{step_name} Complete**\n{details}"
)
```

## Video Quotes to Code Reality

| Video Quote | Code Reality |
|-------------|--------------|
| "Your agent is brilliant, but blind" | Fresh context via `AgentTemplateRequest` |
| "Stay out the loop" | Autonomous `adw_plan_build.py` execution |
| "Four elements of AFK agents" | Issue→Trigger→Environment→PR |
| "Template your engineering" | `.claude/commands/` directory |
| "ADW ID to identify this workflow" | `make_adw_id()` function |
| "Specialized agents for specific tasks" | 6 distinct agent roles |
| "Observable and understandable" | Comprehensive logging system |

## Conclusion

The TAC-4 codebase is a direct manifestation of the author's teachings. Every concept discussed in the videos has a concrete implementation, often more sophisticated than initially described. The code reveals additional patterns and practices that enhance the core teachings, showing that the author has battle-tested these concepts in production scenarios.

The mapping shows:
- **Theory → Practice**: Every concept has code
- **Simplicity → Sophistication**: Simple ideas, robust implementation
- **Teaching → Production**: Educational examples that actually work
- **Evolution → Revolution**: Building on TAC-1/2/3 to create something new
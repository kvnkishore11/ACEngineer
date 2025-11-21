# Agent Command Template

<!--
Command that delegates work to specialized agents
Place in: .claude/commands/[command-name].md
-->

## Command: [command-name]

Delegate [specific task] to specialized agent for expert handling.

### Agent Selection

```yaml
# Define agent to use based on task
agent_selection:
  default: implementation-agent

  conditions:
    - if: "task contains 'research' or 'analyze'"
      use: research-agent

    - if: "task contains 'review' or 'validate'"
      use: review-agent

    - if: "task contains 'coordinate' or 'multiple'"
      use: orchestrator-agent

    - if: "task requires domain expertise"
      use: specialist-agent
```

### Command Flow

#### Step 1: Parse and Prepare Context
```python
def prepare_agent_context(arguments):
    """
    Prepare comprehensive context for agent.
    """
    context = {
        "task": parse_task(arguments),
        "constraints": extract_constraints(arguments),
        "requirements": identify_requirements(arguments),
        "existing_context": gather_existing_context(),
        "success_criteria": define_success_criteria(arguments)
    }

    # Add relevant files and documentation
    context["files"] = find_relevant_files(context["task"])
    context["documentation"] = locate_documentation(context["task"])

    return context
```

#### Step 2: Invoke Agent
```markdown
## Delegating to Agent

### Task Assignment
**Agent**: [selected-agent]
**Task**: $ARGUMENTS
**Context**:
- Working directory: [pwd]
- Related files: [list]
- Dependencies: [list]
- Constraints: [list]

### Instructions for Agent
1. Analyze the provided task and context
2. Plan your approach
3. Execute the implementation
4. Validate your work
5. Report back with results

### Expected Deliverables
- [Primary output]
- [Secondary outputs]
- [Documentation]
- [Test results]
```

#### Step 3: Monitor Execution
```python
class AgentMonitor:
    """
    Monitor agent execution and handle issues.
    """
    def monitor_agent(self, agent_id, task):
        status = "running"
        start_time = time.now()

        while status == "running":
            # Check agent progress
            progress = self.get_agent_progress(agent_id)

            # Update status display
            self.display_progress(progress)

            # Check for timeout
            if time.now() - start_time > MAX_TIMEOUT:
                self.handle_timeout(agent_id)
                break

            # Check for errors
            if progress.has_error:
                self.handle_error(agent_id, progress.error)
                break

            # Update status
            status = progress.status

        return self.get_agent_results(agent_id)
```

#### Step 4: Process Results
```yaml
result_processing:
  validation:
    - Check completeness
    - Verify quality standards
    - Test functionality
    - Review documentation

  integration:
    - Merge with existing code
    - Update configurations
    - Run integration tests
    - Update documentation

  reporting:
    - Summarize achievements
    - List created artifacts
    - Note any issues
    - Suggest next steps
```

### Agent Interaction Patterns

#### Pattern 1: Simple Delegation
```markdown
# Direct task delegation
/[command-name] "Implement user authentication with JWT"

## Agent receives:
- Clear task description
- Current codebase context
- Success criteria

## Agent returns:
- Implementation files
- Test files
- Documentation
- Status report
```

#### Pattern 2: Guided Delegation
```markdown
# Delegation with specific guidance
/[command-name] "Optimize database queries" \
  --focus="user dashboard" \
  --constraint="maintain backward compatibility" \
  --metric="reduce load time by 50%"

## Agent receives:
- Task with specific focus area
- Clear constraints
- Measurable success metrics

## Agent returns:
- Optimization report
- Modified queries
- Performance benchmarks
- Migration guide
```

#### Pattern 3: Multi-Agent Coordination
```python
def coordinate_multiple_agents(task):
    """
    Coordinate multiple agents for complex tasks.
    """
    # Phase 1: Research
    research_results = invoke_agent(
        "research-agent",
        f"Analyze requirements for {task}"
    )

    # Phase 2: Planning
    plan = invoke_agent(
        "planning-agent",
        f"Create implementation plan based on: {research_results}"
    )

    # Phase 3: Implementation
    implementation = invoke_agent(
        "implementation-agent",
        f"Implement according to plan: {plan}"
    )

    # Phase 4: Review
    review = invoke_agent(
        "review-agent",
        f"Review implementation: {implementation}"
    )

    return {
        "research": research_results,
        "plan": plan,
        "implementation": implementation,
        "review": review
    }
```

### Context Preparation

#### File Context
```bash
# Gather relevant files for agent
find . -type f -name "*.ts" | grep -E "(auth|user)" > relevant_files.txt

# Create context bundle
tar -czf context.tar.gz \
  --files-from=relevant_files.txt \
  README.md \
  package.json \
  tsconfig.json
```

#### Documentation Context
```python
def gather_documentation():
    """
    Collect relevant documentation for agent.
    """
    docs = []

    # API documentation
    if exists("openapi.yaml"):
        docs.append(read_file("openapi.yaml"))

    # Architecture docs
    if exists("docs/architecture.md"):
        docs.append(read_file("docs/architecture.md"))

    # Contributing guidelines
    if exists("CONTRIBUTING.md"):
        docs.append(read_file("CONTRIBUTING.md"))

    return "\n\n".join(docs)
```

#### Historical Context
```sql
-- Gather historical context from previous tasks
SELECT
    task_description,
    agent_used,
    outcome,
    lessons_learned
FROM agent_history
WHERE
    similarity(task_description, :current_task) > 0.7
    OR related_components && :current_components
ORDER BY success_score DESC
LIMIT 5;
```

### Error Handling

```python
class AgentErrorHandler:
    """
    Handle errors during agent execution.
    """
    def handle_agent_error(self, error, agent, task):
        error_type = self.classify_error(error)

        if error_type == "timeout":
            # Agent took too long
            return self.handle_timeout(agent, task)

        elif error_type == "invalid_output":
            # Agent produced invalid results
            return self.retry_with_clarification(agent, task, error)

        elif error_type == "missing_context":
            # Agent needs more information
            additional_context = self.gather_additional_context(error)
            return self.retry_with_context(agent, task, additional_context)

        elif error_type == "capability_mismatch":
            # Wrong agent for the task
            new_agent = self.select_appropriate_agent(task, error)
            return self.delegate_to_new_agent(new_agent, task)

        else:
            # Unknown error
            return self.escalate_to_user(error, agent, task)
```

### Result Validation

```python
def validate_agent_output(output, expected):
    """
    Validate agent output meets requirements.
    """
    validation_results = {
        "valid": True,
        "issues": [],
        "warnings": []
    }

    # Check required files exist
    for file in expected["files"]:
        if not exists(file):
            validation_results["valid"] = False
            validation_results["issues"].append(f"Missing required file: {file}")

    # Run tests if provided
    if expected.get("tests"):
        test_results = run_tests(expected["tests"])
        if not test_results.all_passed:
            validation_results["valid"] = False
            validation_results["issues"].append(f"Tests failed: {test_results.failures}")

    # Check code quality
    if expected.get("quality_checks"):
        quality = check_code_quality(output["files"])
        if quality.score < expected["min_quality_score"]:
            validation_results["warnings"].append(f"Quality score below threshold: {quality.score}")

    return validation_results
```

### Output Format

```markdown
# Agent Command Execution Report

## Command: /[command-name]
## Agent Used: [agent-name]

### Task
[Original task description]

### Execution Summary
- **Status**: ✅ Success / ⚠️ Partial / ❌ Failed
- **Duration**: [time]
- **Agent**: [agent-name]

### Agent Output

#### Created Files
- `src/feature.ts` - Main implementation
- `tests/feature.test.ts` - Test suite
- `docs/feature.md` - Documentation

#### Modifications
- Modified `src/index.ts` - Added feature export
- Updated `README.md` - Added usage examples

#### Validation Results
- ✅ All tests passing
- ✅ Type checking successful
- ✅ Linting passed
- ⚠️ Coverage at 78% (target 80%)

### Agent Recommendations
[Any recommendations from the agent]

### Next Steps
1. [Suggested follow-up action]
2. [Additional testing needed]
3. [Documentation updates]
```

### Advanced Features

#### Agent Chaining
```yaml
# Chain multiple agents for complex workflows
chain:
  - agent: research-agent
    task: "Analyze current authentication system"
    output: research.md

  - agent: specialist-agent
    task: "Design OAuth 2.0 integration"
    input: research.md
    output: design.md

  - agent: implementation-agent
    task: "Implement OAuth 2.0"
    input: design.md
    output: src/oauth/

  - agent: review-agent
    task: "Review OAuth implementation"
    input: src/oauth/
    output: review.md
```

#### Conditional Agent Selection
```python
def select_agent_dynamically(task, context):
    """
    Select the best agent based on task analysis.
    """
    # Analyze task complexity
    complexity = analyze_complexity(task)

    # Check for domain-specific requirements
    domain = identify_domain(task)

    # Consider current system load
    load = get_system_load()

    # Select optimal agent
    if domain in ["security", "auth", "crypto"]:
        return "security-specialist"
    elif complexity > 0.8:
        return "orchestrator-agent"  # Complex task needs orchestration
    elif "research" in task.lower():
        return "research-agent"
    elif load > 0.7:
        return "lightweight-agent"  # Use lighter agent under high load
    else:
        return "implementation-agent"  # Default
```

### Customization Guide

1. **Define Agent Mapping**: Map task types to appropriate agents
2. **Prepare Context**: Determine what context each agent needs
3. **Set Success Criteria**: Define what successful completion looks like
4. **Add Validation**: Specify how to validate agent output
5. **Handle Errors**: Define error recovery strategies
6. **Format Output**: Customize the report format

### Common Use Cases

1. **Feature Development**
   - Research existing code → Plan implementation → Build feature → Review code

2. **Bug Investigation**
   - Analyze bug report → Research codebase → Identify root cause → Implement fix

3. **Performance Optimization**
   - Profile application → Identify bottlenecks → Implement optimizations → Validate improvements

4. **Security Audit**
   - Scan for vulnerabilities → Analyze risks → Implement fixes → Verify security

5. **Documentation Generation**
   - Analyze code → Extract patterns → Generate docs → Review accuracy
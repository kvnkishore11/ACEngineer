---
title: "Workflow Designer"
description: "Design SDLC workflows, ADW pipelines, and orchestration patterns for autonomous development"
tags: ["workflow", "sdlc", "automation", "pipeline", "orchestration"]
---

# Workflow Designer

## Purpose

Design and implement complete development workflows that enable autonomous software development. Create structured processes from simple BFC (Bug/Feature/Chore) patterns to complex ADW (Agentic Development Workflow) pipelines with ZTE (Zero Touch Execution).

## When to Use

- Setting up automated development processes
- Creating CI/CD pipelines with agent integration
- Designing issue-to-PR automation
- Implementing quality gates and review processes
- Building self-documenting development systems
- Orchestrating multi-step development workflows
- Establishing team development standards

## How It Works

### Step 1: Identify Workflow Type

#### BFC Pattern (Bug/Feature/Chore)
Basic workflow classification from TAC-3.

```markdown
## Bug Workflow
1. Reproduce issue
2. Identify root cause
3. Implement fix
4. Add regression test
5. Update documentation

## Feature Workflow
1. Understand requirements
2. Design solution
3. Implement incrementally
4. Add comprehensive tests
5. Document new functionality

## Chore Workflow
1. Identify technical debt
2. Plan refactoring approach
3. Implement improvements
4. Ensure no regressions
5. Update technical docs
```

#### ISO Pattern (Issue/Solution/Output)
Structured problem-solving from TAC-7.

```markdown
## Issue
- Problem statement
- Context and constraints
- Success criteria

## Solution
- Proposed approach
- Implementation plan
- Risk mitigation

## Output
- Deliverables
- Validation method
- Documentation
```

#### ADW Pipeline (Agentic Development Workflow)
Full automation from TAC-4.

```yaml
pipeline:
  trigger: github_issue
  stages:
    - name: planning
      agent: planner-agent
      output: implementation-plan.md

    - name: implementation
      agent: developer-agent
      input: implementation-plan.md
      output: source-code

    - name: testing
      agent: tester-agent
      input: source-code
      output: test-results.json

    - name: review
      agent: reviewer-agent
      inputs: [source-code, test-results.json]
      output: review-report.md

    - name: deployment
      agent: deployer-agent
      condition: review.approved
      output: pull-request
```

### Step 2: Define Workflow Components

#### Triggers
```python
WORKFLOW_TRIGGERS = {
    "issue_created": {
        "source": "github",
        "event": "issues.opened",
        "filter": "label:ready"
    },
    "pr_updated": {
        "source": "github",
        "event": "pull_request.synchronize"
    },
    "schedule": {
        "source": "cron",
        "schedule": "0 0 * * MON"  # Weekly on Monday
    },
    "manual": {
        "source": "api",
        "endpoint": "/workflows/trigger"
    }
}
```

#### Stages
```python
class WorkflowStage:
    def __init__(self, name, agent, inputs=None, outputs=None):
        self.name = name
        self.agent = agent
        self.inputs = inputs or []
        self.outputs = outputs or []
        self.conditions = []

    def add_condition(self, condition):
        """Add execution condition"""
        self.conditions.append(condition)
        return self

    async def execute(self, context):
        """Execute stage with context"""
        if not self.check_conditions(context):
            return {"skipped": True, "reason": "Conditions not met"}

        # Prepare inputs
        stage_inputs = self.gather_inputs(context)

        # Execute agent
        result = await self.agent.execute(stage_inputs)

        # Store outputs
        context[self.name] = result
        return result
```

#### Quality Gates
```python
class QualityGate:
    def __init__(self, name, criteria):
        self.name = name
        self.criteria = criteria

    def evaluate(self, metrics):
        """Check if quality criteria are met"""
        results = {}
        for criterion in self.criteria:
            results[criterion.name] = criterion.check(metrics)

        return {
            "passed": all(results.values()),
            "details": results
        }

# Example quality gates
QUALITY_GATES = {
    "code_quality": QualityGate("Code Quality", [
        Criterion("coverage", lambda m: m["coverage"] >= 80),
        Criterion("complexity", lambda m: m["complexity"] <= 10),
        Criterion("duplication", lambda m: m["duplication"] < 5)
    ]),
    "security": QualityGate("Security", [
        Criterion("vulnerabilities", lambda m: m["high_vulns"] == 0),
        Criterion("secrets", lambda m: m["secrets_found"] == 0)
    ])
}
```

### Step 3: Implement Workflow Patterns

#### Linear Pipeline
```python
class LinearPipeline:
    def __init__(self, stages):
        self.stages = stages

    async def execute(self, initial_context):
        context = initial_context
        results = []

        for stage in self.stages:
            result = await stage.execute(context)
            results.append(result)

            if result.get("failed"):
                break

        return {
            "completed": not any(r.get("failed") for r in results),
            "results": results,
            "final_context": context
        }
```

#### Parallel Execution
```python
class ParallelWorkflow:
    def __init__(self, parallel_stages):
        self.parallel_stages = parallel_stages

    async def execute(self, context):
        tasks = [
            stage.execute(context.copy())
            for stage in self.parallel_stages
        ]

        results = await asyncio.gather(*tasks)

        return {
            "results": results,
            "merged_context": self.merge_contexts(results)
        }
```

#### Conditional Branching
```python
class ConditionalWorkflow:
    def __init__(self):
        self.branches = {}

    def add_branch(self, condition, workflow):
        self.branches[condition] = workflow

    async def execute(self, context):
        for condition, workflow in self.branches.items():
            if condition(context):
                return await workflow.execute(context)

        return {"error": "No matching branch"}
```

#### Loop Pattern
```python
class IterativeWorkflow:
    def __init__(self, stage, max_iterations=10):
        self.stage = stage
        self.max_iterations = max_iterations

    async def execute(self, context):
        iteration = 0
        while iteration < self.max_iterations:
            result = await self.stage.execute(context)

            if result.get("complete"):
                return result

            iteration += 1
            context = result.get("next_context", context)

        return {"error": "Max iterations reached"}
```

### Step 4: Create Workflow Orchestration

```python
class WorkflowOrchestrator:
    def __init__(self):
        self.workflows = {}
        self.running = {}
        self.history = []

    def register_workflow(self, name, workflow):
        """Register a workflow definition"""
        self.workflows[name] = workflow

    async def trigger_workflow(self, name, context):
        """Start workflow execution"""
        if name not in self.workflows:
            raise ValueError(f"Unknown workflow: {name}")

        workflow_id = self.generate_id()
        self.running[workflow_id] = {
            "name": name,
            "started": datetime.now(),
            "status": "running"
        }

        try:
            result = await self.workflows[name].execute(context)
            self.complete_workflow(workflow_id, result)
            return result
        except Exception as e:
            self.fail_workflow(workflow_id, str(e))
            raise

    def get_status(self, workflow_id):
        """Get workflow execution status"""
        if workflow_id in self.running:
            return self.running[workflow_id]
        return self.find_in_history(workflow_id)
```

### Step 5: Implement ZTE (Zero Touch Execution)

```python
class ZTEWorkflow:
    """Zero Touch Execution workflow"""

    def __init__(self):
        self.monitors = []
        self.auto_recovery = True

    async def execute_zte(self, issue):
        """Fully autonomous execution"""
        try:
            # 1. Understand issue
            understanding = await self.understand_issue(issue)

            # 2. Generate plan
            plan = await self.create_plan(understanding)

            # 3. Get approval (optional)
            if self.needs_approval(plan):
                await self.request_approval(plan)

            # 4. Execute plan
            implementation = await self.implement_plan(plan)

            # 5. Validate results
            validation = await self.validate(implementation)

            # 6. Deploy changes
            if validation["passed"]:
                pr = await self.create_pr(implementation)
                await self.merge_when_ready(pr)

            return {"success": True, "pr": pr}

        except Exception as e:
            if self.auto_recovery:
                return await self.recover_from_failure(e)
            raise
```

## Inputs Expected

- **Process Requirements**: What needs to be automated
- **Team Structure**: Roles, permissions, approval requirements
- **Quality Standards**: Testing, coverage, review requirements
- **Integration Points**: GitHub, CI/CD, monitoring systems
- **Compliance Needs**: Audit trails, security requirements

## Outputs Provided

1. **Workflow Definition**
   ```yaml
   workflow:
     name: feature-development
     trigger: issue_labeled
     stages:
       - planning
       - implementation
       - testing
       - review
       - deployment
     quality_gates:
       - code_quality
       - security_scan
     notifications:
       - slack
       - email
   ```

2. **Implementation Code**
   ```python
   # Complete workflow implementation
   - Orchestrator class
   - Stage definitions
   - Agent configurations
   - Quality gate implementations
   ```

3. **Configuration Files**
   ```yaml
   # .github/workflows/agentic.yml
   # .claude/workflows/
   # config/pipelines/
   ```

4. **Documentation**
   - Workflow diagrams
   - Process documentation
   - Runbooks
   - Troubleshooting guides

## Examples

### Example 1: Bug Fix Workflow

```python
class BugFixWorkflow:
    def __init__(self):
        self.stages = [
            ReproduceStage(),
            DiagnoseStage(),
            FixStage(),
            TestStage(),
            ReviewStage(),
            DeployStage()
        ]

    async def execute(self, bug_report):
        context = {"bug": bug_report}

        # Reproduce
        reproduction = await self.stages[0].execute(context)
        if not reproduction["reproducible"]:
            return self.handle_not_reproducible(bug_report)

        # Diagnose
        diagnosis = await self.stages[1].execute(context)
        context["root_cause"] = diagnosis["root_cause"]

        # Fix
        fix = await self.stages[2].execute(context)
        context["changes"] = fix["changes"]

        # Test
        tests = await self.stages[3].execute(context)
        if not tests["passed"]:
            return await self.retry_with_different_approach(context)

        # Review
        review = await self.stages[4].execute(context)
        if review["approved"]:
            # Deploy
            return await self.stages[5].execute(context)

        return {"status": "needs_revision", "feedback": review["feedback"]}
```

### Example 2: Feature Development Pipeline

```yaml
# feature-pipeline.yaml
name: feature-development
description: End-to-end feature development workflow

triggers:
  - type: issue
    labels: [feature, approved]

stages:
  - id: design
    name: Design Phase
    agent: architect-agent
    outputs:
      - design-doc.md
      - api-spec.yaml

  - id: implement
    name: Implementation
    agent: developer-agent
    inputs:
      - design-doc.md
      - api-spec.yaml
    outputs:
      - source-code/
      - unit-tests/

  - id: integrate
    name: Integration
    parallel:
      - agent: frontend-agent
        task: ui-implementation
      - agent: backend-agent
        task: api-implementation

  - id: test
    name: Testing
    sequence:
      - unit-tests
      - integration-tests
      - e2e-tests

  - id: document
    name: Documentation
    agent: doc-agent
    outputs:
      - user-docs/
      - api-docs/
      - changelog.md

quality_gates:
  after_implement:
    - code-coverage: 80%
    - linting: pass
  after_test:
    - all-tests: pass
    - performance: baseline
  after_document:
    - doc-coverage: 100%

notifications:
  on_complete:
    - slack: "#dev-team"
  on_failure:
    - email: "tech-lead@company.com"
```

### Example 3: Multi-Agent SDLC

```python
class SDLCWorkflow:
    """Complete SDLC automation with multiple agents"""

    def __init__(self):
        self.agents = self.initialize_agents()
        self.quality_gates = self.setup_quality_gates()

    def initialize_agents(self):
        return {
            "planner": PlannerAgent(
                prompt="Create detailed implementation plans",
                tools=["github", "jira"]
            ),
            "architect": ArchitectAgent(
                prompt="Design system architecture",
                tools=["diagram", "spec_generator"]
            ),
            "developer": DeveloperAgent(
                prompt="Implement features following best practices",
                tools=["code", "test", "debug"]
            ),
            "reviewer": ReviewerAgent(
                prompt="Review code for quality and standards",
                tools=["linter", "security_scanner"]
            ),
            "tester": TesterAgent(
                prompt="Create and execute comprehensive tests",
                tools=["pytest", "playwright", "k6"]
            ),
            "deployer": DeployerAgent(
                prompt="Deploy safely with rollback capability",
                tools=["kubernetes", "terraform"]
            )
        }

    async def execute_sdlc(self, requirement):
        # Planning Phase
        plan = await self.agents["planner"].create_plan(requirement)
        architecture = await self.agents["architect"].design(plan)

        # Development Phase
        implementation = await self.parallel_development(plan, architecture)

        # Quality Phase
        if not await self.quality_checks(implementation):
            return await self.iterate_on_feedback(implementation)

        # Deployment Phase
        deployment = await self.staged_deployment(implementation)

        return {
            "status": "completed",
            "artifacts": {
                "plan": plan,
                "code": implementation,
                "deployment": deployment
            }
        }

    async def parallel_development(self, plan, architecture):
        """Develop features in parallel"""
        tasks = []
        for feature in plan["features"]:
            task = self.develop_feature(feature, architecture)
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        return self.merge_implementations(results)
```

## Troubleshooting

### Workflow Deadlocks
```python
class DeadlockDetector:
    def detect_circular_dependencies(self, workflow):
        """Detect circular dependencies in workflow"""
        graph = self.build_dependency_graph(workflow)
        return self.has_cycle(graph)

    def resolve_deadlock(self, workflow):
        """Break circular dependencies"""
        # Identify cycle
        cycle = self.find_cycle(workflow)
        # Break weakest link
        self.break_dependency(cycle)
```

### Performance Issues
```python
class WorkflowOptimizer:
    def optimize_workflow(self, workflow):
        """Optimize workflow performance"""
        # Identify bottlenecks
        bottlenecks = self.profile_workflow(workflow)

        # Parallelize where possible
        parallel_opportunities = self.find_parallel_opportunities(workflow)

        # Cache repeated operations
        self.add_caching(workflow)

        return self.rebuild_optimized(workflow)
```

### Failed Stage Recovery
```python
class StageRecovery:
    async def recover_failed_stage(self, stage, context, error):
        """Recover from stage failure"""
        if self.is_transient_error(error):
            # Retry with backoff
            return await self.retry_with_backoff(stage, context)

        elif self.can_self_heal(error):
            # Attempt self-healing
            await self.self_heal(error)
            return await stage.execute(context)

        else:
            # Escalate to human
            return await self.escalate_to_human(stage, context, error)
```

## Related Skills

- **Agentic Architect**: Design overall system architecture
- **Agent Builder**: Create agents for workflow stages
- **Testing Strategist**: Design testing workflows
- **Integration Specialist**: Connect workflows to external systems
- **Context Optimizer**: Optimize workflow performance

## Key Principles

1. **Idempotency**: Workflows should be safely re-runnable
2. **Observability**: Every stage should emit metrics and logs
3. **Resilience**: Handle failures gracefully with recovery
4. **Modularity**: Stages should be composable and reusable
5. **Efficiency**: Optimize for parallel execution where possible

---

*This skill synthesizes workflow patterns from TAC-3, TAC-4, and TAC-7, providing comprehensive workflow design capabilities for autonomous development systems.*
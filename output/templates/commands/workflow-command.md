# Workflow Command Template

<!--
Multi-step workflow command that orchestrates a complete process
Place in: .claude/commands/[workflow-name].md
-->

## Workflow: [workflow-name]

Execute a complete [process description] workflow from start to finish.

### Prerequisites

- [ ] [Required condition 1]
- [ ] [Required tool/file]
- [ ] [Environment setup]

### Workflow Phases

#### Phase 1: Initialization and Analysis
```yaml
steps:
  - Validate prerequisites
  - Analyze current state
  - Identify requirements
  - Create execution plan

outputs:
  - analysis-report.md
  - execution-plan.md
```

#### Phase 2: Preparation
```yaml
steps:
  - Set up environment
  - Create necessary directories
  - Initialize configurations
  - Prepare resources

validation:
  - Check all dependencies available
  - Verify configuration correctness
  - Test connectivity/access
```

#### Phase 3: Core Execution
```yaml
parallel_tasks:
  - task_group_1:
      - Generate components
      - Create services
      - Build interfaces

  - task_group_2:
      - Set up database
      - Configure authentication
      - Initialize monitoring

sequential_tasks:
  - Integrate components
  - Run validation tests
  - Apply optimizations
```

#### Phase 4: Validation and Testing
```yaml
testing:
  - Unit tests
  - Integration tests
  - End-to-end tests
  - Performance tests

quality_checks:
  - Code coverage > 80%
  - No critical vulnerabilities
  - Performance benchmarks met
  - Documentation complete
```

#### Phase 5: Finalization
```yaml
finalization:
  - Generate documentation
  - Create deployment artifacts
  - Update configurations
  - Clean up temporary files

reporting:
  - Summary report
  - Metrics dashboard
  - Next steps document
```

### Detailed Implementation

#### Step 1: Initialize Workflow
```bash
# Create workflow directory
mkdir -p .workflow/[workflow-name]
cd .workflow/[workflow-name]

# Set up logging
echo "Starting workflow at $(date)" > workflow.log

# Capture initial state
git status > initial-state.txt
```

#### Step 2: Analyze Requirements
```python
def analyze_requirements():
    """
    Analyze project and determine workflow needs.
    """
    requirements = {
        "components_needed": [],
        "dependencies": [],
        "configurations": [],
        "validations": []
    }

    # Scan project structure
    # Identify missing components
    # Check dependencies
    # Plan execution order

    return requirements
```

#### Step 3: Execute Core Tasks
```typescript
async function executeWorkflow(plan: ExecutionPlan) {
  const results = [];

  // Execute parallel tasks
  const parallelResults = await Promise.all(
    plan.parallelTasks.map(task => executeTask(task))
  );
  results.push(...parallelResults);

  // Execute sequential tasks
  for (const task of plan.sequentialTasks) {
    const result = await executeTask(task);
    results.push(result);

    // Validate after each step
    if (!validateResult(result)) {
      throw new Error(`Task ${task.name} failed validation`);
    }
  }

  return results;
}
```

#### Step 4: Validate Results
```yaml
validation_suite:
  functional:
    - All features working
    - No regression issues
    - Edge cases handled

  non_functional:
    - Performance acceptable
    - Security standards met
    - Accessibility compliant

  documentation:
    - API documented
    - README updated
    - Examples provided
```

### Error Recovery

```python
class WorkflowErrorHandler:
    def handle_error(self, phase, error):
        """
        Handle errors during workflow execution.
        """
        if phase == "initialization":
            # Clean up and retry
            self.cleanup_partial_init()
            return self.retry_init()

        elif phase == "execution":
            # Rollback to checkpoint
            checkpoint = self.get_last_checkpoint()
            self.rollback_to(checkpoint)
            return self.resume_from(checkpoint)

        elif phase == "validation":
            # Identify and fix issues
            issues = self.diagnose_validation_failure(error)
            fixes = self.generate_fixes(issues)
            self.apply_fixes(fixes)
            return self.rerun_validation()

        else:
            # Critical failure
            self.save_debug_info(error)
            self.alert_operator(error)
            raise WorkflowCriticalError(error)
```

### Progress Tracking

```markdown
## Workflow Progress

### Overall Status: 🟡 In Progress (65%)

#### Completed Phases ✅
- [x] Initialization (5 min)
- [x] Analysis (10 min)
- [x] Preparation (8 min)

#### Current Phase 🔄
- [ ] Core Execution (40% complete)
  - [x] Database setup
  - [x] Service generation
  - [ ] Integration (in progress)
  - [ ] Optimization

#### Pending Phases ⏳
- [ ] Validation
- [ ] Finalization

### Metrics
- Files Created: 23
- Tests Passed: 45/50
- Coverage: 82%
- Time Elapsed: 23 minutes
- Estimated Completion: 12 minutes
```

### Output Report Template

```markdown
# Workflow Execution Report

## Summary
- **Workflow**: [workflow-name]
- **Status**: ✅ Success / ⚠️ Partial / ❌ Failed
- **Duration**: [time]
- **Timestamp**: [date/time]

## Phases Completed

### Phase 1: Initialization
- Duration: 5 minutes
- Status: ✅ Success
- Output: initialization.log

### Phase 2: Preparation
- Duration: 8 minutes
- Status: ✅ Success
- Artifacts: configs/, resources/

### Phase 3: Core Execution
- Duration: 25 minutes
- Status: ✅ Success
- Components Created: 15
- Services Deployed: 5

### Phase 4: Validation
- Duration: 10 minutes
- Status: ✅ Success
- Tests Passed: 50/50
- Coverage: 85%

### Phase 5: Finalization
- Duration: 3 minutes
- Status: ✅ Success
- Documentation: docs/

## Artifacts Generated
- Source code: src/
- Tests: tests/
- Documentation: docs/
- Configurations: config/
- Deployment: deploy/

## Metrics
- Total Files: 45
- Lines of Code: 3,250
- Test Coverage: 85%
- Documentation Pages: 12

## Issues and Resolutions
| Issue | Resolution | Impact |
|-------|------------|---------|
| [Issue description] | [How resolved] | [Low/Medium/High] |

## Recommendations
1. [Follow-up action 1]
2. [Follow-up action 2]
3. [Optimization opportunity]

## Next Steps
1. Review generated code
2. Run acceptance tests
3. Deploy to staging
4. Monitor performance
```

### Integration Examples

#### With Version Control
```bash
# Create feature branch
git checkout -b workflow/[workflow-name]

# Execute workflow
/[workflow-name] --target=production

# Commit results
git add .
git commit -m "Complete [workflow-name] workflow"

# Create pull request
gh pr create --title "Workflow: [workflow-name]" --body "$(cat workflow-report.md)"
```

#### With CI/CD
```yaml
# .github/workflows/workflow-command.yml
name: Execute Workflow Command

on:
  workflow_dispatch:
    inputs:
      workflow_name:
        description: 'Workflow to execute'
        required: true
        type: choice
        options:
          - feature-development
          - bug-fix
          - release-preparation

jobs:
  execute:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Execute Workflow
        run: |
          claude-code /[workflow-name] "${{ inputs.workflow_name }}"
      - name: Upload Artifacts
        uses: actions/upload-artifact@v2
        with:
          name: workflow-artifacts
          path: .workflow/
```

### Customization Guide

1. **Define Phases**: Break your workflow into logical phases
2. **Identify Dependencies**: Map out task dependencies
3. **Plan Parallelization**: Identify independent tasks
4. **Add Validation**: Define success criteria for each phase
5. **Include Recovery**: Plan rollback and retry strategies
6. **Track Progress**: Add progress indicators
7. **Generate Reports**: Create comprehensive output

### Common Workflow Patterns

1. **Feature Development Workflow**
   - Requirements → Design → Implementation → Testing → Documentation

2. **Bug Fix Workflow**
   - Reproduce → Analyze → Fix → Test → Verify → Document

3. **Release Workflow**
   - Version → Build → Test → Package → Deploy → Verify

4. **Migration Workflow**
   - Backup → Transform → Validate → Migrate → Verify → Cleanup

5. **Optimization Workflow**
   - Profile → Analyze → Optimize → Benchmark → Validate → Deploy
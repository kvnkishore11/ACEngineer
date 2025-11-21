# Prompt Patterns Library

## The Definitive Collection of Agentic Prompt Patterns

This library contains battle-tested prompt patterns organized by use case, ready to copy and adapt for your needs. Each pattern includes the template, usage guidelines, real examples, and common variations.

---

## Table of Contents

1. [Task-Specific Patterns](#task-specific-patterns)
2. [Structural Patterns](#structural-patterns)
3. [Meta-Prompt Patterns](#meta-prompt-patterns)
4. [Context Engineering Patterns](#context-engineering-patterns)
5. [Tool Integration Patterns](#tool-integration-patterns)
6. [Fresh Agent Handoff Patterns](#fresh-agent-handoff-patterns)
7. [Validation & Testing Patterns](#validation--testing-patterns)
8. [Optimization Patterns](#optimization-patterns)

---

## Task-Specific Patterns

### 1. The Plan Pattern

**Purpose**: Generate structured implementation plans from high-level requirements

**Template**:
```markdown
---
description: Create detailed implementation plan
argument-hint: [requirements]
allowed-tools: Read, Write
model: sonnet
---

# Plan

Create a detailed implementation plan based on the user's requirements.

## Variables
USER_REQUIREMENTS: $1
PLAN_OUTPUT_DIR: ./specs

## Workflow
1. Parse and understand requirements from {{USER_REQUIREMENTS}}
2. Identify key components and dependencies
3. Create implementation phases with clear boundaries
4. For each phase, detail:
   - Specific tasks with acceptance criteria
   - Required files and changes
   - Testing requirements
   - Success metrics
5. Write plan to `{{PLAN_OUTPUT_DIR}}/plan-{timestamp}.md`

## Report
Output the path to the generated plan file
```

**When to Use**:
- Starting new features
- Complex refactoring
- Multi-phase projects

**Real Example**:
```markdown
/plan "Add user authentication with JWT, OAuth2 support for Google/GitHub, and role-based access control"
```

**Variations**:
- `quick-plan`: Rapid 5-minute planning
- `epic-plan`: Multi-sprint planning
- `tech-plan`: Technical architecture planning

**Common Pitfalls**:
- Over-planning small tasks
- Under-specifying acceptance criteria
- Missing dependency identification

---

### 2. The Build Pattern

**Purpose**: Execute implementation plans with validation

**Template**:
```markdown
---
description: Build feature from plan
argument-hint: [plan-file-path]
allowed-tools: Read, Write, Edit, Bash
---

# Build

Follow the plan to implement the feature, then report completion status.

## Variables
PLAN_PATH: $1

## Workflow
1. Read and parse plan at {{PLAN_PATH}}
2. VALIDATE plan structure:
   - IF invalid: Exit with error
3. FOR each task in plan:
   - Implement according to specifications
   - Run inline tests if specified
   - Track completion status
4. Run final validation:
   - Execute test suite
   - Verify acceptance criteria

## Report
```yaml
implementation:
  tasks_completed: <count>
  files_modified: <list>
  tests_passed: <count>/<total>
status: complete|partial|failed
issues: <list of any problems>
```
```

**When to Use**:
- Executing generated plans
- Systematic implementation
- Trackable progress needed

**Real Example**:
```bash
/build ./specs/auth-plan-2024-01-15.md
```

**Variations**:
- `build-safe`: With automatic backups
- `build-parallel`: Multi-file parallel building
- `build-iterative`: With user checkpoints

---

### 3. The Test Pattern

**Purpose**: Comprehensive testing with coverage reporting

**Template**:
```markdown
---
description: Run comprehensive tests
allowed-tools: Bash, Read, Write
---

# Test

Execute all tests and generate coverage report.

## Variables
TEST_FRAMEWORK: pytest
COVERAGE_THRESHOLD: 80

## Workflow
1. Detect testing framework or use {{TEST_FRAMEWORK}}
2. VALIDATE test environment:
   - Check dependencies installed
   - Ensure test files exist
3. Run test suite with coverage:
   ```bash
   {{TEST_FRAMEWORK}} --cov=. --cov-report=term-missing
   ```
4. IF coverage < {{COVERAGE_THRESHOLD}}:
   - Identify uncovered code
   - Suggest additional tests
5. Check for test quality:
   - Edge cases covered
   - Mocking appropriate
   - Assertions meaningful

## Report
- Test results (pass/fail/skip)
- Coverage percentage and gaps
- Performance metrics (execution time)
- Suggested improvements
```

**When to Use**:
- CI/CD pipelines
- Pre-commit validation
- Code review preparation

**Variations**:
- `test-unit`: Unit tests only
- `test-integration`: Integration tests
- `test-performance`: Load and stress testing

---

### 4. The Review Pattern

**Purpose**: Comprehensive code review with actionable feedback

**Template**:
```markdown
---
description: Perform code review
argument-hint: [file-path-or-pr-url]
allowed-tools: Read, Bash, WebSearch
---

# Review

Perform comprehensive code review with actionable feedback.

## Variables
REVIEW_TARGET: $1
REVIEW_DEPTH: thorough  # quick|standard|thorough

## Workflow
1. Load code to review:
   - IF PR URL: Fetch diff
   - ELSE: Read specified files
2. Analyze across dimensions:
   - **Correctness**: Logic errors, edge cases
   - **Performance**: O(n) complexity, bottlenecks
   - **Security**: Vulnerabilities, input validation
   - **Maintainability**: Code clarity, documentation
   - **Style**: Conventions, consistency
3. FOR each issue found:
   - Categorize severity (critical|major|minor|suggestion)
   - Provide specific line numbers
   - Suggest concrete fix
4. Identify positive patterns to reinforce

## Report
```markdown
## Code Review Summary

### Statistics
- Files reviewed: X
- Lines analyzed: Y
- Issues found: Z (Critical: A, Major: B, Minor: C)

### Critical Issues
1. **[Line X]** Security: SQL injection vulnerability
   ```python
   # Current
   query = f"SELECT * FROM users WHERE id = {user_id}"

   # Suggested
   query = "SELECT * FROM users WHERE id = ?"
   cursor.execute(query, (user_id,))
   ```

### Commendations
- Excellent error handling in auth module
- Well-structured test cases
```
```

**When to Use**:
- Pre-merge reviews
- Security audits
- Code quality assessment

**Variations**:
- `review-security`: Security-focused review
- `review-performance`: Performance optimization review
- `review-architecture`: Design pattern review

---

### 5. The Document Pattern

**Purpose**: Generate or update documentation

**Template**:
```markdown
---
description: Generate/update documentation
allowed-tools: Read, Write, Edit
---

# Document

Generate comprehensive documentation for the codebase.

## Variables
DOC_TYPE: $1  # api|readme|tutorial|architecture
OUTPUT_FORMAT: markdown

## Workflow
1. Scan codebase structure and identify key components
2. Based on {{DOC_TYPE}}, generate:
   - API: Extract docstrings, create endpoint documentation
   - README: Project overview, setup, usage
   - Tutorial: Step-by-step guide with examples
   - Architecture: System design, component relationships
3. Include:
   - Code examples with syntax highlighting
   - Diagrams where applicable (mermaid/plantuml)
   - Cross-references to related docs
4. Validate:
   - All code examples run correctly
   - Links are valid
   - Formatting is consistent

## Report
- Documentation generated/updated
- Word count and sections
- Coverage gaps identified
```

**When to Use**:
- New feature completion
- API changes
- Onboarding materials

---

## Structural Patterns

### 6. The REQUEST → VALIDATE → RESOLVE Pattern

**Purpose**: Universal three-phase execution pattern

**Template**:
```markdown
## Workflow

### REQUEST Phase - Understand
1. Parse input parameters
2. Clarify ambiguous requirements
3. Gather necessary context

### VALIDATE Phase - Verify
4. Check prerequisites:
   - Required files exist
   - Dependencies installed
   - Permissions available
5. Validate constraints:
   - Input within bounds
   - Resources sufficient
   - No conflicts detected

### RESOLVE Phase - Execute
6. Execute main logic
7. Verify outputs meet specifications
8. Clean up temporary resources
9. Report results
```

**When to Use**:
- ANY non-trivial prompt
- Production workflows
- Error-prone operations

**Example Implementation**:
```markdown
## Workflow

### REQUEST
1. Parse database migration requirements
2. Identify affected tables and schemas
3. Load current database structure

### VALIDATE
4. Check database connectivity
5. Verify backup exists
6. Validate migration scripts syntax
7. Ensure rollback plan available

### RESOLVE
8. Execute migration in transaction
9. Verify data integrity
10. Update schema version
11. Report migration status
```

---

### 7. The Pipeline Pattern

**Purpose**: Multi-stage processing with intermediate validation

**Template**:
```markdown
## Workflow

### Stage 1: Input Processing
1. Load raw input from {{SOURCE}}
2. Parse and validate format
3. OUTPUT: structured_data.json

### Stage 2: Transformation
4. Read structured_data.json
5. Apply business logic transformations
6. Validate against schema
7. OUTPUT: transformed_data.json

### Stage 3: Integration
8. Read transformed_data.json
9. Merge with existing data
10. Resolve conflicts using {{CONFLICT_STRATEGY}}
11. OUTPUT: final_data.json

### Stage 4: Delivery
12. Read final_data.json
13. Format for target system
14. Deploy to {{DESTINATION}}
15. Verify successful delivery
```

**When to Use**:
- ETL processes
- Data pipelines
- Multi-step workflows

---

### 8. The Fork-Join Pattern

**Purpose**: Parallel processing with result aggregation

**Template**:
```markdown
## Variables
PARALLEL_TASKS: ["analyze", "optimize", "validate"]
WORKER_COUNT: 3

## Workflow

### Fork Phase
1. Divide work into {{WORKER_COUNT}} independent chunks
2. FOR each task in {{PARALLEL_TASKS}}:
   - Spawn dedicated agent
   - Assign specific subtask
   - Set timeout and resources

### Execute Phase (Parallel)
3. Each agent executes independently:
   - Process assigned work
   - Generate results file
   - Report completion status

### Join Phase
4. Wait for all agents (with timeout)
5. Collect all result files
6. Merge results:
   - Resolve any conflicts
   - Aggregate metrics
   - Synthesize insights
7. Generate unified report
```

**When to Use**:
- Large-scale analysis
- Independent subtasks
- Performance optimization

---

## Meta-Prompt Patterns

### 9. The Prompt Generator Pattern

**Purpose**: Create new prompts from high-level descriptions

**Template**:
```markdown
---
description: Generate new agentic prompt
allowed-tools: Write
---

# Generate Prompt

Create a new agentic prompt based on requirements.

## Variables
PROMPT_REQUIREMENTS: $1
PROMPT_LEVEL: $2  # 1-7
OUTPUT_PATH: .claude/commands/

## Template
```markdown
---
description: {{GENERATED_DESCRIPTION}}
allowed-tools: {{IDENTIFIED_TOOLS}}
---

# {{GENERATED_TITLE}}

{{GENERATED_PURPOSE}}

## Variables
{{GENERATED_VARIABLES}}

## Workflow
{{GENERATED_WORKFLOW}}

## Report
{{GENERATED_REPORT_FORMAT}}
```

## Workflow
1. Parse {{PROMPT_REQUIREMENTS}}
2. Determine appropriate level (1-7)
3. Identify required tools
4. Generate sections:
   - Title: Action-oriented verb
   - Purpose: One-sentence with section refs
   - Variables: Dynamic and static
   - Workflow: Numbered steps
   - Report: Output specification
5. Save to {{OUTPUT_PATH}}/generated-prompt.md
```

**When to Use**:
- Scaling prompt creation
- Enforcing standards
- Team consistency

---

### 10. The Template Specialization Pattern

**Purpose**: Create domain-specific prompts from templates

**Template**:
```markdown
## Variables
DOMAIN: $1  # web|mobile|data|ml|devops
BASE_TEMPLATE: $2

## Workflow
1. Load base template from {{BASE_TEMPLATE}}
2. Apply domain-specific modifications:
   - Web: Add SEO, accessibility, responsive checks
   - Mobile: Add performance, battery, offline checks
   - Data: Add validation, integrity, privacy checks
   - ML: Add accuracy, bias, explainability checks
   - DevOps: Add monitoring, scaling, security checks
3. Inject domain-specific:
   - Tools and dependencies
   - Validation criteria
   - Output formats
   - Best practices
4. Generate specialized prompt
```

---

## Context Engineering Patterns

### 11. The Context Priming Pattern

**Purpose**: Prepare agent with essential context before main task

**Template**:
```markdown
## Workflow

### Prime Phase
1. Load codebase structure:
   ```bash
   find . -type f -name "*.py" | head -20
   ```
2. Read key files:
   - README.md for overview
   - requirements.txt for dependencies
   - Main entry point
3. Understand architecture:
   - Identify design patterns
   - Map component relationships
   - Note conventions used

### Execute Phase
4. With context established, proceed with main task
5. Reference primed knowledge throughout execution
```

**When to Use**:
- New codebase work
- Complex modifications
- Architecture-dependent tasks

---

### 12. The Context Preservation Pattern

**Purpose**: Maintain context across agent handoffs

**Template**:
```markdown
## Variables
CONTEXT_FILE: .context/session-{timestamp}.json

## Workflow
1. Before main execution:
   - Load previous context if exists
   - Merge with current understanding

2. During execution:
   - Track key decisions made
   - Document assumptions
   - Note patterns discovered

3. After execution:
   - Serialize context to {{CONTEXT_FILE}}:
     ```json
     {
       "session_id": "...",
       "timestamp": "...",
       "key_files": [...],
       "patterns": {...},
       "decisions": [...],
       "state": {...}
     }
     ```

4. On handoff:
   - New agent loads {{CONTEXT_FILE}}
   - Continues with preserved context
```

---

### 13. The Progressive Context Loading Pattern

**Purpose**: Load context only as needed to optimize tokens

**Template**:
```markdown
## Workflow
1. Start with minimal context:
   - Project name and type
   - Primary objective

2. As needed, progressively load:
   - Level 1: File structure
   - Level 2: Key file contents
   - Level 3: Related documentation
   - Level 4: Historical changes
   - Level 5: External dependencies

3. FOR each decision point:
   - Assess if current context sufficient
   - IF not: Load next level
   - ELSE: Proceed with action

4. Track context usage metrics:
   - Total tokens consumed
   - Context levels accessed
   - Decisions per level
```

---

## Tool Integration Patterns

### 14. The Tool Orchestration Pattern

**Purpose**: Coordinate multiple tools for complex operations

**Template**:
```markdown
## Workflow

### Tool Preparation
1. Inventory required tools:
   - File operations: Read, Write, Edit
   - Execution: Bash
   - Research: WebSearch
   - Analysis: grep, find

### Orchestrated Execution
2. Read phase (Read tool):
   - Gather all input files
   - Parse configurations

3. Analysis phase (Bash + grep):
   ```bash
   grep -r "pattern" --include="*.py"
   find . -type f -exec wc -l {} \;
   ```

4. Modification phase (Edit tool):
   - Apply changes based on analysis
   - Maintain consistency

5. Validation phase (Bash):
   ```bash
   python -m pytest
   python -m black --check .
   ```

6. Documentation phase (Write):
   - Update relevant docs
   - Add changelog entry
```

**When to Use**:
- Complex multi-tool workflows
- Ensuring tool coordination
- Avoiding conflicts

---

### 15. The Tool Fallback Pattern

**Purpose**: Graceful degradation when tools unavailable

**Template**:
```markdown
## Workflow
1. Attempt primary approach:
   TRY:
     - Use specialized MCP tool
   CATCH (tool unavailable):
     - Fallback to Bash equivalent
   CATCH (bash restricted):
     - Fallback to manual instructions

2. Example fallback chain:
   - Primary: mcp_git_tool.commit()
   - Fallback 1: Bash("git commit -m '...'")
   - Fallback 2: Provide git commands for user

3. Report tool usage:
   - Primary tools used
   - Fallbacks triggered
   - Manual steps required
```

---

## Fresh Agent Handoff Patterns

### 16. The Agent Handoff Pattern

**Purpose**: Seamless work transfer between agents

**Template**:
```markdown
## Variables
HANDOFF_FILE: .handoff/state.json
NEXT_AGENT_PROMPT: continue-work.md

## Workflow

### Prepare Handoff
1. Document current state:
   ```json
   {
     "completed_tasks": [...],
     "pending_tasks": [...],
     "blockers": [...],
     "context": {...},
     "next_steps": [...]
   }
   ```

2. Create continuation prompt:
   - Summary of work done
   - Current state description
   - Clear next steps
   - Any warnings or issues

### Execute Handoff
3. Save state to {{HANDOFF_FILE}}
4. Trigger next agent with {{NEXT_AGENT_PROMPT}}

### Verify Handoff
5. New agent confirms:
   - State loaded successfully
   - Understanding of task
   - Ready to continue
```

**When to Use**:
- Long-running tasks
- Shift changes
- Specialized subtasks

---

### 17. The Checkpoint Pattern

**Purpose**: Create resumable checkpoints in workflows

**Template**:
```markdown
## Variables
CHECKPOINT_DIR: .checkpoints/
CHECKPOINT_INTERVAL: 5  # steps

## Workflow
1. Initialize checkpoint system:
   - Create {{CHECKPOINT_DIR}}
   - Set checkpoint counter to 0

2. FOR each major step:
   - Execute step
   - IF step_number % {{CHECKPOINT_INTERVAL}} == 0:
     - Create checkpoint:
       ```bash
       cp -r . {{CHECKPOINT_DIR}}/checkpoint-{step}/
       ```
     - Document state:
       ```json
       {
         "step": N,
         "timestamp": "...",
         "can_resume": true,
         "state": {...}
       }
       ```

3. On failure or interruption:
   - Identify last checkpoint
   - Provide resume instructions
   - Preserve partial work
```

---

## Validation & Testing Patterns

### 18. The Assertion Pattern

**Purpose**: Inline validation throughout workflow

**Template**:
```markdown
## Workflow
1. Setup with assertions:
   ```python
   assert Path(INPUT_FILE).exists(), f"Input file {INPUT_FILE} not found"
   assert THRESHOLD > 0, "Threshold must be positive"
   ```

2. Process with validation:
   - Read data
   - ASSERT: Data format matches schema
   - Transform data
   - ASSERT: No data loss in transformation
   - Write output
   - ASSERT: Output file created and non-empty

3. Final validation:
   ```python
   assert all_tests_pass(), "Tests failed after changes"
   assert metrics_improved(), "Performance degraded"
   ```

## Report
- Assertions passed: X/Y
- Assertion failures (if any) with details
```

---

### 19. The Test Generation Pattern

**Purpose**: Automatically generate comprehensive tests

**Template**:
```markdown
## Variables
TARGET_FILE: $1
TEST_FRAMEWORK: pytest
COVERAGE_TARGET: 90

## Workflow
1. Analyze target code:
   - Identify functions/classes
   - Detect edge cases
   - Find dependencies

2. Generate test structure:
   ```python
   import pytest
   from {{MODULE}} import {{FUNCTIONS}}

   class Test{{ClassName}}:
       def setup_method(self):
           # Setup test fixtures

       def test_happy_path(self):
           # Test normal operation

       def test_edge_cases(self):
           # Test boundaries

       def test_error_handling(self):
           # Test failures
   ```

3. For each function:
   - Generate happy path tests
   - Add edge case tests
   - Include error scenarios
   - Add performance tests if applicable

4. Validate generated tests:
   - Run test suite
   - Check coverage >= {{COVERAGE_TARGET}}
   - Ensure no test interdependencies
```

---

## Optimization Patterns

### 20. The Performance Optimization Pattern

**Purpose**: Systematic performance improvement

**Template**:
```markdown
## Variables
OPTIMIZATION_TARGET: $1  # speed|memory|tokens
BASELINE_METRICS: .metrics/baseline.json

## Workflow

### Measure Baseline
1. Profile current implementation:
   ```bash
   python -m cProfile -o profile.stats main.py
   time python main.py
   ```
2. Save metrics to {{BASELINE_METRICS}}

### Identify Bottlenecks
3. Analyze profile data:
   - Find hotspots (>10% time)
   - Identify memory leaks
   - Detect inefficient algorithms

### Apply Optimizations
4. FOR each bottleneck (ordered by impact):
   - Document current implementation
   - Apply optimization technique:
     * Algorithm: O(n²) → O(n log n)
     * Caching: Add memoization
     * Parallelism: Use multiprocessing
     * Data structures: List → Set for lookups
   - Measure improvement
   - IF improvement < 10%:
     - Revert change

### Validate Results
5. Run full test suite
6. Compare against baseline:
   - Speed improvement: X%
   - Memory reduction: Y%
   - Token usage: Z%
```

---

### 21. The Token Optimization Pattern

**Purpose**: Minimize token usage while maintaining quality

**Template**:
```markdown
## Variables
TOKEN_BUDGET: 4000
CONCISENESS_LEVEL: balanced  # verbose|balanced|concise

## Workflow
1. Analyze token usage:
   - Count current tokens
   - Identify verbose sections
   - Find redundancies

2. Apply compression techniques:
   - Use abbreviations for common terms
   - Reference previous definitions
   - Batch similar operations
   - Use concise syntax:
     ```python
     # Verbose
     for item in items:
         if item > threshold:
             results.append(item)

     # Concise
     results = [i for i in items if i > threshold]
     ```

3. Optimize output format:
   - Use structured data (JSON/YAML)
   - Avoid repetitive text
   - Summary + details pattern

4. Validate quality maintained:
   - All requirements met
   - No information loss
   - Clear and actionable
```

---

### 22. The Batch Processing Pattern

**Purpose**: Efficiently process multiple items

**Template**:
```markdown
## Variables
BATCH_SIZE: 10
ITEMS: $1  # List or directory

## Workflow
1. Prepare batches:
   - Chunk {{ITEMS}} into groups of {{BATCH_SIZE}}
   - Create work queue

2. Process batches:
   ```python
   for batch in batches:
       # Process all items in batch simultaneously
       results = parallel_process(batch)

       # Validate batch results
       assert all(validate(r) for r in results)

       # Save intermediate results
       save_checkpoint(batch_num, results)
   ```

3. Aggregate results:
   - Combine all batch outputs
   - Resolve any conflicts
   - Generate summary statistics

## Report
- Total items processed: X
- Batches completed: Y
- Average time per batch: Z seconds
- Success rate: %
```

---

## Usage Guidelines

### Selecting the Right Pattern

1. **Identify your primary need**:
   - Task execution → Task-Specific Patterns
   - Workflow structure → Structural Patterns
   - Prompt creation → Meta-Prompt Patterns
   - Performance → Optimization Patterns

2. **Consider complexity**:
   - Simple task → Level 1-2 patterns
   - Control flow → Level 3 patterns
   - Multi-agent → Level 4+ patterns

3. **Match skills to patterns**:
   - Beginner → Start with Plan, Build, Test
   - Intermediate → Add Pipeline, Fork-Join
   - Advanced → Meta-prompts, Optimizations

### Combining Patterns

Patterns can be composed for complex workflows:

```markdown
## Workflow
# Use Context Priming Pattern
1. Prime agent with codebase knowledge

# Use Fork-Join Pattern
2. Spawn 3 parallel agents for:
   - Code analysis
   - Test generation
   - Documentation

# Use Pipeline Pattern
3. Pipeline results through:
   - Validation stage
   - Integration stage
   - Deployment stage

# Use Checkpoint Pattern
4. Create resumable checkpoint before deployment
```

### Pattern Evolution

Start simple and evolve:

1. **Version 1**: Basic workflow
```markdown
## Workflow
1. Read file
2. Process data
3. Write output
```

2. **Version 2**: Add validation
```markdown
## Workflow
1. VALIDATE: Input file exists
2. Read file
3. Process data
4. ASSERT: Output valid
5. Write output
```

3. **Version 3**: Add error handling
```markdown
## Workflow
1. TRY:
   - Validate and read input
   - Process data
   - Write output
2. CATCH errors:
   - Log error details
   - Attempt recovery
   - Report failure gracefully
```

### Anti-Patterns to Avoid

❌ **Pattern Overload**: Using too many patterns in one prompt
❌ **Premature Optimization**: Optimizing before establishing baseline
❌ **Missing Validation**: No assertions or checks
❌ **Unbounded Loops**: Loops without exit conditions
❌ **Tool Assumptions**: Assuming tools always available
❌ **Context Overflow**: Loading entire codebase unnecessarily

---

## Quick Reference Card

### Essential Patterns by Frequency of Use

| Pattern | Use Frequency | Skill Level | Impact |
|---------|--------------|-------------|---------|
| Workflow | Daily | Beginner | High |
| REQUEST→VALIDATE→RESOLVE | Daily | Beginner | High |
| Plan-Build-Test | Daily | Intermediate | Very High |
| Context Priming | Weekly | Intermediate | High |
| Fork-Join | Weekly | Advanced | Very High |
| Meta-Prompt | Monthly | Expert | Extreme |
| Pipeline | Weekly | Intermediate | High |
| Checkpoint | Weekly | Intermediate | Medium |

### Pattern Selection Matrix

| If You Need To... | Use This Pattern |
|------------------|------------------|
| Start a new feature | Plan Pattern |
| Execute a plan | Build Pattern |
| Ensure quality | Test Pattern |
| Process in parallel | Fork-Join Pattern |
| Generate prompts | Meta-Prompt Pattern |
| Handle failures | Checkpoint Pattern |
| Optimize performance | Performance Pattern |
| Transfer work | Handoff Pattern |
| Validate continuously | Assertion Pattern |

---

## Conclusion

This library provides the foundation patterns for agentic prompt engineering. Master these patterns, combine them creatively, and evolve them for your specific needs. Remember:

1. **Start with simple patterns** and compose them
2. **Consistency trumps cleverness** every time
3. **Validate early and often** to catch issues
4. **Document your patterns** for team reuse
5. **Evolve patterns based on experience**

The patterns here aren't rules—they're starting points. Adapt them, combine them, and create your own. The goal is to build a library of reliable, reusable prompts that multiply your engineering impact through agents.

---

*Next: See IDK-FRAMEWORK.md for mastering Information Dense Keywords*
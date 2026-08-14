# TAC-5: Concept Mapping - Video to Code

## Core Concepts: Transcript → Implementation

### 1. The Closed Loop System

#### Video Teaching (Video 27-30)
> "Notice the structure of this simple closed loop prompt. We have our request, we have our validation and then we have our resolution."

#### Code Implementation
**Location**: `.claude/commands/bug.md`, `.claude/commands/feature.md`

```markdown
## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `cd app/server && uv run pytest`
- `cd app/client && bun tsc --noEmit`
- `cd app/client && bun run build`
```

**Pattern**: Request → Validate → Resolve

### 2. Always Add Feedback Loops

#### Video Teaching (Video 7, 15, 38)
> "The lesson five tactic is always add feedback loops. Your work, my work, any engineer's work is useless unless it's tested."

#### Code Implementation
**Location**: `adws/adw_test.py`

```python
# Maximum number of test retry attempts after resolution
MAX_TEST_RETRY_ATTEMPTS = 4
MAX_E2E_TEST_RETRY_ATTEMPTS = 2

def run_tests_with_resolution():
    for iteration in range(max_iterations):
        result = run_tests()
        if result.passed:
            break
        fix_failures(result.failures)
```

### 3. Playwright Browser Automation

#### Video Teaching (Video 41-44)
> "Browser control is another tool that you can use to validate work... If you haven't played with this yet, if you're not aware of this, this is huge."

#### Code Implementation
**Location**: `.claude/commands/test_e2e.md`

```markdown
## Instructions
- Initialize Playwright browser in headed mode for visibility
- Use the `application_url`
- Allow time for async operations and element visibility
- Capture screenshots as specified
```

**MCP Server Integration**: Enables browser control for E2E testing

### 4. Screenshot Documentation

#### Video Teaching (Video 45-47)
> "We have two screenshots saved... you can see a real snapshot of our codebase."

#### Code Implementation
**Location**: Screenshot directory structure

```
agents/<adw_id>/<agent_name>/img/<test_name>/
├── 01_initial_page.png
├── 02_query_input.png
├── 03_results_display.png
└── 04_error_state.png
```

### 5. Test Resolution Agents

#### Video Teaching (Video 73, 85-86)
> "We're looping through all the failed tests and kicking off individual agents to resolve the failed test."

#### Code Implementation
**Location**: `adws/adw_test.py`

```python
def resolve_failed_tests(failures):
    for test in failures:
        execute_template(
            template_path=".claude/commands/resolve_failed_test.md",
            test_failure=test
        )
```

### 6. Testing as Rule of Law

#### Video Teaching (Video 34-35)
> "What's more important, the code or your tests? The answer should be your tests. Your tests should be the rule of law in your codebase."

#### Code Implementation
**Location**: Meta-prompt integration in `.claude/commands/bug.md`

```markdown
## Step by Step Tasks
<Your last step should be running the `Validation Commands` to validate the bug is fixed with zero regressions.>
```

### 7. E2E Test Structure

#### Video Teaching (Video 69, 87-89)
> "Our closed loop prompt, you can see we have clean user store here that describes what we're testing exactly."

#### Code Implementation
**Location**: `.claude/commands/e2e/test_basic_query.md`

```markdown
## User Story
As a user I want to query my data using natural language

## Test Steps
1. Navigate to the Application URL
2. **Verify** the page title
3. Enter query
4. **Verify** results

## Success Criteria
- Query input accepts text
- Results display correctly
```

### 8. Fresh Agent Principle

#### Video Teaching (Video 70-71)
> "Always run fresh agents is a good practice and it moves you toward true off device Agentic coding."

#### Code Implementation
**Location**: ADW architecture design

Each agent starts with:
- New context window
- Clean state
- Specific task focus

### 9. Templated Testing

#### Video Teaching (Video 52-59)
> "We're templating our engineering into some key reusable prompts into the codebase so that we can solve problems very quickly."

#### Code Implementation
**Location**: `.claude/commands/bug.md` lines 25-29

```markdown
- IMPORTANT: If the bug affects the UI or user interactions:
  - Add a task to create E2E test file
  - Add E2E test validation to Validation Commands
  - Include instruction to read test examples
```

### 10. The Confidence Stack

#### Video Teaching (Video 42-43, 51)
> "We're stacking up. We're increasing the confidence that our agent has done everything to completion without regression."

#### Code Implementation
Progressive validation layers:

1. **Linting**: `ruff check`
2. **Unit Tests**: `pytest`
3. **Type Checking**: `tsc --noEmit`
4. **Build**: `bun run build`
5. **E2E Tests**: Playwright automation

### 11. ADW Test Workflow

#### Video Teaching (Video 78-82)
> "We have this ADW test workflow here. This is going to run a series of prompts."

#### Code Implementation
**Location**: `adws/adw_test.py`

Workflow sequence:
1. Fetch GitHub issue
2. Run application test suite
3. Report results
4. Create commit
5. Push and update PR

### 12. Test Parallelization

#### Video Teaching (Video 85-86)
> "We can parallelize this, we can do a lot of things here with the architecture of our ADW."

#### Code Implementation
**Location**: `adws/adw_modules/workflow_ops.py`

```python
# Parallel test execution capability
for test_file in e2e_tests:
    run_e2e_test(test_file)
```

### 13. Observability & Tracing

#### Video Teaching (Video 95-97)
> "This is the importance of observability and tracing. You wanna know exactly what's going on inside of our code base."

#### Code Implementation
**Location**: Log structure

```
agents/
└── <adw_id>/
    └── <agent_name>/
        ├── logs/
        ├── img/
        └── results.json
```

### 14. The Plan-Build-Test Pipeline

#### Video Teaching (Video 92-93)
> "ADW plan build test. And this is what ran in the beginning."

#### Code Implementation
**Location**: `adws/adw_plan_build_test.py`

Complete SDLC automation:
```python
# Composed workflow
run_plan()
run_build()
run_test()
```

### 15. Error Recovery Philosophy

#### Video Teaching (Video 32-34)
> "Without knowing what we previously did, right, thanks to the context window clearing, it fixed this issue."

#### Code Implementation
**Location**: `.claude/commands/resolve_failed_test.md`

Self-healing pattern:
1. Analyze failure
2. Fix root cause
3. Re-run tests
4. Confirm resolution

## Hidden Patterns: Video-Only Insights

### 1. The "Think Hard" Keyword
**Video 73-74**:
> "I have think hard. the Claude Code, Anthropic, Encoded Information Dense Keyword."

Not obvious in code - activates Claude's thinking mode.

### 2. The In-Loop Limitation
**Video 71-72**:
> "This is one limitation of in loop Agentic coding. You're pretty much limited one agent."

Explains why ADW architecture uses isolated agents.

### 3. The Meta Testing
**Video 92**:
> "We're getting really meta now."

ADW tests testing the testing system itself.

### 4. Database Reset Importance
**Video Teaching**: Emphasized multiple times
**Code**: `scripts/reset_db.sh` called before each test run

### 5. Port Management
**Video 26**: Shows real-world debugging of port conflicts
**Code**: Handled in startup scripts

## Progression from Previous TAC Modules

### TAC-1 → TAC-5: Programmable Prompts Evolution
- **TAC-1**: Basic prompts
- **TAC-5**: Closed-loop prompts with validation

### TAC-2 → TAC-5: Leverage Points Implementation
- **TAC-2**: Identified 12 leverage points
- **TAC-5**: Testing as highest leverage point

### TAC-3 → TAC-5: Template Enhancement
- **TAC-3**: Meta-prompts for planning
- **TAC-5**: Meta-prompts with embedded testing

### TAC-4 → TAC-5: ADW Maturation
- **TAC-4**: Basic ADW pipeline
- **TAC-5**: ADW with test resolution loops

## Key Implementation Files

### Core Testing Infrastructure
1. `adws/adw_test.py` - Main test orchestrator
2. `.claude/commands/test.md` - Unit test runner
3. `.claude/commands/test_e2e.md` - E2E test executor
4. `.claude/commands/resolve_failed_test.md` - Failure resolver
5. `.claude/commands/resolve_failed_e2e_test.md` - E2E failure resolver

### E2E Test Specifications
1. `.claude/commands/e2e/test_basic_query.md`
2. `.claude/commands/e2e/test_complex_query.md`
3. `.claude/commands/e2e/test_sql_injection.md`

### Meta-Prompt Integration
1. `.claude/commands/bug.md` - Bug fixing with tests
2. `.claude/commands/feature.md` - Feature building with tests

### ADW Components
1. `adws/adw_modules/` - Reusable workflow components
2. `adws/adw_tests/` - Test specifications
3. `adws/adw_triggers/` - Workflow triggers

## The Complete Picture

The code implements everything the author teaches, but the video provides:
1. **The "why" behind decisions**
2. **The philosophy driving the architecture**
3. **Real-world debugging examples**
4. **Progressive teaching methodology**
5. **Passionate conviction about testing importance**

The combination of video + code reveals:
- **Testing isn't optional** - it's the core of agentic development
- **Feedback loops multiply value** with each agent execution
- **Fresh contexts prevent contamination** between agent runs
- **Templates embed best practices** automatically
- **ADW orchestrates everything** into a self-operating system
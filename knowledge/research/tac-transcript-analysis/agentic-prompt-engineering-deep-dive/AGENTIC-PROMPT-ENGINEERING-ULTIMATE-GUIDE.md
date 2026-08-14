# Agentic Prompt Engineering - The Ultimate Guide

## Executive Summary: The Prompt Is THE Fundamental Unit

In the age of agents, **the prompt is THE fundamental unit of engineering**. This isn't hyperbole—it's the new reality. Every prompt you write now has the ability to generate tens or hundreds of hours of productive work through tool calls that run for minutes to hours. One well-crafted prompt becomes a force multiplier. One bad prompt compounds failure at the same rate.

This guide teaches you the definitive framework for engineering prompts specifically for autonomous agents, not humans. You'll learn to write prompts for three audiences: yourself, your team, and most importantly, your agents.

---

## The Paradigm Shift: From Human to Agent Prompting

### The Old Way: Human Prompting
```markdown
"Please write a Python function that calculates the factorial of a number"
```
- **Audience**: Human reader
- **Tone**: Polite, conversational
- **Structure**: Loose, flexible
- **Execution**: Single response
- **Impact**: One-time text generation

### The New Way: Agentic Prompting
```markdown
# Build Factorial Calculator

Execute the `Workflow` to implement a factorial calculator, then `Report` the results.

## Workflow
1. Create `factorial.py` with iterative and recursive implementations
2. Add comprehensive docstrings and type hints
3. Create `test_factorial.py` with edge cases
4. Run tests and verify 100% coverage
5. Generate performance comparison report

## Report
- Implementation details (lines of code, complexity)
- Test coverage metrics
- Performance comparison (time/space complexity)
```
- **Audience**: Agent executor
- **Tone**: Direct, imperative
- **Structure**: Rigid, sectioned
- **Execution**: Multi-step workflow with tool calls
- **Impact**: Hours of autonomous work

### The Stakeholder Trifecta

When engineering agentic prompts, you're writing for three distinct audiences:

1. **You** - Quick understanding when revisiting
2. **Your Team** - Clear communication of intent
3. **Your Agents** - Unambiguous execution instructions

> "The winners here are building libraries of reusable, battle-tested agentic prompts with composable sections that work like Lego blocks."

---

## Core Principles of Agentic Prompt Engineering

### Principle 1: Consistency Beats Complexity
```
Consistency is the greatest weapon against confusion for both you and your agent.
```

Every prompt should follow the same structural pattern. When an engineer opens any prompt in your library, they should immediately recognize:
- Where variables are defined
- Where the workflow begins
- How output is formatted

### Principle 2: The Three-Step Pattern
Every agentic prompt follows INPUT → WORKFLOW → OUTPUT:

```markdown
## Variables          # INPUT - What comes in
USER_REQUEST: $1

## Workflow          # WORK - What the agent does
1. Parse request
2. Execute tasks
3. Validate results

## Report            # OUTPUT - What comes out
- Summary of changes
- Metrics and statistics
```

### Principle 3: Direct Communication
Agentic prompts use imperative, direct language:

**Bad (Human-style):**
```
"Could you please analyze the codebase and perhaps identify some potential issues?"
```

**Good (Agent-style):**
```
"Execute the workflow to analyze the codebase and identify all critical issues."
```

### Principle 4: Composable Sections
Prompts are built from swappable, optional sections:
- Use only what you need
- Each section has a specific purpose
- Sections can be mixed and matched

### Principle 5: Information Dense Keywords (IDKs)
Certain keywords carry special weight with agents:

- **IMPORTANT**: Elevates priority
- **CRITICAL**: Maximum attention required
- **EXCLUSIVE**: Ignore everything else
- **ALWAYS/NEVER**: Absolute constraints

---

## The 7 Levels of Agentic Prompt Formats

### Level 1: High Level Prompt
**Purpose**: Static, reusable, ad-hoc prompts for simple tasks

**Structure**:
```markdown
# Title

High-level description of what to do

## Purpose (optional)
One-line clarification of intent
```

**Example**: `.claude/commands/all_tools.md`
```markdown
# All Tools

Look at your system prompt and list all of your tools

## Purpose
List all available tools from the system prompt
```

**When to Use**:
- One-off tasks
- Simple queries
- Quick utilities

**Skill Tier**: D (Easy)
**Usefulness Tier**: C (Moderate)

---

### Level 2: Workflow Prompt ⭐
**Purpose**: Sequential workflow with input→work→output structure

**Structure**:
```markdown
---
description: Brief description
---

# Title

## Purpose
Execute the `Workflow` and `Report` sections to accomplish X

## Variables
DYNAMIC_VAR: $1
STATIC_VAR: /fixed/path

## Workflow
1. Step one with clear action
2. Step two with tool usage
3. Step three with validation

## Report
- Format for output
- Required information
```

**Example**: `.claude/commands/prime.md`
```markdown
---
description: Gain a general understanding of the codebase
---

# Prime

Execute the `Workflow` and `Report` sections to understand the codebase

## Workflow
1. Run `git ls-files` to list all files
2. Read `README.md` for overview

## Report
Summarize your understanding of the codebase
```

**When to Use**:
- Most common format (80% of prompts)
- Multi-step processes
- Reusable workflows

**Skill Tier**: C (Moderate)
**Usefulness Tier**: S (Essential) ⭐

---

### Level 3: Control Flow Prompt
**Purpose**: Adds conditions and loops to workflows

**Structure**:
```markdown
## Workflow
1. Check condition
   - IF condition: take action A
   - ELSE: take action B
2. LOOP for each item:
   - Process item
   - Validate result
3. Continue workflow
```

**Example**: `.claude/commands/create_image.md`
```markdown
## Variables
PROMPT_FILE: $1
NUM_IMAGES: $2

## Workflow
1. Read prompt file
2. IF file not found:
   - Exit with error message
3. IMPORTANT: Generate {{NUM_IMAGES}} following the loop:
   <image_loop>
   - Call image generation API
   - Save to output directory
   - Log generation details
   </image_loop>
```

**When to Use**:
- Dynamic workflows
- Batch processing
- Conditional execution

**Skill Tier**: B (Advanced)
**Usefulness Tier**: A (Very High)

---

### Level 4: Delegate Prompt
**Purpose**: Orchestrates multiple agents for parallel work

**Structure**:
```markdown
## Variables
AGENT_COUNT: 5
AGENT_MODEL: sonnet
AGENT_TOOLS: Read, Write, WebSearch

## Workflow
1. Parse requirements
2. Design agent prompts
   - Create self-contained prompts
   - Define clear output expectations
3. Launch {{AGENT_COUNT}} parallel agents
4. Collect and summarize results
```

**Example**: `.claude/commands/parallel_subagents.md`

**When to Use**:
- Parallel processing
- Diverse perspectives needed
- Large-scale operations

**Skill Tier**: A (Expert)
**Usefulness Tier**: S (Essential for scale)

---

### Level 5: Higher Order Prompt
**Purpose**: Accepts other prompts as input for dynamic execution

**Structure**:
```markdown
## Variables
PATH_TO_PROMPT: $1

## Workflow
1. Read prompt at {{PATH_TO_PROMPT}}
2. Parse prompt structure
3. Execute embedded workflow
4. Report according to prompt specification
```

**Example**: `.claude/commands/build.md`

**When to Use**:
- Executing generated plans
- Dynamic workflow execution
- Prompt composition

**Skill Tier**: A (Expert)
**Usefulness Tier**: B (Specialized)

---

### Level 6: Template Metaprompt
**Purpose**: Generates other prompts in specific formats

**Structure**:
```markdown
## Variables
HIGH_LEVEL_REQUEST: $1

## Template
```markdown
---
allowed-tools: <tools>
description: <description>
---

# <Title>

<Purpose referencing sections>

## Variables
<DYNAMIC_VAR>: $1
<STATIC_VAR>: value

## Workflow
<numbered steps>

## Report
<output format>
```

## Workflow
1. Parse high-level request
2. Generate prompt using template
3. Save to .claude/commands/
```

**Example**: `.claude/commands/t_metaprompt_workflow.md`

**When to Use**:
- Scaling prompt creation
- Enforcing standards
- Team consistency

**Skill Tier**: S (Master)
**Usefulness Tier**: S (Game-changing) ⭐

---

### Level 7: Self-Improving Prompt
**Purpose**: Prompts that update themselves based on experience

**Structure**:
```markdown
## Expertise
<!-- Dynamic section updated by agent -->
- Pattern: X leads to Y
- Optimization: Use A instead of B
- Domain knowledge: Accumulated insights

## Workflow
1. Execute main task
2. Analyze outcomes
3. Update expertise section
4. Document learnings
```

**Example**: `.claude/commands/experts/cc_hook_expert/`

**When to Use**:
- Domain specialization
- Continuous improvement
- Knowledge accumulation

**Skill Tier**: S (Master)
**Usefulness Tier**: A (Powerful but rare)

---

## Anatomy of Great Agentic Prompts

### Essential Sections

#### 1. Metadata (YAML Frontmatter)
```yaml
---
description: Quick identifier for the prompt
allowed-tools: Read, Write, Edit, Bash
argument-hint: [file-path] [output-format]
model: sonnet
---
```
- Controls agent configuration
- Restricts tool access for safety
- Provides UI hints

#### 2. Title
```markdown
# Build Feature
```
- Action-oriented verb
- Clear, specific
- 2-4 words maximum

#### 3. Purpose
```markdown
Execute the `Workflow` and `Report` sections to implement the feature specified in the plan
```
- One sentence
- References key sections
- Direct, imperative tone

#### 4. Variables
```markdown
## Variables
# Dynamic (from user)
USER_REQUEST: $1
FILE_PATH: $2

# Static (fixed values)
OUTPUT_DIR: ./output
MODEL: claude-3-opus
MAX_RETRIES: 3
```
- Dynamic variables use $1, $2, or $ARGUMENTS
- Static variables are constants
- Reference with {{VARIABLE_NAME}}

#### 5. Workflow
```markdown
## Workflow
1. **Initialize**: Set up environment
   - Create output directory
   - Validate prerequisites

2. **Process**: Execute main logic
   - Read input files
   - Transform data
   - Generate output

3. **Validate**: Ensure quality
   - Run tests
   - Check output format
   - Log metrics
```
- Numbered steps (required)
- Nested bullets for details
- Tool calls explicitly stated
- Variables referenced with {{}}

#### 6. Report
```markdown
## Report
Generate summary in this format:
```yaml
status: success/failure
metrics:
  files_changed: <count>
  lines_added: <count>
  tests_passed: <count>
results:
  - file: <path>
    changes: <description>
```
```
- Defines output structure
- Can specify JSON/YAML/Markdown
- Controls agent response format

### Optional Sections

#### 7. Instructions
```markdown
## Instructions
- IMPORTANT: Always validate input before processing
- Use error handling for all file operations
- Prefer explicit over implicit
```
- Auxiliary guidelines
- Constraints and preferences
- Best practices

#### 8. Relevant Files
```markdown
## Relevant Files
- `src/main.py`: Entry point
- `config/settings.yaml`: Configuration
- `tests/`: Test directory
```
- Quick reference for agent
- Reduces search time
- Improves accuracy

#### 9. Codebase Structure
```markdown
## Codebase Structure
```
project/
├── src/           # Source code
│   ├── main.py    # Entry point
│   └── utils/     # Utilities
├── tests/         # Test files
└── docs/          # Documentation
```
```
- Visual map for navigation
- Context without reading
- Speeds up execution

#### 10. Examples
```markdown
## Examples
Input: "Create user authentication"
Output:
- Created `auth.py` with JWT implementation
- Added tests in `test_auth.py`
- Updated `requirements.txt`
```
- Shows expected behavior
- Clarifies edge cases
- Improves consistency

#### 11. Documentation
```markdown
## Documentation
- API Reference: https://docs.example.com/api
- Style Guide: ./docs/style-guide.md
```
- External resources
- Links for agent to fetch
- Reference materials

#### 12. Template
```markdown
## Template
```python
class {{CLASS_NAME}}:
    """{{DESCRIPTION}}"""

    def __init__(self):
        {{INITIALIZATION}}
```
```
- Boilerplate structures
- Consistent formatting
- Fill-in-the-blank patterns

#### 13. Expertise
```markdown
## Expertise
<!-- Updated by agent through experience -->
- In this codebase, always use pytest for testing
- The API expects ISO 8601 date formats
- Performance bottleneck is in the data transformation layer
```
- Accumulated knowledge
- Self-updating section
- Domain-specific insights

---

## Information Dense Keywords (IDKs)

### What Are IDKs?

Information Dense Keywords are specific words that carry disproportionate weight in agent processing. They act as signal amplifiers, directing agent attention and behavior.

### Core IDKs and Their Effects

#### Priority Modifiers
- **IMPORTANT**: 2x attention weight
- **CRITICAL**: 3x attention weight, may override other instructions
- **ESSENTIAL**: Must be completed for success
- **OPTIONAL**: Can be skipped if issues arise

#### Constraint Keywords
- **ALWAYS**: Absolute requirement, no exceptions
- **NEVER**: Absolute prohibition, no exceptions
- **MUST**: Strong requirement (slightly softer than ALWAYS)
- **SHOULD**: Strong preference but not absolute
- **MAY**: Permission granted but not required

#### Scope Limiters
- **ONLY**: Exclusive focus, ignore everything else
- **EXCLUSIVELY**: Even stronger than ONLY
- **SPECIFICALLY**: Narrow interpretation required
- **EXACTLY**: Precise match required, no variation

#### Action Intensifiers
- **IMMEDIATELY**: Do this first, before anything else
- **CAREFULLY**: Increase validation and error checking
- **THOROUGHLY**: Comprehensive execution required
- **QUICKLY**: Optimize for speed over perfection

### IDK Stacking Patterns

```markdown
## Workflow
1. CRITICAL: IMMEDIATELY validate all inputs
2. IMPORTANT: CAREFULLY process each file
3. ALWAYS run tests after EVERY change
```

### Creating Custom IDKs

You can establish custom IDKs within your prompts:

```markdown
## Instructions
- When you see VALIDATE, always run the test suite
- SAFEGUARD means create a backup before proceeding
- TURBO indicates parallel processing is allowed
```

---

## Prompt Optimization Framework

### The REQUEST → VALIDATE → RESOLVE Pattern

Every robust agentic prompt follows this macro pattern:

```markdown
## Workflow
# REQUEST Phase
1. Parse input parameters
2. Understand requirements
3. Gather necessary context

# VALIDATE Phase
4. Check prerequisites
5. Validate inputs
6. Ensure tools available

# RESOLVE Phase
7. Execute main logic
8. Verify outputs
9. Report results
```

### Performance Optimization Techniques

#### 1. Minimize Tool Calls
```markdown
## Workflow
# Bad: Multiple searches
1. Search for Python files
2. Search for test files
3. Search for config files

# Good: Single comprehensive search
1. Run `find . -type f \( -name "*.py" -o -name "*.yaml" -o -name "*test*" \)`
```

#### 2. Batch Operations
```markdown
## Workflow
# Bad: Individual file operations
1. Read file1.py
2. Read file2.py
3. Read file3.py

# Good: Batch reading
1. Read all Python files in src/ directory simultaneously
```

#### 3. Early Validation
```markdown
## Workflow
1. IMMEDIATELY check if required files exist
   - IF missing: Exit with clear error
2. Proceed with main workflow
```

#### 4. Progressive Enhancement
```markdown
## Workflow
1. Implement basic functionality
2. IF basic tests pass:
   - Add advanced features
3. ELSE:
   - Fix basic issues first
```

### Token Economics

#### Verbose vs Concise Prompting

**Verbose (Development)**:
```markdown
## Workflow
1. First, navigate to the source directory
2. Then, list all Python files to understand structure
3. Next, read the main.py file completely
4. After that, analyze the code for issues
```

**Concise (Production)**:
```markdown
## Workflow
1. Analyze src/main.py for issues
```

#### Output Control
```markdown
## Report
# Token-Heavy
Provide detailed analysis including:
- Full code snippets
- Line-by-line explanation
- Alternative implementations

# Token-Light
Summary only:
- Issue count
- Critical fixes needed
- One-line per change
```

---

## Testing and Validation

### Prompt Testing Checklist

#### Functional Testing
- [ ] Does the prompt execute without errors?
- [ ] Are all variables properly referenced?
- [ ] Do conditional branches work correctly?
- [ ] Are loops bounded and terminating?

#### Output Testing
- [ ] Is the report format consistent?
- [ ] Are success/failure cases handled?
- [ ] Is the output deterministic enough?

#### Edge Case Testing
- [ ] Missing variables handled gracefully?
- [ ] Empty inputs processed correctly?
- [ ] Large inputs don't cause timeouts?
- [ ] Parallel execution conflicts resolved?

### Validation Patterns

```markdown
## Workflow
1. Validate inputs
   ```python
   assert PATH_TO_FILE.exists(), "File not found"
   assert MODEL in ['sonnet', 'opus'], "Invalid model"
   ```

2. Execute with validation
   - Run main logic
   - IMPORTANT: Capture any errors

3. Validate outputs
   - Ensure all expected files created
   - Verify format matches specification
   - Check metrics are within bounds
```

---

## Common Mistakes and Antipatterns

### Antipattern 1: Human Politeness
❌ **Wrong**:
```markdown
Could you please analyze the codebase when you have a chance?
```

✅ **Right**:
```markdown
Analyze the codebase following the workflow below.
```

### Antipattern 2: Ambiguous Instructions
❌ **Wrong**:
```markdown
Process the files appropriately
```

✅ **Right**:
```markdown
Process each .py file: lint, format with black, add type hints
```

### Antipattern 3: Missing Structure
❌ **Wrong**:
```markdown
Build the feature described in the plan and make sure it works
```

✅ **Right**:
```markdown
## Workflow
1. Read plan.md
2. Implement features listed in section 2
3. Add tests for each feature
4. Run test suite and verify passing
```

### Antipattern 4: Unbounded Loops
❌ **Wrong**:
```markdown
Keep improving the code until it's perfect
```

✅ **Right**:
```markdown
Run optimization loop (MAX 3 iterations):
1. Analyze performance metrics
2. IF improvement < 10%: exit loop
3. Apply optimization
```

### Antipattern 5: Over-Engineering
❌ **Wrong**:
```markdown
## Variables
VAR1: value1
VAR2: value2
... (20 more rarely-used variables)
```

✅ **Right**:
```markdown
## Variables
ESSENTIAL_VAR: $1
# Add other variables only when needed
```

### Antipattern 6: Implicit Expectations
❌ **Wrong**:
```markdown
Update the configuration
```

✅ **Right**:
```markdown
Update config.yaml:
- Set debug: false
- Update api_endpoint to production URL
- Increment version number
```

---

## Integration with TAC Workflows

### From TAC-1: Programmable Prompts
```python
# Execute agentic prompts programmatically
import subprocess

def execute_prompt(prompt_name, *args):
    cmd = ["claude", f"/claude/commands/{prompt_name}.md"] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout
```

### From TAC-3: Meta-Prompt Generation
```markdown
# Meta-prompt that generates workflow prompts
## Template
Create a Level 2 Workflow Prompt with:
- Variables section for inputs
- 5-step workflow
- Structured YAML report
```

### From TAC-7: Multi-Agent Orchestration
```markdown
## Workflow
1. Generate 3 specialized prompts using template
2. Launch parallel agents with each prompt
3. Aggregate results
4. Synthesize final output
```

### From Elite Context Engineering
```markdown
## Workflow
1. Prime context with codebase structure
2. Load relevant documentation
3. Execute main workflow with rich context
4. Preserve context for next agent
```

---

## Advanced Techniques

### Technique 1: Prompt Chaining
```markdown
## Workflow
1. Execute /prime to understand codebase
2. Run /plan to generate implementation plan
3. Execute /build with generated plan
4. Run /test to validate implementation
5. Execute /document to update docs
```

### Technique 2: Conditional Delegation
```markdown
## Workflow
1. Analyze task complexity
2. IF complexity > threshold:
   - Spawn 5 specialized agents
   - Distribute subtasks
3. ELSE:
   - Execute locally
```

### Technique 3: Progressive Context Building
```markdown
## Workflow
1. Start with minimal context
2. FOR each step:
   - Execute task
   - IF more context needed:
     - Load specific files
     - Update working knowledge
3. Preserve enriched context
```

### Technique 4: Self-Healing Workflows
```markdown
## Workflow
1. Execute main task
2. IF error occurs:
   - Analyze error type
   - Apply appropriate fix:
     - Missing dep: install
     - Syntax error: fix and retry
     - Logic error: rollback and try alternative
3. Maximum 3 self-heal attempts
```

### Technique 5: Parallel Exploration
```markdown
## Variables
APPROACHES: ["functional", "object-oriented", "hybrid"]

## Workflow
1. PARALLEL for each approach in {{APPROACHES}}:
   - Generate implementation
   - Run benchmarks
   - Calculate metrics
2. Compare results
3. Select optimal approach
```

---

## Implementation Checklist

### Before Writing Any Prompt
- [ ] Is this a repeating task? (If yes, create prompt)
- [ ] What level of prompt is needed? (1-7)
- [ ] Who is the audience? (You/Team/Agent)
- [ ] What tools are required?

### Prompt Structure Checklist
- [ ] Clear, action-verb title
- [ ] One-sentence purpose with section references
- [ ] All variables defined (dynamic first, static second)
- [ ] Numbered workflow steps
- [ ] Report format specified
- [ ] Only necessary sections included

### Quality Checklist
- [ ] Would a coworker understand this?
- [ ] Are all IDKs intentional and necessary?
- [ ] Can this be tested deterministically?
- [ ] Are edge cases handled?
- [ ] Is the tone direct and imperative?

### Optimization Checklist
- [ ] Minimal tool calls?
- [ ] Batched operations where possible?
- [ ] Early validation implemented?
- [ ] Token usage optimized?
- [ ] Parallel execution where beneficial?

---

## Key Takeaways

### The 10 Commandments of Agentic Prompt Engineering

1. **The prompt is THE fundamental unit of engineering**
2. **Write for the trifecta**: You, Your Team, Your Agents
3. **Consistency beats complexity** every time
4. **Follow INPUT → WORKFLOW → OUTPUT** religiously
5. **Use direct, imperative language** (no politeness)
6. **Master Level 2 (Workflow)** before advancing
7. **Level 6 (Template Metaprompt)** is your force multiplier
8. **Only include sections you need** (composability)
9. **IDKs are powerful** - use them intentionally
10. **Test your prompts** like you test your code

### The Path to Mastery

1. **Start**: Write Level 1 prompts for repeated tasks
2. **Foundation**: Master Level 2 workflow prompts (80% of needs)
3. **Expand**: Add control flow (Level 3) for dynamic workflows
4. **Scale**: Delegate to multiple agents (Level 4)
5. **Compose**: Build higher-order systems (Level 5)
6. **Accelerate**: Generate prompts with templates (Level 6)
7. **Transcend**: Create self-improving systems (Level 7)

### Your Next Actions

1. **Inventory your repeated tasks** - What do you do 3+ times?
2. **Create your first Level 2 workflow prompt** today
3. **Build a prompt library** in `.claude/commands/`
4. **Establish team conventions** for prompt structure
5. **Create a template metaprompt** for your domain
6. **Share your prompts** - They're reusable assets
7. **Measure the multiplier** - Track hours saved

---

## Remember: The Future Belongs to Prompt Engineers

> "Every prompt you write, every line that goes into your prompt has the ability to call tens and hundreds of tool calls and run from minutes to hours. This makes agentic prompt engineering one of the most important skills for engineers to focus on and master."

The engineers who master agentic prompt engineering won't just be more productive - they'll operate at a fundamentally different level. They'll command armies of agents, orchestrate complex systems, and build solutions that would take traditional engineers months in mere hours.

**The prompt is no longer just text. It's executable specification. It's distributed computation. It's the future of engineering.**

Master it, and you master the age of agents.

---

*End of Ultimate Guide*

*Next: See PROMPT-PATTERNS-LIBRARY.md for ready-to-use templates*
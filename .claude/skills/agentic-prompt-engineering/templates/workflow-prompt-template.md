# Workflow Prompt Template (Level 2)

**Use this template for 80% of your prompts. It's the workhorse format.**

```markdown
---
description: [Brief one-line description of what this does]
argument-hint: [optional-arg-name]
allowed-tools: Read, Write, Edit, Bash  # Customize as needed
model: sonnet  # or opus, haiku
---

# [Command Name]

[One paragraph explaining what this command does and when to use it]

## Purpose
Execute the `Workflow` and `Report` sections to [accomplish specific goal]

## Variables
[REQUIRED_INPUT]: $1  # First argument
[OPTIONAL_INPUT]: $2  # Second argument (if needed)
[STATIC_PATH]: ./path/to/resource
[CONFIG_VALUE]: default_value

## Workflow
1. [First clear, actionable step]
   - [Sub-step if needed]
   - [Another sub-step]
2. [Second step with tool usage]
   ```bash
   # Example command if relevant
   command --flag value
   ```
3. VALIDATE [what you're checking]:
   - IF [condition]: [action]
   - ELSE: [alternative action]
4. [Continue with remaining steps]
5. [Final step - often validation or reporting]

## Report
[Specify exact output format]

**Format**:
```[language if code]
[Structure the agent should output]
```

**Must Include**:
- [Required element 1]
- [Required element 2]
- [Required element 3]

## Error Handling (optional but recommended)
- IF [error type]: [recovery action]
- IF [error type]: [recovery action]
- IF unrecoverable: [escalation procedure]

## Examples (optional but recommended)
### Example 1: [Scenario]
```bash
/command-name arg1 arg2
```
Expected output: [what the report should look like]
```

---

## Filling Out the Template

### Description (YAML frontmatter)
**Purpose**: Shows up in command list, helps with discovery
**Guidelines**:
- Keep under 60 characters
- Be specific about what it does
- Example: "Generate implementation plan from requirements"

### Title
**Purpose**: The command name users will type
**Guidelines**:
- Use kebab-case for multi-word commands: `create-feature`, `run-tests`
- Be concise but clear
- Example: `# Plan`, `# Build`, `# Test`

### Purpose Section
**Purpose**: High-level goal and scope
**Guidelines**:
- One sentence explaining the transformation: input → output
- Use format: "Execute the `Workflow` and `Report` sections to [goal]"
- Example: "Execute the `Workflow` and `Report` sections to create a comprehensive test suite for the specified module"

### Variables Section
**Purpose**: Define all inputs and configuration
**Guidelines**:
- UPPERCASE for variable names
- Use $1, $2, etc. for command arguments
- Use descriptive names: `USER_INPUT: $1` not `VAR1: $1`
- Include default values where appropriate
- Add inline comments explaining each variable
- Example:
  ```markdown
  ## Variables
  FEATURE_NAME: $1  # The feature to implement
  OUTPUT_DIR: ./specs  # Where to write the plan
  TEMPLATE_PATH: ./.claude/templates/plan.md
  URGENCY: normal  # normal|high|critical
  ```

### Workflow Section (THE CRITICAL PART)
**Purpose**: Step-by-step execution instructions
**Guidelines**:
- **Use numbered lists** (1, 2, 3...) for sequential steps
- **Be specific and actionable** - avoid vague instructions
- **One clear action per step**
- **Use sub-bullets** for details or conditions
- **Include tool calls** where relevant (bash commands, file operations)
- **Add validation steps** after critical operations
- **Use IDKs strategically**: CRITICAL, IMPORTANT, ALWAYS, NEVER
- **Show conditional logic**: IF/ELSE statements
- **Specify loops**: FOR each item, WHILE condition

**Example of good workflow**:
```markdown
## Workflow
1. VALIDATE input requirements:
   - REQUIRED: {{FEATURE_NAME}} is provided
   - REQUIRED: {{OUTPUT_DIR}} exists and is writable
   - IF validation fails: Exit with error message
2. Read existing project structure:
   ```bash
   tree -L 3 -I 'node_modules|.git'
   ```
3. IMPORTANT: Analyze dependencies and constraints:
   - Check for related features
   - Identify affected files
   - Note breaking changes
4. Generate implementation plan with these sections:
   - Overview and objectives
   - File changes required
   - Testing strategy
   - Deployment considerations
5. Write plan to `{{OUTPUT_DIR}}/plan-{{FEATURE_NAME}}.md`
6. CRITICAL: Validate generated plan:
   - All sections present
   - Acceptance criteria defined
   - No placeholder content (TBD, TODO, etc.)
7. IF validation passes: Continue
   ELSE: Regenerate missing sections
```

### Report Section
**Purpose**: Specify exact output format
**Guidelines**:
- **Be explicit about structure** - use code blocks to show format
- **Specify required vs optional fields**
- **Use structured formats**: JSON, YAML, Markdown with specific headers
- **Include examples**
- **Specify what constitutes success vs failure**

**Example of good report**:
```markdown
## Report

Provide a structured summary in the following format:

```yaml
status: success|failure|partial
plan_file: [path to generated file]
features_identified: [count]
estimated_complexity: low|medium|high
dependencies:
  - [dependency 1]
  - [dependency 2]
breaking_changes: yes|no
notes: [any important considerations]
```

REQUIRED fields:
- status (must be one of: success, failure, partial)
- plan_file (absolute path)
- estimated_complexity

OPTIONAL fields:
- notes (additional context)
```

### Error Handling Section (recommended)
**Purpose**: Define failure modes and recovery
**Guidelines**:
- **Anticipate common failures**
- **Specify recovery procedures**
- **Define escalation conditions**
- **Use IF/THEN format**

**Example**:
```markdown
## Error Handling
- IF {{FEATURE_NAME}} is empty or invalid:
  → Exit immediately with error message
  → Suggest valid format
- IF {{OUTPUT_DIR}} doesn't exist:
  → Attempt to create it
  → IF creation fails: exit with permission error
- IF plan generation produces placeholder content:
  → Retry with more specific instructions
  → IF retry fails: return partial plan with warnings
- IF unrecoverable error:
  → Log full context
  → Provide debugging information
  → Suggest next steps for human
```

### Examples Section (recommended)
**Purpose**: Show concrete usage
**Guidelines**:
- **Provide 2-3 real examples**
- **Show command invocation**
- **Show expected output**
- **Cover happy path and edge cases**

**Example**:
```markdown
## Examples

### Example 1: New feature
```bash
/plan "Add user authentication with OAuth2"
```

Expected output:
```yaml
status: success
plan_file: ./specs/plan-user-auth.md
estimated_complexity: high
dependencies:
  - OAuth2 library
  - Session management
breaking_changes: yes
```

### Example 2: Bug fix
```bash
/plan "Fix memory leak in data processor"
```

Expected output:
```yaml
status: success
plan_file: ./specs/plan-memory-leak-fix.md
estimated_complexity: medium
dependencies: []
breaking_changes: no
```
```

---

## Common Patterns

### Pattern: Read → Process → Write
```markdown
## Workflow
1. Read input from {{INPUT_FILE}}
2. Process data:
   - Parse and validate
   - Transform according to rules
   - Verify output meets criteria
3. Write results to {{OUTPUT_FILE}}
4. Validate written file:
   - Verify file exists
   - Check file size > 0
   - Validate format
```

### Pattern: Validate → Execute → Verify
```markdown
## Workflow
1. VALIDATE preconditions:
   - Required files exist
   - Dependencies installed
   - Permissions correct
2. Execute main task:
   - [Core work here]
3. VERIFY results:
   - Check success criteria
   - Run smoke tests
   - Confirm no side effects
```

### Pattern: Parallel Execution
```markdown
## Workflow
1. Parse requirements into tasks
2. FOR each task in parallel:
   - Spawn fresh agent with task
   - Execute independently
   - Collect results
3. Aggregate results
4. Validate combined output
```

---

## IDK Placement Guide

**CRITICAL** - Use for:
- Data loss prevention
- Security checks
- Irreversible operations
- System-breaking actions

**IMPORTANT** - Use for:
- Quality requirements
- Performance requirements
- Key validations
- Must-have features

**ALWAYS/NEVER** - Use for:
- Absolute requirements
- Safety constraints
- Security rules
- Non-negotiable standards

**Example with strategic IDK placement**:
```markdown
## Workflow
1. CRITICAL: Create backup before any modifications:
   ```bash
   cp -r {{TARGET_DIR}} {{TARGET_DIR}}.backup
   ```
2. IMPORTANT: Validate input format meets specification:
   - Schema validation
   - Type checking
   - Range validation
3. Execute transformations:
   - NEVER modify files outside {{TARGET_DIR}}
   - ALWAYS preserve original permissions
   - Log every file modification
4. CRITICAL: Verify backup integrity before cleanup:
   - Compare checksums
   - Validate restoration works
   - IF verification fails: STOP and escalate
```

---

## Quick Checklist for Your Prompt

Before saving, verify:
- [ ] Description is clear and under 60 chars
- [ ] Variables section defines all inputs with types
- [ ] Workflow has numbered steps (not bullets)
- [ ] Each step is specific and actionable
- [ ] Validation steps are included
- [ ] Report format is explicit with examples
- [ ] IDKs are used for critical sections
- [ ] Error handling covers common failures
- [ ] At least one example is provided
- [ ] No ambiguous language ("maybe", "try to", "should")
- [ ] No assumed context - everything is explicit

---

## Testing Your Prompt

1. **Create the prompt file**: `.claude/commands/your-command.md`
2. **Test with real input**: `/your-command arg1 arg2`
3. **Verify output matches Report spec**
4. **Test edge cases**: Missing input, invalid input, error conditions
5. **Iterate**: Refine workflow based on actual behavior
6. **Document learnings**: Update prompt with insights

---

**Remember**: This is a **workflow prompt** - it does work and produces results. If you just need information, use Level 1 (High Level) instead.

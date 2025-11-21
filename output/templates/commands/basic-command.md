# Basic Command Template

<!--
This is a simple command template for Claude Code (.claude/commands/[name].md)
Commands are triggered with /[name] and can accept arguments
-->

## Command: [name]

[Brief description of what this command does]

### Instructions

1. [First step - typically reading or analyzing something]
2. [Second step - processing or transforming]
3. [Third step - producing output or taking action]

### Input

<!-- Define what arguments or context this command expects -->
$ARGUMENTS

<!-- Or use specific placeholders -->
- Target: $1
- Options: $2

### Process

<!-- Describe the detailed process -->

1. **Analyze Input**
   - Validate the provided arguments
   - Extract key information
   - Note any constraints

2. **Execute Task**
   - [Main action to perform]
   - [Secondary actions]
   - [Error handling]

3. **Report Results**
   - Summarize what was done
   - List any created/modified files
   - Note any issues or warnings

### Output Format

<!-- Define expected output structure -->
```markdown
## Summary
[Brief description of what was accomplished]

## Details
- [Specific change or action 1]
- [Specific change or action 2]
- [Files affected]

## Next Steps
- [Any follow-up actions needed]
```

### Examples

<!-- Provide usage examples -->
```bash
# Basic usage
/[name] "parameter"

# With options
/[name] "target" --option=value

# Complex example
/[name] "src/components" --recursive --fix
```

### Error Handling

- If [condition], then [action]
- If unable to [task], explain why and suggest alternatives
- Always provide partial results when possible

### Notes

<!-- Additional context or warnings -->
- This command assumes [precondition]
- Best used when [scenario]
- Not recommended for [anti-pattern]

---

## Customization Points

1. **[name]**: Replace with actual command name
2. **Instructions**: Adapt steps to your specific workflow
3. **Arguments**: Define what inputs are needed
4. **Process**: Detail the specific operations
5. **Output Format**: Customize to your needs

## Common Variations

### Simple Action Command
```markdown
# Execute [action]
Perform the following action: $ARGUMENTS

Report completion with:
- What was done
- Any issues encountered
```

### Analysis Command
```markdown
# Analyze [target]
1. Read and analyze: $ARGUMENTS
2. Identify patterns and issues
3. Generate detailed report with findings and recommendations
```

### Generation Command
```markdown
# Generate [artifact]
Based on: $ARGUMENTS

Create:
1. [Primary output]
2. [Supporting files]
3. [Documentation]

Ensure:
- Follows project conventions
- Includes error handling
- Has appropriate tests
```
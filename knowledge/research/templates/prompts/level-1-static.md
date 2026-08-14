# Level 1: Static Prompts

Basic, fixed prompts that don't change based on context. Suitable for simple, repetitive tasks.

## Template Structure

```markdown
# [Task Name]

[Clear, specific instruction that doesn't change]

## Requirements
- [Fixed requirement 1]
- [Fixed requirement 2]
- [Fixed requirement 3]

## Expected Output
[Exactly what should be produced]
```

## Examples

### Example 1: Code Formatting
```markdown
# Format Code

Format the following code according to standard conventions:
- Use 2 spaces for indentation
- Add semicolons at end of statements
- Use camelCase for variables
- Use PascalCase for classes

Input: [CODE]

Output the formatted version.
```

### Example 2: Simple Analysis
```markdown
# Analyze Dependencies

List all npm packages used in package.json with their versions.

For each package, indicate:
- Current version
- Latest version available
- Whether it's a dev dependency

Format as a markdown table.
```

### Example 3: Data Extraction
```markdown
# Extract Error Messages

Find all error messages in the codebase.

Search for patterns:
- throw new Error(...)
- console.error(...)
- logger.error(...)

List each unique error message with its file location.
```

## Common Static Prompt Patterns

### 1. Transformation Prompts
```markdown
# Transform [Input] to [Output]

Convert the provided [input format] to [output format].

Rules:
- [Transformation rule 1]
- [Transformation rule 2]
- [Transformation rule 3]

Example:
Input: [example input]
Output: [example output]

Now transform: [ACTUAL INPUT]
```

### 2. Validation Prompts
```markdown
# Validate [Target]

Check if [target] meets the following criteria:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

Report:
- Pass/Fail for each criterion
- Overall status
- Any issues found
```

### 3. Generation Prompts
```markdown
# Generate [Artifact]

Create a [artifact type] with these characteristics:
- Property 1: [value]
- Property 2: [value]
- Property 3: [value]

Must include:
- [Required element 1]
- [Required element 2]

Must not include:
- [Forbidden element 1]
- [Forbidden element 2]
```

### 4. Classification Prompts
```markdown
# Classify [Items]

Categorize each item into one of these categories:
1. Category A: [description]
2. Category B: [description]
3. Category C: [description]

Output format:
- Item: [item name]
- Category: [A/B/C]
- Reason: [brief explanation]
```

### 5. Summarization Prompts
```markdown
# Summarize [Document]

Create a summary with:
- Maximum 3 paragraphs
- Focus on [key aspect]
- Include main points about:
  - [Topic 1]
  - [Topic 2]
  - [Topic 3]

Style: [formal/casual/technical]
Length: [word count]
```

## Best Practices for Static Prompts

### 1. Be Specific and Clear
```markdown
# BAD: Fix the code
# GOOD: Fix syntax errors in JavaScript code by adding missing semicolons and closing brackets
```

### 2. Provide Structure
```markdown
# Review Code

Examine the code for:

## 1. Syntax Issues
- Missing semicolons
- Unclosed brackets
- Typos in keywords

## 2. Logic Issues
- Infinite loops
- Null pointer access
- Off-by-one errors

## 3. Style Issues
- Naming conventions
- Indentation
- Comment quality
```

### 3. Include Examples
```markdown
# Convert to Markdown Table

Convert CSV data to markdown table format.

Example:
Input: name,age,city
      John,30,NYC
      Jane,25,LA

Output: | name | age | city |
        |------|-----|------|
        | John | 30  | NYC  |
        | Jane | 25  | LA   |

Now convert: [YOUR_CSV_DATA]
```

### 4. Define Constraints
```markdown
# Generate Test Cases

Create 5 unit tests for the function.

Constraints:
- Each test must be independent
- Include edge cases
- Use Jest syntax
- Maximum 10 lines per test
- Include descriptive test names
```

### 5. Specify Output Format
```markdown
# Analyze Performance

Report format:
```yaml
performance_report:
  metrics:
    load_time: [seconds]
    memory_usage: [MB]
    cpu_usage: [percentage]

  bottlenecks:
    - location: [file:line]
      issue: [description]
      impact: [high/medium/low]

  recommendations:
    - [specific improvement]
```

## Static Prompt Library

### Development Tasks

#### 1. Add Comments
```markdown
Add explanatory comments to complex code sections.
- Add function documentation
- Explain algorithm logic
- Note any assumptions
- Use JSDoc format for functions
```

#### 2. Create README
```markdown
Generate a README.md with:
- Project title and description
- Installation instructions
- Usage examples
- API documentation
- Contributing guidelines
- License information
```

#### 3. Write Tests
```markdown
Create unit tests that:
- Test happy path
- Test error conditions
- Test edge cases
- Mock external dependencies
- Assert expected outcomes
```

### Analysis Tasks

#### 1. Find Duplicates
```markdown
Identify duplicate code blocks.
- Minimum 5 lines to be considered duplicate
- Ignore whitespace differences
- Report location of each duplicate
- Suggest refactoring approach
```

#### 2. Security Scan
```markdown
Check for common security issues:
- Hardcoded credentials
- SQL injection vulnerabilities
- Unvalidated input
- Insecure random generation
- Missing authentication
```

### Documentation Tasks

#### 1. API Documentation
```markdown
Document each endpoint with:
- HTTP method and path
- Request parameters
- Request body schema
- Response format
- Error codes
- Example request/response
```

#### 2. Change Log
```markdown
Create changelog entry:
- Version number
- Release date
- Added features
- Changed functionality
- Deprecated features
- Removed features
- Fixed bugs
- Security updates
```

## When to Use Static Prompts

✅ **Good for:**
- Repetitive tasks with consistent requirements
- Simple transformations
- Basic validations
- Standard formatting
- Fixed classification schemes

❌ **Not suitable for:**
- Context-dependent tasks
- Complex decision making
- Tasks requiring external data
- Adaptive or learning scenarios
- Multi-step workflows with dependencies

## Limitations and Upgrades

### Limitations of Static Prompts
1. No context awareness
2. Can't adapt to variations
3. May produce repetitive output
4. Limited error handling
5. No learning from feedback

### When to Upgrade to Higher Levels

Upgrade to **Level 2 (Input-Based)** when:
- Need to incorporate user input
- Task varies based on parameters
- Require dynamic examples

Upgrade to **Level 3 (Context-Aware)** when:
- Need to reference external files
- Require understanding of system state
- Task depends on environment

Upgrade to **Level 5 (Adaptive)** when:
- Need to learn from previous executions
- Require optimization over time
- Task complexity varies significantly

## Testing Static Prompts

```python
def test_static_prompt(prompt, test_cases):
    """
    Test static prompt consistency.
    """
    results = []
    for test_case in test_cases:
        output = execute_prompt(prompt, test_case['input'])

        # Check output format
        assert matches_format(output, test_case['expected_format'])

        # Check required elements
        for element in test_case['required_elements']:
            assert element in output

        # Check constraints
        assert meets_constraints(output, test_case['constraints'])

        results.append({
            'input': test_case['input'],
            'output': output,
            'passed': True
        })

    return results
```
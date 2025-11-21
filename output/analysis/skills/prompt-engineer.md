---
title: "Prompt Engineer"
description: "Master the 7 levels of prompt engineering from static to self-improving, with meta-prompt creation and optimization"
tags: ["prompts", "engineering", "meta-prompts", "optimization", "delegation"]
---

# Prompt Engineer

## Purpose

Master prompt engineering as a fundamental engineering discipline, progressing through 7 levels from basic static prompts to self-improving meta-prompts. Create prompts that are composable, delegatable, and evolvable - treating them as first-class engineering artifacts.

## When to Use

- Designing new agent behaviors or capabilities
- Optimizing existing prompts for better performance
- Creating reusable prompt templates and libraries
- Building meta-prompts that generate other prompts
- Implementing self-improving prompt systems
- Debugging unexpected agent behaviors

## How It Works

### The 7 Levels of Prompt Engineering

#### Level 1: Static Prompts
Basic, fixed prompts with no variation.

```markdown
You are a helpful assistant. Answer the user's questions accurately and concisely.
```

**Characteristics**:
- Fixed content
- No adaptation
- Single purpose
- Limited reusability

#### Level 2: Prompts as Workflows
Prompts that define step-by-step processes.

```markdown
You are a code reviewer. Follow these steps:

1. Read the provided code
2. Check for syntax errors
3. Evaluate code style and formatting
4. Assess logic and algorithm efficiency
5. Identify security vulnerabilities
6. Suggest improvements
7. Provide a summary with action items

For each step, provide detailed feedback.
```

**Characteristics**:
- Sequential execution
- Predictable flow
- Process-oriented
- Checkpoints and validation

#### Level 3: Control Flow Prompts
Prompts with conditional logic and branching.

```markdown
You are a customer service agent. Analyze the customer's message:

IF the message contains a complaint:
    1. Express empathy
    2. Identify the specific issue
    3. Offer a solution or escalation

ELIF the message is a question:
    1. Identify the topic
    2. Search knowledge base
    3. Provide clear answer with examples

ELIF the message is positive feedback:
    1. Thank the customer
    2. Ask for a review
    3. Offer additional assistance

ELSE:
    1. Clarify the customer's need
    2. Provide relevant options
```

**Characteristics**:
- Conditional logic
- Dynamic responses
- Context-aware decisions
- Multiple execution paths

#### Level 4: Delegator Prompts
Prompts that can spawn and coordinate other agents.

```python
# Orchestrator prompt that delegates to specialists
ORCHESTRATOR_PROMPT = """
You are an orchestrator that delegates tasks to specialized agents.

Available agents:
- researcher: Gathers information and analyzes data
- writer: Creates content and documentation
- coder: Writes and reviews code
- tester: Creates and executes tests

When given a task:
1. Analyze what needs to be done
2. Break it into subtasks
3. Assign each subtask to the appropriate agent
4. Coordinate the execution
5. Synthesize the results

Use this format to delegate:
DELEGATE TO: [agent_name]
TASK: [specific task description]
CONTEXT: [relevant information]
EXPECTED OUTPUT: [what you need back]
"""
```

**Characteristics**:
- Multi-agent coordination
- Task decomposition
- Parallel execution
- Result synthesis

#### Level 5: Higher-Order Prompts
Prompts that accept other prompts as parameters.

```python
# Meta-prompt that modifies other prompts
PROMPT_ENHANCER = """
You are a prompt enhancement system. You will receive a base prompt and enhancement instructions.

Base Prompt: {base_prompt}
Enhancement Type: {enhancement_type}
Parameters: {parameters}

Enhancement Types:
- add_examples: Add relevant examples to the prompt
- add_constraints: Add safety and quality constraints
- add_reasoning: Add chain-of-thought reasoning steps
- add_validation: Add output validation criteria
- optimize_tokens: Reduce token usage while maintaining effectiveness

Generate an enhanced version of the base prompt that incorporates the requested enhancement.
"""

# Usage
enhanced_prompt = generate(PROMPT_ENHANCER, {
    "base_prompt": original_prompt,
    "enhancement_type": "add_reasoning",
    "parameters": {"style": "step_by_step"}
})
```

**Characteristics**:
- Prompt composition
- Dynamic generation
- Reusable transformations
- Prompt algebra

#### Level 6: Prompt Templates
Reusable prompt patterns with variable substitution.

```python
# Advanced template with multiple variables and sections
AGENT_TEMPLATE = """
You are {agent_name}, a specialized {domain} agent.

## Core Responsibilities
{responsibilities}

## Available Tools
{tools_list}

## Behavioral Guidelines
{guidelines}

## Output Format
{output_format}

## Success Criteria
{success_metrics}

## Error Handling
When encountering errors:
{error_protocol}

## Example Interactions
{examples}

Remember: {key_principle}
"""

# Template registry for different agent types
TEMPLATES = {
    "developer": AGENT_TEMPLATE.format(
        agent_name="DevBot",
        domain="software development",
        responsibilities="- Write clean, efficient code\n- Follow best practices\n- Document thoroughly",
        # ... other parameters
    ),
    "analyst": AGENT_TEMPLATE.format(
        agent_name="AnalystBot",
        domain="data analysis",
        responsibilities="- Analyze datasets\n- Generate insights\n- Create visualizations",
        # ... other parameters
    )
}
```

**Characteristics**:
- Parameterized content
- Consistent structure
- Rapid deployment
- Maintainable prompts

#### Level 7: Self-Improving Prompts
Prompts that evolve based on performance feedback.

```python
class SelfImprovingPrompt:
    def __init__(self, base_prompt):
        self.current_prompt = base_prompt
        self.performance_history = []
        self.improvement_prompt = """
        Analyze the performance data and improve the prompt:

        Current Prompt: {current}
        Performance Metrics: {metrics}
        Failed Cases: {failures}
        User Feedback: {feedback}

        Generate an improved version that addresses the issues while maintaining strengths.
        """

    async def execute(self, input):
        result = await llm.complete(self.current_prompt, input)
        return result

    async def improve(self):
        if len(self.performance_history) >= 10:
            # Analyze performance
            metrics = self.calculate_metrics()

            # Generate improved version
            improved = await llm.complete(
                self.improvement_prompt,
                {
                    "current": self.current_prompt,
                    "metrics": metrics,
                    "failures": self.get_failures(),
                    "feedback": self.get_feedback()
                }
            )

            # Test improved version
            if await self.validate_improvement(improved):
                self.current_prompt = improved
                self.version += 1
```

**Characteristics**:
- Performance tracking
- Automatic optimization
- Continuous learning
- Version control

### Advanced Prompt Patterns

#### Chain-of-Thought (CoT)
```markdown
Let's solve this step-by-step:

1. First, I'll identify the key components of the problem
2. Next, I'll analyze the relationships between them
3. Then, I'll formulate a solution approach
4. Finally, I'll implement and validate the solution

[Detailed reasoning for each step follows]
```

#### Few-Shot Learning
```markdown
Here are examples of the task:

Example 1:
Input: [example input]
Output: [example output]
Reasoning: [why this output]

Example 2:
Input: [example input]
Output: [example output]
Reasoning: [why this output]

Now, for your input: {user_input}
```

#### Role-Based Prompting
```markdown
You are an expert {role} with {years} years of experience in {domain}.

Your expertise includes:
- {skill_1}
- {skill_2}
- {skill_3}

Approach this task as you would in a professional setting, considering:
- Industry best practices
- Common pitfalls to avoid
- Long-term implications
```

#### Constraint-Based Prompting
```markdown
Complete this task with the following constraints:

MUST:
- Include specific examples
- Cite sources when making claims
- Provide actionable recommendations

MUST NOT:
- Make assumptions without stating them
- Provide medical/legal/financial advice
- Generate harmful or biased content

Format: {required_format}
Length: {min_words} to {max_words} words
```

## Inputs Expected

- **Task Definition**: Clear description of what the prompt should accomplish
- **Success Criteria**: How to measure prompt effectiveness
- **Constraints**: Limitations, safety requirements, format needs
- **Examples**: Input/output pairs showing desired behavior
- **Context**: Domain knowledge, user expertise level

## Outputs Provided

1. **Optimized Prompt**
   - Complete, production-ready prompt
   - Comments explaining design decisions
   - Version for different complexity levels

2. **Test Suite**
   ```python
   # Prompt validation tests
   test_cases = [
       {"input": "...", "expected": "..."},
       {"input": "...", "should_reject": True},
       # Edge cases, error conditions
   ]
   ```

3. **Performance Metrics**
   ```yaml
   metrics:
     accuracy: 95%
     token_usage: 450 avg
     response_time: 1.2s avg
     user_satisfaction: 4.8/5
   ```

4. **Documentation**
   - Usage guide
   - Parameter descriptions
   - Example interactions
   - Troubleshooting guide

## Examples

### Example 1: Bug Report Analyzer (Level 3 - Control Flow)

```markdown
You are a bug report analyzer. Process the bug report:

1. CLASSIFY the severity:
   - Critical: System crash, data loss, security breach
   - High: Major feature broken, widespread impact
   - Medium: Feature partially working, workaround exists
   - Low: Minor issue, cosmetic problem

2. EXTRACT key information:
   - Affected component
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details

3. IF severity is Critical or High:
   - Generate immediate action plan
   - Identify stakeholders to notify
   - Suggest temporary mitigation

4. SEARCH for similar issues:
   - Check if duplicate
   - Find related bugs
   - Identify patterns

5. OUTPUT structured report:
   ```json
   {
     "severity": "...",
     "component": "...",
     "summary": "...",
     "action_items": [...],
     "related_issues": [...]
   }
   ```
```

### Example 2: Code Generation Meta-Prompt (Level 5 - Higher-Order)

```python
META_CODE_GENERATOR = """
You are a meta-prompt generator for code generation tasks.

Given:
- Language: {language}
- Framework: {framework}
- Task Type: {task_type}
- Complexity: {complexity}

Generate a specialized prompt that will:
1. Understand the specific syntax and idioms of {language}
2. Follow {framework} best practices
3. Include appropriate error handling for {complexity} level
4. Generate code with proper documentation

The prompt should include:
- Role definition for the specific technology stack
- Code quality requirements
- Testing requirements
- Documentation standards
- Example code patterns

Output the complete prompt that another AI can use to generate high-quality {language} code.
"""
```

### Example 3: Self-Improving Customer Service (Level 7)

```python
class EvolvingServicePrompt:
    def __init__(self):
        self.base_prompt = """
        You are a customer service representative.
        Help customers professionally and efficiently.
        """
        self.feedback_analyzer = """
        Based on these customer interactions:
        {interactions}

        Identify:
        1. Common pain points
        2. Successful resolution patterns
        3. Areas needing improvement

        Suggest prompt improvements to address these findings.
        """

    async def evolve(self, interaction_logs):
        # Analyze recent interactions
        analysis = await llm.complete(
            self.feedback_analyzer,
            {"interactions": interaction_logs}
        )

        # Generate improved prompt
        self.base_prompt = await self.improve_prompt(
            self.base_prompt,
            analysis
        )

        # A/B test new version
        await self.ab_test_prompt()
```

## Troubleshooting

### Common Issues and Solutions

1. **Prompt Too Vague**
   ```markdown
   # Bad
   "Help with code"

   # Good
   "You are a Python expert. Review this code for:
   1. Syntax errors
   2. Performance issues
   3. Security vulnerabilities
   Provide specific line numbers and fixes."
   ```

2. **Over-Constrained**
   ```markdown
   # Too rigid - add flexibility
   "IMPORTANT: You have some flexibility in approach while maintaining quality.
   Prioritize these requirements:
   1. [Most important]
   2. [Important]
   3. [Nice to have]"
   ```

3. **Token Inefficiency**
   ```python
   # Optimize token usage
   def compress_prompt(prompt):
       # Remove redundancy
       # Use references instead of repetition
       # Compress examples
       return optimized_prompt
   ```

## Related Skills

- **Agent Builder**: Create agents using your engineered prompts
- **Context Optimizer**: Optimize prompts for context efficiency
- **Workflow Designer**: Design workflows that prompts will execute
- **Testing Strategist**: Test and validate prompt effectiveness
- **Agentic Instructor**: Document and teach prompt patterns

## Key Principles

1. **Clarity Over Cleverness**: Clear, explicit instructions outperform clever tricks
2. **Progressive Refinement**: Start simple, add complexity as needed
3. **Test-Driven Prompting**: Define success criteria before writing prompts
4. **Version Control**: Track prompt versions and performance
5. **Composability**: Design prompts that can be combined and reused

## Advanced Techniques

### Prompt Chaining
```python
# Chain multiple prompts for complex tasks
async def chain_prompts(prompts, initial_input):
    result = initial_input
    for prompt in prompts:
        result = await llm.complete(prompt, result)
    return result
```

### Prompt Fusion
```python
# Combine multiple prompts into one
def fuse_prompts(prompts, weights=None):
    if weights is None:
        weights = [1.0] * len(prompts)

    fused = "Consider these perspectives:\n\n"
    for prompt, weight in zip(prompts, weights):
        fused += f"[Weight: {weight}]\n{prompt}\n\n"

    fused += "Synthesize these into a balanced response."
    return fused
```

### Adaptive Prompting
```python
# Adjust prompt based on context
def adapt_prompt(base_prompt, context):
    if context["expertise"] == "beginner":
        base_prompt += "\nExplain concepts simply with examples."
    elif context["expertise"] == "expert":
        base_prompt += "\nProvide technical details and edge cases."

    if context["time_constraint"]:
        base_prompt += "\nBe concise, focus on essentials."

    return base_prompt
```

---

*This skill synthesizes the complete "Agentic Prompt Engineering" module from the Agentic Horizon course, providing a comprehensive framework for prompt engineering mastery.*
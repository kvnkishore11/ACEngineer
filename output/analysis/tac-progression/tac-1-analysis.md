# TAC-1 Analysis: Foundation and Introduction

## Overview
TAC-1 establishes the fundamental distinction between traditional "AI Coding" and the new paradigm of "Agentic Coding." This module introduces the concept of programmable prompts and demonstrates how Claude can be invoked programmatically to execute structured tasks with specific permissions.

## Structure
```
tac-1/
├── .claude/
│   └── settings.json     # Permission configuration
├── programmable/
│   ├── programmable.py   # Python script to invoke Claude
│   ├── programmable.sh   # Shell script variant
│   ├── programmable.ts   # TypeScript variant
│   └── prompt.md         # The actual prompt template
├── .env.sample           # Environment variable template
└── README.md            # Module documentation
```

## Key Concepts

### 1. **AI Coding vs Agentic Coding**
The module demonstrates the philosophical shift:
- **AI Coding**: Simple command execution (e.g., "print goodbye ai coding")
- **Agentic Coding**: Multi-step workflows with git operations, file creation, and automated execution

### 2. **Permission Model**
The `.claude/settings.json` introduces controlled tool access:
```json
{
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Bash(uv run:*)",
      "Bash(git checkout:*)",
      "Bash(git branch:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "WebSearch"
    ]
  }
}
```

This granular permission system ensures Claude only performs authorized actions, establishing security boundaries from the start.

### 3. **Programmable Prompts**
The `programmable/prompt.md` file demonstrates structured task definition:
- RUN directives for command execution
- CREATE directives for file generation
- REPORT directives for output verification

### 4. **Multiple Invocation Methods**
Three implementation approaches are provided:
- Python using subprocess
- Shell script using direct CLI invocation
- TypeScript using Bun runtime

## Code Patterns

### Prompt Execution Pattern
```python
def main():
    with open("programmable/prompt.md", "r") as f:
        prompt_content = f.read()

    command = ["claude", "-p", prompt_content]
    result = subprocess.run(command, capture_output=True, text=True)
```

This pattern establishes:
1. External prompt storage (separation of concerns)
2. Programmatic invocation of Claude CLI
3. Structured output handling

## Evolution
TAC-1 lays the groundwork for:
- Structured command execution
- Permission-based security model
- Programmable AI interactions
- Multi-step workflow automation

## Author Insights

### Design Philosophy
1. **Explicit over Implicit**: Every action must be explicitly permitted
2. **Structured Communication**: Use markdown-based DSL for clear task definition
3. **Tool Agnosticism**: Support multiple programming languages for invocation
4. **Workflow Thinking**: Move from single commands to complete workflows

### Pedagogical Approach
The author starts with a minimal viable example that:
- Contrasts old and new paradigms immediately
- Provides working code from lesson one
- Introduces security considerations early
- Demonstrates practical git workflow integration

### Mental Models
1. **Claude as a Programmable Agent**: Not just a chatbot, but an executable system
2. **Permissions as Guardrails**: Safety through explicit capability grants
3. **Prompts as Programs**: Structured markdown becomes executable specifications

## Key Takeaways
- Agentic coding transcends simple command execution
- Security and permissions are foundational, not afterthoughts
- Structured prompts enable complex, reliable workflows
- The system is designed for programmatic integration from the start
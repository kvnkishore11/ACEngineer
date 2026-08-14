# Minimal Agentic Layer

The simplest working agentic system you can build. Start here and expand as needed.

## Quick Start

```bash
# 1. Copy this template to your project
cp -r minimal-agentic-layer/ my-project/

# 2. Install Claude CLI (if not already installed)
npm install -g @anthropic/claude-cli

# 3. Test the setup
claude /hello

# 4. Try a real command
claude /analyze "Check code quality"
```

## Project Structure

```
.claude/                    # Claude configuration directory
├── settings.json          # Basic settings
├── commands/              # Slash commands
│   ├── hello.md          # Test command
│   ├── analyze.md        # Analysis command
│   ├── implement.md      # Implementation command
│   └── review.md         # Review command
└── agents/               # Agent configurations
    ├── basic-agent.md    # Simple general-purpose agent
    └── reviewer.md       # Code review agent

src/                       # Your application code
├── index.js              # Entry point
└── utils/                # Utilities

package.json              # Project configuration
README.md                # This file
```

## Core Components

### 1. Settings Configuration
**`.claude/settings.json`**
```json
{
  "version": "1.0",
  "model": "claude-3-sonnet",
  "context": {
    "include": ["src/**/*", "*.json", "*.md"],
    "exclude": ["node_modules", "dist", ".git"]
  },
  "commands": {
    "prefix": "/",
    "directory": "commands"
  },
  "agents": {
    "directory": "agents",
    "default": "basic-agent"
  }
}
```

### 2. Basic Command
**`.claude/commands/hello.md`**
```markdown
# Hello Command

A simple test command to verify your setup.

## Task
Respond with a friendly greeting and confirm the system is working.

Say: "Hello! The agentic system is working. Today is $DATE."

Also list:
- Current working directory
- Number of files in src/ directory
- Node.js version
```

### 3. Basic Agent
**`.claude/agents/basic-agent.md`**
```markdown
---
name: basic-agent
tools: Read, Write, Edit, Bash
model: sonnet
---

# Basic Agent

You are a helpful development assistant. You can:
- Analyze code and suggest improvements
- Implement new features
- Fix bugs
- Write documentation
- Run commands and tests

Always:
- Follow existing code patterns
- Include error handling
- Add helpful comments
- Test your changes when possible
```

### 4. Implementation Command
**`.claude/commands/implement.md`**
```markdown
# Implement Feature

## Task
Implement the following: $ARGUMENTS

## Steps
1. Understand the requirement
2. Check existing code patterns
3. Implement the solution
4. Add basic tests if applicable
5. Update documentation

## Report
Provide:
- Files created/modified
- Key decisions made
- Any assumptions
- Suggested next steps
```

## Usage Examples

### Example 1: Code Analysis
```bash
claude /analyze "src/utils"
```

### Example 2: Feature Implementation
```bash
claude /implement "Add logging utility with timestamp"
```

### Example 3: Code Review
```bash
claude /review "src/index.js"
```

## Extending the System

### Add New Commands

1. Create a new file in `.claude/commands/`:
```markdown
# Command Name

## Task
$ARGUMENTS

## Process
[Your process here]

## Output
[Expected output format]
```

2. Use it:
```bash
claude /your-command "parameters"
```

### Add Agents

1. Create a new file in `.claude/agents/`:
```markdown
---
name: specialist-agent
tools: [needed tools]
model: sonnet
---

# Specialist Agent

[Agent instructions]
```

2. Reference in commands:
```markdown
## Agent
Use: specialist-agent
```

### Add Workflows

1. Create multi-step commands that chain operations
2. Use agents for specialized tasks
3. Add validation and error handling

## Best Practices

1. **Start Simple**: Use basic commands and gradually add complexity
2. **Document Everything**: Keep commands self-documenting
3. **Test Incrementally**: Verify each component works before combining
4. **Use Agents Wisely**: Only create specialized agents when needed
5. **Maintain Context**: Keep the context focused on relevant files

## Common Patterns

### Pattern 1: Analysis → Implementation → Review
```bash
# Analyze current state
claude /analyze "authentication system"

# Implement improvements
claude /implement "Add JWT token refresh"

# Review the changes
claude /review "src/auth"
```

### Pattern 2: Bug Fix Workflow
```bash
# Identify the issue
claude /analyze "error logs"

# Fix the bug
claude /fix "null pointer in user service"

# Verify the fix
claude /test "user service"
```

## Troubleshooting

### Issue: Command not found
**Solution**: Check file exists in `.claude/commands/` and has `.md` extension

### Issue: Agent not responding correctly
**Solution**: Verify agent configuration and model selection

### Issue: Context too large
**Solution**: Adjust `include/exclude` patterns in settings.json

## Next Steps

Once comfortable with this minimal setup:

1. **Add more commands** for your specific workflow
2. **Create specialized agents** for complex tasks
3. **Implement workflows** for multi-step processes
4. **Add hooks** for preprocessing/postprocessing
5. **Integrate with CI/CD** for automation

## Resources

- [Claude Documentation](https://docs.anthropic.com)
- [Agentic Patterns Guide](../patterns.md)
- [Full ADW System](../full-adw-system/)
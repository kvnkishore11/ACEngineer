# Agentic Engineering Quick Start Guide

**Time Required**: 30 minutes
**Outcome**: Your first working autonomous development system

## 🚀 Minute 0-5: Essential Setup

### 1. Install Claude CLI (2 min)

```bash
# macOS
brew install claude

# Windows (WSL/Git Bash)
curl -o- https://claude.ai/cli/install.sh | bash

# Linux
wget -qO- https://claude.ai/cli/install.sh | bash
```

### 2. Verify Installation (1 min)

```bash
claude --version
# Should show: Claude CLI vX.X.X

# Login (if needed)
claude login
```

### 3. Initialize Your Project (2 min)

```bash
# Create project directory
mkdir my-agentic-project
cd my-agentic-project

# Initialize git (required for many features)
git init

# Create the agentic structure
mkdir -p .claude/commands
mkdir -p specs
mkdir -p app

# Create settings file
echo '{"name": "My Agentic Project"}' > .claude/settings.json
```

## 🎯 Minute 5-15: First Agentic Command

### 4. Create Your First Command (5 min)

Create `.claude/commands/implement.md`:

```markdown
# Implement Feature

## Instructions
You are an expert developer. Implement the requested feature following best practices.

## Variables
- FEATURE: The feature to implement
- LANGUAGE: The programming language to use (default: JavaScript)

## Process
1. Understand the feature requirements
2. Create necessary files
3. Implement the feature with clean, documented code
4. Add error handling
5. Create basic tests

## Report
Provide a summary of:
- Files created/modified
- Key implementation decisions
- How to use the feature
- Any assumptions made
```

### 5. Test Your Command (5 min)

```bash
# Run the command
claude run implement.md FEATURE="user authentication" LANGUAGE="Python"

# Watch as Claude:
# - Plans the implementation
# - Creates files
# - Writes code
# - Documents the feature
```

## ⚡ Minute 15-25: Build an Automated Workflow

### 6. Create a Bug Fix Workflow (5 min)

Create `.claude/commands/bugfix.md`:

```markdown
# Automated Bug Fix

## Instructions
Analyze, fix, and test the reported bug.

## Variables
- BUG_DESCRIPTION: Description of the bug
- FILE_PATH: File where bug exists (optional)

## Process
1. Reproduce the bug
2. Identify root cause
3. Implement fix
4. Test the fix
5. Document the solution

## Report
- Root cause analysis
- Fix implementation
- Test results
- Prevention recommendations
```

### 7. Create a Test Generator (5 min)

Create `.claude/commands/test.md`:

```markdown
# Test Generator

## Instructions
Generate comprehensive tests for the specified code.

## Variables
- TARGET: File or function to test
- FRAMEWORK: Testing framework (default: auto-detect)

## Process
1. Analyze the code structure
2. Identify test scenarios
3. Generate test cases
4. Include edge cases
5. Add test documentation

## Report
- Test coverage summary
- Number of test cases created
- Critical paths tested
```

## 🏆 Minute 25-30: Your First Win

### 8. Create a Complete Feature Pipeline

Create `.claude/commands/pipeline.md`:

```markdown
# Complete Development Pipeline

## Instructions
Execute a complete development cycle for the requested feature.

## Variables
- REQUIREMENT: What needs to be built

## Process
1. **Plan**: Create implementation plan
   - Break down into tasks
   - Identify components needed

2. **Implement**: Build the feature
   - Use command: implement.md

3. **Test**: Generate and run tests
   - Use command: test.md

4. **Document**: Create documentation
   - API documentation
   - Usage examples

5. **Review**: Code quality check
   - Check for best practices
   - Identify improvements

## Report
Complete development report including all phases
```

### 9. Run Your Pipeline!

```bash
# Execute the complete pipeline
claude run pipeline.md REQUIREMENT="REST API for todo list with CRUD operations"

# Watch your system autonomously:
# - Plan the API structure
# - Implement endpoints
# - Generate tests
# - Create documentation
# - Review code quality
```

## 📋 Core Concepts (The 20% That Gives 80%)

### 1. Commands Are Reusable Agents
Each `.md` file in `.claude/commands/` is a reusable agent that can be invoked with different parameters.

### 2. Variables Make Commands Dynamic
Use `$VARIABLE_NAME` in commands to create flexible, reusable behaviors.

### 3. Commands Can Call Commands
Chain commands together for complex workflows (like our pipeline example).

### 4. The Permission Model Gives You Control
- `ask`: Claude asks before taking action
- `allow`: Claude proceeds automatically
- `deny`: Claude cannot perform action

### 5. Context Is Everything
Keep commands focused. Complex tasks should be broken into specialized commands.

## 🎪 Next Steps: Where to Go from Here

### Hour 1-2: Expand Your Toolkit

Create these additional commands:
- `review.md` - Code review automation
- `refactor.md` - Code improvement
- `optimize.md` - Performance optimization
- `security.md` - Security scanning

### Day 1: Build Real Workflows

1. **Development Workflow**
   ```
   plan.md → implement.md → test.md → document.md
   ```

2. **Maintenance Workflow**
   ```
   analyze.md → refactor.md → test.md → deploy.md
   ```

3. **Debug Workflow**
   ```
   reproduce.md → diagnose.md → fix.md → verify.md
   ```

### Week 1: GitHub Integration

```bash
# Install GitHub CLI
gh auth login

# Create issue-to-PR workflow
mkdir .claude/commands/github
# Add issue.md, pr.md, review.md commands
```

### Month 1: Production System

- Add error handling patterns
- Implement logging and monitoring
- Create deployment automation
- Build self-documenting systems

## 🚧 Templates: Copy-Paste Starting Points

### Universal Feature Builder

```markdown
# Build Feature

## Instructions
Build a complete, production-ready feature.

## Variables
- SPEC: Feature specification
- STACK: Technology stack

## Process
1. Analyze requirements
2. Design architecture
3. Implement core functionality
4. Add error handling
5. Create tests
6. Generate documentation
7. Prepare deployment

## Report
- Architecture decisions
- Implementation details
- Test coverage
- Deployment instructions
```

### Smart Debugger

```markdown
# Smart Debug

## Instructions
Automatically debug and fix issues in the codebase.

## Variables
- ERROR: Error message or symptom
- CONTEXT: Additional context (optional)

## Process
1. Analyze error patterns
2. Search for root cause
3. Generate fix candidates
4. Test each fix
5. Apply working solution
6. Add regression test

## Report
- Root cause
- Fix applied
- Test added
- Prevention tips
```

### API Generator

```markdown
# API Generator

## Instructions
Generate a complete REST API with documentation.

## Variables
- ENTITIES: List of entities (e.g., User, Product)
- DATABASE: Database type (default: PostgreSQL)

## Process
1. Design database schema
2. Create models
3. Implement CRUD endpoints
4. Add authentication
5. Generate OpenAPI spec
6. Create integration tests

## Report
- Endpoints created
- Authentication method
- API documentation link
- Test results
```

## 💡 Pro Tips for Immediate Success

### 1. Start Small, Think Big
Begin with simple commands, then compose them into complex workflows.

### 2. Use Git From the Start
```bash
git init
git add .
git commit -m "Initial agentic setup"
```
Many advanced features require git.

### 3. Iterate Quickly
Don't perfect commands; use them, learn, improve.

### 4. Share Variables Between Commands
```bash
# Set once, use everywhere
export PROJECT_NAME="my-app"
claude run implement.md FEATURE="auth" PROJECT=$PROJECT_NAME
```

### 5. Create Project-Specific Commands
Each project should have its own `.claude/commands/` tailored to its needs.

## 🔥 Your 30-Minute Achievement

Congratulations! In just 30 minutes, you've:
- ✅ Set up an agentic development environment
- ✅ Created reusable AI agents
- ✅ Built automated workflows
- ✅ Executed a complete development pipeline
- ✅ Learned the core concepts

You're now officially doing Agentic Engineering!

## 🎯 Challenge: Your Next 30 Minutes

Can you:
1. Create a command that generates other commands?
2. Build a workflow that fixes its own errors?
3. Make a self-improving documentation system?

The only limit is your imagination.

## 📚 Quick Reference Card

```bash
# Run a command
claude run <command>.md VAR1="value1" VAR2="value2"

# List available commands
ls .claude/commands/

# Create new command
echo "# Command Name" > .claude/commands/newcmd.md

# Chain commands (in bash)
claude run plan.md && claude run implement.md && claude run test.md

# Set permissions
claude config set permissions.file_write ask
claude config set permissions.command_run allow
```

## 🚀 You're Ready!

You've just scratched the surface of Agentic Engineering. In 30 minutes, you've built what would have taken days to code manually.

**Next Discovery**: What if your agents could create other agents? What if they could improve themselves? What if they could learn from every execution?

That's not the future. That's what you'll build next.

Welcome to Agentic Engineering. Now go build something amazing!
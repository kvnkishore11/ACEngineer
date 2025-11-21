# 🚀 Production-Ready Agentic Templates

Complete template library extracted from the Agentic Engineering course. Go from zero to production-ready agentic systems in hours, not weeks.

## 📚 Template Categories

### 🤖 [Agents](./agents/)
Pre-configured agent templates for common roles:
- **[basic-agent.md](./agents/basic-agent.md)** - Simple starting template for any agent
- **[research-agent.md](./agents/research-agent.md)** - Deep investigation and analysis specialist
- **[implementation-agent.md](./agents/implementation-agent.md)** - Code generation and feature implementation
- **[review-agent.md](./agents/review-agent.md)** - Code review and quality assurance
- **[orchestrator-agent.md](./agents/orchestrator-agent.md)** - Multi-agent coordination and workflow management
- **[specialist-agent.md](./agents/specialist-agent.md)** - Domain-specific expert template

### 📝 [Commands](./commands/)
Slash command templates for Claude Code:
- **[basic-command.md](./commands/basic-command.md)** - Simple command structure
- **[workflow-command.md](./commands/workflow-command.md)** - Multi-step workflow orchestration
- **[agent-command.md](./commands/agent-command.md)** - Commands that delegate to agents
- **[pipeline-command.md](./commands/pipeline-command.md)** - Complete automation pipelines

### 🎯 [Skills](./skills/)
Reusable skill definitions:
- **[basic-skill.md](./skills/basic-skill.md)** - Template for defining new skills
- Research skills, generation skills, and analysis patterns (additional templates available)

### 🔄 [Workflows](./workflows/)
Complete workflow configurations:
- **[bfc-workflow.yaml](./workflows/bfc-workflow.yaml)** - Bug Fix Commit workflow
- ISO (Issue Structured Orchestration) workflows
- ADW (Autonomous Development Workflow) patterns
- ZTE (Zero Touch Execution) configurations

### 💭 [Prompts](./prompts/)
Prompt engineering at different complexity levels:
- **[level-1-static.md](./prompts/level-1-static.md)** - Basic static prompts
- Level 3 Delegating - Context reduction strategies
- Level 5 Adaptive - Dynamic prompt generation
- Level 7 Self-Improving - Evolutionary prompts

### 🏗️ [Projects](./projects/)
Complete project scaffolds:
- **[minimal-agentic-layer/](./projects/minimal-agentic-layer/)** - Simplest working system
- Full ADW systems with complete automation
- Multi-agent orchestration setups
- Domain-specific implementations

### 🔌 [Integrations](./integrations/)
Integration patterns and templates:
- **[mcp-server-template.py](./integrations/mcp-server-template.py)** - Model Context Protocol server
- GitHub API integration patterns
- Database connection templates
- WebSocket and REST API patterns

## 🚀 Quick Start

### 1. Choose Your Starting Point

#### For Beginners
Start with the minimal agentic layer:
```bash
cp -r templates/projects/minimal-agentic-layer/ my-project/
cd my-project
```

#### For Specific Tasks
Copy individual templates:
```bash
# Copy an agent template
cp templates/agents/implementation-agent.md .claude/agents/

# Copy a command template
cp templates/commands/workflow-command.md .claude/commands/

# Copy a workflow
cp templates/workflows/bfc-workflow.yaml .claude/workflows/
```

### 2. Customize Templates

All templates have clear customization points marked:
- Look for `[PLACEHOLDER]` markers
- Check "Customization Guide" sections
- Follow inline comments

### 3. Test Your Setup

```bash
# Test a basic command
claude /hello

# Test an agent
claude /agent basic-agent "Analyze this codebase"

# Run a workflow
claude /workflow bfc-workflow --issue=123
```

## 📖 How to Use Each Template Type

### Agents
1. Choose an agent template based on your needs
2. Copy to `.claude/agents/[name].md`
3. Customize the purpose, tools, and workflow sections
4. Reference in commands or workflows

### Commands
1. Select a command pattern (basic, workflow, agent-based, or pipeline)
2. Copy to `.claude/commands/[name].md`
3. Define inputs, process, and outputs
4. Use with `/[name]` in Claude

### Workflows
1. Choose a workflow pattern (sequential, parallel, or adaptive)
2. Define stages, dependencies, and validation
3. Configure error handling and rollback
4. Execute with appropriate triggers

### Skills
1. Define the skill's purpose and workflow
2. Document prerequisites and tools
3. Provide examples and patterns
4. Reference in agent configurations

## 🏆 Best Practices

### Start Simple
- Begin with basic templates
- Add complexity gradually
- Test each component independently
- Document as you go

### Compose Templates
```yaml
# Combine templates for complex systems
project:
  agents:
    - research-agent (from template)
    - implementation-agent (from template)
    - custom-domain-agent (modified specialist)

  commands:
    - analyze (basic-command template)
    - implement (agent-command template)
    - deploy (pipeline-command template)

  workflows:
    - development (custom workflow)
    - review (bfc-workflow template)
```

### Customize Thoughtfully
- Keep core structure intact
- Modify specific sections as needed
- Preserve error handling
- Maintain documentation

## 🎯 Common Use Cases

### Feature Development
```bash
# Use this combination:
1. research-agent → Analyze existing code
2. implementation-agent → Build feature
3. review-agent → Quality check
4. bfc-workflow → Commit and PR
```

### Bug Fixing
```bash
# Use BFC workflow:
templates/workflows/bfc-workflow.yaml
```

### Code Analysis
```bash
# Use research agent:
templates/agents/research-agent.md
```

### Multi-Agent Systems
```bash
# Use orchestrator pattern:
templates/agents/orchestrator-agent.md
templates/commands/workflow-command.md
```

## 📊 Template Selection Guide

| Use Case | Agent | Command | Workflow | Complexity |
|----------|-------|---------|----------|------------|
| Simple task | basic-agent | basic-command | - | Low |
| Code analysis | research-agent | agent-command | - | Medium |
| Feature development | implementation-agent | workflow-command | ISO | Medium |
| Bug fixing | multiple | pipeline-command | BFC | High |
| Full automation | orchestrator + specialists | pipeline-command | ADW/ZTE | Very High |

## 🔧 Customization Patterns

### Agent Customization
```markdown
# In agent template, modify:
1. Purpose → Your specific domain
2. Tools → Required capabilities
3. Workflow → Your process steps
4. Output format → Your standards
```

### Command Customization
```markdown
# In command template, modify:
1. Instructions → Your specific steps
2. Arguments → Required inputs
3. Process → Your logic
4. Output → Your format
```

### Workflow Customization
```yaml
# In workflow template, modify:
stages:
  - Your stages here
dependencies:
  - Your dependencies
validation:
  - Your criteria
error_handling:
  - Your recovery strategy
```

## 🚨 Important Notes

### Security Considerations
- Review and modify security-related code
- Don't commit sensitive data to templates
- Implement proper authentication where needed
- Validate all inputs

### Performance
- Start with small tests
- Monitor resource usage
- Optimize based on metrics
- Scale gradually

### Maintenance
- Keep templates updated
- Document modifications
- Version your customizations
- Test regularly

## 📚 Learning Path

### Week 1: Basics
1. Set up minimal-agentic-layer
2. Create first custom command
3. Modify basic-agent for your needs
4. Run simple workflows

### Week 2: Intermediate
1. Implement multi-step workflows
2. Create specialized agents
3. Build agent-command integrations
4. Add error handling

### Week 3: Advanced
1. Design multi-agent orchestration
2. Implement full pipelines
3. Create domain-specific agents
4. Build production workflows

### Week 4: Production
1. Add monitoring and metrics
2. Implement CI/CD integration
3. Create comprehensive tests
4. Deploy to production

## 🤝 Contributing

Found improvements? Create variations? Share them!

1. Document your customizations
2. Include usage examples
3. Provide test cases
4. Share with the community

## 📞 Support

- Review template documentation
- Check customization guides
- Refer to course materials
- Engage with the community

## 🎉 Success Stories

These templates have been used to build:
- Autonomous code review systems
- Self-healing infrastructure
- Automated documentation generators
- Multi-agent development teams
- Zero-touch deployment pipelines

Start with these templates and build your own success story!

---

**Remember**: These templates are starting points. The real power comes from understanding the patterns and adapting them to your specific needs. Start simple, iterate quickly, and scale confidently.
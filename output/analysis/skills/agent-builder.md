---
title: "Agent Builder"
description: "Create specialized agents from basic to advanced, with tools, state management, and orchestration capabilities"
tags: ["agents", "development", "tools", "state-management", "specialization"]
---

# Agent Builder

## Purpose

Build custom agents tailored to specific domains and tasks, from simple reactive agents to complex stateful systems with streaming capabilities. Master the progression from basic echo agents to sophisticated orchestration systems.

## When to Use

- Creating domain-specific agents for your project
- Building agents with custom tool integrations
- Implementing stateful agent behaviors
- Developing specialized agents for production systems
- Upgrading from simple prompts to full agent systems

## How It Works

### Step 1: Define Agent Purpose

```markdown
## Agent Specification
- **Name**: descriptive-agent-name
- **Purpose**: Primary task or domain
- **Capabilities**: What it can do
- **Limitations**: What it shouldn't do
- **Integration**: Systems it connects to
```

### Step 2: Choose Agent Complexity Level

Based on the 8-agent progression from Agentic Horizon:

#### Level 1: Basic Agent (Pong Pattern)
```python
# Simple request-response agent
class BasicAgent:
    def __init__(self, name: str, prompt: str):
        self.name = name
        self.prompt = prompt

    async def respond(self, message: str) -> str:
        # Simple prompt completion
        return await llm.complete(
            system=self.prompt,
            user=message
        )
```

#### Level 2: Tool-Enabled Agent (Echo Pattern)
```python
# Agent with tool access
class ToolAgent:
    def __init__(self, name: str, tools: list):
        self.name = name
        self.tools = tools

    async def execute(self, task: str) -> str:
        # Select and use tools
        tool = self.select_tool(task)
        result = await tool.run(task)
        return self.format_response(result)
```

#### Level 3: Stateful Agent (Calculator Pattern)
```python
# Agent with memory and state
class StatefulAgent:
    def __init__(self, name: str):
        self.name = name
        self.state = {}
        self.history = []

    async def process(self, input: str) -> str:
        # Update state based on input
        self.update_state(input)
        self.history.append(input)

        # Generate response considering state
        response = await self.generate_with_context()
        return response
```

#### Level 4: Streaming Agent (Social Hype Pattern)
```python
# Agent with real-time streaming
class StreamingAgent:
    def __init__(self, name: str):
        self.name = name
        self.websocket = None

    async def stream(self, prompt: str):
        async for chunk in llm.stream(prompt):
            await self.websocket.send_json({
                "type": "stream",
                "content": chunk
            })
```

#### Level 5: Specialized Agent (QA Pattern)
```python
# Domain-specific agent
class QAAgent:
    def __init__(self):
        self.name = "qa-specialist"
        self.test_patterns = load_patterns()

    async def test_feature(self, feature: dict):
        # Generate test plan
        plan = await self.create_test_plan(feature)

        # Execute tests
        results = await self.run_tests(plan)

        # Generate report
        return self.create_report(results)
```

#### Level 6: Web App Agent (Tri-Copy Pattern)
```python
# Full application agent
class WebAppAgent:
    def __init__(self):
        self.name = "webapp-builder"
        self.frameworks = ["next", "react", "vue"]

    async def build_app(self, spec: dict):
        # Select framework
        framework = self.select_framework(spec)

        # Generate components
        components = await self.generate_components(spec)

        # Create routes
        routes = await self.create_routes(spec)

        # Deploy
        return await self.deploy(framework, components, routes)
```

#### Level 7: Orchestration Agent (SDLC Pattern)
```python
# Multi-agent coordinator
class SDLCOrchestrator:
    def __init__(self):
        self.agents = {
            "planner": PlannerAgent(),
            "developer": DeveloperAgent(),
            "tester": TesterAgent(),
            "reviewer": ReviewerAgent()
        }

    async def execute_issue(self, issue: dict):
        # Coordinate multiple agents
        plan = await self.agents["planner"].plan(issue)
        code = await self.agents["developer"].implement(plan)
        tests = await self.agents["tester"].test(code)
        review = await self.agents["reviewer"].review(code, tests)

        return self.create_pr(code, tests, review)
```

#### Level 8: Dual-System Agent (Ultra Stream Pattern)
```python
# Complex multi-channel agent
class UltraStreamAgent:
    def __init__(self):
        self.websocket = WebSocketManager()
        self.sse = SSEManager()
        self.database = DatabaseManager()

    async def handle_request(self, request: dict):
        # Process through multiple channels
        ws_task = self.websocket.broadcast(request)
        sse_task = self.sse.stream(request)
        db_task = self.database.log(request)

        # Coordinate responses
        await asyncio.gather(ws_task, sse_task, db_task)
```

### Step 3: Design Agent Configuration

#### Claude Code Agent Definition
```yaml
# .claude/agents/code-reviewer.md
---
name: code-reviewer
description: Reviews code for quality, security, and best practices
color: green
tools:
  - bash
  - read
  - grep
  - edit
---

You are a code review specialist. Your role is to:

1. Analyze code for quality issues
2. Check for security vulnerabilities
3. Suggest improvements
4. Ensure best practices

## Review Process

1. Read the changed files
2. Run static analysis tools
3. Check test coverage
4. Generate review report

## Standards

- Follow team coding standards
- Check for common anti-patterns
- Ensure proper error handling
- Verify documentation
```

### Step 4: Implement Tool Integration

```python
# Custom tool for agent
class CustomTool:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    async def execute(self, params: dict):
        # Tool implementation
        pass

# Register with agent
agent.register_tool(CustomTool(
    name="database_query",
    description="Query the application database"
))
```

### Step 5: Add Agent Behaviors

```python
class BehavioralAgent:
    def __init__(self):
        self.behaviors = {
            "proactive": self.proactive_check,
            "reactive": self.reactive_response,
            "scheduled": self.scheduled_task
        }

    async def proactive_check(self):
        # Monitor and act without prompting
        if self.detect_issue():
            await self.auto_fix()

    async def reactive_response(self, trigger):
        # Respond to events
        await self.handle_event(trigger)

    async def scheduled_task(self):
        # Run periodic tasks
        await self.daily_report()
```

## Inputs Expected

- **Agent Purpose**: Clear definition of what the agent should do
- **Domain Knowledge**: Understanding of the specific field
- **Integration Requirements**: Systems the agent needs to connect with
- **Performance Needs**: Speed, accuracy, resource constraints
- **Interaction Model**: How users/systems will interact with the agent

## Outputs Provided

1. **Agent Configuration File**
   ```yaml
   # Complete .claude/agents/ configuration
   - Agent metadata
   - System prompt
   - Tool permissions
   - Behavioral rules
   ```

2. **Implementation Code**
   ```python
   # Python/JavaScript agent implementation
   - Agent class
   - Tool integrations
   - State management
   - Communication protocols
   ```

3. **Test Suite**
   ```python
   # Agent testing framework
   - Unit tests for behaviors
   - Integration tests
   - Performance tests
   - Edge case handling
   ```

4. **Documentation**
   ```markdown
   # Agent documentation
   - Usage guide
   - API reference
   - Examples
   - Troubleshooting
   ```

## Examples

### Example 1: Database Migration Agent

```python
# Migration specialist agent
class MigrationAgent:
    def __init__(self, db_config):
        self.name = "migration-specialist"
        self.db = Database(db_config)
        self.validator = SchemaValidator()

    async def plan_migration(self, from_version, to_version):
        # Analyze schema differences
        changes = self.analyze_changes(from_version, to_version)

        # Generate migration plan
        plan = {
            "pre_checks": self.generate_prechecks(changes),
            "migrations": self.generate_migrations(changes),
            "rollback": self.generate_rollback(changes),
            "validation": self.generate_validation(changes)
        }

        return plan

    async def execute_migration(self, plan):
        # Run pre-checks
        if not await self.run_prechecks(plan["pre_checks"]):
            return {"status": "failed", "stage": "pre-check"}

        # Execute migration with rollback capability
        try:
            await self.db.transaction(plan["migrations"])
            await self.validate(plan["validation"])
            return {"status": "success"}
        except Exception as e:
            await self.db.rollback(plan["rollback"])
            return {"status": "failed", "error": str(e)}
```

### Example 2: Customer Support Agent

```python
# Support agent with sentiment analysis
class SupportAgent:
    def __init__(self):
        self.name = "customer-support"
        self.knowledge_base = KnowledgeBase()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.ticket_system = TicketSystem()

    async def handle_inquiry(self, message: dict):
        # Analyze sentiment
        sentiment = self.sentiment_analyzer.analyze(message["text"])

        # Route based on urgency
        if sentiment["score"] < -0.5:
            # Escalate negative sentiment
            return await self.escalate_to_human(message)

        # Search knowledge base
        solutions = await self.knowledge_base.search(message["text"])

        if solutions:
            response = self.format_solution(solutions[0])
        else:
            # Create ticket for new issue
            ticket = await self.ticket_system.create(message)
            response = f"I've created ticket {ticket.id} for your issue."

        return response
```

### Example 3: Security Audit Agent

```python
# Security scanning agent
class SecurityAgent:
    def __init__(self):
        self.name = "security-auditor"
        self.scanners = {
            "dependencies": DependencyScanner(),
            "code": StaticAnalyzer(),
            "secrets": SecretScanner(),
            "config": ConfigAuditor()
        }

    async def audit_project(self, project_path: str):
        results = {}

        # Run all scanners in parallel
        tasks = [
            self.scan_dependencies(project_path),
            self.scan_code(project_path),
            self.scan_secrets(project_path),
            self.audit_config(project_path)
        ]

        scan_results = await asyncio.gather(*tasks)

        # Synthesize findings
        report = self.create_security_report(scan_results)

        # Generate fixes
        fixes = await self.generate_fixes(report["vulnerabilities"])

        return {
            "report": report,
            "fixes": fixes,
            "risk_score": self.calculate_risk(report)
        }
```

## Troubleshooting

### Common Issues

1. **Agent Not Responding**
   ```python
   # Add timeout handling
   async def safe_execute(agent, task, timeout=30):
       try:
           return await asyncio.wait_for(
               agent.execute(task),
               timeout=timeout
           )
       except asyncio.TimeoutError:
           return {"error": "Agent timeout"}
   ```

2. **Tool Conflicts**
   ```python
   # Implement tool priority
   class ToolManager:
       def select_tool(self, task, available_tools):
           # Score each tool for the task
           scores = {
               tool: self.score_tool(task, tool)
               for tool in available_tools
           }
           return max(scores, key=scores.get)
   ```

3. **State Corruption**
   ```python
   # Add state validation
   class StatefulAgent:
       def validate_state(self):
           required_keys = ["session_id", "user", "context"]
           return all(key in self.state for key in required_keys)

       def reset_state(self):
           self.state = self.get_default_state()
   ```

## Related Skills

- **Prompt Engineer**: Create effective prompts for your agents
- **Context Optimizer**: Optimize agent performance and context usage
- **Testing Strategist**: Test your agent implementations
- **Workflow Designer**: Design workflows that agents will execute
- **Integration Specialist**: Connect agents to external systems

## Advanced Techniques

### Agent Cloning
```python
# Create variations of successful agents
class AgentFactory:
    def clone_with_specialization(self, base_agent, specialization):
        cloned = copy.deepcopy(base_agent)
        cloned.prompt += f"\nSpecialization: {specialization}"
        return cloned
```

### Agent Evolution
```python
# Agents that improve over time
class EvolvingAgent:
    def learn_from_feedback(self, task, result, feedback):
        if feedback.positive:
            self.reinforce_behavior(task, result)
        else:
            self.adjust_behavior(task, feedback.suggestion)
```

### Agent Composition
```python
# Combine multiple agents into one
class CompositeAgent:
    def __init__(self, agents: list):
        self.agents = agents

    async def execute(self, task):
        # Each agent votes on approach
        votes = await self.collect_votes(task)
        # Execute with majority approach
        return await self.execute_consensus(votes)
```

## Key Principles

1. **Single Responsibility**: Each agent should have one clear purpose
2. **Tool Appropriateness**: Give agents only the tools they need
3. **State Management**: Decide if agent needs memory/state upfront
4. **Error Handling**: Build robust error recovery into agents
5. **Observability**: Log agent decisions and actions for debugging

---

*This skill is derived from the "Building Specialized Agents" module of the Agentic Horizon course, providing a complete framework for creating production-ready agents.*
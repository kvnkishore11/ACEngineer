---
title: "Agentic Architect"
description: "Design complete agentic system architectures using patterns from TAC-8 and orchestration principles"
tags: ["architecture", "system-design", "patterns", "adw", "orchestration"]
---

# Agentic Architect

## Purpose

Design and architect complete agentic systems, from simple automation to enterprise-scale multi-agent orchestration. This skill helps you select the right architectural pattern, design system components, and create implementation blueprints.

## When to Use

- Starting a new agentic project and need to choose architecture
- Refactoring existing systems to be more agentic
- Scaling from single-agent to multi-agent systems
- Designing production-ready autonomous development workflows
- Evaluating different architectural approaches for specific use cases

## How It Works

### Step 1: Analyze Requirements
```markdown
1. Identify the problem domain
2. Determine autonomy level needed
3. Assess integration requirements
4. Define quality and scale requirements
5. Evaluate team expertise level
```

### Step 2: Select Architectural Pattern

Based on TAC-8's five proven patterns:

#### Pattern 1: API + WebSocket Server
**When**: Real-time updates, multiple clients, streaming data
```python
# Architecture Components:
- FastAPI backend
- WebSocket for real-time events
- PostgreSQL for persistence
- Event-driven architecture
```

#### Pattern 2: Browser Extension Architecture
**When**: Enhancing web applications, browser automation
```javascript
// Components:
- Content scripts for page manipulation
- Background service workers
- Message passing architecture
- Chrome/Firefox APIs
```

#### Pattern 3: Python + GitHub App
**When**: Repository automation, CI/CD integration
```yaml
# Components:
- GitHub webhook handlers
- GitHub API integration
- Issue-to-PR automation
- Code review automation
```

#### Pattern 4: CLI Multi-Tool Architecture
**When**: Developer tools, command-line automation
```bash
# Components:
- Click/Typer CLI framework
- Modular command structure
- Plugin system
- Configuration management
```

#### Pattern 5: Full Stack Web (Next.js + Supabase)
**When**: User-facing applications, SaaS products
```typescript
// Components:
- Next.js frontend
- Supabase backend
- Real-time subscriptions
- Authentication & authorization
```

### Step 3: Design Agent Topology

#### Single Agent Pattern
```
User → Agent → Task → Output
```

#### Pipeline Pattern (ADW Style)
```
Issue → Planner → Implementer → Reviewer → Deployer → PR
```

#### Orchestrator Pattern
```
         ┌─→ Agent A ─┐
User → Orchestrator ├─→ Agent B ─┤→ Results
         └─→ Agent C ─┘
```

#### Hierarchical Pattern
```
    Master Orchestrator
    ├── Team Lead Agent 1
    │   ├── Worker Agent A
    │   └── Worker Agent B
    └── Team Lead Agent 2
        ├── Worker Agent C
        └── Worker Agent D
```

### Step 4: Define Integration Points

#### MCP (Model Context Protocol)
```yaml
# .claude/mcp/config.json
{
  "servers": {
    "database": {
      "command": ["uv", "run", "mcp_server.py"],
      "tools": ["query", "update", "migrate"]
    }
  }
}
```

#### API Integration
```python
# RESTful API design
GET /api/agents           # List agents
POST /api/agents          # Create agent
GET /api/tasks/{id}       # Get task status
POST /api/tasks/execute   # Execute task
```

#### Event System
```python
# Event-driven architecture
class EventBus:
    def emit(self, event: str, data: dict):
        # Broadcast to all subscribers
        pass

    def on(self, event: str, handler: callable):
        # Subscribe to events
        pass
```

### Step 5: Create Implementation Blueprint

```markdown
## System Architecture Document

### 1. Overview
- System purpose
- Key stakeholders
- Success metrics

### 2. Architecture Pattern
- Selected pattern and rationale
- Alternative patterns considered
- Trade-offs accepted

### 3. Component Design
- Agent specifications
- Data flow diagrams
- Integration points
- Security boundaries

### 4. Implementation Plan
- Phase 1: Core infrastructure
- Phase 2: Agent implementation
- Phase 3: Integration
- Phase 4: Testing & deployment

### 5. Quality Attributes
- Performance requirements
- Scalability approach
- Reliability measures
- Security controls
```

## Inputs Expected

- **Business Requirements**: What problem needs solving
- **Technical Constraints**: Existing systems, technology stack
- **Scale Requirements**: Number of users, data volume, performance needs
- **Team Capabilities**: Developer expertise, maintenance capacity
- **Timeline**: Development schedule, milestones

## Outputs Provided

1. **Architecture Decision Record (ADR)**
   - Pattern selection rationale
   - Trade-off analysis
   - Risk assessment

2. **System Design Document**
   - Component diagrams
   - Sequence diagrams
   - Data flow diagrams
   - API specifications

3. **Implementation Roadmap**
   - Phased development plan
   - Dependency management
   - Risk mitigation strategies

4. **Agent Specifications**
   - Individual agent designs
   - Communication protocols
   - Tool configurations
   - Prompt templates

## Examples

### Example 1: E-commerce Automation System

**Requirement**: Automate product listing, inventory management, and customer support

**Architecture Selected**: API + WebSocket Server
```python
# System Components
orchestrator_api/
├── agents/
│   ├── product_manager.py    # Handles listings
│   ├── inventory_tracker.py  # Monitors stock
│   └── support_agent.py      # Customer queries
├── database/
│   └── models.py             # Product, Order, Customer
├── websocket/
│   └── events.py             # Real-time updates
└── api/
    └── endpoints.py          # REST API
```

### Example 2: Code Review Automation

**Requirement**: Automated PR reviews with specific team standards

**Architecture Selected**: Python + GitHub App
```yaml
# Workflow
1. PR opened/updated webhook
2. Code analysis agent triggered
3. Style checker agent runs
4. Security scanner agent runs
5. Review synthesizer combines feedback
6. Posts review comment on PR
```

### Example 3: Multi-Agent Development System

**Requirement**: Complete SDLC automation from issue to deployment

**Architecture Selected**: Orchestrator Pattern with PostgreSQL
```python
# Agent Registry
agents = {
    "planner": PlannerAgent(),      # Creates implementation plans
    "coder": CoderAgent(),          # Writes code
    "tester": TesterAgent(),        # Creates and runs tests
    "reviewer": ReviewerAgent(),    # Reviews code quality
    "documenter": DocAgent(),       # Updates documentation
    "deployer": DeployAgent()       # Handles deployment
}

# Orchestration Logic
async def handle_issue(issue_id):
    plan = await agents["planner"].create_plan(issue_id)
    code = await agents["coder"].implement(plan)
    tests = await agents["tester"].test(code)
    review = await agents["reviewer"].review(code, tests)
    if review.approved:
        docs = await agents["documenter"].update(code)
        await agents["deployer"].deploy(code)
```

## Troubleshooting

### Common Architecture Anti-Patterns

1. **Over-Engineering**
   - Solution: Start with simplest pattern that works
   - Evolve complexity as needed

2. **Tight Coupling**
   - Solution: Use message passing, event-driven design
   - Keep agents independent

3. **Context Explosion**
   - Solution: Implement context boundaries
   - Use delegation patterns

4. **Single Point of Failure**
   - Solution: Design for graceful degradation
   - Implement retry mechanisms

### Performance Issues

```python
# Pattern: Circuit Breaker for Agent Calls
class CircuitBreaker:
    def __init__(self, threshold=5, timeout=60):
        self.threshold = threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure = None

    async def call(self, agent_func, *args):
        if self.is_open():
            raise Exception("Circuit breaker is open")

        try:
            result = await agent_func(*args)
            self.reset()
            return result
        except Exception as e:
            self.record_failure()
            raise e
```

## Related Skills

- **Agent Builder**: Create the individual agents for your architecture
- **Workflow Designer**: Design the workflows within your system
- **Integration Specialist**: Connect your system to external services
- **Context Optimizer**: Optimize performance of your architecture
- **Testing Strategist**: Validate your architectural decisions

## Advanced Patterns

### Self-Healing Architecture
```python
# Agents that monitor and fix themselves
class SelfHealingOrchestrator:
    async def health_check(self):
        for agent in self.agents:
            if not agent.is_healthy():
                await self.restart_agent(agent)
```

### Adaptive Architecture
```python
# System that adjusts based on load
class AdaptiveSystem:
    def scale_agents(self, metrics):
        if metrics.latency > threshold:
            self.spawn_additional_agents()
        elif metrics.utilization < minimum:
            self.reduce_agent_pool()
```

### Meta-Architecture
```python
# Architecture that can redesign itself
class MetaArchitect:
    def evaluate_performance(self):
        if self.metrics.below_target():
            new_design = self.generate_architecture()
            self.migrate_to(new_design)
```

## Key Principles

1. **Start Simple**: Begin with minimal viable architecture
2. **Design for Change**: Assume requirements will evolve
3. **Isolate Complexity**: Keep complex logic in specialized agents
4. **Embrace Events**: Use event-driven patterns for loose coupling
5. **Monitor Everything**: Build observability from the start

---

*This skill synthesizes architectural patterns from TAC-8 and multi-agent orchestration modules, providing battle-tested approaches for building production agentic systems.*
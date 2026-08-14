# Concept Mapping: Video Teachings to Code Implementation

*Bridging the gap between theoretical patterns and working examples*

## Introduction

This document maps the concepts taught in the Building Specialized Agents video series to actual implementations in the codebase. It shows how abstract principles become concrete code, helping you understand both the "why" and the "how" of specialized agent development.

---

## Core Concept Mappings

### Concept 1: "Better Agents → More Agents → Custom Agents"

**Video Teaching**:
> "Agentic engineering leads every engineer down one single path. Better agents, more agents, and then custom agents."

**Code Implementation**:

The progression is demonstrated through 8 increasingly sophisticated custom agents:

```python
# Stage 1: Better Agents (Simple overrides)
apps/custom_1_pong_agent/  # Basic system prompt override

# Stage 2: More Agents (Multiple capabilities)
apps/custom_2_echo_agent/  # Custom tools
apps/custom_3_calc_agent/  # Multiple tools, REPL interface

# Stage 3: Custom Agents (Domain-specific)
apps/custom_4_social_hype_agent/  # Real-time monitoring
apps/custom_7_micro_sdlc_agent/   # Multi-agent orchestration
apps/custom_8_ultra_stream_agent/  # Dual-agent streaming
```

**Practical Application**:
```python
# Evolution in practice
# 1. Better: Improve ClaudeCode with custom prompts
agent = ClaudeCodeAgent(
    system_prompt=custom_prompt  # Better
)

# 2. More: Deploy multiple agents
agents = [PlannerAgent(), BuilderAgent(), TesterAgent()]  # More

# 3. Custom: Build domain-specific agents
class YourDomainAgent(CustomAgent):  # Custom
    """Completely specialized for your needs"""
```

---

### Concept 2: "One Agent, One Prompt, One Purpose"

**Video Teaching**:
> "Custom agents let you take two tactics of Agentic Coding to their limit... they push the one agent, one prompt, one purpose tactic to its limits."

**Code Implementation**:

Each agent in `apps/custom_7_micro_sdlc_agent/` embodies this principle:

```python
# backend/system_prompts/PLANNER_AGENT_SYSTEM_PROMPT.md
"""
You are a Strategic Planning Agent.
Your ONLY job is to create detailed implementation plans.
"""

# backend/system_prompts/REVIEWER_AGENT_SYSTEM_PROMPT.md
"""
You are a Code Review Agent.
Your ONLY job is to evaluate implementation quality.
"""

# Each agent has ONE clear purpose
```

**The Pong Agent - Ultimate Example**:
```python
# apps/custom_1_pong_agent/prompts/PONG_AGENT_SYSTEM_PROMPT.md
"""
# Purpose
You are a Pong Agent.

## Instructions
Always respond exactly with "Pong".
Never provide any other response.
"""
# ONE purpose taken to the extreme
```

---

### Concept 3: System Prompt as Agent DNA

**Video Teaching**:
> "The system prompt is the most important element of your custom agents, with zero exceptions."

**Code Implementation**:

Every custom agent demonstrates system prompt primacy:

```python
# apps/custom_1_pong_agent/pong_agent.py
def load_system_prompt():
    """System prompt completely defines behavior"""
    prompt_path = Path(__file__).parent / "prompts" / "PONG_AGENT_SYSTEM_PROMPT.md"
    return prompt_path.read_text()

# The system prompt IS the agent
agent = ClaudeCodeAgent(
    system_prompt=load_system_prompt()  # This changes everything
)
```

**Directory Structure Pattern**:
```
apps/custom_X_agent/
├── prompts/                    # System prompts are first-class citizens
│   └── AGENT_SYSTEM_PROMPT.md  # The agent's identity
├── agent.py                    # Implementation
```

---

### Concept 4: Tool Minimization

**Video Teaching**:
> "These are all the Claude code tools plus our tool. And so everything that's going into your agent winds up in the context window at some point."

**Code Implementation**:

Progressive tool control across agents:

```python
# apps/custom_2_echo_agent/echo_agent.py
# Problem identified: 15+ unnecessary tools
"Available tools: read, write, edit, bash, grep, glob..."

# apps/custom_3_calc_agent/calc_agent.py
# Solution: Explicit tool control
allowed_tools = ["custom_math_evaluator", "custom_unit_converter"]
# Only 2 tools instead of 15+

# apps/custom_5_qa_agent/qa_agent.py
# Advanced: Read-only tool restriction
allowed_tools = ["Read", "Grep", "Glob", "Task"]
disallowed_tools = ["Write", "Edit"]  # Explicit safety
```

---

### Concept 5: Custom Tool Creation

**Video Teaching**:
> "Tools for your Claude Code SDK, they're built like this, a decorator. The description of your tool tells your agent how to use it."

**Code Implementation**:

```python
# apps/custom_2_echo_agent/echo_agent.py
@tool(
    name="echo_tool",
    description="Echo a message with transformations"
)
def echo_tool(args: dict) -> str:
    """Custom tool implementation"""
    message = args.get("message", "")
    repeat = args.get("repeat", 1)
    transform = args.get("transform", "none")

    # Tool logic here
    result = apply_transform(message, transform)
    return " ".join([result] * repeat)

# Create in-memory MCP server
mcp_server = create_sdk_mcp_server([echo_tool])
```

---

### Concept 6: Fresh Agent Pattern

**Video Teaching**:
> "No matter what we prompt here, the response is always pong. Why is that?"

**Code Implementation**:

Scout-Plan-Build workflow demonstrates fresh agents:

```python
# .claude/commands/scout_plan_build.md
"""
1. Run SlashCommand(`/scout "[USER_PROMPT]"`) -> relevant_files
2. Run SlashCommand(`/plan_w_docs "[USER_PROMPT]" "[files]"`) -> plan
3. Run SlashCommand(`/build "[plan]"`) -> build_report
"""
# Each command is a fresh agent with no memory of previous

# Implementation in practice
def execute_workflow(requirement):
    # Fresh scout agent
    files = ScoutAgent().find_files(requirement)

    # Fresh planner (doesn't know scout's internal state)
    plan = PlannerAgent().create_plan(requirement, files)

    # Fresh builder (doesn't know planner's internal state)
    code = BuilderAgent().build(plan)
```

---

### Concept 7: Model Selection by Task

**Video Teaching**:
> "We have downgraded our model to a cheaper, less intelligent, but much faster model. This is a simple agent. It doesn't need powerful intelligence."

**Code Implementation**:

```python
# apps/custom_2_echo_agent/echo_agent.py
model="claude-3-haiku-20240307"  # Simple task, fast model

# apps/custom_3_calc_agent/calc_agent.py
model="claude-3-sonnet-20240229"  # Moderate complexity

# apps/custom_7_micro_sdlc_agent/backend/modules/agents.py
SONNET = "claude-3-5-sonnet-20241022"  # Complex planning
OPUS = "claude-3-opus-20240229"  # Deep analysis

# Model selection based on task complexity
```

---

### Concept 8: Interface Evolution

**Video Teaching**:
> "You can also use agents in terminal UIs... you can build up full agents as backend methods and as data streamers."

**Code Implementation**:

Progressive interface sophistication:

```python
# 1. Script Interface
apps/custom_1_pong_agent/  # Simple script execution

# 2. REPL Interface
apps/custom_3_calc_agent/  # Interactive terminal UI
"""
Calculator Agent> What tools do you have?
Calculator Agent> Convert 55 F to C
"""

# 3. Web Backend
apps/custom_6_tri_copy_writer/  # FastAPI + Vue.js
"""
backend/main.py: FastAPI server
frontend/: Vue.js application
"""

# 4. WebSocket Streaming
apps/custom_8_ultra_stream_agent/  # Real-time streaming
"""
async def websocket_endpoint(websocket: WebSocket):
    await manager.stream_to_client(websocket)
"""
```

---

### Concept 9: Multi-Agent Orchestration

**Video Teaching**:
> "Scale your compute to scale your impact... learn to delegate work to sub agents and new primary agents."

**Code Implementation**:

Micro SDLC Agent shows full orchestration:

```python
# apps/custom_7_micro_sdlc_agent/backend/modules/agents.py

class AgentOrchestrator:
    """Three specialized agents working together"""

    async def run_plan_agent(self, ticket):
        """Planner specialist"""
        agent = PlannerAgent()
        plan = await agent.create_plan(ticket.description)
        ticket.stage = "BUILD"

    async def run_build_agent(self, ticket):
        """Builder specialist"""
        agent = BuilderAgent()
        result = await agent.implement(ticket.plan_path)
        ticket.stage = "REVIEW"

    async def run_review_agent(self, ticket):
        """Reviewer specialist"""
        agent = ReviewerAgent()
        review = await agent.review(ticket.plan_path)
        ticket.stage = "SHIPPED" if review.passed else "ERRORED"
```

**Kanban Board Visualization**:
```
IDLE → PLAN → BUILD → REVIEW → SHIPPED/ERRORED → ARCHIVED
         ↑       ↑       ↑
      Planner Builder Reviewer
       Agent   Agent   Agent
```

---

### Concept 10: Domain-Specific Knowledge Injection

**Video Teaching**:
> "Custom agents let you pass your domain specific unique knowledge right to your agents."

**Code Implementation**:

Social Hype Agent demonstrates domain injection:

```python
# apps/custom_4_social_hype_agent/prompts/SOCIAL_HYPE_AGENT_SYSTEM_PROMPT.md
"""
You analyze social media posts from Bluesky's firehose.

Domain-specific knowledge:
- Bluesky post structure
- Social media sentiment patterns
- Trending topic identification
- User notification preferences
"""

# Domain-specific tool integration
async def monitor_firehose(keywords: List[str]):
    """Connect to Bluesky-specific WebSocket"""
    async with websockets.connect("wss://jetstream2.us-east.bsky.network") as ws:
        # Domain-specific protocol handling
```

---

## Implementation Patterns

### Pattern: Consistent Project Structure

**Teaching**: Organized, predictable structure

**Implementation**:
```
apps/custom_X_[name]_agent/
├── prompts/                  # Agent identity
│   └── [NAME]_AGENT_SYSTEM_PROMPT.md
├── [name]_agent.py          # Main implementation
├── modules/                 # Support code
├── README.md               # Documentation
├── pyproject.toml          # Dependencies
└── uv.lock                 # Lock file
```

### Pattern: Progressive Complexity

**Teaching**: Start simple, add complexity gradually

**Implementation**:
```python
# Level 1: Override system prompt
PongAgent: "Just change the prompt"

# Level 2: Add custom tools
EchoAgent: "Custom tools with MCP"

# Level 3: Add state management
CalcAgent: "REPL with conversation memory"

# Level 4: Add external integrations
SocialHypeAgent: "WebSocket + AI analysis"

# Level 5: Multi-agent systems
MicroSDLCAgent: "Orchestrated specialist teams"
```

### Pattern: Tool Progression

**Teaching**: Control your agent's capabilities

**Implementation**:
```python
# No tool restriction (default)
tools = None  # Gets all 15+ tools

# Allowed tools only
allowed_tools = ["Read", "Write", "Edit"]

# Custom tools only
custom_tools = [your_tool_1, your_tool_2]

# Mixed approach
allowed_tools = ["Read"] + custom_tools

# Explicit exclusion
disallowed_tools = ["Bash", "Write"]
```

---

## Advanced Concept Mappings

### Parallel Agent Execution

**Teaching**: "Scale your compute"

**Implementation**:
```python
# apps/custom_5_qa_agent/modules/agent.py
async def parallel_search(queries: List[str]):
    """Run multiple agents in parallel"""
    tasks = []
    for query in queries:
        task = Task(f"Search for: {query}")
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    return consolidate_results(results)
```

### Agent Cost Optimization

**Teaching**: "Template your engineering"

**Implementation**:
```python
# Track costs across all agents
session_stats = {
    "total_tokens": input_tokens + output_tokens,
    "cost": calculate_cost(model, tokens),
    "duration": end_time - start_time
}

# Optimize by model selection
if task_complexity == "simple":
    model = "haiku"  # $0.25 per million
elif task_complexity == "moderate":
    model = "sonnet"  # $3 per million
else:
    model = "opus"    # $15 per million
```

### Stream Processing Agents

**Teaching**: "Data streamers and processors"

**Implementation**:
```python
# apps/custom_8_ultra_stream_agent/backend/modules/agents.py
class StreamAgent:
    """Process infinite streams"""

    async def process_stream(self, jsonl_file):
        async for line in self.read_lines(jsonl_file):
            # Process in small batches
            batch = await self.collect_batch(3, 5)

            # Summarize with fresh context
            summary = await self.summarize_batch(batch)

            # Emit results
            await self.emit_summary(summary)

            # Clear context for next batch
            self.reset_context()
```

---

## Command Structure Mapping

### Scout Pattern

**Video Reference**: "Scout the codebase for files needed"

**Implementation**:
```markdown
# .claude/commands/scout.md
Find relevant files for the task using multiple search strategies:
1. Grep for keywords
2. Glob for patterns
3. Read key files
4. Follow dependencies
```

### Conditional Documentation

**Video Reference**: "Documentation that future agents read"

**Implementation**:
```markdown
# .claude/commands/conditional_docs.md
Load relevant documentation based on current task:
- If working with auth: load auth docs
- If working with API: load API docs
- If working with frontend: load component docs
```

### Expert Agents

**Video Reference**: "Domain expertise in agents"

**Implementation**:
```
.claude/commands/experts/
└── cc_hook_expert/
    ├── cc_hook_expert_plan.md
    ├── cc_hook_expert_build.md
    └── cc_hook_expert_improve.md
```

---

## Integration Points

### With TAC System

**TAC-3 (Planning)** → Planner Agent
**TAC-4 (Building)** → Builder Agent
**TAC-5 (Testing)** → Tester Agent
**TAC-6 (Review/Doc)** → Reviewer + Documenter Agents

### With ADW System

```python
# Each ADW step uses a specialized agent
adw_plan.py → PlannerAgent
adw_build.py → BuilderAgent
adw_test.py → TesterAgent
adw_review.py → ReviewerAgent
```

### With MCP Servers

```python
# Custom tools via MCP
mcp_server = create_sdk_mcp_server(custom_tools)
agent = ClaudeCodeAgent(mcp_servers=[mcp_server])
```

---

## Gaps and Opportunities

### Current Gaps

1. **No Agent Discovery System**
   - Opportunity: Build agent registry
   - Implementation: `AgentRegistry` class

2. **Limited Agent Communication**
   - Opportunity: Inter-agent messaging
   - Implementation: Message bus pattern

3. **No Agent Versioning**
   - Opportunity: Version control for prompts
   - Implementation: Prompt versioning system

4. **Basic Error Recovery**
   - Opportunity: Sophisticated retry logic
   - Implementation: Circuit breaker pattern

### Future Opportunities

1. **Agent Marketplace**
```python
class AgentMarketplace:
    """Share and discover specialized agents"""
    def publish(self, agent): ...
    def search(self, capability): ...
    def install(self, agent_id): ...
```

2. **Agent Learning**
```python
class LearningAgent:
    """Agents that improve over time"""
    def learn_from_success(self, task, result): ...
    def adapt_strategy(self): ...
```

3. **Meta-Agents**
```python
class MetaAgent:
    """Agents that create other agents"""
    def analyze_need(self, requirement): ...
    def generate_agent(self, specification): ...
```

---

## Summary

The Building Specialized Agents codebase is a comprehensive implementation of the video teachings. Key mappings:

1. **System Prompt = Agent Identity** (Pong Agent proves this)
2. **Tool Minimization = Performance** (Calc Agent demonstrates)
3. **Fresh Agents = Clean Context** (Scout-Plan-Build workflow)
4. **Specialization = Power** (Micro SDLC orchestration)
5. **Custom Tools = Domain Knowledge** (Social Hype monitoring)

The progression from simple prompt overrides to complex multi-agent systems shows the complete journey from "Better Agents" to "Custom Agents," with each implementation teaching a specific lesson about specialization.

Remember: **"The out-of-the-box agents are incredible, but there's a massive problem with these tools. They're built for everyone's codebase, not yours."** The implementations in this codebase show exactly how to build agents for YOUR specific needs.
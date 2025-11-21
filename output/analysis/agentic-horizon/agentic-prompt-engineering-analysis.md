# Agentic Prompt Engineering - Module Analysis

## Domain Overview: The Prompt as THE Fundamental Unit

This module teaches that **the prompt is THE fundamental unit of engineering** in the age of agents. It's not just about writing better prompts - it's about understanding prompts as the building blocks of all agentic systems, from simple tasks to complex orchestrations.

## Complete Structure

```
agentic-prompt-engineering/
├── .claude/
│   ├── agents/
│   │   ├── crypto-coin-analyzer.md    # Specialized crypto analysis agent
│   │   ├── docs-scraper.md            # Documentation fetching agent
│   │   └── meta-agent.md              # Agent that creates other agents
│   ├── commands/
│   │   ├── all_tools.md               # Level 1: High-level prompt
│   │   ├── build.md                   # Level 3: Control flow + Level 5: Higher order
│   │   ├── create_image.md            # Level 3: Control flow
│   │   ├── crypto_coin_analyzer_agent_prompt.md  # Domain-specific prompt
│   │   ├── experts/                   # Level 7: Self-improving prompts
│   │   │   └── cc_hook_expert/
│   │   │       ├── cc_hook_expert_build.md
│   │   │       ├── cc_hook_expert_improve.md
│   │   │       └── cc_hook_expert_plan.md
│   │   ├── load_ai_docs.md           # Level 4: Delegate prompt
│   │   ├── load_bundle.md            # Level 5: Higher order
│   │   ├── parallel_subagents.md     # Level 4: Delegate prompt
│   │   ├── plan_vite_vue.md          # Level 6: Template metaprompt
│   │   ├── prime.md                  # Level 2: Workflow prompt
│   │   ├── quick-plan.md             # Level 2: Workflow prompt
│   │   └── t_metaprompt_workflow.md  # Level 6: Template metaprompt
│   ├── hooks/
│   │   ├── context_bundle_builder.py  # Captures context for reuse
│   │   └── universal_hook_logger.py   # Logging infrastructure
│   ├── output-styles/                 # Control output token generation
│   │   ├── concise-done.md
│   │   ├── concise-tts.md
│   │   ├── concise-ultra.md
│   │   ├── verbose-bullet-points.md
│   │   └── verbose-yaml-structured.md
│   └── utils/                         # LLM and TTS utilities
│       ├── llm/
│       └── tts/
├── apps/
│   └── prompt_tier_list/              # Vue app for prompt evaluation
└── ai_docs/
```

## The 7 Levels of Prompt Mastery

### Level 1: High Level Prompt
- **Concept**: Static, reusable, adhoc prompts
- **Sections**: Title, High Level Prompt (required), Purpose
- **Examples**: `all_tools.md`, `start.md`
- **Mastery**: Understanding atomic prompt units

### Level 2: Workflow Prompt
- **Concept**: Sequential workflow with input→work→output
- **Sections**: Metadata, Workflow (required), Instructions, Variables, Report
- **Examples**: `prime.md`, `build.md`, `quick-plan.md`
- **Mastery**: Structuring complex tasks as workflows

### Level 3: Control Flow Prompt
- **Concept**: Conditions and loops within workflows
- **Examples**: `build.md`, `create_image.md`, `edit_image.md`
- **Mastery**: Dynamic execution based on context

### Level 4: Delegate Prompt
- **Concept**: Work delegation to other agents
- **Variables**: Agent config (model, count, tools)
- **Examples**: `parallel_subagents.md`, `load_ai_docs.md`, `background.md`
- **Mastery**: Orchestrating multiple agents

### Level 5: Higher Order Prompt
- **Concept**: Accept other prompts as input
- **Variables**: Prompt file variables
- **Examples**: `build.md`, `load_bundle.md`
- **Mastery**: Composable prompt architectures

### Level 6: Template Metaprompt
- **Concept**: Prompts that create other prompts
- **Sections**: Template (required)
- **Examples**: `t_metaprompt_workflow.md`, `plan_vite_vue.md`
- **Mastery**: Dynamic prompt generation

### Level 7: Self-Improving Prompt
- **Concept**: Prompts that update themselves or are updated by others
- **Sections**: Expertise (accumulated knowledge)
- **Examples**: `cc_hook_expert` series
- **Mastery**: Evolving prompt intelligence

## Advanced Concepts

### Prompt Section Architecture
The module defines 13 distinct prompt sections, each serving a specific purpose:

1. **Metadata**: YAML frontmatter for configuration
2. **Title**: Action-oriented naming
3. **Purpose**: High-level accomplishment description
4. **Variables**: Dynamic and static values
5. **Instructions**: Guidelines and constraints
6. **Relevant Files**: Context specification
7. **Codebase Structure**: Directory organization
8. **Workflow**: Numbered execution steps
9. **Expertise**: Accumulated domain knowledge
10. **Template**: Reusable patterns
11. **Examples**: Usage scenarios
12. **Report**: Output formatting

### System vs User Prompts
The module makes a critical distinction:

- **System Prompts**:
  - Set persistent rules for ALL conversations
  - Define agent identity and behavior
  - Cannot be changed mid-conversation
  - Require extensive testing

- **User Prompts**:
  - Request specific tasks
  - Can be refined with follow-ups
  - Work within system prompt constraints
  - Mistakes are easily corrected

### The Meta-Agent Pattern
The `meta-agent.md` demonstrates the pinnacle of prompt engineering - an agent that creates other agents:

```yaml
name: meta-agent
description: Generates new Claude Code sub-agent configuration files
tools: Write, WebFetch, mcp__firecrawl-mcp__firecrawl_scrape
model: opus
```

This agent:
1. Scrapes latest documentation
2. Analyzes user requirements
3. Devises agent name and color
4. Selects necessary tools
5. Constructs system prompt
6. Writes complete agent file

## Implementation Patterns

### Parallel Subagents Pattern
```markdown
## Workflow
1. Parse Input Parameters
2. Design Agent Prompts
   - Create self-contained prompts
   - Define clear output expectations
3. Launch Parallel Agents
   - Spawn N agents simultaneously
4. Collect & Summarize Results
```

### Expert Agent Pattern (Self-Improving)
```
Plan → Build → Improve
```
Each expert maintains:
- Domain-specific knowledge
- Accumulated patterns
- Self-documenting expertise

### Context Bundle Pattern
- Hooks capture file operations
- Store in `context_bundles/<session_id>.jsonl`
- Reload previous context instantly

## Real-World Applications

1. **Crypto Analysis Agent**: Real-time cryptocurrency evaluation
2. **Documentation Scraper**: Automated doc fetching and processing
3. **Prompt Tier List App**: Visual prompt evaluation system
4. **Expert Systems**: Self-improving domain specialists

## Integration with TAC Foundation

This module builds directly on TAC concepts:
- **TAC-1 to TAC-3**: Basic prompt engineering
- **TAC-4 to TAC-6**: Advanced prompt patterns
- **TAC-7 to TAC-8**: Multi-agent prompt orchestration

The quantum leap: Understanding prompts not as text, but as **engineering artifacts** that can be:
- Composed
- Delegated
- Generated
- Self-improved

## Production Considerations

1. **Token Economics**: Output styles control costs
2. **Prompt Versioning**: Track prompt evolution
3. **Testing Strategies**: Validate prompt behaviors
4. **Error Handling**: Graceful degradation patterns
5. **Performance**: Parallel execution for scale

## Expert-Level Insights

### The Prompt is THE API
In agentic systems, prompts are the API. They define:
- Input contracts (Variables)
- Processing logic (Workflow)
- Output contracts (Report)
- Side effects (Tool usage)

### Prompt Composition Theory
Higher-order prompts enable:
- Functional composition
- Dependency injection
- Strategy patterns
- Factory patterns

### The Evolution Path
1. Start with static prompts (Level 1)
2. Add workflows (Level 2)
3. Introduce control flow (Level 3)
4. Delegate to agents (Level 4)
5. Compose prompts (Level 5)
6. Generate prompts (Level 6)
7. Evolve prompts (Level 7)

## Key Takeaway

**"The prompt is THE fundamental unit of engineering."**

This module teaches that mastery comes not from writing better individual prompts, but from understanding prompts as composable, delegatable, generatable, and evolvable engineering artifacts. The 7 levels provide a clear progression from basic static prompts to self-improving prompt systems that learn and adapt.
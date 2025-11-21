# Agentic Engineering Glossary

## A

### ADW (Agentic Development Workflow)
A comprehensive system introduced in TAC-4 that automates the entire software development lifecycle from issue to pull request. ADW orchestrates specialized agents through a pipeline: classify → plan → implement → test → PR.
*See also: Pipeline Architecture, Agent Orchestration*

### Agent
An autonomous AI entity designed to perform specific tasks without human intervention. In Agentic Engineering, agents are specialized workers that handle distinct aspects of development (implementation, testing, documentation, etc.).
*See also: Specialized Agent, Multi-Agent System*

### Agent Orchestration
The practice of coordinating multiple agents to work together on complex tasks. Involves managing communication, state, and workflow between agents.
*See also: Multi-Agent System, MAO*

### Agentic Engineering
The discipline of building autonomous software development systems using AI agents. Unlike AI-assisted coding where AI helps humans write code, Agentic Engineering creates systems where AI agents independently develop software.
*See also: Autonomous Development, AI-Assisted Coding*

### Agentic Layer
A dedicated architectural layer (typically `.claude/` directory) that separates AI-driven development from application code. Contains commands, agents, workflows, and settings.
*See also: Separation of Concerns, Project Structure*

### Allow (Permission)
A permission setting that enables agents to perform actions automatically without asking for confirmation.
*See also: Ask, Deny, Permission Model*

### Ask (Permission)
A permission setting that requires agents to request confirmation before performing actions.
*See also: Allow, Deny, Permission Model*

### Autonomous Development
Software development performed independently by AI agents without human intervention, from requirements to deployment.
*See also: ADW, ZTE*

## B

### BFC (Bug/Feature/Chore)
A template pattern introduced in TAC-3 for structuring different types of development work. Each template provides specific workflows for bugs, features, and maintenance tasks.
*See also: Template Pattern, Structured Workflow*

### Browser Automation
Using tools like Playwright to automate web browser interactions for testing and validation. Introduced in TAC-5 for end-to-end testing.
*See also: E2E Testing, Playwright*

### Bundle (Context Bundle)
A technique from Elite Context Engineering where related context is packaged together for efficient reuse across agent calls.
*See also: Context Engineering, R&D Framework*

## C

### Chain of Thought
A prompting technique where agents explain their reasoning step-by-step, improving accuracy and transparency.
*See also: Prompt Engineering, Meta-Reasoning*

### CLAUDE.md
A special markdown file that provides project-specific context to Claude, reducing the need to repeat information in every command.
*See also: Context Optimization, Project Context*

### Claude CLI
The command-line interface tool for interacting with Claude, enabling execution of commands and workflows from the terminal.
*See also: Command Execution, Terminal Interface*

### Command
A reusable markdown file in `.claude/commands/` that defines agent behavior with instructions, variables, process steps, and reporting format.
*See also: Command as Component, Markdown Command*

### Command as Component Pattern
An architectural pattern where agent behaviors are encapsulated as reusable markdown commands that can be composed into workflows.
*See also: Command, Reusability, Composition*

### Conditional Documentation
Documentation that adapts based on context, user level, or system state. Introduced in TAC-6.
*See also: Self-Documentation, Dynamic Documentation*

### Context Engineering
The practice of optimizing how context (information, state, history) is managed and provided to agents for maximum performance.
*See also: R&D Framework, Context Window*

### Context Overflow
When an agent receives more context than it can process, leading to truncation or errors.
*See also: Context Window, Context Optimization*

### Context Window
The maximum amount of text/tokens an AI model can process in a single interaction.
*See also: Token Limit, Context Management*

## D

### Delegation Pattern
A strategy where complex tasks are broken down and delegated to specialized agents rather than handled by a single agent.
*See also: Multi-Agent System, Specialization*

### Deny (Permission)
A permission setting that prevents agents from performing specific actions.
*See also: Allow, Ask, Permission Model*

### Dynamic Documentation
Documentation that updates automatically based on code changes, execution results, or system state.
*See also: Self-Documentation, Documentation Agent*

## E

### E2E Testing (End-to-End Testing)
Comprehensive testing that validates entire workflows from start to finish, often using browser automation. Featured in TAC-5.
*See also: Testing Agent, Playwright*

### Echo Server
A simple agent type from the Horizon modules that demonstrates tool usage and message handling.
*See also: Specialized Agent, Agent Types*

### Elite Context Engineering
Advanced module in Agentic Horizon focusing on the R&D framework for optimizing agent performance through context management.
*See also: R&D Framework, Context Optimization*

### Execution Flow
The sequence of operations in an agentic system from trigger through orchestration, execution, validation, and integration.
*See also: Pipeline, Workflow*

## F

### Feature Template
A structured markdown template for implementing new features, part of the BFC pattern.
*See also: BFC, Template, Structured Development*

## G

### Git Worktree
A Git feature allowing multiple working directories for the same repository, used in TAC-7 for isolating agent work.
*See also: Worktree Isolation, Parallel Development*

### GitHub Integration
Connecting agentic systems with GitHub for issue tracking, pull requests, and version control automation.
*See also: ADW, Version Control*

## H

### Higher-Order Prompt
A prompt that generates or modifies other prompts. Level 5 in the prompt engineering hierarchy.
*See also: Meta-Prompt, Prompt Engineering*

### Horizon Modules
Advanced mastery modules covering Prompt Engineering, Building Specialized Agents, Elite Context Engineering, and Multi-Agent Orchestration.
*See also: Mastery Path, Advanced Patterns*

## I

### Implementation Agent
A specialized agent responsible for writing code based on specifications and requirements.
*See also: Specialized Agent, Code Generation*

### ISO (Issue-Solution-Outcome)
A comprehensive workflow pattern from TAC-7 that tracks development from problem identification through solution implementation to measurable outcomes.
*See also: Workflow Pattern, Traceability*

## L

### Learning Loop
A system where agents improve their performance based on past executions and outcomes.
*See also: Self-Improvement, Adaptive System*

## M

### MAO (Multi-Agent Orchestration)
The practice and patterns for coordinating multiple agents to work together on complex systems. Covered in Horizon modules.
*See also: Agent Orchestration, Distributed Systems*

### Markdown Command
A command defined in markdown format with structured sections for instructions, variables, process, and reporting.
*See also: Command, Command Structure*

### MCP (Model Context Protocol)
A protocol for efficiently managing and sharing context between agents and models.
*See also: Context Engineering, Protocol*

### Meta-Agent
An agent that creates, modifies, or manages other agents.
*See also: Agent Generator, Self-Organizing System*

### Meta-Prompt
A prompt that generates other prompts based on requirements or patterns.
*See also: Higher-Order Prompt, Prompt Template*

### Meta-Reasoning
The ability of agents to reason about their own reasoning process.
*See also: Chain of Thought, Self-Reflection*

### Minimum Viable Agent
An architectural pattern focusing on the simplest possible agent implementation that still provides value.
*See also: Architectural Patterns, MVP*

### Multi-Agent System
A system where multiple specialized agents work together to accomplish complex tasks.
*See also: Agent Orchestration, MAO*

## N

### Natural Language Control
Using natural language to direct agent orchestration systems rather than code or configuration.
*See also: Orchestrator, User Interface*

### NLQ (Natural Language Query)
Queries written in natural language that are translated to structured formats like SQL. Featured in TAC-2.
*See also: Query Translation, Natural Language*

## O

### Observability
The ability to monitor, track, and understand agent system behavior through logging, metrics, and tracing.
*See also: Monitoring, Debugging*

### Orchestrator
A master agent or system that coordinates multiple agents, managing their execution and communication.
*See also: Multi-Agent Orchestration, Coordination*

## P

### Permission Model
The system controlling what actions agents can perform (ask, allow, deny).
*See also: Security, Access Control*

### Pipeline Architecture
An architectural pattern where agents are arranged in a sequence, with each agent's output feeding into the next.
*See also: ADW, Sequential Processing*

### Playwright
A browser automation framework used for end-to-end testing in agentic systems.
*See also: E2E Testing, Browser Automation*

### Pong
The simplest agent type in the Horizon modules, demonstrating basic input/output.
*See also: Agent Types, Learning Path*

### Production System
An agentic system ready for real-world deployment with proper error handling, monitoring, and quality gates.
*See also: Enterprise Ready, Quality Gates*

### Project Structure
The organization of files and directories in an agentic project, typically including `.claude/`, `app/`, `specs/`, and `adws/`.
*See also: Agentic Layer, File Organization*

### Prompt Engineering
The practice of designing effective prompts for AI systems, ranging from basic to self-improving prompts.
*See also: Seven Levels, Prompt Taxonomy*

### Prompt Template
A reusable prompt structure with variable placeholders for dynamic content.
*See also: Template Pattern, Reusability*

## Q

### QA Agent
A specialized agent for quality assurance, including testing, validation, and review.
*See also: Testing Agent, Quality Gate*

### Quality Gate
Checkpoints in workflows that ensure standards are met before proceeding.
*See also: Validation, Production Standards*

## R

### R&D Framework (Reduce & Delegate)
A systematic approach to context optimization: Reduce unnecessary context and Delegate to specialized agents.
*See also: Context Engineering, Optimization*

### Reset-Prime Pattern
A context management technique where agent state is reset and re-initialized with essential context.
*See also: Context Management, State Reset*

### Review Agent
An agent specialized in code review, checking for quality, standards, and best practices.
*See also: Quality Assurance, Code Review*

## S

### SDLC (Software Development Life Cycle)
The complete process of software development from planning through deployment and maintenance.
*See also: Development Process, Workflow*

### SDLC Agent
A comprehensive agent from Horizon modules that handles the entire software development lifecycle.
*See also: Orchestration, Complete System*

### Self-Documentation
Systems that automatically generate and maintain their own documentation.
*See also: Documentation Agent, TAC-6*

### Self-Improving Prompt
Level 7 in the prompt taxonomy - prompts that learn and improve from their executions.
*See also: Learning Loop, Adaptive System*

### Self-Organizing System
A system where agents autonomously organize and coordinate without external orchestration.
*See also: Autonomous Systems, Emergence*

### Separation of Concerns
Architectural principle of keeping different aspects of the system (like AI logic and application code) separate.
*See also: Agentic Layer, Clean Architecture*

### Seven Levels (of Prompt Engineering)
The complete taxonomy from static to self-improving: Static → Workflow → Control Flow → Delegation → Higher Order → Template → Self-Improving.
*See also: Prompt Engineering, Mastery Path*

### Specialized Agent
An agent designed for a specific task or domain (e.g., testing, documentation, security).
*See also: Agent Types, Specialization*

### State Management
Maintaining context and information across agent executions and workflow steps.
*See also: Persistence, Context Management*

### Structured Workflow
A workflow with defined steps, inputs, outputs, and validation points.
*See also: BFC, Workflow Pattern*

## T

### TAC (Tactical Agentic Coding)
The foundational 8-module course teaching progressive agentic engineering concepts from basic commands to complex architectures.
*See also: Learning Path, Course Modules*

### Template Pattern
Using structured templates to ensure consistency and completeness in agent operations.
*See also: BFC, Command Template*

### Test Agent
An agent specialized in generating and running tests.
*See also: Testing Strategy, Automation*

### Testing Strategy
The approach to validating agent-generated code and ensuring quality.
*See also: E2E Testing, Validation*

### Token
The basic unit of text processed by language models, typically representing parts of words.
*See also: Token Limit, Context Window*

### Token Limit
The maximum number of tokens a model can process in one interaction.
*See also: Context Window, Optimization*

### Traceability
The ability to track decisions, changes, and outcomes throughout the development process.
*See also: ISO, Audit Trail*

### Tri-Copy
An agent type from Horizon modules demonstrating web application patterns.
*See also: Agent Types, Web Development*

## U

### Ultra Stream
An advanced agent type demonstrating dual-system architecture with streaming.
*See also: Agent Types, Advanced Patterns*

## V

### Validation Loop
A cycle where output is checked and corrected until it meets requirements.
*See also: Quality Gate, Testing*

### Variable (in Commands)
Dynamic inputs to commands that make them reusable with different parameters.
*See also: Command Structure, Parameters*

### Version Control
Managing changes to code and configurations, typically using Git.
*See also: Git, GitHub Integration*

## W

### WebSocket
A protocol for real-time bidirectional communication, used in multi-agent orchestration for streaming updates.
*See also: Streaming, Real-time Communication*

### Workflow
A sequence of steps or agent operations to accomplish a task.
*See also: Pipeline, Process*

### Workflow Pattern
Reusable workflow structures like ADW, ISO, and BFC.
*See also: Pattern Library, Best Practices*

### Worktree Isolation Pattern
Using Git worktrees to isolate agent work in separate directories, preventing conflicts.
*See also: Git Worktree, Parallel Development*

## Z

### Zero Touch Execution (ZTE)
Fully automated execution requiring no human intervention from start to finish.
*See also: Autonomous Development, Full Automation*

---

## Quick Reference: Key Acronyms

- **ADW**: Agentic Development Workflow
- **BFC**: Bug/Feature/Chore
- **CLI**: Command Line Interface
- **E2E**: End-to-End
- **ISO**: Issue-Solution-Outcome
- **MAO**: Multi-Agent Orchestration
- **MCP**: Model Context Protocol
- **MVP**: Minimum Viable Product
- **NLQ**: Natural Language Query
- **QA**: Quality Assurance
- **R&D**: Reduce & Delegate
- **SDLC**: Software Development Life Cycle
- **TAC**: Tactical Agentic Coding
- **ZTE**: Zero Touch Execution

---

## Cross-Reference Index

### By Module
- **TAC-1**: Paradigm Shift, Claude CLI, Permission Model
- **TAC-2**: NLQ, Command Structure, Project Organization
- **TAC-3**: BFC, Templates, Structured Workflows
- **TAC-4**: ADW, Pipeline Architecture, GitHub Integration
- **TAC-5**: E2E Testing, Playwright, Validation
- **TAC-6**: Self-Documentation, Knowledge Management
- **TAC-7**: ISO, Worktree Isolation, ZTE
- **TAC-8**: Architectural Patterns, Multiple Architectures
- **Horizon**: Advanced Patterns, MAO, R&D Framework

### By Concept Category
- **Architecture**: Agentic Layer, Pipeline, Patterns
- **Agents**: Specialized, Multi-Agent, Orchestration
- **Commands**: Structure, Variables, Templates
- **Context**: Engineering, R&D, Optimization
- **Testing**: E2E, Validation, Quality Gates
- **Workflow**: ADW, ISO, BFC, ZTE

---

*This glossary is a living document. As Agentic Engineering evolves, new terms and concepts will be added to maintain a comprehensive reference.*
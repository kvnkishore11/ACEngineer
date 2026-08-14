# 🗺️ CONCEPT MAPPING: Video Teachings to Code Implementation

## Bridging Theory and Practice in TAC-8

> **"The whole point here is to give you hands on quick starts you can use to build that V1, that proof of concept, that minimum viable agentic layer of your codebase."**

---

## 📹 Core Concepts from Video → 💻 Implementation in Code

### Concept 1: The Agentic Layer Ring

#### 🎥 What the Author Teaches (Video)

> **"Imagine a ring around your codebase. At first it's thin, then it becomes thicker as you scale agentics into your codebase."**

The author uses this powerful visual metaphor throughout:
- Start with a thin ring (basic automation)
- Make it thicker over time (more capabilities)
- The ring operates your application
- You work on the ring, not in the application

#### 💻 How It's Implemented (Code)

**App 1: Agent Layer Primitives**
```
project/
├── apps/                    # ← The center (application)
├── specs/                   # ← The ring begins
├── .claude/commands/        # ← The ring continues
├── adws/                    # ← The ring thickens
└── agents/                  # ← The ring completes
```

**The "thickness" is measured by**:
- Number of templates in `.claude/commands/`
- Complexity of workflows in `adws/`
- Coverage of problem classes in `specs/`

---

### Concept 2: One Agent, One Prompt, One Purpose

#### 🎥 What the Author Teaches (Video)

> **"The tactic is one agent one prompt one purpose. This unlocks massive Agentic Coding capabilities throughout the new agentic layer of your code base."**

The author warns against:
- Context pollution
- Context overloading
- Toxic context
- Confused agents from too much information

#### 💻 How It's Implemented (Code)

**App 1: Specialized Commands**
```markdown
# .claude/commands/prime.md
Purpose: Initialize agent understanding of codebase

# .claude/commands/start.md
Purpose: Start the application

# .claude/commands/chore.md
Purpose: Plan a chore

# .claude/commands/implement.md
Purpose: Implement a plan
```

**App 2: Workflow Separation**
```python
# adw_plan_build.py
# Agent 1: Planner
plan = agent.slash_command("/chore", description)

# Agent 2: Builder (fresh agent, new purpose)
result = agent.slash_command("/implement", plan_path)
```

**Key Implementation Detail**: Each slash command spawns a **fresh agent** with no prior context except what's explicitly passed.

---

### Concept 3: Prioritize Agentics (>50% Time)

#### 🎥 What the Author Teaches (Video)

> **"I recommend half of your engineering time, at least half, should be spent on the new agentic layer."**

The author emphasizes:
- This is an investment, not a cost
- The more you invest, the thicker the ring
- Clear your schedule for this
- Tell your boss, your team, yourself

#### 💻 How It's Implemented (Code)

**Evidence in Repository Structure**:
```
tac-8/
├── tac8_app1/
│   ├── apps/           # ~20% of code
│   └── [agentic]       # ~80% of code
├── tac8_app2/
│   ├── apps/           # ~30% of code
│   └── [agentic]       # ~70% of code
```

**Time Investment Visible in**:
- Detailed template engineering in `.claude/commands/`
- Sophisticated workflow orchestration in `adws/`
- Comprehensive logging in `agents/`
- Extensive documentation and specs

---

### Concept 4: Template Your Engineering

#### 🎥 What the Author Teaches (Video)

> **"These are meta prompts. They template out what your engineering workflows look like."**

The author explains:
- Don't solve one-off problems
- Solve problem classes
- Template your engineering patterns
- Create prompts that generate prompts

#### 💻 How It's Implemented (Code)

**App 1: Meta-Prompt Structure**
```markdown
# .claude/commands/chore.md
## Chore Planner Template

You are a planning specialist...

### Plan Format
1. Objective: [What we're doing]
2. Context: [Current state analysis]
3. Implementation Steps: [Detailed steps]
4. Success Criteria: [How we know it works]
```

**App 1: Template Execution**
```python
# adw_plan_build.py
# The template generates a plan
plan = agent.slash_command("/chore", "Add error handling to main.sh")
# Returns: specs/chore-[uuid]-add-error-handling.md
```

**Key Pattern**: Templates don't solve problems—they create problem-solving plans.

---

### Concept 5: Multi-Agent Parallel Execution

#### 🎥 What the Author Teaches (Video)

> **"We're working across five Git WorkTrees. They're just going to do engineering work for us, right? Across five WorkTrees."**

The author demonstrates:
- Parallel agent execution
- Git worktree isolation
- Task management system
- Automatic status updates

#### 💻 How It's Implemented (Code)

**App 2: Task Management System**
```markdown
# tasks.md
## Git Worktree enhance-model
[] Add cross-validation to sentiment classifier
[🟡, adw_12345] Implementing ensemble model
[✅ abc123, adw_12345] Added data augmentation

## Git Worktree optimize-performance
[] Profile and optimize inference speed
[] Implement caching layer
```

**App 2: Parallel Orchestration**
```python
# adw_triggers/adw_trigger_cron_todone.py
def process_all_worktrees():
    tasks = parse_tasks_file()
    processes = []

    for worktree, task_list in tasks.items():
        # Spawn separate process for each worktree
        p = Process(target=process_worktree, args=(worktree, task_list))
        p.start()
        processes.append(p)

    # Wait for all to complete
    for p in processes:
        p.join()
```

---

### Concept 6: ADW (AI Developer Workflow) Progression

#### 🎥 What the Author Teaches (Video)

> **"At first, you're fully in the loop... This is a great place to start. It's a great place to do deep work. It's a terrible place to stay."**

The progression taught:
1. In-loop (interactive Claude Code)
2. Slightly out-loop (slash commands)
3. Out-loop (ADWs)
4. Fully automated (triggers)

#### 💻 How It's Implemented (Code)

**Stage 1: In-Loop**
```bash
# Direct interaction in Claude Code terminal
$ claude
> /prime
> /start
> Please add error handling...
```

**Stage 2: Slash Commands**
```python
# adw_slash.py
agent.slash_command("/chore", "Add error handling")
```

**Stage 3: Composed ADWs**
```python
# adw_plan_build.py
plan = agent.slash_command("/chore", description)
result = agent.slash_command("/implement", plan)
```

**Stage 4: Triggered Automation**
```python
# adw_trigger_cron_todone.py
@schedule(every_5_minutes)
def automated_processing():
    tasks = get_pending_tasks()
    for task in tasks:
        process_automatically(task)
```

---

### Concept 7: Composable Primitives

#### 🎥 What the Author Teaches (Video)

> **"Keep your eyes on the primitives. Keep your eyes on the composable units of Agentic Coding that make up the work."**

The author emphasizes:
- Focus on the pieces, not the whole
- Primitives are atoms
- Compose them into molecules
- Build any structure needed

#### 💻 How It's Implemented (Code)

**Primitive Levels in Code**:

**Level 1: Prompt Primitives**
```markdown
# .claude/commands/analyze.md  (atomic)
Analyze the following code...
```

**Level 2: Agent Primitives**
```python
# adw_modules/agent.py  (molecular)
class Agent:
    def prompt(self, text): ...
    def slash_command(self, cmd, args): ...
```

**Level 3: Workflow Primitives**
```python
# adw_sdlc.py  (compound)
def sdlc_workflow(issue):
    plan = planner.execute(issue)
    code = builder.execute(plan)
    tests = tester.execute(code)
    return integrate(plan, code, tests)
```

**Level 4: System Primitives**
```python
# adw_trigger_system.py  (solution)
class AgenticSystem:
    def __init__(self):
        self.prompts = PromptLibrary()
        self.agents = AgentPool()
        self.workflows = WorkflowEngine()
        self.orchestrator = Orchestrator()
```

---

### Concept 8: The Application Layer Boundary

#### 🎥 What the Author Teaches (Video)

> **"Our application and our agents, right? They're distinctly different. Our apps is in a completely separate directory that our agentic layer, our agentic ring can operate around."**

The author stresses:
- Clear separation of concerns
- Agents operate ON the application
- Never mix agentic and application code
- The boundary is sacred

#### 💻 How It's Implemented (Code)

**Every App Maintains Strict Separation**:

```
tac8_app1/
├── apps/                    # APPLICATION LAYER
│   └── main.sh             # Never contains agent code
│
├── specs/                  # AGENTIC LAYER
├── .claude/                # AGENTIC LAYER
├── adws/                   # AGENTIC LAYER
└── agents/                 # AGENTIC LAYER
```

**Crossing the Boundary**:
```python
# Agents operate ON the application
agent.execute("cd apps && ./main.sh")  # Run app
agent.edit("apps/main.sh", changes)    # Modify app
agent.test("apps/", test_suite)        # Test app

# But never:
# apps/main.sh containing agent code ❌
# Mixing layers ❌
```

---

## 🔗 Connection Patterns

### Pattern 1: Video Concept → Multiple Implementations

**Concept**: "One Agent, One Prompt, One Purpose"

**Implementations**:
- App 1: Separate command files
- App 2: Fresh agents per task
- App 3: Specialized agent roles
- App 4: Single-purpose prototyping agents
- App 5: Domain-specific NLQ agents

### Pattern 2: Progressive Complexity

**Video Teaching**: "Start thin, make it thicker"

**Code Progression**:
```
App 1: Minimum viable (thin ring)
  ↓
App 2: Multi-agent (thicker)
  ↓
App 3: Observability (thicker)
  ↓
App 4: Rapid prototyping (thicker)
  ↓
App 5: Domain expertise (thickest)
```

### Pattern 3: Theory to Practice Bridge

| Video Theory | Code Practice |
|-------------|---------------|
| "Template your engineering" | Meta-prompts in `.claude/commands/` |
| "Solve problem classes" | Reusable specs and templates |
| "Scale through composition" | ADW pipeline combinations |
| "Parallel execution" | Git worktree isolation |
| "Stay out of the loop" | Trigger-based automation |

---

## 🎓 Learning Path Through Code

### For Beginners: Start with App 1

**Why**: Simplest implementation of core concepts
**Focus on**:
- Basic directory structure
- Simple prompts
- One ADW at a time
- Manual execution

### For Intermediate: Move to App 2

**Why**: Introduces parallelization and automation
**Focus on**:
- Task management system
- Multi-agent coordination
- Status tracking
- Automatic triggers

### For Advanced: Study Apps 3-5

**Why**: Production patterns and specialization
**Focus on**:
- Observability hooks (App 3)
- Rapid prototyping (App 4)
- Domain specialization (App 5)
- Complete systems

---

## 🔍 Hidden Implementations

### Things in Code Not Explicitly Taught in Video

1. **ADW ID Propagation**
   - Every workflow gets unique ID
   - Traced through entire execution
   - Enables debugging and auditing

2. **State Management**
   ```python
   # adw_state.json
   {
     "adw_id": "adw_12345",
     "status": "in_progress",
     "current_step": "building",
     "history": [...]
   }
   ```

3. **Error Recovery Mechanisms**
   - Retry logic in workflows
   - Fallback strategies
   - Graceful degradation

4. **Hook System for Observability**
   - Pre/post tool use hooks
   - Event streaming
   - Real-time monitoring

---

## 💡 Key Insights from Mapping

### Insight 1: The Gap Between Simple and Complex

The video makes it sound simple:
> "Just template your engineering"

The code shows the reality:
- Templates need error handling
- Workflows need state management
- Agents need isolation
- Systems need observability

### Insight 2: The Power of Separation

Video emphasizes separation conceptually.
Code enforces it architecturally:
- Physical directory separation
- Process isolation (worktrees)
- State boundaries
- Clean interfaces

### Insight 3: The Importance of Persistence

Video focuses on execution.
Code reveals persistence needs:
- Saving plans in `specs/`
- Logging in `agents/`
- State in `adw_state.json`
- Tasks in `tasks.md`

### Insight 4: The Orchestration Complexity

Video: "Run agents in parallel"
Code: Sophisticated orchestration including:
- Process management
- Resource allocation
- Conflict resolution
- Status synchronization

---

## 🎯 Practical Mapping Guide

### To Implement Video Concept → Find Code Pattern

| If Video Says... | Look in Code For... |
|-----------------|-------------------|
| "Template your engineering" | `.claude/commands/*.md` |
| "One agent, one purpose" | Fresh agent spawning in ADWs |
| "Solve problem classes" | Template meta-prompts |
| "Build the agentic layer" | Directory structure separation |
| "Parallel execution" | Git worktree + process spawning |
| "Stay out of the loop" | `adw_triggers/` directory |
| "Compose primitives" | ADW workflow combinations |
| "Track everything" | `agents/` logging directory |

---

## 🏁 Summary: The Complete Picture

### What Video Provides
- Vision and philosophy
- Mental models
- Conceptual framework
- Motivation and urgency

### What Code Provides
- Concrete implementation
- Practical patterns
- Error handling
- Production readiness

### Together They Create
- **Complete understanding** of agentic engineering
- **Practical ability** to implement systems
- **Confidence** to build production solutions
- **Framework** for continuous improvement

The mapping between video and code reveals that TAC-8 is not just theory—it's a **complete, production-ready system** for building the agentic layer that will transform how we engineer software.

---

*"Focus on the pieces that make the whole, from the individual agentic prompts up to the composed multi-step AI developer workflows. This is what matters."*

**The code is the pieces. The video is the vision. Together, they are mastery.**
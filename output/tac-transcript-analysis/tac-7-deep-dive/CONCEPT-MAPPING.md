# Concept Mapping: From Video to Code

## The Secret in Code

### Transcript Teaching
> "The secret of tactical agentic coding is that it's not about the software developer lifecycle at all. It's about composable agentic primitives you can use to solve any engineering problem class."

### Code Implementation
The TAC-7 codebase demonstrates this through:

#### 1. Composable ADW Files
```
adws/
├── adw_plan_iso.py          # Primitive: Planning
├── adw_build_iso.py         # Primitive: Building
├── adw_test_iso.py          # Primitive: Testing
├── adw_review_iso.py        # Primitive: Reviewing
├── adw_document_iso.py      # Primitive: Documenting
├── adw_ship_iso.py          # Primitive: Shipping
├── adw_patch_iso.py         # Primitive: Quick fixes
└── adw_sdlc_iso.py          # Composition: Full SDLC
```

Each file is a **primitive** that can be:
- Run independently
- Composed into workflows
- Parallelized across environments

#### 2. Arbitrary Compositions
Beyond SDLC, the code shows multiple compositions:
- `adw_plan_build_iso.py` - Just plan + build
- `adw_plan_build_test_iso.py` - Plan + build + test
- `adw_plan_build_review_iso.py` - Custom workflow
- `adw_patch_iso.py` - Skip planning for simple fixes

## ISO (Isolated) Workflows

### Transcript Teaching
> "We've adjusted all of our workflows to create their own isolated trees... In every tree, right, in every one of these directories, the application exists for a specific agent to build in."

### Code Implementation

#### Git Worktrees as Isolation Primitive
From `adw_modules/worktree_ops.py`:
- Each agent gets its own worktree
- Parallel execution without conflicts
- Complete environment isolation

#### State Management Primitive
From `adw_modules/state.py`:
- `ADWState` class manages workflow state
- Persistent across phases via `adw_state.json`
- Enables handoffs between primitives

## Zero Touch Engineering (ZTE)

### Transcript Teaching
> "This is YOLO mode for your AI developer workflows. This is high confidence mode for agenting engineering... No review, right? Just like you've stopped coding, you'll stop reviewing."

### Code Implementation

#### adw_sdlc_zte_iso.py
```python
# The complete ZTE workflow:
1. Plan (isolated)
2. Build (isolated)
3. Test (isolated)
4. Review (isolated)
5. Document (isolated)
6. Ship (approve & merge PR) 🚢  # THE KEY ADDITION

# Warning in the code:
"⚠️ WARNING: This will automatically merge to main if all phases pass!"
```

#### adw_ship_iso.py - The Shipping Primitive
```python
def manual_merge_to_main(branch_name: str, logger: logging.Logger):
    """Manually merge a branch to main using git commands."""
    # Fetches latest
    # Checks out main
    # Merges feature branch
    # Pushes to origin/main
```

## One Agent, One Prompt, One Purpose

### Transcript Teaching
> "We have one agent, one prompt, one purpose. This unlocks massive Agentic Coding capabilities throughout the new agentic layer of your code base."

### Code Implementation

#### Specialized Agent Prompts
From `agents/prompts/`:
- Each agent has a single, focused prompt
- Clear purpose and boundaries
- No context pollution

#### Agent Composition in ADWs
```python
# From adw_sdlc_iso.py
# Each phase is a separate agent with one purpose:
plan = subprocess.run([...,"adw_plan_iso.py"])     # One purpose: Plan
build = subprocess.run([...,"adw_build_iso.py"])   # One purpose: Build
test = subprocess.run([...,"adw_test_iso.py"])     # One purpose: Test
```

## Model Sets and Compute Scaling

### Transcript Teaching
> "Our model set changes the set of models that runs against our workflow... It gives us a little knob to turn to increase the compute that our workflow uses."

### Code Implementation

#### From agents.py
```python
# Base models vs Heavy models
MODEL_MAP = {
    "/plan": "base_model",
    "/plan_forward_opus": "heavy_model",
    # Different compute for different problems
}
```

#### Information Dense Keywords (IDKs)
- `model_set: heavy` - Scales compute up
- `think` - Activates reasoning
- `iso` - Triggers isolation

## The Agentic Layer

### Transcript Teaching
> "We're building the system that builds the system. We're not solving the problem directly anymore."

### Code Implementation

#### Layer Structure
```
tac-7/
├── adws/           # AI Developer Workflows (highest level)
├── agents/         # Agent primitives
├── prompts/        # Prompt primitives
├── specs/          # Planning artifacts
├── app_docs/       # Documentation artifacts
└── ai_docs/        # Conditional documentation
```

#### Self-Referential System
- Agents read their own documentation
- Workflows improve based on past runs
- State persists across executions

## Parallelization

### Transcript Teaching
> "We have not one issue, not two issues, three, four, five issues. Getting tackled by our agentic pipelines, right? By our AI developer workflows. This is all happening in parallel."

### Code Implementation

#### Worktree-based Parallelization
```python
# Each workflow gets unique:
- Worktree directory: trees/{adw_id}/
- Port allocation: 3000-3999 range
- State file: adw_state.json
- Branch name: {type}/task_issue_{number}_{adw_id}
```

#### From workflow_ops.py
```python
def ensure_adw_id(issue_number: str, adw_id: Optional[str] = None):
    """Ensure we have an ADW ID and initialized state."""
    # Generates unique ID if not provided
    # Initializes isolated environment
    # Returns ID for tracking
```

## Feedback Loops

### Transcript Teaching
> "Documentation provides feedback on work done for future agents to reference in their work."

### Code Implementation

#### Conditional Documentation System
From `ai_docs/`:
- Agents contribute documentation
- Future agents pull relevant docs
- System learns from each run

#### Review Screenshots
From review workflows:
- Agents take screenshots as proof
- Visual validation of features
- Automated verification

## The Peter → Pete Evolution

### Transcript Teaching
> "You'll drop yourself off the end of the Outloop Peter framework and it becomes Pete not Peter you'll drop off the review."

### Code Implementation

#### Peter Framework (with Review)
```python
# adw_sdlc_iso.py - Still has human review
plan → build → test → review → document
# Human reviews PR before merge
```

#### Pete Framework (No Review)
```python
# adw_sdlc_zte_iso.py - Drops human review
plan → build → test → review → document → ship
# Automatically merges if all pass
```

## Problem Classes vs One-offs

### Transcript Teaching
> "We're not solving one-off problems anymore. All we've been doing is showcasing what this could look like inside of the agentic layer."

### Code Implementation

#### Problem Class Templates
- `feature` - Full SDLC workflow
- `bug` - Targeted fix workflow
- `chore` - Simple update workflow
- `patch` - Minimal change workflow

#### Workflow Selection
From `classify_adw.py`:
```python
# Automatically selects workflow based on:
- Issue type (feature/bug/chore)
- Complexity markers
- Model set requirements
```

## Summary: The Code Proves The Secret

The TAC-7 codebase perfectly demonstrates that **the SDLC is just one possible composition**:

1. **Primitives are everywhere**: Each Python file is a primitive
2. **Compositions are flexible**: Multiple workflow combinations exist
3. **Isolation enables scale**: Worktrees allow parallel execution
4. **State enables handoffs**: JSON state connects primitives
5. **The system builds itself**: Self-documenting and self-improving

The secret is visible in the code structure itself - it's not a monolithic SDLC system, but a **collection of composable primitives** that can be arranged in any pattern needed to solve engineering problems.
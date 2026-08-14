# Plan: Parallel Team Duplication — UI Generation B/C & Validation B/C

## Task Description
Add two additional UI Generation teams (B, C) and two additional Validation teams (B, C) to the multi-team config for 3x parallel generation throughput. The new teams reuse the exact same agent prompt files — no copies, no new agents. Branches are assigned via round-robin across all available teams for instant parallelism. A new `parallel-mental-model-updates` skill teaches shared agents that their mental model file has concurrent readers/writers.

## Objective
When complete, the orchestrator can round-robin assign branches across three generation teams and three validation teams, tripling throughput. No TillDone task list — we test whether the orchestrator can coordinate three parallel teams using only its conversation context and `trees.yaml`. Shared agents are aware their mental model is a living, concurrent document.

## Problem Statement
The current system generates branches sequentially — one at a time through a single UI Generation team, then one at a time through a single Validation team. For 3 branches this is fine. For 6+ it's slow, and at 9+ it's a bottleneck. By adding two more instances of each team (same agents, different team names), the orchestrator can distribute work across three parallel pipelines. Because agents are reused across teams, their mental model files become shared concurrent state — agents need a skill to handle this correctly.

## Solution Approach
Pure horizontal scaling via team duplication in config only, with round-robin assignment for instant parallelism.

Key design decisions:
- **Reuse agent files** — B and C teams reference the same `.md` files and mental models as the original teams. No copies. The Pi runtime spawns separate instances per team conversation.
- **Config-only change** — four new team blocks in `multi-team-config.yaml`, each pointing to existing agent paths.
- **Round-robin routing** — the orchestrator assigns branches to teams in a cycle: branch 1 → UI Generation, branch 2 → UI Generation B, branch 3 → UI Generation C, branch 4 → UI Generation, etc. No thresholds, no tiers. Every run uses all available teams instantly.
- **Shared mental models** — since agents are reused, their expertise YAML files have concurrent readers/writers. A new skill (`parallel-mental-model-updates`) teaches agents that siblings exist, write errors mean retry, and sibling entries are fair game to read, build on, or correct.
- **No TillDone** — the orchestrator tracks state through conversation context + `trees.yaml`. We intentionally skip the task list to see where coordination breaks at scale.

## Relevant Files
Use these files to complete the task:

- `.pi/multi-team/multi-team-config.yaml` — add four new team blocks (UI Generation B/C, Validation B/C) that reference existing agent files
- `.pi/multi-team/agents/orchestrator.md` — update delegation instructions for round-robin parallel routing
- `.pi/prompts/multi-team/generate.md` — update workflow for round-robin parallel generation
- `.pi/prompts/multi-team/fork-leaf.md` — update workflow for round-robin parallel forking
- `.pi/prompts/multi-team/validate.md` — update workflow for round-robin parallel validation
- `.pi/prompts/multi-team/rebrand.md` — update workflow for round-robin parallel rebranding
- `.pi/prompts/multi-team/new-branch.md` — no change (single branch, single team)
- `.pi/multi-team/skills/mental-model.md` — reference for skill format and structure

Agent files that need `skills` frontmatter updated to include the new skill (read-only otherwise):
- `.pi/multi-team/agents/ui-generation-lead.md`
- `.pi/multi-team/agents/vue-generator.md`
- `.pi/multi-team/agents/animation-specialist.md`
- `.pi/multi-team/agents/validation-lead.md`
- `.pi/multi-team/agents/soft-validator.md`
- `.pi/multi-team/agents/hard-validator.md`

### New Files
- `.pi/multi-team/skills/parallel-mental-model-updates.md` — skill teaching shared agents how to handle concurrent mental model reads/writes

## Implementation Phases

### Phase 1: Skill + Config
Create the `parallel-mental-model-updates` skill. Add four new team blocks to `multi-team-config.yaml`.

### Phase 2: Agent Frontmatter + Orchestrator + Workflows
Add the new skill to all 6 shared agent frontmatters. Update orchestrator prompt with round-robin delegation. Update workflow prompts with round-robin patterns.

### Phase 3: Validation
Read all modified files end-to-end. Verify config is valid YAML, paths resolve, skill is referenced correctly.

## Team Orchestration

- You operate as the team lead and orchestrate the team to execute the plan.
- You're responsible for deploying the right team members with the right context to execute the plan.
- IMPORTANT: You NEVER operate directly on the codebase. You use `Task` and `Task*` tools to deploy team members to to the building, validating, testing, deploying, and other tasks.
  - This is critical. You're job is to act as a high level director of the team, not a builder.
  - You're role is to validate all work is going well and make sure the team is on track to complete the plan.
  - You'll orchestrate this by using the Task* Tools to manage coordination between the team members.
  - Communication is paramount. You'll use the Task* Tools to communicate with the team members and ensure they're on track to complete the plan.
- Take note of the session id of each team member. This is how you'll reference them.

### Team Members

- Builder
  - Name: skill-builder
  - Role: Create the parallel-mental-model-updates skill file and add it to all 6 shared agent frontmatters
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: config-and-orchestrator
  - Role: Add four new team blocks to multi-team-config.yaml and update orchestrator.md with round-robin parallel delegation routing
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: workflow-updater
  - Role: Update the 4 workflow prompts (generate, fork-leaf, validate, rebrand) with round-robin parallel team patterns
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: validator
  - Role: Read all modified files end-to-end, verify config paths resolve, check for consistency
  - Agent Type: general-purpose
  - Resume: false

## Step by Step Tasks

### 1. Create Parallel Mental Model Skill + Update Agent Frontmatters
- **Task ID**: create-skill
- **Depends On**: none
- **Assigned To**: skill-builder
- **Agent Type**: general-purpose
- **Parallel**: true (can run alongside tasks 2 and 3)
- Create `.pi/multi-team/skills/parallel-mental-model-updates.md` following the exact format of existing skills (see `.pi/multi-team/skills/mental-model.md` for structure). The skill content:

```markdown
---
name: parallel-mental-model-updates
description: Handle shared mental model files when running as one of multiple parallel team instances. Siblings may be reading and writing the same file concurrently — retry on write errors, ingest sibling work.
---

# Parallel Mental Model Updates

## Instructions

Your mental model expertise file is shared with sibling instances of yourself running in parallel teams. When the orchestrator scales work across multiple teams (UI Generation, UI Generation B, UI Generation C), each team gets its own agent instance — but they all read and write the same expertise YAML file.

You have full read/write access. Update the file exactly as you normally would — restructure, merge, trim, overwrite sections. The only difference: **you're not the only one writing.**

### Write Errors

If a write fails or you get a conflict error, it's because a sibling agent is writing to the same file at the same time. This is expected. Just:

1. Re-read the file to get the latest version
2. Apply your changes on top of the current content
3. Write again

Don't panic, don't skip the update. Just retry.

### Sibling Awareness

When you read your mental model, you may find entries you didn't write — a sibling added them during their parallel work. This is normal and valuable:

- **Ingest their learnings.** If a sibling recorded a useful pattern or observation, apply it to your own work. Their context is your context.
- **Build on their entries.** If you have additional insight on something a sibling noted, enrich the entry rather than duplicating it.
- **Correct if wrong.** If a sibling entry is outdated or incorrect based on what you've observed, update or remove it. You have full ownership of the file — treat sibling entries the same as your own.

### What This Means

- You're not alone. Siblings are generating/validating different branches in parallel.
- The mental model file gets richer faster with parallel teams — lean into that.
- Write errors are not bugs. They're coordination signals. Re-read, re-apply, retry.
```

- Then update the YAML frontmatter `skills` section in all 6 shared agent files to add the new skill. Add this entry to each agent's `skills` list:
  ```yaml
  - path: .pi/multi-team/skills/parallel-mental-model-updates.md
    use-when: Always. Your mental model file is shared with sibling instances in parallel teams.
  ```
- Agent files to update:
  - `.pi/multi-team/agents/ui-generation-lead.md`
  - `.pi/multi-team/agents/vue-generator.md`
  - `.pi/multi-team/agents/animation-specialist.md`
  - `.pi/multi-team/agents/validation-lead.md`
  - `.pi/multi-team/agents/soft-validator.md`
  - `.pi/multi-team/agents/hard-validator.md`
- Do NOT modify any agent instructions or other frontmatter fields. Only add the new skill entry to the `skills` list.

### 2. Add B and C Team Blocks to Config + Update Orchestrator
- **Task ID**: update-config
- **Depends On**: none
- **Assigned To**: config-and-orchestrator
- **Agent Type**: general-purpose
- **Parallel**: true (can run alongside tasks 1 and 3)
- Read `.pi/multi-team/multi-team-config.yaml`
- Append four new team blocks after the existing Validation team. These reuse the same agent files:

```yaml
  - team-name: UI Generation B
    team-color: "#2ad6d0"
    consult-when: >
      Second generation team for parallel workloads. Same capabilities as
      UI Generation. Orchestrator round-robins branches across generation teams.
    lead:
      name: UI Generation Lead
      path: .pi/multi-team/agents/ui-generation-lead.md
      color: "#2ad6d0"
    members:
      - name: Vue Generator
        path: .pi/multi-team/agents/vue-generator.md
        color: "#00b8d4"
        consult-when: >
          Vue SFC component authoring, Composition API,
          layout structure, state management, routing
      - name: Animation Specialist
        path: .pi/multi-team/agents/animation-specialist.md
        color: "#6bb8e8"
        consult-when: >
          CSS transitions, Vue transition components,
          micro-interactions, scroll animations, motion design

  - team-name: UI Generation C
    team-color: "#1abfa0"
    consult-when: >
      Third generation team for parallel workloads. Same capabilities as
      UI Generation. Orchestrator round-robins branches across generation teams.
    lead:
      name: UI Generation Lead
      path: .pi/multi-team/agents/ui-generation-lead.md
      color: "#1abfa0"
    members:
      - name: Vue Generator
        path: .pi/multi-team/agents/vue-generator.md
        color: "#00a0b8"
        consult-when: >
          Vue SFC component authoring, Composition API,
          layout structure, state management, routing
      - name: Animation Specialist
        path: .pi/multi-team/agents/animation-specialist.md
        color: "#5aa0d0"
        consult-when: >
          CSS transitions, Vue transition components,
          micro-interactions, scroll animations, motion design

  - team-name: Validation B
    team-color: "#e8825a"
    consult-when: >
      Second validation team for parallel workloads. Same capabilities as
      Validation. Orchestrator round-robins branches across validation teams.
    lead:
      name: Validation Lead
      path: .pi/multi-team/agents/validation-lead.md
      color: "#e8825a"
    members:
      - name: Soft Validator
        path: .pi/multi-team/agents/soft-validator.md
        color: "#e8a06c"
        consult-when: >
          Screenshot capture, visual regression, brand token compliance,
          layout correctness, typography adherence
      - name: Hard Validator
        path: .pi/multi-team/agents/hard-validator.md
        color: "#d4657e"
        consult-when: >
          Interactive testing, click flows, responsive breakpoints,
          accessibility audit, animation performance

  - team-name: Validation C
    team-color: "#d06a48"
    consult-when: >
      Third validation team for parallel workloads. Same capabilities as
      Validation. Orchestrator round-robins branches across validation teams.
    lead:
      name: Validation Lead
      path: .pi/multi-team/agents/validation-lead.md
      color: "#d06a48"
    members:
      - name: Soft Validator
        path: .pi/multi-team/agents/soft-validator.md
        color: "#d08858"
        consult-when: >
          Screenshot capture, visual regression, brand token compliance,
          layout correctness, typography adherence
      - name: Hard Validator
        path: .pi/multi-team/agents/hard-validator.md
        color: "#c05068"
        consult-when: >
          Interactive testing, click flows, responsive breakpoints,
          accessibility audit, animation performance
```

- Then update `.pi/multi-team/agents/orchestrator.md` — add a new section `### Parallel Delegation` after the existing `### Delegation Order` section:

```markdown
### Parallel Delegation

You have three UI Generation teams and three Validation teams:
- **UI Generation**, **UI Generation B**, **UI Generation C** — identical capabilities, same agents
- **Validation**, **Validation B**, **Validation C** — identical capabilities, same agents

**Round-robin assignment — always use all teams:**

Assign branches to teams in a repeating cycle. No thresholds, no tiers — every generation run distributes across all available teams instantly.

```
Branch 1 → UI Generation
Branch 2 → UI Generation B
Branch 3 → UI Generation C
Branch 4 → UI Generation
Branch 5 → UI Generation B
...
```

**How to execute:**
1. After Setup scaffolds all branches, assign each branch to a team via round-robin
2. Delegate to all assigned generation teams in parallel — be explicit about which branch slugs each team owns
3. After all generation teams complete, assign the same branches to validation teams via the same round-robin pattern
4. Delegate to all assigned validation teams in parallel
5. Collect results from all teams and delegate final status update to **Setup**

**Example — 7 branches:**
- UI Generation: branches 1, 4, 7
- UI Generation B: branches 2, 5
- UI Generation C: branches 3, 6
- (same assignment for validation teams)

**Important:** All teams write to the same filesystem. Each branch directory is independent, so there are no write conflicts as long as each team works on its assigned branches only. Be explicit in your delegation about which branch slugs each team should work on.
```

- Do NOT remove or modify any existing orchestrator content. Only ADD the new section.

### 3. Update Workflow Prompts
- **Task ID**: update-workflows
- **Depends On**: none
- **Assigned To**: workflow-updater
- **Agent Type**: general-purpose
- **Parallel**: true (can run alongside tasks 1 and 2)
- Read all 4 workflow files first, then update each:
- Update `.pi/prompts/multi-team/generate.md` — this is the primary target. Modify the workflow steps to use round-robin parallel assignment:
  - After step 2 (Brand), replace the single-team delegation with: "Assign branches to generation teams via round-robin: branch 1 → **UI Generation**, branch 2 → **UI Generation B**, branch 3 → **UI Generation C**, branch 4 → **UI Generation**, etc. Delegate to all teams in parallel."
  - Same round-robin for validation: "Assign branches to validation teams via the same round-robin. Delegate to all teams in parallel."
  - Failure handling: route fixes back to whichever team generated the failing branch
- Update `.pi/prompts/multi-team/fork-leaf.md` — same round-robin pattern for distributing forks across generation and validation teams
- Update `.pi/prompts/multi-team/validate.md` — round-robin branches across **Validation**, **Validation B**, **Validation C**
- Update `.pi/prompts/multi-team/rebrand.md` — round-robin across both generation and validation teams based on branch list
- Do NOT modify `.pi/prompts/multi-team/new-branch.md` — single branch always uses single team (UI Generation only)
- Keep the existing workflow structure intact. Add round-robin parallel logic, don't restructure from scratch.

### 4. Validate All Changes
- **Task ID**: validate-all
- **Depends On**: create-skill, update-config, update-workflows
- **Assigned To**: validator
- **Agent Type**: general-purpose
- **Parallel**: false
- Read `multi-team-config.yaml` end-to-end — verify all 8 team blocks are well-formed YAML
- For every `path:` value in the config, verify the referenced file exists on disk
- Read `.pi/multi-team/skills/parallel-mental-model-updates.md` — verify it exists and has correct frontmatter format
- Read all 6 shared agent files — verify each has the new skill in its `skills` frontmatter list
- Read orchestrator.md — verify the new parallel delegation section uses round-robin (not tiers) and doesn't conflict with existing delegation order rules
- Read all 4 updated workflow prompts — verify they reference all team names ("UI Generation B", "UI Generation C", "Validation B", "Validation C") and use round-robin assignment
- Verify YAML is valid: `python3 -c "import yaml; yaml.safe_load(open('.pi/multi-team/multi-team-config.yaml'))"`
- Report any issues found

## Acceptance Criteria
- `multi-team-config.yaml` has 8 teams: Setup, Brand, UI Generation, UI Generation B, UI Generation C, Validation, Validation B, Validation C
- All new team entries reference the same agent `.md` files as originals (no new agent files created)
- `.pi/multi-team/skills/parallel-mental-model-updates.md` exists with correct frontmatter
- All 6 shared agent files have the new skill in their `skills` frontmatter
- Orchestrator prompt uses round-robin assignment (no tier thresholds)
- `generate.md`, `fork-leaf.md`, `validate.md`, `rebrand.md` all use round-robin parallel patterns
- `new-branch.md` is unchanged (single branch = single team)
- No existing agent instructions are modified — only frontmatter `skills` list additions
- Config YAML parses without errors

## Validation Commands
Execute these commands to validate the task is complete:

- `grep -c 'team-name:' .pi/multi-team/multi-team-config.yaml` — should return 8
- `cat .pi/multi-team/skills/parallel-mental-model-updates.md | head -3` — should show valid frontmatter
- `grep 'parallel-mental-model-updates' .pi/multi-team/agents/vue-generator.md` — should match
- `grep 'parallel-mental-model-updates' .pi/multi-team/agents/ui-generation-lead.md` — should match
- `grep 'parallel-mental-model-updates' .pi/multi-team/agents/validation-lead.md` — should match
- `grep 'parallel-mental-model-updates' .pi/multi-team/agents/soft-validator.md` — should match
- `grep 'parallel-mental-model-updates' .pi/multi-team/agents/hard-validator.md` — should match
- `grep 'parallel-mental-model-updates' .pi/multi-team/agents/animation-specialist.md` — should match
- `grep 'round-robin' .pi/multi-team/agents/orchestrator.md` — should match
- `grep 'UI Generation B' .pi/prompts/multi-team/generate.md` — should match
- `grep 'UI Generation C' .pi/prompts/multi-team/generate.md` — should match
- `grep 'Validation B' .pi/prompts/multi-team/validate.md` — should match
- `grep 'Validation C' .pi/prompts/multi-team/validate.md` — should match
- `python3 -c "import yaml; yaml.safe_load(open('.pi/multi-team/multi-team-config.yaml')); print('YAML valid')"` — should print "YAML valid"
- Verify no new agent `.md` files: `ls .pi/multi-team/agents/` — should have same file count as before

## Notes
- This is a prototype to test whether the orchestrator can coordinate three parallel teams with round-robin assignment without a dedicated task list (TillDone). If the orchestrator struggles with tracking which team owns which branch at 9+ branches, that's the signal to add TillDone.
- All new teams reuse the exact same agent files. At runtime, the Pi system spawns separate agent instances per team conversation, so there's no state conflict. Each team's agents operate in their own conversation thread.
- Mental model files ARE shared across team instances. The `parallel-mental-model-updates` skill handles this — agents know siblings exist, retry on write errors, and treat sibling entries as their own (read, build on, correct, or remove). Full update access, not append-only.
- The orchestrator is the only component that needs to know about the parallel pattern. Team leads and members are unaware of A/B/C — they just do their work on whatever branches they're assigned. The new skill only teaches them about shared mental models, not about team topology.
- `new-branch.md` is intentionally left unchanged. Single-branch generation always routes to UI Generation (first in the round-robin).
- 3 generation teams × 3 agents each = 9 concurrent generation agents at max scale. 3 validation teams × 3 agents each = 9 concurrent validation agents. Total system: 18 concurrent agents at peak (plus Setup, Brand, and Orchestrator).

---
description: Generate N variant branches for a tree
argument-hint: <brand> <product> <tree> <count> <prompt>
---

# Purpose
Generate multiple variant branches — the main workhorse for producing UI at scale.

## Variables
BRAND: $1
PRODUCT: $2
TREE: $3
COUNT: $4
PROMPT: $5

## Instructions
- The UI Generation Lead decides how to differentiate each variant
- Auto-name branches: `$TREE-v1` through `$TREE-v$COUNT`
- If tree doesn't exist, create it first via Setup
- All variants must use brand tokens — no hardcoded values
- Each variant should explore a different layout, emphasis, or style approach

## Workflow
1. Delegate to **Setup** team:
   - Create tree if it doesn't exist
   - Scaffold $COUNT branch directories with auto-generated slugs
   - Add all branches to `trees.yaml` (status: generating)
   - Write `activity.yaml` alongside `trees.yaml` with `active: true`, pipeline: `generate`, the user's brief text, and a branch list with each branch's slug, tree, phase: `scaffolding`, and team: `TBD`
   - Run Zod validation
2. Delegate to **Brand** team:
   - Load `brand.yaml`, prepare brand context
3. Delegate to **UI Generation** team:
   - UI Gen Lead creates $COUNT differentiated briefs from: "$PROMPT"
   - Each variant should explore a different layout, emphasis, or style approach
   - All must use brand tokens from brand.yaml
4. Assign branches to generation teams via round-robin and delegate in parallel:
   - Branch 1 → **UI Generation**, Branch 2 → **UI Generation B**, Branch 3 → **UI Generation C**, Branch 4 → **UI Generation**, etc.
   - Each team's Vue Generator builds its assigned variants
   - Update `activity.yaml` — set each branch's phase to `generating` and assign the team name
5. Delegate to **Setup** team:
   - Update each branch status in `trees.yaml`: `generating` → `validating`
   - Update `activity.yaml` — set each branch's phase to `validating`
6. Assign branches to validation teams via the same round-robin and delegate in parallel:
   - Branch 1 → **Validation**, Branch 2 → **Validation B**, Branch 3 → **Validation C**, Branch 4 → **Validation**, etc.
   - Soft + hard validate all assigned variants
   - Report which pass and which fail
   - Update `activity.yaml` — assign the validation team name
7. For any failures:
   - Route fixes back to whichever generation team generated the failing branch
   - Route re-validation back to the corresponding validation team
8. Delegate to **Setup** team:
   - Update each branch status in `trees.yaml`: `validating` → `validated` (if passed) or `failed` (if not)
   - Clear `activity.yaml` by setting `active: false`

## Report
Generated $COUNT variants in tree "$TREE" for brand "$BRAND":
- Passed: N/$COUNT
- [List each variant with status and route path]
- Browse: `/gallery/$TREE/`

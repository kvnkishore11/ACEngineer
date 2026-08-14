---
description: Fork an existing leaf N times with specified changes
argument-hint: <brand> <product> <tree> <branch> <count> <prompt>
---

# Purpose
Take an existing validated component and create N variations with specific modifications.

## Variables
BRAND: $1
PRODUCT: $2
TREE: $3
BRANCH: $4
COUNT: $5
PROMPT: $6

## Instructions
- Source leaf must exist at `apps/infinite-ui/src/brands/$BRAND/products/$PRODUCT/trees/$TREE/$BRANCH/index.vue`
- Each fork should be a distinct interpretation of the requested changes
- Name forks: `$BRANCH-fork-1` through `$BRANCH-fork-$COUNT`
- Maintain brand consistency across all forks

## Workflow
1. Delegate to **Setup** team:
   - Verify source leaf exists
   - Read source `index.vue`
   - Scaffold $COUNT new branch directories
   - Add to `trees.yaml` (status: `generating`, forkedFrom: `$BRANCH`)
   - Write `activity.yaml` alongside `trees.yaml` with `active: true`, pipeline: `fork-leaf`, the user's brief text, and a branch list with each branch's slug, tree, phase: `scaffolding`, and team: `TBD`
   - Run Zod validation
2. Delegate to **Brand** team:
   - Load brand context
3. Assign forks to generation teams via round-robin and delegate in parallel:
   - Fork 1 → **UI Generation**, Fork 2 → **UI Generation B**, Fork 3 → **UI Generation C**, Fork 4 → **UI Generation**, etc.
   - Each team reads the source index.vue and produces its assigned variations applying: "$PROMPT"
   - Each fork should be a distinct interpretation of the changes
   - Maintain brand consistency across all forks
   - Update `activity.yaml` — set each branch's phase to `generating` and assign the team name
4. Delegate to **Setup** team:
   - Update each branch status in `trees.yaml`: `generating` → `validating`
   - Update `activity.yaml` — set each branch's phase to `validating`
5. Assign forks to validation teams via the same round-robin and delegate in parallel:
   - Fork 1 → **Validation**, Fork 2 → **Validation B**, Fork 3 → **Validation C**, Fork 4 → **Validation**, etc.
   - Soft + hard validate each fork
   - Update `activity.yaml` — assign the validation team name
6. For any failures:
   - Route fixes back to whichever generation team produced the failing fork
   - Route re-validation back to the corresponding validation team
7. Delegate to **Setup** team:
   - Update each branch status in `trees.yaml`: `validating` → `validated` (if passed) or `failed` (if not)
   - Clear `activity.yaml` by setting `active: false`

## Report
Forked "$BRANCH" into $COUNT variations:
- Source: `/gallery/$TREE/$BRANCH`
- [List each fork with status and how it differs]

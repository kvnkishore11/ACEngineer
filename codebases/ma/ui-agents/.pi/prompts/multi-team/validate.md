---
description: Run validation on specific or all branches
argument-hint: <brand> <product> [tree] [branch]
---

# Purpose
Run the validation pipeline on branches — scoped to a single branch, a tree, or all.

## Variables
BRAND: $1
PRODUCT: $2
TREE: $3 (optional — blank = all trees)
BRANCH: $4 (optional — blank = all branches in tree)

## Instructions
- Determine scope from provided arguments
- No generation happens here unless explicitly fixing
- Update statuses after validation

## Workflow
1. Delegate to **Setup** team:
   - Read `trees.yaml`, determine validation scope
   - If $TREE and $BRANCH → validate one branch
   - If $TREE only → validate all branches in that tree
   - If neither → validate ALL branches in ALL trees
2. Delegate to **Brand** team:
   - Load `brand.yaml` for compliance reference
3. Assign branches in scope to validation teams via round-robin and delegate in parallel:
   - Branch 1 → **Validation**, Branch 2 → **Validation B**, Branch 3 → **Validation C**, Branch 4 → **Validation**, etc.
   - Soft validate each branch (screenshot + brand check)
   - Hard validate branches that pass soft (interaction + responsive)
4. Delegate to **Setup** team:
   - Update statuses in `trees.yaml` (validated / failed)

## Report
Validation complete for "$BRAND" (scope: $TREE $BRANCH):
- Passed: N/N
- [List failures with reasons]

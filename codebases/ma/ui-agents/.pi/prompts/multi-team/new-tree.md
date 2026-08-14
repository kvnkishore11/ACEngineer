---
description: Add a new tree to a product's hierarchy
argument-hint: <brand> <product> <tree-slug> <prompt>
---

# Purpose
Create a new tree (purpose category) within a product's hierarchy.

## Variables
BRAND: $1
PRODUCT: $2
TREE: $3
PROMPT: $4

## Instructions
- Tree slug must be lowercase kebab-case
- Only the Setup team is needed
- trees.yaml must pass Zod validation after update
- Create the directory even though it has no branches yet

## Workflow
1. Delegate to **Setup** team:
   - Create directory: `apps/infinite-ui/src/brands/$BRAND/products/$PRODUCT/trees/$TREE/`
   - Add tree entry to `trees.yaml`: slug "$TREE", description based on "$PROMPT", empty branches
2. Delegate to **Setup** team (Structure Validator):
   - Validate `trees.yaml` via Zod

## Report
Tree "$TREE" created in product "$PRODUCT" (brand "$BRAND").
- Ready for branches via `/new-branch` or `/generate`

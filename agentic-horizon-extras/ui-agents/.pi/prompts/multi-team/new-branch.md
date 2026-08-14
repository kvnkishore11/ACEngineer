---
description: Scaffold and generate a single branch with full validation
argument-hint: <brand> <product> <tree> <branch-slug> <prompt>
---

# Purpose
Create a single branch — scaffold the directory, generate the Vue component, and validate it.

## Variables
BRAND: $1
PRODUCT: $2
TREE: $3
BRANCH: $4
PROMPT: $5

## Instructions
- Full pipeline: Setup → Brand → UI Generation → Validation → Setup
- If the tree doesn't exist yet, create it first
- The generated component must use brand CSS custom properties exclusively — no hardcoded colors/fonts
- Validation failures trigger regen with specific fix instructions

## Workflow
1. Delegate to **Setup** team:
   - Create `apps/infinite-ui/src/brands/$BRAND/products/$PRODUCT/trees/$TREE/$BRANCH/`
   - Stub `index.vue` with brand token imports
   - Add branch to `trees.yaml` (status: generating)
   - Run Zod validation
2. Delegate to **Brand** team:
   - Load `brand.yaml`, prepare brand tokens + constraints brief
3. Delegate to **UI Generation** team:
   - Generate `index.vue` from: "$PROMPT"
   - Use brand context from step 2
   - Component must be responsive using brand breakpoints
4. Delegate to **Validation** team:
   - Soft validate: screenshot + brand compliance check
   - Hard validate: interaction + responsive test
   - If fail → send fix instructions to UI Generation, re-validate
5. Delegate to **Setup** team:
   - Update `trees.yaml` status to `validated` or `failed`

## Report
Branch "$BRANCH" in tree "$TREE" for brand "$BRAND":
- Status: [validated/failed]
- Preview: `/gallery/$TREE/$BRANCH`

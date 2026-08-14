---
description: Create a new brand from the _template reference app
argument-hint: <brand-slug> <prompt>
---

# Purpose
Create a new brand by copying the _template reference app and customizing it.

## Variables
BRAND: $1
PROMPT: $2

## Instructions
- Brand slug must be lowercase kebab-case
- The _template app is the copy source — never modify _template itself
- After copy, reset trees.yaml to empty manifest
- Use $PROMPT to guide the brand identity — tone, audience, visual direction, palette mood, etc.
- Zod validation must pass before reporting success

## Workflow
1. Delegate to **Setup** team:
   - Copy `apps/infinite-ui/src/brands/_template/` → `apps/infinite-ui/src/brands/$BRAND/`
   - Find-replace `_template` → `$BRAND` across all config files
   - Reset `trees.yaml` to: `{ version: 1, brand: "$BRAND", trees: [] }`
   - Update `brand.yaml` name field to "$BRAND"
2. Delegate to **Brand** team:
   - Customize `brand.yaml` based on: "$PROMPT"
   - Set palette, typography, tone, audience, identity fields to match the prompt
3. Delegate to **Setup** team (Structure Validator):
   - Run Zod validation on `brand.yaml` and `trees.yaml`
   - Verify directory structure matches expectations

## Report
Brand "$BRAND" created successfully.
- Path: `apps/infinite-ui/src/brands/$BRAND/`
- Next: add a product with `/new-product $BRAND <product-name>`

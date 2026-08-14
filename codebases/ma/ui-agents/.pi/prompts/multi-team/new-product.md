---
description: Create a new product within a brand
argument-hint: <brand> <product-slug> <prompt>
---

# Purpose
Create a new product within an existing brand by copying the _template-product.

## Variables
BRAND: $1
PRODUCT: $2
PROMPT: $3

## Instructions
- Product slug must be lowercase kebab-case
- Copy from `_template/products/_template-product/` — never modify the template itself
- The brand-level brand.yaml at `apps/infinite-ui/src/brands/$BRAND/brand.yaml` must already exist
- Use $PROMPT to guide the product identity — what it does, who it's for, any brand overrides
- Reset trees.yaml to empty manifest

## Workflow
1. Delegate to **Setup** team:
   - Copy `apps/infinite-ui/src/brands/_template/products/_template-product/` → `apps/infinite-ui/src/brands/$BRAND/products/$PRODUCT/`
   - Find-replace `_template-product` → `$PRODUCT` across config files
   - Reset `trees.yaml` to: `{ version: 1, brand: "$BRAND", product: "$PRODUCT", trees: [] }`
2. Delegate to **Brand** team:
   - Based on: "$PROMPT", decide if a product-level `brand.yaml` override is needed
   - If the product has a distinct sub-identity (different palette, tagline, audience), create the override
   - If it inherits the brand identity fully, leave absent
3. Delegate to **Setup** team (Structure Validator):
   - Validate merged brand.yaml (brand-level + product-level) via Zod
   - Validate trees.yaml via Zod

## Report
Product "$PRODUCT" created in brand "$BRAND".
- Path: `apps/infinite-ui/src/brands/$BRAND/products/$PRODUCT/`
- Start dev server: `just dev`
- Next: create trees with `/new-tree $BRAND $PRODUCT <tree> <description>`

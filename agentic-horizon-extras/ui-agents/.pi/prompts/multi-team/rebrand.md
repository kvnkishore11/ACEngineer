---
description: Re-validate and update all branches after brand.yaml changes
argument-hint: <brand> [product] <prompt>
---

# Purpose
Apply brand changes described in the prompt, update brand.yaml, and cascade to all existing components. If product is specified, only rebrand that product. If omitted, rebrand all products in the brand.

## Variables
BRAND: $1
PRODUCT: $2 (optional — blank = all products in brand)
PROMPT: $3

## Instructions
- Use $PROMPT to guide what brand changes to make (palette shifts, typography changes, tone updates, etc.)
- Brand team applies the changes to brand.yaml, then identifies affected tokens
- Every existing branch gets re-validated against new tokens
- Failing branches get fixed by UI Generation
- This can be expensive — it touches every branch

## Workflow
1. Delegate to **Brand** team:
   - Apply changes from: "$PROMPT" to `brand.yaml`
   - Identify which tokens changed
   - Produce rebrand brief listing affected tokens
2. Assign all existing branches to validation teams via round-robin and delegate in parallel:
   - Branch 1 → **Validation**, Branch 2 → **Validation B**, Branch 3 → **Validation C**, etc.
   - Re-validate against new tokens
   - Set all to status: validating in `trees.yaml`
   - Report which pass and which fail
3. Assign failing branches to generation teams via round-robin and delegate in parallel:
   - Failure 1 → **UI Generation**, Failure 2 → **UI Generation B**, Failure 3 → **UI Generation C**, etc.
   - Fix each failing branch to match new brand identity
4. Assign fixed branches to validation teams via round-robin and delegate in parallel:
   - Re-validate fixed branches
5. Delegate to **Setup** team:
   - Update all statuses in `trees.yaml` (validated or failed)

## Report
Rebrand complete for "$BRAND":
- Branches compliant: N/N
- [List any that required fixes and what changed]

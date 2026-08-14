---
description: Natural language command — describe what you want and the orchestrator routes to the right workflow
argument-hint: <prompt>
---

# Purpose
Accept a natural language request and route it to the correct workflow. This is the catch-all command — users describe what they want in plain English, and you figure out which workflow(s) to execute.

## Variables
PROMPT: $1

## Instructions
- Parse the user's natural language $PROMPT
- Identify which workflow(s) to execute based on intent
- Extract the required arguments (brand, product, tree, branch, count) from context
- If arguments are ambiguous or missing, check existing brands/products/trees to infer them
- If you truly can't infer, ask — but try hard to figure it out first
- You may chain multiple workflows in sequence if the request spans them

## Workflow Reference

Match the user's intent to these workflows:

### Creating things
- **New brand** → `/new-brand <brand-slug> <prompt>` — "create a brand", "new brand called X", "set up a brand for Y"
- **New product** → `/new-product <brand> <product-slug> <prompt>` — "add a product", "create a product for X"
- **New tree** → `/new-tree <brand> <product> <tree-slug> <prompt>` — "add a landing page category", "create a tree for dashboards"

### Generating UI
- **Single branch** → `/new-branch <brand> <product> <tree> <branch-slug> <prompt>` — "make one hero section", "generate a single pricing page"
- **Multiple variants** → `/generate <brand> <product> <tree> <count> <prompt>` — "generate 6 landing pages", "make 3 dashboard variants", "create N versions of X"
- **Fork existing** → `/fork-leaf <brand> <product> <tree> <branch> <count> <prompt>` — "fork hero-v1 with darker colors", "take the split layout and make 3 variations"

### Brand changes
- **Rebrand** → `/rebrand <brand> [product] <prompt>` — "change the palette to warmer tones", "update typography to use Poppins", "make it more playful"

### Quality
- **Validate** → `/validate <brand> <product> [tree] [branch]` — "check if everything passes", "validate the landing pages", "re-run validation"
- **Status** → `/status <brand> <product>` — "what's the status", "how many are validated", "show me the overview"

## Routing Rules
1. Read $PROMPT carefully. Identify the primary intent.
2. If the request involves creating structure (brand, product, tree) AND generating UI, chain the workflows: create first, then generate.
3. If the request is ambiguous between workflows, prefer the more specific one (e.g., "make a hero" is `/new-branch`, not `/generate` with count=1).
4. If the user references an existing brand/product/tree by name, verify it exists before proceeding. Use `just list-brands`, `just list-products`, etc. to check.
5. If the user doesn't specify a count for generation, default to 3.
6. Pass the user's original language through as the $PROMPT argument to whichever workflow you invoke — don't strip context.

## Examples

"Create a SaaS brand called nextra with a clean blue palette and generate 5 landing page heroes"
→ `/new-brand nextra "clean blue palette, SaaS, professional"` then `/new-product nextra app "main SaaS application"` then `/generate nextra app landing 5 "landing page heroes, clean blue palette"`

"Make the aegis palette darker and more cyberpunk"
→ `/rebrand aegis "darker palette, cyberpunk aesthetic, neon accents on dark backgrounds"`

"Generate 9 pricing page variants for aegis cuts"
→ `/generate aegis cuts pricing 9 "pricing page variants"`

"What's the status of aegis cuts?"
→ `/status aegis cuts`

"Fork the hero-centered landing with a more minimal approach, 3 versions"
→ `/fork-leaf aegis cuts landing hero-centered 3 "more minimal approach, reduce visual density"`

## Report
Report the result of you and your teams work.

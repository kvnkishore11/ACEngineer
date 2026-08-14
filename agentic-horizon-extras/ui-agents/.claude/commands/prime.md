---
description: Prime context for the UI Agents infinite UI generation system
---

# Purpose

Explore the UI Agents project — a multi-team agent system that generates brand-consistent Vue user interfaces at scale. Brands define visual identity, products contain generated UI trees, and 12 specialized agents collaborate through an orchestrator to scaffold, generate, validate, and maintain the UI components.

## Instructions

- When working on the Multi Team system. Keep these rules in mind.
  - Leads and Orchestrators are thinkers, planners and managers. They are not doers. Other than updating their own mental models, they should not write files.
  - Workers are doers. They are the ones who write files. They make changes to the system.

## Workflow

1. Run `git ls-files | head -120` using the Bash tool to see the full project structure
2. Read `README.md` for project overview, hierarchy, commands, and architecture summary
3. Read `.pi/multi-team/multi-team-config.yaml` — team configuration: Orchestrator + 4 teams (Setup, Brand, UI Generation, Validation), each with a Lead + Members, shared context paths
4. Read `.pi/multi-team/agents/orchestrator.md` — how it routes requests to the right team, always calling Setup first for structural changes and last for status updates
5. Read `.pi/multi-team/agents/setup-lead.md` (first 50 lines) — owns trees.yaml integrity, coordinates scaffold + validate workers
6. Read `.pi/multi-team/agents/vue-generator.md` (first 50 lines) — how Vue components are generated using only CSS custom properties from brand tokens
7. Read `apps/infinite-ui/src/schemas/brand.schema.ts` — the Zod schema defining the full brand.yaml contract (palette, typography, spacing, breakpoints, shadows, motion, identity, assets)
8. Read `apps/infinite-ui/src/schemas/trees.schema.ts` — the Zod schema for trees.yaml (manifest of trees, branches, statuses)
9. Read `apps/infinite-ui/src/stores/brand.ts` (first 60 lines) — how brand config is loaded with deep merge (brand-level + product-level override), route-based context switching
10. Read `apps/infinite-ui/src/brands/_template/brand.yaml` — the template brand identity (copy source for new brands)
11. Read `apps/infinite-ui/src/brands/aegis/products/app/trees.yaml` — example of a populated product manifest with validated branches
12. Read one generated leaf: `apps/infinite-ui/src/brands/aegis/products/app/trees/dashboard/v1-grid-gauge/index.vue` (first 80 lines) — see how agents write Vue components using brand CSS custom properties
13. Read `.pi/prompts/multi-team/generate.md` — the main workflow command that drives the full generation pipeline (Setup → Brand → UI Gen → Validation → Setup)
14. Read `justfile` — all available recipes: team, dev, list commands, workflow shortcuts
15. Read `scripts/list.py` (first 40 lines) — the uv inline script CLI for listing brands/products/trees/branches
16. Summarize your understanding:
    - **Purpose**: Infinite brand-consistent UI generation via multi-team agent orchestration
    - **Hierarchy**: Brand → Product → Tree → Branch → Leaf (5 levels)
    - **Architecture**: Single Vue app at `apps/infinite-ui/`, all brands/products under `src/brands/`. One dev server serves everything.
    - **Agent teams**: Setup (scaffold + validate), Brand (identity + compliance), UI Generation (Vue SFCs + animation), Validation (Playwright screenshots + accessibility)
    - **Brand system**: `brand.yaml` at brand level (global), optional product-level override (deep-merged). All components use CSS custom properties — no hardcoded values.
    - **Generation pipeline**: `/generate` → Setup scaffolds → Brand prepares brief → UI Gen writes components → Validation checks via Playwright → Setup marks validated
    - **Key files**: `multi-team-config.yaml` (teams), `brand.schema.ts` + `trees.schema.ts` (contracts), `brand.ts` store (merge + tokens), `.pi/prompts/multi-team/*.md` (9 workflow commands)
    - **Nav**: Floating breadcrumb bar (Ctrl+H), overlay sidebar with brand editor (Ctrl+S), VueFlow canvas with dagre layout
    - **Mental models**: Agents maintain `.pi/multi-team/expertise/*.yaml` files that compound knowledge across sessions

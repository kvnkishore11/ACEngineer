# specs/init.md — UI Agents Implementation Plan

## Overview

Phased implementation plan for the ui-agents infinite UI generation system. Each phase has **builder agents** and **validator agents**. Validators use `/playwright-bowser` for concrete UI verification when applicable. All agents run on **Claude Opus 4.6**.

**Source of truth:** `DEBRIEF.md` — all architecture decisions, schemas, store designs, team configs, and workflow prompts are defined there.

**Total phases:** 7
**Total agents:** 14 (7 builders + 7 validators)

### Agent Prereading Convention

Every agent (builder and validator) has a **Prereading** section listing files and skills they must read before starting work. This ensures agents have full context and activate the right skills for their task. Prereading is not optional — it is step 0 of every agent's work.

### Key Skills

| Skill | When to Activate | What It Does |
|-------|-------------------|-------------|
| `/meta-agent` | Phase 7 builder — creating agent `.md` files | Provides the correct frontmatter structure, field reference, and agent creation workflow |
| `/meta-prompt` | Phase 6 builder — creating workflow prompt files | Provides the 6-section template for reusable slash commands |
| `/playwright-bowser` | All validators with UI to test | Headless browser automation for screenshots, DOM verification, interaction testing |

---

## Phase 1: Project Scaffolding + Zod Schemas

**Goal:** Initialize the `_template` Vue app with correct directory structure, install dependencies, create Zod schemas, and set up the Vite build.

### Builder: `phase-1-builder`

**Model:** `claude-opus-4-6`

**Prereading:**
- `DEBRIEF.md` — sections: App Structure, brand.yaml, trees.yaml, Zod Validation Schema
- `apps/infinite-ui/_template/` — verify current state before scaffolding

**Tasks:**

1. Create the two-level template structure:
   ```bash
   mkdir -p apps/infinite-ui/_template/_template-product
   cd apps/infinite-ui/_template/_template-product
   bun create vite . --template vue-ts
   bun add vue-router pinia @vue-flow/core @vue-flow/background @vue-flow/minimap zod yaml
   bun add -D @types/node
   ```

2. Create directory structure inside `_template-product/` per DEBRIEF.md `App Structure`:
   ```
   src/schemas/
   src/stores/
   src/brand/
   src/layout/
   src/canvas/
   src/gallery/
   src/trees/
   screenshots/
   public/assets/
   ```

3. Create `src/schemas/brand.schema.ts` — copy the Zod schema exactly as defined in DEBRIEF.md section "Zod Validation Schema" (the `BrandSchema` export)

4. Create `src/schemas/trees.schema.ts` — copy the Zod schema exactly as defined in DEBRIEF.md section "Zod Validation Schema" (the `TreesManifestSchema`, `TreeSchema`, `BranchSchema` exports)

5. Create **brand-level** `brand.yaml` at `apps/infinite-ui/_template/brand.yaml` — the global template brand identity. Use the "Acme Corp" placeholder with all fields (full Zod validation must pass):
   ```yaml
   name: _template
   tagline: "Template brand — copy me to create a new brand"
   tone: bold, obvious, placeholder
   audience: developers setting up new brands
   ```
   Use the full palette/typography/spacing/breakpoints/shadows/motion/assets structure from DEBRIEF.md but with intentionally obvious placeholder colors (hot pink `#ff1493` as primary, lime green `#32cd32` as secondary)

6. Create **product-level** `brand.yaml` at `apps/infinite-ui/_template/_template-product/brand.yaml` — a partial override example:
   ```yaml
   name: _template-product
   tagline: "Template product — demonstrates product-level override"
   ```
   This file is intentionally minimal to demonstrate that products only override what they need.

7. Create `src/trees/trees.yaml` with one example tree:
   ```yaml
   version: 1
   brand: _template
   trees:
     - slug: example
       name: Example Tree
       description: Demonstrates the tree/branch/leaf hierarchy
       icon: sparkles
       branches:
         - slug: variant-a
           name: Variant A
           description: First example variant
           created: "2026-03-31"
           status: validated
           screenshot: null
         - slug: variant-b
           name: Variant B
           description: Second example variant
           created: "2026-03-31"
           status: validated
           screenshot: null
   ```

8. Create example leaves:
   - `src/trees/example/variant-a/index.vue` — simple Vue SFC that uses brand CSS custom properties (`var(--brand-primary)`, etc.) to render a heading, paragraph, and CTA button
   - `src/trees/example/variant-b/index.vue` — different layout, same brand tokens

9. Create `vite.config.ts` with the `brandSyncPlugin` as defined in DEBRIEF.md — exposes `GET/POST /api/brand` (brand-level), `GET/POST /api/brand/product` (product-level override), and `GET/POST /api/trees` endpoints. The plugin takes three paths: brand-level brand.yaml (one dir up), product-level brand.yaml (local), and trees.yaml.

10. Create `index.html` with basic Vue mount point

11. Create `src/main.ts` — bootstrap Vue app with router and Pinia

### Validator: `phase-1-validator`

**Model:** `claude-opus-4-6`

**Prereading:**
- `DEBRIEF.md` — sections: App Structure, Zod Validation Schema
- `apps/infinite-ui/_template/` — verify builder output

**Tasks:**

1. **Schema validation** — write a test script and run it:
   ```bash
   cd apps/infinite-ui/_template
   bun run -e "
     import { BrandSchema } from './src/schemas/brand.schema';
     import { TreesManifestSchema } from './src/schemas/trees.schema';
     import * as yaml from 'yaml';
     import * as fs from 'fs';
     const brand = yaml.parse(fs.readFileSync('brand.yaml', 'utf-8'));
     const trees = yaml.parse(fs.readFileSync('src/trees/trees.yaml', 'utf-8'));
     console.log('Brand:', BrandSchema.parse(brand).name);
     console.log('Trees:', TreesManifestSchema.parse(trees).trees.length, 'trees');
     console.log('PASS: Both schemas validate');
   "
   ```

2. **Build check** — verify the app compiles:
   ```bash
   cd apps/infinite-ui/_template && bun run build
   ```

3. **Directory structure check** — verify all expected directories and files exist per DEBRIEF.md `App Structure`

4. **Vite dev server check** — start dev server, verify it boots without errors:
   ```bash
   cd apps/infinite-ui/_template && timeout 10 bun run dev 2>&1 || true
   ```

**Exit criteria:** Zod parses both YAML files without errors. `bun run build` succeeds. All directories exist.

---

## Phase 2: Pinia Stores + Brand Tokens

**Goal:** Implement all four Pinia stores and the brand token system so CSS custom properties are reactive.

### Builder: `phase-2-builder`

**Model:** `claude-opus-4-6`

**Prereading:**
- `DEBRIEF.md` — sections: Pinia Stores (all 4 store specs), Brand Save → Cascade Flow
- `apps/infinite-ui/_template/src/schemas/brand.schema.ts` — know the types you're working with
- `apps/infinite-ui/_template/src/schemas/trees.schema.ts` — know the types you're working with
- `apps/infinite-ui/_template/brand.yaml` — the data you're loading

**Tasks:**

1. Create `src/stores/brand.ts` — implement `useBrandStore` exactly as specified in DEBRIEF.md `Pinia Stores > brandStore`:
   - `config` ref, `isDirty` ref, `lastSaved` ref
   - `tokens` computed (all `--brand-*`, `--font-*`, `--space-*`, `--radius-*`, `--container-*`, `--duration-*`, `--easing`, `--bp-*`, `--shadow-*` CSS custom properties)
   - `cssVars` computed (joined string)
   - `load()` action — **brand merge logic**: fetch `/api/brand` (brand-level, full), fetch `/api/brand/product` (product-level, partial, may 404), deep-merge brand + product, validate merged result via `BrandSchema`
   - `update(patch)` action — merge patch into config, set dirty
   - `save()` action — validate via Zod, `POST /api/brand/product` (writes to product-level file, creates if needed), clear dirty
   - Include a `deepMerge` utility function for nested object merging

2. Create `src/stores/trees.ts` — implement `useTreesStore` as specified:
   - `manifest` ref, `trees` computed, `treeCount`, `branchCount`
   - `treeBySlug` computed lookup
   - `getTree(slug)`, `getBranch(treeSlug, branchSlug)` methods
   - `nodes` computed — generates VueFlow node array (brand node + tree nodes + branch nodes with positions)
   - `edges` computed — generates VueFlow edge array
   - `load()` / `save()` actions

3. Create `src/stores/canvas.ts` — implement `useCanvasStore`:
   - `zoom`, `pan`, `selectedNode`, `hoveredNode` refs
   - `selectNode(id)`, `resetView()` actions

4. Create `src/stores/sidebar.ts` — implement `useSidebarStore`:
   - `isOpen`, `activeTab`, `width` refs
   - `toggle()`, `setTab()` actions

5. Create `src/brand/tokens.ts` — a composable that injects brand CSS custom properties onto `:root`:
   ```typescript
   export function useBrandTokens() {
     const brand = useBrandStore()
     watchEffect(() => {
       const root = document.documentElement
       for (const [key, value] of Object.entries(brand.tokens)) {
         root.style.setProperty(key, value)
       }
     })
   }
   ```

6. Create `src/brand/theme.css` — base styles that consume the CSS custom properties:
   - Body: `background: var(--brand-bg); color: var(--brand-text); font-family: var(--font-body);`
   - Headings: `font-family: var(--font-heading);`
   - Code: `font-family: var(--font-mono);`
   - Utility classes for surfaces, borders, radius, shadows

7. Update `src/main.ts` — install Pinia, call `useBrandTokens()` in `App.vue` setup, import `theme.css`

### Validator: `phase-2-validator`

**Model:** `claude-opus-4-6`

**Prereading:**
- `DEBRIEF.md` — sections: Pinia Stores, Brand Save → Cascade Flow
- Activate `/playwright-bowser` — for verifying CSS custom properties on `:root`
- `apps/infinite-ui/_template/src/stores/` — read the builder's output

**Tasks:**

1. **Build check** — `bun run build` still succeeds after store changes

2. **Playwright UI check** — start dev server, verify brand tokens are applied:
   ```bash
   cd apps/infinite-ui/_template && bun run dev &
   DEV_PID=$!
   sleep 3

   # Verify CSS custom properties exist on :root
   playwright-cli -s=phase2-val open http://localhost:5173
   playwright-cli -s=phase2-val run-code "
     const styles = getComputedStyle(document.documentElement);
     const primary = styles.getPropertyValue('--brand-primary').trim();
     console.log('--brand-primary:', primary);
     console.log('HAS_TOKENS:', primary.length > 0);
   "
   playwright-cli -s=phase2-val screenshot --filename=screenshots/phase2-tokens.png
   playwright-cli -s=phase2-val close

   kill $DEV_PID
   ```

3. **Store reactivity check** — verify the brand store's `tokens` computed updates when `config` changes (unit-level, via bun test or inline script)

**Exit criteria:** CSS custom properties are injected on `:root`. Screenshot shows themed page. Build passes.

---

## Phase 3: Vue Router + Gallery Views

**Goal:** Implement the router that auto-discovers trees/branches from `trees.yaml`, and build the gallery views (GalleryHome, TreeView, BranchPreview).

### Builder: `phase-3-builder`

**Model:** `claude-opus-4-6`

**Prereading:**
- `DEBRIEF.md` — sections: Vue Router — Route Structure, Gallery UI, App Structure
- `apps/infinite-ui/_template/src/stores/trees.ts` — understand the store API for tree/branch lookups
- `apps/infinite-ui/_template/src/trees/trees.yaml` — the manifest driving route registration

**Tasks:**

1. Create `src/router/index.ts`:
   - Import route components for all view levels
   - Define routes matching the 5-level hierarchy:
     - `/` → `WorkspaceView.vue` — lists all brands
     - `/:brand` → `BrandView.vue` — lists all products in a brand
     - `/:brand/:product` → `CanvasView.vue` (placeholder for now — built in Phase 4)
     - `/:brand/:product/gallery` → `GalleryHome.vue`
     - `/:brand/:product/gallery/:tree` → `TreeView.vue`
     - `/:brand/:product/gallery/:tree/:branch` → dynamically resolved leaf component
   - For the dynamic leaf route, use `defineAsyncComponent` + dynamic import to load `../trees/${tree}/${branch}/index.vue`

2. Create `src/workspace/WorkspaceView.vue`:
   - Reads `apps/infinite-ui/` filesystem to list all brand directories (excluding `_template`)
   - Renders each brand as a card with name and product count
   - Each card links to `/:brand`
   - Lightweight — no Pinia store needed, fetches brand list from a Vite middleware endpoint (`GET /api/workspace/brands`)

3. Create `src/workspace/BrandView.vue`:
   - Route param `:brand` — reads product directories within the brand folder
   - Shows brand-level `brand.yaml` identity (palette preview, name)
   - Lists all products as cards with name and whether they have a product-level brand.yaml override
   - Each card links to `/:brand/:product`
   - Fetches product list from Vite middleware endpoint (`GET /api/workspace/products/:brand`)

4. Create `src/gallery/GalleryHome.vue`:
   - Read from `useTreesStore().trees`
   - Render a grid of tree cards (name, description, icon, branch count)
   - Each card links to `/:brand/:product/gallery/:tree`
   - Styled with brand CSS custom properties

5. Create `src/gallery/TreeView.vue`:
   - Route param `:tree` → `useTreesStore().getTree(slug)`
   - Render all branches as cards with status badges (colored dot: green/yellow/red/gray)
   - Each card links to `/:brand/:product/gallery/:tree/:branch`
   - Show branch description, created date, status

6. Create `src/gallery/BranchPreview.vue`:
   - Wrapper that loads the actual leaf component via dynamic import
   - Shows brand/product/tree/branch breadcrumb navigation
   - Back button to tree view

7. Create `src/App.vue`:
   - Shell layout: sidebar (collapsed placeholder for now) + `<router-view />`
   - Call `useBrandTokens()` in setup
   - Load brand store and trees store on mount (when at product level)

8. Update Vite plugin (`brandSyncPlugin`) — add workspace endpoints:
   - `GET /api/workspace/brands` — list brand directories
   - `GET /api/workspace/products/:brand` — list product directories within a brand

### Validator: `phase-3-validator`

**Model:** `claude-opus-4-6`

**Prereading:**
- `DEBRIEF.md` — sections: Vue Router — Route Structure
- Activate `/playwright-bowser` — for navigation testing and screenshot capture
- `apps/infinite-ui/_template/_template-product/src/trees/trees.yaml` — know expected tree/branch content

**Tasks:**

1. **Build check** — `bun run build` succeeds

2. **Playwright — Full navigation flow (workspace → brand → product → gallery → leaf):**
   ```bash
   cd apps/infinite-ui/_template/_template-product && bun run dev &
   DEV_PID=$!
   sleep 3

   # Workspace view — list all brands
   playwright-cli -s=phase3-val open http://localhost:5173
   playwright-cli -s=phase3-val screenshot --filename=screenshots/phase3-workspace.png
   playwright-cli -s=phase3-val snapshot
   # Verify: at least one brand card visible ("_template")

   # Brand view — list products
   playwright-cli -s=phase3-val click <ref-to-template-brand>
   playwright-cli -s=phase3-val screenshot --filename=screenshots/phase3-brand-view.png
   # Verify: product card visible ("_template-product")

   # Gallery home — list trees
   playwright-cli -s=phase3-val click <ref-to-template-product>
   playwright-cli -s=phase3-val goto http://localhost:5173/_template/_template-product/gallery
   playwright-cli -s=phase3-val screenshot --filename=screenshots/phase3-gallery-home.png
   playwright-cli -s=phase3-val snapshot
   # Verify: at least one tree card visible with text "Example Tree"

   # Click into the example tree
   playwright-cli -s=phase3-val click <ref-to-example-tree-card>
   playwright-cli -s=phase3-val screenshot --filename=screenshots/phase3-tree-view.png
   playwright-cli -s=phase3-val snapshot
   # Verify: branch cards visible — "Variant A", "Variant B"

   # Click into a branch
   playwright-cli -s=phase3-val click <ref-to-variant-a>
   playwright-cli -s=phase3-val screenshot --filename=screenshots/phase3-leaf-view.png
   # Verify: the actual generated leaf component renders

   playwright-cli -s=phase3-val close
   kill $DEV_PID
   ```

3. **Route verification** — confirm all three routes resolve:
   - `/gallery` → GalleryHome renders
   - `/gallery/example` → TreeView renders with 2 branches
   - `/gallery/example/variant-a` → leaf index.vue renders

**Exit criteria:** All three gallery routes render. Navigation between them works. Screenshots captured. Build passes.

---

## Phase 4: VueFlow Canvas View

**Goal:** Build the Figma-like canvas view using VueFlow that shows Brand → Tree → Branch hierarchy as an interactive node graph.

### Builder: `phase-4-builder`

**Model:** `claude-opus-4-6`

**Prereading:**
- `DEBRIEF.md` — sections: Gallery UI (canvas subsection), Team Architecture diagram
- `apps/infinite-ui/_template/src/stores/trees.ts` — the `nodes` and `edges` computed properties drive the graph
- VueFlow docs: `@vue-flow/core` API, custom node types, minimap, background

**Tasks:**

1. Create `src/canvas/CanvasView.vue`:
   - Use `<VueFlow>` with `<Background>` and `<MiniMap>` from `@vue-flow/core`, `@vue-flow/background`, `@vue-flow/minimap`
   - Bind `:nodes` and `:edges` from `useTreesStore().nodes` and `useTreesStore().edges`
   - Register custom node types: `brand`, `tree`, `branch`
   - Enable pan (scroll) and zoom (pinch/scroll)
   - Use dagre layout algorithm for auto-positioning (install `dagre` or `@dagrejs/dagre`)
   - On node click: if branch node, navigate to `/gallery/:tree/:branch`

2. Create `src/canvas/TreeNode.vue` — custom VueFlow node:
   - Card shape with tree name, description, branch count badge
   - Border color from brand palette (`--brand-secondary`)
   - Hover: subtle elevation change

3. Create `src/canvas/BranchNode.vue` — custom VueFlow node:
   - Smaller card with branch name and status badge
   - Border color based on status: green (validated), yellow (draft/generating), red (failed)
   - Click → navigate to leaf

4. Create `src/canvas/LeafNode.vue` — custom VueFlow node (optional, for future use):
   - Tiny preview thumbnail placeholder

5. Update `src/router/index.ts` — wire `/` route to `CanvasView.vue`

6. Install dagre: `bun add @dagrejs/dagre`

7. Implement auto-layout in `useTreesStore().nodes` computed:
   - Use dagre to compute positions based on hierarchy
   - Brand node at top, trees in second tier, branches in third tier
   - Consistent spacing

### Validator: `phase-4-validator`

**Model:** `claude-opus-4-6`

**Prereading:**
- `DEBRIEF.md` — sections: Gallery UI (canvas subsection)
- Activate `/playwright-bowser` — for canvas node/edge verification and click testing
- `apps/infinite-ui/_template/src/trees/trees.yaml` — expected node count: 1 brand + 1 tree + 2 branches = 4

**Tasks:**

1. **Build check** — `bun run build` succeeds

2. **Playwright — Canvas renders:**
   ```bash
   cd apps/infinite-ui/_template && bun run dev &
   DEV_PID=$!
   sleep 3

   playwright-cli -s=phase4-val open http://localhost:5173
   playwright-cli -s=phase4-val screenshot --filename=screenshots/phase4-canvas.png
   playwright-cli -s=phase4-val snapshot
   # Verify: VueFlow canvas visible, nodes rendered

   # Verify node count: 1 brand + 1 tree + 2 branches = 4 nodes
   playwright-cli -s=phase4-val run-code "
     const nodes = document.querySelectorAll('.vue-flow__node');
     console.log('NODE_COUNT:', nodes.length);
     console.log('PASS:', nodes.length >= 4);
   "

   # Verify edges exist
   playwright-cli -s=phase4-val run-code "
     const edges = document.querySelectorAll('.vue-flow__edge');
     console.log('EDGE_COUNT:', edges.length);
     console.log('PASS:', edges.length >= 3);
   "

   # Click a branch node → should navigate to gallery
   playwright-cli -s=phase4-val click <ref-to-branch-node>
   playwright-cli -s=phase4-val screenshot --filename=screenshots/phase4-nav.png
   # Verify: URL changed to /gallery/example/variant-a or similar

   playwright-cli -s=phase4-val close
   kill $DEV_PID
   ```

3. **Minimap check** — verify minimap element exists in DOM

**Exit criteria:** Canvas renders with correct node/edge counts. Clicking branch navigates to gallery. Minimap present. Build passes.

---

## Phase 5: Sidebar + Visual Brand Editor

**Goal:** Build the collapsible sidebar with visual brand controls (color pickers, sliders, dropdowns), trees panel, and the save/reset cascade flow.

### Builder: `phase-5-builder`

**Model:** `claude-opus-4-6`

**Prereading:**
- `DEBRIEF.md` — sections: Gallery UI — Sidebar (full control table), Brand Save → Cascade Flow
- `apps/infinite-ui/_template/src/stores/brand.ts` — the store API for `update()`, `save()`, `isDirty`
- `apps/infinite-ui/_template/src/stores/sidebar.ts` — sidebar state management
- `apps/infinite-ui/_template/src/schemas/brand.schema.ts` — know which fields exist and their types

**Tasks:**

1. Create `src/layout/Sidebar.vue`:
   - Collapsible panel (toggle via `useSidebarStore().toggle()`)
   - Tab bar: Brand | Trees | Settings
   - Renders active tab component
   - Resizable width via drag handle
   - Styled with brand surface/border tokens

2. Create `src/layout/BrandPanel.vue`:
   - Sections: Identity, Palette, Typography, Spacing, Motion
   - Each section renders its sub-editor component
   - Save button (calls `brandStore.save()`) and Reset button (reverts to last saved)
   - Dirty indicator (dot/badge) when `brandStore.isDirty`

3. Create `src/layout/PaletteEditor.vue`:
   - Grid of color swatches for each palette key
   - Each swatch: `<input type="color">` wrapped in a styled swatch container
   - Label below each swatch (Primary, Secondary, Accent, etc.)
   - On change: `brandStore.update({ palette: { ...palette, [key]: newColor } })`
   - Overlay field gets an opacity slider alongside color picker

4. Create `src/layout/TypographyEditor.vue`:
   - Font family dropdowns for heading/body/mono (curated list: Inter, Roboto, Poppins, Montserrat, Playfair Display, JetBrains Mono, Fira Code, etc.)
   - Per-scale-tier controls (h1, h2, h3, body, small, caption):
     - Size slider: range 0.5rem–5rem, step 0.125rem, displays current value
     - Weight slider: range 100–900, step 100
     - Tracking slider (if applicable): range -0.05em–0.1em

5. Create `src/layout/SpacingEditor.vue`:
   - Unit slider: 0.25rem–1rem
   - Radius sliders: sm, md, lg (0–2rem)
   - Container max slider: 800px–1600px
   - Visual preview box that shows current radius/spacing

6. Create `src/layout/MotionEditor.vue`:
   - Duration sliders: fast, normal, slow (50ms–1000ms)
   - Easing dropdown: presets (ease, ease-in, ease-out, ease-in-out, cubic-bezier)
   - Preview animation that plays with current motion settings

7. Create `src/layout/TreesPanel.vue`:
   - Read-only view of `useTreesStore().trees`
   - Tree list with branch counts and status summary
   - Click tree → set `canvasStore.selectedNode` to that tree's node ID

8. Update `src/App.vue`:
   - Layout: `<Sidebar />` on left + `<router-view />` filling remaining space
   - Sidebar width from `sidebarStore.width`

### Validator: `phase-5-validator`

**Model:** `claude-opus-4-6`

**Prereading:**
- `DEBRIEF.md` — sections: Gallery UI — Sidebar, Brand Save → Cascade Flow
- Activate `/playwright-bowser` — for sidebar interaction testing, color picker verification, save cascade
- `apps/infinite-ui/_template/brand.yaml` — know initial values to verify against

**Tasks:**

1. **Build check** — `bun run build` succeeds

2. **Playwright — Sidebar renders with tabs:**
   ```bash
   cd apps/infinite-ui/_template && bun run dev &
   DEV_PID=$!
   sleep 3

   playwright-cli -s=phase5-val open http://localhost:5173
   playwright-cli -s=phase5-val screenshot --filename=screenshots/phase5-sidebar.png
   playwright-cli -s=phase5-val snapshot
   # Verify: sidebar visible, Brand tab active, palette swatches visible
   ```

3. **Playwright — Color picker changes propagate:**
   ```bash
   # Change primary color via JS (simulating picker)
   playwright-cli -s=phase5-val run-code "
     const primary = document.documentElement.style.getPropertyValue('--brand-primary');
     console.log('BEFORE:', primary);
   "

   # Interact with a color input
   playwright-cli -s=phase5-val snapshot
   # Find and interact with color picker for primary
   # After change:
   playwright-cli -s=phase5-val run-code "
     const primary = document.documentElement.style.getPropertyValue('--brand-primary');
     console.log('AFTER:', primary);
   "
   playwright-cli -s=phase5-val screenshot --filename=screenshots/phase5-color-change.png
   ```

4. **Playwright — Tab switching:**
   ```bash
   # Click Trees tab
   playwright-cli -s=phase5-val click <ref-to-trees-tab>
   playwright-cli -s=phase5-val screenshot --filename=screenshots/phase5-trees-panel.png
   playwright-cli -s=phase5-val snapshot
   # Verify: trees panel visible with "Example Tree"

   playwright-cli -s=phase5-val close
   kill $DEV_PID
   ```

5. **Playwright — Save cascade:**
   ```bash
   # Modify a brand value, click Save, verify brand.yaml on disk updated
   playwright-cli -s=phase5-save open http://localhost:5173
   # Change a color, click Save button
   # Then verify file was written:
   # Save writes to product-level brand.yaml:
   # cat apps/infinite-ui/_template/_template-product/brand.yaml | grep the-new-color
   playwright-cli -s=phase5-save close
   ```

**Exit criteria:** Sidebar renders with all tabs. Color picker changes update CSS vars in real time. Save writes to disk. Tab switching works. Build passes.

---

## Phase 6: Justfile + Scripts + Workflow Prompts

**Goal:** Create the justfile with all recipes, the `scripts/list.py` CLI, and all 8 workflow prompt files.

### Builder: `phase-6-builder`

**Model:** `claude-opus-4-6`

**Prereading:**
- `DEBRIEF.md` — sections: Workflows (full section), Justfile, `scripts/list.py`, all 8 workflow definitions
- Activate `/meta-prompt` — use the 6-section template structure for all command files
- Read `/meta-prompt` examples — understand frontmatter, variables, instructions, workflow, report sections
- `~/.claude/skills/meta-prompt/PROMPT_TEMPLATE.md` — the template to follow

**Tasks:**

1. Create `justfile` at project root — copy the full justfile from DEBRIEF.md section "Justfile" with all recipes:
   - `team`, `new-brand`, `rebrand`, `new-tree`, `new-branch`, `generate`, `fork-leaf`, `validate`, `status`
   - `list-brands`, `list-products`, `list-trees`, `list-branches`, `list-leaves`
   - `dev`, `serve`
   - Update all prompt paths from `prompts/` → `.pi/commands/multi-team/`

2. Create `scripts/list.py` — copy the full script from DEBRIEF.md section "`scripts/list.py`":
   - uv inline script metadata with `pyyaml` and `rich` dependencies
   - Five subcommands: `brands`, `products`, `trees`, `branches`, `leaves`
   - Rich table output with status icons
   - `products` subcommand lists product directories within a brand, noting which have product-level `brand.yaml` overrides

3. Create directory: `.pi/commands/multi-team/`

4. Create all 9 command files in `.pi/commands/multi-team/` using the `/meta-prompt` 6-section structure. Each command is a reusable prompt addressed to the **Orchestrator** — it tells the orchestrator which teams to call, in what order, with what parameters.

   **`.pi/commands/multi-team/new-brand.md`:**
   ```markdown
   ---
   description: Create a new brand from the _template reference app
   argument-hint: <brand-slug>
   ---

   # Purpose
   Create a new brand by copying the _template reference app and customizing it.

   ## Variables
   BRAND: $1

   ## Instructions
   - Brand slug must be lowercase kebab-case
   - The _template app is the copy source — never modify _template itself
   - After copy, reset trees.yaml to empty manifest
   - Zod validation must pass before reporting success
   - Only the Setup team is needed for this workflow

   ## Workflow
   1. Delegate to **Setup** team:
      - Copy `apps/infinite-ui/_template/` → `apps/infinite-ui/$BRAND/`
      - Find-replace `_template` → `$BRAND` across all config files
      - Reset `trees.yaml` to: `{ version: 1, brand: "$BRAND", trees: [] }`
      - Update `brand.yaml` name field to "$BRAND"
   2. Delegate to **Setup** team (Structure Validator):
      - Run Zod validation on `brand.yaml` and `trees.yaml`
      - Verify directory structure matches expectations

   ## Report
   Brand "$BRAND" created successfully.
   - Path: `apps/infinite-ui/$BRAND/`
   - Next: add a product with `/new-product $BRAND <product-name>`
   ```

   **`.pi/commands/multi-team/new-product.md`:**
   ```markdown
   ---
   description: Create a new product within a brand
   argument-hint: <brand> <product-slug>
   ---

   # Purpose
   Create a new product within an existing brand by copying the _template-product.

   ## Variables
   BRAND: $1
   PRODUCT: $2

   ## Instructions
   - Product slug must be lowercase kebab-case
   - Copy from `_template/_template-product/` — never modify the template itself
   - The brand-level brand.yaml at `apps/infinite-ui/$BRAND/brand.yaml` must already exist
   - Reset trees.yaml to empty manifest
   - Only the Setup team is needed

   ## Workflow
   1. Delegate to **Setup** team:
      - Copy `apps/infinite-ui/_template/_template-product/` → `apps/infinite-ui/$BRAND/$PRODUCT/`
      - Find-replace `_template-product` → `$PRODUCT` across config files
      - Reset `trees.yaml` to: `{ version: 1, brand: "$BRAND", product: "$PRODUCT", trees: [] }`
      - Optionally create product-level `brand.yaml` override (or leave absent to inherit)
   2. Delegate to **Setup** team (Structure Validator):
      - Validate merged brand.yaml (brand-level + product-level) via Zod
      - Validate trees.yaml via Zod

   ## Report
   Product "$PRODUCT" created in brand "$BRAND".
   - Path: `apps/infinite-ui/$BRAND/$PRODUCT/`
   - Start dev server: `just dev $BRAND $PRODUCT`
   - Next: create trees with `/new-tree $BRAND $PRODUCT <tree> <description>`
   ```

   **`.pi/commands/multi-team/new-tree.md`:**
   ```markdown
   ---
   description: Add a new tree to a product's hierarchy
   argument-hint: <brand> <product> <tree-slug> <description>
   ---

   # Purpose
   Create a new tree (purpose category) within a product's hierarchy.

   ## Variables
   BRAND: $1
   PRODUCT: $2
   TREE: $3
   DESCRIPTION: $4

   ## Instructions
   - Tree slug must be lowercase kebab-case
   - Only the Setup team is needed
   - trees.yaml must pass Zod validation after update
   - Create the directory even though it has no branches yet

   ## Workflow
   1. Delegate to **Setup** team:
      - Create directory: `apps/infinite-ui/$BRAND/$PRODUCT/src/trees/$TREE/`
      - Add tree entry to `trees.yaml`: slug "$TREE", description "$DESCRIPTION", empty branches
   2. Delegate to **Setup** team (Structure Validator):
      - Validate `trees.yaml` via Zod

   ## Report
   Tree "$TREE" created in product "$PRODUCT" (brand "$BRAND").
   - Ready for branches via `/new-branch` or `/generate`
   ```

   **`.pi/commands/multi-team/new-branch.md`:**
   ```markdown
   ---
   description: Scaffold and generate a single branch with full validation
   argument-hint: <brand> <product> <tree> <branch-slug> <brief>
   ---

   # Purpose
   Create a single branch — scaffold the directory, generate the Vue component, and validate it.

   ## Variables
   BRAND: $1
   PRODUCT: $2
   TREE: $3
   BRANCH: $4
   BRIEF: $5

   ## Instructions
   - Full pipeline: Setup → Brand → UI Generation → Validation → Setup
   - If the tree doesn't exist yet, create it first
   - The generated component must use brand CSS custom properties exclusively — no hardcoded colors/fonts
   - Validation failures trigger regen with specific fix instructions

   ## Workflow
   1. Delegate to **Setup** team:
      - Create `apps/infinite-ui/$BRAND/$PRODUCT/src/trees/$TREE/$BRANCH/`
      - Stub `index.vue` with brand token imports
      - Add branch to `trees.yaml` (status: generating)
      - Run Zod validation
   2. Delegate to **Brand** team:
      - Load `brand.yaml`, prepare brand tokens + constraints brief
   3. Delegate to **UI Generation** team:
      - Generate `index.vue` from: "$BRIEF"
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
   ```

   **`.pi/commands/multi-team/generate.md`:**
   ```markdown
   ---
   description: Generate N variant branches for a tree
   argument-hint: <brand> <product> <tree> <count> <brief>
   ---

   # Purpose
   Generate multiple variant branches — the main workhorse for producing UI at scale.

   ## Variables
   BRAND: $1
   PRODUCT: $2
   TREE: $3
   COUNT: $4
   BRIEF: $5

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
      - Run Zod validation
   2. Delegate to **Brand** team:
      - Load `brand.yaml`, prepare brand context
   3. Delegate to **UI Generation** team:
      - UI Gen Lead creates $COUNT differentiated briefs from: "$BRIEF"
      - Vue Generator builds each variant
   4. Delegate to **Validation** team:
      - Soft + hard validate all $COUNT variants
      - Report which pass and which fail
   5. For any failures:
      - Delegate to **UI Generation** to fix
      - Delegate to **Validation** to re-check
   6. Delegate to **Setup** team:
      - Update all statuses in `trees.yaml`

   ## Report
   Generated $COUNT variants in tree "$TREE" for brand "$BRAND":
   - Passed: N/$COUNT
   - [List each variant with status and route path]
   - Browse: `/gallery/$TREE/`
   ```

   **`.pi/commands/multi-team/fork-leaf.md`:**
   ```markdown
   ---
   description: Fork an existing leaf N times with specified changes
   argument-hint: <brand> <product> <tree> <branch> <count> <changes>
   ---

   # Purpose
   Take an existing validated component and create N variations with specific modifications.

   ## Variables
   BRAND: $1
   PRODUCT: $2
   TREE: $3
   BRANCH: $4
   COUNT: $5
   CHANGES: $6

   ## Instructions
   - Source leaf must exist at `apps/infinite-ui/$BRAND/$PRODUCT/src/trees/$TREE/$BRANCH/index.vue`
   - Each fork should be a distinct interpretation of the requested changes
   - Name forks: `$BRANCH-fork-1` through `$BRANCH-fork-$COUNT`
   - Maintain brand consistency across all forks

   ## Workflow
   1. Delegate to **Setup** team:
      - Verify source leaf exists
      - Read source `index.vue`
      - Scaffold $COUNT new branch directories
      - Add to `trees.yaml` (status: generating)
      - Run Zod validation
   2. Delegate to **Brand** team:
      - Load brand context
   3. Delegate to **UI Generation** team:
      - Read source leaf
      - Produce $COUNT variations applying: "$CHANGES"
      - Each fork should be a distinct interpretation
   4. Delegate to **Validation** team:
      - Validate all forks
   5. Fix failures via **UI Generation** → re-validate
   6. Delegate to **Setup** team:
      - Update statuses in `trees.yaml`

   ## Report
   Forked "$BRANCH" into $COUNT variations:
   - Source: `/gallery/$TREE/$BRANCH`
   - [List each fork with status and how it differs]
   ```

   **`.pi/commands/multi-team/rebrand.md`:**
   ```markdown
   ---
   description: Re-validate and update all branches after brand.yaml changes
   argument-hint: <brand> [product]
   ---

   # Purpose
   After editing brand.yaml (brand-level or product-level), cascade changes to all existing components. If product is specified, only rebrand that product. If omitted, rebrand all products in the brand.

   ## Variables
   BRAND: $1
   PRODUCT: $2 (optional — blank = all products in brand)

   ## Instructions
   - Brand team identifies what changed
   - Every existing branch gets re-validated against new tokens
   - Failing branches get fixed by UI Generation
   - This can be expensive — it touches every branch

   ## Workflow
   1. Delegate to **Brand** team:
      - Re-read `brand.yaml`, identify token changes
      - Produce rebrand brief listing affected tokens
   2. Delegate to **Validation** team:
      - Re-validate ALL existing branches against new tokens
      - Set all to status: validating in `trees.yaml`
      - Report which pass and which fail
   3. Delegate to **UI Generation** team:
      - Fix failing branches to match new brand identity
   4. Delegate to **Validation** team:
      - Re-validate fixed branches
   5. Delegate to **Setup** team:
      - Update all statuses in `trees.yaml`

   ## Report
   Rebrand complete for "$BRAND":
   - Branches compliant: N/N
   - [List any that required fixes and what changed]
   ```

   **`.pi/commands/multi-team/validate.md`:**
   ```markdown
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
   3. Delegate to **Validation** team:
      - Soft validate each branch in scope (screenshot + brand check)
      - Hard validate branches that pass soft (interaction + responsive)
   4. Delegate to **Setup** team:
      - Update statuses in `trees.yaml` (validated / failed)

   ## Report
   Validation complete for "$BRAND" (scope: $TREE $BRANCH):
   - Passed: N/N
   - [List failures with reasons]
   ```

   **`.pi/commands/multi-team/status.md`:**
   ```markdown
   ---
   description: Show product health overview
   argument-hint: <brand> <product>
   ---

   # Purpose
   Read-only status report for a product — no generation, no validation.

   ## Variables
   BRAND: $1
   PRODUCT: $2

   ## Instructions
   - Read `trees.yaml` only — no team delegation needed
   - Display tree counts, branch counts, status breakdown
   - Use status icons: ✓ validated, ● generating/validating, ✗ failed, ○ draft

   ## Workflow
   1. Read `apps/infinite-ui/$BRAND/$PRODUCT/src/trees/trees.yaml`
   2. Parse and display:
      - Brand name, total tree count, total branch count
      - Per-tree: name, branch count
      - Per-branch: slug, status icon, created date
      - Summary: counts by status

   ## Report
   Brand: $BRAND
   Trees: N | Branches: N
   [Per-tree breakdown]
   Summary: N validated | N generating | N failed | N draft
   ```

5. Verify `just` is available, if not document installation: `brew install just`

### Validator: `phase-6-validator`

**Model:** `claude-opus-4-6`

**Prereading:**
- `DEBRIEF.md` — sections: Workflows, Justfile, `scripts/list.py`
- `.pi/commands/multi-team/` — read all 9 command files to verify structure
- `~/.claude/skills/meta-prompt/PROMPT_TEMPLATE.md` — verify commands follow the template

**Tasks:**

1. **Justfile parse check:**
   ```bash
   cd /path/to/ui-agents && just --list
   ```
   Verify all expected recipes appear in output.

2. **List script check:**
   ```bash
   cd /path/to/ui-agents && uv run --script scripts/list.py brands
   ```
   Should show `_template` (or empty if no real brands yet).

   ```bash
   uv run --script scripts/list.py products _template
   ```
   Should show `_template-product`.

   ```bash
   uv run --script scripts/list.py trees _template _template-product
   ```
   Should show "Example Tree" with 2 branches.

   ```bash
   uv run --script scripts/list.py branches _template _template-product example
   ```
   Should show variant-a and variant-b with validated status.

   ```bash
   uv run --script scripts/list.py leaves _template _template-product
   ```
   Should show `example/variant-a/index.vue` and `example/variant-b/index.vue`.

3. **Prompt files check:**
   ```bash
   ls .pi/commands/multi-team/*.md | wc -l
   ```
   Should output `8`.

   Verify each prompt contains `{{BRAND}}` placeholder (at minimum):
   ```bash
   for f in .pi/commands/multi-team/*.md; do echo "$f: $(grep -c '\$' $f) variables"; done
   ```

4. **Dev server via justfile:**
   ```bash
   just dev _template _template-product &
   DEV_PID=$!
   sleep 3
   curl -s http://localhost:5173 | head -5
   kill $DEV_PID
   ```
   Verify HTML response.

**Exit criteria:** `just --list` shows all recipes. List script returns correct data for `_template`. All 8 command files exist in `.pi/commands/multi-team/` with correct variables and `/meta-prompt` structure. `just dev _template _template-product` boots the app.

---

## Phase 7: Team Config + Agent Prompts

**Goal:** Create the multi-team-config.yaml with all four teams and write system prompts for all 10 agents + orchestrator. This is the agent layer — no Vue code, just the orchestration configuration.

### Builder: `phase-7-builder`

**Model:** `claude-opus-4-6`

**Prereading:**
- `DEBRIEF.md` — sections: Team Architecture, Team Breakdown, Config: multi-team-config.yaml, Shared Context, Mental Models
- Activate `/meta-agent` — use this skill to generate every agent file. Follow its 12-step workflow and frontmatter field reference exactly.
- `~/.claude/skills/meta-agent/SKILL.md` — read fully, understand all frontmatter fields
- `~/.claude/skills/meta-agent/examples.md` — read examples of well-structured agents
- **Read existing agent files as reference for the extended frontmatter structure used in this codebase:**
  - `.pi/multi-team/agents/orchestrator.md` — reference for orchestrator pattern (expertise, skills, domain, tools)
  - `.pi/multi-team/agents/engineering-lead.md` — reference for lead pattern (delegate tool, zero-micro-management skill)
  - `.pi/multi-team/agents/frontend-dev.md` — reference for worker pattern (precise-worker skill, no delegate, bash tool)
- `.pi/multi-team/skills/` — read all shared skill files to understand which skills to assign to which agent role

**Tasks:**

1. Overwrite `.pi/multi-team/multi-team-config.yaml` with the config from DEBRIEF.md section "Config: multi-team-config.yaml":
   - Orchestrator
   - Setup team (Setup Lead, Scaffold Worker, Structure Validator)
   - Brand team (Brand Lead, Brand Analyst)
   - UI Generation team (UI Generation Lead, Vue Generator, Animation Specialist)
   - Validation team (Validation Lead, Soft Validator, Hard Validator)
   - `shared_context` referencing `_template` paths

2. **Use `/meta-agent` to create each agent file** in `.pi/multi-team/agents/`. Follow the existing frontmatter structure from the reference agents above. Each agent file must include:
   - YAML frontmatter with: `name`, `model` (`anthropic/claude-opus-4-6` for all), `expertise` (path to mental model, `updatable: true`, `max-lines: 10000`), `skills` (appropriate subset from `.pi/multi-team/skills/`), `tools`, `domain`
   - Markdown system prompt below the frontmatter

   **Agents to create (12 total):**

   **Orchestrator** — `orchestrator.md`:
   - Role: routes requests to teams, synthesizes output, always calls Setup first for structural changes and last for status updates
   - Skills: `conversational-response`, `mental-model`, `active-listener`, `zero-micro-management`, `high-autonomy`
   - Tools: `read`, `write`, `edit`, `grep`, `find`, `ls`, `delegate`
   - Domain: expertise updatable, `.pi/multi-team/` read-only, root read-only
   - System prompt must reference all workflow commands in `.pi/commands/multi-team/` and know team routing

   **Setup Lead** — `setup-lead.md`:
   - Role: owns trees.yaml integrity, decides tree/branch naming, coordinates scaffold worker + structure validator
   - Skills: `conversational-response`, `mental-model`, `active-listener`, `zero-micro-management`
   - Tools: `read`, `write`, `edit`, `bash`, `grep`, `find`, `ls`, `delegate`
   - Domain: `apps/infinite-ui/` read/write, `.pi/multi-team/` read/write, root read

   **Scaffold Worker** — `scaffold-worker.md`:
   - Role: creates directories, stubs index.vue with brand tokens, updates trees.yaml entries, copies `_template` for new brands
   - Skills: `mental-model`, `active-listener`, `precise-worker`
   - Tools: `read`, `write`, `edit`, `bash`, `grep`, `find`, `ls` (no `delegate`)
   - Domain: `apps/infinite-ui/` read/write/delete, `.pi/multi-team/` read, root read

   **Structure Validator** — `structure-validator.md`:
   - Role: runs Zod parse on trees.yaml and brand.yaml, verifies filesystem matches manifest, reports drift
   - Skills: `mental-model`, `active-listener`, `precise-worker`
   - Tools: `read`, `bash`, `grep`, `find`, `ls` (no `delegate`, no `write`/`edit` — read-only + bash for running validation scripts)
   - Domain: `apps/infinite-ui/` read, `.pi/multi-team/` read, root read

   **Brand Lead** — `brand-lead.md`:
   - Role: guards brand.yaml consistency, produces brand briefs for UI generation, reviews generated components for brand compliance
   - Skills: `conversational-response`, `mental-model`, `active-listener`, `zero-micro-management`
   - Tools: `read`, `write`, `edit`, `grep`, `find`, `ls`, `delegate`
   - Domain: `apps/infinite-ui/` read, `.pi/multi-team/expertise/brand-*` read/write, root read

   **Brand Analyst** — `brand-analyst.md`:
   - Role: reads brand.yaml tokens, checks generated Vue components for correct CSS custom property usage, flags hardcoded colors/fonts, validates contrast ratios
   - Skills: `mental-model`, `active-listener`, `precise-worker`
   - Tools: `read`, `bash`, `grep`, `find`, `ls` (no `delegate`)
   - Domain: `apps/infinite-ui/` read, `.pi/multi-team/expertise/brand-analyst-*` read/write, root read

   **UI Generation Lead** — `ui-generation-lead.md`:
   - Role: translates user requests into Vue component briefs, decides layout strategies, differentiates variants when generating N branches
   - Skills: `conversational-response`, `mental-model`, `active-listener`, `zero-micro-management`
   - Tools: `read`, `write`, `edit`, `bash`, `grep`, `find`, `ls`, `delegate`
   - Domain: `apps/infinite-ui/` read/write, `.pi/multi-team/expertise/ui-generation-*` read/write, root read

   **Vue Generator** — `vue-generator.md`:
   - Role: writes Vue 3 SFC components using Composition API + `<script setup>`. All styling via brand CSS custom properties. Responsive using brand breakpoints. No hardcoded values.
   - Skills: `mental-model`, `active-listener`, `precise-worker`
   - Tools: `read`, `write`, `edit`, `bash`, `grep`, `find`, `ls` (no `delegate`)
   - Domain: `apps/infinite-ui/*/src/trees/` read/write, `apps/infinite-ui/*/brand.yaml` read, `.pi/multi-team/expertise/vue-generator-*` read/write

   **Animation Specialist** — `animation-specialist.md`:
   - Role: CSS transitions, Vue `<Transition>` components, scroll-triggered animations, micro-interactions. Uses brand motion tokens for all timing.
   - Skills: `mental-model`, `active-listener`, `precise-worker`
   - Tools: `read`, `write`, `edit`, `bash`, `grep`, `find`, `ls` (no `delegate`)
   - Domain: `apps/infinite-ui/*/src/trees/` read/write, `.pi/multi-team/expertise/animation-*` read/write

   **Validation Lead** — `validation-lead.md`:
   - Role: coordinates soft and hard validation pipeline, decides pass/fail, sends specific fix instructions back to UI generation
   - Skills: `conversational-response`, `mental-model`, `active-listener`, `zero-micro-management`
   - Tools: `read`, `write`, `edit`, `bash`, `grep`, `find`, `ls`, `delegate`
   - Domain: `apps/infinite-ui/` read, `screenshots/` read/write, `.pi/multi-team/expertise/validation-*` read/write

   **Soft Validator** — `soft-validator.md`:
   - Role: uses `playwright-cli` to screenshot rendered components, checks brand compliance (correct colors, fonts, spacing), validates layout correctness
   - Skills: `mental-model`, `active-listener`, `precise-worker`
   - Tools: `read`, `bash`, `grep`, `find`, `ls` (no `delegate` — uses `bash` for playwright-cli)
   - Domain: `apps/infinite-ui/` read, `screenshots/` read/write, `.pi/multi-team/expertise/soft-validator-*` read/write
   - System prompt must include playwright-cli usage patterns for screenshots and DOM inspection

   **Hard Validator** — `hard-validator.md`:
   - Role: uses `playwright-cli` to test interactivity (clicks, hovers, transitions), responsive behavior (resize viewport to each breakpoint), accessibility (keyboard nav, contrast)
   - Skills: `mental-model`, `active-listener`, `precise-worker`
   - Tools: `read`, `bash`, `grep`, `find`, `ls` (no `delegate`)
   - Domain: `apps/infinite-ui/` read, `screenshots/` read/write, `.pi/multi-team/expertise/hard-validator-*` read/write
   - System prompt must include playwright-cli usage patterns for interaction testing and viewport resizing

3. Set appropriate domain permissions per agent (as detailed above per agent)

4. Set appropriate tools per agent (as detailed above per agent)

### Validator: `phase-7-validator`

**Model:** `claude-opus-4-6`

**Prereading:**
- `DEBRIEF.md` — sections: Team Architecture, Config: multi-team-config.yaml, Shared Context
- `.pi/multi-team/agents/orchestrator.md` — verify it follows the existing frontmatter pattern (expertise, skills, domain, tools)
- `~/.claude/skills/meta-agent/SKILL.md` — verify agents match the `/meta-agent` structure
- `.pi/multi-team/multi-team-config.yaml` — the config being validated

**Tasks:**

1. **Config parse check** — verify the YAML parses correctly:
   ```bash
   python3 -c "
   import yaml
   with open('.pi/multi-team/multi-team-config.yaml') as f:
       config = yaml.safe_load(f)
   teams = config['teams']
   print(f'Teams: {len(teams)}')
   for t in teams:
       members = t.get('members', [])
       print(f'  {t[\"team-name\"]}: {t[\"lead\"][\"name\"]} + {len(members)} members')
   print(f'Shared context: {len(config[\"shared_context\"])} files')
   print('PASS: Config valid')
   "
   ```

2. **Agent file check** — verify all 11 agent files exist and have valid frontmatter:
   ```bash
   for f in .pi/multi-team/agents/*.md; do
     echo "$f: $(head -1 $f)"
   done
   ```
   Expected: 12 files (orchestrator + 11 agents)

3. **Shared context file check** — verify every file referenced in `shared_context` exists:
   ```bash
   python3 -c "
   import yaml
   with open('.pi/multi-team/multi-team-config.yaml') as f:
       config = yaml.safe_load(f)
   import os
   for path in config['shared_context']:
       exists = os.path.exists(path)
       status = '✓' if exists else '✗ MISSING'
       print(f'  {status} {path}')
   "
   ```

5. **Agent path check** — verify every agent path referenced in config exists:
   ```bash
   python3 -c "
   import yaml, os
   with open('.pi/multi-team/multi-team-config.yaml') as f:
       config = yaml.safe_load(f)
   # Check orchestrator
   print('Orchestrator:', '✓' if os.path.exists(config['orchestrator']['path']) else '✗')
   # Check all team agents
   for team in config['teams']:
       lead_path = team['lead']['path']
       print(f'{team[\"lead\"][\"name\"]}:', '✓' if os.path.exists(lead_path) else '✗')
       for member in team.get('members', []):
           print(f'{member[\"name\"]}:', '✓' if os.path.exists(member['path']) else '✗')
   "
   ```

6. **Model check** — verify all agents use `claude-opus-4-6`:
   ```bash
   grep -l "model:" .pi/multi-team/agents/*.md | while read f; do
     model=$(grep "^model:" "$f" | head -1)
     echo "$f: $model"
   done
   ```

**Exit criteria:** Config parses with 4 teams. All 11 agent files exist with valid frontmatter. All shared context paths resolve. All agent paths in config resolve. All models are Opus. Mental models are created and maintained by the agents themselves at runtime.

---

## Phase Summary

| Phase | Builds | Validates | Playwright |
|-------|--------|-----------|:----------:|
| 1. Scaffolding + Schemas | App structure, Zod schemas, brand.yaml, trees.yaml, example leaves, Vite config | Schema parse, build, directory check | — |
| 2. Stores + Tokens | 4 Pinia stores, brand token injection, theme.css | Token injection on :root, build | Yes |
| 3. Router + Gallery + Workspace | Vue Router, WorkspaceView, BrandView, GalleryHome, TreeView, BranchPreview | All 6 route levels, navigation flow | Yes |
| 4. VueFlow Canvas | CanvasView, custom nodes, dagre layout, minimap | Node/edge counts, click navigation | Yes |
| 5. Sidebar + Brand Editor | Sidebar, BrandPanel, PaletteEditor, TypographyEditor, SpacingEditor, MotionEditor, TreesPanel | Tab switching, live color updates, save cascade | Yes |
| 6. Justfile + Scripts + Commands | justfile, scripts/list.py, 9 command files in `.pi/commands/multi-team/` | Recipe list, script output, command structure validation | — |
| 7. Team Config + Agents | multi-team-config.yaml, 12 agent prompts | Config parse, file existence, path resolution, model check | — |

**Note:** Agent count is 12 total: 1 orchestrator + 3 setup + 2 brand + 3 UI gen + 3 validation.

**Total deliverables:**
- 1 fully functional `_template` Vue app
- 4 Pinia stores
- 2 Zod schemas
- 6 sidebar components
- 4 canvas components
- 2 workspace components (WorkspaceView, BrandView)
- 3 gallery components
- 1 Vite plugin
- 1 justfile (15+ recipes)
- 1 Python CLI script
- 9 workflow commands in `.pi/commands/multi-team/`
- 12 agent system prompts
- 1 multi-team config

**Execution model:** Each phase runs sequentially. Builder completes all tasks, then validator runs all checks. Phase N+1 only starts after phase N validator passes. All agents are `claude-opus-4-6`.

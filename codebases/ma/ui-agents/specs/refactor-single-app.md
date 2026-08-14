# Refactor: Single App Architecture

## Summary

Collapse from "one Vue app per product" to **one Vue app total**. All brands and products live under a single Vite project. One dev server, one port, one browser tab.

**Why:** This is a design/prototype tool, not a deployment pipeline. Users need to browse across brands and products fluidly without switching dev servers.

---

## Current State

```
apps/infinite-ui/
├── _template/
│   ├── brand.yaml
│   └── _template-product/        ← separate Vite app
│       ├── package.json
│       ├── vite.config.ts
│       ├── src/main.ts
│       └── src/...
├── agentix/
│   ├── brand.yaml
│   └── cuts/                     ← separate Vite app
│       ├── package.json
│       └── src/...
```

Problem: Each product is its own Vite app. Switching brands/products means switching dev servers.

## Target State

```
apps/infinite-ui/
├── package.json                  ← single Vite app
├── vite.config.ts
├── index.html
├── src/
│   ├── main.ts
│   ├── App.vue
│   ├── router/index.ts
│   ├── schemas/
│   │   ├── brand.schema.ts
│   │   └── trees.schema.ts
│   ├── stores/
│   │   ├── brand.ts              ← switches context based on route params
│   │   ├── trees.ts              ← loads active product's trees.yaml
│   │   ├── canvas.ts
│   │   └── sidebar.ts
│   ├── brand/
│   │   ├── tokens.ts
│   │   └── theme.css
│   ├── layout/
│   │   ├── Sidebar.vue
│   │   ├── BrandPanel.vue
│   │   ├── IdentityEditor.vue
│   │   ├── PaletteEditor.vue
│   │   ├── TypographyEditor.vue
│   │   ├── SpacingEditor.vue
│   │   ├── MotionEditor.vue
│   │   ├── MediaPanel.vue
│   │   └── TreesPanel.vue
│   ├── workspace/
│   │   ├── WorkspaceView.vue     ← / route: list all brands
│   │   └── BrandView.vue         ← /:brand route: list products
│   ├── canvas/
│   │   ├── CanvasView.vue        ← /:brand/:product route
│   │   ├── TreeNode.vue
│   │   ├── BranchNode.vue
│   │   └── LeafNode.vue
│   ├── gallery/
│   │   ├── GalleryHome.vue
│   │   ├── TreeView.vue
│   │   └── BranchPreview.vue
│   └── brands/                   ← all brand/product data (agents write here)
│       ├── _template/
│       │   ├── brand.yaml
│       │   └── products/
│       │       └── _template-product/
│       │           ├── brand.yaml
│       │           ├── trees.yaml
│       │           └── trees/
│       │               └── example/
│       │                   ├── variant-a/index.vue
│       │                   └── variant-b/index.vue
│       └── agentix/
│           ├── brand.yaml
│           └── products/
│               └── cuts/
│                   ├── brand.yaml
│                   ├── trees.yaml
│                   └── trees/
│                       └── landing/
│                           ├── hero-centered/index.vue
│                           ├── hero-split/index.vue
│                           └── hero-cinematic/index.vue
└── screenshots/

```

---

## Routes

```
/                                      → WorkspaceView (list all brands)
/:brand                                → BrandView (list products, palette preview)
/:brand/:product                       → CanvasView (VueFlow tree graph)
/:brand/:product/gallery               → GalleryHome (flat tree list)
/:brand/:product/gallery/:tree         → TreeView (branch cards)
/:brand/:product/gallery/:tree/:branch → BranchPreview (rendered leaf)
```

---

## Navigation & Layout

The app has three persistent UI elements that float over the content:

### 1. Breadcrumb Bar (always visible, toggleable)

A floating bar at the top of the viewport. Always shows the current location in the hierarchy. Clickable segments for navigation.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ☰  Workspace / agentix / cuts / gallery / landing / hero-centered   Ctrl+S Ctrl+H │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Structure:**
- **Menu icon (☰)** — left side, opens the Brand Identity sidebar (Ctrl+S also toggles this)
- **Breadcrumb segments** — each level is a clickable link:
  - `Workspace` → `/`
  - `agentix` → `/agentix`
  - `cuts` → `/agentix/cuts`
  - `gallery` → `/agentix/cuts/gallery`
  - `landing` → `/agentix/cuts/gallery/landing`
  - `hero-centered` → current (no link)
- **Hotkey hints** — right side, subtle muted text: `Ctrl+S` (toggle sidebar) `Ctrl+H` (toggle nav)
- **Floating container** — `position: fixed`, top of viewport, translucent background with backdrop-blur, z-index above content
- **Toggleable** — Ctrl+H hides/shows the breadcrumb bar entirely so you can focus on the UI below

**Breadcrumb adapts to route depth:**
```
/                          → ☰  Workspace                              Ctrl+H
/:brand                    → ☰  Workspace / agentix                    Ctrl+H
/:brand/:product           → ☰  Workspace / agentix / cuts             Ctrl+H
/:brand/:product/gallery   → ☰  Workspace / agentix / cuts / gallery   Ctrl+H
...and so on
```

### 2. Brand Identity Sidebar (Ctrl+S to toggle)

The existing sidebar with Brand/Trees/Settings tabs. Opens from the left.

**Changes from current design:**
- No longer always visible — opens via ☰ menu icon or Ctrl+S
- When open, overlays the content (doesn't push it)
- Close button (✕) or Ctrl+S to close
- Tabs remain: Brand (palette, typography, spacing, motion, identity, media), Trees, Settings

**Trees tab — filesystem-like UI:**
- Render the trees.yaml manifest as a collapsible tree structure (like VS Code explorer)
- Brand name at root
  - Product name
    - Tree name (collapsible)
      - Branch name (with status icon: ✓ ● ✗ ○)
        - Click → navigate to that branch's leaf view
- Shows the full hierarchy at a glance
- Collapsible groups for each tree

```
▼ agentix
  ▼ cuts
    ▼ landing
      ✓ hero-centered
      ✓ hero-split
      ● hero-cinematic
    ▶ dashboard (3 branches)
    ▶ pricing (1 branch)
```

### 3. Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+H` | Toggle breadcrumb bar visibility |
| `Ctrl+S` | Toggle brand identity sidebar |

Both are registered globally via `onMounted`/`onUnmounted` keyboard event listeners in `App.vue`.

### Layout Flow

```
┌─────────────────────────────────────────────────┐
│ ☰  Breadcrumb / path / here           Ctrl+H   │  ← floating, fixed top
├───────────┬─────────────────────────────────────┤
│           │                                     │
│  Sidebar  │         Main Content                │  ← sidebar overlays when open
│  (hidden  │    (WorkspaceView, BrandView,       │
│  by       │     CanvasView, Gallery, Leaf)      │
│  default) │                                     │
│           │                                     │
└───────────┴─────────────────────────────────────┘
```

When sidebar is closed (default state), content takes full width. Breadcrumb floats above. Clean, distraction-free.

### Components

```
src/layout/
├── BreadcrumbBar.vue       ← floating nav with menu icon + segments + Ctrl+H hint
├── Sidebar.vue             ← overlay sidebar (brand/trees/settings tabs)
├── BrandPanel.vue          ← brand tab content (existing)
├── TreesPanel.vue          ← trees tab content (REDESIGNED as filesystem tree)
├── IdentityEditor.vue      ← identity section (existing)
├── PaletteEditor.vue       ← palette section (existing)
├── TypographyEditor.vue    ← typography section (existing)
├── SpacingEditor.vue       ← spacing section (existing)
├── MotionEditor.vue        ← motion section (existing)
└── MediaPanel.vue          ← media section (existing)
```

---

## Phases

### Phase 1: Scaffold single app

**Builder:**
1. Create `apps/infinite-ui/package.json` at root level (move from `_template-product/`)
2. Create `apps/infinite-ui/vite.config.ts` with updated `brandSyncPlugin`:
   - `GET /api/workspace/brands` — list dirs in `src/brands/` excluding `_template`
   - `GET /api/workspace/products/:brand` — list dirs in `src/brands/:brand/products/`
   - `GET /api/brand/:brand` — read brand-level brand.yaml
   - `GET /api/brand/:brand/:product` — read product-level brand.yaml (404 if absent)
   - `GET/POST /api/trees/:brand/:product` — read/write product's trees.yaml
   - `POST /api/brand/:brand/:product` — write product-level brand.yaml
3. Create `apps/infinite-ui/index.html`
4. Create `apps/infinite-ui/src/main.ts` — Vue + Pinia + Router + theme.css
5. Move `src/schemas/`, `src/brand/` from `_template-product/` to `apps/infinite-ui/src/`
6. Create `apps/infinite-ui/src/brands/` directory

**Validator:**
- `bun run build` passes
- Vite dev server starts

### Phase 2: Move stores + update brand store for route-based context switching

**Builder:**
1. Move stores from `_template-product/src/stores/` to `apps/infinite-ui/src/stores/`
2. Update `brandStore.load()`:
   - Takes `brand` and `product` params (from route)
   - Fetches `GET /api/brand/:brand` (brand-level)
   - Fetches `GET /api/brand/:brand/:product` (product-level, may 404)
   - Deep merges + validates
3. Update `brandStore.save()`:
   - Posts to `POST /api/brand/:brand/:product`
4. Update `treesStore.load()`:
   - Takes `brand` and `product` params
   - Fetches `GET /api/trees/:brand/:product`
5. Update `treesStore.save()`:
   - Posts to `POST /api/trees/:brand/:product`
6. Update `App.vue`:
   - Watch route params for `:brand` and `:product`
   - When both are present, load brand + trees stores
   - When navigating away, clear store state

**Validator:**
- `bun run build` passes
- Stores compile with new signatures

### Phase 3: Move view components + build new navigation

**Builder:**
1. Move from `_template-product/src/` to `apps/infinite-ui/src/`:
   - `workspace/WorkspaceView.vue`, `workspace/BrandView.vue`
   - `canvas/CanvasView.vue`, `canvas/TreeNode.vue`, `canvas/BranchNode.vue`, `canvas/LeafNode.vue`
   - `gallery/GalleryHome.vue`, `gallery/TreeView.vue`, `gallery/BranchPreview.vue`
   - All `layout/` components (Sidebar, BrandPanel, editors, etc.)
2. Update `router/index.ts` with all routes
3. Update `BranchPreview.vue` dynamic import path — leaves are now at `../brands/${brand}/products/${product}/trees/${tree}/${branch}/index.vue`

4. **Create `BreadcrumbBar.vue`** — floating nav bar:
   - `position: fixed`, top, full width, `z-index: 1000`
   - Translucent background with `backdrop-filter: blur(12px)`
   - Left: ☰ menu icon button (toggles sidebar via `sidebarStore.toggle()`)
   - Center: breadcrumb segments built from `useRoute().params` — each segment is a `<router-link>`
   - Right: subtle hotkey hints — `Ctrl+S` (sidebar) and `Ctrl+H` (hide nav), muted text
   - Reactive: segments update automatically as route changes
   - Hidden state controlled by a `navVisible` ref

5. **Redesign `TreesPanel.vue`** — filesystem-like tree explorer:
   - Fetch brand/product data from stores
   - Render collapsible tree structure:
     - Brand name (root, non-collapsible)
       - Product name (collapsible group)
         - Tree name (collapsible group, shows branch count)
           - Branch name (leaf item, status icon ✓/●/✗/○)
   - Click a branch → `router.push()` to that leaf's route
   - Chevron icons for expand/collapse
   - Indentation with left-border lines (like VS Code)

6. **Redesign `Sidebar.vue`** — overlay mode:
   - `position: fixed`, left, full height, `z-index: 900`
   - Slides in/out with transition (translateX)
   - Semi-transparent backdrop behind it (click to close)
   - NOT visible by default — opens via ☰ or Ctrl+S
   - Close button + Ctrl+S to close
   - Tabs: Brand | Trees | Settings

7. **Update `App.vue`**:
   - Import `BreadcrumbBar` — render at top level (always present)
   - Import `Sidebar` — render as overlay (hidden by default)
   - Register global keyboard listeners:
     - `Ctrl+H` → toggle `navVisible` (breadcrumb bar)
     - `Ctrl+S` → `preventDefault()` + toggle sidebar (prevent browser save dialog)
   - Content takes full width (no sidebar flex layout — sidebar overlays)
   - Add top padding to `<router-view>` to account for floating breadcrumb height

**Validator:**
- `bun run build` passes
- All routes resolve
- Breadcrumb shows correct segments for each route depth
- Ctrl+H toggles breadcrumb visibility
- Ctrl+S toggles sidebar
- Trees panel shows filesystem tree structure

### Phase 4: Migrate brand data

**Builder:**
1. Move `_template/brand.yaml` → `src/brands/_template/brand.yaml`
2. Move `_template-product/` content → `src/brands/_template/products/_template-product/`
   - `brand.yaml`, `trees.yaml`, `trees/` directory with example leaves
3. Move `agentix/brand.yaml` → `src/brands/agentix/brand.yaml`
4. Move `agentix/cuts/` content → `src/brands/agentix/products/cuts/`
   - `brand.yaml`, `trees.yaml` (if exists), `trees/` directory with generated leaves (hero-centered, hero-split, hero-cinematic)
5. Remove old per-product app files (package.json, vite.config.ts, node_modules, etc. from each product dir)
6. Install dependencies at root: `cd apps/infinite-ui && bun install`

**Validator:**
- All brand.yaml and trees.yaml files exist at new paths
- Example leaves exist at new paths
- Generated cuts leaves exist at new paths
- `bun run build` passes
- `bun run dev` serves the app, workspace shows brands

### Phase 5: Update justfile + agent system

**Builder:**
1. Update `justfile`:
   - `dev` recipe: `cd apps/infinite-ui && bun run dev` (no brand/product args — one app)
   - All other recipes stay the same (they talk to the team system, not the app)
2. Update agent domain paths in `.pi/multi-team/agents/*.md`:
   - Change `apps/infinite-ui/` paths to reflect new `src/brands/` structure
3. Update `shared_context` in `.pi/multi-team/multi-team-config.yaml`:
   - Point to `apps/infinite-ui/src/brands/_template/` paths
4. Update `.pi/prompts/multi-team/*.md` command files:
   - Paths agents write to: `apps/infinite-ui/src/brands/$BRAND/products/$PRODUCT/trees/`
5. Update `scripts/list.py`:
   - `APPS_DIR` now points to `apps/infinite-ui/src/brands`
   - Product dirs are under `<brand>/products/`

**Validator:**
- `just --list` shows updated recipes
- `just dev` starts the app
- `uv run --script scripts/list.py brands` works with new paths
- Agent config YAML parses correctly
- All shared_context paths exist

### Phase 6: Playwright validation

**Validator (Playwright only):**
1. Start dev server: `just dev`
2. Open `http://localhost:5173`
3. Verify workspace shows brands (_template, agentix)
4. Click agentix → verify products (cuts)
5. Click cuts → verify canvas with VueFlow nodes
6. Navigate to gallery → verify trees
7. Click into a tree → verify branches
8. Click a branch → verify leaf renders
9. Test sidebar: palette colors visible, tabs switch
10. Screenshot each view for evidence

---

## Key Decisions

| Decision | Choice |
|----------|--------|
| App count | **One app total** |
| Dev command | `just dev` (no args) |
| Brand data location | `src/brands/<brand>/` |
| Product data location | `src/brands/<brand>/products/<product>/` |
| Leaf dynamic imports | `../brands/${brand}/products/${product}/trees/${tree}/${branch}/index.vue` |
| Vite API endpoints | Parameterized by brand/product from URL |
| Store context | Route params drive which brand/product is loaded |
| Sidebar | Shows active product's brand config, switches on navigation |

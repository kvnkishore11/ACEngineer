# Plan: Canvas Activity Indicator & Brand Node Enrichment

## Task Description
Two enhancements to the canvas view in the Infinite UI app:
1. **Live generation activity indicator** — surface what agents are currently building. Introduce an `activity.yaml` file that agents write during generation, a new Vite API endpoint to serve it, a Pinia store that polls for changes, and a canvas overlay panel showing in-progress and queued work.
2. **Brand node enrichment** — replace the minimal brand-name-only `LeafNode.vue` with a richer `BrandNode.vue` that displays palette swatches, tagline, product name, tree/branch counts, and status summary — making the leftmost canvas node actually informative.

## Objective
When complete, the canvas view will:
- Show a live activity panel (bottom-right overlay) whenever branches are being generated/validated, with per-branch status and team assignment
- Auto-refresh trees.yaml via polling so branch node statuses update without manual reload
- Display a rich brand card as the leftmost canvas node with palette preview, tagline, product context, and aggregate metrics

## Problem Statement
Currently the canvas is a static snapshot — users navigate to it and see whatever trees.yaml contained at load time. During multi-team generation runs (which can take minutes), there's no visibility into what's happening. The brand node shows only a name label, wasting prime canvas real estate that could orient users with brand context at a glance.

## Solution Approach

### Feature 1: Activity Indicator

**New file convention**: Agents write `activity.yaml` alongside `trees.yaml` in each product directory during generation runs. This is a lightweight sidecar file — not a schema-validated manifest, just a status signal.

```yaml
# apps/infinite-ui/src/brands/{brand}/products/{product}/activity.yaml
active: true
started: "2026-04-02T14:30:00Z"
pipeline: generate           # generate | validate | fork-leaf | rebrand
brief: "Hero sections with bold typography"
branches:
  - slug: landing-v1
    tree: landing
    phase: generating        # scaffolding | generating | validating | done | failed
    team: "UI Generation"
  - slug: landing-v2
    tree: landing
    phase: validating
    team: "Validation B"
  - slug: landing-v3
    tree: landing
    phase: done
    team: "UI Generation C"
```

**Why activity.yaml instead of extending trees.yaml**: The trees.yaml manifest is the source of truth validated by Zod schemas. Adding transient fields (team assignment, pipeline phase, timing) would pollute a clean contract. A sidecar file keeps concerns separated — agents write activity.yaml during runs and delete it (or set `active: false`) when the pipeline completes.

**Agent-side changes**: The orchestrator and setup lead agent prompts need a small addition — the scaffold worker writes `activity.yaml` at pipeline start and the setup lead clears it at pipeline end. This is a prompt-level change in `.pi/prompts/multi-team/generate.md` and `.pi/multi-team/agents/scaffold-worker.md`.

**UI-side changes**:
- New Vite endpoint: `GET /api/activity/{brand}/{product}` — reads activity.yaml, returns 404 if absent
- New Pinia store: `activityStore` — polls the endpoint every 3 seconds when the canvas is mounted, stops when unmounted
- The activity store also triggers `treesStore.load()` on each poll cycle so branch statuses stay fresh
- New overlay component: `ActivityPanel.vue` — fixed bottom-right, shows pipeline name, brief, per-branch progress with status dots and team labels. Collapses to a small pulsing indicator when minimized.

### Feature 2: Brand Node Enrichment

Replace `LeafNode.vue` (31 lines, label-only) with a new `BrandNode.vue` that reads from both `brandStore.config` and `treesStore` to display:

- **Brand name** (existing)
- **Product name** (from treesStore.manifest.product)
- **Tagline** (from brandStore.config.tagline)
- **Palette preview** — 5 color dots (primary, secondary, accent, success, error)
- **Metrics row** — tree count, branch count, validated count
- **Activity pulse** — small animated dot when activity.yaml reports `active: true`

The dagre layout node size needs to increase from `160×50` to `220×140` to accommodate the richer content.

## Relevant Files
Use these files to complete the task:

**Stores (modify)**
- `apps/infinite-ui/src/stores/trees.ts` — add polling support, expose status aggregates (validated/generating/failed counts)
- `apps/infinite-ui/src/stores/brand.ts` — already has full config, no changes needed but consumed by BrandNode
- `apps/infinite-ui/src/stores/canvas.ts` — add activity panel visibility toggle

**Canvas components (modify)**
- `apps/infinite-ui/src/canvas/CanvasView.vue` — register BrandNode type, mount ActivityPanel, start/stop polling on mount/unmount
- `apps/infinite-ui/src/canvas/LeafNode.vue` — replaced by BrandNode.vue (delete or keep as alias)

**Vite config (modify)**
- `apps/infinite-ui/vite.config.ts` — add `GET /api/activity/{brand}/{product}` endpoint

**Agent prompts (modify)**
- `.pi/prompts/multi-team/generate.md` — add activity.yaml write/clear steps to workflow
- `.pi/multi-team/agents/scaffold-worker.md` — add instruction to write activity.yaml during scaffold phase
- `.pi/multi-team/agents/setup-lead.md` — add instruction to clear activity.yaml after final status update

**Schemas (no change)**
- `apps/infinite-ui/src/schemas/trees.schema.ts` — unchanged, activity.yaml is intentionally unschema'd
- `apps/infinite-ui/src/schemas/brand.schema.ts` — unchanged

### New Files
- `apps/infinite-ui/src/stores/activity.ts` — Pinia store for polling activity.yaml
- `apps/infinite-ui/src/canvas/BrandNode.vue` — rich brand card replacing LeafNode
- `apps/infinite-ui/src/canvas/ActivityPanel.vue` — overlay panel showing generation progress

## Implementation Phases

### Phase 1: Foundation
- Create `activity.ts` store with polling logic
- Add `/api/activity` Vite endpoint
- Update `trees.ts` store with status aggregates and a `reload()` method the activity store can call

### Phase 2: Core Implementation
- Build `BrandNode.vue` with palette swatches, tagline, metrics
- Build `ActivityPanel.vue` with branch progress list
- Wire both into `CanvasView.vue`
- Update dagre layout sizing for the new brand node dimensions
- Update agent prompts to write/clear activity.yaml

### Phase 3: Integration & Polish
- Add activity pulse animation to BrandNode when generation is active
- Add minimize/expand toggle to ActivityPanel
- Test with real generation run (write a mock activity.yaml manually first)
- Ensure polling starts/stops cleanly on route changes

## Team Orchestration

- You operate as the team lead and orchestrate the team to execute the plan.
- You're responsible for deploying the right team members with the right context to execute the plan.
- IMPORTANT: You NEVER operate directly on the codebase. You use `Task` and `Task*` tools to deploy team members to to the building, validating, testing, deploying, and other tasks.
  - This is critical. You're job is to act as a high level director of the team, not a builder.
  - You're role is to validate all work is going well and make sure the team is on track to complete the plan.
  - You'll orchestrate this by using the Task* Tools to manage coordination between the team members.
  - Communication is paramount. You'll use the Task* Tools to communicate with the team members and ensure they're on track to complete the plan.
- Take note of the session id of each team member. This is how you'll reference them.

### Team Members

- Builder
  - Name: builder-stores
  - Role: Build the activity store, update trees store with aggregates and polling support, update canvas store with activity panel toggle
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-canvas
  - Role: Build BrandNode.vue, ActivityPanel.vue, update CanvasView.vue registration and mounting, update dagre layout sizing in trees.ts
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-api-prompts
  - Role: Add /api/activity Vite endpoint, update agent prompts (generate.md, scaffold-worker.md, setup-lead.md) to write/clear activity.yaml
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-validator
  - Role: Validate all changes compile, dev server starts, canvas renders correctly with new components
  - Agent Type: general-purpose
  - Resume: true

## Step by Step Tasks

- IMPORTANT: Execute every step in order, top to bottom. Each task maps directly to a `TaskCreate` call.
- Before you start, run `TaskCreate` to create the initial task list that all team members can see and execute.

### 1. Add Activity API Endpoint + Agent Prompt Updates
- **Task ID**: api-and-prompts
- **Depends On**: none
- **Assigned To**: builder-api-prompts
- **Agent Type**: general-purpose
- **Parallel**: true (independent of store/canvas work)
- Add `GET /api/activity/:brand/:product` route to `apps/infinite-ui/vite.config.ts` — read `activity.yaml` from `brands/{brand}/products/{product}/activity.yaml`, return YAML text or 404
- Update `.pi/prompts/multi-team/generate.md` — in step 1 (Setup delegation), add: "Write `activity.yaml` with `active: true`, pipeline name, brief, and branch list with initial phase `scaffolding`". In step 7 (final Setup delegation), add: "Clear `activity.yaml` (set `active: false` or delete)"
- Update `.pi/multi-team/agents/scaffold-worker.md` — add instruction: "When scaffolding branches for a generation run, write `activity.yaml` alongside `trees.yaml` with branch slugs, tree assignments, and phase: scaffolding"
- Update `.pi/multi-team/agents/setup-lead.md` — add instruction: "After updating final statuses in trees.yaml, clear activity.yaml by setting `active: false`"

### 2. Build Activity Store + Update Trees Store
- **Task ID**: stores
- **Depends On**: none
- **Assigned To**: builder-stores
- **Agent Type**: general-purpose
- **Parallel**: true (independent of canvas/API work)
- Create `apps/infinite-ui/src/stores/activity.ts`:
  - State: `activity` ref (parsed activity.yaml or null), `isActive` computed (activity?.active === true), `branches` computed (activity?.branches ?? [])
  - `startPolling(brand, product)` — fetch `/api/activity/{brand}/{product}` every 3s, parse YAML, update state. On each poll also call `treesStore.load()` to refresh branch statuses. Use `setInterval` stored in a ref.
  - `stopPolling()` — clear interval, reset state
  - Export: `activity`, `isActive`, `branches`, `startPolling`, `stopPolling`
- Update `apps/infinite-ui/src/stores/trees.ts`:
  - Add computed `statusCounts`: `{ validated: number, generating: number, validating: number, draft: number, failed: number }` derived from all branches across all trees
  - Add computed `validatedCount`: shorthand for statusCounts.validated
- Update `apps/infinite-ui/src/stores/canvas.ts`:
  - Add `activityPanelOpen` ref (default true), `toggleActivityPanel()` method

### 3. Build BrandNode Component
- **Task ID**: brand-node
- **Depends On**: stores
- **Assigned To**: builder-canvas
- **Agent Type**: general-purpose
- **Parallel**: false (needs stores complete for type-safe access)
- Create `apps/infinite-ui/src/canvas/BrandNode.vue`:
  - Props: `data: { label: string }` (same interface as LeafNode for compatibility)
  - Imports: `useBrandStore`, `useTreesStore`, `useActivityStore`
  - Template structure:
    ```
    .brand-node
      .brand-header
        .brand-name         ← brand name (data.label)
        .brand-product      ← "/ {product}" from treesStore
      .brand-tagline        ← from brandStore.config.tagline
      .brand-palette        ← 5 color dots (primary, secondary, accent, success, error)
      .brand-metrics        ← "{N} trees · {N} branches · {N} validated"
      .activity-pulse       ← small animated dot, visible only when activityStore.isActive
      Handle(source, Right)
    ```
  - Styling: all brand tokens, 220px wide, surface background, primary border, rounded
  - The activity pulse: a small 8px dot with CSS animation (scale pulse) using `--brand-accent`, only rendered when `activityStore.isActive`
- Update `apps/infinite-ui/src/stores/trees.ts` — change brand node dagre size from `{ width: 160, height: 50 }` to `{ width: 220, height: 140 }`
- Update `apps/infinite-ui/src/canvas/CanvasView.vue`:
  - Import `BrandNode` instead of `LeafNode`
  - Change nodeTypes mapping: `brand: markRaw(BrandNode)`
  - Import and call `useActivityStore` — call `startPolling()` on mount, `stopPolling()` on unmount via `onMounted`/`onUnmounted`

### 4. Build Activity Panel
- **Task ID**: activity-panel
- **Depends On**: stores
- **Assigned To**: builder-canvas
- **Agent Type**: general-purpose
- **Parallel**: false (needs stores, builds on same canvas context as brand-node)
- Create `apps/infinite-ui/src/canvas/ActivityPanel.vue`:
  - Imports: `useActivityStore`, `useCanvasStore`
  - Only renders when `activityStore.isActive`
  - Template structure:
    ```
    .activity-panel (v-if="activityStore.isActive")
      .activity-header
        .activity-title      ← "Generating" / "Validating" / pipeline name
        .activity-brief      ← the generation brief text
        button.minimize      ← toggles canvasStore.activityPanelOpen
      .activity-branches (v-if="canvasStore.activityPanelOpen")
        .activity-branch (v-for branch)
          .branch-status-dot ← colored by phase (scaffolding=muted, generating=accent, validating=warning, done=success, failed=error)
          .branch-slug       ← branch slug
          .branch-team       ← team assignment label
          .branch-phase      ← phase text
    ```
  - Styling: fixed position bottom-right, 320px wide, surface background, border, shadow-lg, z-index above canvas, max-height 300px with overflow scroll
  - Minimized state: collapse to just the header row with a branch count badge
- Mount `ActivityPanel` inside `CanvasView.vue` template (after VueFlow)

### 5. Validate All Changes
- **Task ID**: validate-all
- **Depends On**: api-and-prompts, stores, brand-node, activity-panel
- **Assigned To**: builder-validator
- **Agent Type**: general-purpose
- **Parallel**: false
- Run `cd apps/infinite-ui && npx vue-tsc --noEmit` to verify TypeScript compiles
- Run `cd apps/infinite-ui && bun run dev` briefly to verify dev server starts and no runtime errors
- Manually create a mock `activity.yaml` in `apps/infinite-ui/src/brands/agentix/products/cuts/activity.yaml` to verify the panel renders:
  ```yaml
  active: true
  started: "2026-04-02T14:30:00Z"
  pipeline: generate
  brief: "Testing activity indicator"
  branches:
    - slug: hero-centered
      tree: landing
      phase: generating
      team: "UI Generation"
  ```
- Verify canvas loads with enriched brand node showing palette dots, tagline, counts
- Verify activity panel appears with mock data
- Delete mock activity.yaml after verification
- Report any issues found

## Acceptance Criteria

- [ ] Brand node on canvas shows: brand name, product name, tagline, 5 palette dots, tree/branch/validated counts
- [ ] Brand node shows a pulsing activity dot when generation is active
- [ ] Activity panel appears bottom-right during active generation with per-branch status
- [ ] Activity panel is dismissible (minimize to header-only)
- [ ] Canvas auto-refreshes trees.yaml every 3 seconds during active polling so branch statuses update live
- [ ] Polling starts on canvas mount, stops on unmount (no leaked intervals)
- [ ] `/api/activity/{brand}/{product}` endpoint returns activity.yaml content or 404
- [ ] Agent prompts updated so scaffold-worker writes activity.yaml and setup-lead clears it
- [ ] TypeScript compiles with no errors
- [ ] All existing canvas functionality preserved (node clicks, preview branches, minimap)

## Validation Commands
Execute these commands to validate the task is complete:

- `cd apps/infinite-ui && npx vue-tsc --noEmit` — TypeScript compilation check
- `cd apps/infinite-ui && bun run dev` — Dev server starts without errors
- `curl http://localhost:5173/api/activity/agentix/cuts` — Returns 404 (no active generation)
- Create mock activity.yaml, refresh canvas, verify panel renders
- Navigate to `/agentix/cuts` canvas, verify brand node shows palette + metrics + tagline

## Notes

- The 3-second polling interval is a pragmatic choice — fast enough for visibility, slow enough to not spam the filesystem. Could be made configurable later.
- `activity.yaml` is intentionally NOT Zod-validated. It's a transient signal file, not a contract. If it's malformed, the store should silently fall back to `null`.
- The polling also refreshes trees.yaml, which means branch nodes will update their status colors in near-real-time during generation runs. This is the main UX win — watching branches go from `generating` → `validating` → `validated` live on the canvas.
- No WebSocket needed — file polling through the Vite dev server is sufficient for a local development tool.

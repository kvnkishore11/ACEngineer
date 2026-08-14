# Plan: Canvas Leaf Preview Iframes

## Task Description
Embed live iframe previews of leaf components directly inside the VueFlow canvas branch nodes. Instead of just seeing a card with the branch name and status, users see a miniature rendered preview of the actual generated UI. Add resize controls so users can adjust the preview size. This lets you see the application right away without navigating into it.

## Objective
When viewing the canvas at `/:brand/:product`, each branch node renders an iframe showing the actual leaf component at a small preview size (default 16:9 aspect ratio, approximately 480x270). Users can resize previews via controls on the canvas. Clicking the preview still navigates to the full leaf view.

## Problem Statement
Currently branch nodes on the canvas show only name + status text. To see what a generated UI looks like, you have to click into the gallery and navigate to the leaf. This breaks the design flow — you want to see all variants at a glance on the canvas without leaving it.

## Solution Approach
Replace the simple BranchNode card with a new `PreviewBranchNode` that contains an iframe pointing to the leaf's gallery route (`/:brand/:product/gallery/:tree/:branch`). The iframe is scaled down using CSS `transform: scale()` inside a fixed-size container to create a miniature preview. A resize handle and preset size buttons let users adjust the preview dimensions. The existing `BranchNode` is kept as a fallback for branches with `status !== 'validated'` (no point previewing draft/failed branches).

## Relevant Files

- `apps/infinite-ui/src/canvas/BranchNode.vue` — current branch node (keep as fallback for non-validated)
- `apps/infinite-ui/src/canvas/CanvasView.vue` — registers node types, handles clicks
- `apps/infinite-ui/src/stores/trees.ts` — provides node data with branch info
- `apps/infinite-ui/src/stores/canvas.ts` — zoom/pan/selection state
- `apps/infinite-ui/src/gallery/BranchPreview.vue` — the leaf loader (iframe target)

### New Files
- `apps/infinite-ui/src/canvas/PreviewBranchNode.vue` — new branch node with embedded iframe preview
- `apps/infinite-ui/src/canvas/PreviewControls.vue` — resize controls (preset sizes + drag handle)

## Implementation Phases

### Phase 1: PreviewBranchNode Component
Create the iframe-based branch node that renders a live preview of the leaf component.

**Key design decisions:**
- Use an iframe pointing to the app's own route: `/:brand/:product/gallery/:tree/:branch`
- The iframe loads the same Vue app — the leaf renders inside it with full brand tokens
- Render the full page at 1280x720 inside the iframe, then CSS `transform: scale(0.375)` to fit into a 480x270 container (16:9)
- Container has `overflow: hidden`, `pointer-events: none` on the iframe (clicks go to the node, not into the iframe)
- Status badge overlay in the corner
- Branch name below the preview

**Aspect ratio math (16:9):**
- Small: 480x270 (renders 1280x720 at scale 0.375)
- Medium: 640x360 (renders 1280x720 at scale 0.5)
- Large: 960x540 (renders 1280x720 at scale 0.75)

### Phase 2: Preview Size Controls
Add controls to adjust preview size. Two approaches combined:
- **Preset buttons**: S / M / L on the canvas toolbar
- **Per-node resize**: drag handle on the bottom-right corner of each preview node

Store the preview size preference in `canvasStore` so it persists during the session.

### Phase 3: Canvas Integration
Wire PreviewBranchNode into the canvas:
- Register as a new node type `preview-branch` in CanvasView
- Update the trees store to use `preview-branch` type for validated branches, `branch` type for others
- Increase dagre node dimensions for preview nodes to account for the larger size
- Adjust dagre `nodesep` and `ranksep` for the bigger nodes

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
  - Name: builder-preview
  - Role: Build the PreviewBranchNode, PreviewControls, and canvas integration
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: validator-preview
  - Role: Validate the build via Playwright — verify iframes render, resize controls work, navigation still works
  - Agent Type: general-purpose
  - Resume: true

## Step by Step Tasks

### 1. Create PreviewBranchNode Component
- **Task ID**: create-preview-node
- **Depends On**: none
- **Assigned To**: builder-preview
- **Agent Type**: general-purpose
- **Parallel**: false
- Read `apps/infinite-ui/src/canvas/BranchNode.vue` to understand existing node structure
- Read `apps/infinite-ui/src/canvas/CanvasView.vue` to understand node type registration
- Create `apps/infinite-ui/src/canvas/PreviewBranchNode.vue`:
  - Props: `data` with `slug`, `name`, `description`, `status`, `treeSlug` (same as BranchNode)
  - Computed `previewUrl`: builds `/${brand}/${product}/gallery/${treeSlug}/${slug}` from route params
  - Template: container div with fixed 16:9 aspect ratio, iframe inside scaled down via CSS transform
  - The iframe renders at 1280x720, container clips to preview size (default 480x270, scale 0.375)
  - `pointer-events: none` on iframe so clicks pass through to the VueFlow node
  - Status badge absolutely positioned in top-right corner
  - Branch name below the preview
  - VueFlow Handle components for edge connections (target left, source right — matching BranchNode)
  - Hover: subtle shadow elevation
- All styling via brand CSS custom properties

### 2. Create PreviewControls Component
- **Task ID**: create-preview-controls
- **Depends On**: none
- **Assigned To**: builder-preview
- **Agent Type**: general-purpose
- **Parallel**: true (can run alongside task 1)
- Create `apps/infinite-ui/src/canvas/PreviewControls.vue`:
  - Three preset size buttons: S (480x270), M (640x360), L (960x540)
  - Floating toolbar positioned at top-right of the canvas
  - Active state highlighting on the selected size
  - Emits `update:size` event with `{ width, height, scale }` payload
  - Styled with brand tokens, translucent background with backdrop-blur (matching breadcrumb bar)
- Update `apps/infinite-ui/src/stores/canvas.ts`:
  - Add `previewSize` ref with default `{ width: 480, height: 270, scale: 0.375 }`
  - Add `setPreviewSize(size)` action
  - Size presets: `small` (480x270, 0.375), `medium` (640x360, 0.5), `large` (960x540, 0.75)

### 3. Integrate into Canvas
- **Task ID**: integrate-canvas
- **Depends On**: create-preview-node, create-preview-controls
- **Assigned To**: builder-preview
- **Agent Type**: general-purpose
- **Parallel**: false
- Update `apps/infinite-ui/src/canvas/CanvasView.vue`:
  - Import and register `PreviewBranchNode` as node type `preview-branch`
  - Import and add `PreviewControls` component (positioned absolutely in top-right of canvas)
  - Pass `previewSize` from canvasStore to PreviewBranchNode nodes (via data or provide/inject)
- Update `apps/infinite-ui/src/stores/trees.ts`:
  - In the `nodes` computed, set node type to `preview-branch` for branches with `status === 'validated'`, keep `branch` type for others
  - Update dagre node dimensions for `preview-branch` nodes: use `canvasStore.previewSize.width + 40` x `canvasStore.previewSize.height + 60` (padding for name + status)
  - Increase `ranksep` to 180 to give preview nodes breathing room
- Verify `bun run build` passes

### 4. Validate with Playwright
- **Task ID**: validate-preview
- **Depends On**: integrate-canvas
- **Assigned To**: validator-preview
- **Agent Type**: general-purpose
- **Parallel**: false
- Start dev server: `cd apps/infinite-ui && bun run dev`
- Open Playwright session, navigate to `http://localhost:<port>/agentix/cuts`
- Verify: preview branch nodes render with visible iframe content
- Screenshot the canvas with previews visible
- Test size controls: click S/M/L buttons, verify preview sizes change
- Test click-through: click a preview node, verify navigation to leaf route
- Test non-validated branches: verify they still show the simple BranchNode (not preview)
- Screenshot at each size preset
- Verify `bun run build` passes

## Acceptance Criteria
- Branch nodes for validated branches show a live rendered preview of the leaf component
- Preview is 16:9 aspect ratio, default 480x270
- Three size presets (S/M/L) accessible via toolbar buttons
- Clicking a preview node still navigates to the full leaf view
- Non-validated branches (draft/generating/failed) show the original simple node
- Dagre layout adapts to preview node dimensions
- `bun run build` passes with zero errors
- No iframe scrollbar visible (overflow hidden)
- Preview is non-interactive (pointer-events: none on iframe)

## Validation Commands
- `cd apps/infinite-ui && bun run build` — TypeScript + Vite build passes
- `playwright-cli -s=preview-test open http://localhost:<port>/agentix/cuts` — canvas renders with preview nodes
- `playwright-cli -s=preview-test screenshot` — visual verification of previews

## Notes
- The iframe approach means each preview loads the full Vue app in a separate browsing context. For 3-6 branches this is fine. For 20+ branches it could get heavy — but that's a future optimization (screenshot thumbnails instead of live iframes).
- The `pointer-events: none` on the iframe prevents interaction inside the preview. Users must click the node border/name area to navigate. This is intentional — the preview is for viewing, not interacting.
- The iframe URL uses the same dev server, so brand tokens cascade correctly — the preview looks exactly like the full view.

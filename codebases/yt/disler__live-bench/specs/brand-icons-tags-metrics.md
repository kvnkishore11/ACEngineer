# Plan: Brand Icons — Tags & Metric Bar Icons

## Task Description
Add brand identity to benchmarks by introducing two features:
1. **Tags with icons** — A new `tags` field on `BenchmarkConfig` that displays branded pill-style tags between the page header and the chart grid. Each tag has a `name` and an array of `icons` (URLs to SVG logos) representing the companies/technologies involved in that benchmark entry.
2. **Metric bar icons** — A new optional `icon` field on `MetricDef` that renders a small logo between the top of each bar and its numeric value label, branding each bar with its model/backend origin.

Both features also require sourcing new SVG icon assets (Apple/MLX, NVIDIA, Qwen/Alibaba, Google/Gemma) and updating all 4 benchmark YAML files.

## Objective
When complete, every benchmark page will show branded tags below the header (e.g. "Qwen 3.5 35B-A3B" with Alibaba + NVIDIA icons) and each bar in the chart will display its brand icon between the bar top and the numeric value overlay.

## Problem Statement
The benchmarks currently display raw text labels with no visual brand identity. Viewers can't instantly tell which company/technology a model or backend belongs to. Adding icons makes the dashboard more presentation-ready and scannable at a glance.

## Solution Approach
- Add `tags` (list of `{name, icons[]}`) to `BenchmarkConfig` in Pydantic, Zod, and YAML.
- Add optional `icon` (string URL) to `MetricDef` in Pydantic, Zod, and YAML.
- Create a new `TagBar.vue` component that renders horizontally between the page header and the chart grid.
- Modify `AnimatedBar.vue` to render an `<image>` element between bar top and value text (BT mode) or beside the value (LR mode), increasing top padding to prevent clipping.
- Source/create SVG icons for Apple (MLX), NVIDIA (GGUF format origin), Alibaba (Qwen), and Google (Gemma).
- Update all 4 benchmark YAML files with tags and metric icons.

## Relevant Files
Use these files to complete the task:

**Backend models & config:**
- `apps/backend/src/live_bench_server/models.py` — Add `icon` to `MetricDef`, add `TagDef` model, add `tags` to `BenchmarkConfig`
- `apps/backend/src/live_bench_server/config.py` — No changes needed (YAML loader is schema-driven)

**Frontend schemas:**
- `apps/frontend/src/schemas.ts` — Add `icon` to `MetricDefSchema`, add `TagDefSchema`, add `tags` to `BenchmarkConfigSchema`

**Frontend components:**
- `apps/frontend/src/components/AnimatedBar.vue` — Render metric icon between bar top and value label
- `apps/frontend/src/components/GroupedBarChart.vue` — Pass metric icon through Cell, increase top padding for icon space
- `apps/frontend/src/pages/BenchmarkPage.vue` — Render `TagBar` between header and grid

**Frontend styles:**
- `apps/frontend/src/styles/main.css` — Add `.tag-bar`, `.tag-bar__tag`, `.tag-bar__icon` styles

**Benchmark definitions (YAML):**
- `benchmarks/qwen35-vs-gemma4.yaml` — Add tags + metric icons
- `benchmarks/context-scaling.yaml` — Add tags + metric icons
- `benchmarks/pi-coding-agent.yaml` — Add tags + metric icons
- `benchmarks/mock-test.yaml` — Optionally add tags for testing

**Icon assets:**
- `apps/frontend/public/icons/alibaba.svg` — Already exists (Qwen)
- `apps/frontend/public/icons/google.svg` — Already exists (Gemma)

### New Files
- `apps/frontend/public/icons/apple.svg` — Apple logo for MLX backend
- `apps/frontend/public/icons/nvidia.svg` — NVIDIA logo for GGUF format
- `apps/frontend/src/components/TagBar.vue` — New component for rendering tags between header and charts

## Implementation Phases
### Phase 1: Foundation
- Add `TagDef` Pydantic model and `tags` field to `BenchmarkConfig`
- Add `icon` field to `MetricDef` (Pydantic)
- Mirror both changes in Zod schemas
- Source Apple and NVIDIA SVG icons, add to `public/icons/`

### Phase 2: Core Implementation
- Build `TagBar.vue` component — horizontal row of pill-shaped tags, each showing its name and icon array
- Modify `AnimatedBar.vue` to accept and render an optional `icon` prop between bar top and value text
- Modify `GroupedBarChart.vue` to pass metric `icon` through Cell data and increase top padding when metric icons are present
- Wire `TagBar` into `BenchmarkPage.vue` between `<header>` and `<BenchmarkGrid>`

### Phase 3: Integration & Polish
- Update all 4 benchmark YAML files with tags and metric icons
- Visual testing: run `just mock` and verify tags render, icons display, bars have proper spacing
- Run `just test` to ensure no regressions

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
  - Name: builder-schema
  - Role: Backend Pydantic models + frontend Zod schema updates (TagDef, MetricDef.icon, BenchmarkConfig.tags)
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-icons
  - Role: Source/create Apple and NVIDIA SVG icon files, place in public/icons/
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-frontend
  - Role: Build TagBar.vue, modify AnimatedBar.vue and GroupedBarChart.vue for metric icons, wire TagBar into BenchmarkPage.vue, add CSS
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: builder-yaml
  - Role: Update all 4 benchmark YAML files with tags and metric icons
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: validator
  - Role: Run all tests, start dev server, verify visual rendering
  - Agent Type: general-purpose
  - Resume: false

## Step by Step Tasks

### 1. Add TagDef model and MetricDef.icon to backend Pydantic models
- **Task ID**: schema-backend
- **Depends On**: none
- **Assigned To**: builder-schema
- **Agent Type**: general-purpose
- **Parallel**: true
- In `apps/backend/src/live_bench_server/models.py`:
  - Add a `TagDef` model (subclass of `_LiveBenchModel`):
    ```python
    class TagDef(_LiveBenchModel):
        name: str
        icons: list[str] = Field(default_factory=list)  # URLs to icon SVGs
    ```
  - Add `icon: str | None = None` field to `MetricDef` (after `color`)
  - Add `tags: list[TagDef] | None = None` field to `BenchmarkConfig` (after `subtitle`)
  - Add `TagDef` to `__all__`

### 2. Mirror schema changes in frontend Zod
- **Task ID**: schema-frontend
- **Depends On**: schema-backend
- **Assigned To**: builder-schema
- **Agent Type**: general-purpose
- **Parallel**: false
- In `apps/frontend/src/schemas.ts`:
  - Add `TagDefSchema`:
    ```typescript
    export const TagDefSchema = z.object({
      name: z.string(),
      icons: z.array(z.string()).default([]),
    })
    ```
  - Add `icon: z.string().nullish()` to `MetricDefSchema`
  - Add `tags: z.array(TagDefSchema).nullish()` to `BenchmarkConfigSchema` (after `subtitle`)
  - Export `TagDef` type: `export type TagDef = z.infer<typeof TagDefSchema>`

### 3. Source and create SVG icon assets
- **Task ID**: icons-assets
- **Depends On**: none
- **Assigned To**: builder-icons
- **Agent Type**: general-purpose
- **Parallel**: true
- Create minimal, clean SVG icons suitable for 20-27px rendering on dark backgrounds:
  - `apps/frontend/public/icons/apple.svg` — Apple logo (white fill, works on dark theme)
  - `apps/frontend/public/icons/nvidia.svg` — NVIDIA logo (green #76B900 fill)
- Verify existing icons still work:
  - `apps/frontend/public/icons/alibaba.svg` — already exists
  - `apps/frontend/public/icons/google.svg` — already exists

### 4. Build TagBar.vue component
- **Task ID**: tagbar-component
- **Depends On**: schema-frontend
- **Assigned To**: builder-frontend
- **Agent Type**: general-purpose
- **Parallel**: false
- Create `apps/frontend/src/components/TagBar.vue`:
  - Props: `tags: TagDef[]`
  - Renders a horizontal flex row of pill-shaped tags
  - Each tag shows its `name` text and renders each icon in `icons[]` as a small `<img>` (20px height)
  - Style: dark pill background (`var(--bg-card)`), border (`var(--border-card)`), rounded corners, horizontal gap
  - The row should wrap if there are many tags
- Add CSS to `apps/frontend/src/styles/main.css`:
  ```css
  .tag-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
  }
  .tag-bar__tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: var(--radius-pill);
    font-size: var(--fs-base);
    color: var(--fg-medium);
  }
  .tag-bar__icon {
    height: 20px;
    width: auto;
  }
  ```

### 5. Add metric icon rendering to bar charts
- **Task ID**: metric-icons-bars
- **Depends On**: schema-frontend, icons-assets
- **Assigned To**: builder-frontend
- **Agent Type**: general-purpose
- **Parallel**: false
- In `apps/frontend/src/components/GroupedBarChart.vue`:
  - Add `metricIcon: string | null` to the `Cell` interface
  - Populate `metricIcon` from `m.icon ?? null` in the cell computation (both BT and LR branches) — note: this is the **metric** icon, not the group icon
  - Add a computed `hasMetricIcons` that checks if any metric has an icon
  - When `hasMetricIcons` is true, increase `padTop` by ~30px (icon size + gap) so bars don't clip into the icon+value area
  - After the "bar text overlays" `<g>` block, add a new `<g>` block that renders `<image>` elements for each cell that has a `metricIcon`:
    - **BT mode**: Position the icon centered horizontally on the bar, vertically between the bar top and the value text. The icon should sit just above the bar top, and the value text should move up by icon height to accommodate. Specifically:
      - Icon: `x = cell center - METRIC_ICON_SIZE/2`, `y = bar_top - METRIC_ICON_SIZE - 4` (4px gap above bar)
      - Value text: shift up by `METRIC_ICON_SIZE + 8` from current position
    - **LR mode**: Position the icon to the left of the value text, vertically centered on the bar
  - Use `METRIC_ICON_SIZE = 20` (slightly smaller than group icons)
- In `apps/frontend/src/components/AnimatedBar.vue`:
  - Add optional `icon` prop: `icon?: string | null`
  - Adjust `overlayPos` computation for BT mode: when `icon` is provided, shift the text `y` up by an additional 24px (icon height + gap) to make room for the icon between text and bar
  - Render the icon as an SVG `<image>` element positioned between the text and the bar top:
    ```html
    <image
      v-if="icon && (layer ?? 'both') !== 'rect'"
      :href="icon"
      :x="overlayPos.x - 10"
      :y="overlayPos.y + 4"
      width="20"
      height="20"
    />
    ```

### 6. Wire TagBar into BenchmarkPage
- **Task ID**: tagbar-wire
- **Depends On**: tagbar-component
- **Assigned To**: builder-frontend
- **Agent Type**: general-purpose
- **Parallel**: false
- In `apps/frontend/src/pages/BenchmarkPage.vue`:
  - Import `TagBar` component
  - Add a computed `tags` that reads `session.config?.tags ?? []`
  - Insert `<TagBar v-if="tags.length" :tags="tags" />` between `</header>` and `<BenchmarkGrid>`

### 7. Update benchmark YAML files with tags and metric icons
- **Task ID**: yaml-update
- **Depends On**: schema-backend, icons-assets
- **Assigned To**: builder-yaml
- **Agent Type**: general-purpose
- **Parallel**: false
- Update `benchmarks/qwen35-vs-gemma4.yaml`:
  - Add tags after subtitle:
    ```yaml
    tags:
      - { name: "Qwen 3.5 35B-A3B", icons: ["/icons/alibaba.svg", "/icons/nvidia.svg"] }
      - { name: "Gemma 4 26B-A4B", icons: ["/icons/google.svg"] }
      - { name: "GGUF", icons: ["/icons/nvidia.svg"] }
      - { name: "MLX", icons: ["/icons/apple.svg"] }
    ```
  - Add icon to each metric in the `&model_metrics` anchor:
    ```yaml
    metrics: &model_metrics
      - { key: qwen_gguf,  label: "Qwen 3.5 GGUF",  color: "#f59e0b", icon: "/icons/alibaba.svg" }
      - { key: qwen_mlx,   label: "Qwen 3.5 MLX",   color: "#fbbf24", icon: "/icons/alibaba.svg" }
      - { key: gemma4_gguf, label: "Gemma 4 GGUF",   color: "#3b82f6", icon: "/icons/google.svg" }
      - { key: gemma4_mlx,  label: "Gemma 4 MLX",    color: "#60a5fa", icon: "/icons/google.svg" }
    ```
- Update `benchmarks/context-scaling.yaml`:
  - Add tags:
    ```yaml
    tags:
      - { name: "Gemma 4 26B", icons: ["/icons/google.svg"] }
      - { name: "Qwen 3.5 35B", icons: ["/icons/alibaba.svg"] }
      - { name: "MLX 4-bit", icons: ["/icons/apple.svg"] }
      - { name: "GraphWalks", icons: [] }
    ```
  - Add icon to metrics anchor:
    ```yaml
    metrics: &model_metrics
      - { key: gemma4_mlx, label: "Gemma 4 26B MLX", color: "#3498DB", icon: "/icons/google.svg" }
      - { key: qwen_mlx,   label: "Qwen 3.5 35B MLX", color: "#F39C12", icon: "/icons/alibaba.svg" }
    ```
- Update `benchmarks/pi-coding-agent.yaml`:
  - Add tags:
    ```yaml
    tags:
      - { name: "Qwen 3.5 35B", icons: ["/icons/alibaba.svg"] }
      - { name: "Qwen 3.5 Coding", icons: ["/icons/alibaba.svg"] }
      - { name: "Gemma 4 26B", icons: ["/icons/google.svg"] }
      - { name: "GGUF + MLX", icons: ["/icons/nvidia.svg", "/icons/apple.svg"] }
    ```
  - Add icon to metrics anchor:
    ```yaml
    metrics: &model_metrics
      - { key: qwen_gguf,    label: "Qwen 3.5 GGUF",    color: "#f59e0b", icon: "/icons/alibaba.svg" }
      - { key: qwen_mlx,     label: "Qwen 3.5 MLX",     color: "#fbbf24", icon: "/icons/alibaba.svg" }
      - { key: qwen_coding,  label: "Qwen 3.5 Coding",  color: "#34d399", icon: "/icons/alibaba.svg" }
      - { key: gemma4_gguf,  label: "Gemma 4 GGUF",     color: "#3b82f6", icon: "/icons/google.svg" }
    ```
- Update `benchmarks/mock-test.yaml` (**required** — this is the primary validation target):
  - Add tags:
    ```yaml
    tags:
      - { name: "Model A", icons: ["/icons/alibaba.svg"] }
      - { name: "Model B", icons: ["/icons/google.svg"] }
    ```
  - Add icon to metrics:
    ```yaml
    metrics:
      - { key: model_a, label: "Model A", color: "#f59e0b", icon: "/icons/alibaba.svg" }
      - { key: model_b, label: "Model B", color: "#3b82f6", icon: "/icons/google.svg" }
    ```

### 8. Validate with mock benchmark
- **Task ID**: validate-all
- **Depends On**: schema-backend, schema-frontend, icons-assets, tagbar-component, metric-icons-bars, tagbar-wire, yaml-update
- **Assigned To**: validator
- **Agent Type**: general-purpose
- **Parallel**: false
- Run `just test-backend` — ensure Pydantic model changes don't break existing tests
- Run `just test-frontend` — ensure Zod schema changes don't break existing tests
- Run `just build-frontend` — ensure TypeScript compilation passes
- Run `just mock` — this is the **primary validation**: it starts the server, emits fake data into mock-test, and opens the dashboard. Verify:
  - Tags render as pills between the page header and chart grid
  - Tag pills show icons inline with name text
  - Metric icons appear between the top of each bar and the numeric value label
  - No clipping or overlap between icons, values, and bars
  - Icons render correctly on the dark theme

## Acceptance Criteria
- `BenchmarkConfig` supports an optional `tags` field (list of `{name, icons[]}`)
- `MetricDef` supports an optional `icon` field (string URL)
- Tags render as styled pills between the page header (back link + title + subtitle) and the chart grid
- Each tag displays its name and inline icon images
- Metric icons render between the top of each bar and its numeric value label in BT mode
- Icons don't clip or overlap with adjacent elements
- All existing tests pass (`just test`)
- Frontend builds cleanly (`just build-frontend`)
- Apple and NVIDIA SVG icons exist in `apps/frontend/public/icons/`
- All 4 benchmark YAML files are updated with appropriate tags and metric icons

## Validation Commands
Execute these commands to validate the task is complete:

- `just test-backend` — Backend pytest suite passes with new model fields
- `just test-frontend` — Frontend vitest suite passes with new schema fields
- `just build-frontend` — TypeScript compilation succeeds
- `just mock` — **Primary validation**: starts server, emits mock data, verify tags + metric icons render correctly
- `ls apps/frontend/public/icons/` — Confirm apple.svg and nvidia.svg exist

## Notes
- The `GroupDef.icon` field already exists in both Pydantic and Zod — this plan adds the **separate** `MetricDef.icon` field. Group icons appear on the x-axis below bars; metric icons appear above bars next to values. They serve different purposes.
- SVG icons should use `currentColor` or light fills (white/light gray) for dark-theme compatibility, or use brand colors that contrast well against dark backgrounds.
- The NVIDIA icon represents the GGUF quantization format because NVIDIA developed the format. The Apple icon represents MLX because Apple developed the MLX framework.
- Tags are purely presentational — they don't affect data flow, SSE, or the ingest pipeline.
- No new Python dependencies needed. No new npm packages needed.

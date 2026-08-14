---
name: svg-generate
description: Hand-craft production-ready SVG vector images and animations. Use when the user asks to generate SVGs, create vector icons, animate SVGs, or build diagrams as SVG. Keywords - svg, generate, vector, icon, animate, hand-craft. .
---

# SVG Generate

## Purpose

Hand-craft production-ready SVG vector images from text descriptions. Supports static SVGs, CSS-animated SVGs, and batch generation with parallel subagents.

## Workflow

### 1. Parse parameters from the user's request

Extract these from the invocation arguments and conversation context:

| Parameter      | Source                                       | Default      |
| -------------- | -------------------------------------------- | ------------ |
| **prompt**     | User's image description                     | *(required)* |
| **count**      | Look for a number N, `count`, or `x3` style  | `1`          |
| **animate**    | If user says "animate", "animated", "motion" | `false`      |
| **loop after** | If user specifies "loop after Ns"            | none         |

### 2. Determine output directory

If the user specified an output directory, use it. If they did NOT, **ask the user** where they want the SVGs saved before proceeding. Suggest a sensible default like `/tmp/svg-output/` or a subdirectory of cwd.

### 3. Hand-craft the SVG(s)

Write each SVG file directly, crafting clean, semantic SVG code:

- Use proper `viewBox` attributes for scalability
- Prefer `<g>` groups for logical organization
- Use meaningful `id` and `class` attributes
- Keep paths clean and optimized
- No JavaScript - CSS only for animations
- No embedded raster images
- No text unless explicitly requested

For batch generation (count > 1):
- Give each SVG a unique creative angle or variation
- Use parallel subagents (one per SVG) for speed
- Name files `claude-svg-1.svg`, `claude-svg-2.svg`, etc.

### 4. Animation guidelines

If animation is requested, add CSS `@keyframes` animations inside a `<style>` block:

- Use `animation` shorthand on SVG elements
- Prefer `transform`, `opacity`, and `stroke-dashoffset` for smooth GPU-accelerated animation
- Keep animations subtle and purposeful
- Default to `infinite` iteration unless told otherwise

#### Cinematic reveal + ambient loop pattern

If the user mentions **"loop after"**, **"repeat after"**, or specifies a duration like **"loop after 10s"**, use this two-phase pattern:

1. **Phase 1 - One-shot reveal**: Stagger elements in with `fill="freeze"` fade-ins over the specified duration (default ~10s). Each element appears sequentially to create a cinematic build-up. These never repeat.
2. **Phase 2 - Ambient loop**: After the reveal completes, begin `repeatCount="indefinite"` animations that keep the SVG alive - subtle pulsing borders, traveling particle dots along connection paths, dashed-border marching, gentle opacity oscillation. These emphasize core relationships and data flow without changing layout.

The key principle: the reveal draws attention once, then ambient motion sustains visual interest indefinitely. Phase 2 should be **minimal** - only animate elements that reinforce the main idea (connections, flow, hierarchy). Never animate text content or move elements from their final positions.

### 5. Present results

After crafting completes:

1. List all generated SVG files with their paths
2. If count > 1, number them clearly
3. Briefly describe what each SVG depicts and any animations included

## Examples

**Basic:**
```
/svg-generate a flat icon of a rocket ship
```
-> Hand-crafts 1 static SVG.

**Batch with variations:**
```
/svg-generate a geometric wolf head, x5
```
-> Hand-crafts 5 unique SVG variations using parallel subagents.

**Animated:**
```
/svg-generate animate: a pulsing wifi signal icon, x3
```
-> Hand-crafts 3 animated SVGs with CSS keyframe animations.

**Cinematic reveal:**
```
/svg-generate animate, loop after 8s: a network architecture diagram
```
-> Hand-crafts an SVG with 8s staggered reveal, then ambient looping animations.

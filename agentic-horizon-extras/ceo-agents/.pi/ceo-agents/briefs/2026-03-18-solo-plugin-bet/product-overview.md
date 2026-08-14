# Product Overview — LayoutForge

## What It Is
A Figma plugin that auto-generates responsive layouts from rough wireframes. Users sketch a basic layout, hit "Forge," and get production-ready responsive variants (mobile, tablet, desktop) with proper auto-layout, constraints, and spacing tokens.

## How It Works
1. User draws rough frames with basic shapes in Figma
2. LayoutForge analyzes the spatial relationships and content hierarchy
3. Generates clean auto-layout frames with proper responsive breakpoints
4. Outputs design-token-aware spacing, typography scale, and grid alignment
5. Users can tweak the "forge rules" to match their design system

## Why Users Love It
- Saves 2-4 hours per page on responsive layout work
- Enforces consistency across breakpoints automatically
- Learns from the user's existing components and spacing patterns
- "It's like having a junior designer who actually reads the style guide"

## Tech Stack
- Figma Plugin API (TypeScript)
- Layout engine: custom constraint solver (~4,000 lines of TS)
- No backend — runs entirely in-browser within Figma
- License server: simple Node.js API on Railway ($7/month)

## Pricing
- Free tier: 5 forges/month
- Pro: $14/month (unlimited forges, custom rules, priority support)
- Team: $10/seat/month (shared rules, team templates) — just launched, 12 teams so far

## Competitive Landscape
- Competitor A (ForgeUI): VC-backed ($2M seed), launched 6 weeks ago, free beta
- Competitor B (ResponsiveAI): VC-backed ($800K pre-seed), launched 3 weeks ago, $9/month
- Both are feature-light compared to LayoutForge but have marketing budgets
- Neither has the constraint solver sophistication or design-system learning

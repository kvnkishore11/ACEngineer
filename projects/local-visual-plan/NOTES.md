# Teaching Notes — visual-plan customization

## Learner profile
- Advanced. Has authored SKILL.md files and wired MCP servers. Pitch deep, skip basics.
- Prefers terse "caveman" chat; wants full technical accuracy kept.
- Wants lessons delivered as beautiful, self-contained HTML artifacts.

## Preferences
- Default artifact skill (per global CLAUDE.md): thariq-design. Lessons here use a self-contained editorial style.
- Wants ALL customization paths covered together, not drip-fed — delivered in one artifact.

## Working facts (verified from source, 2026-06-16)
- Skill dir: `~/.claude/skills/visual-plan/` — `SKILL.md` (460 lines), `references/{wireframe,canvas,document-quality,exemplar}.md`, `agent-native-skill.json`.
- `agent-native-skill.json`: `mcpUrl = https://plan.agent-native.com/_agent-native/mcp`, `contentHash = 17ed15010f99c2cc`, `updateCommand = npx @agent-native/core@latest skills update visual-plan`.
- References carry `<!-- SHARED-CORE:... START -->` markers → synced word-for-word with `/visual-recap`. Hand-edits to shared cores are upstream-owned.
- Remote MCP tools: get-plan-blocks, create-visual-plan / create-ui-plan / create-prototype-plan / create-plan-design / create-visual-questions, update-visual-plan, get-plan-feedback, export-visual-plan, read/patch/import-visual-plan-source, set-resource-visibility, share-resource.
- Local-files mode: `AGENT_NATIVE_PLANS_MODE=local-files`, writes `plans/<slug>/{plan,canvas,prototype}.mdx` + `.plan-state.json`, preview via `npx @agent-native/core@latest plan local preview --dir plans/<slug> --kind plan`.

## Next candidate lessons
- 0002: hands-on — fork visual-plan into `my-plan` and swap the renderer to thariq-design.
- 0003: write a settings.json hook that re-applies your SKILL.md patch after `skills update`.

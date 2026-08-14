# visual-plan Customization Resources

## Knowledge

- [Skill source: `~/.claude/skills/visual-plan/SKILL.md`](file:///Users/kvnkishore/.claude/skills/visual-plan/SKILL.md)
  The 460-line policy/brain of the skill. Primary source for gating, workflow, surface choice, tool guidance. Use for: anything about HOW the skill decides and orchestrates.
- [Reference cores: `~/.claude/skills/visual-plan/references/`](file:///Users/kvnkishore/.claude/skills/visual-plan/references/)
  `wireframe.md`, `canvas.md`, `document-quality.md`, `exemplar.md` — on-demand quality bars, SHARED-CORE with /visual-recap. Use for: the rendering/quality rules.
- [`agent-native-skill.json`](file:///Users/kvnkishore/.claude/skills/visual-plan/agent-native-skill.json)
  The manifest tying the skill to its remote MCP + update command. Use for: understanding the sync/overwrite model.
- `write-a-skill` skill (`~/.claude/skills/write-a-skill/SKILL.md`)
  Anthropic's own guide to authoring skills with progressive disclosure. Use for: the build-my-own-variant path.
- `update-config` skill — settings.json hooks. Use for: auto-reapplying local edits after `skills update`.
- Agent-Native CLI: `npx @agent-native/core@latest --help`
  Install/update/connect/local-preview commands. Use for: self-host + local-files mode.

## Wisdom (Communities)

- Gaps — no community sourced yet. Candidates to vet: agent-native Discord/GitHub, Claude Code community forums. Surface when the user wants to validate a fork against others' practice.

## Gaps
- No public docs URL captured yet for the agent-native block registry schema (`get-plan-blocks` output). To fully own the renderer you'd reverse it at runtime or self-host. Find canonical schema docs before the build-my-own deep dive.

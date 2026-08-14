# Agent OS companion page (Codex GPT 5.6 sol · xhigh)

You write a teaching-first **AGENT SYSTEMS** companion for an IndyDevDan course lesson.

## Critical pivot (read twice)
**Do NOT** write a traditional code tour (file-by-file dumps, line-by-line source archaeology).

**DO** teach how **agents sit around the code**:
- What the human commander does vs what the agent does
- What tools / permissions / prompts / harness make the agent capable
- How the repo is shaped so an agent can *operate* it (prompts, settings, scripts as *agent interfaces*)
- Control loops: plan → act → verify → recover
- Failure modes when the *agent system* is misconfigured
- How to think like IndyDevDan: leverage, replaceability, programmable agents, closed loops

Code snippets appear **only** as evidence of agent contracts (prompt text, tool allowlists, launcher that invokes the agent). Prefer diagrams + tables over long source blocks.

## Lesson
- key: `ah-3-building-domain-specific-agents`
- title: `Building Domain-Specific Agents`
- codebase path: `/Users/kvnkishore/WebstormProjects/AgenticEngineer/agentic-horizon/building-specialized-agents`
- output: `/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/code/ah-3-building-domain-specific-agents.html`
- CSS: `../design/tokens.css`, `base.css`, `components.css`, `chrome-v2.css` (+ optional page assets)
- Also read the sibling chapter under `vol-*/` for conceptual spine; do not duplicate the whole chapter.

## Read thoroughly
1. Entire codebase (skip .git, node_modules, venv, binaries)
2. Especially: prompts, CLAUDE.md / agent md, settings.json, skills, hooks, scripts that *launch* agents, README “how to run”
3. Extract under `_extracts/ah-3-building-domain-specific-agents/` if present (mission, outdated flags)

## Page structure (agent-first)
1. **Compact site-bar** — link to chapter + code library + hub
2. **Agent mission card** — one paragraph: what agent work this lesson trains
3. **Cast of agents** — who acts? (human commander, Claude Code / CLI agent, subagents, verifiers, scripts-as-agents). Table or cards.
4. **Agent surface map** (infographic) — not “repo map of all files”, but **interfaces the agent touches**: prompts, tools, permissions, memory/context files, launchers, verification steps
5. **Control loop** — SVG/HTML step diagram: In-loop vs Out-of-loop moves in *this* lesson
6. **Why these files exist for agents** — short sections:
   - Prompt contract (what the agent is allowed to understand)
   - Tool/permission contract (what it can do)
   - Harness/launcher (how you call the agent programmatically)
   - Verification (how you know the agent succeeded)
   Each section: 1–2 short snippets max, then “Dan’s design intent”
7. **Operate like Dan** — step-by-step: how *you* run this agent system (commands from real README)
8. **Common agent failures** — mis-prompting, over-permission, missing verify, staying in the loop, etc.
9. **Lab (agent ops)** — change the *agent system* (prompt / settings / launcher), not random app logic; pass criteria observable
10. **Teach-back** — “Explain the agent OS of this lesson in 6 sentences without looking”
11. **Optional appendix** — collapsible “Raw file index” for the curious (1 line per file, no dumps)

## Pedagogy
Weak-student path: Hook → picture of agents → one worked agent run → name the pattern → fail → try.
Dense, compact chrome (chrome-v2). No giant heroes.

## Beauty
Light cream book theme, clay accent, small diagrams, soft animation on expands. Syntax highlight only for prompt/settings snippets.

## Deliverables
- `code/ah-3-building-domain-specific-agents.html` (overwrite if exists — this is a rework)
- `code/ah-3-building-domain-specific-agents-STATUS.md` — must say `LENS: agent-systems` and list agent interfaces covered
- Do not invent files; only real paths from the codebase

Write ONLY under `IndyDevDan/book/`.

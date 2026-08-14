# Mission: Customize the `/visual-plan` skill

## Why
I want to bend `/visual-plan` to my own planning workflow — change how it gates,
defaults, and renders — and where the hosted engine won't bend, build my own
local variant that produces visual plans the way I want without depending on
`plan.agent-native.com`. End goal: a planning skill I own and trust.

## Success looks like
- I can explain the two-layer architecture (local prompt + remote MCP) without looking it up.
- I can edit `SKILL.md` / `references/*.md` to change gating, defaults, or quality bars — and survive `skills update`.
- I can scaffold a NEW local skill that emits visual plans as self-contained HTML, no MCP dependency.
- I can run visual-plan in local-files / self-hosted mode for private, repo-owned plans.

## Constraints
- Already built skills before — go deep, skip foundations.
- Want the explanation delivered as one beautiful self-contained HTML artifact.
- Caveman comms preference for chat; full technical accuracy retained.

## Out of scope (for now)
- Reverse-engineering the proprietary renderer / block registry internals on the server.
- Contributing upstream to agent-native.

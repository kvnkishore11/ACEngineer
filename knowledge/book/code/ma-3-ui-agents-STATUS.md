# STATUS: COMPLETE ✅

LENS: agent-systems

`ma-3-ui-agents` — **Infinite UI Agents** companion reworked as a teaching-first Agent OS field guide.

## Deliverables

- `code/ma-3-ui-agents.html` — compact companion centered on human/agent boundaries, harness interfaces, the closed generation loop, failure recovery, and an agent-ops lab.
- `code/ma-3-ui-agents.css` — page-specific composition using only shared semantic color/type tokens and loading before `chrome-v2.css`.
- `code/ma-3-ui-agents-STATUS.md` — this status and grounding record.

## Agent interfaces covered

- Human commander contract: problem class, scope, authority, budget, observable pass evidence, and escalation boundary.
- Claude Code meta-layer: `/install`, `/prime`, plan/build commands, Bowser, and the tmux `drive` harness.
- Pi boot and lifecycle: `.pi/settings.json`, prompt registration, high thinking, auto-compaction, and the 80% threshold.
- Programmatic launchers: `justfile`, the `teams` alias, reusable slash commands, list scripts, and Drive’s sentinel/JSON process interface.
- Orchestration topology: one Orchestrator, Setup/Brand/UI Generation/Validation team families, A/B/C round-robin scaling, and `delegate`/`tilldone`.
- Prompt contracts: all ten `.pi/prompts/multi-team/` operations, with `/generate` taught as the primary closed loop.
- Role contracts: model, expertise, skills, tools, and `domain` path permissions from agent front matter.
- Memory/context: shared context, conversation logs, twelve expertise YAML stubs, mental-model maintenance, parallel sibling updates, and compaction.
- Work surface: `brand.yaml`, `trees.yaml`, branch leaves, status lifecycle, activity sidecar behavior, gallery routes, and iframe previews.
- Verification: Zod brand/tree schemas, filesystem-manifest sync, product-read-only soft/hard validators, build/list evidence, and recovery routing; the lab hardens the Hard Validator role used by both `/generate` and `/validate`.
- Failure seams: missing bootloader, human-in-the-loop routing, leader permission leaks, prompt/runtime token drift, false-positive validation, cold-start memory expectations, stuck status, and over-permission.

## Accuracy decisions

- The committed clone is described as all-Sonnet, one real brand, one config, and twelve one-line mental-model stubs; mixed models, populated expertise, and extra brands are labeled live-demo state.
- Leader non-writing is taught as design intent, not uniformly enforced fact: committed Setup/UI leads retain write-capable tools and product `upsert: true`.
- The preview mechanism is stated as iframe → gallery route → `import.meta.glob` dynamic component; Teleport is identified only in `Sidebar.vue`.
- The on-screen TillDone list is attributed to the Orchestrator’s `tilldone` tool, not embedded in committed `generate.md`.
- Token compliance is not overclaimed: committed `agent-stream` leaves contain raw hex/redeclared palettes despite validated status. The lab hardens that agent-system seam without hand-editing product code.

## Page structure

1. Compact site bar
2. Agent mission card
3. Cast of agents
4. Agent surface infographic
5. In-loop / out-of-loop control loop and worked run
6. Prompt, permission, launcher, and verification contracts
7. README/justfile operating sequence
8. Common Agent OS failures
9. Agent-ops lab with observable pass criteria
10. Six-sentence teach-back
11. Collapsible selected real-file interface index

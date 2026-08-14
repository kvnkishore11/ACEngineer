# visual-plan is a prompt layer over a remote MCP engine, not a self-contained skill

Established (Lesson 01): the learner now sees that `/visual-plan` splits into a LOCAL
editable layer (`SKILL.md` + `references/*.md` + `agent-native-skill.json`) and a REMOTE
engine (`plan.agent-native.com` MCP: blocks, renderer, canvas, export) they cannot edit.
This corrects the likely starting misconception that the 460-line SKILL.md "is" the skill
and can be edited freely to change rendering.

Why it steers future sessions: every customization question now routes through one test —
"does this change live in the prompt or the engine?" Path 1 (tweak prompt), Path 2 (fork +
own renderer), Path 3 (local-files, keep engine). The `contentHash` + `skills update`
overwrite risk is the recurring gotcha to design around.

Learner is advanced (has authored skills + wired MCP), wants depth, and consumes lessons as
HTML artifacts. Next: hands-on fork into `my-plan` (Path 2) and a settings.json survival hook
for Path 1. See [[MISSION.md]].

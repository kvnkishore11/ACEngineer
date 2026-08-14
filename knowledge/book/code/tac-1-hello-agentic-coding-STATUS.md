# TAC-1 Hello Agentic Coding companion

STATUS: COMPLETE

LENS: agent-systems

## Agent interfaces covered

- Human commander boundary: mission, starting state, authority audit, review, and recovery
- Interactive intent interface: `README.md` AI Coding Prompt and Agentic Coding Prompt
- Headless prompt contract: `programmable/prompt.md` with RUN / CREATE / RUN / REPORT
- Tool and permission contract: `.claude/settings.json`
- Callable-agent harness: `programmable/programmable.sh`
- Callable-agent harness: `programmable/programmable.py`
- Callable-agent harness: `programmable/programmable.ts`
- Credential seam: `.env.sample`
- Working context: prompt text plus current repository state; no lesson-local `CLAUDE.md`
- Verification interface: exact REPORT output, independent UV execution, branch state, Git commit, and process status
- Recovery interface: revise prompt, permission surface, launcher behavior, or starting state and rerun
- Explicit absences: no lesson-local skills, hooks, subagents, or separate verifier agent

## Page structure covered

- Compact site bar with chapter, code library, and book hub links
- Agent mission card
- Cast of agents and non-agent supporting roles
- Agent surface map infographic
- In-loop versus out-of-loop control loop
- Prompt, permission, harness, and verification contracts
- Real README launcher commands
- Agent-system failure modes and recovery moves
- Agent-ops lab with observable pass criteria
- Six-sentence teach-back
- Collapsible seven-file raw index

## Source fidelity

- All seven committed files under `tac/tac-1` were read.
- The TAC-1 extract set and sibling conceptual chapter were read for mission, pedagogy, and outdated-practice flags.
- Generated runtime artifacts are labeled as outputs, not committed source interfaces.
- No lesson-local agent files, hooks, skills, subagents, or verifier were invented.

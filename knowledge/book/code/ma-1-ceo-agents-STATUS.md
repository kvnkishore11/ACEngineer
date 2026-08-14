# CEO Agents companion — status

STATUS: REWORKED

LENS: agent-systems

## Deliverable

- code/ma-1-ceo-agents.html

## Agent interfaces covered

- Human commander boundary: decision framing, evidence quality, stakes, authority, time/budget envelope, roster, interruption, and final acceptance
- Primary Pi agent as CEO: runtime system-prompt injection, decision framing, board orchestration, constraint awareness, synthesis, and memo ownership
- Eight Pi board subprocesses: Revenue, Product Strategist, Technical Architect, Contrarian, Compounder, Customer Oracle, Market Strategist, and Moonshot
- Claude Code meta-pi-agent as a separate harness-maintainer agent rather than a deliberation seat
- Scripts-as-agent interfaces: just ceo, metacc, metapi, the tmux-backed drive CLI, SVG generation, and ElevenLabs TTS
- Prompt contracts: model, expertise, skills, objective function, time horizon, bias, risk tolerance, evidence standard, tension partners, workflow, runtime variables, and report shape
- Tool and permission contracts: Pi core read / bash / edit / write, custom converse and end_deliberation, board subprocess resource-disabling flags, API-key surfaces, and the high-risk metacc permission bypass
- Context and memory contracts: validated brief, sibling Markdown context, persistent per-seat sessions, shared conversation.jsonl, and updatable per-role expertise scratch pads
- Settings and policy contracts: theme, provider, model, thinking level, compaction, roster, active prompt paths, editor, required brief headings, and meeting constraints
- Harness and launcher contracts: project-root discovery, explicit extension loading, session creation, input lockdown, target resolution, concurrent fan-out, tool-boundary constraint checks, state tracking, memo path creation, and editor open
- Verification contracts: brief validation, roster/status surfaces, time/budget gauges, returned constraint state, conversation.jsonl, tool-use.jsonl, independently verified memo front matter, SVG assets, and optional MP3 output
- Recovery loop: validation block, missing-path/provider failures, per-seat error isolation, stop, wrap, max-limit closure, config/prompt repair, rerun, and human rejection
- Out-of-loop operating model: human supplies the decision contract; the CEO runs the meeting; a verifier or commander closes plan → act → verify → recover only after durable evidence exists
- Agent replaceability lab: remove one complete roster entry, prove the seven-seat runtime in log and memo, observe input lockdown, then restore the canonical OS

## Source audit

- Audited the complete agentic-horizon-extras/ceo-agents tree, excluding .git, dependency/virtual-environment directories, and binary screenshots.
- Indexed 258 real text, code, configuration, lock, Markdown, JSON, YAML, MDC, and SVG files in the collapsible appendix.
- Read the runtime-critical surfaces in full: root and app READMEs, both CLAUDE files, justfile, .env.sample, app settings, Cursor Bun rule, tool manifest, both board configuration YAMLs, all nine canonical prompts, the multimodel prompt diffs, all Claude commands and skill contracts, the Pi extension and five runtime modules, brief template/examples, expertise/memo artifacts, and implementation specs.
- Read the lesson extracts under _extracts/ma-1-ceo-agents/, including mission, lab, nuggets, frame plan, status, and outdated/current flags.
- Read sibling vol-3-ma/15-ceo-agents.html and its asset CSS for the conceptual spine; this companion does not reproduce the full chapter’s long-context, board-role, or graded-lab teaching.
- Used the existing code-library agent-systems pages as compact chrome and interaction-shell references; all lesson content and the lab are CEO-Agents-specific.

## Course-era and runtime caveats surfaced

- Exact model IDs are course-era configuration, not “latest model” claims.
- The demonstrated all-Claude roster and shipped multimodel roster are both real; the latter requires corresponding provider credentials and is not selected by a documented CLI flag.
- converse launches selected board members concurrently with Promise.allSettled, despite CEO prompt copy describing sequential calls.
- Same-round cross-pollination is therefore not ordered or guaranteed; cross-round sharing is reliable through persistent sessions and the shared conversation log.
- end_deliberation launches final statements concurrently in configuration order; Contrarian is not serialized last despite README, prompt, and tool-description claims.
- The early-close guard enforces minimum time but does not programmatically enforce configured minimum budget.
- Maximum checks occur at tool boundaries; an in-flight round can finish after a configured ceiling.
- end_deliberation records meeting_end and marks the phase complete before instructing the CEO to write memo.md; phase completion therefore does not verify that the memo exists.
- Board subprocess flags disable auto-loaded extensions, skills, prompt templates, and themes, but do not sandbox retained core bash, edit, or write tools.
- The brief validator checks case-insensitive heading presence, not factual sufficiency or section semantics.
- Arbitrary TUI input and common built-in commands are deliberately blocked; the live surface supports /ceo-begin, stop, and wrap.
- just metacc uses --dangerously-skip-permissions; the page treats this as explicit maintainer authority, not a default runtime requirement.
- TTS is optional and depends on ELEVENLABS_API_KEY, Python/uv, ElevenLabs availability, and macOS afplay.

## Page structure check

- Compact site bar links to Chapter 15, code library, and book hub
- One-paragraph agent mission card and leverage hook
- Cast-of-agents table with commander, CEO, board, harness, maintainer, automation, and verifier roles
- Agent surface map of prompts, tools, permissions, context/memory, launch, settings, and evidence
- In-loop versus out-of-loop plan → act → verify → recover diagram
- Worked agent run from validated brief through concurrent fan-out to memo and log receipts
- Four agent-contract sections with short evidence excerpts and Dan’s design intent
- Real root README operation sequence using cp .env.sample .env, Bun, just ceo, and /ceo-begin
- Agent-system failure taxonomy, including mis-prompting, persona theater, over-permission, open loops, missing verification, and contract drift
- Deterministic agent-ops lab that changes roster configuration rather than application logic
- Six-sentence teach-back with a collapsible model answer
- Collapsible one-line index of 258 real non-binary source files

## Validation

- Structural check passed: 10 ordered sections match 10 rail links; all 14 IDs are unique; all fragment targets and 9 local stylesheet/page links resolve; relevant semantic tag counts balance.
- JavaScript parse check passed for the navigation/progress behavior and collapsible appendix population.
- Appendix audit passed against a fresh recursive filesystem walk: 258 indexed non-binary files, 258 actual non-binary files, no duplicates, omissions, or invented entries.
- Design-contract check passed: tokens, base, components, then chrome-v2 load in the required order; page CSS has no literal colors or type sizes; 900px and 650px breakpoints, reduced-motion handling, and print rules are present.
- Runtime claims were spot-checked against the extension, subprocess launcher, configuration parser, prompts, justfile, and root README.
- Parallel Standards and Spec reviews completed with no remaining findings after corrections to completion semantics, permission language, boundary-check language, heading matching, source paths, appendix coverage, chrome load order, typography tokens, and duplicated step styles.
- Managed browser automation could not initialize in this workspace, so visual browser QA is not claimed; responsive and interaction coverage was validated statically.

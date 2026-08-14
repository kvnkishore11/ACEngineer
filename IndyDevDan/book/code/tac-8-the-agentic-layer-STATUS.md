# TAC 8 — The Agentic Layer companion status

STATUS: COMPLETE

LENS: agent-systems

OUTPUT: `IndyDevDan/book/code/tac-8-the-agentic-layer.html`

PAGE ASSET: `IndyDevDan/book/code/tac-8-the-agentic-layer.assets.css`

## Agent interfaces covered

- Human commander boundary: intent, risk, credentials, authority, and acceptance
- CLI worker and specialist-role boundary: one agent, one prompt, one purpose
- Prompt contracts: priming, planning, building, testing, reviewing, patching, and parseable reports
- Context and memory surfaces: README, CLAUDE.md, specs, and conditional `ai_docs`
- Tool and permission contracts: allow/deny settings, hooks, safe environment filtering, MCP, and course-era permission bypasses
- Harnesses and launchers: one-shot gateways, slash-command gateways, composed ADWs, cron triggers, and product AEA server
- State and isolation: task markers, Notion status, ADW IDs, SQLite session IDs, sparse worktrees, and isolated ports
- Verification and recovery: JSONL receipts, validation commands, structured tests, spec-versus-diff review, screenshots, patch/re-review, and fail/stop/write-back behavior
- Persistent-agent exception: the AEA’s stored Claude session ID and resume path
- Current-use cautions from the supplied extracts: broad permission bypass, hard-coded machine paths, and period-specific orchestration choices

## Teaching structure

- Compact book navigation to chapter, code library, and hub
- Agent mission card
- Cast-of-agents responsibility table
- Agent operating-surface infographic
- In-loop versus out-of-loop control-loop diagram
- Four agent contracts with short prompt/settings evidence
- Worked App 1 operator run plus escalation ladder
- Agent-system failure and repair cards
- Prompt-contract lab with observable pass criteria
- Six-sentence teach-back retrieval check
- Collapsible agent-interface index

## Source audit notes

- Audited all five `tac/tac-8` app trees while excluding dependency directories, generated logs, and binaries from prose analysis.
- Read the sibling chapter at `IndyDevDan/book/vol-1-tac/08-the-agentic-layer.html` for the conceptual spine without reproducing the chapter.
- Read the supplied `_extracts/tac-8-the-agentic-layer/` mission, lab, status, nuggets, and outdated/current flags.
- Verified that every path shown in the companion exists in the tracked lesson source.
- Preserved an important snapshot caveat: App 3 documents an HTTP event pipeline, but its tracked `.claude/settings.json` wires local logging hooks rather than `send_event.py`.
- Preserved an authority caveat: several course launchers use broad permission bypasses; the page frames them as audited course evidence rather than a recommended default.

## Validation

- HTML structure and internal anchor checks: passed (22 unique IDs; 10 required sections present; no missing anchors)
- Local CSS/link/path checks: passed (20 hrefs checked: 9 file links and 11 in-page anchors; appendix interface paths verified against the lesson tree)
- Design-token check: passed (page-specific CSS consumes the shared color and type tokens; `chrome-v2.css` loads last)
- Evidence-snippet check: passed (two highlighted snippets, limited to the prompt and settings contracts)
- Desktop/mobile render inspection: passed in Chrome at full desktop width and an emulated 430 × 932 viewport
- Responsive behavior: passed (rail hidden, contract/lab/diagram grids collapse, no visible horizontal overflow)
- Standards review: passed after fixing normal-text contrast, preserving loop text for assistive technology, and defining the table’s visually-hidden header utility
- Spec review: passed after making escalation commands app-rooted, correcting README/demo provenance, and adding a parser-only lab check

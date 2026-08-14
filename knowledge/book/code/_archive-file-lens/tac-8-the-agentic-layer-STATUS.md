# TAC-8 code companion — coverage status

- Lesson key: tac-8-the-agentic-layer
- Source root: /Users/kvnkishore/WebstormProjects/AgenticEngineer/tac/tac-8
- Output: IndyDevDan/book/code/tac-8-the-agentic-layer.html
- Audit date: 2026-07-13
- Files inspected: **410 / 410**
- Text files read: **402**
- Text lines covered: **89,030** newline-counted lines
- Binary files inspected by metadata/content structure: **8**

## Inventory reconciliation

| Application snapshot | Files | Text files | Text lines | Binary files | Coverage |
|---|---:|---:|---:|---:|---:|
| tac8_app1__agent_layer_primitives | 19 | 19 | 3,441 | 0 | 19 / 19 |
| tac8_app2__multi_agent_todone | 33 | 33 | 9,388 | 0 | 33 / 33 |
| tac8_app3__out_loop_multi_agent_task_board | 126 | 123 | 25,502 | 3 | 126 / 126 |
| tac8_app4__agentic_prototyping | 52 | 52 | 23,152 | 0 | 52 / 52 |
| tac8_app5__nlq_to_sql_aea | 180 | 175 | 27,547 | 5 | 180 / 180 |
| **Total** | **410** | **402** | **89,030** | **8** | **410 / 410** |

## Binary inspection

- App 3 images/AgentDataFlowV2.gif — GIF metadata: 800 × 450.
- App 3 images/AgentDataFlowV2_compressed.mp4 — H.264/AAC metadata: 1920 × 1080, 30 fps, 15 seconds.
- App 3 images/app.png — PNG metadata: 1728 × 969.
- App 5 app/client/public/bg.png — PNG metadata: 1456 × 816.
- App 5 app/server/db/backup.db — SQLite schema and fixtures: users (6 columns, 20 rows) and products (6 columns, 32 rows).
- App 5 app_docs/assets/01-tables-with-export-buttons.png — JPEG metadata: 1920 × 1080.
- App 5 app_docs/assets/02-query-results-with-export-button.png — JPEG metadata: 1920 × 1080.
- App 5 app_docs/assets/03-empty-results-with-export-button.png — JPEG metadata: 1920 × 1080.

Two .png-suffixed app-doc assets are actually plain-text screenshot placeholders. They are included in the 402 text-file audit and identified as such in the HTML ledger.

## Page coverage

- Five-stage architecture and design rationale: covered.
- Control, worker, and evidence planes: covered.
- Jump-linked repository map and file tree: covered.
- App 1 prompt contracts, CLI/SDK runners, receipts, toy application, and historical specs: covered.
- App 2 task state machine, typed eligibility, worktrees, routing, concurrency, and workload: covered.
- App 3 hooks, local receipts, optional forwarding, Bun/SQLite/WebSocket service, Vue observer, themes, media, and real logs: covered.
- App 4 Notion eligibility, visible claim, prototype routing, detached workflows, AI references, and sample MCP config: covered.
- App 5 isolated state/worktrees/ports, GitHub triggers, SDLC/ZTE, tests/review/docs/ship, AEA session continuity, and NLQ product: covered.
- Exhaustive static role ledger: all 410 real paths included.
- End-to-end run, common failures, modification lab, and teach-back: covered.
- Back-link to existing chapter: ../vol-1-tac/08-the-agentic-layer.html.

## Audit notes

- Excluded only .git, node_modules, venv/.venv, and __pycache__ per the lesson rules.
- Large media bytes were not treated as text; dimensions, formats, duration/codecs where applicable, and inspectable SQLite contents were audited.
- Locks, datasets, the notebook, JSON receipts, bundled AI references, scripts, styles, and configuration were included in the text line count.
- Duplicate snapshots were reconciled as separate real files. Identical hashes explain reuse but do not remove them from coverage.
- Historical specs are taught as intent artifacts, not proof that proposed files exist. The HTML names only real checkout paths.

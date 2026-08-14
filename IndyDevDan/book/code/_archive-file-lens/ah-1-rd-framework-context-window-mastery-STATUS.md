# AH-1 code companion — coverage status

- Lesson key: `ah-1-rd-framework-context-window-mastery`
- Lesson title: **Elite Context Engineering**
- Source root: `/Users/kvnkishore/WebstormProjects/AgenticEngineer/agentic-horizon/elite-context-engineering`
- Output: `IndyDevDan/book/code/ah-1-rd-framework-context-window-mastery.html`
- Audit date: 2026-07-13
- Files inspected: **53 / 53**
- Text files read: **53 / 53**
- Newline-counted source lines covered: **6,745**
- Binary files skipped: **0**

## Inventory reconciliation

| Area | Files | Lines covered | Coverage |
|---|---:|---:|---:|
| Root files | 11 | 3,639 | 11 / 11 |
| `.claude/` | 28 | 2,490 | 28 / 28 |
| `apps/` | 12 | 581 | 12 / 12 |
| `ai_docs/` | 1 | 14 | 1 / 1 |
| `scripts/` | 1 | 21 | 1 / 1 |
| **Total** | **53** | **6,745** | **53 / 53** |

## Page coverage

- Hook: measured contrast between `CLAUDE.md` and the deliberate `CLAUDE.large.md` bloat specimen.
- Repository map: Reduce, prime-on-demand, Delegate, observe/automate lanes.
- Jump-linked file tree: covered.
- Architecture and design rationale: covered.
- Always-on context (`CLAUDE*`, MCP samples): annotated.
- Purpose-specific priming (`prime.md`, `prime_cc.md`): annotated.
- Event wiring and context evidence (`settings.json`, both Python hooks): annotated.
- Bundle replay/deduplication (`load_bundle.md`): annotated.
- Documentation sub-agents and meta-agent: annotated.
- Background primary-agent process and report handoff: annotated.
- Planner/builder and hook-expert plan/build/improve pipelines: annotated.
- Output styles and provider utilities: covered.
- Raw SDK probes and TypeScript wrapper (`types.ts`, `core.ts`, `cli.ts`): annotated.
- Every real file's role: covered in the exhaustive 53-file ledger.
- End-to-end interactive and SDK control flow: covered.
- Common failure modes: covered with source-backed examples.
- Lab: add one reusable prompt and verify via typecheck plus the no-token `--list` path.
- Teach-back retrieval checks: covered.
- Back-link to existing chapter: `../vol-2-ah/09-rd-framework-context-window-mastery.html`.

## Audit notes

- All 53 source files are text-sized and were read in full. No `.git`, `node_modules`, virtual environment, or binary content was included.
- `apps/cc_ts_wrapper/index.ts` contains one line without a trailing newline; `wc -l` therefore reports 0 for that file even though its contents were inspected.
- Runtime paths named by source code (context bundles, hook logs, reports, fetched docs, and specs) are described as generated artifacts and are not counted as checkout files.
- Paths mentioned by instruction files but absent from the checkout are explicitly labeled as absent; the companion does not present them as real files.
- The Bun-based source lab was statically checked against the CLI control flow. It could not be executed in this workspace because `bun` is not installed.
- The in-app browser and local headless render fallbacks were blocked by the managed sandbox. DOM structure, responsive CSS rules, collapsible markup, anchors, local links, and code-overflow/highlighting contracts were verified deterministically; no screenshot pass is claimed.
- The HTML loads `tokens.css`, `base.css`, and `components.css`, then page-local teaching/highlighting styles, with the required compact `chrome-v2.css` override loaded last.

# TAC-2 code deep-dive status — The 12 Leverage Points

Status: **complete**. Exhaustive source read and deterministic artifact verification passed. The sandbox did not expose a working browser renderer, so screenshot-based visual QA was not available.

## Output artifacts

- `code/tac-2-the-12-leverage-points.html` — teaching-first companion page
- `code/tac-2-the-12-leverage-points.assets.css` — page-specific styles, loaded before `chrome-v2.css`
- `code/tac-2-the-12-leverage-points-STATUS.md` — this coverage and verification record

## Coverage

- Codebase: `tac/tac-2`
- Eligible files read: **49 / 49**
- Logical lines read: **6,292 / 6,292**
- Newline-terminated line count (`wc -l`): 6,261
- Non-empty files without a trailing newline: 31 (counted as one additional logical line each)
- Zero-byte files: 5 (read and documented as placeholders)
- Skipped by rule: `.git`, `node_modules`, virtual environments, huge binaries (none of the 49 eligible files were skipped)

## Per-file line coverage

| Lines | File |
| ---: | --- |
| 7 | `.claude/commands/install.md` |
| 8 | `.claude/commands/prime.md` |
| 3 | `.claude/commands/tools.md` |
| 22 | `.claude/settings.json` |
| 45 | `.gitignore` |
| 154 | `README.md` |
| 0 | `adws/README.md` |
| 0 | `agents/README.md` |
| 181 | `ai_docs/anthropic_quick_start.md` |
| 312 | `ai_docs/openai_quick_start.md` |
| 24 | `app/client/.gitignore` |
| 91 | `app/client/index.html` |
| 1,023 | `app/client/package-lock.json` |
| 15 | `app/client/package.json` |
| 33 | `app/client/public/sample-data/orders_(32).csv` |
| 33 | `app/client/public/sample-data/products.csv` |
| 162 | `app/client/public/sample-data/users.json` |
| 1 | `app/client/public/vite.svg` |
| 79 | `app/client/src/api/client.ts` |
| 415 | `app/client/src/main.ts` |
| 484 | `app/client/src/style.css` |
| 80 | `app/client/src/types.d.ts` |
| 1 | `app/client/src/vite-env.d.ts` |
| 25 | `app/client/tsconfig.json` |
| 13 | `app/client/vite.config.ts` |
| 4 | `app/server/.env.sample` |
| 1 | `app/server/.python-version` |
| 1 | `app/server/core/__init__.py` |
| 82 | `app/server/core/data_models.py` |
| 111 | `app/server/core/file_processor.py` |
| 83 | `app/server/core/insights.py` |
| 157 | `app/server/core/llm_processor.py` |
| 100 | `app/server/core/sql_processor.py` |
| 20 | `app/server/pyproject.toml` |
| 234 | `app/server/server.py` |
| 0 | `app/server/tests/__init__.py` |
| 3 | `app/server/tests/assets/column_names.csv` |
| 4 | `app/server/tests/assets/invalid.csv` |
| 23 | `app/server/tests/assets/test_products.json` |
| 5 | `app/server/tests/assets/test_users.csv` |
| 0 | `app/server/tests/core/__init__.py` |
| 164 | `app/server/tests/core/test_file_processor.py` |
| 287 | `app/server/tests/core/test_llm_processor.py` |
| 173 | `app/server/tests/core/test_sql_processor.py` |
| 780 | `app/server/uv.lock` |
| 81 | `scripts/start.sh` |
| 19 | `scripts/stop_apps.sh` |
| 749 | `specs/init_nlq_to_sql_to_table.md` |
| 0 | `trees/README.md` |

## Page requirements covered

- Compact site bar and title
- Link back to `vol-1-tac/02-the-12-leverage-points.html`
- Repo architecture infographic
- Jump-linked file tree
- Collapsible important-file walkthroughs
- Syntax-highlighted, horizontally scrollable code blocks
- Upload and query end-to-end control/data flow
- Common failure and design-tradeoff section
- Complete 49-file job ledger
- Modify-one-thing lab with verification criteria
- Teach-back and retrieval questions
- Shared light-theme CSS: `../design/tokens.css`, `../design/base.css`, `../design/components.css`, `../design/chrome-v2.css`

## Artifact verification

- The page's 49-path ledger exactly matches the 49 eligible source paths.
- Every internal jump target resolves; every local stylesheet and chapter link exists.
- IDs are unique and critical opening/closing tag counts are balanced.
- The inline interaction script passes `node --check`.
- Page-specific styles live outside the HTML, and `chrome-v2.css` loads last.
- Highlight.js is pinned to 11.11.1; readable, scrollable code remains available if the CDN is unavailable.

## Accuracy notes

- The page distinguishes the 749-line plan from the flatter shipped client.
- The page does not claim runtime-created database files are checked in.
- Empty `adws/`, `agents/`, and `trees/` placeholders are described as empty, not implemented capabilities.
- The course-era provider quickstarts and model pins are described as repository evidence, not current API recommendations.
- The table-name punctuation failure is traced from the real sample file through the real filename normalization and unquoted SQLite metadata query.

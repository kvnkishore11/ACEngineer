# TAC-6 code companion — coverage status

- Lesson key: `tac-6-let-your-agents-focus`
- Source root: `/Users/kvnkishore/WebstormProjects/AgenticEngineer/tac/tac-6`
- Output: `IndyDevDan/book/code/tac-6-let-your-agents-focus.html`
- Audit date: 2026-07-13
- Files inspected: **136 / 136**
- Text files read: **134**
- Text lines covered: **18,776** newline-counted lines
- Binary files inspected: **2**
  - `app/client/public/bg.png` — PNG metadata inspected: 1456 × 816, RGB, non-interlaced.
  - `app/server/db/backup.db` — SQLite schema and fixture counts inspected: `users` (20 rows), `products` (32 rows).

## Inventory reconciliation

| Area | Files | Coverage |
|---|---:|---:|
| `.claude/` | 38 | 38 / 38 |
| `adws/` | 31 | 31 / 31 |
| `app/client/` | 17 | 17 / 17 |
| `app/server/` | 28 | 28 / 28 |
| Root files + `scripts/` + `specs/` | 22 | 22 / 22 |
| **Total** | **136** | **136 / 136** |

## Page coverage

- Architecture and rationale: covered.
- Repository map and jump-linked tree: covered.
- Every real file's role: covered in the exhaustive file ledger.
- Focus boundary (`adws/adw_modules/agent.py`): annotated.
- Durable state contract (`state.py`, `data_types.py`): annotated.
- Phase composition (`adw_sdlc.py`, wrapper scripts): annotated.
- Plan/build handoff: covered.
- Unit/E2E test repair loops: covered.
- Review/blocker repair loop and screenshots/R2: covered.
- Patch and documentation specialists: covered.
- Prompt contracts and conditional context: covered.
- Trigger/GitHub entry paths: covered.
- Product client/server request flow: covered.
- End-to-end run, common failures, lab, and teach-back: covered.
- Back-link to existing chapter: `../vol-1-tac/06-let-your-agents-focus.html`.

## Audit notes

- Skipped raw binary bytes under the user's huge-binary exception; metadata and inspectable database contents were still covered.
- Generated lockfiles were read and are explained as reproducibility artifacts rather than hand-authored logic.
- Historical specs were treated as plans, not as proof that proposed files exist. The HTML ledger names only real checkout paths.

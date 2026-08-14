# TAC-4 AFK Agents — code companion status

status=complete
lesson=tac-4-afk-agents
source=`tac/tac-4`
output=`code/tac-4-afk-agents.html`
chapter=`vol-1-tac/04-afk-agents.html`
updated=2026-07-13 05:44:02 CDT

## Coverage

- Files inventoried in the lesson codebase: **154**
- Eligible text files read and represented: **148 / 148**
- Logical lines covered: **23,453 / 23,453**
- Physical newline characters: **23,337**
- Non-empty files without a final newline: **116**
- Zero-byte text files: **2**
- Text bytes covered: **1,433,896**
- Excluded binaries: **6** compiled `.pyc` cache files
- Other exclusions: `.git`, `node_modules`, and virtual environments; none contributed eligible source text

“Logical lines” counts the final unterminated line in each non-empty file. That is why it is larger than the physical newline count.

| Area | Files | Logical lines |
|---|---:|---:|
| `.claude` | 22 | 1,249 |
| `adws` | 9 | 2,394 |
| `agents` | 26 | 4,156 |
| `ai_docs` | 5 | 2,116 |
| `app/client` | 15 | 2,479 |
| `app/server` | 23 | 3,060 |
| `logs` | 33 | 6,234 |
| repository root | 4 | 310 |
| `scripts` | 7 | 324 |
| `specs` | 4 | 1,131 |
| **Total** | **148** | **23,453** |

## Companion checklist

- [x] Compact site bar and title
- [x] Hook and mental model for a first-time learner
- [x] Repository architecture infographic
- [x] File tree with valid jump links
- [x] Collapsible walkthroughs for the important implementation files
- [x] Complete responsibility ledger naming all 148 eligible text files
- [x] Annotated, horizontally scrollable code snippets with CSS syntax highlighting
- [x] End-to-end issue-to-pull-request control flow
- [x] Common failure modes tied to the actual implementation
- [x] Safe local modification lab with a verification command
- [x] Teach-back prompts and retrieval questions
- [x] Backlink to the existing TAC chapter
- [x] Shared design stylesheets, with `chrome-v2.css` loaded last
- [x] Reduced-motion behavior and responsive navigation

## Accuracy notes

- The live `.env` file was inspected for configuration shape and key names. Secret values are deliberately absent from the companion.
- Generated logs contain historical artifacts that are not present in the current source tree. The page labels those as historical evidence instead of presenting them as real current files.
- Proposed paths mentioned inside planning documents are not presented as implemented files.
- The saved successful run `5f2e861e` is used as the concrete trace: issue `#9` to pull request `#10`, with eight isolated agent calls.

## Verification

- All **148** eligible source paths occur in the generated HTML; missing paths: **0**.
- HTML IDs are unique: **28 / 28**.
- Internal fragment links resolve: **27 / 27**.
- Referenced local files resolve: **8 / 8**.
- The inline JavaScript passes `node --check`.
- All requested writes are contained under `IndyDevDan/book/`.

The in-app browser could not establish a render session in this workspace, and the installed Chrome binary did not produce headless output. Deterministic DOM, stylesheet, script, link, and disclosure audits passed; screenshot-based visual QA was unavailable.

# Database Expert — Question

Answer a question about the sample_app data layer the way an expert does:
from the mental model first, proven against the code before anything ships.
This is the REUSE step of Act–Learn–Reuse.

## Variables

USER_QUESTION: $1
EXPERTISE_FILE: experts/database/expertise.yaml

## Instructions

- IMPORTANT: question-answering only — DO NOT write or edit any files.
- The expertise file is a lens, not a source of truth. The code is the source of truth.
- No expert relearns their craft on every task: reach for key_files directly, don't search.

## Workflow

1. Read EXPERTISE_FILE — load your mental model before touching anything else.
2. Draft an answer to USER_QUESTION from the mental model alone, noting which
   key_files and conventions it leans on.
3. <!-- YOUR TURN: the step that keeps experts honest. Before reporting,
   open the key_files your draft leaned on and prove each fact against the
   actual code — expertise is a lens; where the two disagree, the yaml loses. -->
   ____
4. Report the answer with a file:line citation for every claim.

## Report

- Direct answer first, no preamble.
- Every claim cites file:line evidence (e.g. sample_app/db.py:31).
- Flag any spot where the expertise file disagreed with the code.

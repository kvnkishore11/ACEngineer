#!/bin/bash
set -euo pipefail
export PATH="/Users/kvnkishore/.local/bin:/opt/homebrew/bin:/usr/bin:/bin"
export HOME="/Users/kvnkishore"
cd "/Users/kvnkishore/WebstormProjects/AgenticEngineer"
PROMPT="/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/_orchestration/TAC1-CLAUDE-CROSS-REVIEW.md"
OUT="/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/_logs/tac1-claude-cross-review.json"
ERR="/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/_logs/tac1-claude-cross-review.err"
: > "$OUT"; : > "$ERR"
claude -p "$(cat "$PROMPT")" \
  --model fable \
  --effort max \
  --permission-mode bypassPermissions \
  --dangerously-skip-permissions \
  --output-format json \
  > "$OUT" 2>"$ERR"
echo EXIT:$? | tee -a "$ERR"
ls -la IndyDevDan/book/vol-1-tac/ | tee -a "$ERR"
test -f IndyDevDan/book/vol-1-tac/01-CROSS-REVIEW-CLAUDE.md && echo REVIEW_OK | tee -a "$ERR"

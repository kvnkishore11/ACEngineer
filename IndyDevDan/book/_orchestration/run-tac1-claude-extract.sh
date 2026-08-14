#!/bin/bash
set -euo pipefail
export PATH="/Users/kvnkishore/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
export HOME="/Users/kvnkishore"
cd "/Users/kvnkishore/WebstormProjects/AgenticEngineer"
PROMPT_FILE="/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/_orchestration/TAC1-CLAUDE-EXTRACT-RESUME.md"
OUT="/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/_logs/tac1-claude-extract-resume.json"
ERR="/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/_logs/tac1-claude-extract-resume.err"
: > "$OUT"
: > "$ERR"
# file-based prompt avoids shell escaping
claude -p "$(cat "$PROMPT_FILE")" \
  --model fable \
  --effort max \
  --permission-mode bypassPermissions \
  --dangerously-skip-permissions \
  --output-format json \
  > "$OUT" 2>"$ERR"
echo "EXIT:$?" | tee -a "$ERR"
ls -la "/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/_extracts/tac-1-hello-agentic-coding/" | tee -a "$ERR"

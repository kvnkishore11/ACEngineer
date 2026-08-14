#!/bin/bash
set -euo pipefail
export PATH="/Users/kvnkishore/.nvm/versions/node/v20.19.5/bin:/Users/kvnkishore/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export HOME="/Users/kvnkishore"
cd "/Users/kvnkishore/WebstormProjects/AgenticEngineer"
PROMPT_FILE="/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/_orchestration/TAC1-CODEX-CHAPTER.md"
OUT="/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/_logs/tac1-codex-chapter.out"
ERR="/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/_logs/tac1-codex-chapter.err"
: > "$OUT"
: > "$ERR"
# Verify extract ready
test -f "IndyDevDan/book/_extracts/tac-1-hello-agentic-coding/STATUS.md" || { echo "BLOCKED: no STATUS" | tee -a "$ERR"; exit 2; }
codex exec \
  --model gpt-5.6-sol \
  -c model_reasoning_effort=\"xhigh\" \
  --full-auto \
  --skip-git-repo-check \
  "$(cat "$PROMPT_FILE")" \
  > "$OUT" 2>"$ERR"
echo "EXIT:$?" | tee -a "$ERR"
ls -la "IndyDevDan/book/vol-1-tac/" | tee -a "$ERR"
test -f "IndyDevDan/book/vol-1-tac/01-hello-agentic-coding.html" && echo CHAPTER_OK | tee -a "$ERR"

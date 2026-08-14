#!/bin/bash
set -euo pipefail
export PATH="/Users/kvnkishore/.nvm/versions/node/v20.19.5/bin:/Users/kvnkishore/.local/bin:/opt/homebrew/bin:/usr/bin:/bin"
export HOME="/Users/kvnkishore"
cd "/Users/kvnkishore/WebstormProjects/AgenticEngineer"
OUT="/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/_logs/tac1-stitch.out"
ERR="/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan/book/_logs/tac1-stitch.err"
: > "$OUT"; : > "$ERR"
PROMPT='STITCH ONLY (no chapter rewrite). Under IndyDevDan/book/:
1) Update data/curriculum.json so tac-1-hello-agentic-coding status reflects chaptered+reviewed, set chapter_html to vol-1-tac/01-hello-agentic-coding.html, extract_status done, review path vol-1-tac/01-CROSS-REVIEW-CLAUDE.md, page_estimate 45-52, word_estimate ~13100. Keep other lessons intact.
2) If index.html progress text is wrong, lightly fix to show TAC-1 gold pilot complete and reviewed.
3) Write vol-1-tac/01-STITCH.md with DONE + what changed.
Do not rewrite the chapter HTML body. Paths absolute under AgenticEngineer.'
codex exec --model gpt-5.6-sol -c model_reasoning_effort=\"xhigh\" --full-auto --skip-git-repo-check "$PROMPT" >"$OUT" 2>"$ERR"
echo EXIT:$? | tee -a "$ERR"
ls -la IndyDevDan/book/vol-1-tac/ IndyDevDan/book/data/ | tee -a "$ERR"

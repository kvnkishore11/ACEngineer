#!/usr/bin/env bash
# 01 · the-agentic-prompt — fire the agentic prompt programmatically.
# Claude Code is a programmable agentic coding tool: the same prompt that runs
# interactively runs headlessly from any script. This is the seed of every ADW.
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v claude >/dev/null 2>&1; then
  echo "claude CLI not found — install Claude Code to run this lesson live."
  echo "The offline check (just check 01) never needs it. Nothing else to do."
  exit 0
fi

# YOUR TURN: invoke Claude Code headlessly with prompt.md as the prompt.
# Shape:  claude -p "$(cat prompt.md)"
# Tip: add --output-format text for plain text (try stream-json --verbose later).
____

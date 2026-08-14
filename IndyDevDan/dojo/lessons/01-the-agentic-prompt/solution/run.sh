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

# One agent, one prompt, one purpose — fired headlessly.
claude -p "$(cat prompt.md)" --output-format text

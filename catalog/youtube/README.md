# `catalog/youtube/` — the video catalog

Public channel videos, in the same lesson-folder shape as the paid TAC/AH/MA
courses under `catalog/courses/`.

Channel: https://www.youtube.com/@IndyDevDan
Cutoff: a rolling ~13-month window; older videos age out of the inventory.

Counts drift, so produce them rather than reading them:

```sh
ls -d catalog/youtube/yt-*/ | wc -l          # videos
find catalog/youtube -name codebase -type l | wc -l   # with an attached codebase
```

## Layout (every video)

```
catalog/youtube/yt-NN-<slug>/
  video/<key>.mp4          # optional; else video/SOURCE.md with a yt-dlp recipe
  transcript/*.{md,txt,vtt}
  metadata/lesson.json     # includes codebase + codebase_url when present
  metadata/lesson.html
  metadata/course-page.html
  metadata/video-info.json
  metadata/repos.json      # primary + related GitHub links from the description
  codebase/                # symlink into codebases/yt/<owner>__<repo> when linked
  README.md
  STATUS.json
```

Shared vendored clones live in `codebases/yt/`. Videos with no public repo in
their description get a `CODEBASE.md` note instead of a symlink — that is
expected, not a gap.

Learning path: `transcript/*.md` + `codebase/` + `metadata/lesson.html`.

## Rebuild

```bash
uv run tools/youtube/weekly_update.py       # discover new uploads, build folders
uv run tools/youtube/attach_codebases.py    # symlink codebases from descriptions
uv run tools/youtube/fill_missing_codebases.py  # link videos that map to course codebases
uv run tools/youtube/rebuild_index.py       # rewrite INDEX.json + the table below

# or simply:
make youtube
```

> Run `attach_codebases.py` before `fill_missing_codebases.py`. The first prunes
> links for videos whose description names no repo, which includes the ones the
> second attaches to course-local codebases.

## Index

`INDEX.json` is the machine-readable catalog. The table below is generated into
this README by `rebuild_index.py`.

## Catalog table

| # | Key | Title | Date | TX | Meta | Code | Video |
|--:|-----|-------|------|:--:|:----:|:----:|:-----:|
| 1 | `yt-01-i-can-see-everything-claude-code-hooks-for-multi-agent-obser` | I Can SEE EVERYTHING: Claude Code Hooks for Multi Agent Obse | 20250714 | ✓ | ✓ | ✓ | src |
| 2 | `yt-02-how-claude-code-changed-engineering-forever-and-whats-next` | How Claude Code CHANGED Engineering Forever (and what's next | 20250721 | ✓ | ✓ | — | src |
| 3 | `yt-03-my-claude-code-sub-agents-build-themselves` | My Claude Code Sub Agents BUILD THEMSELVES | 20250728 | ✓ | ✓ | ✓ | src |
| 4 | `yt-04-im-addicted-to-claude-code-rate-limits-agent-models-and-cc-a` | I'm ADDICTED to Claude Code: RATE LIMITS, Agent Models, and  | 20250804 | ✓ | ✓ | ✓ | src |
| 5 | `yt-05-gpt-5-agentic-coding-with-claude-code` | GPT-5 Agentic Coding with Claude Code | 20250811 | ✓ | ✓ | ✓ | src |
| 6 | `yt-06-engineers-claude-code-output-styles-are-here-dont-miss-this` | Engineers… Claude Code Output Styles Are Here. Don’t Miss Th | 20250818 | ✓ | ✓ | ✓ | src |
| 7 | `yt-07-5-agent-patterns-to-simplify-your-agentic-coding-claude-code` | 5 Agent PATTERNS to SIMPLIFY Your Agentic Coding (Claude Cod | 20250825 | ✓ | ✓ | — | src |
| 8 | `yt-08-agentic-workflows-beyond-the-chat-ui-with-claude-code-sdk-an` | Agentic Workflows: BEYOND the Chat UI with Claude Code SDK a | 20250901 | ✓ | ✓ | ✓ | src |
| 9 | `yt-09-elite-context-engineering-with-claude-code` | Elite Context Engineering with Claude Code | 20250908 | ✓ | ✓ | ✓ | src |
| 10 | `yt-10-agentic-prompt-engineering-with-claude-code-for-you-your-tea` | Agentic Prompt Engineering with Claude Code (For you, your t | 20250915 | ✓ | ✓ | ✓ | src |
| 11 | `yt-11-agentic-coding-endgame-build-your-claude-code-sdk-custom-age` | Agentic Coding ENDGAME: Build your Claude Code SDK Custom Ag | 20250922 | ✓ | ✓ | ✓ | src |
| 12 | `yt-12-my-top-5-agentic-engineering-bets-anthropic-custom-agents-mu` | My TOP 5 Agentic Engineering Bets: Anthropic, Custom Agents, | 20250929 | ✓ | ✓ | — | src |
| 13 | `yt-13-claude-code-2-0-agentic-coding-no-other-agents-arent-even-cl` | Claude Code 2.0 Agentic Coding: No, other agents aren't even | 20251006 | ✓ | ✓ | ✓ | src |
| 14 | `yt-14-big-3-super-agent-gemini-2-5-computer-use-openai-realtime-ap` | BIG 3 SUPER AGENT: Gemini 2.5 Computer Use, OpenAI Realtime  | 20251013 | ✓ | ✓ | ✓ | src |
| 15 | `yt-15-claude-haiku-4-5-is-light-speed-agentic-coding-but-can-it-be` | Claude HAIKU 4.5 is LIGHT SPEED Agentic Coding… BUT can it B | 20251020 | ✓ | ✓ | ✓ | src |
| 16 | `yt-16-i-finally-cracked-claude-agent-skills-breakdown-for-engineer` | I finally CRACKED Claude Agent Skills (Breakdown For Enginee | 20251027 | ✓ | ✓ | ✓ | src |
| 17 | `yt-17-the-one-agent-to-rule-them-all-advanced-agentic-coding` | The One Agent to RULE them ALL - Advanced Agentic Coding | 20251103 | ✓ | ✓ | ✓ | src |
| 18 | `yt-18-why-are-top-engineers-ditching-mcp-servers-3-proven-solution` | Why are top engineers DITCHING MCP Servers? (3 PROVEN Soluti | 20251110 | ✓ | ✓ | ✓ | src |
| 19 | `yt-19-e2b-agent-sandboxes-the-space-to-place-your-claude-agents` | E2B Agent Sandboxes: The Space to Place your Claude Agents | 20251117 | ✓ | ✓ | ✓ | src |
| 20 | `yt-20-i-gave-gemini-3-pro-its-own-computer-its-official-claude-cod` | I gave Gemini 3 Pro its own computer... it's official, Claud | 20251124 | ✓ | ✓ | ✓ | src |
| 21 | `yt-21-claude-opus-4-5-the-engineers-model` | Claude Opus 4.5: The Engineers' Model | 20251201 | ✓ | ✓ | ✓ | src |
| 22 | `yt-22-raw-agentic-coding-zero-to-agent-skill` | RAW Agentic Coding: ZERO to Agent SKILL | 20251208 | ✓ | ✓ | ✓ | src |
| 23 | `yt-23-agent-experts-finally-agents-that-actually-learn` | Agent Experts: Finally, Agents That ACTUALLY Learn | 20251215 | ✓ | ✓ | ✓ | src |
| 24 | `yt-24-top-2-engineering-plan-2026` | TOP 2% Engineering: /PLAN 2026 | 20251222 | ✓ | ✓ | — | src |
| 25 | `yt-25-the-codebase-singularity-my-agents-run-my-codebase-better-th` | The Codebase Singularity: “My agents run my codebase better  | 20251229 | ✓ | ✓ | ✓ | src |
| 26 | `yt-26-claude-code-is-amazing-until-it-deletes-production` | Claude Code is Amazing... Until It DELETES Production | 20260105 | ✓ | ✓ | ✓ | src |
| 27 | `yt-27-agent-threads-how-to-ship-like-boris-cherny-ralph-wiggum-in` | AGENT THREADS. How to SHIP like Boris Cherny. Ralph Wiggum i | 20260112 | ✓ | ✓ | ✓ | src |
| 28 | `yt-28-the-claude-code-feature-senior-engineers-keep-missing` | The Claude Code Feature Senior Engineers KEEP MISSING | 20260119 | ✓ | ✓ | ✓ | src |
| 29 | `yt-29-one-prompt-every-agentic-codebase-should-have-for-engineerin` | One Prompt Every AGENTIC Codebase Should Have (For Engineeri | 20260126 | ✓ | ✓ | ✓ | src |
| 30 | `yt-30-claude-code-task-system-anti-hype-agentic-coding-advanced` | Claude Code Task System: ANTI-HYPE Agentic Coding (Advanced) | 20260202 | ✓ | ✓ | ✓ | src |
| 31 | `yt-31-claude-code-multi-agent-orchestration-with-opus-4-6-tmux-and` | Claude Code Multi-Agent Orchestration with Opus 4.6, Tmux an | 20260209 | ✓ | ✓ | ✓ | src |
| 32 | `yt-32-my-4-layer-claude-code-playwright-cli-skill-agentic-browser` | My 4-Layer Claude Code Playwright CLI Skill  (Agentic Browse | 20260216 | ✓ | ✓ | ✓ | src |
| 33 | `yt-33-the-pi-coding-agent-the-only-real-claude-code-competitor` | The Pi Coding Agent: The ONLY REAL Claude Code COMPETITOR | 20260223 | ✓ | ✓ | ✓ | src |
| 34 | `yt-34-i-studied-stripes-ai-agents-vibe-coding-is-already-dead` | I Studied Stripe's AI Agents... Vibe Coding Is Already Dead | 20260302 | ✓ | ✓ | — | src |
| 35 | `yt-35-mac-mini-agents-openclaw-is-a-nightmare-use-these-skills-ins` | Mac Mini Agents: OpenClaw is a NIGHTMARE... Use these SKILLS | 20260309 | ✓ | ✓ | ✓ | src |
| 36 | `yt-36-the-library-meta-skill-how-i-distribute-private-skills-agent` | The Library Meta-Skill: How I Distribute PRIVATE Skills, Age | 20260316 | ✓ | ✓ | ✓ | src |
| 37 | `yt-37-pi-ceo-agents-claude-1m-context-multi-agent-teams` | Pi CEO Agents. Claude 1M Context. Multi-Agent Teams. | 20260323 | ✓ | ✓ | ✓ | src |
| 38 | `yt-38-one-agent-is-not-enough-agentic-coding-beyond-claude-code` | One Agent Is NOT ENOUGH: Agentic Coding BEYOND Claude Code | 20260330 | ✓ | ✓ | ✓ | src |
| 39 | `yt-39-my-pi-agent-teams-claude-code-leak-signal-harness-engineerin` | My Pi Agent Teams. Claude Code Leak SIGNAL. Harness Engineer | 20260406 | ✓ | ✓ | ✓ | src |
| 40 | `yt-40-the-first-unshipped-model-claude-mythos-senior-engineer-brea` | The First UNSHIPPED Model: Claude MYTHOS (Senior Engineer Br | 20260413 | ✓ | ✓ | — | src |
| 41 | `yt-41-my-m5-max-gemma-4-mlx-local-stack-this-kills-model-providers` | My M5 Max, Gemma 4, MLX LOCAL Stack. (This KILLS MODEL PROVI | 20260420 | ✓ | ✓ | ✓ | src |
| 42 | `yt-42-maximize-your-claude-code-subscription-without-getting-banne` | MAXIMIZE Your Claude Code Subscription (Without Getting BANN | 20260427 | ✓ | ✓ | ✓ | src |
| 43 | `yt-43-gpt-5-5-verified-opus-4-7-a-pi-coding-agent-that-reviews-lik` | GPT-5.5 VERIFIED Opus 4.7: A Pi Coding Agent That REVIEWS Li | 20260504 | ✓ | ✓ | ✓ | src |
| 44 | `yt-44-engineers-delete-the-bash-tool-agentic-security-for-pi-agent` | Engineers, DELETE the BASH Tool: Agentic Security For Pi Age | 20260511 | ✓ | ✓ | ✓ | src |
| 45 | `yt-45-pi-to-pi-two-way-agent-orchestration-with-the-pi-coding-agen` | Pi to Pi: Two-Way Agent Orchestration with the Pi Coding Age | 20260518 | ✓ | ✓ | ✓ | src |
| 46 | `yt-46-top-1-opportunity-for-senior-engineers-agentic-engineering` | Top #1 Opportunity for Senior Engineers: Agentic Engineering | 20260525 | ✓ | ✓ | ✓ | src |
| 47 | `yt-47-pi-coding-agent-observability-html-specs-with-gemini-3-5-fla` | Pi Coding Agent Observability: HTML Specs with Gemini 3.5 Fl | 20260601 | ✓ | ✓ | ✓ | src |
| 48 | `yt-48-i-ranked-cloudflares-software-factory-and-wow-s-tier-tokenom` | I Ranked Cloudflare’s Software Factory and Wow… S TIER TOKEN | 20260608 | ✓ | ✓ | — | src |
| 49 | `yt-49-claude-fable-5-banned-the-first-model-agentic-engineers-dont` | Claude Fable 5 BANNED: The First Model Agentic Engineers DON | 20260615 | ✓ | ✓ | — | src |
| 50 | `yt-50-plans-for-fable-5-rebuilding-my-plan-skill-for-mythos-class` | PLANS For Fable 5: Rebuilding My /Plan Skill for Mythos Clas | 20260622 | ✓ | ✓ | ✓ | src |
| 51 | `yt-51-glm-5-2-vs-minimax-m3-opus-has-real-competition-model-stacki` | GLM-5.2 vs MiniMax-M3: Opus Has REAL COMPETITION (Model Stac | 20260629 | ✓ | ✓ | — | src |
| 52 | `yt-52-see-cmux-solve-multi-agent-orchestration-claude-code-and-pi` | SEE CMUX SOLVE Multi-Agent Orchestration (Claude Code and Pi | 20260706 | ✓ | ✓ | ✓ | src |
| 53 | `yt-53-forget-loop-engineering-agentic-engineering-is-about-this` | FORGET Loop Engineering. Agentic Engineering is about THIS | 20260713 | — | ✓ | — | src |
| 54 | `yt-54-engineers-stop-picking-gpt-5-6-sol-or-claude-fable-5-fuse-th` | Engineers... STOP Picking GPT-5.6 Sol OR Claude Fable 5… FUS | 20260720 | ✓ | ✓ | ✓ | src |
| 55 | `yt-55-is-anthropic-stealing-your-data-while-you-pay-for-it` | Is Anthropic STEALING Your Data? (While You PAY FOR IT) | 20260727 | ✓ | ✓ | — | src |
| 56 | `yt-56-my-super-simple-software-factory-for-agentic-engineers` | My Super Simple Software Factory (For Agentic Engineers) | 20260803 | ✓ | ✓ | ✓ | src |
| 57 | `yt-57-engineers-your-software-factory-needs-agent-sandboxes-to-sca` | Engineers… Your Software Factory NEEDS Agent Sandboxes to SC | 20260810 | ✓ | ✓ | ✓ | src |

_Stats: transcript 56/57, metadata 57/57, codebase 46/57, mp4 0/57_

## Weekly auto-update (cron)

Hermes no-agent crons (host local **CDT** = Eastern−1h):

| Pass | Local cron | Eastern | Job ID | Script |
|------|------------|---------|--------|--------|
| Primary | Mon 16:00 `0 16 * * 1` | Mon **5pm** | `0a4aea80c465` | `~/.hermes/scripts/indydevdan_youtube_weekly_5pm.py` |
| Double-check | Mon 22:00 `0 22 * * 1` | Mon **11pm** | `87b8cfd4a1aa` | `~/.hermes/scripts/indydevdan_youtube_weekly_11pm.py` |

Core: `weekly_update.py` — dedupes by video id + existing folders; only builds **new** uploads; attach codebases + rebuild INDEX. Silent stdout when nothing new; delivers summary when new videos land. Heartbeat: `_weekly_last_run.json`.

Manual:
```bash
python3 weekly_update.py --pass primary --verbose
```


- Paid catalog: sibling folders `../tac-*`, `../ah-*`, `../ma-*`
- Expert book YT overlays: prefer **1–3 related** public videos per lesson (Phase 1), not every upload
- This tree is the **full 1-year public corpus** for broader learning / Phase 2

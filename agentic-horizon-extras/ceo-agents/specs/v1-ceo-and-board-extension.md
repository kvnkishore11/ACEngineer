# Plan: v1 CEO & Board Deliberation Engine

## Task Description

Build the v1 functional deliberation engine in `apps/ceo/extensions/ceo-and-board.ts`. This extension turns the Pi coding agent into a CEO that orchestrates board member conversations using custom tools, stateless LLM calls, and a `.jsonl` conversation log.

## Objective

A working deliberation system where the CEO agent (Pi on Opus) can prompt board members via `converse()`, see responses rendered in the TUI, log everything to `.jsonl`, and respect time/budget guardrails that force continuation or halt the meeting. The user can type `stop` to hard-stop or `wrap` to trigger early wrap-up.

## Problem Statement

The scaffolding extension exists but has no deliberation engine. We need the core loop: CEO prompts board members → members respond as Pi agent subprocesses → responses appear in TUI → conversation log grows → guardrails enforce min/max constraints → meeting concludes with final statements.

## Solution Approach

The CEO IS the Pi agent. We load the CEO's system prompt via `before_agent_start`, register `converse` and `end_deliberation` as custom tools via `pi.registerTool()`, and **spawn each board member as a Pi agent subprocess** on each tool invocation.

**Board members are persistent Pi agent sessions.** Each member gets a session file at `.pi/agent-sessions/<member-name>.json`. On the first `converse()` call, we spawn `pi --mode json -p --session <path> --system-prompt <file> <task>` (overwrites default system prompt). On subsequent calls, the same `--session <path>` automatically resumes — pi loads the existing session file. No `-c` flag needed. The member's full context window is preserved across rounds. No re-reading the conversation log. No raw Anthropic API calls.

**Subprocess pattern:**
```bash
# First call (session file doesn't exist yet — system prompt sets personality):
pi --mode json -p --no-extensions --no-skills --no-prompt-templates --no-themes \
   --session .pi/agent-sessions/revenue.jsonl \
   --system-prompt "$(cat agents/revenue.md body)" \
   --model anthropic/claude-sonnet-4-6 --thinking off \
   "CEO's first message"

# All subsequent calls (session file exists — auto-resumes with full context):
pi --mode json -p --no-extensions --no-skills --no-prompt-templates --no-themes \
   --session .pi/agent-sessions/revenue.jsonl \
   --thinking off \
   "CEO's next message"
```

- `--mode json -p`: JSON event streaming on stdout for real-time parsing
- `--session <path>`: Persistent session file per member. If file exists, pi auto-resumes — no `-c` flag needed.
- `--system-prompt <text>`: **Overwrites** the default system prompt (first call only — sets the member's personality). Passed as text, not a file path.
- `--no-extensions --no-skills --no-prompt-templates --no-themes`: Lightweight subagent, no discovery overhead
- `--thinking off`: No extended thinking for board member responses (cost control)

We parse `message_end` events from stdout to capture responses, usage stats (tokens, cost), and track each member's context window fill. The `.jsonl` conversation log remains the source of truth for the deliberation record.

---

## Release Roadmap

### v1 — Core Deliberation Loop (this plan)

The bare minimum to run a working meeting. CEO prompts, board responds, conversation is visible and logged, guardrails work.

| Feature | Details |
|---------|---------|
| **`converse(to, message)` tool** | CEO tool that spawns/resumes Pi agent subprocesses for board members sequentially. Each member has a persistent session file (`.pi/agent-sessions/<name>.json`). First call spawns with `--append-system-prompt`, subsequent calls resume with `-c` flag. Parses JSON events from stdout for responses + usage. Returns responses + constraint state. |
| **`.jsonl` conversation logging** | Every message (prompt, response, meeting_start, meeting_end) appended to `deliberations/<slug>.jsonl` with timestamps, type fields, and token/cost tracking. |
| **TUI conversation rendering** | Three-layer rendering: (1) `onUpdate` streams real-time partial text as each board member subprocess runs ("Revenue is responding..." → streamed text). (2) `renderCall`/`renderResult` on `converse` tool — styled CEO prompt header + final formatted response block with all members. (3) `pi.sendMessage` + `registerMessageRenderer` — each board member response injected as a standalone custom message in the conversation stream (customType: `"board-response"`), rendered with the member's unique background color, name, and response text. This makes each response a visible entry in the conversation flow, not buried inside a tool result. |
| **Time/budget guardrails** | Constraint state returned on every `converse()` call. If `hit_max` is true, the tool returns a hard-stop signal. If mins aren't reached, `end_deliberation` rejects and tells the CEO to keep going. |
| **`stop` and `wrap` user commands** | User types `stop` → hard abort, meeting ends immediately with `meeting_end` bookend. User types `wrap` → triggers `end_deliberation` flow (contrarian last, final statements). Input handled via `input` event interception. |
| **`/ceo-begin` command** | Prompts user to select a brief file (autocomplete from `briefs/`), validates required headers, writes `meeting_start` to .jsonl, injects CEO system prompt via `before_agent_start`, sends opening prompt to kick off the CEO. |
| **Board member Pi subprocess calls** | Each member spawned as `pi --mode json -p --session <file> <message>`. First call includes `--system-prompt` (overwrites) with member's `.md` body + `--model`. Subsequent calls just pass `--session` — pi auto-resumes. Member retains full context window. Parse JSON events from stdout for response text, usage stats, and context fill. |
| **`end_deliberation(message)` tool** | Prompts all active board members for final statements (contrarian last, enforced). Appends `final_statement` entries. Rejects if min constraints not reached. |
| **Meeting state tracking** | In-memory state: start time, budget spent (sum of response costs), active board members, meeting phase (idle/deliberating/ending/complete), paths to brief/deliberation/memo files. Tracks per-member session files and `hasSession` flag for resume. |
| **Board status widget** | Persistent TUI widget (`ctx.ui.setWidget`) showing all active board members in rows of 4. Each member in a colored box (color from config YAML). Shows: name, total chats (prompts + responses), total cost, remaining context window (in `XXXk` format). Minimal info, unique background colors per member. Updates after every `converse()` call. |
| **Agent color in config** | Each board member in the config YAML gets a `color` field (hex or named). Widget renders each member's box with their assigned background color for visual distinction. |
| **Memo generation** | After `end_deliberation` returns, CEO uses pi's built-in `write` tool to produce the memo. The extension intercepts the write via `tool_result` event and auto-injects YAML frontmatter (date, duration, budget_used, board_members, brief path, transcript path). Memo written to `memos/<YYYY-MM-DD>-<brief-slug>.md`. |
| **Open memo in editor** | After memo file is written, extension spawns the configured editor (`code`, `cursor`, etc. from config YAML) via `child_process.spawn` to open the memo file. |

### v2 — Polish & Reliability

| Feature | Details |
|---------|---------|
| **Brief validation UX** | Rich validation of brief headers with specific feedback on what's missing. Rejection with formatted error before meeting starts. |
| **Input locking during deliberation** | User prompts eaten during active deliberation — only `stop` and `wrap` are processed. All other input silently dropped with a notification. |
| **Meeting cost tracking** | Real token counting and cost calculation from Anthropic API response usage data. Accurate budget constraint enforcement. |
| **`meeting_start` / `meeting_end` bookends** | Full metadata entries in .jsonl with constraints, board members, brief path, and end-of-meeting summary stats. |

### v3 — Production Features

| Feature | Details |
|---------|---------|
| **Board member selection UI** | Interactive TUI for selecting which board members to activate for this meeting (from the config YAML roster). |
| **Budget confirmation flow** | On boot, show meeting constraints and ask user to lock in or adjust before starting. |
| **Conversation-prompt template as skill** | Load `conversation-prompt.md` as a Pi skill injected into board member calls. |
| **Model-per-member routing** | Each board member's frontmatter `model` field routes to different Anthropic models (Opus for CEO, Sonnet for members). |
| **Custom tool renderers** | `renderCall` and `renderResult` for `converse` and `end_deliberation` — show board member names, response previews, constraint gauges. |
| **Session persistence** | Meeting state survives Pi session restarts via `pi.appendEntry()`. Resume interrupted meetings. |
| **Parallel converse mode** | Optional parallel execution when CEO addresses multiple members — faster but members can't see each other's same-round responses. |
| **Context file injection** | Brief's `## Context Files` section loads referenced files into board member system prompts as additional expertise. |

---

## Relevant Files

### Existing Files

- `apps/ceo/extensions/ceo-and-board.ts` — **Primary target.** Existing scaffolding with config parsing, theme helpers, welcome widget, footer, and placeholder commands. All v1 work goes here.
- `specs/init.md` — Tool specs (`converse`, `end_deliberation`), subagent architecture, file formats (.jsonl, brief, memo, conversation-prompt), directory structure, configuration YAML.
- `specs/init-ceo-and-board.md` — 9 board member roles, decision protocol, meeting constraints, tension pairs, reasoning patterns.
- `.pi/ceo-agents/agents/*.md` — 9 board member system prompt files with frontmatter (name, model, expertise, skills, domain).
- `.pi/ceo-agents/ceo-and-board-configuration.yaml` — Meeting constraints and board member roster.

### Reference Files (Pi Agent Patterns)

- `ai_docs/pi-agent/extensions.md` — Extension API: `pi.registerTool()`, `pi.on()` events, `ctx.ui` methods, `ExtensionContext`.
- `ai_docs/pi-agent/examples-extensions/subagent/index.ts` — Subagent spawning pattern (we adapt this for stateless API calls instead of pi subprocess spawning).
- `ai_docs/pi-agent/examples-extensions/subagent/agents.ts` — Agent discovery: `parseFrontmatter`, `loadAgentsFromDir` patterns.
- `ai_docs/pi-agent/examples-extensions/send-user-message.ts` — `pi.sendUserMessage()` for kicking off the CEO after setup.
- `ai_docs/pi-agent/sdk.md` — `createAgentSession`, `AgentSession.prompt()`, `session.subscribe()` for programmatic SDK usage.
- `ai_docs/pi-agent/examples-sdk/12-full-control.ts` — Full SDK control: `createAgentSession` with custom tools, models, system prompts.

### New Files

- `.pi/ceo-agents/briefs/` — Directory already exists. User creates brief `.md` files here.
- `.pi/ceo-agents/deliberations/` — Directory already exists. `.jsonl` conversation logs written here by the extension.
- `.pi/ceo-agents/memos/` — Directory already exists. Memo files written here (v2).

---

## Implementation Phases

### Phase 1: Foundation — Meeting State & Board Member Loading

Build the in-memory meeting state, board member loading (parse `.md` frontmatter), and the core function that makes a stateless Anthropic API call to a single board member.

**Key pieces:**
- `MeetingState` interface: startTime, budgetSpent, activeMembers, phase, paths
- `loadBoardMember(path)`: read `.md`, parse frontmatter (name, model), extract system prompt body
- `callBoardMember(member, conversationLogPath, ceoMessage)`: assemble conversation-prompt template, call Anthropic API, return response + usage
- `appendToLog(logPath, entry)`: append a single `.jsonl` line

### Phase 2: Core Implementation — Tools & Commands

Register `converse` and `end_deliberation` as custom tools. Implement `/ceo-begin` as the meeting launcher. Wire up the `input` event to intercept `stop` and `wrap`.

**Key pieces:**
- `pi.registerTool("converse", ...)`: parameter schema (to, message), sequential board member calls, .jsonl logging, constraint state calculation and return
- `pi.registerTool("end_deliberation", ...)`: min-constraint guard, sequential final statement collection (contrarian last), .jsonl logging
- `/ceo-begin` command: brief file selection (autocomplete from `briefs/`), header validation, meeting_start .jsonl entry, CEO system prompt injection via `before_agent_start`, `pi.sendUserMessage()` to kick off CEO
- `input` event: intercept `stop` → hard abort, `wrap` → trigger end_deliberation flow

### Phase 3: Integration & Polish

Wire the CEO system prompt injection, ensure the conversation renders in TUI, test the full loop, handle edge cases (empty board, missing brief, API errors).

**Key pieces:**
- `before_agent_start` handler: if meeting is active, inject CEO system prompt from `agents/ceo.md` + brief content + tool instructions
- TUI rendering: `converse` tool's `renderCall` and `renderResult` to show board member names and response text
- Error handling: API call failures, missing config, invalid brief, abort signal propagation
- Meeting end: write `meeting_end` .jsonl entry with stats

---

## Architecture: How the CEO Agent Works

```
User runs /ceo-begin
  │
  ├─► Select brief file (autocomplete from briefs/)
  ├─► Validate brief headers
  ├─► Write meeting_start to .jsonl
  ├─► Set meeting phase = "deliberating"
  ├─► before_agent_start injects CEO system prompt + brief
  └─► pi.sendUserMessage("Read the brief and begin the deliberation.")
      │
      ▼
CEO (Pi agent on Opus) receives brief + tools
  │
  ├─► Calls converse("all", "Here's what we're deciding...")
  │   │
  │   ├─► For each board member (sequential):
  │   │   ├─► Append CEO prompt to .jsonl (type: "prompt")
  │   │   ├─► Spawn Pi subprocess:
  │   │   │   ├─► pi --mode json -p --session <file> [--system-prompt on first] <message>
  │   │   │   └─► Session file auto-resumes if it exists — no -c flag needed
  │   │   ├─► Parse JSON events from stdout (text_delta, message_end)
  │   │   ├─► Append member response to .jsonl (type: "response")
  │   │   └─► Track tokens/cost/context from message_end usage stats
  │   │
  │   └─► Return: all responses + constraint state
  │
  ├─► CEO reads constraint state, decides next move
  ├─► Calls converse() again for deeper digs...
  │   (repeats until constraints force conclusion)
  │
  ├─► Calls end_deliberation("Summarize your final position.")
  │   │
  │   ├─► Guard: reject if min_time or min_budget not reached
  │   ├─► Prompt all active members for final statement
  │   ├─► Contrarian goes LAST (enforced by tool)
  │   └─► Return all final statements
  │
  └─► CEO writes memo (v2) or meeting ends with meeting_end .jsonl entry
```

### User Intervention

```
During deliberation, the input event intercepts user typing:

"stop"  → Abort immediately. Write meeting_end with end_reason: "user_stop".
           ctx.abort() to halt the current agent turn.

"wrap"  → Force end_deliberation even if CEO hasn't called it.
           pi.sendUserMessage with steer delivery to interrupt.

anything else → Silently dropped (v2). For v1, just notify "meeting in progress".
```

---

## Team Orchestration

- You operate as the team lead and orchestrate the team to execute the plan.
- You're responsible for deploying the right team members with the right context to execute the plan.
- IMPORTANT: You NEVER operate directly on the codebase. You use `Task` and `Task*` tools to deploy team members to do the building, validating, testing, deploying, and other tasks.

### Team Members

- Builder
  - Name: ext-builder
  - Role: Implement the full ceo-and-board.ts extension — meeting state, board member loading, Anthropic API calls, custom tools (converse, end_deliberation), /ceo-begin command, input interception, .jsonl logging, TUI rendering
  - Agent Type: general-purpose
  - Resume: true

- Validator
  - Name: ext-validator
  - Role: Validate the extension compiles, tools are correctly typed, config parsing works, .jsonl output is well-formed, and the full meeting loop is coherent
  - Agent Type: general-purpose
  - Resume: true

---

## Step by Step Tasks

### 1. Build Meeting State & Board Member Infrastructure

- **Task ID**: meeting-state-infra
- **Depends On**: none
- **Assigned To**: ext-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- Add `MeetingState` interface to `ceo-and-board.ts`: `startTime: number`, `budgetSpent: number`, `activeMembers: BoardMemberConfig[]`, `phase: "idle" | "deliberating" | "ending" | "complete"`, `briefPath: string`, `logPath: string`, `memoPath: string`, `constraints: MeetingConstraints`
- Add `BoardMemberConfig` interface: `name: string`, `model: string`, `systemPrompt: string`, `filePath: string`, `color: string` (hex color from config), `sessionFile: string` (path to `.pi/agent-sessions/<name>.jsonl`)
- Add `MemberStats` interface: `chats: number`, `cost: number`, `tokensUsed: number`, `contextWindow: number`
- Add `memberStats: Map<string, MemberStats>` to meeting state for per-member tracking
- Update `BoardMember` interface to include `color: string` and update `parseConfig` to extract it from each board entry
- Add `parseHexColor(hex: string): { r: number, g: number, b: number }` helper for the widget
- Add `loadBoardMembers(agentsDir: string, board: BoardMember[])` function: read each `.md` file, parse frontmatter (name, model), extract body as system prompt, compute session file path as `.pi/agent-sessions/<kebab-name>.jsonl`, return `BoardMemberConfig[]`
- Create `.pi/agent-sessions/` directory if it doesn't exist
- Add `appendToLog(logPath: string, entry: object)` function: JSON.stringify + newline + appendFileSync
- Add `getConstraintState(state: MeetingState)` function: calculate elapsed minutes, check past_min/past_max/approaching/hit_max booleans based on meeting constraints and budget
- Read `@specs/init.md` for the exact .jsonl entry format and constraint state fields
- Read `@apps/ceo/extensions/ceo-and-board.ts` for the existing scaffolding to extend
- Read `@ai_docs/pi-agent/extensions.md` for the extension API patterns

### 2. Build Board Member Pi Subprocess Function

- **Task ID**: board-member-call
- **Depends On**: meeting-state-infra
- **Assigned To**: ext-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- Add `callBoardMember(member: BoardMemberConfig, ceoMessage: string, signal?: AbortSignal)` async function that spawns a Pi agent subprocess
- **Every call** builds the same base args: `["--mode", "json", "-p", "--no-extensions", "--no-skills", "--no-prompt-templates", "--no-themes", "--session", member.sessionFile, "--thinking", "off"]`
- **First call** (session file doesn't exist): add `["--system-prompt", member.systemPrompt, "--model", member.model]` to set personality and model
- **Subsequent calls** (session file exists): just the base args + message — pi auto-resumes from the session file. No `-c` flag needed.
- Check `existsSync(member.sessionFile)` to determine first vs subsequent
- **JSON event parsing** from stdout (follow pattern from `ai_docs/pi-agent/examples-extensions/subagent/index.ts`):
  - Accumulate text from `message_update` events where `assistantMessageEvent.type === "text_delta"`
  - On `message_end`: extract full response text, usage stats (`input`, `output`, `cacheRead`, `cacheWrite`, `cost.total`), model, stopReason
  - Track `contextTokens` from `msg.usage.totalTokens` for remaining context window calculation
- Accept an optional `onText?: (partial: string) => void` callback — called on each `text_delta` event so the caller can stream partial text to the TUI via `onUpdate`
- Return: `{ response: string, tokensIn: number, tokensOut: number, cost: number, contextTokens: number, model: string }`
- Handle subprocess errors: non-zero exit code, stderr output, abort signal propagation (kill process on signal abort)
- Read `@ai_docs/pi-agent/examples-extensions/subagent/index.ts` lines 210-377 for the subprocess spawn and JSON event parsing pattern
- Read `@ai_docs/pi-agent/pi-vs-cc/extensions/agent-team.ts` for the session file management pattern
- **Tested and confirmed**: `--session <path>` auto-resumes if the file exists. No `-c` flag needed. `--system-prompt` overwrites (not appends). System prompt passed as text arg, not file path.

### 3. Register `converse` Tool

- **Task ID**: converse-tool
- **Depends On**: board-member-call
- **Assigned To**: ext-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- Register `converse` via `pi.registerTool()` with TypeBox schema: `to` (string or array of strings), `message` (string)
- In `execute()`: resolve `to` to board member names (handle `"all"` → all active members), iterate sequentially, for each member:
  1. Append CEO prompt entry to .jsonl
  2. Stream real-time updates via `onUpdate?.({ content: [{ type: "text", text: "Revenue is responding..." }] })` — shows partial text as the subprocess runs (pass `onText` callback to `callBoardMember` that calls `onUpdate` with accumulated text)
  3. Call `callBoardMember()` (spawns/resumes Pi subprocess)
  4. On completion: inject a standalone `pi.sendMessage({ customType: "board-response", content: response, display: true, details: { member: name, color: member.color } })` — this renders as a visible colored message in the conversation flow via our custom renderer
  5. Append response entry to .jsonl
  6. Update `meetingState.budgetSpent` and `memberStats`
- After all calls: compute constraint state via `getConstraintState()`, check if `hit_max` — if true, include a hard message telling the CEO to call `end_deliberation` immediately
- Return: `{ content: [{ type: "text", text: formatted summary of all responses }], details: { responses: [...], constraintState: {...} } }`
- **Critical guardrail**: if `hit_max` is already true when `converse` is called, reject the call with a message telling the CEO the meeting is over and they must call `end_deliberation`
- **`renderCall`**: styled header showing CEO → member name(s), message preview
- **`renderResult`**: compact summary with constraint state, member count, total cost. Detail on expand (Ctrl+O).
- Register `pi.registerMessageRenderer("board-response", ...)` — renders each board member's response with their unique background color (from config hex), bold name header, response text. This is the primary visual for the conversation.
- Read `@ai_docs/pi-agent/extensions.md` for `pi.registerTool()` API, `onUpdate` streaming, `pi.sendMessage()`, `registerMessageRenderer`
- Read `@ai_docs/pi-agent/examples-extensions/subagent/index.ts` for the tool registration pattern with `renderCall`, `renderResult`, `onUpdate`

### 4. Register `end_deliberation` Tool

- **Task ID**: end-deliberation-tool
- **Depends On**: converse-tool
- **Assigned To**: ext-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- Register `end_deliberation` via `pi.registerTool()` with TypeBox schema: `message` (string)
- **Critical guardrail**: if `past_min_time` is false OR `past_min_budget` is false, REJECT the call — return a tool result telling the CEO "Min constraints not reached. You have X minutes and $Y remaining before you can end. Keep deliberating."
- In `execute()`: set `meetingState.phase = "ending"`, iterate all active members sequentially for final statements, **contrarian goes last** (sort members to put contrarian at end), for each member: append `end_deliberation` entry to .jsonl, call `callBoardMember()` with the CEO's closing message, append `final_statement` entry to .jsonl
- After all statements: set `meetingState.phase = "complete"`, write `meeting_end` entry to .jsonl with stats
- Return all final statements as formatted text

### 5. Implement `/ceo-begin` Command & CEO System Prompt Injection

- **Task ID**: ceo-begin-command
- **Depends On**: end-deliberation-tool
- **Assigned To**: ext-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- Update the existing `/ceo-begin` command handler: (1) check config exists, (2) list `.md` files in `briefs/` sorted by mtime, (3) present `ctx.ui.select()` for brief selection, (4) read and validate brief (check for `## Situation`, `## Stakes`, `## Constraints`, `## Key Question` headers), (5) initialize `MeetingState`, (6) write `meeting_start` .jsonl entry, (7) load board members via `loadBoardMembers()`, (8) set `meetingState.phase = "deliberating"`
- Register `before_agent_start` handler: if `meetingState.phase === "deliberating"`, read `agents/ceo.md` body as CEO system prompt, append brief content, append tool usage instructions, return `{ systemPrompt: assembledPrompt }`
- After setup: call `pi.sendUserMessage()` with the opening prompt: "Read the brief below and begin the board deliberation.\n\n<brief content>"
- Read `@ai_docs/pi-agent/examples-extensions/send-user-message.ts` for the `pi.sendUserMessage()` pattern

### 6. Build Board Status Widget

- **Task ID**: board-status-widget
- **Depends On**: ceo-begin-command
- **Assigned To**: ext-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- Build a persistent TUI widget via `ctx.ui.setWidget("board-status", ...)` that shows all active board members
- Layout: rows of 4 members. Each member in a colored box using their `color` from the config YAML
- Per-member info (minimal): name, total chats (count of prompt + response entries for this member), total cost ($X.XX), remaining context window (e.g. `847k` — calculated as model context window minus estimated tokens used by this member's last call)
- Use ANSI 24-bit color escapes (`\x1b[48;2;R;G;Bm`) to render each member's background color from their hex config value
- Widget re-renders after every `converse()` and `end_deliberation()` call by calling `widget.invalidate()` or re-setting the widget
- Parse hex colors from config: `"#ff7edb"` → `{ r: 255, g: 126, b: 219 }`
- Track per-member stats in meeting state: `memberStats: Map<string, { chats: number, cost: number, tokensUsed: number }>`
- Read `@ai_docs/pi-agent/extensions.md` for `ctx.ui.setWidget()` API
- Read `@ai_docs/pi-agent/examples-extensions/subagent/index.ts` for widget rendering patterns (Container, Text, render method)
- Read `@ai_docs/pi-agent/tui.md` for TUI component details

### 7. Implement `stop` and `wrap` Input Interception

- **Task ID**: input-interception
- **Depends On**: board-status-widget
- **Assigned To**: ext-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- Register `input` event handler: if `meetingState.phase === "deliberating"` or `meetingState.phase === "ending"`:
  - If text is `stop`: set phase to "complete", write `meeting_end` to .jsonl with `end_reason: "user_stop"`, call `ctx.abort()`, notify user "Meeting stopped.", return `{ action: "handled" }`
  - If text is `wrap`: notify "Wrapping up deliberation...", use `pi.sendUserMessage("Call end_deliberation now. The user has requested an early wrap-up.", { deliverAs: "steer" })`, return `{ action: "handled" }`
  - Otherwise: notify "Meeting in progress. Type 'stop' to halt or 'wrap' to end early.", return `{ action: "handled" }`

### 8. Memo Generation & Editor Open

- **Task ID**: memo-generation
- **Depends On**: input-interception
- **Assigned To**: ext-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- Register a `tool_result` event handler: when a `write` tool completes and the file path is inside `memos/`, auto-inject YAML frontmatter at the top of the written file
- Frontmatter fields (from meeting state): `title`, `date`, `duration`, `budget_used`, `board_members` (list), `brief` (path), `transcript` (path to .jsonl)
- Use `readFileSync` to read what the CEO wrote, prepend the frontmatter block, `writeFileSync` back
- After frontmatter injection: spawn the configured editor via `child_process.spawn(config.meeting.editor, [memoPath], { detached: true, stdio: "ignore" })` and `.unref()` so it doesn't block pi
- Set `meetingState.phase = "complete"` and write `meeting_end` .jsonl entry with final stats
- Notify user: "Memo saved to <path>. Opening in <editor>."
- The CEO's system prompt (in ceo.md Workflow step 6) already instructs it to write the memo after end_deliberation — this task just handles the frontmatter injection and editor launch
- Read `@specs/init.md` for the exact Memo File Format frontmatter fields

### 9. Validate Full Extension

- **Task ID**: validate-all
- **Depends On**: memo-generation
- **Assigned To**: ext-validator
- **Agent Type**: general-purpose
- **Parallel**: false
- Read the completed `ceo-and-board.ts` and verify:
  - All TypeBox schemas are valid and match the spec in `specs/init.md`
  - Config parsing still works (existing `parseConfig` function preserved)
  - `.jsonl` entries match the format from `specs/init.md` (type fields: prompt, response, final_statement, meeting_start, meeting_end, end_deliberation)
  - Constraint state calculation is correct (elapsed time vs min/max, budget vs min/max, approaching = 80% of max)
  - `end_deliberation` correctly rejects when mins not reached
  - `converse` correctly stops when max is hit
  - `stop` and `wrap` input interception works
  - Contrarian-last ordering in `end_deliberation`
  - All imports are correct (`node:child_process`, `node:fs`, `node:path`, `node:os`, `@sinclair/typebox`, `@mariozechner/pi-coding-agent`, `@mariozechner/pi-tui`)
  - No leftover placeholder code from the scaffolding

---

## Acceptance Criteria

- [ ] `/ceo-begin` lists brief files, validates headers, starts meeting, injects CEO system prompt
- [ ] `converse` tool makes sequential stateless Anthropic API calls to board members
- [ ] Each `converse` call appends prompt + response entries to `.jsonl`
- [ ] Constraint state (elapsed time, budget, min/max flags) returned on every `converse` call
- [ ] `converse` rejects if `hit_max` is already true
- [ ] `end_deliberation` rejects if min constraints not reached
- [ ] `end_deliberation` collects final statements with contrarian last
- [ ] `stop` input immediately halts the meeting and writes `meeting_end`
- [ ] `wrap` input steers the CEO to call `end_deliberation`
- [ ] Board member responses visible in TUI as tool results
- [ ] `.jsonl` file contains well-formed JSON lines with correct type fields
- [ ] Board status widget renders active members in rows of 4 with unique background colors
- [ ] Widget updates after each `converse()` call showing chats, cost, and remaining context per member
- [ ] Agent colors parsed from config YAML and rendered as ANSI 24-bit background colors
- [ ] CEO writes memo via `write` tool, extension auto-injects YAML frontmatter (date, duration, budget, members, brief, transcript)
- [ ] Memo file opened in configured editor after write completes

## Validation Commands

- `cd apps/ceo && npx tsc --noEmit extensions/ceo-and-board.ts` — verify TypeScript compiles
- `cat .pi/ceo-agents/deliberations/*.jsonl | head -20` — verify .jsonl format after a test run
- `pi -e extensions/ceo-and-board.ts` — launch and test `/ceo-begin` flow manually

## Notes

- Board members are spawned as `pi` subprocesses — no direct Anthropic API calls. Pi handles auth, model routing, and token tracking natively.
- Cost tracking comes from `message_end` events: `msg.usage.cost.total` gives the actual cost per turn. Budget tracking is the sum of all member turn costs.
- Context window tracking comes from `msg.usage.totalTokens` in `message_end` events. Remaining context = model's context window - totalTokens.
- Session files live in `.pi/agent-sessions/` — one `.json` file per board member. These persist across meetings. For a fresh meeting, delete the directory.
- The system prompt is only passed on the first call via `--system-prompt <text>` (overwrites, not appends). On subsequent calls (session file exists), pi auto-resumes — no system prompt or `-c` flag needed.
- Board member model defaults to `anthropic/claude-sonnet-4-6-20260219` if not specified in frontmatter. Passed via `--model` flag.
- The CEO system prompt is the full body of `agents/ceo.md` plus the brief content appended at the end.
- Follow the subprocess spawn pattern from `ai_docs/pi-agent/examples-extensions/subagent/index.ts` and the session resume pattern from `ai_docs/pi-agent/pi-vs-cc/extensions/agent-team.ts`.
- The `.jsonl` conversation log is a separate artifact from the Pi session files. It's our structured record of the deliberation. Session files are Pi's internal state.

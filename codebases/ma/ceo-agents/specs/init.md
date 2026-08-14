# CEO Agents
> Make high leverage strategic decisions with your dedicated CEO & Board members.

## Purpose

### Problem

Soon... You and I will have access to a country of geniuses in a data center. The question is then, what's the highest leverage way to use them?
Right now, we're treating agents as 'workers' to do the low level work. This is a great start, but they can do so much more.
Powerful models and agents can do much more than just write plans, code, review, test, document, etc. They can make high leverage strategic decisions.
Not only that, they can help improve your understanding of trade offs and constraints when making critical decisions.

### Solution

So, I propose a dedicated CEO & Board members to help you make high leverage strategic decisions.
Great leaders, builders, and creators are NEVER successful alone. They have a team of advisors, mentors, and experts to help them make the best decisions.
What we'll do here, may be the most high leverage way to use agents. There are so many decisions that have life changing consequences. They deserve the best possible advice, time, and resources.

Let me be clear, this is not a replacement for your human team. The CEO Agents are meant to be an additional layer of information to present new solutions and expose flaws in your current plans.

This system will be built using the pi agent for complete customization.

## Implementation Details

- The CEO and Board members are one shot agents. After your initial prompt, they don't take additional input. You're not included in the conversation. So make sure your initial prompt is clear and concise.
- The application contains the ui needed to follow along the conversation to see how the decisions are made.
- Providing key context about your business, problem, and question is critical to the success of the conversation.
- The ceo and board members have unique perspectives on how to make decisions. They will present different solutions and expose flaws in your current plans.
- The ceo and board member pi coding agent will NOT start unless the 'brief' file is present in the correct format (check headers). It will not let you waste their time (your resources) by not providing the correct input.
  - If presented in the wrong format, they will give feedback and ask you to correct it.

### User Interface

- Once prompted, the ui will be a chat interface with the ceo and board members.
- The ceo will be on the right (acting as the user), and the board members will be on the left (acting as the agents).
- The ceo will conduct the conversation, and ask questions to one or more board members.
- On boot up the customized pi coding agent will do the following.
  - Look for a `.pi/ceo-agents/` directory.
  - Look for a `ceo-and-board-configuration.yaml` file.
  - Look for the path to all the board members based on the yaml file (based on root of project). (we'll store in `.pi/ceo-agents/agents/<agent name system prompts>.md`)
  - Upon confirmation, the pi coding agent will show these items and ask you to lock in or change the budget, min, and max time for the meeting.
  - Then, finally, it will ask you to provide a path to the brief file.
    - It will provide an autocomplete for this, sorting by most recent .md files with a depth of 3 respecting gitignore.
  - Upon confirmation, the pi coding agent will start the conversation. And it's completely hands off from there for the user.
- Now the ceo will conduct the conversation, and ask questions to one or more board members.
  - The user will be able to view the conversation in the ui. But they won't be able to prompt anything (all prompts will be ignored).
    - The user can type 'stop' the process by hitting escape. They can also end the conversation early by typing 'wrap'.
  - The ceo and board will think through the problem, and present their solutions, discuss at length, back and fourth.
  - If they have not reached a min time, they will continue to think through the problem.
  - Upon hitting the budget or max time, they will stop, the ceo will then ask every agent to summarize their final stance on the problem.
  - The ceo will then generate an output memo of every board members staance, decision, top 3 recommendations, with the final decision as #1, and breakdown why including all the trade offs, constraints, risks, reasoning, etc.
  - After that, the pi coding agent will disable entries (users can type but nothing will be sent, we'll eat incoming commands).
  - We'll maintain a persistant path to the memo file.
  - When the conversation completes the pi coding agent will open the memo file in the editor specified in the configuration file.

## Inputs and Outputs

- Inputs:
  - ceo and board configuration file.
  - ceo and board member specialized system prompts (customized agents).
  - business context and information.
  - Brief: user prompt / plan / question.
  - customized pi coding agent to orchestrate the ceo and board members.
- Outputs:
  - conversation with the ceo and board members.
  - Memo: a 'memo' - a summary of the conversation and the decisions made.

## CEO Agent Tools

The CEO agent has two custom tools plus pi's built-in `write` tool. That's it.

### `converse(to, message)`

The workhorse. Every board interaction goes through this tool.

**Parameters:**
- `to` — `string | string[]` — board member name(s). CEO can address 1, multiple, or `"all"`.
- `message` — `string` — the CEO's question, challenge, follow-up, or directive.

**Behavior:**
1. For each addressed board member (sequentially — later members see earlier responses from the same round):
   a. Load the member's system prompt (personality + expertise files + domain restrictions from their frontmatter).
   b. Assemble the conversation-prompt template: inject `CONVERSATION_LOG_PATH` and fill `CEO_PROMPT` with the CEO's message.
   c. Make a **stateless LLM call** — fresh call each time, not a persistent session. The member re-reads the full conversation log on every invocation. This is why 1M context matters.
   d. Append the CEO's outbound message to the `.jsonl` conversation log.
   e. Append the member's response to the `.jsonl` conversation log.
2. Return all responses to the CEO, plus the current **constraint state**:
   - `elapsed_time_minutes` — how long the meeting has been running
   - `budget_spent` — total spend so far
   - `past_min_time` — `boolean`
   - `past_min_budget` — `boolean`
   - `approaching_max_time` — `boolean` (within 80% of max)
   - `approaching_max_budget` — `boolean` (within 80% of max)
   - `hit_max` — `boolean` — if `true`, the CEO must call `end_deliberation` immediately

**Conversation log entries (appended per call):**

```jsonl
{"from": "CEO", "to": "Revenue", "message": "...", "timestamp": "...", "type": "prompt"}
{"from": "Revenue", "to": "all", "message": "...", "timestamp": "...", "type": "response", "tokens_in": 0, "tokens_out": 0, "cost": 0.00}
```

Every message gets a `type` field: `prompt` for CEO outbound, `response` for board member replies. Token and cost tracking on responses feeds the constraint state.

### `end_deliberation(message)`

Wraps the meeting. Combines contrarian-last and final statement collection into one tool call.

**Parameters:**
- `message` — `string` — the CEO's closing prompt to the board (e.g., "We've reached our time limit. Summarize your final position in one statement.")

**Behavior:**
1. Prompts all active board members sequentially for their final one-statement position.
2. **Contrarian goes last** — enforced by the tool, not left to the CEO to remember.
3. Each final statement is appended to the `.jsonl` conversation log with `"type": "final_statement"`.
4. Returns all final statements in order.
5. After this tool returns, the CEO's only remaining job is to synthesize and write the memo using the `write` tool.

**Conversation log entries:**

```jsonl
{"from": "CEO", "to": "all", "message": "...", "timestamp": "...", "type": "end_deliberation"}
{"from": "Revenue", "to": "all", "message": "...", "timestamp": "...", "type": "final_statement", "tokens_in": 0, "tokens_out": 0, "cost": 0.00}
{"from": "Contrarian", "to": "all", "message": "...", "timestamp": "...", "type": "final_statement", "tokens_in": 0, "tokens_out": 0, "cost": 0.00}
```

### `write` (pi built-in)

The CEO uses pi's built-in write tool to produce the final memo file. The pi extension auto-injects the YAML frontmatter (date, duration, budget_used, board_members, brief path, transcript path). The CEO writes the markdown body.

---

## Subagent Architecture

Board members are **persistent Pi agent sessions** spawned as subprocesses. Each board member gets their own session file at `.pi/agent-sessions/<member-name>.json` and retains their full context window across rounds of deliberation.

### Why persistent sessions

- Each board member's 1M context window accumulates the full conversation naturally — no need to re-read a `.jsonl` log every call.
- Pi handles compaction, token tracking, and model routing natively per session.
- Session files persist on disk — meetings can theoretically be resumed if interrupted.
- The subprocess pattern (`pi --mode json -p`) gives us JSON event streaming for real-time response parsing, usage stats, and context fill tracking.

### How a board member call works

```bash
# First call (session file doesn't exist — set personality):
pi --mode json -p --no-extensions --no-skills --no-prompt-templates --no-themes \
   --session .pi/agent-sessions/revenue.jsonl \
   --system-prompt "<revenue.md body>" \
   --model anthropic/claude-sonnet-4-6 --thinking off \
   "What's the fastest paid wedge here?"

# All subsequent calls (session file exists — auto-resumes):
pi --mode json -p --no-extensions --no-skills --no-prompt-templates --no-themes \
   --session .pi/agent-sessions/revenue.jsonl \
   --thinking off \
   "Revenue, stress-test the Compounder's retention argument."
```

Parse JSON events from stdout:
- `text_delta` → accumulate response text in real-time
- `message_end` (role=assistant) → extract usage (tokens, cost, context fill)

Response returned to CEO + appended to `.jsonl` conversation log.

### Session management

- Session directory: `.pi/agent-sessions/` (created on first meeting)
- Session file naming: `<kebab-case-member-name>.jsonl` (e.g., `revenue.jsonl`, `customer-oracle.jsonl`)
- `--session <path>` auto-resumes if the file exists — no `-c` flag needed
- First call detected via `existsSync(sessionFile)` — only the first call passes `--system-prompt` and `--model`
- `--system-prompt` **overwrites** the default system prompt (not appends). Passed as text argument, not a file path.

### Model selection

Each board member specifies their model in their system prompt frontmatter (`model: anthropic/claude-sonnet-4-6-20260219`). The extension passes `--model <model>` to the subprocess. The CEO agent itself runs on Opus. Board members can run on Sonnet for cost efficiency or Opus for deeper reasoning — configurable per member.

### Call sequencing

When the CEO addresses multiple members in a single `converse()` call, subprocess calls are made **sequentially**. Each member's response is appended to the `.jsonl` before the next member is prompted. Later members in the same round don't automatically see earlier responses (they're in separate sessions), but the CEO's follow-up prompts carry the context forward.

### Conversation log as source of truth

The `.jsonl` file is the single source of truth for the entire deliberation. Every interaction flows through it:

| Event                        | Who writes           | `type` field                   |
| ---------------------------- | -------------------- | ------------------------------ |
| CEO prompts a member         | `converse()`         | `prompt`                       |
| Board member responds        | `converse()`         | `response`                     |
| CEO ends deliberation        | `end_deliberation()` | `end_deliberation`             |
| Board member final stance    | `end_deliberation()` | `final_statement`              |
| Meeting metadata (start/end) | Pi extension         | `meeting_start`, `meeting_end` |

The pi extension also writes bookend entries when the meeting starts and ends:

```jsonl
{"type": "meeting_start", "timestamp": "...", "brief": "path/to/brief.md", "board_members": ["Revenue", "Compounder", "Contrarian", ...], "constraints": {"min_time": 5, "max_time": 10, "min_budget": 2, "max_budget": 10}}
{"type": "meeting_end", "timestamp": "...", "elapsed_minutes": 8.3, "total_cost": 7.42, "end_reason": "max_time"}
```

---

## Critical File Formats

### CEO and Board Configuration File

- This is the configuration file that details the board members you want to include in the conversation.

```yaml
---
meeting:
    - constraints:
        - min_time_minutes: 5
          max_time_minutes: 10
          min_budget: $2
          max_budget: $10
    - editor: 'code' # or cursor or whatever
paths:
    briefs: .pi/ceo-agents/briefs/         # where brief .md files live
    deliberations: .pi/ceo-agents/deliberations/ # conversation .jsonl logs
    memos: .pi/ceo-agents/memos/           # output memo .md files
    agents: .pi/ceo-agents/agents/         # board member system prompts
board:
    - name: Revenue
      path: agents/revenue.md              # relative to paths.agents
      color: "#ff7edb"                     # pink — unique bg color for TUI widget
    - name: Compounder
      path: agents/compounder.md
      color: "#72f1b8"                     # green
    - name: Customer Oracle
      path: agents/customer-oracle.md
      color: "#36f9f6"                     # cyan
    - name: Product Strategist
      path: agents/product-strategist.md
      color: "#fede5d"                     # yellow
    - name: Technical Architect
      path: agents/technical-architect.md
      color: "#ff6e96"                     # red-pink
    - name: Market Strategist
      path: agents/market-strategist.md
      color: "#b893ce"                     # purple
    - name: Contrarian
      path: agents/contrarian.md
      color: "#ff9e64"                     # orange
    - name: Moonshot
      path: agents/moonshot.md
      color: "#7dcfff"                     # light blue
```

#### Directory Structure

```
.pi/ceo-agents/
├── ceo-and-board-configuration.yaml
├── agents/                          # board member system prompts
│   ├── ceo.md
│   ├── revenue.md
│   ├── compounder.md
│   ├── customer-oracle.md
│   ├── product-strategist.md
│   ├── technical-architect.md
│   ├── market-strategist.md
│   ├── contrarian.md
│   └── moonshot.md
├── briefs/                          # input: user-authored brief files
│   └── 2026-03-17-pricing-strategy.md
├── deliberations/                   # conversation logs (.jsonl per meeting)
│   └── 2026-03-17-pricing-strategy.jsonl
└── memos/                           # output: CEO-generated memos
    └── 2026-03-17-pricing-strategy.md
```

- **`briefs/`** — user creates brief files here. The pi extension autocompletes from this directory (sorted by most recent) when prompting the user to select a brief.
- **`deliberations/`** — one `.jsonl` file per meeting. Named to match the brief. This is the full conversation transcript the memo frontmatter `transcript:` field points to.
- **`memos/`** — one `.md` file per meeting. Named to match the brief. The pi extension opens this in the configured editor when the meeting completes.
- **`agents/`** — board member system prompt files with frontmatter (expertise, skills, model, domain).

File naming convention: `<YYYY-MM-DD>-<brief-slug>.<ext>`. The deliberation and memo files inherit the brief's filename stem so all three artifacts for a single meeting are trivially linked.

### Customized System Prompts

- This is the system prompt
- No skill search other than whats given.
- Domain restricts access
- It has frontmatter that details the expertise, skills, model, and domain files of the agent.
    
```yaml
---
name: CEO
expertise:
    - path: file.xml
      use-when: ".."
      updatable: false
skills:
    - path-to-auto-activated-skill.md
    - ceo-and-board-member.md
model: anthropic/claude-4-6-sonnet-20260219
domain:
    - path: path-to-dir-this-agent-can-access/
        crud: r
---

...remaining system prompt here...
```
    
### Conversation File Format

- Append only.
- **Addressing rules:**
  - **CEO** can address 1 or more specific board members (`to: "member"` or `to: ["member1", "member2"]`) or the entire board (`to: "all"`). The CEO is the only role that can direct questions to specific members.
  - **Board members** must always respond to everyone (`to: "all"`). No side conversations. Every opinion is out in the open for the full board to see and challenge.

```jsonl
{"from": "<agent name>", "to": "<agent name>" | ["<name1>", "<name2>"] | "all", "message": "..."}
```

### Conversation Prompt (`conversation-prompt.md`)

- This is the prompt template the CEO uses to invoke board members during deliberation.
- Every board member, every time they are prompted, must reread the full conversation log before responding. No exceptions. This ensures no context is lost across rounds.
- The CEO fills in the `CONVERSATION_LOG_PATH` and `CEO_PROMPT` variables before sending.
- Board members respond to `all` per the addressing rules above.

```md
## Step 1: Reread the conversation log

Read the full conversation log at:

> `{{CONVERSATION_LOG_PATH}}`

Parse every entry. Understand who said what, what positions have been taken, what tensions are unresolved, and where the deliberation currently stands.

## Step 2: Respond

{{CEO_PROMPT}}

Respond to the CEO and the full board with your position. Be direct. Reference specific arguments from the conversation log if you agree or disagree. Do not repeat what others have already said — build on it, challenge it, or take it further.
```

### Brief File Format

- The Brief is the structured input document that frames what the board will deliberate on.
- It can frame a problem, an opportunity, a trade-off, or a strategic question — it is NOT limited to "problems."
- The pi coding agent validates the presence and format of required headers before starting the meeting. Missing or empty required headers will be rejected with feedback.
- The `## Proposed Direction` section is optional — omit it to get a fully open deliberation without anchoring the board.

```md
# Brief: <concise title of what the board will deliberate on>

## Situation
<!-- What is happening right now? State the facts. No opinion, no spin. -->

## Stakes
<!-- What's at risk? What's the upside if we get this right? What's the downside if we get it wrong? -->

## Constraints
<!-- What are the boundaries? Budget, timeline, team capacity, technical debt, regulatory, contractual, etc. -->

## Key Question
<!-- The single most important question you want the board to answer. Be specific. -->

## Proposed Direction (optional)
<!-- If you already have a leaning, state it here. The board will stress-test it. -->

## Context Files (optional)
<!-- Paths to files the board should read before deliberating. These get loaded into agent context. -->
<!-- - path/to/relevant-doc.md -->
<!-- - path/to/data-export.csv -->
```

### Memo File Format

- The Memo is the structured output of the board deliberation. Generated by the CEO agent after the meeting concludes.
- It captures the final recommendation, each board member's stance, dissenting views, and concrete next actions.
- The CEO writes this after asking every board member to summarize their final position.
- The top recommendation is always #1. Remaining recommendations are ranked by the CEO based on the deliberation.
- Metadata is output as YAML frontmatter so it can be parsed programmatically by the pi coding agent and downstream tooling.
- The frontmatter includes the path to the full conversation transcript (.jsonl) for auditability and replay.

```md
---
title: "Board Memo: <title from the brief>"
date: <YYYY-MM-DD>
duration: <actual meeting duration>
budget_used: <actual spend>
board_members:
  - <agent name>
  - <agent name>
brief: <path to the original brief file>
transcript: <path to the conversation .jsonl file>
---

## Final Recommendation

### #1: <recommended decision>
<!-- 2-4 sentence summary of what the board recommends and why. This is the top-line answer to the Key Question from the Brief. -->

### #2: <second-best option>
<!-- 1-2 sentence summary. Why it was considered but ranked lower. -->

### #3: <third option>
<!-- 1-2 sentence summary. Why it was considered but ranked lower. -->

---

## Board Member Stances

### <Board Member Name>
- **Position:** <for / against / conditional on X>
- **Reasoning:** <1-3 sentences on their core argument>
- **Key Concern:** <the biggest risk or blind spot they flagged>

### <Board Member Name>
- **Position:** <for / against / conditional on X>
- **Reasoning:** <1-3 sentences on their core argument>
- **Key Concern:** <the biggest risk or blind spot they flagged>

<!-- repeat for each board member -->

---

## Dissent & Unresolved Tensions
<!-- Capture any strong disagreements that were NOT resolved during deliberation. These are the things to watch. -->

---

## Trade-offs & Risks
<!-- Structured breakdown of what you gain and what you give up with the #1 recommendation. -->

| Factor                         | Upside   | Downside |
| ------------------------------ | -------- | -------- |
| <!-- e.g. Speed to market -->  | <!-- --> | <!-- --> |
| <!-- e.g. Engineering cost --> | <!-- --> | <!-- --> |
| <!-- e.g. Customer impact -->  | <!-- --> | <!-- --> |

---

## Next Actions
<!-- Concrete, assignable steps to execute on the #1 recommendation. -->
- [ ] <action item 1>
- [ ] <action item 2>
- [ ] <action item 3>

---

## Deliberation Summary
<!-- A narrative summary of how the conversation unfolded. Key turning points, what changed minds, what arguments held up under scrutiny. 3-5 paragraphs. -->
```

# Plan: TillDone Multi-Team Integration

## Task Description

Integrate a TillDone task tracking system into the Multi-Team Chat orchestration system. This transforms the single-agent TillDone extension (reference: `/Users/indydevdan/Documents/projects/experimental/pi-vs-cc/extensions/tilldone.ts`) into a multi-agent task management system where the Orchestrator creates a task list from the user's request, Team Leads mark tasks in-progress and done as they delegate work to members, and the UI shows live task progress in the footer alongside the agent tree.

The original TillDone is a single-agent discipline tool: one agent, one task at a time, three-state toggle cycle (idle → inprogress → done), blocking gate that prevents tool use without a task list, auto-nudge on incomplete tasks. The multi-team version adapts this for a depth-2 delegation hierarchy where multiple teams can work in parallel.

## Objective

When complete, the Multi-Team Chat system will:
1. Orchestrator creates a titled TillDone list before delegating work
2. Team Leads mark tasks `inprogress` before starting and `done` upon completion
3. A live task progress panel renders in the footer's right column, alongside the existing agent tree on the left
4. On `agent_end`, the orchestrator is nudged to continue if incomplete tasks remain
5. Parallel team mutations are handled safely via intent-based actions and Node.js event loop serialization — no explicit locks or queues needed

## Problem Statement

The Multi-Team Chat system has no visibility into work progress. The user sends a prompt, the orchestrator delegates, and the only feedback is the agent tree showing active/idle status and streaming chat bubbles. There's no structured way to see:
- What work items were planned
- Which items are in progress and by which team
- Which items are complete
- Whether everything the user asked for was actually delivered

The TillDone system gives the orchestrator a planning discipline (break down work before delegating) and gives the user a persistent progress dashboard.

## Solution Approach

### Architecture: Parent-Child Mutation Flow

TillDone state lives **in the main Pi process** (the orchestrator's multi-team-chat.ts extension). This is where the nuclear UI runs, the footer renders, and all subprocess results flow back to.

Leads run as Pi subprocesses. They interact with TillDone through a **lead-side extension** (`tilldone-lead.ts`) that mirrors the pattern of `lead-delegate.ts`:

```
                          multi-team-chat.ts (parent)
                         ┌─────────────────────────┐
                         │  Canonical TillDone      │
                         │  State (in-memory)       │
                         │                          │
                         │  tilldone tool           │
                         │  (orchestrator actions)  │
                         │                          │
                         │  Footer renderer         │
                         │  (left: agents,          │
                         │   right: tasks)          │
                         └──────┬──────────────┬────┘
                                │              │
                    onToolUpdate │              │ onToolUpdate
                    (mutations)  │              │ (mutations)
                                │              │
                  ┌─────────────┴──┐   ┌───────┴─────────────┐
                  │ Lead subprocess │   │ Lead subprocess      │
                  │ (Engineering)   │   │ (Planning)           │
                  │                 │   │                      │
                  │ tilldone-lead.ts│   │ tilldone-lead.ts     │
                  │ (start/done)   │   │ (start/done)         │
                  └────────────────┘   └──────────────────────┘
```

**Spawn-time**: Parent serializes current task list as `TILLDONE_TASKS` env var → lead subprocess reads it at boot.

**Mutation flow**: Lead calls `tilldone start 3` → `tilldone-lead.ts` execute() sends mutation via `onUpdate()` → parent's `onToolUpdate` callback receives it → parent applies to canonical state → footer re-renders.

### Intent-Based Mutations (No Queue Needed)

Instead of the original's `toggle` cycle (idle → inprogress → done → idle), we use **intent-based actions**: `start(id)` and `done(id)`. These are naturally idempotent:

- `start(3)` when task 3 is already inprogress → no-op
- `done(3)` when task 3 is already done → no-op

Since Node.js is single-threaded, `onToolUpdate` callbacks from parallel subprocesses are processed sequentially on the event loop. This gives us **natural serialization** with no explicit mutex or message queue. Two leads marking the same task is harmless.

### Footer Two-Column Layout

```
 lead-agents │ 2m 30s                       Auth System [3/7]
 └─ ⚡ Orch 💰$0.042 🧠890K                 ● Add auth middleware    ⚡ Engineering
    ├─ ◆ Planning Lead 💰$0.015              ● Create user migration  ⚡ Engineering
    ├─ ⚡ Eng Lead 💰$0.028                  ✓ Define requirements    ◆ Planning
    └─ ◆ Validation Lead 💰$0.012            ✓ User story mapping     ◆ Planning
                                             ○ Write integration tests
                                             ○ Security audit
                                             ○ Final review
```

Left column: existing agent tree (~55% width). Right column: TillDone list (~45% width). Merged line-by-line with padding. When no TillDone list exists, left column uses full width (current behavior).

## Relevant Files

Use these files to complete the task:

- `apps/multi-team-chat/extensions/multi-team-chat.ts` — Main extension entry point. Register the orchestrator's `tilldone` tool here (alongside `delegate`). Modify `setupFooter()` to render two-column layout. Add nudge logic on `agent_end`. Pass `TILLDONE_TASKS` and `TILLDONE_TEAM_NAME` env vars to lead subprocesses in the `delegate` tool execute function. Extend `onToolUpdate` callback to handle tilldone mutations from leads.
- `apps/multi-team-chat/extensions/modules/types.ts` — Add TillDone types: `TillDoneTask`, `TillDoneState`, `TillDoneMutation`.
- `apps/multi-team-chat/extensions/modules/theme.ts` — May need a `mergeColumns()` helper for side-by-side footer rendering.
- `apps/multi-team-chat/extensions/lead-delegate.ts` — Reference for the subprocess extension pattern. The new `tilldone-lead.ts` follows this same structure (env var guard, tool registration, onUpdate communication).
- `apps/multi-team-chat/extensions/modules/subprocess.ts` — `callAgent()` function. The `-e` flag already loads `lead-delegate.ts`; needs to also load `tilldone-lead.ts`.
- `.pi/multi-team/agents/orchestrator.md` — Add `tilldone` to tools list. Add instructions for creating task lists before delegation.
- `.pi/multi-team/agents/engineering-lead.md` — Add `tilldone` to tools list. Add instructions for marking tasks.
- `.pi/multi-team/agents/planning-lead.md` — Same as above.
- `.pi/multi-team/agents/validation-lead.md` — Same as above.
- `/Users/indydevdan/Documents/projects/experimental/pi-vs-cc/extensions/tilldone.ts` — Reference implementation. Borrow types, status helpers, UI patterns. Do NOT copy-paste; adapt for multi-agent.

### New Files

- `apps/multi-team-chat/extensions/modules/tilldone.ts` — TillDone state management module: types, mutation functions, rendering helpers for the footer right-column.
- `apps/multi-team-chat/extensions/tilldone-lead.ts` — Lead subprocess extension. Registers a `tilldone` tool with limited actions (`start`, `done`, `list`). Communicates mutations back to parent via `onUpdate`.

## Implementation Phases

### Phase 1: Foundation — State Module + Types

Build the TillDone state management module that both the main extension and the lead extension will use.

**`modules/tilldone.ts`** — Core state and rendering:

```typescript
// ── Types ──────────────────────────────────────────────────────
export type TaskStatus = "idle" | "inprogress" | "done";

export interface TillDoneTask {
    id: number;
    text: string;
    status: TaskStatus;
    team?: string;       // team name when marked inprogress
    teamColor?: string;  // hex color for UI
}

export interface TillDoneState {
    title: string;
    description?: string;
    tasks: TillDoneTask[];
    nextId: number;
}

// Mutation sent from lead subprocess → parent via onUpdate
export interface TillDoneMutation {
    type: "tilldone-mutation";
    action: "start" | "done";
    id: number;
    team?: string;
    teamColor?: string;
}

// ── Status helpers ─────────────────────────────────────────────
export const STATUS_ICON: Record<TaskStatus, string> = {
    idle: "○", inprogress: "●", done: "✓"
};

// ── State mutations (all idempotent) ───────────────────────────
export function applyMutation(state: TillDoneState, mutation: TillDoneMutation): void { ... }
export function addTask(state: TillDoneState, text: string): TillDoneTask { ... }
export function addTasks(state: TillDoneState, texts: string[]): TillDoneTask[] { ... }
export function startTask(state: TillDoneState, id: number, team?: string, teamColor?: string): TillDoneTask | null { ... }
export function doneTask(state: TillDoneState, id: number): TillDoneTask | null { ... }
export function updateTask(state: TillDoneState, id: number, text: string): TillDoneTask | null { ... }
export function removeTask(state: TillDoneState, id: number): TillDoneTask | null { ... }

// ── Footer rendering ───────────────────────────────────────────
export function renderTillDoneColumn(state: TillDoneState, width: number, hexFg: ..., dim: ..., bold: ...): string[] { ... }
export function mergeColumns(left: string[], right: string[], leftWidth: number, totalWidth: number, truncFn: ...): string[] { ... }
```

Key design decisions for the state module:
- `startTask` is idempotent: if already inprogress, no-op but updates team attribution
- `doneTask` is idempotent: if already done, no-op
- `mergeColumns` pads shorter column with empty lines, truncates each merged line to total width
- State is a plain object (no class) — easy to serialize for env var injection

### Phase 2: Core Implementation

**2a. Orchestrator `tilldone` tool** (in `multi-team-chat.ts`)

Register alongside the existing `delegate` tool. Full action set for the orchestrator:

```typescript
pi.registerTool({
    name: "tilldone",
    label: "TillDone",
    description: "Manage the task list. Create a list before delegating work. " +
        "Actions: new-list (text=title, description), add (text or texts[]), " +
        "start (id — mark inprogress), done (id — mark complete), " +
        "update (id + text), remove (id), list, clear.",
    parameters: Type.Object({
        action: StringEnum(["new-list", "add", "start", "done", "update", "remove", "list", "clear"]),
        text: Type.Optional(Type.String()),
        texts: Type.Optional(Type.Array(Type.String())),
        description: Type.Optional(Type.String()),
        id: Type.Optional(Type.Number()),
    }),
    async execute(_id, params) {
        // Apply mutation to shared tilldoneState
        // Return confirmation text
        // Call refresh() to update footer
    },
    renderCall() { return new Text("", 0, 0); },  // Invisible — handled by chat UI
    renderResult() { return new Text("", 0, 0); },
});
```

Add the `tilldone` tool emoji to the TOOL_EMOJI map:
```typescript
const TOOL_EMOJI: Record<string, string> = {
    // ... existing
    tilldone: "📋",
};
```

**2b. Lead TillDone extension** (`tilldone-lead.ts`)

Follows the `lead-delegate.ts` pattern exactly:

```typescript
export default function (pi: ExtensionAPI) {
    // Guard: only activate for leads (not members)
    const tasksJson = process.env.TILLDONE_TASKS;
    if (!tasksJson) return;

    const teamName = process.env.TILLDONE_TEAM_NAME || "";
    const teamColor = process.env.TILLDONE_TEAM_COLOR || "#ffffff";

    let state: TillDoneState;
    try { state = JSON.parse(tasksJson); } catch { return; }

    pi.registerTool({
        name: "tilldone",
        label: "TillDone",
        description: "Mark tasks in the shared task list. " +
            "Actions: start (id — mark inprogress), done (id — mark complete), list.",
        parameters: Type.Object({
            action: StringEnum(["start", "done", "list"]),
            id: Type.Optional(Type.Number()),
        }),
        async execute(_id, params, _signal, onUpdate) {
            switch (params.action) {
                case "start": {
                    startTask(state, params.id!, teamName, teamColor);
                    // Send mutation to parent
                    onUpdate?.({
                        type: "tilldone-mutation",
                        action: "start",
                        id: params.id!,
                        team: teamName,
                        teamColor,
                    });
                    return { content: [{ type: "text", text: `Task #${params.id} → inprogress` }] };
                }
                case "done": { /* similar */ }
                case "list": { /* return formatted task list */ }
            }
        },
        renderCall() { return new Text("", 0, 0); },
        renderResult() { return new Text("", 0, 0); },
    });
}
```

**2c. Load tilldone-lead.ts in subprocess spawning**

In `subprocess.ts`, add the extension path:

```typescript
const TILLDONE_LEAD_PATH = join(__extensionsDir, "tilldone-lead.ts");

// In callAgent args:
const args: string[] = [
    "--mode", "json", "-p",
    "--no-extensions",
    "-e", ENFORCER_PATH,
    "-e", LEAD_DELEGATE_PATH,
    "-e", TILLDONE_LEAD_PATH,    // ← NEW
    // ...
];
```

**2d. Pass TillDone state to leads in delegate tool**

In the `delegate` tool's execute function (multi-team-chat.ts ~line 1035), add to `leadEnv`:

```typescript
const leadEnv: Record<string, string> = {
    ...subprocessEnv,
    LEAD_MEMBERS_JSON: JSON.stringify(leadMembersRef),
    LEAD_LOG_PATH: logPath,
    TILLDONE_TASKS: JSON.stringify(tilldoneState),        // ← NEW
    TILLDONE_TEAM_NAME: team.name,                        // ← NEW
    TILLDONE_TEAM_COLOR: team.color,                      // ← NEW
};
```

**2e. Intercept lead TillDone mutations in onToolUpdate**

In the `callAgent` onToolUpdate callback (~line 1124), add before the delegate check:

```typescript
(toolCallId, toolName, partialResult) => {
    // ── TillDone mutations from lead ─────────────────
    if (toolName === "tilldone" && partialResult?.type === "tilldone-mutation") {
        applyMutation(tilldoneState, partialResult as TillDoneMutation);
        refresh(); // Re-render footer with updated task state
        return;
    }

    if (toolName !== "delegate") return;
    // ... existing member streaming logic
},
```

**2f. Two-column footer**

Modify `setupFooter()` in multi-team-chat.ts. When `tilldoneState.tasks.length > 0`, render two columns:

```typescript
function setupFooter(ctx: any) {
    ctx.ui.setFooter((_tui: any, _theme: any, _fd: any) => ({
        render(w: number): string[] {
            const leftLines = renderAgentTree(w); // Extract existing agent tree rendering
            
            if (tilldoneState.tasks.length === 0) {
                return leftLines; // No tasks — full-width agent tree (unchanged)
            }
            
            const leftW = Math.floor(w * 0.55);
            const rightW = w - leftW;
            const rightLines = renderTillDoneColumn(tilldoneState, rightW, hexFg, dim, bold);
            return mergeColumns(leftLines, rightLines, leftW, w, truncateToWidth);
        },
    }));
}
```

The right column rendering (`renderTillDoneColumn`):

```
Auth System [3/7]
● Add auth middleware    ⚡ Engineering
● Create user migration  ⚡ Engineering
✓ Define requirements    Planning
✓ User story mapping     Planning
○ Write integration tests
○ Security audit
○ Final review
```

- Line 1: title + `[done/total]` progress fraction
- Subsequent lines: status icon + task text + team attribution (if assigned)
- inprogress tasks sorted first, then idle, then done (most recent first)
- Limit to ~8 visible tasks, show "+N more" if exceeded
- inprogress icons colored by team color, done icons in green, idle in dim
- Team name shown next to inprogress/done tasks

**2g. Nudge on agent_end**

In the `agent_end` handler (~line 952), after existing cleanup:

```typescript
pi.on("agent_end", async () => {
    // ... existing cleanup ...
    
    // TillDone nudge — if list exists with incomplete tasks
    if (tilldoneState.tasks.length > 0) {
        const incomplete = tilldoneState.tasks.filter(t => t.status !== "done");
        if (incomplete.length > 0) {
            const taskList = incomplete
                .map(t => `  ${STATUS_ICON[t.status]} #${t.id}: ${t.text}`)
                .join("\n");
            addMsg("System", "#ff9e64", 
                `⚠️ ${incomplete.length} task(s) remain:\n\n${taskList}\n\nContinue working or mark them done.`,
                "system"
            );
            refresh();
            pi.sendMessage(
                { customType: "tilldone-nudge", content: `...`, display: false },
                { triggerTurn: true }
            );
        }
    }
});
```

**2h. `/tilldone` command**

Register a `/tilldone` command that posts the full task list to chat:

```typescript
pi.registerCommand("tilldone", {
    description: "Show the TillDone task list",
    handler: async () => {
        if (tilldoneState.tasks.length === 0) {
            addMsg("System", "#555", "No TillDone list active.", "system");
        } else {
            const lines = [bold(tilldoneState.title || "TillDone")];
            if (tilldoneState.description) lines.push(dim(tilldoneState.description));
            lines.push("");
            const done = tilldoneState.tasks.filter(t => t.status === "done").length;
            lines.push(`Progress: ${done}/${tilldoneState.tasks.length}`);
            lines.push("");
            for (const t of tilldoneState.tasks) {
                const icon = STATUS_ICON[t.status];
                const team = t.team ? ` (${t.team})` : "";
                lines.push(`${icon} #${t.id} ${t.text}${team}`);
            }
            addMsg("System", "#72f1b8", lines.join("\n"), "system");
        }
        refresh();
    },
});
```

### Phase 3: Integration & Polish

**3a. Agent prompt updates**

**Orchestrator** (`.pi/multi-team/agents/orchestrator.md`):

Add `tilldone` to the tools list in frontmatter:
```yaml
tools:
  - write
  - edit
  - read
  - grep
  - find
  - ls
  - delegate
  - tilldone
```

Add instructions in the body:

```markdown
### Task Management

**tilldone** — Manage the work task list.

Before delegating substantial work:
1. Call `tilldone new-list` with a descriptive title
2. Call `tilldone add` with discrete, verifiable work items
3. Then delegate to teams

After receiving team results, check the list. If tasks are incomplete, either continue delegating or mark them done with `tilldone done`.

For simple questions (greetings, clarifications, quick lookups), skip the task list entirely — only create one for work that involves multiple steps or teams.
```

**Team Leads** (engineering-lead.md, planning-lead.md, validation-lead.md):

Add `tilldone` to tools in frontmatter:
```yaml
tools:
  - write
  - edit
  - read
  - grep
  - find
  - ls
  - delegate
  - tilldone
```

Add instructions:

```markdown
### Task Management

**tilldone** — Mark tasks in the shared task list.

When you receive delegated work:
1. Call `tilldone start <id>` on the task you're taking ownership of
2. Do your work (read, delegate to members, etc.)
3. Call `tilldone done <id>` when the task is complete

Use `tilldone list` to see all tasks and their current status.
```

**3b. Orchestrator tool allowlist enforcement**

The existing `tool_call` handler at line 772 checks `orch.tools.includes(toolName)`. Adding `tilldone` to the orchestrator's frontmatter tools list ensures it passes. No code change needed — just the frontmatter update.

Similarly, the domain enforcer extension (loaded on subprocesses) checks `AGENT_ALLOWED_TOOLS`. Adding `tilldone` to lead frontmatter ensures the enforcer allows it.

**3c. Edge cases**

- **No TillDone list**: Footer renders full-width agent tree (unchanged behavior)
- **Session start with existing list**: TillDone state is in-memory, resets on session start. No persistence needed.
- **Abort/cancel**: On `agent_end`, finalize any stale states. The nudge only fires if tasks remain.
- **`/toggle-workers`**: Two-column layout still works — left column just gets taller. The `mergeColumns` function handles mismatched heights by padding the shorter column.
- **Narrow terminal**: If width < 80, could fall back to single-column (agent tree only) with TillDone in a separate footer section below. Or just let truncation handle it.

## Team Orchestration

- You operate as the team lead and orchestrate the team to execute the plan.
- You're responsible for deploying the right team members with the right context to execute the plan.
- IMPORTANT: You NEVER operate directly on the codebase. You use `Task` and `Task*` tools to deploy team members to to the building, validating, testing, deploying, and other tasks.
  - This is critical. You're job is to act as a high level director of the team, not a builder.
  - You're role is to validate all work is going well and make sure the team is on track to complete the plan.
  - You'll orchestrate this by using the Task* Tools to manage coordination between the team members.
  - Communication is paramount. You'll use the Task* Tools to communicate with the team members and ensure they're on track to complete the plan.
- Take note of the session id of each team member. This is how you'll reference them.

### Team Members

- Builder
  - Name: tilldone-builder
  - Role: Build all TillDone components — state module, lead extension, orchestrator tool integration, footer layout, nudge logic, prompt updates, and validation. Single builder with full context across all files.
  - Agent Type: general-purpose
  - Resume: true

## Step by Step Tasks

- IMPORTANT: Execute every step in order, top to bottom. Each task maps directly to a `TaskCreate` call.
- Before you start, run `TaskCreate` to create the initial task list that all team members can see and execute.

### 1. Add TillDone Types to types.ts
- **Task ID**: add-tilldone-types
- **Depends On**: none
- **Assigned To**: tilldone-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- Add `TaskStatus`, `TillDoneTask`, `TillDoneState`, and `TillDoneMutation` types to `apps/multi-team-chat/extensions/modules/types.ts`
- Keep types minimal — no methods, just plain interfaces
- `TillDoneMutation` must have `type: "tilldone-mutation"` discriminator for parent-side detection

### 2. Build TillDone State Module
- **Task ID**: build-tilldone-module
- **Depends On**: add-tilldone-types
- **Assigned To**: tilldone-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- Create `apps/multi-team-chat/extensions/modules/tilldone.ts`
- Implement all mutation functions: `createState()`, `addTask()`, `addTasks()`, `startTask()`, `doneTask()`, `updateTask()`, `removeTask()`, `clearState()`, `applyMutation()`
- All mutations are **idempotent**: `startTask` on an already-inprogress task is a no-op, `doneTask` on an already-done task is a no-op
- Implement `renderTillDoneColumn(state, width, hexFg, dim, bold, truncateToWidth)` — returns `string[]` for the footer right column
- Implement `mergeColumns(left, right, leftWidth, totalWidth, truncFn)` — merges two `string[]` side-by-side with padding
- Export `STATUS_ICON` constant for use in chat messages
- Follow existing module patterns (pure functions, no side effects, imports from types.ts)

### 3. Build Lead TillDone Extension
- **Task ID**: build-lead-extension
- **Depends On**: build-tilldone-module
- **Assigned To**: tilldone-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- Create `apps/multi-team-chat/extensions/tilldone-lead.ts`
- Follow `lead-delegate.ts` pattern exactly: env var guard (`TILLDONE_TASKS`), parse state from env, register tool, communicate via `onUpdate`
- Read `TILLDONE_TEAM_NAME` and `TILLDONE_TEAM_COLOR` env vars for team attribution
- Tool actions: `start(id)`, `done(id)`, `list`
- On `start` and `done`: apply local mutation AND send `TillDoneMutation` via `onUpdate`
- On `list`: return formatted task list text
- `renderCall` and `renderResult` return empty Text (invisible — chatView handles display)
- Import `TillDoneState`, `TillDoneMutation` from `./modules/types`
- Import mutation functions from `./modules/tilldone`
- **IMPORTANT**: Only leads get this tool. The env var guard (`TILLDONE_TASKS`) ensures workers never see it — `TILLDONE_TASKS` is only set in the lead's env, not passed through to member subprocesses.

### 4. Add tilldone-lead.ts to Subprocess Spawning
- **Task ID**: add-to-subprocess
- **Depends On**: build-lead-extension
- **Assigned To**: tilldone-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- In `apps/multi-team-chat/extensions/modules/subprocess.ts`:
  - Add `const TILLDONE_LEAD_PATH = join(__extensionsDir, "tilldone-lead.ts");`
  - Add `-e`, `TILLDONE_LEAD_PATH` to the args array (after LEAD_DELEGATE_PATH)
- Note: this loads on ALL subprocesses but self-exits immediately on workers since `TILLDONE_TASKS` is not in their env (same pattern as `lead-delegate.ts` with `LEAD_MEMBERS_JSON`)

### 5. Register Orchestrator TillDone Tool + Integrate into multi-team-chat.ts
- **Task ID**: register-orch-tool
- **Depends On**: add-to-subprocess
- **Assigned To**: tilldone-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- In `apps/multi-team-chat/extensions/multi-team-chat.ts`:
  - Add `import { ... } from "./modules/tilldone"` for state functions and rendering
  - Add `let tilldoneState: TillDoneState = createState()` at module scope (alongside other state vars)
  - Add `tilldone: "📋"` to the `TOOL_EMOJI` map
  - Register `tilldone` tool with full action set: `new-list`, `add`, `start`, `done`, `update`, `remove`, `list`, `clear`
  - Each action mutates `tilldoneState` and calls `refresh()`
  - `renderCall`/`renderResult` return empty Text (consistent with delegate tool)
  - Import `StringEnum` from `@mariozechner/pi-ai` (already available — used in reference tilldone.ts)
- **Tool access**: Only the orchestrator (main Pi process) gets the full action set. Leads get `start`/`done`/`list` via `tilldone-lead.ts`. Workers get nothing.

### 6. Integrate Two-Column Footer
- **Task ID**: integrate-footer
- **Depends On**: register-orch-tool
- **Assigned To**: tilldone-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- Modify `setupFooter()` in multi-team-chat.ts:
  - Extract existing agent tree render logic into a helper function `renderAgentTree(w): string[]`
  - When `tilldoneState.tasks.length > 0`: compute `leftW = Math.floor(w * 0.55)`, `rightW = w - leftW`
  - Call `renderTillDoneColumn(tilldoneState, rightW, ...)` for right column
  - Call `mergeColumns(leftLines, rightLines, leftW, w, truncateToWidth)` to combine
  - When no tasks: return `renderAgentTree(w)` unchanged (existing behavior)
  - Line 1 of the footer should show the TillDone title + progress on the right side of the existing `dir │ elapsed` line

### 7. Wire Up Lead Mutations + Env Vars
- **Task ID**: wire-mutations
- **Depends On**: integrate-footer
- **Assigned To**: tilldone-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- In the `delegate` tool's execute function (~line 1035):
  - Add `TILLDONE_TASKS: JSON.stringify(tilldoneState)` to `leadEnv`
  - Add `TILLDONE_TEAM_NAME: team.name` to `leadEnv`
  - Add `TILLDONE_TEAM_COLOR: team.color` to `leadEnv`
  - **Do NOT add these to member env** — `lead-delegate.ts` already strips `LEAD_MEMBERS_JSON` from the env before spawning members. Similarly, `tilldone-lead.ts` must not leak `TILLDONE_TASKS` to workers.
- In the `onToolUpdate` callback (~line 1124):
  - Before the `if (toolName !== "delegate") return;` check, add:
  - `if (toolName === "tilldone" && partialResult?.type === "tilldone-mutation") { applyMutation(tilldoneState, partialResult); refresh(); return; }`
- In the existing `tool_call` handler for non-delegate tools (~line 925):
  - Add `tilldone` to the set of tools that get emoji badges on the orchestrator bubble

### 8. Add Nudge + /tilldone Command
- **Task ID**: add-nudge-command
- **Depends On**: wire-mutations
- **Assigned To**: tilldone-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- In the `agent_end` handler (~line 952):
  - After existing cleanup, check `tilldoneState.tasks.length > 0`
  - If incomplete tasks exist, add a system message to chat and call `pi.sendMessage()` with `triggerTurn: true` to nudge the orchestrator
  - Add a `nudgedThisCycle` guard (reset on `input` event) to prevent infinite nudge loops
- Register `/tilldone` command that posts the full task list to chat as a system message

### 9. Update Agent Prompts
- **Task ID**: update-prompts
- **Depends On**: add-nudge-command
- **Assigned To**: tilldone-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- Add `tilldone` to `tools:` array in frontmatter of:
  - `.pi/multi-team/agents/orchestrator.md`
  - `.pi/multi-team/agents/engineering-lead.md`
  - `.pi/multi-team/agents/planning-lead.md`
  - `.pi/multi-team/agents/validation-lead.md`
- **Do NOT add `tilldone` to any worker/member agent prompts** (backend-dev.md, frontend-dev.md, qa-engineer.md, etc.)
- Add `### Task Management` section to orchestrator.md body with instructions for creating lists before delegation
- Add `### Task Management` section to each lead .md body with instructions for marking tasks
- Keep instructions concise — leads and orchestrator already have the `conversational-response` skill

### 10. Final Validation
- **Task ID**: validate-all
- **Depends On**: update-prompts
- **Assigned To**: tilldone-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- Run `cd apps/multi-team-chat && bun install` to ensure dependencies resolve
- Run `npx tsc --noEmit` or `bun run check` to verify TypeScript compiles
- Verify all new imports resolve correctly
- Verify `tilldone-lead.ts` self-exits when `TILLDONE_TASKS` env var is missing (member subprocess safety)
- Verify the orchestrator prompt includes `tilldone` in both the frontmatter tools list and the body instructions
- Verify all three lead prompts include `tilldone` in their frontmatter tools list
- Verify NO worker/member prompts have `tilldone` in their tools list
- Spot-check that `mergeColumns` produces correct output for mismatched-height columns and narrow widths
- Verify the `TOOL_EMOJI` map includes `tilldone: "📋"`

## Acceptance Criteria

1. The orchestrator has a `tilldone` tool with full actions: new-list, add, start, done, update, remove, list, clear
2. Team leads have a `tilldone` tool (via `tilldone-lead.ts`) with limited actions: start, done, list
3. Workers (member subprocesses) have **NO** access to the tilldone tool — enforced by env var guard (`TILLDONE_TASKS` only set for leads, not members) AND worker agent prompts do NOT list `tilldone` in their tools frontmatter
4. Lead mutations flow back to the parent via `onToolUpdate` and are applied to canonical state
5. The footer renders a two-column layout when a TillDone list is active: agent tree (left), task progress (right)
6. When no TillDone list exists, the footer renders the agent tree full-width (unchanged behavior)
7. Task progress shows: title, `[done/total]`, inprogress tasks with team color/name, idle tasks, done tasks
8. On `agent_end`, if incomplete tasks remain, the orchestrator is nudged to continue
9. The `/tilldone` command shows the full task list in chat
10. All agent prompts (.md files) include `tilldone` in their tools list and have task management instructions
11. TypeScript compiles without errors
12. Parallel team mutations are safe (intent-based, idempotent)

## Validation Commands

Execute these commands to validate the task is complete:

- `cd apps/multi-team-chat && bun install` — Verify dependencies install
- `cd apps/multi-team-chat && npx tsc --noEmit` — Verify TypeScript compiles (if tsconfig exists)
- `grep -r "tilldone" apps/multi-team-chat/extensions/ --include="*.ts" -l` — Verify tilldone is referenced in expected files
- `grep "tilldone" .pi/multi-team/agents/orchestrator.md` — Verify orchestrator prompt includes tilldone
- `grep "tilldone" .pi/multi-team/agents/engineering-lead.md` — Verify lead prompt includes tilldone
- `grep "TILLDONE_TASKS" apps/multi-team-chat/extensions/modules/subprocess.ts` — Verify subprocess loads tilldone-lead extension
- `grep "tilldone-mutation" apps/multi-team-chat/extensions/multi-team-chat.ts` — Verify parent intercepts lead mutations

## Notes

- **No new dependencies needed.** All imports (`@sinclair/typebox`, `@mariozechner/pi-coding-agent`, `@mariozechner/pi-tui`, `@mariozechner/pi-ai`) are already in the project's package.json.
- **StringEnum** from `@mariozechner/pi-ai` is needed for the action parameter. The reference tilldone.ts imports it — verify it's available in the multi-team-chat project's dependencies. If not, use `Type.Union` with `Type.Literal` values as an alternative.
- **Session persistence**: TillDone state is in-memory only. It resets on session start. This matches the original extension's behavior and is appropriate — the task list is ephemeral to the current work session.
- **Conversation log**: TillDone mutations are NOT logged to the JSONL conversation log. The task list is visible in the footer and through the `/tilldone` command. If leads need context about what tasks exist, they receive the full state at spawn time via `TILLDONE_TASKS`.
- **Future enhancement**: Could add a `tilldone` entry type to the conversation log so agents loading context via `active-listener` skill can see what tasks were planned and completed. Not needed for v1.

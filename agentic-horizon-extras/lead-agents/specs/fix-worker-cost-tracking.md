# Plan: Fix Worker Cost Tracking

## Task Description
Worker subprocess costs are silently dropped, causing the TUI footer to report ~25% of actual API spend. A user reported the API dashboard showing $34.28 while the TUI displayed $8.79 — the difference is the cost of all 6 worker agents (Product Manager, UX Researcher, Frontend Dev, Backend Dev, QA Engineer, Security Reviewer) across 3 teams.

## Objective
Ensure `totalCost()` in the TUI footer matches the real API spend by capturing worker costs from all three propagation layers: incremental `onToolUpdate` stats, final `onUpdate` after `callAgent` resolves, and `tool_execution_end` result details.

## Problem Statement
Worker costs propagate from `lead-delegate.ts` via `onUpdate({type: "stats", member, cost})`, which Pi emits as `tool_execution_update` events. These arrive in `multi-team-chat.ts`'s `onToolUpdate` handler. **But all processing is gated behind a `memberBubbles.get(toolCallId)` lookup (line 1294).** If the `toolCallId` doesn't match between `tool_execution_start` and `tool_execution_update` events — or if `tool_execution_start` lacked a `toolCallId` — the stats are silently dropped at `if (!entry) return;`.

Stats don't need a bubble reference. They only need the member name, which is already in `partialResult.member`. The fix decouples cost tracking from UI bubble tracking.

## Solution Approach
Three-layer defense to guarantee worker costs are always captured:

1. **Primary (onToolUpdate)**: Move stats handling BEFORE the `memberBubbles` lookup, keyed on `partialResult.member` directly — no dependency on `toolCallId` matching.
2. **Safety net (lead-delegate.ts)**: Send a guaranteed final stats `onUpdate` AFTER `callAgent()` resolves with the definitive `SubprocessResult` cost — not just the incremental `onUsage` callback during execution.
3. **Belt & suspenders (onToolEnd)**: Include member cost in the delegate tool's return `details`, and extract it in the `onToolEnd` handler by member name — completely independent of `tool_execution_update` events.

## Relevant Files
Use these files to complete the task:

- **`apps/multi-team-chat/extensions/multi-team-chat.ts`** — Main extension. Contains `onToolUpdate` handler (lines 1285-1328), `onToolEnd` handler (lines 1330-1344), `totalCost()` (line 111), `teamCost()` (lines 339-343), `agentStats` map (line 100), `addStats`/`getStats` helpers (lines 104-110). All changes are in the delegate tool's `callAgent()` callback block.
- **`apps/multi-team-chat/extensions/lead-delegate.ts`** — Lead's delegate tool. Contains `onUsage` callback (lines 136-138) that sends worker stats via `onUpdate`, and the tool return value (lines 176-179). Needs a final stats `onUpdate` after `callAgent` resolves, and cost data in the return `details`.
- **`apps/multi-team-chat/extensions/modules/subprocess.ts`** — Subprocess spawner. Contains `onUsage` accumulation (lines 121-129) and `tool_execution_update` parsing (lines 107-109). Read-only for understanding — no changes needed.
- **`apps/multi-team-chat/extensions/modules/types.ts`** — Type definitions. Contains `AgentStats`, `SubprocessResult`, `ToolUse`. Read-only — no changes needed.

## Implementation Phases
### Phase 1: Foundation — Decouple Stats from Bubble Lookup
Restructure the `onToolUpdate` handler in `multi-team-chat.ts` so stats processing uses `partialResult.member` directly, before the `memberBubbles` guard.

### Phase 2: Core Implementation — Triple-Layer Cost Capture
1. Fix `onToolUpdate` stats path (primary)
2. Add final stats `onUpdate` in `lead-delegate.ts` (safety net)
3. Add cost data to tool return `details` + extract in `onToolEnd` (belt & suspenders)

### Phase 3: Integration & Polish — Validation
Test with a trimmed single-team config via `/drive` to verify costs match across orchestrator, lead, and worker layers.

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
  - Name: cost-fix-builder
  - Role: Implement the three-layer cost tracking fix across `multi-team-chat.ts` and `lead-delegate.ts`
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: drive-validator
  - Role: Validate the fix by launching a trimmed team config via `/drive`, sending a delegation prompt, and verifying worker costs appear in the footer
  - Agent Type: general-purpose
  - Resume: true

## Step by Step Tasks

### 1. Fix onToolUpdate — Stats Before Bubble Guard
- **Task ID**: fix-ontoolupdate-stats
- **Depends On**: none
- **Assigned To**: cost-fix-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- In `apps/multi-team-chat/extensions/multi-team-chat.ts`, restructure the `onToolUpdate` callback (lines 1285-1328) inside the delegate tool's `callAgent()` call:
  - **After** the `if (toolName !== "delegate") return;` check at line 1293
  - **Before** the `const entry = memberBubbles.get(toolCallId);` lookup at line 1294
  - Insert a new stats handler block:
    ```typescript
    // Member stats — keyed by name, no bubble reference needed
    if (partialResult?.type === "stats" && partialResult.member) {
        const memberName: string = partialResult.member;
        addStats(memberName, 0, 0, 0, 0); // ensure entry
        const ms = getStats(memberName);
        ms.cost = partialResult.cost || 0;
        ms.tokensIn = partialResult.tokensIn || 0;
        ms.tokensOut = partialResult.tokensOut || 0;
        ms.contextTokens = partialResult.contextTokens || 0;
        refresh();
        return;
    }
    ```
  - **Remove** the old `else if (partialResult?.type === "stats")` block inside the `if (!entry) return;` guard (lines 1306-1314), since it's now unreachable for stats.
  - The streaming and tool-badge branches remain inside the `memberBubbles` guard since they need `entry.mId` for bubble updates.

### 2. Add Final Stats onUpdate in lead-delegate.ts
- **Task ID**: add-final-stats-update
- **Depends On**: none
- **Assigned To**: cost-fix-builder
- **Agent Type**: general-purpose
- **Parallel**: true (can run alongside task 1)
- In `apps/multi-team-chat/extensions/lead-delegate.ts`, after `callAgent()` resolves (line 159, after the try/catch), add a **guaranteed final stats update** before the "done" update:
  ```typescript
  // ── Final stats update — guaranteed delivery with definitive SubprocessResult costs
  onUpdate?.({ type: "stats", member, cost: result.cost, tokensIn: result.tokensIn, tokensOut: result.tokensOut, contextTokens: result.contextTokens } as any);
  ```
  - Place this immediately before the existing line 161: `onUpdate?.({ type: "done", member, text: result.response } as any);`
  - This is redundant with the `onUsage` callback (line 136-138) but guarantees the final cost is sent even if the incremental `onUsage` update was lost due to timing.

### 3. Include Cost in Tool Return Details
- **Task ID**: add-cost-to-details
- **Depends On**: none
- **Assigned To**: cost-fix-builder
- **Agent Type**: general-purpose
- **Parallel**: true (can run alongside tasks 1 & 2)
- In `apps/multi-team-chat/extensions/lead-delegate.ts`, modify the tool return value (lines 176-179) to include member cost data in `details`:
  ```typescript
  return {
      content: [{ type: "text", text: result.response }],
      details: {
          memberName: member,
          cost: result.cost,
          tokensIn: result.tokensIn,
          tokensOut: result.tokensOut,
          contextTokens: result.contextTokens,
      },
  };
  ```

### 4. Extract Cost from onToolEnd Result
- **Task ID**: extract-cost-ontoolend
- **Depends On**: add-cost-to-details
- **Assigned To**: cost-fix-builder
- **Agent Type**: general-purpose
- **Parallel**: false
- In `apps/multi-team-chat/extensions/multi-team-chat.ts`, modify the `onToolEnd` callback (lines 1330-1344):
  - **Before** the `const entry = memberBubbles.get(toolCallId);` lookup at line 1334
  - Insert a cost extraction block using `result.details`:
    ```typescript
    // Extract member costs from tool result (safety net — independent of tool_execution_update)
    const details = result?.details;
    if (details?.memberName && details?.cost != null) {
        addStats(details.memberName, 0, 0, 0, 0);
        const ms = getStats(details.memberName);
        // Use max() to avoid overwriting with stale data if onToolUpdate already set a higher value
        if (details.cost > ms.cost) {
            ms.cost = details.cost;
            ms.tokensIn = details.tokensIn || ms.tokensIn;
            ms.tokensOut = details.tokensOut || ms.tokensOut;
            ms.contextTokens = details.contextTokens || ms.contextTokens;
        }
        refresh();
    }
    ```
  - The existing bubble finalization logic (entry lookup, marking done) stays unchanged after this block.
  - Note: if Pi strips `details` from `tool_execution_end` events in JSON mode, this block is a no-op — the primary fix (task 1) and safety net (task 2) still cover cost capture.

### 5. Create Trimmed Test Config
- **Task ID**: create-test-config
- **Depends On**: fix-ontoolupdate-stats, add-final-stats-update, add-cost-to-details, extract-cost-ontoolend
- **Assigned To**: drive-validator
- **Agent Type**: general-purpose
- **Parallel**: false
- Create a temporary minimal team config at `.pi/multi-team/test-cost-config.yaml` with:
  - Only the Engineering team (1 lead + 1 member — Backend Dev)
  - This minimizes API spend during testing while still exercising the full Orchestrator → Lead → Worker cost propagation chain
  - Use `anthropic/claude-sonnet-4-20250514` for all agents (cheapest viable model)
  - Example:
    ```yaml
    orchestrator:
      name: Orchestrator
      path: .pi/multi-team/agents/orchestrator.md
      color: "#72f1b8"

    paths:
      agents: .pi/multi-team/agents/
      sessions: .pi/multi-team/sessions/

    shared_context:
      - README.md
      - CLAUDE.md

    teams:
      - team-name: Engineering
        team-color: "#ff6e96"
        consult-when: Architecture, implementation, code changes
        lead:
          name: Engineering Lead
          path: .pi/multi-team/agents/engineering-lead.md
          color: "#ff6e96"
        members:
          - name: Backend Dev
            path: .pi/multi-team/agents/backend-dev.md
            color: "#ff7edb"
            consult-when: APIs, databases, infrastructure
    ```

### 6. Validate with /drive
- **Task ID**: validate-with-drive
- **Depends On**: create-test-config
- **Assigned To**: drive-validator
- **Agent Type**: general-purpose
- **Parallel**: false
- Use `/drive` to test the fix end-to-end:
  1. Kill any existing tmux session: `drive session kill multi-team-test`
  2. Create a fresh tmux session: `drive session create multi-team-test`
  3. Launch the trimmed team: `drive run multi-team-test "cd apps/multi-team-chat && pi -e extensions/multi-team-chat.ts --team .pi/multi-team/test-cost-config.yaml"`
  4. Wait for Pi to boot (poll/screenshot until the editor is ready)
  5. Send a prompt that forces delegation + worker consultation: `drive send multi-team-test "Review the README.md and suggest one improvement to the architecture section. Delegate to your Engineering team and have the lead consult Backend Dev."`
  6. Poll/screenshot until the orchestrator finishes (watch for the idle ◆ diamond, not ⚡)
  7. Toggle workers visible: `drive send multi-team-test "/toggle-workers"`
  8. Screenshot the footer and verify:
     - Orch line (`totalCost()`) > sum of team costs (proves orch own cost is tracked)
     - Engineering Lead line shows `teamCost()` > 0
     - Backend Dev line shows individual cost > 0
     - `totalCost()` ≈ Orch cost + Engineering Lead cost + Backend Dev cost
  9. Kill the session: `drive session kill multi-team-test`
  10. Delete the test config: `rm .pi/multi-team/test-cost-config.yaml`

### 7. Final Validation
- **Task ID**: validate-all
- **Depends On**: validate-with-drive
- **Assigned To**: drive-validator
- **Agent Type**: general-purpose
- **Parallel**: false
- Verify no regressions:
  - Read `apps/multi-team-chat/extensions/multi-team-chat.ts` and confirm `totalCost()` and `teamCost()` functions are unchanged (they were always correct — the bug was in data propagation, not aggregation)
  - Confirm no new TypeScript errors: `cd apps/multi-team-chat && bun run tsc --noEmit 2>&1 || true` (best-effort — project may not have tsconfig)
  - Verify `lead-delegate.ts` still returns a valid tool result shape (`content` array + `details` object)
  - Confirm the three cost capture paths are in place:
    1. `onToolUpdate` stats by `partialResult.member` (before `memberBubbles` guard)
    2. Final stats `onUpdate` after `callAgent` resolves in `lead-delegate.ts`
    3. Cost extraction from `result.details` in `onToolEnd`

## Acceptance Criteria
- `totalCost()` in the TUI footer includes orchestrator + all lead + all worker costs
- `teamCost(t)` includes lead cost + all member costs for that team
- `/toggle-workers` shows individual worker costs > $0 after a delegation that consulted workers
- The footer's Orch line total approximately matches the API dashboard total for a given session
- No regressions in streaming text, tool badges, or bubble rendering for workers
- Stats are captured even when `memberBubbles.get(toolCallId)` returns null (the primary fix path)

## Validation Commands
Execute these commands to validate the task is complete:

- `cd apps/multi-team-chat && grep -n "partialResult.member" extensions/multi-team-chat.ts` — Verify the new stats-by-name handler exists in onToolUpdate
- `cd apps/multi-team-chat && grep -n "Final stats update" extensions/lead-delegate.ts` — Verify the guaranteed final stats onUpdate exists
- `cd apps/multi-team-chat && grep -n "memberName.*cost" extensions/lead-delegate.ts` — Verify cost data is in the tool return details
- `cd apps/multi-team-chat && grep -n "details?.memberName" extensions/multi-team-chat.ts` — Verify onToolEnd extracts cost from details
- `/drive` integration test per task 6 above

## Notes
- The `memberBubbles` map is still used for streaming text and tool badge rendering — those features DO require a bubble ID. Only stats tracking is decoupled from it.
- The `addStats(name, 0, 0, 0, 0)` pattern increments `calls++` each time. With the new code, worker `calls` count may be higher than before (due to redundant stats updates). This is cosmetic — `calls` is not displayed anywhere.
- If Pi strips `details` from `tool_execution_end` events in JSON mode, task 4's safety net is a no-op. The primary fix (task 1) and guaranteed final update (task 2) still cover cost capture.
- After the fix, consider removing the test config `.pi/multi-team/test-cost-config.yaml` to keep the repo clean.
- The root cause of WHY `memberBubbles.get(toolCallId)` was returning null is likely a `toolCallId` mismatch between Pi's `tool_execution_start` and `tool_execution_update` events. This fix sidesteps the issue entirely for stats, making it resilient to Pi's internal event ID handling.

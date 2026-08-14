# Owning the Pi UI — Full Chat Container Replacement

> How to replace Pi's entire chat rendering with your own custom component, without modifying Pi's source code.

**Discovered:** 2026-03-24
**Used in:** `apps/team-chat-nuclear/extensions/team-chat.ts`
**Pi version tested:** 0.61.x

---

## The Problem

Pi's extension API provides `setWidget`, `setFooter`, `setHeader`, `setEditorComponent`, and `ctx.ui.custom()` — but none of these control the **chat container**, which is where all assistant messages, user messages, tool calls, and the "Working..." spinner render. There is no `setChatContainer()`, `hideChat()`, or `replaceChat()` method in the extension API.

The official documentation and `ExtensionUIContext` type definition confirm: **there is no public API to suppress, hide, or replace the chat area.**

Every approach using the documented API — widgets, custom messages, message renderers, tool renderCall/renderResult — layers content ON TOP of or ALONGSIDE Pi's default chat rendering. You always get Pi's chrome: the assistant message markdown, the tool execution boxes with borders, the "Working..." status, the pending messages area.

---

## The Discovery

`TUI` extends `Container`. `Container.children` is a **public array**. Every factory function (`setHeader`, `setFooter`, `setWidget`, `ctx.ui.custom()`) receives the `tui` instance as its first parameter. That `tui` instance IS the root of the entire terminal UI, and its `children` array is the complete layout — directly mutable.

### The Layout

Pi's `InteractiveMode.init()` builds the TUI layout by adding children in this exact order:

```
Index   Component                   Purpose
─────   ─────────────────────────   ─────────────────────────────────
[0]     headerContainer             Session header, update notices
[1]     chatContainer               ALL messages render here (the target)
[2]     pendingMessagesContainer    Messages waiting to be processed
[3]     statusContainer             "Working..." spinner, retry indicators
[4]     widgetContainerAbove        Extension widgets (setWidget default)
[5]     editorContainer             User input editor
[6]     widgetContainerBelow        Extension widgets (setWidget belowEditor)
[7]     footer                      Status bar, model info, git branch
```

Source: `packages/coding-agent/src/modes/interactive/interactive-mode.ts`, lines ~504-511.

### The Key Insight

`tui.children` is a plain JavaScript array. You can assign to any index:

```typescript
tui.children[1] = myCustomComponent;
```

Pi's `InteractiveMode` holds its own `private chatContainer` reference internally. When the LLM responds, Pi calls `this.chatContainer.addChild(new AssistantMessageComponent(...))`. But `this.chatContainer` points to the **original** Container object — the one you just evicted from the render tree. Those components accumulate in memory on an orphaned container that the TUI never renders.

Your replacement component sits at `tui.children[1]`. The TUI calls `yourComponent.render(width)` every frame. You control what the user sees.

---

## The Takeover — Step by Step

### Step 1: Create your chat component

Your component must implement the `Component` interface: `render(width: number): string[]` and `invalidate(): void`.

```typescript
// A simple component that satisfies the interface
const EMPTY = { render: () => [] as string[], invalidate() {} };

// Your actual chat view
let chatDirty = true;
let chatCache: string[] | null = null;

const chatView = {
    render(width: number): string[] {
        if (chatCache && !chatDirty) return chatCache;

        const allLines: string[] = [];
        for (const msg of messages) {
            allLines.push(...renderBubble(msg, width));
        }

        // Bottom-align: anchor content to bottom of available space
        const rows = process.stdout.rows || 50;
        const available = Math.max(5, rows - 5); // minus footer + editor
        if (allLines.length >= available) {
            chatCache = allLines.slice(-available);
        } else {
            // Pad top with empty lines — messages grow upward from bottom
            chatCache = [...new Array(available - allLines.length).fill(""), ...allLines];
        }
        chatDirty = false;
        return chatCache;
    },
    invalidate() {
        chatDirty = true;
        chatCache = null;
    },
};
```

**Critical:** The `invalidate()` method MUST clear the cache. The TUI calls `invalidate()` when it needs fresh content. If you return stale cached data, the display won't update when new messages arrive.

### Step 2: Get the TUI reference and replace components

Use any factory function to access the `tui` instance. `setHeader` is ideal because it fires early and you want to kill the header anyway:

```typescript
let tuiRef: any = null;

pi.on("session_start", async (_event, ctx) => {
    ctx.ui.setHeader((tui: any) => {
        if (!tuiRef && tui?.children) {
            tuiRef = tui;

            // THE TAKEOVER — three assignments
            tui.children[1] = chatView;   // Replace chatContainer
            tui.children[2] = EMPTY;      // Kill pendingMessagesContainer
            tui.children[3] = EMPTY;      // Kill statusContainer
        }
        return EMPTY; // Header renders nothing
    });
});
```

After these three assignments:
- `tui.children[1]` → your `chatView` (renders your chat bubbles)
- `tui.children[2]` → `EMPTY` (no pending messages noise)
- `tui.children[3]` → `EMPTY` (no "Working..." spinner)
- `tui.children[0]` → `EMPTY` (header returns nothing)

Pi's editor (`tui.children[5]`) and your custom footer (`tui.children[7]`) remain functional.

### Step 3: Trigger re-renders

When your chat state changes (new message, streaming update), clear the cache and tell the TUI to re-render:

```typescript
function refresh() {
    chatDirty = true;
    chatCache = null;
    try { tuiRef?.requestRender?.(); } catch {}
}
```

Call `refresh()` after every `addMsg()` or `updateMsg()` call.

### Step 4: Intercept user input

Pi normally renders user messages in its chatContainer. Since that container is orphaned, the messages would accumulate invisibly. But you should also prevent Pi from processing the input through its normal rendering path:

```typescript
pi.on("input", async (event) => {
    if ((event as any).source === "extension") return { action: "continue" };
    const text = event.text?.trim();
    if (!text) return { action: "handled" };

    // Render in YOUR chat
    addMsg("You", "#4a90d9", text, "user");
    refresh();

    // Forward to the agent — triggers LLM turn
    pi.sendUserMessage(text);

    // Block Pi from rendering the user message in its (orphaned) chat
    return { action: "handled" };
});
```

The `{ action: "handled" }` return tells Pi "I dealt with this input, don't process it further." But `pi.sendUserMessage(text)` separately triggers the agent to respond. The agent's response goes to the orphaned chatContainer (invisible), while you capture it via `message_update` events and render it in your chatView.

### Step 5: Capture orchestrator streaming

The orchestrator's response streams via `message_update` events. Capture the deltas and render them in your chat:

```typescript
let orchId = -1, orchText = "";

pi.on("agent_start", async () => {
    orchText = "";
    // Find the thinking bubble we created in the input handler
    for (let i = msgs.length - 1; i >= 0; i--) {
        if (msgs[i].state === "thinking") { orchId = msgs[i].id; break; }
    }
});

pi.on("message_update", async (event) => {
    const ame = (event as any).assistantMessageEvent;
    if (ame?.type === "text_delta" && (ame.delta || ame.text)) {
        orchText += ame.delta || ame.text;
        if (orchId >= 0) {
            updateMsg(orchId, { text: orchText, state: "streaming" });
            refresh();
        }
    }
});

pi.on("agent_end", async () => {
    if (orchId >= 0) updateMsg(orchId, { text: orchText, state: "done" });
    orchId = -1; orchText = "";
    refresh();
});
```

### Step 6: Handle tool calls (message ordering)

When the orchestrator calls a tool (like `delegate`), it outputs text BEFORE the tool call, then more text AFTER. In a chat UI, the post-tool text should appear as a NEW bubble at the bottom, not update the old bubble in-place. Use the `tool_call` event to detect this:

```typescript
let orchToolCalled = false;

pi.on("tool_call", async () => {
    // Finalize current orchestrator bubble
    if (orchId >= 0 && orchText.trim()) {
        updateMsg(orchId, { state: "done" });
    }
    orchToolCalled = true;
    orchText = "";
});

pi.on("message_update", async (event) => {
    const ame = (event as any).assistantMessageEvent;
    if (ame?.type === "text_delta" && (ame.delta || ame.text)) {
        const delta = ame.delta || ame.text;

        // If tool was called, create NEW bubble at bottom
        if (orchToolCalled && orchId >= 0) {
            updateMsg(orchId, { state: "done" });
            orchText = delta;
            orchId = addMsg("Orchestrator", "#72f1b8", delta, "orchestrator", "streaming");
            orchToolCalled = false;
            refresh();
            return;
        }

        orchText += delta;
        if (orchId >= 0) { updateMsg(orchId, { text: orchText, state: "streaming" }); refresh(); }
    }
});
```

This ensures the conversation flows chronologically: Orchestrator routing → team responses → Orchestrator synthesis (as a new bubble at the bottom).

---

## What Pi Still Controls

After the takeover, Pi still manages:

| Component | Status |
|-----------|--------|
| **Editor** (`tui.children[5]`) | Fully functional — user types here |
| **Agent loop** | Untouched — LLM calls, tool execution, compaction all work |
| **Tool execution** | Your registered tools run normally |
| **Session management** | Sessions, forking, navigation all work |
| **Extension events** | All events fire normally |

You've only replaced the DISPLAY layer. Pi's brain is intact.

## What Goes to the Orphaned Container

Pi's `InteractiveMode` still holds its private `this.chatContainer` reference. These operations write to the orphaned (invisible) container:

- `AssistantMessageComponent` for every LLM response
- `UserMessageComponent` for user messages (if not intercepted with `handled`)
- `ToolExecutionComponent` for every tool call
- `CustomMessageComponent` for `pi.sendMessage()` calls
- `SkillInvocationMessage` for skill expansions
- `CompactionSummaryMessage` on compaction
- `BranchSummaryMessage` on session switches

None of these render. They accumulate in memory on the orphaned container. This is a small memory leak over very long sessions. For typical multi-team chat sessions (minutes to an hour), it's negligible.

## What Could Break

### Index fragility

The child index `[1]` depends on the order established in `InteractiveMode.init()`. If a Pi update inserts a new component before the chatContainer, the index shifts. A more robust approach would be to identify the chatContainer by iterating children and checking properties, but there's no `id` or `name` field on Container — identification would rely on heuristics (e.g., the second child, or the largest child).

**Mitigation:** Pin your Pi version in production. Test after every Pi update. The layout order has been stable across v0.57–v0.62.

### Session operations

`newSession`, `fork`, and `navigateTree` call `this.chatContainer.clear()` on the ORIGINAL reference. This clears the orphaned container (irrelevant). They also call `rebuildChatFromMessages()` which adds new components to the orphaned container (also irrelevant). Your chatView is unaffected.

However, these operations reset conversational state. If your extension tracks chat messages in its own array, you need to clear that array on session change.

### Compaction

Auto-compaction calls `this.chatContainer.clear()` and rebuilds. Same as above — affects the orphaned container only. Your chatView persists.

### The `setHeader` factory re-invocation

Pi may call the `setHeader` factory multiple times (on theme change, on session switch). The `if (!tuiRef)` guard ensures the takeover only happens once. If you need to re-takeover after a session switch, remove the guard and always reassign.

---

## The Bottom-Alignment Pattern

Chat apps anchor content to the bottom — new messages appear at the bottom, old messages scroll up. In a terminal, there's no CSS `flex-end`. You achieve this by padding the top of your render output with empty lines:

```typescript
render(width: number): string[] {
    const allLines = buildChatContent(width);
    const available = process.stdout.rows - 5;

    if (allLines.length >= available) {
        // More content than screen — show the tail
        return allLines.slice(-available);
    }

    // Less content — pad top so content sticks to bottom
    const padding = new Array(available - allLines.length).fill("");
    return [...padding, ...allLines];
}
```

`process.stdout.rows` gives the terminal height. Subtract footer lines and editor lines to get the available chat height. When there are fewer messages than available height, empty lines fill the top. As messages accumulate, the padding shrinks. Eventually, messages fill the screen and you show only the tail (newest at bottom, oldest scrolled off top).

This is NOT the same as the padding hack from Strategy B (which filled a widget to push Pi's chatContainer off-screen). Here, the chatContainer IS your component — the padding is just for bottom-alignment within your own content.

---

## Complete Architecture Diagram

```
BEFORE (default Pi):

┌─ TUI ───────────────────────────────────┐
│ [0] headerContainer    ← Pi header      │
│ [1] chatContainer      ← Pi messages    │  ← ALL rendering here
│ [2] pendingMessages    ← queued msgs    │
│ [3] statusContainer    ← "Working..."   │
│ [4] widgetAbove        ← ext widgets    │
│ [5] editorContainer    ← user input     │
│ [6] widgetBelow        ← ext widgets    │
│ [7] footer             ← status bar     │
└─────────────────────────────────────────┘

AFTER (takeover):

┌─ TUI ───────────────────────────────────┐
│ [0] EMPTY              ← hidden         │
│ [1] chatView           ← YOUR component │  ← ALL rendering here
│ [2] EMPTY              ← hidden         │
│ [3] EMPTY              ← hidden         │
│ [4] widgetAbove        ← unused         │
│ [5] editorContainer    ← user input     │  ← Pi's editor, untouched
│ [6] widgetBelow        ← unused         │
│ [7] custom footer      ← YOUR footer    │
└─────────────────────────────────────────┘

Pi's orphaned chatContainer (in memory, never rendered):
  └─ AssistantMessageComponent (invisible)
  └─ ToolExecutionComponent (invisible)
  └─ AssistantMessageComponent (invisible)
  └─ ... accumulates but never displays
```

---

## Reference Implementation

See `apps/team-chat-nuclear/extensions/team-chat.ts` for a complete working implementation that uses this technique to build a Slack-like multi-team chat UI with:

- Colored avatar bubbles with initials, names, timestamps, and accent bars
- Live streaming from multiple agents (orchestrator, team leads, team members)
- Bottom-aligned chat that grows upward
- Tool-call detection for correct message ordering
- Hierarchical footer with per-agent cost/token tracking
- Invisible tool chrome (renderCall/renderResult return empty Text)
- Full input interception with agent forwarding

The entire takeover is **three array assignments** in a `setHeader` factory callback. Everything else is your custom rendering logic.

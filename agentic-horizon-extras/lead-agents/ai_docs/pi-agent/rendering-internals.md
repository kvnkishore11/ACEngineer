# Pi Coding Agent: Rendering Internals Reference

> Source repository: `github.com/badlogic/pi-mono`
> Primary package: `packages/coding-agent`
> Last verified against: `main` branch, March 2026

This document provides a comprehensive, low-level reference for how the Pi coding agent renders messages, tool executions, and custom UI elements in interactive (TUI) mode. It is intended for extension authors building custom chat interfaces on top of Pi.

---

## Table of Contents

1. [Interactive Mode Architecture](#1-interactive-mode-architecture)
2. [Assistant Message Rendering](#2-assistant-message-rendering)
3. [Custom Message Rendering](#3-custom-message-rendering)
4. [Tool Execution Rendering](#4-tool-execution-rendering)
5. [Extension API Surface for UI Control](#5-extension-api-surface-for-ui-control)
6. [What Cannot Be Overridden](#6-what-cannot-be-overridden)
7. [Strategy Patterns for Custom Chat UIs](#7-strategy-patterns-for-custom-chat-uis)

---

## 1. Interactive Mode Architecture

**Source file:** `packages/coding-agent/src/modes/interactive/interactive-mode.ts` (~4647 lines)

### 1.1 The InteractiveMode Class

`InteractiveMode` is the central class that manages the entire TUI display. It is instantiated with an `AgentSession` and creates a `TUI` instance (from `@mariozechner/pi-tui`) which serves as the root rendering surface. The class owns:

- The TUI rendering loop
- The layout hierarchy of containers
- Event subscription to the agent session
- All extension UI context (widgets, footers, headers, etc.)

Key constructor logic:

```typescript
export class InteractiveMode {
    private session: AgentSession;
    private ui: TUI;
    private chatContainer: Container;
    private pendingMessagesContainer: Container;
    private statusContainer: Container;
    private defaultEditor: CustomEditor;
    private editor: EditorComponent;
    private editorContainer: Container;
    private footer: FooterComponent;
    private headerContainer: Container;
    private widgetContainerAbove: Container;
    private widgetContainerBelow: Container;
    // ... many more private fields

    constructor(session: AgentSession, options: InteractiveModeOptions = {}) {
        this.ui = new TUI(new ProcessTerminal(), ...);
        this.headerContainer = new Container();
        this.chatContainer = new Container();
        this.pendingMessagesContainer = new Container();
        this.statusContainer = new Container();
        this.widgetContainerAbove = new Container();
        this.widgetContainerBelow = new Container();
        // ...
    }
}
```

### 1.2 Layout Hierarchy (Top to Bottom)

During `init()`, children are added to the TUI in this exact order, which determines the vertical layout from top to bottom:

```
ui (TUI root)
  |-- headerContainer          (Container)
  |     |-- Spacer(1)
  |     |-- builtInHeader      (Text: logo + keybinding hints) -OR- customHeader
  |     |-- Spacer(1)
  |     |-- [changelog if applicable]
  |
  |-- chatContainer            (Container) -- all messages go here
  |
  |-- pendingMessagesContainer (Container) -- queued/pending messages
  |
  |-- statusContainer          (Container) -- loading animation, compaction status
  |
  |-- widgetContainerAbove     (Container) -- extension widgets (placement: "aboveEditor")
  |
  |-- editorContainer          (Container) -- wraps the editor component
  |     |-- editor             (CustomEditor or extension EditorComponent)
  |
  |-- widgetContainerBelow     (Container) -- extension widgets (placement: "belowEditor")
  |
  |-- footer                   (FooterComponent) -OR- customFooter
```

The layout is established in `init()` around line 520-530:

```typescript
this.ui.addChild(this.headerContainer);
this.ui.addChild(this.chatContainer);
this.ui.addChild(this.pendingMessagesContainer);
this.ui.addChild(this.statusContainer);
this.renderWidgets(); // Initialize with default spacer
this.ui.addChild(this.widgetContainerAbove);
this.ui.addChild(this.editorContainer);
this.ui.addChild(this.widgetContainerBelow);
this.ui.addChild(this.footer);
this.ui.setFocus(this.editor);
```

### 1.3 How Messages Are Added to the Chat

All messages flow through the `addMessageToChat()` method (~line 2533). This method is a switch on the message's `role` field:

```typescript
private addMessageToChat(message: AgentMessage, options?: { populateHistory?: boolean }): void {
    switch (message.role) {
        case "bashExecution": {
            const component = new BashExecutionComponent(message.command, this.ui, message.excludeFromContext);
            // ... set output, completion state
            this.chatContainer.addChild(component);
            break;
        }
        case "custom": {
            if (message.display) {
                const renderer = this.session.extensionRunner?.getMessageRenderer(message.customType);
                const component = new CustomMessageComponent(message, renderer, this.getMarkdownThemeWithSettings());
                component.setExpanded(this.toolOutputExpanded);
                this.chatContainer.addChild(component);
            }
            break;
        }
        case "compactionSummary": { /* CompactionSummaryMessageComponent */ }
        case "branchSummary":     { /* BranchSummaryMessageComponent */ }
        case "user": {
            // UserMessageComponent or SkillInvocationMessageComponent
            break;
        }
        case "assistant": {
            const assistantComponent = new AssistantMessageComponent(
                message, this.hideThinkingBlock, this.getMarkdownThemeWithSettings()
            );
            this.chatContainer.addChild(assistantComponent);
            break;
        }
        case "toolResult": {
            // Tool results are rendered inline with tool calls, handled separately
            break;
        }
    }
}
```

Critical detail: `toolResult` messages are **not** rendered by `addMessageToChat()` -- they are matched to their corresponding `ToolExecutionComponent` instances via `toolCallId` in `renderSessionContext()`.

### 1.4 The Event Subscription Pipeline

`subscribeToAgent()` (~line 2199) subscribes to `AgentSessionEvent` via `this.session.subscribe()`. The `handleEvent()` method processes events in a large switch statement. The key rendering events are:

| Event | What Happens |
|-------|-------------|
| `agent_start` | Clears status, shows loading spinner |
| `message_start` (assistant) | Creates new `AssistantMessageComponent`, adds to chatContainer |
| `message_start` (user) | Calls `addMessageToChat()` for user message |
| `message_start` (custom) | Calls `addMessageToChat()` for custom message |
| `message_update` | Updates streaming `AssistantMessageComponent`, creates `ToolExecutionComponent` for new tool calls |
| `message_end` | Finalizes streaming component, handles abort/error states |
| `tool_execution_start` | Creates or updates `ToolExecutionComponent`, marks execution started |
| `tool_execution_update` | Calls `component.updateResult()` with `isPartial=true` |
| `tool_execution_end` | Calls `component.updateResult()` with final result, removes from pending map |
| `agent_end` | Stops loading animation, clears status |

### 1.5 Streaming Message Tracking

The class maintains streaming state via two fields:

```typescript
private streamingComponent: AssistantMessageComponent | undefined = undefined;
private streamingMessage: AssistantMessage | undefined = undefined;
```

And tool execution tracking via a Map:

```typescript
private pendingTools = new Map<string, ToolExecutionComponent>();
```

When `message_update` fires, the streaming component's `updateContent()` is called with the latest `AssistantMessage`. For each `toolCall` content block, if a `ToolExecutionComponent` does not yet exist for that `toolCallId`, one is created and added to `chatContainer`.

### 1.6 Initial Message Rendering

When the session is loaded (or after compaction/fork), `renderInitialMessages()` (~line 2691) rebuilds the chat from the session's persisted state:

```typescript
renderInitialMessages(): void {
    const context = this.sessionManager.buildSessionContext();
    this.renderSessionContext(context, {
        updateFooter: true,
        populateHistory: true,
    });
}
```

`renderSessionContext()` (~line 2639) iterates all messages, calling `addMessageToChat()` for each. Assistant messages get special handling: after the assistant message component is added, each `toolCall` content block gets its own `ToolExecutionComponent`, and subsequent `toolResult` messages are matched by `toolCallId` to update them.

---

## 2. Assistant Message Rendering

**Source file:** `packages/coding-agent/src/modes/interactive/components/assistant-message.ts`

### 2.1 Class Structure

```typescript
export class AssistantMessageComponent extends Container {
    private contentContainer: Container;
    private hideThinkingBlock: boolean;
    private markdownTheme: MarkdownTheme;
    private lastMessage?: AssistantMessage;

    constructor(
        message?: AssistantMessage,
        hideThinkingBlock = false,
        markdownTheme: MarkdownTheme = getMarkdownTheme(),
    ) {
        super();
        this.hideThinkingBlock = hideThinkingBlock;
        this.markdownTheme = markdownTheme;
        this.contentContainer = new Container();
        this.addChild(this.contentContainer);
        if (message) {
            this.updateContent(message);
        }
    }
}
```

`AssistantMessageComponent` extends `Container` (from `pi-tui`). It contains a single `contentContainer` child that holds the rendered content blocks.

### 2.2 The updateContent() Method

This is the core rendering method. It is called:
- Once at construction (if a message is passed)
- On every `message_update` event during streaming
- On `message_end` to finalize
- On `invalidate()` (e.g., when terminal is resized)

The method:

1. Clears the content container
2. Iterates over `message.content[]` blocks in order
3. For each `text` block: renders a `Markdown` component with the content
4. For each `thinking` block: renders either a collapsed "Thinking..." label or the full thinking trace in italic with `thinkingText` color
5. Handles `aborted` and `error` stop reasons by appending error text

```typescript
updateContent(message: AssistantMessage): void {
    this.lastMessage = message;
    this.contentContainer.clear();

    // ... check hasVisibleContent, add Spacer(1)

    for (let i = 0; i < message.content.length; i++) {
        const content = message.content[i];
        if (content.type === "text" && content.text.trim()) {
            this.contentContainer.addChild(
                new Markdown(content.text.trim(), 1, 0, this.markdownTheme)
            );
        } else if (content.type === "thinking" && content.thinking.trim()) {
            if (this.hideThinkingBlock) {
                this.contentContainer.addChild(
                    new Text(theme.italic(theme.fg("thinkingText", "Thinking...")), 1, 0)
                );
            } else {
                this.contentContainer.addChild(
                    new Markdown(content.thinking.trim(), 1, 0, this.markdownTheme, {
                        color: (text: string) => theme.fg("thinkingText", text),
                        italic: true,
                    })
                );
            }
        }
    }

    // Handle abort/error (only if no tool calls present)
    const hasToolCalls = message.content.some((c) => c.type === "toolCall");
    if (!hasToolCalls) {
        if (message.stopReason === "aborted") {
            // ... render abort message
        } else if (message.stopReason === "error") {
            // ... render error message
        }
    }
}
```

### 2.3 Content Block Types

The `AssistantMessage.content` array contains blocks of type:
- `"text"` -- rendered as Markdown
- `"thinking"` -- rendered as italic Markdown or collapsed label
- `"toolCall"` -- **not rendered by AssistantMessageComponent** (handled separately as `ToolExecutionComponent`)

This means `AssistantMessageComponent` only renders the text and thinking portions of assistant responses. Tool calls are rendered as separate components added directly to `chatContainer`.

### 2.4 Streaming Updates

During streaming:
1. `message_start` (assistant): A new `AssistantMessageComponent` is created with no initial message and added to `chatContainer`.
2. `message_update`: `streamingComponent.updateContent(event.message)` is called. Each call clears and rebuilds the content container from scratch.
3. `message_end`: Final `updateContent()` call, then `streamingComponent` is set to `undefined`.

This means the entire assistant message is re-rendered on every streaming update. There is no incremental append -- it's a full clear-and-rebuild each time.

### 2.5 Why There Is No Hook to Override Assistant Message Rendering

The assistant message rendering pipeline is hardcoded in two places:

1. **In `handleEvent()` for `message_start`:** The component is instantiated directly:
   ```typescript
   this.streamingComponent = new AssistantMessageComponent(
       undefined, this.hideThinkingBlock, this.getMarkdownThemeWithSettings()
   );
   ```

2. **In `addMessageToChat()` for history replay:**
   ```typescript
   case "assistant": {
       const assistantComponent = new AssistantMessageComponent(
           message, this.hideThinkingBlock, this.getMarkdownThemeWithSettings()
       );
       this.chatContainer.addChild(assistantComponent);
       break;
   }
   ```

There is no `extensionRunner.getAssistantRenderer()` call, no hook point, no configuration. The `AssistantMessageComponent` is always used. This is a fundamental constraint of the architecture.

---

## 3. Custom Message Rendering

**Source files:**
- `packages/coding-agent/src/modes/interactive/components/custom-message.ts`
- `packages/coding-agent/src/core/extensions/types.ts` (MessageRenderer type)
- `packages/coding-agent/src/core/extensions/runner.ts` (getMessageRenderer)
- `packages/coding-agent/src/core/messages.ts` (CustomMessage type)

### 3.1 The Full Pipeline

```
Extension calls pi.sendMessage({ customType, content, display, details })
    |
    v
Runtime.sendMessage() -> AgentSession stores message
    |
    v
AgentSession fires "message_start" event with { role: "custom", ... }
    |
    v
InteractiveMode.handleEvent("message_start") calls addMessageToChat()
    |
    v
addMessageToChat() case "custom":
    |-- Checks message.display (skips if false)
    |-- Calls extensionRunner.getMessageRenderer(message.customType)
    |-- Creates new CustomMessageComponent(message, renderer)
    |-- Adds to chatContainer
```

### 3.2 The CustomMessage Type

Defined in `packages/coding-agent/src/core/messages.ts`:

```typescript
export interface CustomMessage<T = unknown> {
    role: "custom";
    customType: string;            // Your custom type key, e.g. "team-response"
    content: string | (TextContent | ImageContent)[];  // Text or structured content
    display: boolean;              // If false, message is in context but not rendered
    details?: T;                   // Arbitrary typed payload for rendering
    timestamp: number;
}
```

When `display` is `false`, the message is still added to the LLM conversation context (converted to a user message by `convertToLlm()`), but no UI component is created.

### 3.3 Sending Custom Messages

From an extension:

```typescript
pi.sendMessage<T = unknown>(
    message: Pick<CustomMessage<T>, "customType" | "content" | "display" | "details">,
    options?: {
        triggerTurn?: boolean;                            // Default: false
        deliverAs?: "steer" | "followUp" | "nextTurn";   // Delivery mode
    },
): void;
```

- `triggerTurn: true` causes the agent to start a new response turn after the message is added.
- `deliverAs: "steer"` injects the message into the current turn's context.
- `deliverAs: "followUp"` queues the message for after the current turn.
- `deliverAs: "nextTurn"` defers until the next user-initiated turn.

### 3.4 Registering a Custom Renderer

```typescript
pi.registerMessageRenderer<T = unknown>(customType: string, renderer: MessageRenderer<T>): void;
```

The renderer is stored in the `Extension.messageRenderers` map:

```typescript
// In Extension interface (types.ts line ~1422):
export interface Extension {
    path: string;
    resolvedPath: string;
    sourceInfo: SourceInfo;
    handlers: Map<string, HandlerFn[]>;
    tools: Map<string, RegisteredTool>;
    messageRenderers: Map<string, MessageRenderer>;   // <-- stored here
    commands: Map<string, RegisteredCommand>;
    flags: Map<string, ExtensionFlag>;
    shortcuts: Map<KeyId, ExtensionShortcut>;
}
```

### 3.5 The MessageRenderer Type Signature

Defined in `types.ts` (~line 952):

```typescript
export interface MessageRenderOptions {
    expanded: boolean;
}

export type MessageRenderer<T = unknown> = (
    message: CustomMessage<T>,
    options: MessageRenderOptions,
    theme: Theme,
) => Component | undefined;
```

Parameters:
- `message`: The full `CustomMessage` object including `customType`, `content`, `details`, etc.
- `options.expanded`: Whether the user has toggled tool output expansion (Ctrl+E). This is a global toggle, not per-message.
- `theme`: The current `Theme` instance for accessing colors.

Return value:
- A `Component` (from `pi-tui`) that will be rendered. Returning `undefined` falls through to default rendering.

### 3.6 How the Renderer Is Resolved

In `ExtensionRunner.getMessageRenderer()` (~line 461 of runner.ts):

```typescript
getMessageRenderer(customType: string): MessageRenderer | undefined {
    for (const ext of this.extensions) {
        const renderer = ext.messageRenderers.get(customType);
        if (renderer) {
            return renderer;
        }
    }
    return undefined;
}
```

Extensions are iterated in load order. The first extension that has a renderer for the given `customType` wins. There is no composition or chaining.

### 3.7 The CustomMessageComponent

**Source file:** `packages/coding-agent/src/modes/interactive/components/custom-message.ts`

```typescript
export class CustomMessageComponent extends Container {
    private message: CustomMessage<unknown>;
    private customRenderer?: MessageRenderer;
    private box: Box;
    private customComponent?: Component;
    private markdownTheme: MarkdownTheme;
    private _expanded = false;

    constructor(
        message: CustomMessage<unknown>,
        customRenderer?: MessageRenderer,
        markdownTheme: MarkdownTheme = getMarkdownTheme(),
    ) {
        super();
        this.message = message;
        this.customRenderer = customRenderer;
        this.markdownTheme = markdownTheme;
        this.addChild(new Spacer(1));
        this.box = new Box(1, 1, (t) => theme.bg("customMessageBg", t));
        this.rebuild();
    }
}
```

The `rebuild()` method is where rendering decisions happen:

```typescript
private rebuild(): void {
    // Remove previous custom component if any
    if (this.customComponent) {
        this.removeChild(this.customComponent);
        this.customComponent = undefined;
    }
    this.removeChild(this.box);

    // Try custom renderer first - it handles its own styling
    if (this.customRenderer) {
        try {
            const component = this.customRenderer(this.message, { expanded: this._expanded }, theme);
            if (component) {
                this.customComponent = component;
                this.addChild(component);
                return;  // <-- Custom renderer succeeded, skip default
            }
        } catch {
            // Fall through to default rendering
        }
    }

    // Default rendering uses our box with customMessageBg background
    this.addChild(this.box);
    this.box.clear();
    const label = theme.fg("customMessageLabel", `\x1b[1m[${this.message.customType}]\x1b[22m`);
    this.box.addChild(new Text(label, 0, 0));
    this.box.addChild(new Spacer(1));
    // ... extract text content, render as Markdown with customMessageText color
}
```

Critical behavior:
- **If a custom renderer is provided and returns a `Component`:** That component is added directly. The default Box is NOT used. The custom renderer has full control over styling.
- **If no renderer or renderer returns `undefined`:** Default rendering kicks in -- a `Box` with `customMessageBg` background, showing `[customType]` label and content as Markdown.
- **On `setExpanded()`:** The component is rebuilt, passing the new `expanded` value to the renderer.

### 3.8 The `expanded` Option

The `expanded` boolean comes from the global `toolOutputExpanded` state in `InteractiveMode`. When the user presses the expand keybinding (Ctrl+E), `setToolsExpanded()` iterates all children of `chatContainer` and calls `setExpanded()` on any component that implements the `Expandable` interface:

```typescript
private setToolsExpanded(expanded: boolean): void {
    this.toolOutputExpanded = expanded;
    for (const child of this.chatContainer.children) {
        if (isExpandable(child)) {
            child.setExpanded(expanded);
        }
    }
    this.ui.requestRender();
}
```

`CustomMessageComponent` implements `Expandable` via its `setExpanded()` method.

### 3.9 Example: Complete Custom Renderer

From `packages/coding-agent/examples/extensions/message-renderer.ts`:

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Box, Text } from "@mariozechner/pi-tui";

export default function (pi: ExtensionAPI) {
    pi.registerMessageRenderer("status-update", (message, { expanded }, theme) => {
        const details = message.details as { level: string; timestamp: number } | undefined;
        const level = details?.level ?? "info";
        const color = level === "error" ? "error" : level === "warn" ? "warning" : "success";
        const prefix = theme.fg(color, `[${level.toUpperCase()}]`);

        let text = `${prefix} ${message.content}`;
        if (expanded && details?.timestamp) {
            const time = new Date(details.timestamp).toLocaleTimeString();
            text += `\n${theme.fg("dim", ` at ${time}`)}`;
        }

        const box = new Box(1, 1, (t) => theme.bg("customMessageBg", t));
        box.addChild(new Text(text, 0, 0));
        return box;
    });

    pi.registerCommand("status", {
        description: "Send a status message",
        handler: async (args, _ctx) => {
            const parts = args.trim().split(/\s+/);
            let level = "info";
            let content = args.trim();
            if (parts[0] === "warn" || parts[0] === "error") {
                level = parts[0];
                content = parts.slice(1).join(" ") || "Status update";
            }
            pi.sendMessage({
                customType: "status-update",
                content,
                display: true,
                details: { level, timestamp: Date.now() },
            });
        },
    });
}
```

---

## 4. Tool Execution Rendering

**Source file:** `packages/coding-agent/src/modes/interactive/components/tool-execution.ts`

### 4.1 Class Structure

```typescript
export class ToolExecutionComponent extends Container {
    private contentBox: Box;
    private contentText: Text;
    private callRendererComponent?: Component;
    private resultRendererComponent?: Component;
    private rendererState: any = {};
    private imageComponents: Image[] = [];
    private imageSpacers: Spacer[] = [];
    private toolName: string;
    private toolCallId: string;
    private args: any;
    private expanded = false;
    private showImages: boolean;
    private isPartial = true;
    private toolDefinition?: ToolDefinition<any, any>;
    private builtInToolDefinition?: ToolDefinition<any, any>;
    private ui: TUI;
    private cwd: string;
    private executionStarted = false;
    private argsComplete = false;
    private result?: { content: Array<{...}>; isError: boolean; details?: any };
    private convertedImages: Map<number, { data: string; mimeType: string }> = new Map();
    private hideComponent = false;
    // ...
}
```

### 4.2 Construction and Initial State

```typescript
constructor(
    toolName: string,
    toolCallId: string,
    args: any,
    options: ToolExecutionOptions = {},
    toolDefinition: ToolDefinition<any, any> | undefined,
    ui: TUI,
    cwd: string = process.cwd(),
) {
    super();
    this.toolName = toolName;
    this.toolCallId = toolCallId;
    this.args = args;
    this.toolDefinition = toolDefinition;       // Extension-provided definition
    this.builtInToolDefinition = allToolDefinitions[toolName as keyof typeof allToolDefinitions];
    this.showImages = options.showImages ?? true;
    this.ui = ui;
    this.cwd = cwd;

    this.addChild(new Spacer(1));

    this.contentBox = new Box(1, 1, (text: string) => theme.bg("toolPendingBg", text));
    this.contentText = new Text("", 1, 1, (text: string) => theme.bg("toolPendingBg", text));

    if (this.hasRendererDefinition()) {
        this.addChild(this.contentBox);
    } else {
        this.addChild(this.contentText);
    }

    this.updateDisplay();
}
```

Two rendering paths:
- **If a tool definition exists (custom or built-in):** Uses `contentBox` (a `Box` component) and renders via `renderCall`/`renderResult` functions.
- **If no definition at all:** Uses `contentText` (a `Text` component) with a generic JSON dump.

### 4.3 The Box Wrapper

Tool executions are **always** wrapped in a `Box` component (when a definition exists). The `Box` background changes based on state:

```typescript
private updateDisplay(): void {
    const bgFn = this.isPartial
        ? (text: string) => theme.bg("toolPendingBg", text)       // Yellow-ish during execution
        : this.result?.isError
            ? (text: string) => theme.bg("toolErrorBg", text)     // Red on error
            : (text: string) => theme.bg("toolSuccessBg", text);  // Green on success

    if (this.hasRendererDefinition()) {
        this.contentBox.setBgFn(bgFn);
        this.contentBox.clear();
        // ... render call and result into contentBox
    } else {
        this.contentText.setCustomBgFn(bgFn);
        this.contentText.setText(this.formatToolExecution());
    }
}
```

The three background colors (`toolPendingBg`, `toolSuccessBg`, `toolErrorBg`) are theme-defined and cannot be removed by extensions. The `Box` wrapper is always present.

### 4.4 Renderer Resolution: Custom Over Built-In

The component maintains two definition references:
- `toolDefinition`: The definition provided by extensions (via `registerTool`)
- `builtInToolDefinition`: The built-in definition looked up from `allToolDefinitions`

The resolution priority for `renderCall`:

```typescript
private getCallRenderer(): ToolDefinition<any, any>["renderCall"] | undefined {
    // 1. If no built-in exists, use custom definition's renderer
    if (!this.builtInToolDefinition) {
        return this.toolDefinition?.renderCall;
    }
    // 2. If no custom def, or custom IS the built-in, use built-in renderer
    if (!this.toolDefinition || this.isBuiltInDefinition(this.toolDefinition)) {
        return this.builtInToolDefinition.renderCall;
    }
    // 3. Custom def exists and is different: prefer custom, fall back to built-in
    return this.toolDefinition.renderCall ?? this.builtInToolDefinition.renderCall;
}
```

The same logic applies to `getResultRenderer()`. In summary:

| Has Custom Def | Custom has `renderCall` | Has Built-in | Result |
|---|---|---|---|
| No | N/A | Yes | Built-in renderer |
| No | N/A | No | Generic fallback (tool name as text) |
| Yes | Yes | Yes | Custom renderer |
| Yes | No | Yes | Built-in renderer |
| Yes | Yes | No | Custom renderer |
| Yes | No | No | Generic fallback |

### 4.5 The ToolRenderContext

Both `renderCall` and `renderResult` receive a `ToolRenderContext`:

```typescript
export interface ToolRenderContext<TState = any, TArgs = any> {
    args: TArgs;                    // Current tool call arguments
    toolCallId: string;             // Unique ID for this tool execution
    invalidate: () => void;         // Trigger re-render of just this component
    lastComponent: Component | undefined;  // Previously returned component (for reuse)
    state: TState;                  // Shared mutable state across call/result renders
    cwd: string;                    // Working directory
    executionStarted: boolean;      // Whether execute() has begun
    argsComplete: boolean;          // Whether args are final (not still streaming)
    isPartial: boolean;             // Whether result is partial/streaming
    expanded: boolean;              // Whether user has toggled expansion
    showImages: boolean;            // Whether images should be shown
    isError: boolean;               // Whether the result is an error
}
```

Key patterns:
- `state` is initialized as `{}` and shared across all renders for the same tool execution. Use it for computed data (e.g., parsed diffs).
- `lastComponent` allows reuse of the previously created component instead of creating a new one each render cycle.
- `invalidate()` triggers a re-render of just this component. Call it for async updates (e.g., after computing a diff).

### 4.6 The renderCall Signature

```typescript
renderCall?: (
    args: Static<TParams>,
    theme: Theme,
    context: ToolRenderContext<TState, Static<TParams>>
) => Component;
```

Called during `updateDisplay()` to render the "what is being called" portion. Returns a `Component` that is added to the `contentBox`.

### 4.7 The renderResult Signature

```typescript
renderResult?: (
    result: AgentToolResult<TDetails>,
    options: ToolRenderResultOptions,
    theme: Theme,
    context: ToolRenderContext<TState, Static<TParams>>,
) => Component;
```

Where `ToolRenderResultOptions` is:

```typescript
export interface ToolRenderResultOptions {
    expanded: boolean;
    isPartial: boolean;
}
```

Called when a result (partial or final) is available. The returned `Component` is added below the call component inside the same `contentBox`.

### 4.8 The `isPartial` and `expanded` Options

- **`isPartial`**: `true` during streaming tool execution (before final result). Set to `false` when `tool_execution_end` fires. Affects the Box background color (pending vs success/error).
- **`expanded`**: Controlled by global tool expansion toggle. Allows renderers to show collapsed vs detailed views.

### 4.9 How `onUpdate` Triggers Re-Renders

During tool execution, the tool's `execute()` function can call `onUpdate()` to stream partial results. This triggers the event pipeline:

```
Tool execute() calls onUpdate(partialResult)
    |
    v
AgentSession fires "tool_execution_update" event
    |
    v
InteractiveMode.handleEvent():
    const component = this.pendingTools.get(event.toolCallId);
    if (component) {
        component.updateResult({ ...event.partialResult, isError: false }, true);  // isPartial=true
        this.ui.requestRender();
    }
```

`updateResult()` stores the result and calls `updateDisplay()`, which rebuilds the Box contents.

### 4.10 Lifecycle of a ToolExecutionComponent

1. **Creation during streaming** (`message_update`): Component created when a `toolCall` block first appears in the assistant message.
2. **Args updates** (`message_update`): As more tokens stream in, `updateArgs()` is called.
3. **Execution starts** (`tool_execution_start`): `markExecutionStarted()` sets `executionStarted = true`.
4. **Args finalized** (`message_end`): `setArgsComplete()` sets `argsComplete = true` (triggers diff computation for edit tools).
5. **Partial results** (`tool_execution_update`): `updateResult(result, true)` with `isPartial = true`.
6. **Final result** (`tool_execution_end`): `updateResult(result)` with `isPartial = false`. Background changes to success/error. Component removed from `pendingTools` map.

### 4.11 Hidden Components

If a tool definition has renderers but they produce no visible content and there are no images, the component hides itself:

```typescript
if (this.hasRendererDefinition() && !hasContent && this.imageComponents.length === 0) {
    this.hideComponent = true;
}
```

This is used by tools that want to suppress their UI entirely in certain states.

---

## 5. Extension API Surface for UI Control

**Source files:**
- `packages/coding-agent/src/core/extensions/types.ts` (ExtensionUIContext interface)
- `packages/coding-agent/src/modes/interactive/interactive-mode.ts` (implementations)

### 5.1 Complete API Reference Table

| API Method | What It Controls | Container/Area | Limitations |
|---|---|---|---|
| `setWidget(key, content, options?)` | Extension widgets above/below editor | `widgetContainerAbove` or `widgetContainerBelow` | Max 10 lines total. String arrays or component factory. |
| `setFooter(factory \| undefined)` | Custom footer replacing built-in | Bottom of screen (replaces `FooterComponent`) | Must implement `render(width): string[]` and `invalidate()`. Receives `FooterDataProvider`. |
| `setHeader(factory \| undefined)` | Custom header replacing built-in | Top of screen (`headerContainer`) | Must implement `render(width): string[]` and `invalidate()`. |
| `setStatus(key, text \| undefined)` | Extension status text in footer | Footer status area | Text only. Keyed (multiple extensions can set different keys). |
| `setWorkingMessage(message?)` | Loading animation text | `statusContainer` | Only effective while agent is streaming. Call with no args to restore default. |
| `setEditorComponent(factory \| undefined)` | Replace default input editor | `editorContainer` | Must return `EditorComponent`. Complex: needs keybinding support. |
| `custom(factory, options?)` | Show arbitrary component with focus | Replaces editor OR shown as overlay | Blocks until `done()` is called. Can be overlay with positioning options. |
| `notify(message, type?)` | Show notification | Status area of chat | Transient. Types: "info", "warning", "error". |
| `select(title, options, opts?)` | Show selector dialog | Replaces editor area | Returns `Promise<string \| undefined>`. Supports timeout and AbortSignal. |
| `confirm(title, message, opts?)` | Show confirmation dialog | Replaces editor area | Returns `Promise<boolean>`. Supports timeout and AbortSignal. |
| `input(title, placeholder?, opts?)` | Show text input dialog | Replaces editor area | Returns `Promise<string \| undefined>`. Supports timeout and AbortSignal. |
| `editor(title, prefill?)` | Show multi-line editor | Replaces editor area | Returns `Promise<string \| undefined>`. For longer text input. |
| `setTitle(title)` | Terminal window/tab title | Terminal title bar | String only. |
| `setTheme(theme)` | Change color theme | Entire UI | Accepts theme name (string) or `Theme` instance. Returns `{ success, error? }`. |
| `pasteToEditor(text)` | Paste text into editor | Editor | Triggers paste handling (may collapse large content). |
| `setEditorText(text)` | Set editor text directly | Editor | Overwrites current content. |
| `getEditorText()` | Read current editor text | Editor | Returns expanded text if available. |
| `onTerminalInput(handler)` | Listen to raw terminal input | Global | Returns unsubscribe function. Handler can consume/modify input. |
| `getToolsExpanded()` | Query expansion state | N/A | Returns boolean. |
| `setToolsExpanded(expanded)` | Set expansion state | All expandable components in chat | Affects all tool results, custom messages, compaction summaries, etc. |
| `getAllThemes()` | List available themes | N/A | Returns `{ name, path }[]`. |
| `getTheme(name)` | Load a theme by name | N/A | Returns `Theme \| undefined`. Does not activate it. |
| `theme` (getter) | Access current theme | N/A | Read-only `Theme` instance for color access. |

### 5.2 setWidget Details

```typescript
setWidget(key: string, content: string[] | undefined, options?: ExtensionWidgetOptions): void;
setWidget(
    key: string,
    content: ((tui: TUI, theme: Theme) => Component & { dispose?(): void }) | undefined,
    options?: ExtensionWidgetOptions,
): void;
```

Options:
```typescript
export interface ExtensionWidgetOptions {
    placement?: "aboveEditor" | "belowEditor";  // Default: "aboveEditor"
}
```

Widgets are keyed by string. Setting the same key replaces the previous widget. Setting content to `undefined` removes the widget.

Maximum lines enforced at `MAX_WIDGET_LINES = 10` (defined as a static on `InteractiveMode`). Excess lines show "... (widget truncated)".

Example:
```typescript
ctx.ui.setWidget("my-status", ["Line 1", "Line 2"]);
ctx.ui.setWidget("my-component", (tui, theme) => {
    return { render(width) { return ["custom component"]; }, invalidate() {}, dispose() {} };
}, { placement: "belowEditor" });
ctx.ui.setWidget("my-status", undefined);  // Remove
```

### 5.3 setFooter Details

The factory receives:
- `tui: TUI` -- the TUI instance for `requestRender()`
- `theme: Theme` -- current theme
- `footerData: ReadonlyFooterDataProvider` -- access to git branch, extension statuses

The returned component must implement:
- `render(width: number): string[]` -- return rendered lines
- `invalidate(): void` -- called when data changes
- `dispose?(): void` -- optional cleanup

Example from `packages/coding-agent/examples/extensions/custom-footer.ts`:
```typescript
ctx.ui.setFooter((tui, theme, footerData) => {
    const unsub = footerData.onBranchChange(() => tui.requestRender());
    return {
        dispose: unsub,
        invalidate() {},
        render(width: number): string[] {
            const branch = footerData.getGitBranch();
            const left = theme.fg("dim", `tokens info here`);
            const right = theme.fg("dim", `model${branch ? ` (${branch})` : ""}`);
            const pad = " ".repeat(Math.max(1, width - visibleWidth(left) - visibleWidth(right)));
            return [truncateToWidth(left + pad + right, width)];
        },
    };
});
```

### 5.4 setHeader Details

```typescript
setHeader(factory: ((tui: TUI, theme: Theme) => Component & { dispose?(): void }) | undefined): void;
```

Replaces the built-in header (logo + keybinding hints). Pass `undefined` to restore.

### 5.5 custom() Details

```typescript
custom<T>(
    factory: (
        tui: TUI,
        theme: Theme,
        keybindings: KeybindingsManager,
        done: (result: T) => void,
    ) => (Component & { dispose?(): void }) | Promise<Component & { dispose?(): void }>,
    options?: {
        overlay?: boolean;
        overlayOptions?: OverlayOptions | (() => OverlayOptions);
        onHandle?: (handle: OverlayHandle) => void;
    },
): Promise<T>;
```

This is the most powerful UI primitive. It either replaces the editor area (default) or shows as an overlay. The promise resolves when `done()` is called.

Key behaviors:
- When not overlay: saves editor text, replaces editor container content, sets focus to new component.
- When overlay: uses `ui.showOverlay()` with positioning options. Handle exposed via `onHandle`.
- On `done(result)`: restores editor, resolves promise with result.
- Component's `dispose()` is called after closing.

### 5.6 Dialog Options

All dialog methods (`select`, `confirm`, `input`) accept:

```typescript
export interface ExtensionUIDialogOptions {
    signal?: AbortSignal;    // Programmatic dismissal
    timeout?: number;        // Auto-dismiss after N milliseconds (shows countdown)
}
```

---

## 6. What Cannot Be Overridden

This section documents the hard constraints of the Pi rendering system. These are architectural limitations, not bugs.

### 6.1 No Assistant Message Renderer Override

There is no `registerAssistantRenderer()` or equivalent. The `AssistantMessageComponent` is always used for `role: "assistant"` messages. You cannot:
- Replace the Markdown rendering
- Inject custom content into assistant messages
- Suppress assistant message display
- Change the text color or styling of assistant text

The only control over assistant messages is:
- `hideThinkingBlock` (user setting, not extension-controllable)
- Theme colors for `thinkingText` (via theme customization)

### 6.2 No Way to Suppress Default Rendering

When a message is added to the chat, it **will** be rendered. There is no event that fires before rendering with an option to cancel. Specifically:
- Custom messages with `display: true` will always create a `CustomMessageComponent`
- If your custom renderer returns `undefined`, default rendering takes over (Box with label)
- You cannot intercept and suppress rendering of user messages or assistant messages

### 6.3 Tool Results Always in Box

`ToolExecutionComponent` always wraps its content in a `Box` with a background color. You can control what goes **inside** the Box via `renderCall` and `renderResult`, but you cannot:
- Remove the Box wrapper
- Remove the background color
- Change the background color scheme (toolPendingBg/toolSuccessBg/toolErrorBg) from an extension (only via theme)
- Render tool results outside of a Box

The one exception: if `hideComponent` is set (when renderers produce no content), the component renders empty lines.

### 6.4 No Control Over Layout Order

The layout order (header -> chat -> pending -> status -> widgets -> editor -> widgets -> footer) is hardcoded. You cannot:
- Move the editor above the chat
- Insert components between chat messages and the editor
- Add content between the status area and widgets

### 6.5 No Chat Container Access

Extensions cannot directly access `chatContainer` to add or remove children. All chat content flows through the event pipeline (`message_start`/`message_update`/`message_end`) and `addMessageToChat()`.

### 6.6 No Message Removal or Modification After Rendering

Once a component is added to `chatContainer`, there is no API to remove or update it (except through the built-in mechanisms like compaction rebuild).

### 6.7 Global Expansion Toggle

The `expanded` state is global for all expandable components. You cannot have per-component expansion state through the public API.

### 6.8 No Streaming Content Interception

You cannot intercept or modify assistant message content during streaming. The `message_update` event in extensions is informational -- it does not allow modification of the content before rendering.

---

## 7. Strategy Patterns for Custom Chat UIs

Given the constraints documented above, there are three main strategies for building custom chat experiences in Pi.

### Strategy A: Style the Tool Block Interior

**Approach:** Register tools with custom `renderCall` and `renderResult` functions to control what appears inside the tool execution Box.

**When to use:** You want to customize how specific tools are displayed, but the overall chat structure (assistant messages, user messages) is fine.

**Trade-offs:**
- Pros: Works within the existing system. Full control over tool content rendering. Built-in state management via `ToolRenderContext.state`.
- Cons: Cannot remove the Box wrapper. Cannot change Box background colors (only via theme). Cannot affect assistant message rendering.

**Code example:**

```typescript
import type { ExtensionAPI, ReadToolDetails } from "@mariozechner/pi-coding-agent";
import { createReadTool } from "@mariozechner/pi-coding-agent";
import { Text } from "@mariozechner/pi-tui";

export default function (pi: ExtensionAPI) {
    const originalRead = createReadTool(process.cwd());

    pi.registerTool({
        name: "read",
        label: "read",
        description: originalRead.description,
        parameters: originalRead.parameters,

        async execute(toolCallId, params, signal, onUpdate) {
            return originalRead.execute(toolCallId, params, signal, onUpdate);
        },

        renderCall(args, theme, context) {
            let text = theme.fg("toolTitle", theme.bold("read "));
            text += theme.fg("accent", args.path);
            if (args.offset || args.limit) {
                const parts: string[] = [];
                if (args.offset) parts.push(`offset=${args.offset}`);
                if (args.limit) parts.push(`limit=${args.limit}`);
                text += theme.fg("dim", ` (${parts.join(", ")})`);
            }
            return new Text(text, 0, 0);
        },

        renderResult(result, { expanded, isPartial }, theme, context) {
            if (isPartial) return new Text(theme.fg("warning", "Reading..."), 0, 0);

            const details = result.details as ReadToolDetails | undefined;
            const content = result.content[0];
            if (content?.type !== "text") {
                return new Text(theme.fg("error", "No content"), 0, 0);
            }

            const lineCount = content.text.split("\n").length;
            let text = theme.fg("success", `${lineCount} lines`);

            if (expanded) {
                const preview = content.text.split("\n").slice(0, 15);
                for (const line of preview) {
                    text += `\n${theme.fg("dim", line)}`;
                }
                if (lineCount > 15) {
                    text += `\n${theme.fg("muted", `... ${lineCount - 15} more`)}`;
                }
            }

            return new Text(text, 0, 0);
        },
    });
}
```

### Strategy B: Custom Messages for Team Responses

**Approach:** Use `pi.sendMessage()` with custom types and `registerMessageRenderer()` to inject styled messages into the chat. Each "team member" or "agent" gets its own custom type.

**When to use:** You are building a multi-agent or team chat UI where different agents produce responses that should be visually distinct from the main assistant.

**Trade-offs:**
- Pros: Full control over rendering via custom renderers. Can use any `pi-tui` components. Messages appear inline in the chat flow. Can carry arbitrary `details` payload. Can control whether messages are sent to LLM context.
- Cons: The main assistant message is still rendered by `AssistantMessageComponent` (cannot be overridden). Custom messages are user-role in LLM context (not assistant-role). Cannot suppress the default rendering if renderer returns `undefined`.

**Code example:**

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Box, Container, Spacer, Text } from "@mariozechner/pi-tui";

interface TeamResponse {
    agent: string;
    role: string;
    confidence: number;
}

export default function (pi: ExtensionAPI) {
    // Register renderers for each team member type
    pi.registerMessageRenderer<TeamResponse>("team-response", (message, { expanded }, theme) => {
        const details = message.details;
        if (!details) return undefined;

        const container = new Container();

        // Agent header with role badge
        const roleColor = details.role === "lead" ? "accent"
            : details.role === "reviewer" ? "warning"
            : "success";

        const header = `${theme.bold(theme.fg(roleColor, details.agent))} ${theme.fg("dim", `[${details.role}]`)}`;

        const box = new Box(1, 1, (t) => theme.bg("customMessageBg", t));
        box.addChild(new Text(header, 0, 0));
        box.addChild(new Spacer(1));

        // Content
        const text = typeof message.content === "string"
            ? message.content
            : message.content.filter(c => c.type === "text").map(c => c.text).join("\n");
        box.addChild(new Text(text, 0, 0));

        // Show confidence when expanded
        if (expanded && details.confidence !== undefined) {
            box.addChild(new Spacer(1));
            const bar = "#".repeat(Math.round(details.confidence * 20));
            box.addChild(new Text(
                theme.fg("dim", `Confidence: [${bar.padEnd(20, ".")}] ${(details.confidence * 100).toFixed(0)}%`),
                0, 0
            ));
        }

        container.addChild(box);
        return container;
    });

    // Tool or event handler that sends team messages
    pi.on("message_end", async (event, ctx) => {
        if (event.message.role !== "assistant") return;

        // Example: inject a "review" message after each assistant response
        pi.sendMessage<TeamResponse>({
            customType: "team-response",
            content: "I have reviewed the above response and it looks correct.",
            display: true,
            details: {
                agent: "Reviewer",
                role: "reviewer",
                confidence: 0.92,
            },
        });
    });
}
```

### Strategy C: Full UI Takeover

**Approach:** Use `custom()` to take over the editor area with a complete custom component, `setHeader()` and `setFooter()` to control chrome, and `setWidget()` for persistent status displays. Use `sendMessage()` with `display: false` to inject context without default rendering.

**When to use:** You want a radically different UI paradigm (e.g., a panel-based layout, a Kanban board, a custom game interface).

**Trade-offs:**
- Pros: Maximum control over the visible UI. Can hide default header/footer. Can show arbitrary components. `custom()` gives full keyboard focus.
- Cons: The `chatContainer` still exists and renders messages -- you cannot suppress it. `custom()` blocks the input loop while active. Complex to manage state across custom components and the chat flow. Must re-implement features like scrolling if needed.

**Code example:**

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Container, Text, Box } from "@mariozechner/pi-tui";

export default function (pi: ExtensionAPI) {
    pi.on("session_start", async (_event, ctx) => {
        if (!ctx.hasUI) return;

        // Replace header
        ctx.ui.setHeader((_tui, theme) => ({
            render(width: number): string[] {
                const title = theme.bold(theme.fg("accent", "MY CUSTOM AGENT"));
                return ["", ` ${title}`, ""];
            },
            invalidate() {},
        }));

        // Replace footer
        ctx.ui.setFooter((tui, theme, footerData) => ({
            render(width: number): string[] {
                return [theme.fg("dim", " Custom footer | Press Ctrl+C to exit")];
            },
            invalidate() {},
        }));

        // Add persistent widget
        ctx.ui.setWidget("dashboard", (tui, theme) => {
            const container = new Container();
            container.addChild(new Text(theme.fg("accent", "  Status: Active"), 0, 0));
            return Object.assign(container, { dispose() {} });
        });

        // Set custom working message
        ctx.ui.setWorkingMessage("Custom agent thinking...");
    });

    // Use display:false to add context without rendering
    pi.on("before_agent_start", async (_event, ctx) => {
        pi.sendMessage({
            customType: "system-context",
            content: "Additional context injected silently",
            display: false,  // Not rendered, but sent to LLM
        });
    });

    // Custom command to show a full-screen panel
    pi.registerCommand("panel", {
        description: "Show custom panel",
        handler: async (_args, ctx) => {
            const result = await ctx.ui.custom<string>((tui, theme, keybindings, done) => {
                const container = new Container();
                const box = new Box(1, 1, (t) => theme.bg("customMessageBg", t));
                box.addChild(new Text("Full-screen custom panel", 0, 0));
                box.addChild(new Text("Press 'q' to close", 0, 0));
                container.addChild(box);

                // Handle keyboard input
                const component = Object.assign(container, {
                    handleInput(data: string) {
                        if (data === "q") done("closed");
                    },
                    dispose() {},
                });

                return component;
            });
            ctx.ui.notify(`Panel result: ${result}`, "info");
        },
    });
}
```

### Strategy Comparison Matrix

| Capability | Strategy A (Tool Interior) | Strategy B (Custom Messages) | Strategy C (Full Takeover) |
|---|---|---|---|
| Custom tool rendering | Full control inside Box | No direct control | No direct control |
| Custom chat messages | No | Full control | Full control |
| Override assistant rendering | No | No | No |
| Custom header/footer | No | Optional | Yes |
| Custom editor | No | Optional | Yes |
| Persistent widgets | No | Optional | Yes |
| Implementation complexity | Low | Medium | High |
| Maintenance burden | Low | Medium | High |
| Works with streaming | Yes (via `onUpdate`) | Yes (via events) | Partially (custom() blocks) |
| LLM context control | Via tool results | Via `display` flag | Via `display` flag |

### Hybrid Approach

In practice, the most effective approach for a multi-agent chat UI combines strategies A and B:

1. **Strategy B** for team member responses: Each agent's output is sent as a custom message with a registered renderer, giving full visual control.
2. **Strategy A** for tool customization: Override built-in tool renderers for a more compact or styled display.
3. **Strategy C elements** (setHeader, setFooter, setWidget) for chrome customization.

The main assistant message remains uncontrollable -- it will always render with the default `AssistantMessageComponent`. The recommended workaround is to instruct the LLM (via system prompt) to keep its direct responses minimal, with the bulk of the visible output flowing through custom messages and tool renderers where you have full control.

---

## Appendix A: Key Source File Locations

| File | Path | Purpose |
|---|---|---|
| Interactive Mode | `packages/coding-agent/src/modes/interactive/interactive-mode.ts` | Main TUI orchestration (~4647 lines) |
| AssistantMessageComponent | `packages/coding-agent/src/modes/interactive/components/assistant-message.ts` | Assistant message rendering |
| CustomMessageComponent | `packages/coding-agent/src/modes/interactive/components/custom-message.ts` | Custom message rendering |
| ToolExecutionComponent | `packages/coding-agent/src/modes/interactive/components/tool-execution.ts` | Tool call/result rendering |
| Extension Types | `packages/coding-agent/src/core/extensions/types.ts` | All type definitions (~1451 lines) |
| Extension Runner | `packages/coding-agent/src/core/extensions/runner.ts` | Extension lifecycle, `getMessageRenderer()` |
| Extension Index | `packages/coding-agent/src/core/extensions/index.ts` | Public re-exports |
| Messages | `packages/coding-agent/src/core/messages.ts` | `CustomMessage`, `convertToLlm()` |
| Extension Wrapper | `packages/coding-agent/src/core/extensions/wrapper.ts` | Tool wrapping utilities |

## Appendix B: Example Extensions

| Example | Path | Demonstrates |
|---|---|---|
| Message Renderer | `packages/coding-agent/examples/extensions/message-renderer.ts` | `registerMessageRenderer` + `sendMessage` |
| Widget Placement | `packages/coding-agent/examples/extensions/widget-placement.ts` | `setWidget` with above/below placement |
| Custom Footer | `packages/coding-agent/examples/extensions/custom-footer.ts` | `setFooter` with FooterDataProvider |
| Custom Header | `packages/coding-agent/examples/extensions/custom-header.ts` | `setHeader` replacement |
| Built-in Tool Renderer | `packages/coding-agent/examples/extensions/built-in-tool-renderer.ts` | Override renderCall/renderResult for built-in tools |
| Tool Override | `packages/coding-agent/examples/extensions/tool-override.ts` | Replace built-in tool entirely, uses built-in renderer fallback |

## Appendix C: Theme Colors Relevant to Rendering

These theme color keys are used in the rendering components:

| Color Key | Used By | Purpose |
|---|---|---|
| `toolPendingBg` | ToolExecutionComponent | Box background during execution |
| `toolSuccessBg` | ToolExecutionComponent | Box background on success |
| `toolErrorBg` | ToolExecutionComponent | Box background on error |
| `toolTitle` | ToolExecutionComponent | Tool name text |
| `toolOutput` | ToolExecutionComponent | Tool output text |
| `customMessageBg` | CustomMessageComponent | Default Box background |
| `customMessageLabel` | CustomMessageComponent | `[customType]` label text |
| `customMessageText` | CustomMessageComponent | Message content text |
| `thinkingText` | AssistantMessageComponent | Thinking block text color |
| `error` | AssistantMessageComponent, ToolExecutionComponent | Error message text |
| `accent` | Various | Primary accent color |
| `dim` | Various | Muted/secondary text |
| `muted` | Various | Even more muted text |
| `warning` | Various | Warning text |
| `success` | Various | Success text |

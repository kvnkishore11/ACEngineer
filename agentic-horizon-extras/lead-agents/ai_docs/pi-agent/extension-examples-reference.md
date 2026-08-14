# Pi Coding Agent Extension Examples Reference

> Source: https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions
> Fetched: 2026-03-24

This document contains the complete source code and detailed annotations for every key Pi extension example that demonstrates message handling, UI control, input interception, tool registration, and inter-extension communication. It is intended as a comprehensive reference for building custom Pi extensions.

---

## Table of Contents

1. [Message Renderer](#1-message-renderer)
2. [Plan Mode](#2-plan-mode)
3. [Send User Message](#3-send-user-message)
4. [Subagent](#4-subagent)
5. [Input Transform](#5-input-transform)
6. [File Trigger](#6-file-trigger)
7. [Event Bus](#7-event-bus)
8. [Dynamic Tools](#8-dynamic-tools)
9. [Tool Override](#9-tool-override)
10. [Built-in Tool Renderer](#10-built-in-tool-renderer)
11. [Handoff](#11-handoff)
12. [Widget Placement](#12-widget-placement)
13. [Custom Header](#13-custom-header)
14. [Custom Footer](#14-custom-footer)
15. [Pattern Summary Table](#15-pattern-summary-table)

---

## 1. Message Renderer

**File:** `examples/extensions/message-renderer.ts`

This example shows how to use `registerMessageRenderer` to control how custom messages appear in the TUI, and how `sendMessage` creates those custom message entries.

### Full Source

```typescript
/**
 * Custom message rendering example.
 *
 * Shows how to use registerMessageRenderer to control how custom messages
 * appear in the TUI, with colors, formatting, and expandable details.
 *
 * Usage: /status [message] - sends a status message with custom rendering
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Box, Text } from "@mariozechner/pi-tui";

export default function (pi: ExtensionAPI) {
	// Register custom renderer for "status-update" messages
	pi.registerMessageRenderer("status-update", (message, { expanded }, theme) => {
		const details = message.details as { level: string; timestamp: number } | undefined;
		const level = details?.level ?? "info";

		// Color based on level
		const color = level === "error" ? "error" : level === "warn" ? "warning" : "success";
		const prefix = theme.fg(color, `[${level.toUpperCase()}]`);

		let text = `${prefix} ${message.content}`;

		// Show timestamp when expanded
		if (expanded && details?.timestamp) {
			const time = new Date(details.timestamp).toLocaleTimeString();
			text += `\n${theme.fg("dim", `  at ${time}`)}`;
		}

		// Use Box with customMessageBg for consistent styling
		const box = new Box(1, 1, (t) => theme.bg("customMessageBg", t));
		box.addChild(new Text(text, 0, 0));
		return box;
	});

	// Command to send status messages
	pi.registerCommand("status", {
		description: "Send a status message (usage: /status [warn|error] message)",
		handler: async (args, _ctx) => {
			const parts = args.trim().split(/\s+/);
			let level = "info";
			let content = args.trim();

			// Check for level prefix
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

### Detailed Annotations

#### `pi.registerMessageRenderer(customType, renderFn)`

- **First argument** (`"status-update"`): The `customType` string that identifies which messages this renderer handles. When `pi.sendMessage()` is called with `customType: "status-update"`, this renderer is invoked.
- **Second argument**: A render function with signature `(message, { expanded }, theme) => TUIComponent`.
  - `message` -- The custom message object containing `content`, `details`, and other fields.
  - `expanded` -- A boolean toggled by the user (Ctrl+O in the TUI). Use this to show/hide additional detail.
  - `theme` -- The TUI theme object providing `theme.fg(colorName, text)` and `theme.bg(colorName, text)` for styling.

#### The Expanded Toggle Pattern

The `expanded` boolean allows two rendering modes:
- **Collapsed** (default): Show only the essential info -- the level prefix and content text.
- **Expanded**: Show additional metadata -- here, the timestamp. Users toggle with Ctrl+O.

This is the idiomatic pattern for any tool or message renderer that has more detail than fits in one line.

#### `pi.sendMessage(options)`

Creates a custom message entry in the conversation. Key fields:
- `customType: "status-update"` -- Links this message to the registered renderer.
- `content: string` -- The main text content of the message.
- `display: true` -- Makes the message visible in the TUI. If `false`, the message exists in the session but is not rendered.
- `details: object` -- Arbitrary JSON data attached to the message. The renderer accesses this via `message.details`.

Note: `sendMessage` by default does **not** trigger an LLM turn. To trigger a turn, pass a second argument: `{ triggerTurn: true }`.

#### TUI Components Used

- `Box(paddingX, paddingY, bgTransform)` -- A container with padding and optional background. `theme.bg("customMessageBg", t)` applies the standard custom message background color.
- `Text(content, x, y)` -- A text node positioned at (x, y) within its parent.
- `box.addChild(child)` -- Adds a child component to the box.

---

## 2. Plan Mode

**Files:** `examples/extensions/plan-mode/index.ts` and `examples/extensions/plan-mode/utils.ts`

This is the most complex example. It demonstrates:
- Toggling between restricted/full tool sets with `setActiveTools`
- Injecting context messages via `before_agent_start`
- Blocking tool calls via `tool_call` event
- Filtering context messages via `context` event
- Tracking progress with `setWidget` and `setStatus`
- Persisting state across sessions with `appendEntry`
- Interactive UI with `select` and `editor` prompts
- Sending messages that trigger or do not trigger LLM turns

### Full Source: `index.ts`

```typescript
/**
 * Plan Mode Extension
 *
 * Read-only exploration mode for safe code analysis.
 * When enabled, only read-only tools are available.
 *
 * Features:
 * - /plan command or Ctrl+Alt+P to toggle
 * - Bash restricted to allowlisted read-only commands
 * - Extracts numbered plan steps from "Plan:" sections
 * - [DONE:n] markers to complete steps during execution
 * - Progress tracking widget during execution
 */

import type { AgentMessage } from "@mariozechner/pi-agent-core";
import type { AssistantMessage, TextContent } from "@mariozechner/pi-ai";
import type { ExtensionAPI, ExtensionContext } from "@mariozechner/pi-coding-agent";
import { Key } from "@mariozechner/pi-tui";
import { extractTodoItems, isSafeCommand, markCompletedSteps, type TodoItem } from "./utils.js";

// Tools
const PLAN_MODE_TOOLS = ["read", "bash", "grep", "find", "ls", "questionnaire"];
const NORMAL_MODE_TOOLS = ["read", "bash", "edit", "write"];

// Type guard for assistant messages
function isAssistantMessage(m: AgentMessage): m is AssistantMessage {
	return m.role === "assistant" && Array.isArray(m.content);
}

// Extract text content from an assistant message
function getTextContent(message: AssistantMessage): string {
	return message.content
		.filter((block): block is TextContent => block.type === "text")
		.map((block) => block.text)
		.join("\n");
}

export default function planModeExtension(pi: ExtensionAPI): void {
	let planModeEnabled = false;
	let executionMode = false;
	let todoItems: TodoItem[] = [];

	pi.registerFlag("plan", {
		description: "Start in plan mode (read-only exploration)",
		type: "boolean",
		default: false,
	});

	function updateStatus(ctx: ExtensionContext): void {
		// Footer status
		if (executionMode && todoItems.length > 0) {
			const completed = todoItems.filter((t) => t.completed).length;
			ctx.ui.setStatus("plan-mode", ctx.ui.theme.fg("accent", `📋 ${completed}/${todoItems.length}`));
		} else if (planModeEnabled) {
			ctx.ui.setStatus("plan-mode", ctx.ui.theme.fg("warning", "⏸ plan"));
		} else {
			ctx.ui.setStatus("plan-mode", undefined);
		}

		// Widget showing todo list
		if (executionMode && todoItems.length > 0) {
			const lines = todoItems.map((item) => {
				if (item.completed) {
					return (
						ctx.ui.theme.fg("success", "☑ ") + ctx.ui.theme.fg("muted", ctx.ui.theme.strikethrough(item.text))
					);
				}
				return `${ctx.ui.theme.fg("muted", "☐ ")}${item.text}`;
			});
			ctx.ui.setWidget("plan-todos", lines);
		} else {
			ctx.ui.setWidget("plan-todos", undefined);
		}
	}

	function togglePlanMode(ctx: ExtensionContext): void {
		planModeEnabled = !planModeEnabled;
		executionMode = false;
		todoItems = [];

		if (planModeEnabled) {
			pi.setActiveTools(PLAN_MODE_TOOLS);
			ctx.ui.notify(`Plan mode enabled. Tools: ${PLAN_MODE_TOOLS.join(", ")}`);
		} else {
			pi.setActiveTools(NORMAL_MODE_TOOLS);
			ctx.ui.notify("Plan mode disabled. Full access restored.");
		}
		updateStatus(ctx);
	}

	function persistState(): void {
		pi.appendEntry("plan-mode", {
			enabled: planModeEnabled,
			todos: todoItems,
			executing: executionMode,
		});
	}

	pi.registerCommand("plan", {
		description: "Toggle plan mode (read-only exploration)",
		handler: async (_args, ctx) => togglePlanMode(ctx),
	});

	pi.registerCommand("todos", {
		description: "Show current plan todo list",
		handler: async (_args, ctx) => {
			if (todoItems.length === 0) {
				ctx.ui.notify("No todos. Create a plan first with /plan", "info");
				return;
			}
			const list = todoItems.map((item, i) => `${i + 1}. ${item.completed ? "✓" : "○"} ${item.text}`).join("\n");
			ctx.ui.notify(`Plan Progress:\n${list}`, "info");
		},
	});

	pi.registerShortcut(Key.ctrlAlt("p"), {
		description: "Toggle plan mode",
		handler: async (ctx) => togglePlanMode(ctx),
	});

	// Block destructive bash commands in plan mode
	pi.on("tool_call", async (event) => {
		if (!planModeEnabled || event.toolName !== "bash") return;

		const command = event.input.command as string;
		if (!isSafeCommand(command)) {
			return {
				block: true,
				reason: `Plan mode: command blocked (not allowlisted). Use /plan to disable plan mode first.\nCommand: ${command}`,
			};
		}
	});

	// Filter out stale plan mode context when not in plan mode
	pi.on("context", async (event) => {
		if (planModeEnabled) return;

		return {
			messages: event.messages.filter((m) => {
				const msg = m as AgentMessage & { customType?: string };
				if (msg.customType === "plan-mode-context") return false;
				if (msg.role !== "user") return true;

				const content = msg.content;
				if (typeof content === "string") {
					return !content.includes("[PLAN MODE ACTIVE]");
				}
				if (Array.isArray(content)) {
					return !content.some(
						(c) => c.type === "text" && (c as TextContent).text?.includes("[PLAN MODE ACTIVE]"),
					);
				}
				return true;
			}),
		};
	});

	// Inject plan/execution context before agent starts
	pi.on("before_agent_start", async () => {
		if (planModeEnabled) {
			return {
				message: {
					customType: "plan-mode-context",
					content: `[PLAN MODE ACTIVE]
You are in plan mode - a read-only exploration mode for safe code analysis.

Restrictions:
- You can only use: read, bash, grep, find, ls, questionnaire
- You CANNOT use: edit, write (file modifications are disabled)
- Bash is restricted to an allowlist of read-only commands

Ask clarifying questions using the questionnaire tool.
Use brave-search skill via bash for web research.

Create a detailed numbered plan under a "Plan:" header:

Plan:
1. First step description
2. Second step description
...

Do NOT attempt to make changes - just describe what you would do.`,
					display: false,
				},
			};
		}

		if (executionMode && todoItems.length > 0) {
			const remaining = todoItems.filter((t) => !t.completed);
			const todoList = remaining.map((t) => `${t.step}. ${t.text}`).join("\n");
			return {
				message: {
					customType: "plan-execution-context",
					content: `[EXECUTING PLAN - Full tool access enabled]

Remaining steps:
${todoList}

Execute each step in order.
After completing a step, include a [DONE:n] tag in your response.`,
					display: false,
				},
			};
		}
	});

	// Track progress after each turn
	pi.on("turn_end", async (event, ctx) => {
		if (!executionMode || todoItems.length === 0) return;
		if (!isAssistantMessage(event.message)) return;

		const text = getTextContent(event.message);
		if (markCompletedSteps(text, todoItems) > 0) {
			updateStatus(ctx);
		}
		persistState();
	});

	// Handle plan completion and plan mode UI
	pi.on("agent_end", async (event, ctx) => {
		// Check if execution is complete
		if (executionMode && todoItems.length > 0) {
			if (todoItems.every((t) => t.completed)) {
				const completedList = todoItems.map((t) => `~~${t.text}~~`).join("\n");
				pi.sendMessage(
					{ customType: "plan-complete", content: `**Plan Complete!** ✓\n\n${completedList}`, display: true },
					{ triggerTurn: false },
				);
				executionMode = false;
				todoItems = [];
				pi.setActiveTools(NORMAL_MODE_TOOLS);
				updateStatus(ctx);
				persistState();
			}
			return;
		}

		if (!planModeEnabled || !ctx.hasUI) return;

		// Extract todos from last assistant message
		const lastAssistant = [...event.messages].reverse().find(isAssistantMessage);
		if (lastAssistant) {
			const extracted = extractTodoItems(getTextContent(lastAssistant));
			if (extracted.length > 0) {
				todoItems = extracted;
			}
		}

		// Show plan steps and prompt for next action
		if (todoItems.length > 0) {
			const todoListText = todoItems.map((t, i) => `${i + 1}. ☐ ${t.text}`).join("\n");
			pi.sendMessage(
				{
					customType: "plan-todo-list",
					content: `**Plan Steps (${todoItems.length}):**\n\n${todoListText}`,
					display: true,
				},
				{ triggerTurn: false },
			);
		}

		const choice = await ctx.ui.select("Plan mode - what next?", [
			todoItems.length > 0 ? "Execute the plan (track progress)" : "Execute the plan",
			"Stay in plan mode",
			"Refine the plan",
		]);

		if (choice?.startsWith("Execute")) {
			planModeEnabled = false;
			executionMode = todoItems.length > 0;
			pi.setActiveTools(NORMAL_MODE_TOOLS);
			updateStatus(ctx);

			const execMessage =
				todoItems.length > 0
					? `Execute the plan. Start with: ${todoItems[0].text}`
					: "Execute the plan you just created.";
			pi.sendMessage(
				{ customType: "plan-mode-execute", content: execMessage, display: true },
				{ triggerTurn: true },
			);
		} else if (choice === "Refine the plan") {
			const refinement = await ctx.ui.editor("Refine the plan:", "");
			if (refinement?.trim()) {
				pi.sendUserMessage(refinement.trim());
			}
		}
	});

	// Restore state on session start/resume
	pi.on("session_start", async (_event, ctx) => {
		if (pi.getFlag("plan") === true) {
			planModeEnabled = true;
		}

		const entries = ctx.sessionManager.getEntries();

		// Restore persisted state
		const planModeEntry = entries
			.filter((e: { type: string; customType?: string }) => e.type === "custom" && e.customType === "plan-mode")
			.pop() as { data?: { enabled: boolean; todos?: TodoItem[]; executing?: boolean } } | undefined;

		if (planModeEntry?.data) {
			planModeEnabled = planModeEntry.data.enabled ?? planModeEnabled;
			todoItems = planModeEntry.data.todos ?? todoItems;
			executionMode = planModeEntry.data.executing ?? executionMode;
		}

		// On resume: re-scan messages to rebuild completion state
		const isResume = planModeEntry !== undefined;
		if (isResume && executionMode && todoItems.length > 0) {
			let executeIndex = -1;
			for (let i = entries.length - 1; i >= 0; i--) {
				const entry = entries[i] as { type: string; customType?: string };
				if (entry.customType === "plan-mode-execute") {
					executeIndex = i;
					break;
				}
			}

			const messages: AssistantMessage[] = [];
			for (let i = executeIndex + 1; i < entries.length; i++) {
				const entry = entries[i];
				if (entry.type === "message" && "message" in entry && isAssistantMessage(entry.message as AgentMessage)) {
					messages.push(entry.message as AssistantMessage);
				}
			}
			const allText = messages.map(getTextContent).join("\n");
			markCompletedSteps(allText, todoItems);
		}

		if (planModeEnabled) {
			pi.setActiveTools(PLAN_MODE_TOOLS);
		}
		updateStatus(ctx);
	});
}
```

### Full Source: `utils.ts`

```typescript
/**
 * Pure utility functions for plan mode.
 * Extracted for testability.
 */

// Destructive commands blocked in plan mode
const DESTRUCTIVE_PATTERNS = [
	/\brm\b/i,
	/\brmdir\b/i,
	/\bmv\b/i,
	/\bcp\b/i,
	/\bmkdir\b/i,
	/\btouch\b/i,
	/\bchmod\b/i,
	/\bchown\b/i,
	/\bchgrp\b/i,
	/\bln\b/i,
	/\btee\b/i,
	/\btruncate\b/i,
	/\bdd\b/i,
	/\bshred\b/i,
	/(^|[^<])>(?!>)/,
	/>>/,
	/\bnpm\s+(install|uninstall|update|ci|link|publish)/i,
	/\byarn\s+(add|remove|install|publish)/i,
	/\bpnpm\s+(add|remove|install|publish)/i,
	/\bpip\s+(install|uninstall)/i,
	/\bapt(-get)?\s+(install|remove|purge|update|upgrade)/i,
	/\bbrew\s+(install|uninstall|upgrade)/i,
	/\bgit\s+(add|commit|push|pull|merge|rebase|reset|checkout|branch\s+-[dD]|stash|cherry-pick|revert|tag|init|clone)/i,
	/\bsudo\b/i,
	/\bsu\b/i,
	/\bkill\b/i,
	/\bpkill\b/i,
	/\bkillall\b/i,
	/\breboot\b/i,
	/\bshutdown\b/i,
	/\bsystemctl\s+(start|stop|restart|enable|disable)/i,
	/\bservice\s+\S+\s+(start|stop|restart)/i,
	/\b(vim?|nano|emacs|code|subl)\b/i,
];

// Safe read-only commands allowed in plan mode
const SAFE_PATTERNS = [
	/^\s*cat\b/,
	/^\s*head\b/,
	/^\s*tail\b/,
	/^\s*less\b/,
	/^\s*more\b/,
	/^\s*grep\b/,
	/^\s*find\b/,
	/^\s*ls\b/,
	/^\s*pwd\b/,
	/^\s*echo\b/,
	/^\s*printf\b/,
	/^\s*wc\b/,
	/^\s*sort\b/,
	/^\s*uniq\b/,
	/^\s*diff\b/,
	/^\s*file\b/,
	/^\s*stat\b/,
	/^\s*du\b/,
	/^\s*df\b/,
	/^\s*tree\b/,
	/^\s*which\b/,
	/^\s*whereis\b/,
	/^\s*type\b/,
	/^\s*env\b/,
	/^\s*printenv\b/,
	/^\s*uname\b/,
	/^\s*whoami\b/,
	/^\s*id\b/,
	/^\s*date\b/,
	/^\s*cal\b/,
	/^\s*uptime\b/,
	/^\s*ps\b/,
	/^\s*top\b/,
	/^\s*htop\b/,
	/^\s*free\b/,
	/^\s*git\s+(status|log|diff|show|branch|remote|config\s+--get)/i,
	/^\s*git\s+ls-/i,
	/^\s*npm\s+(list|ls|view|info|search|outdated|audit)/i,
	/^\s*yarn\s+(list|info|why|audit)/i,
	/^\s*node\s+--version/i,
	/^\s*python\s+--version/i,
	/^\s*curl\s/i,
	/^\s*wget\s+-O\s*-/i,
	/^\s*jq\b/,
	/^\s*sed\s+-n/i,
	/^\s*awk\b/,
	/^\s*rg\b/,
	/^\s*fd\b/,
	/^\s*bat\b/,
	/^\s*exa\b/,
];

export function isSafeCommand(command: string): boolean {
	const isDestructive = DESTRUCTIVE_PATTERNS.some((p) => p.test(command));
	const isSafe = SAFE_PATTERNS.some((p) => p.test(command));
	return !isDestructive && isSafe;
}

export interface TodoItem {
	step: number;
	text: string;
	completed: boolean;
}

export function cleanStepText(text: string): string {
	let cleaned = text
		.replace(/\*{1,2}([^*]+)\*{1,2}/g, "$1") // Remove bold/italic
		.replace(/`([^`]+)`/g, "$1") // Remove code
		.replace(
			/^(Use|Run|Execute|Create|Write|Read|Check|Verify|Update|Modify|Add|Remove|Delete|Install)\s+(the\s+)?/i,
			"",
		)
		.replace(/\s+/g, " ")
		.trim();

	if (cleaned.length > 0) {
		cleaned = cleaned.charAt(0).toUpperCase() + cleaned.slice(1);
	}
	if (cleaned.length > 50) {
		cleaned = `${cleaned.slice(0, 47)}...`;
	}
	return cleaned;
}

export function extractTodoItems(message: string): TodoItem[] {
	const items: TodoItem[] = [];
	const headerMatch = message.match(/\*{0,2}Plan:\*{0,2}\s*\n/i);
	if (!headerMatch) return items;

	const planSection = message.slice(message.indexOf(headerMatch[0]) + headerMatch[0].length);
	const numberedPattern = /^\s*(\d+)[.)]\s+\*{0,2}([^*\n]+)/gm;

	for (const match of planSection.matchAll(numberedPattern)) {
		const text = match[2]
			.trim()
			.replace(/\*{1,2}$/, "")
			.trim();
		if (text.length > 5 && !text.startsWith("`") && !text.startsWith("/") && !text.startsWith("-")) {
			const cleaned = cleanStepText(text);
			if (cleaned.length > 3) {
				items.push({ step: items.length + 1, text: cleaned, completed: false });
			}
		}
	}
	return items;
}

export function extractDoneSteps(message: string): number[] {
	const steps: number[] = [];
	for (const match of message.matchAll(/\[DONE:(\d+)\]/gi)) {
		const step = Number(match[1]);
		if (Number.isFinite(step)) steps.push(step);
	}
	return steps;
}

export function markCompletedSteps(text: string, items: TodoItem[]): number {
	const doneSteps = extractDoneSteps(text);
	for (const step of doneSteps) {
		const item = items.find((t) => t.step === step);
		if (item) item.completed = true;
	}
	return doneSteps.length;
}
```

### Detailed Annotations

#### `pi.registerFlag("plan", { ... })`

Registers a CLI flag (`--plan`) so the extension can be activated from the command line: `pi --plan`. On `session_start`, the flag value is read via `pi.getFlag("plan")`.

#### `pi.setActiveTools(toolNames)`

Restricts which tools the LLM can invoke. In plan mode, only read-only tools are available (`read`, `bash`, `grep`, `find`, `ls`, `questionnaire`). When plan mode is disabled, full tools are restored. This is the primary mechanism for enforcing read-only behavior.

#### `pi.on("tool_call", handler)` -- Blocking Tool Calls

The `tool_call` event fires before a tool executes. Returning `{ block: true, reason: "..." }` prevents execution and shows the reason to the user. Here it blocks destructive bash commands even though `bash` is in the allowed tool list -- the `isSafeCommand` allowlist provides fine-grained control.

#### `pi.on("context", handler)` -- Modifying Context

The `context` event fires before messages are sent to the LLM. Returning `{ messages: filteredMessages }` replaces the message list. Plan mode uses this to strip out stale plan-mode context messages when plan mode is no longer active, preventing confusion in the LLM's context window.

#### `pi.on("before_agent_start", handler)` -- Injecting System Messages

Fires before the agent begins processing. Returning `{ message: { customType, content, display } }` injects a message into the conversation. The `display: false` flag means this message is visible to the LLM but not shown in the TUI. This is how plan mode instructs the LLM about its current restrictions and expected output format.

#### `pi.sendMessage(options, { triggerTurn })` -- Message with Turn Control

The second argument controls whether the message triggers an LLM turn:
- `{ triggerTurn: true }` -- After sending the message, the LLM processes it and responds. Used when executing a plan.
- `{ triggerTurn: false }` -- The message is added to the conversation but the LLM does not respond. Used for status updates like "Plan Complete!".

#### `ctx.ui.setStatus(key, text | undefined)`

Sets or clears a status indicator in the TUI footer bar. Each extension gets a unique key. Passing `undefined` clears the status. Used here to show "plan" mode indicator or progress counts.

#### `ctx.ui.setWidget(key, lines | undefined)`

Displays a persistent widget above the editor (by default) showing the given lines array. Passing `undefined` removes it. Here it shows the todo checklist with completion state.

#### `pi.appendEntry(customType, data)`

Writes a custom entry to the session file for persistence. On session resume, `ctx.sessionManager.getEntries()` retrieves all entries, and the extension filters for its own entries by `customType === "plan-mode"` to restore state.

#### `ctx.ui.select(prompt, options)` / `ctx.ui.editor(prompt, initialContent)`

Interactive UI prompts:
- `select` shows a selection list and returns the chosen string (or `undefined` if cancelled).
- `editor` opens a text editor overlay and returns the edited text.

#### `pi.on("turn_end", handler)` / `pi.on("agent_end", handler)`

- `turn_end` fires after each individual LLM turn (one request-response cycle). Used to scan for `[DONE:n]` markers and update progress.
- `agent_end` fires when the agent finishes all turns (no more tool calls to process). Used to extract the plan from the final response and show the interactive menu.

#### `pi.registerShortcut(Key.ctrlAlt("p"), handler)`

Registers a keyboard shortcut. `Key.ctrlAlt("p")` creates the Ctrl+Alt+P combo. The handler receives `ctx` (no event).

#### `pi.registerCommand("plan", { description, handler })`

Registers a slash command `/plan`. The handler receives `(args, ctx)` where `args` is the text after the command name.

#### Session Resume Pattern

On `session_start`, the extension:
1. Checks CLI flags with `pi.getFlag("plan")`
2. Reads persisted entries from `ctx.sessionManager.getEntries()`
3. Finds the last entry with `customType === "plan-mode"`
4. Restores `planModeEnabled`, `todoItems`, and `executionMode`
5. Re-scans assistant messages after the last `plan-mode-execute` entry to rebuild completion state
6. Applies tool restrictions and updates the UI

---

## 3. Send User Message

**File:** `examples/extensions/send-user-message.ts`

This example demonstrates the difference between `pi.sendMessage()` (custom messages) and `pi.sendUserMessage()` (actual user messages), plus the `deliverAs` options for mid-stream delivery.

### Full Source

```typescript
/**
 * Send User Message Example
 *
 * Demonstrates pi.sendUserMessage() for sending user messages from extensions.
 * Unlike pi.sendMessage() which sends custom messages, sendUserMessage() sends
 * actual user messages that appear in the conversation as if typed by the user.
 *
 * Usage:
 *   /ask What is 2+2?     - Sends a user message (always triggers a turn)
 *   /steer Focus on X     - Sends while streaming with steer delivery
 *   /followup And then?   - Sends while streaming with followUp delivery
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI) {
	// Simple command that sends a user message
	pi.registerCommand("ask", {
		description: "Send a user message to the agent",
		handler: async (args, ctx) => {
			if (!args.trim()) {
				ctx.ui.notify("Usage: /ask <message>", "warning");
				return;
			}

			// sendUserMessage always triggers a turn when not streaming
			// If streaming, it will throw (no deliverAs specified)
			if (!ctx.isIdle()) {
				ctx.ui.notify("Agent is busy. Use /steer or /followup instead.", "warning");
				return;
			}

			pi.sendUserMessage(args);
		},
	});

	// Command that steers the agent mid-conversation
	pi.registerCommand("steer", {
		description: "Send a steering message (interrupts current processing)",
		handler: async (args, ctx) => {
			if (!args.trim()) {
				ctx.ui.notify("Usage: /steer <message>", "warning");
				return;
			}

			if (ctx.isIdle()) {
				// Not streaming, just send normally
				pi.sendUserMessage(args);
			} else {
				// Streaming - use steer to interrupt
				pi.sendUserMessage(args, { deliverAs: "steer" });
			}
		},
	});

	// Command that queues a follow-up message
	pi.registerCommand("followup", {
		description: "Queue a follow-up message (waits for current processing)",
		handler: async (args, ctx) => {
			if (!args.trim()) {
				ctx.ui.notify("Usage: /followup <message>", "warning");
				return;
			}

			if (ctx.isIdle()) {
				// Not streaming, just send normally
				pi.sendUserMessage(args);
			} else {
				// Streaming - queue as follow-up
				pi.sendUserMessage(args, { deliverAs: "followUp" });
				ctx.ui.notify("Follow-up queued", "info");
			}
		},
	});

	// Example with content array (text + images would go here)
	pi.registerCommand("askwith", {
		description: "Send a user message with structured content",
		handler: async (args, ctx) => {
			if (!args.trim()) {
				ctx.ui.notify("Usage: /askwith <message>", "warning");
				return;
			}

			if (!ctx.isIdle()) {
				ctx.ui.notify("Agent is busy", "warning");
				return;
			}

			// sendUserMessage accepts string or (TextContent | ImageContent)[]
			pi.sendUserMessage([
				{ type: "text", text: `User request: ${args}` },
				{ type: "text", text: "Please respond concisely." },
			]);
		},
	});
}
```

### Detailed Annotations

#### `pi.sendMessage()` vs `pi.sendUserMessage()`

| Feature | `sendMessage()` | `sendUserMessage()` |
|---|---|---|
| Message type | Custom message with `customType` | Actual user message (`role: "user"`) |
| Appears as | Extension-rendered custom block | User chat bubble |
| Triggers turn | Only if `{ triggerTurn: true }` | Always (when idle) |
| Mid-stream | Works with `triggerTurn: false` | Requires `deliverAs` option |
| Content format | `{ content: string, customType, details }` | `string` or `(TextContent \| ImageContent)[]` |

#### `deliverAs` Options

When the agent is actively streaming (not idle), `sendUserMessage` needs a delivery strategy:

- **`"steer"`** -- Interrupts the current LLM generation. The steering message is injected into the conversation context, causing the LLM to shift its response direction. Use this when you want to redirect the agent mid-thought.

- **`"followUp"`** -- Queues the message to be delivered after the current turn completes. The agent finishes its current response, then processes the follow-up as a new turn. Use this when you want to add a task without interrupting.

- **No `deliverAs`** (default) -- Throws an error if the agent is not idle. Always check `ctx.isIdle()` before calling without `deliverAs`.

#### `ctx.isIdle()`

Returns `true` when the agent is not currently streaming/processing. Always check this before calling `sendUserMessage()` without a `deliverAs` option.

#### Content Array Format

`sendUserMessage` accepts either a plain string or an array of content blocks:
```typescript
pi.sendUserMessage([
    { type: "text", text: "User request: ..." },
    { type: "text", text: "Please respond concisely." },
]);
```
This allows sending multimodal content (text + images) in a single user message.

---

## 4. Subagent

**File:** `examples/extensions/subagent/index.ts`

This is the most complex extension example. It registers a custom tool that spawns isolated `pi` subprocesses. The key patterns for UI/message control are in the rendering functions.

### Full Source

```typescript
/**
 * Subagent Tool - Delegate tasks to specialized agents
 *
 * Spawns a separate `pi` process for each subagent invocation,
 * giving it an isolated context window.
 *
 * Supports three modes:
 *   - Single: { agent: "name", task: "..." }
 *   - Parallel: { tasks: [{ agent: "name", task: "..." }, ...] }
 *   - Chain: { chain: [{ agent: "name", task: "... {previous} ..." }, ...] }
 *
 * Uses JSON mode to capture structured output from subagents.
 */

import { spawn } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import type { AgentToolResult } from "@mariozechner/pi-agent-core";
import type { Message } from "@mariozechner/pi-ai";
import { StringEnum } from "@mariozechner/pi-ai";
import { type ExtensionAPI, getMarkdownTheme, withFileMutationQueue } from "@mariozechner/pi-coding-agent";
import { Container, Markdown, Spacer, Text } from "@mariozechner/pi-tui";
import { Type } from "@sinclair/typebox";
import { type AgentConfig, type AgentScope, discoverAgents } from "./agents.js";

const MAX_PARALLEL_TASKS = 8;
const MAX_CONCURRENCY = 4;
const COLLAPSED_ITEM_COUNT = 10;

function formatTokens(count: number): string {
	if (count < 1000) return count.toString();
	if (count < 10000) return `${(count / 1000).toFixed(1)}k`;
	if (count < 1000000) return `${Math.round(count / 1000)}k`;
	return `${(count / 1000000).toFixed(1)}M`;
}

function formatUsageStats(
	usage: {
		input: number;
		output: number;
		cacheRead: number;
		cacheWrite: number;
		cost: number;
		contextTokens?: number;
		turns?: number;
	},
	model?: string,
): string {
	const parts: string[] = [];
	if (usage.turns) parts.push(`${usage.turns} turn${usage.turns > 1 ? "s" : ""}`);
	if (usage.input) parts.push(`↑${formatTokens(usage.input)}`);
	if (usage.output) parts.push(`↓${formatTokens(usage.output)}`);
	if (usage.cacheRead) parts.push(`R${formatTokens(usage.cacheRead)}`);
	if (usage.cacheWrite) parts.push(`W${formatTokens(usage.cacheWrite)}`);
	if (usage.cost) parts.push(`$${usage.cost.toFixed(4)}`);
	if (usage.contextTokens && usage.contextTokens > 0) {
		parts.push(`ctx:${formatTokens(usage.contextTokens)}`);
	}
	if (model) parts.push(model);
	return parts.join(" ");
}

function formatToolCall(
	toolName: string,
	args: Record<string, unknown>,
	themeFg: (color: any, text: string) => string,
): string {
	const shortenPath = (p: string) => {
		const home = os.homedir();
		return p.startsWith(home) ? `~${p.slice(home.length)}` : p;
	};

	switch (toolName) {
		case "bash": {
			const command = (args.command as string) || "...";
			const preview = command.length > 60 ? `${command.slice(0, 60)}...` : command;
			return themeFg("muted", "$ ") + themeFg("toolOutput", preview);
		}
		case "read": {
			const rawPath = (args.file_path || args.path || "...") as string;
			const filePath = shortenPath(rawPath);
			const offset = args.offset as number | undefined;
			const limit = args.limit as number | undefined;
			let text = themeFg("accent", filePath);
			if (offset !== undefined || limit !== undefined) {
				const startLine = offset ?? 1;
				const endLine = limit !== undefined ? startLine + limit - 1 : "";
				text += themeFg("warning", `:${startLine}${endLine ? `-${endLine}` : ""}`);
			}
			return themeFg("muted", "read ") + text;
		}
		case "write": {
			const rawPath = (args.file_path || args.path || "...") as string;
			const filePath = shortenPath(rawPath);
			const content = (args.content || "") as string;
			const lines = content.split("\n").length;
			let text = themeFg("muted", "write ") + themeFg("accent", filePath);
			if (lines > 1) text += themeFg("dim", ` (${lines} lines)`);
			return text;
		}
		case "edit": {
			const rawPath = (args.file_path || args.path || "...") as string;
			return themeFg("muted", "edit ") + themeFg("accent", shortenPath(rawPath));
		}
		case "ls": {
			const rawPath = (args.path || ".") as string;
			return themeFg("muted", "ls ") + themeFg("accent", shortenPath(rawPath));
		}
		case "find": {
			const pattern = (args.pattern || "*") as string;
			const rawPath = (args.path || ".") as string;
			return themeFg("muted", "find ") + themeFg("accent", pattern) + themeFg("dim", ` in ${shortenPath(rawPath)}`);
		}
		case "grep": {
			const pattern = (args.pattern || "") as string;
			const rawPath = (args.path || ".") as string;
			return (
				themeFg("muted", "grep ") +
				themeFg("accent", `/${pattern}/`) +
				themeFg("dim", ` in ${shortenPath(rawPath)}`)
			);
		}
		default: {
			const argsStr = JSON.stringify(args);
			const preview = argsStr.length > 50 ? `${argsStr.slice(0, 50)}...` : argsStr;
			return themeFg("accent", toolName) + themeFg("dim", ` ${preview}`);
		}
	}
}

interface UsageStats {
	input: number;
	output: number;
	cacheRead: number;
	cacheWrite: number;
	cost: number;
	contextTokens: number;
	turns: number;
}

interface SingleResult {
	agent: string;
	agentSource: "user" | "project" | "unknown";
	task: string;
	exitCode: number;
	messages: Message[];
	stderr: string;
	usage: UsageStats;
	model?: string;
	stopReason?: string;
	errorMessage?: string;
	step?: number;
}

interface SubagentDetails {
	mode: "single" | "parallel" | "chain";
	agentScope: AgentScope;
	projectAgentsDir: string | null;
	results: SingleResult[];
}

function getFinalOutput(messages: Message[]): string {
	for (let i = messages.length - 1; i >= 0; i--) {
		const msg = messages[i];
		if (msg.role === "assistant") {
			for (const part of msg.content) {
				if (part.type === "text") return part.text;
			}
		}
	}
	return "";
}

type DisplayItem = { type: "text"; text: string } | { type: "toolCall"; name: string; args: Record<string, any> };

function getDisplayItems(messages: Message[]): DisplayItem[] {
	const items: DisplayItem[] = [];
	for (const msg of messages) {
		if (msg.role === "assistant") {
			for (const part of msg.content) {
				if (part.type === "text") items.push({ type: "text", text: part.text });
				else if (part.type === "toolCall") items.push({ type: "toolCall", name: part.name, args: part.arguments });
			}
		}
	}
	return items;
}

async function mapWithConcurrencyLimit<TIn, TOut>(
	items: TIn[],
	concurrency: number,
	fn: (item: TIn, index: number) => Promise<TOut>,
): Promise<TOut[]> {
	if (items.length === 0) return [];
	const limit = Math.max(1, Math.min(concurrency, items.length));
	const results: TOut[] = new Array(items.length);
	let nextIndex = 0;
	const workers = new Array(limit).fill(null).map(async () => {
		while (true) {
			const current = nextIndex++;
			if (current >= items.length) return;
			results[current] = await fn(items[current], current);
		}
	});
	await Promise.all(workers);
	return results;
}

async function writePromptToTempFile(agentName: string, prompt: string): Promise<{ dir: string; filePath: string }> {
	const tmpDir = await fs.promises.mkdtemp(path.join(os.tmpdir(), "pi-subagent-"));
	const safeName = agentName.replace(/[^\w.-]+/g, "_");
	const filePath = path.join(tmpDir, `prompt-${safeName}.md`);
	await withFileMutationQueue(filePath, async () => {
		await fs.promises.writeFile(filePath, prompt, { encoding: "utf-8", mode: 0o600 });
	});
	return { dir: tmpDir, filePath };
}

function getPiInvocation(args: string[]): { command: string; args: string[] } {
	const currentScript = process.argv[1];
	if (currentScript && fs.existsSync(currentScript)) {
		return { command: process.execPath, args: [currentScript, ...args] };
	}

	const execName = path.basename(process.execPath).toLowerCase();
	const isGenericRuntime = /^(node|bun)(\.exe)?$/.test(execName);
	if (!isGenericRuntime) {
		return { command: process.execPath, args };
	}

	return { command: "pi", args };
}

type OnUpdateCallback = (partial: AgentToolResult<SubagentDetails>) => void;

async function runSingleAgent(
	defaultCwd: string,
	agents: AgentConfig[],
	agentName: string,
	task: string,
	cwd: string | undefined,
	step: number | undefined,
	signal: AbortSignal | undefined,
	onUpdate: OnUpdateCallback | undefined,
	makeDetails: (results: SingleResult[]) => SubagentDetails,
): Promise<SingleResult> {
	const agent = agents.find((a) => a.name === agentName);

	if (!agent) {
		const available = agents.map((a) => `"${a.name}"`).join(", ") || "none";
		return {
			agent: agentName,
			agentSource: "unknown",
			task,
			exitCode: 1,
			messages: [],
			stderr: `Unknown agent: "${agentName}". Available agents: ${available}.`,
			usage: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0, cost: 0, contextTokens: 0, turns: 0 },
			step,
		};
	}

	const args: string[] = ["--mode", "json", "-p", "--no-session"];
	if (agent.model) args.push("--model", agent.model);
	if (agent.tools && agent.tools.length > 0) args.push("--tools", agent.tools.join(","));

	let tmpPromptDir: string | null = null;
	let tmpPromptPath: string | null = null;

	const currentResult: SingleResult = {
		agent: agentName,
		agentSource: agent.source,
		task,
		exitCode: 0,
		messages: [],
		stderr: "",
		usage: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0, cost: 0, contextTokens: 0, turns: 0 },
		model: agent.model,
		step,
	};

	const emitUpdate = () => {
		if (onUpdate) {
			onUpdate({
				content: [{ type: "text", text: getFinalOutput(currentResult.messages) || "(running...)" }],
				details: makeDetails([currentResult]),
			});
		}
	};

	try {
		if (agent.systemPrompt.trim()) {
			const tmp = await writePromptToTempFile(agent.name, agent.systemPrompt);
			tmpPromptDir = tmp.dir;
			tmpPromptPath = tmp.filePath;
			args.push("--append-system-prompt", tmpPromptPath);
		}

		args.push(`Task: ${task}`);
		let wasAborted = false;

		const exitCode = await new Promise<number>((resolve) => {
			const invocation = getPiInvocation(args);
			const proc = spawn(invocation.command, invocation.args, {
				cwd: cwd ?? defaultCwd,
				shell: false,
				stdio: ["ignore", "pipe", "pipe"],
			});
			let buffer = "";

			const processLine = (line: string) => {
				if (!line.trim()) return;
				let event: any;
				try {
					event = JSON.parse(line);
				} catch {
					return;
				}

				if (event.type === "message_end" && event.message) {
					const msg = event.message as Message;
					currentResult.messages.push(msg);

					if (msg.role === "assistant") {
						currentResult.usage.turns++;
						const usage = msg.usage;
						if (usage) {
							currentResult.usage.input += usage.input || 0;
							currentResult.usage.output += usage.output || 0;
							currentResult.usage.cacheRead += usage.cacheRead || 0;
							currentResult.usage.cacheWrite += usage.cacheWrite || 0;
							currentResult.usage.cost += usage.cost?.total || 0;
							currentResult.usage.contextTokens = usage.totalTokens || 0;
						}
						if (!currentResult.model && msg.model) currentResult.model = msg.model;
						if (msg.stopReason) currentResult.stopReason = msg.stopReason;
						if (msg.errorMessage) currentResult.errorMessage = msg.errorMessage;
					}
					emitUpdate();
				}

				if (event.type === "tool_result_end" && event.message) {
					currentResult.messages.push(event.message as Message);
					emitUpdate();
				}
			};

			proc.stdout.on("data", (data) => {
				buffer += data.toString();
				const lines = buffer.split("\n");
				buffer = lines.pop() || "";
				for (const line of lines) processLine(line);
			});

			proc.stderr.on("data", (data) => {
				currentResult.stderr += data.toString();
			});

			proc.on("close", (code) => {
				if (buffer.trim()) processLine(buffer);
				resolve(code ?? 0);
			});

			proc.on("error", () => {
				resolve(1);
			});

			if (signal) {
				const killProc = () => {
					wasAborted = true;
					proc.kill("SIGTERM");
					setTimeout(() => {
						if (!proc.killed) proc.kill("SIGKILL");
					}, 5000);
				};
				if (signal.aborted) killProc();
				else signal.addEventListener("abort", killProc, { once: true });
			}
		});

		currentResult.exitCode = exitCode;
		if (wasAborted) throw new Error("Subagent was aborted");
		return currentResult;
	} finally {
		if (tmpPromptPath)
			try {
				fs.unlinkSync(tmpPromptPath);
			} catch {
				/* ignore */
			}
		if (tmpPromptDir)
			try {
				fs.rmdirSync(tmpPromptDir);
			} catch {
				/* ignore */
			}
	}
}

// ... (TaskItem, ChainItem, SubagentParams schema definitions omitted for brevity -- see full source above)

export default function (pi: ExtensionAPI) {
	pi.registerTool({
		name: "subagent",
		label: "Subagent",
		description: [
			"Delegate tasks to specialized subagents with isolated context.",
			"Modes: single (agent + task), parallel (tasks array), chain (sequential with {previous} placeholder).",
			'Default agent scope is "user" (from ~/.pi/agent/agents).',
			'To enable project-local agents in .pi/agents, set agentScope: "both" (or "project").',
		].join(" "),
		parameters: SubagentParams,

		async execute(_toolCallId, params, signal, onUpdate, ctx) {
			// ... (full execution logic -- see complete source above)
		},

		renderCall(args, theme, _context) {
			const scope: AgentScope = args.agentScope ?? "user";
			if (args.chain && args.chain.length > 0) {
				let text =
					theme.fg("toolTitle", theme.bold("subagent ")) +
					theme.fg("accent", `chain (${args.chain.length} steps)`) +
					theme.fg("muted", ` [${scope}]`);
				for (let i = 0; i < Math.min(args.chain.length, 3); i++) {
					const step = args.chain[i];
					const cleanTask = step.task.replace(/\{previous\}/g, "").trim();
					const preview = cleanTask.length > 40 ? `${cleanTask.slice(0, 40)}...` : cleanTask;
					text +=
						"\n  " +
						theme.fg("muted", `${i + 1}.`) +
						" " +
						theme.fg("accent", step.agent) +
						theme.fg("dim", ` ${preview}`);
				}
				if (args.chain.length > 3) text += `\n  ${theme.fg("muted", `... +${args.chain.length - 3} more`)}`;
				return new Text(text, 0, 0);
			}
			if (args.tasks && args.tasks.length > 0) {
				let text =
					theme.fg("toolTitle", theme.bold("subagent ")) +
					theme.fg("accent", `parallel (${args.tasks.length} tasks)`) +
					theme.fg("muted", ` [${scope}]`);
				for (const t of args.tasks.slice(0, 3)) {
					const preview = t.task.length > 40 ? `${t.task.slice(0, 40)}...` : t.task;
					text += `\n  ${theme.fg("accent", t.agent)}${theme.fg("dim", ` ${preview}`)}`;
				}
				if (args.tasks.length > 3) text += `\n  ${theme.fg("muted", `... +${args.tasks.length - 3} more`)}`;
				return new Text(text, 0, 0);
			}
			const agentName = args.agent || "...";
			const preview = args.task ? (args.task.length > 60 ? `${args.task.slice(0, 60)}...` : args.task) : "...";
			let text =
				theme.fg("toolTitle", theme.bold("subagent ")) +
				theme.fg("accent", agentName) +
				theme.fg("muted", ` [${scope}]`);
			text += `\n  ${theme.fg("dim", preview)}`;
			return new Text(text, 0, 0);
		},

		renderResult(result, { expanded }, theme, _context) {
			const details = result.details as SubagentDetails | undefined;
			if (!details || details.results.length === 0) {
				const text = result.content[0];
				return new Text(text?.type === "text" ? text.text : "(no output)", 0, 0);
			}

			const mdTheme = getMarkdownTheme();

			// ... (renderDisplayItems helper)

			if (details.mode === "single" && details.results.length === 1) {
				const r = details.results[0];
				const isError = r.exitCode !== 0 || r.stopReason === "error" || r.stopReason === "aborted";
				const icon = isError ? theme.fg("error", "✗") : theme.fg("success", "✓");
				const displayItems = getDisplayItems(r.messages);
				const finalOutput = getFinalOutput(r.messages);

				if (expanded) {
					const container = new Container();
					let header = `${icon} ${theme.fg("toolTitle", theme.bold(r.agent))}${theme.fg("muted", ` (${r.agentSource})`)}`;
					if (isError && r.stopReason) header += ` ${theme.fg("error", `[${r.stopReason}]`)}`;
					container.addChild(new Text(header, 0, 0));
					if (isError && r.errorMessage)
						container.addChild(new Text(theme.fg("error", `Error: ${r.errorMessage}`), 0, 0));
					container.addChild(new Spacer(1));
					container.addChild(new Text(theme.fg("muted", "─── Task ───"), 0, 0));
					container.addChild(new Text(theme.fg("dim", r.task), 0, 0));
					container.addChild(new Spacer(1));
					container.addChild(new Text(theme.fg("muted", "─── Output ───"), 0, 0));
					// ... (display items and markdown rendering)
					if (finalOutput) {
						container.addChild(new Spacer(1));
						container.addChild(new Markdown(finalOutput.trim(), 0, 0, mdTheme));
					}
					const usageStr = formatUsageStats(r.usage, r.model);
					if (usageStr) {
						container.addChild(new Spacer(1));
						container.addChild(new Text(theme.fg("dim", usageStr), 0, 0));
					}
					return container;
				}

				// Collapsed view
				let text = `${icon} ${theme.fg("toolTitle", theme.bold(r.agent))}`;
				// ... (truncated display items)
				return new Text(text, 0, 0);
			}

			// ... (parallel and chain rendering -- similar patterns)
		},
	});
}
```

### Key Patterns Annotated

#### `pi.registerTool({ renderCall, renderResult, execute, onUpdate })`

Custom tools have four key functions:

1. **`execute(toolCallId, params, signal, onUpdate, ctx)`** -- The actual tool logic. Returns `AgentToolResult` with `content` (array of text/image blocks) and optional `details` (arbitrary data for the renderer).

2. **`renderCall(args, theme, context)`** -- Controls how the tool invocation appears in the TUI *before* results are available. Returns a TUI component (`Text`, `Container`, etc.). Receives the raw tool arguments.

3. **`renderResult(result, { expanded, isPartial }, theme, context)`** -- Controls how the tool result appears. Receives the full `AgentToolResult` including `details`. The `expanded` boolean toggles between summary and full views. `isPartial` is `true` during streaming.

4. **`onUpdate` callback** -- Called from within `execute` to stream partial results. The TUI re-renders `renderResult` with `isPartial: true` each time `onUpdate` is called.

#### Container / Text / Markdown / Spacer Components

These are the TUI layout primitives from `@mariozechner/pi-tui`:

- **`Container()`** -- A vertical layout container. Children are stacked top-to-bottom. Use `container.addChild(child)` to add elements.
- **`Text(content, x, y)`** -- A text node with themed/styled content. Position (x, y) is relative to parent.
- **`Markdown(content, x, y, mdTheme)`** -- Renders markdown content with syntax highlighting. Use `getMarkdownTheme()` from the coding-agent package.
- **`Spacer(lines)`** -- Adds vertical spacing between elements.

#### The Expanded View Pattern (Tool Results)

```typescript
renderResult(result, { expanded }, theme, _context) {
    if (expanded) {
        // Full detail view with Container layout
        const container = new Container();
        container.addChild(new Text(header, 0, 0));
        container.addChild(new Spacer(1));
        container.addChild(new Markdown(fullOutput, 0, 0, mdTheme));
        return container;
    }

    // Collapsed single-line summary
    return new Text(summaryLine, 0, 0);
}
```

This is the canonical pattern: collapsed shows a one-line summary, expanded uses a `Container` with full detail including markdown-rendered output.

#### Streaming Updates with `onUpdate`

```typescript
const emitUpdate = () => {
    if (onUpdate) {
        onUpdate({
            content: [{ type: "text", text: getFinalOutput(currentResult.messages) || "(running...)" }],
            details: makeDetails([currentResult]),
        });
    }
};
```

Each call to `onUpdate` causes `renderResult` to be called again with `isPartial: true`. The `details` object is passed through so the renderer has access to the latest state.

---

## 5. Input Transform

**File:** `examples/extensions/input-transform.ts`

This example demonstrates the `input` event for intercepting and modifying user input before it reaches the LLM.

### Full Source

```typescript
/**
 * Input Transform Example - demonstrates the `input` event for intercepting user input.
 *
 * Start pi with this extension:
 *   pi -e ./examples/extensions/input-transform.ts
 *
 * Then type these inside pi:
 *   ?quick What is TypeScript?  → "Respond briefly: What is TypeScript?"
 *   ping                        → "pong" (instant, no LLM)
 *   time                        → current time (instant, no LLM)
 */
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI) {
	pi.on("input", async (event, ctx) => {
		// Source-based logic: skip processing for extension-injected messages
		if (event.source === "extension") {
			return { action: "continue" };
		}

		// Transform: ?quick prefix for brief responses
		if (event.text.startsWith("?quick ")) {
			const query = event.text.slice(7).trim();
			if (!query) {
				ctx.ui.notify("Usage: ?quick <question>", "warning");
				return { action: "handled" };
			}
			return { action: "transform", text: `Respond briefly in 1-2 sentences: ${query}` };
		}

		// Handle: instant responses without LLM (extension shows its own feedback)
		if (event.text.toLowerCase() === "ping") {
			ctx.ui.notify("pong", "info");
			return { action: "handled" };
		}
		if (event.text.toLowerCase() === "time") {
			ctx.ui.notify(new Date().toLocaleString(), "info");
			return { action: "handled" };
		}

		return { action: "continue" };
	});
}
```

### Detailed Annotations

#### `pi.on("input", handler)` -- The Input Event

Fires when the user submits text (presses Enter in the editor). The handler receives:
- `event.text` -- The raw user input string.
- `event.source` -- Where the input came from: `"user"` (typed by user), `"extension"` (injected by `sendUserMessage`), or other sources.

#### The Three Return Actions

| Action | Behavior | Use Case |
|---|---|---|
| `{ action: "continue" }` | Input passes through unmodified to the LLM | Default pass-through; also used to skip processing for extension-injected messages |
| `{ action: "transform", text: "..." }` | Input is replaced with the new text before reaching the LLM | Shorthand expansions, prefix commands, prompt wrapping |
| `{ action: "handled" }` | Input is consumed by the extension; no LLM turn occurs | Instant local commands (ping, time), validation errors |

#### The `event.source` Field

**Critical for avoiding infinite loops.** When an extension calls `pi.sendUserMessage(text)`, that message also passes through the `input` event. Check `event.source === "extension"` and return `{ action: "continue" }` to avoid re-processing extension-injected messages.

#### Event Flow

```
User types "?quick What is TS?"
  → input event fires
  → Handler returns { action: "transform", text: "Respond briefly in 1-2 sentences: What is TS?" }
  → Transformed text is sent to the LLM as the user message

User types "ping"
  → input event fires
  → Handler calls ctx.ui.notify("pong") and returns { action: "handled" }
  → No LLM turn; user sees "pong" notification
```

---

## 6. File Trigger

**File:** `examples/extensions/file-trigger.ts`

This example demonstrates how external systems can inject messages into the conversation by writing to a trigger file.

### Full Source

```typescript
/**
 * File Trigger Extension
 *
 * Watches a trigger file and injects its contents into the conversation.
 * Useful for external systems to send messages to the agent.
 *
 * Usage:
 *   echo "Run the tests" > /tmp/agent-trigger.txt
 */

import * as fs from "node:fs";
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI) {
	pi.on("session_start", async (_event, ctx) => {
		const triggerFile = "/tmp/agent-trigger.txt";

		fs.watch(triggerFile, () => {
			try {
				const content = fs.readFileSync(triggerFile, "utf-8").trim();
				if (content) {
					pi.sendMessage(
						{
							customType: "file-trigger",
							content: `External trigger: ${content}`,
							display: true,
						},
						{ triggerTurn: true }, // triggerTurn - get LLM to respond
					);
					fs.writeFileSync(triggerFile, ""); // Clear after reading
				}
			} catch {
				// File might not exist yet
			}
		});

		if (ctx.hasUI) {
			ctx.ui.notify(`Watching ${triggerFile}`, "info");
		}
	});
}
```

### Detailed Annotations

#### External Event Injection Pattern

This is the canonical pattern for external-to-agent communication:

1. **Watch for external signal** -- `fs.watch(triggerFile, callback)` monitors a file for changes.
2. **Read the signal content** -- `fs.readFileSync(triggerFile, "utf-8")` reads what the external system wrote.
3. **Inject into conversation** -- `pi.sendMessage({ ... }, { triggerTurn: true })` adds the message and triggers an LLM response.
4. **Clean up** -- `fs.writeFileSync(triggerFile, "")` clears the file to prevent re-triggering.

#### `pi.sendMessage(options, { triggerTurn: true })`

The key difference from the message-renderer example: `triggerTurn: true` causes the LLM to process the message and respond. This is what makes external triggers actually drive agent behavior.

#### `pi.on("session_start", handler)` Setup Pattern

File watchers and other long-lived resources are initialized in the `session_start` event. This ensures they are created once when the session begins and persist for the session lifetime.

#### `ctx.hasUI`

Check this before calling `ctx.ui.*` methods. In headless/non-interactive mode, `ctx.hasUI` is `false` and UI calls would fail.

---

## 7. Event Bus

**File:** `examples/extensions/event-bus.ts`

This example demonstrates `pi.events` for inter-extension communication.

### Full Source

```typescript
/**
 * Inter-extension event bus example.
 *
 * Shows pi.events for communication between extensions. One extension
 * can emit events that other extensions listen to.
 *
 * Usage: /emit [event-name] [data] - emit an event on the bus
 */

import type { ExtensionAPI, ExtensionContext } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI) {
	// Store ctx for use in event handler
	let currentCtx: ExtensionContext | undefined;

	pi.on("session_start", async (_event, ctx) => {
		currentCtx = ctx;
	});

	// Listen for events from other extensions
	pi.events.on("my:notification", (data) => {
		const { message, from } = data as { message: string; from: string };
		currentCtx?.ui.notify(`Event from ${from}: ${message}`, "info");
	});

	// Command to emit events (emits "my:notification" which the listener above receives)
	pi.registerCommand("emit", {
		description: "Emit my:notification event (usage: /emit message)",
		handler: async (args, _ctx) => {
			const message = args.trim() || "hello";
			pi.events.emit("my:notification", { message, from: "/emit command" });
			// Listener above will show the notification
		},
	});

	// Example: emit on session start
	pi.on("session_start", async () => {
		pi.events.emit("my:notification", {
			message: "Session started",
			from: "event-bus-example",
		});
	});
}
```

### Detailed Annotations

#### `pi.events.on(eventName, handler)` / `pi.events.emit(eventName, data)`

The event bus is a simple pub/sub system shared across all loaded extensions:
- **`pi.events.on(name, handler)`** -- Subscribe to events with a given name. The handler receives the arbitrary data payload.
- **`pi.events.emit(name, data)`** -- Broadcast an event to all subscribers. Data is any JSON-serializable value.

#### Namespacing Convention

Use a namespace prefix for event names (e.g., `"my:notification"`, `"plan:completed"`) to avoid collisions between extensions.

#### Storing `ctx` for Event Handlers

The event bus handlers run outside the normal event lifecycle, so they do not receive `ctx` as an argument. The pattern is to capture `ctx` from `session_start` into a closure variable (`currentCtx`) and use it in the event handler. This is necessary because `pi.events.on()` is called during extension initialization, before any session exists.

---

## 8. Dynamic Tools

**File:** `examples/extensions/dynamic-tools.ts`

This example demonstrates registering tools dynamically at runtime.

### Full Source

```typescript
/**
 * Dynamic Tools Extension
 *
 * Demonstrates registering tools after session initialization.
 *
 * - Registers one tool during session_start
 * - Registers additional tools at runtime via /add-echo-tool <name>
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Type } from "@sinclair/typebox";

const ECHO_PARAMS = Type.Object({
	message: Type.String({ description: "Message to echo" }),
});

function normalizeToolName(input: string): string | undefined {
	const trimmed = input.trim().toLowerCase();
	if (!trimmed) return undefined;
	if (!/^[a-z0-9_]+$/.test(trimmed)) return undefined;
	return trimmed;
}

export default function dynamicToolsExtension(pi: ExtensionAPI) {
	const registeredToolNames = new Set<string>();

	const registerEchoTool = (name: string, label: string, prefix: string): boolean => {
		if (registeredToolNames.has(name)) {
			return false;
		}

		registeredToolNames.add(name);
		pi.registerTool({
			name,
			label,
			description: `Echo a message with prefix: ${prefix}`,
			promptSnippet: `Echo back user-provided text with ${prefix.trim()} prefix`,
			promptGuidelines: ["Use this tool when the user asks for exact echo output."],
			parameters: ECHO_PARAMS,
			async execute(_toolCallId, params) {
				return {
					content: [{ type: "text", text: `${prefix}${params.message}` }],
					details: { tool: name, prefix },
				};
			},
		});

		return true;
	};

	pi.on("session_start", (_event, ctx) => {
		registerEchoTool("echo_session", "Echo Session", "[session] ");
		ctx.ui.notify("Registered dynamic tool: echo_session", "info");
	});

	pi.registerCommand("add-echo-tool", {
		description: "Register a new echo tool dynamically: /add-echo-tool <tool_name>",
		handler: async (args, ctx) => {
			const toolName = normalizeToolName(args);
			if (!toolName) {
				ctx.ui.notify("Usage: /add-echo-tool <tool_name> (lowercase, numbers, underscores)", "warning");
				return;
			}

			const created = registerEchoTool(toolName, `Echo ${toolName}`, `[${toolName}] `);
			if (!created) {
				ctx.ui.notify(`Tool already registered: ${toolName}`, "warning");
				return;
			}

			ctx.ui.notify(`Registered dynamic tool: ${toolName}`, "info");
		},
	});
}
```

### Detailed Annotations

#### `pi.registerTool({ name, label, description, parameters, execute, ... })`

Registers a tool that the LLM can invoke. Key fields:
- **`name`** -- The tool identifier used in LLM tool calls. Must be unique (or overrides built-in if same name).
- **`label`** -- Human-readable name shown in the TUI.
- **`description`** -- Sent to the LLM so it knows when to use the tool.
- **`promptSnippet`** -- Additional context injected into the system prompt about this tool.
- **`promptGuidelines`** -- Array of usage guidelines injected into the system prompt.
- **`parameters`** -- TypeBox schema defining the tool's input parameters.
- **`execute(toolCallId, params, signal, onUpdate, ctx)`** -- The tool implementation.

#### Dynamic Registration

Tools can be registered at any time -- during initialization, in `session_start`, or in response to user commands. The LLM will see newly registered tools on its next turn. This enables workflows where the available tools change based on context.

#### TypeBox Schemas

Parameters use `@sinclair/typebox` for JSON Schema generation:
```typescript
const ECHO_PARAMS = Type.Object({
    message: Type.String({ description: "Message to echo" }),
});
```
This generates the JSON Schema that the LLM uses to understand the tool's expected input format.

---

## 9. Tool Override

**File:** `examples/extensions/tool-override.ts`

This example demonstrates overriding built-in tools to add logging, access control, or custom behavior.

### Full Source

```typescript
/**
 * Tool Override Example - Demonstrates overriding built-in tools
 *
 * Extensions can register tools with the same name as built-in tools to replace them.
 * This is useful for:
 * - Adding logging or auditing to tool calls
 * - Implementing access control or sandboxing
 * - Routing tool calls to remote systems (e.g., pi-ssh-remote)
 * - Modifying tool behavior for specific workflows
 *
 * This example overrides the `read` tool to:
 * 1. Log all file access to a log file
 * 2. Block access to sensitive paths (e.g., .env files)
 * 3. Delegate to the original read implementation for allowed files
 *
 * Since no custom renderCall/renderResult are provided, the built-in renderer
 * is used automatically (syntax highlighting, line numbers, truncation warnings).
 *
 * Usage:
 *   pi -e ./tool-override.ts
 */

import type { TextContent } from "@mariozechner/pi-ai";
import { type ExtensionAPI, getAgentDir, withFileMutationQueue } from "@mariozechner/pi-coding-agent";
import { Type } from "@sinclair/typebox";
import { constants, readFileSync } from "fs";
import { access, appendFile, readFile } from "fs/promises";
import { join, resolve } from "path";

const LOG_FILE = join(getAgentDir(), "read-access.log");

// Paths that are blocked from reading
const BLOCKED_PATTERNS = [
	/\.env$/,
	/\.env\..+$/,
	/secrets?\.(json|yaml|yml|toml)$/i,
	/credentials?\.(json|yaml|yml|toml)$/i,
	/\/\.ssh\//,
	/\/\.aws\//,
	/\/\.gnupg\//,
];

function isBlockedPath(path: string): boolean {
	return BLOCKED_PATTERNS.some((pattern) => pattern.test(path));
}

async function logAccess(path: string, allowed: boolean, reason?: string) {
	const timestamp = new Date().toISOString();
	const status = allowed ? "ALLOWED" : "BLOCKED";
	const msg = reason ? ` (${reason})` : "";
	const line = `[${timestamp}] ${status}: ${path}${msg}\n`;

	try {
		await withFileMutationQueue(LOG_FILE, async () => {
			await appendFile(LOG_FILE, line);
		});
	} catch {
		// Ignore logging errors
	}
}

const readSchema = Type.Object({
	path: Type.String({ description: "Path to the file to read (relative or absolute)" }),
	offset: Type.Optional(Type.Number({ description: "Line number to start reading from (1-indexed)" })),
	limit: Type.Optional(Type.Number({ description: "Maximum number of lines to read" })),
});

export default function (pi: ExtensionAPI) {
	pi.registerTool({
		name: "read", // Same name as built-in - this will override it
		label: "read (audited)",
		description:
			"Read the contents of a file with access logging. Some sensitive paths (.env, secrets, credentials) are blocked.",
		parameters: readSchema,

		async execute(_toolCallId, params, _signal, _onUpdate, ctx) {
			const { path, offset, limit } = params;
			const absolutePath = resolve(ctx.cwd, path);

			// Check if path is blocked
			if (isBlockedPath(absolutePath)) {
				await logAccess(absolutePath, false, "matches blocked pattern");
				return {
					content: [
						{
							type: "text",
							text: `Access denied: "${path}" matches a blocked pattern (sensitive file).`,
						},
					],
					details: { blocked: true },
				};
			}

			// Log allowed access
			await logAccess(absolutePath, true);

			// Perform the actual read
			try {
				await access(absolutePath, constants.R_OK);
				const content = await readFile(absolutePath, "utf-8");
				const lines = content.split("\n");

				const startLine = offset ? Math.max(0, offset - 1) : 0;
				const endLine = limit ? startLine + limit : lines.length;
				const selectedLines = lines.slice(startLine, endLine);

				let text = selectedLines.join("\n");
				const maxBytes = 50 * 1024;
				if (Buffer.byteLength(text, "utf-8") > maxBytes) {
					text = `${text.slice(0, maxBytes)}\n\n[Output truncated at 50KB]`;
				}

				return {
					content: [{ type: "text", text }] as TextContent[],
					details: { lines: lines.length },
				};
			} catch (error: any) {
				return {
					content: [{ type: "text", text: `Error reading file: ${error.message}` }] as TextContent[],
					details: { error: true },
				};
			}
		},

		// No renderCall/renderResult - uses built-in renderer automatically
	});

	pi.registerCommand("read-log", {
		description: "View the file access log",
		handler: async (_args, ctx) => {
			try {
				const log = readFileSync(LOG_FILE, "utf-8");
				const lines = log.trim().split("\n").slice(-20);
				ctx.ui.notify(`Recent file access:\n${lines.join("\n")}`, "info");
			} catch {
				ctx.ui.notify("No access log found", "info");
			}
		},
	});
}
```

### Detailed Annotations

#### Overriding Built-in Tools

Registering a tool with `name: "read"` (same as the built-in) replaces the built-in entirely. The extension's `execute` function runs instead. This is the mechanism for:
- **Auditing** -- Log every tool invocation.
- **Access control** -- Block certain paths or operations.
- **Remoting** -- Forward tool calls to a remote machine via SSH.
- **Sandboxing** -- Run operations in a restricted environment.

#### Omitting `renderCall` / `renderResult`

When no custom renderers are provided, the built-in renderer is used automatically. This means the overridden `read` tool still gets syntax highlighting, line numbers, and truncation warnings -- only the execution logic changes.

#### `withFileMutationQueue(path, fn)`

A utility from Pi that serializes file writes to avoid race conditions. Important when multiple extensions or concurrent tool calls might write to the same file.

#### `getAgentDir()`

Returns the path to `~/.pi/agent/`, the standard location for agent-level data files.

---

## 10. Built-in Tool Renderer

**File:** `examples/extensions/built-in-tool-renderer.ts`

This example shows how to override the rendering of built-in tools without changing their behavior -- the inverse of tool-override.ts.

### Full Source

```typescript
/**
 * Built-in Tool Renderer Example - Custom rendering for built-in tools
 *
 * Demonstrates how to override the rendering of built-in tools (read, bash,
 * edit, write) without changing their behavior. Each tool is re-registered
 * with the same name, delegating execution to the original implementation
 * while providing compact custom renderCall/renderResult functions.
 *
 * How it works:
 * - registerTool() with the same name as a built-in replaces it entirely
 * - We create instances of the original tools via createReadTool(), etc.
 *   and delegate execute() to them
 * - renderCall() controls what's shown when the tool is invoked
 * - renderResult() controls what's shown after execution completes
 * - The `expanded` flag in renderResult indicates whether the user has
 *   toggled the tool output open (via ctrl+e or clicking)
 */

import type { BashToolDetails, EditToolDetails, ExtensionAPI, ReadToolDetails } from "@mariozechner/pi-coding-agent";
import { createBashTool, createEditTool, createReadTool, createWriteTool } from "@mariozechner/pi-coding-agent";
import { Text } from "@mariozechner/pi-tui";

export default function (pi: ExtensionAPI) {
	const cwd = process.cwd();

	// --- Read tool: show path and line count ---
	const originalRead = createReadTool(cwd);
	pi.registerTool({
		name: "read",
		label: "read",
		description: originalRead.description,
		parameters: originalRead.parameters,

		async execute(toolCallId, params, signal, onUpdate) {
			return originalRead.execute(toolCallId, params, signal, onUpdate);
		},

		renderCall(args, theme, _context) {
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

		renderResult(result, { expanded, isPartial }, theme, _context) {
			if (isPartial) return new Text(theme.fg("warning", "Reading..."), 0, 0);

			const details = result.details as ReadToolDetails | undefined;
			const content = result.content[0];

			if (content?.type === "image") {
				return new Text(theme.fg("success", "Image loaded"), 0, 0);
			}

			if (content?.type !== "text") {
				return new Text(theme.fg("error", "No content"), 0, 0);
			}

			const lineCount = content.text.split("\n").length;
			let text = theme.fg("success", `${lineCount} lines`);

			if (details?.truncation?.truncated) {
				text += theme.fg("warning", ` (truncated from ${details.truncation.totalLines})`);
			}

			if (expanded) {
				const lines = content.text.split("\n").slice(0, 15);
				for (const line of lines) {
					text += `\n${theme.fg("dim", line)}`;
				}
				if (lineCount > 15) {
					text += `\n${theme.fg("muted", `... ${lineCount - 15} more lines`)}`;
				}
			}

			return new Text(text, 0, 0);
		},
	});

	// --- Bash tool: show command and exit code ---
	const originalBash = createBashTool(cwd);
	pi.registerTool({
		name: "bash",
		label: "bash",
		description: originalBash.description,
		parameters: originalBash.parameters,

		async execute(toolCallId, params, signal, onUpdate) {
			return originalBash.execute(toolCallId, params, signal, onUpdate);
		},

		renderCall(args, theme, _context) {
			let text = theme.fg("toolTitle", theme.bold("$ "));
			const cmd = args.command.length > 80 ? `${args.command.slice(0, 77)}...` : args.command;
			text += theme.fg("accent", cmd);
			if (args.timeout) {
				text += theme.fg("dim", ` (timeout: ${args.timeout}s)`);
			}
			return new Text(text, 0, 0);
		},

		renderResult(result, { expanded, isPartial }, theme, _context) {
			if (isPartial) return new Text(theme.fg("warning", "Running..."), 0, 0);

			const details = result.details as BashToolDetails | undefined;
			const content = result.content[0];
			const output = content?.type === "text" ? content.text : "";

			const exitMatch = output.match(/exit code: (\d+)/);
			const exitCode = exitMatch ? parseInt(exitMatch[1], 10) : null;
			const lineCount = output.split("\n").filter((l) => l.trim()).length;

			let text = "";
			if (exitCode === 0 || exitCode === null) {
				text += theme.fg("success", "done");
			} else {
				text += theme.fg("error", `exit ${exitCode}`);
			}
			text += theme.fg("dim", ` (${lineCount} lines)`);

			if (details?.truncation?.truncated) {
				text += theme.fg("warning", " [truncated]");
			}

			if (expanded) {
				const lines = output.split("\n").slice(0, 20);
				for (const line of lines) {
					text += `\n${theme.fg("dim", line)}`;
				}
				if (output.split("\n").length > 20) {
					text += `\n${theme.fg("muted", "... more output")}`;
				}
			}

			return new Text(text, 0, 0);
		},
	});

	// --- Edit tool: show path and diff stats ---
	const originalEdit = createEditTool(cwd);
	pi.registerTool({
		name: "edit",
		label: "edit",
		description: originalEdit.description,
		parameters: originalEdit.parameters,

		async execute(toolCallId, params, signal, onUpdate) {
			return originalEdit.execute(toolCallId, params, signal, onUpdate);
		},

		renderCall(args, theme, _context) {
			let text = theme.fg("toolTitle", theme.bold("edit "));
			text += theme.fg("accent", args.path);
			return new Text(text, 0, 0);
		},

		renderResult(result, { expanded, isPartial }, theme, _context) {
			if (isPartial) return new Text(theme.fg("warning", "Editing..."), 0, 0);

			const details = result.details as EditToolDetails | undefined;
			const content = result.content[0];

			if (content?.type === "text" && content.text.startsWith("Error")) {
				return new Text(theme.fg("error", content.text.split("\n")[0]), 0, 0);
			}

			if (!details?.diff) {
				return new Text(theme.fg("success", "Applied"), 0, 0);
			}

			const diffLines = details.diff.split("\n");
			let additions = 0;
			let removals = 0;
			for (const line of diffLines) {
				if (line.startsWith("+") && !line.startsWith("+++")) additions++;
				if (line.startsWith("-") && !line.startsWith("---")) removals++;
			}

			let text = theme.fg("success", `+${additions}`);
			text += theme.fg("dim", " / ");
			text += theme.fg("error", `-${removals}`);

			if (expanded) {
				for (const line of diffLines.slice(0, 30)) {
					if (line.startsWith("+") && !line.startsWith("+++")) {
						text += `\n${theme.fg("success", line)}`;
					} else if (line.startsWith("-") && !line.startsWith("---")) {
						text += `\n${theme.fg("error", line)}`;
					} else {
						text += `\n${theme.fg("dim", line)}`;
					}
				}
				if (diffLines.length > 30) {
					text += `\n${theme.fg("muted", `... ${diffLines.length - 30} more diff lines`)}`;
				}
			}

			return new Text(text, 0, 0);
		},
	});

	// --- Write tool: show path and size ---
	const originalWrite = createWriteTool(cwd);
	pi.registerTool({
		name: "write",
		label: "write",
		description: originalWrite.description,
		parameters: originalWrite.parameters,

		async execute(toolCallId, params, signal, onUpdate) {
			return originalWrite.execute(toolCallId, params, signal, onUpdate);
		},

		renderCall(args, theme, _context) {
			let text = theme.fg("toolTitle", theme.bold("write "));
			text += theme.fg("accent", args.path);
			const lineCount = args.content.split("\n").length;
			text += theme.fg("dim", ` (${lineCount} lines)`);
			return new Text(text, 0, 0);
		},

		renderResult(result, { isPartial }, theme, _context) {
			if (isPartial) return new Text(theme.fg("warning", "Writing..."), 0, 0);

			const content = result.content[0];
			if (content?.type === "text" && content.text.startsWith("Error")) {
				return new Text(theme.fg("error", content.text.split("\n")[0]), 0, 0);
			}

			return new Text(theme.fg("success", "Written"), 0, 0);
		},
	});
}
```

### Detailed Annotations

#### Delegation Pattern: `createReadTool()` / `createBashTool()` / `createEditTool()` / `createWriteTool()`

These factory functions from `@mariozechner/pi-coding-agent` create instances of the built-in tools. The pattern is:

```typescript
const original = createReadTool(cwd);
pi.registerTool({
    name: "read",                         // Override built-in by using same name
    description: original.description,     // Keep original description
    parameters: original.parameters,       // Keep original schema
    execute: original.execute,             // Delegate execution to original
    renderCall(args, theme) { ... },       // Custom rendering
    renderResult(result, opts, theme) { ... }, // Custom rendering
});
```

This separates concerns: execution stays the same, only presentation changes.

#### `isPartial` in `renderResult`

When a tool is still executing (streaming output), `isPartial` is `true`. Show a loading indicator:
```typescript
if (isPartial) return new Text(theme.fg("warning", "Running..."), 0, 0);
```

#### Tool-Specific Details Types

Each built-in tool provides typed details:
- `ReadToolDetails` -- Contains `truncation: { truncated: boolean, totalLines: number }`
- `BashToolDetails` -- Contains `truncation` info
- `EditToolDetails` -- Contains `diff: string` with the unified diff

---

## 11. Handoff

**File:** `examples/extensions/handoff.ts`

Demonstrates creating new sessions, using the LLM for context extraction, and advanced UI patterns.

### Key Patterns (Abbreviated)

```typescript
// Creating a new session with parent tracking
const newSessionResult = await ctx.newSession({
    parentSession: currentSessionFile,
});

// Using ctx.ui.editor for interactive prompt editing
const editedPrompt = await ctx.ui.editor("Edit handoff prompt", result);

// Setting editor text programmatically
ctx.ui.setEditorText(editedPrompt);

// Using ctx.ui.custom for fully custom UI overlays
const result = await ctx.ui.custom<string | null>((tui, theme, _kb, done) => {
    const loader = new BorderedLoader(tui, theme, `Generating handoff prompt...`);
    loader.onAbort = () => done(null);
    // ... async work ...
    doGenerate().then(done);
    return loader;
});

// Using the complete() function for direct LLM calls from extensions
import { complete } from "@mariozechner/pi-ai";
const response = await complete(ctx.model!, { systemPrompt, messages }, { apiKey, signal });

// Getting API keys from the model registry
const apiKey = await ctx.modelRegistry.getApiKey(ctx.model!);

// Serializing conversation history
const llmMessages = convertToLlm(messages);
const conversationText = serializeConversation(llmMessages);
```

### Annotations

#### `ctx.newSession({ parentSession })`

Creates a new session, optionally linking it to a parent session for context tracking. Returns `{ cancelled: boolean }`.

#### `ctx.ui.custom<T>((tui, theme, kb, done) => Component)`

The most powerful UI primitive. Creates a fully custom overlay:
- `tui` -- The terminal UI instance for rendering.
- `theme` -- The current theme.
- `kb` -- Keyboard handler.
- `done(value)` -- Call to close the overlay and return a value.
- Return a TUI component to render.

#### `ctx.ui.setEditorText(text)`

Programmatically sets the text in the user's input editor. Used after handoff to pre-fill the prompt for the new session.

---

## 12. Widget Placement

**File:** `examples/extensions/widget-placement.ts`

Demonstrates widget positioning options.

### Full Source

```typescript
import type { ExtensionAPI, ExtensionContext } from "@mariozechner/pi-coding-agent";

const applyWidgets = (ctx: ExtensionContext) => {
	if (!ctx.hasUI) return;
	ctx.ui.setWidget("widget-above", ["Above editor widget"]);
	ctx.ui.setWidget("widget-below", ["Below editor widget"], { placement: "belowEditor" });
};

export default function widgetPlacementExtension(pi: ExtensionAPI) {
	pi.on("session_start", (_event, ctx) => {
		applyWidgets(ctx);
	});

	pi.on("session_switch", (_event, ctx) => {
		applyWidgets(ctx);
	});
}
```

### Annotations

#### `ctx.ui.setWidget(key, lines, options)`

- **Default placement** (no options): Widget appears **above** the editor.
- **`{ placement: "belowEditor" }`**: Widget appears **below** the editor.
- `key` is a unique identifier; calling `setWidget` with the same key replaces the previous widget.
- `lines` is a `string[]` where each element is one rendered line.
- Pass `undefined` as `lines` to remove the widget.

#### `session_switch` Event

Fires when the user switches between sessions. Widgets must be re-applied since the UI state resets.

---

## 13. Custom Header

**File:** `examples/extensions/custom-header.ts`

Demonstrates replacing the built-in header with a custom component.

### Key Pattern

```typescript
ctx.ui.setHeader((_tui, theme) => {
    return {
        render(width: number): string[] {
            // Return an array of strings, one per line
            return [...mascotLines, subtitle];
        },
        invalidate() {},
    };
});

// Restore built-in header
ctx.ui.setHeader(undefined);
```

#### `ctx.ui.setHeader(factory | undefined)`

- **Factory function**: `(tui, theme) => { render(width): string[], invalidate() }`
  - `render(width)` returns the header lines for the given terminal width.
  - `invalidate()` is called to signal the header needs re-rendering.
- **`undefined`**: Restores the built-in header (logo + keybinding hints).

---

## 14. Custom Footer

**File:** `examples/extensions/custom-footer.ts`

Demonstrates replacing the built-in footer with a custom component.

### Key Pattern

```typescript
ctx.ui.setFooter((tui, theme, footerData) => {
    const unsub = footerData.onBranchChange(() => tui.requestRender());

    return {
        dispose: unsub,
        invalidate() {},
        render(width: number): string[] {
            const branch = footerData.getGitBranch();
            const statuses = footerData.getExtensionStatuses();
            // ... format and return footer lines
            return [formattedLine];
        },
    };
});
```

#### `footerData` API

The footer factory receives a `footerData` object with methods not otherwise accessible:
- **`footerData.getGitBranch()`** -- Returns the current git branch name.
- **`footerData.getExtensionStatuses()`** -- Returns status texts set by extensions via `ctx.ui.setStatus()`.
- **`footerData.onBranchChange(callback)`** -- Subscribe to git branch changes; returns an unsubscribe function.

#### Footer Component Shape

```typescript
{
    dispose?: () => void,    // Cleanup (unsubscribe from events)
    invalidate(): void,      // Signal for re-render
    render(width): string[], // Return footer lines for terminal width
}
```

---

## 15. Pattern Summary Table

| API Call | Purpose | Example(s) |
|---|---|---|
| `pi.registerMessageRenderer(type, fn)` | Custom rendering for messages with a given `customType` | [Message Renderer](#1-message-renderer) |
| `pi.sendMessage(opts)` | Send a custom message (no LLM turn by default) | [Message Renderer](#1-message-renderer), [Plan Mode](#2-plan-mode) |
| `pi.sendMessage(opts, { triggerTurn: true })` | Send a custom message AND trigger an LLM response | [File Trigger](#6-file-trigger), [Plan Mode](#2-plan-mode) |
| `pi.sendMessage(opts, { triggerTurn: false })` | Send a custom message without triggering an LLM response | [Plan Mode](#2-plan-mode) |
| `pi.sendUserMessage(text)` | Send a user message (always triggers turn when idle) | [Send User Message](#3-send-user-message), [Plan Mode](#2-plan-mode) |
| `pi.sendUserMessage(text, { deliverAs: "steer" })` | Interrupt current streaming with a steering message | [Send User Message](#3-send-user-message) |
| `pi.sendUserMessage(text, { deliverAs: "followUp" })` | Queue a message for after current turn completes | [Send User Message](#3-send-user-message) |
| `pi.registerCommand(name, { handler })` | Register a `/command` | All examples |
| `pi.registerShortcut(key, { handler })` | Register a keyboard shortcut | [Plan Mode](#2-plan-mode) |
| `pi.registerFlag(name, opts)` | Register a CLI flag (`--name`) | [Plan Mode](#2-plan-mode) |
| `pi.getFlag(name)` | Read a CLI flag value | [Plan Mode](#2-plan-mode) |
| `pi.registerTool({ name, execute, ... })` | Register a custom tool for the LLM | [Subagent](#4-subagent), [Dynamic Tools](#8-dynamic-tools), [Tool Override](#9-tool-override), [Built-in Tool Renderer](#10-built-in-tool-renderer) |
| `pi.setActiveTools(toolNames)` | Restrict which tools the LLM can use | [Plan Mode](#2-plan-mode) |
| `pi.appendEntry(customType, data)` | Persist custom data in the session file | [Plan Mode](#2-plan-mode) |
| `pi.on("input", handler)` | Intercept/transform user input | [Input Transform](#5-input-transform) |
| `pi.on("tool_call", handler)` | Intercept/block tool calls before execution | [Plan Mode](#2-plan-mode) |
| `pi.on("context", handler)` | Filter/modify messages before they reach the LLM | [Plan Mode](#2-plan-mode) |
| `pi.on("before_agent_start", handler)` | Inject context messages before the agent starts | [Plan Mode](#2-plan-mode) |
| `pi.on("turn_end", handler)` | React after each LLM turn | [Plan Mode](#2-plan-mode) |
| `pi.on("agent_end", handler)` | React when the agent finishes all turns | [Plan Mode](#2-plan-mode) |
| `pi.on("session_start", handler)` | Initialize state when a session begins | [File Trigger](#6-file-trigger), [Event Bus](#7-event-bus), [Dynamic Tools](#8-dynamic-tools) |
| `pi.on("session_switch", handler)` | React when user switches sessions | [Widget Placement](#12-widget-placement) |
| `pi.events.on(name, handler)` | Subscribe to inter-extension events | [Event Bus](#7-event-bus) |
| `pi.events.emit(name, data)` | Broadcast inter-extension events | [Event Bus](#7-event-bus) |
| `ctx.ui.setStatus(key, text)` | Set/clear footer status indicator | [Plan Mode](#2-plan-mode) |
| `ctx.ui.setWidget(key, lines, opts)` | Set/clear a persistent widget (above or below editor) | [Plan Mode](#2-plan-mode), [Widget Placement](#12-widget-placement) |
| `ctx.ui.setHeader(factory)` | Replace the built-in header | [Custom Header](#13-custom-header) |
| `ctx.ui.setFooter(factory)` | Replace the built-in footer | [Custom Footer](#14-custom-footer) |
| `ctx.ui.setEditorText(text)` | Programmatically set editor content | [Handoff](#11-handoff) |
| `ctx.ui.notify(message, level)` | Show a transient notification | All examples |
| `ctx.ui.select(prompt, options)` | Show a selection menu | [Plan Mode](#2-plan-mode) |
| `ctx.ui.editor(prompt, initial)` | Open a text editor overlay | [Plan Mode](#2-plan-mode), [Handoff](#11-handoff) |
| `ctx.ui.confirm(title, body)` | Show a confirmation dialog | [Subagent](#4-subagent) |
| `ctx.ui.custom(factory)` | Create a fully custom UI overlay | [Handoff](#11-handoff) |
| `ctx.isIdle()` | Check if agent is not streaming | [Send User Message](#3-send-user-message) |
| `ctx.hasUI` | Check if TUI is available | [File Trigger](#6-file-trigger), [Widget Placement](#12-widget-placement) |
| `ctx.sessionManager.getEntries()` | Read all session entries (for state restore) | [Plan Mode](#2-plan-mode) |
| `ctx.sessionManager.getBranch()` | Get current conversation branch entries | [Custom Footer](#14-custom-footer), [Handoff](#11-handoff) |
| `ctx.newSession(opts)` | Create a new session | [Handoff](#11-handoff) |
| `ctx.modelRegistry.getApiKey(model)` | Get API key for direct LLM calls | [Handoff](#11-handoff) |
| `renderCall(args, theme, ctx)` | Custom tool invocation display | [Subagent](#4-subagent), [Built-in Tool Renderer](#10-built-in-tool-renderer) |
| `renderResult(result, { expanded, isPartial }, theme, ctx)` | Custom tool result display | [Subagent](#4-subagent), [Built-in Tool Renderer](#10-built-in-tool-renderer) |
| `onUpdate(partialResult)` | Stream partial tool results to the UI | [Subagent](#4-subagent) |
| `createReadTool(cwd)` / `createBashTool(cwd)` / etc. | Create instances of built-in tools for delegation | [Built-in Tool Renderer](#10-built-in-tool-renderer) |
| `withFileMutationQueue(path, fn)` | Serialize file writes to avoid race conditions | [Tool Override](#9-tool-override) |
| `getAgentDir()` | Get `~/.pi/agent/` directory path | [Tool Override](#9-tool-override) |
| `getMarkdownTheme()` | Get theme for Markdown TUI component | [Subagent](#4-subagent) |

### TUI Components

| Component | Import | Purpose | Example |
|---|---|---|---|
| `Text(content, x, y)` | `@mariozechner/pi-tui` | Render styled text | All renderer examples |
| `Box(padX, padY, bgFn)` | `@mariozechner/pi-tui` | Container with padding and background | [Message Renderer](#1-message-renderer) |
| `Container()` | `@mariozechner/pi-tui` | Vertical layout container | [Subagent](#4-subagent) |
| `Markdown(content, x, y, theme)` | `@mariozechner/pi-tui` | Rendered markdown content | [Subagent](#4-subagent) |
| `Spacer(lines)` | `@mariozechner/pi-tui` | Vertical whitespace | [Subagent](#4-subagent) |
| `Key.ctrlAlt(key)` | `@mariozechner/pi-tui` | Keyboard shortcut definition | [Plan Mode](#2-plan-mode) |
| `BorderedLoader` | `@mariozechner/pi-coding-agent` | Loading overlay with abort support | [Handoff](#11-handoff) |

### Theme Colors

Used with `theme.fg(colorName, text)` and `theme.bg(colorName, text)`:

| Color Name | Typical Use |
|---|---|
| `"accent"` | Highlighted text, file paths, agent names |
| `"success"` | Completed items, success status |
| `"error"` | Errors, failed items |
| `"warning"` | Warnings, in-progress indicators |
| `"dim"` | De-emphasized text, metadata |
| `"muted"` | Very de-emphasized text, separators |
| `"toolTitle"` | Tool name headers |
| `"toolOutput"` | Tool output text |
| `"customMessageBg"` | Background for custom messages |
| `"text"` | Default text color |

### Event Lifecycle Order

```
session_start
  → (user types or extension sends message)
  → input (can transform/handle/continue)
  → before_agent_start (can inject context message)
  → context (can filter messages sent to LLM)
  → tool_call (can block tool execution) [per tool call]
  → turn_end [per LLM turn]
  → agent_end (all turns complete)
  → (user types next message...)
```

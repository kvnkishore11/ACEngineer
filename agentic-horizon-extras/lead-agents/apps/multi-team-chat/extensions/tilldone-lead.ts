/**
 * TillDone Lead Extension
 *
 * Registers the `tilldone` tool for lead subprocesses, allowing leads
 * to mark tasks as inprogress or done. Mutations are sent back to the
 * parent process via onUpdate for application to canonical state.
 *
 * Loaded via `-e` on every subprocess. Self-exits immediately if
 * TILLDONE_TASKS is not set, so member subprocesses are unaffected.
 *
 * Environment variables consumed:
 *   TILLDONE_TASKS      — JSON-serialized TillDoneState snapshot
 *   TILLDONE_TEAM_NAME  — this lead's team name (e.g. "Engineering")
 *   TILLDONE_TEAM_COLOR — hex color for team attribution
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Text } from "@mariozechner/pi-tui";
import { Type } from "@sinclair/typebox";

import type { TillDoneState, TillDoneMutation } from "./modules/types";
import { startTask, doneTask, STATUS_ICON } from "./modules/tilldone";

export default function (pi: ExtensionAPI) {
	// ── Guard: only activate for lead subprocesses ───────────────
	const tasksJson = process.env.TILLDONE_TASKS;
	if (!tasksJson) return;

	const teamName = process.env.TILLDONE_TEAM_NAME || "";
	const teamColor = process.env.TILLDONE_TEAM_COLOR || "#ffffff";

	let state: TillDoneState;
	try {
		state = JSON.parse(tasksJson) as TillDoneState;
	} catch {
		return; // malformed JSON — fail silently
	}

	// Strip TILLDONE env vars so member subprocesses don't get them
	delete process.env.TILLDONE_TASKS;
	delete process.env.TILLDONE_TEAM_NAME;
	delete process.env.TILLDONE_TEAM_COLOR;

	// ── tilldone tool ────────────────────────────────────────────

	pi.registerTool({
		name: "tilldone",
		label: "TillDone",
		description:
			"Mark tasks in the shared task list. " +
			"Actions: start (id — mark inprogress), done (id — mark complete), list.",
		parameters: Type.Object({
			action: Type.Union([
				Type.Literal("start"),
				Type.Literal("done"),
				Type.Literal("list"),
			], { description: "Action to perform" }),
			id: Type.Optional(Type.Number({ description: "Task ID (for start/done)" })),
		}),

		async execute(_toolCallId, params, _signal, onUpdate) {
			switch (params.action) {
				case "start": {
					if (params.id === undefined) {
						return { content: [{ type: "text" as const, text: "Error: id required for start" }] };
					}
					const task = startTask(state, params.id, teamName, teamColor);
					if (!task) {
						return { content: [{ type: "text" as const, text: `Task #${params.id} not found` }] };
					}
					// Send mutation to parent
					const mutation: TillDoneMutation = {
						type: "tilldone-mutation",
						action: "start",
						id: params.id,
						team: teamName,
						teamColor,
					};
					onUpdate?.(mutation);
					return { content: [{ type: "text" as const, text: `Task #${params.id} → inprogress` }] };
				}

				case "done": {
					if (params.id === undefined) {
						return { content: [{ type: "text" as const, text: "Error: id required for done" }] };
					}
					const task = doneTask(state, params.id);
					if (!task) {
						return { content: [{ type: "text" as const, text: `Task #${params.id} not found` }] };
					}
					// Send mutation to parent
					const mutation: TillDoneMutation = {
						type: "tilldone-mutation",
						action: "done",
						id: params.id,
						team: teamName,
						teamColor,
					};
					onUpdate?.(mutation);
					return { content: [{ type: "text" as const, text: `Task #${params.id} → done` }] };
				}

				case "list": {
					if (state.tasks.length === 0) {
						return { content: [{ type: "text" as const, text: "No tasks in the list." }] };
					}
					const header = state.title ? `${state.title}:` : "Tasks:";
					const taskLines = state.tasks
						.map(t => `${STATUS_ICON[t.status]} #${t.id} (${t.status}): ${t.text}${t.team ? ` [${t.team}]` : ""}`)
						.join("\n");
					return { content: [{ type: "text" as const, text: `${header}\n${taskLines}` }] };
				}

				default:
					return { content: [{ type: "text" as const, text: `Unknown action: ${params.action}` }] };
			}
		},

		// Invisible — chatView in multi-team-chat.ts shows the bubbles
		renderCall() { return new Text("", 0, 0); },
		renderResult() { return new Text("", 0, 0); },
	});
}

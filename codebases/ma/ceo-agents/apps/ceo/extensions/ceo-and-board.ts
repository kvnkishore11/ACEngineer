/**
 * CEO & Board — Strategic Decision-Making Agent Team
 *
 * v1 deliberation engine. Registers `converse` and `end_deliberation`
 * custom tools, spawns board member Pi agent subprocesses with persistent
 * sessions, logs all conversations to .jsonl, and renders board member
 * responses in the TUI.
 *
 * Usage: pi -e extensions/ceo-and-board.ts
 *        or auto-loaded via .pi/settings.json
 */

import { spawn } from "node:child_process";
import {
	existsSync,
	readFileSync,
	writeFileSync,
	mkdirSync,
	readdirSync,
	statSync,
} from "node:fs";
import { join, basename } from "node:path";
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { parseFrontmatter } from "@mariozechner/pi-coding-agent";
import { Text, truncateToWidth, visibleWidth } from "@mariozechner/pi-tui";
import { Type } from "@sinclair/typebox";

// ── Module imports ───────────────────────────────────────────────
import type { CeoConfig, MeetingState, MemberStats, ConstraintState, BoardMemberConfig } from "./modules/types";
import { findProjectRoot, parseConfig, loadBoardMembers, loadDotEnv, buildExpertiseBlock, buildSkillsBlock } from "./modules/config";
import { bgWarm, cyan, pink, yellow, green, dim, bold, parseHexColor, formatTokenCount, renderGaugeLine, renderBoardStatusLines } from "./modules/theme";
import { callBoardMember } from "./modules/subprocess";
import { generateSessionId, parseBudget, appendToLog, trimToolArgs, appendToolUse, getConstraintState } from "./modules/helpers";

// ── Extension ────────────────────────────────────────────────────

export default function (pi: ExtensionAPI) {
	// ── State variables ──────────────────────────────────────────
	let config: CeoConfig | null = null;
	let meetingState: MeetingState | null = null;
	let memberStats: Map<string, MemberStats> = new Map();
	let projectRoot: string | null = null;
	let subprocessEnv: Record<string, string> = { ...process.env } as Record<string, string>;
	const respondingMembers: Set<string> = new Set();
	let ceoCost: number = 0;

	// ── Helper: register constraint gauge widget ────────────────
	// Extracted so it can be re-registered (moved to end of widget
	// insertion order) after the board live-feed widget is set.

	let gaugeCtx: { ui: any } | null = null;

	function registerConstraintGauges() {
		if (!gaugeCtx) return;
		// Remove first to move to end of Map insertion order
		gaugeCtx.ui.setWidget("constraint-gauges", undefined);
		gaugeCtx.ui.setWidget("constraint-gauges", () => ({
			render(width: number): string[] {
				if (!config || !meetingState) return [];

				const c = config.meeting.constraints;
				const minTime = c.min_time_minutes;
				const maxTime = c.max_time_minutes;
				const minBudget = parseBudget(c.min_budget);
				const maxBudget = parseBudget(c.max_budget);

				const isActive =
					meetingState.phase === "deliberating" || meetingState.phase === "ending";
				const isComplete = meetingState.phase === "complete";
				const currentTime =
					isActive || isComplete
						? (Date.now() - meetingState.startTime) / 1000 / 60
						: 0;
				const currentBudget = meetingState.budgetSpent;

				const barWidth = Math.max(10, width - 39);
				const pad = bgWarm(" ".repeat(width));

				const timeLine = renderGaugeLine(
					"TIME",
					currentTime,
					minTime,
					maxTime,
					barWidth,
					`${currentTime.toFixed(1)} min`,
					`${minTime}-${maxTime} min`,
					width,
				);

				const budgetLine = renderGaugeLine(
					"BUDGET",
					currentBudget,
					minBudget,
					maxBudget,
					barWidth,
					`$${currentBudget.toFixed(2)}`,
					`${c.min_budget}-${c.max_budget}`,
					width,
				);

				return [pad, timeLine, budgetLine, pad];
			},
			invalidate() {},
		}));
	}

	// ── registerMessageRenderer("board-response") ────────────────

	pi.registerMessageRenderer("board-response", (message, _options, theme) => {
		const details = message.details as { member?: string; color?: string } | undefined;
		const memberName = details?.member || "Board Member";
		const color = details?.color || "#ffffff";
		const { r, g, b } = parseHexColor(color);

		const bgOpen = `\x1b[48;2;${r};${g};${b}m`;
		const fgDark = `\x1b[38;2;30;30;30m`;
		const reset = `\x1b[0m`;

		const header = `${bgOpen}${fgDark} ${memberName} ${reset}`;
		const body = typeof message.content === "string" ? message.content : "";

		let text = header + "\n" + theme.fg("dim", body);
		return new Text(text, 0, 0);
	});

	// ── registerTool("converse") ─────────────────────────────────

	pi.registerTool({
		name: "converse",
		label: "Converse",
		description:
			"Send a message to one or more board members. Use `to` to address specific members by name, an array of names, or \"all\" to address the entire board. Returns their responses and the current constraint state (time/budget).",
		promptSnippet:
			'Send a message to board members. to: member name, array of names, or "all". Returns responses + constraint state.',
		promptGuidelines: [
			'ALWAYS default to converse("all", message) to broadcast to the entire board. Only address individual members for targeted follow-ups on specific arguments.',
			'Do NOT loop through members individually with the same message. Use "all" to let all members respond in one call.',
			"Check constraint_state in every response: if hit_max is true, call end_deliberation immediately.",
			"If approaching_max_time or approaching_max_budget, start wrapping up.",
		],
		parameters: Type.Object({
			to: Type.Union([Type.String(), Type.Array(Type.String())], {
				description:
					'Board member name, array of names, or "all" to address the entire board',
			}),
			message: Type.String({
				description: "The CEO's question, challenge, follow-up, or directive",
			}),
		}),

		async execute(_toolCallId, params, signal, onUpdate, ctx) {
			if (!meetingState || meetingState.phase !== "deliberating") {
				throw new Error(
					"No active deliberation. Use /ceo-begin to start a meeting first.",
				);
			}

			// Check if max already hit
			const preCheck = getConstraintState(meetingState);
			if (preCheck.hit_max) {
				throw new Error(
					"Meeting constraints exceeded. You MUST call end_deliberation immediately to collect final statements and write the memo.",
				);
			}

			const { to, message } = params;

			// Resolve target members
			let targetMembers: BoardMemberConfig[] = [];
			if (to === "all") {
				targetMembers = [...meetingState.activeMembers];
			} else if (typeof to === "string") {
				const found = meetingState.activeMembers.find(
					(m) => m.name.toLowerCase() === to.toLowerCase(),
				);
				if (!found) {
					throw new Error(
						`Board member "${to}" not found. Available: ${meetingState.activeMembers.map((m) => m.name).join(", ")}`,
					);
				}
				targetMembers = [found];
			} else if (Array.isArray(to)) {
				for (const name of to) {
					const found = meetingState.activeMembers.find(
						(m) => m.name.toLowerCase() === name.toLowerCase(),
					);
					if (!found) {
						throw new Error(
							`Board member "${name}" not found. Available: ${meetingState.activeMembers.map((m) => m.name).join(", ")}`,
						);
					}
					targetMembers.push(found);
				}
			}

			if (targetMembers.length === 0) {
				throw new Error("No valid board members specified.");
			}

			// Log CEO prompt (once for all targets)
			const toField = targetMembers.length === meetingState.activeMembers.length
				? "all"
				: targetMembers.map((m) => m.name).join(", ");
			appendToLog(meetingState.logPath, {
				from: "CEO",
				to: toField,
				message,
				timestamp: new Date().toISOString(),
				type: "prompt",
			});

			// Call all board members in PARALLEL
			const perMemberText: Map<string, string> = new Map();
			for (const m of targetMembers) {
				perMemberText.set(m.name, "");
				respondingMembers.add(m.name);
			}

			// Single streaming widget — renders ALL members in config order
			// (same approach as the footer: one render, fixed order, no shuffling)
			const memberState: Map<string, { text: string; active: boolean }> = new Map();

			const refreshBoardWidget = () => {
				ctx.ui.setWidget("board-live-feed", () => ({
					render(rawWidth: number): string[] {
						const width = Math.floor(rawWidth * 0.9);
						const allLines: string[] = [];

						// Render ALL active members in config order
						for (const m of meetingState!.activeMembers) {
							const state = memberState.get(m.name);
							if (!state) continue;

							const { r, g, b } = parseHexColor(m.color);
							const bgOpen = `\x1b[48;2;${r};${g};${b}m`;
							const fgDark = `\x1b[38;2;30;30;30m`;
							const reset = `\x1b[0m`;

							const icon = state.active ? "\u{1F4AC}" : "\u{2705}";
							const status = state.active ? " responding..." : " done";
							const header = `${bgOpen}${fgDark} ${icon} ${m.name}${status} ${reset}`;
							const headerLine = truncateToWidth(header + " ".repeat(rawWidth), rawWidth, "");

							const lines = state.text.split("\n").filter((l) => l.trim());
							const lastLine = lines[lines.length - 1] || "";
							const contentLine = truncateToWidth(
								"  " + dim(lastLine) + " ".repeat(width),
								width,
								"",
							);

							allLines.push(headerLine, contentLine);
						}

						return allLines;
					},
					invalidate() {},
				}));
				// Re-register gauges AFTER live feed to keep them at the bottom
				// (widget Map insertion order = render order)
				registerConstraintGauges();
			};

			const removeBoardWidget = () => {
				ctx.ui.setWidget("board-live-feed", undefined);
			};

			// Initialize state for all target members in config order, then render
			for (const m of targetMembers) {
				memberState.set(m.name, { text: "", active: true });
			}
			refreshBoardWidget();

			const results = await Promise.allSettled(
				targetMembers.map(async (member) => {
					try {
						const result = await callBoardMember(
							member,
							message,
							subprocessEnv,
							signal,
							(accumulated) => {
								perMemberText.set(member.name, accumulated);
								memberState.set(member.name, { text: accumulated, active: true });
								refreshBoardWidget();
							},
							meetingState!.contextFiles,
							meetingState!.deliberationDir,
							(toolName, toolCallId, toolArgs) => {
								appendToolUse(meetingState!.deliberationDir, {
									agent: member.name,
									timestamp: new Date().toISOString(),
									tool_name: toolName,
									tool_call_id: toolCallId,
									args: trimToolArgs(toolArgs),
								});
							},
						);
						respondingMembers.delete(member.name);
						memberState.set(member.name, { text: result.response, active: false });
						refreshBoardWidget();

						// Log the response
						appendToLog(meetingState!.logPath, {
							from: member.name,
							to: "all",
							message: result.response,
							timestamp: new Date().toISOString(),
							type: "response",
							tokens_in: result.tokensIn,
							tokens_out: result.tokensOut,
							cost: result.cost,
						});

						// Update stats
						meetingState!.budgetSpent += result.cost;
						const stats = memberStats.get(member.name) || {
							chats: 0,
							cost: 0,
							tokensUsed: 0,
							contextWindow: 256000,
						};
						stats.chats += 1;
						stats.cost += result.cost;
						stats.tokensUsed = result.contextTokens;
						memberStats.set(member.name, stats);

						return { member: member.name, response: result.response, cost: result.cost };
					} catch (err: any) {
						respondingMembers.delete(member.name);
						const errorMsg = `[Error from ${member.name}: ${err.message}]`;
						perMemberText.set(member.name, errorMsg);
						memberState.set(member.name, { text: errorMsg, active: false });
						refreshBoardWidget();
						return { member: member.name, response: errorMsg, cost: 0 };
					}
				}),
			);

			// Clear all responding flags and remove widget
			for (const m of targetMembers) {
				respondingMembers.delete(m.name);
			}
			removeBoardWidget();

			// Collect results
			const allResponses: { member: string; response: string; cost: number }[] = [];
			for (const r of results) {
				if (r.status === "fulfilled") {
					allResponses.push(r.value);
				}
			}


			// Compute final constraint state
			const constraintState = getConstraintState(meetingState);

			// Build return text
			let resultText = "";
			for (const resp of allResponses) {
				resultText += `\n\n### ${resp.member}\n${resp.response}`;
			}
			resultText += "\n\n---\n\n### Constraint State\n";
			resultText += `- Elapsed: ${constraintState.elapsed_time_minutes} minutes\n`;
			resultText += `- Budget spent: $${constraintState.budget_spent.toFixed(2)}\n`;
			resultText += `- Past min time: ${constraintState.past_min_time}\n`;
			resultText += `- Past min budget: ${constraintState.past_min_budget}\n`;
			resultText += `- Approaching max time: ${constraintState.approaching_max_time}\n`;
			resultText += `- Approaching max budget: ${constraintState.approaching_max_budget}\n`;
			resultText += `- Hit max: ${constraintState.hit_max}\n`;

			if (constraintState.hit_max) {
				resultText +=
					"\n**CONSTRAINT LIMIT REACHED.** You MUST call `end_deliberation` immediately.";
			}

			return {
				content: [{ type: "text", text: resultText.trim() }],
				details: { responses: allResponses, constraintState },
			};
		},

		renderCall(args, theme) {
			const toStr =
				typeof args.to === "string" ? args.to : Array.isArray(args.to) ? args.to.join(", ") : "...";
			const msgPreview =
				args.message && args.message.length > 80
					? args.message.slice(0, 80) + "..."
					: args.message || "...";
			let text = theme.fg("toolTitle", theme.bold("converse "));
			text += theme.fg("accent", `CEO -> ${toStr}`);
			text += "\n  " + theme.fg("dim", msgPreview);
			return new Text(text, 0, 0);
		},

		renderResult(result, { expanded, isPartial }, theme) {
			if (isPartial) {
				const text = result.content?.[0];
				return new Text(
					theme.fg("warning", text?.type === "text" ? text.text : "Board members responding..."),
					0,
					0,
				);
			}

			const details = result.details as
				| { responses?: { member: string; response: string; cost: number }[]; constraintState?: ConstraintState }
				| undefined;
			const responses = details?.responses || [];
			const cs = details?.constraintState;

			let text = theme.fg("success", `${responses.length} response(s)`);
			if (cs) {
				text += theme.fg("muted", ` | ${cs.elapsed_time_minutes}min | $${cs.budget_spent.toFixed(2)}`);
				if (cs.hit_max) text += " " + theme.fg("error", "[MAX REACHED]");
				else if (cs.approaching_max_time || cs.approaching_max_budget)
					text += " " + theme.fg("warning", "[APPROACHING MAX]");
			}

			if (expanded) {
				for (const r of responses) {
					text += `\n\n${theme.fg("accent", theme.bold(r.member))}${theme.fg("dim", ` ($${r.cost.toFixed(4)})`)}`;
					text += `\n${theme.fg("dim", r.response)}`;
				}
			} else {
				for (const r of responses) {
					const preview =
						r.response.length > 100 ? r.response.slice(0, 100) + "..." : r.response;
					text += `\n  ${theme.fg("accent", r.member)}: ${theme.fg("dim", preview.replace(/\n/g, " "))}`;
				}
			}

			return new Text(text, 0, 0);
		},
	});

	// ── registerTool("end_deliberation") ─────────────────────────

	pi.registerTool({
		name: "end_deliberation",
		label: "End Deliberation",
		description:
			"End the deliberation and collect final one-statement positions from all board members. Contrarian speaks last (enforced). After this tool returns, write the memo.",
		promptSnippet:
			"End deliberation. Collects final statements from all members (contrarian last). Then write the memo.",
		promptGuidelines: [
			"Call end_deliberation when hit_max is true, or when you have sufficient discussion to make a decision.",
			"After end_deliberation returns, your only job is to write the memo using the write tool.",
		],
		parameters: Type.Object({
			message: Type.String({
				description:
					"The CEO's closing prompt to the board (e.g. 'Summarize your final position in one statement.')",
			}),
		}),

		async execute(_toolCallId, params, signal, onUpdate, ctx) {
			if (!meetingState || (meetingState.phase !== "deliberating" && meetingState.phase !== "ending")) {
				throw new Error("No active deliberation to end.");
			}

			// Guard: check if min constraints are met
			const cs = getConstraintState(meetingState);
			if (!cs.past_min_time && !cs.hit_max) {
				const remainingTime = meetingState.constraints.min_time_minutes - cs.elapsed_time_minutes;
				throw new Error(
					`Min time constraint not reached. ${remainingTime.toFixed(1)} minutes remaining before you can end. ` +
						`Budget spent: $${cs.budget_spent.toFixed(2)}. Keep deliberating.`,
				);
			}

			meetingState.phase = "ending";

			// Log the end_deliberation prompt
			appendToLog(meetingState.logPath, {
				from: "CEO",
				to: "all",
				message: params.message,
				timestamp: new Date().toISOString(),
				type: "end_deliberation",
			});

			// All members give final statements in PARALLEL (including contrarian)
			const allMembers = [...meetingState.activeMembers];

			const finalStatements: { member: string; response: string }[] = [];

			// Live feed widget for final statements
			const endMemberState: Map<string, { text: string; active: boolean }> = new Map();
			for (const m of allMembers) {
				endMemberState.set(m.name, { text: "", active: true });
			}

			const refreshEndWidget = () => {
				ctx.ui.setWidget("board-live-feed", () => ({
					render(rawWidth: number): string[] {
						const width = Math.floor(rawWidth * 0.9);
						const allLines: string[] = [];
						for (const m of allMembers) {
							const state = endMemberState.get(m.name);
							if (!state) continue;

							const { r, g, b } = parseHexColor(m.color);
							const bgOpen = `\x1b[48;2;${r};${g};${b}m`;
							const fgDark = `\x1b[38;2;30;30;30m`;
							const reset = `\x1b[0m`;

							const icon = state.active ? "\u{1F4AC}" : "\u{2705}";
							const status = state.active ? " final statement..." : " done";
							const header = `${bgOpen}${fgDark} ${icon} ${m.name}${status} ${reset}`;
							const headerLine = truncateToWidth(header + " ".repeat(rawWidth), rawWidth, "");

							const lines = state.text.split("\n").filter((l) => l.trim());
							const lastLine = lines[lines.length - 1] || "";
							const contentLine = truncateToWidth(
								"  " + dim(lastLine) + " ".repeat(width),
								width,
								"",
							);
							allLines.push(headerLine, contentLine);
						}
						return allLines;
					},
					invalidate() {},
				}));
				registerConstraintGauges();
			};

			refreshEndWidget();

			const endResults = await Promise.allSettled(
				allMembers.map(async (member) => {
					try {
						const result = await callBoardMember(
							member,
							params.message,
							subprocessEnv,
							signal,
							(accumulated) => {
								endMemberState.set(member.name, { text: accumulated, active: true });
								refreshEndWidget();
							},
							meetingState!.contextFiles,
							meetingState!.deliberationDir,
							(toolName, toolCallId, toolArgs) => {
								appendToolUse(meetingState!.deliberationDir, {
									agent: member.name,
									timestamp: new Date().toISOString(),
									tool_name: toolName,
									tool_call_id: toolCallId,
									args: trimToolArgs(toolArgs),
								});
							},
						);

						endMemberState.set(member.name, { text: result.response, active: false });
						refreshEndWidget();

						// Log final statement
						appendToLog(meetingState!.logPath, {
							from: member.name,
							to: "all",
							message: result.response,
							timestamp: new Date().toISOString(),
							type: "final_statement",
							tokens_in: result.tokensIn,
							tokens_out: result.tokensOut,
							cost: result.cost,
						});

						// Update stats
						meetingState!.budgetSpent += result.cost;
						const stats = memberStats.get(member.name) || {
							chats: 0,
							cost: 0,
							tokensUsed: 0,
							contextWindow: 256000,
						};
						stats.chats += 1;
						stats.cost += result.cost;
						stats.tokensUsed = result.contextTokens;
						memberStats.set(member.name, stats);

						return { member: member.name, response: result.response };
					} catch (err: any) {
						const errorMsg = `[Error from ${member.name}: ${err.message}]`;
						endMemberState.set(member.name, { text: errorMsg, active: false });
						refreshEndWidget();
						return { member: member.name, response: errorMsg };
					}
				}),
			);

			// Collect results in config order
			for (const r of endResults) {
				if (r.status === "fulfilled") {
					finalStatements.push(r.value);
				}
			}

			// Write meeting_end to log
			const finalCs = getConstraintState(meetingState);
			appendToLog(meetingState.logPath, {
				type: "meeting_end",
				timestamp: new Date().toISOString(),
				elapsed_minutes: finalCs.elapsed_time_minutes,
				total_cost: finalCs.budget_spent,
				end_reason: finalCs.hit_max ? finalCs.hit_max_reason : "deliberation_complete",
			});

			meetingState.phase = "complete";

			// Remove live feed widget
			ctx.ui.setWidget("board-live-feed", undefined);

			// Build result text
			let resultText = "## Final Statements\n";
			for (const stmt of finalStatements) {
				resultText += `\n### ${stmt.member}\n${stmt.response}\n`;
			}
			resultText += `\n---\n\nDeliberation complete. Elapsed: ${finalCs.elapsed_time_minutes} min, Cost: $${finalCs.budget_spent.toFixed(2)}.`;
			resultText += `\nNow write the memo to: ${meetingState.memoPath}`;

			return {
				content: [{ type: "text", text: resultText }],
				details: { finalStatements, constraintState: finalCs },
			};
		},

		renderCall(args, theme) {
			const preview =
				args.message && args.message.length > 80
					? args.message.slice(0, 80) + "..."
					: args.message || "...";
			let text = theme.fg("toolTitle", theme.bold("end_deliberation "));
			text += theme.fg("warning", "Closing meeting");
			text += "\n  " + theme.fg("dim", preview);
			return new Text(text, 0, 0);
		},

		renderResult(result, { expanded }, theme) {
			const details = result.details as
				| { finalStatements?: { member: string; response: string }[]; constraintState?: ConstraintState }
				| undefined;
			const statements = details?.finalStatements || [];
			const cs = details?.constraintState;

			let text = theme.fg("success", `Deliberation ended. ${statements.length} final statement(s).`);
			if (cs) {
				text += theme.fg("muted", ` | ${cs.elapsed_time_minutes}min | $${cs.budget_spent.toFixed(2)}`);
			}

			if (expanded) {
				for (const stmt of statements) {
					text += `\n\n${theme.fg("accent", theme.bold(stmt.member))}`;
					text += `\n${theme.fg("dim", stmt.response)}`;
				}
			} else {
				for (const stmt of statements) {
					const preview =
						stmt.response.length > 80 ? stmt.response.slice(0, 80) + "..." : stmt.response;
					text += `\n  ${theme.fg("accent", stmt.member)}: ${theme.fg("dim", preview.replace(/\n/g, " "))}`;
				}
			}

			return new Text(text, 0, 0);
		},
	});

	// ── registerCommand("ceo-begin") ─────────────────────────────

	pi.registerCommand("ceo-begin", {
		description: "Begin a CEO & Board deliberation session",
		handler: async (_args, ctx) => {
			if (!config) {
				ctx.ui.notify(
					"No configuration found. Create .pi/ceo-agents/ceo-and-board-configuration.yaml",
					"error",
				);
				return;
			}

			if (!projectRoot) {
				ctx.ui.notify("Could not find project root.", "error");
				return;
			}

			if (meetingState && meetingState.phase === "deliberating") {
				ctx.ui.notify(
					"A meeting is already in progress. Type 'stop' to halt or 'wrap' to end early.",
					"warning",
				);
				return;
			}

			// List brief directories (each dir contains brief.md + context files)
			const briefsDir = join(projectRoot, config.paths.briefs);
			if (!existsSync(briefsDir)) {
				mkdirSync(briefsDir, { recursive: true });
			}

			let briefDirs: string[] = [];
			try {
				briefDirs = readdirSync(briefsDir)
					.filter((f) => {
						const full = join(briefsDir, f);
						return statSync(full).isDirectory() && existsSync(join(full, "brief.md"));
					})
					.map((f) => {
						const briefFile = join(briefsDir, f, "brief.md");
						const stat = statSync(briefFile);
						return { name: f, mtime: stat.mtimeMs };
					})
					.sort((a, b) => b.mtime - a.mtime)
					.map((f) => f.name);
			} catch {
				ctx.ui.notify("Could not read briefs directory.", "error");
				return;
			}

			if (briefDirs.length === 0) {
				ctx.ui.notify(
					`No brief directories found in ${config.paths.briefs}\n` +
						`Create a directory with a brief.md file containing:\n` +
						`## Situation, ## Stakes, ## Constraints, ## Key Question`,
					"warning",
				);
				return;
			}

			// Let user select a brief directory
			const selected = await ctx.ui.select("Select a brief:", briefDirs);
			if (selected === undefined || selected === null) {
				ctx.ui.notify("No brief selected. Cancelled.", "info");
				return;
			}

			const selectedBrief = typeof selected === "number" ? briefDirs[selected] : selected;
			const briefDir = join(briefsDir, selectedBrief);
			const briefPath = join(briefDir, "brief.md");

			// Read and validate brief
			let briefContent: string;
			try {
				briefContent = readFileSync(briefPath, "utf-8");
			} catch {
				ctx.ui.notify(`Could not read brief: ${briefPath}`, "error");
				return;
			}

			// Validate required sections (case-insensitive, from config)
			const briefLower = briefContent.toLowerCase();
			const missingSections = config.brief_sections.filter(
				(s) => !briefLower.includes(s.section.toLowerCase()),
			);
			if (missingSections.length > 0) {
				const details = missingSections
					.map((s) => `${s.section}\n    ${s.description}`)
					.join("\n\n");
				ctx.ui.notify(
					`Brief is missing required section(s):\n\n${details}\n\nAdd these sections to ${briefPath} and try again.`,
					"error",
				);
				return;
			}

			// Discover context files — all .md files in the brief dir except brief.md
			const contextFiles: string[] = [];
			try {
				for (const f of readdirSync(briefDir)) {
					if (f === "brief.md") continue;
					if (!f.endsWith(".md")) continue;
					const full = join(briefDir, f);
					if (statSync(full).isFile()) {
						contextFiles.push(full);
					}
				}
			} catch {
				// No context files — not fatal
			}

			if (contextFiles.length > 0) {
				ctx.ui.notify(
					`Loaded ${contextFiles.length} context file(s):\n` +
						contextFiles.map((f) => `  ${basename(f)}`).join("\n"),
					"info",
				);
			}

			// Initialize meeting state with unique session ID
			const sessionId = generateSessionId();
			const briefSlug = selectedBrief;
			const deliberationsDir = join(projectRoot, config.paths.deliberations);
			const memosDir = join(projectRoot, config.paths.memos);
			if (!existsSync(deliberationsDir)) mkdirSync(deliberationsDir, { recursive: true });
			if (!existsSync(memosDir)) mkdirSync(memosDir, { recursive: true });

			// Deliberation lives in its own directory to support additional assets
			const deliberationDir = join(deliberationsDir, `${briefSlug}-${sessionId}`);
			if (!existsSync(deliberationDir)) mkdirSync(deliberationDir, { recursive: true });
			const logPath = join(deliberationDir, "conversation.jsonl");
			// Memo lives in its own directory to support assets (SVGs, etc.)
			const memoDir = join(memosDir, `${briefSlug}-${sessionId}`);
			if (!existsSync(memoDir)) mkdirSync(memoDir, { recursive: true });
			const memoPath = join(memoDir, "memo.md");

			// Create session-scoped agent-sessions dir (isolates board member sessions per meeting)
			const sessionDir = join(projectRoot, ".pi", "agent-sessions", sessionId);
			if (!existsSync(sessionDir)) mkdirSync(sessionDir, { recursive: true });

			// Load board members with session-scoped session dir
			const activeMembers = loadBoardMembers(projectRoot, config.board, sessionDir);
			if (activeMembers.length === 0) {
				ctx.ui.notify(
					"No board members could be loaded. Check agent file paths in config.",
					"error",
				);
				return;
			}

			meetingState = {
				sessionId,
				startTime: Date.now(),
				budgetSpent: 0,
				activeMembers,
				phase: "deliberating",
				briefPath,
				briefContent,
				contextFiles,
				deliberationDir,
				logPath,
				memoPath,
				constraints: config.meeting.constraints,
			};

			// Reset CEO cost tracker
			ceoCost = 0;

			// Initialize member stats — look up real context window per model
			memberStats = new Map();
			for (const m of activeMembers) {
				let ctxWin = 256000; // fallback
				try {
					const parts = m.model.split("/");
					const provider = parts.length > 1 ? parts[0] : "anthropic";
					const modelName = parts.length > 1 ? parts.slice(1).join("/") : parts[0];
					const found = ctx.modelRegistry.find(provider, modelName);
					if (found?.contextWindow) ctxWin = found.contextWindow;
				} catch {}
				memberStats.set(m.name, {
					chats: 0,
					cost: 0,
					tokensUsed: 0,
					contextWindow: ctxWin,
				});
			}

			// Write meeting_start to log
			appendToLog(logPath, {
				type: "meeting_start",
				session_id: sessionId,
				timestamp: new Date().toISOString(),
				brief: briefPath,
				board_members: activeMembers.map((m) => m.name),
				constraints: {
					min_time: config.meeting.constraints.min_time_minutes,
					max_time: config.meeting.constraints.max_time_minutes,
					min_budget: parseBudget(config.meeting.constraints.min_budget),
					max_budget: parseBudget(config.meeting.constraints.max_budget),
				},
			});

			// Gauge widget is NOT registered here — it gets registered inside
			// refreshBoardWidget() AFTER the live feed, so it renders below.

			ctx.ui.notify(
				`Meeting started! [${sessionId}]\nBrief: ${selectedBrief}\nBoard: ${activeMembers.map((m) => m.name).join(", ")}\nMemo: ${memoPath}`,
				"info",
			);

			// Build CEO kick-off message with context + brief
			let kickoff =
				"Read the brief below and begin the board deliberation. " +
				"Use the `converse` tool to engage board members and `end_deliberation` when ready to wrap up.";

			// Prepend shared context file contents for the CEO
			if (contextFiles.length > 0) {
				let contextBlock = "\n\n## Shared Context\n\nThe following documents provide background on the product and business.\n";
				for (const cf of contextFiles) {
					try {
						const content = readFileSync(cf, "utf-8");
						contextBlock += `\n### ${basename(cf)}\n\n${content}\n`;
					} catch {
						// Skip unreadable files
					}
				}
				kickoff += contextBlock;
			}

			kickoff += `\n\n---\n\n## Brief\n\n${briefContent}`;

			pi.sendUserMessage(kickoff);
		},
	});

	// ── on("before_agent_start") handler ─────────────────────────

	pi.on("before_agent_start", async (event, _ctx) => {
		if (!meetingState || (meetingState.phase !== "deliberating" && meetingState.phase !== "ending")) {
			return;
		}

		if (!projectRoot) return;

		// Read CEO system prompt
		const ceoPath = join(projectRoot, ".pi", "ceo-agents", "agents", "ceo.md");
		if (!existsSync(ceoPath)) return;

		let ceoContent: string;
		try {
			ceoContent = readFileSync(ceoPath, "utf-8");
		} catch {
			return;
		}

		const { frontmatter: ceoFrontmatter, body } = parseFrontmatter<Record<string, any>>(ceoContent);

		// Build skills block from frontmatter
		const expertiseBlock = buildExpertiseBlock(ceoFrontmatter.expertise || [], projectRoot);
		const skillsBlock = buildSkillsBlock(ceoFrontmatter.skills || [], projectRoot);

		// String-replace {{VARIABLE}} placeholders in the CEO system prompt
		const systemPrompt = body.trim()
			.replace(/\{\{SESSION_ID\}\}/g, meetingState.sessionId)
			.replace(/\{\{BRIEF_CONTENT\}\}/g, meetingState.briefContent)
			.replace(/\{\{BOARD_MEMBERS\}\}/g, meetingState.activeMembers.map((m) => m.name).join(", "))
			.replace(/\{\{MEMO_PATH\}\}/g, meetingState.memoPath)
			.replace(/\{\{MIN_TIME\}\}/g, String(meetingState.constraints.min_time_minutes))
			.replace(/\{\{MAX_TIME\}\}/g, String(meetingState.constraints.max_time_minutes))
			.replace(/\{\{MIN_BUDGET\}\}/g, meetingState.constraints.min_budget)
			.replace(/\{\{MAX_BUDGET\}\}/g, meetingState.constraints.max_budget)
			.replace(/\{\{EXPERTISE_BLOCK\}\}/g, expertiseBlock)
			.replace(/\{\{SKILLS_BLOCK\}\}/g, skillsBlock);

		return {
			systemPrompt,
		};
	});

	// ── on("message_end") handler — track CEO token costs ───────

	pi.on("message_end", async (event, _ctx) => {
		if (!meetingState || meetingState.phase === "idle" || meetingState.phase === "complete") return;

		const msg = event.message as any;
		if (msg?.role === "assistant" && msg?.usage?.cost?.total) {
			const cost = msg.usage.cost.total;
			meetingState.budgetSpent += cost;
			ceoCost += cost;
		}
	});

	// ── on("tool_execution_start") handler — track CEO tool usage ─

	pi.on("tool_execution_start", async (event, _ctx) => {
		if (!meetingState || !meetingState.deliberationDir) return;
		if (meetingState.phase === "idle" || meetingState.phase === "complete") return;

		appendToolUse(meetingState.deliberationDir, {
			agent: "CEO",
			timestamp: new Date().toISOString(),
			tool_name: (event as any).toolName || "unknown",
			tool_call_id: (event as any).toolCallId,
			args: trimToolArgs((event as any).args),
		});
	});

	// ── Block all commands except /ceo-begin ─────────────────────
	//
	// Register shadow commands for common pi built-ins so they show
	// a blocking notification instead of executing. Extension commands
	// are checked before built-ins, so these take precedence.

	const blockedCommands = [
		"help", "clear", "model", "settings", "compact", "logout",
		"status", "cost", "doctor", "bug", "review", "init",
		"memory", "config", "vim", "permissions", "mcp",
	];

	function getBlockMessage(): string {
		if (meetingState && (meetingState.phase === "deliberating" || meetingState.phase === "ending")) {
			return "Meeting in progress. Type 'stop' to halt or 'wrap' to end early.";
		}
		if (meetingState && meetingState.phase === "complete") {
			return "Deliberation complete. Run /ceo-begin to start a new meeting.";
		}
		return "This agent only runs deliberations. Run /ceo-begin to start a meeting.";
	}

	for (const cmd of blockedCommands) {
		pi.registerCommand(cmd, {
			description: `Blocked — this agent only supports /ceo-begin`,
			handler: async (_args, ctx) => {
				ctx.ui.notify(getBlockMessage(), "warning");
			},
		});
	}

	// ── on("input") handler — block all user input ──────────────
	//
	// This is a deliberation-only agent. User input is never forwarded
	// to the model. The only user actions are:
	//   /ceo-begin  — start a meeting
	//   stop        — hard-stop an active meeting
	//   wrap        — early wrap-up of an active meeting

	pi.on("input", async (event, ctx) => {
		// Always let extension-sourced messages through (sendUserMessage from /ceo-begin, /wrap, etc.)
		if ((event as any).source === "extension") {
			return { action: "continue" as const };
		}

		const text = event.text.trim().toLowerCase();

		// ── Active meeting: only stop/wrap allowed ──
		if (meetingState && (meetingState.phase === "deliberating" || meetingState.phase === "ending")) {
			if (text === "stop") {
				const cs = getConstraintState(meetingState);
				appendToLog(meetingState.logPath, {
					type: "meeting_end",
					timestamp: new Date().toISOString(),
					elapsed_minutes: cs.elapsed_time_minutes,
					total_cost: cs.budget_spent,
					end_reason: "user_stop",
				});
				meetingState.phase = "complete";
				ctx.abort();
				ctx.ui.notify("Meeting stopped by user.", "warning");
				return { action: "handled" as const };
			}

			if (text === "wrap") {
				ctx.ui.notify("Wrapping up deliberation...", "info");
				pi.sendUserMessage(
					"The user has requested an early wrap-up. Call end_deliberation now with a closing prompt to collect final statements from all board members.",
					{ deliverAs: "steer" },
				);
				return { action: "handled" as const };
			}

			ctx.ui.notify(
				"Meeting in progress. Type 'stop' to halt or 'wrap' to end early.",
				"info",
			);
			return { action: "handled" as const };
		}

		// ── Deliberation complete: only /ceo-begin allowed ──
		if (meetingState && meetingState.phase === "complete") {
			ctx.ui.notify(
				"Deliberation complete. Run /ceo-begin to start a new meeting.",
				"info",
			);
			return { action: "handled" as const };
		}

		// ── No active meeting: block everything ──
		ctx.ui.notify(
			"This agent only runs deliberations. Run /ceo-begin to start a meeting.",
			"warning",
		);
		return { action: "handled" as const };
	});

	// ── on("tool_result") handler for memo frontmatter ───────────

	pi.on("tool_result", async (event, ctx) => {
		if (!meetingState) return;
		if (event.toolName !== "write") return;

		const input = event.input as { file_path?: string; path?: string } | undefined;
		const filePath = input?.file_path || input?.path || "";

		// Check if the written file is in the memos directory
		if (!filePath.includes("memos/") && !filePath.includes("memos\\")) return;
		// Only inject frontmatter into memo.md — not SVGs or other assets
		if (!filePath.endsWith("memo.md")) return;

		// Read the file that was just written
		let content: string;
		try {
			content = readFileSync(filePath, "utf-8");
		} catch {
			return;
		}

		// Skip if it already has frontmatter
		if (content.startsWith("---\n")) return;

		// Build YAML frontmatter
		const elapsedMs = Date.now() - meetingState.startTime;
		const durationMinutes = Math.round(elapsedMs / 1000 / 60 * 10) / 10;
		const boardMemberNames = meetingState.activeMembers.map((m) => m.name);

		let frontmatter = "---\n";
		frontmatter += `title: "Board Memo: ${basename(meetingState.briefPath, ".md")}"\n`;
		frontmatter += `date: ${new Date().toISOString().split("T")[0]}\n`;
		frontmatter += `duration: ${durationMinutes} minutes\n`;
		frontmatter += `budget_used: $${meetingState.budgetSpent.toFixed(2)}\n`;
		frontmatter += `board_members:\n`;
		for (const name of boardMemberNames) {
			frontmatter += `  - ${name}\n`;
		}
		frontmatter += `brief: ${meetingState.briefPath}\n`;
		frontmatter += `transcript: ${meetingState.logPath}\n`;
		frontmatter += "---\n\n";

		// Prepend frontmatter
		writeFileSync(filePath, frontmatter + content, "utf-8");

		// Write meeting_end if not already written
		if (meetingState.phase !== "complete") {
			const cs = getConstraintState(meetingState);
			appendToLog(meetingState.logPath, {
				type: "meeting_end",
				timestamp: new Date().toISOString(),
				elapsed_minutes: cs.elapsed_time_minutes,
				total_cost: cs.budget_spent,
				end_reason: "memo_written",
			});
			meetingState.phase = "complete";
		}

		// Spawn editor
		if (config?.meeting.editor) {
			try {
				const editorProc = spawn(config.meeting.editor, [filePath], {
					detached: true,
					stdio: "ignore",
				});
				editorProc.unref();
			} catch {
				// Editor spawn failed, not critical
			}
		}

		ctx.ui.notify(
			`Memo saved to ${filePath}\nFrontmatter injected. Opening in ${config?.meeting.editor || "editor"}.`,
			"info",
		);
	});

	// ── on("session_start") handler ──────────────────────────────

	pi.on("session_start", async (_event, ctx) => {
		// Store ctx for gauge widget re-registration
		gaugeCtx = ctx;

		// Apply synthwave theme on boot
		if (ctx.hasUI) {
			ctx.ui.setTheme("synthwave");
			setTimeout(() => ctx.ui.setTitle("pi - CEO & Board"), 150);
		}

		// Load configuration
		config = parseConfig(ctx.cwd);
		projectRoot = findProjectRoot(ctx.cwd);

		// Load .env from project root for subprocess env vars
		if (projectRoot) {
			subprocessEnv = loadDotEnv(projectRoot);
		}

		// Set CEO model from ceo.md frontmatter (e.g. "anthropic/claude-opus-4-6")
		if (projectRoot) {
			const ceoPath = join(projectRoot, ".pi", "ceo-agents", "agents", "ceo.md");
			if (existsSync(ceoPath)) {
				try {
					const ceoRaw = readFileSync(ceoPath, "utf-8");
					const { frontmatter: ceoFm } = parseFrontmatter<Record<string, string>>(ceoRaw);
					if (ceoFm.model) {
						const parts = ceoFm.model.split("/");
						const provider = parts.length > 1 ? parts[0] : "anthropic";
						const modelName = parts.length > 1 ? parts.slice(1).join("/") : parts[0];
						const foundModel = ctx.modelRegistry.find(provider, modelName);
						if (foundModel) {
							await pi.setModel(foundModel);
						}
					}
				} catch {
					// Fall through — use whatever pi defaults to
				}
			}
		}

		// Footer: CEO card (full row) + board member cards
		ctx.ui.setFooter((_tui, theme, _footerData) => ({
			dispose: () => {},
			invalidate() {},
			render(width: number): string[] {
				const lines: string[] = [];

				// CEO card — full width, same style as board members
				const model = ctx.model?.id || "no-model";
				const usage = ctx.getContextUsage();
				const pct = usage && usage.percent !== null ? usage.percent : 0;
				const ctxWindow = ctx.model?.contextWindow || 0;
				const ctxK = ctxWindow >= 1000 ? `${Math.round(ctxWindow / 1000)}k` : `${ctxWindow}`;

				const phaseStr = meetingState ? ` [${meetingState.phase}]` : "";

				// CEO uses cyan color from the synthwave palette
				const ceoBg = `\x1b[48;2;54;249;246m`;
				const fgDark = `\x1b[38;2;30;30;30m`;
				const reset = `\x1b[0m`;

				const ceoIcon = meetingState && meetingState.phase === "deliberating" ? " \u{1F4AC} " : " ";
				// const ceoLeft = `${ceoIcon}CEO ${model}${phaseStr} `;
				const ceoLeft = `${ceoIcon}CEO${phaseStr} `;
				const usedTokens = usage && usage.tokens !== null ? usage.tokens : 0;
				const remainingTokens = ctxWindow - usedTokens;
				const ceoCtxStr = formatTokenCount(Math.max(0, remainingTokens));
				const ceoRight = `\u{1F4B0}$${ceoCost.toFixed(2)} \u{1F9E0}${ceoCtxStr} `;
				const ceoInner = visibleWidth(ceoLeft) + visibleWidth(ceoRight);
				const ceoPad = " ".repeat(Math.max(1, width - ceoInner));
				const ceoLine = truncateToWidth(`${ceoBg}${fgDark}${ceoLeft}${ceoPad}${ceoRight}${reset}`, width, "");
				lines.push(ceoLine);

				// Gap between CEO and board members
				lines.push("");

				// Board member status cards (2 per row, no gaps between rows)
				const boardLines = renderBoardStatusLines(width, meetingState?.activeMembers || [], memberStats, respondingMembers);
				lines.push(...boardLines);

				return lines;
			},
		}));

		// Status line
		const memberCount = config?.board.length ?? 0;
		ctx.ui.setStatus("ceo", `Board: ${memberCount} members`);

		// Startup message — show models in [brackets] for each agent
		if (config) {
			const c = config.meeting.constraints;

			// Append "1M" context badge for Claude 4-6 models
			const modelLabel = (model: string): string =>
				/claude-.*-4-6/.test(model) ? `${model} 1M` : model;

			// Read CEO model from frontmatter
			let ceoModelStr = "unknown";
			if (projectRoot) {
				const ceoAgentPath = join(projectRoot, ".pi", "ceo-agents", "agents", "ceo.md");
				if (existsSync(ceoAgentPath)) {
					try {
						const raw = readFileSync(ceoAgentPath, "utf-8");
						const { frontmatter: fm } = parseFrontmatter<Record<string, string>>(raw);
						if (fm.model) ceoModelStr = fm.model;
					} catch {}
				}
			}

			// Build styled board member lines with per-member colors
			const fgFromHex = (hex: string, s: string): string => {
				const { r, g, b } = parseHexColor(hex);
				return `\x1b[38;2;${r};${g};${b}m${s}\x1b[39m`;
			};

			const memberLines: string[] = [];
			// CEO line — use cyan (synthwave accent)
			memberLines.push(`\n   ${cyan("\u25C6")} ${bold(cyan("CEO"))} ${dim(`[${modelLabel(ceoModelStr)}]`)}`);
			for (const b of config.board) {
				let memberModel = "unknown";
				if (projectRoot) {
					const memberPath = join(projectRoot, b.path);
					if (existsSync(memberPath)) {
						try {
							const raw = readFileSync(memberPath, "utf-8");
							const { frontmatter: fm } = parseFrontmatter<Record<string, string>>(raw);
							if (fm.model) memberModel = fm.model;
						} catch {}
					}
				}
				memberLines.push(`\n   ${fgFromHex(b.color, "\u25C6")} ${bold(fgFromHex(b.color, b.name))} ${dim(`[${modelLabel(memberModel)}]`)}`);
			}

			ctx.ui.notify(
				`${bold(pink("CEO & Board"))} ${dim("\u2014")} ${yellow("Strategic Decision-Making Agent Team")}\n\n` +
					`${dim("Time")}    ${cyan(`${c.min_time_minutes}-${c.max_time_minutes}`)} ${dim("min")}\n` +
					`${dim("Budget")}  ${green(c.min_budget)}${dim("-")}${green(c.max_budget)}\n` +
					`${dim("Editor")}  ${yellow(config.meeting.editor)}\n\n` +
					`${bold("Board")}${memberLines.join("")}\n\n` +
					`${dim("Run")} ${cyan("/ceo-begin")} ${dim("to start a deliberation.")}`,
				"info",
			);
		} else {
			ctx.ui.notify(
				"CEO & Board Agent Team\n\n" +
					"No configuration found.\n" +
					"Create .pi/ceo-agents/ceo-and-board-configuration.yaml",
				"warning",
			);
		}
	});
}

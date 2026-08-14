/**
 * Lead Delegate Extension
 *
 * Registers the `delegate(member, question)` tool for lead subprocesses.
 * Mirrors the orchestrator's `delegate` tool but routes to individual members
 * rather than teams — giving leads full agency over who they consult.
 *
 * Loaded via `-e` on every subprocess. Self-exits immediately if
 * LEAD_MEMBERS_JSON is not set, so member subprocesses are unaffected.
 *
 * Environment variables consumed:
 *   LEAD_MEMBERS_JSON  — JSON array of AgentConfig (name, model, systemPrompt,
 *                        sessionFile, domain, expertise, consultWhen)
 *   LEAD_LOG_PATH      — absolute path to the shared conversation log
 *   AGENT_PROJECT_ROOT — project root (set by subprocess.ts for all agents)
 */

import { existsSync } from "node:fs";
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Text } from "@mariozechner/pi-tui";
import { Type } from "@sinclair/typebox";

import { callAgent } from "./modules/subprocess";
import { appendToLog, readLog, formatTranscript } from "./modules/log";
import type { AgentConfig } from "./modules/types";

// ── Streaming update shape — sent via onUpdate, received as tool_execution_update
export interface ConsultUpdate {
	type: "streaming" | "done";
	member: string;
	text: string;
}

export default function (pi: ExtensionAPI) {
	// ── Guard: only activate for lead subprocesses ───────────────
	const membersJson = process.env.LEAD_MEMBERS_JSON;
	if (!membersJson) return;

	let members: AgentConfig[];
	try {
		members = JSON.parse(membersJson) as AgentConfig[];
	} catch {
		return; // malformed JSON — fail silently
	}
	if (!members.length) return;

	const logPath   = process.env.LEAD_LOG_PATH      || "";
	const projectRoot = process.env.AGENT_PROJECT_ROOT || process.cwd();
	const env       = { ...process.env } as Record<string, string>;
	delete env.LEAD_MEMBERS_JSON; // Don't leak to member subprocesses — prevents workers from registering delegate

	// ── delegate tool ────────────────────────────────────────────

	pi.registerTool({
		name: "delegate",
		label: "Delegate",
		description: [
			"Consult a team member for specialist input.",
			"Members: " + members.map(m => `${m.name} (${m.consultWhen || "specialist"})`).join("; "),
		].join(" "),
		promptSnippet: "Consult a specific team member. Returns their specialist response.",
		promptGuidelines: [
			"Only consult a member when you genuinely need their specialist knowledge.",
			"You can call delegate multiple times in sequence for different members.",
			"Answer directly when you already have enough context.",
		],
		parameters: Type.Object({
			member: Type.String({
				description: "Exact member name to consult (e.g. 'Backend Dev'). Pass the exact member-name value from your team roster.",
			}),
			question: Type.String({
				description: "Your question for the member — include your own analysis so they have full context.",
			}),
		}),

		async execute(_id, params, signal, onUpdate) {
			const { member, question } = params;

			// ── Find member config ───────────────────────────────
			const memberConf = members.find(
				m => m.name.toLowerCase() === member.toLowerCase(),
			);
			if (!memberConf) {
				const available = members.map(m => m.name).join(", ");
				throw new Error(`Member "${member}" not found. Available: ${available}`);
			}

			// ── Build message with full conversation context ─────
			const transcript = logPath
				? formatTranscript(readLog(logPath))
				: "(No conversation history yet.)";

			const message = [
				"## Context",
				"",
				transcript,
				"",
				"---",
				"",
				"## Question",
				"",
				question,
			].join("\n");

			// ── Call member subprocess — stream updates back up ──
			// Timeout: 10 minutes per member to prevent runaway execution
			const MEMBER_TIMEOUT_MS = 10 * 60 * 1000;
			const timeout = AbortSignal.timeout(MEMBER_TIMEOUT_MS);
			const combined = signal
				? AbortSignal.any([signal, timeout])
				: timeout;

			let accText = "";

			let result;
			try {
				result = await callAgent(
					memberConf,
					message,
					env,
					projectRoot,
					combined,
					// onText — stream member's response up to parent via onUpdate
					(accumulated: string) => {
						accText = accumulated;
						const update: ConsultUpdate = { type: "streaming", member, text: accumulated };
						onUpdate?.(update);
					},
					// onToolCall — surface member's tool calls to parent
					(tu) => {
						onUpdate?.({ type: "tool", member, toolName: tu.name, blocked: tu.blocked } as any);
					},
					undefined, // onToolUpdate
					undefined, // onToolEnd
					// onUsage — incremental member cost/context updates
					(stats) => {
						onUpdate?.({ type: "stats", member, cost: stats.cost, tokensIn: stats.tokensIn, tokensOut: stats.tokensOut, contextTokens: stats.contextTokens } as any);
					},
				);
			} catch (err: any) {
				// Error, timeout, or abort — surface the actual error message
				const errMsg = err.message || String(err);
				const isTimeout = errMsg.includes("Aborted") || errMsg.includes("timed out");
				const partial = accText || (isTimeout
					? `(${member} timed out after ${MEMBER_TIMEOUT_MS / 1000}s)`
					: `❌ ${member} error: ${errMsg}`);
				const doneUpdate: ConsultUpdate = { type: "done", member, text: partial };
				onUpdate?.(doneUpdate);
				if (logPath) {
					appendToLog(logPath, {
						from: memberConf.name,
						message: `[ERROR] ${partial}`,
						timestamp: new Date().toISOString(),
						type: "member",
					});
				}
				return { content: [{ type: "text" as const, text: `[${member} error] ${partial}` }] };
			}

			// ── Final stats update — guaranteed delivery with definitive SubprocessResult costs
			// Redundant with onUsage callback but ensures final cost is captured even if
			// incremental updates were lost due to timing or toolCallId mismatch
			onUpdate?.({ type: "stats", member, cost: result.cost, tokensIn: result.tokensIn, tokensOut: result.tokensOut, contextTokens: result.contextTokens } as any);

			// ── Final "done" update ──
			onUpdate?.({ type: "done", member, text: result.response } as any);

			// ── Append member response to shared log ─────────────
			if (logPath) {
				appendToLog(logPath, {
					from: memberConf.name,
					message: result.response,
					timestamp: new Date().toISOString(),
					type: "member",
					cost: result.cost,
					tokens_in: result.tokensIn,
					tokens_out: result.tokensOut,
				});
			}

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
		},

		// Invisible — chatView in multi-team-chat.ts shows the bubbles
		renderCall()   { return new Text("", 0, 0); },
		renderResult() { return new Text("", 0, 0); },
	});
}

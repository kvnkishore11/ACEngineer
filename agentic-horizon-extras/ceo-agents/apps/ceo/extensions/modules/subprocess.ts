// ── Subprocess Spawner ───────────────────────────────────────────
// Board member pi subprocess spawning and JSON event stream parsing.

import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import type { BoardMemberConfig, BoardMemberResult } from "./types";

/**
 * Board members spawn with --no-extensions so the CEO extension does not load
 * recursively. That also drops package providers like pi-xai-oauth (xai-auth).
 * Explicit -e paths still work under --no-extensions — reattach those providers.
 */
function resolveProviderExtensions(): string[] {
	const home = homedir();
	const candidates = [
		// Grok subscription OAuth
		join(home, ".pi/agent/npm/node_modules/pi-xai-oauth/extensions/xai-oauth.ts"),
		join(process.cwd(), ".pi/npm/node_modules/pi-xai-oauth/extensions/xai-oauth.ts"),
		// Kimi Code subscription OAuth
		join(home, ".pi/agent/npm/node_modules/pi-kimi-coder/extensions/index.ts"),
		join(process.cwd(), ".pi/npm/node_modules/pi-kimi-coder/extensions/index.ts"),
	];
	return candidates.filter((p) => existsSync(p));
}

export async function callBoardMember(
	member: BoardMemberConfig,
	ceoMessage: string,
	subprocessEnv: Record<string, string>,
	signal?: AbortSignal,
	onText?: (accumulated: string) => void,
	contextFiles?: string[],
	deliberationDir?: string,
	onToolUse?: (toolName: string, toolCallId: string, args: Record<string, any>) => void,
): Promise<BoardMemberResult> {
	const args: string[] = [
		"--mode",
		"json",
		"-p",
		"--no-extensions",
		"--no-skills",
		"--no-prompt-templates",
		"--no-themes",
		"--session",
		member.sessionFile,
		"--thinking",
		"off",
	];

	// Keep Grok OAuth (xai-auth) available for board members under --no-extensions.
	for (const ext of resolveProviderExtensions()) {
		args.push("-e", ext);
	}

	// First call: session file doesn't exist yet — set personality and model
	if (!existsSync(member.sessionFile)) {
		// Late-resolve runtime paths so board members know where to write assets and read logs
		let resolvedPrompt = member.systemPrompt;
		if (deliberationDir) {
			resolvedPrompt = resolvedPrompt
				.replace(/\{\{DELIBERATION_DIR\}\}/g, deliberationDir)
				.replace(/\{\{CONVERSATION_LOG\}\}/g, join(deliberationDir, "conversation.jsonl"));
		}
		args.push("--system-prompt", resolvedPrompt, "--model", member.model);
		// Preload brief context files via @file syntax — loads into context window
		if (contextFiles && contextFiles.length > 0) {
			for (const cf of contextFiles) {
				args.push(`@${cf}`);
			}
		}
	}

	// Final arg: the CEO's message
	args.push(ceoMessage);

	let accumulatedText = "";
	let tokensIn = 0;
	let tokensOut = 0;
	let cost = 0;
	let contextTokens = 0;
	let model = member.model;
	let finalResponse = "";

	return new Promise<BoardMemberResult>((resolve, reject) => {
		const proc = spawn("pi", args, {
			shell: false,
			stdio: ["ignore", "pipe", "pipe"],
			env: subprocessEnv,
		});

		let buffer = "";
		let stderr = "";
		let wasAborted = false;

		const processLine = (line: string) => {
			if (!line.trim()) return;
			let event: any;
			try {
				event = JSON.parse(line);
			} catch {
				return;
			}

			// Track tool usage from board member subprocess
			if (event.type === "tool_execution_start") {
				onToolUse?.(event.toolName || "unknown", event.toolCallId || "", event.args || {});
			}

			// Stream text deltas for real-time updates
			if (event.type === "message_update" && event.assistantMessageEvent) {
				const ame = event.assistantMessageEvent;
				if (ame.type === "text_delta" && (ame.delta || ame.text)) {
					accumulatedText += ame.delta || ame.text;
					onText?.(accumulatedText);
				}
			}

			// Final message with usage stats
			if (event.type === "message_end" && event.message) {
				const msg = event.message;
				if (msg.role === "assistant") {
					// Extract full response text from content
					if (msg.content && Array.isArray(msg.content)) {
						for (const part of msg.content) {
							if (part.type === "text") {
								finalResponse = part.text;
							}
						}
					}

					// Extract usage stats
					const usage = msg.usage;
					if (usage) {
						tokensIn += usage.input || 0;
						tokensOut += usage.output || 0;
						cost += usage.cost?.total || 0;
						contextTokens = usage.totalTokens || 0;
					}
					if (msg.model) model = msg.model;
				}
			}
		};

		proc.stdout.on("data", (data: Buffer) => {
			buffer += data.toString();
			const lines = buffer.split("\n");
			buffer = lines.pop() || "";
			for (const line of lines) processLine(line);
		});

		proc.stderr.on("data", (data: Buffer) => {
			stderr += data.toString();
		});

		proc.on("close", (code: number | null) => {
			if (buffer.trim()) processLine(buffer);
			if (wasAborted) {
				reject(new Error("Board member call was aborted"));
				return;
			}
			if (code !== 0 && !finalResponse && !accumulatedText) {
				reject(
					new Error(
						`Board member ${member.name} process exited with code ${code}: ${stderr.slice(0, 500)}`,
					),
				);
				return;
			}
			resolve({
				response: finalResponse || accumulatedText,
				tokensIn,
				tokensOut,
				cost,
				contextTokens,
				model,
			});
		});

		proc.on("error", (err: Error) => {
			reject(new Error(`Failed to spawn pi for ${member.name}: ${err.message}`));
		});

		// Handle abort signal
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
}

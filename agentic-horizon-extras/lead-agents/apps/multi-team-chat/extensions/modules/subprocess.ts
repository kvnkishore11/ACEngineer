// ── Subprocess Spawner ───────────────────────────────────────────

import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { join } from "node:path";
import type { AgentConfig, SubprocessResult, ToolUse } from "./types";

/**
 * Resolve extension paths relative to THIS file's location (the source repo),
 * not the project root. This ensures enforcement works when running from any
 * directory via the `teams` alias.
 */
import { fileURLToPath } from "node:url";
const __extensionsDir = join(fileURLToPath(import.meta.url), "..", "..");
const ENFORCER_PATH = join(__extensionsDir, "domain-enforcer.ts");
const LEAD_DELEGATE_PATH = join(__extensionsDir, "lead-delegate.ts");
const TILLDONE_LEAD_PATH = join(__extensionsDir, "tilldone-lead.ts");

export async function callAgent(
	agent: AgentConfig,
	message: string,
	env: Record<string, string>,
	projectRoot: string,
	signal?: AbortSignal,
	onText?: (accumulated: string) => void,
	onToolCall?: (tool: ToolUse) => void,
	onToolUpdate?: (toolCallId: string, toolName: string, partialResult: any) => void,
	onToolEnd?: (toolCallId: string, toolName: string, result: any) => void,
	onUsage?: (stats: { tokensIn: number; tokensOut: number; cost: number; contextTokens: number }) => void,
): Promise<SubprocessResult> {
	const args: string[] = [
		"--mode", "json", "-p",
		"--no-extensions",                       // Don't auto-load project extensions
		"-e", ENFORCER_PATH,                     // Explicitly load domain enforcer
		"-e", LEAD_DELEGATE_PATH,                // Load lead delegate (self-exits if not a lead)
		"-e", TILLDONE_LEAD_PATH,                // Load tilldone (self-exits if not a lead)
		"--no-skills", "--no-prompt-templates", "--no-themes",
		"--session", agent.sessionFile,
	];

	if (!existsSync(agent.sessionFile)) {
		args.push("--system-prompt", agent.systemPrompt, "--model", agent.model);
	}

	args.push(message);

	// Inject domain + expertise + tool enforcement env vars
	const agentEnv: Record<string, string> = {
		...env,
		AGENT_DOMAIN_RULES: JSON.stringify(agent.domain),
		AGENT_EXPERTISE: JSON.stringify(agent.expertise || []),
		AGENT_ALLOWED_TOOLS: JSON.stringify(agent.tools || []),
		AGENT_PROJECT_ROOT: projectRoot,
	};

	let accumulatedText = "";
	let tokensIn = 0, tokensOut = 0, cost = 0, contextTokens = 0;
	let model = agent.model;
	let finalResponse = "";
	const toolCalls: ToolUse[] = [];

	return new Promise<SubprocessResult>((resolve, reject) => {
		const proc = spawn("pi", args, {
			shell: false,
			stdio: ["ignore", "pipe", "pipe"],
			env: agentEnv,
		});

		let buffer = "", stderr = "", wasAborted = false;

		const processLine = (line: string) => {
			if (!line.trim()) return;
			let event: any;
			try { event = JSON.parse(line); } catch { return; }

			// Text streaming
			if (event.type === "message_update" && event.assistantMessageEvent) {
				const ame = event.assistantMessageEvent;
				if (ame.type === "text_delta" && (ame.delta || ame.text)) {
					accumulatedText += ame.delta || ame.text;
					onText?.(accumulatedText);
				}
			}

			// Tool call detection — Pi emits these event types:
			//   message_update with assistantMessageEvent.type === "toolcall_start" (name in toolCall)
			//   tool_execution_start (top-level, toolName + args)
			if (event.type === "tool_execution_start" && event.toolName) {
				// Inject visual break into text stream between tool calls
				if (accumulatedText && !accumulatedText.endsWith("\n")) accumulatedText += "\n";
				onText?.(accumulatedText);
				const tu: ToolUse = { name: event.toolName, args: event.args || {}, callId: event.toolCallId };
				toolCalls.push(tu);
				onToolCall?.(tu);
			} else if (event.type === "message_update" && event.assistantMessageEvent?.type === "toolcall_start") {
				const tc = event.assistantMessageEvent.toolCall || event.assistantMessageEvent.partial?.content?.[0];
				const toolName = tc?.name;
				if (toolName) {
					const tu: ToolUse = { name: toolName, args: tc.arguments || {} };
					toolCalls.push(tu);
					onToolCall?.(tu);
				}
			}

			// Tool update — emitted when execute() calls onUpdate(partialResult)
			if (event.type === "tool_execution_update" && event.toolCallId) {
				onToolUpdate?.(event.toolCallId, event.toolName, event.partialResult);
			}

			// Tool end — emitted when execute() resolves with final result
			if (event.type === "tool_execution_end" && event.toolCallId) {
				onToolEnd?.(event.toolCallId, event.toolName, event.result);
				// If tool was blocked/errored, emit a rejected marker
				if (event.isError || event.result?.isError) {
					onToolCall?.({ name: event.toolName, args: {}, blocked: true } as any);
				}
			}

			// Message end — extract final response + usage
			if (event.type === "message_end" && event.message?.role === "assistant") {
				const msg = event.message;
				if (msg.content) for (const p of msg.content) { if (p.type === "text") finalResponse = p.text; }
				if (msg.usage) {
					tokensIn += msg.usage.input || 0;
					tokensOut += msg.usage.output || 0;
					cost += msg.usage.cost?.total || 0;
					contextTokens = msg.usage.totalTokens || 0;
					onUsage?.({ tokensIn, tokensOut, cost, contextTokens });
				}
				if (msg.model) model = msg.model;
			}
		};

		proc.stdout.on("data", (d: Buffer) => {
			buffer += d.toString();
			const lines = buffer.split("\n");
			buffer = lines.pop() || "";
			for (const l of lines) processLine(l);
		});
		proc.stderr.on("data", (d: Buffer) => { stderr += d.toString(); });
		proc.on("close", (code: number | null) => {
			if (buffer.trim()) processLine(buffer);
			if (wasAborted) { reject(new Error("Aborted")); return; }
			if (code !== 0 && !finalResponse && !accumulatedText) {
				reject(new Error(`${agent.name} exit ${code}: ${stderr.slice(0, 200)}`));
				return;
			}
			resolve({ response: finalResponse || accumulatedText, tokensIn, tokensOut, cost, contextTokens, model, toolCalls });
		});
		proc.on("error", (e: Error) => reject(new Error(`Spawn failed for ${agent.name}: ${e.message}`)));

		if (signal) {
			const kill = () => { wasAborted = true; proc.kill("SIGTERM"); setTimeout(() => { if (!proc.killed) proc.kill("SIGKILL"); }, 5000); };
			if (signal.aborted) kill(); else signal.addEventListener("abort", kill, { once: true });
		}
	});
}

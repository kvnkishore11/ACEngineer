// ── Shared Conversation Log ──────────────────────────────────────

import { appendFileSync, readFileSync, existsSync } from "node:fs";
import type { LogEntry } from "./types";

export function appendToLog(logPath: string, entry: LogEntry): void {
	appendFileSync(logPath, JSON.stringify(entry) + "\n", "utf-8");
}

export function readLog(logPath: string): LogEntry[] {
	if (!existsSync(logPath)) return [];
	try {
		const raw = readFileSync(logPath, "utf-8").trim();
		if (!raw) return [];
		return raw.split("\n").map(line => {
			try { return JSON.parse(line); } catch { return null; }
		}).filter(Boolean) as LogEntry[];
	} catch { return []; }
}

export function formatTranscript(entries: LogEntry[], maxEntries = 40): string {
	const recent = entries.slice(-maxEntries);
	if (recent.length === 0) return "(No conversation history yet.)";

	const lines: string[] = [];
	for (const e of recent) {
		const team = e.team ? ` [${e.team}]` : "";
		switch (e.type) {
			case "user":
				lines.push(`[User]: ${e.message}`);
				break;
			case "orchestrator":
				lines.push(`[Orchestrator]: ${e.message}`);
				break;
			case "delegate":
				lines.push(`[Orchestrator → ${e.to}]: ${e.message}`);
				break;
			case "lead":
				lines.push(`[${e.from}${team} Lead]: ${e.message}`);
				break;
			case "member":
				lines.push(`[${e.from}${team}]: ${e.message}`);
				break;
			case "synthesis":
				lines.push(`[${e.from}${team} Synthesis]: ${e.message}`);
				break;
			case "system":
				lines.push(`[System]: ${e.message}`);
				break;
		}
	}
	return lines.join("\n\n");
}

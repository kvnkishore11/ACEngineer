/**
 * Multi-Team Chat — Full Custom Chat UI (Nuclear Pattern)
 *
 * Replaces Pi's chatContainer via tui.children[1] with our own
 * ChatView component. Pi's brain (agent loop, tools, sessions)
 * stays intact — we only replace the DISPLAY layer.
 *
 * Usage: pi -e extensions/multi-team-chat.ts
 */

import { existsSync, mkdirSync, writeFileSync, readdirSync } from "node:fs";
import { join, isAbsolute } from "node:path";
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Text, truncateToWidth, visibleWidth, wrapTextWithAnsi } from "@mariozechner/pi-tui";
import { Type } from "@sinclair/typebox";

import type {
	MultiTeamConfig, OrchestratorConfig, TeamConfig, AgentStats, TeamChatDetails, LogEntry,
	TillDoneState, TillDoneMutation,
} from "./modules/types";
import { findProjectRoot, parseConfig, loadOrchestrator, loadTeams, loadDotEnv } from "./modules/config";
import { appendToLog, readLog, formatTranscript } from "./modules/log";
import { callAgent } from "./modules/subprocess";
import { buildOrchestratorPrompt } from "./modules/prompt";
import { parseHexColor, dim, bold, hexFg } from "./modules/theme";
import { isDomainAllowed, BASH_WRITE_PATTERNS, BASH_DELETE_PATTERNS } from "./modules/domain";
import {
	createState, addTask, addTasks, startTask, doneTask, updateTask, removeTask, clearState,
	applyMutation, renderTillDoneColumn, mergeColumns, STATUS_ICON,
} from "./modules/tilldone";

// Empty component — renders nothing
const EMPTY = { render: () => [] as string[], invalidate() { } };

// ── Chat Message Type ───────────────────────────────────────────

interface ChatMsg {
	id: number;
	from: string;
	color: string;
	text: string;
	timestamp: string;
	state: "thinking" | "streaming" | "done";
	role: "user" | "orchestrator" | "lead" | "member" | "system" | "delegation";
	team?: string;
	tools?: string[]; // tool emojis accumulated during execution
}

// ── Tool → Emoji map ────────────────────────────────────────────

const TOOL_EMOJI: Record<string, string> = {
	write: "📝",
	edit: "✏️",
	read: "📖",
	bash: "💻",
	grep: "🔍",
	find: "🔎",
	ls: "📁",
	glob: "📂",
	delegate: "🔀",
	tilldone: "📋",
};

function toolEmoji(name: string): string {
	return TOOL_EMOJI[name] || "🔧";
}

// ── Extension ───────────────────────────────────────────────────

export default function (pi: ExtensionAPI) {
	let config: MultiTeamConfig | null = null;
	let orch: OrchestratorConfig | null = null;
	let teams: TeamConfig[] = [];
	// ── --team flag ──────────────────────────────────────────────
	// Point to any config file: pi -e extensions/multi-team-chat.ts --team .pi/ml-team/config.yaml
	// Path is resolved relative to project root. Defaults to .pi/multi-team/multi-team-config.yaml.
	pi.registerFlag("team", {
		description: "Path to team config file (relative to project root or absolute). Defaults to .pi/multi-team/multi-team-config.yaml.",
		type: "string",
	});
	pi.registerFlag("list", {
		description: "List all available team configs and their agent trees.",
		type: "boolean",
	});

	let projectRoot: string | null = null;
	let subprocessEnv: Record<string, string> = { ...process.env } as Record<string, string>;
	let logPath = "";
	let sessionBaseDir = "";
	let currentSessionId = "";
	let activeElapsedMs = 0;
	let agentStartedAt = 0;
	let tuiRef: any = null;

	// ── TillDone state ──────────────────────────────────────────
	const tilldoneState: TillDoneState = createState();
	let nudgedThisCycle = false;

	// ── Stats ────────────────────────────────────────────────────
	const agentStats = new Map<string, AgentStats>();
	let orchCost = 0, orchTokensIn = 0, orchTokensOut = 0, orchContextTokens = 0, orchCalls = 0;
	const activeTeams = new Set<string>();

	function getStats(n: string): AgentStats {
		if (!agentStats.has(n)) agentStats.set(n, { cost: 0, tokensIn: 0, tokensOut: 0, contextTokens: 0, calls: 0 });
		return agentStats.get(n)!;
	}
	function addStats(n: string, c: number, ti: number, to: number, cx: number) {
		const s = getStats(n); s.cost += c; s.tokensIn += ti; s.tokensOut += to; s.contextTokens = cx; s.calls++;
	}
	function totalCost() { let t = orchCost; for (const s of agentStats.values()) t += s.cost; return t; }
	function totalTokens() {
		let i = orchTokensIn, o = orchTokensOut;
		for (const s of agentStats.values()) { i += s.tokensIn; o += s.tokensOut; }
		return { in: i, out: o };
	}
	function fmtT(n: number) { return n >= 1_000_000 ? `1M` : n < 1000 ? `${n}` : n < 100_000 ? `${(n / 1000).toFixed(1)}K` : `${Math.round(n / 1000)}K`; }
	function fmtC(n: number) { return `$${n.toFixed(3)}`; }
	function elapsed() {
		const total = activeElapsedMs + (agentStartedAt ? Date.now() - agentStartedAt : 0);
		const s = Math.floor(total / 1000);
		const h = Math.floor(s / 3600);
		const m = Math.floor((s % 3600) / 60);
		const sec = s % 60;
		if (h > 0) return `${h}h ${m.toString().padStart(2, "0")}m ${sec.toString().padStart(2, "0")}s`;
		return m > 0 ? `${m}m ${sec.toString().padStart(2, "0")}s` : `${sec}s`;
	}
	function ts() { return new Date().toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit", hour12: true }); }

	// ── Chat state ──────────────────────────────────────────────
	const msgs: ChatMsg[] = [];
	let nextId = 0;

	function addMsg(from: string, color: string, text: string, role: ChatMsg["role"], state: ChatMsg["state"] = "done", team?: string): number {
		const id = nextId++;
		msgs.push({ id, from, color, text, timestamp: ts(), state, role, team });
		return id;
	}
	/** addMsg + log to conversation in one call. Use for messages that don't have a separate explicit appendToLog. */
	function addMsgAndLog(from: string, color: string, text: string, role: ChatMsg["role"], team?: string): number {
		const id = addMsg(from, color, text, role, "done", team);
		if (logPath && text) {
			const type: LogEntry["type"] = role === "orchestrator" ? "orchestrator" : role === "user" ? "user" : role === "system" ? "system" : role === "delegation" ? "delegate" : role === "synthesis" ? "synthesis" : role === "lead" ? "lead" : "member";
			appendToLog(logPath, { from, message: text, timestamp: new Date().toISOString(), type, team });
		}
		return id;
	}
	function updateMsg(id: number, u: Partial<ChatMsg>) {
		const m = msgs.find(x => x.id === id);
		if (m) Object.assign(m, u);
	}

	// ── Simple markdown → ANSI ──────────────────────────────────

	function mdLine(line: string): string {
		// Headers → bold + bright
		if (line.match(/^#{1,3}\s/)) return bold(line.replace(/^#{1,3}\s+/, ""));
		// Bold **text**
		line = line.replace(/\*\*(.+?)\*\*/g, (_m, t) => bold(t));
		// Inline code `text`
		line = line.replace(/`([^`]+)`/g, (_m, t) => `\x1b[36m${t}\x1b[39m`);
		// Horizontal rules
		if (line.match(/^---+$/)) return dim("─".repeat(20));
		return line;
	}

	// ── @mention highlighting ───────────────────────────────────
	// Build regex from actual team/agent names so only real names match.
	const mentionNames: string[] = [];
	// Populated after config loads — called in session_start
	function buildMentionRegex() {
		if (orch) mentionNames.push(orch.name);
		for (const t of teams) {
			mentionNames.push(t.name, t.lead.name);
			for (const m of t.members) mentionNames.push(m.name);
		}
	}
	function highlightMentions(s: string): string {
		if (mentionNames.length === 0) return s;
		// Sort longest first so "Engineering Lead" matches before "Engineering"
		const sorted = [...mentionNames].sort((a, b) => b.length - a.length);
		const pattern = sorted.map(n => n.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|");
		return s.replace(new RegExp(`@(${pattern})`, "g"), m => hexFg("#7aa2f7", m));
	}

	// ── Bubble rendering ────────────────────────────────────────

	function renderBubble(m: ChatMsg, w: number): string[] {
		const { r, g, b } = parseHexColor(m.color);
		// Safety: every line MUST be truncated to w to avoid TUI crash
		const safe = (s: string) => truncateToWidth(s, w, "");

		// Pick black or white text based on background luminance
		const lum = (0.299 * r + 0.587 * g + 0.114 * b);
		const fg = lum > 140 ? "0;0;0" : "255;255;255";
		const badge = `\x1b[48;2;${r};${g};${b}m\x1b[38;2;${fg}m ${m.from.charAt(0).toUpperCase()} \x1b[0m`;
		const name = hexFg(m.color, bold(m.from));
		const stateIcon = m.state === "thinking" ? "  💭" : m.state === "streaming" ? "  💬" : "";
		const time = dim(m.timestamp);

		const left = `${badge}  ${name}${stateIcon}`;
		const pad = Math.max(2, w - visibleWidth(left) - visibleWidth(time) - 1);
		const lines: string[] = [safe(`${left}${" ".repeat(pad)}${time}`)];

		const bar = `\x1b[38;2;${r};${g};${b}m│\x1b[0m`;
		const indent = `     ${bar}  `;
		const bw = Math.max(20, w - 10);

		// Tool call stack — show individual emojis until a full row is used, then collapse.
		// Once collapsed, Nx = total hidden emojis (increments in row-sized chunks).
		// e.g. row fits 25: "📖...📖" → "25x 📖" → "25x 📖📖📖..." → "50x 📖" → ...
		if (m.tools?.length) {
			const indentW = visibleWidth(indent);
			const availW = Math.max(10, w - indentW - 1);

			const allStr = m.tools.join(" ");
			if (visibleWidth(allStr) <= availW) {
				// All emojis fit in one row — show them individually
				lines.push(safe(`${indent}${dim(allStr)}`));
			} else {
				// Calculate how many emojis fit per row
				let perRow = 0, testW = 0;
				for (let i = 0; i < m.tools.length; i++) {
					const ew = visibleWidth(m.tools[i]) + (i > 0 ? 1 : 0);
					if (testW + ew > availW) break;
					testW += ew;
					perRow++;
				}
				if (perRow < 1) perRow = 1;

				// Hidden = completed full rows × perRow (total hidden emoji count)
				const remainder = m.tools.length % perRow;
				const fullRows = remainder === 0
					? (m.tools.length / perRow) - 1
					: Math.floor(m.tools.length / perRow);
				const hiddenCount = fullRows * perRow;
				const visible = m.tools.slice(hiddenCount).join(" ");

				lines.push(safe(`${indent}${dim(`${hiddenCount}x ${visible}`)}`));
			}
		}

		if (m.state === "thinking") {
			lines.push(safe(`${indent}${dim("thinking...")}`));
		} else if (m.text) {
			const bl = m.text.split("\n").filter(l => l.trim()).map(l => highlightMentions(mdLine(l)));
			// Orchestrator + user get full output; team members stay truncated
			const noLimit = m.role === "orchestrator" || m.role === "user" || m.role === "system";
			const max = noLimit ? 9999 : m.state === "streaming" ? 4 : 6;
			if (m.state === "streaming") {
				for (const l of bl.slice(-max))
					for (const wl of wrapTextWithAnsi(l, bw)) lines.push(safe(`${indent}${wl}`));
			} else if (bl.length <= max) {
				for (const l of bl)
					for (const wl of wrapTextWithAnsi(l, bw)) lines.push(safe(`${indent}${wl}`));
			} else {
				for (let i = 0; i < max - 1; i++)
					for (const wl of wrapTextWithAnsi(bl[i], bw)) lines.push(safe(`${indent}${wl}`));
				lines.push(safe(`${indent}${dim(`··· ${bl.length - max + 1} more lines ···`)}`));
			}
		}
		lines.push("");
		return lines;
	}

	// ── ChatView — REPLACES Pi's chatContainer at tui.children[1]
	//
	// Returns ALL lines. The TUI handles viewport clipping (always anchored
	// to bottom) and terminal-native scrollback handles scroll-up for free.
	// No scroll state, no scroll offset, no scroll keybindings.

	let chatDirty = true;
	let chatCache: string[] | null = null;
	let chatCacheWidth = 0;

	const chatView = {
		render(width: number): string[] {
			if (chatCache && chatCacheWidth === width && !chatDirty) return chatCache;

			const allLines: string[] = [];
			for (const m of msgs) allLines.push(...renderBubble(m, width));

			// Return ALL lines — TUI auto-scrolls to bottom.
			// Old messages go into terminal scrollback (scroll-up is free).
			// Only pad top when content is shorter than screen (bottom-align).
			const rows = process.stdout.rows || 50;
			const available = Math.max(5, rows - 5);

			if (allLines.length < available) {
				// Bottom-align: pad top with empty lines so messages sit at bottom
				chatCache = [...new Array(available - allLines.length).fill(""), ...allLines];
			} else {
				// Content overflows — return raw lines; TUI handles viewport clipping
				chatCache = allLines;
			}
			chatCacheWidth = width;
			chatDirty = false;
			return chatCache;
		},
		invalidate() { chatDirty = true; chatCache = null; },
	};

	function refresh() {
		chatDirty = true;
		chatCache = null;
		try { tuiRef?.requestRender?.(); } catch { }
	}

	// ── Footer ──────────────────────────────────────────────────

	const CTX_DEFAULT = 200_000;
	// Dynamic context window cache — populated from model registry at session_start
	const ctxWindowCache = new Map<string, number>();
	let sessionCtx: any = null; // ctx reference for model registry lookups

	function ctxWindow(model?: string): number {
		if (!model) return CTX_DEFAULT;
		// Check cache first
		if (ctxWindowCache.has(model)) return ctxWindowCache.get(model)!;
		// Try model registry lookup
		if (sessionCtx?.modelRegistry) {
			const parts = model.split("/");
			// Handle provider/id (e.g. "anthropic/claude-opus-4-6")
			// and provider/org/id (e.g. "openrouter/openai/gpt-5.4")
			const provider = parts[0];
			const id = parts.slice(1).join("/");
			try {
				const m = sessionCtx.modelRegistry.find(provider, id);
				if (m?.contextWindow) {
					ctxWindowCache.set(model, m.contextWindow);
					return m.contextWindow;
				}
			} catch { /* model not in registry */ }
		}
		return CTX_DEFAULT;
	}
	let showWorkers = false;

	function teamCost(t: TeamConfig): number {
		let c = getStats(t.lead.name).cost;
		for (const m of t.members) c += getStats(m.name).cost;
		return c;
	}

	function fmtCtx(used: number, model?: string): string {
		const max = ctxWindow(model);
		const remaining = Math.max(0, max - used);
		if (used === 0) return `🧠${fmtT(max)}`;
		return `🧠${fmtT(Math.max(0, remaining))}`;
	}

	function setupFooter(ctx: any) {
		// /toggle-workers command
		pi.registerCommand("toggle-workers", {
			description: "Show/hide team members in the footer",
			handler: async () => {
				showWorkers = !showWorkers;
				refresh();
			},
		});

		// /tilldone command
		pi.registerCommand("tilldone", {
			description: "Show the TillDone task list",
			handler: async () => {
				if (tilldoneState.tasks.length === 0) {
					addMsg("System", "#555555", "No TillDone list active.", "system");
				} else {
					const taskLines: string[] = [bold(tilldoneState.title || "TillDone")];
					if (tilldoneState.description) taskLines.push(dim(tilldoneState.description));
					taskLines.push("");
					const doneCount = tilldoneState.tasks.filter(t => t.status === "done").length;
					taskLines.push(`Progress: ${doneCount}/${tilldoneState.tasks.length}`);
					taskLines.push("");
					for (const t of tilldoneState.tasks) {
						const icon = STATUS_ICON[t.status];
						const team = t.team ? ` (${t.team})` : "";
						taskLines.push(`${icon} #${t.id} ${t.text}${team}`);
					}
					addMsg("System", "#72f1b8", taskLines.join("\n"), "system");
				}
				refresh();
			},
		});

		ctx.ui.setFooter((_tui: any, _theme: any, _fd: any) => ({
			invalidate() { },
			render(w: number): string[] {
				const shortModel = (s: string) => s.replace(/^anthropic\//, "").replace(/^openai\//, "");
				const lastDir = (p: string) => p.split("/").filter(Boolean).pop() || p;
				const icon = (color: string, active: boolean) =>
					active ? "⚡" : hexFg(color, "◆");

				// ── Agent tree (left column) ────────────────────
				const leftLines: string[] = [];

				const dirName = lastDir(projectRoot || "");
				leftLines.push(truncateToWidth(` ${dim(showWorkers ? `${dirName} │ ${currentSessionId} │ ${elapsed()}` : `${dirName} │ ${elapsed()}`)}`, w));

				const orchDiamond = icon(orch?.color || "#72f1b8", busy);
				const tc = totalCost();
				let orchLine = `${orchDiamond} ${hexFg(orch?.color || "#72f1b8", "Orch")}`;
				orchLine += ` ${dim(`💰${fmtC(tc)} ${fmtCtx(orchContextTokens, orch?.model)}${showWorkers ? ` ${shortModel(orch?.model || "")}` : ""}`)}`;
				leftLines.push(truncateToWidth(` └─ ${orchLine}`, w));

				for (let i = 0; i < teams.length; i++) {
					const t = teams[i];
					const ls = getStats(t.lead.name);
					const a = activeTeams.has(t.name);
					const isLastLead = i === teams.length - 1;
					const leadConn = isLastLead ? "└─" : "├─";
					const leadCont = isLastLead ? "   " : "│  ";
					const leadDiamond = icon(t.lead.color, a);
					let leadLine = `${leadDiamond} ${hexFg(t.lead.color, t.lead.name)}`;
					const tCost = teamCost(t);
					leadLine += ` ${dim(`💰${fmtC(tCost)} ${fmtCtx(ls.contextTokens, t.lead.model)}${showWorkers ? ` ${shortModel(t.lead.model)}` : ""}`)}`;
					leftLines.push(truncateToWidth(`    ${leadConn} ${leadLine}`, w));

					if (showWorkers) {
						for (let j = 0; j < t.members.length; j++) {
							const m = t.members[j];
							const ms = getStats(m.name);
							const memberConn = j === t.members.length - 1 ? "└─" : "├─";
							const memberActive = msgs.some(b => b.from === m.name && (b.state === "streaming" || b.state === "thinking"));
							const memberDiamond = icon(m.color, memberActive);
							const memberLine = `${memberDiamond} ${hexFg(m.color, m.name)} ${dim(`💰${fmtC(ms.cost)} ${fmtCtx(ms.contextTokens, m.model)} ${shortModel(m.model)}`)}`;
							leftLines.push(truncateToWidth(`    ${leadCont} ${memberConn} ${memberLine}`, w));
						}
					}
				}

				// ── Two-column merge when TillDone is active ────
				if (tilldoneState.tasks.length > 0) {
					const leftW = Math.floor(w * 0.50);
					const rightW = w - leftW;
					const rightLines = renderTillDoneColumn(tilldoneState, rightW, showWorkers);
					return mergeColumns(leftLines, rightLines, leftW, w);
				}

				return leftLines;
			},
		}));
	}

	// ══════════════════════════════════════════════════════════════
	// SESSION START — THE TAKEOVER
	// ══════════════════════════════════════════════════════════════

	pi.on("session_start", async (_event, ctx) => {
		sessionCtx = ctx; // Store for model registry lookups
		// ─── THE TAKEOVER (always, even without config) ────────
		ctx.ui.setHeader((tui: any) => {
			if (!tuiRef && tui?.children) {
				tuiRef = tui;
				tui.children[1] = chatView;   // Our chat replaces Pi's chatContainer
				tui.children[2] = EMPTY;      // Kill pendingMessagesContainer
				tui.children[3] = EMPTY;      // Kill statusContainer
			}
			return EMPTY;
		});

		// ─── LIST FLAG ───────────────────────────────────────
		if (pi.getFlag("list")) {
			// Find project root without a custom config — just look for any .pi/multi-team/
			const listRoot = findProjectRoot(ctx.cwd);
			if (!listRoot) {
				addMsg("System", "#ff6e96", [
					bold("Multi-Team Chat — no configs found"),
					"",
					`No .pi/multi-team/ directory found in ${ctx.cwd} or any parent.`,
				].join("\n"), "system");
				refresh();
				return;
			}

			const multiTeamDir = join(listRoot, ".pi", "multi-team");
			let yamlFiles: string[] = [];
			try {
				yamlFiles = readdirSync(multiTeamDir)
					.filter(f => f.endsWith(".yaml") || f.endsWith(".yml"))
					.sort();
			} catch { /* dir doesn't exist or unreadable */ }

			if (yamlFiles.length === 0) {
				addMsg("System", "#ff6e96", [
					bold("Multi-Team Chat — no configs found"),
					"",
					`No .yaml files in ${multiTeamDir}`,
				].join("\n"), "system");
				refresh();
				return;
			}

			const lines: string[] = [bold("Available Team Configs"), ""];

			for (const file of yamlFiles) {
				const relPath = `.pi/multi-team/${file}`;
				const absPath = join(multiTeamDir, file);

				let parsed: ReturnType<typeof parseConfig>;
				try {
					parsed = parseConfig(listRoot, absPath);
				} catch (err: any) {
					lines.push(`${hexFg("#ff6e96", `✗ ${relPath}`)}`);
					lines.push(`  ${dim(`Parse error: ${err.message}`)}`);
					lines.push("");
					continue;
				}

				if (!parsed) {
					lines.push(`${hexFg("#ff6e96", `✗ ${relPath}`)}`);
					lines.push(`  ${dim("Failed to parse — check YAML syntax")}`);
					lines.push("");
					continue;
				}

				// Validate structure
				const errors: string[] = [];
				if (!parsed.orchestrator?.path) errors.push("Missing orchestrator.path");
				if (!parsed.orchestrator?.name) errors.push("Missing orchestrator.name");
				for (let ti = 0; ti < parsed.teams.length; ti++) {
					const t = parsed.teams[ti];
					if (!t.name) errors.push(`teams[${ti}]: missing team-name`);
					if (!t.lead?.name) errors.push(`teams[${ti}]: missing lead.name`);
					if (!t.lead?.path) errors.push(`teams[${ti}]: missing lead.path`);
					if (t.lead?.path && !existsSync(join(listRoot, t.lead.path))) {
						errors.push(`teams[${ti}]: lead file not found: ${t.lead.path}`);
					}
					for (let mi = 0; mi < t.members.length; mi++) {
						const m = t.members[mi];
						if (!m.name) errors.push(`teams[${ti}].members[${mi}]: missing name`);
						if (!m.path) errors.push(`teams[${ti}].members[${mi}]: missing path`);
						if (m.path && !existsSync(join(listRoot, m.path))) {
							errors.push(`teams[${ti}].members[${mi}]: file not found: ${m.path}`);
						}
					}
				}

				if (errors.length > 0) {
					lines.push(`${hexFg("#ff9e64", `⚠ ${relPath}`)}`);
					for (const e of errors) lines.push(`  ${hexFg("#ff6e96", `✗ ${e}`)}`);
					lines.push("");
					continue;
				}

				// Valid config — render tree with models
				// Helper: resolve model for an agent ref (config override > frontmatter > default)
				const agentModel = (ref: { path: string; model?: string }): string => {
					if (ref.model) return ref.model;
					try {
						const content = require("node:fs").readFileSync(join(listRoot, ref.path), "utf-8");
						const fm = content.match(/^---\s*\n([\s\S]*?)\n---/);
						if (fm) { const mm = fm[1].match(/^model:\s*(.+)/m); if (mm) return mm[1].trim(); }
					} catch {}
					return "anthropic/claude-sonnet-4-6";
				};
				const shortModel = (m: string) => m.replace(/^anthropic\//, "").replace(/^openrouter\//, "");

				lines.push(`${hexFg("#72f1b8", `✓ ${relPath}`)}`);
				lines.push(`  ${hexFg(parsed.orchestrator.color || "#72f1b8", parsed.orchestrator.name)} ${dim(`(${shortModel(agentModel(parsed.orchestrator))})`)}`);

				for (let ti = 0; ti < parsed.teams.length; ti++) {
					const t = parsed.teams[ti];
					const isLastTeam = ti === parsed.teams.length - 1;
					const teamConn = isLastTeam ? "└─" : "├─";
					const teamCont = isLastTeam ? "   " : "│  ";
					lines.push(`  ${teamConn} ${hexFg(t.lead.color || t.color, t.lead.name)} ${dim(`(${shortModel(agentModel(t.lead))})`)}`);
					for (let mi = 0; mi < t.members.length; mi++) {
						const m = t.members[mi];
						const isLastMember = mi === t.members.length - 1;
						const memConn = isLastMember ? "└─" : "├─";
						lines.push(`  ${teamCont} ${memConn} ${m.name} ${dim(`(${shortModel(agentModel(m))})`)}`);
					}
				}
				lines.push("");
			}

			lines.push(dim(`Usage: teams --team .pi/multi-team/<config>.yaml`));

			addMsg("System", "#72f1b8", lines.join("\n"), "system");
			refresh();
			// Fall through to load the default config normally
		}

		// ─── CONFIG CHECK ──────────────────────────────────────
		// --team flag: point to any config file relative to project root or absolute
		// e.g. pi -e extensions/multi-team-chat.ts --team .pi/ml-team/config.yaml
		const teamFlag = pi.getFlag("team");
		const customConfig = typeof teamFlag === "string" && teamFlag ? teamFlag : undefined;

		projectRoot = findProjectRoot(ctx.cwd, customConfig);
		if (!projectRoot) {
			if (customConfig) {
				// Bad --team flag: no .pi/ directory found anywhere up the tree
				addMsg("System", "#ff6e96", [
					bold("Multi-Team Chat — --team flag error"),
					"",
					`  No .pi/ directory found in ${ctx.cwd} or any parent.`,
					`  Run from your project root when using --team.`,
					"",
					`  Passed: --team ${customConfig}`,
				].join("\n"), "system");
			} else {
				// No config at all — show full setup guide
				addMsg("System", "#ff6e96", [
					bold("Multi-Team Chat — config not found"),
					"",
					"",
					`No .pi/multi-team/multi-team-config.yaml in ${ctx.cwd}`,
					"",
					"",
					bold("Setup steps:"),
					"",
					`  1. Copy team config from the source repo:`,
					`     cp -r <source-repo>/.pi/multi-team/ ${ctx.cwd}/.pi/multi-team/`,
					"",
					`  2. Customize your agents for your project's domain`,
					`     .pi/multi-team/agents/*.md`,
					"",
					`  3. Configure your team roster`,
					`     .pi/multi-team/multi-team-config.yaml`,
					"",
					`  4. Re-run your alias (e.g. teams)`,
					"",
					"",
					dim("First time? Run 'just install' from the source repo."),
				].join("\n"), "system");
			}
			refresh();
			return;
		}

		// Resolve config path: absolute as-is, relative resolved from project root
		const configPath = customConfig
			? (isAbsolute(customConfig) ? customConfig : join(projectRoot, customConfig))
			: undefined;

		// Validate custom config file exists before attempting to parse
		if (configPath && !existsSync(configPath)) {
			addMsg("System", "#ff6e96", [
				bold("Multi-Team Chat — --team file not found"),
				"",
				`  Passed:   --team ${customConfig}`,
				`  Resolved: ${configPath}`,
				`  Root:     ${projectRoot}`,
				"",
				dim("Relative paths resolve from project root (nearest .pi/ ancestor)."),
				dim("Use an absolute path to reference a file outside the project."),
			].join("\n"), "system");
			refresh();
			return;
		}

		config = parseConfig(projectRoot, configPath);
		if (!config) {
			const label = configPath ?? join(projectRoot, ".pi/multi-team/multi-team-config.yaml");
			addMsg("System", "#ff6e96", [
				bold("Multi-Team Chat — config parse error"),
				"",
				`  Check YAML syntax in:`,
				`  ${label}`,
			].join("\n"), "system");
			refresh();
			return;
		}

		// ─── LOAD SYSTEM ───────────────────────────────────────
		let configWarnings: string[] = [];
		try {
			configWarnings = [];
			orch = loadOrchestrator(projectRoot, config, configWarnings);
			subprocessEnv = loadDotEnv(projectRoot);
			const sessionId = Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
			currentSessionId = sessionId;
			sessionBaseDir = join(projectRoot, config.paths.sessions, sessionId);
			mkdirSync(sessionBaseDir, { recursive: true });
			logPath = join(sessionBaseDir, "conversation.jsonl");
			teams = loadTeams(projectRoot, config, sessionBaseDir, logPath, configWarnings);
			activeElapsedMs = 0;

			// ── Write resolved system prompts for inspection ────────
			const promptsDir = join(sessionBaseDir, "system-prompts");
			mkdirSync(promptsDir, { recursive: true });
			const orchFullPrompt = buildOrchestratorPrompt(orch.basePrompt, teams, logPath, projectRoot, orch.domain, sessionBaseDir, config?.sharedContext || []);
			writeFileSync(join(promptsDir, "orchestrator.md"), orchFullPrompt);
			for (const team of teams) {
				const slug = (n: string) => n.toLowerCase().replace(/\s+/g, "-");
				writeFileSync(join(promptsDir, `${slug(team.lead.name)}.md`), team.lead.systemPrompt);
				for (const member of team.members) {
					writeFileSync(join(promptsDir, `${slug(member.name)}.md`), member.systemPrompt);
				}
			}

			appendToLog(logPath, { from: "System", message: "Session started.", timestamp: new Date().toISOString(), type: "system" });

			setupFooter(ctx);
			buildMentionRegex();

			// ── Register .claude/commands/ and .claude/skills/ from project root ──
			const claudeCommandsDir = join(projectRoot, ".claude", "commands");
			if (existsSync(claudeCommandsDir)) {
				for (const file of readdirSync(claudeCommandsDir)) {
					if (!file.endsWith(".md")) continue;
					const name = file.replace(/\.md$/, "");
					const filePath = join(claudeCommandsDir, file);
					pi.registerCommand(name, {
						description: `Command: .claude/commands/${file}`,
						handler: async (args, cmdCtx) => {
							const content = readFileSync(filePath, "utf-8")
								.replace(/^---[\s\S]*?---\n*/, ""); // strip frontmatter
							const expanded = args ? `${content}\n\nArguments: ${args}` : content;
							pi.sendUserMessage(expanded);
						},
					});
				}
			}
			const claudeSkillsDir = join(projectRoot, ".claude", "skills");
			if (existsSync(claudeSkillsDir)) {
				for (const entry of readdirSync(claudeSkillsDir, { withFileTypes: true })) {
					if (!entry.isDirectory()) continue;
					const skillMd = join(claudeSkillsDir, entry.name, "SKILL.md");
					if (!existsSync(skillMd)) continue;
					pi.registerCommand(`skill:${entry.name}`, {
						description: `Skill: .claude/skills/${entry.name}`,
						handler: async (args, cmdCtx) => {
							const content = readFileSync(skillMd, "utf-8")
								.replace(/^---[\s\S]*?---\n*/, ""); // strip frontmatter
							const expanded = args ? `${content}\n\nArguments: ${args}` : content;
							pi.sendUserMessage(expanded);
						},
					});
				}
			}

			// Welcome message — agent tree with models and colored leads/orch
			const shortModel = (m: string) => m.replace(/^anthropic\//, "").replace(/^openai\//, "");
			const orchModel = shortModel(orch.model);
			const treeLines: string[] = [bold("Your Agent Teams"), `${hexFg(orch.color, orch.name)} ${dim(`(${orchModel})`)}`];
			for (let i = 0; i < teams.length; i++) {
				const t = teams[i];
				const isLastTeam = i === teams.length - 1;
				const teamConn = isLastTeam ? "└─" : "├─";
				const teamCont = isLastTeam ? "   " : "│  ";
				treeLines.push(`${teamConn} ${hexFg(t.lead.color, t.lead.name)} ${dim(`(${shortModel(t.lead.model)})`)}`);
				for (let j = 0; j < t.members.length; j++) {
					const m = t.members[j];
					const isLastMember = j === t.members.length - 1;
					const memConn = isLastMember ? "└─" : "├─";
					treeLines.push(`${teamCont} ${memConn} ${m.name} ${dim(`(${shortModel(m.model)})`)}`);
				}
			}
			addMsgAndLog("System", "#555555", treeLines.join("\n"), "system");

			// Surface config warnings as system messages (deduplicated)
			for (const w of [...new Set(configWarnings)]) {
				addMsgAndLog("System", "#ff9e64", `⚠️ ${w}`, "system");
			}
			refresh();

		} catch (err: any) {
			// Show fatal errors as a system message instead of blank screen
			const msg = err?.message || String(err);
			addMsg("System", "#ff6e96", [
				bold("Multi-Team Chat — startup error"),
				"",
				"",
				msg,
				"",
				"",
				dim("Fix the issue above and re-run your alias."),
			].join("\n"), "system");
			refresh();
		}
	});

	// ── Capture context window from Pi's model registry ─────────

	// ── System prompt ───────────────────────────────────────────

	pi.on("before_agent_start", async () => {
		if (!orch || !teams.length || !projectRoot) return;
		return { systemPrompt: buildOrchestratorPrompt(orch.basePrompt, teams, logPath, projectRoot, orch.domain, sessionBaseDir, config?.sharedContext || []) };
	});

	// ── Orchestrator domain + expertise enforcement ─────────────

	/**
	 * Check expertise first — exact file match overrides domain.
	 * Returns true (allow), false (deny), or null (no match, fall through).
	 */
	function checkOrchestratorExpertise(filePath: string, operation: "read" | "upsert"): boolean | null {
		if (!orch || !orch.expertise.length || !projectRoot) return null;
		const abs = filePath.startsWith("/") ? filePath : (projectRoot + "/" + filePath);
		for (const exp of orch.expertise) {
			if (abs === exp.absPath) {
				if (operation === "read") return true;
				if (operation === "upsert") return exp.updatable;
			}
		}
		return null;
	}

	pi.on("tool_call", async (event) => {
		if (!orch || !projectRoot) return undefined;

		const toolName = event.toolName;
		const input = event.input as Record<string, any>;

		// Tool allowlist — if specified, block anything not listed (delegate always allowed)
		if (orch.tools.length > 0 && toolName !== "delegate" && !orch.tools.includes(toolName)) {
			const m = msgs.find(x => x.id === orchId);
			if (m) { m.tools = m.tools || []; m.tools.push("❌"); refresh(); }
			return { block: true, reason: `Orchestrator: tool '${toolName}' not allowed. Permitted: ${orch.tools.join(", ")}` };
		}

		const domain = orch.domain;
		if (!domain || domain.length === 0) return undefined;

		// Our delegate tool is always allowed
		if (toolName === "delegate") return undefined;

		// Read-only tools
		if (toolName === "read" || toolName === "grep" || toolName === "find" || toolName === "ls" || toolName === "glob") {
			const path = input.path || input.file_path || ".";
			// Expertise override
			const expResult = checkOrchestratorExpertise(path, "read");
			if (expResult === true) return undefined;
			if (!isDomainAllowed(path, "read", domain, projectRoot)) {
				return { block: true, reason: `Orchestrator domain: read denied for '${path}'` };
			}
			return undefined;
		}

		// Write tools — expertise override allows writes to personal files
		if (toolName === "write" || toolName === "edit") {
			const path = input.path || input.file_path || "";
			if (!path) return undefined;
			// Expertise override
			const expResult = checkOrchestratorExpertise(path, "upsert");
			if (expResult === true) return undefined;
			if (expResult === false) {
				return { block: true, reason: `Orchestrator expertise: file is read-only` };
			}
			if (!isDomainAllowed(path, "upsert", domain, projectRoot)) {
				return { block: true, reason: `Orchestrator domain: write denied for '${path}'` };
			}
			return undefined;
		}

		// Bash — heuristic analysis
		if (toolName === "bash") {
			const command = (input.command || "") as string;
			const anyDelete = domain.some(r => r.delete);
			const anyUpsert = domain.some(r => r.upsert) || orch.expertise.some(e => e.updatable);

			if (!anyDelete && BASH_DELETE_PATTERNS.some(p => p.test(command))) {
				return { block: true, reason: `Orchestrator domain: delete not permitted` };
			}
			if (!anyUpsert && BASH_WRITE_PATTERNS.some(p => p.test(command))) {
				return { block: true, reason: `Orchestrator domain: write not permitted` };
			}
			return undefined;
		}

		return undefined;
	});

	// ── Input: intercept → our bubble → forward to agent ────────

	let busy = false;

	pi.on("input", async (event) => {
		if ((event as any).source === "extension") return { action: "continue" as const };
		nudgedThisCycle = false;
		const text = event.text?.trim();
		if (!text || !logPath) return { action: "handled" as const };

		if (busy) {
			addMsg("System", "#555555", dim("⏳ Working — waiting for current task to complete."), "system");
			refresh();
			return { action: "handled" as const };
		}

		busy = true;
		addMsg("You", "#4a90d9", text, "user");
		appendToLog(logPath, { from: "User", message: text, timestamp: new Date().toISOString(), type: "user" });
		addMsg(orch?.name || "Orchestrator", orch?.color || "#72f1b8", "", "orchestrator", "thinking");
		refresh();

		pi.sendUserMessage(text);
		return { action: "handled" as const };
	});

	// ── Orchestrator streaming → chat bubbles ────────────────────

	let orchId = -1, orchText = "", orchToolCalled = false;

	// ── Model change — update context window cache for orchestrator ──
	pi.on("model_select", async (event: any) => {
		if (event.model?.contextWindow) {
			const key = `${event.model.provider}/${event.model.id}`;
			ctxWindowCache.set(key, event.model.contextWindow);
			refresh();
		}
	});

	pi.on("agent_start", async () => {
		agentStartedAt = Date.now();
		orchText = "";
		orchToolCalled = false;
		for (let i = msgs.length - 1; i >= 0; i--) {
			if (msgs[i].role === "orchestrator" && msgs[i].state === "thinking") { orchId = msgs[i].id; break; }
		}
	});

	pi.on("message_update", async (event) => {
		const ame = (event as any).assistantMessageEvent;
		if (ame?.type === "text_delta" && (ame.delta || ame.text)) {
			const delta = ame.delta || ame.text;

			// After a tool call, orchestrator resumes → NEW bubble at bottom
			if (orchToolCalled && orchId >= 0) {
				// Skip empty/whitespace deltas — don't create a hollow bubble between consecutive delegates
				if (!delta.trim()) return;
				updateMsg(orchId, { state: "done" });
				orchText = delta;
				orchId = addMsg(orch?.name || "Orchestrator", orch?.color || "#72f1b8", delta, "orchestrator", "streaming");
				orchToolCalled = false;
				refresh();
				return;
			}

			orchText += delta;
			if (orchId >= 0) { updateMsg(orchId, { text: orchText, state: "streaming" }); refresh(); }
		}
	});

	pi.on("tool_call", async (event) => {
		const toolName = (event as any).toolName || (event as any).name || "delegate";
		const toolArgs = (event as any).args || (event as any).input || {};

		if (toolName === "delegate" && toolArgs.question) {
			// Finalize current bubble only on delegation — this is a meaningful split point
			if (orchId >= 0 && orchText.trim()) {
				updateMsg(orchId, { text: orchText, state: "done" });
				appendToLog(logPath, { from: "Orchestrator", message: orchText.trim(), timestamp: new Date().toISOString(), type: "orchestrator" });
			}
			// Build @mentions from teams param
			const teamsParam = toolArgs.teams;
			let mentions = "";
			if (teamsParam === "all") {
				mentions = teams.map(t => `@${t.name}`).join(" ");
			} else if (typeof teamsParam === "string") {
				mentions = `@${teamsParam}`;
			} else if (Array.isArray(teamsParam)) {
				mentions = teamsParam.map((t: string) => `@${t}`).join(" ");
			}
			const preview = toolArgs.question;
			addMsg(orch?.name || "Orchestrator", orch?.color || "#72f1b8", `${mentions} ${preview}`, "orchestrator", "done");
			orchToolCalled = true;
			orchText = "";
			refresh();
		} else {
			// Non-delegate tool — badge the bubble + inline emoji
			const emoji = toolEmoji(toolName);
			if (orchId >= 0) {
				const m = msgs.find(x => x.id === orchId);
				if (m) { m.tools = m.tools || []; m.tools.push(emoji); }
			}
			// Inject emoji at current position — only if there's real text (otherwise header row handles it)
			if (orchText.trim()) {
				orchText += `${emoji} `;
				if (orchId >= 0) { updateMsg(orchId, { text: orchText, state: "streaming" }); }
			}
			refresh();
		}
	});

	pi.on("message_end", async (event) => {
		const m = (event as any).message;
		if (m?.role === "assistant" && m.usage) {
			orchCost += m.usage.cost?.total || 0;
			orchTokensIn += m.usage.input || 0;
			orchTokensOut += m.usage.output || 0;
			orchContextTokens = m.usage.totalTokens || 0;
			orchCalls++;
			refresh();
		}
	});

	pi.on("agent_end", async () => {
		if (orchId >= 0) {
			if (orchText.trim()) {
				updateMsg(orchId, { text: orchText, state: "done" });
				appendToLog(logPath, { from: "Orchestrator", message: orchText.trim(), timestamp: new Date().toISOString(), type: "orchestrator" });
			} else {
				// Aborted or empty — remove the empty bubble
				const idx = msgs.findIndex(x => x.id === orchId);
				if (idx >= 0) msgs.splice(idx, 1);
			}
		}
		// Clean up any thinking/streaming bubbles left by abort
		for (const m of msgs) {
			if (m.state === "thinking" || m.state === "streaming") {
				updateMsg(m.id, { state: "done", text: m.text || "Cancelled" });
			}
		}
		orchId = -1; orchText = ""; orchToolCalled = false;
		activeTeams.clear();
		if (agentStartedAt) { activeElapsedMs += Date.now() - agentStartedAt; agentStartedAt = 0; }
		busy = false;
		refresh();

		// ── TillDone nudge — continue if tasks remain ────────
		if (tilldoneState.tasks.length > 0 && !nudgedThisCycle) {
			const incomplete = tilldoneState.tasks.filter(t => t.status !== "done");
			if (incomplete.length > 0) {
				nudgedThisCycle = true;
				const taskList = incomplete
					.map(t => `  ${STATUS_ICON[t.status]} #${t.id}: ${t.text}`)
					.join("\n");
				addMsg("System", "#ff9e64",
					`⚠️ ${incomplete.length} task(s) remain:\n\n${taskList}\n\nContinue working or mark them done.`,
					"system"
				);
				refresh();
				pi.sendMessage(
					{
						customType: "tilldone-nudge",
						content: `You still have ${incomplete.length} incomplete TillDone task(s):\n\n${taskList}\n\nEither continue delegating to complete them or mark them done with \`tilldone done\`. Don't stop until it's done!`,
						display: false,
					},
					{ triggerTurn: true },
				);
			}
		}
	});

	// ── TillDone tool (orchestrator) ────────────────────────────

	pi.registerTool({
		name: "tilldone",
		label: "TillDone",
		description:
			"Manage the task list. Create a list before delegating substantial work. " +
			"Actions: new-list (text=title, description), add (text or texts[] for batch), " +
			"start (id — mark inprogress), done (id — mark complete), " +
			"update (id + text), remove (id), list, clear.",
		parameters: Type.Object({
			action: Type.Union([
				Type.Literal("new-list"), Type.Literal("add"), Type.Literal("start"),
				Type.Literal("done"), Type.Literal("update"), Type.Literal("remove"),
				Type.Literal("list"), Type.Literal("clear"),
			], { description: "Action to perform" }),
			text: Type.Optional(Type.String({ description: "Task text (for add/update), or list title (for new-list)" })),
			texts: Type.Optional(Type.Array(Type.String(), { description: "Multiple task texts (for add batch)" })),
			description: Type.Optional(Type.String({ description: "List description (for new-list)" })),
			id: Type.Optional(Type.Number({ description: "Task ID (for start/done/update/remove)" })),
			team: Type.Optional(Type.String({ description: "Team name to assign (for add). Assign the team that will own this task." })),
		}),

		async execute(_id, params) {
			switch (params.action) {
				case "new-list": {
					if (!params.text) return { content: [{ type: "text" as const, text: "Error: text (title) required for new-list" }] };
					clearState(tilldoneState);
					tilldoneState.title = params.text;
					tilldoneState.description = params.description || undefined;
					refresh();
					return { content: [{ type: "text" as const, text: `New list: "${tilldoneState.title}"${tilldoneState.description ? ` — ${tilldoneState.description}` : ""}` }] };
				}
				case "add": {
					const items = params.texts?.length ? params.texts : params.text ? [params.text] : [];
					if (items.length === 0) return { content: [{ type: "text" as const, text: "Error: text or texts required for add" }] };
					const teamColor = params.team ? teams.find(t => t.name.toLowerCase() === params.team!.toLowerCase())?.color : undefined;
					const added = addTasks(tilldoneState, items, params.team, teamColor);
					const msg = added.length === 1 ? `Added task #${added[0].id}: ${added[0].text}${params.team ? ` [${params.team}]` : ""}` : `Added ${added.length} tasks: ${added.map(t => `#${t.id}`).join(", ")}${params.team ? ` [${params.team}]` : ""}`;
					refresh();
					return { content: [{ type: "text" as const, text: msg }] };
				}
				case "start": {
					if (params.id === undefined) return { content: [{ type: "text" as const, text: "Error: id required for start" }] };
					const task = startTask(tilldoneState, params.id);
					if (!task) return { content: [{ type: "text" as const, text: `Task #${params.id} not found` }] };
					refresh();
					return { content: [{ type: "text" as const, text: `Task #${params.id} → inprogress` }] };
				}
				case "done": {
					if (params.id === undefined) return { content: [{ type: "text" as const, text: "Error: id required for done" }] };
					const task = doneTask(tilldoneState, params.id);
					if (!task) return { content: [{ type: "text" as const, text: `Task #${params.id} not found` }] };
					refresh();
					return { content: [{ type: "text" as const, text: `Task #${params.id} → done` }] };
				}
				case "update": {
					if (params.id === undefined) return { content: [{ type: "text" as const, text: "Error: id required for update" }] };
					if (!params.text) return { content: [{ type: "text" as const, text: "Error: text required for update" }] };
					const task = updateTask(tilldoneState, params.id, params.text);
					if (!task) return { content: [{ type: "text" as const, text: `Task #${params.id} not found` }] };
					refresh();
					return { content: [{ type: "text" as const, text: `Updated #${params.id}: "${task.text}"` }] };
				}
				case "remove": {
					if (params.id === undefined) return { content: [{ type: "text" as const, text: "Error: id required for remove" }] };
					const task = removeTask(tilldoneState, params.id);
					if (!task) return { content: [{ type: "text" as const, text: `Task #${params.id} not found` }] };
					refresh();
					return { content: [{ type: "text" as const, text: `Removed task #${params.id}: ${task.text}` }] };
				}
				case "list": {
					if (tilldoneState.tasks.length === 0) return { content: [{ type: "text" as const, text: "No tasks defined yet." }] };
					const header = tilldoneState.title ? `${tilldoneState.title}:` : "Tasks:";
					const taskLines = tilldoneState.tasks
						.map(t => `${STATUS_ICON[t.status]} #${t.id} (${t.status}): ${t.text}${t.team ? ` [${t.team}]` : ""}`)
						.join("\n");
					refresh();
					return { content: [{ type: "text" as const, text: `${header}\n${taskLines}` }] };
				}
				case "clear": {
					const count = tilldoneState.tasks.length;
					clearState(tilldoneState);
					refresh();
					return { content: [{ type: "text" as const, text: `Cleared ${count} task(s)` }] };
				}
				default:
					return { content: [{ type: "text" as const, text: `Unknown action: ${params.action}` }] };
			}
		},

		// Invisible — our chatView shows everything
		renderCall() { return new Text("", 0, 0); },
		renderResult() { return new Text("", 0, 0); },
	});

	// ── Delegate tool ───────────────────────────────────────────

	pi.registerTool({
		name: "delegate",
		label: "Delegate",
		description: "Delegate a question to a team. Route to the ONE team whose domain best matches.",
		promptSnippet: "Delegate to a team. Returns the team's synthesized position.",
		promptGuidelines: [
			"ALWAYS route to the single best team.",
			"Planning = what to build. Engineering = how to build it. Validation = does it work.",
			"Call delegate sequentially if you need multiple teams.",
		],
		parameters: Type.Object({
			teams: Type.Union([Type.String(), Type.Array(Type.String())], { description: 'Team name or "all"' }),
			question: Type.String({ description: "Your question" }),
		}),

		async execute(_id, params, signal) {
			const { question } = params;
			let targetTeams: TeamConfig[] = [];
			if (params.teams === "all") targetTeams = [...teams];
			else if (typeof params.teams === "string") {
				const f = teams.find(t => t.name.toLowerCase() === params.teams.toString().toLowerCase());
				if (!f) throw new Error(`Team "${params.teams}" not found`);
				targetTeams = [f];
			} else if (Array.isArray(params.teams)) {
				for (const tn of params.teams) {
					const f = teams.find(t => t.name.toLowerCase() === tn.toLowerCase());
					if (!f) throw new Error(`Team "${tn}" not found`);
					targetTeams.push(f);
				}
			}

			const teamNames = targetTeams.map(t => t.name).join(", ");
			appendToLog(logPath, { from: "Orchestrator", to: teamNames, message: question, timestamp: new Date().toISOString(), type: "delegate" });
			refresh();

			const transcript = formatTranscript(readLog(logPath));

			const results = await Promise.allSettled(targetTeams.map(async (team) => {
				activeTeams.add(team.name); refresh();

				// ── Lead bubble ──────────────────────────────────
				const leadId = addMsg(team.lead.name, team.lead.color, "", "lead", "thinking", team.name);
				refresh();

				// ── Build lead env: inject member configs + log path
				// so lead-delegate.ts can spawn members on the lead's behalf.
				const leadMembersRef = team.members.map(m => ({
					name: m.name,
					model: m.model,
					systemPrompt: m.systemPrompt,
					filePath: m.filePath,
					color: m.color,
					domain: m.domain,
					expertise: m.expertise,
					consultWhen: m.consultWhen,
					sessionFile: m.sessionFile,
				}));
				const leadEnv: Record<string, string> = {
					...subprocessEnv,
					LEAD_MEMBERS_JSON: JSON.stringify(leadMembersRef),
					LEAD_LOG_PATH: logPath,
					TILLDONE_TASKS: JSON.stringify(tilldoneState),
					TILLDONE_TEAM_NAME: team.name,
					TILLDONE_TEAM_COLOR: team.color,
				};

				// ── Per-member bubble tracking ───────────────────
				// callId → { bubbleId, memberName, rawLen (subprocess text length for delta tracking) }
				const memberBubbles = new Map<string, { mId: number; memberName: string; rawLen: number }>();

				// Mirror the orchToolCalled pattern exactly:
				// seal the active bubble on delegate call, open a NEW bubble at the
				// bottom when the very next text delta arrives.
				let leadToolCalled = false;
				let leadText = "";
				let leadRawLen = 0; // tracks subprocess accumulated text length (without our injected emojis)
				let leadBubbleId = leadId;

				let lr: Awaited<ReturnType<typeof callAgent>>;
				try {
				lr = await callAgent(
					team.lead,
					`## Context\n\n${transcript}\n\n---\n\n## Question\n\n${question}`,
					leadEnv,
					projectRoot!,
					signal,

					// ── onText: delta-append to preserve injected emojis
					(acc) => {
						if (leadToolCalled) {
							// First delta after a delegate call → open fresh bubble at bottom
							// Only take the NEW text (delta since last known position), not the full accumulated history
							const delta = acc.slice(leadRawLen);
							leadRawLen = acc.length;
							// Skip empty/whitespace deltas — don't create a hollow bubble between consecutive delegates
							if (!delta.trim()) return;
							leadText = delta;
							leadBubbleId = addMsg(team.lead.name, team.lead.color, delta, "lead", "streaming", team.name);
							leadToolCalled = false;
						} else {
							// Append only the NEW text (delta), preserving emojis we injected
							const delta = acc.slice(leadRawLen);
							leadRawLen = acc.length;
							leadText += delta;
							updateMsg(leadBubbleId, { text: leadText, state: "streaming" });
						}
						refresh();
					},

					// ── onToolCall: delegate(@Member) or other tool
					(tu) => {
						if (tu.name === "delegate" && tu.args?.member) {
							const memberName: string = tu.args.member;

							// Seal the current lead bubble
							updateMsg(leadBubbleId, { state: "done" });

							// @mention bubble — code-generated, same as orchestrator
							const preview = (tu.args.question || "").length > 100
								? tu.args.question.slice(0, 100) + "..."
								: (tu.args.question || "");
							addMsg(team.lead.name, team.lead.color, `@${memberName} ${preview}`, "lead", "done", team.name);

							// Member thinking bubble — appended to bottom
							const memberConf = team.members.find(
								m => m.name.toLowerCase() === memberName.toLowerCase(),
							);
							if (memberConf) {
								const mId = addMsg(memberConf.name, memberConf.color, "", "member", "thinking", team.name);
								if (tu.callId) memberBubbles.set(tu.callId, { mId, memberName, rawLen: 0 });
							}

							// Flag: next text delta opens a new lead bubble at bottom
							leadToolCalled = true;

						} else {
							// Non-delegate tool — badge + inject emoji at current text position
							const emoji = tu.blocked ? "❌" : toolEmoji(tu.name);
							const m = msgs.find(x => x.id === leadBubbleId);
							if (m) { m.tools = m.tools || []; m.tools.push(emoji); }
							if (leadText.trim()) {
								leadText += `${emoji} `;
								updateMsg(leadBubbleId, { text: leadText, state: "streaming" });
							}
						}
						refresh();
					},

					// ── onToolUpdate: tilldone mutations + member streaming + tool badges
					(toolCallId, toolName, partialResult) => {
						// TillDone mutations from lead
						if (toolName === "tilldone" && partialResult?.type === "tilldone-mutation") {
							applyMutation(tilldoneState, partialResult as TillDoneMutation);
							refresh();
							return;
						}
						if (toolName !== "delegate") return;

						// Member stats — keyed by name, no bubble reference needed
						// Decoupled from memberBubbles lookup so stats are captured even
						// when toolCallId doesn't match between tool_execution_start/update
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

						const entry = memberBubbles.get(toolCallId);
						if (!entry) return;
						if (partialResult?.type === "streaming" && partialResult.text) {
							// Delta-append to preserve injected emojis
							const bubble = msgs.find(x => x.id === entry.mId);
							if (bubble) {
								const delta = partialResult.text.slice(entry.rawLen);
								entry.rawLen = partialResult.text.length;
								bubble.text += delta;
								updateMsg(entry.mId, { text: bubble.text, state: "streaming" });
							}
							refresh();
						} else if (partialResult?.type === "tool") {
							// Member tool call — inject emoji at current text position
							const emoji = partialResult.blocked ? "❌" : toolEmoji(partialResult.toolName);
							const bubble = msgs.find(x => x.id === entry.mId);
							if (bubble) {
								bubble.tools = bubble.tools || [];
								bubble.tools.push(emoji);
								if (bubble.text.trim()) {
									bubble.text += `${emoji} `;
								}
								refresh();
							}
						}
					},

					// ── onToolEnd: member finished — mark done
					// Fallback if streaming updates never arrived
					(toolCallId, toolName, result) => {
						if (toolName !== "delegate") return;

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

						const entry = memberBubbles.get(toolCallId);
						if (!entry) return;
						const bubble = msgs.find(x => x.id === entry.mId);
						if (!bubble) return;
						if (!bubble.text && result?.content?.[0]?.text) {
							updateMsg(entry.mId, { text: result.content[0].text, state: "done" });
						} else {
							updateMsg(entry.mId, { state: "done" });
						}
						refresh();
					},

					// ── onUsage: incremental lead cost/context updates
					(stats) => {
						addStats(team.lead.name, 0, 0, 0, 0); // ensure entry exists
						const s = getStats(team.lead.name);
						s.cost = stats.cost;
						s.tokensIn = stats.tokensIn;
						s.tokensOut = stats.tokensOut;
						s.contextTokens = stats.contextTokens;
						refresh();
					},
				);

				} catch (err: any) {
					const errMsg = `❌ ${team.lead.name} error: ${err.message || String(err)}`;
					updateMsg(leadBubbleId, { text: errMsg, state: "done" });
					appendToLog(logPath, { from: team.lead.name, message: errMsg, timestamp: new Date().toISOString(), type: "lead", team: team.name });
					activeTeams.delete(team.name); refresh();
					return { team: team.name, lead: team.lead.name, synthesis: errMsg };
				}

				// ── Finalize ─────────────────────────────────────
				updateMsg(leadBubbleId, { text: leadText, state: "done" });
				for (const { mId } of memberBubbles.values()) {
					const b = msgs.find(x => x.id === mId);
					if (b && b.state !== "done") updateMsg(mId, { state: "done" });
				}

				appendToLog(logPath, {
					from: team.lead.name,
					message: lr.response,
					timestamp: new Date().toISOString(),
					type: "lead",
					team: team.name,
					cost: lr.cost,
					tokens_in: lr.tokensIn,
					tokens_out: lr.tokensOut,
				});
				refresh();

				activeTeams.delete(team.name); refresh();
				return { team: team.name, lead: team.lead.name, synthesis: lr.response };
			}));

			const syntheses: { team: string; lead: string; synthesis: string }[] = [];
			for (let i = 0; i < results.length; i++) {
				const r = results[i];
				if (r.status === "fulfilled") {
					syntheses.push(r.value);
				} else {
					const team = targetTeams[i];
					const errMsg = `❌ ${team.lead.name} failed: ${r.reason?.message || String(r.reason)}`;
					syntheses.push({ team: team.name, lead: team.lead.name, synthesis: errMsg });
				}
			}
			let text = "";
			for (const s of syntheses) text += `\n\n## ${s.team} Team (${s.lead})\n${s.synthesis}`;
			return { content: [{ type: "text", text: text.trim() }] };
		},

		// Invisible — our chatView shows everything
		renderCall() { return new Text("", 0, 0); },
		renderResult() { return new Text("", 0, 0); },
	});
}

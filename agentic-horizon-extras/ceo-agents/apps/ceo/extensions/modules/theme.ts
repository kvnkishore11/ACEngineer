// ── Theme Helpers ────────────────────────────────────────────────
// ANSI color helpers, TUI gauge rendering, board status rendering.

import { truncateToWidth, visibleWidth } from "@mariozechner/pi-tui";
import type { BoardMemberConfig, MemberStats } from "./types";

// ── ANSI Color Functions (synthwave palette) ─────────────────────

export function bgWarm(s: string): string {
	return `\x1b[48;2;74;30;106m${s}\x1b[49m`;
}

export function cyan(s: string): string {
	return `\x1b[38;2;54;249;246m${s}\x1b[39m`;
}

export function pink(s: string): string {
	return `\x1b[38;2;255;126;219m${s}\x1b[39m`;
}

export function yellow(s: string): string {
	return `\x1b[38;2;254;222;93m${s}\x1b[39m`;
}

export function green(s: string): string {
	return `\x1b[38;2;114;241;184m${s}\x1b[39m`;
}

export function dim(s: string): string {
	return `\x1b[38;2;187;187;187m${s}\x1b[39m`;
}

export function bold(s: string): string {
	return `\x1b[1m${s}\x1b[22m`;
}

// ── Utility Functions ────────────────────────────────────────────

export function parseHexColor(hex: string): { r: number; g: number; b: number } {
	const clean = hex.replace(/^#/, "");
	return {
		r: parseInt(clean.substring(0, 2), 16) || 0,
		g: parseInt(clean.substring(2, 4), 16) || 0,
		b: parseInt(clean.substring(4, 6), 16) || 0,
	};
}

export function formatTokenCount(count: number): string {
	if (count < 1000) return `${count}`;
	if (count < 1000000) return `${Math.round(count / 1000)}k`;
	return `${(count / 1000000).toFixed(1)}M`;
}

// ── Rendering Functions ──────────────────────────────────────────

/**
 * Render a single constraint gauge line with a progress bar.
 *
 * The bar fills from left to right. A thin `|` marks the min threshold.
 * Fill color shifts through zones:
 *   cyan  -> below min (warming up)
 *   green -> min-80% max (healthy)
 *   yellow -> 80%+ of max (approaching limit)
 *   pink  -> at/past max (done)
 */
export function renderGaugeLine(
	label: string,
	current: number,
	minVal: number,
	maxVal: number,
	barWidth: number,
	valueStr: string,
	rangeStr: string,
	totalWidth: number,
): string {
	const pct = maxVal > 0 ? Math.min(current / maxVal, 1) : 0;
	const filledCount = Math.round(pct * barWidth);
	const minPos = maxVal > 0 ? Math.round((minVal / maxVal) * barWidth) : 0;

	// Pick fill color based on zone
	let fillFn: (s: string) => string;
	if (current >= maxVal) fillFn = pink;
	else if (current >= maxVal * 0.8) fillFn = yellow;
	else if (current >= minVal) fillFn = green;
	else fillFn = cyan;

	// Build bar with min-threshold marker
	let bar = "";
	for (let i = 0; i < barWidth; i++) {
		if (i === minPos && minVal > 0 && minVal < maxVal) {
			bar += i < filledCount ? fillFn("\u2503") : dim("\u2503");
		} else if (i < filledCount) {
			bar += fillFn("\u2588");
		} else {
			bar += dim("\u2591");
		}
	}

	const content =
		"  " +
		pink(label.padEnd(8)) +
		" " +
		bar +
		"  " +
		cyan(valueStr.padEnd(12)) +
		dim(rangeStr);

	return bgWarm(
		truncateToWidth(content + " ".repeat(totalWidth), totalWidth, ""),
	);
}

/**
 * Render board member status cards for the footer.
 * Accepts explicit parameters instead of relying on closure variables.
 */
export function renderBoardStatusLines(
	width: number,
	activeMembers: BoardMemberConfig[],
	memberStats: Map<string, MemberStats>,
	respondingMembers: Set<string>,
): string[] {
	if (activeMembers.length === 0) return [];

	const lines: string[] = [];
	const members = activeMembers;
	const cols = Math.min(2, members.length);
	const gap = 2;
	const totalGaps = cols - 1;
	const colWidth = Math.floor((width - totalGaps * gap) / cols);

	// Member rows (2 per row for more space)
	for (let row = 0; row < Math.ceil(members.length / cols); row++) {
		const cells: string[] = [];
		for (let col = 0; col < cols; col++) {
			const idx = row * cols + col;
			if (idx >= members.length) break;
			const m = members[idx];
			const stats = memberStats.get(m.name) || {
				chats: 0,
				cost: 0,
				tokensUsed: 0,
				contextWindow: 256000,
			};
			const { r, g, b } = parseHexColor(m.color);
			const isResponding = respondingMembers.has(m.name);

			const bgOpen = `\x1b[48;2;${r};${g};${b}m`;
			const fgDark = `\x1b[38;2;30;30;30m`;
			const reset = `\x1b[0m`;

			const icon = isResponding ? " \u{1F4AC} " : " \u{2705} ";
			const nameStr = m.name.length > colWidth - 10 ? m.name.slice(0, colWidth - 10) : m.name;
			const remaining = stats.contextWindow - stats.tokensUsed;
			const remainingStr = formatTokenCount(Math.max(0, remaining));
			const infoStr = `\u{1F4E8}${stats.chats} \u{1F4B0}$${stats.cost.toFixed(2)} \u{1F9E0}${remainingStr}`;

			const cellContent = `${icon}${nameStr} `;
			const infoPart = `${infoStr} `;
			const innerLen = visibleWidth(cellContent) + visibleWidth(infoPart);
			const padLen = Math.max(1, colWidth - innerLen);
			const cellStr = cellContent + " ".repeat(padLen) + infoPart;
			const truncated = truncateToWidth(cellStr, colWidth, "");
			const finalPad = " ".repeat(Math.max(0, colWidth - visibleWidth(truncated)));

			cells.push(`${bgOpen}${fgDark}${truncated}${finalPad}${reset}`);
		}
		lines.push(cells.join(" ".repeat(gap)));
	}

	return lines;
}

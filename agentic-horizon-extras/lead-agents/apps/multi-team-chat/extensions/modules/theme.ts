// ── Theme Helpers ────────────────────────────────────────────────

import { truncateToWidth, visibleWidth, wrapTextWithAnsi } from "@mariozechner/pi-tui";

export function parseHexColor(hex: string): { r: number; g: number; b: number } {
	const clean = hex.replace(/^#/, "");
	return {
		r: parseInt(clean.substring(0, 2), 16) || 0,
		g: parseInt(clean.substring(2, 4), 16) || 0,
		b: parseInt(clean.substring(4, 6), 16) || 0,
	};
}

export function hexFg(hex: string, text: string): string {
	const { r, g, b } = parseHexColor(hex);
	return `\x1b[38;2;${r};${g};${b}m${text}\x1b[39m`;
}

export function nameTag(name: string, color: string): string {
	const { r, g, b } = parseHexColor(color);
	return `\x1b[48;2;${r};${g};${b}m\x1b[38;2;30;30;30m ${name} \x1b[0m`;
}

export function dim(s: string): string {
	return `\x1b[38;2;120;120;120m${s}\x1b[39m`;
}

export function bold(s: string): string {
	return `\x1b[1m${s}\x1b[22m`;
}

export { truncateToWidth, visibleWidth, wrapTextWithAnsi };

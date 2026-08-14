// ── Domain Restriction Helpers ───────────────────────────────────

import { join } from "node:path";
import type { DomainRule } from "./types";

/**
 * Build a domain restrictions block for injection into system prompts.
 * Returns markdown describing what files/dirs the agent can access.
 */
export function buildDomainBlock(domain: DomainRule[], projectRoot: string): string {
	if (!domain || domain.length === 0) return "_No domain restrictions — full codebase access._";

	const lines: string[] = [
		"**You are restricted to the following areas of the codebase.** Do NOT access files outside these paths.\n",
	];

	for (const rule of domain) {
		const perms: string[] = [];
		if (rule.read) perms.push("read");
		if (rule.upsert) perms.push("write/edit");
		if (rule.delete) perms.push("delete");
		const permStr = perms.length > 0 ? perms.join(", ") : "no access";
		const absPath = rule.path === "." ? projectRoot : join(projectRoot, rule.path);
		lines.push(`- \`${absPath}\` — ${permStr}`);
	}

	lines.push("\nIf a file is not under one of these paths, do not read, write, or reference it.");

	return lines.join("\n");
}

/**
 * Check if a file path is allowed under domain rules for a given operation.
 * Handles both absolute and relative paths, including the root "." rule.
 */
export function isDomainAllowed(
	filePath: string,
	operation: "read" | "upsert" | "delete",
	domain: DomainRule[],
	projectRoot?: string,
): boolean {
	if (!domain || domain.length === 0) return true; // No restrictions

	// Normalize to relative path
	let rel = filePath;
	if (projectRoot && rel.startsWith(projectRoot)) {
		rel = rel.slice(projectRoot.length).replace(/^\//, "");
	}
	if (rel.startsWith("./")) rel = rel.slice(2);

	for (const rule of domain) {
		// Root rule matches everything
		if (rule.path === ".") return rule[operation] === true;
		const rulePath = rule.path.replace(/\/$/, "");
		if (rel === rulePath || rel.startsWith(rulePath + "/") || rel.startsWith(rule.path)) {
			return rule[operation] === true;
		}
	}
	return false; // Not in any allowed domain
}

// ── Bash Heuristics ─────────────────────────────────────────────

/** Patterns that indicate a bash command performs write/create operations */
export const BASH_WRITE_PATTERNS = [
	/>(?!&)/,                                              // Output redirect (> or >>) but not 2>&1
	/\btee\b/, /\bmv\b/, /\bcp\b/, /\bmkdir\b/, /\btouch\b/,
	/\bchmod\b/, /\bchown\b/,
	/\bnpm\s+install/, /\bbun\s+(install|add)/,
	/\bgit\s+(commit|push|merge|rebase|reset|checkout\s+-)/,
	/\bsed\s+-i/, /\bpatch\b/,
	/\bdd\b.*\bof=/, /\bcurl\b.*\s-o\s/i, /\bwget\b.*\s-O\s/,
];

/** Patterns that indicate a bash command performs delete operations */
export const BASH_DELETE_PATTERNS = [
	/\brm\s/, /\brmdir\b/, /\bunlink\b/, /\bgit\s+clean/,
];

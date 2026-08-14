// ── Config Parsing ───────────────────────────────────────────────
// YAML config parsing, project root discovery, board member loading.

import { existsSync, readFileSync, mkdirSync } from "node:fs";
import { join, dirname, basename, parse } from "node:path";
import { createRequire } from "node:module";
import { parseFrontmatter } from "@mariozechner/pi-coding-agent";
import type { CeoConfig, BoardMember, BoardMemberConfig, BriefSection, MeetingConstraints } from "./types";

export function findProjectRoot(cwd: string): string | null {
	let dir = cwd;
	const { root } = parse(dir);
	while (dir !== root) {
		const candidate = join(dir, ".pi", "ceo-agents", "ceo-and-board-configuration.yaml");
		if (existsSync(candidate)) return dir;
		dir = dirname(dir);
	}
	return null;
}

export function findConfigPath(cwd: string): string | null {
	let dir = cwd;
	const { root } = parse(dir);
	while (dir !== root) {
		const candidate = join(dir, ".pi", "ceo-agents", "ceo-and-board-configuration.yaml");
		if (existsSync(candidate)) return candidate;
		dir = dirname(dir);
	}
	return null;
}

export function parseConfig(cwd: string): CeoConfig | null {
	const configPath = findConfigPath(cwd);
	if (!configPath) return null;

	try {
		const raw = readFileSync(configPath, "utf-8");
		const config: CeoConfig = {
			meeting: {
				constraints: {
					min_time_minutes: 5,
					max_time_minutes: 10,
					min_budget: "$2",
					max_budget: "$10",
				},
				editor: "code",
			},
			paths: {
				briefs: ".pi/ceo-agents/briefs/",
				deliberations: ".pi/ceo-agents/deliberations/",
				memos: ".pi/ceo-agents/memos/",
				agents: ".pi/ceo-agents/agents/",
			},
			brief_sections: [
				{ section: "## Situation", description: "What is happening right now? State the facts." },
				{ section: "## Stakes", description: "What's at risk? Upside and downside." },
				{ section: "## Constraints", description: "Budget, timeline, team, technical, regulatory boundaries." },
				{ section: "## Key Question", description: "The single most important question for the board." },
			],
			board: [],
		};

		// Simple line-by-line extraction for constraints and editor
		for (const line of raw.split("\n")) {
			const kv = line.match(
				/^\s+(min_time_minutes|max_time_minutes|min_budget|max_budget|editor):\s*['"]?([^'"#]+)['"]?/,
			);
			if (kv) {
				const key = kv[1].trim();
				const val = kv[2].trim();
				if (key === "editor") {
					config.meeting.editor = val;
				} else if (key === "min_time_minutes" || key === "max_time_minutes") {
					(config.meeting.constraints as any)[key] = parseInt(val, 10);
				} else {
					(config.meeting.constraints as any)[key] = val;
				}
			}
		}

		// Parse paths
		let inPaths = false;
		for (const line of raw.split("\n")) {
			if (line.match(/^paths:/)) {
				inPaths = true;
				continue;
			}
			if (inPaths && line.match(/^\S/) && !line.match(/^\s/)) {
				inPaths = false;
				continue;
			}
			if (!inPaths) continue;
			const pathMatch = line.match(/^\s+(briefs|deliberations|memos|agents):\s*(.+)/);
			if (pathMatch) {
				(config.paths as any)[pathMatch[1].trim()] = pathMatch[2].trim();
			}
		}

		// Parse board members (with name, path, color)
		let inBoard = false;
		let currentMember: Partial<BoardMember> = {};
		for (const line of raw.split("\n")) {
			if (line.match(/^board:/)) {
				inBoard = true;
				continue;
			}
			if (inBoard && line.match(/^\S/) && !line.match(/^\s/)) {
				inBoard = false;
				continue;
			}
			if (!inBoard) continue;
			if (line.trim().startsWith("#")) continue;

			const nameMatch = line.match(/^\s+-\s+name:\s*(.+)/);
			const pathMatch = line.match(/^\s+path:\s*(.+)/);
			const colorMatch = line.match(/^\s+color:\s*["']?([^"'#\s]+(?:#[^"'\s]*)?)["']?/);
			// Better color match for hex values
			const colorMatch2 = line.match(/^\s+color:\s*["']?(#[0-9a-fA-F]{6})["']?/);

			if (nameMatch) {
				if (currentMember.name && currentMember.path) {
					config.board.push(currentMember as BoardMember);
				}
				currentMember = { name: nameMatch[1].trim(), color: "#ffffff" };
			}
			if (pathMatch) {
				currentMember.path = pathMatch[1].trim();
			}
			if (colorMatch2) {
				currentMember.color = colorMatch2[1].trim();
			} else if (colorMatch) {
				currentMember.color = colorMatch[1].trim();
			}
		}
		if (currentMember.name && currentMember.path) {
			config.board.push(currentMember as BoardMember);
		}

		// Parse brief_sections (section + description pairs)
		let inBriefSections = false;
		let currentSection: Partial<BriefSection> = {};
		const parsedSections: BriefSection[] = [];
		for (const line of raw.split("\n")) {
			if (line.match(/^brief_sections:/)) {
				inBriefSections = true;
				continue;
			}
			if (inBriefSections && line.match(/^\S/) && !line.match(/^\s/)) {
				inBriefSections = false;
				continue;
			}
			if (!inBriefSections) continue;
			if (line.trim().startsWith("#")) continue;

			const sectionMatch = line.match(/^\s+-\s+section:\s*["']?(.+?)["']?\s*$/);
			const descMatch = line.match(/^\s+description:\s*["']?(.+?)["']?\s*$/);

			if (sectionMatch) {
				if (currentSection.section && currentSection.description) {
					parsedSections.push(currentSection as BriefSection);
				}
				currentSection = { section: sectionMatch[1].trim() };
			}
			if (descMatch) {
				currentSection.description = descMatch[1].trim();
			}
		}
		if (currentSection.section && currentSection.description) {
			parsedSections.push(currentSection as BriefSection);
		}
		if (parsedSections.length > 0) {
			config.brief_sections = parsedSections;
		}

		return config;
	} catch {
		return null;
	}
}

// ── Helper functions ─────────────────────────────────────────────

/**
 * Load .env from project root into process.env via dotenv.
 * Uses createRequire scoped to apps/ceo/ so node_modules resolves
 * from the extension's package.json, not the project root.
 * Returns the merged env for subprocess spawning.
 */
export function loadDotEnv(projectRoot: string): Record<string, string> {
	const envPath = join(projectRoot, ".env");
	if (!existsSync(envPath)) {
		throw new Error(
			`FATAL: .env file not found at ${envPath}\n` +
			`CEO & Board requires a .env file with ANTHROPIC_API_KEY in the project root.`,
		);
	}
	const appRequire = createRequire(join(projectRoot, "apps/ceo/package.json"));
	const dotenv = appRequire("dotenv");
	dotenv.config({ path: envPath, quiet: true });
	return { ...process.env } as Record<string, string>;
}

/**
 * Build the {{EXPERTISE_BLOCK}} content from frontmatter expertise.
 * Provides full path and access mode (read-only or read/write).
 * The agent reads/writes these files directly during deliberation.
 */
export function buildExpertiseBlock(
	expertise: Array<{ path: string; "use-when": string; updatable: boolean }>,
	projectRoot: string,
): string {
	if (!expertise || expertise.length === 0) return "_No expertise files configured._";

	const lines: string[] = [];
	for (const entry of expertise) {
		const fullPath = join(projectRoot, entry.path);
		const mode = entry.updatable ? "read/write" : "read-only";
		lines.push(
			`- **${basename(entry.path)}** [${mode}] — \`${fullPath}\`\n` +
			`  Use when: ${entry["use-when"]}`,
		);
	}
	return lines.join("\n");
}

/**
 * Build the {{SKILLS_BLOCK}} content from frontmatter skills.
 * Does NOT load skill file content — just provides the path and use-when.
 * The agent reads the skill file themselves when the time is right.
 */
export function buildSkillsBlock(
	skills: Array<{ path: string; "use-when": string }>,
	projectRoot: string,
): string {
	if (!skills || skills.length === 0) return "_No skills configured._";

	const lines: string[] = [];
	for (const skill of skills) {
		const skillPath = join(projectRoot, skill.path);
		lines.push(
			`- **${basename(skill.path, ".md")}** — read \`${skillPath}\`\n` +
			`  Use when: ${skill["use-when"]}`,
		);
	}
	return lines.join("\n");
}

export function loadBoardMembers(
	projectRoot: string,
	board: BoardMember[],
	sessionDir: string,
): BoardMemberConfig[] {
	const members: BoardMemberConfig[] = [];
	if (!existsSync(sessionDir)) {
		mkdirSync(sessionDir, { recursive: true });
	}

	for (const entry of board) {
		const filePath = join(projectRoot, entry.path);
		if (!existsSync(filePath)) continue;

		let content: string;
		try {
			content = readFileSync(filePath, "utf-8");
		} catch {
			continue;
		}

		const { frontmatter, body } = parseFrontmatter<Record<string, any>>(content);
		const model = (frontmatter.model as string) || "anthropic/claude-sonnet-4-6";
		const kebabName = entry.name.toLowerCase().replace(/\s+/g, "-");
		const sessionFile = join(sessionDir, `${kebabName}.jsonl`);

		// Build expertise + skills blocks and replace template variables
		const expertiseBlock = buildExpertiseBlock(frontmatter.expertise || [], projectRoot);
		const skillsBlock = buildSkillsBlock(frontmatter.skills || [], projectRoot);
		const resolvedBody = body.trim()
			.replace(/\{\{EXPERTISE_BLOCK\}\}/g, expertiseBlock)
			.replace(/\{\{SKILLS_BLOCK\}\}/g, skillsBlock);

		members.push({
			name: entry.name,
			model,
			systemPrompt: resolvedBody,
			filePath,
			color: entry.color || "#ffffff",
			sessionFile,
		});
	}

	return members;
}

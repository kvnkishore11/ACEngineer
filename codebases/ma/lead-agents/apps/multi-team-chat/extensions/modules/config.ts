// ── Config Parsing ───────────────────────────────────────────────

import { existsSync, readFileSync, mkdirSync } from "node:fs";
import { join, dirname, parse, isAbsolute } from "node:path";
import { createRequire } from "node:module";
import { parseFrontmatter } from "@mariozechner/pi-coding-agent";
import type { MultiTeamConfig, AgentRef, AgentConfig, TeamConfig, OrchestratorConfig, DomainRule, ResolvedExpertise } from "./types";
import { buildDomainBlock } from "./domain";

/**
 * Walk up from cwd to find the project root.
 * When a custom config file is provided via --team, we look for ancestors that
 * have both a .pi/ directory AND the config file resolves from that root.
 * Otherwise we look for the default multi-team-config.yaml location.
 */
export function findProjectRoot(cwd: string, customConfig?: string): string | null {
	let dir = cwd;
	const { root } = parse(dir);
	while (dir !== root) {
		if (customConfig) {
			// Custom config: require both .pi/ dir AND the config file to resolve from here
			if (existsSync(join(dir, ".pi"))) {
				const candidatePath = isAbsolute(customConfig) ? customConfig : join(dir, customConfig);
				if (existsSync(candidatePath)) return dir;
			}
		} else {
			// Default: look for the canonical config location
			if (existsSync(join(dir, ".pi", "multi-team", "multi-team-config.yaml"))) return dir;
		}
		dir = dirname(dir);
	}
	return null;
}

/**
 * Minimal YAML parser for our config format.
 * Handles nested structures: orchestrator, teams[].lead, teams[].members[]
 *
 * Domain rules are NOT parsed here — they live in agent frontmatter.
 *
 * @param projectRoot  Absolute project root (used to resolve all relative paths)
 * @param configPath   Optional explicit config file path. Defaults to the canonical
 *                     .pi/multi-team/multi-team-config.yaml location.
 */
export function parseConfig(projectRoot: string, configPath?: string): MultiTeamConfig | null {
	const resolvedConfigPath = configPath ?? join(projectRoot, ".pi", "multi-team", "multi-team-config.yaml");
	if (!existsSync(resolvedConfigPath)) return null;

	const raw = readFileSync(resolvedConfigPath, "utf-8");
	const config: MultiTeamConfig = {
		orchestrator: { name: "Orchestrator", path: "", color: "#72f1b8" },
		teams: [],
		paths: { agents: "", sessions: ".pi/multi-team/sessions/" },
		sharedContext: [],
	};

	// Parse orchestrator
	let inOrch = false;
	for (const line of raw.split("\n")) {
		if (line.match(/^orchestrator:/)) { inOrch = true; continue; }
		if (inOrch && line.match(/^\S/) && !line.match(/^\s/)) { inOrch = false; continue; }
		if (!inOrch) continue;

		const nm = line.match(/^\s+name:\s*(.+)/);
		const pm = line.match(/^\s+path:\s*(.+)/);
		const cm = line.match(/^\s+color:\s*["']?(#[0-9a-fA-F]{6})["']?/);
		if (nm) config.orchestrator.name = nm[1].trim();
		if (pm) config.orchestrator.path = pm[1].trim();
		if (cm) config.orchestrator.color = cm[1].trim();
	}

	// Parse paths
	let inPaths = false;
	for (const line of raw.split("\n")) {
		if (line.match(/^paths:/)) { inPaths = true; continue; }
		if (inPaths && line.match(/^\S/) && !line.match(/^\s/)) { inPaths = false; continue; }
		if (!inPaths) continue;
		const m = line.match(/^\s+(agents|sessions):\s*(.+)/);
		if (m) (config.paths as any)[m[1].trim()] = m[2].trim();
	}

	// Parse shared_context
	let inShared = false;
	for (const line of raw.split("\n")) {
		if (line.match(/^shared_context:/)) { inShared = true; continue; }
		if (inShared && line.match(/^\S/) && !line.match(/^\s/)) { inShared = false; continue; }
		if (!inShared) continue;
		const m = line.match(/^\s+-\s+(.+)/);
		if (m) config.sharedContext.push(m[1].trim());
	}

	// Parse teams — use a block-based approach
	const teamBlocks = raw.split(/\n\s+-\s+team-name:\s*/);
	for (let i = 1; i < teamBlocks.length; i++) {
		const block = teamBlocks[i];
		const teamNameMatch = block.match(/^(.+)/);
		const teamColorMatch = block.match(/team-color:\s*["']?(#[0-9a-fA-F]{6})["']?/);
		if (!teamNameMatch) continue;

		const consultWhenMatch = block.match(/^\s{4}consult-when:\s*(.+)/m);

		const team: MultiTeamConfig["teams"][0] = {
			name: teamNameMatch[1].trim(),
			color: teamColorMatch?.[1]?.trim() || "#888888",
			consultWhen: consultWhenMatch?.[1]?.trim() || "",
			lead: { name: "", path: "", color: "" },
			members: [],
		};

		// Parse lead
		const leadSection = block.match(/lead:\s*\n([\s\S]*?)(?=\n\s{4}members:|\n\s+-\s+team-name:|\n\w|$)/);
		if (leadSection) {
			const ls = leadSection[1];
			const lnm = ls.match(/name:\s*(.+)/); if (lnm) team.lead.name = lnm[1].trim();
			const lpm = ls.match(/path:\s*(.+)/); if (lpm) team.lead.path = lpm[1].trim();
			const lcm = ls.match(/color:\s*["']?(#[0-9a-fA-F]{6})["']?/); if (lcm) team.lead.color = lcm[1].trim();
			const lmm = ls.match(/model:\s*(.+)/); if (lmm) team.lead.model = lmm[1].trim();
		}

		// Parse members
		const membersSection = block.match(/members:\s*\n([\s\S]*?)(?=\n\s+-\s+team-name:|\n\w|$)/);
		if (membersSection) {
			// Prepend \n so the first member's "- name:" is found by the same \n-prefixed split pattern
			const memberBlocks = ("\n" + membersSection[1]).split(/\n\s{6}-\s+name:\s*/);
			for (let j = 1; j < memberBlocks.length; j++) {
				const mb = memberBlocks[j];
				const mnm = mb.match(/^(.+)/);
				const mpm = mb.match(/path:\s*(.+)/);
				const mcm = mb.match(/color:\s*["']?(#[0-9a-fA-F]{6})["']?/);
				const cwm = mb.match(/consult-when:\s*(.+)/);
				const mmm = mb.match(/model:\s*(.+)/);
				if (mnm && mpm) {
					const member: AgentRef = {
						name: mnm[1].trim(),
						path: mpm[1].trim(),
						color: mcm?.[1]?.trim() || "#ffffff",
						consultWhen: cwm?.[1]?.trim() || "",
						model: mmm?.[1]?.trim(),
					};
					team.members.push(member);
				}
			}
		}

		config.teams.push(team);
	}

	return config;
}

// ── Frontmatter Loaders ─────────────────────────────────────────

/**
 * Parse domain rules from agent frontmatter.
 * Expects `domain:` array with { path, read, upsert, delete } entries.
 */
function parseFrontmatterDomain(frontmatter: Record<string, any>): DomainRule[] {
	const domain = frontmatter.domain as { path: string; read?: boolean; upsert?: boolean; delete?: boolean }[] | undefined;
	if (!domain || !Array.isArray(domain) || domain.length === 0) return [];

	return domain.map(d => ({
		path: d.path || "",
		read: d.read ?? false,
		upsert: d.upsert ?? false,
		delete: d.delete ?? false,
	}));
}

/**
 * Parse expertise entries from frontmatter and resolve to absolute paths.
 * Returns ResolvedExpertise[] for enforcement and subprocess env injection.
 */
function parseFrontmatterExpertise(projectRoot: string, frontmatter: Record<string, any>): ResolvedExpertise[] {
	const expertise = frontmatter.expertise as { path: string; updatable?: boolean; "use-when"?: string; "max-lines"?: number }[] | undefined;
	if (!expertise || !Array.isArray(expertise) || expertise.length === 0) return [];

	return expertise.map(exp => ({
		absPath: join(projectRoot, exp.path),
		updatable: exp.updatable ?? false,
		maxLines: exp["max-lines"] ?? 10000,
	}));
}

/**
 * Build the expertise block to replace {{EXPERTISE_BLOCK}} in agent prompts.
 * Plain YAML content — sits inside the ```yaml fence already in the .md template.
 * Matches the Skills block format exactly: path + metadata, no inlined content.
 * The agent reads the file itself when it needs the content.
 */
function buildExpertiseBlock(projectRoot: string, frontmatter: Record<string, any>, agentName: string, warnings: string[]): string {
	const expertise = frontmatter.expertise as { path: string; updatable?: boolean; "use-when"?: string; "max-lines"?: number }[] | undefined;
	if (!expertise || !Array.isArray(expertise) || expertise.length === 0) return "[]";

	const lines: string[] = [];
	for (const exp of expertise) {
		const absPath = join(projectRoot, exp.path);
		const exists = existsSync(absPath);
		lines.push(`- path: ${absPath}`);
		lines.push(`  updatable: ${exp.updatable ? "yes" : "no"}`);
		if (exp["use-when"]) lines.push(`  use-when: "${exp["use-when"]}"`);
		if (!exists) {
			lines.push(`  exists: false`);
		}
	}
	return lines.join("\n");
}

/**
 * Build the {{MEMBERS_BLOCK}} content for a lead's system prompt.
 * Lists each member's name and consult-when hint, formatted as YAML — same
 * pattern as buildTeamsBlock() in prompt.ts. Resolved in loadTeams() after
 * members are loaded so the lead knows who is on its team.
 */
export function buildMembersBlock(members: AgentConfig[]): string {
	if (members.length === 0) return "_No team members configured._";

	const lines: string[] = [];
	for (const m of members) {
		lines.push(`- member-name: ${m.name}   # pass this exact value to delegate()`);
		lines.push(`  consult-when: ${m.consultWhen || "General specialist"}`);
		if (m.tools.length > 0) lines.push(`  tools: [${m.tools.join(", ")}]`);
		if (m.domain.length > 0) {
			const domainSummary = m.domain.map(d => {
				const perms = [d.read ? "read" : "", d.upsert ? "write" : "", d.delete ? "delete" : ""].filter(Boolean).join("+");
				return `${d.path} (${perms})`;
			}).join(", ");
			lines.push(`  domain: ${domainSummary}`);
		}
	}
	return lines.join("\n");
}

/**
 * Build the shared context block — files from multi-team-config.yaml shared_context.
 * Appended as a new section with a ```yaml fence, matching Skills/Expertise format.
 * The agent reads the files itself when it needs the content.
 * Pushes warnings for missing files (non-fatal).
 */
export function buildSharedContextBlock(projectRoot: string, sharedContext: string[], warnings?: string[]): string {
	if (!sharedContext || sharedContext.length === 0) return "";

	const lines: string[] = [];
	for (const relPath of sharedContext) {
		const absPath = join(projectRoot, relPath);
		if (!existsSync(absPath)) {
			warnings?.push(`Shared context file not found: ${relPath} (resolved: ${absPath})`);
			continue;
		}
		lines.push(`- path: ${absPath}`);
	}

	if (lines.length === 0) return "";
	return `\n\n## Shared Context\n\n> Read these files at the start of each task for project context.\n\n\`\`\`yaml\n${lines.join("\n")}\n\`\`\``;
}

/**
 * Build the skills block to replace {{SKILLS_BLOCK}} in agent prompts.
 * Lists absolute paths to skill files with use-when metadata.
 * Pushes warnings for missing skill files (non-fatal).
 */
function buildSkillsBlock(projectRoot: string, frontmatter: Record<string, any>, agentName: string, warnings: string[]): string {
	const skills = frontmatter.skills as { path: string; "use-when"?: string }[] | undefined;
	if (!skills || !Array.isArray(skills) || skills.length === 0) return "[]";

	const lines: string[] = [];
	for (const skill of skills) {
		const absPath = join(projectRoot, skill.path);
		const exists = existsSync(absPath);
		lines.push(`- path: ${absPath}`);
		if (skill["use-when"]) lines.push(`  use-when: "${skill["use-when"]}"`);
		if (!exists) {
			lines.push(`  exists: false`);
			warnings.push(`[${agentName}] Skill file not found: ${skill.path} (resolved: ${absPath})`);
		}
	}
	return lines.join("\n");
}

/**
 * Validate domain paths exist as directories. Non-fatal — pushes warnings.
 */
function validateDomainPaths(projectRoot: string, domain: DomainRule[], agentName: string, warnings: string[]): void {
	for (const rule of domain) {
		if (rule.path === ".") continue; // Root always exists
		const absPath = join(projectRoot, rule.path);
		if (!existsSync(absPath)) {
			warnings.push(`[${agentName}] Domain path not found: ${rule.path} (resolved: ${absPath})`);
		}
	}
}

/**
 * Replace template placeholders in an agent prompt body.
 * Handles {{EXPERTISE_BLOCK}}, {{SKILLS_BLOCK}}, and {{SESSION_DIR}}.
 *
 * When sessionDir is omitted (e.g. orchestrator at load time), {{SESSION_DIR}}
 * is left as-is for later resolution at runtime.
 */
function resolveTemplates(body: string, projectRoot: string, frontmatter: Record<string, any>, agentName: string, warnings: string[], sessionDir?: string, logPath?: string): string {
	let resolved = body;
	resolved = resolved.replace("{{EXPERTISE_BLOCK}}", buildExpertiseBlock(projectRoot, frontmatter, agentName, warnings));
	resolved = resolved.replace("{{SKILLS_BLOCK}}", buildSkillsBlock(projectRoot, frontmatter, agentName, warnings));
	if (sessionDir) resolved = resolved.replace("{{SESSION_DIR}}", sessionDir);
	if (logPath)    resolved = resolved.replace("{{CONVERSATION_LOG}}", logPath);
	return resolved;
}

// ── Agent Loaders ───────────────────────────────────────────────

/**
 * Load orchestrator config from its agent .md file.
 * THROWS if the orchestrator .md file is missing — this is fatal.
 */
export function loadOrchestrator(projectRoot: string, config: MultiTeamConfig, warnings: string[]): OrchestratorConfig {
	const filePath = join(projectRoot, config.orchestrator.path);

	if (!existsSync(filePath)) {
		throw new Error(`FATAL: Orchestrator agent file not found: ${filePath}\nCheck orchestrator.path in multi-team-config.yaml`);
	}

	const content = readFileSync(filePath, "utf-8");
	const { frontmatter, body } = parseFrontmatter<Record<string, any>>(content);
	const model = (frontmatter.model as string) || "anthropic/claude-sonnet-4-6";
	const domain = parseFrontmatterDomain(frontmatter);
	const expertise = parseFrontmatterExpertise(projectRoot, frontmatter);

	validateDomainPaths(projectRoot, domain, config.orchestrator.name, warnings);

	const tools = (frontmatter.tools as string[] | undefined) || [];
	const basePrompt = resolveTemplates(body.trim(), projectRoot, frontmatter, config.orchestrator.name, warnings);

	return {
		name: config.orchestrator.name,
		color: config.orchestrator.color,
		model,
		basePrompt,
		domain,
		expertise,
		tools,
	};
}

/**
 * Load agent config from its .md file.
 * THROWS if the agent .md file is missing — this is fatal.
 */
function loadAgentConfig(projectRoot: string, ref: AgentRef, teamSessionDir: string, sessionBaseDir: string, logPath: string, sharedContext: string[], warnings: string[]): AgentConfig {
	const filePath = join(projectRoot, ref.path);

	if (!existsSync(filePath)) {
		throw new Error(`FATAL: Agent file not found: ${filePath}\nAgent "${ref.name}" declared in multi-team-config.yaml but .md file is missing`);
	}

	let content: string;
	try { content = readFileSync(filePath, "utf-8"); } catch (e: any) {
		throw new Error(`FATAL: Agent file unreadable: ${filePath}\n${e.message}`);
	}

	const { frontmatter, body } = parseFrontmatter<Record<string, any>>(content);
	// Config model override (ref.model from YAML) takes precedence over frontmatter model
	const model = ref.model || (frontmatter.model as string) || "anthropic/claude-sonnet-4-6";
	const kebabName = ref.name.toLowerCase().replace(/\s+/g, "-");
	const domain = parseFrontmatterDomain(frontmatter);
	const expertise = parseFrontmatterExpertise(projectRoot, frontmatter);
	const tools = (frontmatter.tools as string[] | undefined) || [];

	validateDomainPaths(projectRoot, domain, ref.name, warnings);

	// Build system prompt: resolve templates, append domain, append shared context
	let prompt = resolveTemplates(body.trim(), projectRoot, frontmatter, ref.name, warnings, sessionBaseDir, logPath);
	if (domain.length > 0) {
		prompt += `\n\n## Domain Restrictions\n\n${buildDomainBlock(domain, projectRoot)}`;
	}
	prompt += buildSharedContextBlock(projectRoot, sharedContext, warnings);

	return {
		name: ref.name,
		model,
		systemPrompt: prompt,
		filePath,
		color: ref.color,
		domain,
		expertise,
		tools,
		consultWhen: ref.consultWhen || "",
		sessionFile: join(teamSessionDir, `${kebabName}.jsonl`),
	};
}

/**
 * Load all teams with their leads and members.
 * THROWS if any agent .md file is missing — this is fatal.
 */
export function loadTeams(projectRoot: string, config: MultiTeamConfig, sessionBaseDir: string, logPath: string, warnings: string[]): TeamConfig[] {
	const teams: TeamConfig[] = [];

	for (const teamDef of config.teams) {
		const teamSessionDir = join(sessionBaseDir, teamDef.name.toLowerCase().replace(/\s+/g, "-"));
		if (!existsSync(teamSessionDir)) mkdirSync(teamSessionDir, { recursive: true });

		const leadConfig = loadAgentConfig(projectRoot, teamDef.lead, teamSessionDir, sessionBaseDir, logPath, config.sharedContext, warnings);

		const members: AgentConfig[] = [];
		for (const memberRef of teamDef.members) {
			const mc = loadAgentConfig(projectRoot, memberRef, teamSessionDir, sessionBaseDir, logPath, config.sharedContext, warnings);
			members.push(mc);
		}

		// Resolve {{MEMBERS_BLOCK}} now that we have the full member list.
		// This must happen after members are loaded — the lead's loadAgentConfig()
		// intentionally leaves {{MEMBERS_BLOCK}} unresolved (like {{TEAMS_BLOCK}}
		// in the orchestrator, which is resolved at runtime in buildOrchestratorPrompt).
		leadConfig.systemPrompt = leadConfig.systemPrompt.replace("{{MEMBERS_BLOCK}}", buildMembersBlock(members));

		teams.push({
			name: teamDef.name,
			color: teamDef.color,
			consultWhen: teamDef.consultWhen || "",
			lead: leadConfig,
			members,
		});
	}

	return teams;
}

/**
 * Validate shared_context file paths. Pushes warnings for missing files.
 */
export function validateSharedContext(projectRoot: string, sharedContext: string[], warnings: string[]): void {
	for (const relPath of sharedContext) {
		const absPath = join(projectRoot, relPath);
		if (!existsSync(absPath)) {
			warnings.push(`Shared context file not found: ${relPath} (resolved: ${absPath})`);
		}
	}
}

export function loadDotEnv(projectRoot: string): Record<string, string> {
	const envPath = join(projectRoot, ".env");
	if (!existsSync(envPath)) throw new Error(`No .env at ${envPath}`);
	const appRequire = createRequire(import.meta.url);
	const dotenv = appRequire("dotenv");
	dotenv.config({ path: envPath, quiet: true });
	return { ...process.env } as Record<string, string>;
}

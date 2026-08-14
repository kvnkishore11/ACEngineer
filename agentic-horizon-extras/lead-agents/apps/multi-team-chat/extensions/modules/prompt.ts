// ── Orchestrator Prompt Builder ──────────────────────────────────

import type { TeamConfig, DomainRule } from "./types";
import { buildDomainBlock } from "./domain";
import { buildSharedContextBlock } from "./config";

/**
 * Build the {{TEAMS_BLOCK}} content as YAML.
 * The `team-name` field is the exact value to pass to `delegate(teams: ...)`.
 */
export function buildTeamsBlock(teams: TeamConfig[]): string {
	if (teams.length === 0) return "_No teams configured._";

	const lines: string[] = [];
	for (const t of teams) {
		lines.push(`- team-name: ${t.name}   # pass this exact value to delegate()`);
		if (t.consultWhen) lines.push(`  consult-when: ${t.consultWhen}`);
		lines.push(`  lead: ${t.lead.name}`);
		lines.push(`  members:`);
		for (const m of t.members) {
			lines.push(`    - name: ${m.name}`);
			lines.push(`      consult-when: ${m.consultWhen || "General specialist"}`);
		}
	}
	return lines.join("\n");
}

/**
 * Resolve the orchestrator's system prompt.
 *
 * The basePrompt (from orchestrator.md body with {{EXPERTISE_BLOCK}} and
 * {{SKILLS_BLOCK}} already resolved) still contains {{TEAMS_BLOCK}} and
 * {{SESSION_DIR}}. This function fills them, then appends domain
 * restrictions and the conversation log path.
 */
export function buildOrchestratorPrompt(
	basePrompt: string,
	teams: TeamConfig[],
	logPath: string,
	projectRoot: string,
	orchestratorDomain: DomainRule[],
	sessionDir: string,
	sharedContext: string[],
): string {
	let prompt = basePrompt;

	// Resolve orchestrator-specific templates
	prompt = prompt.replace("{{TEAMS_BLOCK}}", buildTeamsBlock(teams));
	prompt = prompt.replace("{{SESSION_DIR}}", sessionDir);
	prompt = prompt.replace("{{CONVERSATION_LOG}}", logPath);

	// Append domain restrictions
	if (orchestratorDomain.length > 0) {
		prompt += `\n\n## Domain Restrictions\n\n${buildDomainBlock(orchestratorDomain, projectRoot)}`;
	}

	// Append shared context
	prompt += buildSharedContextBlock(projectRoot, sharedContext);

	return prompt;
}

// ── Helper Utilities ─────────────────────────────────────────────
// Small utility functions: logging, budgets, constraints, session IDs.

import { appendFileSync } from "node:fs";
import { join } from "node:path";
import type { MeetingState, ConstraintState } from "./types";

export function generateSessionId(): string {
	return Math.random().toString(36).substring(2, 8);
}

export function parseBudget(budget: string): number {
	return parseFloat(budget.replace(/^\$/, "")) || 0;
}

export function appendToLog(logPath: string, entry: object): void {
	appendFileSync(logPath, JSON.stringify(entry) + "\n", "utf-8");
}

/**
 * Trim tool args for logging — truncate each value to 20 chars.
 */
export function trimToolArgs(args: Record<string, any> | undefined): Record<string, string> {
	if (!args || typeof args !== "object") return {};
	const trimmed: Record<string, string> = {};
	for (const [key, val] of Object.entries(args)) {
		const str = typeof val === "string" ? val : JSON.stringify(val) ?? "";
		trimmed[key] = str.length > 24 ? str.slice(0, 10) + "..." + str.slice(-10) : str;
	}
	return trimmed;
}

/**
 * Append a tool-use entry to the deliberation's tool-use.jsonl.
 */
export function appendToolUse(deliberationDir: string, entry: {
	agent: string;
	timestamp: string;
	tool_name: string;
	tool_call_id?: string;
	args: Record<string, string>;
}): void {
	const toolLogPath = join(deliberationDir, "tool-use.jsonl");
	appendFileSync(toolLogPath, JSON.stringify(entry) + "\n", "utf-8");
}

export function getConstraintState(state: MeetingState): ConstraintState {
	const elapsedMs = Date.now() - state.startTime;
	const elapsedMinutes = elapsedMs / 1000 / 60;
	const minTime = state.constraints.min_time_minutes;
	const maxTime = state.constraints.max_time_minutes;
	const minBudget = parseBudget(state.constraints.min_budget);
	const maxBudget = parseBudget(state.constraints.max_budget);
	const budgetSpent = state.budgetSpent;

	const pastMinTime = elapsedMinutes >= minTime;
	const pastMinBudget = budgetSpent >= minBudget;
	const approachingMaxTime = elapsedMinutes >= maxTime * 0.8;
	const approachingMaxBudget = budgetSpent >= maxBudget * 0.8;
	const hitMaxTime = elapsedMinutes >= maxTime;
	const hitMaxBudget = budgetSpent >= maxBudget;

	let hitMaxReason: ConstraintState["hit_max_reason"] = "none";
	if (hitMaxTime && hitMaxBudget) hitMaxReason = "max_time_and_budget_constraint";
	else if (hitMaxTime) hitMaxReason = "max_time_constraint";
	else if (hitMaxBudget) hitMaxReason = "max_budget_constraint";

	return {
		elapsed_time_minutes: Math.round(elapsedMinutes * 10) / 10,
		budget_spent: Math.round(budgetSpent * 100) / 100,
		past_min_time: pastMinTime,
		past_min_budget: pastMinBudget,
		approaching_max_time: approachingMaxTime,
		approaching_max_budget: approachingMaxBudget,
		hit_max: hitMaxTime || hitMaxBudget,
		hit_max_reason: hitMaxReason,
	};
}

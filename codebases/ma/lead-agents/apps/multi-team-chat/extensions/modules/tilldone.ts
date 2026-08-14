// ── TillDone State Management ────────────────────────────────────

import type { TaskStatus, TillDoneTask, TillDoneState, TillDoneMutation } from "./types";
import { hexFg, dim, bold, truncateToWidth, visibleWidth, wrapTextWithAnsi } from "./theme";

// ── Status helpers ─────────────────────────────────────────────

export const STATUS_ICON: Record<TaskStatus, string> = {
	idle: "○",
	inprogress: "●",
	done: "✓",
};

// ── State factory ──────────────────────────────────────────────

export function createState(): TillDoneState {
	return { title: "", tasks: [], nextId: 1 };
}

// ── Mutations (all idempotent) ─────────────────────────────────

export function addTask(state: TillDoneState, text: string, team?: string, teamColor?: string): TillDoneTask {
	const task: TillDoneTask = { id: state.nextId++, text, status: "idle" };
	if (team) task.team = team;
	if (teamColor) task.teamColor = teamColor;
	state.tasks.push(task);
	return task;
}

export function addTasks(state: TillDoneState, texts: string[], team?: string, teamColor?: string): TillDoneTask[] {
	return texts.map(t => addTask(state, t, team, teamColor));
}

export function startTask(state: TillDoneState, id: number, team?: string, teamColor?: string): TillDoneTask | null {
	const task = state.tasks.find(t => t.id === id);
	if (!task) return null;
	if (task.status === "done") return task; // Don't regress done → inprogress
	task.status = "inprogress";
	if (team) task.team = team;
	if (teamColor) task.teamColor = teamColor;
	return task;
}

export function doneTask(state: TillDoneState, id: number): TillDoneTask | null {
	const task = state.tasks.find(t => t.id === id);
	if (!task) return null;
	task.status = "done";
	return task;
}

export function updateTask(state: TillDoneState, id: number, text: string): TillDoneTask | null {
	const task = state.tasks.find(t => t.id === id);
	if (!task) return null;
	task.text = text;
	return task;
}

export function removeTask(state: TillDoneState, id: number): TillDoneTask | null {
	const idx = state.tasks.findIndex(t => t.id === id);
	if (idx === -1) return null;
	return state.tasks.splice(idx, 1)[0];
}

export function clearState(state: TillDoneState): void {
	state.tasks = [];
	state.nextId = 1;
	state.title = "";
	state.description = undefined;
}

export function applyMutation(state: TillDoneState, mutation: TillDoneMutation): void {
	switch (mutation.action) {
		case "start":
			startTask(state, mutation.id, mutation.team, mutation.teamColor);
			break;
		case "done":
			doneTask(state, mutation.id);
			break;
	}
}

// ── Footer rendering ───────────────────────────────────────────

/**
 * Render the TillDone column for the footer right side.
 * Returns string[] lines ready for mergeColumns.
 *
 * @param expanded  When true (e.g. /toggle-workers mode), show full task text
 *                  with wrapping. When false, truncate with ellipsis.
 */
export function renderTillDoneColumn(state: TillDoneState, width: number, expanded = false): string[] {
	if (state.tasks.length === 0) return [];

	const lines: string[] = [];
	const doneCount = state.tasks.filter(t => t.status === "done").length;
	const total = state.tasks.length;

	// Line 1: title + [done/total]
	const title = state.title || "TillDone";
	const progress = `[${doneCount}/${total}]`;
	const l1 = `${dim("TillDone:")} ${hexFg("#72f1b8", title)} ${dim(progress)}`;
	lines.push(truncateToWidth(l1, width, ""));

	// Build smart window: done first (most recent at top), then inprogress, then idle
	const done = state.tasks.filter(t => t.status === "done").reverse(); // most recent first
	const inprogress = state.tasks.filter(t => t.status === "inprogress");
	const idle = state.tasks.filter(t => t.status === "idle");

	const maxSlots = expanded ? state.tasks.length : 8;
	const visible: TillDoneTask[] = [];

	// Recent completions first — shows progress at a glance
	for (const t of done) { if (visible.length < maxSlots) visible.push(t); }
	// Then active work
	for (const t of inprogress) { if (visible.length < maxSlots) visible.push(t); }
	// Fill remaining with queued tasks
	for (const t of idle) { if (visible.length < maxSlots) visible.push(t); }

	const hiddenIdle = idle.length - idle.filter(t => visible.includes(t)).length;
	const hiddenDone = done.length - done.filter(t => visible.includes(t)).length;

	for (const t of visible) {
		const icon = t.status === "done"
			? hexFg("#9ece6a", STATUS_ICON.done)
			: t.status === "inprogress"
				? hexFg(t.teamColor || "#72f1b8", STATUS_ICON.inprogress)
				: dim(STATUS_ICON.idle);

		const text = t.status === "done"
			? dim(t.text)
			: t.status === "inprogress"
				? hexFg(t.teamColor || "#72f1b8", t.text)
				: t.text;

		const teamLabel = t.team && t.status !== "idle"
			? ` ${dim(t.team)}`
			: "";

		const fullLine = ` ${icon} ${text}${teamLabel}`;

		if (expanded) {
			const wrapped = wrapTextWithAnsi(fullLine, width - 1);
			for (const wl of wrapped) lines.push(truncateToWidth(wl, width, ""));
		} else {
			lines.push(truncateToWidth(fullLine, width));
		}
	}

	// Summary of hidden tasks
	const hiddenParts: string[] = [];
	if (hiddenIdle > 0) hiddenParts.push(`${hiddenIdle} queued`);
	if (hiddenDone > 0) hiddenParts.push(`${hiddenDone} done`);
	if (hiddenParts.length > 0) {
		lines.push(truncateToWidth(` ${dim(`+${hiddenParts.join(", ")}`)}`, width, ""));
	}

	return lines;
}

/**
 * Merge two string[] columns side-by-side.
 * Pads shorter column, truncates each merged line to totalWidth.
 */
export function mergeColumns(
	left: string[],
	right: string[],
	leftWidth: number,
	totalWidth: number,
): string[] {
	const maxLen = Math.max(left.length, right.length);
	const result: string[] = [];

	for (let i = 0; i < maxLen; i++) {
		const l = left[i] || "";
		const r = right[i] || "";
		const lVis = visibleWidth(l);
		const pad = Math.max(1, leftWidth - lVis);
		result.push(truncateToWidth(l + " ".repeat(pad) + r, totalWidth, ""));
	}

	return result;
}

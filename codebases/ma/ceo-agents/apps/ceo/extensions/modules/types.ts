// ── Type Definitions ─────────────────────────────────────────────
// Shared interfaces used across all CEO & Board extension modules.

export interface MeetingConstraints {
	min_time_minutes: number;
	max_time_minutes: number;
	min_budget: string;
	max_budget: string;
}

export interface BriefSection {
	section: string;
	description: string;
}

export interface BoardMember {
	name: string;
	path: string;
	color: string;
}

export interface BoardMemberConfig {
	name: string;
	model: string;
	systemPrompt: string;
	filePath: string;
	color: string;
	sessionFile: string;
}

export interface CeoConfig {
	meeting: {
		constraints: MeetingConstraints;
		editor: string;
	};
	paths: {
		briefs: string;
		deliberations: string;
		memos: string;
		agents: string;
	};
	brief_sections: BriefSection[];
	board: BoardMember[];
}

export interface MeetingState {
	sessionId: string;
	startTime: number;
	budgetSpent: number;
	activeMembers: BoardMemberConfig[];
	phase: "idle" | "deliberating" | "ending" | "complete";
	briefPath: string;
	briefContent: string;
	contextFiles: string[];
	deliberationDir: string;
	logPath: string;
	memoPath: string;
	constraints: MeetingConstraints;
}

export interface MemberStats {
	chats: number;
	cost: number;
	tokensUsed: number;
	contextWindow: number;
}

export interface ConstraintState {
	elapsed_time_minutes: number;
	budget_spent: number;
	past_min_time: boolean;
	past_min_budget: boolean;
	approaching_max_time: boolean;
	approaching_max_budget: boolean;
	hit_max: boolean;
	hit_max_reason: "none" | "max_time_constraint" | "max_budget_constraint" | "max_time_and_budget_constraint";
}

export interface BoardMemberResult {
	response: string;
	tokensIn: number;
	tokensOut: number;
	cost: number;
	contextTokens: number;
	model: string;
}

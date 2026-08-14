// ── Type Definitions ─────────────────────────────────────────────

export interface DomainRule {
	path: string;
	read: boolean;
	upsert: boolean;
	delete: boolean;
}

export interface SkillRef {
	path: string;
	useWhen?: string;
}

export interface ExpertiseRef {
	path: string;
	updatable: boolean;
	useWhen?: string;
}

/** Expertise ref with absolute path — used for enforcement and subprocess env */
export interface ResolvedExpertise {
	absPath: string;
	updatable: boolean;
	maxLines: number;
}

export interface AgentRef {
	name: string;
	path: string;
	color: string;
	model?: string;
	domain?: DomainRule[];
	consultWhen?: string;
	skills?: SkillRef[];
}

export interface AgentConfig {
	name: string;
	model: string;
	systemPrompt: string;
	filePath: string;
	color: string;
	domain: DomainRule[];
	expertise: ResolvedExpertise[];
	tools: string[];
	consultWhen: string;
	sessionFile: string;
}

export interface TeamConfig {
	name: string;
	color: string;
	consultWhen: string;
	lead: AgentConfig;
	members: AgentConfig[];
}

export interface MultiTeamConfig {
	orchestrator: AgentRef;
	teams: {
		name: string;
		color: string;
		consultWhen: string;
		lead: AgentRef;
		members: AgentRef[];
	}[];
	paths: {
		agents: string;
		sessions: string;
	};
	sharedContext: string[];
}

export interface OrchestratorConfig {
	name: string;
	color: string;
	model: string;
	basePrompt: string;
	domain: DomainRule[];
	expertise: ResolvedExpertise[];
	tools: string[];
}

export interface LogEntry {
	from: string;
	to?: string;
	message: string;
	timestamp: string;
	type: "user" | "orchestrator" | "delegate" | "lead" | "member" | "synthesis" | "system";
	team?: string;
	cost?: number;
	tokens_in?: number;
	tokens_out?: number;
}

export interface ToolUse {
	name: string;
	args?: Record<string, any>;
	callId?: string; // tool_execution_start toolCallId — needed to match updates/ends
	blocked?: boolean; // true if tool was rejected by domain/tool enforcement
}

export interface SubprocessResult {
	response: string;
	tokensIn: number;
	tokensOut: number;
	cost: number;
	contextTokens: number;
	model: string;
	toolCalls: ToolUse[];
}

// ── Stats Tracking ───────────────────────────────────────────────

export interface AgentStats {
	cost: number;
	tokensIn: number;
	tokensOut: number;
	contextTokens: number;
	calls: number;
}

// ── Delegate Tool Progress ───────────────────────────────────────

export interface MemberProgress {
	name: string;
	color: string;
	text: string;
	state: "waiting" | "thinking" | "streaming" | "done";
}

export interface TeamProgress {
	name: string;
	color: string;
	leadName: string;
	leadColor: string;
	phase: "lead-analyzing" | "members-working" | "synthesizing" | "done";
	leadText: string;
	members: MemberProgress[];
	synthesis: string;
}

export interface DelegateDetails {
	teams: TeamProgress[];
	finalSyntheses?: { team: string; lead: string; synthesis: string; cost: number }[];
}

// ── Chat Bubble Message ─────────────────────────────────────────

export interface TeamChatDetails {
	name: string;
	color: string;
	role: "lead" | "member" | "synthesis";
	team: string;
	timestamp: string;
}

// ── TillDone Task Tracking ─────────────────────────────────────

export type TaskStatus = "idle" | "inprogress" | "done";

export interface TillDoneTask {
	id: number;
	text: string;
	status: TaskStatus;
	team?: string;
	teamColor?: string;
}

export interface TillDoneState {
	title: string;
	description?: string;
	tasks: TillDoneTask[];
	nextId: number;
}

/** Mutation sent from lead subprocess → parent via onUpdate */
export interface TillDoneMutation {
	type: "tilldone-mutation";
	action: "start" | "done";
	id: number;
	team?: string;
	teamColor?: string;
}

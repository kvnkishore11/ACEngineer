# Plan: Modularize CEO & Board Extension

## Task Description

Break the monolithic `apps/ceo/extensions/ceo-and-board.ts` (2,021 lines) into ~5 focused module files under `apps/ceo/extensions/modules/`. The main entry point stays as the orchestrator, importing from the modules. Each module has a single responsibility and clean export surface.

## Objective

Reduce the main extension file from 2,021 lines to ~1,250 lines by extracting 5 cohesive modules into `extensions/modules/`. All existing behavior is preserved — the extension boots, deliberates, and produces memos identically to before. The only change is file organization.

## Problem Statement

The extension is a single 2k-line file containing types, YAML parsing, ANSI theme helpers, subprocess management, TUI widget rendering, and tool/command/event registration. This makes it hard to navigate, test individual pieces, or onboard contributors. The file has natural seam lines (types, config, theme, subprocess, utilities) that map cleanly to modules.

## Solution Approach

Extract code into 5 modules by concern. Each module exports only what the main file needs. No new dependencies, no behavior changes, no API changes. The main file becomes a thin orchestrator that imports types and functions, then wires them into pi's extension API.

## Relevant Files

Use these files to complete the task:

- `apps/ceo/extensions/ceo-and-board.ts` — the 2,021-line monolith to modularize. This is the ONLY source of truth. Every line of code in the new modules must come from this file.
- `.pi/ceo-agents/ceo-and-board-configuration.yaml` — the YAML config the `config.ts` module parses. Use to verify parsing still works.
- `.pi/ceo-agents/agents/ceo.md` — CEO system prompt with frontmatter. Used by `buildExpertiseBlock` and `buildSkillsBlock` in the config module.
- `.pi/ceo-agents/agents/revenue.md` — example board member prompt. Used to verify `loadBoardMembers` still resolves paths and parses frontmatter.
- `.pi/ceo-agents/briefs/2026-03-18-solo-plugin-bet/brief.md` — example brief. Used to verify brief validation in `/ceo-begin`.
- `justfile` — `just ceo` launches the extension. Use for smoke testing.
- `README.md` — update the Directory Structure section to reflect the new `modules/` directory.

### New Files

- `apps/ceo/extensions/modules/types.ts` — all interfaces and type definitions
- `apps/ceo/extensions/modules/config.ts` — YAML config parsing, project root discovery, board member loading
- `apps/ceo/extensions/modules/theme.ts` — ANSI color helpers, gauge rendering, board status rendering
- `apps/ceo/extensions/modules/subprocess.ts` — board member pi subprocess spawning
- `apps/ceo/extensions/modules/helpers.ts` — small utility functions (logging, budgets, constraints, session IDs)

## Implementation Phases

### Phase 1: Foundation — Create Module Files with Exports

Extract code from the monolith into 5 module files. Each module is a pure extraction — copy the relevant functions/interfaces, add the necessary imports, and export everything the main file needs.

### Phase 2: Core Implementation — Rewire the Main File

Replace the extracted code in `ceo-and-board.ts` with imports from the 5 modules. Remove all moved code. The main file should contain ONLY the `export default function(pi: ExtensionAPI)` body and nothing else (no standalone functions, no interfaces, no theme helpers).

### Phase 3: Integration & Polish — Validate, Fix, Document

Run the extension via `just ceo` to verify it boots and the TUI renders correctly. Run `/ceo-begin` to ensure brief selection and board member loading work. Update README.md with the new directory structure. Use `/drive` to validate terminal behavior. Use `/tts-eleven` to announce completion.

## Module Breakdown

### 1. `modules/types.ts` (~85 lines)

**Exports:** All interfaces used across modules.

```ts
// Extract these interfaces (lines 60–143 of the original):
export interface MeetingConstraints { ... }
export interface BriefSection { ... }
export interface BoardMember { ... }
export interface BoardMemberConfig { ... }
export interface CeoConfig { ... }
export interface MeetingState { ... }
export interface MemberStats { ... }
export interface ConstraintState { ... }
export interface BoardMemberResult { ... }
```

**Imports:** None (pure type definitions).

### 2. `modules/config.ts` (~270 lines)

**Exports:** `findProjectRoot`, `findConfigPath`, `parseConfig`, `loadBoardMembers`, `loadDotEnv`, `buildExpertiseBlock`, `buildSkillsBlock`.

```ts
// Extract these functions (lines 147–507 of the original):
export function findProjectRoot(cwd: string): string | null { ... }
export function findConfigPath(cwd: string): string | null { ... }
export function parseConfig(cwd: string): CeoConfig | null { ... }
export function loadDotEnv(projectRoot: string): Record<string, string> { ... }
export function buildExpertiseBlock(...): string { ... }
export function buildSkillsBlock(...): string { ... }
export function loadBoardMembers(...): BoardMemberConfig[] { ... }
```

**Imports:**
- `node:fs` — `existsSync`, `readFileSync`, `mkdirSync`
- `node:path` — `join`, `dirname`, `basename`
- `@mariozechner/pi-coding-agent` — `parseFrontmatter`
- `./types` — `CeoConfig`, `BoardMember`, `BoardMemberConfig`, `BriefSection`, `MeetingConstraints`

### 3. `modules/theme.ts` (~170 lines)

**Exports:** `bgWarm`, `cyan`, `pink`, `yellow`, `green`, `dim`, `bold`, `parseHexColor`, `formatTokenCount`, `renderGaugeLine`, `renderBoardStatusLines`.

```ts
// Extract these (lines 29–57, 386–393, 509–570, 814–865):
export function bgWarm(s: string): string { ... }
export function cyan(s: string): string { ... }
export function pink(s: string): string { ... }
export function yellow(s: string): string { ... }
export function green(s: string): string { ... }
export function dim(s: string): string { ... }
export function bold(s: string): string { ... }
export function parseHexColor(hex: string): { r: number; g: number; b: number } { ... }
export function formatTokenCount(count: number): string { ... }
export function renderGaugeLine(...): string { ... }

// renderBoardStatusLines becomes a standalone exported function.
// It currently lives inside the `export default function(pi)` closure,
// accessing `meetingState`, `memberStats`, and `respondingMembers` via closure.
// To extract it, pass those as parameters:
export function renderBoardStatusLines(
  width: number,
  activeMembers: BoardMemberConfig[],
  memberStats: Map<string, MemberStats>,
  respondingMembers: Set<string>,
): string[] { ... }
```

**Imports:**
- `@mariozechner/pi-tui` — `truncateToWidth`, `visibleWidth`
- `./types` — `BoardMemberConfig`, `MemberStats`, `MeetingState`

### 4. `modules/subprocess.ts` (~170 lines)

**Exports:** `callBoardMember`.

```ts
// Extract lines 572–738:
export async function callBoardMember(
  member: BoardMemberConfig,
  ceoMessage: string,
  subprocessEnv: Record<string, string>,
  signal?: AbortSignal,
  onText?: (accumulated: string) => void,
  contextFiles?: string[],
  deliberationDir?: string,
  onToolUse?: (toolName: string, toolCallId: string, args: Record<string, any>) => void,
): Promise<BoardMemberResult> { ... }
```

**Imports:**
- `node:child_process` — `spawn`
- `node:fs` — `existsSync`
- `node:path` — `join`
- `./types` — `BoardMemberConfig`, `BoardMemberResult`

### 5. `modules/helpers.ts` (~80 lines)

**Exports:** `generateSessionId`, `parseBudget`, `appendToLog`, `trimToolArgs`, `appendToolUse`, `getConstraintState`.

```ts
// Extract lines 337–461 (minus loadBoardMembers which goes to config.ts):
export function generateSessionId(): string { ... }
export function parseBudget(budget: string): number { ... }
export function appendToLog(logPath: string, entry: object): void { ... }
export function trimToolArgs(args: Record<string, any> | undefined): Record<string, string> { ... }
export function appendToolUse(deliberationDir: string, entry: { ... }): void { ... }
export function getConstraintState(state: MeetingState): ConstraintState { ... }
```

**Imports:**
- `node:fs` — `appendFileSync`
- `node:path` — `join`
- `./types` — `MeetingState`, `ConstraintState`

### Main File After Modularization (`ceo-and-board.ts`)

**Imports from modules:**
```ts
import type { CeoConfig, MeetingState, MemberStats, ConstraintState, BoardMemberConfig } from "./modules/types";
import { findProjectRoot, parseConfig, loadBoardMembers, loadDotEnv, buildExpertiseBlock, buildSkillsBlock } from "./modules/config";
import { bgWarm, cyan, pink, yellow, green, dim, bold, parseHexColor, formatTokenCount, renderGaugeLine, renderBoardStatusLines } from "./modules/theme";
import { callBoardMember } from "./modules/subprocess";
import { generateSessionId, parseBudget, appendToLog, trimToolArgs, appendToolUse, getConstraintState } from "./modules/helpers";
```

**Remaining content:** Only the `export default function(pi: ExtensionAPI)` body containing:
- State variables (config, meetingState, memberStats, etc.)
- `registerConstraintGauges()` closure helper
- `registerMessageRenderer("board-response")`
- `registerTool("converse")` with execute, renderCall, renderResult
- `registerTool("end_deliberation")` with execute, renderCall, renderResult
- `registerCommand("ceo-begin")`
- Event handlers: `before_agent_start`, `message_end`, `tool_execution_start`, `input`, `tool_result`, `session_start`

Estimated: ~1,250 lines (down from 2,021).

## Key Refactoring Notes

### `renderBoardStatusLines` Signature Change

This function currently lives inside the main closure and accesses `meetingState`, `memberStats`, and `respondingMembers` as free variables. When extracting to `theme.ts`, change its signature to accept these as parameters:

```ts
// BEFORE (closure access):
function renderBoardStatusLines(width: number): string[] {
  if (!meetingState || meetingState.activeMembers.length === 0) return [];
  const members = meetingState.activeMembers;
  // ...uses memberStats, respondingMembers from closure
}

// AFTER (explicit parameters):
export function renderBoardStatusLines(
  width: number,
  activeMembers: BoardMemberConfig[],
  memberStats: Map<string, MemberStats>,
  respondingMembers: Set<string>,
): string[] {
  if (activeMembers.length === 0) return [];
  const members = activeMembers;
  // ...same logic, using parameters instead of closure vars
}
```

Update the call site in `session_start` handler's footer render:
```ts
// BEFORE:
const boardLines = renderBoardStatusLines(width);

// AFTER:
const boardLines = renderBoardStatusLines(width, meetingState?.activeMembers || [], memberStats, respondingMembers);
```

### No Barrel File

Do NOT create an `modules/index.ts` barrel file. Each consumer imports directly from the specific module file. This keeps dependency chains explicit and avoids circular import issues.

### Import Style

Use named imports only. No `import *`. Every import is explicit so it's clear what each module provides.

## Team Orchestration

- You operate as the team lead and orchestrate the team to execute the plan.
- You're responsible for deploying the right team members with the right context to execute the plan.
- IMPORTANT: You NEVER operate directly on the codebase. You use `Task` and `Task*` tools to deploy team members to do the building, validating, testing, deploying, and other tasks.
- Take note of the session id of each team member. This is how you'll reference them.

### Team Members

- Builder
  - Name: modularizer
  - Role: Extract modules from the monolith and rewire the main entry point
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: validator
  - Role: Validate the modularized extension compiles and the TUI boots correctly
  - Agent Type: general-purpose
  - Resume: true

- Builder
  - Name: docs-updater
  - Role: Update README.md with the new modules directory structure and file descriptions
  - Agent Type: general-purpose
  - Resume: false

## Step by Step Tasks

- IMPORTANT: Execute every step in order, top to bottom. Each task maps directly to a `TaskCreate` call.
- Before you start, run `TaskCreate` to create the initial task list that all team members can see and execute.

### 1. Create modules/types.ts
- **Task ID**: create-types-module
- **Depends On**: none
- **Assigned To**: modularizer
- **Agent Type**: general-purpose
- **Parallel**: false
- Create `apps/ceo/extensions/modules/` directory
- Extract all 9 interfaces (lines 60–143) from `ceo-and-board.ts` into `modules/types.ts`
- Add `export` keyword to each interface
- No imports needed — these are pure type definitions
- Verify the file has no runtime code, only type definitions

### 2. Create modules/helpers.ts
- **Task ID**: create-helpers-module
- **Depends On**: create-types-module
- **Assigned To**: modularizer
- **Agent Type**: general-purpose
- **Parallel**: false
- Extract `generateSessionId` (line 337), `parseBudget` (line 395), `appendToLog` (line 399), `trimToolArgs` (line 406), `appendToolUse` (line 419), `getConstraintState` (line 430) into `modules/helpers.ts`
- Add necessary imports: `appendFileSync` from `node:fs`, `join` from `node:path`
- Import types from `./types`: `MeetingState`, `ConstraintState`
- Export all functions
- `parseBudget` is used by `getConstraintState` internally — keep both in this module

### 3. Create modules/config.ts
- **Task ID**: create-config-module
- **Depends On**: create-types-module
- **Assigned To**: modularizer
- **Agent Type**: general-purpose
- **Parallel**: true (can run in parallel with create-helpers-module)
- Extract `findProjectRoot` (line 147), `findConfigPath` (line 158), `parseConfig` (line 169), `loadDotEnv` (line 324), `buildExpertiseBlock` (line 346), `buildSkillsBlock` (line 369), `loadBoardMembers` (line 463) into `modules/config.ts`
- Add necessary imports: `existsSync`, `readFileSync`, `mkdirSync` from `node:fs`; `join`, `dirname`, `basename` from `node:path`; `parseFrontmatter` from `@mariozechner/pi-coding-agent`
- Import types from `./types`: `CeoConfig`, `BoardMember`, `BoardMemberConfig`, `BriefSection`, `MeetingConstraints`
- Export all functions
- Note: `loadBoardMembers` calls `buildExpertiseBlock` and `buildSkillsBlock` internally, so they share the same module

### 4. Create modules/theme.ts
- **Task ID**: create-theme-module
- **Depends On**: create-types-module
- **Assigned To**: modularizer
- **Agent Type**: general-purpose
- **Parallel**: true (can run in parallel with create-helpers-module and create-config-module)
- Extract all ANSI color functions (lines 30–57): `bgWarm`, `cyan`, `pink`, `yellow`, `green`, `dim`, `bold`
- Extract `parseHexColor` (line 386), `formatTokenCount` (line 509), `renderGaugeLine` (line 525)
- Extract `renderBoardStatusLines` (line 814) — refactor signature to accept `activeMembers`, `memberStats`, `respondingMembers` as parameters instead of closure access
- Add imports: `truncateToWidth`, `visibleWidth` from `@mariozechner/pi-tui`
- Import types from `./types`: `BoardMemberConfig`, `MemberStats`
- The color functions (`bgWarm`, `cyan`, `pink`, etc.) are used by `renderGaugeLine` internally — keep them all together
- Export everything

### 5. Create modules/subprocess.ts
- **Task ID**: create-subprocess-module
- **Depends On**: create-types-module
- **Assigned To**: modularizer
- **Agent Type**: general-purpose
- **Parallel**: true (can run in parallel with other module creation tasks)
- Extract `callBoardMember` (lines 574–738) into `modules/subprocess.ts`
- Add imports: `spawn` from `node:child_process`; `existsSync` from `node:fs`; `join` from `node:path`
- Import types from `./types`: `BoardMemberConfig`, `BoardMemberResult`
- Export the function
- This is a self-contained async function with no closure dependencies

### 6. Rewire Main Entry Point
- **Task ID**: rewire-main
- **Depends On**: create-types-module, create-helpers-module, create-config-module, create-theme-module, create-subprocess-module
- **Assigned To**: modularizer
- **Agent Type**: general-purpose
- **Parallel**: false
- Remove ALL extracted code from `ceo-and-board.ts` (interfaces, standalone functions, color helpers)
- Add import statements at the top for all 5 modules (see "Import Style" section above)
- Keep only: the file header comment, external library imports (`Text`, `Type`, `ExtensionAPI`, `parseFrontmatter`), and the `export default function(pi)` body
- Update the `renderBoardStatusLines` call site in the footer render to pass explicit parameters
- Verify every function that was extracted is now imported and called correctly
- The `parseBudget` function is used inside `registerConstraintGauges` — make sure it's imported from `helpers`
- The color functions (`cyan`, `pink`, `yellow`, `green`, `dim`, `bold`, `bgWarm`) are used in the `session_start` handler — make sure they're imported from `theme`
- `parseHexColor` is used in the `converse` tool widget, `end_deliberation` widget, footer, and `board-response` renderer — import from `theme`

### 7. Validate Compilation
- **Task ID**: validate-compilation
- **Depends On**: rewire-main
- **Assigned To**: validator
- **Agent Type**: general-purpose
- **Parallel**: false
- Run `cd apps/ceo && bun build extensions/ceo-and-board.ts --no-bundle 2>&1` (or `bun --dry-run` equivalent) to check for TypeScript/import errors
- If `bun build` doesn't flag type errors, alternatively run: `cd apps/ceo && npx tsc --noEmit extensions/ceo-and-board.ts` or manually inspect all imports match exports
- Fix any missing imports, wrong paths, or type mismatches
- Verify every `export` in each module has a corresponding `import` in the consumer
- Check for circular imports (there should be none — types.ts has no imports, all other modules only import from types.ts)

### 8. Validate Boot & TUI
- **Task ID**: validate-boot
- **Depends On**: validate-compilation
- **Assigned To**: validator
- **Agent Type**: general-purpose
- **Parallel**: false
- Use `/drive` to launch `just ceo` in a tmux session and verify:
  - Extension loads without errors
  - Synthwave theme applies
  - Startup notification renders with board member list and models
  - Footer shows CEO card and board member status cards
  - `/ceo-begin` command is available and lists briefs
- Fix any runtime bugs discovered during validation
- If critical issues are found, resume the modularizer agent to fix them

### 9. Update README
- **Task ID**: update-readme
- **Depends On**: validate-boot
- **Assigned To**: docs-updater
- **Agent Type**: general-purpose
- **Parallel**: false
- Update the "Directory Structure" section in `README.md` to include the new `modules/` directory
- Add a brief description of each module file's purpose in the directory tree:
  ```
  apps/ceo/extensions/
  ├── ceo-and-board.ts                  # main entry point — pi extension orchestrator
  └── modules/
      ├── types.ts                      # shared interfaces and type definitions
      ├── config.ts                     # YAML config parsing, board member loading
      ├── theme.ts                      # ANSI color helpers, TUI gauge and status rendering
      ├── subprocess.ts                 # board member pi subprocess spawning
      └── helpers.ts                    # utility functions (logging, budgets, constraints)
  ```
- Do NOT change the rest of the README content — only the directory structure section

### 10. Final Validation & Announce
- **Task ID**: validate-all
- **Depends On**: validate-boot, update-readme
- **Assigned To**: validator
- **Agent Type**: general-purpose
- **Parallel**: false
- Run `wc -l apps/ceo/extensions/ceo-and-board.ts` — confirm it's ~1,200-1,300 lines (down from 2,021)
- Run `wc -l apps/ceo/extensions/modules/*.ts` — confirm each module is a reasonable size
- Verify no duplicate code exists between modules and the main file
- Use `/tts-eleven` to announce "Modularization complete. The CEO extension has been split into 5 modules."

## Acceptance Criteria

- [ ] `apps/ceo/extensions/modules/` directory exists with exactly 5 `.ts` files: `types.ts`, `config.ts`, `theme.ts`, `subprocess.ts`, `helpers.ts`
- [ ] `ceo-and-board.ts` contains NO standalone interfaces, NO standalone functions outside `export default function(pi)`, and NO ANSI color helper functions
- [ ] `ceo-and-board.ts` imports from all 5 modules
- [ ] No circular imports between modules (types.ts is the leaf; all others import only from types.ts)
- [ ] `just ceo` boots the extension without errors
- [ ] Startup notification renders correctly with board member names and models
- [ ] Footer renders CEO card and board member status cards
- [ ] `/ceo-begin` lists available briefs and validates required sections
- [ ] `README.md` directory structure section includes the `modules/` directory with file descriptions
- [ ] Main file is ~1,200-1,300 lines (down from 2,021)
- [ ] No behavior changes — the extension works identically to before

## Validation Commands

Execute these commands to validate the task is complete:

- `ls apps/ceo/extensions/modules/` — Verify all 5 module files exist
- `wc -l apps/ceo/extensions/ceo-and-board.ts` — Confirm main file is ~1,200-1,300 lines
- `wc -l apps/ceo/extensions/modules/*.ts` — Confirm module sizes are reasonable (~80-270 lines each)
- `cd apps/ceo && bun build extensions/ceo-and-board.ts --no-bundle 2>&1 | head -20` — Check for compilation errors
- `grep -c "export" apps/ceo/extensions/modules/types.ts` — Should be 9 (one per interface)
- `grep "from.*modules/" apps/ceo/extensions/ceo-and-board.ts` — Verify all 5 module imports are present
- `grep -r "from.*\.\/types" apps/ceo/extensions/modules/` — Verify modules import types correctly

## Notes

- No new dependencies needed. All imports already exist in the project.
- The `@sinclair/typebox` `Type` import stays in `ceo-and-board.ts` — it's only used in tool parameter definitions.
- The `Text` import from `@mariozechner/pi-tui` stays in `ceo-and-board.ts` — it's only used in render functions within the tool registrations.
- `parseFrontmatter` from `@mariozechner/pi-coding-agent` is used in both `config.ts` (for board member loading) AND the main file (in `before_agent_start` for CEO prompt). Import it in both places.
- The `require("dotenv")` call in `loadDotEnv` uses a dynamic require — this is intentional and should stay as-is in `config.ts`.
- The `require("path").parse` call in `findProjectRoot`/`findConfigPath` should be replaced with a proper import of `parse` from `node:path` in `config.ts` during extraction.

# Project: AgenticKanban - Intelligent AI-Driven Kanban Board

## Project Overview
AgenticKanban is a web-based application that serves as an intelligent Kanban board for managing AI-driven development workflows with self-improving capabilities, comprehensive state management, and autonomous sub-agent support. The application provides a visual interface for managing development tasks through a structured pipeline of stages (Plan, Build, Test, Review, Document, PR, Errored) while leveraging AI workflows and sub-agents for autonomous monitoring and execution. It integrates seamlessly with existing Claude Code commands and supports multiple projects with configurable workflows.

## Project Goals
- Create a project-agnostic Kanban board that works with any codebase containing `.claude/commands` and `agentics/` structure
- Provide intelligent workflow management through AI-driven development workflows (ADWs)
- Enable autonomous monitoring through sub-agent systems during build, test, and review phases
- Support rich multimedia input including image annotation and markup
- Integrate with CodeRabbit for automated code review
- Maintain comprehensive logging and error tracking for debugging and improvement
- Deliver real-time visual feedback on workflow progress with substage granularity

## Target Users
- AI-assisted developers managing complex development workflows
- Development teams using Claude Code for automated task execution
- Project managers overseeing AI-driven development pipelines
- DevOps engineers monitoring autonomous development processes

## Project ScopeV
### In Scope
- Multi-project Kanban board with project selection interface
- Six-stage workflow visualization (Plan, Build, Test, Review, Document, PR, Errored)
- Integration with existing `.claude/commands` slash command system
- Support for AI Developer Workflows (ADWs) in `agentics/adws/` directory
- Rich text editor with image support (paste, annotate, crop, markup)
- Sub-agent monitoring system for frontend/backend processes
- SQLite-based data persistence with file system logging
- Real-time progress tracking with substage visibility
- GitHub issues-style input interface for task creation
- Comprehensive error handling and logging visualization
- CodeRabbit integration for automated code reviews

### Out of Scope
- Direct Claude Code execution engine (delegated to existing `.claude/commands`)
- AI orchestration logic (delegated to `agentics/adws/` scripts)
- Version control operations beyond branch visualization
- Advanced analytics and reporting features (Phase 4+)
- Multi-user collaboration features
- Cloud deployment configurations

## Technical Architecture Overview
**Frontend**: React 18+ with TypeScript, Tailwind CSS for styling, ShadCn UI component library, Framer Motion for animations, TipTap rich text editor with image editing plugins

**State Management**: Zustand for global state management with persistence

**Data Storage**: SQLite for structured workflow data, file system for logs and artifacts

**AI Integration**: RESTful API endpoints for prompt validation, similarity search, KPI analysis, and sub-agent communication protocol

**Build Tools**: Vite for frontend bundling, modern ES modules support

## Relevant Files
Use these files to understand the existing codebase structure:

**Existing Architecture**
- `.claude/commands/` - Contains all slash command definitions including `project.md`, `implement.md`, `test_e2e.md`
- `.claude/commands/e2e/test_basic_query.md` - E2E test pattern reference
- `.claude/commands/conditional_docs.md` - Documentation reference guide
- `agentics/logs/` - Current logging structure with JSON format
- `prompt.md` - Core project requirements and vision

### New Files
- `app/` - Main application directory
  - `app/client/` - React frontend application
  - `app/server/` - Backend API server (Python/FastAPI)
- `agentics/specs/` - Project and feature specifications
- `agentics/ai-docs/` - AI agent documentation
- `agentics/app-docs/` - User-facing documentation
- `agentics/scripts/` - Utility scripts
- `agentics/agents/` - Sub-agent execution logs
- `agentics/adws/` - AI Developer Workflow scripts

## Feature Breakdown

### Phase 1: Foundation Features (MVP)

#### Feature 1.1: Project Selection Interface
- **Description**: VS Code-style project folder selection with support for multiple projects
- **User Story**: As a developer, I want to select any project containing `.claude/commands` and `agentics/` structure so that I can manage workflows for different codebases
- **Acceptance Criteria**:
  - Folder browser interface for project selection
  - Validation of required directory structure (.claude/commands, agentics/)
  - Project tabs showing "Ongoing" and "Completed" workflows
  - Persistent project selection across sessions
- **Dependencies**: None
- **Estimated Complexity**: Medium

#### Feature 1.2: Basic Kanban Board Layout
- **Description**: Six-column Kanban board with automatic stage progression (no drag-and-drop)
- **User Story**: As a user, I want to visualize my workflow stages (Plan, Build, Test, Review, Document, PR, Errored) so that I can track progress at a glance
- **Acceptance Criteria**:
  - Six columns for each workflow stage
  - Cards display task titles and current substage
  - Automatic progression between stages
  - Responsive design for different screen sizes
- **Dependencies**: Feature 1.1
- **Estimated Complexity**: Medium

#### Feature 1.3: Task Input Interface
- **Description**: GitHub issues-style input for creating new workflow tasks
- **User Story**: As a developer, I want to input task descriptions using a rich interface so that AI agents can understand and process my requirements
- **Acceptance Criteria**:
  - Rich text input with markdown support
  - Image paste and basic annotation capabilities
  - Task type classification (feature, bug, chore, patch)
  - Auto-generated titles based on AI analysis
- **Dependencies**: Feature 1.2
- **Estimated Complexity**: High

#### Feature 1.4: SQLite Data Persistence
- **Description**: Local SQLite database for storing workflow data and state
- **User Story**: As a user, I want my workflow data to persist between sessions so that I don't lose progress
- **Acceptance Criteria**:
  - SQLite schema for projects, workflows, tasks, and logs
  - CRUD operations for all entities
  - Database migration support
  - Data export capabilities
- **Dependencies**: None
- **Estimated Complexity**: Medium

### Phase 2: Core Features

#### Feature 2.1: ADW Integration System
- **Description**: Discovery and execution of AI Developer Workflows from `agentics/adws/` directory
- **User Story**: As a developer, I want to trigger custom ADW scripts so that I can leverage AI automation for my specific project needs
- **Acceptance Criteria**:
  - Auto-discovery of available ADW scripts
  - Pipeline selection interface (plan-build, plan-build-document, etc.)
  - ADW execution with real-time progress tracking
  - Integration with existing `.claude/commands` system
- **Dependencies**: Features 1.1, 1.2, 1.4
- **Estimated Complexity**: High

#### Feature 2.2: Substage Progress Visualization
- **Description**: Detailed progress tracking within each main workflow stage
- **User Story**: As a user, I want to see detailed progress within each stage so that I can understand exactly where my workflow currently stands
- **Acceptance Criteria**:
  - Visual indicators for substages (initialize, classify, branch, generate, commit for Plan stage)
  - Progress bars and status indicators
  - Estimated time remaining for current substage
  - Error highlighting for failed substages
- **Dependencies**: Feature 2.1
- **Estimated Complexity**: Medium

#### Feature 2.3: Comprehensive Logging System
- **Description**: Centralized logging with LLM-readable format for easy agent interpretation
- **User Story**: As a developer, I want to view detailed logs of all workflow activities so that I can debug issues and understand agent decisions
- **Acceptance Criteria**:
  - Structured JSON logging format
  - Log aggregation from sub-agents
  - Searchable and filterable log interface
  - Error categorization and linking to ADW context
- **Dependencies**: Feature 2.1
- **Estimated Complexity**: Medium

#### Feature 2.4: Slash Command Integration
- **Description**: Integration with existing `.claude/commands` slash command system
- **User Story**: As a developer, I want to trigger slash commands from the Kanban interface so that I can execute specific operations without leaving the workflow view
- **Acceptance Criteria**:
  - Command palette interface for slash command discovery
  - Parameter input forms for command arguments
  - Command execution status and result display
  - Integration with workflow stage progression
- **Dependencies**: Features 2.1, 2.3
- **Estimated Complexity**: High

### Phase 3: Advanced Features

#### Feature 3.1: Sub-Agent Monitoring System
- **Description**: Autonomous frontend and backend monitoring agents during Build, Test, Review stages
- **User Story**: As a developer, I want sub-agents to monitor my build and test processes so that I can receive real-time feedback without manual oversight
- **Acceptance Criteria**:
  - Frontend sub-agent for monitoring client builds/tests
  - Backend sub-agent for monitoring server builds/tests
  - Real-time error reporting to main ADW
  - Sub-agent lifecycle management (start/stop/restart)
- **Dependencies**: Features 2.1, 2.3
- **Estimated Complexity**: High

#### Feature 3.2: Advanced Rich Text Editor
- **Description**: Enhanced TipTap editor with full multimedia support and annotation tools
- **User Story**: As a user, I want to create rich task descriptions with images, annotations, and markup so that I can provide comprehensive context to AI agents
- **Acceptance Criteria**:
  - Image paste, crop, and annotation tools
  - Drawing and markup capabilities
  - Multi-media input support (audio notes, video)
  - Collaborative editing features
- **Dependencies**: Feature 1.3
- **Estimated Complexity**: High

#### Feature 3.3: CodeRabbit Integration
- **Description**: Automated code review integration during Review stage
- **User Story**: As a developer, I want automated code review feedback so that I can improve code quality without manual review overhead
- **Acceptance Criteria**:
  - CodeRabbit API integration
  - Automated review trigger during Review stage
  - Feedback incorporation into workflow
  - Issue tracking and linking to ADW context
- **Dependencies**: Features 2.1, 2.2
- **Estimated Complexity**: Medium

#### Feature 3.4: Error Recovery and Feedback Loop
- **Description**: Intelligent error handling with automatic replanning capabilities
- **User Story**: As a developer, I want the system to automatically handle errors and replan workflows so that I can recover from failures without manual intervention
- **Acceptance Criteria**:
  - Error detection and classification
  - Automatic trigger of replanning workflows
  - Feedback loop integration with main ADW
  - Error history and pattern recognition
- **Dependencies**: Features 2.1, 2.3, 3.1
- **Estimated Complexity**: High

## Implementation Roadmap
### Development Sequence
1. **Foundation Setup**: Begin with project selection and basic Kanban layout to establish core infrastructure
2. **Data Layer**: Implement SQLite persistence to ensure reliable data storage before adding complex features
3. **Task Management**: Build task input interface and basic workflow progression
4. **ADW Integration**: Connect with existing AI workflows to enable core automation
5. **Monitoring & Logging**: Add comprehensive logging and progress tracking
6. **Advanced Features**: Implement sub-agent monitoring and advanced editor capabilities
7. **Quality & Recovery**: Add CodeRabbit integration and error recovery systems

### Milestone Definitions
#### Milestone 1: Basic Kanban MVP
- **Target**: Functional Kanban board with project selection and task management
- **Features Included**: 1.1, 1.2, 1.3, 1.4
- **Success Criteria**:
  - Can select projects and create tasks
  - Basic workflow visualization works
  - Data persists between sessions
  - E2E test for core functionality passes

#### Milestone 2: AI Integration Core
- **Target**: Full ADW integration with progress tracking and logging
- **Features Included**: 2.1, 2.2, 2.3, 2.4
- **Success Criteria**:
  - ADW scripts execute successfully
  - Real-time progress tracking works
  - Comprehensive logging system operational
  - Slash commands integrate seamlessly

#### Milestone 3: Advanced Monitoring
- **Target**: Sub-agent monitoring and enhanced user experience
- **Features Included**: 3.1, 3.2, 3.3, 3.4
- **Success Criteria**:
  - Sub-agents monitor builds/tests autonomously
  - Rich editor supports full multimedia workflow
  - CodeRabbit reviews integrate automatically
  - Error recovery system handles common failures

## Risk Assessment
### Technical Risks
- **SQLite Concurrency**: Risk of database locks during concurrent ADW executions
  - *Mitigation*: Implement connection pooling and retry logic
- **Sub-Agent Communication**: Complex inter-process communication between monitoring agents
  - *Mitigation*: Use established messaging patterns and comprehensive error handling
- **React State Management**: Complex state synchronization between UI and background processes
  - *Mitigation*: Use Zustand with middleware for persistence and debugging

### Project Risks
- **Scope Creep**: Tendency to add more AI features than necessary
  - *Mitigation*: Strict adherence to phase-based delivery and MVP principles
- **Integration Complexity**: Existing `.claude/commands` may require modifications
  - *Mitigation*: Design for minimal changes to existing command structure
- **Performance**: Large projects with many workflows may impact UI responsiveness
  - *Mitigation*: Implement virtual scrolling and lazy loading for large datasets

## Testing Strategy
### Overall Testing Approach
- **Unit Tests**: Jest/Vitest for React components and utility functions
- **Integration Tests**: API endpoint testing with test database
- **E2E Tests**: Playwright tests following `.claude/commands/e2e/` patterns
- **Manual Testing**: User workflow validation for each milestone

### Feature Testing Requirements
- **UI Components**: Component testing with user interaction simulation
- **ADW Integration**: Mock ADW executions for predictable testing
- **Database Operations**: Transaction testing with rollback capabilities
- **Sub-Agent Communication**: Message passing and error handling validation

## Validation Commands for Each Phase
### Phase 1 Validation
- `cd app/server && uv run pytest` - Run server tests
- `cd app/client && bun tsc --noEmit` - Run frontend type checking
- `cd app/client && bun run build` - Run frontend build
- `cd app/client && bun run test` - Run frontend unit tests
- `.claude/commands/test_e2e.md e2e/test_project_selection.md` - E2E test for project selection

### Phase 2 Validation
- `cd app/server && uv run pytest` - Run server tests
- `cd app/client && bun tsc --noEmit` - Run frontend type checking
- `cd app/client && bun run build` - Run frontend build
- `cd app/client && bun run test` - Run frontend unit tests
- `.claude/commands/test_e2e.md e2e/test_adw_integration.md` - E2E test for ADW execution
- `.claude/commands/test_e2e.md e2e/test_progress_tracking.md` - E2E test for progress visualization

### Phase 3 Validation
- `cd app/server && uv run pytest` - Run server tests
- `cd app/client && bun tsc --noEmit` - Run frontend type checking
- `cd app/client && bun run build` - Run frontend build
- `cd app/client && bun run test` - Run frontend unit tests
- `.claude/commands/test_e2e.md e2e/test_sub_agent_monitoring.md` - E2E test for sub-agent system
- `.claude/commands/test_e2e.md e2e/test_error_recovery.md` - E2E test for error handling

## Next Steps
1. **Create Individual Feature Plans**: Use `/feature` command to create detailed plans for each feature starting with Phase 1
2. **Set Up Project Infrastructure**: Create `app/client` and `app/server` directories with initial configurations
3. **Begin Phase 1 Implementation**: Start with Feature 1.1 (Project Selection Interface) as it provides the foundation for all other features

## Notes
- **Technology Dependencies**: Will require TipTap editor, Playwright for E2E testing, FastAPI for backend
- **Claude Code Integration**: Designed to work seamlessly with existing command structure without requiring modifications
- **Scalability Considerations**: Architecture supports adding new ADW types and workflow stages in future iterations
- **Multi-Project Support**: Core design principle - one Kanban app works with any project containing required directory structure
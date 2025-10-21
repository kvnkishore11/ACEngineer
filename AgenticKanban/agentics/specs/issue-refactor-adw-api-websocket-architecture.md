# Feature: API + WebSocket Architecture Refactor

## Metadata
issue_number: `refactor-001`
adw_id: `adw_api_websocket_refactor_${Date.now()}`
issue_json: `{"title": "Refactor File-Based ADW System to API + WebSocket Architecture", "body": "Replace the current file-based polling system (File System Access API + trigger files + 2-second polling) with a modern API + WebSocket architecture for immediate response and real-time updates."}`

## Feature Description

This refactor transforms the current file-based polling ADW (Agentic Data Workflow) system into a modern, efficient API + WebSocket architecture. The current system relies on File System Access API to write trigger files, followed by 2-second polling cycles, creating performance bottlenecks and user experience issues. The new architecture provides immediate HTTP API responses (<100ms) with real-time WebSocket updates, eliminating polling delays and improving reliability.

## User Story

As a developer using the AgenticKanban board
I want instant feedback when creating tasks and real-time progress updates
So that I can work efficiently without waiting for 2+ second polling delays and get immediate validation of my task submissions

## Problem Statement

The current file-based system has critical architectural flaws:

**Performance Issues:**
- 2-second minimum delay for any task feedback
- Continuous file I/O operations waste CPU cycles
- File system operations slower than in-memory communication
- Poor scalability - more tasks = more file monitoring overhead

**Reliability Problems:**
- File write/read race conditions
- No guarantee orchestrator is running when files are written
- File permission issues can silently break the system
- No immediate error feedback if orchestrator is down

**User Experience Problems:**
- Artificial delays in task creation and updates
- No immediate validation of task submission
- Users don't know if the system is working properly

## Solution Statement

Implement a FastAPI + WebSocket architecture that:

1. **Immediate API Response**: HTTP POST endpoints return task status within 100ms
2. **Real-time Updates**: WebSocket connections stream progress, logs, and status changes
3. **Background Processing**: Async task queue replaces file polling
4. **Database Persistence**: SQLite storage replaces scattered JSON files
5. **Backwards Compatibility**: Maintain existing ADW orchestrator as fallback

## Relevant Files

Use these files to implement the feature:

**Current Implementation to Refactor:**
- `src/stores/kanbanStore.js` - Contains file-based task creation and polling logic (lines 334-633)
- `src/utils/workflowExecutor.js` - File System Access API execution logic that needs API replacement
- `src/utils/commandGenerator.js` - Polling and file-based state management to be replaced with WebSocket
- `agentics/adws/adw_orchestrator.py` - Current file-based orchestrator (will become fallback)

**Frontend Files to Update:**
- `src/components/ProjectSelector.jsx` - May need updates for API endpoint configuration
- `src/components/TaskInput.jsx` - Task creation UI that triggers API calls
- `src/components/CommandDisplay.jsx` - Manual fallback display component
- `src/components/ExecutionStatus.jsx` - Real-time status display via WebSocket
- `src/App.jsx` - Main app component for WebSocket connection management

**Configuration and Dependencies:**
- `package.json` - Need to add WebSocket client dependencies
- `agentics/adws/requirements.txt` - Need FastAPI, WebSocket, SQLite dependencies

**Read conditional documentation:**
- `README.md` - Project structure and commands
- `agentics/adws/README.md` - Current ADW system architecture

### New Files

**Backend API Server:**
- `app/server/main.py` - FastAPI application entry point
- `app/server/core/api.py` - API endpoint definitions
- `app/server/core/websocket.py` - WebSocket connection management
- `app/server/core/orchestrator.py` - Background task orchestration
- `app/server/core/database.py` - SQLite database models and operations
- `app/server/core/models.py` - Pydantic data models
- `app/server/requirements.txt` - Python dependencies

**Frontend API Integration:**
- `src/services/apiService.js` - HTTP API client wrapper
- `src/services/websocketService.js` - WebSocket connection management
- `src/hooks/useWebSocket.js` - React hook for WebSocket integration

**Testing:**
- `.claude/commands/e2e/test_api_websocket_integration.md` - E2E test for new architecture

## Implementation Plan

### Phase 1: Foundation
Set up the basic FastAPI server structure with core endpoints and database models. Create the HTTP API interface that will replace file-based task creation, ensuring immediate response times and proper error handling.

### Phase 2: Core Implementation
Implement the WebSocket system for real-time updates and integrate background task processing. Replace the file-based orchestrator with an async task queue system that can execute ADW workflows efficiently.

### Phase 3: Integration
Update the React frontend to use the new API instead of File System Access API. Implement WebSocket connections for real-time updates and maintain backwards compatibility with the existing ADW orchestrator as a fallback option.

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### Backend API Development

#### Create FastAPI Server Structure
- Set up FastAPI application in `app/server/main.py`
- Configure CORS for frontend integration
- Add basic health check endpoint
- Set up SQLite database with SQLAlchemy models
- Create Pydantic models for request/response validation

#### Implement Core API Endpoints
- `POST /api/v1/workflows/create` - Task creation with immediate validation
- `GET /api/v1/workflows/{adw_id}` - Task status retrieval
- `PUT /api/v1/workflows/{adw_id}/status` - Manual status updates
- `DELETE /api/v1/workflows/{adw_id}` - Task cancellation
- Implement proper HTTP status codes and error responses

#### WebSocket Implementation
- Create WebSocket endpoint at `/ws/workflows/{adw_id}`
- Implement connection management with proper cleanup
- Create message broadcasting system for task updates
- Add WebSocket authentication and validation

#### Background Task Processing
- Replace file-based orchestrator with async task queue
- Implement background workers for ADW pipeline execution
- Create task state management with database persistence
- Add retry logic and error handling for failed tasks

### Frontend Refactoring

#### API Service Layer
- Create `src/services/apiService.js` with HTTP client functions
- Implement error handling and retry logic
- Add request/response interceptors for logging
- Create TypeScript types for API responses

#### WebSocket Integration
- Create `src/services/websocketService.js` for connection management
- Implement `src/hooks/useWebSocket.js` React hook
- Add automatic reconnection logic
- Handle connection state management

#### Store Refactoring
- Update `src/stores/kanbanStore.js` to use API instead of File System Access
- Replace file polling with WebSocket event handling
- Remove file-based execution functions
- Maintain existing state structure for UI compatibility

#### Component Updates
- Update task creation flow in `TaskInput.jsx` to use API
- Modify `ExecutionStatus.jsx` for WebSocket-based updates
- Update `ProjectSelector.jsx` for API endpoint configuration
- Ensure `CommandDisplay.jsx` works for manual fallback scenarios

### Testing and Validation

#### Create E2E Test
- Create `.claude/commands/e2e/test_api_websocket_integration.md`
- Test complete task creation → API call → WebSocket updates flow
- Validate real-time progress updates and completion notifications
- Test error scenarios and fallback mechanisms

#### Unit Testing
- Add tests for API endpoints with various input scenarios
- Test WebSocket connection handling and message broadcasting
- Test background task processing and state management
- Validate backwards compatibility with existing ADW orchestrator

#### Integration Testing
- Test complete frontend-to-backend integration
- Validate database persistence and state recovery
- Test concurrent task execution scenarios
- Performance testing to ensure <100ms API response times

### Final Integration and Cleanup

#### Backwards Compatibility
- Ensure existing `agentics/adws/adw_orchestrator.py` works as fallback
- Maintain existing file format compatibility for external tools
- Add configuration option to choose between API and file-based modes

#### Documentation Updates
- Update `agentics/adws/README.md` with new API architecture
- Add API documentation with endpoint specifications
- Update frontend documentation for new service layer

#### Performance Optimization
- Add database indexing for common queries
- Implement connection pooling for WebSocket management
- Add caching layer for frequently accessed task data
- Monitor and optimize API response times

### Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && python -m pytest tests/` - Run backend API tests
- `cd app/server && python main.py --test-mode` - Start API server in test mode
- `curl -X POST http://localhost:8000/api/v1/workflows/create -H "Content-Type: application/json" -d '{"title":"Test","description":"Test task","type":"feature","stages":["plan","implement"]}'` - Test API endpoint
- Read `.claude/commands/e2e/test_api_websocket_integration.md`, then execute the E2E test to validate real-time functionality
- `cd /Users/kvnkishore/WebstormProjects/AgenticEngineer/AgenticKanban && npm test` - Run frontend tests
- `cd /Users/kvnkishore/WebstormProjects/AgenticEngineer/AgenticKanban && npm run build` - Validate frontend builds successfully
- `cd app/server && python -c "import websockets; print('WebSocket support available')"` - Verify WebSocket dependencies
- Test WebSocket connection: `wscat -c ws://localhost:8000/ws/workflows/test` - Validate WebSocket connectivity

## Testing Strategy

### Unit Tests
- **API Endpoints**: Test all CRUD operations with valid/invalid inputs
- **WebSocket Connections**: Test connection establishment, message handling, cleanup
- **Background Processing**: Test task queue operations, retry logic, error handling
- **Database Operations**: Test task persistence, state management, concurrent access
- **Frontend Services**: Test API service calls, WebSocket hook behavior

### Edge Cases
- **Network Failures**: Test API timeout handling and WebSocket reconnection
- **Concurrent Tasks**: Test multiple simultaneous task executions
- **Database Corruption**: Test recovery from invalid state data
- **WebSocket Disconnection**: Test automatic reconnection and state synchronization
- **File System Fallback**: Test backwards compatibility when API unavailable
- **Invalid Task Data**: Test validation and error handling for malformed requests

## Acceptance Criteria

1. **Performance**: Task creation API responds within 100ms
2. **Real-time Updates**: WebSocket delivers progress updates within 500ms
3. **Reliability**: Zero file permission or race condition errors
4. **Backwards Compatibility**: Existing ADW orchestrator continues to work as fallback
5. **Error Handling**: Immediate feedback for invalid task submissions
6. **Scalability**: System handles 10+ concurrent tasks without performance degradation
7. **Data Persistence**: All task data survives server restarts
8. **UI Responsiveness**: No artificial 2-second delays in task operations
9. **WebSocket Stability**: Automatic reconnection after network interruptions
10. **API Documentation**: Complete OpenAPI specification available at `/docs`

## Validation Commands

Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd /Users/kvnkishore/WebstormProjects/AgenticEngineer/AgenticKanban && bun tsc --noEmit` - Run frontend type checking
- `cd /Users/kvnkishore/WebstormProjects/AgenticEngineer/AgenticKanban && bun run build` - Run frontend build to validate the feature works with zero regressions
- `cd app/server && python main.py &` - Start API server in background
- `curl -f http://localhost:8000/health` - Validate API server health
- `wscat -c ws://localhost:8000/ws/workflows/test` - Test WebSocket connectivity
- Read `.claude/commands/test_e2e.md`, then read and execute the E2E test file `.claude/commands/e2e/test_api_websocket_integration.md` to validate this functionality works
- `cd agentics/adws && python adw_orchestrator.py --test` - Validate backwards compatibility

## Notes

**Critical Architecture Decision**: This refactor maintains the existing ADW pipeline execution logic while replacing only the communication layer. The core orchestration, planning, implementation, and testing pipelines remain unchanged, ensuring minimal risk to existing functionality.

**Migration Strategy**: The system will support both API and file-based modes during transition. Users can configure which mode to use, allowing gradual migration and easy rollback if issues arise.

**WebSocket Considerations**: Implement proper connection pooling and cleanup to handle browser refreshes and network interruptions gracefully. Include heartbeat mechanism to detect stale connections.

**Database Choice**: SQLite chosen for simplicity and zero-configuration deployment. Can be easily upgraded to PostgreSQL for production scaling if needed.

**Security**: API endpoints include request validation, rate limiting, and proper error handling. WebSocket connections include authentication and message validation.

**Performance Monitoring**: Add metrics collection for API response times, WebSocket message latency, and task execution performance to ensure the system meets performance requirements.
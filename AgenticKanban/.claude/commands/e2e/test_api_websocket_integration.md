# E2E Test: API + WebSocket Integration

## Test Description
This end-to-end test validates the complete API + WebSocket architecture refactor functionality, ensuring that task creation, real-time updates, and workflow execution work correctly with zero regressions.

## Prerequisites
1. FastAPI server running on http://localhost:8000
2. Frontend development server running on http://localhost:3000 or http://localhost:5173
3. SQLite database initialized
4. WebSocket endpoints accessible

## Test Setup Commands

### 1. Start Backend API Server
```bash
cd app/server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 2. Start Frontend Development Server
```bash
cd /Users/kvnkishore/WebstormProjects/AgenticEngineer/AgenticKanban
npm install
npm run dev
```

### 3. Verify API Health
```bash
curl -f http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "AgenticKanban API",
  "version": "1.0.0"
}
```

## Core Integration Tests

### Test 1: API Endpoint Functionality

#### 1.1 Create Workflow Task via API
```bash
curl -X POST http://localhost:8000/api/v1/workflows/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "E2E Test Task",
    "description": "Testing API + WebSocket integration",
    "task_type": "feature",
    "stages": ["plan", "implement", "test"]
  }'
```

**Expected Result:**
- HTTP 201 status code
- Response contains `adw_id`, `id`, `title`, `description`, `task_type`, `status`, `stages`
- `status` should be "pending"
- `adw_id` should match pattern `adw_feature_\d+_[a-f0-9]{8}`

#### 1.2 Retrieve Task by ADW ID
```bash
# Replace {adw_id} with actual ADW ID from previous response
curl -X GET http://localhost:8000/api/v1/workflows/{adw_id}
```

**Expected Result:**
- HTTP 200 status code
- Complete task data returned
- Status updated to "running" (orchestrator should have picked it up)

#### 1.3 List All Workflows
```bash
curl -X GET http://localhost:8000/api/v1/workflows
```

**Expected Result:**
- HTTP 200 status code
- JSON with `tasks`, `total`, `page`, `per_page` fields
- Created task should be in the list

### Test 2: WebSocket Real-time Updates

#### 2.1 Connect to Workflow WebSocket
```bash
# Install wscat if not available: npm install -g wscat
wscat -c ws://localhost:8000/ws/workflows/{adw_id}
```

**Expected Result:**
- Connection established successfully
- Receive connection confirmation message:
```json
{
  "type": "connection_established",
  "adw_id": "{adw_id}",
  "message": "Connected to workflow {adw_id}"
}
```

#### 2.2 Verify Real-time Updates
While WebSocket connection is open, the orchestrator should send progress updates:

**Expected Messages:**
1. **Task Created:**
```json
{
  "type": "task_created",
  "data": {
    "adw_id": "{adw_id}",
    "status": "pending"
  }
}
```

2. **Status Updates:**
```json
{
  "type": "status_update",
  "data": {
    "adw_id": "{adw_id}",
    "status": "running",
    "current_stage": "plan"
  }
}
```

3. **Stage Updates:**
```json
{
  "type": "stage_update",
  "data": {
    "adw_id": "{adw_id}",
    "current_stage": "implement"
  }
}
```

4. **Progress Updates:**
```json
{
  "type": "progress_update",
  "data": {
    "adw_id": "{adw_id}",
    "stage": "plan",
    "progress": 33,
    "stage_result": {
      "plan_created": true
    }
  }
}
```

#### 2.3 Test WebSocket Ping/Pong
Send ping message:
```json
{"type": "ping", "timestamp": "2024-01-01T00:00:00Z"}
```

**Expected Response:**
```json
{"type": "pong", "timestamp": "2024-01-01T00:00:00Z"}
```

### Test 3: Frontend Integration

#### 3.1 Task Creation Flow
1. Open browser to http://localhost:3000 or http://localhost:5173
2. Create a new task with:
   - Title: "E2E Frontend Test"
   - Description: "Testing frontend API integration"
   - Type: "feature"
   - Stages: ["plan", "implement", "test"]

**Expected Behavior:**
- Task appears in Kanban board immediately
- No artificial 2-second delay
- Task shows "API" execution mode indicator
- WebSocket connection established indicator visible

#### 3.2 Real-time Progress Updates
1. Monitor the created task in the UI
2. Open ExecutionStatus modal

**Expected Behavior:**
- WebSocket connection status shows "Real-time updates connected"
- Progress bar updates in real-time (not simulated)
- Stage changes reflected immediately
- Log messages appear as they're received
- No polling delays

#### 3.3 Error Handling
1. Stop the API server while frontend is running
2. Try to create a new task

**Expected Behavior:**
- Frontend gracefully falls back to file-based system
- Error message displayed to user
- No crashes or unhandled errors
- System continues to function in fallback mode

### Test 4: Performance Validation

#### 4.1 API Response Time
Measure API response times:
```bash
time curl -X POST http://localhost:8000/api/v1/workflows/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Performance Test",
    "description": "Testing response time",
    "task_type": "feature",
    "stages": ["plan"]
  }'
```

**Expected Result:**
- Response time < 100ms
- No timeout errors

#### 4.2 WebSocket Message Latency
1. Connect to WebSocket
2. Trigger task updates
3. Measure time from API call to WebSocket message receipt

**Expected Result:**
- WebSocket messages received within 500ms of API updates
- No missed or duplicate messages

### Test 5: Concurrent Operations

#### 5.1 Multiple Simultaneous Tasks
Create 5 tasks simultaneously:
```bash
for i in {1..5}; do
  curl -X POST http://localhost:8000/api/v1/workflows/create \
    -H "Content-Type: application/json" \
    -d "{
      \"title\": \"Concurrent Test $i\",
      \"description\": \"Testing concurrent execution\",
      \"task_type\": \"feature\",
      \"stages\": [\"plan\", \"implement\"]
    }" &
done
wait
```

**Expected Result:**
- All 5 tasks created successfully
- No database conflicts or race conditions
- Each task gets unique ADW ID
- All tasks process independently

#### 5.2 Multiple WebSocket Connections
Connect to multiple workflow WebSockets simultaneously:
```bash
# In separate terminals
wscat -c ws://localhost:8000/ws/workflows/{adw_id_1}
wscat -c ws://localhost:8000/ws/workflows/{adw_id_2}
wscat -c ws://localhost:8000/ws/global
```

**Expected Result:**
- All connections established successfully
- Each receives appropriate messages
- No connection interference

### Test 6: Database Persistence

#### 6.1 Data Survival After Server Restart
1. Create several tasks via API
2. Stop and restart the API server
3. Query tasks again

**Expected Result:**
- All task data persists
- Database integrity maintained
- Tasks resume processing after restart

#### 6.2 WebSocket Reconnection
1. Establish WebSocket connection
2. Restart API server
3. Observe frontend behavior

**Expected Result:**
- WebSocket automatically reconnects
- No data loss
- Seamless user experience

## Backwards Compatibility Tests

### Test 7: File-based Fallback

#### 7.1 API Unavailable Scenario
1. Stop API server
2. Create task through frontend
3. Verify file-based system activates

**Expected Result:**
- System automatically detects API unavailability
- Falls back to file-based execution
- No user intervention required
- Original functionality preserved

#### 7.2 Existing ADW Orchestrator
1. Verify existing `agentics/adws/adw_orchestrator.py` still works
2. Test manual execution mode

**Expected Result:**
- Existing orchestrator functions normally
- Manual commands still work
- No breaking changes to existing workflows

## Acceptance Criteria Validation

Verify all acceptance criteria from the specification:

1. **✓ Performance**: Task creation API responds within 100ms
2. **✓ Real-time Updates**: WebSocket delivers progress updates within 500ms
3. **✓ Reliability**: Zero file permission or race condition errors
4. **✓ Backwards Compatibility**: Existing ADW orchestrator continues to work as fallback
5. **✓ Error Handling**: Immediate feedback for invalid task submissions
6. **✓ Scalability**: System handles 10+ concurrent tasks without performance degradation
7. **✓ Data Persistence**: All task data survives server restarts
8. **✓ UI Responsiveness**: No artificial 2-second delays in task operations
9. **✓ WebSocket Stability**: Automatic reconnection after network interruptions
10. **✓ API Documentation**: Complete OpenAPI specification available at `/docs`

## Test Cleanup

After completing all tests:

```bash
# Stop servers
# Clean up test data
curl -X DELETE http://localhost:8000/api/v1/workflows/{adw_id}

# Verify cleanup
curl -X GET http://localhost:8000/api/v1/workflows
```

## Success Criteria

- ✅ All API endpoints respond correctly
- ✅ WebSocket connections establish and receive real-time updates
- ✅ Frontend integration works without polling delays
- ✅ Error handling gracefully degrades to file-based system
- ✅ Performance meets specified requirements (<100ms API, <500ms WebSocket)
- ✅ Concurrent operations work without conflicts
- ✅ Data persists across server restarts
- ✅ Backwards compatibility maintained
- ✅ Zero regressions in existing functionality

## Failure Investigation

If any test fails:

1. Check API server logs: `cd app/server && python main.py`
2. Check browser developer console for WebSocket errors
3. Verify database state: Check SQLite database contents
4. Review frontend network tab for API request/response details
5. Test individual components in isolation

## Additional Validation Commands

```bash
# Check database schema
cd app/server && python -c "from core.database import engine, Base; import asyncio; asyncio.run(Base.metadata.create_all(bind=engine.sync_engine))"

# Validate WebSocket dependencies
python -c "import websockets; print('WebSocket support available')"

# Test API documentation
curl http://localhost:8000/docs

# Validate frontend build
cd /Users/kvnkishore/WebstormProjects/AgenticEngineer/AgenticKanban && npm run build
```

This comprehensive E2E test ensures the API + WebSocket architecture refactor works correctly with all specified features and maintains backwards compatibility.
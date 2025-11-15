# Multi-Agent Orchestration System - Detailed Implementation Analysis

## Overview
The multi-agent orchestration system at `/Users/kvnkishore/WebstormProjects/multi-agent-orchestration/apps/orchestrator_3_stream` implements sophisticated features for:
1. **Detailed streaming from WebSockets** - Not just final states, but detailed stage-by-stage execution tracking
2. **UI-based code navigation** - Click on UI elements to open files in IDE and jump to specific lines
3. **File tracking and modification tracking** - Complete tracking of what files were touched/modified
4. **Session output and summary generation** - Automatic markdown summaries and session persistence

---

## 1. DETAILED STREAMING FROM WEBSOCKETS

### Architecture Pattern
The system implements a **three-phase logging pattern** with detailed event streaming at each phase:

```
Phase 1: PRE-EXECUTION → Log to DB → Broadcast via WebSocket
Phase 2: EXECUTION → Stream each block/hook event → Broadcast in real-time  
Phase 3: POST-EXECUTION → Update costs → Broadcast final state
```

### WebSocket Message Structure
**File:** `/Users/kvnkishore/WebstormProjects/multi-agent-orchestration/apps/orchestrator_3_stream/backend/modules/websocket_manager.py` (257 lines)

All WebSocket messages follow a standardized structure with typed events:

```python
# Core broadcast method
async def broadcast(self, data: dict, exclude: WebSocket = None):
    """
    Broadcast JSON data to all connected clients
    - Adds timestamp if not present
    - Logs event type
    - Handles disconnections gracefully
    """
    if "timestamp" not in data:
        data["timestamp"] = datetime.now().isoformat()
    # Send to all active connections
```

**15+ Specialized Broadcasting Methods:**
- `broadcast_agent_created` - When agents are created
- `broadcast_agent_updated` - When agent costs/tokens change
- `broadcast_agent_status_changed` - When agent status changes (idle→executing→idle)
- `broadcast_agent_log` - Hook events (PreToolUse, PostToolUse, etc.)
- `broadcast_agent_summary_update` - When AI-generated summaries are ready
- `broadcast_orchestrator_updated` - Orchestrator cost updates
- `broadcast_chat_stream` - Real-time chat response chunks
- `set_typing_indicator` - Show when orchestrator is thinking
- `broadcast_error` - Error conditions
- `broadcast_system_log` - System-level events

### Detailed Event Types in WebSocket Messages

**1. Agent Log Events (Most Detailed)**
```json
{
  "type": "agent_log",
  "timestamp": "2025-11-03T10:30:45.123Z",
  "log": {
    "id": "uuid-string",
    "agent_id": "agent-uuid",
    "agent_name": "Analyzer",
    "task_slug": "task_123",
    "entry_index": 5,
    "event_category": "hook",           // OR "response"
    "event_type": "PreToolUse",         // 6 hook types
    "content": "Using tool: Read",
    "summary": "Reading config.py to understand project structure",
    "payload": {
      "tool_name": "Read",
      "tool_input": {
        "file_path": "/path/to/file"
      },
      "tool_use_id": "tool_123"
    },
    "timestamp": "2025-11-03T10:30:45.123Z"
  }
}
```

**2. Hook Events (6 Types)**
File: `/Users/kvnkishore/WebstormProjects/multi-agent-orchestration/apps/orchestrator_3_stream/backend/modules/command_agent_hooks.py` (629 lines)

```python
# Hook Types:
1. PreToolUse   - Fired BEFORE tool execution
2. PostToolUse  - Fired AFTER tool execution (with results)
3. UserPrompt   - When agent receives new prompt
4. Stop         - When agent session stops
5. SubagentStop - When subagent stops
6. PreCompact   - Before message compacting

# Each hook:
- Captures event to database (agent_logs table)
- Broadcasts immediately via WebSocket
- Spawns async AI summarization
- Updates frontend in real-time
```

**3. Response Block Events (What happens DURING execution)**
```python
# During orchestrator execution, real-time events for:
- TextBlock      → Claude's text response (streamed)
- ThinkingBlock  → Claude's internal reasoning (streamed)
- ToolUseBlock   → Tool invocations (streamed)
- ResultMessage  → Tool results (streamed)

# Each block event:
message_type: "thinking_block" | "tool_use_block" | "orchestrator_chat"
content: [full block data]
timestamp: ISO8601
```

**4. Orchestrator Chat Events**
```json
{
  "type": "orchestrator_chat",
  "timestamp": "2025-11-03T10:30:45.123Z",
  "message": {
    "id": "chat-uuid",
    "sender_type": "orchestrator",
    "receiver_type": "user",
    "message": "I'll analyze this repository...",
    "metadata": {
      "type": "thinking|tool_use|text",
      "thinking": "Full thinking content if thinking block",
      "tool_name": "Tool name if tool_use",
      "tool_input": {...}
    },
    "created_at": "2025-11-03T10:30:45.123Z"
  }
}
```

### Implementation - Streaming During Execution
File: `/Users/kvnkishore/WebstormProjects/multi-agent-orchestration/apps/orchestrator_3_stream/backend/modules/orchestrator_service.py` (1009 lines)

```python
async def process_user_message(self, user_message: str, orchestrator_agent_id: str):
    """
    Three-phase streaming pattern:
    
    PHASE 1: PRE-EXECUTION
    - Insert user message to orchestrator_chat table
    - Broadcast "orchestrator_chat" event immediately
    
    PHASE 2: EXECUTION (where detailed streaming happens)
    - Query Claude SDK with pre/post tool hooks
    - As response blocks arrive:
      * TextBlock → broadcast "orchestrator_chat"
      * ThinkingBlock → broadcast "thinking_block" 
      * ToolUseBlock → broadcast "tool_use_block"
    - For each tool call:
      * PreToolUse hook → broadcast "agent_log" (orchestrator's tools)
      * Tool execution
      * PostToolUse hook → broadcast "agent_log"
    
    PHASE 3: POST-EXECUTION
    - Update orchestrator costs
    - Broadcast "orchestrator_updated"
    - Update session_id if new
    """
```

### Key Pattern: Hooks for Detailed Stage Tracking
File: `/Users/kvnkishore/WebstormProjects/multi-agent-orchestration/apps/orchestrator_3_stream/backend/modules/orchestrator_hooks.py` (168 lines)

```python
def create_orchestrator_pre_tool_hook(orchestrator_agent_id, logger, ws_manager):
    async def hook(input_data, tool_use_id, context):
        tool_name = input_data.get("tool_name")
        # IMMEDIATELY broadcast - don't wait for tool execution
        await ws_manager.broadcast_orchestrator_chat({
            "type": "tool_use",
            "tool_name": tool_name,
            "timestamp": datetime.now().isoformat()
        })
        return {}
    return hook
```

### Frontend: Real-time Event Routing
File: `/Users/kvnkishore/WebstormProjects/multi-agent-orchestration/apps/orchestrator_3_stream/frontend/src/stores/orchestratorStore.ts` (1005 lines)

```typescript
// 15+ Event Handlers in Pinia Store
connectWebSocket(wsUrl, {
  onAgentLog: (msg) => addAgentLogEvent(msg.log),
  onOrchestratorChat: (msg) => addOrchestratorChatEvent(msg.message),
  onThinkingBlock: (msg) => {
    addThinkingBlockEvent(msg.data)
    addThinkingToChatMessage(msg.data)  // Dual display
  },
  onToolUseBlock: (msg) => {
    addToolUseBlockEvent(msg.data)
    addToolUseToChatMessage(msg.data)   // Dual display
  },
  onAgentCreated: handleAgentCreated,
  onAgentUpdated: handleAgentUpdated,
  onAgentStatusChange: handleAgentStatusChange,
  // ... 8 more handlers
})

// Critical Pattern: Spread operator for Vue reactivity
function addEventStreamEntry(entry: EventStreamEntry) {
  eventStreamEntries.value = [...eventStreamEntries.value, entry]  // ✅ Reactive
}
```

---

## 2. UI-BASED CODE NAVIGATION & IDE INTEGRATION

### File Opening in IDE
File: `/Users/kvnkishore/WebstormProjects/multi-agent-orchestration/apps/orchestrator_3_stream/backend/main.py` (lines 315-385)

**Backend Implementation:**
```python
@app.post("/api/open-file")
async def open_file_in_ide(request: OpenFileRequest):
    """
    Open a file in the configured IDE (Cursor or VS Code).
    Uses subprocess to invoke IDE command.
    """
    if not config.IDE_ENABLED:
        return {"status": "error", "message": "IDE integration disabled"}
    
    file_path = request.file_path
    
    # Validate file exists
    if not os.path.exists(file_path):
        return {"status": "error", "message": f"File not found: {file_path}"}
    
    # Build IDE command (from config.IDE_COMMAND)
    full_command = [config.IDE_COMMAND, file_path]
    
    # Execute IDE command (Cursor, VS Code, etc.)
    result = subprocess.run(
        full_command,
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0:
        return {
            "status": "success",
            "message": f"Opened {file_path} in {config.IDE_COMMAND}",
            "file_path": file_path
        }
```

### Frontend: File Opening Service
File: `/Users/kvnkishore/WebstormProjects/multi-agent-orchestration/apps/orchestrator_3_stream/frontend/src/services/fileService.ts` (64 lines)

```typescript
export async function openFileInIDE(absolutePath: string): Promise<OpenFileResponse> {
  try {
    const response = await apiClient.post<OpenFileResponse>('/api/open-file', {
      file_path: absolutePath
    })
    
    if (response.data.status === 'success') {
      console.log(`[FileService] Opened file in IDE: ${absolutePath}`)
      return response.data
    }
  } catch (error: any) {
    return {
      status: 'error',
      message: error.response?.data?.message || error.message
    }
  }
}
```

### UI Integration: File Changes Display Component
File: `/Users/kvnkishore/WebstormProjects/multi-agent-orchestration/apps/orchestrator_3_stream/frontend/src/components/event-rows/FileChangesDisplay.vue` (858 lines)

**Key Features:**

1. **Click to Open Files in IDE**
```vue
<div
  v-for="file in fileChanges"
  @click="handleFileClick(file.absolute_path)"
  class="file-card"
>
  <div class="file-path">{{ file.path }}</div>
  <div class="file-badges">
    <span class="status-badge">✓ Created</span>
  </div>
</div>

<!-- Script -->
const handleFileClick = async (absolutePath: string) => {
  const result = await openFileInIDE(absolutePath)
  if (result.status === "success") {
    console.log("✓ File opened in IDE:", absolutePath)
  }
}
```

2. **Display File Modifications with Stats**
```vue
<!-- Show what changed -->
<div class="line-changes-summary">
  <span class="line-stats">
    <span class="added">+{{ file.lines_added }} Added</span>
    <span class="removed">-{{ file.lines_removed }} Removed</span>
  </span>
</div>

<!-- Show diff with expandable view -->
<div v-if="file.diff" class="diff-section">
  <button @click.stop="toggleDiff(file.path)">
    {{ expandedDiffs.has(file.path) ? "▼ Hide Diff" : "▶ Show Diff" }}
  </button>
  
  <div v-if="expandedDiffs.has(file.path)" class="diff-viewer">
    <pre><code v-html="formatDiff(file.diff)"></code></pre>
  </div>
</div>
```

3. **Diff Syntax Highlighting**
```vue
<style scoped>
/* Added lines (green) */
.diff-viewer :deep(.addition) {
  background-color: rgba(16, 185, 129, 0.2) !important;
  color: #4ede80 !important;
  border-left: 4px solid #22c55e !important;
}

/* Deleted lines (red) */
.diff-viewer :deep(.deletion) {
  background-color: rgba(239, 68, 68, 0.2) !important;
  color: #fca5a5 !important;
  border-left: 4px solid #dc2626 !important;
}

/* Chunk headers (blue) */
.diff-viewer :deep(.chunk-header) {
  background-color: rgba(59, 130, 246, 0.15) !important;
  color: #60a5fa !important;
}
```

### File Summary Generation
```typescript
const formatDiff = (diff: string | undefined): string => {
  if (!diff) return ""
  
  const lines = diff.split("\n")
  const formattedLines = lines.map((line) => {
    const escapedLine = escapeHtml(line)
    
    if (line.startsWith("+") && !line.startsWith("+++")) {
      return `<span class="addition">${escapedLine}</span>`
    }
    if (line.startsWith("-") && !line.startsWith("---")) {
      return `<span class="deletion">${escapedLine}</span>`
    }
    if (line.startsWith("@@")) {
      return `<span class="chunk-header">${escapedLine}</span>`
    }
    return escapedLine
  })
  
  return formattedLines.join("\n")
}
```

4. **Export File Activity**
```typescript
const exportFileActivity = () => {
  const exportData = {
    timestamp: new Date().toISOString(),
    file_changes: props.fileChanges,
    read_files: props.readFiles,
    summary: {
      total_files_modified: props.fileChanges.length,
      total_files_read: props.readFiles.length,
    },
  }
  
  const blob = new Blob([JSON.stringify(exportData, null, 2)], {
    type: "application/json"
  })
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = `file-activity-${Date.now()}.json`
  a.click()
}
```

---

## 3. FILE TRACKING & MODIFICATION TRACKING

### FileTracker Implementation
File: `/Users/kvnkishore/WebstormProjects/multi-agent-orchestration/apps/orchestrator_3_stream/backend/modules/file_tracker.py` (285 lines)

**Purpose:** Track all file operations (reads, modifications) per agent during execution

```python
class FileTracker:
    """Tracks file operations for a single agent."""
    
    def __init__(self, agent_id: UUID, agent_name: str, working_dir: str):
        self.agent_id = str(agent_id)
        self.agent_name = agent_name
        self.working_dir = working_dir
        
        # Use sets to track unique file paths
        self.modified_files: Set[str] = set()
        self.read_files: Set[str] = set()
        
        # Store detailed info
        self._file_details: Dict[str, Dict[str, Any]] = {}
    
    def track_modified_file(self, tool_name: str, tool_input: Dict[str, Any]):
        """Record a file modification from a tool."""
        file_path = tool_input.get("file_path")
        if not file_path:
            return
        
        self.modified_files.add(file_path)
        
        # Store tool info for later summary generation
        if file_path not in self._file_details:
            self._file_details[file_path] = {
                "tool_name": tool_name,
                "tool_input": tool_input
            }
    
    def track_read_file(self, file_path: str):
        """Record a file read operation."""
        if file_path:
            self.read_files.add(file_path)
```

### File Change Summary Generation
```python
async def generate_file_changes_summary(self) -> List[Dict[str, Any]]:
    """
    Generate comprehensive summary of file modifications with:
    - Diffs (git diff)
    - Stats (lines added/removed)
    - AI summaries (using fast_claude_query)
    - File status (created/modified/deleted)
    """
    file_changes = []
    
    for file_path in self.modified_files:
        # Get tool info
        tool_info = self._file_details.get(file_path, {})
        tool_name = tool_info.get("tool_name", "Unknown")
        
        # Resolve absolute path
        abs_path = GitUtils.resolve_absolute_path(file_path, self.working_dir)
        
        # Generate diff using git
        diff = GitUtils.get_file_diff(file_path, self.working_dir)
        
        # Parse stats
        lines_added, lines_removed = GitUtils.parse_diff_stats(diff)
        
        # Determine status
        status = GitUtils.get_file_status(file_path, self.working_dir)
        
        # Generate AI summary
        summary = await generate_file_change_summary(file_path, diff, tool_name)
        
        file_change = {
            "path": rel_path,
            "absolute_path": abs_path,
            "status": status,              # created|modified|deleted
            "lines_added": lines_added,
            "lines_removed": lines_removed,
            "diff": diff,                  # Full git diff
            "summary": summary,            # AI-generated summary
            "agent_id": self.agent_id,
            "agent_name": self.agent_name
        }
        
        file_changes.append(file_change)
    
    return file_changes
```

### AI-Powered File Change Summaries
```python
async def generate_file_change_summary(
    file_path: str,
    diff: Optional[str],
    tool_name: str
) -> str:
    """
    Generate AI summary for a file change using Claude Haiku (fast & cheap).
    """
    if not diff or not diff.strip():
        return f"{tool_name} operation on {os.path.basename(file_path)}"
    
    # Truncate diff if too large
    truncated_diff = (
        diff[:2000] + "\n[...truncated]" 
        if len(diff) > 2000 
        else diff
    )
    
    # Build details
    details = f"""File: {os.path.basename(file_path)}
Tool: {tool_name}
Diff (first 2000 chars):
{truncated_diff}"""
    
    # Use existing EVENT_SUMMARIZER_USER_PROMPT template
    prompt = EVENT_SUMMARIZER_USER_PROMPT.format(
        event_type="FileChange",
        details=details
    )
    
    # Query Claude Haiku for fast summary
    summary = await fast_claude_query(
        prompt, 
        system_prompt=EVENT_SUMMARIZER_SYSTEM_PROMPT
    )
    
    # Return summary (max 200 chars) or fallback
    return summary.strip()[:200] if summary else fallback_heuristic(diff)
```

### Integration with Agent Hooks
File: `/Users/kvnkishore/WebstormProjects/multi-agent-orchestration/apps/orchestrator_3_stream/backend/modules/command_agent_hooks.py` (629 lines)

```python
def create_post_tool_file_tracking_hook(...):
    """
    PostToolUse hook that tracks file modifications.
    Called AFTER every tool execution.
    """
    async def hook(input_data, tool_use_id, context):
        tool_name = input_data.get("tool_name", "unknown")
        tool_input = input_data.get("tool_input", {})
        
        # Track modifications for tools that modify files
        if tool_name in ["Write", "Edit", "MultiEdit", "Bash"]:
            file_tracker.track_modified_file(tool_name, tool_input)
        
        # Track reads for tools that read files
        if tool_name in ["Read"]:
            file_path = tool_input.get("file_path")
            file_tracker.track_read_file(file_path)
        
        return {}
    
    return hook
```

### Storage in Database
File: `/Users/kvnkishore/WebstormProjects/multi-agent-orchestration/apps/orchestrator_3_stream/backend/modules/database.py` (1600 lines)

```python
# agent_logs table - event_category='hook' stores file tracking data
agent_logs {
    id: UUID,
    agent_id: UUID FK,
    session_id: string,
    task_slug: string,
    entry_index: int,
    event_category: 'hook' | 'response',
    event_type: string,
    content: string,
    payload: JSONB,  # Contains file tracking data
    summary: string,  # AI-generated summary
    timestamp: datetime
}

# Payload structure for file tracking events:
{
    "event_type": "PostToolUse",
    "tool_name": "Write",
    "tool_input": {
        "file_path": "src/app.py",
        "content": "..."
    },
    "file_changes": [
        {
            "path": "src/app.py",
            "status": "modified",
            "lines_added": 45,
            "lines_removed": 12,
            "diff": "...",
            "summary": "Added error handling to request handler"
        }
    ]
}
```

---

## 4. SESSION OUTPUT & SUMMARY GENERATION

### Session Persistence
File: `/Users/kvnkishore/WebstormProjects/multi-agent-orchestration/apps/orchestrator_3_stream/backend/modules/database.py`

**Session Management:**
```python
# Each orchestrator session has:
- session_id: UUID (persistent identifier)
- working_dir: Path (working directory for agents)
- system_prompt: Full orchestrator system prompt
- metadata: JSONB containing:
  * system_message_info
  * captured_at
  * subtype: fallback|captured
```

### Multiple Output Formats

**1. JSON Export Files**
File: `/Users/kvnkishore/WebstormProjects/multi-agent-orchestration/apps/orchestrator_3_stream/frontend/src/components/event-rows/FileChangesDisplay.vue` (lines 310-329)

```typescript
const exportFileActivity = () => {
  const exportData = {
    timestamp: new Date().toISOString(),
    file_changes: props.fileChanges,
    read_files: props.readFiles,
    summary: {
      total_files_modified: props.fileChanges.length,
      total_files_read: props.readFiles.length,
    },
  }
  
  // Generate JSON file and trigger download
  const blob = new Blob([JSON.stringify(exportData, null, 2)], {
    type: "application/json"
  })
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = `file-activity-${Date.now()}.json`
  a.click()
}
```

**2. Markdown Documentation Files**
Path: `/Users/kvnkishore/WebstormProjects/multi-agent-orchestration/apps/orchestrator_3_stream/app_docs/`

Generated files:
- `full-stack-architecture-summary.md` - Complete system architecture
- `backend-structure-summary.md` - Backend components and modules
- `frontend-structure-summary.md` - Frontend components and services
- `backend-modules-reference.md` - Detailed API documentation
- `responsive-ui-implementation-report.md` - UI implementation details
- `BACKEND_DOCUMENTATION_INDEX.md` - Documentation index

**3. AI-Generated Summaries (Fast Claude Haiku)**
File: `/Users/kvnkishore/WebstormProjects/multi-agent-orchestration/apps/orchestrator_3_stream/backend/modules/single_agent_prompt.py` (285 lines)

```python
async def summarize_event(event_data: dict[str, Any], event_type: str) -> str:
    """
    Generate concise 1-sentence summary of agent events.
    Used for all agent_log.summary and chat.summary fields.
    
    Event types:
    - Hook types: PreToolUse, PostToolUse, UserPromptSubmit, Stop
    - Block types: text, thinking, tool_use, tool_result
    """
    
    # Build event description from event_data
    details = _format_event_details(event_data, event_type)
    
    # Use Haiku for fast, cost-effective summarization
    prompt = EVENT_SUMMARIZER_USER_PROMPT.format(
        event_type=event_type,
        details=details
    )
    
    summary = await fast_claude_query(
        prompt,
        system_prompt=EVENT_SUMMARIZER_SYSTEM_PROMPT
    )
    
    return summary.strip()[:200]  # Limit to 200 chars
```

### Generated Documentation Files

**Full Stack Architecture Summary:**
```markdown
# Orchestrator 3 Stream - Full-Stack Architecture Summary

**Date:** 2025-01-22
**Version:** 1.0

## Key System Nodes - Quick Reference

**Backend Layer:**
- FastAPI Backend (main.py): 646 lines
- WebSocket Manager: 257 lines
- Orchestrator Service: 1009 lines
- Agent Manager: 1397 lines
- Database Module: 1600 lines

**Frontend Layer:**
- Vue3 Frontend (App.vue): 3-column responsive layout
- Pinia Store (orchestratorStore.ts): 1005 lines
- Chat Service: 179 lines
- Event Service: HTTP client for /get_events

**Database:**
- PostgreSQL (NeonDB)
- 6 tables: orchestrator_agents, agents, agent_logs, etc.
- All append-only event logs

...generated automatically based on codebase analysis
```

### Database Summary Tables

Each execution generates records in:

```sql
-- orchestrator_chat: Chat history with summaries
SELECT id, sender_type, message, summary, created_at
FROM orchestrator_chat
WHERE orchestrator_agent_id = $1
ORDER BY created_at DESC;

-- agent_logs: All agent events with summaries
SELECT id, agent_id, event_type, content, summary, timestamp
FROM agent_logs
WHERE agent_id = $1
ORDER BY timestamp DESC;

-- agents: Agent registry with cumulative costs
SELECT id, name, model, status, input_tokens, output_tokens, total_cost
FROM agents
WHERE orchestrator_agent_id = $1;

-- system_logs: System-level events
SELECT id, level, message, summary, timestamp
FROM system_logs
ORDER BY timestamp DESC;
```

### Metadata Capture
```python
# orchestrator_agents.metadata JSONB field stores:
{
  "system_message_info": {
    "session_id": "uuid",
    "cwd": "/path/to/project",
    "captured_at": "2025-11-03T10:30:45.123Z",
    "subtype": "captured"  # OR "fallback"
  },
  "slash_commands": [
    {
      "name": "/help",
      "description": "Get help",
      "usage": "/help [command]"
    },
    // ... more commands
  ],
  "agent_templates": [
    {
      "name": "code-analyzer",
      "description": "Analyzes code patterns",
      "model": "claude-sonnet-4-5-20250929"
    },
    // ... more templates
  ]
}
```

---

## 5. KEY TECHNICAL PATTERNS

### Pattern 1: Three-Phase Logging
```
USER SENDS MESSAGE
  ↓
PHASE 1: PRE-EXECUTION
  • Insert to database
  • Broadcast via WebSocket
  • Return 202 Accepted to user immediately
  ↓
ASYNC TASK (Fire and forget)
PHASE 2: EXECUTION
  • Call Claude SDK
  • For each block/hook event:
    - Insert to database
    - Broadcast via WebSocket (real-time)
    - Trigger async summarization
  ↓
PHASE 3: POST-EXECUTION
  • Update costs
  • Update session_id
  • Broadcast final state
  ↓
FRONTEND (via WebSocket)
  • Real-time updates
  • Event routing to handlers
  • UI reactivity with Vue spreads
```

### Pattern 2: Fire-and-Forget AI Summarization
```python
# Don't wait for AI - let it complete in background
asyncio.create_task(
    self._summarize_and_update_chat(chat_id, message)
)

# Return immediately to user with partial data
# Summary arrives separately via WebSocket when ready
```

### Pattern 3: Vue Reactivity with Spread Operators
```typescript
// ❌ WRONG - Won't trigger reactivity during rapid updates
function addEventWrong(entry) {
  eventStreamEntries.value.push(entry)
}

// ✅ CORRECT - Creates new array, always reactive
function addEventStreamEntry(entry) {
  eventStreamEntries.value = [...eventStreamEntries.value, entry]
}
```

### Pattern 4: Dual-Display for Blocks
```typescript
// Thinking and tool blocks appear in TWO places:
onThinkingBlock: (message) => {
  addThinkingBlockEvent(message.data)      // Event stream
  addThinkingToChatMessage(message.data)   // Chat UI
}
```

### Pattern 5: File Tracking via Hooks
```python
# Track files automatically - no manual intervention needed
create_post_tool_hook() → captures tool execution
  → if tool is Write/Edit/Bash → track_modified_file()
  → if tool is Read → track_read_file()
  → generates summary with diff and AI analysis
```

---

## 6. FILES TOUCHED & MODIFIED

### Backend Modules (1600 total lines)
```
modules/
├── main.py                      (646 lines) - FastAPI app + WebSocket endpoint
├── database.py                  (1600 lines) - All DB operations
├── websocket_manager.py         (257 lines) - Broadcast hub
├── orchestrator_service.py      (1009 lines) - Orchestrator execution
├── agent_manager.py             (1397 lines) - Agent lifecycle + 8 tools
├── orchestrator_hooks.py        (168 lines) - Orchestrator event hooks
├── command_agent_hooks.py       (629 lines) - Agent event hooks (6 types)
├── single_agent_prompt.py       (285 lines) - Fast Claude summarization
├── file_tracker.py              (285 lines) - File operation tracking
├── orch_database_models.py      (344 lines) - Pydantic models
├── config.py                    (197 lines) - Environment config
├── logger.py                    (182 lines) - Rich logging
├── subagent_loader.py           (220 lines) - Template discovery
├── slash_command_parser.py      (267 lines) - Command discovery
└── event_summarizer.py          (lightweight wrapper)
```

### Frontend Components (Vue 3)
```
frontend/src/
├── App.vue                                    - Main 3-column layout
├── stores/orchestratorStore.ts  (1005 lines) - Pinia store + 15 handlers
├── components/
│   ├── EventStream.vue          (300 lines) - Live event log
│   ├── AgentList.vue            (250 lines) - Sidebar with pulse
│   ├── OrchestratorChat.vue     (265 lines) - Chat interface
│   ├── GlobalCommandInput.vue             - Command input
│   ├── AppHeader.vue                      - Header/stats
│   ├── FilterControls.vue                 - Event filtering
│   └── event-rows/
│       ├── FileChangesDisplay.vue (858 lines) - Click-to-open files
│       ├── AgentLogRow.vue
│       ├── OrchestratorChatRow.vue
│       ├── ToolUseBlockRow.vue
│       └── ... (more event types)
├── services/
│   ├── chatService.ts           (179 lines) - WebSocket + HTTP
│   ├── fileService.ts           (64 lines) - IDE integration
│   ├── eventService.ts          (42 lines) - Event fetching
│   ├── agentService.ts                    - Agent operations
│   └── api.ts                             - Axios config
└── composables/
    ├── useAgentPulse.ts                  - Animation manager
    ├── useEventStreamFilter.ts           - Event filtering
    └── ... (more utilities)
```

### Documentation Generated
```
app_docs/
├── full-stack-architecture-summary.md
├── backend-structure-summary.md
├── frontend-structure-summary.md
├── backend-modules-reference.md
├── responsive-ui-implementation-report.md
├── BACKEND_DOCUMENTATION_INDEX.md
├── BACKEND_QUICK_START.md
└── ... (13 total)
```

### Configuration & Schema
```
specs/
├── orchestrator-3-event-stream-ui-implementation.md
├── orchestrator-3-stream-chat-implementation.md
├── orchestrator-3-wire-command-agents-and-event-streaming.md
└── ... (10+ detailed specs)

backend/
└── prompts/
    ├── event_summarizer_system_prompt.md
    ├── event_summarizer_user_prompt.md
    └── orchestrator_system_prompt.md
```

---

## 7. OUTPUTS CREATED

### Runtime Outputs

**1. Database Records (PostgreSQL)**
- orchestrator_agents (1 per session)
- agents (1+ per session)
- agent_logs (100s-1000s per execution)
- orchestrator_chat (10-100 per interaction)
- system_logs (ongoing)
- prompts (1 per agent task)

**2. WebSocket Events (Real-time)**
- 15+ event types streamed to connected clients
- Each with JSON payload + timestamp
- Broadcast to all connected frontend clients simultaneously

**3. JSON Exports (On Demand)**
- File activity exports with full diffs
- Format: `file-activity-{timestamp}.json`
- Contains: changed files + read files + statistics

**4. Generated Summaries**
- agent_logs.summary (AI-generated, 1-sentence)
- orchestrator_chat.summary (AI-generated)
- system_logs.summary (AI-generated)
- Generated by fast_claude_query(Haiku) in background

**5. Documentation Files**
- auto-generated markdown files in app_docs/
- Full-stack architecture overviews
- Backend/frontend structure summaries
- Module-by-module references

---

## 8. MESSAGE FLOW EXAMPLE

```
User: "Analyze the codebase"
  ↓
Frontend: POST /send_chat with message
  ↓
Backend: 202 Accepted (immediate return)
  ↓
ASYNC Task Starts:
  1. Insert user message to orchestrator_chat
     • Broadcast "orchestrator_chat" event
  2. Query Claude SDK with orchestrator system prompt
  3. PreToolUse hook fires:
     • Insert hook event to orchestrator_chat
     • Broadcast "orchestrator_chat" (type: tool_use)
     • Async summarization task spawned
  4. Tool executes: create_agent("Analyzer")
     • AgentManager.create_agent() called
     • FileTracker initialized
     • Agent inserted to agents table
     • Broadcast "agent_created" event
  5. PostToolUse hook fires:
     • Insert hook event
     • Broadcast "agent_log"
  6. Claude responds with TextBlock:
     • Insert to orchestrator_chat
     • Broadcast "orchestrator_chat" (type: text)
     • Async summarization task spawned
  7. Claude responds with ThinkingBlock:
     • Broadcast "thinking_block"
     • Frontend adds to both event stream + chat UI
  8. PostToolUse: Update costs
     • Broadcast "orchestrator_updated"
     • Update session_id if new
  ↓
Frontend (via WebSocket):
  • receive "orchestrator_chat" → addOrchestratorChatEvent()
  • receive "agent_created" → handleAgentCreated()
  • receive "thinking_block" → addThinkingBlockEvent() + addThinkingToChatMessage()
  • UI updates in real-time
  ↓
User sees:
  • Chat interface updating live
  • New agent appearing in sidebar
  • Event stream growing
  • File activity widget showing changes
```

---

## 9. KEY CONFIGURATION

**Backend (.env)**
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/orch_db
ANTHROPIC_API_KEY=sk-ant-...
BACKEND_HOST=127.0.0.1
BACKEND_PORT=9403
ORCHESTRATOR_MODEL=claude-sonnet-4-5-20250929
ORCHESTRATOR_WORKING_DIR=/path/to/project
LOG_LEVEL=INFO
IDE_ENABLED=true
IDE_COMMAND=cursor  # OR code
```

**Frontend (.env)**
```bash
VITE_API_BASE_URL=http://127.0.0.1:9403
VITE_WEBSOCKET_URL=ws://127.0.0.1:9403/ws
FRONTEND_PORT=5175
```

---

## Summary of Implementation Patterns

| Feature | Implementation | Location |
|---------|---|---|
| **Detailed Streaming** | 15+ WebSocket event types + hooks (6 types) | websocket_manager.py, hooks files |
| **IDE Navigation** | POST /api/open-file endpoint + Vue click handler | main.py + FileChangesDisplay.vue |
| **File Tracking** | FileTracker class + PostToolUse hook integration | file_tracker.py + command_agent_hooks.py |
| **Session Persistence** | PostgreSQL with JSONB metadata + session_id | database.py + models |
| **AI Summaries** | fast_claude_query(Haiku) with background tasks | single_agent_prompt.py |
| **Documentation** | auto-generated markdown in app_docs/ | Generated during development |
| **UI Reactivity** | Spread operator pattern for Vue ref updates | orchestratorStore.ts |
| **Fire-and-Forget** | asyncio.create_task() for summarization | orchestrator_service.py |
| **Dual Display** | Same event in event stream + chat UI | orchestratorStore.ts handlers |


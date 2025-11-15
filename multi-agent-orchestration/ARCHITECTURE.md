# Multi-Agent Orchestration System - Architecture Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [WebSocket Architecture](#websocket-architecture)
3. [Log Flow: Backend → Frontend](#log-flow-backend--frontend)
4. [Frontend WebSocket Handling](#frontend-websocket-handling)
5. [Agent Orchestration Flow](#agent-orchestration-flow)
6. [Database Schema](#database-schema)
7. [Critical Components Reference](#critical-components-reference)

---

## System Overview

### High-Level Architecture

```mermaid
graph TB
    subgraph "Frontend - Vue 3 + TypeScript"
        UI[User Interface]
        Store[Pinia Store<br/>orchestratorStore.ts]
        WS_Client[WebSocket Client<br/>chatService.ts]
        HTTP_Client[HTTP Client<br/>Axios]
    end

    subgraph "Backend - FastAPI + Python"
        API[FastAPI Endpoints]
        WS_Server[WebSocket Server<br/>/ws endpoint]
        WS_Manager[WebSocketManager<br/>Broadcast Hub]
        Orch_Service[OrchestratorService<br/>Claude SDK Client]
        Agent_Manager[AgentManager<br/>8 Management Tools]
    end

    subgraph "Data Layer"
        DB[(PostgreSQL<br/>6 Tables)]
        Claude[Anthropic Claude API]
    end

    UI -->|User Messages| HTTP_Client
    UI <-->|Real-time Updates| WS_Client
    HTTP_Client -->|REST API| API
    WS_Client <-->|WebSocket Protocol| WS_Server

    WS_Server -->|Connection Management| WS_Manager
    API -->|Execute Commands| Orch_Service
    API -->|Manage Agents| Agent_Manager

    Orch_Service -->|Query LLM| Claude
    Agent_Manager -->|Query LLM| Claude

    Orch_Service -->|Store Events| DB
    Agent_Manager -->|Store Events| DB
    WS_Manager -->|Broadcast Events| WS_Server

    Store -->|Update Reactive State| UI
    WS_Server -->|Event Stream| WS_Client
    WS_Client -->|Route Events| Store

    style WS_Manager fill:#ff9999
    style WS_Server fill:#ff9999
    style WS_Client fill:#ff9999
    style Store fill:#99ccff
```

---

## WebSocket Architecture

### 1. WebSocket Manager Configuration

The WebSocketManager (`backend/modules/websocket_manager.py`) is the central hub for all real-time communication.

```mermaid
graph TB
    subgraph "WebSocketManager Class"
        Connections[Active Connections List<br/>List&lt;WebSocket&gt;]
        Metadata[Connection Metadata<br/>Dict&lt;WebSocket, ClientInfo&gt;]

        subgraph "Connection Lifecycle"
            Connect[connect&#40;websocket&#41;<br/>- Add to active list<br/>- Store metadata<br/>- Send welcome message]
            Disconnect[disconnect&#40;websocket&#41;<br/>- Remove from list<br/>- Clean metadata]
        end

        subgraph "Broadcast Methods"
            Generic[broadcast&#40;data, exclude&#41;<br/>Core broadcast with timestamp]
            Agent[Agent Events<br/>- agent_created<br/>- agent_updated<br/>- agent_deleted<br/>- agent_status_change<br/>- agent_log<br/>- agent_summary_update]
            Orch[Orchestrator Events<br/>- orchestrator_updated<br/>- chat_stream<br/>- typing_indicator]
            System[System Events<br/>- system_log<br/>- error]
        end
    end

    Connect --> Connections
    Connect --> Metadata
    Disconnect --> Connections
    Disconnect --> Metadata

    Agent --> Generic
    Orch --> Generic
    System --> Generic

    Generic -->|JSON Messages| WS_Clients[All Connected<br/>WebSocket Clients]

    style Generic fill:#ffcc99
    style Connections fill:#99ff99
    style Metadata fill:#99ff99
```

**Key Features:**
- **Connection Pool**: Maintains list of active WebSocket connections
- **Auto-cleanup**: Removes stale connections during broadcast
- **Timestamp Injection**: Adds ISO8601 timestamp to all events
- **Exclude Option**: Can exclude specific clients from broadcast

### 2. WebSocket Message Format

All WebSocket messages follow this standardized structure:

```mermaid
graph LR
    subgraph "WebSocket Message Structure"
        Base[Base Fields<br/>- type: string<br/>- timestamp: ISO8601]

        subgraph "Event-Specific Payloads"
            AgentLog[agent_log<br/>- log: AgentLogEvent<br/>- agent_id: UUID<br/>- event_type: string<br/>- content: string]

            OrchChat[orchestrator_chat<br/>- message: ChatMessage<br/>- sender_type: string<br/>- content: string<br/>- metadata: JSON]

            AgentStatus[agent_status_changed<br/>- agent_id: UUID<br/>- old_status: string<br/>- new_status: string]

            AgentUpdated[agent_updated<br/>- agent_id: UUID<br/>- costs: Costs<br/>- tokens: Tokens]
        end
    end

    Base --> AgentLog
    Base --> OrchChat
    Base --> AgentStatus
    Base --> AgentUpdated
```

**Example Message:**
```json
{
  "type": "agent_log",
  "timestamp": "2025-11-03T10:30:45.123Z",
  "log": {
    "id": "uuid-here",
    "agent_id": "agent-uuid",
    "event_type": "PreToolUse",
    "content": "About to execute bash command",
    "payload": { "tool": "bash", "input": {...} }
  }
}
```

---

## Log Flow: Backend → Frontend

### Complete Log Flow Architecture

This diagram shows how logs flow from backend events through WebSocket to frontend state updates.

```mermaid
sequenceDiagram
    participant User
    participant FastAPI as FastAPI Server
    participant OrchService as OrchestratorService
    participant Claude as Claude SDK
    participant DB as PostgreSQL
    participant WSManager as WebSocketManager
    participant WS as WebSocket Protocol
    participant Frontend as Frontend Store
    participant UI as Vue UI

    Note over User,UI: User sends message "Create a new agent"

    User->>FastAPI: POST /send_chat
    FastAPI->>DB: insert_chat_message()<br/>(orchestrator_chat table)
    FastAPI->>WSManager: broadcast('orchestrator_chat')
    WSManager->>WS: Send to all clients
    WS->>Frontend: message type='orchestrator_chat'
    Frontend->>UI: Update chat UI (optimistic)

    FastAPI-->>User: 202 Accepted

    Note over FastAPI,Claude: Async processing starts

    FastAPI->>OrchService: process_user_message()
    OrchService->>Claude: client.query(message)

    loop Stream Response Blocks
        Claude-->>OrchService: TextBlock
        OrchService->>DB: insert_chat_message()
        OrchService->>WSManager: broadcast('orchestrator_chat')
        WSManager->>WS: {type: 'orchestrator_chat', message: {...}}
        WS->>Frontend: Receive event
        Frontend->>Frontend: addOrchestratorChatEvent()
        Frontend->>UI: Append to chat (live)

        Claude-->>OrchService: ThinkingBlock
        OrchService->>DB: insert_system_log()
        OrchService->>WSManager: broadcast('thinking_block')
        WSManager->>WS: {type: 'thinking_block', data: {...}}
        WS->>Frontend: Receive event
        Frontend->>Frontend: addThinkingBlockEvent()
        Frontend->>UI: Show thinking indicator

        Claude-->>OrchService: ToolUseBlock (create_agent)
        OrchService->>DB: insert_system_log()
        OrchService->>WSManager: broadcast('tool_use_block')
        WSManager->>WS: {type: 'tool_use_block', data: {...}}
        WS->>Frontend: Receive event
        Frontend->>Frontend: addToolUseBlockEvent()
        Frontend->>UI: Show tool execution
    end

    OrchService->>DB: update_orchestrator_costs()
    OrchService->>WSManager: broadcast_orchestrator_updated()
    WSManager->>WS: {type: 'orchestrator_updated', costs: {...}}
    WS->>Frontend: Receive event
    Frontend->>UI: Update stats header
```

### Agent Command Flow with Hooks

```mermaid
sequenceDiagram
    participant Orch as Orchestrator
    participant AM as AgentManager
    participant SDK as Claude SDK<br/>(Agent Session)
    participant Hooks as Hook System
    participant DB as PostgreSQL
    participant WSM as WebSocketManager
    participant WS as WebSocket
    participant FE as Frontend

    Orch->>AM: command_agent(agent_id, prompt)
    AM->>DB: insert_prompt()
    AM->>DB: update_agent_status('executing')
    AM->>WSM: broadcast_agent_status_change()
    WSM->>WS: {type: 'agent_status_changed'}
    WS->>FE: Update agent card status

    AM->>SDK: client.query(prompt)

    Note over SDK,Hooks: Hook: PreToolUse fires
    SDK->>Hooks: on_pre_tool_use(event)
    Hooks->>DB: insert_hook_event()<br/>(agent_logs table)
    Hooks->>WSM: broadcast_agent_log()
    WSM->>WS: {type: 'agent_log', log: {...}}
    WS->>FE: addAgentLogEvent()
    FE->>FE: Pulse animation on agent card

    SDK-->>AM: TextBlock
    AM->>DB: insert_message_block()
    AM->>WSM: broadcast_agent_log()
    WSM->>WS: {type: 'agent_log'}
    WS->>FE: Add to event stream

    SDK-->>AM: ThinkingBlock
    AM->>DB: insert_message_block()
    AM->>WSM: broadcast_agent_log()
    WSM->>WS: {type: 'agent_log'}
    WS->>FE: Add to event stream

    SDK-->>AM: ToolUseBlock
    AM->>DB: insert_message_block()
    AM->>WSM: broadcast_agent_log()
    WSM->>WS: {type: 'agent_log'}
    WS->>FE: Add to event stream

    Note over SDK,Hooks: Hook: PostToolUse fires
    SDK->>Hooks: on_post_tool_use(event)
    Hooks->>Hooks: Track file changes
    Hooks->>DB: insert_hook_event()
    Hooks->>WSM: broadcast_agent_log()
    WSM->>WS: {type: 'agent_log'}
    WS->>FE: Add to event stream

    AM->>DB: update_agent_costs()
    AM->>WSM: broadcast_agent_updated()
    WSM->>WS: {type: 'agent_updated'}
    WS->>FE: Update agent stats

    AM->>DB: update_agent_status('idle')
    AM->>WSM: broadcast_agent_status_change()
    WSM->>WS: {type: 'agent_status_changed'}
    WS->>FE: Update agent card
```

---

## Frontend WebSocket Handling

### 1. Connection Initialization

```mermaid
graph TB
    subgraph "App Lifecycle"
        Mount[App.vue onMounted]
        Init[orchestratorStore.initialize&#40;&#41;]
    end

    subgraph "Initialize Sequence"
        API1[GET /get_orchestrator<br/>Fetch orchestrator info]
        WS[connectWebSocket&#40;&#41;]
        API2[GET /list_agents<br/>Load agents]
        API3[POST /load_chat<br/>Load chat history]
        API4[GET /get_events<br/>Load event stream<br/>limit: 500]
    end

    subgraph "WebSocket Setup"
        WSCreate[new WebSocket&#40;url&#41;]
        Handlers[Register 15+ event handlers]
        Store[Store connection in state]
    end

    Mount --> Init
    Init --> API1
    API1 --> WS
    WS --> API2
    API2 --> API3
    API3 --> API4

    WS --> WSCreate
    WSCreate --> Handlers
    Handlers --> Store

    style WS fill:#ff9999
    style WSCreate fill:#ff9999
```

### 2. Event Routing System

The frontend has a sophisticated event routing system in `orchestratorStore.ts`:

```mermaid
graph TB
    subgraph "WebSocket Layer"
        WSMsg[ws.onmessage]
        Parse[JSON.parse&#40;event.data&#41;]
    end

    subgraph "Event Router"
        Switch{message.type}
    end

    subgraph "Event Handlers"
        H1[onAgentLog]
        H2[onOrchestratorChat]
        H3[onThinkingBlock]
        H4[onToolUseBlock]
        H5[onAgentCreated]
        H6[onAgentUpdated]
        H7[onAgentDeleted]
        H8[onAgentStatusChange]
        H9[onAgentSummaryUpdate]
        H10[onOrchestratorUpdated]
        H11[onChatStream]
        H12[onTyping]
        H13[onError]
    end

    subgraph "State Updates"
        S1[eventStreamEntries<br/>reactive array]
        S2[chatMessages<br/>reactive array]
        S3[agents<br/>reactive array]
        S4[orchestratorAgent<br/>reactive object]
        S5[isTyping<br/>reactive boolean]
        S6[agentPulse<br/>animation manager]
    end

    WSMsg --> Parse
    Parse --> Switch

    Switch -->|agent_log| H1
    Switch -->|orchestrator_chat| H2
    Switch -->|thinking_block| H3
    Switch -->|tool_use_block| H4
    Switch -->|agent_created| H5
    Switch -->|agent_updated| H6
    Switch -->|agent_deleted| H7
    Switch -->|agent_status_changed| H8
    Switch -->|agent_summary_update| H9
    Switch -->|orchestrator_updated| H10
    Switch -->|chat_stream| H11
    Switch -->|chat_typing| H12
    Switch -->|error| H13

    H1 --> S1
    H1 --> S6
    H2 --> S1
    H2 --> S2
    H3 --> S1
    H3 --> S2
    H4 --> S1
    H4 --> S2
    H5 --> S3
    H6 --> S3
    H7 --> S3
    H8 --> S3
    H9 --> S3
    H10 --> S4
    H11 --> S5
    H12 --> S5
    H13 --> S5

    style Switch fill:#ffcc99
    style S1 fill:#99ccff
    style S2 fill:#99ccff
    style S3 fill:#99ccff
    style S4 fill:#99ccff
    style S5 fill:#99ccff
```

### 3. Critical Vue Reactivity Pattern

**The Spread Operator Pattern** - Essential for real-time updates:

```mermaid
graph LR
    subgraph "❌ WRONG - May Miss Updates"
        Wrong1[Receive event]
        Wrong2[chatMessages.value.push&#40;msg&#41;]
        Wrong3[Vue may not detect change<br/>during rapid updates]
    end

    subgraph "✅ CORRECT - Always Reactive"
        Right1[Receive event]
        Right2[chatMessages.value = <br/>[...chatMessages.value, msg]]
        Right3[Vue detects new array<br/>Triggers re-render]
    end

    Wrong1 --> Wrong2 --> Wrong3
    Right1 --> Right2 --> Right3

    style Wrong2 fill:#ff9999
    style Right2 fill:#99ff99
```

**Code Example:**
```typescript
// ❌ WRONG - Mutation, may not trigger reactivity
function addEventWrong(entry: EventStreamEntry) {
  eventStreamEntries.value.push(entry)
}

// ✅ CORRECT - Creates new array, always reactive
function addEventStreamEntry(entry: EventStreamEntry) {
  eventStreamEntries.value = [...eventStreamEntries.value, entry]
}
```

### 4. Pulse Animation System

The frontend has a sophisticated pulse animation system for agent cards:

```mermaid
graph TB
    subgraph "AgentPulse Manager"
        Manager[agentPulse singleton]
        Active[activePulses<br/>Map&lt;agentId, boolean&gt;]
        Duration[PULSE_DURATION = 2000ms]
    end

    subgraph "Trigger Flow"
        Event[agent_log event received]
        Check{Is agent<br/>already pulsing?}
        Set[setPulse&#40;agentId&#41;]
        Timer[setTimeout&#40;2000ms&#41;]
        Clear[clearPulse&#40;agentId&#41;]
    end

    subgraph "UI Binding"
        Comp[AgentCard Component]
        Computed[isPulsing computed property]
        Class[CSS class binding<br/>.agent-pulse]
        Anim[CSS animation]
    end

    Event --> Check
    Check -->|No| Set
    Check -->|Yes| Event
    Set --> Active
    Set --> Timer
    Timer --> Clear
    Clear --> Active

    Active --> Computed
    Comp --> Computed
    Computed --> Class
    Class --> Anim

    style Set fill:#99ff99
    style Anim fill:#ffcc99
```

---

## Agent Orchestration Flow

### 1. User Message → Agent Creation

```mermaid
flowchart TB
    Start([User: Create new agent])

    subgraph "Frontend"
        UI1[User types message]
        UI2[sendMessage&#40;text&#41;]
        UI3[POST /send_chat]
        UI4[Optimistic UI update]
    end

    subgraph "Backend API"
        API1[Receive POST /send_chat]
        API2[Return 202 Accepted]
        API3[Start async task]
    end

    subgraph "Orchestrator Processing"
        Orch1[Insert user message to DB]
        Orch2[Broadcast orchestrator_chat]
        Orch3[Query Claude SDK]
        Orch4{Process blocks}
        Orch5[TextBlock:<br/>Create agent explanation]
        Orch6[ToolUseBlock:<br/>create_agent tool]
    end

    subgraph "Agent Manager"
        AM1[create_agent&#40;name, model, prompt&#41;]
        AM2[Insert agent to DB]
        AM3[Initialize FileTracker]
        AM4[Create Claude SDK client]
        AM5[Send greeting message]
        AM6[Store session_id]
        AM7[Broadcast agent_created]
    end

    subgraph "Frontend Updates"
        FE1[Receive agent_created event]
        FE2[Add to agents array]
        FE3[Update agent sidebar]
        FE4[Show success notification]
    end

    Start --> UI1
    UI1 --> UI2
    UI2 --> UI3
    UI3 --> UI4
    UI3 --> API1
    API1 --> API2
    API2 --> API3
    API3 --> Orch1
    Orch1 --> Orch2
    Orch2 --> Orch3
    Orch3 --> Orch4
    Orch4 --> Orch5
    Orch4 --> Orch6

    Orch6 --> AM1
    AM1 --> AM2
    AM2 --> AM3
    AM3 --> AM4
    AM4 --> AM5
    AM5 --> AM6
    AM6 --> AM7

    AM7 --> FE1
    FE1 --> FE2
    FE2 --> FE3
    FE3 --> FE4

    style Orch6 fill:#ffcc99
    style AM7 fill:#ff9999
    style FE1 fill:#99ccff
```

### 2. Agent Command Execution

```mermaid
flowchart TB
    Start([Orchestrator commands agent])

    subgraph "Tool Invocation"
        T1[ToolUseBlock:<br/>command_agent]
        T2[Extract: agent_id, command]
    end

    subgraph "Agent Manager"
        AM1[insert_prompt&#40;&#41; to DB]
        AM2[update_agent_status<br/>→ 'executing']
        AM3[broadcast_agent_status_change]
        AM4[Create Claude SDK client<br/>resume session]
        AM5[Query with command]
    end

    subgraph "Claude SDK Processing"
        SDK1{Process Blocks}
        SDK2[PreToolUse Hook]
        SDK3[TextBlock]
        SDK4[ThinkingBlock]
        SDK5[ToolUseBlock]
        SDK6[PostToolUse Hook]
    end

    subgraph "Database Logging"
        DB1[insert_hook_event&#40;&#41;]
        DB2[insert_message_block&#40;&#41;]
        DB3[update_agent_costs&#40;&#41;]
        DB4[update_agent_status<br/>→ 'idle']
    end

    subgraph "WebSocket Broadcasting"
        WS1[broadcast_agent_log]
        WS2[broadcast_agent_updated]
        WS3[broadcast_agent_status_change]
    end

    subgraph "Frontend"
        FE1[Event stream updates]
        FE2[Agent card pulsing]
        FE3[Stats updated]
        FE4[Status indicator]
    end

    Start --> T1
    T1 --> T2
    T2 --> AM1
    AM1 --> AM2
    AM2 --> AM3
    AM3 --> AM4
    AM4 --> AM5
    AM5 --> SDK1

    SDK1 --> SDK2
    SDK1 --> SDK3
    SDK1 --> SDK4
    SDK1 --> SDK5
    SDK1 --> SDK6

    SDK2 --> DB1
    SDK3 --> DB2
    SDK4 --> DB2
    SDK5 --> DB2
    SDK6 --> DB1

    DB1 --> WS1
    DB2 --> WS1

    SDK6 --> DB3
    DB3 --> WS2
    DB3 --> DB4
    DB4 --> WS3

    WS1 --> FE1
    WS1 --> FE2
    WS2 --> FE3
    WS3 --> FE4

    style SDK1 fill:#ffcc99
    style WS1 fill:#ff9999
    style WS2 fill:#ff9999
    style WS3 fill:#ff9999
```

---

## Database Schema

### Entity Relationship Diagram

```mermaid
erDiagram
    ORCHESTRATOR_AGENTS ||--o{ AGENTS : "has many"
    ORCHESTRATOR_AGENTS ||--o{ ORCHESTRATOR_CHAT : "has many"
    AGENTS ||--o{ AGENT_LOGS : "has many"
    AGENTS ||--o{ PROMPTS : "has many"
    AGENTS ||--o{ ORCHESTRATOR_CHAT : "optional messages"

    ORCHESTRATOR_AGENTS {
        uuid id PK
        text session_id UK "Claude SDK session"
        text system_prompt
        text status "idle|executing|waiting"
        text working_dir
        int input_tokens "Cumulative"
        int output_tokens "Cumulative"
        decimal total_cost "USD"
        boolean archived
        jsonb metadata "System info, commands"
        timestamptz created_at
        timestamptz updated_at
    }

    AGENTS {
        uuid id PK
        uuid orchestrator_agent_id FK
        text name
        text model "claude-sonnet-4-5-20250929"
        text system_prompt
        text working_dir
        text status
        text session_id UK
        int input_tokens
        int output_tokens
        decimal total_cost
        boolean archived
        jsonb metadata
        timestamptz created_at
        timestamptz updated_at
    }

    ORCHESTRATOR_CHAT {
        uuid id PK
        uuid orchestrator_agent_id FK
        text sender_type "user|orchestrator|agent"
        text receiver_type "user|orchestrator|agent"
        text message "Content"
        text summary "AI-generated"
        uuid agent_id FK "nullable"
        jsonb metadata "tools_used, type"
        timestamptz created_at
        timestamptz updated_at
    }

    AGENT_LOGS {
        uuid id PK
        uuid agent_id FK
        text session_id
        text task_slug "Task identifier"
        int entry_index "Sequential"
        text event_category "hook|response"
        text event_type "PreToolUse, TextBlock"
        text content "Text content"
        jsonb payload "Full event data"
        text summary "AI-generated"
        timestamptz timestamp
    }

    PROMPTS {
        uuid id PK
        uuid agent_id FK
        text task_slug
        text author "engineer|orchestrator_agent"
        text prompt_text
        text summary
        timestamptz timestamp
        text session_id
    }

    SYSTEM_LOGS {
        uuid id PK
        text level "DEBUG|INFO|WARNING|ERROR"
        text message
        text summary
        jsonb metadata
        timestamptz timestamp
    }
```

### Table Purposes

| Table | Purpose | Append-Only | Key Indexes |
|-------|---------|--------------|-------------|
| `orchestrator_agents` | Singleton orchestrator state | No | id, session_id |
| `agents` | Command agents | No | id, orchestrator_agent_id, session_id |
| `orchestrator_chat` | Chat message log | **Yes** | orchestrator_agent_id, agent_id |
| `agent_logs` | Unified event log | **Yes** | agent_id, session_id, task_slug |
| `prompts` | Agent task history | **Yes** | agent_id, session_id |
| `system_logs` | Global application events | **Yes** | level, timestamp |

---

## Critical Components Reference

### Backend Components

```mermaid
graph TB
    subgraph "Core Modules"
        Main[main.py<br/>646 lines<br/>FastAPI + WebSocket]
        DB[database.py<br/>1600 lines<br/>All DB operations]
        WS[websocket_manager.py<br/>258 lines<br/>Connection hub]
    end

    subgraph "Services"
        Orch[orchestrator_service.py<br/>1010 lines<br/>Orchestrator execution]
        Agent[agent_manager.py<br/>1398 lines<br/>8 management tools]
    end

    subgraph "Hooks"
        OHooks[orchestrator_hooks.py<br/>PreToolUse, PostToolUse, Stop]
        AHooks[command_agent_hooks.py<br/>All agent lifecycle hooks]
    end

    subgraph "Utilities"
        Config[config.py<br/>Environment]
        Logger[logger.py<br/>Rich console]
        File[file_tracker.py<br/>Track changes]
    end

    Main --> Orch
    Main --> Agent
    Main --> WS
    Orch --> DB
    Agent --> DB
    Agent --> File
    Orch --> OHooks
    Agent --> AHooks
    OHooks --> WS
    AHooks --> WS
```

### Frontend Components

```mermaid
graph TB
    subgraph "Entry Point"
        App[App.vue<br/>Initialize store]
    end

    subgraph "State Management"
        Store[orchestratorStore.ts<br/>1005 lines<br/>15+ WebSocket handlers]
    end

    subgraph "Services"
        Chat[chatService.ts<br/>179 lines<br/>HTTP + WebSocket]
        API[api.ts<br/>Axios client]
    end

    subgraph "UI Components"
        OrcChat[OrchestratorChat.vue<br/>265 lines<br/>Chat interface]
        Events[EventStream.vue<br/>~300 lines<br/>Live event log]
        Agents[AgentList.vue<br/>~250 lines<br/>Sidebar with pulse]
    end

    subgraph "Composables"
        Pulse[agentPulse.ts<br/>Animation manager]
        Utils[Various utilities]
    end

    App --> Store
    Store --> Chat
    Store --> API
    Store --> Pulse

    OrcChat --> Store
    Events --> Store
    Agents --> Store
    Agents --> Pulse
```

---

## Key Technical Patterns

### 1. Three-Phase Logging Pattern

Used for all orchestrator interactions:

```mermaid
graph LR
    subgraph "Phase 1: Pre-execution"
        P1[Log input<br/>user message/prompt]
        P2[Insert to DB]
        P3[Broadcast to clients]
    end

    subgraph "Phase 2: Execution"
        E1[Stream blocks]
        E2[Log each block]
        E3[Broadcast in real-time]
    end

    subgraph "Phase 3: Post-execution"
        Po1[Update costs]
        Po2[Update session ID]
        Po3[Broadcast final state]
    end

    P1 --> P2 --> P3 --> E1 --> E2 --> E3 --> Po1 --> Po2 --> Po3
```

### 2. Async Background Tasks

AI summarization runs without blocking:

```python
# Fire and forget pattern
asyncio.create_task(self._summarize_and_update_chat(chat_id, message))
```

### 3. Connection Pooling

```python
# asyncpg pool with 5-20 connections
_pool = await asyncpg.create_pool(
    database_url,
    min_size=5,
    max_size=20,
    command_timeout=60
)

# Safe connection handling
async with get_connection() as conn:
    await conn.execute(...)
```

---

## WebSocket Event Types Complete Reference

### Event Type Catalog

| Event Type | Direction | Trigger | Payload | Frontend Updates |
|-----------|-----------|---------|---------|------------------|
| `orchestrator_chat` | Backend→Frontend | User/AI message | ChatMessage with DB ID | Event stream + Chat UI |
| `thinking_block` | Backend→Frontend | Claude thinking | Thinking content | Event stream + Chat UI |
| `tool_use_block` | Backend→Frontend | Tool invocation | Tool name + input | Event stream + Chat UI |
| `agent_log` | Backend→Frontend | Hook or response | AgentLogEvent | Event stream + Pulse |
| `agent_created` | Backend→Frontend | Agent created | Agent metadata | Agent list |
| `agent_updated` | Backend→Frontend | Costs updated | Costs/tokens | Agent stats |
| `agent_deleted` | Backend→Frontend | Agent deleted | Agent ID | Remove from list |
| `agent_status_changed` | Backend→Frontend | Status change | Old/new status | Agent card |
| `agent_summary_update` | Backend→Frontend | Summary generated | Latest summary | Agent card |
| `orchestrator_updated` | Backend→Frontend | Costs updated | Costs/tokens | Header stats |
| `chat_stream` | Backend→Frontend | Streaming response | Response chunk | Typing indicator |
| `chat_typing` | Backend→Frontend | Typing started/stopped | Boolean flag | Typing indicator |
| `error` | Backend→Frontend | Error occurred | Error details | Console log |
| `connection_established` | Backend→Frontend | Client connected | Client ID | Connection status |

---

## Configuration Reference

### Environment Variables

**Backend (.env)**
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/orch_db

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Server
BACKEND_HOST=127.0.0.1
BACKEND_PORT=9403

# Orchestrator
ORCHESTRATOR_MODEL=claude-sonnet-4-5-20250929
ORCHESTRATOR_WORKING_DIR=/path/to/project
LOG_LEVEL=INFO
```

**Frontend (.env)**
```bash
# API endpoints
VITE_API_BASE_URL=http://127.0.0.1:9403
VITE_WEBSOCKET_URL=ws://127.0.0.1:9403/ws

# Server
FRONTEND_PORT=5175
```

---

## Summary

This multi-agent orchestration system demonstrates:

1. **Real-time Architecture**: WebSocket-based event streaming with comprehensive broadcasting
2. **State Management**: Sophisticated Pinia store with reactive updates using spread operators
3. **Database Persistence**: 6-table PostgreSQL schema with append-only event logs
4. **Agent Lifecycle**: Complete management from creation to deletion with session resumption
5. **Event Tracking**: Unified logging system with hooks capturing all LLM interactions
6. **UI Responsiveness**: Pulse animations, typing indicators, and live updates
7. **Scalability**: Connection pooling, async processing, and background tasks

The WebSocket manager acts as the central nervous system, broadcasting all events from backend services (orchestrator + agent manager) to connected frontend clients, enabling a truly real-time multi-agent development experience.

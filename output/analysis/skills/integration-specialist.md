---
title: "Integration Specialist"
description: "Integrate agentic systems with MCP, APIs, databases, and production infrastructure"
tags: ["integration", "mcp", "api", "database", "production", "deployment"]
---

# Integration Specialist

## Purpose

Connect agentic systems to existing infrastructure, external services, and production environments. Master MCP (Model Context Protocol) servers, API integration, database connectivity, and deployment patterns for enterprise-ready agentic systems.

## When to Use

- Connecting agents to databases and file systems via MCP
- Building REST APIs and WebSocket servers for agent communication
- Integrating with GitHub, CI/CD pipelines, and cloud services
- Deploying agents to production environments
- Setting up monitoring and observability for agent systems
- Implementing secure agent-to-service communication
- Creating bridges between legacy systems and agents

## How It Works

### Step 1: MCP Server Integration

#### Understanding MCP
Model Context Protocol enables agents to interact with external systems without consuming context.

```json
// .claude/mcp/config.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "env": {
        "PATHS": "/project,/data"
      }
    },
    "postgres": {
      "command": "uv",
      "args": ["run", "mcp_postgres_server.py"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

#### Creating Custom MCP Servers

```python
# mcp_custom_server.py
from mcp import McpServer, Tool, Resource
import asyncio
from typing import Any, Dict

class CustomMCPServer(McpServer):
    def __init__(self):
        super().__init__(
            name="custom-integration",
            version="1.0.0"
        )
        self.register_tools()
        self.register_resources()

    def register_tools(self):
        @self.tool(
            name="query_data",
            description="Query custom data source",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "filters": {"type": "object"}
                }
            }
        )
        async def query_data(query: str, filters: Dict = None) -> Dict[str, Any]:
            # Implement custom query logic
            result = await self.execute_query(query, filters)
            return {"data": result}

        @self.tool(
            name="update_system",
            description="Update external system",
            input_schema={
                "type": "object",
                "properties": {
                    "entity": {"type": "string"},
                    "updates": {"type": "object"}
                }
            }
        )
        async def update_system(entity: str, updates: Dict) -> Dict[str, Any]:
            # Implement update logic
            success = await self.apply_updates(entity, updates)
            return {"success": success}

    def register_resources(self):
        @self.resource(
            uri="custom://config",
            name="System Configuration",
            mime_type="application/json"
        )
        async def get_config() -> Dict[str, Any]:
            return self.load_configuration()

if __name__ == "__main__":
    server = CustomMCPServer()
    asyncio.run(server.run())
```

### Step 2: API Integration

#### RESTful API Design

```python
# agent_api.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
import uuid

app = FastAPI(title="Agent Integration API")

class TaskRequest(BaseModel):
    agent: str
    action: str
    parameters: Dict[str, Any]
    callback_url: Optional[str] = None

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None

@app.post("/api/v1/tasks", response_model=TaskResponse)
async def create_task(
    request: TaskRequest,
    background_tasks: BackgroundTasks
):
    """Submit task to agent for processing"""
    task_id = str(uuid.uuid4())

    # Queue task for agent processing
    background_tasks.add_task(
        process_agent_task,
        task_id,
        request
    )

    return TaskResponse(
        task_id=task_id,
        status="queued"
    )

@app.get("/api/v1/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Get task execution status"""
    task = await get_task_from_db(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(
        task_id=task_id,
        status=task["status"],
        result=task.get("result")
    )

async def process_agent_task(task_id: str, request: TaskRequest):
    """Process task with appropriate agent"""
    try:
        # Get agent
        agent = get_agent(request.agent)

        # Execute task
        result = await agent.execute(
            action=request.action,
            parameters=request.parameters
        )

        # Update task status
        await update_task(task_id, "completed", result)

        # Send callback if provided
        if request.callback_url:
            await send_callback(request.callback_url, result)

    except Exception as e:
        await update_task(task_id, "failed", {"error": str(e)})
```

#### WebSocket Integration

```python
# websocket_server.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.subscriptions: Dict[str, Set[str]] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        self.active_connections.pop(client_id, None)
        # Clean up subscriptions
        for topic in self.subscriptions:
            self.subscriptions[topic].discard(client_id)

    async def send_message(self, client_id: str, message: dict):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)

    async def broadcast(self, topic: str, message: dict):
        subscribers = self.subscriptions.get(topic, set())
        for client_id in subscribers:
            await self.send_message(client_id, message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            if data["type"] == "subscribe":
                topic = data["topic"]
                if topic not in manager.subscriptions:
                    manager.subscriptions[topic] = set()
                manager.subscriptions[topic].add(client_id)

            elif data["type"] == "agent_request":
                # Process agent request
                result = await process_agent_request(data["payload"])

                # Send response
                await manager.send_message(client_id, {
                    "type": "agent_response",
                    "result": result
                })

            elif data["type"] == "stream_request":
                # Stream responses
                async for chunk in process_streaming_request(data["payload"]):
                    await manager.send_message(client_id, {
                        "type": "stream_chunk",
                        "chunk": chunk
                    })

    except WebSocketDisconnect:
        manager.disconnect(client_id)
```

### Step 3: Database Integration

#### PostgreSQL with Agent Systems

```python
# database_integration.py
import asyncpg
from contextlib import asynccontextmanager
from typing import List, Dict, Any

class AgentDatabase:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None

    async def initialize(self):
        """Initialize database connection pool"""
        self.pool = await asyncpg.create_pool(
            self.database_url,
            min_size=10,
            max_size=20,
            max_inactive_connection_lifetime=300
        )
        await self.create_tables()

    async def create_tables(self):
        """Create required tables for agent system"""
        async with self.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS agent_tasks (
                    id UUID PRIMARY KEY,
                    agent_name VARCHAR(255),
                    status VARCHAR(50),
                    input JSONB,
                    output JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS agent_conversations (
                    id UUID PRIMARY KEY,
                    agent_name VARCHAR(255),
                    messages JSONB[],
                    metadata JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS agent_state (
                    agent_name VARCHAR(255) PRIMARY KEY,
                    state JSONB,
                    version INTEGER,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')

    @asynccontextmanager
    async def acquire(self):
        """Acquire database connection from pool"""
        async with self.pool.acquire() as conn:
            yield conn

    async def log_task(self, task_id: str, agent_name: str, input_data: Dict):
        """Log agent task execution"""
        async with self.acquire() as conn:
            await conn.execute('''
                INSERT INTO agent_tasks (id, agent_name, status, input)
                VALUES ($1, $2, $3, $4)
            ''', task_id, agent_name, 'started', json.dumps(input_data))

    async def update_task_result(self, task_id: str, output: Dict, status: str = 'completed'):
        """Update task with result"""
        async with self.acquire() as conn:
            await conn.execute('''
                UPDATE agent_tasks
                SET output = $1, status = $2, updated_at = CURRENT_TIMESTAMP
                WHERE id = $3
            ''', json.dumps(output), status, task_id)

    async def get_agent_state(self, agent_name: str) -> Dict:
        """Get agent state from database"""
        async with self.acquire() as conn:
            row = await conn.fetchrow('''
                SELECT state, version FROM agent_state
                WHERE agent_name = $1
            ''', agent_name)
            if row:
                return json.loads(row['state'])
            return {}

    async def update_agent_state(self, agent_name: str, state: Dict):
        """Update agent state with optimistic locking"""
        async with self.acquire() as conn:
            await conn.execute('''
                INSERT INTO agent_state (agent_name, state, version)
                VALUES ($1, $2, 1)
                ON CONFLICT (agent_name)
                DO UPDATE SET
                    state = $2,
                    version = agent_state.version + 1,
                    updated_at = CURRENT_TIMESTAMP
            ''', agent_name, json.dumps(state))
```

### Step 4: GitHub Integration

```python
# github_integration.py
from github import Github
from github.PullRequest import PullRequest
import asyncio
from typing import Optional

class GitHubAgentIntegration:
    def __init__(self, token: str, repo_name: str):
        self.github = Github(token)
        self.repo = self.github.get_repo(repo_name)

    async def create_issue_handler(self):
        """Set up webhook handler for new issues"""
        @app.post("/webhooks/github/issues")
        async def handle_issue(payload: dict):
            if payload["action"] == "opened":
                issue = payload["issue"]

                # Trigger agent workflow
                await self.process_issue(issue)

            return {"status": "processed"}

    async def process_issue(self, issue: dict):
        """Process GitHub issue with agents"""
        # Analyze issue
        analysis = await self.analyze_issue(issue)

        if analysis["auto_solvable"]:
            # Create branch
            branch_name = f"fix-{issue['number']}"
            await self.create_branch(branch_name)

            # Generate solution
            solution = await self.generate_solution(issue, analysis)

            # Create PR
            pr = await self.create_pull_request(
                branch_name,
                solution,
                issue["number"]
            )

            # Add comment to issue
            await self.comment_on_issue(
                issue["number"],
                f"I've created PR #{pr.number} to address this issue."
            )

    async def create_pull_request(
        self,
        branch: str,
        changes: dict,
        issue_number: int
    ) -> PullRequest:
        """Create PR with agent-generated changes"""
        # Apply changes to branch
        for file_path, content in changes.items():
            self.update_file(branch, file_path, content)

        # Create PR
        pr = self.repo.create_pull(
            title=f"Fix issue #{issue_number}",
            body=self.generate_pr_description(changes),
            head=branch,
            base="main"
        )

        return pr

    async def setup_pr_review_automation(self):
        """Automate PR reviews with agents"""
        @app.post("/webhooks/github/pull_request")
        async def handle_pr(payload: dict):
            if payload["action"] in ["opened", "synchronize"]:
                pr = payload["pull_request"]

                # Run agent review
                review = await self.review_pull_request(pr)

                # Post review comment
                await self.post_review(pr["number"], review)

            return {"status": "reviewed"}
```

### Step 5: CI/CD Integration

```yaml
# .github/workflows/agent-pipeline.yml
name: Agent-Driven Pipeline

on:
  issues:
    types: [opened, labeled]
  pull_request:
    types: [opened, synchronize]

jobs:
  agent-process:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -r requirements.txt

      - name: Run Agent Workflow
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          python -m agent_system.pipeline \
            --event-type ${{ github.event_name }} \
            --payload '${{ toJson(github.event) }}'

      - name: Upload Agent Artifacts
        uses: actions/upload-artifact@v2
        with:
          name: agent-outputs
          path: outputs/
```

### Step 6: Production Deployment

```python
# deployment.py
import kubernetes
from kubernetes import client, config
import docker

class AgentDeployment:
    def __init__(self):
        # Load Kubernetes config
        config.load_incluster_config()  # For in-cluster
        # config.load_kube_config()  # For local

        self.k8s_apps = client.AppsV1Api()
        self.k8s_core = client.CoreV1Api()
        self.docker_client = docker.from_env()

    async def deploy_agent_service(self, agent_config: dict):
        """Deploy agent as Kubernetes service"""
        # Build Docker image
        image = await self.build_agent_image(agent_config)

        # Create Kubernetes deployment
        deployment = self.create_deployment_manifest(agent_config, image)
        self.k8s_apps.create_namespaced_deployment(
            namespace="agents",
            body=deployment
        )

        # Create service
        service = self.create_service_manifest(agent_config)
        self.k8s_core.create_namespaced_service(
            namespace="agents",
            body=service
        )

        # Set up monitoring
        await self.setup_monitoring(agent_config["name"])

    def create_deployment_manifest(self, config: dict, image: str):
        """Create Kubernetes deployment manifest"""
        return client.V1Deployment(
            metadata=client.V1ObjectMeta(name=config["name"]),
            spec=client.V1DeploymentSpec(
                replicas=config.get("replicas", 1),
                selector=client.V1LabelSelector(
                    match_labels={"app": config["name"]}
                ),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(
                        labels={"app": config["name"]}
                    ),
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name=config["name"],
                                image=image,
                                env=[
                                    client.V1EnvVar(
                                        name="ANTHROPIC_API_KEY",
                                        value_from=client.V1EnvVarSource(
                                            secret_key_ref=client.V1SecretKeySelector(
                                                name="agent-secrets",
                                                key="anthropic-key"
                                            )
                                        )
                                    )
                                ],
                                resources=client.V1ResourceRequirements(
                                    limits={"memory": "1Gi", "cpu": "1"},
                                    requests={"memory": "256Mi", "cpu": "0.5"}
                                )
                            )
                        ]
                    )
                )
            )
        )
```

## Inputs Expected

- **Integration Requirements**: Systems to connect, protocols, authentication
- **Performance Requirements**: Latency, throughput, scalability needs
- **Security Requirements**: Authentication, encryption, audit requirements
- **Infrastructure Details**: Cloud provider, deployment environment
- **Monitoring Needs**: Metrics, logging, alerting requirements

## Outputs Provided

1. **Integration Configuration**
   ```yaml
   integrations:
     mcp_servers:
       - filesystem
       - database
       - github
     apis:
       - rest: http://api.service/v1
       - websocket: ws://stream.service
     databases:
       - postgres: primary
       - redis: cache
   ```

2. **Implementation Code**
   - MCP server implementations
   - API endpoints and clients
   - Database connectors
   - Deployment scripts

3. **Infrastructure as Code**
   ```yaml
   # terraform/kubernetes/docker-compose
   - Service definitions
   - Network configurations
   - Security policies
   - Monitoring setup
   ```

4. **Documentation**
   - API documentation
   - Integration guides
   - Security documentation
   - Troubleshooting guides

## Examples

### Example 1: Full MCP Integration Suite

```python
class MCPIntegrationSuite:
    """Complete MCP integration for agent system"""

    def __init__(self):
        self.servers = {}

    async def initialize(self):
        """Initialize all MCP servers"""
        # Filesystem access
        self.servers["fs"] = await self.start_mcp_server(
            "filesystem",
            paths=["/data", "/config"]
        )

        # Database access
        self.servers["db"] = await self.start_mcp_server(
            "postgres",
            connection_string=os.getenv("DATABASE_URL")
        )

        # External APIs
        self.servers["api"] = await self.start_custom_mcp(
            "api_bridge",
            endpoints=self.load_api_config()
        )

    async def start_custom_mcp(self, name: str, **config):
        """Start custom MCP server"""
        server = CustomMCPServer(name, config)
        await server.start()
        return server

    def get_mcp_config(self):
        """Generate MCP configuration for Claude"""
        return {
            "mcpServers": {
                name: server.get_config()
                for name, server in self.servers.items()
            }
        }
```

### Example 2: Event-Driven Integration

```python
class EventDrivenIntegration:
    """Event-driven architecture for agent integration"""

    def __init__(self):
        self.event_bus = EventBus()
        self.agents = {}
        self.handlers = {}

    def setup_event_routing(self):
        """Configure event routing between systems"""
        # GitHub events
        self.event_bus.on("github.issue.created", self.handle_new_issue)
        self.event_bus.on("github.pr.updated", self.handle_pr_update)

        # Database events
        self.event_bus.on("db.record.created", self.handle_new_record)
        self.event_bus.on("db.alert.triggered", self.handle_alert)

        # Agent events
        self.event_bus.on("agent.task.completed", self.handle_task_complete)
        self.event_bus.on("agent.error", self.handle_agent_error)

    async def handle_new_issue(self, event: dict):
        """Process new GitHub issue"""
        # Route to appropriate agent
        if "bug" in event["labels"]:
            agent = self.agents["bug_fixer"]
        elif "feature" in event["labels"]:
            agent = self.agents["feature_developer"]
        else:
            agent = self.agents["triage"]

        # Process with agent
        result = await agent.process(event)

        # Emit completion event
        self.event_bus.emit("issue.processed", result)
```

### Example 3: Monitoring Integration

```python
class MonitoringIntegration:
    """Comprehensive monitoring for agent systems"""

    def __init__(self):
        self.prometheus = PrometheusClient()
        self.grafana = GrafanaClient()
        self.alerts = AlertManager()

    def setup_metrics(self):
        """Define and register metrics"""
        # Agent metrics
        self.agent_requests = Counter(
            'agent_requests_total',
            'Total agent requests',
            ['agent_name', 'action']
        )
        self.agent_latency = Histogram(
            'agent_latency_seconds',
            'Agent response latency',
            ['agent_name']
        )
        self.agent_errors = Counter(
            'agent_errors_total',
            'Agent errors',
            ['agent_name', 'error_type']
        )

        # Integration metrics
        self.api_calls = Counter(
            'external_api_calls_total',
            'External API calls',
            ['service', 'endpoint']
        )
        self.db_queries = Histogram(
            'database_query_duration_seconds',
            'Database query duration',
            ['query_type']
        )

    def track_agent_execution(self, agent_name: str):
        """Decorator to track agent execution"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    self.agent_requests.labels(
                        agent_name=agent_name,
                        action=func.__name__
                    ).inc()
                    return result
                except Exception as e:
                    self.agent_errors.labels(
                        agent_name=agent_name,
                        error_type=type(e).__name__
                    ).inc()
                    raise
                finally:
                    self.agent_latency.labels(
                        agent_name=agent_name
                    ).observe(time.time() - start_time)
            return wrapper
        return decorator
```

## Troubleshooting

### MCP Connection Issues
```python
def diagnose_mcp_connection(server_name: str):
    """Diagnose MCP server connection issues"""
    checks = {
        "server_running": check_process(server_name),
        "port_open": check_port(get_mcp_port(server_name)),
        "permissions": check_permissions(),
        "environment": check_env_variables()
    }
    return generate_diagnostic_report(checks)
```

### API Rate Limiting
```python
class RateLimitHandler:
    def __init__(self):
        self.buckets = {}

    async def handle_rate_limit(self, service: str):
        """Handle API rate limiting"""
        if service not in self.buckets:
            self.buckets[service] = TokenBucket(rate=10, capacity=100)

        if not self.buckets[service].consume():
            # Implement backoff strategy
            await self.exponential_backoff(service)
```

### Database Connection Pool Issues
```python
async def manage_connection_pool(pool):
    """Monitor and manage database connection pool"""
    while True:
        stats = await pool.get_stats()
        if stats["used"] / stats["size"] > 0.8:
            # Scale up pool
            await pool.resize(stats["size"] * 1.5)
        elif stats["used"] / stats["size"] < 0.2:
            # Scale down pool
            await pool.resize(max(10, stats["size"] * 0.7))
        await asyncio.sleep(60)
```

## Related Skills

- **Agentic Architect**: Design integration architecture
- **Agent Builder**: Create agents that use integrations
- **Workflow Designer**: Design workflows using integrated services
- **Testing Strategist**: Test integration points
- **Context Optimizer**: Optimize integration performance

## Key Principles

1. **Loose Coupling**: Keep integrations modular and replaceable
2. **Error Resilience**: Handle failures gracefully with retries and fallbacks
3. **Security First**: Authenticate, authorize, and encrypt all communications
4. **Observability**: Monitor and log all integration points
5. **Performance**: Optimize for latency and throughput

---

*This skill combines integration patterns from TAC-4 through TAC-8 and the Multi-Agent Orchestration module, providing comprehensive integration capabilities for production agentic systems.*
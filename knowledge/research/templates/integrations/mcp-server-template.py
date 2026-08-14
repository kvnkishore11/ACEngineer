#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Server Template

This template provides a complete MCP server implementation that can be customized
for your specific use case. MCP servers expose tools and resources to AI assistants.

Usage:
1. Customize the server name and capabilities
2. Implement your tool functions
3. Run with: python mcp-server.py
4. Connect from Claude or other MCP clients
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

# MCP SDK imports (install with: pip install mcp-sdk)
from mcp import MCPServer, Request, Response
from mcp.types import (
    Tool,
    Resource,
    CompletionResult,
    ErrorResult,
    ToolCall,
    ResourceContent
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ServerConfig:
    """Server configuration."""
    name: str = "custom-mcp-server"
    version: str = "1.0.0"
    description: str = "Custom MCP server for specialized tasks"
    host: str = "localhost"
    port: int = 8765
    max_connections: int = 10


class CustomMCPServer(MCPServer):
    """
    Custom MCP Server implementation.

    This server provides tools and resources for AI assistants to interact
    with your specific domain or application.
    """

    def __init__(self, config: ServerConfig):
        super().__init__(
            name=config.name,
            version=config.version,
            description=config.description
        )
        self.config = config
        self.state = {}  # Server state storage
        self.register_handlers()

    def register_handlers(self):
        """Register all tool and resource handlers."""
        # Register tools
        self.register_tool(
            "example_tool",
            self.handle_example_tool,
            description="Example tool that demonstrates basic functionality",
            parameters={
                "input": {
                    "type": "string",
                    "description": "Input text to process"
                },
                "options": {
                    "type": "object",
                    "description": "Optional parameters",
                    "properties": {
                        "format": {"type": "string", "enum": ["json", "text", "markdown"]},
                        "verbose": {"type": "boolean"}
                    }
                }
            }
        )

        self.register_tool(
            "database_query",
            self.handle_database_query,
            description="Execute database queries safely",
            parameters={
                "query": {
                    "type": "string",
                    "description": "SQL query to execute"
                },
                "database": {
                    "type": "string",
                    "description": "Database name",
                    "default": "main"
                }
            }
        )

        self.register_tool(
            "api_request",
            self.handle_api_request,
            description="Make HTTP API requests",
            parameters={
                "method": {
                    "type": "string",
                    "enum": ["GET", "POST", "PUT", "DELETE"]
                },
                "url": {
                    "type": "string",
                    "description": "API endpoint URL"
                },
                "headers": {
                    "type": "object",
                    "description": "Request headers"
                },
                "body": {
                    "type": "object",
                    "description": "Request body for POST/PUT"
                }
            }
        )

        # Register resources
        self.register_resource(
            "system_info",
            self.get_system_info,
            description="Get system information and status"
        )

        self.register_resource(
            "configuration",
            self.get_configuration,
            description="Get current server configuration"
        )

    async def handle_example_tool(self, params: Dict[str, Any]) -> CompletionResult:
        """
        Handle example tool execution.

        This demonstrates the basic pattern for tool handlers:
        1. Validate input
        2. Process request
        3. Return result or error
        """
        try:
            # Extract parameters
            input_text = params.get("input", "")
            options = params.get("options", {})
            format_type = options.get("format", "text")
            verbose = options.get("verbose", False)

            # Validate input
            if not input_text:
                return ErrorResult(
                    error="Input text is required",
                    details={"params": params}
                )

            # Process input (your custom logic here)
            result = self.process_input(input_text, verbose)

            # Format output based on requested format
            if format_type == "json":
                output = json.dumps(result, indent=2)
            elif format_type == "markdown":
                output = self.format_as_markdown(result)
            else:
                output = str(result)

            # Return successful result
            return CompletionResult(
                completion=output,
                metadata={
                    "processed_at": datetime.now().isoformat(),
                    "format": format_type,
                    "input_length": len(input_text)
                }
            )

        except Exception as e:
            logger.error(f"Error in example_tool: {e}")
            return ErrorResult(
                error=f"Tool execution failed: {str(e)}",
                details={"traceback": str(e)}
            )

    async def handle_database_query(self, params: Dict[str, Any]) -> CompletionResult:
        """
        Handle database query execution.

        IMPORTANT: This is a template. Implement proper security measures:
        - Parameterized queries
        - Input sanitization
        - Access control
        - Query limits
        """
        try:
            query = params.get("query", "")
            database = params.get("database", "main")

            # Security checks (IMPLEMENT THESE!)
            if not self.is_safe_query(query):
                return ErrorResult(error="Query contains unsafe operations")

            if not self.has_database_access(database):
                return ErrorResult(error=f"No access to database: {database}")

            # Execute query (replace with actual database connection)
            # results = await self.db_connection.execute(query)
            results = [
                {"id": 1, "name": "Example", "value": 100},
                {"id": 2, "name": "Sample", "value": 200}
            ]

            return CompletionResult(
                completion=json.dumps(results, indent=2),
                metadata={
                    "row_count": len(results),
                    "database": database,
                    "query_time": "0.05s"
                }
            )

        except Exception as e:
            logger.error(f"Database query error: {e}")
            return ErrorResult(error=f"Query failed: {str(e)}")

    async def handle_api_request(self, params: Dict[str, Any]) -> CompletionResult:
        """
        Handle API request execution.

        Implement proper:
        - Rate limiting
        - Authentication
        - Error handling
        - Response validation
        """
        try:
            import aiohttp

            method = params.get("method", "GET")
            url = params.get("url", "")
            headers = params.get("headers", {})
            body = params.get("body", None)

            # Validate URL (implement whitelist/blacklist)
            if not self.is_allowed_url(url):
                return ErrorResult(error=f"URL not allowed: {url}")

            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=body if body else None
                ) as response:
                    response_text = await response.text()

                    return CompletionResult(
                        completion=response_text,
                        metadata={
                            "status_code": response.status,
                            "headers": dict(response.headers),
                            "method": method,
                            "url": url
                        }
                    )

        except Exception as e:
            logger.error(f"API request error: {e}")
            return ErrorResult(error=f"Request failed: {str(e)}")

    async def get_system_info(self) -> ResourceContent:
        """Get system information resource."""
        import platform
        import psutil

        info = {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "server_uptime": self.get_uptime(),
            "active_connections": len(self.connections),
            "processed_requests": self.request_count
        }

        return ResourceContent(
            content=json.dumps(info, indent=2),
            content_type="application/json",
            metadata={"timestamp": datetime.now().isoformat()}
        )

    async def get_configuration(self) -> ResourceContent:
        """Get server configuration resource."""
        config_data = {
            "name": self.config.name,
            "version": self.config.version,
            "description": self.config.description,
            "host": self.config.host,
            "port": self.config.port,
            "max_connections": self.config.max_connections,
            "available_tools": list(self.tools.keys()),
            "available_resources": list(self.resources.keys())
        }

        return ResourceContent(
            content=json.dumps(config_data, indent=2),
            content_type="application/json"
        )

    # Helper methods (implement these based on your needs)

    def process_input(self, text: str, verbose: bool = False) -> Dict[str, Any]:
        """Process input text (customize this)."""
        result = {
            "original": text,
            "processed": text.upper(),
            "length": len(text),
            "word_count": len(text.split())
        }

        if verbose:
            result["details"] = {
                "processing_time": "0.01s",
                "method": "simple_transformation"
            }

        return result

    def format_as_markdown(self, data: Dict[str, Any]) -> str:
        """Format data as markdown."""
        md = "# Processing Result\n\n"
        for key, value in data.items():
            if isinstance(value, dict):
                md += f"## {key}\n"
                for k, v in value.items():
                    md += f"- **{k}**: {v}\n"
            else:
                md += f"- **{key}**: {value}\n"
        return md

    def is_safe_query(self, query: str) -> bool:
        """Check if SQL query is safe (IMPLEMENT PROPERLY)."""
        # This is a basic example - implement proper SQL injection prevention
        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER", "EXEC"]
        query_upper = query.upper()
        return not any(keyword in query_upper for keyword in dangerous_keywords)

    def has_database_access(self, database: str) -> bool:
        """Check database access permissions."""
        allowed_databases = ["main", "analytics", "reporting"]
        return database in allowed_databases

    def is_allowed_url(self, url: str) -> bool:
        """Check if URL is allowed for API requests."""
        # Implement whitelist/blacklist logic
        if not url.startswith(("http://", "https://")):
            return False

        # Example: Only allow certain domains
        allowed_domains = ["api.example.com", "data.service.com"]
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc in allowed_domains

    def get_uptime(self) -> str:
        """Get server uptime."""
        if hasattr(self, 'start_time'):
            uptime = datetime.now() - self.start_time
            return str(uptime)
        return "Unknown"


async def main():
    """Main entry point."""
    # Create configuration
    config = ServerConfig(
        name="my-custom-mcp-server",
        version="1.0.0",
        description="Custom MCP server for my application",
        host="localhost",
        port=8765
    )

    # Create and start server
    server = CustomMCPServer(config)
    server.start_time = datetime.now()

    logger.info(f"Starting {config.name} v{config.version} on {config.host}:{config.port}")

    try:
        await server.start(config.host, config.port)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
    finally:
        await server.shutdown()
        logger.info("Server shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())


"""
## Installation Requirements

```bash
pip install mcp-sdk aiohttp psutil
```

## Configuration File (mcp-config.json)

```json
{
  "server": {
    "name": "custom-mcp-server",
    "version": "1.0.0",
    "host": "localhost",
    "port": 8765
  },
  "security": {
    "api_key": "your-secret-key",
    "allowed_ips": ["127.0.0.1", "192.168.1.0/24"],
    "rate_limit": {
      "requests_per_minute": 60,
      "burst": 10
    }
  },
  "tools": {
    "database": {
      "enabled": true,
      "connection_string": "postgresql://user:pass@localhost/db"
    },
    "api": {
      "enabled": true,
      "timeout": 30
    }
  }
}
```

## Client Usage Example

```python
from mcp import MCPClient

async def use_mcp_server():
    client = MCPClient()
    await client.connect("localhost", 8765)

    # Call a tool
    result = await client.call_tool(
        "example_tool",
        {
            "input": "Hello, MCP!",
            "options": {"format": "json", "verbose": true}
        }
    )
    print(result)

    # Get a resource
    system_info = await client.get_resource("system_info")
    print(system_info)

    await client.disconnect()
```

## Extending the Server

1. Add new tools by implementing handler methods
2. Register resources for read-only data access
3. Implement authentication and authorization
4. Add logging and monitoring
5. Implement rate limiting and quotas
6. Add WebSocket support for real-time updates
7. Integrate with your existing services
"""
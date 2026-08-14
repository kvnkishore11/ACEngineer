---
title: "Context Optimizer"
description: "Apply the R&D (Reduce & Delegate) framework to optimize context usage and agent performance"
tags: ["context", "optimization", "performance", "delegation", "mcp"]
---

# Context Optimizer

## Purpose

Master context engineering to maximize agent performance while minimizing token usage. Apply the R&D (Reduce & Delegate) framework and 12 advanced techniques to create efficient, scalable agentic systems that handle complex tasks within context limitations.

## When to Use

- Agent hitting context window limits
- Slow response times due to large context
- Need to scale agent operations
- Optimizing token costs
- Handling complex, multi-file operations
- Implementing production systems with efficiency requirements
- Debugging context-related performance issues

## How It Works

### The R&D Framework

#### **R**educe: Minimize Context Size
Systematically reduce the information sent to the model.

#### **D**elegate: Distribute Cognitive Load
Offload processing to specialized systems and agents.

### Step 1: Measure Current Context Usage

```python
class ContextMeasurer:
    def __init__(self):
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")

    def measure_context(self, messages):
        """Measure token usage in context"""
        total_tokens = 0
        breakdown = {}

        for message in messages:
            role = message["role"]
            content = message["content"]
            tokens = len(self.tokenizer.encode(content))

            total_tokens += tokens
            breakdown[role] = breakdown.get(role, 0) + tokens

        return {
            "total": total_tokens,
            "breakdown": breakdown,
            "percentage_used": (total_tokens / 128000) * 100
        }

    def identify_bottlenecks(self, context):
        """Find the largest context consumers"""
        bottlenecks = []

        # Check for large files
        if "files" in context:
            for file in context["files"]:
                if len(file["content"]) > 10000:
                    bottlenecks.append(f"Large file: {file['name']}")

        # Check for repetitive content
        if self.has_repetition(context):
            bottlenecks.append("Repetitive content detected")

        return bottlenecks
```

### Step 2: Apply Reduction Techniques

#### Technique 1: MCP (Model Context Protocol)
Move file operations outside the context window.

```yaml
# .claude/mcp/config.json
{
  "servers": {
    "filesystem": {
      "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem"],
      "args": {
        "paths": ["/project"]
      }
    },
    "database": {
      "command": ["uv", "run", "mcp_database_server.py"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/app"
      }
    }
  }
}
```

**Benefits**:
- File operations don't consume context
- Direct database access without query results in context
- Persistent state management

#### Technique 2: CLAUDE.md Files
Project-specific instructions that load automatically.

```markdown
# CLAUDE.md in project root

## Project Context
This is a React application with TypeScript.

## Key Conventions
- Use functional components with hooks
- Follow Airbnb style guide
- All async operations use async/await
- Test files alongside source files

## Do NOT:
- Modify package-lock.json directly
- Use class components
- Include console.log in production code
```

**Benefits**:
- Instructions don't need repeating
- Project-specific rules always applied
- Team conventions maintained

#### Technique 3: Chunked Output
Break large outputs into manageable pieces.

```python
class ChunkedProcessor:
    def __init__(self, chunk_size=5000):
        self.chunk_size = chunk_size

    def process_large_file(self, file_path):
        """Process file in chunks"""
        with open(file_path, 'r') as f:
            content = f.read()

        chunks = [
            content[i:i + self.chunk_size]
            for i in range(0, len(content), self.chunk_size)
        ]

        results = []
        for i, chunk in enumerate(chunks):
            result = self.process_chunk(chunk, i, len(chunks))
            results.append(result)

        return self.merge_results(results)
```

#### Technique 4: Lazy Loading
Load information only when needed.

```python
class LazyContext:
    def __init__(self):
        self.loaded = {}

    async def get_file(self, path):
        """Load file only if not in context"""
        if path not in self.loaded:
            self.loaded[path] = await self.read_file(path)
        return self.loaded[path]

    def clear_unused(self, accessed_recently):
        """Remove files not accessed recently"""
        for path in list(self.loaded.keys()):
            if path not in accessed_recently:
                del self.loaded[path]
```

### Step 3: Apply Delegation Techniques

#### Technique 5: Sub-Agent Delegation
Create specialized agents for specific tasks.

```python
# Main orchestrator with minimal context
class Orchestrator:
    def __init__(self):
        self.agents = {
            "file_analyzer": FileAnalyzerAgent(),
            "code_generator": CodeGeneratorAgent(),
            "test_runner": TestRunnerAgent()
        }

    async def process_request(self, request):
        # Determine which agent to use
        task_type = self.classify_task(request)

        # Delegate to specialist
        if task_type == "analysis":
            return await self.agents["file_analyzer"].analyze(request)
        elif task_type == "coding":
            return await self.agents["code_generator"].generate(request)
```

#### Technique 6: Tool Patterns
Use tools instead of including data in context.

```python
# Instead of including file content in context
# Bad:
context = {
    "files": [
        {"path": "src/app.py", "content": "... 10000 lines ..."}
    ]
}

# Good: Use a tool
class FileSearchTool:
    def search(self, pattern: str, path: str = "."):
        """Search files without loading all content"""
        return grep(pattern, path)

    def read_lines(self, file: str, start: int, end: int):
        """Read specific lines only"""
        return read_file_lines(file, start, end)
```

### Step 4: Advanced Optimization Techniques

#### Technique 7: Reset and Prime
Clear context and rebuild with only essentials.

```python
class ContextResetter:
    def reset_and_prime(self, conversation):
        """Reset context keeping only essential info"""
        # Extract key information
        summary = self.summarize_conversation(conversation)
        key_decisions = self.extract_decisions(conversation)
        current_task = self.get_current_task(conversation)

        # Create fresh context
        return {
            "summary": summary,
            "decisions": key_decisions,
            "task": current_task,
            "message": "Context reset. Continue with current task."
        }
```

#### Technique 8: Context Bundles
Pre-package common context combinations.

```python
CONTEXT_BUNDLES = {
    "react_setup": {
        "files": ["package.json", "tsconfig.json", "vite.config.ts"],
        "instructions": "React + TypeScript + Vite project setup"
    },
    "api_development": {
        "files": ["openapi.yaml", "src/routes/"],
        "instructions": "RESTful API development context"
    },
    "testing": {
        "files": ["jest.config.js", "tests/"],
        "instructions": "Testing context with Jest"
    }
}

def load_bundle(bundle_name):
    """Load a predefined context bundle"""
    return CONTEXT_BUNDLES[bundle_name]
```

#### Technique 9: Semantic Compression
Compress information while preserving meaning.

```python
class SemanticCompressor:
    def compress_code(self, code):
        """Remove comments, whitespace, maintain functionality"""
        # Remove comments
        code = re.sub(r'#.*', '', code)
        # Remove empty lines
        code = '\n'.join(line for line in code.split('\n') if line.strip())
        # Minimize whitespace
        code = re.sub(r'\s+', ' ', code)
        return code

    def compress_docs(self, docs):
        """Extract key points from documentation"""
        return self.extract_summary(docs, max_tokens=500)
```

#### Technique 10: Dynamic Context Windows
Adjust context based on task complexity.

```python
class DynamicContextManager:
    def calculate_context_size(self, task):
        """Determine optimal context size for task"""
        base_size = 4000

        if task.complexity == "high":
            return base_size * 3
        elif task.complexity == "medium":
            return base_size * 2
        else:
            return base_size

    def prepare_context(self, task, available_tokens):
        """Prepare context within token budget"""
        priority_items = self.prioritize_context(task)
        context = []
        used_tokens = 0

        for item in priority_items:
            item_tokens = self.count_tokens(item)
            if used_tokens + item_tokens <= available_tokens:
                context.append(item)
                used_tokens += item_tokens

        return context
```

### Step 5: Implement Agentic Techniques

#### Technique 11: System Prompts as Context
Embed context in system prompts.

```python
def create_system_prompt(project_info):
    return f"""
You are working on: {project_info['name']}
Tech stack: {', '.join(project_info['stack'])}
Key patterns: {', '.join(project_info['patterns'])}

Always follow these project conventions:
{project_info['conventions']}

This context applies to all requests.
"""
```

#### Technique 12: Expert Models
Use specialized models for specific domains.

```python
class ExpertRouter:
    def __init__(self):
        self.experts = {
            "sql": SQLExpert(),
            "frontend": ReactExpert(),
            "devops": DevOpsExpert(),
            "security": SecurityExpert()
        }

    def route_to_expert(self, query):
        """Route to domain expert with minimal context"""
        domain = self.identify_domain(query)
        expert = self.experts.get(domain)

        # Expert has domain-specific context built-in
        return expert.process(query)
```

## Inputs Expected

- **Current Context Metrics**: Token usage, response times
- **Task Requirements**: What needs to be accomplished
- **Performance Goals**: Target response time, token budget
- **System Constraints**: Available tools, APIs, infrastructure
- **Quality Requirements**: Accuracy needs vs efficiency trade-offs

## Outputs Provided

1. **Optimization Report**
   ```yaml
   metrics:
     before:
       tokens: 50000
       response_time: 8.5s
       cost: $0.15
     after:
       tokens: 12000
       response_time: 2.1s
       cost: $0.036
     improvement: 76% reduction
   ```

2. **Optimized Configuration**
   ```python
   # Optimized context management setup
   config = {
       "mcp_servers": ["filesystem", "database"],
       "context_bundles": ["project_base"],
       "delegation_map": {...},
       "compression_settings": {...}
   }
   ```

3. **Implementation Code**
   - Context management classes
   - MCP server configurations
   - Delegation strategies
   - Monitoring utilities

4. **Performance Dashboard**
   - Real-time token usage
   - Context efficiency metrics
   - Cost tracking
   - Bottleneck identification

## Examples

### Example 1: Large Codebase Analysis

**Problem**: Analyzing a 100,000 line codebase exceeds context limits.

**Solution**: Combine reduction and delegation techniques.

```python
class CodebaseAnalyzer:
    def __init__(self):
        self.file_index = self.build_index()
        self.pattern_cache = {}

    async def analyze_codebase(self, query):
        # Step 1: Use MCP for file operations
        relevant_files = await self.mcp_search(query)

        # Step 2: Delegate to specialized analyzers
        results = await asyncio.gather(
            self.security_analyzer.scan(relevant_files),
            self.dependency_analyzer.check(relevant_files),
            self.quality_analyzer.assess(relevant_files)
        )

        # Step 3: Synthesize without loading all code
        summary = self.synthesize_results(results)

        return summary

    async def mcp_search(self, query):
        """Search using MCP without loading content"""
        return await self.mcp_client.search_files(
            pattern=query,
            file_type="python"
        )
```

### Example 2: Multi-File Refactoring

**Problem**: Refactoring across 50+ files requires too much context.

**Solution**: Chunked processing with state persistence.

```python
class RefactoringOrchestrator:
    def __init__(self):
        self.state = RefactoringState()

    async def refactor_codebase(self, refactor_spec):
        # Break into chunks
        file_groups = self.group_related_files(refactor_spec.files)

        for group in file_groups:
            # Process each group with minimal context
            changes = await self.refactor_group(group, refactor_spec)

            # Persist state between chunks
            self.state.record_changes(changes)

            # Clear context before next group
            await self.clear_context()

        # Final validation with aggregated state
        return await self.validate_all_changes(self.state)
```

### Example 3: Real-time Monitoring System

**Problem**: Monitoring logs from multiple services overflows context.

**Solution**: Streaming with semantic compression.

```python
class LogMonitor:
    def __init__(self):
        self.compressor = SemanticCompressor()
        self.alert_patterns = self.load_patterns()

    async def monitor_streams(self, log_streams):
        compressed_buffer = []

        async for log_entry in self.merge_streams(log_streams):
            # Compress semantically
            compressed = self.compressor.compress_log(log_entry)

            # Keep only recent relevant entries
            compressed_buffer.append(compressed)
            if len(compressed_buffer) > 100:
                compressed_buffer = self.keep_relevant(compressed_buffer)

            # Check for alerts without full context
            if self.matches_alert_pattern(compressed):
                await self.handle_alert(compressed, compressed_buffer[-10:])
```

## Troubleshooting

### Context Overflow
```python
# Implement automatic context pruning
class ContextPruner:
    def prune_on_overflow(self, context, max_tokens):
        while self.count_tokens(context) > max_tokens:
            # Remove least recently used items
            context = self.remove_oldest_item(context)
        return context
```

### Performance Degradation
```python
# Monitor and adapt optimization strategy
class AdaptiveOptimizer:
    def monitor_performance(self):
        if self.response_time > self.threshold:
            self.increase_delegation()
        if self.accuracy < self.minimum:
            self.decrease_compression()
```

### Delegation Failures
```python
# Implement fallback strategies
class DelegationManager:
    async def delegate_with_fallback(self, task, primary_agent):
        try:
            return await primary_agent.execute(task)
        except Exception:
            # Fall back to general agent with more context
            return await self.general_agent.execute(
                task,
                context=self.get_full_context()
            )
```

## Related Skills

- **Agent Builder**: Create specialized agents for delegation
- **Prompt Engineer**: Optimize prompts for efficiency
- **Workflow Designer**: Design efficient workflows
- **Integration Specialist**: Implement MCP and tool integrations
- **Testing Strategist**: Validate optimization effectiveness

## Key Principles

1. **Measure First**: Always measure before optimizing
2. **Preserve Quality**: Don't sacrifice accuracy for efficiency
3. **Progressive Optimization**: Start with easy wins
4. **Monitor Continuously**: Track metrics in production
5. **Adapt Dynamically**: Adjust strategy based on task

---

*This skill is derived from the "Elite Context Engineering" module of the Agentic Horizon course, providing battle-tested techniques for optimizing agentic systems.*
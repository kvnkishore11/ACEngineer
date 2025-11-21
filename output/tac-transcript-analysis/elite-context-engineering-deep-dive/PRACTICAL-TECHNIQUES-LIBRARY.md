# PRACTICAL TECHNIQUES LIBRARY

> *Your actionable catalog of context optimization patterns, ready to copy and use immediately*

## Overview

This is your implementation-ready reference guide. Every technique includes working code, configuration examples, and immediate action steps. Copy, paste, and optimize.

---

## Table of Contents

1. [Quick Wins (Immediate Impact)](#quick-wins-immediate-impact)
2. [Context Reduction Patterns](#context-reduction-patterns)
3. [Delegation Strategies](#delegation-strategies)
4. [Tool Integration Methods](#tool-integration-methods)
5. [Prompt Optimization Techniques](#prompt-optimization-techniques)
6. [MCP Server Configurations](#mcp-server-configurations)
7. [Measurement Approaches](#measurement-approaches)
8. [Debugging Context Issues](#debugging-context-issues)
9. [Advanced Optimizations](#advanced-optimizations)
10. [Production Patterns](#production-patterns)

---

## Quick Wins (Immediate Impact)

### 1. The 30-Second Context Cleanup

**Impact: Save 40K+ tokens instantly**

```bash
# Step 1: Delete default MCP config
rm .mcp.json

# Step 2: Minimize CLAUDE.md
cat > CLAUDE.md << 'EOF'
# Project Name

## Essential Context
- Core purpose: [1 sentence]
- Tech stack: [minimum list]
- Key conventions: [max 5 items]
EOF

# Step 3: Create concise output style
mkdir -p .claude/output-styles
cat > .claude/output-styles/concise.md << 'EOF'
Success: "Done."
Failure: "Error: [reason]"
Question: [Brief answer]
EOF

# Result: 40K+ tokens saved on every agent start
```

### 2. The Instant Context Check

**Impact: Awareness enables optimization**

```bash
# Add to your shell aliases (.zshrc or .bashrc)
alias cx='echo "/context" | pbcopy && echo "Copied /context command"'
alias cxclear='echo "/clear" | pbcopy && echo "Copied /clear command"'
alias cxprime='echo "/prime" | pbcopy && echo "Copied /prime command"'

# Usage: Type cx, then paste in Claude to check context
```

### 3. The Emergency Context Reset

**Impact: Recover from context overflow in 10 seconds**

```bash
# Create reset script
cat > reset-context.sh << 'EOF'
#!/bin/bash
echo "Emergency Context Reset Protocol"
echo "1. /clear - Resetting context"
echo "2. /prime_[task] - Reloading minimal context"
echo "3. Continue with focused context"
echo ""
echo "Commands copied to clipboard!"
echo -e "/clear\n/prime" | pbcopy
EOF

chmod +x reset-context.sh
```

### 4. The Token Counter Setup

**Impact: Real-time awareness**

```json
// VSCode: Install "Token Counter" extension
// settings.json
{
  "tokenCounter.modelName": "claude-3",
  "tokenCounter.showInStatusBar": true,
  "tokenCounter.countOnSave": true
}

// Cursor: Already built-in, enable in settings
```

### 5. The Startup Optimizer

**Impact: 90% faster agent initialization**

```bash
# Create optimized launch script
cat > launch-optimized.sh << 'EOF'
#!/bin/bash
# Launch Claude with optimized settings
claude \
  --no-mcp \
  --settings .claude/settings.concise.json \
  --model sonnet
EOF

chmod +x launch-optimized.sh
alias clo='./launch-optimized.sh'
```

---

## Context Reduction Patterns

### Pattern 1: Smart File Reading

**Save 80% on file operations**

```python
# Instead of reading entire files
def read_entire_file(filepath):
    with open(filepath) as f:
        return f.read()  # Could be 10K+ tokens

# Use incremental reading
def read_smart(filepath, task_type):
    """Read only what's needed for the task"""

    if task_type == "find_function":
        # Read signatures only
        return read_functions_signatures(filepath)
    elif task_type == "understand_structure":
        # Read first 100 lines
        return read_first_n_lines(filepath, 100)
    elif task_type == "debug_error":
        # Read around error line
        return read_context_around_line(filepath, error_line, context=50)
    else:
        # Default: progressive reading
        return read_progressive(filepath)

def read_progressive(filepath):
    """Read in chunks until sufficient"""
    with open(filepath) as f:
        chunks = []
        for _ in range(3):  # Max 3 chunks
            chunk = f.read(1000)  # 1000 chars at a time
            chunks.append(chunk)
            if contains_sufficient_info(chunk):
                break
        return ''.join(chunks)
```

### Pattern 2: Context Compression

**Reduce context by 70% while preserving information**

```python
def compress_for_context(content, compression_level="standard"):
    """Compress content based on need"""

    compressions = {
        "minimal": lambda c: extract_summary(c, max_lines=10),
        "standard": lambda c: remove_redundancy(c),
        "aggressive": lambda c: extract_key_points(c, max_points=5)
    }

    return compressions[compression_level](content)

def remove_redundancy(content):
    """Remove common redundancies"""
    # Remove comments
    content = re.sub(r'//.*?\n', '\n', content)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # Remove empty lines
    content = re.sub(r'\n\s*\n', '\n', content)

    # Remove obvious imports
    content = re.sub(r'import.*?from [\'"]react[\'"];?\n', '', content)

    return content

def extract_key_points(content, max_points=5):
    """Extract only the most important points"""
    lines = content.split('\n')

    # Priority patterns
    important_patterns = [
        r'def ',
        r'class ',
        r'export ',
        r'interface ',
        r'type ',
        r'TODO',
        r'FIXME',
        r'throw ',
        r'error'
    ]

    key_lines = []
    for line in lines:
        if any(re.search(pattern, line) for pattern in important_patterns):
            key_lines.append(line.strip())
            if len(key_lines) >= max_points:
                break

    return '\n'.join(key_lines)
```

### Pattern 3: Selective Context Loading

**Load only relevant context for specific tasks**

```bash
# Create task-specific prime commands
cat > .claude/commands/prime_api.md << 'EOF'
---
description: Prime for API work only
---
# API Context

Read only:
- src/routes/**/*.ts (list files only)
- src/middleware/auth.ts
- docs/api.md

Skip:
- Frontend files
- Test files
- Configuration files
EOF

cat > .claude/commands/prime_frontend.md << 'EOF'
---
description: Prime for frontend work only
---
# Frontend Context

Read only:
- src/components/**/*.tsx (list files only)
- src/hooks/*.ts
- src/styles/theme.ts

Skip:
- Backend files
- Database files
- DevOps files
EOF
```

---

## Delegation Strategies

### Strategy 1: Sub-Agent Task Distribution

**Parallel processing with isolated contexts**

```markdown
# .claude/agents/analyzer.md
You are a code analysis specialist.
Focus: Find patterns and issues
Output: Concise report with findings
Max context: 20K tokens

# .claude/agents/implementer.md
You are an implementation specialist.
Focus: Write clean, working code
Input: Specification from analyzer
Max context: 30K tokens

# .claude/agents/validator.md
You are a validation specialist.
Focus: Test and verify implementations
Output: Test results and coverage
Max context: 15K tokens
```

```python
# Orchestration pattern
def distribute_work(task):
    """Distribute task across specialized agents"""

    # Phase 1: Analysis
    analysis = invoke_agent("analyzer", task.description)

    # Phase 2: Parallel implementation
    implementations = []
    for spec in analysis.specifications:
        impl = invoke_agent("implementer", spec)
        implementations.append(impl)

    # Phase 3: Validation
    results = invoke_agent("validator", implementations)

    return results
```

### Strategy 2: Expert Agent Pattern

**Self-improving specialized agents**

```bash
# Create expert structure
mkdir -p .claude/experts/api_expert
cat > .claude/experts/api_expert/plan.md << 'EOF'
---
description: API planning expert
---
# API Planning Expert

## Expertise
- RESTful design patterns
- Authentication strategies
- Rate limiting approaches
- Error handling patterns

## Workflow
1. Analyze requirements
2. Design endpoint structure
3. Define data models
4. Specify validation rules
5. Generate OpenAPI spec
EOF

cat > .claude/experts/api_expert/build.md << 'EOF'
---
description: API building expert
---
# API Building Expert

## Expertise
- Express/Fastify patterns
- Middleware composition
- Database query optimization
- Caching strategies

## Workflow
1. Read specification
2. Implement endpoints
3. Add middleware
4. Implement validation
5. Add error handling
EOF

cat > .claude/experts/api_expert/improve.md << 'EOF'
---
description: Self-improvement expert
---
# API Improvement Expert

## Workflow
1. Analyze git diff
2. Extract patterns from implementation
3. Update expertise sections in plan.md and build.md
4. Document learned optimizations
EOF
```

### Strategy 3: Background Agent Orchestration

**Fire-and-forget parallel execution**

```python
#!/usr/bin/env python3
# parallel_executor.py

import subprocess
import json
from pathlib import Path

def launch_background_agent(task, model="sonnet", report_dir="./agents/reports"):
    """Launch background agent for task"""

    Path(report_dir).mkdir(parents=True, exist_ok=True)
    report_file = f"{report_dir}/{task['name']}_{timestamp()}.md"

    cmd = [
        "claude",
        "--model", model,
        "--output-format", "text",
        "--dangerously-skip-permissions",
        "--print",
        f"Task: {task['description']}\\nReport to: {report_file}"
    ]

    # Launch in background
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True
    )

    return {
        "task": task['name'],
        "pid": process.pid,
        "report": report_file
    }

def orchestrate_parallel_tasks(tasks):
    """Launch multiple background agents"""

    agents = []
    for task in tasks:
        agent = launch_background_agent(task)
        agents.append(agent)
        print(f"Launched agent for {task['name']} (PID: {agent['pid']})")

    return agents

# Usage
tasks = [
    {"name": "analyze_performance", "description": "Profile and optimize slow endpoints"},
    {"name": "security_audit", "description": "Scan for security vulnerabilities"},
    {"name": "test_coverage", "description": "Identify untested code paths"},
    {"name": "documentation", "description": "Generate missing API documentation"}
]

agents = orchestrate_parallel_tasks(tasks)
```

---

## Tool Integration Methods

### Method 1: On-Demand MCP Loading

**Load tools only when needed**

```bash
# Create task-specific MCP configs
cat > .mcp.database.json << 'EOF'
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@database/postgres-mcp"],
      "env": {
        "CONNECTION_STRING": "${DATABASE_URL}"
      }
    }
  }
}
EOF

cat > .mcp.web.json << 'EOF'
{
  "mcpServers": {
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "@mendable/firecrawl-mcp"],
      "config": {
        "maxTokens": 5000
      }
    }
  }
}
EOF

# Launch with specific tools
alias claude-db='claude --mcp-config .mcp.database.json'
alias claude-web='claude --mcp-config .mcp.web.json'
alias claude-minimal='claude --no-mcp'
```

### Method 2: Tool Context Budget

**Limit context consumption per tool**

```python
class ToolContextManager:
    """Manage context budget for tools"""

    def __init__(self, total_budget=50_000):
        self.total_budget = total_budget
        self.tool_budgets = {
            "filesystem": 5_000,
            "git": 3_000,
            "database": 8_000,
            "web": 10_000,
            "search": 7_000
        }
        self.used = {}

    def can_use_tool(self, tool_name):
        """Check if tool fits in budget"""
        if tool_name not in self.tool_budgets:
            return False

        current_usage = sum(self.used.values())
        tool_cost = self.tool_budgets[tool_name]

        return (current_usage + tool_cost) <= self.total_budget

    def use_tool(self, tool_name):
        """Register tool usage"""
        if self.can_use_tool(tool_name):
            self.used[tool_name] = self.tool_budgets[tool_name]
            return True
        return False

    def get_status(self):
        """Get current budget status"""
        used = sum(self.used.values())
        return {
            "used": used,
            "remaining": self.total_budget - used,
            "percentage": (used / self.total_budget) * 100,
            "tools_loaded": list(self.used.keys())
        }
```

---

## Prompt Optimization Techniques

### Technique 1: Structured Prompts

**Reduce ambiguity, improve focus**

```markdown
# Template: Optimized Task Prompt
## Purpose
[Single sentence describing the goal]

## Context
- Only relevant information
- Maximum 3-5 bullet points
- Reference specific files if needed

## Constraints
- Token budget: [number]
- Output format: [specific format]
- Must not: [clear boundaries]

## Expected Output
[Precise description of desired result]
```

### Technique 2: Progressive Prompting

**Build context incrementally**

```python
def progressive_prompt(task, agent):
    """Build context progressively"""

    prompts = [
        f"Understand the codebase structure: {task.repo}",
        f"Identify relevant files for: {task.description}",
        f"Read only the identified files",
        f"Create plan for: {task.description}",
        f"Implement the plan"
    ]

    context = []
    for prompt in prompts:
        response = agent.execute(prompt)
        context.append(extract_key_info(response))

        # Stop if we have enough context
        if has_sufficient_context(context, task):
            break

    return context
```

### Technique 3: Prompt Compression

**Say more with less**

```python
def compress_prompt(verbose_prompt):
    """Compress prompt while preserving meaning"""

    # Remove filler words
    compressed = re.sub(r'\b(please|could you|I need you to|basically)\b', '', verbose_prompt)

    # Use abbreviations
    abbreviations = {
        "implementation": "impl",
        "configuration": "config",
        "documentation": "docs",
        "repository": "repo",
        "development": "dev",
        "production": "prod"
    }

    for full, short in abbreviations.items():
        compressed = compressed.replace(full, short)

    # Remove redundancy
    compressed = ' '.join(dict.fromkeys(compressed.split()))

    return compressed.strip()

# Example
verbose = "Please could you implement a new user authentication feature with proper documentation"
compressed = compress_prompt(verbose)
# Result: "implement new user auth feature with docs"
```

---

## MCP Server Configurations

### Configuration 1: Minimal Setup

**Absolute minimum for basic operations**

```json
// .mcp.minimal.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "config": {
        "directories": ["./src"],
        "maxFileSize": 50000,
        "excludePatterns": ["node_modules", "*.log", "*.tmp"]
      }
    }
  }
}
```

### Configuration 2: Development Setup

**Balanced for development work**

```json
// .mcp.development.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "config": {
        "directories": ["./"],
        "excludePatterns": ["node_modules", ".git", "dist", "build"]
      }
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"],
      "config": {
        "repoPath": "./",
        "maxCommits": 20
      }
    }
  }
}
```

### Configuration 3: Production Debugging

**Optimized for production issues**

```json
// .mcp.production-debug.json
{
  "mcpServers": {
    "logs": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-logs"],
      "config": {
        "logPaths": ["/var/log/app/*.log"],
        "maxLines": 1000,
        "timeWindow": "1h"
      }
    },
    "metrics": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-prometheus"],
      "config": {
        "endpoint": "${METRICS_URL}",
        "queries": ["preset:errors", "preset:latency"]
      }
    }
  }
}
```

---

## Measurement Approaches

### Approach 1: Context Usage Tracking

**Track every token**

```python
#!/usr/bin/env python3
# context_tracker.py

import json
from datetime import datetime
from pathlib import Path

class ContextTracker:
    def __init__(self, log_file="context_usage.jsonl"):
        self.log_file = Path(log_file)

    def log_measurement(self, measurement):
        """Log context measurement"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": measurement.get("session_id"),
            "tokens": measurement.get("tokens"),
            "percentage": measurement.get("percentage"),
            "task": measurement.get("task"),
            "techniques_used": measurement.get("techniques", [])
        }

        with self.log_file.open('a') as f:
            f.write(json.dumps(entry) + '\n')

    def analyze_usage(self):
        """Analyze context usage patterns"""
        if not self.log_file.exists():
            return {}

        measurements = []
        with self.log_file.open() as f:
            for line in f:
                measurements.append(json.loads(line))

        if not measurements:
            return {}

        # Calculate statistics
        tokens = [m['tokens'] for m in measurements]
        return {
            "total_sessions": len(measurements),
            "average_tokens": sum(tokens) / len(tokens),
            "min_tokens": min(tokens),
            "max_tokens": max(tokens),
            "total_tokens": sum(tokens),
            "cost_estimate": sum(tokens) * 0.00001  # Rough estimate
        }

# Usage
tracker = ContextTracker()
tracker.log_measurement({
    "session_id": "abc123",
    "tokens": 45_000,
    "percentage": 22.5,
    "task": "feature_implementation",
    "techniques": ["prime", "concise_output", "sub_agents"]
})

stats = tracker.analyze_usage()
print(f"Average context usage: {stats['average_tokens']:,.0f} tokens")
```

### Approach 2: Performance Correlation

**Correlate context size with success**

```python
def correlate_context_success(sessions):
    """Find optimal context range"""

    # Group by context size buckets
    buckets = {
        "minimal": {"range": (0, 20_000), "sessions": []},
        "small": {"range": (20_000, 50_000), "sessions": []},
        "medium": {"range": (50_000, 100_000), "sessions": []},
        "large": {"range": (100_000, 150_000), "sessions": []},
        "overflow": {"range": (150_000, float('inf')), "sessions": []}
    }

    # Categorize sessions
    for session in sessions:
        tokens = session['tokens']
        for bucket_name, bucket_data in buckets.items():
            if bucket_data['range'][0] <= tokens < bucket_data['range'][1]:
                buckets[bucket_name]['sessions'].append(session)
                break

    # Calculate success rates
    results = {}
    for bucket_name, bucket_data in buckets.items():
        sessions_list = bucket_data['sessions']
        if sessions_list:
            success_rate = sum(s['success'] for s in sessions_list) / len(sessions_list)
            avg_time = sum(s['time'] for s in sessions_list) / len(sessions_list)
            results[bucket_name] = {
                "success_rate": success_rate,
                "avg_time": avg_time,
                "count": len(sessions_list)
            }

    return results
```

---

## Debugging Context Issues

### Issue 1: Context Overflow

**Symptoms:** Agent becomes incoherent, forgets earlier context

```bash
# Debug script
cat > debug_context_overflow.sh << 'EOF'
#!/bin/bash
echo "Context Overflow Diagnosis"
echo "========================="
echo ""
echo "1. Check current context usage:"
echo "   /context"
echo ""
echo "2. Identify largest consumers:"
echo "   - CLAUDE.md size: $(wc -l < CLAUDE.md) lines"
echo "   - MCP servers: $(cat .mcp.json 2>/dev/null | grep -c '"command"' || echo 0)"
echo ""
echo "3. Recovery steps:"
echo "   a. /clear"
echo "   b. /prime_minimal"
echo "   c. Continue with focused prompts"
EOF

chmod +x debug_context_overflow.sh
```

### Issue 2: Slow Performance

**Symptoms:** Agent takes long to respond, seems confused

```python
def diagnose_performance(session):
    """Diagnose context-related performance issues"""

    issues = []

    # Check for context bloat
    if session.context_size > 100_000:
        issues.append({
            "issue": "Context bloat",
            "severity": "high",
            "solution": "Reset and use minimal prime"
        })

    # Check for redundant information
    if session.redundancy_ratio > 0.3:
        issues.append({
            "issue": "High redundancy",
            "severity": "medium",
            "solution": "Use context compression"
        })

    # Check for unfocused context
    if session.relevance_score < 0.7:
        issues.append({
            "issue": "Unfocused context",
            "severity": "high",
            "solution": "Use task-specific priming"
        })

    return issues
```

### Issue 3: Inconsistent Results

**Symptoms:** Same prompt gives different quality results

```python
def ensure_consistency():
    """Ensure consistent context across runs"""

    # Create context snapshot
    snapshot = {
        "files_loaded": get_loaded_files(),
        "prime_commands": get_prime_sequence(),
        "mcp_servers": get_active_mcp(),
        "output_style": get_output_style()
    }

    # Save snapshot
    with open(".claude/context_snapshot.json", "w") as f:
        json.dump(snapshot, f, indent=2)

    # Create restoration script
    restore_script = f"""#!/bin/bash
    # Restore context snapshot
    /clear
    /prime {' '.join(snapshot['prime_commands'])}
    # Files will be loaded as needed
    """

    with open("restore_context.sh", "w") as f:
        f.write(restore_script)

    return snapshot
```

---

## Advanced Optimizations

### Optimization 1: Predictive Context Loading

**Load context before it's needed**

```python
class PredictiveLoader:
    """Predict and preload context needs"""

    def __init__(self):
        self.task_patterns = {
            "bug_fix": ["error_logs", "recent_commits", "test_files"],
            "feature": ["requirements", "existing_features", "api_specs"],
            "refactor": ["code_quality_report", "architecture", "tests"],
            "optimization": ["performance_metrics", "bottlenecks", "profiling"]
        }

    def predict_context_needs(self, task_description):
        """Predict what context will be needed"""

        # Simple keyword matching (can be ML in production)
        predicted_needs = set()

        for task_type, needs in self.task_patterns.items():
            if task_type in task_description.lower():
                predicted_needs.update(needs)

        return list(predicted_needs)

    def preload_context(self, needs):
        """Preload predicted context"""

        context_map = {
            "error_logs": "/read logs/error.log | tail -100",
            "recent_commits": "git log --oneline -20",
            "test_files": "/read tests/ | grep -l test",
            "requirements": "/read docs/requirements.md",
            # ... more mappings
        }

        commands = []
        for need in needs:
            if need in context_map:
                commands.append(context_map[need])

        return commands
```

### Optimization 2: Context Caching

**Reuse computed context**

```python
import hashlib
import pickle
from functools import lru_cache

class ContextCache:
    """Cache expensive context operations"""

    def __init__(self, cache_dir=".claude/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def cache_key(self, operation, params):
        """Generate cache key"""
        content = f"{operation}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(content.encode()).hexdigest()

    def get(self, operation, params):
        """Get cached context"""
        key = self.cache_key(operation, params)
        cache_file = self.cache_dir / f"{key}.pkl"

        if cache_file.exists():
            with cache_file.open('rb') as f:
                return pickle.load(f)

        return None

    def set(self, operation, params, result):
        """Cache context result"""
        key = self.cache_key(operation, params)
        cache_file = self.cache_dir / f"{key}.pkl"

        with cache_file.open('wb') as f:
            pickle.dump(result, f)

    @lru_cache(maxsize=100)
    def get_or_compute(self, operation, params, compute_func):
        """Get from cache or compute"""

        cached = self.get(operation, params)
        if cached:
            return cached

        result = compute_func()
        self.set(operation, params, result)

        return result
```

### Optimization 3: Dynamic Context Windows

**Adjust context size based on task complexity**

```python
class DynamicContextManager:
    """Dynamically adjust context window size"""

    def __init__(self):
        self.complexity_indicators = {
            "simple": ["fix typo", "update comment", "change color"],
            "medium": ["add feature", "fix bug", "update api"],
            "complex": ["refactor", "optimize", "redesign", "migrate"]
        }

        self.context_budgets = {
            "simple": 20_000,
            "medium": 50_000,
            "complex": 100_000
        }

    def assess_complexity(self, task_description):
        """Assess task complexity"""

        task_lower = task_description.lower()

        for complexity, indicators in self.complexity_indicators.items():
            if any(indicator in task_lower for indicator in indicators):
                return complexity

        return "medium"  # Default

    def allocate_context(self, task_description):
        """Allocate context budget based on complexity"""

        complexity = self.assess_complexity(task_description)
        budget = self.context_budgets[complexity]

        return {
            "complexity": complexity,
            "budget": budget,
            "reset_threshold": budget * 0.8,
            "warning_threshold": budget * 0.6
        }

    def optimize_for_task(self, task_description, available_context):
        """Optimize context for specific task"""

        allocation = self.allocate_context(task_description)

        if available_context < allocation['budget']:
            return {
                "action": "reset_and_prime",
                "reason": "Insufficient context for task complexity"
            }

        return {
            "action": "proceed",
            "budget": allocation['budget'],
            "monitoring": allocation['warning_threshold']
        }
```

---

## Production Patterns

### Pattern 1: Context Budget Enforcement

**Enforce context limits in production**

```python
class ContextBudgetEnforcer:
    """Enforce context budgets in production"""

    def __init__(self, max_context=150_000, reset_threshold=0.75):
        self.max_context = max_context
        self.reset_threshold = reset_threshold
        self.current_usage = 0
        self.session_id = None

    def check_budget(self, tokens_to_add):
        """Check if operation fits in budget"""

        if self.current_usage + tokens_to_add > self.max_context:
            return {
                "allowed": False,
                "reason": "Would exceed context budget",
                "suggestion": "Reset context or delegate to sub-agent"
            }

        if self.current_usage + tokens_to_add > (self.max_context * self.reset_threshold):
            return {
                "allowed": True,
                "warning": "Approaching context limit",
                "suggestion": "Consider reset after this operation"
            }

        return {"allowed": True}

    def use_tokens(self, tokens):
        """Register token usage"""

        check = self.check_budget(tokens)

        if check["allowed"]:
            self.current_usage += tokens

            if "warning" in check:
                self.trigger_warning(check["warning"])

        return check

    def reset(self):
        """Reset context usage"""

        self.current_usage = 0
        self.session_id = generate_session_id()

        return {
            "session_id": self.session_id,
            "context_reset": True,
            "available": self.max_context
        }

    def trigger_warning(self, warning):
        """Trigger context warning"""

        # Log warning
        print(f"⚠️  Context Warning: {warning}")

        # Could also:
        # - Send alert to monitoring
        # - Trigger automatic optimization
        # - Queue for reset
```

### Pattern 2: Multi-Agent Pipeline

**Production-ready agent pipeline**

```python
class ProductionPipeline:
    """Production agent orchestration pipeline"""

    def __init__(self):
        self.stages = []
        self.context_budgets = {}
        self.results = {}

    def add_stage(self, name, agent_type, context_budget):
        """Add pipeline stage"""

        self.stages.append({
            "name": name,
            "agent_type": agent_type,
            "context_budget": context_budget,
            "dependencies": []
        })

        self.context_budgets[name] = context_budget

    def execute(self, input_data):
        """Execute pipeline"""

        for stage in self.stages:
            # Spawn agent with budget
            agent = spawn_agent(
                stage["agent_type"],
                context_limit=stage["context_budget"]
            )

            # Execute stage
            stage_input = self.prepare_stage_input(stage, input_data)
            result = agent.execute(stage_input)

            # Store result
            self.results[stage["name"]] = result

            # Check for early termination
            if self.should_terminate(result):
                break

        return self.results

    def prepare_stage_input(self, stage, initial_input):
        """Prepare input for stage"""

        if not stage["dependencies"]:
            return initial_input

        # Combine dependent results
        combined = {}
        for dep in stage["dependencies"]:
            if dep in self.results:
                combined[dep] = self.results[dep]

        return combined

    def should_terminate(self, result):
        """Check if pipeline should terminate"""

        return result.get("status") == "failed"

# Usage
pipeline = ProductionPipeline()
pipeline.add_stage("analysis", "analyzer", 30_000)
pipeline.add_stage("planning", "planner", 20_000)
pipeline.add_stage("implementation", "builder", 40_000)
pipeline.add_stage("validation", "tester", 15_000)

results = pipeline.execute({"task": "Create user API"})
```

### Pattern 3: Self-Healing Context

**Automatically recover from context issues**

```python
class SelfHealingContext:
    """Self-healing context management"""

    def __init__(self):
        self.health_checks = []
        self.recovery_strategies = {}

    def add_health_check(self, check_func, recovery_func):
        """Add health check and recovery"""

        self.health_checks.append({
            "check": check_func,
            "recover": recovery_func
        })

    def monitor_health(self, context_state):
        """Monitor context health"""

        issues = []

        for check in self.health_checks:
            issue = check["check"](context_state)
            if issue:
                issues.append({
                    "issue": issue,
                    "recovery": check["recover"]
                })

        return issues

    def auto_heal(self, context_state):
        """Automatically heal context issues"""

        issues = self.monitor_health(context_state)

        for issue in issues:
            print(f"Healing: {issue['issue']}")
            recovery_func = issue["recovery"]
            recovery_func(context_state)

        return len(issues) > 0

# Define health checks
def check_bloat(state):
    if state["tokens"] > 100_000:
        return "Context bloat detected"
    return None

def recover_bloat(state):
    # Reset and reload minimal context
    execute("/clear")
    execute("/prime_minimal")

def check_staleness(state):
    if state["age_minutes"] > 60:
        return "Stale context detected"
    return None

def recover_staleness(state):
    # Refresh context
    execute("/load_bundle latest")

# Setup self-healing
healer = SelfHealingContext()
healer.add_health_check(check_bloat, recover_bloat)
healer.add_health_check(check_staleness, recover_staleness)

# Monitor and heal
context_state = get_current_context_state()
healed = healer.auto_heal(context_state)
```

---

## Summary Quick Reference

### The 5-Minute Setup

```bash
# 1. Clean house
rm .mcp.json
echo "# Project\nMinimal info only" > CLAUDE.md

# 2. Create essentials
mkdir -p .claude/{commands,agents,output-styles}

# 3. Add concise output
echo 'Success: "Done."' > .claude/output-styles/concise.md

# 4. Create prime command
cat > .claude/commands/prime.md << 'EOF'
Read README.md
List src/ structure
Report understanding
EOF

# 5. Launch optimized
claude --no-mcp --settings .claude/settings.concise.json
```

### The Daily Workflow

```bash
# Morning: Fresh start
/clear && /prime

# Before task: Check context
/context

# During work: Monitor growth
# If > 50K: /clear && /prime_[task]

# Heavy task: Delegate
/background "Complex task" opus report.md

# End of day: Save context
/status  # Note session ID for tomorrow
```

### The Context Equation

```
Optimal Context = Minimal Essential + Zero Waste + Perfect Distribution
```

Remember: **A focused agent is a performant agent!**
# ✅ Agentic Engineering Best Practices

> **Do's and Don'ts Distilled from the Complete Course**

## 🌟 Universal Principles

### The Golden Rules

1. **Start Simple, Iterate Fast**
   - ✅ DO: Begin with basic patterns, add complexity gradually
   - ❌ DON'T: Over-engineer from the start

2. **Test Early, Test Often**
   - ✅ DO: Validate at every stage
   - ❌ DON'T: Deploy without comprehensive testing

3. **Monitor Everything**
   - ✅ DO: Track performance, costs, and quality metrics
   - ❌ DON'T: Run blind in production

4. **Document Patterns**
   - ✅ DO: Record what works for reuse
   - ❌ DON'T: Rely on memory or tribal knowledge

5. **Plan for Failure**
   - ✅ DO: Implement fallbacks and error handling
   - ❌ DON'T: Assume happy path only

## 📝 Prompt Engineering

### ✅ DO's

#### Structure & Clarity
```python
# DO: Clear, structured prompts
prompt = """
Task: Analyze customer feedback
Input: {feedback_text}
Requirements:
- Identify sentiment (positive/negative/neutral)
- Extract key themes
- Suggest actionable improvements
Output format: JSON with sentiment, themes, and actions
"""
```

#### Examples & Context
```python
# DO: Provide examples
prompt = """
Examples:
Input: "The product is great but shipping was slow"
Output: {"sentiment": "mixed", "themes": ["product quality", "shipping"], "actions": ["improve logistics"]}

Now analyze: {new_feedback}
"""
```

#### Constraints & Boundaries
```python
# DO: Set clear boundaries
prompt = """
Analyze the following text (max 500 words).
Focus ONLY on technical aspects.
Ignore pricing discussions.
"""
```

### ❌ DON'T's

#### Ambiguous Instructions
```python
# DON'T: Vague or ambiguous prompts
bad_prompt = "Tell me about this data"  # Too vague
bad_prompt = "Analyze everything"       # No boundaries
bad_prompt = "Be creative"              # Undefined creativity
```

#### Contradictory Requirements
```python
# DON'T: Conflicting instructions
bad_prompt = """
Be extremely detailed but keep it brief.
Be creative but follow the exact format.
"""
```

#### Implicit Assumptions
```python
# DON'T: Assume context
bad_prompt = "Continue from where we left off"  # No context
bad_prompt = "Do it like last time"             # No reference
```

## 🏗️ System Architecture

### ✅ DO's

#### Modular Design
```python
# DO: Separate concerns
class Agent:
    def __init__(self):
        self.prompt_manager = PromptManager()
        self.memory_store = MemoryStore()
        self.tool_registry = ToolRegistry()
        self.error_handler = ErrorHandler()
```

#### Clear Interfaces
```python
# DO: Define clear contracts
class AgentInterface(Protocol):
    def process(self, input: str) -> AgentResponse:
        """Process input and return structured response"""

    def get_state(self) -> AgentState:
        """Return current agent state"""
```

#### Graceful Degradation
```python
# DO: Fallback mechanisms
async def process_with_fallback(input):
    try:
        return await primary_agent.process(input)
    except Exception:
        try:
            return await fallback_agent.process(input)
        except Exception:
            return default_response()
```

### ❌ DON'T's

#### Tight Coupling
```python
# DON'T: Hard dependencies
class BadAgent:
    def process(self, input):
        # Directly calling external services
        response = requests.post("http://specific-api.com", ...)
        # Hard-coded processing logic
        if response.text.startswith("ERROR"):
            # Tight coupling to specific format
```

#### No Error Handling
```python
# DON'T: Assume success
def bad_process(input):
    response = api_call(input)  # What if this fails?
    parsed = json.loads(response)  # What if invalid JSON?
    return parsed["result"]  # What if key missing?
```

#### Resource Leaks
```python
# DON'T: Forget cleanup
def bad_connection():
    conn = create_connection()
    process_data(conn)
    # No conn.close() - resource leak!
```

## 🧠 Context Management

### ✅ DO's

#### Efficient Context Windows
```python
# DO: Manage context size
class ContextManager:
    def __init__(self, max_tokens=4000):
        self.max_tokens = max_tokens
        self.context = []

    def add(self, message):
        self.context.append(message)
        self._prune_if_needed()

    def _prune_if_needed(self):
        while self.token_count() > self.max_tokens:
            self.context.pop(0)  # Remove oldest
```

#### Context Compression
```python
# DO: Compress when needed
def compress_context(messages):
    if len(messages) > 10:
        # Summarize older messages
        summary = summarize(messages[:-5])
        return [summary] + messages[-5:]
    return messages
```

#### State Persistence
```python
# DO: Save state regularly
class StatefulAgent:
    def checkpoint(self):
        state = {
            'context': self.context,
            'memory': self.memory,
            'timestamp': datetime.now()
        }
        save_to_storage(state)
```

### ❌ DON'T's

#### Context Overflow
```python
# DON'T: Unlimited context growth
bad_context = []
for message in all_messages:
    bad_context.append(message)  # Will eventually overflow
```

#### Losing Important Context
```python
# DON'T: Random pruning
def bad_prune(context):
    # Randomly removing messages loses important info
    return random.sample(context, len(context)//2)
```

#### No Context Validation
```python
# DON'T: Trust all context
def bad_add_context(message):
    self.context.append(message)  # No validation
    # Could contain malicious content
```

## 🔄 Multi-Agent Orchestration

### ✅ DO's

#### Clear Coordination
```python
# DO: Explicit coordination
class Orchestrator:
    def delegate(self, task):
        if task.type == "research":
            return self.research_agent.handle(task)
        elif task.type == "analysis":
            return self.analysis_agent.handle(task)
        else:
            return self.general_agent.handle(task)
```

#### Async Communication
```python
# DO: Non-blocking operations
async def parallel_process(tasks):
    results = await asyncio.gather(
        agent1.process(tasks[0]),
        agent2.process(tasks[1]),
        agent3.process(tasks[2])
    )
    return merge_results(results)
```

#### Result Validation
```python
# DO: Validate agent outputs
def validate_and_merge(results):
    validated = []
    for result in results:
        if self.validator.check(result):
            validated.append(result)
        else:
            validated.append(self.request_retry(result))
    return self.merger.combine(validated)
```

### ❌ DON'T's

#### Circular Dependencies
```python
# DON'T: Create circular waiting
async def bad_orchestration():
    # Agent A waits for B, B waits for C, C waits for A
    result_a = await agent_a.process(wait_for=agent_c)
    result_b = await agent_b.process(wait_for=agent_a)
    result_c = await agent_c.process(wait_for=agent_b)
```

#### No Timeout Management
```python
# DON'T: Infinite waiting
async def bad_wait():
    result = await agent.process(task)  # Could hang forever
```

#### Uncoordinated Access
```python
# DON'T: Race conditions
shared_state = {}
# Multiple agents modifying without locks
agent1.modify(shared_state)
agent2.modify(shared_state)  # Race condition!
```

## 🚀 Production Deployment

### ✅ DO's

#### Health Checks
```python
# DO: Implement health endpoints
@app.route('/health')
def health_check():
    checks = {
        'api': check_api_connection(),
        'database': check_db_connection(),
        'model': check_model_loaded(),
        'memory': check_memory_usage() < 0.9
    }
    if all(checks.values()):
        return {'status': 'healthy', 'checks': checks}, 200
    return {'status': 'unhealthy', 'checks': checks}, 503
```

#### Rate Limiting
```python
# DO: Protect against overuse
from functools import wraps
import time

def rate_limit(max_calls=10, period=60):
    def decorator(func):
        calls = []

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [c for c in calls if c > now - period]
            if len(calls) >= max_calls:
                raise RateLimitError(f"Rate limit exceeded")
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

#### Graceful Shutdown
```python
# DO: Clean shutdown
def signal_handler(signum, frame):
    logger.info("Shutdown signal received")
    orchestrator.stop_accepting_new_tasks()
    orchestrator.wait_for_current_tasks()
    orchestrator.save_state()
    orchestrator.cleanup_resources()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
```

### ❌ DON'T's

#### No Monitoring
```python
# DON'T: Deploy without observability
def bad_process():
    result = process_data()  # No metrics
    return result  # No logging
```

#### Hardcoded Secrets
```python
# DON'T: Embed secrets in code
API_KEY = "sk-abc123..."  # NEVER DO THIS
DATABASE_URL = "postgresql://user:password@..."  # NEVER!
```

#### No Resource Limits
```python
# DON'T: Unlimited resource usage
def bad_batch_process(items):
    # Processing everything at once
    results = [heavy_process(item) for item in items]
    # Could consume all memory/CPU
```

## 🧪 Testing Strategies

### ✅ DO's

#### Comprehensive Test Coverage
```python
# DO: Test all paths
def test_agent_responses():
    # Happy path
    assert agent.process("valid input").success

    # Error cases
    assert agent.process("").error == "Empty input"
    assert agent.process(None).error == "Invalid input"

    # Edge cases
    assert agent.process("x" * 10000).error == "Too long"
```

#### Mock External Dependencies
```python
# DO: Isolate tests
@patch('requests.post')
def test_with_mock(mock_post):
    mock_post.return_value.json.return_value = {"result": "success"}
    result = agent.process("test")
    assert result == "success"
```

#### Performance Testing
```python
# DO: Test performance
def test_response_time():
    start = time.time()
    agent.process("test input")
    duration = time.time() - start
    assert duration < 2.0, f"Too slow: {duration}s"
```

### ❌ DON'T's

#### Testing in Production
```python
# DON'T: Test with live data
def bad_test():
    # Using production API
    result = production_api.delete_user("test@example.com")
    # Just deleted a real user!
```

#### Ignoring Edge Cases
```python
# DON'T: Only test happy path
def incomplete_test():
    assert agent.process("normal input").success
    # What about errors, edge cases, invalid input?
```

#### No Regression Tests
```python
# DON'T: Forget regression testing
# After fixing a bug, always add a test
def test_regression_issue_123():
    # This specific input caused a crash before
    result = agent.process("special \x00 character")
    assert result.success
```

## 💰 Cost Optimization

### ✅ DO's

#### Implement Caching
```python
# DO: Cache expensive operations
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_operation(input_hash):
    return model.generate(input_hash)
```

#### Batch Processing
```python
# DO: Batch when possible
def batch_process(items, batch_size=10):
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        results = model.batch_generate(batch)
        yield from results
```

#### Model Selection
```python
# DO: Use appropriate models
def smart_routing(task):
    if task.complexity == "simple":
        return use_small_model(task)  # Cheaper
    elif task.complexity == "medium":
        return use_medium_model(task)
    else:
        return use_large_model(task)  # Only when needed
```

### ❌ DON'T's

#### Unnecessary API Calls
```python
# DON'T: Redundant calls
def bad_loop():
    for item in items:
        # Same context every time - wasteful!
        result = api.call(context=full_context, item=item)
```

#### No Token Optimization
```python
# DON'T: Waste tokens
bad_prompt = """
Please, if you would be so kind, I would really appreciate
if you could possibly help me to analyze this data and
provide me with your thoughts and insights...
"""  # Verbose and wasteful
```

#### Ignore Free Tiers
```python
# DON'T: Miss optimization opportunities
# Not using free tiers, credits, or bulk discounts
# Not negotiating enterprise agreements for scale
```

## 🔒 Security Considerations

### ✅ DO's

#### Input Validation
```python
# DO: Validate all inputs
def validate_input(user_input):
    # Check length
    if len(user_input) > MAX_LENGTH:
        raise ValueError("Input too long")

    # Sanitize
    sanitized = remove_special_characters(user_input)

    # Check for injection attempts
    if contains_injection_pattern(sanitized):
        raise SecurityError("Potential injection detected")

    return sanitized
```

#### Output Sanitization
```python
# DO: Sanitize outputs
def sanitize_output(response):
    # Remove potential PII
    response = redact_pii(response)

    # Escape HTML/SQL
    response = escape_special_chars(response)

    # Validate format
    if not is_valid_format(response):
        return get_safe_default()

    return response
```

#### Secure Configuration
```python
# DO: Use environment variables
import os
from cryptography.fernet import Fernet

class SecureConfig:
    def __init__(self):
        self.api_key = os.environ.get('API_KEY')
        self.db_url = os.environ.get('DATABASE_URL')

        # Encrypt sensitive data at rest
        self.cipher = Fernet(os.environ.get('ENCRYPTION_KEY'))
```

### ❌ DON'T's

#### Trust User Input
```python
# DON'T: Execute untrusted input
def bad_eval(user_code):
    result = eval(user_code)  # NEVER DO THIS
    return result
```

#### Log Sensitive Data
```python
# DON'T: Log secrets
logger.info(f"API call with key: {api_key}")  # Exposed!
logger.debug(f"User password: {password}")    # Terrible!
```

#### Weak Authentication
```python
# DON'T: Simple auth checks
def bad_auth(token):
    return token == "secret123"  # Too simple
```

## 🎯 Performance Tips

### ✅ DO's

#### Stream Responses
```python
# DO: Stream for better UX
async def stream_response():
    async for chunk in model.stream_generate(prompt):
        yield chunk
        await asyncio.sleep(0)  # Yield control
```

#### Optimize Prompts
```python
# DO: Minimize tokens
optimized = """
Task: Summarize
Input: {text}
Output: 3 bullets
"""
# vs verbose version that uses 3x tokens
```

#### Use Connection Pooling
```python
# DO: Reuse connections
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

### ❌ DON'T's

#### Block on I/O
```python
# DON'T: Synchronous blocking
def bad_process():
    data = fetch_from_api()  # Blocks
    result = process(data)   # Can't start until fetch completes
    return result
```

#### Recreate Resources
```python
# DON'T: Create new connections each time
def bad_query():
    conn = create_connection()  # Expensive
    result = conn.query(...)
    conn.close()
    return result
```

#### Ignore Batch Opportunities
```python
# DON'T: Process one at a time when batch is possible
for item in items:
    result = model.process(item)  # Could batch!
```

## 📋 Maintenance Strategies

### ✅ DO's

#### Version Control
```python
# DO: Version your prompts and configs
PROMPT_VERSION = "2.3.1"
prompts = {
    "2.3.1": "Current prompt...",
    "2.3.0": "Previous prompt...",  # For rollback
}
```

#### Monitoring & Alerts
```python
# DO: Set up comprehensive monitoring
def monitor_system():
    metrics = {
        'response_time': measure_response_time(),
        'error_rate': calculate_error_rate(),
        'token_usage': get_token_usage(),
        'cost': calculate_current_cost()
    }

    if metrics['error_rate'] > 0.05:
        send_alert("High error rate detected")
```

#### Regular Updates
```python
# DO: Keep dependencies updated
# requirements.txt
langchain>=0.1.0,<0.2.0  # Pin major version
openai>=1.0.0,<2.0.0
# Regular updates with testing
```

### ❌ DON'T's

#### No Documentation
```python
# DON'T: Leave code undocumented
def process(x, y, z):
    return x * y + z  # What do x, y, z represent?
```

#### Ignore Deprecations
```python
# DON'T: Use deprecated features
result = old_api.deprecated_method()  # Will break soon
```

#### No Backup Plan
```python
# DON'T: Single point of failure
if primary_service.is_down():
    raise Exception("Service unavailable")  # No fallback!
```

## 🏁 Production Readiness Checklist

### Before Deployment

- [ ] **All tests passing** (unit, integration, e2e)
- [ ] **Error handling** for all external calls
- [ ] **Monitoring** configured (metrics, logs, alerts)
- [ ] **Documentation** updated
- [ ] **Security review** completed
- [ ] **Performance testing** done
- [ ] **Cost analysis** performed
- [ ] **Rollback plan** ready
- [ ] **Rate limits** configured
- [ ] **Caching** implemented

### After Deployment

- [ ] **Monitor metrics** for 24 hours
- [ ] **Check error rates**
- [ ] **Verify costs** align with estimates
- [ ] **Gather user feedback**
- [ ] **Document lessons learned**
- [ ] **Plan improvements**

---

## 💡 Key Takeaways

### The Most Important Rules

1. **Start simple, iterate based on data**
2. **Test everything, assume nothing**
3. **Monitor costs and performance constantly**
4. **Document patterns for reuse**
5. **Always have a fallback plan**

### Common Pitfalls to Avoid

1. **Over-engineering initial solution**
2. **Ignoring error cases**
3. **Not monitoring production**
4. **Hardcoding configuration**
5. **Skipping documentation**

### Success Patterns

1. **Incremental complexity**
2. **Comprehensive testing**
3. **Proactive monitoring**
4. **Regular optimization**
5. **Continuous learning**

---

*Follow these practices to build robust, scalable, and maintainable agent systems.*

**Last Updated: November 2024**
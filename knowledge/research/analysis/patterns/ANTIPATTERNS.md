# Antipatterns in Agentic Engineering

## Overview

This document identifies common mistakes, pitfalls, and antipatterns observed in agentic engineering. These are patterns to AVOID, inferred from what successful implementations DON'T do and from common failure modes.

---

## Categories of Antipatterns

1. **Architectural Antipatterns**: Poor system structure
2. **Prompting Antipatterns**: Ineffective agent communication
3. **Workflow Antipatterns**: Inefficient process design
4. **Context Antipatterns**: Poor information management
5. **Integration Antipatterns**: Faulty system connections
6. **Testing Antipatterns**: Inadequate validation
7. **Production Antipatterns**: Operational failures

---

## Architectural Antipatterns

### 1. The Monolithic Agent

**What It Is**: One giant agent that tries to do everything

**Why It Happens**:
- Seems simpler initially
- Avoiding multi-agent complexity
- Not understanding specialization benefits

**Problems**:
- Poor performance (context overload)
- Difficult to debug
- Can't iterate on parts
- Single point of failure

**Example**:
```python
# ANTIPATTERN
class DoEverythingAgent:
    def handle(self, task):
        if task == "plan":
            # planning logic
        elif task == "build":
            # building logic
        elif task == "test":
            # testing logic
        # ... 500 more conditions
```

**Solution**: Use specialized agents with single responsibilities

### 2. The Tangled Layer

**What It Is**: Mixing agentic and application code

**Why It Happens**:
- Quick prototyping
- Not understanding separation
- Laziness in organization

**Problems**:
- Hard to maintain
- Can't reuse agent logic
- Version control conflicts
- Testing nightmares

**Example**:
```python
# ANTIPATTERN
def user_login():
    # Application logic
    validate_credentials()

    # Agent logic mixed in
    claude_response = claude("Check if this login is suspicious")

    # More application logic
    create_session()
```

**Solution**: Maintain clean separation with .claude/ directory

### 3. The Infinite Loop Architecture

**What It Is**: Agents calling agents without termination conditions

**Why It Happens**:
- Poor workflow design
- Missing exit conditions
- Recursive delegation without limits

**Problems**:
- Resource exhaustion
- Infinite costs
- System hangs
- Unpredictable behavior

**Example**:
```python
# ANTIPATTERN
def agent_a():
    result = agent_b()
    if not satisfied(result):
        agent_a()  # Recursive without limit

def agent_b():
    result = agent_a()  # Circular dependency
```

**Solution**: Always include termination conditions and depth limits

### 4. The Stateless Maze

**What It Is**: No state management between agent calls

**Why It Happens**:
- Not planning for continuity
- Ignoring persistence needs
- Over-simplifying architecture

**Problems**:
- Can't resume failed workflows
- No learning from past runs
- Repeated work
- No audit trail

**Example**:
```python
# ANTIPATTERN
def process_task():
    step1()  # No state saved
    step2()  # If fails, start over
    step3()  # No memory of previous runs
```

**Solution**: Implement proper state management and persistence

---

## Prompting Antipatterns

### 5. The Vague Instruction

**What It Is**: Unclear, ambiguous prompts

**Why It Happens**:
- Assuming AI understands context
- Lazy prompt writing
- Not testing edge cases

**Problems**:
- Inconsistent results
- Unexpected behaviors
- Poor quality outputs
- Frustrating debugging

**Example**:
```markdown
# ANTIPATTERN
Fix the bug in the code and make it better.
```

**Solution**: Be specific with clear requirements and constraints

### 6. The Context Dump

**What It Is**: Providing entire codebase as context

**Why It Happens**:
- Fear of missing something
- Not understanding token limits
- Lazy context curation

**Problems**:
- Token limit exceeded
- Slow performance
- Irrelevant responses
- High costs

**Example**:
```python
# ANTIPATTERN
context = load_entire_repository()
claude(f"Fix this bug: {bug}\nContext: {context}")
```

**Solution**: Curate context carefully, use Reduce & Delegate pattern

### 7. The Rigid Template

**What It Is**: Over-constraining output format

**Why It Happens**:
- Over-engineering
- Fear of variability
- Misunderstanding AI capabilities

**Problems**:
- Stifles creativity
- Misses edge cases
- Brittle parsing
- Poor adaptation

**Example**:
```markdown
# ANTIPATTERN
Output MUST be EXACTLY in this format with NO DEVIATIONS:
Line 1: [STATUS]
Line 2: [CODE]
Line 3: [COMMENT]
Any deviation will cause system failure.
```

**Solution**: Allow flexibility while maintaining structure

### 8. The Prompt Spaghetti

**What It Is**: Massive, unstructured prompts

**Why It Happens**:
- Incremental additions
- No refactoring
- Copy-paste accumulation

**Problems**:
- Hard to maintain
- Conflicting instructions
- Unpredictable behavior
- Poor performance

**Example**:
```markdown
# ANTIPATTERN
Do this and also that but not when this unless that and always
remember to check but don't check too much and make sure to but
not always and consider all factors except when you shouldn't...
```

**Solution**: Use structured sections and clear organization

---

## Workflow Antipatterns

### 9. The Sequential Bottleneck

**What It Is**: Forcing sequential execution when parallel is possible

**Why It Happens**:
- Simple mental model
- Not recognizing independence
- Fear of concurrency

**Problems**:
- Slow execution
- Wasted time
- Poor resource utilization
- User frustration

**Example**:
```python
# ANTIPATTERN
def process_features():
    implement_feature_1()  # 5 minutes
    implement_feature_2()  # 5 minutes (could run parallel)
    implement_feature_3()  # 5 minutes (could run parallel)
    # Total: 15 minutes instead of 5
```

**Solution**: Identify independent tasks and parallelize

### 10. The Missing Rollback

**What It Is**: No recovery mechanism for failures

**Why It Happens**:
- Optimistic planning
- Complexity avoidance
- Not considering failure modes

**Problems**:
- Corrupted state
- Manual recovery needed
- Data loss
- System downtime

**Example**:
```python
# ANTIPATTERN
def deploy():
    update_database()
    update_code()
    update_config()
    # If any fails, system is in inconsistent state
```

**Solution**: Implement rollback capabilities and transactions

### 11. The Premature Optimization

**What It Is**: Over-engineering before understanding needs

**Why It Happens**:
- Anticipating scale that never comes
- Resume-driven development
- FOMO on patterns

**Problems**:
- Unnecessary complexity
- Maintenance burden
- Slower development
- Confused team

**Example**:
```python
# ANTIPATTERN (for a 10-user app)
class UltraScalableMultiRegionEventSourcedCQRSSystem:
    # 5000 lines of unnecessary complexity
```

**Solution**: Start simple, evolve as needed (Progressive Enhancement)

### 12. The Manual Bridge

**What It Is**: Requiring human intervention between automated steps

**Why It Happens**:
- Partial automation
- Trust issues
- Legacy processes

**Problems**:
- Breaks automation flow
- Human bottleneck
- Increased errors
- Can't run 24/7

**Example**:
```python
# ANTIPATTERN
def workflow():
    auto_generate_code()
    print("Please review and press Enter to continue...")
    input()  # Manual step
    auto_deploy()
```

**Solution**: Full automation with quality gates instead

---

## Context Antipatterns

### 13. The Stale Context

**What It Is**: Using outdated information

**Why It Happens**:
- Caching too aggressively
- Not refreshing context
- Ignoring changes

**Problems**:
- Working on old code
- Missing recent changes
- Conflicts and overwrites
- Frustrated users

**Example**:
```python
# ANTIPATTERN
context = load_context()  # Loaded once at start
# ... 1 hour later ...
use_context(context)  # Still using hour-old data
```

**Solution**: Implement context refresh strategies

### 14. The Context Black Hole

**What It Is**: Loading context but not using it

**Why It Happens**:
- Copy-paste development
- Not understanding token costs
- "Just in case" mentality

**Problems**:
- Wasted tokens
- Increased costs
- Slower performance
- Confused AI

**Example**:
```python
# ANTIPATTERN
context = load_everything()
prompt = "What's 2+2?"  # Doesn't need context
claude(prompt, context=context)
```

**Solution**: Load only what's needed for the task

### 15. The Split Brain

**What It Is**: Different agents having conflicting context

**Why It Happens**:
- No context coordination
- Parallel execution without sync
- Poor state management

**Problems**:
- Conflicting outputs
- Overwritten changes
- Inconsistent behavior
- Merge conflicts

**Example**:
```python
# ANTIPATTERN
agent_1_context = load_context()  # Version A
agent_2_context = load_context()  # Version A
# ... time passes, changes happen ...
agent_1_work()  # Uses stale Version A
agent_2_work()  # Uses stale Version A
# Both produce conflicting changes
```

**Solution**: Implement context versioning and coordination

---

## Integration Antipatterns

### 16. The Brittle Integration

**What It Is**: Hard-coded external dependencies

**Why It Happens**:
- Quick implementation
- Not planning for change
- Tight coupling

**Problems**:
- Breaks with API changes
- Can't switch providers
- Testing difficulties
- Vendor lock-in

**Example**:
```python
# ANTIPATTERN
def get_data():
    # Hard-coded to specific API version
    response = requests.get("https://api.v1.example.com/data")
    return response.json()["specific"]["nested"]["field"]
```

**Solution**: Use abstractions and configuration

### 17. The Synchronous Trap

**What It Is**: Blocking on slow external calls

**Why It Happens**:
- Simpler mental model
- Not understanding async
- Legacy patterns

**Problems**:
- System hangs
- Poor user experience
- Resource waste
- Timeout cascades

**Example**:
```python
# ANTIPATTERN
def process_request():
    result1 = slow_api_call()  # Blocks for 30s
    result2 = another_slow_call()  # Blocks for 30s
    return combine(result1, result2)  # Total: 60s
```

**Solution**: Use async patterns and parallel execution

### 18. The Credential Leak

**What It Is**: Exposing secrets in code or prompts

**Why It Happens**:
- Convenience
- Poor security awareness
- Quick prototyping

**Problems**:
- Security breaches
- Compromised systems
- Compliance violations
- Public embarrassment

**Example**:
```python
# ANTIPATTERN
prompt = f"""
Use this API key to access the service: sk-1234567890
Database password is: admin123
"""
```

**Solution**: Use environment variables and secret management

---

## Testing Antipatterns

### 19. The Untested Agent

**What It Is**: No validation of agent outputs

**Why It Happens**:
- "AI is smart enough"
- Difficulty testing non-deterministic outputs
- Time pressure

**Problems**:
- Unreliable results
- Production failures
- No quality assurance
- Regression bugs

**Example**:
```python
# ANTIPATTERN
def deploy_agent():
    # No tests, just deploy
    agent = create_agent()
    deploy_to_production(agent)
```

**Solution**: Implement comprehensive testing strategies

### 20. The Flaky Test

**What It Is**: Tests that randomly fail

**Why It Happens**:
- Race conditions
- External dependencies
- Time-based logic
- Random elements

**Problems**:
- False positives
- Ignored test results
- Lost confidence
- Hidden real issues

**Example**:
```python
# ANTIPATTERN
def test_agent():
    result = agent.process()
    # Might fail based on time of day
    assert "morning" in result if datetime.now().hour < 12 else True
```

**Solution**: Make tests deterministic and isolated

### 21. The Test Theater

**What It Is**: Tests that don't actually test anything

**Why It Happens**:
- Coverage metrics gaming
- Not understanding testing
- Copy-paste testing

**Problems**:
- False confidence
- Missed bugs
- Wasted time
- Technical debt

**Example**:
```python
# ANTIPATTERN
def test_everything_works():
    try:
        do_something()
        assert True  # Always passes
    except:
        pass  # Swallow all errors
```

**Solution**: Write meaningful assertions and test cases

---

## Production Antipatterns

### 22. The Silent Failure

**What It Is**: Failures without notification

**Why It Happens**:
- No monitoring
- Swallowed exceptions
- Poor error handling

**Problems**:
- Unknown failures
- Data corruption
- User frustration
- Late discovery

**Example**:
```python
# ANTIPATTERN
def critical_process():
    try:
        important_operation()
    except:
        pass  # Silently fail
```

**Solution**: Implement comprehensive logging and alerting

### 23. The Runaway Agent

**What It Is**: Agents consuming unlimited resources

**Why It Happens**:
- No resource limits
- Missing termination conditions
- Recursive loops

**Problems**:
- Excessive costs
- System crashes
- API rate limits
- Service disruption

**Example**:
```python
# ANTIPATTERN
def process_all():
    while True:  # No termination
        expensive_ai_call()  # No rate limiting
```

**Solution**: Implement resource limits and circuit breakers

### 24. The Unobservable System

**What It Is**: No visibility into system behavior

**Why It Happens**:
- Not prioritizing observability
- Complex implementation
- "It works fine"

**Problems**:
- Can't debug issues
- No performance insights
- Missing bottlenecks
- Poor optimization

**Example**:
```python
# ANTIPATTERN
def black_box_process():
    # No logging
    # No metrics
    # No tracing
    do_mysterious_things()
```

**Solution**: Implement comprehensive observability

### 25. The Configuration Chaos

**What It Is**: Hard-coded configuration everywhere

**Why It Happens**:
- Quick development
- No configuration strategy
- Multiple contributors

**Problems**:
- Can't change without code changes
- Environment-specific bugs
- Deployment difficulties
- Security issues

**Example**:
```python
# ANTIPATTERN
def connect():
    if environment == "prod":
        url = "https://prod.example.com"
    elif environment == "staging":
        url = "https://staging.example.com"
    # ... 20 more conditions
```

**Solution**: Centralized configuration management

---

## Meta-Antipatterns

### 26. The Pattern Zealotry

**What It Is**: Using patterns everywhere regardless of fit

**Why It Happens**:
- Learning new patterns
- Resume building
- Cargo culting

**Problems**:
- Over-complexity
- Poor fit
- Team confusion
- Maintenance nightmare

**Example**:
```python
# ANTIPATTERN: Using orchestration for 2-line script
class SimpleTaskOrchestratorFactoryBuilderStrategy:
    # 500 lines to print "Hello World"
```

**Solution**: Use patterns judiciously based on actual needs

### 27. The NIH Syndrome

**What It Is**: Not Invented Here - rebuilding everything

**Why It Happens**:
- Ego
- Control desires
- Misunderstanding requirements

**Problems**:
- Wasted effort
- Bugs in reimplementation
- Missing features
- Maintenance burden

**Example**:
```python
# ANTIPATTERN
class MyOwnClaudeAPI:  # Reimplementing Claude SDK
    def __init__(self):
        self.build_entire_api_client()
```

**Solution**: Use existing tools and libraries when appropriate

### 28. The Premature Abstraction

**What It Is**: Creating abstractions before patterns emerge

**Why It Happens**:
- Anticipating future needs
- Over-engineering
- Fear of duplication

**Problems**:
- Wrong abstractions
- Increased complexity
- Harder refactoring
- Confused developers

**Example**:
```python
# ANTIPATTERN: After writing ONE command
class AbstractCommandFactoryInterface:
    class CommandBuilder:
        class CommandStrategy:
            # ... 10 levels of abstraction
```

**Solution**: Extract abstractions after patterns emerge (Rule of Three)

---

## Common Antipattern Combinations

### The Death Spiral
```
Monolithic Agent + Context Dump + No Testing + Silent Failures
= Complete system failure with no debugging capability
```

### The Complexity Trap
```
Premature Optimization + Pattern Zealotry + NIH Syndrome
= Unmaintainable, over-engineered system
```

### The Performance Killer
```
Sequential Bottleneck + Synchronous Trap + Context Dump
= Extremely slow, expensive system
```

### The Debugging Nightmare
```
Unobservable System + Silent Failures + Split Brain
= Impossible to diagnose issues
```

---

## How to Avoid Antipatterns

### 1. Start Simple
- Begin with minimal viable implementation
- Add complexity only when needed
- Follow Progressive Enhancement pattern

### 2. Test Early and Often
- Write tests before complexity grows
- Test agent outputs
- Validate integrations

### 3. Monitor Everything
- Add observability from the start
- Track metrics and costs
- Set up alerting

### 4. Review and Refactor
- Regular code reviews
- Refactor when patterns emerge
- Remove unused code

### 5. Learn from Mistakes
- Document failures
- Share learnings
- Update patterns

### 6. Follow Established Patterns
- Use proven patterns from the library
- Understand before modifying
- Contribute improvements back

---

## Red Flags to Watch For

### In Code
- 🚩 Functions over 100 lines
- 🚩 Deeply nested conditions
- 🚩 No error handling
- 🚩 Hard-coded values
- 🚩 No tests
- 🚩 Circular dependencies

### In Prompts
- 🚩 Over 1000 tokens
- 🚩 No structure
- 🚩 Vague instructions
- 🚩 No examples
- 🚩 Conflicting requirements

### In Architecture
- 🚩 Single point of failure
- 🚩 No state management
- 🚩 No rollback capability
- 🚩 Synchronous everything
- 🚩 No monitoring

### In Process
- 🚩 No documentation
- 🚩 No code reviews
- 🚩 Direct production deployment
- 🚩 No testing strategy
- 🚩 Manual steps in automation

---

## Conclusion

Antipatterns in agentic engineering often arise from:
1. **Rushing implementation** without proper planning
2. **Over-engineering** before understanding requirements
3. **Ignoring established patterns** and best practices
4. **Poor understanding** of AI capabilities and limitations
5. **Lack of testing** and observability

The key to avoiding antipatterns is to:
- Start simple and evolve
- Test and monitor everything
- Follow established patterns
- Learn from the community
- Refactor regularly

Remember: The absence of these antipatterns in the TAC curriculum is intentional. The course carefully avoids these pitfalls while teaching positive patterns. Learn from what it does AND what it deliberately doesn't do.
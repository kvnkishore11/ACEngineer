---
title: "Testing Strategist"
description: "Design and implement comprehensive testing strategies for agentic systems, workflows, and integrations"
tags: ["testing", "validation", "quality-assurance", "e2e", "automation"]
---

# Testing Strategist

## Purpose

Create comprehensive testing strategies for agentic systems, from unit testing individual agents to end-to-end validation of complete workflows. Master testing patterns specific to AI-driven systems, including prompt testing, behavior validation, and multi-agent interaction testing.

## When to Use

- Testing agent behaviors and responses
- Validating multi-agent workflows
- Creating test automation for agentic systems
- Implementing quality gates in CI/CD pipelines
- Testing prompt effectiveness and edge cases
- Validating integration points
- Debugging unexpected agent behaviors
- Performance testing agent systems

## How It Works

### Step 1: Define Testing Layers

#### Layer 1: Prompt Testing
Test prompts in isolation before agent deployment.

```python
class PromptTester:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.test_cases = []

    def add_test_case(self, input_text: str, expected_patterns: List[str],
                      forbidden_patterns: List[str] = None):
        """Add test case for prompt validation"""
        self.test_cases.append({
            "input": input_text,
            "expected": expected_patterns,
            "forbidden": forbidden_patterns or []
        })

    async def test_prompt(self, prompt: str) -> TestResult:
        """Test prompt against all test cases"""
        results = []

        for case in self.test_cases:
            response = await self.llm.complete(
                system=prompt,
                user=case["input"]
            )

            # Check expected patterns
            expected_pass = all(
                pattern in response
                for pattern in case["expected"]
            )

            # Check forbidden patterns
            forbidden_pass = not any(
                pattern in response
                for pattern in case["forbidden"]
            )

            results.append({
                "case": case["input"],
                "passed": expected_pass and forbidden_pass,
                "response": response,
                "issues": self.identify_issues(response, case)
            })

        return TestResult(
            passed=all(r["passed"] for r in results),
            details=results,
            coverage=self.calculate_coverage()
        )
```

#### Layer 2: Agent Unit Testing
Test individual agent behaviors.

```python
class AgentUnitTest:
    def __init__(self, agent):
        self.agent = agent
        self.mock_tools = {}

    def mock_tool(self, tool_name: str, mock_response):
        """Mock agent tool for testing"""
        self.mock_tools[tool_name] = mock_response

    async def test_agent_behavior(self, scenario: dict) -> bool:
        """Test specific agent behavior"""
        # Setup mocks
        original_tools = self.agent.tools
        self.agent.tools = self.create_mocked_tools()

        try:
            # Execute agent
            result = await self.agent.execute(scenario["input"])

            # Validate behavior
            assertions = [
                self.assert_tool_usage(result, scenario["expected_tools"]),
                self.assert_output_format(result, scenario["output_schema"]),
                self.assert_business_logic(result, scenario["validations"])
            ]

            return all(assertions)

        finally:
            # Restore original tools
            self.agent.tools = original_tools

    def assert_tool_usage(self, result, expected_tools):
        """Verify agent used expected tools"""
        used_tools = result.get("tools_used", [])
        return all(tool in used_tools for tool in expected_tools)
```

#### Layer 3: Integration Testing
Test agent interactions with external systems.

```python
class IntegrationTest:
    def __init__(self):
        self.test_db = TestDatabase()
        self.test_api = MockAPIServer()
        self.test_mcp = MockMCPServer()

    async def setup(self):
        """Setup test environment"""
        await self.test_db.initialize()
        await self.test_api.start()
        await self.test_mcp.start()

    async def teardown(self):
        """Cleanup test environment"""
        await self.test_db.cleanup()
        await self.test_api.stop()
        await self.test_mcp.stop()

    async def test_database_integration(self, agent):
        """Test agent database operations"""
        # Setup test data
        test_data = await self.test_db.seed_data()

        # Execute agent operation
        result = await agent.query_database("SELECT * FROM test_table")

        # Validate
        assert len(result) == len(test_data)
        assert self.test_db.query_count == 1

    async def test_api_integration(self, agent):
        """Test agent API calls"""
        # Setup mock responses
        self.test_api.add_response("/endpoint", {"status": "success"})

        # Execute agent
        result = await agent.call_api("/endpoint")

        # Validate
        assert result["status"] == "success"
        assert self.test_api.call_count("/endpoint") == 1
```

#### Layer 4: Workflow Testing
Test complete multi-agent workflows.

```python
class WorkflowTest:
    def __init__(self, workflow):
        self.workflow = workflow
        self.checkpoints = []

    async def test_workflow_execution(self, test_scenario):
        """Test complete workflow execution"""
        # Setup initial context
        context = test_scenario["initial_context"]

        # Execute workflow with monitoring
        result = await self.execute_with_monitoring(context)

        # Validate checkpoints
        checkpoint_results = self.validate_checkpoints()

        # Validate final state
        final_validation = self.validate_final_state(
            result,
            test_scenario["expected_output"]
        )

        return TestResult(
            passed=checkpoint_results["passed"] and final_validation,
            checkpoints=checkpoint_results["details"],
            output=result
        )

    async def execute_with_monitoring(self, context):
        """Execute workflow with checkpoint monitoring"""
        # Hook into workflow stages
        self.workflow.on_stage_complete = self.record_checkpoint

        result = await self.workflow.execute(context)
        return result

    def record_checkpoint(self, stage_name, stage_result):
        """Record workflow checkpoint"""
        self.checkpoints.append({
            "stage": stage_name,
            "result": stage_result,
            "timestamp": datetime.now()
        })
```

### Step 2: Implement Test Patterns

#### Pattern 1: Behavior-Driven Testing
```python
class BehaviorTest:
    """Test agent behaviors using Given-When-Then pattern"""

    def given(self, context: dict):
        """Setup test context"""
        self.context = context
        return self

    def when(self, action: str, params: dict = None):
        """Execute action"""
        self.result = self.execute_action(action, params)
        return self

    def then(self, assertion: callable):
        """Verify outcome"""
        assert assertion(self.result), f"Assertion failed: {assertion.__name__}"
        return self

# Usage
test = BehaviorTest()
test.given({"user_role": "admin"}) \
    .when("delete_record", {"id": 123}) \
    .then(lambda r: r["status"] == "success") \
    .then(lambda r: r["audit_logged"] == True)
```

#### Pattern 2: Property-Based Testing
```python
class PropertyTest:
    """Test agent properties that should always hold true"""

    @property_test
    def test_idempotency(self, agent, random_input):
        """Same input should produce same output"""
        result1 = agent.execute(random_input)
        result2 = agent.execute(random_input)
        assert result1 == result2

    @property_test
    def test_determinism(self, agent, inputs):
        """Agent should be deterministic with temperature=0"""
        agent.temperature = 0
        results = [agent.execute(input) for input in inputs]
        unique_results = len(set(results))
        assert unique_results == len(inputs)

    @property_test
    def test_safety(self, agent, malicious_inputs):
        """Agent should handle malicious inputs safely"""
        for input in malicious_inputs:
            try:
                result = agent.execute(input)
                assert "error" not in result
                assert self.is_safe_output(result)
            except Exception as e:
                # Should fail gracefully
                assert isinstance(e, SafetyException)
```

#### Pattern 3: Chaos Testing
```python
class ChaosTest:
    """Test system resilience under failure conditions"""

    def __init__(self, system):
        self.system = system
        self.chaos_events = []

    def inject_failure(self, component: str, failure_type: str):
        """Inject failure into system"""
        self.chaos_events.append({
            "component": component,
            "type": failure_type,
            "timestamp": datetime.now()
        })

        if failure_type == "network_partition":
            self.partition_network(component)
        elif failure_type == "high_latency":
            self.add_latency(component, delay=5000)
        elif failure_type == "resource_exhaustion":
            self.exhaust_resources(component)

    async def test_resilience(self):
        """Test system behavior under chaos"""
        # Normal operation baseline
        baseline = await self.system.benchmark()

        # Inject chaos
        self.inject_failure("database", "high_latency")
        self.inject_failure("agent_2", "network_partition")

        # Test degraded operation
        degraded = await self.system.benchmark()

        # System should still function
        assert degraded["success_rate"] > 0.5
        assert degraded["response_time"] < baseline["response_time"] * 3

        # Test recovery
        self.clear_chaos()
        recovered = await self.system.benchmark()
        assert recovered["success_rate"] > 0.95
```

### Step 3: Create Test Automation

#### E2E Test Framework
```python
class E2ETestFramework:
    """End-to-end testing for agentic systems"""

    def __init__(self):
        self.playwright = None
        self.agents = {}
        self.validators = []

    async def setup(self):
        """Setup E2E test environment"""
        # Initialize browser automation
        from playwright.async_api import async_playwright
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch()

        # Start agent system
        await self.start_agent_system()

        # Setup validators
        self.setup_validators()

    async def test_user_journey(self, journey: dict):
        """Test complete user journey"""
        page = await self.browser.new_page()

        try:
            # Navigate to application
            await page.goto(journey["start_url"])

            # Execute journey steps
            for step in journey["steps"]:
                await self.execute_step(page, step)

                # Validate agent behavior
                agent_response = await self.validate_agent_behavior(step)
                assert agent_response["valid"], f"Agent failed at step: {step['name']}"

            # Validate final state
            final_validation = await self.validate_final_state(page, journey)
            return final_validation

        finally:
            await page.close()

    async def execute_step(self, page, step):
        """Execute test step"""
        if step["type"] == "click":
            await page.click(step["selector"])
        elif step["type"] == "fill":
            await page.fill(step["selector"], step["value"])
        elif step["type"] == "wait":
            await page.wait_for_selector(step["selector"])
        elif step["type"] == "api_call":
            await self.call_api(step["endpoint"], step["payload"])
```

#### Continuous Testing Pipeline
```yaml
# .github/workflows/continuous-testing.yml
name: Continuous Agent Testing

on:
  push:
    branches: [main, develop]
  pull_request:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  prompt-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Test Prompts
        run: |
          python -m pytest tests/prompts/ \
            --cov=prompts \
            --cov-report=xml

  agent-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        agent: [planner, developer, tester, reviewer]
    steps:
      - name: Test Agent ${{ matrix.agent }}
        run: |
          python -m pytest tests/agents/${{ matrix.agent }} \
            --timeout=300

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
      redis:
        image: redis:7
    steps:
      - name: Run Integration Tests
        run: |
          python -m pytest tests/integration/ \
            --database-url=${{ services.postgres.url }}

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Setup Playwright
        run: npx playwright install

      - name: Run E2E Tests
        run: |
          python -m pytest tests/e2e/ \
            --headed \
            --video=retain-on-failure
```

### Step 4: Implement Monitoring & Validation

```python
class TestMonitor:
    """Monitor and validate test execution"""

    def __init__(self):
        self.metrics = defaultdict(list)
        self.alerts = []

    def track_test_execution(self, test_name: str, duration: float, passed: bool):
        """Track test execution metrics"""
        self.metrics[test_name].append({
            "duration": duration,
            "passed": passed,
            "timestamp": datetime.now()
        })

        # Check for anomalies
        if duration > self.get_p95_duration(test_name) * 2:
            self.alert(f"Test {test_name} took unusually long: {duration}s")

        # Check for flakiness
        recent_results = self.metrics[test_name][-10:]
        failure_rate = sum(1 for r in recent_results if not r["passed"]) / len(recent_results)
        if 0.1 < failure_rate < 0.9:
            self.alert(f"Test {test_name} is flaky: {failure_rate:.0%} failure rate")

    def generate_test_report(self):
        """Generate comprehensive test report"""
        return {
            "summary": {
                "total_tests": len(self.metrics),
                "passed": sum(r["passed"] for tests in self.metrics.values() for r in tests),
                "failed": sum(not r["passed"] for tests in self.metrics.values() for r in tests),
                "avg_duration": np.mean([r["duration"] for tests in self.metrics.values() for r in tests])
            },
            "flaky_tests": self.identify_flaky_tests(),
            "slow_tests": self.identify_slow_tests(),
            "coverage": self.calculate_coverage(),
            "alerts": self.alerts
        }
```

## Inputs Expected

- **System Architecture**: Understanding of agent system design
- **Test Requirements**: Coverage goals, performance benchmarks
- **Risk Assessment**: Critical paths, failure modes
- **Environment Details**: Test infrastructure, data requirements
- **Compliance Needs**: Regulatory requirements, audit needs

## Outputs Provided

1. **Test Strategy Document**
   ```markdown
   ## Testing Strategy
   - Test levels and coverage
   - Test data management
   - Environment setup
   - Automation approach
   - Risk mitigation
   ```

2. **Test Implementation**
   ```python
   # Complete test suite
   - Unit tests
   - Integration tests
   - E2E tests
   - Performance tests
   - Chaos tests
   ```

3. **CI/CD Configuration**
   ```yaml
   # Pipeline configuration
   - Test stages
   - Quality gates
   - Reporting
   - Notifications
   ```

4. **Test Reports**
   - Coverage reports
   - Performance metrics
   - Failure analysis
   - Trend analysis

## Examples

### Example 1: Multi-Agent Workflow Testing

```python
class MultiAgentWorkflowTest:
    """Test complex multi-agent workflows"""

    async def test_issue_to_pr_workflow(self):
        # Setup
        issue = self.create_test_issue("Fix login bug")

        # Execute workflow
        workflow_result = await self.workflow.process_issue(issue)

        # Validate stages
        assert workflow_result["planning"]["status"] == "completed"
        assert "implementation_plan.md" in workflow_result["planning"]["outputs"]

        assert workflow_result["implementation"]["status"] == "completed"
        assert len(workflow_result["implementation"]["changes"]) > 0

        assert workflow_result["testing"]["status"] == "completed"
        assert workflow_result["testing"]["test_results"]["passed"] == True

        assert workflow_result["review"]["status"] == "approved"

        # Validate PR creation
        pr = workflow_result["pull_request"]
        assert pr["state"] == "open"
        assert "Fixes #" in pr["body"]

    async def test_workflow_failure_recovery(self):
        # Inject failure
        self.mock_agent_failure("tester-agent", iteration=2)

        # Execute with recovery
        result = await self.workflow.process_with_recovery(self.test_issue)

        # Should recover and complete
        assert result["status"] == "completed"
        assert result["recovery_attempts"] == 1
```

### Example 2: Prompt Regression Testing

```python
class PromptRegressionTest:
    """Ensure prompt changes don't break existing behavior"""

    def __init__(self):
        self.baseline_results = self.load_baseline()

    async def test_prompt_regression(self, new_prompt: str):
        # Run standard test suite
        test_cases = self.load_test_cases()
        results = []

        for case in test_cases:
            new_result = await self.execute_prompt(new_prompt, case)
            baseline_result = self.baseline_results[case["id"]]

            # Compare semantic similarity
            similarity = self.calculate_similarity(new_result, baseline_result)

            results.append({
                "case": case["id"],
                "similarity": similarity,
                "regression": similarity < 0.85
            })

        # Check for regressions
        regressions = [r for r in results if r["regression"]]
        if regressions:
            raise RegressionError(f"Prompt regression detected in {len(regressions)} cases")

        return results
```

### Example 3: Performance Testing

```python
class PerformanceTest:
    """Test agent system performance"""

    async def test_agent_latency(self):
        """Test agent response latency"""
        latencies = []

        for _ in range(100):
            start = time.time()
            await self.agent.execute(self.standard_query)
            latencies.append(time.time() - start)

        assert np.percentile(latencies, 50) < 1.0  # p50 < 1s
        assert np.percentile(latencies, 95) < 3.0  # p95 < 3s
        assert np.percentile(latencies, 99) < 5.0  # p99 < 5s

    async def test_concurrent_load(self):
        """Test system under concurrent load"""
        tasks = []
        for _ in range(50):
            task = self.agent.execute(self.generate_query())
            tasks.append(task)

        start = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        duration = time.time() - start

        # Check success rate
        successes = sum(1 for r in results if not isinstance(r, Exception))
        assert successes / len(results) > 0.95  # 95% success rate

        # Check throughput
        throughput = len(results) / duration
        assert throughput > 10  # At least 10 req/s
```

## Troubleshooting

### Flaky Tests
```python
def diagnose_flaky_test(test_name: str):
    """Diagnose why a test is flaky"""
    # Run test multiple times
    results = []
    for _ in range(20):
        result = run_test(test_name)
        results.append(result)

    # Analyze patterns
    failures = [r for r in results if not r["passed"]]
    if failures:
        # Check for timing issues
        if all("timeout" in f["error"] for f in failures):
            return "Timing dependent - increase timeout"

        # Check for ordering issues
        if failures_cluster_at_start(failures):
            return "State initialization issue"

        # Check for external dependencies
        if "connection" in str(failures):
            return "External dependency issue"
```

### Test Data Management
```python
class TestDataManager:
    """Manage test data lifecycle"""

    def __init__(self):
        self.data_sets = {}

    def create_isolated_data(self, test_id: str):
        """Create isolated test data"""
        namespace = f"test_{test_id}_{uuid.uuid4()}"
        self.data_sets[namespace] = {
            "created_at": datetime.now(),
            "entities": []
        }
        return namespace

    def cleanup_test_data(self, namespace: str):
        """Clean up test data after test"""
        if namespace in self.data_sets:
            for entity in self.data_sets[namespace]["entities"]:
                self.delete_entity(entity)
            del self.data_sets[namespace]
```

## Related Skills

- **Agent Builder**: Create testable agents
- **Workflow Designer**: Design testable workflows
- **Integration Specialist**: Test integration points
- **Context Optimizer**: Performance testing strategies
- **Prompt Engineer**: Test prompt effectiveness

## Key Principles

1. **Test at Every Level**: From prompts to complete systems
2. **Automate Everything**: Manual testing doesn't scale
3. **Test Early and Often**: Shift testing left
4. **Monitor Continuously**: Track test metrics and trends
5. **Fail Fast**: Quick feedback on issues

---

*This skill is derived from TAC-5's testing patterns and validation approaches throughout the course, providing comprehensive testing strategies for agentic systems.*
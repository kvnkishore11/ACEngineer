# Pipeline Command Template

<!--
Complete automation pipeline command for end-to-end workflows
Place in: .claude/commands/[pipeline-name].md
-->

## Pipeline: [pipeline-name]

Execute a complete automated pipeline for [purpose], from initial input to final deployment.

### Pipeline Architecture

```yaml
pipeline:
  name: [pipeline-name]
  type: sequential | parallel | hybrid
  stages:
    - input_validation
    - preparation
    - processing
    - transformation
    - quality_assurance
    - deployment
    - monitoring

  triggers:
    - manual: /[pipeline-name]
    - automated: [cron, webhook, event]
    - conditional: [based on metrics]

  outputs:
    - artifacts: [build outputs]
    - reports: [execution reports]
    - metrics: [performance data]
```

### Pipeline Stages

#### Stage 1: Input Validation
```python
class InputValidator:
    """
    Validate and prepare pipeline inputs.
    """
    def validate(self, inputs):
        validations = {
            "schema": self.validate_schema(inputs),
            "business_rules": self.validate_business_rules(inputs),
            "dependencies": self.check_dependencies(inputs),
            "permissions": self.verify_permissions(inputs)
        }

        if not all(validations.values()):
            raise PipelineValidationError(validations)

        return self.transform_inputs(inputs)

    def validate_schema(self, inputs):
        # Check input structure and types
        required_fields = ["source", "target", "config"]
        return all(field in inputs for field in required_fields)

    def check_dependencies(self, inputs):
        # Verify all dependencies available
        deps = ["database", "api_keys", "storage"]
        return all(self.check_dependency(dep) for dep in deps)
```

#### Stage 2: Preparation
```bash
#!/bin/bash
# Preparation stage script

# Set up environment
export PIPELINE_NAME="[pipeline-name]"
export PIPELINE_RUN_ID=$(uuidgen)
export PIPELINE_START_TIME=$(date +%s)

# Create working directory
mkdir -p /tmp/pipeline/$PIPELINE_RUN_ID
cd /tmp/pipeline/$PIPELINE_RUN_ID

# Download required resources
download_resources() {
    echo "Downloading resources..."
    # Download templates, configs, etc.
    curl -o template.yaml https://...
    curl -o config.json https://...
}

# Initialize services
initialize_services() {
    echo "Initializing services..."
    # Start required services
    docker-compose up -d
    wait_for_services
}

# Set up logging
setup_logging() {
    echo "Setting up logging..."
    mkdir -p logs
    exec 1> >(tee -a logs/pipeline.log)
    exec 2>&1
}
```

#### Stage 3: Core Processing
```typescript
interface ProcessingStage {
  name: string;
  execute(): Promise<StageResult>;
  rollback(): Promise<void>;
}

class DataProcessingStage implements ProcessingStage {
  name = "data_processing";

  async execute(): Promise<StageResult> {
    const startTime = Date.now();

    try {
      // Step 1: Load data
      const data = await this.loadData();
      this.checkpoint("data_loaded", data);

      // Step 2: Transform data
      const transformed = await this.transformData(data);
      this.checkpoint("data_transformed", transformed);

      // Step 3: Validate transformation
      const validation = await this.validateData(transformed);
      if (!validation.isValid) {
        throw new ValidationError(validation.errors);
      }

      // Step 4: Save results
      const output = await this.saveResults(transformed);

      return {
        status: "success",
        duration: Date.now() - startTime,
        output,
        metrics: this.collectMetrics()
      };

    } catch (error) {
      await this.handleError(error);
      throw new StageExecutionError(this.name, error);
    }
  }

  async rollback(): Promise<void> {
    // Restore from last checkpoint
    const checkpoint = await this.getLastCheckpoint();
    await this.restoreFromCheckpoint(checkpoint);
  }
}
```

#### Stage 4: Quality Assurance
```python
class QualityAssuranceStage:
    """
    Comprehensive quality checks.
    """
    def __init__(self):
        self.checks = [
            self.check_functionality,
            self.check_performance,
            self.check_security,
            self.check_compliance
        ]

    async def execute(self, artifacts):
        results = {
            "passed": [],
            "failed": [],
            "warnings": []
        }

        for check in self.checks:
            try:
                result = await check(artifacts)
                if result.status == "pass":
                    results["passed"].append(result)
                elif result.status == "fail":
                    results["failed"].append(result)
                else:
                    results["warnings"].append(result)
            except Exception as e:
                results["failed"].append({
                    "check": check.__name__,
                    "error": str(e)
                })

        # Determine overall status
        if results["failed"]:
            raise QualityCheckFailure(results)

        return results

    async def check_functionality(self, artifacts):
        # Run functional tests
        test_results = await run_tests(artifacts["code"])
        return {
            "status": "pass" if test_results.all_pass else "fail",
            "details": test_results
        }

    async def check_performance(self, artifacts):
        # Run performance benchmarks
        benchmarks = await run_benchmarks(artifacts["code"])
        return {
            "status": "pass" if benchmarks.meet_sla else "warning",
            "details": benchmarks
        }
```

#### Stage 5: Deployment
```yaml
# Deployment configuration
deployment:
  strategy: blue-green | canary | rolling

  blue_green:
    prepare_new_environment:
      - Provision resources
      - Deploy application
      - Run smoke tests

    switch_traffic:
      - Update load balancer
      - Monitor metrics
      - Verify health

    cleanup_old:
      - Wait for drain
      - Terminate old instances
      - Release resources

  canary:
    initial_rollout:
      percentage: 5
      duration: 10m
      metrics:
        - error_rate < 1%
        - latency_p99 < 200ms

    gradual_rollout:
      - 25% after 30m
      - 50% after 1h
      - 100% after 2h

    rollback_triggers:
      - error_rate > 5%
      - latency_p99 > 500ms
      - cpu_usage > 90%
```

### Pipeline Configuration

```yaml
# pipeline.config.yaml
pipeline:
  name: [pipeline-name]
  version: 1.0.0

  parameters:
    source:
      type: string
      required: true
      description: Source data location

    environment:
      type: string
      required: true
      enum: [dev, staging, production]

    options:
      parallel_workers:
        type: integer
        default: 4
        min: 1
        max: 16

      timeout:
        type: duration
        default: 30m
        max: 2h

      retry_policy:
        max_attempts: 3
        backoff: exponential
        initial_delay: 5s

  stages:
    - name: validation
      timeout: 5m
      critical: true

    - name: preparation
      timeout: 10m
      critical: true

    - name: processing
      timeout: 30m
      critical: true
      parallel: true

    - name: quality_assurance
      timeout: 15m
      critical: false

    - name: deployment
      timeout: 20m
      critical: true
      manual_approval: true

  notifications:
    on_start:
      - email: team@example.com
      - slack: #deployments

    on_failure:
      - email: oncall@example.com
      - pagerduty: critical

    on_success:
      - slack: #deployments
```

### Monitoring and Observability

```python
class PipelineMonitor:
    """
    Monitor pipeline execution in real-time.
    """
    def __init__(self, pipeline_id):
        self.pipeline_id = pipeline_id
        self.metrics = MetricsCollector()
        self.alerts = AlertManager()

    def track_stage(self, stage_name):
        """Track stage execution."""
        @contextmanager
        def stage_tracker():
            start_time = time.time()
            self.log_event(f"Stage {stage_name} started")

            try:
                yield
                duration = time.time() - start_time
                self.metrics.record_stage_success(stage_name, duration)
                self.log_event(f"Stage {stage_name} completed in {duration}s")

            except Exception as e:
                duration = time.time() - start_time
                self.metrics.record_stage_failure(stage_name, duration)
                self.alerts.trigger(f"Stage {stage_name} failed: {e}")
                self.log_event(f"Stage {stage_name} failed after {duration}s")
                raise

        return stage_tracker()

    def get_status(self):
        """Get current pipeline status."""
        return {
            "pipeline_id": self.pipeline_id,
            "current_stage": self.get_current_stage(),
            "progress": self.calculate_progress(),
            "metrics": self.metrics.get_summary(),
            "alerts": self.alerts.get_active(),
            "estimated_completion": self.estimate_completion()
        }
```

### Error Recovery

```python
class PipelineRecovery:
    """
    Handle pipeline failures and recovery.
    """
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.checkpoints = CheckpointManager()

    async def handle_failure(self, stage, error):
        """Handle stage failure with recovery options."""
        severity = self.assess_severity(error)

        if severity == "low":
            # Retry the stage
            return await self.retry_stage(stage)

        elif severity == "medium":
            # Rollback and retry
            await self.rollback_stage(stage)
            return await self.retry_stage(stage)

        elif severity == "high":
            # Partial rollback to last stable state
            stable_checkpoint = self.checkpoints.get_last_stable()
            await self.rollback_to_checkpoint(stable_checkpoint)
            return await self.resume_from_checkpoint(stable_checkpoint)

        else:  # critical
            # Full pipeline abort and cleanup
            await self.abort_pipeline()
            await self.cleanup_resources()
            await self.notify_operators(error)
            raise PipelineCriticalError(error)

    async def retry_stage(self, stage, attempt=1, max_attempts=3):
        """Retry a failed stage with exponential backoff."""
        if attempt > max_attempts:
            raise StageRetryExhausted(stage)

        wait_time = 2 ** attempt  # Exponential backoff
        await asyncio.sleep(wait_time)

        try:
            return await stage.execute()
        except Exception as e:
            return await self.retry_stage(stage, attempt + 1)
```

### Pipeline Execution Report

```markdown
# Pipeline Execution Report

## Pipeline: [pipeline-name]
## Run ID: abc123-def456-789012

### Summary
- **Status**: ✅ Success
- **Duration**: 45 minutes
- **Start Time**: 2024-01-10 10:00:00 UTC
- **End Time**: 2024-01-10 10:45:00 UTC

### Stage Results

| Stage | Status | Duration | Details |
|-------|--------|----------|---------|
| Input Validation | ✅ | 30s | All inputs valid |
| Preparation | ✅ | 2m | Environment ready |
| Processing | ✅ | 25m | Processed 1M records |
| Quality Assurance | ✅ | 10m | All checks passed |
| Deployment | ✅ | 8m | Deployed to production |

### Metrics

#### Performance
- Records Processed: 1,000,000
- Processing Rate: 667 records/sec
- Error Rate: 0.01%
- Success Rate: 99.99%

#### Resource Usage
- Peak CPU: 75%
- Peak Memory: 4.2GB
- Network I/O: 500MB
- Storage Used: 2.1GB

### Artifacts Generated
- Build: `builds/v1.2.3.tar.gz`
- Logs: `logs/pipeline-abc123.log`
- Reports: `reports/execution-abc123.pdf`
- Metrics: `metrics/pipeline-abc123.json`

### Quality Gates
- ✅ Unit Tests: 150/150 passed
- ✅ Integration Tests: 50/50 passed
- ✅ Security Scan: No vulnerabilities
- ✅ Performance: Within SLA
- ✅ Code Coverage: 85%

### Deployment Details
- Environment: Production
- Version: v1.2.3
- Strategy: Blue-Green
- Rollback Point: v1.2.2

### Recommendations
1. Consider increasing parallel workers for faster processing
2. Add caching for frequently accessed data
3. Implement circuit breaker for external API calls

### Next Steps
- Monitor application metrics for 24 hours
- Schedule post-deployment review
- Update documentation
```

### Integration Examples

#### GitHub Actions Integration
```yaml
# .github/workflows/pipeline.yml
name: Automated Pipeline

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  execute-pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Execute Pipeline
        run: |
          claude-code /[pipeline-name] \
            --source=${{ github.repository }} \
            --environment=production \
            --parallel-workers=8

      - name: Upload Artifacts
        uses: actions/upload-artifact@v2
        with:
          name: pipeline-artifacts
          path: artifacts/

      - name: Publish Metrics
        run: |
          curl -X POST https://metrics.example.com/pipeline \
            -H "Content-Type: application/json" \
            -d @metrics/pipeline.json
```

#### Kubernetes Job Integration
```yaml
# k8s-pipeline-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pipeline-[pipeline-name]
spec:
  template:
    spec:
      containers:
      - name: pipeline-executor
        image: claude-code:latest
        command: ["/bin/sh"]
        args:
          - -c
          - |
            claude-code /[pipeline-name] \
              --source=s3://bucket/data \
              --environment=production
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
      restartPolicy: OnFailure
  backoffLimit: 3
```

### Customization Guide

1. **Define Stages**: Identify your pipeline stages and dependencies
2. **Configure Parameters**: Set up input parameters and validation
3. **Implement Processing**: Add your core business logic
4. **Add Quality Gates**: Define quality criteria and checks
5. **Set Up Monitoring**: Configure metrics and alerts
6. **Plan Recovery**: Define rollback and retry strategies
7. **Document Outputs**: Specify artifacts and reports

### Common Pipeline Patterns

1. **Data Processing Pipeline**
   - Ingest → Validate → Transform → Load → Verify

2. **CI/CD Pipeline**
   - Build → Test → Scan → Package → Deploy → Monitor

3. **ML Pipeline**
   - Data Prep → Feature Engineering → Training → Evaluation → Deployment

4. **ETL Pipeline**
   - Extract → Transform → Load → Validate → Report

5. **Release Pipeline**
   - Version → Build → Test → Stage → Approve → Deploy → Verify
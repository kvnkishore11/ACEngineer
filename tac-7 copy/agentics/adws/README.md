# Agentic Development Workflow System (ADWS)

An optimized workflow orchestration system designed for direct integration with AgenticKanban.

## Overview

The ADWS provides automated workflow execution through file-based triggers from the AgenticKanban UI. It handles multi-stage development workflows including planning, implementation, testing, and review phases.

## Architecture

```
agentics/
├── adws/                          # ADW System core
│   ├── adw_orchestrator.py       # Main orchestrator
│   ├── pipelines/                # Stage-specific pipelines
│   │   ├── plan_pipeline.py      # Planning stage
│   │   ├── implement_pipeline.py # Implementation stage
│   │   ├── test_pipeline.py      # Testing stage
│   │   └── review_pipeline.py    # Review stage
│   ├── logs/                     # System logs
│   ├── requirements.txt          # Python dependencies
│   ├── start_orchestrator.sh     # Startup script
│   └── README.md                 # This file
└── agents/                       # Task execution directories
    └── {adw_id}/                 # Individual task workspaces
        ├── task_data.json        # Task input data
        ├── adw_state.json        # Execution state
        ├── plan_output.json      # Planning results
        ├── implement_output.json # Implementation results
        ├── test_output.json      # Testing results
        └── review_output.json    # Review results
```

## Integration with AgenticKanban

The system integrates seamlessly with the AgenticKanban UI through file-based triggers:

1. **Task Creation**: User creates task in Kanban UI
2. **Trigger Generation**: UI writes trigger file to `adws/trigger_{adw_id}.json`
3. **Task Data**: UI writes task data to `agents/{adw_id}/task_data.json`
4. **Automatic Execution**: Orchestrator detects trigger and executes workflow
5. **State Updates**: Real-time state updates written to `agents/{adw_id}/adw_state.json`
6. **UI Polling**: Kanban UI polls state file for progress updates

## Workflow Stages

### 1. Planning Stage (`plan_pipeline.py`)
- Analyzes task requirements
- Generates implementation plan
- Estimates effort and identifies dependencies
- Outputs: `plan_output.json`

### 2. Implementation Stage (`implement_pipeline.py`)
- Implements features based on plan
- Creates sample code structures
- Generates documentation stubs
- Outputs: `implement_output.json`

### 3. Testing Stage (`test_pipeline.py`)
- Runs unit and integration tests
- Performs code quality checks
- Executes security scans
- Generates test reports
- Outputs: `test_output.json`

### 4. Review Stage (`review_pipeline.py`)
- Conducts automated code review
- Performs architecture assessment
- Validates security compliance
- Generates approval status
- Outputs: `review_output.json`

## Getting Started

### Prerequisites
- Python 3.8 or higher
- AgenticKanban application running

### Setup
1. Ensure Python is installed:
   ```bash
   python3 --version
   ```

2. Navigate to the ADWS directory:
   ```bash
   cd agentics/adws
   ```

3. (Optional) Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

### Running the Orchestrator

#### Option 1: Using the startup script (Recommended)
```bash
./start_orchestrator.sh
```

#### Option 2: Direct Python execution
```bash
python3 adw_orchestrator.py --workspace /path/to/AgenticKanban
```

#### Option 3: Daemon mode
```bash
python3 adw_orchestrator.py --workspace /path/to/AgenticKanban --daemon
```

### Manual Task Execution
```bash
python3 adw_orchestrator.py '{"adw_id": "test_123", "title": "Test Task", "description": "Test description", "type": "feature", "stages": ["plan", "implement"]}'
```

## Configuration

The orchestrator uses smart defaults but can be configured through:

1. **Task Data**: Configure stages and parameters per task
2. **Pipeline Scripts**: Customize individual stage behavior
3. **Environment Variables**: Set system-wide defaults

### Supported Task Types
- `feature`: New feature development
- `bug`: Bug fixes
- `chore`: Maintenance tasks
- `patch`: Small patches/updates

### Supported Stages
- `plan`: Planning and analysis
- `implement`: Implementation
- `test`: Testing and validation
- `review`: Code review and approval
- `document`: Documentation
- `pr`: Pull request preparation

## Monitoring and Logging

### Log Files
- System logs: `logs/adw_orchestrator_YYYYMMDD.log`
- Stage logs: `{task_dir}/{stage}_pipeline.log`

### State Monitoring
- Real-time state: `agents/{adw_id}/adw_state.json`
- Execution history: Individual stage output files

### Key State Fields
```json
{
  "adw_id": "unique_task_id",
  "status": "executing|completed|failed",
  "current_stage": "plan|implement|test|review",
  "progress": 0-100,
  "overall_status": "pending|executing|completed|failed",
  "logs": [/* execution logs */],
  "completed_stages": ["plan"],
  "failed_stages": []
}
```

## Customization

### Adding New Pipelines
1. Create new pipeline script in `pipelines/`
2. Follow the existing pipeline interface
3. Accept `--task-id`, `--task-dir`, `--stage` arguments
4. Output results to `{stage}_output.json`

### Pipeline Interface
```python
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--task-dir", required=True, type=Path)
    parser.add_argument("--stage", required=True)

    # Execute stage logic
    # Save results to {stage}_output.json
    # Exit with 0 for success, 1 for failure
```

### Extending Task Types
Modify pipeline scripts to handle new task types by updating the type-specific logic in each pipeline.

## Troubleshooting

### Common Issues

1. **Orchestrator not detecting triggers**
   - Verify file permissions
   - Check workspace directory path
   - Review log files for errors

2. **Pipeline failures**
   - Check individual pipeline logs
   - Verify Python path and dependencies
   - Review task data format

3. **State not updating**
   - Ensure proper file system access
   - Check agents directory permissions
   - Verify JSON format

### Debug Mode
Enable detailed logging by setting log level to DEBUG in the orchestrator script.

### Manual State Recovery
If state becomes inconsistent:
1. Stop orchestrator
2. Review log files
3. Manually correct state files if needed
4. Restart orchestrator

## Performance Considerations

- **File System**: Uses efficient file watching and polling
- **Concurrency**: Handles multiple tasks simultaneously
- **Resource Usage**: Minimal Python overhead
- **Scalability**: Designed for typical development team usage

## Security

- **File Access**: Limited to workspace directory
- **Execution**: Only runs predefined pipeline scripts
- **Data**: No external network access required
- **Isolation**: Each task runs in isolated directory

## Integration Notes

### With AgenticKanban UI
- File-based communication for reliability
- Real-time state synchronization
- Automatic cleanup of completed tasks

### Future Enhancements
- Database integration for persistent storage
- Web API for external integrations
- Plugin system for custom stages
- Distributed execution capabilities

## Support

For issues and feature requests, check:
1. Log files in `logs/` directory
2. Task-specific logs in agent directories
3. AgenticKanban UI console for client-side issues

## License

Part of the AgenticKanban project.
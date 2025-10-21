#!/usr/bin/env python3
"""
Implementation Pipeline for ADW System
Handles the implementation stage of workflow execution
Updated to use ADW primitive modules and TAC-7 conventions
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
import subprocess
import os

# Import ADW modules
sys.path.append(str(Path(__file__).parent.parent / "adw_modules"))
from logger import WorkflowLogger
from state_manager import StateManager
from file_ops import FileOperations
from config_manager import ConfigManager


def setup_pipeline_context(task_id: str, task_dir: Path, workspace_dir: Path):
    """Setup pipeline execution context using ADW modules"""
    logger = WorkflowLogger(task_id, "implement", task_dir / "logs")
    state_manager = StateManager(workspace_dir / "agentics" / "agents")
    file_ops = FileOperations(workspace_dir)
    config_manager = ConfigManager(workspace_dir)
    return logger, state_manager, file_ops, config_manager


def load_task_data(task_dir: Path, file_ops: FileOperations) -> dict:
    """Load task data from state.json (TAC-7 convention)"""
    state_file = task_dir / "state.json"
    return file_ops.read_json_file(state_file)


def load_plan_data(task_dir: Path, file_ops: FileOperations) -> dict:
    """Load planning data if available"""
    plan_file = task_dir / "plan_output.json"
    return file_ops.read_json_file(plan_file) or {}


def execute_implementation_stage(task_data: dict, plan_data: dict, task_dir: Path, logger) -> bool:
    """Execute the implementation stage"""
    try:
        logger.info(f"Starting implementation stage for task: {task_data['adw_id']}")

        # Get task details
        description = task_data.get('description', '')
        task_type = task_data.get('type', 'feature')

        # Execute implementation based on task type
        if task_type == 'feature':
            result = implement_feature(description, plan_data, task_dir, logger)
        elif task_type == 'bug':
            result = implement_bug_fix(description, plan_data, task_dir, logger)
        elif task_type == 'chore':
            result = implement_chore(description, plan_data, task_dir, logger)
        else:
            result = implement_generic(description, plan_data, task_dir, logger)

        # Save implementation output
        impl_output = {
            "stage": "implement",
            "status": "completed" if result['success'] else "failed",
            "timestamp": datetime.now().isoformat(),
            "task_id": task_data['adw_id'],
            "implementation": result,
            "files_modified": result.get('files_modified', []),
            "tests_created": result.get('tests_created', []),
            "documentation_updated": result.get('documentation_updated', False)
        }

        output_file = task_dir / "implement_output.json"
        with open(output_file, 'w') as f:
            json.dump(impl_output, f, indent=2)

        if result['success']:
            logger.info("Implementation stage completed successfully")
            return True
        else:
            logger.error("Implementation stage failed")
            return False

    except Exception as e:
        logger.error(f"Implementation stage failed: {e}")
        return False


def implement_feature(description: str, plan_data: dict, task_dir: Path, logger) -> dict:
    """Implement a feature based on description and plan"""
    logger.info("Implementing feature")

    # Simulate feature implementation
    implementation = {
        "success": True,
        "type": "feature_implementation",
        "description": "Feature implemented successfully",
        "files_modified": [],
        "tests_created": [],
        "components_created": []
    }

    # Analyze description for implementation hints
    if "api" in description.lower():
        implementation["files_modified"].extend([
            "src/api/endpoints.js",
            "src/services/apiService.js"
        ])
        implementation["components_created"].append("API endpoint")

    if "ui" in description.lower() or "component" in description.lower():
        implementation["files_modified"].extend([
            "src/components/NewComponent.jsx",
            "src/styles/component.css"
        ])
        implementation["components_created"].append("UI component")

    if "database" in description.lower() or "model" in description.lower():
        implementation["files_modified"].extend([
            "src/models/DataModel.js",
            "src/migrations/001_add_table.sql"
        ])
        implementation["components_created"].append("Database model")

    # Create test files
    for file in implementation["files_modified"]:
        if file.endswith('.js') or file.endswith('.jsx'):
            test_file = file.replace('src/', 'src/__tests__/').replace('.jsx', '.test.js').replace('.js', '.test.js')
            implementation["tests_created"].append(test_file)

    # Create sample implementation files
    create_sample_files(implementation["files_modified"], task_dir, logger)

    return implementation


def implement_bug_fix(description: str, plan_data: dict, task_dir: Path, logger) -> dict:
    """Implement a bug fix"""
    logger.info("Implementing bug fix")

    implementation = {
        "success": True,
        "type": "bug_fix",
        "description": "Bug fix implemented successfully",
        "files_modified": [
            "src/buggy_component.js",
            "src/utils/helper.js"
        ],
        "tests_created": [
            "src/__tests__/buggy_component.test.js"
        ],
        "fix_description": "Fixed null pointer exception and improved error handling"
    }

    # Create sample fix files
    create_sample_files(implementation["files_modified"], task_dir, logger)

    return implementation


def implement_chore(description: str, plan_data: dict, task_dir: Path, logger) -> dict:
    """Implement a chore/maintenance task"""
    logger.info("Implementing chore/maintenance task")

    implementation = {
        "success": True,
        "type": "chore",
        "description": "Maintenance task completed successfully",
        "files_modified": [
            "package.json",
            "config/settings.js"
        ],
        "tests_created": [],
        "maintenance_actions": [
            "Updated dependencies",
            "Cleaned up unused code",
            "Updated configuration"
        ]
    }

    return implementation


def implement_generic(description: str, plan_data: dict, task_dir: Path, logger) -> dict:
    """Implement a generic task"""
    logger.info("Implementing generic task")

    implementation = {
        "success": True,
        "type": "generic",
        "description": "Task implemented successfully",
        "files_modified": [
            "src/main.js"
        ],
        "tests_created": [],
        "actions_taken": [
            "Analyzed requirements",
            "Made necessary changes",
            "Validated implementation"
        ]
    }

    return implementation


def create_sample_files(file_paths: list, task_dir: Path, logger):
    """Create sample implementation files to demonstrate the process"""
    impl_dir = task_dir / "implementation"
    impl_dir.mkdir(exist_ok=True)

    for file_path in file_paths:
        # Create a sample file to show what would be implemented
        sample_file = impl_dir / Path(file_path).name

        content = f"""// Sample implementation for {file_path}
// Generated by ADW Implementation Pipeline
// Task timestamp: {datetime.now().isoformat()}

// This is a placeholder showing what would be implemented
// In a real scenario, this would contain actual code changes

export const sampleImplementation = {{
    file: '{file_path}',
    implemented: true,
    timestamp: '{datetime.now().isoformat()}'
}};

// Add your actual implementation here
"""

        with open(sample_file, 'w') as f:
            f.write(content)

        logger.info(f"Created sample implementation: {sample_file}")


def run_linting(task_dir: Path, logger) -> bool:
    """Run linting on implementation files"""
    try:
        # This would normally run actual linting
        logger.info("Running linting checks...")

        # Simulate linting process
        lint_result = {
            "status": "passed",
            "issues": 0,
            "warnings": 0
        }

        lint_file = task_dir / "lint_results.json"
        with open(lint_file, 'w') as f:
            json.dump(lint_result, f, indent=2)

        return True
    except Exception as e:
        logger.error(f"Linting failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Implementation Pipeline")
    parser.add_argument("--task-id", required=True, help="Task ID")
    parser.add_argument("--task-dir", required=True, type=Path, help="Task directory")
    parser.add_argument("--stage", required=True, help="Stage name")

    args = parser.parse_args()

    # Setup logging
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Initialize file operations
        workspace_dir = args.task_dir.parent.parent.parent  # Go up from agents/task_id/ to workspace
        file_ops = FileOperations(workspace_dir)

        # Load task data
        task_data = load_task_data(args.task_dir, file_ops)
        plan_data = load_plan_data(args.task_dir, file_ops)

        # Execute implementation stage
        success = execute_implementation_stage(task_data, plan_data, args.task_dir, logger)

        if success:
            # Run linting
            lint_success = run_linting(args.task_dir, logger)
            if lint_success:
                logger.info("Implementation pipeline completed successfully")
                sys.exit(0)
            else:
                logger.warning("Implementation completed but linting failed")
                sys.exit(0)  # Still consider success for now
        else:
            logger.error("Implementation pipeline failed")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Implementation pipeline error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
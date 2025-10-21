#!/usr/bin/env python3
"""
Planning Pipeline for ADW System
Handles the planning stage of workflow execution
Updated to use ADW primitive modules and TAC-7 conventions
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Import ADW modules
sys.path.append(str(Path(__file__).parent.parent / "adw_modules"))
from logger import WorkflowLogger
from state_manager import StateManager
from file_ops import FileOperations
from config_manager import ConfigManager


def setup_pipeline_context(task_id: str, task_dir: Path, workspace_dir: Path):
    """Setup pipeline execution context using ADW modules"""
    # Initialize ADW modules
    logger = WorkflowLogger(task_id, "plan", task_dir / "logs")
    state_manager = StateManager(workspace_dir / "agentics" / "agents")
    file_ops = FileOperations(workspace_dir)
    config_manager = ConfigManager(workspace_dir)

    return logger, state_manager, file_ops, config_manager


def load_task_data(task_dir: Path, file_ops: FileOperations) -> dict:
    """Load task data from state.json (TAC-7 convention)"""
    state_file = task_dir / "state.json"
    return file_ops.read_json_file(state_file)


def execute_planning_stage(task_data: dict, task_dir: Path, logger: WorkflowLogger,
                          file_ops: FileOperations, state_manager: StateManager) -> bool:
    """Execute the planning stage using ADW modules"""
    try:
        adw_id = task_data['adw_id']
        logger.log_stage_start("plan")

        # Update state to show planning in progress
        state_manager.add_log(adw_id, "info", "plan", "Starting planning stage")

        # Analyze task description and type
        description = task_data.get('description', '')
        task_type = task_data.get('type', 'feature')

        # Generate planning output based on task type
        if task_type == 'feature':
            plan = generate_feature_plan(description, logger)
        elif task_type == 'bug':
            plan = generate_bug_fix_plan(description, logger)
        elif task_type == 'chore':
            plan = generate_chore_plan(description, logger)
        else:
            plan = generate_generic_plan(description, logger)

        # Save planning output using file_ops
        plan_output = {
            "stage": "plan",
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
            "task_id": adw_id,
            "plan": plan,
            "estimated_effort": plan.get('estimated_hours', 2),
            "dependencies": plan.get('dependencies', []),
            "risks": plan.get('risks', [])
        }

        output_file = task_dir / "plan_output.json"
        success = file_ops.write_json_file(output_file, plan_output)

        if not success:
            raise Exception("Failed to write plan output file")

        # Update state with completion
        state_manager.add_log(adw_id, "success", "plan", "Planning stage completed successfully")
        logger.log_stage_complete("plan")
        return True

    except Exception as e:
        logger.log_stage_error("plan", str(e))
        if 'adw_id' in locals():
            state_manager.add_log(adw_id, "error", "plan", f"Planning stage failed: {e}")
        return False


def generate_feature_plan(description: str, logger) -> dict:
    """Generate a plan for a feature development task"""
    logger.info("Generating feature development plan")

    # Basic feature analysis
    plan = {
        "type": "feature_development",
        "phases": [
            {
                "name": "Analysis",
                "description": "Analyze requirements and design approach",
                "estimated_hours": 1
            },
            {
                "name": "Design",
                "description": "Create technical design and architecture",
                "estimated_hours": 2
            },
            {
                "name": "Implementation",
                "description": "Develop the feature according to design",
                "estimated_hours": 4
            },
            {
                "name": "Testing",
                "description": "Test the feature and fix issues",
                "estimated_hours": 2
            }
        ],
        "estimated_hours": 9,
        "dependencies": ["UI framework", "Database access"],
        "risks": ["Complexity underestimation", "Integration challenges"],
        "deliverables": [
            "Feature implementation",
            "Unit tests",
            "Integration tests",
            "Documentation"
        ]
    }

    # Add description-specific planning
    if "api" in description.lower():
        plan["dependencies"].append("API documentation")
        plan["phases"].append({
            "name": "API Integration",
            "description": "Integrate with external APIs",
            "estimated_hours": 2
        })

    if "ui" in description.lower() or "interface" in description.lower():
        plan["dependencies"].append("UI/UX design")
        plan["deliverables"].append("UI components")

    return plan


def generate_bug_fix_plan(description: str, logger) -> dict:
    """Generate a plan for bug fix task"""
    logger.info("Generating bug fix plan")

    plan = {
        "type": "bug_fix",
        "phases": [
            {
                "name": "Investigation",
                "description": "Investigate and reproduce the bug",
                "estimated_hours": 1
            },
            {
                "name": "Root Cause Analysis",
                "description": "Identify the root cause of the issue",
                "estimated_hours": 1
            },
            {
                "name": "Fix Implementation",
                "description": "Implement the fix",
                "estimated_hours": 2
            },
            {
                "name": "Verification",
                "description": "Verify the fix and test edge cases",
                "estimated_hours": 1
            }
        ],
        "estimated_hours": 5,
        "dependencies": ["Bug reproduction environment"],
        "risks": ["Side effects", "Incomplete fix"],
        "deliverables": [
            "Bug fix implementation",
            "Test cases",
            "Fix verification"
        ]
    }

    return plan


def generate_chore_plan(description: str, logger) -> dict:
    """Generate a plan for chore/maintenance task"""
    logger.info("Generating chore/maintenance plan")

    plan = {
        "type": "chore",
        "phases": [
            {
                "name": "Assessment",
                "description": "Assess current state and requirements",
                "estimated_hours": 0.5
            },
            {
                "name": "Execution",
                "description": "Perform the maintenance task",
                "estimated_hours": 1.5
            },
            {
                "name": "Validation",
                "description": "Validate the changes",
                "estimated_hours": 0.5
            }
        ],
        "estimated_hours": 2.5,
        "dependencies": [],
        "risks": ["Breaking existing functionality"],
        "deliverables": [
            "Updated configuration/code",
            "Validation report"
        ]
    }

    return plan


def generate_generic_plan(description: str, logger) -> dict:
    """Generate a generic plan for unknown task types"""
    logger.info("Generating generic plan")

    plan = {
        "type": "generic",
        "phases": [
            {
                "name": "Analysis",
                "description": "Analyze task requirements",
                "estimated_hours": 1
            },
            {
                "name": "Execution",
                "description": "Execute the task",
                "estimated_hours": 3
            },
            {
                "name": "Review",
                "description": "Review and finalize",
                "estimated_hours": 1
            }
        ],
        "estimated_hours": 5,
        "dependencies": [],
        "risks": ["Unclear requirements"],
        "deliverables": ["Task completion"]
    }

    return plan


def main():
    parser = argparse.ArgumentParser(description="Planning Pipeline (ADW System)")
    parser.add_argument("--task-id", required=True, help="Task ID")
    parser.add_argument("--task-dir", required=True, type=Path, help="Task directory")
    parser.add_argument("--stage", required=True, help="Stage name")

    args = parser.parse_args()

    try:
        # Determine workspace directory
        workspace_dir = args.task_dir.parent.parent.parent

        # Setup pipeline context
        logger, state_manager, file_ops, config_manager = setup_pipeline_context(
            args.task_id, args.task_dir, workspace_dir
        )

        # Load task data from state.json
        task_data = load_task_data(args.task_dir, file_ops)
        if not task_data:
            raise Exception("Failed to load task data from state.json")

        # Execute planning stage
        success = execute_planning_stage(
            task_data, args.task_dir, logger, file_ops, state_manager
        )

        if success:
            logger.info("Planning pipeline completed successfully")
            sys.exit(0)
        else:
            logger.error("Planning pipeline failed")
            sys.exit(1)

    except Exception as e:
        if 'logger' in locals():
            logger.error(f"Planning pipeline error: {e}")
        else:
            print(f"Planning pipeline error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Test script for the ADWS system
Creates a sample task and triggers execution
"""

import json
import time
from pathlib import Path
from datetime import datetime


def create_test_task():
    """Create a test task to verify the system works"""

    # Get workspace directory
    workspace_dir = Path(__file__).parent.parent.parent
    adws_dir = workspace_dir / "agentics" / "adws"
    agents_dir = workspace_dir / "agentics" / "agents"

    # Create test task data
    adw_id = f"test_{int(time.time() * 1000)}_{hash('test_task') % 10000}"

    task_data = {
        "adw_id": adw_id,
        "title": "Test Feature Implementation",
        "description": "This is a test task to verify the ADWS system is working correctly. It should go through all stages: plan, implement, test, and review.",
        "type": "feature",
        "priority": "medium",
        "stages": ["plan", "implement", "test", "review"],
        "created_at": datetime.now().isoformat(),
        "project_context": {},
        "execution_mode": "automatic",
        "triggered_at": datetime.now().isoformat(),
        "kanban_integration": True,
        "trigger_source": "test_script",
        "ui_metadata": {
            "test_run": True,
            "timestamp": datetime.now().isoformat()
        }
    }

    # Create task directory
    task_dir = agents_dir / adw_id
    task_dir.mkdir(parents=True, exist_ok=True)

    # Write task data to state.json (TAC-7 convention)
    state_file = task_dir / "state.json"
    with open(state_file, 'w') as f:
        task_data['workflow_status'] = 'initialized'
        json.dump(task_data, f, indent=2)

    # Create trigger file
    trigger_data = {
        "adw_id": adw_id,
        "action": "execute",
        "task_file": f"../agents/{adw_id}/state.json",
        "created_at": datetime.now().isoformat(),
        "status": "pending"
    }

    trigger_file = adws_dir / f"trigger_{adw_id}.json"
    with open(trigger_file, 'w') as f:
        json.dump(trigger_data, f, indent=2)

    print(f"✓ Created test task: {adw_id}")
    print(f"✓ Task data written to: {state_file}")
    print(f"✓ Trigger file created: {trigger_file}")
    print(f"\nTo monitor execution:")
    print(f"  watch cat {task_dir}/state.json")
    print(f"\nTo start the orchestrator:")
    print(f"  cd {adws_dir}")
    print(f"  ./start_orchestrator.sh")

    return adw_id, task_dir


def check_system_setup():
    """Check if the ADWS system is properly set up"""
    workspace_dir = Path(__file__).parent.parent.parent
    adws_dir = workspace_dir / "agentics" / "adws"

    print("Checking ADWS system setup...")

    # Check required directories
    required_dirs = [
        adws_dir,
        adws_dir / "pipelines",
        workspace_dir / "agentics" / "agents"
    ]

    for dir_path in required_dirs:
        if dir_path.exists():
            print(f"✓ {dir_path.relative_to(workspace_dir)} exists")
        else:
            print(f"✗ {dir_path.relative_to(workspace_dir)} missing")
            return False

    # Check required files
    required_files = [
        adws_dir / "adw_orchestrator.py",
        adws_dir / "pipelines" / "plan_pipeline.py",
        adws_dir / "pipelines" / "implement_pipeline.py",
        adws_dir / "pipelines" / "test_pipeline.py",
        adws_dir / "pipelines" / "review_pipeline.py"
    ]

    for file_path in required_files:
        if file_path.exists():
            print(f"✓ {file_path.relative_to(workspace_dir)} exists")
        else:
            print(f"✗ {file_path.relative_to(workspace_dir)} missing")
            return False

    print("\n✓ All required components are present!")
    return True


def main():
    print("ADWS System Test")
    print("=" * 50)

    # Check system setup
    if not check_system_setup():
        print("\n❌ System setup incomplete. Please ensure all files are in place.")
        return

    print()

    # Create test task
    try:
        adw_id, task_dir = create_test_task()
        print(f"\n✅ Test task created successfully!")
        print(f"\nNext steps:")
        print(f"1. Start the orchestrator in another terminal")
        print(f"2. Monitor the task execution")
        print(f"3. Check the generated output files in: {task_dir}")

    except Exception as e:
        print(f"\n❌ Failed to create test task: {e}")


if __name__ == "__main__":
    main()
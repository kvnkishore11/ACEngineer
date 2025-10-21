#!/usr/bin/env python3
"""
TAC-7 Compatible PLAN Phase Pipeline
🎯 PLAN Phase (adw_plan_iso.py)

Substages:
1. State Initialization - Load/create ADW state with ensure_adw_id()
2. Environment Setup - Port allocation, worktree creation, environment files
3. Issue Analysis - Issue classification and branch generation
4. Plan Generation - Worktree installation, plan creation, validation
5. Git Operations - Commit creation, plan commit, PR creation

Following TAC-7 architecture for isolated workflow execution
"""

import json
import sys
import argparse
import subprocess
import os
from pathlib import Path
from datetime import datetime

# Import ADW modules
sys.path.append(str(Path(__file__).parent.parent / "adw_modules"))
from logger import WorkflowLogger
from adw_state import ADWState, WorkflowPhase, WorkflowStatus
from worktree_ops import WorktreeOperations
from file_ops import FileOperations
from config_manager import ConfigManager


class ADWPlanPipeline:
    """TAC-7 Compatible PLAN Phase Pipeline"""

    def __init__(self, workspace_dir: Path, adw_id: str):
        self.workspace_dir = workspace_dir
        self.adw_id = adw_id

        # Initialize ADW modules
        self.logger = WorkflowLogger(adw_id, "plan")
        self.adw_state = ADWState(workspace_dir)
        self.worktree_ops = WorktreeOperations(workspace_dir)
        self.file_ops = FileOperations(workspace_dir)
        self.config = ConfigManager(workspace_dir).get_workflow_config()

    def execute_plan_phase(self, task_data: dict) -> bool:
        """
        Execute complete PLAN phase following TAC-7 substages
        """
        try:
            self.logger.log_stage_start("plan")

            # Substage 1: State Initialization (66-95)
            if not self._initialize_adw_state(task_data):
                return False

            # Substage 2: Environment Setup (108-127)
            if not self._setup_environment():
                return False

            # Substage 3: Issue Analysis (128-158)
            if not self._analyze_issue():
                return False

            # Substage 4: Plan Generation (179-218)
            if not self._generate_plan():
                return False

            # Substage 5: Git Operations (285-328)
            if not self._handle_git_operations():
                return False

            self.logger.log_stage_complete("plan")
            return True

        except Exception as e:
            self.logger.log_stage_error("plan", str(e))
            return False

    def _initialize_adw_state(self, task_data: dict) -> bool:
        """
        Substage 1: State Initialization
        Load/create ADW state with ensure_adw_id()
        Track workflow execution in all_adws list
        """
        try:
            self.logger.info("Initializing ADW state")

            # Ensure ADW ID and initialize state
            self.adw_state.ensure_adw_id(task_data)
            state = self.adw_state.initialize_state(task_data)

            if not state:
                raise Exception("Failed to initialize ADW state")

            # Update phase status
            self.adw_state.update_phase(self.adw_id, WorkflowPhase.PLAN, WorkflowStatus.EXECUTING)

            self.logger.info(f"ADW state initialized for {self.adw_id}")
            return True

        except Exception as e:
            self.logger.error(f"State initialization failed: {e}")
            return False

    def _setup_environment(self) -> bool:
        """
        Substage 2: Environment Setup
        Port Allocation: Deterministic backend/frontend ports (9100-9114/9200-9214)
        Worktree Creation: Isolated git worktree in trees/{adw_id}/
        Environment Files: Create .ports.env with port configuration
        """
        try:
            self.logger.info("Setting up isolated environment")

            # Load state to get configuration
            state = self.adw_state.load_state(self.adw_id)
            if not state:
                raise Exception("State not found")

            # Create worktree
            self.logger.info(f"Creating worktree with branch: {state.branch_name}")

            worktree_result = self.worktree_ops.create_worktree(
                self.adw_id,
                state.branch_name
            )

            if not worktree_result["success"]:
                raise Exception(f"Worktree creation failed: {worktree_result.get('error', 'Unknown error')}")

            # Update state with worktree information
            state.worktree_path = worktree_result["worktree_path"]
            state.backend_port = worktree_result["backend_port"]
            state.frontend_port = worktree_result["frontend_port"]

            self.adw_state.save_state(state)

            self.logger.info(f"Environment setup complete - Worktree: {state.worktree_path}, Ports: {state.backend_port}/{state.frontend_port}")
            return True

        except Exception as e:
            self.logger.error(f"Environment setup failed: {e}")
            return False

    def _analyze_issue(self) -> bool:
        """
        Substage 3: Issue Analysis
        Issue Classification: Use /classify_issue → /chore|/bug|/feature
        Branch Generation: Create standardized branch name via /generate_branch_name
        """
        try:
            self.logger.info("Analyzing issue and classifying task")

            state = self.adw_state.load_state(self.adw_id)
            if not state:
                raise Exception("State not found")

            # Issue classification based on description and type
            issue_type = self._classify_issue(state.description, state.type)

            # Update state with classification
            state.type = issue_type
            self.adw_state.save_state(state)

            self.logger.info(f"Issue classified as: {issue_type}")
            return True

        except Exception as e:
            self.logger.error(f"Issue analysis failed: {e}")
            return False

    def _generate_plan(self) -> bool:
        """
        Substage 4: Plan Generation
        Worktree Installation: Run /install_worktree command for environment setup
        Plan Creation: Execute classified command (/chore, /bug, /feature) in worktree
        Plan Validation: Ensure plan file exists in worktree
        """
        try:
            self.logger.info("Generating plan")

            state = self.adw_state.load_state(self.adw_id)
            if not state:
                raise Exception("State not found")

            # Install worktree dependencies
            self.logger.info("Installing worktree dependencies")
            install_success = self.worktree_ops.install_worktree_dependencies(self.adw_id)
            if not install_success:
                self.logger.warning("Worktree installation had issues, continuing...")

            # Generate plan based on issue type
            plan = self._create_plan_by_type(state.type, state.description, state.title)

            # Save plan to worktree
            worktree_path = Path(state.worktree_path)
            plan_file = worktree_path / f"{state.type}_plan.md"

            success = self.file_ops.write_text_file(plan_file, plan)
            if not success:
                raise Exception("Failed to write plan file")

            # Update state with plan file path
            state.plan_file = str(plan_file)
            self.adw_state.save_state(state)

            self.logger.info(f"Plan generated and saved to: {plan_file}")
            return True

        except Exception as e:
            self.logger.error(f"Plan generation failed: {e}")
            return False

    def _handle_git_operations(self) -> bool:
        """
        Substage 5: Git Operations
        Commit Creation: Generate semantic commit message
        Plan Commit: Commit plan to isolated branch
        PR Creation: Push and create/update pull request
        """
        try:
            self.logger.info("Handling git operations")

            state = self.adw_state.load_state(self.adw_id)
            if not state:
                raise Exception("State not found")

            worktree_path = Path(state.worktree_path)

            # Stage plan file
            subprocess.run(
                ["git", "add", state.plan_file],
                cwd=worktree_path,
                check=True
            )

            # Create semantic commit message
            commit_msg = f"feat: Add {state.type} plan for {state.title}\n\n- Generated comprehensive plan for {state.type}\n- Includes implementation strategy and timeline"

            # Commit plan
            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=worktree_path,
                check=True
            )

            # Push branch
            subprocess.run(
                ["git", "push", "-u", "origin", state.branch_name],
                cwd=worktree_path,
                check=True
            )

            self.logger.info(f"Plan committed and pushed to branch: {state.branch_name}")

            # Mark plan phase as complete
            self.adw_state.complete_phase(self.adw_id, WorkflowPhase.PLAN)

            return True

        except Exception as e:
            self.logger.error(f"Git operations failed: {e}")
            return False

    def _classify_issue(self, description: str, current_type: str) -> str:
        """
        Classify issue type based on description
        Equivalent to TAC-7 /classify_issue command
        """
        description_lower = description.lower()

        # Bug indicators
        if any(keyword in description_lower for keyword in [
            'bug', 'error', 'fail', 'broken', 'fix', 'issue', 'problem'
        ]):
            return 'bug'

        # Chore indicators
        if any(keyword in description_lower for keyword in [
            'refactor', 'cleanup', 'maintenance', 'update', 'upgrade', 'chore'
        ]):
            return 'chore'

        # Feature indicators (default)
        if any(keyword in description_lower for keyword in [
            'feature', 'add', 'implement', 'create', 'new', 'enhancement'
        ]) or current_type == 'feature':
            return 'feature'

        # Default to current type
        return current_type

    def _create_plan_by_type(self, issue_type: str, description: str, title: str) -> str:
        """
        Create plan based on issue type
        Equivalent to TAC-7 /chore, /bug, /feature commands
        """
        timestamp = datetime.now().isoformat()

        if issue_type == 'bug':
            return f"""# Bug Fix Plan: {title}

## Issue Description
{description}

## Root Cause Analysis
1. **Investigation Steps**
   - Reproduce the bug in development environment
   - Identify the root cause through debugging
   - Analyze impact and affected components

2. **Fix Strategy**
   - Implement targeted fix for root cause
   - Ensure no regression in existing functionality
   - Add appropriate error handling

## Implementation Plan
1. **Investigation Phase**
   - Set up reproduction environment
   - Debug and trace issue
   - Document findings

2. **Fix Implementation**
   - Implement fix with minimal impact
   - Add/update unit tests
   - Verify fix resolves issue

3. **Validation**
   - Test fix thoroughly
   - Ensure no regressions
   - Document changes

## Success Criteria
- Bug is resolved without introducing new issues
- Existing functionality remains intact
- Appropriate tests are added/updated

Generated: {timestamp}
"""

        elif issue_type == 'chore':
            return f"""# Maintenance/Chore Plan: {title}

## Task Description
{description}

## Maintenance Strategy
1. **Assessment**
   - Review current state
   - Identify improvement areas
   - Plan implementation approach

2. **Execution**
   - Implement changes systematically
   - Maintain code quality standards
   - Update documentation as needed

## Implementation Plan
1. **Preparation**
   - Backup current state if needed
   - Review dependencies and impacts
   - Plan rollback strategy

2. **Implementation**
   - Execute maintenance tasks
   - Test changes thoroughly
   - Update related documentation

3. **Validation**
   - Verify improvements
   - Ensure no functionality is broken
   - Update any automated processes

## Success Criteria
- Maintenance task completed successfully
- Code quality improved or maintained
- No functional regressions introduced

Generated: {timestamp}
"""

        else:  # feature
            return f"""# Feature Development Plan: {title}

## Feature Description
{description}

## Architecture Overview
1. **Feature Analysis**
   - Requirements gathering and analysis
   - Technical design and architecture
   - Integration planning

2. **Development Strategy**
   - Component-based development
   - Test-driven development approach
   - Incremental implementation

## Implementation Plan
1. **Design Phase**
   - Create technical specification
   - Design user interface mockups
   - Plan database schema changes if needed

2. **Development Phase**
   - Implement core functionality
   - Create user interface components
   - Integrate with existing systems

3. **Testing Phase**
   - Unit testing for all components
   - Integration testing
   - User acceptance testing

4. **Documentation**
   - Update user documentation
   - Create technical documentation
   - Update API documentation if applicable

## Success Criteria
- Feature meets all specified requirements
- Code passes all quality gates
- Feature is properly tested and documented

Generated: {timestamp}
"""


def main():
    parser = argparse.ArgumentParser(description="TAC-7 PLAN Phase Pipeline")
    parser.add_argument("--task-id", required=True, help="Task ID")
    parser.add_argument("--task-dir", required=True, type=Path, help="Task directory")
    parser.add_argument("--stage", required=True, help="Stage name")

    args = parser.parse_args()

    try:
        # Determine workspace directory
        workspace_dir = args.task_dir.parent.parent.parent

        # Load task data from state.json
        state_file = args.task_dir / "state.json"
        file_ops = FileOperations(workspace_dir)
        task_data = file_ops.read_json_file(state_file)

        if not task_data:
            raise Exception("Failed to load task data from state.json")

        # Execute PLAN phase
        pipeline = ADWPlanPipeline(workspace_dir, args.task_id)
        success = pipeline.execute_plan_phase(task_data)

        if success:
            print("PLAN phase completed successfully")
            sys.exit(0)
        else:
            print("PLAN phase failed")
            sys.exit(1)

    except Exception as e:
        print(f"PLAN phase error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
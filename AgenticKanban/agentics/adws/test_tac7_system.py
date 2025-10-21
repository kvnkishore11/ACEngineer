#!/usr/bin/env python3
"""
TAC-7 System Validation Test
Comprehensive test to validate TAC-7 compatibility and implementation
"""

import json
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Import ADW modules
sys.path.append(str(Path(__file__).parent / "adw_modules"))
from adw_state import ADWState, WorkflowPhase, WorkflowStatus
from worktree_ops import WorktreeOperations
from file_ops import FileOperations
from logger import setup_logger


class TAC7SystemValidator:
    """Comprehensive TAC-7 system validation"""

    def __init__(self, workspace_dir: Path):
        self.workspace_dir = workspace_dir
        self.logger = setup_logger("tac7_validator")

        # Initialize all TAC-7 modules
        self.adw_state = ADWState(workspace_dir)
        self.worktree_ops = WorktreeOperations(workspace_dir)
        self.file_ops = FileOperations(workspace_dir)

        self.test_results = {
            "persistent_state": False,
            "worktree_architecture": False,
            "port_allocation": False,
            "environment_isolation": False,
            "workflow_tracking": False,
            "validation_system": False,
            "git_integration": False
        }

    def run_comprehensive_validation(self) -> bool:
        """Run all TAC-7 validation tests"""

        print("🚀 Starting TAC-7 System Validation")
        print("=" * 60)

        # Test 1: Persistent State Management
        print("\n1️⃣ Testing Persistent State Management...")
        self.test_results["persistent_state"] = self._test_persistent_state()

        # Test 2: Isolated Worktree Architecture
        print("\n2️⃣ Testing Isolated Worktree Architecture...")
        self.test_results["worktree_architecture"] = self._test_worktree_architecture()

        # Test 3: Port Allocation System
        print("\n3️⃣ Testing Port Allocation System...")
        self.test_results["port_allocation"] = self._test_port_allocation()

        # Test 4: Environment Isolation
        print("\n4️⃣ Testing Environment Isolation...")
        self.test_results["environment_isolation"] = self._test_environment_isolation()

        # Test 5: Workflow Tracking
        print("\n5️⃣ Testing Workflow Tracking...")
        self.test_results["workflow_tracking"] = self._test_workflow_tracking()

        # Test 6: Validation System
        print("\n6️⃣ Testing Three-way Validation...")
        self.test_results["validation_system"] = self._test_validation_system()

        # Test 7: Git Integration
        print("\n7️⃣ Testing Git Integration...")
        self.test_results["git_integration"] = self._test_git_integration()

        # Summary
        self._print_test_summary()

        return all(self.test_results.values())

    def _test_persistent_state(self) -> bool:
        """Test TAC-7 persistent state management"""
        try:
            # Test state initialization
            task_data = {
                'title': 'TAC-7 State Test',
                'description': 'Testing persistent state management',
                'type': 'feature',
                'issue_number': 123
            }

            # Initialize state
            state = self.adw_state.initialize_state(task_data)

            # Verify TAC-7 required fields
            required_fields = [
                'adw_id', 'issue_number', 'branch_name', 'worktree_path',
                'backend_port', 'frontend_port', 'model_set', 'all_adws'
            ]

            for field in required_fields:
                if not hasattr(state, field):
                    print(f"   ❌ Missing required field: {field}")
                    return False

            # Test state persistence
            saved_state = self.adw_state.load_state(state.adw_id)
            if not saved_state:
                print("   ❌ State not persisted")
                return False

            # Verify state file location (TAC-7 convention)
            state_file = self.workspace_dir / "agentics" / "agents" / state.adw_id / "adw_state.json"
            if not state_file.exists():
                print("   ❌ State file not at TAC-7 path: agents/{adw_id}/adw_state.json")
                return False

            print("   ✅ Persistent state management validated")
            return True

        except Exception as e:
            print(f"   ❌ Persistent state test failed: {e}")
            return False

    def _test_worktree_architecture(self) -> bool:
        """Test isolated worktree architecture"""
        try:
            # Create test state
            task_data = {
                'title': 'Worktree Test',
                'description': 'Testing worktree isolation',
                'type': 'feature'
            }

            state = self.adw_state.initialize_state(task_data)

            # Test worktree creation
            worktree_result = self.worktree_ops.create_worktree(
                state.adw_id,
                state.branch_name
            )

            if not worktree_result["success"]:
                print(f"   ❌ Worktree creation failed: {worktree_result.get('error')}")
                return False

            # Verify worktree location (TAC-7: trees/{adw_id}/)
            expected_path = self.workspace_dir / "trees" / state.adw_id
            if not expected_path.exists():
                print(f"   ❌ Worktree not at TAC-7 path: trees/{state.adw_id}/")
                return False

            # Test git worktree recognition
            worktrees = self.worktree_ops.list_worktrees()
            worktree_found = any(str(expected_path) in wt.get('path', '') for wt in worktrees)

            if not worktree_found:
                print("   ❌ Git worktree not recognized")
                return False

            print("   ✅ Isolated worktree architecture validated")

            # Cleanup
            self.worktree_ops.remove_worktree(state.adw_id)
            return True

        except Exception as e:
            print(f"   ❌ Worktree architecture test failed: {e}")
            return False

    def _test_port_allocation(self) -> bool:
        """Test deterministic port allocation system"""
        try:
            # Test multiple ADWs get different ports
            adw_ids = []
            ports_used = set()

            for i in range(3):
                task_data = {
                    'title': f'Port Test {i}',
                    'description': f'Testing port allocation {i}',
                    'type': 'feature'
                }

                state = self.adw_state.initialize_state(task_data)
                adw_ids.append(state.adw_id)

                # Verify port ranges (TAC-7: backend 9100-9114, frontend 9200-9214)
                if not (9100 <= state.backend_port <= 9114):
                    print(f"   ❌ Backend port {state.backend_port} outside TAC-7 range 9100-9114")
                    return False

                if not (9200 <= state.frontend_port <= 9214):
                    print(f"   ❌ Frontend port {state.frontend_port} outside TAC-7 range 9200-9214")
                    return False

                port_pair = (state.backend_port, state.frontend_port)
                if port_pair in ports_used:
                    print(f"   ❌ Port collision: {port_pair}")
                    return False

                ports_used.add(port_pair)

            # Test deterministic allocation (same ADW ID should get same ports)
            test_id = "test_deterministic_123"
            backend1, frontend1 = self.adw_state.allocate_ports(test_id)
            backend2, frontend2 = self.adw_state.allocate_ports(test_id)

            if backend1 != backend2 or frontend1 != frontend2:
                print(f"   ❌ Port allocation not deterministic: {backend1}/{frontend1} vs {backend2}/{frontend2}")
                return False

            print("   ✅ Port allocation system validated")
            return True

        except Exception as e:
            print(f"   ❌ Port allocation test failed: {e}")
            return False

    def _test_environment_isolation(self) -> bool:
        """Test environment isolation with .ports.env"""
        try:
            task_data = {
                'title': 'Environment Test',
                'description': 'Testing environment isolation',
                'type': 'feature'
            }

            state = self.adw_state.initialize_state(task_data)

            # Check .ports.env file exists
            ports_env_file = Path(state.worktree_path) / ".ports.env"
            if not ports_env_file.exists():
                print(f"   ❌ .ports.env file not created at {ports_env_file}")
                return False

            # Verify .ports.env content
            env_content = self.file_ops.read_text_file(ports_env_file)
            if not env_content:
                print("   ❌ .ports.env file is empty")
                return False

            # Check required environment variables
            required_vars = [
                f"BACKEND_PORT={state.backend_port}",
                f"FRONTEND_PORT={state.frontend_port}",
                f"VITE_BACKEND_URL=http://localhost:{state.backend_port}",
                f"ADW_ID={state.adw_id}"
            ]

            for var in required_vars:
                if var not in env_content:
                    print(f"   ❌ Missing environment variable: {var}")
                    return False

            print("   ✅ Environment isolation validated")
            return True

        except Exception as e:
            print(f"   ❌ Environment isolation test failed: {e}")
            return False

    def _test_workflow_tracking(self) -> bool:
        """Test workflow tracking with all_adws list"""
        try:
            # Create multiple ADWs
            adw_ids = []
            for i in range(3):
                task_data = {
                    'title': f'Workflow Test {i}',
                    'description': f'Testing workflow tracking {i}',
                    'type': 'feature'
                }

                state = self.adw_state.initialize_state(task_data)
                adw_ids.append(state.adw_id)

                # Verify this ADW is in all_adws list
                if state.adw_id not in state.all_adws:
                    print(f"   ❌ ADW {state.adw_id} not in all_adws list")
                    return False

            # Test workflow phase tracking
            test_adw = adw_ids[0]

            # Test phase updates
            phases = [WorkflowPhase.PLAN, WorkflowPhase.BUILD, WorkflowPhase.TEST]
            for phase in phases:
                success = self.adw_state.update_phase(test_adw, phase)
                if not success:
                    print(f"   ❌ Failed to update to phase {phase.value}")
                    return False

                # Complete phase
                success = self.adw_state.complete_phase(test_adw, phase)
                if not success:
                    print(f"   ❌ Failed to complete phase {phase.value}")
                    return False

            # Verify completed phases
            final_state = self.adw_state.load_state(test_adw)
            expected_phases = [p.value for p in phases]

            for phase in expected_phases:
                if phase not in final_state.completed_phases:
                    print(f"   ❌ Phase {phase} not in completed_phases")
                    return False

            print("   ✅ Workflow tracking validated")
            return True

        except Exception as e:
            print(f"   ❌ Workflow tracking test failed: {e}")
            return False

    def _test_validation_system(self) -> bool:
        """Test TAC-7 three-way validation system"""
        try:
            task_data = {
                'title': 'Validation Test',
                'description': 'Testing three-way validation',
                'type': 'feature'
            }

            state = self.adw_state.initialize_state(task_data)

            # Before worktree creation - should fail validation
            validation = self.adw_state.validate_worktree(state.adw_id)
            if validation["valid"]:
                print("   ❌ Validation should fail before worktree creation")
                return False

            # Create worktree
            worktree_result = self.worktree_ops.create_worktree(
                state.adw_id,
                state.branch_name
            )

            if not worktree_result["success"]:
                print("   ❌ Worktree creation failed")
                return False

            # Update state with worktree path
            state.worktree_path = worktree_result["worktree_path"]
            self.adw_state.save_state(state)

            # After worktree creation - should pass validation
            validation = self.adw_state.validate_worktree(state.adw_id)

            # Check all three validation criteria
            if not validation["state_has_path"]:
                print("   ❌ State doesn't have worktree_path")
                return False

            if not validation["directory_exists"]:
                print("   ❌ Worktree directory doesn't exist")
                return False

            if not validation["git_recognizes"]:
                print("   ❌ Git doesn't recognize worktree")
                return False

            if not validation["valid"]:
                print("   ❌ Overall validation failed")
                return False

            print("   ✅ Three-way validation system validated")

            # Cleanup
            self.worktree_ops.remove_worktree(state.adw_id)
            return True

        except Exception as e:
            print(f"   ❌ Validation system test failed: {e}")
            return False

    def _test_git_integration(self) -> bool:
        """Test git integration with branch management"""
        try:
            task_data = {
                'title': 'Git Integration Test',
                'description': 'Testing git branch integration',
                'type': 'feature',
                'issue_number': 456
            }

            state = self.adw_state.initialize_state(task_data)

            # Verify branch name format (TAC-7: {type}-{issue_number}-{clean_adw_id})
            # Clean ADW ID removes the "adw_" prefix and sanitizes (underscores become hyphens)
            clean_adw_id = state.adw_id.replace("adw_", "").replace("_", "-")
            expected_pattern = f"feature-456-{clean_adw_id}"
            if state.branch_name != expected_pattern:
                print(f"   ❌ Branch name format incorrect: expected {expected_pattern}, got {state.branch_name}")
                return False

            # Create worktree with branch
            worktree_result = self.worktree_ops.create_worktree(
                state.adw_id,
                state.branch_name
            )

            if not worktree_result["success"]:
                print("   ❌ Git worktree creation failed")
                return False

            # Verify branch exists
            worktree_path = Path(worktree_result["worktree_path"])
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=worktree_path,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print("   ❌ Git branch query failed")
                return False

            current_branch = result.stdout.strip()
            if current_branch != state.branch_name:
                print(f"   ❌ Branch mismatch: expected {state.branch_name}, got {current_branch}")
                return False

            print("   ✅ Git integration validated")

            # Cleanup
            self.worktree_ops.remove_worktree(state.adw_id)
            return True

        except Exception as e:
            print(f"   ❌ Git integration test failed: {e}")
            return False

    def _print_test_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("📊 TAC-7 Validation Summary")
        print("=" * 60)

        total_tests = len(self.test_results)
        passed_tests = sum(self.test_results.values())

        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            display_name = test_name.replace("_", " ").title()
            print(f"{status} {display_name}")

        print("-" * 60)
        print(f"Results: {passed_tests}/{total_tests} tests passed")

        if passed_tests == total_tests:
            print("🎉 TAC-7 Implementation Fully Validated!")
        else:
            print("⚠️  TAC-7 Implementation Needs Attention")


def main():
    """Run TAC-7 system validation"""
    workspace_dir = Path(__file__).parent.parent.parent
    validator = TAC7SystemValidator(workspace_dir)

    success = validator.run_comprehensive_validation()

    if success:
        print("\n✅ TAC-7 System Validation PASSED")
        return 0
    else:
        print("\n❌ TAC-7 System Validation FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
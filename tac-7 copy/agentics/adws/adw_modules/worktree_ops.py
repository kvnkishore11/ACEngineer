"""
TAC-7 Compatible Worktree Operations
Isolated Worktree Architecture for parallel ADW execution

Features:
- Worktree Creation: trees/{adw_id}/ directory structure
- Branch creation: git worktree add -b {branch_name} {path} origin/main
- Port Allocation: Deterministic backend (9100-9114) and frontend (9200-9214) ports
- Environment Isolation: .ports.env with BACKEND_PORT, FRONTEND_PORT, VITE_BACKEND_URL
- Three-way Validation: State + Filesystem + Git validation
"""

import subprocess
import shutil
from pathlib import Path
from typing import Dict, Optional, Tuple, List
import os

from logger import get_logger
from adw_state import ADWState, WorkflowStatus


class WorktreeOperations:
    """
    TAC-7 Compatible Worktree Operations Manager
    Handles isolated git worktree management for parallel ADW execution
    """

    def __init__(self, workspace_dir: Path):
        self.workspace_dir = Path(workspace_dir)
        self.trees_dir = self.workspace_dir / "trees"
        self.logger = get_logger("worktree_ops")

        # Ensure trees directory exists
        self.trees_dir.mkdir(parents=True, exist_ok=True)

        # Initialize ADW state manager
        self.adw_state = ADWState(workspace_dir)

    def create_worktree(self, adw_id: str, branch_name: str,
                       base_branch: str = "main") -> Dict[str, any]:
        """
        Create isolated worktree following TAC-7 architecture
        Location: trees/{adw_id}/ directory
        Branch creation: git worktree add -b {branch_name} {path} origin/main

        Args:
            adw_id: ADW identifier
            branch_name: Name for new branch
            base_branch: Base branch to branch from (default: main)

        Returns:
            Dict with creation result and metadata
        """
        result = {
            "success": False,
            "worktree_path": None,
            "branch_name": branch_name,
            "backend_port": None,
            "frontend_port": None,
            "error": None
        }

        try:
            # Get worktree path
            worktree_path = self.trees_dir / adw_id
            result["worktree_path"] = str(worktree_path)

            # Remove existing worktree if it exists
            if worktree_path.exists():
                self.logger.warning(f"Removing existing worktree: {worktree_path}")
                self.remove_worktree(adw_id)

            # Create new worktree with branch
            self.logger.info(f"Creating worktree for {adw_id} at {worktree_path}")

            # Git command: git worktree add -b {branch_name} {path} origin/{base_branch}
            cmd = [
                "git", "worktree", "add",
                "-b", branch_name,
                str(worktree_path),
                f"origin/{base_branch}"
            ]

            result_proc = subprocess.run(
                cmd,
                cwd=self.workspace_dir,
                capture_output=True,
                text=True
            )

            if result_proc.returncode != 0:
                raise Exception(f"Git worktree creation failed: {result_proc.stderr}")

            # Allocate ports
            backend_port, frontend_port = self.adw_state.allocate_ports(adw_id)
            result["backend_port"] = backend_port
            result["frontend_port"] = frontend_port

            # Create .ports.env file
            env_success = self.adw_state.create_ports_env(adw_id, backend_port, frontend_port)
            if not env_success:
                self.logger.warning(f"Failed to create .ports.env for {adw_id}")

            # Create package.json and other necessary files for isolation
            self._setup_worktree_environment(worktree_path, adw_id, backend_port, frontend_port)

            result["success"] = True
            self.logger.info(f"Successfully created worktree for {adw_id}")

        except Exception as e:
            error_msg = f"Failed to create worktree for {adw_id}: {e}"
            self.logger.error(error_msg)
            result["error"] = error_msg

            # Cleanup on failure
            if worktree_path.exists():
                try:
                    self.remove_worktree(adw_id)
                except:
                    pass

        return result

    def remove_worktree(self, adw_id: str) -> bool:
        """
        Remove worktree and cleanup
        """
        try:
            worktree_path = self.trees_dir / adw_id

            # Remove git worktree
            if worktree_path.exists():
                # First try git worktree remove
                try:
                    subprocess.run(
                        ["git", "worktree", "remove", str(worktree_path), "--force"],
                        cwd=self.workspace_dir,
                        capture_output=True,
                        text=True,
                        check=True
                    )
                except subprocess.CalledProcessError:
                    # If git remove fails, manually delete directory
                    shutil.rmtree(worktree_path, ignore_errors=True)

            self.logger.info(f"Removed worktree for {adw_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to remove worktree for {adw_id}: {e}")
            return False

    def validate_worktree(self, adw_id: str) -> Dict[str, bool]:
        """
        TAC-7 Three-way Worktree Validation:
        1. State has worktree_path
        2. Directory exists on filesystem
        3. Git recognizes the worktree
        """
        return self.adw_state.validate_worktree(adw_id)

    def list_worktrees(self) -> List[Dict[str, str]]:
        """
        List all git worktrees
        """
        try:
            result = subprocess.run(
                ["git", "worktree", "list", "--porcelain"],
                cwd=self.workspace_dir,
                capture_output=True,
                text=True
            )

            worktrees = []
            if result.returncode == 0:
                current_worktree = {}
                for line in result.stdout.strip().split('\n'):
                    if line.startswith('worktree '):
                        if current_worktree:
                            worktrees.append(current_worktree)
                        current_worktree = {'path': line[9:]}
                    elif line.startswith('branch '):
                        current_worktree['branch'] = line[7:]
                    elif line.startswith('HEAD '):
                        current_worktree['head'] = line[5:]

                if current_worktree:
                    worktrees.append(current_worktree)

            return worktrees

        except Exception as e:
            self.logger.error(f"Failed to list worktrees: {e}")
            return []

    def get_worktree_status(self, adw_id: str) -> Dict[str, any]:
        """
        Get comprehensive worktree status
        """
        worktree_path = self.trees_dir / adw_id
        status = {
            "adw_id": adw_id,
            "path": str(worktree_path),
            "exists": worktree_path.exists(),
            "is_git_worktree": False,
            "branch": None,
            "ports_env_exists": False,
            "validation": self.validate_worktree(adw_id)
        }

        if worktree_path.exists():
            # Check if .ports.env exists
            ports_env = worktree_path / ".ports.env"
            status["ports_env_exists"] = ports_env.exists()

            # Get current branch
            try:
                result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    cwd=worktree_path,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    status["branch"] = result.stdout.strip()
                    status["is_git_worktree"] = True
            except:
                pass

        return status

    def _setup_worktree_environment(self, worktree_path: Path, adw_id: str,
                                  backend_port: int, frontend_port: int):
        """
        Setup isolated environment in worktree
        """
        try:
            # Create .env file for environment variables
            env_file = worktree_path / ".env"
            env_content = f"""# ADW Environment for {adw_id}
BACKEND_PORT={backend_port}
FRONTEND_PORT={frontend_port}
VITE_BACKEND_URL=http://localhost:{backend_port}
ADW_ID={adw_id}
NODE_ENV=development
"""
            with open(env_file, 'w') as f:
                f.write(env_content)

            # Copy package.json if it doesn't exist
            main_package_json = self.workspace_dir / "package.json"
            worktree_package_json = worktree_path / "package.json"

            if main_package_json.exists() and not worktree_package_json.exists():
                shutil.copy2(main_package_json, worktree_package_json)

            # Create vite.config.js with custom port if it doesn't exist
            vite_config = worktree_path / "vite.config.js"
            if not vite_config.exists():
                vite_content = f"""import {{ defineConfig }} from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({{
  plugins: [react()],
  server: {{
    port: {frontend_port},
    host: true
  }}
}})
"""
                with open(vite_config, 'w') as f:
                    f.write(vite_content)

            self.logger.info(f"Setup environment for worktree {adw_id}")

        except Exception as e:
            self.logger.error(f"Failed to setup worktree environment for {adw_id}: {e}")

    def install_worktree_dependencies(self, adw_id: str) -> bool:
        """
        Install dependencies in worktree (equivalent to /install_worktree command)
        """
        try:
            worktree_path = self.trees_dir / adw_id

            if not worktree_path.exists():
                self.logger.error(f"Worktree doesn't exist for {adw_id}")
                return False

            # Check if package.json exists
            package_json = worktree_path / "package.json"
            if not package_json.exists():
                self.logger.warning(f"No package.json found in worktree {adw_id}")
                return True  # Not an error if no package.json

            # Install npm dependencies
            self.logger.info(f"Installing dependencies for worktree {adw_id}")

            result = subprocess.run(
                ["npm", "install"],
                cwd=worktree_path,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                self.logger.error(f"npm install failed for {adw_id}: {result.stderr}")
                return False

            self.logger.info(f"Successfully installed dependencies for {adw_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to install dependencies for {adw_id}: {e}")
            return False

    def cleanup_old_worktrees(self, max_age_days: int = 7) -> int:
        """
        Cleanup old worktrees
        """
        cleanup_count = 0
        try:
            import time
            cutoff_time = time.time() - (max_age_days * 24 * 3600)

            for worktree_dir in self.trees_dir.iterdir():
                if worktree_dir.is_dir():
                    # Check modification time
                    mod_time = worktree_dir.stat().st_mtime
                    if mod_time < cutoff_time:
                        adw_id = worktree_dir.name
                        if self.remove_worktree(adw_id):
                            cleanup_count += 1
                            self.logger.info(f"Cleaned up old worktree: {adw_id}")

        except Exception as e:
            self.logger.error(f"Failed to cleanup old worktrees: {e}")

        return cleanup_count

    def get_available_ports(self) -> Dict[str, List[int]]:
        """
        Get list of available ports in TAC-7 ranges
        """
        # Get all active ADW states to see which ports are in use
        active_tasks = self.adw_state.list_active_tasks()
        used_backend_ports = set()
        used_frontend_ports = set()

        for adw_id in active_tasks:
            state = self.adw_state.load_state(adw_id)
            if state:
                if state.backend_port:
                    used_backend_ports.add(state.backend_port)
                if state.frontend_port:
                    used_frontend_ports.add(state.frontend_port)

        # TAC-7 port ranges
        backend_range = list(range(9100, 9115))  # 9100-9114
        frontend_range = list(range(9200, 9215))  # 9200-9214

        available_backend = [p for p in backend_range if p not in used_backend_ports]
        available_frontend = [p for p in frontend_range if p not in used_frontend_ports]

        return {
            "backend": available_backend,
            "frontend": available_frontend,
            "used_backend": list(used_backend_ports),
            "used_frontend": list(used_frontend_ports)
        }
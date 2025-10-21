"""
Configuration Manager for ADW workflows
Handles configuration loading, validation, and environment management
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, asdict, field

from logger import get_logger
from file_ops import FileOperations


@dataclass
class WorkflowConfig:
    """Default workflow configuration structure"""
    # Execution settings
    default_stages: List[str] = field(default_factory=lambda: ["plan", "implement", "test", "review"])
    execution_timeout: int = 600  # seconds
    polling_interval: int = 2  # seconds
    max_retries: int = 3

    # File settings
    workspace_dir: str = ""
    agents_dir: str = "agentics/agents"
    pipelines_dir: str = "agentics/adws/pipelines"
    logs_dir: str = "agentics/adws/logs"

    # Logging settings
    log_level: str = "INFO"
    log_to_console: bool = True
    log_to_file: bool = True
    max_log_files: int = 10

    # Pipeline settings
    pipeline_parallel_execution: bool = False
    pipeline_continue_on_failure: bool = False

    # Cleanup settings
    auto_cleanup_completed: bool = True
    cleanup_age_days: int = 7

    # Integration settings
    kanban_integration: bool = True
    api_enabled: bool = False
    webhook_enabled: bool = False


@dataclass
class PipelineConfig:
    """Pipeline-specific configuration"""
    name: str
    description: str = ""
    timeout: int = 300
    retry_count: int = 1
    dependencies: List[str] = field(default_factory=list)
    env_vars: Dict[str, str] = field(default_factory=dict)
    arguments: List[str] = field(default_factory=list)
    working_directory: str = ""


class ConfigManager:
    """
    Manages configuration for ADW workflows
    Supports hierarchical config (system > project > task)
    """

    def __init__(self, workspace_dir: Path = None):
        self.workspace_dir = Path(workspace_dir) if workspace_dir else Path.cwd()
        self.file_ops = FileOperations(self.workspace_dir)
        self.logger = get_logger("config_manager")

        # Configuration paths
        self.system_config_path = Path.home() / ".adw" / "config.json"
        self.project_config_path = self.workspace_dir / "agentics" / "adws" / "config.json"

        # Cached configurations
        self._workflow_config = None
        self._pipeline_configs = {}

    def get_workflow_config(self, reload: bool = False) -> WorkflowConfig:
        """
        Get merged workflow configuration

        Args:
            reload: Force reload from files

        Returns:
            WorkflowConfig object
        """
        if self._workflow_config is None or reload:
            self._workflow_config = self._load_workflow_config()

        return self._workflow_config

    def _load_workflow_config(self) -> WorkflowConfig:
        """Load and merge workflow configuration from multiple sources"""
        # Start with defaults
        config = WorkflowConfig()

        # Load system config
        system_config = self.file_ops.read_json_file(self.system_config_path)
        if system_config:
            self._merge_config_dict(config, system_config)
            self.logger.debug(f"Loaded system config from {self.system_config_path}")

        # Load project config
        project_config = self.file_ops.read_json_file(self.project_config_path)
        if project_config:
            self._merge_config_dict(config, project_config.get('workflow', {}))
            self.logger.debug(f"Loaded project config from {self.project_config_path}")

        # Apply environment variable overrides
        self._apply_env_overrides(config)

        # Set workspace_dir if not specified
        if not config.workspace_dir:
            config.workspace_dir = str(self.workspace_dir)

        return config

    def _merge_config_dict(self, config: WorkflowConfig, config_dict: Dict[str, Any]):
        """Merge configuration dictionary into WorkflowConfig object"""
        for key, value in config_dict.items():
            if hasattr(config, key):
                setattr(config, key, value)

    def _apply_env_overrides(self, config: WorkflowConfig):
        """Apply environment variable overrides"""
        env_mappings = {
            'ADW_LOG_LEVEL': 'log_level',
            'ADW_EXECUTION_TIMEOUT': ('execution_timeout', int),
            'ADW_POLLING_INTERVAL': ('polling_interval', int),
            'ADW_MAX_RETRIES': ('max_retries', int),
            'ADW_WORKSPACE_DIR': 'workspace_dir',
            'ADW_AUTO_CLEANUP': ('auto_cleanup_completed', lambda x: x.lower() == 'true'),
        }

        for env_var, mapping in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                if isinstance(mapping, tuple):
                    attr_name, converter = mapping
                    try:
                        setattr(config, attr_name, converter(value))
                    except (ValueError, TypeError) as e:
                        self.logger.warning(f"Invalid value for {env_var}: {value}, error: {e}")
                else:
                    setattr(config, mapping, value)

    def save_workflow_config(self, config: WorkflowConfig, scope: str = "project") -> bool:
        """
        Save workflow configuration

        Args:
            config: WorkflowConfig to save
            scope: "system" or "project"

        Returns:
            True if successful, False otherwise
        """
        try:
            config_dict = asdict(config)

            if scope == "system":
                # Save to system config
                self.file_ops.ensure_directory(self.system_config_path.parent)
                return self.file_ops.write_json_file(self.system_config_path, config_dict)

            elif scope == "project":
                # Save to project config (merge with existing)
                existing_config = self.file_ops.read_json_file(self.project_config_path) or {}
                existing_config['workflow'] = config_dict

                self.file_ops.ensure_directory(self.project_config_path.parent)
                success = self.file_ops.write_json_file(self.project_config_path, existing_config)

                if success:
                    self._workflow_config = config  # Update cache

                return success

            else:
                self.logger.error(f"Invalid config scope: {scope}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to save workflow config: {e}")
            return False

    def get_pipeline_config(self, pipeline_name: str) -> Optional[PipelineConfig]:
        """
        Get configuration for specific pipeline

        Args:
            pipeline_name: Name of the pipeline

        Returns:
            PipelineConfig object or None if not found
        """
        if pipeline_name in self._pipeline_configs:
            return self._pipeline_configs[pipeline_name]

        # Load from project config
        project_config = self.file_ops.read_json_file(self.project_config_path)
        if not project_config:
            return None

        pipelines_config = project_config.get('pipelines', {})
        pipeline_data = pipelines_config.get(pipeline_name)

        if not pipeline_data:
            return None

        # Create PipelineConfig object
        pipeline_config = PipelineConfig(name=pipeline_name, **pipeline_data)
        self._pipeline_configs[pipeline_name] = pipeline_config

        return pipeline_config

    def save_pipeline_config(self, pipeline_config: PipelineConfig) -> bool:
        """
        Save pipeline configuration

        Args:
            pipeline_config: PipelineConfig to save

        Returns:
            True if successful, False otherwise
        """
        try:
            # Load existing project config
            existing_config = self.file_ops.read_json_file(self.project_config_path) or {}

            # Ensure pipelines section exists
            if 'pipelines' not in existing_config:
                existing_config['pipelines'] = {}

            # Save pipeline config
            pipeline_dict = asdict(pipeline_config)
            existing_config['pipelines'][pipeline_config.name] = pipeline_dict

            # Write back to file
            self.file_ops.ensure_directory(self.project_config_path.parent)
            success = self.file_ops.write_json_file(self.project_config_path, existing_config)

            if success:
                self._pipeline_configs[pipeline_config.name] = pipeline_config  # Update cache

            return success

        except Exception as e:
            self.logger.error(f"Failed to save pipeline config for {pipeline_config.name}: {e}")
            return False

    def list_pipeline_configs(self) -> List[str]:
        """
        List all configured pipelines

        Returns:
            List of pipeline names
        """
        project_config = self.file_ops.read_json_file(self.project_config_path)
        if not project_config:
            return []

        return list(project_config.get('pipelines', {}).keys())

    def get_environment_variables(self, pipeline_name: str = None) -> Dict[str, str]:
        """
        Get environment variables for execution

        Args:
            pipeline_name: Optional pipeline name for pipeline-specific vars

        Returns:
            Dictionary of environment variables
        """
        env_vars = {}

        # Start with workflow config
        workflow_config = self.get_workflow_config()
        env_vars.update({
            'ADW_WORKSPACE_DIR': workflow_config.workspace_dir,
            'ADW_AGENTS_DIR': str(Path(workflow_config.workspace_dir) / workflow_config.agents_dir),
            'ADW_PIPELINES_DIR': str(Path(workflow_config.workspace_dir) / workflow_config.pipelines_dir),
            'ADW_LOGS_DIR': str(Path(workflow_config.workspace_dir) / workflow_config.logs_dir),
            'ADW_LOG_LEVEL': workflow_config.log_level,
        })

        # Add pipeline-specific vars
        if pipeline_name:
            pipeline_config = self.get_pipeline_config(pipeline_name)
            if pipeline_config and pipeline_config.env_vars:
                env_vars.update(pipeline_config.env_vars)

        # Add current environment (with ADW_ prefix priority)
        current_env = dict(os.environ)
        for key, value in current_env.items():
            if key.startswith('ADW_') and key not in env_vars:
                env_vars[key] = value

        return env_vars

    def validate_config(self) -> List[str]:
        """
        Validate current configuration

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        try:
            config = self.get_workflow_config()

            # Validate workspace directory
            workspace_path = Path(config.workspace_dir)
            if not workspace_path.exists():
                errors.append(f"Workspace directory does not exist: {workspace_path}")

            # Validate required directories
            required_dirs = [
                workspace_path / config.agents_dir,
                workspace_path / config.pipelines_dir,
            ]

            for dir_path in required_dirs:
                if not dir_path.exists():
                    errors.append(f"Required directory does not exist: {dir_path}")

            # Validate numeric values
            if config.execution_timeout <= 0:
                errors.append("execution_timeout must be positive")

            if config.polling_interval <= 0:
                errors.append("polling_interval must be positive")

            if config.max_retries < 0:
                errors.append("max_retries must be non-negative")

            # Validate log level
            valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            if config.log_level.upper() not in valid_log_levels:
                errors.append(f"Invalid log_level: {config.log_level}")

            # Validate pipeline configs
            for pipeline_name in self.list_pipeline_configs():
                pipeline_config = self.get_pipeline_config(pipeline_name)
                if pipeline_config:
                    if pipeline_config.timeout <= 0:
                        errors.append(f"Pipeline {pipeline_name}: timeout must be positive")

                    if pipeline_config.retry_count < 0:
                        errors.append(f"Pipeline {pipeline_name}: retry_count must be non-negative")

        except Exception as e:
            errors.append(f"Configuration validation failed: {e}")

        return errors

    def create_default_config(self, overwrite: bool = False) -> bool:
        """
        Create default configuration file

        Args:
            overwrite: Overwrite existing config

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.project_config_path.exists() and not overwrite:
                self.logger.info("Project config already exists, use overwrite=True to replace")
                return False

            # Create default configuration
            default_config = {
                "workflow": asdict(WorkflowConfig()),
                "pipelines": {
                    "plan": {
                        "description": "Planning stage for feature development",
                        "timeout": 300,
                        "retry_count": 1,
                        "dependencies": [],
                        "env_vars": {},
                        "arguments": []
                    },
                    "implement": {
                        "description": "Implementation stage for feature development",
                        "timeout": 600,
                        "retry_count": 1,
                        "dependencies": ["plan"],
                        "env_vars": {},
                        "arguments": []
                    },
                    "test": {
                        "description": "Testing stage for feature validation",
                        "timeout": 300,
                        "retry_count": 2,
                        "dependencies": ["implement"],
                        "env_vars": {},
                        "arguments": []
                    },
                    "review": {
                        "description": "Review stage for quality assurance",
                        "timeout": 180,
                        "retry_count": 1,
                        "dependencies": ["test"],
                        "env_vars": {},
                        "arguments": []
                    }
                }
            }

            # Write configuration
            self.file_ops.ensure_directory(self.project_config_path.parent)
            success = self.file_ops.write_json_file(self.project_config_path, default_config)

            if success:
                self.logger.info(f"Created default config at {self.project_config_path}")
                self._workflow_config = None  # Clear cache

            return success

        except Exception as e:
            self.logger.error(f"Failed to create default config: {e}")
            return False
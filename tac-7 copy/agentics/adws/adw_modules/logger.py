"""
Logger module for ADW workflows
Provides centralized logging with structured output for task tracking
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


def setup_logger(
    name: str = "adw",
    log_level: str = "INFO",
    log_dir: Optional[Path] = None,
    console_output: bool = True
) -> logging.Logger:
    """
    Setup structured logger for ADW workflows

    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files (optional)
        console_output: Whether to output to console

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Clear existing handlers to avoid duplicate logging
    logger.handlers.clear()

    # Set log level
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)

    # Create formatter with structured output
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_dir:
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "adw") -> logging.Logger:
    """
    Get existing logger or create default one

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)

    # If logger has no handlers, set up default
    if not logger.handlers:
        return setup_logger(name)

    return logger


class WorkflowLogger:
    """
    Enhanced logger for workflow-specific logging with structured output
    """

    def __init__(self, adw_id: str, stage: str = "", log_dir: Optional[Path] = None):
        self.adw_id = adw_id
        self.stage = stage
        self.logger = setup_logger(f"adw.{adw_id}", log_dir=log_dir)

    def _format_message(self, message: str) -> str:
        """Format message with workflow context"""
        context_parts = [f"ADW:{self.adw_id}"]
        if self.stage:
            context_parts.append(f"Stage:{self.stage}")

        context = " | ".join(context_parts)
        return f"[{context}] {message}"

    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(self._format_message(message))

    def info(self, message: str):
        """Log info message"""
        self.logger.info(self._format_message(message))

    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(self._format_message(message))

    def error(self, message: str):
        """Log error message"""
        self.logger.error(self._format_message(message))

    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(self._format_message(message))

    def set_stage(self, stage: str):
        """Update current stage for logging context"""
        self.stage = stage

    def log_stage_start(self, stage: str):
        """Log stage start with standardized format"""
        self.set_stage(stage)
        self.info(f"Starting {stage} stage")

    def log_stage_complete(self, stage: str):
        """Log stage completion with standardized format"""
        self.info(f"Completed {stage} stage successfully")

    def log_stage_error(self, stage: str, error: str):
        """Log stage error with standardized format"""
        self.error(f"Stage {stage} failed: {error}")
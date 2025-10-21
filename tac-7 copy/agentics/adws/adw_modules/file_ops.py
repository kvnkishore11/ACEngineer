"""
File Operations module for ADW workflows
Handles file system operations with safety checks and error handling
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from logger import get_logger


class FileOperations:
    """
    Safe file operations for ADW workflows
    Provides atomic operations and rollback capabilities
    """

    def __init__(self, workspace_dir: Path = None):
        self.workspace_dir = Path(workspace_dir) if workspace_dir else Path.cwd()
        self.logger = get_logger("file_ops")

    def ensure_directory(self, dir_path: Union[str, Path]) -> Path:
        """
        Ensure directory exists, create if necessary

        Args:
            dir_path: Directory path

        Returns:
            Path object for the directory

        Raises:
            OSError: If directory cannot be created
        """
        dir_path = Path(dir_path)

        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            return dir_path
        except Exception as e:
            self.logger.error(f"Failed to create directory {dir_path}: {e}")
            raise

    def read_json_file(self, file_path: Union[str, Path]) -> Optional[Dict]:
        """
        Safely read JSON file

        Args:
            file_path: Path to JSON file

        Returns:
            Dictionary from JSON or None if failed
        """
        file_path = Path(file_path)

        try:
            if not file_path.exists():
                self.logger.warning(f"JSON file not found: {file_path}")
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)

        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in {file_path}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to read {file_path}: {e}")
            return None

    def write_json_file(self, file_path: Union[str, Path], data: Dict,
                       backup: bool = True, atomic: bool = True) -> bool:
        """
        Safely write JSON file with optional backup and atomic write

        Args:
            file_path: Path to JSON file
            data: Data to write
            backup: Create backup if file exists
            atomic: Use atomic write (temp file + rename)

        Returns:
            True if successful, False otherwise
        """
        file_path = Path(file_path)

        try:
            # Ensure parent directory exists
            self.ensure_directory(file_path.parent)

            # Create backup if requested and file exists
            if backup and file_path.exists():
                backup_path = file_path.with_suffix(f'.backup.{int(datetime.now().timestamp())}')
                shutil.copy2(file_path, backup_path)
                self.logger.debug(f"Created backup: {backup_path}")

            if atomic:
                # Atomic write using temporary file
                temp_path = file_path.with_suffix('.tmp')
                try:
                    with open(temp_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)

                    # Atomic rename
                    temp_path.replace(file_path)
                    self.logger.debug(f"Atomically wrote: {file_path}")

                except Exception as e:
                    # Cleanup temp file on failure
                    if temp_path.exists():
                        temp_path.unlink()
                    raise e
            else:
                # Direct write
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            self.logger.error(f"Failed to write {file_path}: {e}")
            return False

    def read_text_file(self, file_path: Union[str, Path]) -> Optional[str]:
        """
        Safely read text file

        Args:
            file_path: Path to text file

        Returns:
            File content as string or None if failed
        """
        file_path = Path(file_path)

        try:
            if not file_path.exists():
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()

        except Exception as e:
            self.logger.error(f"Failed to read {file_path}: {e}")
            return None

    def write_text_file(self, file_path: Union[str, Path], content: str,
                       backup: bool = False, atomic: bool = True) -> bool:
        """
        Safely write text file

        Args:
            file_path: Path to text file
            content: Content to write
            backup: Create backup if file exists
            atomic: Use atomic write

        Returns:
            True if successful, False otherwise
        """
        file_path = Path(file_path)

        try:
            # Ensure parent directory exists
            self.ensure_directory(file_path.parent)

            # Create backup if requested and file exists
            if backup and file_path.exists():
                backup_path = file_path.with_suffix(f'.backup.{int(datetime.now().timestamp())}')
                shutil.copy2(file_path, backup_path)

            if atomic:
                # Atomic write
                temp_path = file_path.with_suffix('.tmp')
                try:
                    with open(temp_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    temp_path.replace(file_path)
                except Exception as e:
                    if temp_path.exists():
                        temp_path.unlink()
                    raise e
            else:
                # Direct write
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

            return True

        except Exception as e:
            self.logger.error(f"Failed to write {file_path}: {e}")
            return False

    def copy_file(self, src: Union[str, Path], dst: Union[str, Path],
                 backup_dst: bool = True) -> bool:
        """
        Safely copy file with optional destination backup

        Args:
            src: Source file path
            dst: Destination file path
            backup_dst: Create backup of destination if it exists

        Returns:
            True if successful, False otherwise
        """
        src_path = Path(src)
        dst_path = Path(dst)

        try:
            if not src_path.exists():
                self.logger.error(f"Source file not found: {src_path}")
                return False

            # Ensure destination directory exists
            self.ensure_directory(dst_path.parent)

            # Create backup of destination if requested
            if backup_dst and dst_path.exists():
                backup_path = dst_path.with_suffix(f'.backup.{int(datetime.now().timestamp())}')
                shutil.copy2(dst_path, backup_path)

            # Copy file
            shutil.copy2(src_path, dst_path)
            return True

        except Exception as e:
            self.logger.error(f"Failed to copy {src_path} to {dst_path}: {e}")
            return False

    def move_file(self, src: Union[str, Path], dst: Union[str, Path]) -> bool:
        """
        Safely move file

        Args:
            src: Source file path
            dst: Destination file path

        Returns:
            True if successful, False otherwise
        """
        src_path = Path(src)
        dst_path = Path(dst)

        try:
            if not src_path.exists():
                self.logger.error(f"Source file not found: {src_path}")
                return False

            # Ensure destination directory exists
            self.ensure_directory(dst_path.parent)

            # Move file
            shutil.move(str(src_path), str(dst_path))
            return True

        except Exception as e:
            self.logger.error(f"Failed to move {src_path} to {dst_path}: {e}")
            return False

    def delete_file(self, file_path: Union[str, Path], backup: bool = True) -> bool:
        """
        Safely delete file with optional backup

        Args:
            file_path: Path to file to delete
            backup: Create backup before deletion

        Returns:
            True if successful, False otherwise
        """
        file_path = Path(file_path)

        try:
            if not file_path.exists():
                return True  # Already deleted

            # Create backup if requested
            if backup:
                backup_path = file_path.with_suffix(f'.deleted.{int(datetime.now().timestamp())}')
                shutil.copy2(file_path, backup_path)
                self.logger.debug(f"Created deletion backup: {backup_path}")

            # Delete file
            file_path.unlink()
            return True

        except Exception as e:
            self.logger.error(f"Failed to delete {file_path}: {e}")
            return False

    def list_files(self, directory: Union[str, Path], pattern: str = "*",
                  recursive: bool = False) -> List[Path]:
        """
        List files in directory with optional pattern matching

        Args:
            directory: Directory to search
            pattern: Glob pattern for matching files
            recursive: Search recursively

        Returns:
            List of matching file paths
        """
        dir_path = Path(directory)

        try:
            if not dir_path.exists() or not dir_path.is_dir():
                return []

            if recursive:
                return list(dir_path.rglob(pattern))
            else:
                return list(dir_path.glob(pattern))

        except Exception as e:
            self.logger.error(f"Failed to list files in {dir_path}: {e}")
            return []

    def get_file_size(self, file_path: Union[str, Path]) -> Optional[int]:
        """
        Get file size in bytes

        Args:
            file_path: Path to file

        Returns:
            File size in bytes or None if error
        """
        file_path = Path(file_path)

        try:
            if file_path.exists() and file_path.is_file():
                return file_path.stat().st_size
            return None

        except Exception as e:
            self.logger.error(f"Failed to get size of {file_path}: {e}")
            return None

    def get_file_modification_time(self, file_path: Union[str, Path]) -> Optional[datetime]:
        """
        Get file modification time

        Args:
            file_path: Path to file

        Returns:
            Modification time as datetime or None if error
        """
        file_path = Path(file_path)

        try:
            if file_path.exists():
                timestamp = file_path.stat().st_mtime
                return datetime.fromtimestamp(timestamp)
            return None

        except Exception as e:
            self.logger.error(f"Failed to get modification time of {file_path}: {e}")
            return None

    def create_archive(self, source_dir: Union[str, Path], archive_path: Union[str, Path],
                      format: str = "zip") -> bool:
        """
        Create archive of directory

        Args:
            source_dir: Directory to archive
            archive_path: Path for archive file (without extension)
            format: Archive format (zip, tar, gztar, bztar, xztar)

        Returns:
            True if successful, False otherwise
        """
        source_path = Path(source_dir)
        archive_path = Path(archive_path)

        try:
            if not source_path.exists() or not source_path.is_dir():
                self.logger.error(f"Source directory not found: {source_path}")
                return False

            # Ensure archive directory exists
            self.ensure_directory(archive_path.parent)

            # Create archive
            shutil.make_archive(str(archive_path), format, str(source_path))
            self.logger.info(f"Created archive: {archive_path}.{format}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create archive: {e}")
            return False

    def cleanup_temp_files(self, directory: Union[str, Path], max_age_hours: int = 24) -> int:
        """
        Clean up temporary files older than specified age

        Args:
            directory: Directory to clean
            max_age_hours: Maximum age in hours

        Returns:
            Number of files cleaned up
        """
        dir_path = Path(directory)
        cleanup_count = 0

        try:
            cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)

            # Patterns for temporary files
            temp_patterns = ["*.tmp", "*.temp", "*.backup.*", "*.deleted.*"]

            for pattern in temp_patterns:
                for temp_file in dir_path.rglob(pattern):
                    try:
                        if temp_file.stat().st_mtime < cutoff_time:
                            temp_file.unlink()
                            cleanup_count += 1
                            self.logger.debug(f"Cleaned up temp file: {temp_file}")
                    except Exception as e:
                        self.logger.warning(f"Failed to clean {temp_file}: {e}")

            if cleanup_count > 0:
                self.logger.info(f"Cleaned up {cleanup_count} temporary files")

            return cleanup_count

        except Exception as e:
            self.logger.error(f"Failed to cleanup temp files in {dir_path}: {e}")
            return 0
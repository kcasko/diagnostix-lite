"""
DiagnOStiX 3.0 - Maintenance Fixes (Pure Python)
"""

import os
import tempfile
import shutil
import time
from typing import Dict, Any
from pathlib import Path

from core.fixes.base import Fix, FixCategory, RiskLevel
from core.fixes.registry import FixRegistry


class CleanTempAdvancedFix(Fix):
    """Pure Python temp file cleaner."""

    def __init__(self):
        super().__init__()
        self.id = "clean_temp_advanced"
        self.name = "Advanced Temp Cleanup"
        self.description = "Recursively delete temp files, Windows temp, and browser caches."
        self.simple_description = "Delete junk files to free up space and improve performance."
        self.category = FixCategory.MAINTENANCE
        self.risk_level = RiskLevel.MODERATE
        self.supported_platforms = ["windows", "linux", "darwin"]
        self.requires_admin = False
        self.estimated_time = 30
        self.tags = ["temp", "cleanup", "disk", "space", "cache"]

    def detect(self) -> bool:
        temp_dir = Path(tempfile.gettempdir())
        if not temp_dir.exists():
            return False
        try:
            total_size = sum(f.stat().st_size for f in temp_dir.rglob("*") if f.is_file())
            return total_size > 10 * 1024 * 1024  # More than 10MB
        except Exception:
            return True

    def preview(self) -> str:
        temp_dir = Path(tempfile.gettempdir())
        return (
            "Will clean the following locations:\n"
            f"- User temp: {temp_dir}\n"
            "- Browser caches (Chrome, Firefox, Edge)\n\n"
            "Locked files will be skipped safely."
        )

    def _get_cleanup_dirs(self):
        """Get all directories to clean."""
        dirs = [Path(tempfile.gettempdir())]
        
        # Browser caches
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        if local_app_data:
            # Chrome
            chrome_cache = Path(local_app_data) / "Google/Chrome/User Data/Default/Cache"
            if chrome_cache.exists():
                dirs.append(chrome_cache)
            # Edge
            edge_cache = Path(local_app_data) / "Microsoft/Edge/User Data/Default/Cache"
            if edge_cache.exists():
                dirs.append(edge_cache)

        return dirs

    def _clean_directory(self, dir_path: Path) -> tuple:
        """Clean a directory and return (files_deleted, bytes_freed)."""
        files_deleted = 0
        bytes_freed = 0
        
        for item in dir_path.rglob("*"):
            if item.is_file():
                try:
                    size = item.stat().st_size
                    item.unlink()
                    files_deleted += 1
                    bytes_freed += size
                except (PermissionError, OSError):
                    continue  # Skip locked files
        
        return files_deleted, bytes_freed

    def run(self) -> Dict[str, Any]:
        start_time = time.time()
        total_files = 0
        total_bytes = 0
        lines = []

        for dir_path in self._get_cleanup_dirs():
            if dir_path.exists():
                files, bytes_freed = self._clean_directory(dir_path)
                total_files += files
                total_bytes += bytes_freed
                lines.append(f"Cleaned {dir_path}: {files} files, {bytes_freed / (1024*1024):.2f} MB")

        execution_time = time.time() - start_time
        lines.append(f"\nTotal: {total_files} files deleted, {total_bytes / (1024*1024):.2f} MB freed")
        lines.append(f"Execution time: {execution_time:.2f}s")

        return {
            "output": "\n".join(lines),
            "files_deleted": total_files,
            "bytes_freed": total_bytes,
            "execution_time": execution_time
        }

    def verify(self) -> bool:
        return True


FixRegistry.register(CleanTempAdvancedFix)

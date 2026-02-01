"""
DiagnOStiX 3.0 - Maintenance Fixes
"""

import asyncio
import os
import tempfile
from typing import Dict, Any
from pathlib import Path

from core.fixes.base import Fix, FixCategory, RiskLevel
from core.fixes.registry import FixRegistry
from core.script_runner import script_runner


class CleanTempAdvancedFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "clean_temp_advanced"
        self.name = "Advanced Temp Cleanup"
        self.description = "Recursively delete temp files, Windows temp, and Windows Update cache."
        self.simple_description = "Delete junk files to free up space and improve performance."
        self.category = FixCategory.MAINTENANCE
        self.risk_level = RiskLevel.MODERATE
        self.supported_platforms = ["windows"]
        self.requires_admin = False
        self.estimated_time = 30
        self.tags = ["temp", "cleanup", "disk", "space", "cache"]

    def detect(self) -> bool:
        temp_dir = Path(tempfile.gettempdir())
        if not temp_dir.exists():
            return False
        total_size = sum(f.stat().st_size for f in temp_dir.rglob("*") if f.is_file())
        return total_size > 10 * 1024 * 1024  # More than 10MB

    def preview(self) -> str:
        temp_dir = Path(tempfile.gettempdir())
        win_temp = Path("C:/Windows/Temp")
        update_cache = Path("C:/Windows/SoftwareDistribution/Download")
        
        return (
            "Will clean the following locations:
"
            f"- User temp: {temp_dir}
"
            f"- Windows temp: {win_temp}
"
            f"- Windows Update cache: {update_cache}

"
            "Locked files will be skipped safely."
        )

    def run(self) -> Dict[str, Any]:
        result = asyncio.get_event_loop().run_until_complete(
            script_runner.run_batch("01-Quick-Scripts/clean_temp.bat")
        )
        return {"output": result.stdout, "execution_time": result.execution_time}

    def verify(self) -> bool:
        return True


FixRegistry.register(CleanTempAdvancedFix)

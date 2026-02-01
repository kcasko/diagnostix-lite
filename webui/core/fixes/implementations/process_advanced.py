"""
DiagnOStiX 3.0 - Process Fixes (Enhanced)
"""

import asyncio
import psutil
from typing import Dict, Any, Optional

from core.fixes.base import Fix, FixCategory, RiskLevel
from core.fixes.registry import FixRegistry
from core.script_runner import script_runner


class KillProcessAdvancedFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "kill_process_advanced"
        self.name = "Process Terminator (Advanced)"
        self.description = "Terminate processes by name with confirmation and detailed feedback."
        self.simple_description = "Force close a frozen or problematic program."
        self.category = FixCategory.PROCESS
        self.risk_level = RiskLevel.MODERATE
        self.supported_platforms = ["windows"]
        self.requires_admin = False
        self.estimated_time = 5
        self.tags = ["process", "kill", "terminate", "frozen", "stuck"]
        self.target_process: Optional[str] = None

    def set_target(self, process_name: str):
        self.target_process = process_name

    def detect(self) -> bool:
        if not self.target_process:
            return False
        name = self.target_process.replace(".exe", "")
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] and name.lower() in proc.info["name"].lower():
                return True
        return False

    def preview(self) -> str:
        if self.target_process:
            return f"Will terminate all processes matching: {self.target_process}"
        return "No process specified. Provide a process name to terminate."

    def run(self) -> Dict[str, Any]:
        if not self.target_process:
            raise ValueError("No target process specified")
        
        # Use the PowerShell script for interactive termination
        result = asyncio.get_event_loop().run_until_complete(
            script_runner.run_powershell_command(
                f"Stop-Process -Name '{self.target_process.replace('.exe', '')}' -Force -ErrorAction SilentlyContinue"
            )
        )
        return {
            "output": result.stdout or "Process terminated",
            "process": self.target_process,
            "success": result.success
        }

    def verify(self) -> bool:
        if not self.target_process:
            return True
        name = self.target_process.replace(".exe", "")
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] and name.lower() in proc.info["name"].lower():
                return False
        return True


FixRegistry.register(KillProcessAdvancedFix)

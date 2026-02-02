"""
DiagnOStiX 3.0 - Hardware Fixes
"""

from typing import Dict, Any

from core.fixes.base import Fix, FixCategory, RiskLevel
from core.fixes.registry import FixRegistry
from core.script_runner import script_runner


class RAMTestFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "ram_test"
        self.name = "Memory Diagnostic"
        self.description = "Launch Windows Memory Diagnostic to test RAM for hardware errors."
        self.simple_description = "Test your computer memory for problems that cause crashes."
        self.category = FixCategory.HARDWARE
        self.risk_level = RiskLevel.MODERATE
        self.supported_platforms = ["windows"]
        self.requires_admin = True
        self.requires_reboot = True
        self.estimated_time = 600  # Can take 10+ minutes
        self.tags = ["ram", "memory", "hardware", "test", "diagnostic"]

    def detect(self) -> bool:
        return True

    def preview(self) -> str:
        return (
            "Will launch Windows Memory Diagnostic (mdsched.exe).\n\n"
            "IMPORTANT: This will schedule a memory test and restart your computer!\n"
            "The test runs before Windows loads and can take 10-30 minutes.\n\n"
            "Results will be available in Event Viewer after the test completes."
        )

    def run(self) -> Dict[str, Any]:
        result = script_runner.run_batch_sync("05-Utilities/TaurusTech-RAMTest.bat")
        return {
            "output": result.stdout or "Memory diagnostic scheduled. Restart to begin test.",
            "requires_reboot": True
        }

    def verify(self) -> bool:
        return True


FixRegistry.register(RAMTestFix)

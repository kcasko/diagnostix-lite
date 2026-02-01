"""
DiagnOStiX 3.0 - Diagnostic Fixes
"""

import asyncio
import os
from typing import Dict, Any
from pathlib import Path

from core.fixes.base import Fix, FixCategory, RiskLevel
from core.fixes.registry import FixRegistry
from core.script_runner import script_runner


class SystemSnapshotFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "system_snapshot"
        self.name = "System Information Snapshot"
        self.description = "Collects comprehensive system information including hardware, OS, and configuration details."
        self.simple_description = "Creates a full report of your computer specs and health."
        self.category = FixCategory.DIAGNOSTICS
        self.risk_level = RiskLevel.SAFE
        self.supported_platforms = ["windows"]
        self.requires_admin = False
        self.estimated_time = 30
        self.tags = ["system", "info", "snapshot", "hardware", "report"]

    def detect(self) -> bool:
        return True

    def preview(self) -> str:
        return "Will collect comprehensive system information and save to Desktop/TaurusTech-Logs/"

    def run(self) -> Dict[str, Any]:
        result = asyncio.get_event_loop().run_until_complete(
            script_runner.run_batch("01-Quick-Scripts/system_info_snapshot.bat")
        )
        if not result.success and not result.stdout:
            raise Exception(result.error_message or "Script execution failed")
        return {"output": result.stdout, "execution_time": result.execution_time}

    def verify(self) -> bool:
        return True


class NetworkAdapterDiagnosticsFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "network_adapter_diagnostics"
        self.name = "Network Adapter Diagnostics"
        self.description = "Analyzes all network adapters with detailed status, speed, and configuration information."
        self.simple_description = "Checks all your network connections and creates a report."
        self.category = FixCategory.DIAGNOSTICS
        self.risk_level = RiskLevel.SAFE
        self.supported_platforms = ["windows"]
        self.requires_admin = False
        self.estimated_time = 15
        self.tags = ["network", "adapter", "wifi", "ethernet"]

    def detect(self) -> bool:
        return True

    def preview(self) -> str:
        return "Will analyze network adapters and create detailed logs."

    def run(self) -> Dict[str, Any]:
        result = asyncio.get_event_loop().run_until_complete(
            script_runner.run_powershell("01-Quick-Scripts/network_adapter_dump.ps1")
        )
        if not result.success and not result.stdout:
            raise Exception(result.error_message or "Script execution failed")
        return {"output": result.stdout, "execution_time": result.execution_time}

    def verify(self) -> bool:
        return True


class StartupAnalysisFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "startup_analysis"
        self.name = "Startup Folder Analysis"
        self.description = "Opens startup folders for review of autostart applications."
        self.simple_description = "Shows programs that start automatically when you turn on your computer."
        self.category = FixCategory.DIAGNOSTICS
        self.risk_level = RiskLevel.SAFE
        self.supported_platforms = ["windows"]
        self.requires_admin = False
        self.estimated_time = 5
        self.tags = ["startup", "boot", "autostart"]

    def detect(self) -> bool:
        user_startup = Path(os.environ.get("APPDATA", "")) / "Microsoft/Windows/Start Menu/Programs/Startup"
        return user_startup.exists()

    def preview(self) -> str:
        return "Will open startup folders for review of autostart programs."

    def run(self) -> Dict[str, Any]:
        result = asyncio.get_event_loop().run_until_complete(
            script_runner.run_batch("01-Quick-Scripts/cleanup_startup.bat")
        )
        return {"output": result.stdout}

    def verify(self) -> bool:
        return True


FixRegistry.register(SystemSnapshotFix)
FixRegistry.register(NetworkAdapterDiagnosticsFix)
FixRegistry.register(StartupAnalysisFix)

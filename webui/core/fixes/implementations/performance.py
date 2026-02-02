"""
DiagnOStiX 3.0 - Performance Fixes
"""

from typing import Dict, Any

from core.fixes.base import Fix, FixCategory, RiskLevel
from core.fixes.registry import FixRegistry
from core.script_runner import script_runner


class DisableBloatServicesFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "disable_bloat_services"
        self.name = "Disable Bloat Services"
        self.description = "Disable low-value Windows services that consume resources (DiagTrack, MapsBroker, RetailDemo)."
        self.simple_description = "Turn off background services you do not need to speed up your PC."
        self.category = FixCategory.PERFORMANCE
        self.risk_level = RiskLevel.MODERATE
        self.supported_platforms = ["windows"]
        self.requires_admin = True
        self.estimated_time = 15
        self.tags = ["services", "bloat", "telemetry", "performance", "speed"]

    def detect(self) -> bool:
        return True

    def preview(self) -> str:
        return (
            "Will disable the following services:\n"
            "- DiagTrack (Diagnostic Tracking / Telemetry)\n"
            "- MapsBroker (Downloaded Maps Manager)\n"
            "- RetailDemo (Retail Demo Service)\n\n"
            "These services are safe to disable and will improve performance."
        )

    def run(self) -> Dict[str, Any]:
        result = script_runner.run_powershell_sync("01-Quick-Scripts/TaurusTech_Service_Disabler.ps1")
        if not result.success and "error" in result.stderr.lower():
            raise Exception(result.stderr)
        return {"output": result.stdout, "execution_time": result.execution_time}

    def verify(self) -> bool:
        return True


class PowerPerformanceFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "power_performance"
        self.name = "CPU Performance Mode"
        self.description = "Optimize CPU power profile for maximum performance (100% max, 5% min throttling)."
        self.simple_description = "Make your computer run at full speed instead of saving power."
        self.category = FixCategory.PERFORMANCE
        self.risk_level = RiskLevel.MODERATE
        self.supported_platforms = ["windows"]
        self.requires_admin = True
        self.requires_reboot = False
        self.estimated_time = 5
        self.tags = ["power", "cpu", "performance", "speed", "throttle"]

    def detect(self) -> bool:
        return True

    def preview(self) -> str:
        return (
            "Will configure power settings:\n"
            "- Set maximum CPU throttle to 100%\n"
            "- Set minimum CPU throttle to 5%\n"
            "- Activate current power scheme\n\n"
            "Note: This increases power consumption and heat. Best for desktops."
        )

    def run(self) -> Dict[str, Any]:
        result = script_runner.run_batch_sync("03-Config-Tweaks/PowerTweaks.bat")
        return {"output": result.stdout, "execution_time": result.execution_time}

    def verify(self) -> bool:
        return True


FixRegistry.register(DisableBloatServicesFix)
FixRegistry.register(PowerPerformanceFix)

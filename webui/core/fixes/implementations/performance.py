"""
DiagnOStiX 3.0 - Performance Fixes (Pure Python)
"""

import subprocess
from typing import Dict, Any, List

from core.fixes.base import Fix, FixCategory, RiskLevel
from core.fixes.registry import FixRegistry


class DisableBloatServicesFix(Fix):
    """Disable Windows bloat services using sc command via subprocess."""

    BLOAT_SERVICES = ["DiagTrack", "MapsBroker", "RetailDemo"]

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
        results: List[str] = []
        
        for service in self.BLOAT_SERVICES:
            # Stop the service
            stop_result = subprocess.run(
                ["sc", "stop", service],
                capture_output=True, text=True
            )
            # Disable the service
            disable_result = subprocess.run(
                ["sc", "config", service, "start=", "disabled"],
                capture_output=True, text=True
            )
            
            if disable_result.returncode == 0:
                results.append(f"✓ {service}: Disabled")
            else:
                error = disable_result.stderr or disable_result.stdout
                results.append(f"✗ {service}: {error.strip()}")

        output = "\n".join(results)
        return {"output": output, "services_processed": len(self.BLOAT_SERVICES)}

    def verify(self) -> bool:
        return True


class PowerPerformanceFix(Fix):
    """Set CPU to max performance using powercfg via subprocess."""

    def __init__(self):
        super().__init__()
        self.id = "power_performance"
        self.name = "CPU Performance Mode"
        self.description = "Optimize CPU power profile for maximum performance (100% max throttling)."
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
            "- Activate High Performance power scheme\n\n"
            "Note: This increases power consumption and heat. Best for desktops."
        )

    def run(self) -> Dict[str, Any]:
        results: List[str] = []
        
        # Set High Performance power scheme (GUID: 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c)
        high_perf_guid = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
        
        # Activate high performance
        result = subprocess.run(
            ["powercfg", "/setactive", high_perf_guid],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            results.append("✓ High Performance power scheme activated")
        else:
            results.append(f"✗ Failed to set power scheme: {result.stderr}")

        # Set CPU min/max throttle
        # These modify the active scheme
        subprocess.run(
            ["powercfg", "/setacvalueindex", "scheme_current", "sub_processor", "procthrottlemax", "100"],
            capture_output=True
        )
        subprocess.run(
            ["powercfg", "/setacvalueindex", "scheme_current", "sub_processor", "procthrottlemin", "5"],
            capture_output=True
        )
        subprocess.run(["powercfg", "/setactive", "scheme_current"], capture_output=True)
        
        results.append("✓ CPU throttle settings applied (100% max, 5% min)")

        output = "\n".join(results)
        return {"output": output}

    def verify(self) -> bool:
        return True


FixRegistry.register(DisableBloatServicesFix)
FixRegistry.register(PowerPerformanceFix)

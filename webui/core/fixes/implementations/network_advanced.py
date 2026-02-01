"""
DiagnOStiX 3.0 - Network Advanced Fixes
"""

import asyncio
from typing import Dict, Any

from core.fixes.base import Fix, FixCategory, RiskLevel
from core.fixes.registry import FixRegistry
from core.script_runner import script_runner


class NetworkFullResetFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "network_full_reset"
        self.name = "Full Network Stack Reset"
        self.description = "Deep network stack reset: DNS flush, Winsock reset, IP reset, Firewall reset, DHCP renew."
        self.simple_description = "Completely reset your network settings when nothing else works."
        self.category = FixCategory.NETWORK
        self.risk_level = RiskLevel.DANGEROUS
        self.supported_platforms = ["windows"]
        self.requires_admin = True
        self.requires_reboot = True
        self.estimated_time = 60
        self.tags = ["network", "reset", "dns", "winsock", "firewall", "dhcp"]

    def detect(self) -> bool:
        return True

    def preview(self) -> str:
        return (
            "WARNING: This is a comprehensive network reset!\n\n"
            "Will execute:\n"
            "- ipconfig /flushdns (clear DNS cache)\n"
            "- netsh winsock reset (reset TCP/IP stack)\n"
            "- netsh int ip reset (reset IP configuration)\n"
            "- netsh advfirewall reset (reset firewall to defaults)\n"
            "- ipconfig /release and /renew (refresh DHCP)\n\n"
            "CAUTION: Custom firewall rules will be lost!\n"
            "A reboot is recommended after this operation."
        )

    def run(self) -> Dict[str, Any]:
        result = asyncio.get_event_loop().run_until_complete(
            script_runner.run_powershell("01-Quick-Scripts/network_core_reset.ps1")
        )
        return {
            "output": result.stdout,
            "stderr": result.stderr,
            "requires_reboot": True
        }

    def verify(self) -> bool:
        return True


FixRegistry.register(NetworkFullResetFix)

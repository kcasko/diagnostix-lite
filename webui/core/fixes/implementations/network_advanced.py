"""
DiagnOStiX 3.0 - Network Advanced Fixes (Pure Python)
"""

import subprocess
from typing import Dict, Any, List

from core.fixes.base import Fix, FixCategory, RiskLevel
from core.fixes.registry import FixRegistry


class NetworkFullResetFix(Fix):
    """Full network reset using subprocess for ipconfig/netsh commands."""

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
        results: List[str] = []
        commands = [
            (["ipconfig", "/flushdns"], "Flush DNS"),
            (["netsh", "winsock", "reset"], "Winsock Reset"),
            (["netsh", "int", "ip", "reset"], "IP Reset"),
            (["netsh", "advfirewall", "reset"], "Firewall Reset"),
            (["ipconfig", "/release"], "DHCP Release"),
            (["ipconfig", "/renew"], "DHCP Renew"),
        ]

        for cmd, desc in commands:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    results.append(f"✓ {desc}: Success")
                else:
                    results.append(f"⚠ {desc}: {result.stderr.strip() or 'Warning'}")
            except subprocess.TimeoutExpired:
                results.append(f"⚠ {desc}: Timeout")
            except Exception as e:
                results.append(f"✗ {desc}: {e}")

        output = "\n".join(results)
        output += "\n\nNetwork reset complete. Please restart your computer."
        return {"output": output, "requires_reboot": True}

    def verify(self) -> bool:
        return True


FixRegistry.register(NetworkFullResetFix)

"""
DiagnOStiX 3.0 - Diagnostic Fixes (Pure Python)
"""

import os
import platform
import socket
import subprocess
import time
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

import psutil

from core.fixes.base import Fix, FixCategory, RiskLevel
from core.fixes.registry import FixRegistry


class SystemSnapshotFix(Fix):
    """Pure Python system information collector."""

    def __init__(self):
        super().__init__()
        self.id = "system_snapshot"
        self.name = "System Information Snapshot"
        self.description = "Collects comprehensive system information including hardware, OS, and configuration details."
        self.simple_description = "Creates a full report of your computer specs and health."
        self.category = FixCategory.DIAGNOSTICS
        self.risk_level = RiskLevel.SAFE
        self.supported_platforms = ["windows", "linux", "darwin"]
        self.requires_admin = False
        self.estimated_time = 10
        self.tags = ["system", "info", "snapshot", "hardware", "report"]

    def detect(self) -> bool:
        return True

    def preview(self) -> str:
        return "Will collect system info using Python (no external scripts required)."

    def _get_output_path(self) -> Path:
        desktop = Path(os.environ.get("USERPROFILE", os.path.expanduser("~"))) / "Desktop"
        return desktop / "TaurusTech-Logs" / "system_info_snapshot.txt"

    def _collect_system_info(self) -> str:
        lines = []
        lines.append("=" * 60)
        lines.append("DIAGNOSTIX SYSTEM SNAPSHOT")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 60)

        # OS Info
        lines.append("\n[OPERATING SYSTEM]")
        lines.append(f"  System: {platform.system()}")
        lines.append(f"  Release: {platform.release()}")
        lines.append(f"  Version: {platform.version()}")
        lines.append(f"  Machine: {platform.machine()}")
        lines.append(f"  Processor: {platform.processor()}")
        lines.append(f"  Hostname: {socket.gethostname()}")

        # CPU Info
        lines.append("\n[CPU]")
        lines.append(f"  Physical Cores: {psutil.cpu_count(logical=False)}")
        lines.append(f"  Logical Cores: {psutil.cpu_count(logical=True)}")
        lines.append(f"  Current Usage: {psutil.cpu_percent(interval=1)}%")
        try:
            freq = psutil.cpu_freq()
            if freq:
                lines.append(f"  Max Frequency: {freq.max:.0f} MHz")
                lines.append(f"  Current Frequency: {freq.current:.0f} MHz")
        except Exception:
            pass

        # Memory Info
        lines.append("\n[MEMORY]")
        mem = psutil.virtual_memory()
        lines.append(f"  Total: {mem.total / (1024**3):.2f} GB")
        lines.append(f"  Available: {mem.available / (1024**3):.2f} GB")
        lines.append(f"  Used: {mem.used / (1024**3):.2f} GB ({mem.percent}%)")

        # Disk Info
        lines.append("\n[DISKS]")
        for part in psutil.disk_partitions(all=False):
            try:
                usage = psutil.disk_usage(part.mountpoint)
                lines.append(f"  {part.device}")
                lines.append(f"    Mount: {part.mountpoint}")
                lines.append(f"    Type: {part.fstype}")
                lines.append(f"    Total: {usage.total / (1024**3):.2f} GB")
                lines.append(f"    Free: {usage.free / (1024**3):.2f} GB ({100 - usage.percent:.1f}%)")
            except PermissionError:
                lines.append(f"  {part.device} (access denied)")

        # Network Interfaces
        lines.append("\n[NETWORK INTERFACES]")
        for iface, addrs in psutil.net_if_addrs().items():
            lines.append(f"  {iface}:")
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    lines.append(f"    IPv4: {addr.address}")
                elif addr.family == socket.AF_INET6:
                    lines.append(f"    IPv6: {addr.address}")

        # Boot Time
        lines.append("\n[SYSTEM]")
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        lines.append(f"  Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
        uptime = datetime.now() - boot_time
        lines.append(f"  Uptime: {uptime.days}d {uptime.seconds // 3600}h {(uptime.seconds % 3600) // 60}m")

        lines.append("\n" + "=" * 60)
        return "\n".join(lines)

    def run(self) -> Dict[str, Any]:
        start_time = time.time()
        output = self._collect_system_info()
        execution_time = time.time() - start_time

        # Save to file
        output_path = self._get_output_path()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding='utf-8')

        return {
            "output": output,
            "execution_time": execution_time,
            "file_path": str(output_path),
            "file_exists": output_path.exists()
        }

    def verify(self) -> bool:
        return self._get_output_path().exists()


class NetworkAdapterDiagnosticsFix(Fix):
    """Pure Python network adapter diagnostics."""

    def __init__(self):
        super().__init__()
        self.id = "network_adapter_diagnostics"
        self.name = "Network Adapter Diagnostics"
        self.description = "Analyzes all network adapters with detailed status, speed, and configuration information."
        self.simple_description = "Checks all your network connections and creates a report."
        self.category = FixCategory.DIAGNOSTICS
        self.risk_level = RiskLevel.SAFE
        self.supported_platforms = ["windows", "linux", "darwin"]
        self.requires_admin = False
        self.estimated_time = 5
        self.tags = ["network", "adapter", "wifi", "ethernet"]

    def detect(self) -> bool:
        return True

    def preview(self) -> str:
        return "Will analyze network adapters using Python (cross-platform)."

    def _get_output_path(self) -> Path:
        desktop = Path(os.environ.get("USERPROFILE", os.path.expanduser("~"))) / "Desktop"
        return desktop / "TaurusTech-Logs" / "network_adapter_dump.txt"

    def run(self) -> Dict[str, Any]:
        start_time = time.time()
        lines = []
        lines.append("=" * 60)
        lines.append("NETWORK ADAPTER DIAGNOSTICS")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 60)

        # Get interface stats
        net_io = psutil.net_io_counters(pernic=True)
        net_if_stats = psutil.net_if_stats()
        net_if_addrs = psutil.net_if_addrs()

        for iface in net_if_addrs:
            lines.append(f"\n[{iface}]")

            # Status
            if iface in net_if_stats:
                stats = net_if_stats[iface]
                status = "UP" if stats.isup else "DOWN"
                lines.append(f"  Status: {status}")
                lines.append(f"  Speed: {stats.speed} Mbps" if stats.speed else "  Speed: Unknown")
                lines.append(f"  MTU: {stats.mtu}")

            # Addresses
            for addr in net_if_addrs[iface]:
                if addr.family == socket.AF_INET:
                    lines.append(f"  IPv4: {addr.address}")
                    lines.append(f"    Netmask: {addr.netmask}")
                elif addr.family == socket.AF_INET6:
                    lines.append(f"  IPv6: {addr.address}")

            # IO Stats
            if iface in net_io:
                io = net_io[iface]
                lines.append(f"  Bytes Sent: {io.bytes_sent / (1024**2):.2f} MB")
                lines.append(f"  Bytes Recv: {io.bytes_recv / (1024**2):.2f} MB")
                lines.append(f"  Packets Sent: {io.packets_sent}")
                lines.append(f"  Packets Recv: {io.packets_recv}")
                if io.errin or io.errout:
                    lines.append(f"  Errors: In={io.errin}, Out={io.errout}")

        output = "\n".join(lines)
        execution_time = time.time() - start_time

        # Save to file
        output_path = self._get_output_path()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding='utf-8')

        return {"output": output, "execution_time": execution_time, "file_path": str(output_path)}

    def verify(self) -> bool:
        return True


class StartupAnalysisFix(Fix):
    """Pure Python startup folder analysis."""

    def __init__(self):
        super().__init__()
        self.id = "startup_analysis"
        self.name = "Startup Folder Analysis"
        self.description = "Lists and optionally opens startup folders for review of autostart applications."
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
        return "Will list startup items and open startup folders for review."

    def _get_startup_paths(self) -> List[Path]:
        paths = []
        # User startup
        user_startup = Path(os.environ.get("APPDATA", "")) / "Microsoft/Windows/Start Menu/Programs/Startup"
        if user_startup.exists():
            paths.append(user_startup)
        # All users startup
        all_users = Path(os.environ.get("PROGRAMDATA", "C:/ProgramData")) / "Microsoft/Windows/Start Menu/Programs/Startup"
        if all_users.exists():
            paths.append(all_users)
        return paths

    def run(self) -> Dict[str, Any]:
        lines = []
        lines.append("=" * 60)
        lines.append("STARTUP FOLDER ANALYSIS")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 60)

        startup_paths = self._get_startup_paths()
        total_items = 0

        for path in startup_paths:
            lines.append(f"\n[{path}]")
            items = list(path.iterdir())
            if not items:
                lines.append("  (empty)")
            else:
                for item in items:
                    total_items += 1
                    item_type = "FOLDER" if item.is_dir() else "FILE"
                    lines.append(f"  [{item_type}] {item.name}")

            # Open the folder in explorer
            try:
                os.startfile(str(path))
            except Exception:
                pass  # May fail if not on Windows

        output = "\n".join(lines)
        return {"output": output, "startup_items": total_items, "folders_opened": len(startup_paths)}

    def verify(self) -> bool:
        return True


FixRegistry.register(SystemSnapshotFix)
FixRegistry.register(NetworkAdapterDiagnosticsFix)
FixRegistry.register(StartupAnalysisFix)

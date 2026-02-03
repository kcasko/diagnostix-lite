"""
DiagnOStiX 3.0 - Security Fixes (Pure Python)
"""

import hashlib
import socket
import time
from typing import Dict, Any, Optional, List
from pathlib import Path

from core.fixes.base import Fix, FixCategory, RiskLevel
from core.fixes.registry import FixRegistry


class FileHashFix(Fix):
    """Pure Python file hash calculator using hashlib."""

    def __init__(self):
        super().__init__()
        self.id = "file_hash"
        self.name = "File Hash Validator"
        self.description = "Generate SHA256 hash of files for integrity verification."
        self.simple_description = "Check if a file has been tampered with by calculating its unique fingerprint."
        self.category = FixCategory.SECURITY
        self.risk_level = RiskLevel.SAFE
        self.supported_platforms = ["windows", "linux", "darwin"]
        self.requires_admin = False
        self.estimated_time = 5
        self.tags = ["hash", "sha256", "integrity", "verify", "security"]
        self.target_file: Optional[str] = None
        self.required_params = [
            {"name": "file_path", "label": "File Path", "type": "text", "placeholder": "e.g. C:\\path\\to\\file.exe", "required": True}
        ]

    def set_target(self, file_path: str):
        self.target_file = file_path

    def detect(self) -> bool:
        return self.target_file is not None and Path(self.target_file).exists()

    def preview(self) -> str:
        if self.target_file:
            return f"Will calculate SHA256 hash for: {self.target_file}"
        return "No file selected. Provide a file path to hash."

    def run(self) -> Dict[str, Any]:
        if not self.target_file:
            raise ValueError("No target file specified")

        file_path = Path(self.target_file)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {self.target_file}")

        # Calculate SHA256
        sha256 = hashlib.sha256()
        md5 = hashlib.md5()
        file_size = file_path.stat().st_size

        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
                md5.update(chunk)

        output = (
            f"File: {file_path.name}\n"
            f"Path: {self.target_file}\n"
            f"Size: {file_size:,} bytes\n"
            f"\nSHA256: {sha256.hexdigest()}\n"
            f"MD5:    {md5.hexdigest()}"
        )

        return {"output": output, "file": self.target_file, "sha256": sha256.hexdigest(), "md5": md5.hexdigest()}

    def verify(self) -> bool:
        return True


class PortScanFix(Fix):
    """Pure Python port scanner using socket."""

    def __init__(self):
        super().__init__()
        self.id = "port_scan"
        self.name = "Local Port Scanner"
        self.description = "Scan local system for open TCP ports (security audit)."
        self.simple_description = "Check which network ports are open on your computer."
        self.category = FixCategory.SECURITY
        self.risk_level = RiskLevel.SAFE
        self.supported_platforms = ["windows", "linux", "darwin"]
        self.requires_admin = False
        self.estimated_time = 30
        self.tags = ["port", "scan", "network", "security", "audit"]
        # Scan common ports (faster than 1-1024)
        self.common_ports = [
            21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 
            993, 995, 1433, 1521, 3306, 3389, 5432, 5900, 8080, 8443
        ]

    def detect(self) -> bool:
        return True

    def preview(self) -> str:
        return f"Will scan {len(self.common_ports)} common ports on localhost for open connections."

    def _scan_port(self, host: str, port: int, timeout: float = 0.5) -> bool:
        """Check if a port is open."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def run(self) -> Dict[str, Any]:
        start_time = time.time()
        host = "127.0.0.1"
        open_ports: List[int] = []
        
        lines = []
        lines.append(f"Port Scan Results for {host}")
        lines.append("=" * 40)

        for port in self.common_ports:
            if self._scan_port(host, port):
                open_ports.append(port)
                lines.append(f"  Port {port:5d}: OPEN")

        if not open_ports:
            lines.append("  No common ports open.")

        execution_time = time.time() - start_time
        lines.append(f"\nScanned {len(self.common_ports)} ports in {execution_time:.2f}s")
        lines.append(f"Open ports found: {len(open_ports)}")

        output = "\n".join(lines)
        return {"output": output, "open_ports": open_ports, "execution_time": execution_time}

    def verify(self) -> bool:
        return True


FixRegistry.register(FileHashFix)
FixRegistry.register(PortScanFix)

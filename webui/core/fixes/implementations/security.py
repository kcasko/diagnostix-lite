"""
DiagnOStiX 3.0 - Security Fixes
"""

from typing import Dict, Any, Optional
from pathlib import Path

from core.fixes.base import Fix, FixCategory, RiskLevel
from core.fixes.registry import FixRegistry
from core.script_runner import script_runner


class FileHashFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "file_hash"
        self.name = "File Hash Validator"
        self.description = "Generate SHA256 hash of files for integrity verification."
        self.simple_description = "Check if a file has been tampered with by calculating its unique fingerprint."
        self.category = FixCategory.SECURITY
        self.risk_level = RiskLevel.SAFE
        self.supported_platforms = ["windows"]
        self.requires_admin = False
        self.estimated_time = 5
        self.tags = ["hash", "sha256", "integrity", "verify", "security"]
        self.target_file: Optional[str] = None

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
        result = script_runner.run_powershell_sync(
            "05-Utilities/TaurusTech-FileHash.ps1",
            args=[self.target_file]
        )
        return {"output": result.stdout, "file": self.target_file}

    def verify(self) -> bool:
        return True


class PortScanFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "port_scan"
        self.name = "Local Port Scanner"
        self.description = "Scan local system for open TCP ports (security audit)."
        self.simple_description = "Check which network ports are open on your computer."
        self.category = FixCategory.SECURITY
        self.risk_level = RiskLevel.SAFE
        self.supported_platforms = ["windows"]
        self.requires_admin = False
        self.estimated_time = 60
        self.tags = ["port", "scan", "network", "security", "audit"]

    def detect(self) -> bool:
        return True

    def preview(self) -> str:
        return "Will scan ports 1-1024 on localhost for open connections."

    def run(self) -> Dict[str, Any]:
        result = script_runner.run_powershell_sync("05-Utilities/TaurusTech-PortScan.ps1")
        return {"output": result.stdout, "execution_time": result.execution_time}

    def verify(self) -> bool:
        return True


FixRegistry.register(FileHashFix)
FixRegistry.register(PortScanFix)

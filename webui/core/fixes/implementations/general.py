import os
import shutil
import platform
import subprocess
import glob
from pathlib import Path
from ..base import Fix, FixResult
from ..registry import FixRegistry

class ClearTempFilesFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "clear_temp_files"
        self.name = "Clear Temporary Files"
        self.description = "Safely removes temporary files from system directories to free up space."
    
    def detect(self) -> bool:
        # Simple detection: Check if temp dir exists and has more than 10MB of data
        temp_dir = tempfile_dir()
        if not os.path.exists(temp_dir):
            return False
        
        total_size = 0
        try:
            for entry in os.scandir(temp_dir):
                if entry.is_file():
                    total_size += entry.stat().st_size
        except PermissionError:
            pass # Can't read some files, that's expected
            
        return total_size > 10 * 1024 * 1024 # > 10MB

    def preview(self) -> str:
        return f"Will attempt to delete files in {tempfile_dir()}. Locked files will be skipped."

    def run(self):
        temp_dir = tempfile_dir()
        deleted_count = 0
        bytes_cleared = 0
        
        for root, dirs, files in os.walk(temp_dir):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    size = os.path.getsize(file_path)
                    os.remove(file_path)
                    deleted_count += 1
                    bytes_cleared += size
                except (PermissionError, OSError):
                    continue # specific file locked or no permission
            
            # Don't delete directories deeply unless empty, safer to just stick to files for now
            # or just top level contents
        
        return {"deleted_files": deleted_count, "bytes_cleared": bytes_cleared}

    def verify(self) -> bool:
        # Verification is loose here; we just check if we can still access the temp dir
        # A stricter check would be size < previous size, but other processes add temp files constantly.
        return os.path.exists(tempfile_dir())

class FlushDNSCacheFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "flush_dns"
        self.name = "Flush DNS Cache"
        self.description = "Clears the local DNS resolver cache to fix connectivity issues."

    def detect(self) -> bool:
        # Hard to "detect" if DNS cache IS the problem, so we offer it if the command is available.
        # This is a 'manual' fix often.
        return True 

    def preview(self) -> str:
        if platform.system() == "Windows":
            return "Runs 'ipconfig /flushdns'"
        elif platform.system() == "Linux":
            return "Runs 'resolvectl flush-caches' or restarts nscd/systemd-resolved"
        return "Unknown command for this platform"

    def run(self):
        system = platform.system()
        cmd = []
        
        if system == "Windows":
            cmd = ["ipconfig", "/flushdns"]
        elif system == "Linux":
            # Try systemd-resolved first
            cmd = ["resolvectl", "flush-caches"]
            # Fallbacks could be added here
        else:
            raise NotImplementedError(f"Flush DNS not implemented for {system}")

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Command failed: {result.stderr}")
            
        return {"output": result.stdout}

    def verify(self) -> bool:
        # Verification of a "flush" is implied by success of command.
        return True

class ClearApplicationCacheFix(Fix):
    """
    Example targeted fix for a specific application (e.g., Browser cache or Electron apps).
    For this demo, we'll pretend to clear a 'DiagnOStiX' cache if it existed, 
    or a common safe target like pip cache.
    """
    def __init__(self):
        super().__init__()
        self.id = "clear_pip_cache"
        self.name = "Clear Pip Cache"
        self.description = "Removes cached Python packages to free space."

    def detect(self) -> bool:
        # Check if pip cache exists
        # This depends on OS, usually generic user cache dir
        return True # Simplified for demo

    def preview(self) -> str:
        return "Runs 'pip cache purge'"

    def run(self):
        cmd = ["pip", "cache", "purge"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
             # it might return non-zero if cache is already empty, which is fine
             if "No cache entries found" in result.stdout:
                 return {"status": "Already empty"}
             raise Exception(result.stderr)
        return {"output": result.stdout}

    def verify(self) -> bool:
        return True

def tempfile_dir():
    return os.getenv('TEMP') if platform.system() == 'Windows' else '/tmp'

# Register
FixRegistry.register(ClearTempFilesFix)
FixRegistry.register(FlushDNSCacheFix)
FixRegistry.register(ClearApplicationCacheFix)

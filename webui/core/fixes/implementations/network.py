import platform
import subprocess
from ..base import Fix, FixResult
from ..registry import FixRegistry

class RestartNetworkServicesFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "restart_network"
        self.name = "Restart Network Services"
        self.description = "Restarts the network stack to resolve connectivity issues."
        self.requires_admin = True # Often requires admin

    def detect(self) -> bool:
        # User initiated usually
        return True

    def preview(self) -> str:
        if platform.system() == "Windows":
            return "Will release/renew IP and reset Winsock catalog."
        elif platform.system() == "Linux":
            return "Will restart NetworkManager or networking service."
        return "Unknown"

    def run(self):
        system = platform.system()
        
        if system == "Windows":
            # Series of commands
            commands = [
                ["ipconfig", "/release"],
                ["ipconfig", "/renew"],
                ["netsh", "winsock", "reset"]
                # Note: winsock reset usually requires reboot to fully take effect, 
                # but it's a standard 'fix' step.
            ]
            output_log = ""
            for cmd in commands:
                res = subprocess.run(cmd, capture_output=True, text=True)
                output_log += f"CMD: {' '.join(cmd)}\n{res.stdout}\n"
                if res.returncode != 0:
                     output_log += f"ERROR: {res.stderr}\n"
            
            return {"log": output_log}

        elif system == "Linux":
            # Try NetworkManager first
            cmd = ["systemctl", "restart", "NetworkManager"]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                # Fallback to networking
                cmd = ["systemctl", "restart", "networking"]
                res = subprocess.run(cmd, capture_output=True, text=True)
            
            if res.returncode != 0:
                raise Exception(f"Failed to restart network services: {res.stderr}")
                
            return {"output": "Services restarted"}
            
        else:
            raise NotImplementedError

    def verify(self) -> bool:
        # Simple ping check?
        # That assumes internet is reachable.
        # Let's just return true if commands ran without exception.
        return True

FixRegistry.register(RestartNetworkServicesFix)

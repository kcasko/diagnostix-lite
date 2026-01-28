import psutil
from typing import Dict, Any
from ..base import Fix
from ..registry import FixRegistry

class TerminateRunawayProcessFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "terminate_process"
        self.name = "Terminate Process"
        self.description = "Terminates a specific process by PID. Requires explicit selection."
        self.target_pid = None

    def set_target(self, pid: int):
        """Set the target PID to kill."""
        self.target_pid = pid

    def detect(self) -> bool:
        # Check if a target is set and exists
        if self.target_pid is None:
            return False
        return psutil.pid_exists(self.target_pid)

    def preview(self) -> str:
        if not self.target_pid:
            return "No process selected."
        
        try:
            p = psutil.Process(self.target_pid)
            return f"Will terminate process '{p.name()}' (PID: {self.target_pid})."
        except psutil.NoSuchProcess:
            return f"Process PID {self.target_pid} no longer exists."

    def run(self) -> Dict[str, Any]:
        if not self.target_pid:
            raise ValueError("No target PID specified.")

        try:
            p = psutil.Process(self.target_pid)
            name = p.name()
            p.terminate()
            try:
                p.wait(timeout=3)
            except psutil.TimeoutExpired:
                p.kill()
            
            return {"terminated_pid": self.target_pid, "process_name": name}
        except psutil.NoSuchProcess:
            return {"status": "Process already gone"}

    def verify(self) -> bool:
        if not self.target_pid:
            return False
        return not psutil.pid_exists(self.target_pid)

FixRegistry.register(TerminateRunawayProcessFix)

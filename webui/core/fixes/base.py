from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from enum import Enum
import platform
import logging

logger = logging.getLogger(__name__)

class FixResult(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"

class Fix(ABC):
    """
    Abstract Base Class for all DiagnOStiX fixes.
    Enforces a strict lifecycle: Detect -> Preview -> Run -> Verify.
    """
    
    def __init__(self):
        self.id: str = "undefined_fix"
        self.name: str = "Undefined Fix"
        self.description: str = "No description provided."
        self.supported_platforms: List[str] = ["windows", "linux", "darwin"]
        self.requires_admin: bool = False
        self.is_safe: bool = True

    def check_platform_compatibility(self) -> bool:
        """Check if the current platform is supported."""
        current_os = platform.system().lower()
        return current_os in [p.lower() for p in self.supported_platforms]

    @abstractmethod
    def detect(self) -> bool:
        """
        Check if the fix is applicable/needed.
        Returns: True if the condition exists and needs fixing.
        """
        pass

    @abstractmethod
    def preview(self) -> str:
        """
        Return a human-readable description of exactly what will happen.
        """
        pass

    @abstractmethod
    def run(self) -> Dict[str, Any]:
        """
        Execute the fix. 
        Returns: A dictionary representing the 'after' state or result details.
        Raises: Exception on failure.
        """
        pass

    @abstractmethod
    def verify(self) -> bool:
        """
        Verify that the fix was successful.
        Returns: True if fixed, False otherwise.
        """
        pass

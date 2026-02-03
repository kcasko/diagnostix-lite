"""
DiagnOStiX 3.0 - Fix Base Classes

Defines the abstract base class for all fixes with:
- Category classification for UI organization
- Risk levels for safety indicators
- Platform compatibility checking
- Lifecycle enforcement (Detect -> Preview -> Run -> Verify)
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, TypedDict
from enum import Enum
import platform
import logging

logger = logging.getLogger(__name__)


class FixResult(Enum):
    """Result status of a fix execution."""
    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"


class FixCategory(Enum):
    """Categories for organizing fixes in the UI."""
    DIAGNOSTICS = "diagnostics"      # Read-only analysis tools
    MAINTENANCE = "maintenance"      # Cleanup and optimization
    NETWORK = "network"              # Network connectivity fixes
    PERFORMANCE = "performance"      # Speed and resource improvements
    SECURITY = "security"            # Security hardening and audits
    HARDWARE = "hardware"            # Hardware tests and diagnostics
    CONFIG = "config"                # System configuration changes
    PROCESS = "process"              # Process management

    @property
    def label(self) -> str:
        """Human-readable label for the category."""
        return {
            FixCategory.DIAGNOSTICS: "Diagnostics",
            FixCategory.MAINTENANCE: "Maintenance",
            FixCategory.NETWORK: "Network",
            FixCategory.PERFORMANCE: "Performance",
            FixCategory.SECURITY: "Security",
            FixCategory.HARDWARE: "Hardware",
            FixCategory.CONFIG: "Configuration",
            FixCategory.PROCESS: "Process Management"
        }[self]

    @property
    def icon(self) -> str:
        """Icon identifier for UI."""
        return {
            FixCategory.DIAGNOSTICS: "search",
            FixCategory.MAINTENANCE: "wrench",
            FixCategory.NETWORK: "wifi",
            FixCategory.PERFORMANCE: "zap",
            FixCategory.SECURITY: "shield",
            FixCategory.HARDWARE: "cpu",
            FixCategory.CONFIG: "settings",
            FixCategory.PROCESS: "activity"
        }[self]


class RiskLevel(Enum):
    """Risk classification for fixes."""
    SAFE = "safe"           # No data loss possible, read-only or easily reversible
    MODERATE = "moderate"   # May require restart, changes system state
    DANGEROUS = "dangerous" # Could break things, requires backup first

    @property
    def color(self) -> str:
        """Get UI color for risk level."""
        return {
            RiskLevel.SAFE: "#22c55e",       # Green
            RiskLevel.MODERATE: "#f59e0b",   # Amber
            RiskLevel.DANGEROUS: "#ef4444"   # Red
        }[self]

    @property
    def label(self) -> str:
        """Get human-readable label."""
        return {
            RiskLevel.SAFE: "Safe",
            RiskLevel.MODERATE: "Caution",
            RiskLevel.DANGEROUS: "Dangerous"
        }[self]

    @property
    def requires_confirmation(self) -> bool:
        """Whether this risk level requires user confirmation."""
        return self in [RiskLevel.MODERATE, RiskLevel.DANGEROUS]

    @property
    def requires_typed_confirmation(self) -> bool:
        """Whether this risk level requires typed confirmation."""
        return self == RiskLevel.DANGEROUS


class FixParam(TypedDict, total=False):
    """Definition of a required parameter for a fix."""
    name: str          # Parameter name (used as key)
    label: str         # Human-readable label
    type: str          # 'text', 'number', 'file'
    placeholder: str   # Placeholder text
    required: bool     # Whether the param is required


class Fix(ABC):
    """
    Abstract Base Class for all DiagnOStiX fixes.
    Enforces a strict lifecycle: Detect -> Preview -> Run -> Verify.
    """

    def __init__(self):
        # Core identification
        self.id: str = "undefined_fix"
        self.name: str = "Undefined Fix"
        self.description: str = "No description provided."
        self.simple_description: str = ""  # Plain English for Simple Mode

        # Classification
        self.category: FixCategory = FixCategory.MAINTENANCE
        self.risk_level: RiskLevel = RiskLevel.SAFE

        # Platform and requirements
        self.supported_platforms: List[str] = ["windows", "linux", "darwin"]
        self.requires_admin: bool = False
        self.requires_reboot: bool = False

        # Metadata
        self.estimated_time: int = 10  # seconds
        self.tags: List[str] = []

        # Legacy compatibility (deprecated - use risk_level instead)
        self.is_safe: bool = True

        # Dynamic input parameters
        self.required_params: List[FixParam] = []

    def check_platform_compatibility(self) -> bool:
        """Check if the current platform is supported."""
        current_os = platform.system().lower()
        return current_os in [p.lower() for p in self.supported_platforms]

    def get_simple_description(self) -> str:
        """Get plain English description for Simple Mode users."""
        return self.simple_description if self.simple_description else self.description

    def to_dict(self) -> Dict[str, Any]:
        """Convert fix metadata to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "simple_description": self.get_simple_description(),
            "category": self.category.value,
            "category_label": self.category.label,
            "risk_level": self.risk_level.value,
            "risk_label": self.risk_level.label,
            "risk_color": self.risk_level.color,
            "requires_confirmation": self.risk_level.requires_confirmation,
            "requires_typed_confirmation": self.risk_level.requires_typed_confirmation,
            "supported_platforms": self.supported_platforms,
            "requires_admin": self.requires_admin,
            "requires_reboot": self.requires_reboot,
            "estimated_time": self.estimated_time,
            "tags": self.tags,
            "supported": self.check_platform_compatibility(),
            "required_params": self.required_params
        }

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

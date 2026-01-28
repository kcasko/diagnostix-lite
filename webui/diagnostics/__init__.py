"""
DiagnOStiX - Python Diagnostic Module
Cross-platform system diagnostics using Python libraries
"""

from typing import Dict, Callable

# Import diagnostic functions
from .about_diagnostix import run as about_diagnostix
from .system_overview import run as system_overview
from .hardware_health import run as hardware_health
from .disk_diagnostics import run as disk_diagnostics
from .network_diagnostics import run as network_diagnostics
from .memory_stress_test import run as memory_stress_test
from .cpu_stress_test import run as cpu_stress_test
from .gpu_diagnostics import run as gpu_diagnostics

# Diagnostic function registry
DIAGNOSTIC_FUNCTIONS: Dict[str, Callable[[], str]] = {
    "about_diagnostix": about_diagnostix,
    "system_overview": system_overview,
    "hardware_health": hardware_health,
    "disk_diagnostics": disk_diagnostics,
    "network_diagnostics": network_diagnostics,
    "memory_stress_test": memory_stress_test,
    "cpu_stress_test": cpu_stress_test,
    "gpu_diagnostics": gpu_diagnostics,
}

__all__ = ["DIAGNOSTIC_FUNCTIONS"]

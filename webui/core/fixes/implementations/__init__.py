"""
DiagnOStiX 3.0 - Fix Implementations

Auto-imports all fix modules to register them with the FixRegistry.
"""

# Import all fix implementation modules to trigger registration
from core.fixes.implementations import diagnostics
from core.fixes.implementations import security
from core.fixes.implementations import performance
from core.fixes.implementations import process_advanced
from core.fixes.implementations import network_advanced
from core.fixes.implementations import maintenance
from core.fixes.implementations import hardware
from core.fixes.implementations import config

# Also import original implementations for backwards compatibility
from core.fixes.implementations import general
from core.fixes.implementations import network
from core.fixes.implementations import process

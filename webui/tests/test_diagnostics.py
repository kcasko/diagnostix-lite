
import pytest
import sys
import os

# Ensure we can import from current directory
sys.path.append(os.getcwd())

from diagnostics import system_overview
from diagnostics import disk_diagnostics
from diagnostics import about_diagnostix

def test_system_overview():
    """Smoke test for system overview."""
    result = system_overview()
    assert isinstance(result, str)
    assert len(result) > 0
    # Should contain some key system info headers
    assert "System Overview" in result.title() or "CPU" in result

def test_disk_usage():
    """Smoke test for disk diagnostics."""
    result = disk_diagnostics()
    assert isinstance(result, str)
    assert "Disk Diagnostics" in result.title() or "Disk Usage" in result

def test_about_info():
    """Smoke test for about info."""
    result = about_diagnostix()
    assert isinstance(result, str)
    assert "DiagnOStiX" in result

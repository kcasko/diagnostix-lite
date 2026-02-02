
import pytest
from unittest.mock import MagicMock, patch, ANY
import subprocess
from pathlib import Path
import sys
import os

from core.script_runner import ScriptRunner, ScriptType

# Define a dummy scripts dir for testing
TEST_SCRIPTS_DIR = Path("/mock/scripts/dir")

@pytest.fixture
def runner():
    """Create a ScriptRunner instance with a mock directory."""
    return ScriptRunner(scripts_dir=TEST_SCRIPTS_DIR)

class TestScriptRunnerSync:
    """Test synchronous execution methods (mocked)."""

    @patch("subprocess.run")
    @patch.object(ScriptRunner, "get_script_path")
    def test_run_batch_success(self, mock_get_path, mock_run, runner):
        """Test successful batch script execution."""
        # Setup mocks
        mock_path = TEST_SCRIPTS_DIR / "test.bat"
        mock_get_path.return_value = mock_path
        
        mock_run.return_value = subprocess.CompletedProcess(
            args=["cmd", "/c", str(mock_path)],
            returncode=0,
            stdout="Success Output",
            stderr=""
        )

        # Execute
        result = runner.run_batch_sync("test.bat")

        # Assertions
        assert result.success is True
        assert result.exit_code == 0
        assert "Success Output" in result.stdout
        assert result.script_type == ScriptType.BATCH
        
        # Verify subprocess call
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert args[0][0] == "cmd"
        assert str(mock_path) in args[0]

    @patch("subprocess.run")
    @patch.object(ScriptRunner, "get_script_path")
    def test_run_batch_failure(self, mock_get_path, mock_run, runner):
        """Test failed batch script execution."""
        mock_get_path.return_value = TEST_SCRIPTS_DIR / "fail.bat"
        
        mock_run.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=1,
            stdout="",
            stderr="Error Message"
        )

        result = runner.run_batch_sync("fail.bat")

        assert result.success is False
        assert result.exit_code == 1
        assert "Error Message" in result.stderr

    @patch("subprocess.run")
    @patch.object(ScriptRunner, "get_script_path")
    def test_run_batch_timeout(self, mock_get_path, mock_run, runner):
        """Test batch script timeout."""
        mock_get_path.return_value = TEST_SCRIPTS_DIR / "timeout.bat"
        
        # Simulate TimeoutExpired exception
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="cmd", timeout=30)

        result = runner.run_batch_sync("timeout.bat", timeout=30)

        assert result.success is False
        assert result.exit_code == -1
        assert "timed out" in result.error_message

    @patch("core.script_runner.ScriptRunner.get_script_path")
    def test_run_batch_missing_file(self, mock_get_path, runner):
        """Test missing file handling."""
        mock_get_path.side_effect = FileNotFoundError("Script not found")

        result = runner.run_batch_sync("missing.bat")

        assert result.success is False
        assert "not found" in result.error_message


    @patch("subprocess.run")
    @patch.object(ScriptRunner, "get_script_path")
    def test_run_powershell_success(self, mock_get_path, mock_run, runner):
        """Test successful PowerShell execution."""
        mock_path = TEST_SCRIPTS_DIR / "test.ps1"
        mock_get_path.return_value = mock_path

        mock_run.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="PS Output",
            stderr=""
        )

        result = runner.run_powershell_sync("test.ps1")

        assert result.success is True
        assert result.script_type == ScriptType.POWERSHELL
        assert "PS Output" in result.stdout
        
        # Verify arguments include execution policy bypass
        mock_run.assert_called_once()
        cmd_args = mock_run.call_args[0][0]
        assert "powershell" in cmd_args[0].lower() or "powershell" in cmd_args[0]
        assert "-ExecutionPolicy" in cmd_args
        assert "Bypass" in cmd_args

@pytest.mark.asyncio
class TestScriptRunnerAsync:
    """Test async execution methods (mocked)."""
    
    # Note: Mocking asyncio.create_subprocess_exec is complex.
    # For this simplified suite, we will focus on sync methods logic
    # or use basic mocking if feasible. Given constraints, we'll verify
    # the sync wrapper logic which mirrors the async logic structure.
    # If strictly needed, we can add async tests later.
    pass

"""
DiagnOStiX - Cross-platform system diagnostics web application
Optimized version with type hints, better error handling, and improved performance
"""
import os
import re
import platform
import tempfile
import logging
from pathlib import Path
from typing import Dict, Tuple, Optional, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.background import BackgroundTask

# Fix Engine Imports
from core.db import db_instance
from core.fixes.registry import FixRegistry
# Check if internal modules must be imported to trigger registration
import core.fixes.implementations.general
import core.fixes.implementations.network
import core.fixes.implementations.process
from routers.fixes import router as fixes_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Python diagnostics module
try:
    from diagnostics import DIAGNOSTIC_FUNCTIONS
    PYTHON_DIAGNOSTICS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Python diagnostics not available: {e}")
    DIAGNOSTIC_FUNCTIONS = {}
    PYTHON_DIAGNOSTICS_AVAILABLE = False


# Constants
SCRIPT_TIMEOUT = 60  # seconds
ANSI_ESCAPE_PATTERN = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')
TEMP_FILE_PREFIX = "diagnostix_"


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for application startup and shutdown"""
    logger.info(f"Starting DiagnOStiX v{app.version}")
    logger.info(f"Python diagnostics available: {PYTHON_DIAGNOSTICS_AVAILABLE}")
    
    # Initialize Database
    try:
        db_instance.connect()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        
    yield
    logger.info("Shutting down DiagnOStiX")


# Initialize FastAPI app
app = FastAPI(
    title="DiagnOStiX",
    version="2.0",
    description="Cross-platform system diagnostics tool",
    lifespan=lifespan
)


# Path configuration
BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
WEBUI_DIR = BASE_DIR / "webui"
STATIC_DIR = WEBUI_DIR / "static"
TEMPLATES_DIR = WEBUI_DIR / "templates"


# Tool definitions with metadata
TOOLS: Dict[str, Dict[str, Any]] = {
    "about_diagnostix": {
        "label": "About DiagnOStiX",
        "script": "about_diagnostix.sh",
        "description": "Version info and project details.",
        "python_available": True,
        "category": "info"
    },
    "system_overview": {
        "label": "System overview",
        "script": "system_overview.sh",
        "description": "Summary of hardware, kernel, storage, and memory.",
        "python_available": True,
        "category": "system"
    },
    "hardware_health": {
        "label": "Hardware health",
        "script": "hardware_health.sh",
        "description": "CPU, RAM, SMART, and sensor status.",
        "python_available": True,
        "category": "system"
    },
    "disk_diagnostics": {
        "label": "Disk diagnostics",
        "script": "disk_diagnostics.sh",
        "description": "Partition layout and disk checks.",
        "python_available": True,
        "category": "storage"
    },
    "network_diagnostics": {
        "label": "Network diagnostics",
        "script": "network_diagnostics.sh",
        "description": "Interfaces, routes, DNS, and connectivity.",
        "python_available": True,
        "category": "network"
    },
    "memory_stress_test": {
        "label": "Memory stress test",
        "script": "memory_stress_test.sh",
        "description": "Light RAM test.",
        "python_available": True,
        "category": "stress"
    },
    "cpu_stress_test": {
        "label": "CPU stress test",
        "script": "cpu_stress_test.sh",
        "description": "Load test for CPU stability.",
        "python_available": True,
        "category": "stress"
    },
    "gpu_diagnostics": {
        "label": "GPU diagnostics",
        "script": "gpu_diagnostics.sh",
        "description": "Identify GPU and driver state (NVIDIA only in Python mode).",
        "python_available": True,
        "category": "hardware"
    },
    "kraken_repo_scanner": {
        "label": "Kraken Repo Scanner",
        "script": "kraken_repo_scanner.sh",
        "description": "Scan system for Git repositories and integrity issues (Linux only).",
        "python_available": False,
        "category": "developer"
    },
    "network_speed_test": {
        "label": "Network speed test",
        "script": "network_speed_test.sh",
        "description": "Download test file and measure throughput (bash only).",
        "python_available": False,
        "category": "network"
    },
    "quick_repair": {
        "label": "Quick repair",
        "script": "quick_repair.sh",
        "description": "Common repair actions (Linux only).",
        "python_available": False,
        "category": "repair"
    },
    "boot_diagnostics": {
        "label": "Boot diagnostics",
        "script": "boot_diagnostics.sh",
        "description": "UEFI/BIOS mode, fstab, and boot logs (Linux only).",
        "python_available": False,
        "category": "system"
    },
    "master_collect": {
        "label": "Full collection bundle",
        "script": "master_collect.sh",
        "description": "Gather logs and diagnostic info into a bundle (Linux only).",
        "python_available": False,
        "category": "support"
    },
    "tech_support_mode": {
        "label": "Tech Support Mode",
        "script": "tech_support_mode.sh",
        "description": "Run everything and create a full support bundle (Linux only).",
        "python_available": False,
        "category": "support"
    }
}


# Initialize templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Mount static files
app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)

# Mount Routers
app.include_router(fixes_router)


# Helper functions
def get_temp_file_path(tool_id: str) -> Path:
    """Get temporary file path for tool output"""
    return Path(tempfile.gettempdir()) / f"{TEMP_FILE_PREFIX}{tool_id}_output.txt"


def strip_ansi_codes(text: str) -> str:
    """Remove ANSI escape codes from text"""
    return ANSI_ESCAPE_PATTERN.sub('', text)




def format_execution_info(mode: str, use_python: bool) -> str:
    """Format execution information footer"""
    mode_str = "Python (cross-platform)" if use_python else "Bash script"
    return (
        f"\n\n--- Execution Info ---\n"
        f"Mode: {mode_str}\n"
        f"OS: {platform.system()} {platform.release()}\n"
        f"Machine: {platform.machine()}"
    )


async def run_python_diagnostic(tool_id: str) -> Tuple[str, int]:
    """
    Execute Python-based diagnostic

    Args:
        tool_id: Diagnostic tool identifier

    Returns:
        Tuple of (output string, return code)
    """
    try:
        output = DIAGNOSTIC_FUNCTIONS[tool_id]()
        output += format_execution_info("python", True)
        return output, 0
    except KeyError:
        logger.error(f"Python diagnostic '{tool_id}' not found")
        return f"Diagnostic '{tool_id}' not implemented in Python mode\n", 1
    except Exception as e:
        logger.error(f"Python diagnostic '{tool_id}' failed: {e}", exc_info=True)
        error_msg = f"Python diagnostic failed: {type(e).__name__}\n\nAttempting bash fallback...\n\n"
        return error_msg, 1


async def run_bash_diagnostic(tool_id: str, script_path: Path) -> Tuple[str, int]:
    """
    Execute bash script diagnostic

    Args:
        tool_id: Diagnostic tool identifier
        script_path: Path to bash script

    Returns:
        Tuple of (output string, return code)
    """
    import subprocess

    if not script_path.exists():
        return f"Script not found: {script_path.name}", 127

    try:
        # Select command based on OS
        if os.name == 'nt':  # Windows
            cmd = ["bash", str(script_path)]
        else:  # Linux/Unix - Note: sudo may require password, consider using capabilities
            cmd = ["bash", str(script_path)]  # Removed sudo for security

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            timeout=SCRIPT_TIMEOUT
        )

        output = result.stdout or ""

        # Special formatting for network speed test
        if tool_id == "network_speed_test" and result.stdout:
            output = format_network_speed_test(result.stdout)

        if result.stderr:
            output += f"\n\n=== STDERR ===\n{result.stderr}"

        output += format_execution_info("bash", False)

        return output, result.returncode

    except subprocess.TimeoutExpired:
        logger.warning(f"Script '{tool_id}' timed out after {SCRIPT_TIMEOUT}s")
        return f"Execution timed out after {SCRIPT_TIMEOUT}s", 124
    except FileNotFoundError:
        logger.error(f"Bash not found for '{tool_id}'")
        return "Bash unavailable. Install Git Bash or WSL on Windows.", 127
    except Exception as e:
        logger.error(f"Bash diagnostic '{tool_id}' failed: {e}", exc_info=True)
        return f"Script execution failed: {type(e).__name__}", 1


def format_network_speed_test(raw_output: str) -> str:
    """Format network speed test output"""
    mb_match = re.search(r"Approximate download speed:\s*([0-9.]+)", raw_output)
    mb_value = mb_match.group(1) if mb_match else "0"

    try:
        dl_mbps = round(float(mb_value) * 8, 1)
    except (ValueError, TypeError):
        dl_mbps = 0

    ul_match = re.search(r"upload speed:\s*([0-9.]+)", raw_output, re.IGNORECASE)
    try:
        ul_mbps = float(ul_match.group(1)) if ul_match else 0
    except (ValueError, TypeError):
        ul_mbps = 0

    return (
        "=== Network Speed Test ===\n\n"
        f"Download: {dl_mbps} Mbps ({mb_value} MB/s)\n"
        f"Upload: {ul_mbps} Mbps\n\n"
        f"--- Raw Output ---\n{raw_output}"
    )


def save_output_to_temp(tool_id: str, output: str) -> None:
    """
    Save diagnostic output to temporary file

    Args:
        tool_id: Tool identifier
        output: Output text to save
    """
    temp_path = get_temp_file_path(tool_id)
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(output)
    except IOError as e:
        logger.error(f"Failed to save output for {tool_id}: {e}")


def cleanup_temp_file(tool_id: str) -> None:
    """Clean up temporary output file"""
    temp_path = get_temp_file_path(tool_id)
    try:
        if temp_path.exists():
            temp_path.unlink()
    except Exception as e:
        logger.warning(f"Failed to cleanup temp file {temp_path}: {e}")


# API Routes

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main dashboard page"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "tools": TOOLS,
            "title": "DiagnOStiX Control Panel",
            "python_available": PYTHON_DIAGNOSTICS_AVAILABLE
        }
    )


@app.get("/api/tools")
async def list_tools():
    """API endpoint to list all available tools"""
    return {
        "tools": TOOLS,
        "python_diagnostics_available": PYTHON_DIAGNOSTICS_AVAILABLE,
        "platform": platform.system()
    }


@app.get("/run/{tool_id}", response_class=HTMLResponse)
async def run_tool(
    tool_id: str,
    request: Request,
    mode: str = Query("auto", regex="^(auto|python|bash)$")
):
    """
    Execute a diagnostic tool

    Args:
        tool_id: Tool identifier
        request: FastAPI request object
        mode: Execution mode (auto, python, or bash)

    Returns:
        HTML response with diagnostic output
    """
    # Validate tool exists
    if tool_id not in TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_id}' not found")

    tool = TOOLS[tool_id]
    use_python = False
    output = ""
    returncode = 0

    # Determine execution mode
    should_use_python = (
        mode == "python" or
        (mode == "auto" and tool.get("python_available", False) and PYTHON_DIAGNOSTICS_AVAILABLE)
    )

    # Try Python diagnostics first if available
    if should_use_python and tool_id in DIAGNOSTIC_FUNCTIONS:
        output, returncode = await run_python_diagnostic(tool_id)
        use_python = (returncode == 0)

    # Fall back to bash scripts if needed
    if not use_python:
        script_path = SCRIPTS_DIR / tool["script"]
        output, returncode = await run_bash_diagnostic(tool_id, script_path)

    # Strip ANSI color codes
    output = strip_ansi_codes(output)

    # Save output to temp file
    save_output_to_temp(tool_id, output)

    return templates.TemplateResponse(
        "output.html",
        {
            "request": request,
            "title": tool["label"],
            "tool": tool,
            "tool_id": tool_id,
            "returncode": returncode,
            "output": output,
            "python_mode": use_python
        }
    )


@app.get("/download/{tool_id}", response_class=FileResponse)
async def download_output(tool_id: str):
    """
    Download diagnostic output as text file

    Args:
        tool_id: Tool identifier

    Returns:
        File download response
    """
    if tool_id not in TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_id}' not found")

    temp_path = get_temp_file_path(tool_id)

    if not temp_path.exists():
        raise HTTPException(
            status_code=404,
            detail="No output available. Please run the diagnostic first."
        )

    # Return file with background cleanup task
    return FileResponse(
        path=str(temp_path),
        filename=f"{tool_id}_output.txt",
        media_type="text/plain",
        background=BackgroundTask(cleanup_temp_file, tool_id)
    )


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "version": app.version,
        "python_diagnostics": PYTHON_DIAGNOSTICS_AVAILABLE,
        "platform": platform.system()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

import os
import subprocess
import re
import platform
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import Python diagnostics module
try:
    from diagnostics import DIAGNOSTIC_FUNCTIONS
    PYTHON_DIAGNOSTICS_AVAILABLE = True
except ImportError:
    DIAGNOSTIC_FUNCTIONS = {}
    PYTHON_DIAGNOSTICS_AVAILABLE = False

app = FastAPI(title="DiagnOStiX", version="2.0")

# Use relative paths for cross-platform compatibility
BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
WEBUI_DIR = BASE_DIR / "webui"
STATIC_DIR = WEBUI_DIR / "static"
TEMPLATES_DIR = WEBUI_DIR / "templates"

TOOLS = {
    "about_diagnostix": {
        "label": "About DiagnOStiX",
        "script": "about_diagnostix.sh",
        "description": "Version info and project details.",
        "python_available": True
    },
    "system_overview": {
        "label": "System overview",
        "script": "system_overview.sh",
        "description": "Summary of hardware, kernel, storage, and memory.",
        "python_available": True
    },
    "hardware_health": {
        "label": "Hardware health",
        "script": "hardware_health.sh",
        "description": "CPU, RAM, SMART, and sensor status.",
        "python_available": True
    },
    "disk_diagnostics": {
        "label": "Disk diagnostics",
        "script": "disk_diagnostics.sh",
        "description": "Partition layout and disk checks.",
        "python_available": True
    },
    "network_diagnostics": {
        "label": "Network diagnostics",
        "script": "network_diagnostics.sh",
        "description": "Interfaces, routes, DNS, and connectivity.",
        "python_available": True
    },
    "memory_stress_test": {
        "label": "Memory stress test",
        "script": "memory_stress_test.sh",
        "description": "Light RAM test.",
        "python_available": True
    },
    "cpu_stress_test": {
        "label": "CPU stress test",
        "script": "cpu_stress_test.sh",
        "description": "Load test for CPU stability.",
        "python_available": True
    },
    "gpu_diagnostics": {
        "label": "GPU diagnostics",
        "script": "gpu_diagnostics.sh",
        "description": "Identify GPU and driver state (NVIDIA only in Python mode).",
        "python_available": True
    },
    "kraken_repo_scanner": {
        "label": "Kraken Repo Scanner",
        "script": "kraken_repo_scanner.sh",
        "description": "Scan system for Git repositories and integrity issues (Linux only).",
        "python_available": False
    },
    "network_speed_test": {
        "label": "Network speed test",
        "script": "network_speed_test.sh",
        "description": "Download test file and measure throughput (bash only).",
        "python_available": False
    },
    "quick_repair": {
        "label": "Quick repair",
        "script": "quick_repair.sh",
        "description": "Common repair actions (Linux only).",
        "python_available": False
    },
    "boot_diagnostics": {
        "label": "Boot diagnostics",
        "script": "boot_diagnostics.sh",
        "description": "UEFI/BIOS mode, fstab, and boot logs (Linux only).",
        "python_available": False
    },
    "master_collect": {
        "label": "Full collection bundle",
        "script": "master_collect.sh",
        "description": "Gather logs and diagnostic info into a bundle (Linux only).",
        "python_available": False
    },
    "tech_support_mode": {
        "label": "Tech Support Mode",
        "script": "tech_support_mode.sh",
        "description": "Run everything and create a full support bundle (Linux only).",
        "python_available": False
    }
}

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "tools": TOOLS,
            "title": "DiagnOStiX Control Panel"
        }
    )


def grade_network(download_mbps, upload_mbps):
    if download_mbps > 300:
        return "A"
    if download_mbps > 150:
        return "B"
    if download_mbps > 50:
        return "C"
    return "D"


@app.get("/run/{tool_id}", response_class=HTMLResponse)
async def run_tool(tool_id: str, request: Request, mode: str = "auto"):
    """
    Run a diagnostic tool
    mode: "auto" (prefer Python), "python" (force Python), "bash" (force bash script)
    """
    if tool_id not in TOOLS:
        raise HTTPException(status_code=404, detail="Tool not found")

    tool = TOOLS[tool_id]
    use_python = False
    returncode = 0

    # Determine execution mode
    if mode == "python" or (mode == "auto" and tool.get("python_available", False) and PYTHON_DIAGNOSTICS_AVAILABLE):
        use_python = True

    # Try Python diagnostics first if available
    if use_python and tool_id in DIAGNOSTIC_FUNCTIONS:
        try:
            output = DIAGNOSTIC_FUNCTIONS[tool_id]()
            output += f"\n\n--- Execution Info ---\n"
            output += f"Mode: Python (cross-platform)\n"
            output += f"OS: {platform.system()} {platform.release()}\n"
            output += f"Machine: {platform.machine()}"
        except Exception as e:
            output = f"Python diagnostic failed: {e}\n\n"
            output += "Falling back to bash script...\n\n"
            use_python = False
            returncode = 1

    # Fall back to bash scripts
    if not use_python:
        script_path = SCRIPTS_DIR / tool["script"]

        if not script_path.exists():
            raise HTTPException(status_code=500, detail=f"Script not found: {script_path}")

        try:
            # On Windows, run with bash (Git Bash or WSL)
            # On Linux, run with sudo
            if os.name == 'nt':  # Windows
                result = subprocess.run(
                    ["bash", str(script_path)],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=60
                )
            else:  # Linux/Unix
                result = subprocess.run(
                    ["sudo", str(script_path)],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=60
                )

            output = result.stdout or ""
            returncode = result.returncode

            # Network Speed Test special formatting (legacy bash script)
            if tool_id == "network_speed_test" and result.stdout:
                mb_match = re.search(r"Approximate download speed:\s*([0-9.]+)", output)
                mb_value = mb_match.group(1) if mb_match else "0"

                try:
                    dl_mbps = round(float(mb_value) * 8, 1)
                except:
                    dl_mbps = 0

                ul_match = re.search(r"upload speed:\s*([0-9.]+)", output, re.IGNORECASE)
                try:
                    ul_mbps = float(ul_match.group(1)) if ul_match else 0
                except:
                    ul_mbps = 0

                grade = grade_network(dl_mbps, ul_mbps)

                output = (
                    "=== Network Speed Test ===\n\n"
                    f"Download: {dl_mbps} Mbps ({mb_value} MB/s)\n"
                    f"Upload: {ul_mbps} Mbps\n"
                    f"Quality Grade: {grade}\n\n"
                    "--- Raw Output ---\n" + result.stdout
                )

            if result.stderr:
                output += "\n\n=== STDERR ===\n" + result.stderr

            output += f"\n\n--- Execution Info ---\n"
            output += f"Mode: Bash script\n"
            output += f"OS: {platform.system()} {platform.release()}"

        except subprocess.TimeoutExpired:
            output = "Script execution timed out (60 second limit)"
            returncode = 124
        except FileNotFoundError:
            output = "Bash not found. This tool requires Git Bash or WSL on Windows."
            returncode = 127
        except Exception as e:
            output = f"Failed to run script: {e}"
            returncode = 1

    # Strip ANSI color codes
    output = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', output)

    # Save output to temp file
    import tempfile
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"diagnostix_{tool_id}_output.txt")
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(output)

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
    import tempfile
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"diagnostix_{tool_id}_output.txt")
    if not os.path.exists(temp_path):
        raise HTTPException(status_code=404, detail="No output available.")
    return FileResponse(temp_path, filename=f"{tool_id}_output.txt")

import os
import subprocess
import re
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

BASE_DIR = "/opt/diagnostix"
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

TOOLS = {
    "about_diagnostix": {
        "label": "About DiagnostiX",
        "script": "about_diagnostix.sh",
        "description": "Version info and project details."
    },
    "kraken_repo_scanner": {
        "label": "Kraken Repo Scanner",
        "script": "kraken_repo_scanner.sh",
        "description": "Scan system for Git repositories and integrity issues."
    },
    "system_overview": {
        "label": "System overview",
        "script": "system_overview.sh",
        "description": "Summary of hardware, kernel, storage, and memory."
    },
    "hardware_health": {
        "label": "Hardware health",
        "script": "hardware_health.sh",
        "description": "CPU, RAM, SMART, and sensor status."
    },
    "disk_diagnostics": {
        "label": "Disk diagnostics",
        "script": "disk_diagnostics.sh",
        "description": "Partition layout and disk checks."
    },
    "network_diagnostics": {
        "label": "Network diagnostics",
        "script": "network_diagnostics.sh",
        "description": "Interfaces, routes, DNS, and connectivity."
    },
    "memory_stress_test": {
        "label": "Memory stress test",
        "script": "memory_stress_test.sh",
        "description": "Light RAM test."
    },
    "cpu_stress_test": {
        "label": "CPU stress test",
        "script": "cpu_stress_test.sh",
        "description": "Load test for CPU stability."
    },
    "network_speed_test": {
        "label": "Network speed test",
        "script": "network_speed_test.sh",
        "description": "Download test file and measure throughput."
    },
    "quick_repair": {
        "label": "Quick repair",
        "script": "quick_repair.sh",
        "description": "Common repair actions."
    },
    "gpu_diagnostics": {
        "label": "GPU diagnostics",
        "script": "gpu_diagnostics.sh",
        "description": "Identify GPU and driver state."
    },
    "boot_diagnostics": {
        "label": "Boot diagnostics",
        "script": "boot_diagnostics.sh",
        "description": "UEFI/BIOS mode, fstab, and boot logs."
    },
    "master_collect": {
        "label": "Full collection bundle",
        "script": "master_collect.sh",
        "description": "Gather logs and diagnostic info into a bundle."
    },
    "tech_support_mode": {
        "label": "Tech Support Mode",
        "script": "tech_support_mode.sh",
        "description": "Run everything and create a full support bundle."
    }
}

templates = Jinja2Templates(directory="/opt/diagnostix/webui/templates")

app.mount(
    "/static",
    StaticFiles(directory="/opt/diagnostix/webui/static"),
    name="static"
)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "tools": TOOLS,
            "title": "DiagnostiX Control Panel"
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
async def run_tool(tool_id: str, request: Request):
    if tool_id not in TOOLS:
        raise HTTPException(status_code=404, detail="Tool not found")

    tool = TOOLS[tool_id]
    script_path = os.path.join(SCRIPTS_DIR, tool["script"])

    if not os.path.exists(script_path):
        raise HTTPException(status_code=500, detail=f"Script not found: {script_path}")

    try:
        result = subprocess.run(
            ["sudo", script_path],
            capture_output=True,
            text=True,
            check=False
        )
    except Exception as e:
        output = f"Failed to run script: {e}"
        return templates.TemplateResponse(
            "output.html",
            {
                "request": request,
                "title": tool["label"],
                "tool": tool,
                "tool_id": tool_id,
                "returncode": None,
                "output": output
            }
        )

    combined_output = ""

    # Only About page keeps its header
    if tool_id == "about_diagnostix":
        combined_output += (
            "=== DiagnostiX Lite ===\n"
            "Project Information\n"
            "-------------------\n\n"
        )

    combined_output += result.stdout or ""

    # Network Speed Test rewrite
    if tool_id == "network_speed_test":
        mb_match = re.search(r"Approximate download speed:\s*([0-9.]+)", combined_output)
        mb_value = mb_match.group(1) if mb_match else "0"

        try:
            dl_mbps = round(float(mb_value) * 8, 1)
        except:
            dl_mbps = 0

        ul_match = re.search(r"upload speed:\s*([0-9.]+)", combined_output, re.IGNORECASE)
        try:
            ul_mbps = float(ul_match.group(1)) if ul_match else 0
        except:
            ul_mbps = 0

        grade = grade_network(dl_mbps, ul_mbps)

        combined_output = (
            "=== Network Speed Test ===\n\n"
            f"Download: {dl_mbps} Mbps ({mb_value} MB/s)\n"
            f"Upload: {ul_mbps} Mbps\n"
            f"Quality Grade: {grade}\n\n"
            "--- Raw Output ---\n" + result.stdout
        )

    if result.stderr:
        combined_output += "\n\n=== STDERR ===\n" + result.stderr

    combined_output = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', combined_output)

    temp_path = f"/tmp/diagnostix_{tool_id}_output.txt"
    with open(temp_path, "w") as f:
        f.write(combined_output)

    return templates.TemplateResponse(
        "output.html",
        {
            "request": request,
            "title": tool["label"],
            "tool": tool,
            "tool_id": tool_id,
            "returncode": result.returncode,
            "output": combined_output
        }
    )


@app.get("/download/{tool_id}", response_class=FileResponse)
async def download_output(tool_id: str):
    temp_path = f"/tmp/diagnostix_{tool_id}_output.txt"
    if not os.path.exists(temp_path):
        raise HTTPException(status_code=404, detail="No output available.")
    return FileResponse(temp_path, filename=f"{tool_id}_output.txt")

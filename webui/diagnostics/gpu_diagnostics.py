"""
GPU Diagnostics - Identify GPU vendor and driver state
"""
import json
import platform
import shutil
import subprocess
from datetime import datetime
from typing import Dict, List


def _run_command(cmd: List[str], timeout: int = 10) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.SubprocessError):
        return ""
    return ""


def detect_gpu_vendor(name: str) -> str:
    lower = name.lower()
    if "nvidia" in lower:
        return "nvidia"
    if "amd" in lower or "radeon" in lower:
        return "amd"
    if "intel" in lower:
        return "intel"
    return "unknown"


def _get_windows_video_controllers() -> List[Dict[str, str]]:
    ps_cmd = (
        "Get-CimInstance Win32_VideoController | "
        "Select-Object Name, DriverVersion, AdapterCompatibility | ConvertTo-Json"
    )
    output = _run_command(["powershell", "-Command", ps_cmd], timeout=10)
    if not output:
        return []
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return []
    if isinstance(data, dict):
        return [data]
    return data


def _get_linux_gpu_lines() -> List[str]:
    output = _run_command(["lspci"], timeout=10)
    if not output:
        return []
    lines = []
    for line in output.splitlines():
        if "VGA" in line or "3D controller" in line or "Display" in line:
            lines.append(line.strip())
    return lines


def get_nvidia_info() -> List[Dict[str, str]]:
    try:
        import GPUtil

        gpus = GPUtil.getGPUs()
        info = []
        for gpu in gpus:
            info.append(
                {
                    "name": gpu.name,
                    "driver": gpu.driver,
                    "memory_total": f"{gpu.memoryTotal} MB",
                    "memory_used": f"{gpu.memoryUsed} MB",
                    "memory_free": f"{gpu.memoryFree} MB",
                    "load": f"{gpu.load * 100:.1f}%",
                    "temperature": f"{gpu.temperature} C",
                }
            )
        if info:
            return info
    except ImportError:
        pass

    if shutil.which("nvidia-smi"):
        query = "name,driver_version,memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu"
        cmd = [
            "nvidia-smi",
            f"--query-gpu={query}",
            "--format=csv,noheader,nounits",
        ]
        output = _run_command(cmd, timeout=10)
        info = []
        for line in output.splitlines():
            parts = [p.strip() for p in line.split(",")]
            if len(parts) == 7:
                info.append(
                    {
                        "name": parts[0],
                        "driver": parts[1],
                        "memory_total": f"{parts[2]} MB",
                        "memory_used": f"{parts[3]} MB",
                        "memory_free": f"{parts[4]} MB",
                        "load": f"{parts[5]}%",
                        "temperature": f"{parts[6]} C",
                    }
                )
        return info

    return []


def get_amd_info() -> List[Dict[str, str]]:
    if platform.system() == "Windows":
        info = []
        for adapter in _get_windows_video_controllers():
            name = adapter.get("Name", "")
            vendor = adapter.get("AdapterCompatibility", "")
            if "amd" in name.lower() or "radeon" in name.lower() or "advanced micro devices" in vendor.lower():
                info.append(
                    {
                        "name": name,
                        "driver": adapter.get("DriverVersion", ""),
                        "vendor": vendor,
                    }
                )
        return info

    if shutil.which("rocm-smi"):
        output = _run_command(["rocm-smi", "--showproductname", "--showdriverversion"], timeout=10)
        if output:
            return [{"name": "AMD GPU", "driver": "", "details": output}]

    info = []
    for line in _get_linux_gpu_lines():
        if "amd" in line.lower() or "radeon" in line.lower():
            info.append({"name": line, "driver": ""})
    return info


def get_intel_info() -> List[Dict[str, str]]:
    if platform.system() == "Windows":
        info = []
        for adapter in _get_windows_video_controllers():
            name = adapter.get("Name", "")
            vendor = adapter.get("AdapterCompatibility", "")
            if "intel" in name.lower() or "intel" in vendor.lower():
                info.append(
                    {
                        "name": name,
                        "driver": adapter.get("DriverVersion", ""),
                        "vendor": vendor,
                    }
                )
        return info

    info = []
    for line in _get_linux_gpu_lines():
        if "intel" in line.lower():
            info.append({"name": line, "driver": ""})
    return info


def get_all_gpus() -> List[Dict[str, str]]:
    results = []
    system = platform.system()
    if system == "Windows":
        for adapter in _get_windows_video_controllers():
            name = adapter.get("Name", "")
            results.append(
                {
                    "name": name,
                    "vendor": detect_gpu_vendor(name),
                    "driver": adapter.get("DriverVersion", ""),
                }
            )
        return results

    if system == "Linux":
        for line in _get_linux_gpu_lines():
            results.append({"name": line, "vendor": detect_gpu_vendor(line), "driver": ""})
        return results

    if system == "Darwin":
        output = _run_command(["system_profiler", "SPDisplaysDataType"], timeout=10)
        for line in output.splitlines():
            if "Chipset Model" in line:
                name = line.split(":", 1)[-1].strip()
                results.append({"name": name, "vendor": detect_gpu_vendor(name), "driver": ""})
        return results

    return results


def run() -> str:
    output = []
    output.append("=" * 60)
    output.append("GPU DIAGNOSTICS")
    output.append("=" * 60)
    output.append("")

    output.append("--- Detected GPUs ---")
    gpus = get_all_gpus()
    if not gpus:
        output.append("No GPUs detected")
    else:
        for gpu in gpus:
            vendor = gpu.get("vendor", "unknown")
            driver = gpu.get("driver", "")
            driver_text = f" (Driver: {driver})" if driver else ""
            output.append(f"- {gpu.get('name', 'Unknown')} [{vendor}]{driver_text}")

    output.append("")
    output.append("--- NVIDIA Details ---")
    nvidia_info = get_nvidia_info()
    if not nvidia_info:
        output.append("No NVIDIA details available")
    else:
        for info in nvidia_info:
            output.append(f"GPU: {info.get('name', 'Unknown')}")
            output.append(f"  Driver: {info.get('driver', '')}")
            output.append(f"  Memory Total: {info.get('memory_total', '')}")
            output.append(f"  Memory Used: {info.get('memory_used', '')}")
            output.append(f"  Memory Free: {info.get('memory_free', '')}")
            output.append(f"  GPU Load: {info.get('load', '')}")
            output.append(f"  Temperature: {info.get('temperature', '')}")

    output.append("")
    output.append("--- AMD Details ---")
    amd_info = get_amd_info()
    if not amd_info:
        output.append("No AMD details available")
    else:
        for info in amd_info:
            output.append(f"GPU: {info.get('name', 'Unknown')}")
            if info.get("driver"):
                output.append(f"  Driver: {info.get('driver')}")
            if info.get("details"):
                output.append(info.get("details"))

    output.append("")
    output.append("--- Intel Details ---")
    intel_info = get_intel_info()
    if not intel_info:
        output.append("No Intel details available")
    else:
        for info in intel_info:
            output.append(f"GPU: {info.get('name', 'Unknown')}")
            if info.get("driver"):
                output.append(f"  Driver: {info.get('driver')}")

    output.append("")
    output.append("=" * 60)
    output.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("=" * 60)

    return "\n".join(output)

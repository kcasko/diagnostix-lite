"""
GPU Diagnostics - Identify GPU and driver state
"""
import platform
import subprocess
from datetime import datetime


def run() -> str:
    output = []
    output.append("=" * 60)
    output.append("GPU DIAGNOSTICS")
    output.append("=" * 60)
    output.append("")
    
    output.append("--- NVIDIA GPU Detection ---")
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        
        if gpus:
            for i, gpu in enumerate(gpus):
                output.append("")
                output.append(f"GPU {i}: {gpu.name}")
                output.append(f"  Driver: {gpu.driver}")
                output.append(f"  Memory Total: {gpu.memoryTotal} MB")
                output.append(f"  Memory Used: {gpu.memoryUsed} MB")
                output.append(f"  Memory Free: {gpu.memoryFree} MB")
                output.append(f"  GPU Load: {gpu.load * 100:.1f}%")
                output.append(f"  Temperature: {gpu.temperature}C")
                
                if gpu.temperature > 85:
                    output.append("  STATUS: WARNING - High temperature")
                else:
                    output.append("  STATUS: OK")
        else:
            output.append("No NVIDIA GPUs detected")
    except ImportError:
        output.append("GPUtil not installed - NVIDIA GPU detection unavailable")
        output.append("Install with: pip install gputil")
    except Exception as e:
        output.append(f"Error detecting NVIDIA GPUs: {e}")
    
    output.append("")
    output.append("")
    output.append("--- System GPU Information ---")
    try:
        if platform.system() == "Windows":
            # Try wmic first (deprecated but common)
            try:
                result = subprocess.run(
                    ["wmic", "path", "win32_VideoController", "get", "name,driverversion"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    output.append(result.stdout)
                else:
                    raise FileNotFoundError("wmic failed")
            except (FileNotFoundError, subprocess.SubprocessError):
                # Fallback to PowerShell (modern Windows)
                ps_cmd = "Get-CimInstance Win32_VideoController | Select-Object Name, DriverVersion | Format-Table -AutoSize"
                result = subprocess.run(
                    ["powershell", "-Command", ps_cmd],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                output.append(result.stdout)
        elif platform.system() == "Linux":
            try:
                result = subprocess.run(
                    ["lspci"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                lines = result.stdout.split("\n")
                for line in lines:
                    if "VGA" in line or "3D controller" in line or "Display" in line:
                        output.append(line)
            except FileNotFoundError:
                output.append("lspci not found - Install pciutils for GPU detection")
        elif platform.system() == "Darwin":
            result = subprocess.run(
                ["system_profiler", "SPDisplaysDataType"],
                capture_output=True,
                text=True,
                timeout=10
            )
            output.append(result.stdout)
    except Exception as e:
        output.append(f"Error getting system GPU info: {e}")
    
    output.append("")
    output.append("=" * 60)
    output.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("=" * 60)
    
    return "\n".join(output)

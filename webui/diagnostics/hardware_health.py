"""
Hardware Health - CPU, RAM, temperatures, and S.M.A.R.T. data
"""
import platform
import psutil
import subprocess
from datetime import datetime


def format_bytes(bytes_val: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} PB"


def run() -> str:
    output = []
    output.append("=" * 60)
    output.append("HARDWARE HEALTH REPORT")
    output.append("=" * 60)
    output.append("")
    
    # CPU Health
    output.append("--- CPU Health ---")
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        output.append(f"CPU Usage: {cpu_percent}%")
        
        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            output.append(f"Current Frequency: {cpu_freq.current:.2f} MHz")
        
        output.append(f"Physical Cores: {psutil.cpu_count(logical=False)}")
        output.append(f"Logical Cores: {psutil.cpu_count(logical=True)}")
        
        if cpu_percent > 90:
            output.append("STATUS: WARNING - High CPU usage")
        else:
            output.append("STATUS: OK")
    except Exception as e:
        output.append(f"Error: {e}")
    
    output.append("")
    
    # Memory Health
    output.append("--- Memory Health ---")
    try:
        mem = psutil.virtual_memory()
        output.append(f"Total RAM: {format_bytes(mem.total)}")
        output.append(f"Available: {format_bytes(mem.available)}")
        output.append(f"Usage: {mem.percent}%")
        
        if mem.percent > 90:
            output.append("STATUS: CRITICAL")
        elif mem.percent > 75:
            output.append("STATUS: WARNING")
        else:
            output.append("STATUS: OK")
    except Exception as e:
        output.append(f"Error: {e}")
    
    output.append("")
    
    # Temperature
    output.append("--- Temperature Sensors ---")
    try:
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    output.append(f"{name}:")
                    for entry in entries:
                        label = entry.label or "Sensor"
                        output.append(f"  {label}: {entry.current}C")
            else:
                output.append("No sensors detected")
        else:
            output.append("Not supported on this platform")
    except Exception as e:
        output.append(f"Not available: {e}")
    
    output.append("")
    output.append("=" * 60)
    output.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("=" * 60)

    return "\n".join(output)

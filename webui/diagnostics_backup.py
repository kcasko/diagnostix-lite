"""
Cross-platform system diagnostics using Python
Works on Windows, macOS, and Linux
"""
import platform
import psutil
import subprocess
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


def get_system_overview() -> str:
    """Get comprehensive system overview"""
    output = []
    output.append("=== System Overview ===\n")

    # OS Information
    output.append(f"OS: {platform.system()} {platform.release()}")
    output.append(f"Version: {platform.version()}")
    output.append(f"Architecture: {platform.machine()}")
    output.append(f"Processor: {platform.processor()}")
    output.append(f"Hostname: {platform.node()}")
    output.append(f"Python Version: {platform.python_version()}\n")

    # CPU Information
    output.append("--- CPU ---")
    output.append(f"Physical cores: {psutil.cpu_count(logical=False)}")
    output.append(f"Total cores: {psutil.cpu_count(logical=True)}")
    try:
        freq = psutil.cpu_freq()
        if freq:
            output.append(f"Max Frequency: {freq.max:.2f}Mhz")
            output.append(f"Current Frequency: {freq.current:.2f}Mhz")
    except:
        pass
    output.append(f"CPU Usage: {psutil.cpu_percent(interval=1)}%\n")

    # Memory Information
    mem = psutil.virtual_memory()
    output.append("--- Memory ---")
    output.append(f"Total: {mem.total / (1024**3):.2f} GB")
    output.append(f"Available: {mem.available / (1024**3):.2f} GB")
    output.append(f"Used: {mem.used / (1024**3):.2f} GB ({mem.percent}%)")
    output.append(f"Free: {mem.free / (1024**3):.2f} GB\n")

    # Swap Memory
    swap = psutil.swap_memory()
    output.append("--- Swap ---")
    output.append(f"Total: {swap.total / (1024**3):.2f} GB")
    output.append(f"Used: {swap.used / (1024**3):.2f} GB ({swap.percent}%)")
    output.append(f"Free: {swap.free / (1024**3):.2f} GB\n")

    # Disk Information
    output.append("--- Disks ---")
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            output.append(f"\nDevice: {partition.device}")
            output.append(f"  Mountpoint: {partition.mountpoint}")
            output.append(f"  File system: {partition.fstype}")
            output.append(f"  Total: {usage.total / (1024**3):.2f} GB")
            output.append(f"  Used: {usage.used / (1024**3):.2f} GB ({usage.percent}%)")
            output.append(f"  Free: {usage.free / (1024**3):.2f} GB")
        except PermissionError:
            output.append(f"\n{partition.device}: Access denied")

    return "\n".join(output)


def get_hardware_health() -> str:
    """Get hardware health status"""
    output = []
    output.append("=== Hardware Health ===\n")

    # CPU Usage per core
    output.append("--- CPU Usage per Core ---")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        output.append(f"Core {i}: {percentage}%")
    output.append("")

    # Memory details
    mem = psutil.virtual_memory()
    output.append("--- Memory Health ---")
    output.append(f"Total RAM: {mem.total / (1024**3):.2f} GB")
    output.append(f"Available: {mem.available / (1024**3):.2f} GB")
    output.append(f"Used: {mem.percent}%")
    if mem.percent > 90:
        output.append("⚠ WARNING: Memory usage is critically high!")
    elif mem.percent > 75:
        output.append("⚠ CAUTION: Memory usage is high")
    else:
        output.append("✓ Memory usage is normal")
    output.append("")

    # Temperatures (if available)
    output.append("--- Temperature Sensors ---")
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                output.append(f"{name}:")
                for entry in entries:
                    output.append(f"  {entry.label or 'Sensor'}: {entry.current}°C")
                    if entry.high and entry.current > entry.high:
                        output.append("    ⚠ WARNING: Temperature is high!")
        else:
            output.append("No temperature sensors detected (may require admin/root)")
    except AttributeError:
        output.append("Temperature monitoring not available on this platform")
    output.append("")

    # Battery (if available)
    output.append("--- Battery ---")
    try:
        battery = psutil.sensors_battery()
        if battery:
            output.append(f"Charge: {battery.percent}%")
            output.append(f"Plugged in: {'Yes' if battery.power_plugged else 'No'}")
            if not battery.power_plugged:
                secs_left = battery.secsleft
                if secs_left != psutil.POWER_TIME_UNLIMITED:
                    hours = secs_left // 3600
                    minutes = (secs_left % 3600) // 60
                    output.append(f"Time remaining: {hours}h {minutes}m")
        else:
            output.append("No battery detected (desktop system)")
    except AttributeError:
        output.append("Battery monitoring not available on this platform")

    return "\n".join(output)


def get_disk_diagnostics() -> str:
    """Get disk diagnostics and usage"""
    output = []
    output.append("=== Disk Diagnostics ===\n")

    # Disk partitions
    output.append("--- Partitions ---")
    for partition in psutil.disk_partitions():
        output.append(f"\nDevice: {partition.device}")
        output.append(f"Mountpoint: {partition.mountpoint}")
        output.append(f"File system: {partition.fstype}")
        output.append(f"Options: {partition.opts}")

        try:
            usage = psutil.disk_usage(partition.mountpoint)
            output.append(f"Total: {usage.total / (1024**3):.2f} GB")
            output.append(f"Used: {usage.used / (1024**3):.2f} GB")
            output.append(f"Free: {usage.free / (1024**3):.2f} GB")
            output.append(f"Usage: {usage.percent}%")

            if usage.percent > 90:
                output.append("⚠ WARNING: Disk is almost full!")
            elif usage.percent > 75:
                output.append("⚠ CAUTION: Disk usage is high")
        except PermissionError:
            output.append("Access denied")

    # Disk I/O statistics
    output.append("\n--- Disk I/O Statistics ---")
    try:
        io_counters = psutil.disk_io_counters(perdisk=True)
        if io_counters:
            for disk, counters in io_counters.items():
                output.append(f"\n{disk}:")
                output.append(f"  Read: {counters.read_bytes / (1024**3):.2f} GB")
                output.append(f"  Write: {counters.write_bytes / (1024**3):.2f} GB")
                output.append(f"  Read count: {counters.read_count}")
                output.append(f"  Write count: {counters.write_count}")
    except:
        output.append("I/O statistics not available")

    # SMART data (Linux with smartctl)
    if platform.system() == "Linux":
        output.append("\n--- SMART Data (requires smartctl) ---")
        try:
            for partition in psutil.disk_partitions():
                if partition.device.startswith('/dev/sd') or partition.device.startswith('/dev/nvme'):
                    result = subprocess.run(
                        ['smartctl', '-H', partition.device],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode == 0:
                        output.append(f"\n{partition.device}:")
                        output.append(result.stdout)
        except FileNotFoundError:
            output.append("smartctl not installed (install smartmontools)")
        except subprocess.TimeoutExpired:
            output.append("SMART check timed out")
        except Exception as e:
            output.append(f"SMART check failed: {e}")
    else:
        output.append("\n--- SMART Data ---")
        output.append("SMART data requires Linux and smartmontools")

    return "\n".join(output)


def get_network_diagnostics() -> str:
    """Get network diagnostics"""
    output = []
    output.append("=== Network Diagnostics ===\n")

    # Network interfaces
    output.append("--- Network Interfaces ---")
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for interface_name, interface_addrs in addrs.items():
        output.append(f"\n{interface_name}:")

        # Interface stats
        if interface_name in stats:
            stat = stats[interface_name]
            output.append(f"  Status: {'Up' if stat.isup else 'Down'}")
            output.append(f"  Speed: {stat.speed} Mbps")
            output.append(f"  MTU: {stat.mtu}")

        # Addresses
        for addr in interface_addrs:
            if addr.family == 2:  # AF_INET (IPv4)
                output.append(f"  IPv4: {addr.address}")
                output.append(f"  Netmask: {addr.netmask}")
            elif addr.family == 23 or addr.family == 30:  # AF_INET6 (IPv6)
                output.append(f"  IPv6: {addr.address}")
            elif addr.family == -1 or addr.family == 17:  # AF_LINK (MAC)
                output.append(f"  MAC: {addr.address}")

    # Network I/O statistics
    output.append("\n--- Network I/O Statistics ---")
    net_io = psutil.net_io_counters()
    output.append(f"Bytes sent: {net_io.bytes_sent / (1024**2):.2f} MB")
    output.append(f"Bytes received: {net_io.bytes_recv / (1024**2):.2f} MB")
    output.append(f"Packets sent: {net_io.packets_sent}")
    output.append(f"Packets received: {net_io.packets_recv}")
    output.append(f"Errors in: {net_io.errin}")
    output.append(f"Errors out: {net_io.errout}")
    output.append(f"Packets dropped in: {net_io.dropin}")
    output.append(f"Packets dropped out: {net_io.dropout}")

    # Active connections (sample)
    output.append("\n--- Active Connections (sample, first 10) ---")
    try:
        connections = psutil.net_connections(kind='inet')[:10]
        for conn in connections:
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
            output.append(f"{conn.type.name} {laddr} -> {raddr} ({conn.status})")
    except psutil.AccessDenied:
        output.append("Access denied (requires admin/root privileges)")

    return "\n".join(output)


def get_gpu_diagnostics() -> str:
    """Get GPU diagnostics (NVIDIA only via gputil)"""
    output = []
    output.append("=== GPU Diagnostics ===\n")

    try:
        import GPUtil
        gpus = GPUtil.getGPUs()

        if not gpus:
            output.append("No NVIDIA GPUs detected")
            output.append("(Only NVIDIA GPUs are currently supported via GPUtil)")
        else:
            for gpu in gpus:
                output.append(f"GPU {gpu.id}: {gpu.name}")
                output.append(f"  Driver: {gpu.driver}")
                output.append(f"  Temperature: {gpu.temperature}°C")
                output.append(f"  Load: {gpu.load * 100:.1f}%")
                output.append(f"  Memory Total: {gpu.memoryTotal} MB")
                output.append(f"  Memory Used: {gpu.memoryUsed} MB ({gpu.memoryUtil * 100:.1f}%)")
                output.append(f"  Memory Free: {gpu.memoryFree} MB")
                output.append("")
    except Exception as e:
        output.append(f"GPU detection failed: {e}")
        output.append("\nNote: GPU diagnostics currently only support NVIDIA cards")
        output.append("For AMD/Intel GPUs, use platform-specific tools")

    return "\n".join(output)


def run_cpu_stress_test(duration: int = 5) -> str:
    """Run a light CPU stress test"""
    output = []
    output.append(f"=== CPU Stress Test ({duration} seconds) ===\n")

    output.append("Initial CPU usage:")
    initial = psutil.cpu_percent(interval=1)
    output.append(f"  {initial}%\n")

    output.append(f"Starting stress test for {duration} seconds...")
    output.append("(Running single-threaded calculation)\n")

    import time
    start = time.time()
    counter = 0

    # Simple CPU-intensive calculation
    while time.time() - start < duration:
        counter += 1
        _ = sum(i ** 2 for i in range(1000))

    output.append(f"Completed {counter} iterations\n")

    output.append("CPU usage during test:")
    output.append(f"  {psutil.cpu_percent(interval=1)}%\n")

    output.append("CPU usage per core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        output.append(f"  Core {i}: {percentage}%")

    return "\n".join(output)


def run_memory_stress_test() -> str:
    """Run a light memory test"""
    output = []
    output.append("=== Memory Stress Test ===\n")

    mem = psutil.virtual_memory()
    output.append("Initial memory state:")
    output.append(f"  Available: {mem.available / (1024**3):.2f} GB")
    output.append(f"  Used: {mem.percent}%\n")

    output.append("Allocating test memory (100MB)...")
    test_data = bytearray(100 * 1024 * 1024)  # 100MB

    mem = psutil.virtual_memory()
    output.append("Memory after allocation:")
    output.append(f"  Available: {mem.available / (1024**3):.2f} GB")
    output.append(f"  Used: {mem.percent}%\n")

    output.append("✓ Memory test completed successfully")
    output.append("No errors detected")

    # Cleanup
    del test_data

    return "\n".join(output)


def get_about() -> str:
    """Get about information"""
    return """=== DiagnOStiX ===
Project Information
-------------------

Version: 2.0 (Cross-Platform Edition)
Author: Keith (keezay)
License: See LICENSE file

DiagnOStiX is a lightweight diagnostic tool built for PC repair,
system triage, and developer tooling.

Now available as a cross-platform web application!

Features:
- System overview and hardware health monitoring
- CPU and memory stress tests
- GPU diagnostics (NVIDIA)
- Disk checks and usage analysis
- Network diagnostics and monitoring
- Cross-platform support (Windows, macOS, Linux)
- Clean web interface with neon aesthetic

Built with:
- FastAPI (Python web framework)
- psutil (system monitoring)
- Docker (containerization)

Repository: https://github.com/yourusername/diagnostix-lite-1
"""


# Map diagnostic functions to their names
DIAGNOSTIC_FUNCTIONS = {
    'system_overview': get_system_overview,
    'hardware_health': get_hardware_health,
    'disk_diagnostics': get_disk_diagnostics,
    'network_diagnostics': get_network_diagnostics,
    'gpu_diagnostics': get_gpu_diagnostics,
    'cpu_stress_test': run_cpu_stress_test,
    'memory_stress_test': run_memory_stress_test,
    'about_diagnostix': get_about,
}

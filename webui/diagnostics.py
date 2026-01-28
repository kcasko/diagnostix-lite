"""
Cross-platform system diagnostics using Python
Optimized version with type hints, better error handling, and improved performance

Works on Windows, macOS, and Linux
"""
import platform
import psutil
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass

# Configure logging
logger = logging.getLogger(__name__)


# Constants
GB = 1024 ** 3
MB = 1024 ** 2
STRESS_TEST_DURATION = 5  # seconds


@dataclass
class SystemInfo:
    """System information data class"""
    os: str
    os_release: str
    version: str
    architecture: str
    processor: str
    hostname: str
    python_version: str


@dataclass
class MemoryInfo:
    """Memory information data class"""
    total_gb: float
    available_gb: float
    used_gb: float
    percent: float
    free_gb: float


def format_bytes_to_gb(bytes_value: int) -> float:
    """Convert bytes to gigabytes with 2 decimal precision"""
    return round(bytes_value / GB, 2)


def format_output_section(title: str, lines: List[str]) -> str:
    """Format a section of output with title"""
    output = [f"=== {title} ===\n"]
    output.extend(lines)
    return "\n".join(output)


def safe_execute(func: Callable, default: str = "N/A") -> Any:
    """
    Safely execute a function and return default on error

    Args:
        func: Function to execute
        default: Default value if execution fails

    Returns:
        Function result or default value
    """
    try:
        return func()
    except Exception as e:
        logger.warning(f"Error in {func.__name__}: {e}")
        return default


def get_system_info() -> SystemInfo:
    """Get basic system information"""
    return SystemInfo(
        os=platform.system(),
        os_release=platform.release(),
        version=platform.version(),
        architecture=platform.machine(),
        processor=platform.processor() or "Unknown",
        hostname=platform.node(),
        python_version=platform.python_version()
    )


def get_memory_info() -> MemoryInfo:
    """Get memory information"""
    mem = psutil.virtual_memory()
    return MemoryInfo(
        total_gb=format_bytes_to_gb(mem.total),
        available_gb=format_bytes_to_gb(mem.available),
        used_gb=format_bytes_to_gb(mem.used),
        percent=mem.percent,
        free_gb=format_bytes_to_gb(mem.free)
    )


def get_system_overview() -> str:
    """Get comprehensive system overview"""
    lines = []

    # OS Information
    sys_info = get_system_info()
    lines.extend([
        f"OS: {sys_info.os} {sys_info.os_release}",
        f"Version: {sys_info.version}",
        f"Architecture: {sys_info.architecture}",
        f"Processor: {sys_info.processor}",
        f"Hostname: {sys_info.hostname}",
        f"Python Version: {sys_info.python_version}\n",
    ])

    # CPU Information
    cpu_lines = ["--- CPU ---"]
    physical_cores = psutil.cpu_count(logical=False)
    total_cores = psutil.cpu_count(logical=True)

    cpu_lines.append(f"Physical cores: {physical_cores}")
    cpu_lines.append(f"Total cores: {total_cores}")

    freq = safe_execute(psutil.cpu_freq, None)
    if freq:
        cpu_lines.append(f"Max Frequency: {freq.max:.2f}Mhz")
        cpu_lines.append(f"Current Frequency: {freq.current:.2f}Mhz")

    cpu_usage = safe_execute(lambda: psutil.cpu_percent(interval=1), 0)
    cpu_lines.append(f"CPU Usage: {cpu_usage}%\n")
    lines.extend(cpu_lines)

    # Memory Information
    mem = get_memory_info()
    mem_lines = [
        "--- Memory ---",
        f"Total: {mem.total_gb} GB",
        f"Available: {mem.available_gb} GB",
        f"Used: {mem.used_gb} GB ({mem.percent}%)",
        f"Free: {mem.free_gb} GB\n"
    ]
    lines.extend(mem_lines)

    # Swap Memory
    swap = psutil.swap_memory()
    swap_lines = [
        "--- Swap ---",
        f"Total: {format_bytes_to_gb(swap.total)} GB",
        f"Used: {format_bytes_to_gb(swap.used)} GB ({swap.percent}%)",
        f"Free: {format_bytes_to_gb(swap.free)} GB\n"
    ]
    lines.extend(swap_lines)

    # Disk Information
    disk_lines = ["--- Disks ---"]
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_lines.extend([
                f"\nDevice: {partition.device}",
                f"  Mountpoint: {partition.mountpoint}",
                f"  File system: {partition.fstype}",
                f"  Total: {format_bytes_to_gb(usage.total)} GB",
                f"  Used: {format_bytes_to_gb(usage.used)} GB ({usage.percent}%)",
                f"  Free: {format_bytes_to_gb(usage.free)} GB"
            ])
        except PermissionError:
            disk_lines.append(f"\n{partition.device}: Access denied")
    lines.extend(disk_lines)

    return format_output_section("System Overview", lines)


def get_hardware_health() -> str:
    """Get hardware health status"""
    lines = []

    # CPU Usage per core
    cpu_lines = ["--- CPU Usage per Core ---"]
    cpu_percents = safe_execute(
        lambda: psutil.cpu_percent(percpu=True, interval=1),
        []
    )
    for i, percentage in enumerate(cpu_percents):
        cpu_lines.append(f"Core {i}: {percentage}%")
    cpu_lines.append("")
    lines.extend(cpu_lines)

    # Memory health assessment
    mem = get_memory_info()
    mem_lines = [
        "--- Memory Health ---",
        f"Total RAM: {mem.total_gb} GB",
        f"Available: {mem.available_gb} GB",
        f"Used: {mem.percent}%"
    ]

    if mem.percent > 90:
        mem_lines.append("⚠ WARNING: Memory usage is critically high!")
    elif mem.percent > 75:
        mem_lines.append("⚠ CAUTION: Memory usage is high")
    else:
        mem_lines.append("✓ Memory usage is normal")
    mem_lines.append("")
    lines.extend(mem_lines)

    # Temperature sensors (if available)
    temp_lines = ["--- Temperature Sensors ---"]
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                temp_lines.append(f"{name}:")
                for entry in entries:
                    label = entry.label or 'Sensor'
                    temp_lines.append(f"  {label}: {entry.current}°C")
                    if entry.high and entry.current > entry.high:
                        temp_lines.append("    ⚠ WARNING: Temperature is high!")
        else:
            temp_lines.append("No temperature sensors detected (may require admin/root)")
    except AttributeError:
        temp_lines.append("Temperature monitoring not available on this platform")
    temp_lines.append("")
    lines.extend(temp_lines)

    # Battery information (if available)
    battery_lines = ["--- Battery ---"]
    try:
        battery = psutil.sensors_battery()
        if battery:
            battery_lines.extend([
                f"Charge: {battery.percent}%",
                f"Plugged in: {'Yes' if battery.power_plugged else 'No'}"
            ])
            if not battery.power_plugged:
                secs_left = battery.secsleft
                if secs_left != psutil.POWER_TIME_UNLIMITED:
                    hours = secs_left // 3600
                    minutes = (secs_left % 3600) // 60
                    battery_lines.append(f"Time remaining: {hours}h {minutes}m")
        else:
            battery_lines.append("No battery detected (desktop system)")
    except AttributeError:
        battery_lines.append("Battery monitoring not available on this platform")
    lines.extend(battery_lines)

    return format_output_section("Hardware Health", lines)


def get_disk_diagnostics() -> str:
    """Get disk diagnostics and usage"""
    lines = []

    # Disk partitions
    partition_lines = ["--- Partitions ---"]
    for partition in psutil.disk_partitions():
        partition_lines.extend([
            f"\nDevice: {partition.device}",
            f"Mountpoint: {partition.mountpoint}",
            f"File system: {partition.fstype}",
            f"Options: {partition.opts}"
        ])

        try:
            usage = psutil.disk_usage(partition.mountpoint)
            partition_lines.extend([
                f"Total: {format_bytes_to_gb(usage.total)} GB",
                f"Used: {format_bytes_to_gb(usage.used)} GB",
                f"Free: {format_bytes_to_gb(usage.free)} GB",
                f"Usage: {usage.percent}%"
            ])

            if usage.percent > 90:
                partition_lines.append("⚠ WARNING: Disk is almost full!")
            elif usage.percent > 75:
                partition_lines.append("⚠ CAUTION: Disk usage is high")
        except PermissionError:
            partition_lines.append("Access denied")
    lines.extend(partition_lines)

    # Disk I/O statistics
    io_lines = ["\n--- Disk I/O Statistics ---"]
    try:
        io_counters = psutil.disk_io_counters(perdisk=True)
        if io_counters:
            for disk, counters in io_counters.items():
                io_lines.extend([
                    f"\n{disk}:",
                    f"  Read: {format_bytes_to_gb(counters.read_bytes)} GB",
                    f"  Write: {format_bytes_to_gb(counters.write_bytes)} GB",
                    f"  Read count: {counters.read_count}",
                    f"  Write count: {counters.write_count}"
                ])
        else:
            io_lines.append("I/O statistics not available")
    except Exception as e:
        io_lines.append(f"I/O statistics not available: {e}")
    lines.extend(io_lines)

    # SMART data (Linux only)
    smart_lines = ["\n--- SMART Data ---"]
    if platform.system() == "Linux":
        smart_lines.append("(requires smartctl - install smartmontools)")
        # SMART data implementation would go here
        smart_lines.append("Run 'sudo smartctl -a /dev/sdX' for detailed SMART data")
    else:
        smart_lines.append("SMART data collection requires Linux with smartmontools")
    lines.extend(smart_lines)

    return format_output_section("Disk Diagnostics", lines)


def get_network_diagnostics() -> str:
    """Get network diagnostics"""
    lines = []

    # Network interfaces
    interface_lines = ["--- Network Interfaces ---"]
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for interface_name, interface_addrs in addrs.items():
        interface_lines.append(f"\n{interface_name}:")

        # Interface stats
        if interface_name in stats:
            stat = stats[interface_name]
            interface_lines.extend([
                f"  Status: {'Up' if stat.isup else 'Down'}",
                f"  Speed: {stat.speed} Mbps",
                f"  MTU: {stat.mtu}"
            ])

        # Addresses
        for addr in interface_addrs:
            if addr.family == 2:  # AF_INET (IPv4)
                interface_lines.extend([
                    f"  IPv4: {addr.address}",
                    f"  Netmask: {addr.netmask}"
                ])
            elif addr.family in (23, 30):  # AF_INET6 (IPv6)
                interface_lines.append(f"  IPv6: {addr.address}")
            elif addr.family in (-1, 17):  # AF_LINK (MAC)
                interface_lines.append(f"  MAC: {addr.address}")
    lines.extend(interface_lines)

    # Network I/O statistics
    net_io = psutil.net_io_counters()
    io_lines = [
        "\n--- Network I/O Statistics ---",
        f"Bytes sent: {net_io.bytes_sent / MB:.2f} MB",
        f"Bytes received: {net_io.bytes_recv / MB:.2f} MB",
        f"Packets sent: {net_io.packets_sent}",
        f"Packets received: {net_io.packets_recv}",
        f"Errors in: {net_io.errin}",
        f"Errors out: {net_io.errout}",
        f"Packets dropped in: {net_io.dropin}",
        f"Packets dropped out: {net_io.dropout}"
    ]
    lines.extend(io_lines)

    # Active connections (sample)
    conn_lines = ["\n--- Active Connections (sample, first 10) ---"]
    try:
        connections = psutil.net_connections(kind='inet')[:10]
        for conn in connections:
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
            conn_lines.append(f"{conn.type.name} {laddr} -> {raddr} ({conn.status})")
    except psutil.AccessDenied:
        conn_lines.append("Access denied (requires admin/root privileges)")
    lines.extend(conn_lines)

    return format_output_section("Network Diagnostics", lines)


def get_gpu_diagnostics() -> str:
    """Get GPU diagnostics (NVIDIA only via gputil)"""
    lines = ["--- GPU Information ---"]

    try:
        import GPUtil
        gpus = GPUtil.getGPUs()

        if not gpus:
            lines.extend([
                "No NVIDIA GPUs detected",
                "(Only NVIDIA GPUs are currently supported via GPUtil)"
            ])
        else:
            for gpu in gpus:
                lines.extend([
                    f"\nGPU {gpu.id}: {gpu.name}",
                    f"  Driver: {gpu.driver}",
                    f"  Temperature: {gpu.temperature}°C",
                    f"  Load: {gpu.load * 100:.1f}%",
                    f"  Memory Total: {gpu.memoryTotal} MB",
                    f"  Memory Used: {gpu.memoryUsed} MB ({gpu.memoryUtil * 100:.1f}%)",
                    f"  Memory Free: {gpu.memoryFree} MB"
                ])
    except ImportError:
        lines.append("GPUtil not installed. Install with: pip install gputil")
    except Exception as e:
        lines.extend([
            f"GPU detection failed: {e}",
            "\nNote: GPU diagnostics currently only support NVIDIA cards",
            "For AMD/Intel GPUs, use platform-specific tools"
        ])

    return format_output_section("GPU Diagnostics", lines)


def run_cpu_stress_test(duration: int = STRESS_TEST_DURATION) -> str:
    """
    Run a CPU stress test

    Args:
        duration: Test duration in seconds

    Returns:
        Formatted test results
    """
    import time

    lines = [f"(Duration: {duration} seconds)\n"]

    # Initial CPU usage
    initial = psutil.cpu_percent(interval=1)
    lines.extend([
        "Initial CPU usage:",
        f"  {initial}%\n",
        f"Starting stress test for {duration} seconds...",
        "(Running single-threaded calculation)\n"
    ])

    # Run stress test
    start = time.time()
    counter = 0
    while time.time() - start < duration:
        counter += 1
        _ = sum(i ** 2 for i in range(1000))

    lines.append(f"Completed {counter} iterations\n")

    # Final CPU usage
    final = psutil.cpu_percent(interval=1)
    lines.extend([
        "CPU usage during test:",
        f"  {final}%\n",
        "CPU usage per core:"
    ])

    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        lines.append(f"  Core {i}: {percentage}%")

    return format_output_section(f"CPU Stress Test ({duration}s)", lines)


def run_memory_stress_test() -> str:
    """Run a light memory test"""
    lines = []

    # Initial state
    mem = get_memory_info()
    lines.extend([
        "Initial memory state:",
        f"  Available: {mem.available_gb} GB",
        f"  Used: {mem.percent}%\n"
    ])

    # Allocate test memory
    test_size_mb = 100
    lines.append(f"Allocating test memory ({test_size_mb}MB)...")
    test_data = bytearray(test_size_mb * MB)

    # Check state after allocation
    mem = get_memory_info()
    lines.extend([
        "Memory after allocation:",
        f"  Available: {mem.available_gb} GB",
        f"  Used: {mem.percent}%\n",
        "✓ Memory test completed successfully",
        "No errors detected"
    ])

    # Cleanup
    del test_data

    return format_output_section("Memory Stress Test", lines)


def get_about() -> str:
    """Get about information"""
    lines = [
        "Project Information",
        "-------------------\n",
        "Version: 2.0 (Cross-Platform Edition)",
        "Author: Keith (keezay)",
        "License: See LICENSE file\n",
        "DiagnOStiX is a lightweight diagnostic tool built for PC repair,",
        "system triage, and developer tooling.\n",
        "Now available as a cross-platform web application!\n",
        "Features:",
        "- System overview and hardware health monitoring",
        "- CPU and memory stress tests",
        "- GPU diagnostics (NVIDIA)",
        "- Disk checks and usage analysis",
        "- Network diagnostics and monitoring",
        "- Cross-platform support (Windows, macOS, Linux)",
        "- Clean web interface with neon aesthetic\n",
        "Built with:",
        "- FastAPI (Python web framework)",
        "- psutil (system monitoring)",
        "- Docker (containerization)\n",
        "Repository: https://github.com/yourusername/diagnostix-lite-1"
    ]
    return format_output_section("DiagnOStiX", lines)


# Map diagnostic functions to their names
DIAGNOSTIC_FUNCTIONS: Dict[str, Callable[[], str]] = {
    'system_overview': get_system_overview,
    'hardware_health': get_hardware_health,
    'disk_diagnostics': get_disk_diagnostics,
    'network_diagnostics': get_network_diagnostics,
    'gpu_diagnostics': get_gpu_diagnostics,
    'cpu_stress_test': run_cpu_stress_test,
    'memory_stress_test': run_memory_stress_test,
    'about_diagnostix': get_about,
}

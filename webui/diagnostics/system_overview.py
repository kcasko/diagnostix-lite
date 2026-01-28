"""
System Overview - Core system state snapshot
Implements system-overview-contract.md requirements
"""
import platform
from datetime import datetime
from typing import Optional


def format_bytes(bytes_val: int) -> str:
    """Convert bytes to GiB (binary units)"""
    gib = bytes_val / (1024 ** 3)
    return f"{gib:.2f} GiB"


def format_uptime(boot_time: float) -> str:
    """Format system uptime as days, hours, minutes"""
    uptime_seconds = datetime.now().timestamp() - boot_time

    days = int(uptime_seconds // 86400)
    hours = int((uptime_seconds % 86400) // 3600)
    minutes = int((uptime_seconds % 3600) // 60)

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")

    return " ".join(parts)


def get_cpu_state() -> list[str]:
    """Get CPU state (cores, utilization, frequency)"""
    output = []
    output.append("--- CPU State ---")

    try:
        import psutil

        # Core counts
        physical = psutil.cpu_count(logical=False)
        logical = psutil.cpu_count(logical=True)
        output.append(f"Physical cores: {physical if physical else '—'}")
        output.append(f"Logical cores: {logical if logical else '—'}")

        # Current utilization
        utilization = psutil.cpu_percent(interval=1)
        output.append(f"Utilization: {utilization}%")

        # Frequency
        freq = psutil.cpu_freq()
        if freq:
            current_mhz = freq.current
            current_ghz = current_mhz / 1000
            output.append(f"Frequency: {current_ghz:.2f} GHz")
        else:
            output.append("Frequency: unavailable")

    except ImportError:
        output.append("unavailable - install psutil")
    except Exception as e:
        output.append(f"unavailable - {type(e).__name__}")

    return output


def get_memory_state() -> list[str]:
    """Get memory state (total, used, available)"""
    output = []
    output.append("--- Memory State ---")

    try:
        import psutil

        mem = psutil.virtual_memory()

        total_gib = mem.total / (1024 ** 3)
        used_gib = mem.used / (1024 ** 3)
        available_gib = mem.available / (1024 ** 3)

        output.append(f"Total RAM: {total_gib:.2f} GiB")
        output.append(f"Used RAM: {used_gib:.2f} GiB")
        output.append(f"Available RAM: {available_gib:.2f} GiB")
        output.append(f"Utilization: {mem.percent}%")

        # Swap (optional)
        swap = psutil.swap_memory()
        if swap.total > 0:
            swap_total_gib = swap.total / (1024 ** 3)
            swap_used_gib = swap.used / (1024 ** 3)
            output.append(f"Swap total: {swap_total_gib:.2f} GiB")
            output.append(f"Swap used: {swap_used_gib:.2f} GiB")

    except ImportError:
        output.append("unavailable - install psutil")
    except Exception as e:
        output.append(f"unavailable - {type(e).__name__}")

    return output


def get_disk_state() -> list[str]:
    """Get disk state (per-volume capacity and usage)"""
    output = []
    output.append("--- Disk State ---")

    try:
        import psutil

        partitions = psutil.disk_partitions()

        # Filter out virtual/temporary mounts
        excluded_fstypes = {'devfs', 'tmpfs', 'devtmpfs', 'squashfs', 'overlay', 'cgroup'}
        real_partitions = [p for p in partitions if p.fstype.lower() not in excluded_fstypes]

        if not real_partitions:
            output.append("No mounted volumes detected")
            return output

        for partition in real_partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)

                total_gib = usage.total / (1024 ** 3)
                used_gib = usage.used / (1024 ** 3)
                free_gib = usage.free / (1024 ** 3)

                output.append(f"Mount: {partition.mountpoint}")
                output.append(f"  Filesystem: {partition.fstype}")
                output.append(f"  Total: {total_gib:.2f} GiB")
                output.append(f"  Used: {used_gib:.2f} GiB")
                output.append(f"  Free: {free_gib:.2f} GiB")
                output.append(f"  Utilization: {usage.percent}%")

                # Show readonly state if applicable
                if 'ro' in partition.opts:
                    output.append(f"  State: readonly")

                output.append("")

            except PermissionError:
                output.append(f"Mount: {partition.mountpoint}")
                output.append(f"  requires elevation")
                output.append("")
            except Exception as e:
                output.append(f"Mount: {partition.mountpoint}")
                output.append(f"  unavailable - {type(e).__name__}")
                output.append("")

    except ImportError:
        output.append("unavailable - install psutil")
    except Exception as e:
        output.append(f"unavailable - {type(e).__name__}")

    return output


def get_network_state() -> list[str]:
    """Get network state (per-interface status and addressing)"""
    output = []
    output.append("--- Network State ---")

    try:
        import psutil

        # Get interface addresses
        addrs = psutil.net_if_addrs()
        # Get interface stats
        stats = psutil.net_if_stats()

        if not addrs:
            output.append("No interfaces detected")
            return output

        for interface, addr_list in addrs.items():
            # Get status
            status = "—"
            if interface in stats:
                status = "up" if stats[interface].isup else "down"

            output.append(f"Interface: {interface}")
            output.append(f"  Status: {status}")

            # Get addresses
            ipv4 = []
            ipv6 = []
            mac = None

            for addr in addr_list:
                if addr.family == 2:  # AF_INET
                    ipv4.append(addr.address)
                elif addr.family == 23 or addr.family == 30:  # AF_INET6
                    ipv6.append(addr.address)
                elif addr.family == 17 or addr.family == -1:  # AF_LINK/AF_PACKET
                    mac = addr.address

            if ipv4:
                output.append(f"  IPv4: {', '.join(ipv4)}")
            if ipv6:
                output.append(f"  IPv6: {', '.join(ipv6)}")
            if mac:
                output.append(f"  MAC: {mac}")

            output.append("")

    except ImportError:
        output.append("unavailable - install psutil")
    except Exception as e:
        output.append(f"unavailable - {type(e).__name__}")

    return output


def get_os_and_uptime() -> list[str]:
    """Get OS and uptime information"""
    output = []
    output.append("--- OS and Uptime ---")

    try:
        # OS information (always available via platform module)
        output.append(f"OS: {platform.system()} {platform.release()}")
        output.append(f"Kernel: {platform.version()}")
        output.append(f"Architecture: {platform.machine()}")
        output.append(f"Hostname: {platform.node()}")

        # Uptime (requires psutil)
        try:
            import psutil
            boot_time = psutil.boot_time()
            uptime_str = format_uptime(boot_time)
            boot_str = datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')

            output.append(f"Uptime: {uptime_str}")
            output.append(f"Boot time: {boot_str}")
        except ImportError:
            output.append("Uptime: unavailable - install psutil")
        except Exception as e:
            output.append(f"Uptime: unavailable - {type(e).__name__}")

    except Exception as e:
        output.append(f"OS info: unavailable - {type(e).__name__}")

    return output


def run() -> str:
    """
    Generate System Overview report

    Implements system-overview-contract.md:
    - Always loads
    - Never errors globally
    - Shows current state only
    - Sections: CPU, Memory, Disk, Network, OS/Uptime
    """

    output = []
    output.append("=" * 60)
    output.append("SYSTEM OVERVIEW")
    output.append("=" * 60)
    output.append("")

    # Fixed order per contract
    output.extend(get_cpu_state())
    output.append("")

    output.extend(get_memory_state())
    output.append("")

    output.extend(get_disk_state())

    output.extend(get_network_state())

    output.extend(get_os_and_uptime())

    output.append("")
    output.append("=" * 60)
    output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("=" * 60)

    return "\n".join(output)

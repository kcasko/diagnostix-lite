"""
Disk Diagnostics - Partition layout and disk health checks
"""
import psutil
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
    output.append("DISK DIAGNOSTICS")
    output.append("=" * 60)
    output.append("")
    
    output.append("--- Disk Partitions ---")
    try:
        partitions = psutil.disk_partitions()
        for partition in partitions:
            output.append("")
            output.append(f"Device: {partition.device}")
            output.append(f"  Mountpoint: {partition.mountpoint}")
            output.append(f"  Filesystem: {partition.fstype}")
            output.append(f"  Options: {partition.opts}")
            
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                output.append(f"  Total: {format_bytes(usage.total)}")
                output.append(f"  Used: {format_bytes(usage.used)}")
                output.append(f"  Free: {format_bytes(usage.free)}")
                output.append(f"  Usage: {usage.percent}%")
                
                if usage.percent > 90:
                    output.append("  STATUS: CRITICAL - Disk almost full!")
                elif usage.percent > 75:
                    output.append("  STATUS: WARNING - Low disk space")
                else:
                    output.append("  STATUS: OK")
            except PermissionError:
                output.append("  Access Denied")
            except Exception as e:
                output.append(f"  Error: {e}")
    except Exception as e:
        output.append(f"Error retrieving partitions: {e}")
    
    output.append("")
    output.append("")
    output.append("--- Disk I/O Statistics ---")
    try:
        disk_io = psutil.disk_io_counters()
        if disk_io:
            output.append(f"Read Count: {disk_io.read_count:,}")
            output.append(f"Write Count: {disk_io.write_count:,}")
            output.append(f"Read Bytes: {format_bytes(disk_io.read_bytes)}")
            output.append(f"Write Bytes: {format_bytes(disk_io.write_bytes)}")
            output.append(f"Read Time: {disk_io.read_time:,} ms")
            output.append(f"Write Time: {disk_io.write_time:,} ms")
        else:
            output.append("Disk I/O statistics not available")
    except Exception as e:
        output.append(f"Error: {e}")
    
    output.append("")
    output.append("=" * 60)
    output.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("=" * 60)
    
    return "\n".join(output)

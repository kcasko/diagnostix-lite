"""
Network Diagnostics - Interfaces, routes, DNS, and connectivity
"""
import psutil
import socket
import subprocess
import platform
from datetime import datetime


def run() -> str:
    output = []
    output.append("=" * 60)
    output.append("NETWORK DIAGNOSTICS")
    output.append("=" * 60)
    output.append("")
    
    output.append("--- Network Interfaces ---")
    try:
        net_if = psutil.net_if_addrs()
        net_stats = psutil.net_if_stats()
        
        for interface, addrs in net_if.items():
            output.append("")
            output.append(f"{interface}:")
            
            if interface in net_stats:
                stats = net_stats[interface]
                output.append(f"  Status: {'UP' if stats.isup else 'DOWN'}")
                output.append(f"  Speed: {stats.speed} Mbps")
            
            for addr in addrs:
                if addr.family == 2:
                    output.append(f"  IPv4: {addr.address}")
                    if addr.netmask:
                        output.append(f"  Netmask: {addr.netmask}")
                elif addr.family == 23 or addr.family == 30:
                    output.append(f"  IPv6: {addr.address}")
                elif addr.family == 17 or addr.family == -1:
                    output.append(f"  MAC: {addr.address}")
    except Exception as e:
        output.append(f"Error: {e}")
    
    output.append("")
    output.append("")
    output.append("--- Network I/O Statistics ---")
    try:
        net_io = psutil.net_io_counters()
        output.append(f"Bytes Sent: {net_io.bytes_sent:,}")
        output.append(f"Bytes Received: {net_io.bytes_recv:,}")
        output.append(f"Packets Sent: {net_io.packets_sent:,}")
        output.append(f"Packets Received: {net_io.packets_recv:,}")
        output.append(f"Errors In: {net_io.errin}")
        output.append(f"Errors Out: {net_io.errout}")
        output.append(f"Drops In: {net_io.dropin}")
        output.append(f"Drops Out: {net_io.dropout}")
    except Exception as e:
        output.append(f"Error: {e}")
    
    output.append("")
    output.append("")
    output.append("--- DNS Resolution Test ---")
    try:
        test_hosts = ["google.com", "github.com"]
        for host in test_hosts:
            try:
                ip = socket.gethostbyname(host)
                output.append(f"{host}: {ip} - OK")
            except socket.gaierror:
                output.append(f"{host}: FAILED")
    except Exception as e:
        output.append(f"Error: {e}")
    
    output.append("")
    output.append("")
    output.append("--- Connectivity Test ---")
    try:
        ping_cmd = ["ping", "-n", "2" if platform.system() == "Windows" else "-c", "2", "8.8.8.8"]
        result = subprocess.run(ping_cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            output.append("Internet connectivity: OK (8.8.8.8 reachable)")
        else:
            output.append("Internet connectivity: FAILED")
    except Exception as e:
        output.append(f"Connectivity test error: {e}")
    
    output.append("")
    output.append("=" * 60)
    output.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("=" * 60)
    
    return "\n".join(output)

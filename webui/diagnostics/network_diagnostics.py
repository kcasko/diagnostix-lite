"""
Network Diagnostics - Interfaces, routes, DNS, connectivity, and speed test
"""
import psutil
import socket
import subprocess
import platform
from datetime import datetime

try:
    import speedtest
    SPEEDTEST_AVAILABLE = True
except ImportError:
    SPEEDTEST_AVAILABLE = False


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
    output.append("")
    output.append("--- Internet Speed Test ---")
    if SPEEDTEST_AVAILABLE:
        try:
            output.append("Running speed test (this may take a moment)...")
            st = speedtest.Speedtest(secure=True)
            st.get_best_server()

            download_speed = st.download() / 1_000_000  # Convert to Mbps
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            ping = st.results.ping
            server = st.results.server

            output.append(f"Server: {server['sponsor']} ({server['name']}, {server['country']})")
            output.append(f"Ping: {ping:.2f} ms")
            output.append(f"Download: {download_speed:.2f} Mbps")
            output.append(f"Upload: {upload_speed:.2f} Mbps")
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg:
                output.append("Speed test blocked (HTTP 403). This often occurs when:")
                output.append("  - Using a VPN (detected: ProtonVPN may be active)")
                output.append("  - IP is rate-limited by speedtest.net")
                output.append("Try disabling VPN temporarily or run: speedtest-cli --secure")
            else:
                output.append(f"Speed test error: {e}")
    else:
        output.append("speedtest-cli not installed. Run: pip install speedtest-cli")

    output.append("")
    output.append("=" * 60)
    output.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("=" * 60)

    return "\n".join(output)

"""
Network Speed Test - Internet bandwidth measurement using speedtest-cli
"""
from datetime import datetime

try:
    import speedtest
    SPEEDTEST_AVAILABLE = True
except ImportError:
    SPEEDTEST_AVAILABLE = False


def run() -> str:
    output = []
    output.append("=" * 60)
    output.append("NETWORK SPEED TEST")
    output.append("=" * 60)
    output.append("")

    if not SPEEDTEST_AVAILABLE:
        output.append("ERROR: speedtest-cli not installed")
        output.append("Install with: pip install speedtest-cli")
        output.append("")
        output.append("=" * 60)
        return "\n".join(output)

    try:
        output.append("Initializing speed test...")
        output.append("Finding best server...")

        st = speedtest.Speedtest(secure=True)
        st.get_best_server()

        server = st.results.server
        output.append(f"Server: {server['sponsor']}")
        output.append(f"Location: {server['name']}, {server['country']}")
        output.append(f"Host: {server['host']}")
        output.append("")

        output.append("Testing download speed...")
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        output.append(f"Download: {download_speed:.2f} Mbps")

        output.append("Testing upload speed...")
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        output.append(f"Upload: {upload_speed:.2f} Mbps")

        ping = st.results.ping
        output.append("")
        output.append("--- Results Summary ---")
        output.append(f"Ping: {ping:.2f} ms")
        output.append(f"Download: {download_speed:.2f} Mbps ({download_speed/8:.2f} MB/s)")
        output.append(f"Upload: {upload_speed:.2f} Mbps ({upload_speed/8:.2f} MB/s)")

    except Exception as e:
        error_msg = str(e)
        output.append("")
        output.append(f"Speed test failed: {error_msg}")

        if "403" in error_msg:
            output.append("")
            output.append("HTTP 403 errors typically occur when:")
            output.append("  - Using a VPN that blocks speedtest.net")
            output.append("  - IP is rate-limited")
            output.append("Try disabling VPN temporarily.")

    output.append("")
    output.append("=" * 60)
    output.append(f"Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("=" * 60)

    return "\n".join(output)

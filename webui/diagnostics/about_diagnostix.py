"""
About DiagnOStiX - Version and project information
"""
import platform
from datetime import datetime


def run() -> str:
    """Display DiagnOStiX version and project information"""
    
    output = []
    output.append("=" * 60)
    output.append("DiagnOStiX - System Diagnostics Platform")
    output.append("=" * 60)
    output.append("")
    
    output.append("Version: 2.0 (Python Edition)")
    output.append("Project: GitKon Developer Passion Project")
    output.append("Started: November 2025")
    output.append("")
    
    output.append("Description:")
    output.append("  A lightweight web-based diagnostics tool for PC repair,")
    output.append("  system triage, and developer tooling.")
    output.append("")
    
    output.append("Features:")
    output.append("  • Cross-platform (Windows, macOS, Linux)")
    output.append("  • Web-based interface (FastAPI + Jinja2)")
    output.append("  • Python-based diagnostics (psutil, speedtest-cli)")
    output.append("  • Real-time output streaming")
    output.append("  • Docker containerization")
    output.append("  • Dark neon synthwave theme")
    output.append("")
    
    output.append("Diagnostic Categories:")
    output.append("  • System Overview & Hardware Health")
    output.append("  • Disk Diagnostics & S.M.A.R.T. Data")
    output.append("  • Network Diagnostics & Speed Tests")
    output.append("  • CPU & Memory Stress Tests")
    output.append("  • GPU Detection & Monitoring")
    output.append("")
    
    output.append("Runtime Environment:")
    output.append(f"  OS: {platform.system()} {platform.release()}")
    output.append(f"  Architecture: {platform.machine()}")
    output.append(f"  Python: {platform.python_version()}")
    output.append(f"  Hostname: {platform.node()}")
    output.append(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("")
    
    output.append("Repository:")
    output.append("  https://github.com/yourusername/diagnostix")
    output.append("")
    
    output.append("=" * 60)
    output.append("Built for technicians, sysadmins, and developers")
    output.append("who want clean answers fast.")
    output.append("=" * 60)
    
    return "\n".join(output)

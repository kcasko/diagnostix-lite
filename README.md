# DiagnOStiX

A lightweight cross-platform diagnostics tool built for PC repair,
system triage, and developer tooling.

DiagnOStiX is a web-based diagnostic platform that works on Windows,
macOS, and Linux. It provides hardware health monitoring, system diagnostics,
stress tests, and repair utilities through a clean neon-themed web interface.

**Version 2.0** - Now with full cross-platform support via Python and Docker!

Started November 2025.

------------------------------------------------------------------------

## Features

### 🌐 Cross-Platform Support (NEW in v2.0)

**Python-powered diagnostics** work on Windows, macOS, and Linux\
**Docker support** for instant deployment with one command\
**Hybrid mode** - Use Python diagnostics anywhere, or bash scripts on Linux for deeper access\
**No installation required** - Run from Docker or directly with Python

### 🔧 Diagnostic Suite

**System Overview** - CPU, RAM, disk, OS information\
**Hardware Health** - Per-core CPU usage, memory status, temperature sensors, battery info\
**Disk Diagnostics** - Partition info, disk usage, I/O statistics, SMART data (Linux)\
**Network Diagnostics** - Interface details, connection stats, active connections\
**GPU Diagnostics** - NVIDIA GPU detection, temperature, load, memory (via GPUtil)\
**CPU Stress Test** - Load testing for stability checks\
**Memory Stress Test** - RAM allocation and validation\
**Kraken Repo Scanner** - Git repository detection and integrity checks (Linux bash)\
**Network Speed Test** - Throughput measurement (Linux bash)\
**Boot Diagnostics** - UEFI/BIOS detection, boot logs (Linux bash)\
**Quick Repair** - Common system fixes (Linux bash)

### 🎨 Web Interface (FastAPI)

**Dark neon-themed UI** with synthwave aesthetic\
**Real-time diagnostic output** in the browser\
**Downloadable reports** for all diagnostics\
**Auto-detection** of available features per platform\
**REST API** for programmatic access

### 🐳 Deployment Options

1. **Docker** (recommended) - `docker compose up` and go
2. **Direct Python** - Run with `uvicorn` on any OS
3. **Windows Executable** - Standalone .bat launcher
4. **Linux ISO** (legacy) - Bootable diagnostic environment

------------------------------------------------------------------------

## Repository Structure

    diagnostix
    ├── branding
    │   ├── banner.png
    │   ├── icon.png
    │   └── wallpapers
    │       ├── boot.png
    │       ├── desktop.png
    │       └── login.png
    ├── docs
    ├── LICENSE
    ├── README.md
    ├── scripts
    │   ├── about_diagnostix.sh
    │   ├── autobrand.sh
    │   ├── boot_diagnostics.sh
    │   ├── collect_logs.sh
    │   ├── cpu_stress_test.sh
    │   ├── diagnostix_check.sh
    │   ├── diagnostix_menu.sh
    │   ├── diagnostix_tui.sh
    │   ├── disk_diagnostics.sh
    │   ├── gpu_diagnostics.sh
    │   ├── hardware_health.sh
    │   ├── kraken_repo_scanner.sh
    │   ├── master_collect.sh
    │   ├── memory_stress_test.sh
    │   ├── network_diagnostics.sh
    │   ├── network_quick_fix.sh
    │   ├── network_speed_test.sh
    │   ├── quick_repair.sh
    │   ├── system_overview.sh
    │   ├── system_report.sh
    │   └── tech_support_mode.sh
    └── webui
        ├── Dockerfile
        ├── docker-compose.yml
        ├── main.py
        ├── requirements.txt
        ├── diagnostics/
        │   ├── __init__.py
        │   ├── about_diagnostix.py
        │   ├── system_overview.py
        │   ├── hardware_health.py
        │   ├── disk_diagnostics.py
        │   ├── network_diagnostics.py
        │   ├── cpu_stress_test.py
        │   ├── memory_stress_test.py
        │   └── gpu_diagnostics.py
        ├── static/
        │   ├── banner.png
        │   ├── output.js
        │   ├── styles.css
        │   └── styles.stable.css
        └── templates/
            ├── base.html
            ├── index.html
            ├── index.stable.html
            └── output.html

------------------------------------------------------------------------

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/diagnostix
cd diagnostix

# Start with Docker Compose
docker compose up

# Open your browser
http://localhost:8000
```

### Option 2: Direct Python (Windows/Mac/Linux)

```bash
# Install Python 3.10+ if needed
cd webui

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --host 0.0.0.0 --port 8000
```

Or use the provided startup scripts:
- Windows: `start_webui.bat`
- Linux/Mac: `./start_webui.sh`

### Option 3: Quick Test (Current Directory)

If you already have Python and the dependencies installed:

```bash
cd webui
python -m uvicorn main:app --reload
```

------------------------------------------------------------------------

## How It Works

### Architecture

DiagnOStiX uses a **hybrid diagnostic approach**:

1. **Python Diagnostics** (cross-platform) - Uses `psutil`, `platform`, and other Python libraries for system monitoring. Works on any OS.

2. **Bash Scripts** (Linux-enhanced) - Original bash scripts provide deeper system access on Linux systems (SMART data, boot diagnostics, repair tools).

3. **Auto-detection** - The web app automatically uses Python diagnostics by default, falling back to bash scripts on Linux for tools that need it.

### Technology Stack

- **FastAPI** - Modern Python web framework
- **psutil** - Cross-platform system monitoring
- **Jinja2** - HTML templating
- **Docker** - Containerization for easy deployment
- **Bash** - Enhanced diagnostics on Linux

### WebUI

Located in [webui/main.py](webui/main.py).\
Uses Jinja2 templates and neon-themed CSS.\
Diagnostics run server-side and stream output to the browser.\
All outputs can be downloaded as text files.

### Python Diagnostics Module

Located in [webui/diagnostics/](webui/diagnostics/).\
Pure Python implementations of core diagnostics.\
Works identically on Windows, macOS, and Linux.\
No external tools required (except GPU diagnostics needs NVIDIA drivers).

------------------------------------------------------------------------

## Building the ISO (Legacy/Optional)

For the bootable Linux ISO version:

```bash
git clone https://github.com/pieroproietti/fresh-eggs
cd fresh-eggs
sudo ./fresh-eggs.sh
eggs love -n
```

ISO will appear in `/home/eggs/`

**Note:** The ISO approach is now optional. The web app provides most features cross-platform.

------------------------------------------------------------------------

## Platform Compatibility

| Feature | Windows | macOS | Linux |
|---------|---------|-------|-------|
| System Overview | ✅ | ✅ | ✅ |
| Hardware Health | ✅ | ✅ | ✅ |
| Disk Diagnostics | ✅ | ✅ | ✅ Enhanced |
| Network Diagnostics | ✅ | ✅ | ✅ |
| GPU Diagnostics | ✅ NVIDIA | ✅ NVIDIA | ✅ NVIDIA |
| CPU Stress Test | ✅ | ✅ | ✅ |
| Memory Stress Test | ✅ | ✅ | ✅ |
| Temperature Sensors | ⚠️ Limited | ⚠️ Limited | ✅ |
| SMART Disk Data | ❌ | ❌ | ✅ |
| Boot Diagnostics | ❌ | ❌ | ✅ |
| Quick Repair | ❌ | ❌ | ✅ |
| Kraken Repo Scanner | ❌ | ❌ | ✅ |

✅ Full support | ⚠️ Partial support | ❌ Linux only

------------------------------------------------------------------------

## Development

### Project Structure

```
diagnostix/
├── docker-compose.yml      # Docker orchestration (root level)
├── branding/              # Visual assets (logos, wallpapers)
├── scripts/               # Bash diagnostic scripts (Linux)
├── webui/
│   ├── Dockerfile        # Container definition
│   ├── main.py           # FastAPI application
│   ├── requirements.txt  # Python dependencies
│   ├── diagnostics/      # Python diagnostic modules (NEW!)
│   │   ├── __init__.py
│   │   ├── about_diagnostix.py
│   │   ├── system_overview.py
│   │   ├── hardware_health.py
│   │   ├── disk_diagnostics.py
│   │   ├── network_diagnostics.py
│   │   ├── cpu_stress_test.py
│   │   ├── memory_stress_test.py
│   │   └── gpu_diagnostics.py
│   ├── static/           # CSS, JS, images
│   └── templates/        # HTML templates
├── README.md             # This file
└── logs/                 # Runtime logs (created by Docker)
```

### Adding New Diagnostics

1. **Create a new Python module** in [webui/diagnostics/](webui/diagnostics/) (e.g., `my_diagnostic.py`):

```python
"""
My Diagnostic - Description
"""
from datetime import datetime

def run() -> str:
    output = []
    output.append("=" * 60)
    output.append("MY DIAGNOSTIC")
    output.append("=" * 60)
    output.append("")

    # Your diagnostic code here
    output.append("Results go here...")

    output.append("")
    output.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return "\n".join(output)
```

2. **Register it** in [webui/diagnostics/__init__.py](webui/diagnostics/__init__.py):

```python
from .my_diagnostic import run as my_diagnostic

DIAGNOSTIC_FUNCTIONS: Dict[str, Callable[[], str]] = {
    # ... existing diagnostics ...
    "my_diagnostic": my_diagnostic,
}
```

3. **Add tool definition** in [webui/main.py](webui/main.py):

```python
"my_diagnostic": {
    "label": "My Diagnostic",
    "script": "my_diagnostic.sh",  # Optional bash fallback
    "description": "Description here",
    "python_available": True,
    "category": "system"  # or "network", "storage", "stress", etc.
}
```

4. **(Optional) Add bash version** in `scripts/my_diagnostic.sh` for Linux-enhanced mode.

### API Usage

DiagnOStiX provides a REST API:

- `GET /` - Web interface
- `GET /run/{tool_id}` - Run diagnostic (returns HTML)
- `GET /run/{tool_id}?mode=python` - Force Python mode
- `GET /run/{tool_id}?mode=bash` - Force bash mode
- `GET /download/{tool_id}` - Download output as text file

------------------------------------------------------------------------

## Troubleshooting

### "Module not found" errors
```bash
cd webui
pip install -r requirements.txt
```

### "Bash not found" on Windows
Install Git for Windows (includes Git Bash): https://git-scm.com/

### Docker build fails
Make sure Docker Desktop is running and you have sufficient disk space.

### Port 8000 already in use
Change the port in docker-compose.yml or when running uvicorn:
```bash
uvicorn main:app --port 8001
```

### Temperature sensors not showing
Temperature monitoring requires admin/root privileges on most systems. Run with elevated permissions or use Docker.

### GPU not detected
- Only NVIDIA GPUs are supported via GPUtil
- Ensure NVIDIA drivers are installed
- AMD/Intel GPU support coming in future updates

------------------------------------------------------------------------

## Future Roadmap

- [ ] AMD and Intel GPU support
- [ ] Historical data tracking and trending
- [ ] PDF report generation
- [ ] REST API authentication
- [ ] Plugin system for third-party diagnostics
- [ ] Remote diagnostic capabilities
- [ ] Web-based configuration
- [ ] macOS SMART data support
- [ ] Windows SMART data support via WMI
- [ ] Real-time system monitoring dashboard
- [ ] Automated health scoring

------------------------------------------------------------------------

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests if applicable
4. Submit a pull request

Focus areas:
- Cross-platform compatibility improvements
- New diagnostic modules
- UI/UX enhancements
- Documentation

------------------------------------------------------------------------

## License

See [LICENSE](LICENSE) file for details.

------------------------------------------------------------------------

DiagnOStiX is built for technicians, sysadmins, repair shops, and
developers who need fast, reliable system diagnostics across any platform.

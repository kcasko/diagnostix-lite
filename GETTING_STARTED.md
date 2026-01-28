# Getting Started with DiagnOStiX

This guide will help you get DiagnOStiX up and running on your local machine for development and testing.

## Prerequisites

### Windows
- Python 3.10 or higher
- Git Bash (comes with Git for Windows) - required to run the diagnostic bash scripts
- A web browser

### Linux
- Python 3.10 or higher
- Bash shell
- A web browser

## Quick Start

### 1. Install Dependencies

The Python virtual environment and dependencies are already set up in `webui/venv/`. If you need to reinstall:

```bash
cd webui
python -m venv venv
venv/Scripts/activate  # On Windows
# OR
source venv/bin/activate  # On Linux
pip install -r requirements.txt
```

### 2. Start the Web UI

#### On Windows (CMD/PowerShell)
```cmd
start_webui.bat
```

#### On Windows (Git Bash) or Linux
```bash
./start_webui.sh
```

### 3. Access the Web Interface

Open your browser and navigate to:
```
http://localhost:8000
```

You should see the DiagnOStiX Control Panel with all the diagnostic tools listed.

## Project Structure

```
diagnostix-lite/
├── branding/          # Branding assets (wallpapers, icons, banners)
├── scripts/           # Bash diagnostic scripts
├── webui/             # FastAPI web interface
│   ├── main.py        # Main application (now cross-platform compatible)
│   ├── static/        # CSS, JS, and images
│   ├── templates/     # HTML templates
│   ├── venv/          # Python virtual environment
│   └── requirements.txt
├── start_webui.bat    # Windows startup script
├── start_webui.sh     # Linux/Git Bash startup script
└── README.md          # Main project documentation
```

## Running Diagnostic Scripts

The diagnostic scripts are located in the `scripts/` directory. You can run them:

1. **Through the Web UI** - Click on any diagnostic tool in the web interface
2. **From the command line** (on Linux or Git Bash):
   ```bash
   bash scripts/system_overview.sh
   bash scripts/hardware_health.sh
   # etc.
   ```

## Notes for Windows Users

- The diagnostic scripts are bash scripts designed for Linux systems
- On Windows, they will run through Git Bash, but some commands may not work as expected (e.g., hardware diagnostics that use Linux-specific tools)
- For full functionality, consider running the ISO on a VM or bare metal Linux system
- The web UI will work perfectly on Windows for development and testing

## Development

To make changes to the web interface:

1. Edit files in `webui/`
2. The server runs with `--reload` flag, so changes are automatically detected
3. Refresh your browser to see changes

### File Locations
- Python routes: [webui/main.py](webui/main.py)
- HTML templates: [webui/templates/](webui/templates/)
- Styles: [webui/static/styles.css](webui/static/styles.css)
- Scripts: [webui/static/output.js](webui/static/output.js)

## Building the ISO (Linux only)

To build a bootable ISO with DiagnOStiX, see the instructions in the main [README.md](README.md) under "Building the ISO (Penguin-Eggs)".

## Troubleshooting

### Port 8000 already in use
Change the port in the startup script:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Scripts not executing
Make sure Git Bash is installed on Windows, or that you're on a Linux system with bash available.

### Import errors
Reinstall dependencies:
```bash
cd webui
venv/Scripts/activate  # or source venv/bin/activate on Linux
pip install -r requirements.txt
```

## Next Steps

- Explore the web interface
- Try running different diagnostic tools
- Customize the branding in `branding/`
- Add new diagnostic scripts to `scripts/`
- Modify the web UI theme in `webui/static/styles.css`

For more information about the project, see the main [README.md](README.md).

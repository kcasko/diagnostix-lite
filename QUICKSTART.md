# DiagnOStiX - Quick Start Guide

Get DiagnOStiX running in under 5 minutes!

## Option 1: Docker (Recommended) 

**Prerequisites:** Docker Desktop installed

```bash
# Clone the repo
git clone https://github.com/yourusername/diagnostix-lite-1
cd diagnostix-lite-1

# Start the container
docker compose up

# Open in browser
http://localhost:8000
```

That's it! The web interface will be available at [http://localhost:8000](http://localhost:8000)

**To run in background:**
```bash
docker compose up -d
```

**To stop:**
```bash
docker compose down
```

## Option 2: Direct Python (No Docker)

**Prerequisites:** Python 3.10 or higher

```bash
# Clone the repo
git clone https://github.com/yourusername/diagnostix-lite-1
cd diagnostix-lite-1/webui

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Open in browser
http://localhost:8000
```

## Using DiagnOStiX

1. **Select a diagnostic** from the main dashboard
2. **Click the diagnostic** to run it
3. **View real-time output** in your browser
4. **Download the report** as a text file (optional)

## Available Diagnostics

### Cross-Platform (Works Everywhere)
- **System Overview** - CPU, RAM, disk, OS info
- **Hardware Health** - CPU usage, memory, temperatures
- **Disk Diagnostics** - Partitions, usage, I/O stats
- **Network Diagnostics** - Interfaces, connections, DNS tests
- **GPU Diagnostics** - NVIDIA GPU detection (requires drivers)
- **CPU Stress Test** - Load test for stability
- **Memory Stress Test** - RAM allocation test

### Linux-Only (Requires bash scripts)
- **Kraken Repo Scanner** - Git repository analysis
- **Network Speed Test** - Bandwidth measurement
- **Boot Diagnostics** - UEFI/BIOS, boot logs
- **Quick Repair** - Common system fixes

## Troubleshooting

### Port 8000 already in use
```bash
# Use a different port
docker compose down
# Edit docker-compose.yml and change "8000:8000" to "8001:8000"
docker compose up
```

Or with Python:
```bash
python -m uvicorn main:app --port 8001
```

### "Module not found" errors
```bash
cd webui
pip install -r requirements.txt
```

### GPU not detected
- Only NVIDIA GPUs supported currently
- Ensure NVIDIA drivers are installed
- AMD/Intel GPU support coming soon

### Docker build fails
- Make sure Docker Desktop is running
- Check you have sufficient disk space (at least 2GB free)

## Next Steps

- Check out the full [README.md](README.md) for detailed documentation
- Add custom diagnostics (see Development section in README)
- Deploy to a server for remote diagnostics

## Support

- GitHub Issues: https://github.com/yourusername/diagnostix-lite-1/issues
- Documentation: [README.md](README.md)

---

**DiagnOStiX** - Fast, cross-platform system diagnostics for everyone.

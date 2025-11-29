# DiagnostiX Lite

A lightweight neon-themed Linux diagnostics OS built for PC repair,
system triage, and developer tooling.

DiagnostiX Lite is a custom Ubuntu-based environment designed to boot
fast, detect hardware issues, run repair utilities, and provide a clean
web interface for troubleshooting. The goal is simple: reduce friction
and get you straight to the answers.

Started November 2025 for the GitKon Developer Passion Project.

------------------------------------------------------------------------

## Features

### Desktop and Branding

Custom neon DiagnostiX banners, wallpapers, and icons\
Auto-branding engine that syncs Plymouth boot theme, desktop header, and
WebUI assets\
Consistent dark synthwave aesthetic

### Diagnostic Suite (scripts/)

Hardware health report\
CPU and memory stress tests\
GPU diagnostics\
Disk checks and S.M.A.R.T. data\
Network diagnostics, quick fix, and speed test\
Boot diagnostics\
System overview and full report\
Quick Repair mode for common OS faults\
Master log collector for support sessions\
GitKraken-themed Kraken Repo Scanner for repo detection and integrity
checks

### Web Interface (FastAPI)

Dark-themed HTML and CSS\
Tabs for diagnostic categories\
Real-time output renderer\
Download button for logs\
Runs Bash diagnostics from the browser\
Static neon branding assets

### Bootable OS

Built using Penguin-Eggs\
Custom Plymouth theme\
Fast live boot\
Works fully inside VMware and on bare metal\
SquashFS and casper/live boot compatible

------------------------------------------------------------------------

## Repository Structure

    diagnostix-lite
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
        ├── main.py
        ├── static
        │   ├── banner.png
        │   ├── output.js
        │   ├── styles.css
        │   └── styles.stable.css
        └── templates
            ├── base.html
            ├── index.html
            ├── index.stable.html
            └── output.html

------------------------------------------------------------------------

## How It Works

### Bash Diagnostics

Every diagnostic runs as a standalone Bash script.\
The WebUI triggers a script and streams the output back to the browser.\
Scripts are POSIX-friendly and safe for live or installed systems.

### WebUI (FastAPI)

Located in `webui/main.py`.\
Uses Jinja2 templates and static neon styles.\
Clean dark layout with real-time command output and log downloads.

### Branding System

`branding/` contains all assets.\
`autobrand.sh` distributes updated images to:\
Plymouth boot theme\
Desktop banner\
WebUI\
System icons

------------------------------------------------------------------------

## Building the ISO (Penguin-Eggs)

Clone and run the builder:

    git clone https://github.com/pieroproietti/fresh-eggs
    cd fresh-eggs
    sudo ./fresh-eggs.sh 
    eggs love -n

Your ISO will appear under:

    /home/eggs/

The ISO includes the full DiagnostiX Lite environment and branding.

------------------------------------------------------------------------

## GitKon Submission Info

Category: Developer Passion Project

Qualifies because it:\
Helps devs ship code faster\
Includes original tooling (Kraken Repo Scanner, autobranding engine)\
Fits into a five-minute demo\
Started after June 2025\
Contains Git-themed utilities

------------------------------------------------------------------------

## Future Roadmap

GitOps-driven repair mode\
Advanced repo integrity analysis\
Dockerized WebUI\
Third-party script plugins\
Improved Plymouth animations\
Cross-platform log uploader

------------------------------------------------------------------------

DiagnostiX Lite is built for technicians, sysadmins, repair shops, and
developers who want an OS that cuts the nonsense and gives clean answers
fast.

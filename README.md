DiagnostiX Lite

A lightweight neon-themed Linux diagnostics OS built for PC repair, system triage, and developer tooling.

DiagnostiX Lite is a custom Ubuntu-based environment designed to boot fast, detect hardware issues, run repair utilities, and provide a clean web interface for troubleshooting. The goal is simple: help devs and technicians ship fixes faster with as little friction as possible.

Started November 2025 for the GitKon Developer Passion Project.

Features
Desktop and Branding

Custom neon DiagnostiX banners, wallpapers, and icons
Auto-branding system that syncs Plymouth boot theme, desktop header, and WebUI visuals
Consistent DX aesthetic powered by dark synthwave colors

Full Diagnostic Suite

Located in scripts/
Hardware health report
CPU and memory stress tests
GPU diagnostics
Disk checks and S.M.A.R.T. data
Network diagnostics, quick fix, and speed test
Boot diagnostics
System overview and full system report
Quick Repair mode for common OS faults
Master log collector for support sessions
GitKraken-themed Kraken Repo Scanner that finds repos, checks integrity, uncommitted changes, and conflicts

Web Interface (FastAPI)

Located under webui/
Dark-themed HTML and CSS
Tabs for all diagnostic modules
Script output renderer
Download button for logs
Runs Bash scripts safely from the browser
Static neon branding assets

Lightweight Bootable OS

Built using Penguin-Eggs
Custom Plymouth theme
Fast live boot
Fully working in VMware and physical hardware
SquashFS and casper/live boot compatible

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
How It Works
1. Bash Scripts

Every diagnostic action is performed by standalone Bash scripts.
The FastAPI server executes the selected script and streams the output back to the browser.
Each script is POSIX-friendly, safe in live or installed environments, and works offline.

2. WebUI (FastAPI)

webui/main.py serves the interface using FastAPI.
Templates render a neon-themed dark layout.
Outputs are displayed in-browser with buttons for running tests or downloading results.

3. Branding and Boot Themes

Images and assets live under branding/.
autobrand.sh automatically pushes them to:
Plymouth boot theme
Desktop header
WebUI assets
Desktop icon

This creates a consistent neon DiagnostiX aesthetic across the entire OS.

Build Instructions (Penguin-Eggs)
Clone the Eggs builder:

git clone https://github.com/pieroproietti/fresh-eggs
cd fresh-eggs
sudo ./fresh-eggs.sh eggs love -n

The resulting ISO will appear under:
/home/eggs/

The ISO includes the full DiagnostiX Lite environment.

License

This project uses the MIT License.
See LICENSE for full details.

MIT TLDR:
You can use, modify, distribute, or sell it.
Include the same license in your builds.
No liability or warranty.

GitKon Submission Notes

DiagnostiX Lite qualifies for the Developer Passion Project category.

It meets these criteria:
Helps devs ship code faster through integrated diagnostics and repo scanners
Original technical design: auto-branding engine, unified diagnostics, Git-focused tooling
Fits easily into a 5-minute demo
Started after June 2025
Includes Git-themed functionality (Kraken Repo Scanner)

Future Plans

GitOps-driven repair mode
Advanced repo integrity scoring
Dockerized WebUI
Plug-in system for third-party diagnostic scripts
Improved Plymouth animations
Cross-platform log uploader

DiagnostiX Lite is built for anyone who spends their days fixing systems, pulling logs, diagnosing weird failures, or trying to get straight answers out of flaky hardware. The OS removes friction so you can get your answers fast.

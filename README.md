# DiagnostiX Lite  
A lightweight, neon-themed Linux diagnostics OS built for PC repair, system triage, and developer tooling.

DiagnostiX Lite is a custom Ubuntu-based diagnostic environment designed to boot fast, detect hardware issues, run repair utilities, and provide a clean web UI for troubleshooting. Its focus is simple: help devs and technicians ship fixes faster.

This project was started in November 2025 for the GitKon Developer Passion Project category.

---

## Features

### Desktop + Branding
• Custom neon DiagnostiX banners, wallpapers, and icons  
• Auto-branding system that syncs Plymouth boot theme, desktop header, and webUI visuals  
• Consistent DX aesthetic powered by dark synthwave colors

### Full Diagnostic Suite
Located under `scripts/`  
• Hardware health report  
• CPU and memory stress tests  
• GPU diagnostics  
• Disk checks and S.M.A.R.T. data  
• Network diagnostics, quick fix, and speed test  
• Boot diagnostics  
• System overview & system report  
• Quick Repair mode for common OS faults  
• Master log collector for support sessions  
• GitKraken-themed “Kraken Repo Scanner” which scans the system for repos, uncommitted changes, conflicts, last commits, and integrity

### Web Interface (FastAPI)
Located under `webui/`  
• Dark-themed HTML/CSS UI  
• Tabs for all diagnostics  
• Output renderer  
• Download button for logs  
• Built-in scripts callable through the browser  
• Static neon branding assets

### Lightweight Bootable OS  
• Built using Penguin-Eggs  
• Custom Plymouth theme  
• Fast live boot  
• Works fully inside VMware and bare metal  
• SquashFS + casper/live boot compatible

---

## Repository Structure

diagnostix-lite
├── branding
│ ├── banner.png
│ ├── icon.png
│ └── wallpapers
│ ├── boot.png
│ ├── desktop.png
│ └── login.png
├── docs
├── LICENSE
├── README.md
├── scripts
│ ├── about_diagnostix.sh
│ ├── autobrand.sh
│ ├── boot_diagnostics.sh
│ ├── collect_logs.sh
│ ├── cpu_stress_test.sh
│ ├── diagnostix_check.sh
│ ├── diagnostix_menu.sh
│ ├── diagnostix_tui.sh
│ ├── disk_diagnostics.sh
│ ├── gpu_diagnostics.sh
│ ├── hardware_health.sh
│ ├── kraken_repo_scanner.sh
│ ├── master_collect.sh
│ ├── memory_stress_test.sh
│ ├── network_diagnostics.sh
│ ├── network_quick_fix.sh
│ ├── network_speed_test.sh
│ ├── quick_repair.sh
│ ├── system_overview.sh
│ ├── system_report.sh
│ └── tech_support_mode.sh
└── webui
├── main.py
├── static
│ ├── banner.png
│ ├── output.js
│ ├── styles.css
│ └── styles.stable.css
├── templates
│ ├── base.html
│ ├── index.html
│ ├── index.stable.html
│ └── output.html

---

## How It Works

### 1. Scripts  
All diagnostics are handled by Bash scripts.  
FastAPI executes them and streams the output back to the UI.

Each script is standalone, POSIX-friendly, and safe to run in live or installed environments.

### 2. WebUI  
FastAPI app (`webui/main.py`) serves the interface.  
Templates use clean HTML with dark synthwave CSS.  
Neon cyan accent colors match the system branding.

### 3. Branding & Boot Themes  
Branding images live in `branding/`, and the autobranding script pushes them to:  
• Plymouth boot theme  
• Desktop banner  
• WebUI  
• Desktop icon

---

## Build Instructions (Penguin-Eggs)

git clone https://github.com/pieroproietti/fresh-eggs
cd fresh-eggs
sudo ./fresh-eggs.sh
eggs love -n

Resulting ISO appears in:
/home/eggs/

The ISO includes the full DiagnostiX Lite environment.

---

## License

This project is licensed under the MIT License.  
See `LICENSE` for full details.

MIT TLDR:  
• You can use, modify, distribute, and sell it  
• Just include the same license in your builds  
• No liability or warranty

---

## GitKon Submission Notes

DiagnostiX Lite qualifies for the **Developer Passion Project** category.  
Key criteria it satisfies:  
• Helps devs ship code faster (health reports, repo scanner, quick logs)  
• Technical originality (auto-branding, integrated diagnostics, repo integrity scanner)  
• Clear 5-minute demo scope  
• Started after June 2025  
• Git-themed tooling included (Kraken repo scanner)

---

## Future Plans

• Add GitOps-driven repair mode  
• More advanced repo integrity logic  
• Dockerized WebUI  
• Plug-in script system  
• Better Plymouth animations  
• Cross-platform log uploader

---

If you’re testing, building, or repairing systems all day, DiagnostiX Lite removes friction and gets you straight to the answers.

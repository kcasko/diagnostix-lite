# DiagnostiX Lite  
A Developer-Focused Diagnostic OS • Built for Speed, Clarity, and Insight

DiagnostiX Lite is a custom Ubuntu-based diagnostic environment designed for developers, system builders, and IT professionals who need fast, clear insight into system behavior and Git repository health. It packages hardware checks, system overviews, Git repo scanning, and a clean web-based control panel into a single unified desktop experience.

This project began in mid-2025 and continues to evolve as a lightweight tool for rapid diagnosis, repo integrity checks, and streamlined debugging in virtual machines, live environments, and repair shops.

---

## Features

### Web-Based Control Panel (FastAPI)
A clean dashboard accessible at:
```
http://127.0.0.1:8080/
```

Includes:  
• System overview  
• Hardware health tools  
• Repo scanning utilities  
• Network diagnostics  
• Storage information  

Everything is organized into horizontal tabs for quick navigation.

---

### Git Repository Scanner
DiagnostiX Lite includes a repository scanner that crawls the system for Git repos and reports:  
• Current branch  
• Last commit  
• Untracked files  
• Merge conflicts  
• Repo integrity  
• Dirty/uncommitted status  

Perfect for developers debugging project layouts or verifying repo health in unfamiliar systems.

---

### Autobranding Engine
DiagnostiX Lite includes an automated theming script that applies:  
• Desktop wallpaper  
• Login wallpaper  
• Icon set  
• Boot splash (Plymouth)  
• Brand directory syncing  

All branding is stored under:

```
/opt/diagnostix/branding/
```

To rebrand the entire OS instantly:

```
sudo /opt/diagnostix/scripts/autobrand.sh
```

---

### Hardware & System Diagnostics
Built-in tools include:  
• Hardware health checks  
• System overview  
• Memory and swap reporting  
• Storage tree mapping  
• Network diagnostics  
• VM-specific insights  

Everything can be run from the control panel or from `scripts/`.

---

### Custom Branding & Neon Aesthetic
DiagnostiX Lite features a dark neon palette inspired by synthwave and cyber-utility UIs:  
• Custom wallpapers  
• Custom boot splash assets  
• DX icon branding  
• Widescreen header banner  

All assets are included in the repo under `branding/`.

---

## Folder Structure

```
diagnostix-lite/
│
├── branding/
│   ├── banner.png
│   ├── icon.png
│   └── wallpapers/
│       ├── boot.png
│       ├── desktop.png
│       └── login.png
│
├── scripts/
│   ├── autobrand.sh
│   ├── system_overview.sh
│   ├── repo_scanner.sh
│   ├── hardware_health.sh
│   └── network_diagnostics.sh
│
├── webui/
│   ├── main.py
│   ├── static/
│   └── templates/
│
└── docs/
    └── screenshots/
```

---

## Requirements
DiagnostiX Lite currently runs best inside:  
• VMware Workstation  
• VirtualBox  
• Bare-metal Debian/Ubuntu installations  

The included scripts are POSIX-compatible and run on any Debian-derived environment.

---

## Roadmap
Planned improvements:  
• Improved live ISO generation compatibility  
• Additional diagnostic modules  
• GitKraken integration helpers  
• Modular plugin architecture  
• Remote diagnostics toolkit  

---

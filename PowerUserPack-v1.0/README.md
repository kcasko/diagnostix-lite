====================================
TAURUSTECH POWER USER PACK
README v1.0

The Power User Pack is a streamlined Windows toolkit built for fast fixes, clean diagnostics, and proper maintenance. Nothing here is guesswork. Nothing is shady. Everything is open, readable, and designed to help you understand and control your system instead of fighting it.

This kit is built to be portable, modular, and reliable whether you're repairing your own machine or helping someone else dig out of a mess.

====================================
FOLDER STRUCTURE

Root
TaurusTech.bat
Main launcher for the entire toolkit. Directs you into Quick Scripts, Checklists, Config Tweaks, Workflow Guides, and Utilities.

TaurusTech-Launcher.bat
Quick Scripts launcher. Runs all the cleanup, resets, and diagnostic scripts from a single menu.

01-Quick-Scripts
Rapid repair tools that fix common Windows issues in seconds.

02-Checklists
Maintenance routines and setup lists.

03-Config-Tweaks
Registry and tweak scripts to fix or improve Windows behavior.

04-Workflow-Guides
Plain English troubleshooting guides.

05-Utilities
Diagnostics like hashing, GPU info, port scanning, and memory checks.

====================================
ROOT LAUNCHER BEHAVIOR

TaurusTech.bat is the command center.
It loads a clean menu that routes you to the correct module.
Option 1 calls the Quick Scripts launcher.
Everything else opens the proper folder.

TaurusTech-Launcher.bat handles all Quick Script execution.
It lives in the root on purpose.
The main launcher points directly to it.

====================================
QUICK SCRIPTS

cleanup_startup.bat
Removes unnecessary startup entries to speed boot time.

clean_temp.bat
Clears all temp directories for fast disk cleanup.

disable_bloat_services.bat
Disables low value services that slow Windows down.

kill_process.bat
Kills a specified process by name.

kill_process.ps1
PowerShell version that hits stubborn tasks harder.

network_adapter_dump.ps1
Prints adapter configuration for troubleshooting.

network_core_reset.ps1
Deep network reset including Winsock and TCP stack.

network_reset.bat
Safer, lighter network repair.

system_info_snapshot.bat
OS, CPU, RAM, patches, uptime, everything.

TaurusTech_Service_Disabler.ps1
Your curated service disabler that avoids breaking normal use.

====================================
CHECKLISTS

Daily Maintenance
Quick tasks to keep the system behaving.

Monthly Maintenance
Deeper cleanup and performance checks.

Fresh Install Checklist
Everything a clean Windows install should have done the right way.

====================================
CONFIG TWEAKS

ContextMenu_old.reg
Restores the full right click menu in Windows 11.

Disable_Bing_Search.reg
Removes Bing from the Start menu search.

Enable_LongPaths.reg
Allows longer file paths beyond 260 chars.

PowerTweaks.bat
Batch driven quality of life tweaks.

====================================
WORKFLOW GUIDES

How to Identify Spyware or Bloat
Spot suspicious apps and high impact services.

How to Reset Network Safely
Light reset vs full reset explained.

Safe Driver Update Guide
How to update drivers without bricking your system.

====================================
UTILITIES

get_gpu_info.cmd
GPU and driver information.

TaurusTech-FileHash.ps1
Creates MD5, SHA1, and SHA256 hashes.

TaurusTech-PortScan.ps1
Scans local open ports.

TaurusTech-RAMTest.bat
Light RAM testing to detect early failures.
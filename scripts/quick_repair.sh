#!/bin/bash

LOG_DIR="/opt/diagnostix/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/quickrepair_$(date +%Y-%m-%d_%H-%M-%S).log"

log() {
    echo "$1" | tee -a "$LOG_FILE"
}

section() {
    log ""
    log "-- $1 --"
}

log "=== DiagnostiX Quick Repair ==="
log "Log file: $LOG_FILE"
log ""

# ----------------------------------------------------
section "Fixing broken packages"
# Suppress apt warnings, use apt-get instead of apt
APT="apt-get -o=Dpkg::Use-Pty=0 -o=Acquire::Retries=3"

$APT update -y >>"$LOG_FILE" 2>&1
$APT install -f -y >>"$LOG_FILE" 2>&1
$APT autoremove -y >>"$LOG_FILE" 2>&1

log "Package repair complete."

# ----------------------------------------------------
section "Cleaning apt cache"
$APT clean >>"$LOG_FILE" 2>&1
log "Apt cache cleaned."

# ----------------------------------------------------
section "Checking fstab"
cat /etc/fstab | tee -a "$LOG_FILE"

# ----------------------------------------------------
section "Checking mounted disks"
df -h | tee -a "$LOG_FILE"

# ----------------------------------------------------
section "Checking disk health (if available)"
# Try smartctl if installed
if command -v smartctl >/dev/null 2>&1; then
    smartctl --health --info /dev/sda 2>/dev/null | tee -a "$LOG_FILE"
else
    log "smartctl not installed"
fi

# ----------------------------------------------------
section "Checking for read-only filesystems"
mount | grep "(ro," | tee -a "$LOG_FILE"
if mount | grep -q "(ro,"; then
    log "Warning: One or more filesystems are read-only."
else
    log "All mounted filesystems are writable."
fi

# ----------------------------------------------------
section "Checking load average"
uptime | tee -a "$LOG_FILE"

# ----------------------------------------------------
section "Checking system journal for recent errors"
journalctl -p 3 -n 10 --no-pager 2>/dev/null | tee -a "$LOG_FILE"

# ----------------------------------------------------
log ""
log "Quick Repair complete."
log "Log saved to: $LOG_FILE"
log ""

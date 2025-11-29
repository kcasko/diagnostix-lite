#!/bin/bash

LOG_DIR="/opt/diagnostix/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/bootdiag_$(date +%Y-%m-%d_%H-%M-%S).log"

log() {
    echo "$1" | tee -a "$LOG_FILE"
}

section() {
    log ""
    log "-- $1 --"
}

log "=== DiagnostiX Boot Diagnostics ==="
log "Log file: $LOG_FILE"
log ""

# --------------------------------------------------------
section "Boot mode detection"

if [ -d /sys/firmware/efi ]; then
    log "System booted in UEFI mode."
else
    log "System booted in legacy BIOS mode."
fi

# --------------------------------------------------------
section "Boot loader filesystems"
lsblk -f | tee -a "$LOG_FILE"

# --------------------------------------------------------
section "blkid summary"
blkid | tee -a "$LOG_FILE"

# --------------------------------------------------------
section "EFI boot entries"
if [ -d /sys/firmware/efi ]; then
    if command -v efibootmgr >/dev/null 2>&1; then
        efibootmgr | tee -a "$LOG_FILE"
    else
        log "efibootmgr not installed."
    fi
else
    log "EFI not supported (BIOS system). Skipping EFI boot entries."
fi

# --------------------------------------------------------
section "fstab (non commented)"
grep -v "^#" /etc/fstab | tee -a "$LOG_FILE"

# --------------------------------------------------------
section "Kernel command line"
cat /proc/cmdline | tee -a "$LOG_FILE"

# --------------------------------------------------------
section "Recent boot log (journalctl -b | tail)"
journalctl -b -n 20 --no-pager 2>/dev/null | tee -a "$LOG_FILE"

log ""
log "Boot diagnostics complete."
log "Log saved to: $LOG_FILE"
log ""

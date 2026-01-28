#!/bin/bash

LOG_DIR="./logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/gpudiag_$(date +%Y-%m-%d_%H-%M-%S).log"

log() {
    echo "$1" | tee -a "$LOG_FILE"
}

section() {
    log ""
    log "-- $1 --"
}

log "=== DiagnostiX GPU Diagnostics ==="
log "Log file: $LOG_FILE"
log ""

# ----------------------------------------------------
section "PCI GPU devices"
lspci | grep -Ei "vga|3d|display" | tee -a "$LOG_FILE"

# ----------------------------------------------------
section "Kernel modules (video related)"
lsmod | grep -Ei "nvidia|amdgpu|radeon|vmwgfx|i915" | tee -a "$LOG_FILE"

# ----------------------------------------------------
section "Driver summary"
if lsmod | grep -q nvidia; then
    log "NVIDIA driver loaded (nvidia kernel module detected)"
elif lsmod | grep -q amdgpu; then
    log "AMD GPU driver loaded (amdgpu)"
elif lsmod | grep -q radeon; then
    log "Legacy AMD/ATI driver (radeon)"
elif lsmod | grep -q i915; then
    log "Intel GPU driver (i915)"
elif lsmod | grep -q vmwgfx; then
    log "VMware virtual GPU detected (vmwgfx)"
else
    log "No known GPU kernel driver detected."
fi

# ----------------------------------------------------
section "nvidia-smi check"
if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi | tee -a "$LOG_FILE"
else
    log "nvidia-smi not found (no NVIDIA GPU or driver)."
fi

# ----------------------------------------------------
section "OpenGL check (headless-safe)"
if command -v glxinfo >/dev/null 2>&1; then
    if [ -n "$DISPLAY" ]; then
        glxinfo | grep "OpenGL" | tee -a "$LOG_FILE"
    else
        log "glxinfo found, but no DISPLAY. Skipping OpenGL tests (headless environment)."
    fi
else
    log "glxinfo not installed."
fi

# ----------------------------------------------------
log ""
log "GPU diagnostics complete."
log "Log saved to: $LOG_FILE"
log ""

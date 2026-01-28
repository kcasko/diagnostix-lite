#!/bin/bash

LOG_DIR="./logs"
SCRIPTS_DIR="/opt/diagnostix/scripts"

mkdir -p "$LOG_DIR"

TS="$(date +'%Y%m%d_%H%M%S')"
OUT="$LOG_DIR/diagnostix_collect_${TS}.log"
TAR="$LOG_DIR/diagnostix_collect_${TS}.tar.gz"

run_section() {
  local title="$1"
  shift
  echo "=== ${title} ===" | tee -a "$OUT"
  if command -v "$1" >/dev/null 2>&1 || [[ -x "$1" ]]; then
    "$@" 2>&1 | tee -a "$OUT"
  else
    echo "Command or script not found: $1" | tee -a "$OUT"
  fi
  echo | tee -a "$OUT"
}

echo "DiagnostiX Full Collection - ${TS}" | tee -a "$OUT"
echo | tee -a "$OUT"

[ -x "$SCRIPTS_DIR/system_overview.sh" ]       && run_section "System overview"       "$SCRIPTS_DIR/system_overview.sh"
[ -x "$SCRIPTS_DIR/hardware_health.sh" ]       && run_section "Hardware health"       "$SCRIPTS_DIR/hardware_health.sh"
[ -x "$SCRIPTS_DIR/disk_diagnostics.sh" ]      && run_section "Disk diagnostics"      "$SCRIPTS_DIR/disk_diagnostics.sh"
[ -x "$SCRIPTS_DIR/network_diagnostics.sh" ]   && run_section "Network diagnostics"   "$SCRIPTS_DIR/network_diagnostics.sh"
[ -x "$SCRIPTS_DIR/memory_stress_test.sh" ]    && run_section "Memory stress test"    "$SCRIPTS_DIR/memory_stress_test.sh"
[ -x "$SCRIPTS_DIR/cpu_stress_test.sh" ]       && run_section "CPU stress test"       "$SCRIPTS_DIR/cpu_stress_test.sh"
[ -x "$SCRIPTS_DIR/network_speed_test.sh" ]    && run_section "Network speed test"    "$SCRIPTS_DIR/network_speed_test.sh"
[ -x "$SCRIPTS_DIR/quick_repair.sh" ]          && run_section "Quick repair"          "$SCRIPTS_DIR/quick_repair.sh"
[ -x "$SCRIPTS_DIR/gpu_diagnostics.sh" ]       && run_section "GPU diagnostics"       "$SCRIPTS_DIR/gpu_diagnostics.sh"
[ -x "$SCRIPTS_DIR/boot_diagnostics.sh" ]      && run_section "Boot diagnostics"      "$SCRIPTS_DIR/boot_diagnostics.sh"

echo "Collecting extra logs" | tee -a "$OUT"
echo | tee -a "$OUT"

echo "=== dmesg ==="        | tee -a "$OUT"
dmesg 2>&1                  | tee -a "$OUT"
echo                        | tee -a "$OUT"

echo "=== journalctl -xb ===" | tee -a "$OUT"
journalctl -xb 2>&1          | tee -a "$OUT"
echo                          | tee -a "$OUT"

tar czf "$TAR" -C "$LOG_DIR" "$(basename "$OUT")" 2>/dev/null

echo "Log file: $OUT"
echo "Bundle:   $TAR"

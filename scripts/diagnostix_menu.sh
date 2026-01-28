#!/bin/bash

SCRIPTS_DIR="/opt/diagnostix/scripts"

run_if_exists() {
  local script="$1"
  if [ -x "$SCRIPTS_DIR/$script" ]; then
    sudo "$SCRIPTS_DIR/$script"
  else
    echo "Script not found or not executable: $SCRIPTS_DIR/$script"
  fi
}

while true; do
  clear
  echo "=== DiagnOStiX Menu ==="
  echo
  echo "1) System overview"
  echo "2) Hardware health"
  echo "3) Disk diagnostics"
  echo "4) Network diagnostics"
  echo "5) Memory stress test"
  echo "6) CPU stress test"
  echo "7) Network speed test"
  echo "8) Quick repair"
  echo "9) GPU diagnostics"
  echo "10) Boot diagnostics"
  echo "11) Full collection and log bundle"
  echo "12) Exit"
  echo
  read -rp "Choose an option: " choice

  case "$choice" in
    1)  run_if_exists "system_overview.sh" ;;
    2)  run_if_exists "hardware_health.sh" ;;
    3)  run_if_exists "disk_diagnostics.sh" ;;
    4)  run_if_exists "network_diagnostics.sh" ;;
    5)  run_if_exists "memory_stress_test.sh" ;;
    6)  run_if_exists "cpu_stress_test.sh" ;;
    7)  run_if_exists "network_speed_test.sh" ;;
    8)  run_if_exists "quick_repair.sh" ;;
    9)  run_if_exists "gpu_diagnostics.sh" ;;
    10) run_if_exists "boot_diagnostics.sh" ;;
    11) run_if_exists "master_collect.sh" ;;
    12) echo "Bye."; exit 0 ;;
    *)  echo "Invalid choice." ;;
  esac

  echo
  read -rp "Press Enter to return to the menu" _
done

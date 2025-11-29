#!/bin/bash

SCRIPTS="/opt/diagnostix/scripts"
TMP="/tmp/diagnostix_output.txt"

run_script() {
    local script="$1"

    if [ -x "$SCRIPTS/$script" ]; then
        # capture script output
        sudo "$SCRIPTS/$script" > "$TMP" 2>&1

        # display output in a scrollable textbox
        dialog --title "$script Output" \
               --textbox "$TMP" 30 120 \
               --scrolltext
    else
        dialog --msgbox "Script not found or not executable: $SCRIPTS/$script" 8 50
    fi
}

while true; do
    CHOICE=$(dialog --clear --stdout \
        --title "DiagnostiX Control Panel" \
        --menu "Select a diagnostic tool or action." 20 70 15 \
        1 "System overview" \
        2 "Hardware health" \
        3 "Disk diagnostics" \
        4 "Network diagnostics" \
        5 "Memory stress test" \
        6 "CPU stress test" \
        7 "Network speed test" \
        8 "Quick repair" \
        9 "GPU diagnostics" \
        10 "Boot diagnostics" \
        11 "Full log collection bundle" \
        12 "Tech Support Mode (Run Everything)" \
        13 "Exit DiagnostiX")

    [ $? -ne 0 ] && clear && exit 0

    case "$CHOICE" in
        1)  run_script "system_overview.sh" ;;
        2)  run_script "hardware_health.sh" ;;
        3)  run_script "disk_diagnostics.sh" ;;
        4)  run_script "network_diagnostics.sh" ;;
        5)  run_script "memory_stress_test.sh" ;;
        6)  run_script "cpu_stress_test.sh" ;;
        7)  run_script "network_speed_test.sh" ;;
        8)  run_script "quick_repair.sh" ;;
        9)  run_script "gpu_diagnostics.sh" ;;
        10) run_script "boot_diagnostics.sh" ;;
        11) run_script "master_collect.sh" ;;
        12) run_script "tech_support_mode.sh" ;;
        13) clear; exit 0 ;;
    esac
done

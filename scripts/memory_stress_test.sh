#!/bin/bash

LOG_DIR="./logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/memorytest_$(date +%Y-%m-%d_%H-%M-%S).log"

echo "=== DiagnostiX Memory Stress Test ==="
echo
echo "Using: memtester 512M 1"
echo "This will run a basic RAM stress pattern."
echo
echo "Logging results to: $LOG_FILE"
echo

# Run memtester and filter out backspaces, carriage returns, and spinner animations
memtester 512M 1 2>&1 \
    | sed 's/.\x08//g' \
    | sed 's/\r//g' \
    | tee "$LOG_FILE"

echo
echo "Memory test complete."
echo "Log saved to: $LOG_FILE"
echo

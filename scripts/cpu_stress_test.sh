#!/bin/bash
echo "=== DiagnostiX CPU Stress Test ==="
echo
sudo apt-get install -y stress-ng 2>/dev/null
sudo stress-ng --cpu 4 --timeout 30s --metrics-brief

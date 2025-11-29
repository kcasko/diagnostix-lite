#!/bin/bash
echo "=== DiagnostiX Hardware Health Report ==="
echo
echo "-- CPU Info --"
lscpu
echo
echo "-- Memory Info --"
free -h
echo
echo "-- SMART Scans --"
smartctl --scan | while read disk _; do
echo; echo "SMART Data for $disk";
smartctl -H "$disk";
done
echo
echo "-- Sensors --"
sensors 2>/dev/null || echo "No sensors available"

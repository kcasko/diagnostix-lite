#!/bin/bash
echo "=== DiagnostiX Disk Diagnostics ==="
echo
echo "-- lsblk --"
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT
echo
echo "-- Partition Tables --"
for d in /dev/sd?; do
echo; echo "$d:"
sudo parted "$d" print 2>/dev/null
done
echo
echo "-- SMART Health --"
smartctl --scan | while read disk _; do
echo; echo "SMART Health for $disk:"
smartctl -H "$disk"
done

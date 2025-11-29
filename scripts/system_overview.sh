#!/bin/bash
echo "=== DiagnostiX System Overview ==="
echo
inxi -Fxx
echo
echo "Kernel Modules:"
lsmod | head -20
echo
echo "Mounted Filesystems:"
df -h

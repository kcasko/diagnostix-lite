#!/bin/bash
echo "DiagnostiX Report"
inxi -Fxx
smartctl --scan
df -h

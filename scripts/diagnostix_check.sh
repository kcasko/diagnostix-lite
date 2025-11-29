#!/bin/bash
echo "DiagnostiX Pre-Build Check"
echo "Tools:"
command -v inxi
command -v gparted
command -v smartctl
command -v testdisk
echo
echo "Directories:"
ls /opt/diagnostix

#!/bin/bash

echo "=== DiagnostiX Network Quick Fix ==="
echo

echo "Rebuilding DNS resolver..."

# Force overwrite as root
sudo rm -f /etc/resolv.conf
echo "nameserver 1.1.1.1" | sudo tee /etc/resolv.conf >/dev/null
echo "nameserver 8.8.8.8" | sudo tee -a /etc/resolv.conf >/dev/null

echo "DNS repaired."
echo

echo
echo "Restarting networking if possible..."

sudo systemctl daemon-reload

if systemctl list-unit-files | grep -q NetworkManager; then
    sudo systemctl restart NetworkManager
elif systemctl list-unit-files | grep -q networking; then
    sudo systemctl restart networking
else
    echo "No restartable networking services found."
fi


#!/bin/bash

BASE_DIR="/opt/diagnostix/logs"
TS="$(date +'%Y%m%d_%H%M%S')"
BUNDLE_DIR="${BASE_DIR}/bundle_${TS}"

mkdir -p "$BUNDLE_DIR"

echo "=== DiagnostiX Log Collector ==="
echo "Saving bundle to: $BUNDLE_DIR"
echo

cp /var/log/syslog "$BUNDLE_DIR/" 2>/dev/null
cp /var/log/kern.log "$BUNDLE_DIR/" 2>/dev/null
cp /var/log/dmesg "$BUNDLE_DIR/" 2>/dev/null

dmesg > "$BUNDLE_DIR/dmesg_live.log" 2>&1
journalctl -xb > "$BUNDLE_DIR/journalctl_xb.log" 2>&1 || true

cp /etc/fstab "$BUNDLE_DIR/fstab" 2>/dev/null || true
cp /etc/os-release "$BUNDLE_DIR/os-release" 2>/dev/null || true

tar czf "${BUNDLE_DIR}.tar.gz" -C "$BASE_DIR" "bundle_${TS}" 2>/dev/null

echo "Log bundle created:"
echo "  Directory: $BUNDLE_DIR"
echo "  Archive:   ${BUNDLE_DIR}.tar.gz"

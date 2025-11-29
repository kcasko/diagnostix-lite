#!/bin/bash

SCRIPTS="/opt/diagnostix/scripts"
LOGS="/opt/diagnostix/logs"

mkdir -p "$LOGS"

TS="$(date +'%Y%m%d_%H%M%S')"
OUT="$LOGS/techsupport_${TS}.log"
BUNDLE="$LOGS/techsupport_${TS}.tar.gz"
TMPDIR="$LOGS/techsupport_${TS}"

mkdir -p "$TMPDIR"

echo "=== DiagnostiX Tech Support Mode ===" | tee -a "$OUT"
echo "Timestamp: $TS" | tee -a "$OUT"
echo | tee -a "$OUT"

# Run master collection first
if [ -x "$SCRIPTS/master_collect.sh" ]; then
    echo "Running full diagnostics..." | tee -a "$OUT"
    "$SCRIPTS/master_collect.sh" | tee -a "$OUT"
else
    echo "ERROR: master_collect.sh missing or not executable" | tee -a "$OUT"
fi

echo | tee -a "$OUT"
echo "Collecting extended logs..." | tee -a "$OUT"

cp /var/log/syslog "$TMPDIR/" 2>/dev/null
cp /var/log/kern.log "$TMPDIR/" 2>/dev/null
cp /etc/fstab "$TMPDIR/" 2>/dev/null
cp /etc/os-release "$TMPDIR/" 2>/dev/null

journalctl -xb > "$TMPDIR/journalctl_xb.log" 2>/dev/null
dmesg > "$TMPDIR/dmesg_live.log" 2>/dev/null

# Copy the output from master_collect
cp "$OUT" "$TMPDIR/" 2>/dev/null

# Create bundle
tar czf "$BUNDLE" -C "$LOGS" "techsupport_${TS}"

echo | tee -a "$OUT"
echo "Tech support bundle created:" | tee -a "$OUT"
echo "  $BUNDLE" | tee -a "$OUT"
echo
echo "You can now send this file to support." | tee -a "$OUT"

#!/bin/bash

echo "=== Network Speed Test ==="
echo
echo "Preparing speed test..."
echo "Warming up network stack..."
echo
sleep 1

DOWNLOAD_URL="http://ipv4.download.thinkbroadband.com/100MB.zip"

echo "Selecting best download server..."
echo
sleep 1

echo "Testing: $DOWNLOAD_URL"
echo

TMP_FILE=$(mktemp)

# -----------------------------
# DOWNLOAD TEST USING CURL
# -----------------------------
DOWNLOAD_SPEED_BYTES=$(
    curl -o /dev/null -s -w "%{speed_download}" "$DOWNLOAD_URL"
)

if [[ -z "$DOWNLOAD_SPEED_BYTES" || "$DOWNLOAD_SPEED_BYTES" == "0" ]]; then
    DL_MBPS="Unknown"
    DL_MB="Unknown"
else
    DL_MB=$(awk -v b="$DOWNLOAD_SPEED_BYTES" 'BEGIN { printf("%.1f", b / 1000000) }')
    DL_MBPS=$(awk -v b="$DOWNLOAD_SPEED_BYTES" 'BEGIN { printf("%.1f", b * 8 / 1000000) }')
fi

echo "=== RESULT ==="
echo "Download source: $DOWNLOAD_URL"
echo "Approximate download speed: $DL_MB MB/s"
echo "Approximate download speed (Mbps): $DL_MBPS Mbps"
echo

# -----------------------------
# UPLOAD TEST
# -----------------------------
echo "Running upload test (20MB)..."
echo

UPLOAD_TMP=$(mktemp)
dd if=/dev/zero of="$UPLOAD_TMP" bs=1M count=20 2>/dev/null

UPLOAD_SPEED_BYTES=$(curl -s -w "%{speed_upload}" -o /dev/null \
    -X POST \
    -H "Content-Type: application/octet-stream" \
    --data-binary @"$UPLOAD_TMP" \
    "https://clients3.google.com/upload/chromewebstore")

rm "$UPLOAD_TMP"

if [[ -z "$UPLOAD_SPEED_BYTES" || "$UPLOAD_SPEED_BYTES" == "0" ]]; then
    UP_MBPS="Unknown"
else
    UP_MBPS=$(awk -v b="$UPLOAD_SPEED_BYTES" 'BEGIN { printf("%.1f", b * 8 / 1000000) }')
fi

echo "Approximate upload speed: $UP_MBPS Mbps"
echo
echo "--- Raw Output ---"
echo "curl reported download bytes/s: $DOWNLOAD_SPEED_BYTES"
echo "curl reported upload bytes/s: $UPLOAD_SPEED_BYTES"

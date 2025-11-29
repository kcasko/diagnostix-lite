#!/bin/bash

LOG_DIR="/opt/diagnostix/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/network_$(date +%Y-%m-%d_%H-%M-%S).log"

log() {
    echo "$1" | tee -a "$LOG_FILE"
}

section() {
    log ""
    log "-- $1 --"
}

log "=== DiagnostiX Network Diagnostics ==="
log "Log saved to: $LOG_FILE"
log ""

section "Interfaces"
ip a | tee -a "$LOG_FILE"

section "Routing Table"
ip route | tee -a "$LOG_FILE"

section "DNS Servers"
if [ -f /etc/resolv.conf ]; then
    cat /etc/resolv.conf | tee -a "$LOG_FILE"
    log "DNS config loaded"
else
    log "No resolv.conf found"
fi

section "Gateway Reachability"
GATEWAY=$(ip route | awk '/default/ {print $3}')

if [ -n "$GATEWAY" ]; then
    log "Pinging gateway at $GATEWAY..."
    if ping -c 2 "$GATEWAY" >/dev/null 2>&1; then
        log "Gateway reachable"
        ping -c 2 "$GATEWAY" | tee -a "$LOG_FILE"
    else
        log "Gateway unreachable"
    fi
else
    log "No default gateway found"
fi

section "Ping by IP (1.1.1.1)"
if ping -c 2 1.1.1.1 >/dev/null 2>&1; then
    log "Ping to 1.1.1.1 OK"
    ping -c 2 1.1.1.1 | tee -a "$LOG_FILE"
else
    log "Ping to 1.1.1.1 FAILED"
fi

section "Ping by Domain (one.one.one.one)"
DOMAIN_IP=$(getent hosts one.one.one.one | awk '{print $1}')
if [ -n "$DOMAIN_IP" ]; then
    log "Resolved to: $DOMAIN_IP"
fi

if ping -c 2 one.one.one.one >/dev/null 2>&1; then
    log "Domain ping OK"
    ping -c 2 one.one.one.one | tee -a "$LOG_FILE"
else
    log "Domain ping FAILED"
fi

section "HTTP Connectivity (example.com)"
if command -v curl >/dev/null 2>&1; then
    if curl -s -I --max-time 5 http://example.com >/dev/null 2>&1; then
        log "HTTP request OK"
        curl -s -I --max-time 5 http://example.com | tee -a "$LOG_FILE"
    else
        log "HTTP request FAILED"
    fi
else
    log "curl not installed"
fi

section "Traceroute (one.one.one.one)"
if command -v traceroute >/dev/null 2>&1; then
    traceroute -m 5 one.one.one.one | tee -a "$LOG_FILE"
else
    log "traceroute not installed"
fi

section "Active Connections"
ss -tulnp | tee -a "$LOG_FILE"

log ""
log "Diagnostics complete."
log "Saved log file: $LOG_FILE"
log ""

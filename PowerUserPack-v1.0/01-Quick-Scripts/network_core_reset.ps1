param(
    [string]$LogPath
)

# Build default log path if not supplied
if (-not $LogPath -or $LogPath.Trim() -eq "") {
    $LogRoot = Join-Path $env:USERPROFILE "Desktop\TaurusTech-Logs"
    if (-not (Test-Path $LogRoot)) {
        New-Item -Path $LogRoot -ItemType Directory | Out-Null
    }
    $LogPath = Join-Path $LogRoot "network_reset_log.txt"
} else {
    # Ensure folder exists when passed in
    $LogRoot = Split-Path $LogPath
    if (-not (Test-Path $LogRoot)) {
        New-Item -Path $LogRoot -ItemType Directory | Out-Null
    }
}

# Simple helper to append lines to log
function Write-Log {
    param([string]$Text)
    Add-Content -Path $LogPath -Value $Text
}

$timeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Ensure log file exists
if (-not (Test-Path $LogPath)) {
    "" | Out-File -FilePath $LogPath -Encoding UTF8
}

Write-Log ""
Write-Log "TaurusTech Network Reset Log"
Write-Log "Generated: $timeStamp"
Write-Log ""
Write-Log "============================================="
Write-Log "  Core network reset section"
Write-Log "============================================="
Write-Log ""
Write-Log "Resetting core network components..."
Write-Log "-------------------------------------"
Write-Log ""


# Step: Flush DNS
Write-Log "[FLUSH DNS]"
try {
    (ipconfig /flushdns 2>&1) | Out-String | Write-Log
} catch {
    Write-Log "Error: $($_.Exception.Message)"
}
Write-Log ""


# Step: Winsock reset
Write-Log "[NETSH WINSOCK RESET]"
try {
    (netsh winsock reset 2>&1) | Out-String | Write-Log
} catch {
    Write-Log "Error: $($_.Exception.Message)"
}
Write-Log ""


# Step: IP reset
Write-Log "[NETSH INT IP RESET]"
try {
    (netsh int ip reset 2>&1) | Out-String | Write-Log
} catch {
    Write-Log "Error: $($_.Exception.Message)"
}
Write-Log ""


# Step: Firewall reset
Write-Log "[NETSH ADVFIREWALL RESET]"
try {
    (netsh advfirewall reset 2>&1) | Out-String | Write-Log
} catch {
    Write-Log "Error: $($_.Exception.Message)"
}
Write-Log ""


# Step: Release IP
Write-Log "[IPCONFIG /RELEASE]"
try {
    (ipconfig /release 2>&1) | Out-String | Write-Log
} catch {
    Write-Log "Error: $($_.Exception.Message)"
}
Write-Log ""


# Step: Renew IP
Write-Log "[IPCONFIG /RENEW]"
try {
    (ipconfig /renew 2>&1) | Out-String | Write-Log
} catch {
    Write-Log "Error: $($_.Exception.Message)"
}
Write-Log ""


# Step: Full snapshot
Write-Log "[IPCONFIG /ALL SNAPSHOT]"
try {
    (ipconfig /all 2>&1) | Out-String | Write-Log
} catch {
    Write-Log "Error: $($_.Exception.Message)"
}
Write-Log ""

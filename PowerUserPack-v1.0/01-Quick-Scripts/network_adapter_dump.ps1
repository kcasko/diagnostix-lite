param(
    [string]$LogPath
)

function Write-Log {
    param([string]$Text)
    Add-Content -Path $LogPath -Value $Text
}

if (-not $LogPath) {
    $LogPath = "$env:USERPROFILE\Desktop\network_reset_log.txt"
}

if (-not (Test-Path $LogPath)) {
    "" | Out-File -FilePath $LogPath -Encoding UTF8
}

Write-Log ""
Write-Log "============================================="
Write-Log "SORTED ADAPTER SUMMARY"
Write-Log "============================================="
Write-Log ""

Write-Host "Adapter summary (status then speed):"
Write-Host ""

try {
    $adaptersRaw = Get-NetAdapter
} catch {
    $msg = "Get-NetAdapter failed: $($_.Exception.Message)"
    Write-Host $msg
    Write-Log $msg
    return
}

$adapters = foreach ($a in $adaptersRaw) {

    $numericSpeed = 0
    if ($a.LinkSpeed -match '(\d+)\s*Gbps') {
        $numericSpeed = [int]$matches[1] * 1000
    } elseif ($a.LinkSpeed -match '(\d+)\s*Mbps') {
        $numericSpeed = [int]$matches[1]
    }

    [pscustomobject]@{
        Name      = $a.Name
        Status    = $a.Status
        Speed     = $a.LinkSpeed
        MAC       = $a.MacAddress
        SortSpeed = $numericSpeed
        RawObj    = $a
    }
}

$adapters = $adapters | Sort-Object Status, SortSpeed

foreach ($a in $adapters) {
    $line = "{0,-28} {1,-12} {2,-12} {3}" -f $a.Name, $a.Status, $a.Speed, $a.MAC
    Write-Host $line
    Write-Log $line
}

Write-Log ""
Write-Log "FULL ADAPTER DETAIL (Get-NetAdapter | Format-List *):"
Write-Log ""

$baseDir   = Split-Path $LogPath
$detailDir = Join-Path $baseDir "network_adapters"

if (-not (Test-Path $detailDir)) {
    New-Item -Path $detailDir -ItemType Directory | Out-Null
}

foreach ($a in $adapters) {

    $safeName = $a.Name -replace '[\\/:*?"<>|]', '_'
    $filePath = Join-Path $detailDir ("{0}.txt" -f $safeName)

    try {
        $detail = $a.RawObj | Format-List * | Out-String
        $header = "===== Adapter: {0} ({1}) =====" -f $a.Name, $a.MAC

        $header | Out-File -FilePath $filePath -Encoding UTF8
        $detail | Out-File -FilePath $filePath -Encoding UTF8 -Append

        # Write to main log with preserved newlines
        Write-Log $header
        foreach ($line in $detail -split "`r?`n") {
            Write-Log $line
        }
        Write-Log ""

    } catch {
        $msg = "Failed to write detail file for adapter {0}: {1}" -f $a.Name, $_.Exception.Message
        Write-Host $msg
        Write-Log $msg
    }
}

try {
    $zipPath = Join-Path $baseDir "network_adapters.zip"
    if (Test-Path $zipPath) { Remove-Item $zipPath -Force }

    Compress-Archive -Path (Join-Path $detailDir "*") -DestinationPath $zipPath -Force

    Write-Log ""
    Write-Log "Adapter detail files archived to:"
    Write-Log "  $zipPath"

} catch {
    Write-Log "Failed to create adapter detail zip: $($_.Exception.Message)"
}

Write-Host ""
Write-Host "Detailed adapter information appended to:"
Write-Host "  $LogPath"
Write-Host ""
Write-Host "Per adapter details saved under:"
Write-Host "  $detailDir"
Write-Host ""

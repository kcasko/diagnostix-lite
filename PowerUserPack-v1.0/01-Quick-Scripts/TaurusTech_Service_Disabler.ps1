Write-Host "============================================="
Write-Host "  TaurusTech Service Disabler"
Write-Host "============================================="
Write-Host ""

$services = @(
    "DiagTrack",
    "MapsBroker",
    "RetailDemo"
)

foreach ($svc in $services) {

    Write-Host "Processing service: $svc"

    $s = Get-Service -Name $svc -ErrorAction SilentlyContinue

    if (-not $s) {
        Write-Host "  Service not found. Skipping."
        Write-Host ""
        continue
    }

    Write-Host "  Current state: $($s.Status)"
    Write-Host "  Startup type: $($s.StartType)"

    if ($s.StartType -ne "Disabled") {
        Write-Host "  Disabling startup..."
        Set-Service -Name $svc -StartupType Disabled -ErrorAction SilentlyContinue
    } else {
        Write-Host "  Already disabled."
    }

    if ($s.Status -eq "Running") {
        Write-Host "  Stopping service..."
        Stop-Service -Name $svc -Force -ErrorAction SilentlyContinue
    } else {
        Write-Host "  Already stopped."
    }

    Write-Host "  DONE"
    Write-Host ""
}

Write-Host "============================================="
Write-Host "  Completed service adjustments."
Write-Host "============================================="

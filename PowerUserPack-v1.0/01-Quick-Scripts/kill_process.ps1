param(
    [string]$ProcessName
)

# If launched normally, ask for the process name
if (-not $ProcessName) {
    Write-Host "=============================================" -ForegroundColor Cyan
    Write-Host "      TaurusTech Frozen Program Terminator"   -ForegroundColor Cyan
    Write-Host "=============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Enter the name of the program to kill (example: chrome.exe)" -ForegroundColor Yellow
    $ProcessName = Read-Host "Process name"
}

# Strip .exe if user included it
$BaseName = $ProcessName -replace "\.exe$", ""

Write-Host ""
Write-Host "Searching for process: $ProcessName..." -ForegroundColor Gray

$matches = Get-Process -Name $BaseName -ErrorAction SilentlyContinue

if (-not $matches) {
    Write-Host "No running process found matching '$ProcessName'." -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit
}

Write-Host ""
Write-Host "Found $($matches.Count) instance(s):" -ForegroundColor Green
$matches | ForEach-Object {
    Write-Host "  PID $($_.Id)   $($_.ProcessName).exe"
}

Write-Host ""
Write-Host "Terminating..." -ForegroundColor Yellow

try {
    $matches | Stop-Process -Force -ErrorAction Stop
    Write-Host "Process terminated successfully." -ForegroundColor Green
}
catch {
    Write-Host "Failed to kill one or more processes." -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"

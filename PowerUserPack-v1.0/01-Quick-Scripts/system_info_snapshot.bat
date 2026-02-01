@echo off
color 0A

echo TaurusTech System Snapshot
echo ==========================
echo.

:: Create unified log folder
set "LOGROOT=%USERPROFILE%\Desktop\TaurusTech-Logs"
if not exist "%LOGROOT%" mkdir "%LOGROOT%"

:: Save snapshot inside unified folder
set "OUTFILE=%LOGROOT%\system_info_snapshot.txt"

echo Creating text copy at "%OUTFILE%"
echo TaurusTech System Snapshot > "%OUTFILE%"
echo Generated: %DATE% %TIME% >> "%OUTFILE%"
echo. >> "%OUTFILE%"

:: ===============================
:: OS + SYSTEMINFO
:: ===============================
echo OS + System Details
echo --------------------
systeminfo
systeminfo >> "%OUTFILE%"
echo.

:: ===============================
:: CPU
:: ===============================
echo CPU Info
echo ---------
powershell -command "(Get-CimInstance Win32_Processor).Name"
powershell -command "(Get-CimInstance Win32_Processor).Name" >> "%OUTFILE%"
echo.

:: ===============================
:: RAM
:: ===============================
echo RAM Info
echo ---------
powershell -command ^
 "$ram = Get-CimInstance Win32_PhysicalMemory;" ^
 "foreach ($s in $ram) { $gb=[math]::Round($s.Capacity/1GB); 'Stick: ' + $gb + ' GB' }"

powershell -command ^
 "$ram = Get-CimInstance Win32_PhysicalMemory;" ^
 "$total=[math]::Round(($ram|Measure-Object -Property Capacity -Sum).Sum/1GB);" ^
 "'Total RAM: ' + $total + ' GB'"

powershell -command ^
 "$ram = Get-CimInstance Win32_PhysicalMemory;" ^
 "foreach ($s in $ram) { $gb=[math]::Round($s.Capacity/1GB); 'Stick: ' + $gb + ' GB' }" >> "%OUTFILE%"

powershell -command ^
 "$ram = Get-CimInstance Win32_PhysicalMemory;" ^
 "$total=[math]::Round(($ram|Measure-Object -Property Capacity -Sum).Sum/1GB);" ^
 "'Total RAM: ' + $total + ' GB'" >> "%OUTFILE%"
echo.

:: ===============================
:: GPU VRAM
:: ===============================
echo GPU VRAM
echo ---------

for /f "skip=1 tokens=*" %%A in ('nvidia-smi --query-gpu=name --format=csv') do set GPU_NAME=%%A

set "GPU_TEMP=%TEMP%\gpu_vram_out.txt"
nvidia-smi --query-gpu=memory.total --format=csv > "%GPU_TEMP%" 2>&1

set RAW_VRAM=
for /f "skip=1 tokens=1" %%B in ('type "%GPU_TEMP%"') do (
    set RAW_VRAM=%%B
    goto got_gpu_val
)

:got_gpu_val

for /f "delims=MiB" %%C in ("%RAW_VRAM%") do set VRAM_MB=%%C

set /a VRAM_GB=(VRAM_MB + 512) / 1024

echo GPU: %GPU_NAME%
echo VRAM: %VRAM_GB% GB  (%VRAM_MB% MiB)

>> "%OUTFILE%" echo GPU: %GPU_NAME%
>> "%OUTFILE%" echo VRAM: %VRAM_GB% GB  (%VRAM_MB% MiB)
echo.

:: ===============================
:: DISK INFO
:: ===============================
echo Disk Info
echo ---------

powershell -command ^
 "$disks = Get-PhysicalDisk;" ^
 "foreach ($d in $disks) {" ^
 "    $size = $d.Size;" ^
 "    if ($size -ge 1TB) { $human = '{0:N1} TB' -f ($size / 1TB) } else { $human = '{0:N0} GB' -f ($size / 1GB) };" ^
 "    $t = $d.MediaType;" ^
 "    if ($t -eq 'Unspecified') {" ^
 "        if ($d.BusType -eq 'USB') { $t = 'USB Flash Drive' }" ^
 "        elseif ($d.BusType -eq 'NVMe') { $t = 'NVMe SSD' }" ^
 "        elseif ($d.BusType -eq 'SATA') {" ^
 "            if ($d.SpindleSpeed -eq 0 -or $d.SpindleSpeed -eq $null) { $t = 'SATA SSD' } else { $t = 'SATA HDD' }" ^
 "        } else { $t = 'Storage Device' }" ^
 "    };" ^
 "    'Disk: ' + $d.FriendlyName;" ^
 "    'Type: ' + $t;" ^
 "    'Size: ' + $human;" ^
 "    'Status: ' + $d.OperationalStatus;" ^
 "    '';" ^
 "}"

powershell -command ^
 "$disks = Get-PhysicalDisk;" ^
 "foreach ($d in $disks) {" ^
 "    $size = $d.Size;" ^
 "    if ($size -ge 1TB) { $human = '{0:N1} TB' -f ($size / 1TB) } else { $human = '{0:N0} GB' -f ($size / 1GB) };" ^
 "    $t = $d.MediaType;" ^
 "    if ($t -eq 'Unspecified') {" ^
 "        if ($d.BusType -eq 'USB') { $t = 'USB Flash Drive' }" ^
 "        elseif ($d.BusType -eq 'NVMe') { $t = 'NVMe SSD' }" ^
 "        elseif ($d.BusType -eq 'SATA') {" ^
 "            if ($d.SpindleSpeed -eq 0 -or $d.SpindleSpeed -eq $null) { $t = 'SATA SSD' } else { $t = 'SATA HDD' }" ^
 "        } else { $t = 'Storage Device' }" ^
 "    };" ^
 "    'Disk: ' + $d.FriendlyName | Out-File -Append '%OUTFILE%';" ^
 "    'Type: ' + $t | Out-File -Append '%OUTFILE%';" ^
 "    'Size: ' + $human | Out-File -Append '%OUTFILE%';" ^
 "    'Status: ' + $d.OperationalStatus | Out-File -Append '%OUTFILE%';" ^
 "    '' | Out-File -Append '%OUTFILE%';" ^
 "}"
echo.

:: ===============================
:: NETWORK ADAPTERS
:: ===============================
echo Network Adapters
echo ----------------
powershell -command ^
 "Get-NetAdapter | Select-Object Name, InterfaceDescription, Status, LinkSpeed | Format-Table -AutoSize"
powershell -command ^
 "Get-NetAdapter | Select-Object Name, InterfaceDescription, Status, LinkSpeed" >> "%OUTFILE%"
echo.

:: ===============================
:: WINDOWS ACTIVATION
:: ===============================
echo Windows Activation
echo -------------------

for /f %%A in ('powershell -command "(Get-CimInstance -Query \"SELECT LicenseStatus FROM SoftwareLicensingProduct WHERE PartialProductKey IS NOT NULL\").LicenseStatus"') do set ACTIVATION=%%A

if "%ACTIVATION%"=="1" (
    color 0A
    echo Activation: Licensed [OK]
    echo Activation: Licensed [OK] >> "%OUTFILE%"
) else (
    color 0C
    echo Activation: NOT Licensed [FAIL]
    echo Activation: NOT Licensed [FAIL] >> "%OUTFILE%"
)

color 0A
echo.

:: ===============================
:: VIRTUALIZATION
:: ===============================
echo Virtualization / Hyper-V
echo -------------------------
powershell -command ^
 "Get-CimInstance Win32_ComputerSystem | Select-Object HypervisorPresent"
powershell -command ^
 "Get-CimInstance Win32_ComputerSystem | Select-Object HypervisorPresent" >> "%OUTFILE%"
echo.

:: ===============================
:: BATTERY
:: ===============================
echo Battery Health
echo -----------------------------
powershell -command ^
 "Get-CimInstance Win32_Battery | Select-Object EstimatedChargeRemaining, BatteryStatus"
powershell -command ^
 "Get-CimInstance Win32_Battery | Select-Object EstimatedChargeRemaining, BatteryStatus" >> "%OUTFILE%"
echo.

echo Snapshot complete.
echo Saved to: %OUTFILE%
pause

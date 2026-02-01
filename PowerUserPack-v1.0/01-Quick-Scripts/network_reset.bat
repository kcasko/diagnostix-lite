@echo off
setlocal ENABLEDELAYEDEXPANSION

rem TaurusTech Network and Adapter Reset - Entry Script

rem Set log path on Desktop
set "LOGROOT=%USERPROFILE%\Desktop\TaurusTech-Logs"
if not exist "%LOGROOT%" mkdir "%LOGROOT%"

set "LOGFILE=%LOGROOT%\network_reset_log.txt"

cls
echo  =============================================
echo    TaurusTech Network and Adapter Reset
echo  =============================================
echo.
echo  Log file:
echo    %LOGFILE%
echo.

rem Check for PowerShell availability
where powershell >nul 2>&1
if errorlevel 1 (
    echo PowerShell is not available on this system.
    echo This tool requires Windows PowerShell to run.
    echo.
    echo Press any key to exit . . .
    pause >nul
    goto :EOF
)

echo Step 1: Core network reset...
echo.

rem Call core reset PowerShell script
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass ^
  -File "%~dp0network_core_reset.ps1" -LogPath "%LOGFILE%"

echo.
echo Network reset stage logged to:
echo   %LOGFILE%
echo.

echo Step 2: Collecting adapter information...
echo.

rem Call adapter info PowerShell script
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass ^
  -File "%~dp0network_adapter_dump.ps1" -LogPath "%LOGFILE%"

echo.
echo All done.
echo Full diagnostic saved to:
echo   %LOGFILE%
echo.
echo Press any key to continue . . .
pause >nul

endlocal

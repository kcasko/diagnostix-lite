@echo off
setlocal

:: Elevate if needed
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting admin...
    powershell -Command "Start-Process '%~fnx0' -Verb RunAs"
    exit /b
)

:: Run the PowerShell version
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0TaurusTech_Service_Disabler.ps1"
pause

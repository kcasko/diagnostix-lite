@echo off
setlocal ENABLEDELAYEDEXPANSION
title TaurusTech Command Center v1.0

set "ROOT=%~dp0"

:menu
cls
echo ============================================
echo     TaurusTech Command Center v1.0
echo     Power User Pack - Main Menu
echo ============================================
echo.
echo  1] Clean temporary files
echo  2] Reset network stack
echo  3] Kill a frozen program
echo  4] Open startup folders
echo  5] Disable bloat / telemetry services
echo  6] Generate system info snapshot
echo.
echo  0] Exit
echo ============================================
echo.

set /p choice=Select an option: 

if "%choice%"=="1" (
    call "%ROOT%01-Quick-Scripts\clean_temp.bat"
    goto menu
)

if "%choice%"=="2" (
    call "%ROOT%01-Quick-Scripts\network_reset.bat"
    goto menu
)

if "%choice%"=="3" (
    call "%ROOT%01-Quick-Scripts\kill_program.bat"
    goto menu
)

if "%choice%"=="4" (
    call "%ROOT%01-Quick-Scripts\cleanup_startup.bat"
    goto menu
)

if "%choice%"=="5" (
    call "%ROOT%01-Quick-Scripts\disable_bloat_services.bat"
    goto menu
)

if "%choice%"=="6" (
    call "%ROOT%01-Quick-Scripts\system_info_snapshot.bat"
    goto menu
)

if "%choice%"=="0" exit /b

echo Invalid choice.
pause
goto menu

@echo off
color 0A
title TaurusTech Power User Pack Launcher

:menu
cls
echo ======================================
echo        TaurusTech Power User Pack
echo ======================================
echo.
echo 1. Quick Scripts
echo 2. Checklists
echo 3. Config Tweaks
echo 4. Workflow Guides
echo 5. Utilities
echo 6. Exit
echo.
set /p choice="Select an option: "

if "%choice%"=="1" goto quick
if "%choice%"=="2" goto checks
if "%choice%"=="3" goto tweaks
if "%choice%"=="4" goto guides
if "%choice%"=="5" goto utils
if "%choice%"=="6" exit

goto menu

:quick
call ".\TaurusTech-Launcher.bat"
goto menu

:checks
start "" ".\02-Checklists"
goto menu

:tweaks
start "" ".\03-Config-Tweaks"
goto menu

:guides
start "" ".\04-Workflow-Guides"
goto menu

:utils
start "" ".\05-Utilities"
goto menu

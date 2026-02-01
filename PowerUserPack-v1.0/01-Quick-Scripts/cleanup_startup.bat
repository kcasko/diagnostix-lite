@echo off
setlocal ENABLEDELAYEDEXPANSION
color 0A

(
echo =============================================
echo        TaurusTech Startup Manager
echo =============================================
echo.
echo These folders launch apps automatically 
echo when Windows starts.
echo.
echo Clean out anything you don't want running.
echo This window will wait for you.
echo.
echo =============================================
echo.
)

:: Open user Startup folder
start "" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
timeout /t 1 >nul

:: Open system-wide Startup folder
start "" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"

pause
endlocal

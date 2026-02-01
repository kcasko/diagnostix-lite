@echo off
setlocal ENABLEDELAYEDEXPANSION
color 0A

(
echo =============================================
echo          TaurusTech Utility Script
echo =============================================
echo   Script:  %~nx0
echo   Path:    %~dp0
echo =============================================
echo.
echo Cleaning temporary files...
echo.
)

:: -----------------------------------------------
:: Clean user temp
echo [User Temp]
for %%F in ("%TEMP%\*") do (
    echo Deleting: %%~nxF
    del /q /f "%%F" 2>nul
)
for /d %%D in ("%TEMP%\*") do (
    echo Removing folder: %%~nxD
    rd /s /q "%%D" 2>nul
)
echo.

:: -----------------------------------------------
:: Clean Windows temp
echo [Windows Temp]
for %%F in ("C:\Windows\Temp\*") do (
    echo Deleting: %%~nxF
    del /q /f "%%F" 2>nul
)
for /d %%D in ("C:\Windows\Temp\*") do (
    echo Removing folder: %%~nxD
    rd /s /q "%%D" 2>nul
)
echo.

:: -----------------------------------------------
:: Clean SoftwareDistribution cache
echo [Windows Update Cache]
for %%F in ("C:\Windows\SoftwareDistribution\Download\*") do (
    echo Deleting: %%~nxF
    del /q /f "%%F" 2>nul
)
for /d %%D in ("C:\Windows\SoftwareDistribution\Download\*") do (
    echo Removing folder: %%~nxD
    rd /s /q "%%D" 2>nul
)
echo.

echo Done.
pause
endlocal

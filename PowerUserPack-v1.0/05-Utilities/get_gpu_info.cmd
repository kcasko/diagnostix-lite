@echo off
setlocal enabledelayedexpansion
echo =============================================
echo   TaurusTech GPU VRAM Inspector  (Debug Mode)
echo =============================================
echo.

echo Step 1: Checking for nvidia-smi...
echo (If this hangs, your PATH is broken.)
echo.

where nvidia-smi
echo where_exitcode=%errorlevel%
echo.

if %errorlevel% neq 0 (
    echo ERROR: nvidia-smi not found.
    echo This window will NOT close until you press a key.
    pause
    exit /b
)

echo Step 2: Querying GPU name...
echo.

nvidia-smi --query-gpu=name --format=csv
echo query_name_exitcode=%errorlevel%
echo.

echo Step 3: Querying VRAM via fallback parser...
echo.

:: Write output to temp file so we can inspect it
set "TEMPFILE=%TEMP%\gpu_temp_out.txt"
nvidia-smi --query-gpu=memory.total --format=csv > "%TEMPFILE%" 2>&1

echo === RAW OUTPUT BEGIN ===
type "%TEMPFILE%"
echo === RAW OUTPUT END ===
echo.

:: Try to extract the number (skip header)
set VRAM_MB=
for /f "skip=1 tokens=1" %%A in ('type "%TEMPFILE%"') do (
    set RAW=%%A
    goto gotValue
)

:gotValue
echo Raw numeric token extracted: %RAW%
echo.

if not defined RAW (
    echo ERROR: Could not extract VRAM from output.
    pause
    exit /b
)

:: RAW looks like "6141" or "6141MiB" depending on version
for /f "delims=MiB" %%B in ("%RAW%") do set VRAM_MB=%%B

echo Clean VRAM_MB: %VRAM_MB%
echo.

if not defined VRAM_MB (
    echo ERROR: VRAM_MB is missing after cleanup.
    pause
    exit /b
)

set /a VRAM_GB=%VRAM_MB% / 1024

echo VRAM Total: %VRAM_GB% GB  (%VRAM_MB% MiB)
echo.

echo DONE. This window will NOT auto-close.
pause
exit /b

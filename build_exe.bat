@echo off
echo Building DiagnOStiX Desktop Executable...
echo.

cd webui
call venv\Scripts\activate.bat

echo Installing PyInstaller...
venv\Scripts\python.exe -m pip install pyinstaller

echo.
echo Cleaning previous builds...
rmdir /s /q build
rmdir /s /q dist
del /q DiagnOStiX.spec

echo.
echo Running PyInstaller...
echo This may take a minute...

venv\Scripts\python.exe -m PyInstaller --noconfirm --onefile --name "DiagnOStiX" ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --add-data "../PowerUserPack-v1.0;PowerUserPack" ^
    --hidden-import "uvicorn.logging" ^
    --hidden-import "uvicorn.loops" ^
    --hidden-import "uvicorn.loops.auto" ^
    --hidden-import "uvicorn.protocols" ^
    --hidden-import "uvicorn.protocols.http" ^
    --hidden-import "uvicorn.protocols.http.auto" ^
    --hidden-import "uvicorn.lifespan" ^
    --hidden-import "uvicorn.lifespan.on" ^
    gui_launcher.py

echo.
echo Build Complete!
echo Executable is in webui\dist\DiagnOStiX.exe
pause

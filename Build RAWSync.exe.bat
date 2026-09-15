@echo off
REM Double-click this file to build dist\RAWSync.exe.
REM You only need to do this once (or again after changing the code).
REM No need to open PowerShell yourself -- this does it for you.

cd /d "%~dp0"
echo Building RAWSync.exe, this can take a minute...
powershell -NoProfile -ExecutionPolicy Bypass -File "build.ps1"

echo.
if exist "dist\RAWSync.exe" (
    echo Done! dist\RAWSync.exe is ready.
    echo Tip: right-click it and choose "Show more options" -^> "Send to" -^> "Desktop (create shortcut)"
    echo so you can launch RAWSync straight from your desktop from now on.
) else (
    echo Something went wrong -- scroll up to see the error.
)
echo.
pause

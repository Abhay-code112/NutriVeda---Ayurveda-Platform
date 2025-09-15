@echo off
title NutriVeda - Stop All Services
color 0C

echo.
echo ========================================
echo    🛑 STOPPING NUTRIVEDA SERVICES 🛑
echo ========================================
echo.

echo 🔍 Checking for running NutriVeda processes...

REM Check if any Python processes are running
tasklist | findstr python.exe >nul 2>&1
if errorlevel 1 (
    echo ✅ No Python processes found - NutriVeda is already stopped
    echo.
    pause
    exit /b 0
)

echo 📋 Found running Python processes:
tasklist | findstr python.exe

echo.
echo 🛑 Stopping all Python processes...
taskkill /f /im python.exe

if errorlevel 1 (
    echo ❌ Failed to stop some processes
    echo You may need to close the server windows manually
) else (
    echo ✅ All NutriVeda services stopped successfully
)

echo.
echo ========================================
echo    ✅ NUTRIVEDA STOPPED ✅
echo ========================================
echo.
echo 💡 All servers have been shut down
echo 💡 You can now run START_NUTRIVEDA.bat to restart
echo.
pause

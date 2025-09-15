@echo off
title NutriVeda - One Click Startup
color 0A

echo.
echo ========================================
echo    🕉️  NUTRIVEDA ONE-CLICK STARTUP 🕉️
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "simple_backend_fixed.py" (
    echo ❌ Backend file not found: simple_backend_fixed.py
    pause
    exit /b 1
)

if not exist "main_dashboard.html" (
    echo ❌ Frontend file not found: main_dashboard.html
    pause
    exit /b 1
)

REM Kill any existing Python processes to avoid conflicts
echo 🔄 Checking for existing processes...
taskkill /f /im python.exe >nul 2>&1
timeout /t 1 /nobreak >nul

REM Start backend server
echo 🚀 Starting NutriVeda Backend Server...
start "NutriVeda Backend" /min cmd /c "python simple_backend_fixed.py && pause"

REM Wait for backend to initialize
echo ⏳ Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM Start frontend server
echo 🌐 Starting NutriVeda Frontend Server...
start "NutriVeda Frontend" /min cmd /c "python -m http.server 8080 && pause"

REM Wait for frontend to initialize
echo ⏳ Waiting for frontend to initialize...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo    ✅ NUTRIVEDA IS READY! ✅
echo ========================================
echo.
echo 🌐 Frontend: http://localhost:8080/main_dashboard.html
echo 🔧 Backend API: http://localhost:8000
echo.
echo 📊 Features Available:
echo    ✅ Patient Management System
echo    ✅ Comprehensive Food Database (835+ items)
echo    ✅ AI-Powered Dosha Analysis
echo    ✅ Automated Diet Chart Generation
echo    ✅ Ayurvedic Nutrition Recommendations
echo    ✅ Real-time Dashboard Analytics
echo.
echo 🎯 Quick Access Links:
echo    📊 Main Dashboard: http://localhost:8080/main_dashboard.html
echo    🤖 Dosha Analysis: http://localhost:8080/dosha_detector.html
echo    👥 Patient Management: http://localhost:8080/main_dashboard.html#patients
echo    🍽️ Food Database: http://localhost:8080/main_dashboard.html#food-database
echo.

REM Open the application in browser
echo 🌟 Opening NutriVeda in your browser...
start http://localhost:8080/main_dashboard.html

echo.
echo ========================================
echo    🎉 NUTRIVEDA IS RUNNING! 🎉
echo ========================================
echo.
echo 💡 Both servers are running in minimized windows.
echo 💡 Close those windows to stop the servers.
echo 💡 Or run STOP_NUTRIVEDA.bat to stop everything.
echo.
echo Press any key to exit this launcher...
pause >nul

echo.
echo 🕉️ Thank you for using NutriVeda!
echo Ancient Wisdom, Modern Technology!
echo.
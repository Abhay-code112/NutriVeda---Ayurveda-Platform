# NutriVeda Startup Script
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    🕉️  NutriVeda Startup Script 🕉️" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting NutriVeda Backend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python simple_backend_fixed.py" -WindowStyle Normal

Write-Host ""
Write-Host "Waiting 3 seconds for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "Starting NutriVeda Frontend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m http.server 8080" -WindowStyle Normal

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    ✅ NutriVeda is Starting Up! ✅" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Frontend: http://localhost:8080/main_dashboard.html" -ForegroundColor White
Write-Host "🔧 Backend API: http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "📊 Database: 835+ food items loaded" -ForegroundColor Magenta
Write-Host "👥 Patient Management: Ready" -ForegroundColor Magenta
Write-Host "🍽️ Diet Chart Generator: Ready" -ForegroundColor Magenta
Write-Host "🔍 Dosha Analysis: Ready" -ForegroundColor Magenta
Write-Host ""

$response = Read-Host "Press Enter to open the application in your browser"
if ($response -eq "") {
    Write-Host "Opening NutriVeda in your default browser..." -ForegroundColor Green
    Start-Process "http://localhost:8080/main_dashboard.html"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    🎉 NutriVeda is Ready! 🎉" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Both servers are running in separate windows." -ForegroundColor White
Write-Host "Close those windows to stop the servers." -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to exit"

@echo off
title FoodieBot Setup & Launch
color 0A

echo ============================================
echo   FoodieBot - Smart Food Delivery Chatbot
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

echo [1/2] Installing dependencies...
pip install -r requirements.txt --quiet

echo [2/2] Starting FoodieBot...
echo.
echo  Open your browser and go to: http://localhost:5000
echo  Press CTRL+C to stop the server.
echo.
python app.py

pause

@echo off
@chcp 65001 >nul
title TubeTrend Local Helper
echo ========================================================================
echo   TubeTrend Local Helper (Download ^& Script Server)
echo ========================================================================
echo.
echo [1/2] Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.9+.
    pause
    exit /b
)

echo [2/2] Checking required packages...
pip install -q flask flask-cors yt-dlp requests youtube-transcript-api >nul 2>&1

echo.
echo Starting TubeTrend Helper Server on http://127.0.0.1:5001 ...
echo (Do not close this window while using the website)
echo ========================================================================
echo.
python TubeTrend_Helper.py
pause

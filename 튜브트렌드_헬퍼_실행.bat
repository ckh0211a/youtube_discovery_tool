@echo off
chcp 65001 > nul
title TubeTrend Local Helper
echo ========================================================================
echo   ⚡ TubeTrend Local Helper (튜브트렌드 초고속 다운로더 헬퍼) ⚡
echo ========================================================================
echo.
echo  [1/2] 파이썬 및 필수 환경을 확인하는 중입니다...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [오류] Python이 설치되어 있지 않습니다. Python 3.9 이상을 설치해 주세요.
    pause
    exit /b
)

echo  [2/2] 튜브트렌드 다운로더 헬퍼 서버를 시작합니다...
echo.
python TubeTrend_Helper.py
pause

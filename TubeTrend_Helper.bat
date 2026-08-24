@echo off
chcp 65001 > nul
title TubeTrend Local Helper (초고속 무제한 다운로더 헬퍼)
echo ========================================================================
echo   ⚡ TubeTrend Local Helper (튜브트렌드 초고속 다운로더 헬퍼) ⚡
echo ========================================================================
echo.
echo [1/3] 파이썬(Python) 환경을 확인하는 중입니다...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [오류] Python이 설치되어 있지 않습니다.
    echo Python 공식 홈페이지(https://www.python.org)에서 Python을 설치해 주세요.
    echo (설치 시 반드시 'Add python.exe to PATH' 체크박스를 선택해 주세요!)
    echo.
    pause
    exit /b
)

echo [2/3] 필수 라이브러리(Flask, yt-dlp, requests 등)를 점검 중입니다...
pip install -q flask flask-cors yt-dlp requests youtube-transcript-api >nul 2>&1

echo [3/3] 튜브트렌드 다운로더 헬퍼 서버를 시작합니다...
echo.
echo  ● 로컬 주소: http://127.0.0.1:5001
echo  ● 웹사이트(tubetrend.xyz)에서 대본/영상 다운로드를 누르면
echo    이 프로그램을 통해 차단 없이 즉시 초고속 다운로드됩니다!
echo.
echo  ※ 다운로드를 사용하는 동안 이 창을 닫지 마세요.
echo ========================================================================
echo.
python TubeTrend_Helper.py
pause

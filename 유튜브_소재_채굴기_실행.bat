@echo off
:: Set English encoding to prevent broken text issues
chcp 437 >nul
cls

:: Start the python server in a new window so it can stay open
start "YouTube Material Miner Server" cmd /c "title YouTube Server & echo Keep this window open while using the tool! & echo. & .venv\Scripts\python.exe server.py"

exit


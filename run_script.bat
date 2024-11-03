@echo off
cd /d "C:/GitHub/Finance-News-Summary"

REM 啟動虛擬環境
call .venv\Scripts\activate

REM 執行 Python 腳本
python main.py

REM 停用虛擬環境
deactivate

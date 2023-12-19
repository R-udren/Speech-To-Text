@echo off
setlocal

cd /d %~dp0

set "VENV_PATH="
if exist .venv (set "VENV_PATH=.venv") else if exist venv (set "VENV_PATH=venv") else exit /b 1

call %VENV_PATH%\Scripts\activate
python main.py

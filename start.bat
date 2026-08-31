@echo off
TITLE SchemeSaathi Platform
echo ===================================================
echo Starting SchemeSaathi Citizen Action Platform...
echo ===================================================
echo.
cd /d "%~dp0"
start http://localhost:8000
"C:\Users\Dell\AppData\Local\Programs\Python\Python314\python.exe" server.py
pause

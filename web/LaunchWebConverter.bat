@echo off
title MarkItDown Web Converter
color 0A

echo ======================================
echo  MarkItDown Web Converter Launcher
echo ======================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher
    pause
    exit /b 1
)
echo OK - Python found
echo.

echo [2/3] Starting Flask server...
echo.
echo When server starts, your browser will open automatically
echo to http://localhost:5000
echo.
echo Press Ctrl+C to stop the server when done.
echo.
echo ======================================
echo.

python app.py

if errorlevel 1 (
    echo.
    echo ERROR: Server failed to start
    echo.
    echo Possible solutions:
    echo 1. Install dependencies: pip install -r requirements.txt
    echo 2. Check if port 5000 is already in use
    echo 3. Try running: python app.py manually
    echo.
)

pause
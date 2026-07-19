@echo off
title File Organizer
echo.
echo  ========================================
echo    File Organizer - Starting...
echo  ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo  [ERROR] Python is not installed or not in PATH.
    echo.
    echo  Please install Python 3.8+ from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Run the app
python "%~dp0file_organizer.py"

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo  [ERROR] App crashed. Check file_organizer.log for details.
    pause
)

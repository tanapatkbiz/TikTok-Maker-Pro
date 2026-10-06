@echo off
REM Build script for Windows
REM Requirements: Python 3.9+, pip

echo ====================================================
echo  TikTok Maker Pro - Windows Build Script
echo ====================================================
echo.

echo Checking Python version...
python --version
echo.

echo Installing dependencies...
pip install -r requirements.txt --upgrade
echo.

echo Building EXE file...
python build_exe.py

echo.
echo ====================================================
echo Build process complete!
echo ====================================================
pause

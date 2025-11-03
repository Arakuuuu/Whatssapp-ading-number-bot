@echo off
echo ==================================
echo WhatsApp Bot Setup
echo ==================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python is not installed. Please install Python first.
    pause
    exit /b 1
)

echo √ Python found

REM Install requirements
echo.
echo Installing Python packages...
pip install -r requirements.txt

REM Install ChromeDriver manager
echo.
echo Setting up ChromeDriver...
pip install webdriver-manager

echo.
echo ==================================
echo √ Setup Complete!
echo ==================================
echo.
echo To run the bot, use:
echo   python whatsapp_bot.py
echo.
pause

#!/bin/bash

echo "=================================="
echo "WhatsApp Bot Setup"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python first."
    exit 1
fi

echo "✓ Python3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✓ pip3 found"

# Install requirements
echo ""
echo "Installing Python packages..."
pip3 install -r requirements.txt

# Check if Chrome is installed
if command -v google-chrome &> /dev/null || command -v chromium-browser &> /dev/null; then
    echo "✓ Chrome/Chromium found"
else
    echo "⚠️  Chrome not detected. Please install Google Chrome."
fi

# Install ChromeDriver
echo ""
echo "Setting up ChromeDriver..."
pip3 install webdriver-manager

echo ""
echo "=================================="
echo "✓ Setup Complete!"
echo "=================================="
echo ""
echo "To run the bot, use:"
echo "  python3 whatsapp_bot.py"
echo ""

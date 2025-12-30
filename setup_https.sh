#!/bin/bash

# HTTPS Setup Script for Mobile Camera Access

echo "🔒 Setting up HTTPS for mobile camera access..."
echo ""

# Check if ngrok is installed
if command -v ngrok &> /dev/null; then
    echo "✓ ngrok is installed"
    echo ""
    echo "To use your phone's camera:"
    echo "1. Start your Flask app: python app.py"
    echo "2. In another terminal, run: ngrok http 5001"
    echo "3. Copy the HTTPS URL (e.g., https://abc123.ngrok.io)"
    echo "4. Open that URL on your phone"
    echo "5. Your phone's camera will work!"
    echo ""
else
    echo "❌ ngrok is not installed"
    echo ""
    echo "Installing ngrok..."
    echo ""
    
    # Detect OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            echo "Installing via Homebrew..."
            brew install ngrok/ngrok/ngrok
        else
            echo "Please install Homebrew first, or download ngrok manually:"
            echo "1. Visit: https://ngrok.com/download"
            echo "2. Download for macOS"
            echo "3. Extract and add to PATH"
        fi
    else
        echo "Please install ngrok manually:"
        echo "1. Visit: https://ngrok.com/download"
        echo "2. Download for your OS"
        echo "3. Extract and add to PATH"
    fi
    
    echo ""
    echo "Alternative: Set up self-signed SSL (see setup_ssl.sh)"
fi



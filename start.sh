#!/bin/bash

# Startup script for AI Navigation Assistant

echo "🚀 Starting AI Navigation Assistant..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cat > .env << EOF
# Azure Computer Vision API Configuration
AZURE_COMPUTER_VISION_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
AZURE_COMPUTER_VISION_KEY=your-api-key-here

# Azure Face API Configuration (optional, for face recognition)
AZURE_FACE_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
AZURE_FACE_KEY=your-face-api-key-here

# Application Settings
DEBUG=True
PORT=5001
EOF
    echo "⚠️  Please edit .env file and add your Azure API credentials"
    exit 1
fi

# Check Azure credentials
source .env
if [ "$AZURE_COMPUTER_VISION_KEY" = "your-api-key-here" ] || [ -z "$AZURE_COMPUTER_VISION_KEY" ]; then
    echo "⚠️  Azure Computer Vision API key not configured in .env file"
    echo "Please edit .env and add your Azure credentials"
    exit 1
fi

# Get port from .env or use default
PORT=${PORT:-5001}

echo "✓ Configuration loaded"
echo "📡 Starting server on port $PORT"
echo ""
echo "Access the application at:"
echo "  - Local: http://localhost:$PORT"
echo "  - Network: http://$(ipconfig getifaddr en0 2>/dev/null || hostname -I | awk '{print $1}'):$PORT"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the application
python app.py



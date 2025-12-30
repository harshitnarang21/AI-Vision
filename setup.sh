#!/bin/bash

# Setup script for AI Navigation Assistant

echo "🚀 Setting up AI Navigation Assistant for the Blind..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cat > .env << EOF
# Azure Computer Vision API Configuration
AZURE_COMPUTER_VISION_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
AZURE_COMPUTER_VISION_KEY=your-api-key-here

# Azure Face API Configuration (optional, for face recognition)
AZURE_FACE_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
AZURE_FACE_KEY=your-face-api-key-here

# Application Settings
DEBUG=True
PORT=5000
EOF
    echo "⚠️  Please edit .env file and add your Azure API credentials"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your Azure Computer Vision API credentials"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the application: python app.py"
echo "4. Open http://localhost:5000 in your browser"



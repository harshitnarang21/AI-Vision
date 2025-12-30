# Quick Start Guide

## Prerequisites Setup

### 1. Azure Computer Vision Setup

1. Go to [Azure Portal](https://portal.azure.com/)
2. Create a new resource → Search "Computer Vision"
3. Create the resource (choose Free tier for testing)
4. After creation, go to "Keys and Endpoint"
5. Copy the Endpoint URL and Key 1

### 2. (Optional) Azure Face API Setup

1. In Azure Portal, create a "Face" resource
2. Copy the Endpoint URL and Key 1

## Installation

### Option 1: Using Setup Script (Recommended)

```bash
./setup.sh
source venv/bin/activate
```

### Option 2: Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your Azure credentials
```

## Configuration

Edit the `.env` file:

```env
AZURE_COMPUTER_VISION_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_COMPUTER_VISION_KEY=your-actual-key-here
```

## Running the Application

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the app
python app.py
```

The application will start on `http://localhost:5000`

## Using on Your Phone

1. Find your computer's IP address:
   - Mac/Linux: `ifconfig | grep "inet "`
   - Windows: `ipconfig`
   - Look for something like `192.168.1.100`

2. Make sure your phone is on the same Wi-Fi network

3. Open browser on phone and go to: `http://YOUR_IP:5000`

4. Grant camera permissions when prompted

5. Click "Start Camera" to begin!

## Troubleshooting

### Camera Issues
- **Permission denied**: Grant camera permissions in browser settings
- **Camera not found**: Try changing `camera_index` in the start request (0, 1, or 2)
- **Black screen**: Check if another app is using the camera

### Azure API Issues
- **401 Unauthorized**: Check your API key is correct
- **429 Too Many Requests**: You've hit the rate limit (Free tier: 20 calls/minute)
- **Endpoint error**: Make sure endpoint URL ends with `/`

### Audio Issues
- **No sound on macOS**: Install `pyobjc`: `pip install pyobjc`
- **No sound on Linux**: Install `espeak`: `sudo apt-get install espeak`

## Testing Without Camera

You can test the API by uploading an image:

```bash
curl -X POST http://localhost:5000/api/process \
  -F "image=@path/to/your/image.jpg"
```

## Features Overview

- **Real-time Analysis**: Processes camera feed every 2 seconds (configurable)
- **Obstacle Detection**: Automatically warns about obstacles with spatial cues
- **Text Reading**: Reads any visible text aloud
- **Scene Description**: Describes what's in the camera view
- **Object Detection**: Identifies objects with confidence scores
- **Face Recognition**: Detects faces with age, gender, emotion (if Face API configured)

## Next Steps

- Customize `config.py` to adjust processing frequency
- Add your own voice commands
- Integrate with navigation apps
- Deploy to cloud for always-on access



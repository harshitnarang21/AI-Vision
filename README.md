# AI Navigation Assistant for the Blind

A smart phone/web application that uses computer vision to assist blind and visually impaired users by describing surroundings in real-time, reading text aloud, recognizing faces, identifying objects, and warning about obstacles.

## Features

- **Real-time Scene Description**: Uses Azure Computer Vision to describe what's in front of the camera
- **Text Reading (OCR)**: Reads text from signs, documents, and labels aloud
- **Object Detection**: Identifies and describes objects in the environment
- **Obstacle Warning**: Detects potential obstacles and provides spatial audio warnings
- **Face Recognition**: Detects faces and provides basic information (age, gender, emotion)
- **Spatial Audio Cues**: Provides directional information (ahead, left, right) for detected objects
- **Web-based Interface**: Accessible from any smartphone or tablet with a camera

## Prerequisites

- Python 3.8 or higher
- Camera/webcam access
- Azure Computer Vision API key and endpoint
- (Optional) Azure Face API key for face recognition features

## Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Azure Computer Vision**:
   - Create an Azure account if you don't have one
   - Create a Computer Vision resource in Azure Portal
   - Get your endpoint URL and API key

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Azure credentials:
   ```
   AZURE_COMPUTER_VISION_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
   AZURE_COMPUTER_VISION_KEY=your-api-key-here
   
   # Optional: For face recognition
   AZURE_FACE_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
   AZURE_FACE_KEY=your-face-api-key-here
   ```

## Usage

1. **Test your Azure connection** (optional):
   ```bash
   python test_connection.py
   ```

2. **Start the application**:
   ```bash
   # Option 1: Using the startup script (recommended)
   ./start.sh
   
   # Option 2: Manual start
   source venv/bin/activate
   python app.py
   ```

3. **Access the web interface**:
   - Open your browser or phone browser
   - Navigate to `http://localhost:5001` (or your configured port)
   - For phone access, make sure your phone and computer are on the same network
   - The startup script will display the network IP address

3. **Use the application**:
   - Click "Start Camera" to begin real-time analysis
   - The application will automatically:
     - Describe the scene
     - Read any visible text
     - Identify objects
     - Warn about obstacles
     - Detect faces (if Face API is configured)
   - All information is spoken aloud automatically
   - Use the text input to manually speak custom text

## How It Works

1. **Camera Capture**: The app captures frames from your device's camera
2. **Image Analysis**: Frames are sent to Azure Computer Vision API for analysis
3. **Processing**: The app processes the results to:
   - Identify obstacles based on object types and positions
   - Calculate spatial directions (left, right, ahead)
   - Extract text using OCR
   - Detect faces (if enabled)
4. **Audio Feedback**: Results are converted to speech with spatial cues
5. **Real-time Updates**: The process repeats continuously while the camera is active

## Configuration

Edit `config.py` to adjust:
- `FRAME_RATE`: How often to process frames (lower = fewer API calls)
- `OBSTACLE_DETECTION_THRESHOLD`: Confidence threshold for obstacle detection
- `MIN_OBJECT_SIZE`: Minimum object size to report

## API Endpoints

- `GET /`: Main web interface
- `POST /api/camera/start`: Start camera capture
- `POST /api/camera/stop`: Stop camera capture
- `GET /api/camera/frame`: Get current camera frame
- `GET /api/analysis`: Get latest analysis results
- `POST /api/process`: Process uploaded image
- `POST /api/audio/speak`: Speak custom text
- `GET /api/status`: Get application status

## Mobile Access

To use on your phone:
1. Find your computer's IP address (e.g., `192.168.1.100`)
2. Make sure your phone is on the same Wi-Fi network
3. Open browser on phone and go to `http://YOUR_IP:5000`
4. Grant camera permissions when prompted

## Troubleshooting

**Camera not working**:
- Make sure camera permissions are granted
- Try different camera_index values (0, 1, 2)
- Check if camera is being used by another application

**Azure API errors**:
- Verify your API key and endpoint are correct
- Check your Azure subscription has active credits
- Ensure the endpoint URL ends with `/` (trailing slash)

**Audio not working**:
- On macOS/Linux, you may need to install additional audio drivers
- Check system audio settings
- Try using a different TTS engine

## Future Enhancements

- Integration with smart glasses hardware
- GPS-based navigation assistance
- Offline mode with local ML models
- Voice commands for control
- Custom voice profiles
- Multi-language support
- Integration with navigation apps

## License

This project is provided as-is for educational and assistive technology purposes.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

For issues or questions, please open an issue on the repository.


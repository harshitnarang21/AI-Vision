# Quick Usage Guide

## Starting the Application

### Quick Start
```bash
./start.sh
```

This script will:
- Check if virtual environment exists
- Verify Azure credentials are configured
- Display the access URLs
- Start the server

### Manual Start
```bash
source venv/bin/activate
python app.py
```

## Accessing the Application

### On Your Computer
Open your browser and go to:
```
http://localhost:5001
```
(Replace 5001 with your configured port if different)

### On Your Phone/Tablet
1. Make sure your phone is on the same Wi-Fi network as your computer
2. Find your computer's IP address:
   - **Mac/Linux**: Run `ifconfig | grep "inet "` or check the startup script output
   - **Windows**: Run `ipconfig` and look for IPv4 Address
3. Open browser on phone and go to:
   ```
   http://YOUR_IP_ADDRESS:5001
   ```
   Example: `http://192.168.1.100:5001`

## Using the Application

1. **Start Camera**: Click the "Start Camera" button
   - Grant camera permissions when prompted
   - The camera feed will appear on screen

2. **Automatic Analysis**: The app will automatically:
   - Describe the scene
   - Read any visible text
   - Identify objects
   - Warn about obstacles
   - Detect faces (if configured)

3. **Manual Text-to-Speech**: 
   - Type text in the input field
   - Click "Speak" or press Enter
   - The text will be read aloud

4. **View Analysis**: 
   - Analysis results appear in the right panel
   - Obstacle warnings are highlighted in yellow
   - All information is also spoken aloud

## API Endpoints

### Health Check
```bash
curl http://localhost:5001/api/health
```

### Get Status
```bash
curl http://localhost:5001/api/status
```

### Process Image
```bash
curl -X POST -F "image=@path/to/image.jpg" http://localhost:5001/api/process
```

### Speak Text
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"Hello, this is a test"}' \
  http://localhost:5001/api/audio/speak
```

## Troubleshooting

### Camera Not Working
- Check browser permissions for camera access
- Try a different browser (Chrome, Firefox, Safari)
- Make sure no other app is using the camera
- Try different camera_index (0, 1, 2) in the start request

### No Audio
- Check system volume
- On macOS, TTS should work automatically
- Try the manual "Speak" feature to test audio

### API Errors
- Run `python test_connection.py` to verify Azure credentials
- Check your Azure subscription has credits
- Verify endpoint URLs end with `/`

### Port Already in Use
- Change PORT in `.env` file
- Or kill the process using the port:
  ```bash
  lsof -ti:5001 | xargs kill
  ```

## Stopping the Application

Press `Ctrl+C` in the terminal where the app is running.



# Mobile Camera Setup Guide

## Overview

The application now automatically detects mobile devices and uses the device's camera instead of the server's camera. This allows you to use your phone's camera when accessing the app from your mobile browser.

## How It Works

### Automatic Detection
- The app detects if you're using a mobile device (iPhone, iPad, Android, etc.)
- On mobile: Uses your phone's camera directly
- On desktop: Uses the server's camera (as before)

### Mobile Camera Features
- **Back Camera**: Uses the rear camera by default (better for navigation)
- **Real-time Processing**: Captures frames and sends to server for AI analysis
- **Automatic Analysis**: Same AI features work (scene description, OCR, obstacle detection, etc.)

## Usage

### On Mobile Device

1. **Open Browser**:
   - Open Safari (iOS) or Chrome (Android)
   - Navigate to: `http://192.168.1.45:5001/`
   - Make sure your phone is on the same Wi-Fi network

2. **Grant Camera Permission**:
   - When you click "Start Camera", your browser will ask for camera permission
   - Click "Allow" to grant access
   - The camera feed will appear on screen

3. **Use the App**:
   - Point your phone's camera at scenes
   - The AI will analyze and describe what it sees
   - Audio feedback will play automatically

### Camera Permissions

**iOS (Safari)**:
- Settings → Safari → Camera → Allow
- Or grant permission when prompted in browser

**Android (Chrome)**:
- Settings → Apps → Chrome → Permissions → Camera → Allow
- Or grant permission when prompted in browser

## Troubleshooting

### Camera Not Working on Mobile

1. **Check Permissions**:
   - Make sure camera permission is granted
   - Check browser settings

2. **Try Different Browser**:
   - Safari on iOS
   - Chrome on Android
   - Firefox (if available)

3. **Check HTTPS**:
   - Some browsers require HTTPS for camera access
   - If on local network, this should work fine
   - If issues persist, try accessing via HTTPS

4. **Check Network**:
   - Ensure phone is on same Wi-Fi network
   - Verify server IP address is correct

### Camera Shows Black Screen

1. **Refresh the Page**: Sometimes camera needs a refresh
2. **Check Other Apps**: Close other apps using the camera
3. **Restart Browser**: Close and reopen browser
4. **Check Camera**: Make sure camera works in other apps

### No Analysis Results

1. **Check Server**: Make sure server is running
2. **Check Network**: Verify connection to server
3. **Check Azure**: Ensure Azure APIs are configured correctly
4. **Check Logs**: Look at server terminal for errors

## Technical Details

### Frame Processing
- Mobile captures frames at ~10 FPS
- Frames are sent to server every 200ms
- Server processes with Azure Computer Vision API
- Results sent back to mobile device

### Bandwidth
- Each frame is ~50-100KB (compressed JPEG)
- At 10 FPS: ~500KB-1MB per second
- Ensure good Wi-Fi connection for best performance

### Privacy
- Camera feed stays on your device
- Only processed frames are sent to server
- No video is stored or recorded
- All processing happens in real-time

## Tips for Best Experience

1. **Good Lighting**: Better lighting = better AI analysis
2. **Stable Connection**: Use strong Wi-Fi for best performance
3. **Hold Steady**: Keep phone steady for better frame capture
4. **Battery**: Camera usage drains battery - keep phone charged
5. **Volume**: Ensure phone volume is up for audio feedback

## Switching Between Cameras

Currently, the app uses the back camera by default. To change this, you would need to modify the code:

```javascript
facingMode: 'user'  // For front camera
facingMode: 'environment'  // For back camera (default)
```

## Desktop vs Mobile

| Feature | Desktop | Mobile |
|---------|---------|--------|
| Camera Source | Server camera | Device camera |
| Frame Rate | Server controlled | Device controlled |
| Processing | Server-side | Server-side |
| Audio | Server speakers | Device speakers |
| Best For | Testing, demos | Real-world use |

## Need Help?

- Check server logs for errors
- Verify Azure API configuration
- Test camera in other apps
- Check browser console for JavaScript errors



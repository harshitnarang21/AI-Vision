# Troubleshooting Guide

## Audio Not Working / Not Describing Environment

### Issue: Audio service not speaking

**Symptoms:**
- Analysis appears in UI but no audio output
- No speech when camera is active

**Solutions:**

1. **Test Audio Service:**
   ```bash
   curl http://localhost:5001/api/audio/test
   ```
   Or visit: `http://localhost:5001/api/audio/test` in browser

2. **Check System Audio:**
   - Ensure system volume is up
   - Check if other applications can play audio
   - On macOS, TTS should work automatically

3. **Check Logs:**
   Look for `[Audio]` messages in terminal:
   ```
   [Audio] Speaking: ...
   ```
   If you see these, audio is being triggered but may not be playing.

4. **Manual Test:**
   Use the "Speak" button in the UI with test text

5. **Check Audio Service Initialization:**
   The audio service should initialize when the app starts. Check terminal for errors.

### Issue: No description being generated

**Symptoms:**
- Camera works but no scene description
- Analysis panel shows empty or minimal data

**Solutions:**

1. **Check Azure API:**
   ```bash
   python test_connection.py
   ```

2. **Check Logs:**
   Look for `[Processing]` and `[Azure Vision]` messages:
   ```
   [Processing] Analyzing frame...
   [Azure Vision] Analysis complete - Description: ...
   ```

3. **Verify Image Quality:**
   - Ensure good lighting
   - Camera should be focused
   - Try pointing at different scenes

4. **Check API Rate Limits:**
   - Free tier: 20 calls/minute
   - If exceeded, wait a minute and try again

## Face Detection Errors

### Issue: Face detection error

**Symptoms:**
- Error messages about face detection
- Faces not being detected

**Solutions:**

1. **Check Face API Configuration:**
   - Verify `AZURE_FACE_ENDPOINT` and `AZURE_FACE_KEY` in `.env`
   - Run: `python test_connection.py`

2. **Check API Version:**
   - The code now handles different API versions
   - Emotion attribute may not be available in all regions
   - Code will fallback gracefully

3. **Check Logs:**
   Look for face detection messages:
   ```
   [Processing] Face detection skipped: ...
   ```
   Or:
   ```
   Face detection error: ...
   ```

4. **Disable Face Detection (if needed):**
   - Face detection is optional
   - App will work without it
   - Remove Face API credentials from `.env` to disable

### Common Face API Errors:

**Error: "Invalid face attributes"**
- Solution: Code now handles this with fallback
- Emotion attribute may not be supported in your region

**Error: "Face API not configured"**
- Solution: Face API is optional, app works without it
- Or add Face API credentials to `.env`

## General Debugging

### Enable Debug Mode:

1. **Check `.env` file:**
   ```
   DEBUG=True
   ```

2. **Check Terminal Output:**
   - Look for error messages
   - Check for `[Processing]`, `[Audio]`, `[Azure Vision]` prefixes
   - These indicate where processing is happening

### Test Individual Components:

1. **Test Audio:**
   ```bash
   curl http://localhost:5001/api/audio/test
   ```

2. **Test Vision Service:**
   ```bash
   python test_connection.py
   ```

3. **Test Image Processing:**
   - Use the image upload feature in UI
   - Or use API:
   ```bash
   curl -X POST -F "image=@test_image.jpg" http://localhost:5001/api/process
   ```

### Check Application Status:

```bash
curl http://localhost:5001/api/status
```

Should return:
```json
{
  "camera_active": true/false,
  "vision_service_ready": true,
  "face_service_ready": true/false,
  "processing_enabled": true/false,
  "port": 5001
}
```

## Common Issues

### Camera Not Starting

1. **Check Permissions:**
   - Browser must grant camera access
   - Check browser settings

2. **Check Camera Index:**
   - Try different camera_index (0, 1, 2)
   - Some systems have multiple cameras

3. **Check if Camera is in Use:**
   - Close other apps using camera
   - Restart browser

### Slow Processing

1. **Check Frame Rate:**
   - Default: Process every 2 frames
   - Adjust in `config.py`: `FRAME_RATE = 2`

2. **Check API Rate Limits:**
   - Free tier: 20 calls/minute
   - Processing every 2 seconds = 30 calls/minute (exceeds free tier)
   - Increase `FRAME_RATE` to 3 or 4

3. **Network Speed:**
   - Azure API calls require internet
   - Check connection speed

### No Analysis Results

1. **Check Azure Credits:**
   - Verify Azure subscription has credits
   - Free tier has limited calls

2. **Check API Keys:**
   - Verify keys are correct in `.env`
   - Keys should not have extra spaces

3. **Check Endpoint URLs:**
   - Must end with `/`
   - Should be: `https://your-resource.cognitiveservices.azure.com/`

## Getting Help

If issues persist:

1. **Check Logs:**
   - All errors are printed to terminal
   - Look for traceback information

2. **Test Components:**
   - Run `python test_connection.py`
   - Test audio with `/api/audio/test`
   - Check status with `/api/status`

3. **Verify Configuration:**
   - Check `.env` file
   - Verify all required fields are set
   - Ensure no typos in API keys

4. **Check Azure Portal:**
   - Verify resources are active
   - Check usage and quotas
   - Verify API keys are correct



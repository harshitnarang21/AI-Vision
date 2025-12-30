# HTTPS Setup Guide for Mobile Camera

## Why HTTPS is Required

Modern browsers (especially mobile Chrome and Safari) require HTTPS to access the camera API for security reasons. When accessing via HTTP (like `http://192.168.1.45:5001/`), the camera API is blocked.

## Solution Options

### Option 1: Use Server Camera (Easiest - Already Implemented)

The app now automatically falls back to using the server's camera when HTTPS is not available. This works perfectly fine - your phone will display the server's camera feed.

**How it works:**
- Click "Start Camera" on your phone
- If mobile camera fails, click "Use Server Camera Instead"
- The server's camera feed will appear on your phone
- All AI features work the same way

### Option 2: Set Up HTTPS (For True Mobile Camera)

If you want to use your phone's camera directly, you need HTTPS. Here are options:

#### A. Using ngrok (Easiest for Testing)

1. **Install ngrok:**
   ```bash
   # macOS
   brew install ngrok
   
   # Or download from https://ngrok.com/
   ```

2. **Start your Flask app:**
   ```bash
   python app.py
   ```

3. **In another terminal, create HTTPS tunnel:**
   ```bash
   ngrok http 5001
   ```

4. **Use the HTTPS URL:**
   - ngrok will give you a URL like: `https://abc123.ngrok.io`
   - Access this URL from your phone
   - Camera will work!

#### B. Using Flask with SSL (For Local Network)

1. **Generate self-signed certificate:**
   ```bash
   openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
   ```

2. **Modify app.py to use SSL:**
   ```python
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5001, ssl_context=('cert.pem', 'key.pem'), debug=True)
   ```

3. **Access via HTTPS:**
   - `https://192.168.1.45:5001/`
   - Accept the security warning (self-signed certificate)
   - Camera will work!

#### C. Using a Reverse Proxy (Advanced)

Set up nginx or Apache with SSL certificates to proxy to your Flask app.

## Current Workaround (Recommended)

**Just use the server camera!** It works perfectly:

1. On your phone, go to `http://192.168.1.45:5001/`
2. Click "Start Camera"
3. If you see "Use Server Camera Instead" button, click it
4. The server's camera feed will appear on your phone
5. All AI features work exactly the same

## Why Server Camera Works Fine

- The server camera captures frames
- Sends them to Azure for AI processing
- Results are sent back to your phone
- Audio plays on your phone
- Everything works the same, just using server's camera instead

## Quick Test

Try this now:
1. Open `http://192.168.1.45:5001/` on your phone
2. Click "Start Camera"
3. If mobile camera fails, click "Use Server Camera Instead"
4. You should see the server's camera feed!

The app is smart enough to automatically use the server camera when mobile camera isn't available.



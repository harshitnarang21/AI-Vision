# Mobile Camera Setup - Use Your Phone's Camera

## Quick Start (Easiest Method - ngrok)

### Step 1: Install ngrok

**On macOS:**
```bash
brew install ngrok/ngrok/ngrok
```

**Or download manually:**
1. Visit: https://ngrok.com/download
2. Download for your OS
3. Extract and add to PATH

### Step 2: Start Your Flask App

```bash
cd /Users/paras/Desktop/Project/AI
source venv/bin/activate
python app.py
```

Keep this terminal running!

### Step 3: Create HTTPS Tunnel

**Open a NEW terminal window** and run:

```bash
ngrok http 5001
```

You'll see output like:
```
Forwarding   https://abc123.ngrok.io -> http://localhost:5001
```

### Step 4: Use on Your Phone

1. **Copy the HTTPS URL** from ngrok (e.g., `https://abc123.ngrok.io`)
2. **Open that URL on your phone's browser**
3. **Click "Start Camera"**
4. **Grant camera permission**
5. **Your phone's camera will work!** 🎉

---

## Alternative Method: Self-Signed SSL (For Local Network)

### Step 1: Generate SSL Certificate

```bash
cd /Users/paras/Desktop/Project/AI
./setup_ssl.sh
```

This creates `cert.pem` and `key.pem` files.

### Step 2: Restart Your App

The app will automatically detect the certificates and use HTTPS.

### Step 3: Access on Your Phone

1. Go to: `https://192.168.1.45:5001/`
2. **Accept the security warning** (this is normal for self-signed certificates)
3. Click "Start Camera"
4. Your phone's camera will work!

---

## Which Method to Use?

### Use ngrok if:
- ✅ You want the easiest setup
- ✅ You're testing or demonstrating
- ✅ You don't mind the URL changing each time
- ✅ You want it to work immediately

### Use SSL if:
- ✅ You want a fixed URL (`https://192.168.1.45:5001/`)
- ✅ You're using it regularly
- ✅ You don't mind accepting the security warning once

---

## Troubleshooting

### ngrok Issues

**"ngrok: command not found"**
- Install ngrok: `brew install ngrok/ngrok/ngrok`
- Or download from https://ngrok.com/

**"Tunnel not working"**
- Make sure Flask app is running on port 5001
- Check that ngrok is pointing to the correct port

### SSL Issues

**"Security warning in browser"**
- This is normal for self-signed certificates
- Click "Advanced" → "Proceed anyway" (or similar)
- You only need to do this once per browser

**"Certificate error"**
- Make sure `cert.pem` and `key.pem` exist in the project directory
- Regenerate certificates: `./setup_ssl.sh`

### Camera Still Not Working

1. **Check HTTPS**: Make sure URL starts with `https://`
2. **Check Permissions**: Grant camera permission in browser
3. **Try Different Browser**: 
   - Safari on iOS
   - Chrome on Android
4. **Check Console**: Open browser developer tools to see errors

---

## Quick Reference

### ngrok Method:
```bash
# Terminal 1: Start Flask
python app.py

# Terminal 2: Start ngrok
ngrok http 5001

# Use the HTTPS URL on your phone
```

### SSL Method:
```bash
# Generate certificates
./setup_ssl.sh

# Start Flask (auto-detects SSL)
python app.py

# Access on phone: https://192.168.1.45:5001/
```

---

## Why HTTPS is Required

Modern browsers (Chrome, Safari) require HTTPS for security when accessing:
- Camera API
- Microphone API
- Location API
- Other sensitive device features

This is a security feature to prevent malicious websites from accessing your camera without your knowledge.

---

## Need Help?

- Check that Flask is running: `http://192.168.1.45:5001/` should load
- Check ngrok status: Look at ngrok web interface (usually shown in terminal)
- Check browser console: Open developer tools on your phone to see errors
- Try the server camera fallback: Click "Use Server Camera Instead" if mobile camera fails



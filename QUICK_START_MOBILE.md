# Quick Start: Use Your Phone's Camera

## ✅ SSL Certificates Generated!

Your app is now ready to use HTTPS. Follow these steps:

## Step 1: Restart Your Flask App

**If your app is currently running:**
1. Stop it (press `Ctrl+C` in the terminal)
2. Start it again:

```bash
cd /Users/paras/Desktop/Project/AI
source venv/bin/activate
python app.py
```

You should see:
```
🔒 SSL certificates found - Starting HTTPS server on port 5001
   Access via: https://192.168.1.45:5001/
```

## Step 2: Access on Your Phone

1. **Open your phone's browser** (Safari on iOS, Chrome on Android)
2. **Go to:** `https://192.168.1.45:5001/`
3. **You'll see a security warning** - this is normal for self-signed certificates
4. **Click "Advanced" or "Show Details"**
5. **Click "Proceed to 192.168.1.45" or "Accept Risk"**
   - On iOS Safari: Tap "Show Details" → "visit this website"
   - On Android Chrome: Tap "Advanced" → "Proceed to 192.168.1.45"

## Step 3: Use Your Phone's Camera

1. **Click "Start Camera"** on your phone
2. **Grant camera permission** when prompted
3. **Your phone's camera will activate!** 🎉
4. Point it at scenes and the AI will describe them

## Troubleshooting

### "Your connection is not private" Warning
- This is normal for self-signed certificates
- Click "Advanced" → "Proceed anyway"
- You only need to do this once per browser

### Camera Still Not Working
1. Make sure URL starts with `https://` (not `http://`)
2. Check that you accepted the security warning
3. Grant camera permission in browser
4. Try refreshing the page

### Can't Access the Site
1. Make sure Flask app is running
2. Check that you're on the same Wi-Fi network
3. Verify the IP address: `192.168.1.45`
4. Try accessing from your computer first: `https://localhost:5001/`

## That's It!

Your phone's camera should now work! The app will:
- Use your phone's camera directly
- Process frames in real-time
- Provide AI analysis and audio feedback
- Work just like a native app

Enjoy using your AI Navigation Assistant! 🚀



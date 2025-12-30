# Azure Configuration Fix Guide

## Critical Error: Public Access Disabled

You're seeing this error:
```
(403) Public access is disabled. Please configure private endpoint.
```

This means your Azure Computer Vision resource has **public network access disabled**.

## How to Fix

### Step 1: Open Azure Portal
1. Go to [https://portal.azure.com](https://portal.azure.com)
2. Sign in with your Azure account

### Step 2: Find Your Computer Vision Resource
1. In the search bar at the top, type your resource name (e.g., "navivoice")
2. Click on your Computer Vision resource

### Step 3: Enable Public Network Access
**Option A: Using Networking Tab (Recommended)**
1. In the left menu, click **"Networking"** or **"Settings" > "Networking"**
2. Find **"Public network access"** or **"Network access"**
3. Select **"Enabled"** or **"All networks"**
4. Click **"Save"**
5. Wait 1-2 minutes for changes to take effect

**Option B: Using Resource Settings**
1. In the left menu, click **"Settings"** or **"Properties"**
2. Look for **"Public network access"**
3. Change it to **"Enabled"**
4. Click **"Save"**

### Step 4: Verify
1. Wait 1-2 minutes
2. Restart your application
3. The error should be gone

## Alternative: Use Private Endpoint (Advanced)

If you need to keep public access disabled for security reasons, you'll need to:
1. Set up a private endpoint
2. Configure your network to access it
3. This is more complex and usually not needed for development

## Face API Rate Limit Issue

You're also seeing:
```
(429) Requests exceeded call rate limit
```

### Solution Options:

**Option 1: Wait and Reduce Frequency (Free Tier)**
- Free tier allows 20 calls/minute
- The app now processes face detection only every 10 frames
- Wait a few minutes and try again

**Option 2: Upgrade to Paid Tier**
1. Go to Azure Portal
2. Navigate to your Face API resource
3. Go to "Pricing tier" or "Scale"
4. Upgrade to S0 tier (pay-as-you-go)
5. Higher rate limits (10 calls/second)

**Option 3: Disable Face Detection**
- Face detection is optional
- Remove Face API credentials from `.env` file
- App will work without face detection

## Quick Fix Summary

1. **Enable Public Access:**
   - Azure Portal → Computer Vision Resource → Networking → Enable Public Access

2. **Reduce Face API Calls:**
   - Already done in code (processes every 10 frames)
   - Or disable face detection by removing Face API credentials

3. **Restart Application:**
   ```bash
   # Stop current instance (Ctrl+C)
   ./start.sh
   ```

## Still Having Issues?

1. **Check Resource Status:**
   - Ensure resources are "Running" in Azure Portal
   - Check if resources are in correct region

2. **Verify API Keys:**
   - Keys should not have extra spaces
   - Copy keys directly from Azure Portal

3. **Check Endpoint URLs:**
   - Should end with `/`
   - Format: `https://your-resource.cognitiveservices.azure.com/`

4. **Wait Time:**
   - Azure changes can take 1-5 minutes to propagate
   - Be patient after making changes

## Need Help?

- Azure Documentation: [Computer Vision Networking](https://docs.microsoft.com/azure/cognitive-services/computer-vision/)
- Azure Support: Available through Azure Portal



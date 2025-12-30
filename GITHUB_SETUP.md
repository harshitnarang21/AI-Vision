# GitHub Deployment Guide

## Step 1: Create a Personal Access Token (PAT)

1. Go to GitHub: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name like "AI-Vision Deployment"
4. Select scopes:
   - ✅ **repo** (Full control of private repositories)
5. Click **"Generate token"**
6. **COPY THE TOKEN IMMEDIATELY** - you won't see it again!

## Step 2: Use Token for Authentication

When you run `git push`, use your **username** and the **token** as the password:

```bash
git push -u origin main
```

When prompted:
- **Username**: `harshitnarang21`
- **Password**: Paste your Personal Access Token (not your GitHub password)

## Alternative: Use SSH (Recommended for future)

If you prefer SSH authentication:

1. Generate SSH key (if you don't have one):
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

2. Add SSH key to GitHub:
   - Copy: `cat ~/.ssh/id_ed25519.pub`
   - Go to: https://github.com/settings/keys
   - Click "New SSH key" and paste

3. Change remote URL:
```bash
git remote set-url origin git@github.com:harshitnarang21/AI-Vision.git
```

4. Push:
```bash
git push -u origin main
```


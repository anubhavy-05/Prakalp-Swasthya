# 🚀 Complete Deployment Guide - SwasthyaGuide WhatsApp Bot

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Setup](#local-setup)
3. [Twilio Configuration](#twilio-configuration)
4. [Render Deployment](#render-deployment)
5. [Environment Variables](#environment-variables)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites

### What You Need:
- ✅ GitHub account
- ✅ Twilio account (free tier works)
- ✅ Render account (free tier works)
- ✅ Python 3.8+ installed locally
- ✅ Git installed

---

## 2. Local Setup

### Step 1: Clone and Setup
```bash
cd Prakalp-Swasthya
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Create .env File
```bash
# Copy the example file
copy .env.example .env

# Edit .env with your actual values (we'll get these from Twilio)
notepad .env
```

---

## 3. Twilio Configuration

### Step 1: Create Twilio Account
1. Go to https://www.twilio.com/try-twilio
2. Sign up (free trial gives you credits)
3. Verify your phone number

### Step 2: Get Your Credentials
1. Go to https://console.twilio.com
2. From the Dashboard, copy:
   - **Account SID** (starts with AC...)
   - **Auth Token** (click to reveal)
3. Save these in your `.env` file:
   ```env
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token_here
   ```

### Step 3: Set Up WhatsApp Sandbox
1. In Twilio Console, go to: **Messaging** → **Try it out** → **Send a WhatsApp message**
2. You'll see a WhatsApp number like: `+1 415 523 8886`
3. **Join the Sandbox:**
   - Add the number to WhatsApp: `+1 415 523 8886`
   - Send the code shown (e.g., "join <your-code>")
   - You'll get a confirmation message
4. Save the number in `.env`:
   ```env
   TWILIO_PHONE_NUMBER=whatsapp:+14155238886
   ```

### Step 4: Note Your Webhook URL (We'll configure this after deployment)
- Keep this page open - we'll come back to it

---

## 4. Render Deployment

### Step 1: Push Code to GitHub
```bash
# Make sure .env is NOT tracked (check .gitignore)
git status

# If .env appears, it's a problem! Fix .gitignore first
# Otherwise, commit and push:
git add .
git commit -m "Add WhatsApp bot with Twilio integration"
git push origin main
```

### Step 2: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

### Step 3: Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your `Prakalp-Swasthya` repository
3. Configure settings:

   **Basic Settings:**
   - Name: `swasthyaguide-whatsapp`
   - Region: Choose closest to India (Singapore recommended)
   - Branch: `main`
   - Runtime: `Python 3`

   **Build Settings:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

4. Click **"Create Web Service"**

### Step 4: Add Environment Variables in Render
1. In your Render dashboard, go to your service
2. Click **"Environment"** in the left sidebar
3. Add these variables one by one:

   ```
   FLASK_ENV=production
   FLASK_SECRET_KEY=<generate-a-random-secret-key>
   FLASK_DEBUG=False
   
   TWILIO_ACCOUNT_SID=<your-twilio-account-sid>
   TWILIO_AUTH_TOKEN=<your-twilio-auth-token>
   TWILIO_PHONE_NUMBER=whatsapp:+14155238886
   
   APP_NAME=SwasthyaGuide
   APP_VERSION=1.0.0
   LOG_LEVEL=INFO
   ```

   **To generate FLASK_SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

5. Click **"Save Changes"**
6. Render will automatically redeploy

### Step 5: Get Your Render URL
- After deployment completes, you'll see: `https://swasthyaguide-whatsapp.onrender.com`
- Test it: Open `https://swasthyaguide-whatsapp.onrender.com/`
- You should see: `{"status": "running", ...}`

---

## 5. Connect Twilio to Render

### Step 1: Configure Webhook in Twilio
1. Go back to Twilio Console: https://console.twilio.com
2. Navigate to: **Messaging** → **Try it out** → **Send a WhatsApp message**
3. Click **"Sandbox settings"**
4. In **"WHEN A MESSAGE COMES IN"**:
   - Paste your Render URL + `/whatsapp`:
     ```
     https://swasthyaguide-whatsapp.onrender.com/whatsapp
     ```
   - Method: **POST**
5. Click **"Save"**

### Step 2: Test Your Bot! 🎉
1. Open WhatsApp
2. Send a message to your Twilio number
3. Try these:
   - `Mujhe sir dard ho raha hai`
   - `I have a headache`
   - `fever`
   - `clinic andheri`

---

## 6. Environment Variables Reference

### Required Variables:
| Variable | Description | Example |
|----------|-------------|---------|
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID | `AC1234567890abcdef...` |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token | `abcdef1234567890...` |
| `FLASK_SECRET_KEY` | Flask secret for sessions | `<random-64-char-hex>` |

### Optional Variables:
| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `production` |
| `FLASK_DEBUG` | Debug mode | `False` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `MAX_MESSAGE_LENGTH` | Max chars per message | `1600` |

---

## 7. Testing

### Local Testing
```bash
# Activate virtual environment
venv\Scripts\activate

# Run the app
python app.py

# Test in another terminal
curl http://localhost:5000/
curl http://localhost:5000/health
```

### Production Testing
```bash
# Test health endpoint
curl https://swasthyaguide-whatsapp.onrender.com/health

# Check logs in Render dashboard
# Go to: Your Service → Logs
```

---

## 8. Troubleshooting

### Problem: Bot not responding on WhatsApp
**Solutions:**
1. Check Render logs for errors
2. Verify webhook URL in Twilio is correct
3. Make sure environment variables are set in Render
4. Test the `/health` endpoint - should return 200 OK

### Problem: "Configuration errors" in logs
**Solutions:**
1. Double-check all environment variables in Render
2. Make sure `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` are set
3. Regenerate and update `FLASK_SECRET_KEY`

### Problem: Import errors
**Solutions:**
1. Check `requirements.txt` has all dependencies
2. Rebuild on Render (Manual Deploy → Clear build cache)

### Problem: Bot responds but with errors
**Solutions:**
1. Check if `data/clinics.json` exists
2. Check if `data/translations.json` exists
3. Verify all module imports in `chatbot.py`

---

## 9. Important Security Notes

### ✅ DO:
- Keep `.env` file LOCAL ONLY (never commit)
- Use strong random `FLASK_SECRET_KEY`
- Set `FLASK_DEBUG=False` in production
- Monitor Render logs regularly

### ❌ DON'T:
- Never commit `.env` file to Git
- Never share Twilio credentials publicly
- Don't use default secret keys
- Don't expose sensitive logs

---

## 10. Free Tier Limits

### Twilio (Free Trial):
- Limited credits (~$15)
- WhatsApp: Pay-as-you-go after trial
- Sandbox restrictions (users must join)

### Render (Free Tier):
- App sleeps after 15 min inactivity
- First request may be slow (cold start)
- 750 hours/month free

---

## 11. Upgrading to Production

### For Real WhatsApp Business:
1. Create Twilio WhatsApp Business Account
2. Get approved by Facebook/Meta
3. Use production phone number
4. Remove sandbox restrictions

### For Better Performance:
1. Upgrade Render plan (starts at $7/month)
2. No cold starts
3. Better uptime
4. More resources

---

## 🆘 Need Help?

### Quick Checks:
```bash
# 1. Test locally first
python app.py

# 2. Check if all files exist
ls data/clinics.json
ls data/translations.json

# 3. Verify imports
python -c "from chatbot import SwasthyaGuide; print('OK')"

# 4. Test config loading
python -c "from config_loader import Config; Config.validate(); print('OK')"
```

### Common Commands:
```bash
# Install packages
pip install -r requirements.txt

# Check installed packages
pip list

# Update a package
pip install --upgrade twilio

# Test Flask app
python app.py
```

---

## ✅ Checklist Before Deployment

- [ ] `.env` file created and filled
- [ ] `.env` is in `.gitignore`
- [ ] All dependencies in `requirements.txt`
- [ ] Code pushed to GitHub
- [ ] Render service created
- [ ] Environment variables set in Render
- [ ] Twilio webhook configured
- [ ] Tested on WhatsApp
- [ ] Health check returns 200

---

**🎉 Congratulations! Your WhatsApp healthcare bot is live!**

For issues, check Render logs or Twilio debugger console.

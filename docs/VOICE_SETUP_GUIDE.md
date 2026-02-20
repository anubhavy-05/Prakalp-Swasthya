# 🚀 Quick Setup Guide - Voice Feature

## Step-by-Step Setup (15 minutes)

### 1. Prerequisites ✅

**Required:**
- Python 3.8+ installed
- Twilio account with WhatsApp sandbox
- Google Cloud account (free tier available)
- ffmpeg installed on your system

**Check if you have everything:**
```powershell
python --version  # Should show 3.8 or higher
ffmpeg -version   # Should show ffmpeg version
```

---

### 2. Install ffmpeg (Audio Processing)

**Windows:**
```powershell
# Option 1: Using Chocolatey
choco install ffmpeg

# Option 2: Manual installation
# 1. Download from: https://ffmpeg.org/download.html
# 2. Extract to C:\ffmpeg
# 3. Add C:\ffmpeg\bin to PATH environment variable
```

**Verify installation:**
```powershell
ffmpeg -version
```

---

### 3. Google Cloud Setup (Voice APIs)

#### Step 3.1: Create Project
1. Go to: https://console.cloud.google.com
2. Click "Create Project"
3. Name: "swasthya-voice" (or any name)
4. Click "Create"

#### Step 3.2: Enable APIs
1. Go to: Navigation Menu → APIs & Services → Library
2. Search "Speech-to-Text API" → Click → Enable
3. Search "Text-to-Speech API" → Click → Enable

#### Step 3.3: Create Service Account
1. Go to: Navigation Menu → IAM & Admin → Service Accounts
2. Click "Create Service Account"
3. Name: "swasthya-bot"
4. Click "Create and Continue"

#### Step 3.4: Assign Roles
Add these roles:
- Cloud Speech Administrator
- Cloud Text-to-Speech Client

Click "Continue"

#### Step 3.5: Create JSON Key
1. Click on the created service account
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Select "JSON"
5. Click "Create"
6. JSON file will download automatically

#### Step 3.6: Save Credentials
```powershell
# Create credentials folder in your project
mkdir credentials

# Move the downloaded JSON file to credentials folder
# Rename it to: google-credentials.json
move Downloads\swasthya-bot-xxxxx.json credentials\google-credentials.json
```

---

### 4. Environment Variables Setup

**Create .env file:**
```powershell
# Copy example file
copy .env.example .env

# Edit .env file
notepad .env
```

**Add these values in .env:**
```env
# Twilio (you should already have these)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here

# Google Cloud (NEW - for voice feature)
GOOGLE_APPLICATION_CREDENTIALS=./credentials/google-credentials.json

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/swasthya

# Flask
SECRET_KEY=generate-a-random-string-here
FLASK_ENV=development
DEBUG=True
```

---

### 5. Install Dependencies

```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Install all dependencies (including new voice libraries)
pip install -r requirements.txt

# This will install:
# - google-cloud-speech
# - google-cloud-texttospeech
# - pydub
# - and all existing dependencies
```

**Verify installation:**
```powershell
pip list | findstr google
# Should show:
# google-cloud-speech      2.21.0
# google-cloud-texttospeech 2.14.1
```

---

### 6. Test Locally

#### Start Flask App:
```powershell
python app.py
```

**Expected output:**
```
INFO: SwasthyaGuide session manager initialized
INFO: Google Cloud Speech services initialized successfully
INFO: Voice handler initialized. Temp dir: C:\Users\...\Temp\swasthya_voice
INFO: Starting SwasthyaGuide on port 5000
 * Running on http://0.0.0.0:5000
```

#### Expose to Internet (ngrok):
```powershell
# In a new terminal
ngrok http 5000
```

**Copy the HTTPS URL:**
```
Forwarding: https://abc123.ngrok.io → http://localhost:5000
```

#### Configure Twilio Webhook:
1. Go to: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox
2. "When a message comes in" field:
   ```
   https://abc123.ngrok.io/whatsapp
   ```
3. Save

---

### 7. Test Voice Messages

#### Send Test Message:
1. Open WhatsApp
2. Send "join [your-sandbox-code]" to Twilio number
3. **Press and hold the microphone button**
4. Say: "Mujhe bukhar hai" (in Hindi)
5. Release to send

#### Check Logs:
You should see in terminal:
```
INFO: 🎤 Voice message detected! Type: audio/ogg
INFO: Downloading voice message...
INFO: Voice message downloaded: 54321 bytes
INFO: Converting audio: ogg -> wav
INFO: ✅ Voice transcribed: 'मुझे बुखार है'
INFO: 📝 Sending text response...
INFO: 🔊 Converting response to speech...
```

#### Expected Response from Bot:
```
🎤 आपने कहा: मुझे बुखार है

🌡️ बुखार - सामान्य सलाह

लक्षण:
• बुखार (Fever)

घरेलू उपचार:
1. आराम करें
2. पानी पिएं
3. पैरासिटामोल लें

[... more details ...]
```

---

### 8. Deploy to Production

#### Option A: Render.com

**1. Add Google Credentials as Secret File:**
- Render Dashboard → Your Service
- Environment → Secret Files
- Add file:
  - Filename: `/etc/secrets/google-creds.json`
  - Contents: [Paste your JSON file contents]

**2. Add Environment Variable:**
```
GOOGLE_APPLICATION_CREDENTIALS=/etc/secrets/google-creds.json
```

**3. Update render.yaml:**
Already configured! Just push to GitHub.

**4. Deploy:**
```powershell
git add .
git commit -m "Add voice feature"
git push origin main
```

#### Option B: Railway.app

**1. Add Environment Variables:**
```
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/google-credentials.json
```

**2. Upload Credentials:**
- Railway Dashboard → Variables
- Add file upload (coming soon) or use base64:

```powershell
# Encode credentials
$content = Get-Content credentials\google-credentials.json -Raw
$bytes = [System.Text.Encoding]::UTF8.GetBytes($content)
$base64 = [Convert]::ToBase64String($bytes)
echo $base64
```

Add variable:
```
GOOGLE_CREDS_BASE64=[paste encoded content]
```

Update `app.py` to decode:
```python
import os
import json
import base64

# Decode Google credentials from base64
creds_b64 = os.getenv('GOOGLE_CREDS_BASE64')
if creds_b64:
    creds_json = base64.b64decode(creds_b64).decode('utf-8')
    os.makedirs('credentials', exist_ok=True)
    with open('credentials/google-credentials.json', 'w') as f:
        f.write(creds_json)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './credentials/google-credentials.json'
```

---

### 9. Verify Production Deployment

**Test Webhook:**
```powershell
# Send POST request to your production URL
curl -X POST https://your-app.onrender.com/whatsapp
```

**Expected response:**
```json
{
  "status": "webhook active",
  "message": "WhatsApp webhook is ready to receive messages"
}
```

**Update Twilio Webhook:**
1. Twilio Console → WhatsApp Settings
2. Change webhook URL to production:
   ```
   https://your-app.onrender.com/whatsapp
   ```

**Test Voice Message:**
Send a voice message via WhatsApp → Should work!

---

### 10. Monitor & Troubleshoot

#### Check Logs:
**Render:**
- Dashboard → Logs tab
- Look for voice processing messages

**Railway:**
- Dashboard → Deployments → View Logs

**Common Errors:**

**"Google credentials not found"**
```
✗ Fix: Check GOOGLE_APPLICATION_CREDENTIALS path
✓ Should be: /etc/secrets/google-creds.json (Render)
```

**"ffmpeg not found"**
```
✗ Fix: Add buildpack/build command
✓ Render: Already in render.yaml
✓ Railway: Automatically installed
```

**"Speech API quota exceeded"**
```
✗ Fix: Check Google Cloud Console quotas
✓ Free tier: 60 minutes/month
✓ Paid tier: Increase quota or enable billing
```

---

## ✅ Checklist

Before going live, verify:

- [ ] ffmpeg installed locally
- [ ] Google Cloud project created
- [ ] Speech-to-Text API enabled
- [ ] Text-to-Speech API enabled
- [ ] Service account created
- [ ] JSON credentials downloaded
- [ ] `.env` file configured
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Local testing successful (voice → text → response)
- [ ] ngrok testing successful
- [ ] Production deployment successful
- [ ] Production webhook configured
- [ ] Production voice message test successful
- [ ] Monitoring/logging configured

---

## 📚 Next Steps

**After successful deployment:**

1. **Share with Users:**
   - Send instructions on how to use voice messages
   - Target rural areas where literacy is low
   - Demonstrate to health workers

2. **Monitor Usage:**
   - Track voice vs text message ratio
   - Monitor Google API costs
   - Analyze language distribution

3. **Optimize:**
   - Implement audio response delivery (future enhancement)
   - Add voice analytics
   - Improve accuracy for regional accents

4. **Scale:**
   - Monitor server resources
   - Implement caching for common queries
   - Add load balancing if needed

---

## 🆘 Need Help?

**Resources:**
- Detailed explanation: `docs/VOICE_FEATURE_EXPLANATION_HINGLISH.md`
- Voice handler code: `src/voice_handler.py`
- Webhook code: `app.py` (lines ~160-230)

**Common Questions:**
- Q: Do I need billing enabled on Google Cloud?
  - A: No, free tier (60 min/month) is enough for testing

- Q: How much will it cost for production?
  - A: ~$1,380/month for 1000 daily active users (see detailed breakdown in Hinglish doc)

- Q: Can I use other Speech APIs instead of Google?
  - A: Yes! Can integrate Azure, AWS Transcribe, or open-source models

---

**Ready to launch! 🚀**

Good luck with your SwasthyaGuide voice feature!

# ⚡ QUICK START GUIDE - SwasthyaGuide

## 🚀 5-MINUTE SETUP

### 1. Create .env File (2 min)
```bash
copy .env.example .env
notepad .env
```

Add your credentials:
```env
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
FLASK_SECRET_KEY=<generate-random-key>
```

### 2. Install Packages (1 min)
```bash
pip install flask twilio python-dotenv gunicorn werkzeug
```

### 3. Test Locally (1 min)
```bash
python app.py
```
Visit: http://localhost:5000

### 4. Deploy to Render (Follow DEPLOYMENT_GUIDE.md)

---

## 📋 QUICK COMMANDS

```bash
# Run locally
python app.py

# Run CLI version
python main.py

# Install dependencies
pip install -r requirements.txt

# Generate secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Check if modules work
python -c "from chatbot import SwasthyaGuide; print('OK')"
```

---

## 🔑 WHERE TO GET CREDENTIALS

### Twilio:
1. Sign up: https://www.twilio.com/try-twilio
2. Dashboard: https://console.twilio.com
3. Get: Account SID + Auth Token
4. WhatsApp: Messaging → Try it out → WhatsApp

### Render:
1. Sign up: https://render.com
2. New → Web Service
3. Connect GitHub
4. Add environment variables

---

## 🧪 TEST MESSAGES

Send these to your WhatsApp bot:

**Hindi:**
- `Mujhe sir dard ho raha hai`
- `Bukhar hai`
- `Pet dard ho raha hai`
- `Doctor chahiye Andheri`

**English:**
- `I have a headache`
- `Fever`
- `Stomach pain`
- `Find clinic in Mumbai`

**Emergency:**
- `Chest pain`
- `Can't breathe`

---

## 🆘 QUICK FIXES

**Import Error?**
```bash
pip install flask twilio python-dotenv
```

**.env Not Working?**
- Make sure file is named `.env` (not `.env.txt`)
- Check it's in project root folder
- Verify python-dotenv is installed

**Twilio Error?**
- Check Account SID starts with "AC"
- Verify Auth Token is correct
- Test credentials in Twilio Console

**Render Not Working?**
- Check environment variables are set
- View logs in Render dashboard
- Test /health endpoint

---

## 📚 DOCUMENTATION

- **Full Guide**: DEPLOYMENT_GUIDE.md
- **Overview**: README.md
- **Summary**: PROJECT_SUMMARY.md

---

## ✅ DEPLOYMENT CHECKLIST

- [ ] .env file created
- [ ] Twilio credentials added
- [ ] Secret key generated
- [ ] Tested locally (python app.py)
- [ ] Pushed to GitHub (.env NOT included)
- [ ] Render service created
- [ ] Environment variables set in Render
- [ ] Twilio webhook configured
- [ ] Tested on WhatsApp

---

**🎉 That's it! You're ready to deploy!**

Read DEPLOYMENT_GUIDE.md for complete instructions.

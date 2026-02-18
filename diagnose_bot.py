# -*- coding: utf-8 -*-
"""
Diagnostic Tool - Check WhatsApp Bot Configuration and Issues
"""

import os
import sys
from dotenv import load_dotenv
from src.chatbot import SwasthyaGuide
from src.config_loader import Config

load_dotenv()

print("=" * 70)
print("🔍 WHATSAPP BOT DIAGNOSTIC TOOL")
print("=" * 70)

# Check 1: Twilio Configuration
print("\n1️⃣ TWILIO CONFIGURATION:")
print("-" * 70)
twilio_sid = Config.TWILIO_ACCOUNT_SID
twilio_token = Config.TWILIO_AUTH_TOKEN
twilio_number = Config.TWILIO_PHONE_NUMBER

if not twilio_sid or twilio_sid.startswith("your_"):
    print("❌ TWILIO_ACCOUNT_SID: NOT CONFIGURED (placeholder)")
    print("   → This will cause IMAGE DOWNLOAD to FAIL!")
else:
    print(f"✅ TWILIO_ACCOUNT_SID: {twilio_sid[:15]}...")

if not twilio_token or twilio_token.startswith("your_"):
    print("❌ TWILIO_AUTH_TOKEN: NOT CONFIGURED (placeholder)")
    print("   → This will cause IMAGE DOWNLOAD to FAIL!")
else:
    print(f"✅ TWILIO_AUTH_TOKEN: {twilio_token[:15]}...")

print(f"✅ TWILIO_PHONE_NUMBER: {twilio_number}")

# Check 2: Hugging Face API
print("\n2️⃣ HUGGING FACE API:")
print("-" * 70)
hf_key = os.getenv("HUGGINGFACE_API_KEY")
if hf_key and hf_key.startswith("hf_") and not hf_key.startswith("hf_your"):
    print(f"✅ HUGGINGFACE_API_KEY: {hf_key[:20]}...")
else:
    print("❌ HUGGINGFACE_API_KEY: NOT CONFIGURED")

# Check 3: Test Chatbot Response
print("\n3️⃣ CHATBOT FUNCTIONALITY TEST:")
print("-" * 70)
try:
    bot = SwasthyaGuide()
    
    # Test 1: Simple fever message
    test_msg1 = "mujhe bukhar hai"
    print(f"\n   Test Message: '{test_msg1}'")
    response1 = bot.process_message(test_msg1)
    
    if response1 and len(response1) > 50:
        print(f"   ✅ RESPONSE GENERATED: {len(response1)} characters")
        print(f"   Preview: {response1[:100]}...")
    else:
        print(f"   ❌ RESPONSE TOO SHORT OR EMPTY: {len(response1)} characters")
        print(f"   Response: {response1}")
    
    # Test 2: Clinic request
    test_msg2 = "clinic chahiye Lucknow"
    print(f"\n   Test Message: '{test_msg2}'")
    response2 = bot.process_message(test_msg2)
    
    if response2 and len(response2) > 50:
        print(f"   ✅ RESPONSE GENERATED: {len(response2)} characters")
        print(f"   Preview: {response2[:100]}...")
    else:
        print(f"   ❌ RESPONSE TOO SHORT OR EMPTY")
    
except Exception as e:
    print(f"   ❌ CHATBOT ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

# Check 4: Server Status
print("\n4️⃣ SERVER STATUS:")
print("-" * 70)
print("   To check if your server is running:")
print("   → Local: python app.py")
print("   → Production: Check your hosting dashboard (Render/Heroku)")
print("   → Test webhook: curl http://your-server-url/health")

# Check 5: Common Issues
print("\n5️⃣ COMMON ISSUES & SOLUTIONS:")
print("-" * 70)

issues_found = []

if not twilio_sid or twilio_sid.startswith("your_"):
    issues_found.append({
        'issue': 'Twilio credentials not configured',
        'symptom': 'Image download fails with "Error downloading image"',
        'fix': 'Get credentials from https://console.twilio.com and add to .env'
    })

if not hf_key or not hf_key.startswith("hf_"):
    issues_found.append({
        'issue': 'Hugging Face API not configured',
        'symptom': 'AI image analysis won\'t work',
        'fix': 'Get token from https://huggingface.co/settings/tokens and add to .env'
    })

if issues_found:
    for i, issue in enumerate(issues_found, 1):
        print(f"\n   Issue #{i}: {issue['issue']}")
        print(f"   Symptom: {issue['symptom']}")
        print(f"   Fix: {issue['fix']}")
else:
    print("   ✅ No common configuration issues detected!")

# Summary
print("\n" + "=" * 70)
print("📋 DIAGNOSTIC SUMMARY:")
print("=" * 70)

critical_issues = []
warnings = []

if not twilio_sid or twilio_sid.startswith("your_"):
    critical_issues.append("Twilio Account SID missing")
if not twilio_token or twilio_token.startswith("your_"):
    critical_issues.append("Twilio Auth Token missing")

if critical_issues:
    print("\n🚨 CRITICAL ISSUES (must fix):")
    for issue in critical_issues:
        print(f"   - {issue}")
else:
    print("\n✅ All critical configurations OK")

if warnings:
    print("\n⚠️  WARNINGS:")
    for warning in warnings:
        print(f"   - {warning}")

print("\n" + "=" * 70)
print("💡 NEXT STEPS:")
print("=" * 70)

if critical_issues:
    print("\n1. Fix the critical issues above")
    print("2. Get Twilio credentials from: https://console.twilio.com")
    print("3. Update your .env file with real credentials")
    print("4. Restart your server")
    print("5. Run this diagnostic again to verify")
else:
    print("\n✅ Configuration looks good!")
    print("\nIf WhatsApp still not responding:")
    print("1. Check if server is running (python app.py)")
    print("2. Check Twilio webhook is configured correctly")
    print("3. Check server logs for errors")
    print("4. Test locally first with: python main.py")

print("\n" + "=" * 70)

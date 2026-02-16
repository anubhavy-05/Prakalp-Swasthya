#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Diagnostic script to check SwasthyaGuide dependencies and configuration
Run this on your server to verify everything is set up correctly
"""

import sys
import os

print("=" * 70)
print("SwasthyaGuide - Dependency & Configuration Diagnostic")
print("=" * 70)

# Check Python version
print(f"\n✓ Python Version: {sys.version}")
print(f"  Python Executable: {sys.executable}")

# Check required modules
print("\n" + "=" * 70)
print("Checking Required Dependencies:")
print("=" * 70)

dependencies = {
    'flask': 'Flask',
    'twilio': 'Twilio',
    'PIL': 'Pillow (Image Processing)',
    'numpy': 'NumPy (Numerical Computing)',
    'requests': 'Requests (HTTP)',
    'psycopg2': 'PostgreSQL Driver',
    'sqlalchemy': 'SQLAlchemy (ORM)',
}

all_ok = True
for module, name in dependencies.items():
    try:
        __import__(module)
        print(f"✅ {name}")
    except ImportError:
        print(f"❌ {name} - NOT INSTALLED")
        all_ok = False

# Check custom modules
print("\n" + "=" * 70)
print("Checking Custom Modules:")
print("=" * 70)

custom_modules = [
    'src.chatbot',
    'src.language_detector',
    'src.image_analyzer',
    'src.health_responses',
    'src.symptom_checker',
    'src.clinic_finder',
    'src.emergency_handler',
]

for module in custom_modules:
    try:
        __import__(module)
        print(f"✅ {module}")
    except ImportError as e:
        print(f"❌ {module} - {str(e)}")
        all_ok = False

# Check environment variables
print("\n" + "=" * 70)
print("Checking Environment Variables:")
print("=" * 70)

env_vars = [
    'TWILIO_ACCOUNT_SID',
    'TWILIO_AUTH_TOKEN',
    'TWILIO_PHONE_NUMBER',
    'DATABASE_URL',
]

for var in env_vars:
    value = os.getenv(var)
    if value:
        # Mask sensitive data
        if len(value) > 10:
            masked = value[:4] + '*' * (len(value) - 8) + value[-4:]
        else:
            masked = '*' * len(value)
        print(f"✅ {var} = {masked}")
    else:
        print(f"⚠️  {var} - NOT SET")

# Test image analyzer specifically
print("\n" + "=" * 70)
print("Testing Image Analyzer:")
print("=" * 70)

try:
    from src.image_analyzer import ImageAnalyzer
    from PIL import Image
    import io
    
    analyzer = ImageAnalyzer()
    print("✅ ImageAnalyzer instance created")
    
    # Create a tiny test image
    test_img = Image.new('RGB', (100, 100), color=(200, 150, 150))
    img_byte_arr = io.BytesIO()
    test_img.save(img_byte_arr, format='JPEG')
    test_data = img_byte_arr.getvalue()
    
    print(f"✅ Test image created ({len(test_data)} bytes)")
    
    # Try to analyze
    result = analyzer.analyze_skin_condition(test_data, language='english')
    if result['success']:
        print("✅ Image analysis working correctly")
    else:
        print(f"⚠️  Image analysis returned error: {result['error']}")
        
except Exception as e:
    print(f"❌ Image analyzer test failed: {str(e)}")
    import traceback
    traceback.print_exc()
    all_ok = False

# Test Twilio connection (optional)
print("\n" + "=" * 70)
print("Testing Twilio Connection (Optional):")
print("=" * 70)

try:
    from twilio.rest import Client
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    
    if account_sid and auth_token:
        try:
            client = Client(account_sid, auth_token)
            account = client.api.accounts(account_sid).fetch()
            print(f"✅ Twilio connection successful")
            print(f"   Account Status: {account.status}")
        except Exception as e:
            print(f"⚠️  Twilio connection failed: {str(e)}")
    else:
        print("⚠️  Twilio credentials not set - skipping test")
        
except Exception as e:
    print(f"❌ Twilio test error: {str(e)}")

# Final summary
print("\n" + "=" * 70)
if all_ok:
    print("✅ ALL CHECKS PASSED - SwasthyaGuide should work correctly")
else:
    print("⚠️  SOME ISSUES DETECTED - Please review the errors above")
print("=" * 70)

print("\nIf image processing still fails, check:")
print("1. Server has enough memory (at least 512MB free)")
print("2. PIL/Pillow is properly installed: pip install Pillow>=10.0.0")
print("3. NumPy is properly installed: pip install numpy>=1.24.0")
print("4. Server logs for specific error messages")
print("5. Twilio media URLs are accessible from your server")

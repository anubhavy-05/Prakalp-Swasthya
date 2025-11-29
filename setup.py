# -*- coding: utf-8 -*-
"""
Setup Script for SwasthyaGuide
Automates initial setup and validation
"""

import os
import sys
import secrets
import subprocess


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Incompatible")
        print("   Please install Python 3.8 or higher")
        return False


def install_dependencies():
    """Install required packages"""
    print_header("Installing Dependencies")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def create_env_file():
    """Create .env file from template"""
    print_header("Creating Environment File")
    
    if os.path.exists('.env'):
        response = input("⚠️  .env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("✅ Keeping existing .env file")
            return True
    
    # Generate secret key
    secret_key = secrets.token_hex(32)
    
    # Read template
    with open('.env.example', 'r') as f:
        template = f.read()
    
    # Replace with generated secret
    env_content = template.replace(
        'your-super-secret-key-change-this-in-production',
        secret_key
    )
    
    # Write .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully")
    print(f"   Generated FLASK_SECRET_KEY: {secret_key[:20]}...")
    print("\n⚠️  IMPORTANT: Edit .env file and add your Twilio credentials!")
    return True


def check_data_files():
    """Check if required data files exist"""
    print_header("Checking Data Files")
    
    required_files = [
        'data/clinics.json',
        'data/translations.json',
        'config.json'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - Missing")
            all_exist = False
    
    return all_exist


def test_imports():
    """Test if all modules can be imported"""
    print_header("Testing Module Imports")
    
    modules = [
        'flask',
        'twilio',
        'dotenv',
        'chatbot',
        'config_loader'
    ]
    
    all_imported = True
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - Failed: {e}")
            all_imported = False
    
    return all_imported


def display_next_steps():
    """Display next steps for user"""
    print_header("Setup Complete! 🎉")
    print("""
Next Steps:

1. Configure Twilio:
   - Edit .env file with your Twilio credentials
   - Get credentials from: https://console.twilio.com

2. Test Locally:
   python app.py
   
3. Deploy to Render:
   - Follow DEPLOYMENT_GUIDE.md for detailed steps
   - Push code to GitHub (make sure .env is NOT committed!)
   - Create Render web service
   - Add environment variables in Render

4. Connect WhatsApp:
   - Configure webhook in Twilio
   - Test with WhatsApp messages

📚 Read DEPLOYMENT_GUIDE.md for complete instructions!
""")


def main():
    """Main setup function"""
    print_header("SwasthyaGuide Setup Script")
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Create .env file
    if not create_env_file():
        return
    
    # Check data files
    if not check_data_files():
        print("\n⚠️  Some data files are missing. Please check your project structure.")
    
    # Test imports
    if not test_imports():
        print("\n⚠️  Some modules failed to import. Please check error messages above.")
        return
    
    # Display next steps
    display_next_steps()


if __name__ == "__main__":
    main()

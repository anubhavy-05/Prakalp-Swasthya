# -*- coding: utf-8 -*-
"""
Test script to verify webhook functionality locally
Run this to test if the bot responds correctly
"""

from chatbot import SwasthyaGuide

def test_bot():
    """Test the bot with various messages"""
    bot = SwasthyaGuide()
    
    test_messages = [
        "Mujhe sir dard ho raha hai",
        "I have a headache",
        "बुखार है",
        "emergency - chest pain",
        "clinic chahiye Delhi"
    ]
    
    print("=" * 60)
    print("Testing SwasthyaGuide Bot Responses")
    print("=" * 60)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n[Test {i}] User: {message}")
        try:
            response = bot.process_message(message)
            print(f"Bot: {response[:200]}..." if len(response) > 200 else f"Bot: {response}")
        except Exception as e:
            print(f"ERROR: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_bot()

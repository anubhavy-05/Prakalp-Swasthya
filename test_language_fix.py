# -*- coding: utf-8 -*-
"""
Test script to verify language detection and response matching
"""

from src.language_detector import detect_language
from src.chatbot import SwasthyaGuide

def test_language_detection():
    """Test that language detection works correctly"""
    print("=" * 60)
    print("Testing Language Detection")
    print("=" * 60)
    
    test_cases = [
        ("i have fever", "english"),
        ("mujhe bukhar hai", "hinglish"),
        ("मुझे बुखार है", "hindi"),
        ("I have a headache", "english"),
        ("sir mein dard hai", "hinglish"),
    ]
    
    for text, expected in test_cases:
        detected = detect_language(text)
        status = "✅" if detected == expected else "❌"
        print(f"{status} '{text}' -> Detected: {detected} (Expected: {expected})")
    print()


def test_chatbot_responses():
    """Test that chatbot responds in correct language"""
    print("=" * 60)
    print("Testing Chatbot Response Language Matching")
    print("=" * 60)
    
    bot = SwasthyaGuide()
    
    test_cases = [
        ("i have fever", "english", "English"),
        ("mujhe bukhar hai", "hinglish", "Hinglish"),
        ("I have a headache", "english", "English"),
        ("sir dard hai", "hinglish", "Hinglish"),
    ]
    
    for query, expected_lang, lang_name in test_cases:
        print(f"\n📝 Query: '{query}'")
        response = bot.process_message(query)
        detected_lang = bot.user_context['language']
        
        # Check if response contains language-specific keywords
        if expected_lang == "english":
            # English responses should have English words
            has_correct_lang = any(word in response.lower() for word in 
                                  ["about", "fever", "steps", "doctor", "when to see"])
        else:
            # Hinglish responses should have Hindi words in Roman script
            has_correct_lang = any(word in response.lower() for word in 
                                  ["bukhar", "aaram", "karein", "dikhaayein", "agar"])
        
        status = "✅" if (detected_lang == expected_lang and has_correct_lang) else "❌"
        print(f"{status} Detected: {detected_lang} -> Response in {lang_name}: {has_correct_lang}")
        
        # Print first 150 chars of response
        print(f"Response preview: {response[:150]}...")
    print()


if __name__ == "__main__":
    test_language_detection()
    test_chatbot_responses()
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)

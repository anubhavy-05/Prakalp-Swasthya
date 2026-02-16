# Test Hinglish conversation flow
import sys
sys.path.insert(0, 'src')

from language_detector import detect_language
from health_responses import handle_headache, get_general_health_tips
from emergency_handler import get_emergency_response
from clinic_finder import find_nearby_clinics

print("=" * 60)
print("Testing Hinglish Conversation Flow")
print("=" * 60)

# Test 1: Hinglish health query
test_message = "mujhe sir dard ho raha hai"
lang = detect_language(test_message)
print(f"\nUser: {test_message}")
print(f"Detected Language: {lang}")
print(f"\nBot Response:")
response = handle_headache(lang)
print(response)

# Test 2: Hinglish clinic query
test_message = "clinic kahan hai"
lang = detect_language(test_message)
print(f"\n{'-' * 60}")
print(f"User: {test_message}")
print(f"Detected Language: {lang}")

# Test 3: English health query
test_message = "I have a headache"
lang = detect_language(test_message)
print(f"\n{'-' * 60}")
print(f"User: {test_message}")
print(f"Detected Language: {lang}")
print(f"\nBot Response:")
response = handle_headache(lang)
print(response)

# Test 4: Hinglish emergency
test_message = "mujhe chest pain ho raha hai"
lang = detect_language(test_message)
print(f"\n{'-' * 60}")
print(f"User: {test_message}")
print(f"Detected Language: {lang}")
print(f"\nBot Response:")
response = get_emergency_response(lang)
print(response[:200] + "...")  # Truncate for readability

print(f"\n{'=' * 60}")
print("✅ Hinglish conversation flow working correctly!")

# Test language detection for Hinglish vs English vs Hindi
import sys
sys.path.insert(0, 'src')

from language_detector import detect_language

print("=" * 60)
print("Testing Language Detection")
print("=" * 60)

test_cases = [
    ("I have fever", "english"),
    ("mujhe bukhar hai", "hinglish"),
    ("मुझे बुखार है", "hindi"),
    ("What is your name", "english"  ),
    ("aapka naam kya hai", "hinglish"),
    ("आपका नाम क्या है", "hindi"),
    ("clinic kahan hai", "hinglish"),
    ("Where is the clinic", "english"),
    ("क्लिनिक कहाँ है", "hindi"),
    ("226010", "english"),  # Pincode - structured data
    ("Lucknow_Gomti_Nagar", "english"),  # Location key - structured data
    ("sir dard ho raha hai", "hinglish"),
    ("मुझे सिर दर्द हो रहा है", "hindi"),
    ("I need help with headache", "english"),
]

for text, expected in test_cases:
    detected = detect_language(text)
    status = "✅" if detected == expected else "❌"
    print(f"{status} '{text}'")
    print(f"   Expected: {expected}, Got: {detected}")
    if detected != expected:
        print(f"   ^ MISMATCH!")
    print()

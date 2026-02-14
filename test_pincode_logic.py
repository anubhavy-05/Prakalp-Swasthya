# Simple test without imports
text = "226010"

# Test 1: Check if it's a pincode
if text.isdigit() and len(text) == 6:
    print(f"✅ '{text}' is detected as a pincode")
else:
    print(f"❌ '{text}' is NOT detected as a pincode")
    print(f"   isdigit(): {text.isdigit()}")
    print(f"   len(): {len(text)}")

# Test 2: Check affirmative words logic
user_words = text.lower().split()
affirmative_words = ['yes', 'haan', 'ha', 'ji', 'zaroor', 'chahiye', 'chahie', 
                    'sure', 'ok', 'okay', 'please', 'kripya', 'batao', 'bataye']

has_affirmative = any(word in user_words for word in affirmative_words)
word_count = len(text.split())

print(f"\nAffirmative word check:")
print(f"   user_words: {user_words}")
print(f"   has_affirmative: {has_affirmative}")
print(f"   word_count: {word_count}")
print(f"   word_count <= 3: {word_count <= 3}")

if has_affirmative and word_count <= 3:
    print("   ⚠️  Would trigger affirmative response (ask for location again)")
else:
    print("   ✅ Would proceed to extract_location")

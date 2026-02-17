# -*- coding: utf-8 -*-
"""
Test script to verify chatbot fixes for symptom detection while waiting for location
"""

from src.chatbot import SwasthyaGuide
from src.clinic_finder import extract_location
from src.symptom_checker import extract_symptoms

print("=" * 60)
print("Testing Chatbot Fixes")
print("=" * 60)

# Test 1: Location extraction should NOT accept symptom descriptions
print("\n1. Testing location extraction with symptom text:")
test_inputs = [
    "mujhe bukhar hai",
    "have fever",
    "sir dard hai",
    "Lucknow",
    "226010",
    "Gomti Nagar"
]

for text in test_inputs:
    location = extract_location(text)
    print(f"   '{text}' -> Location: {location}")

# Test 2: Symptom extraction should work
print("\n2. Testing symptom extraction:")
for text in ["mujhe bukhar hai", "have fever", "sir dard hai"]:
    symptoms = extract_symptoms(text)
    print(f"   '{text}' -> Symptoms: {symptoms}")

# Test 3: Full conversation flow
print("\n3. Testing full conversation flow:")
chatbot = SwasthyaGuide(session_id="test_session")

# First message: report fever
print("\n   User: have fever")
response1 = chatbot.process_message("have fever")
print(f"   Bot: {response1[:200]}...")
print(f"   Waiting for location: {chatbot.user_context.get('waiting_for_location')}")

# Second message: report another symptom (should NOT be treated as location)
print("\n   User: mujhe bukhar hai")
response2 = chatbot.process_message("mujhe bukhar hai")
print(f"   Bot: {response2[:200]}...")
print(f"   Waiting for location: {chatbot.user_context.get('waiting_for_location')}")
print(f"   Symptoms: {chatbot.user_context.get('symptoms')}")

# Third message: provide actual location
print("\n   User: Lucknow")
response3 = chatbot.process_message("Lucknow")
print(f"   Bot: {response3[:200]}...")
print(f"   Waiting for location: {chatbot.user_context.get('waiting_for_location')}")

print("\n" + "=" * 60)
print("✅ Test completed!")
print("=" * 60)

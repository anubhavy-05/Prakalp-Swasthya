# Quick test to debug pincode issue
import sys
sys.path.insert(0, 'src')

from clinic_finder import extract_location, search_clinics_in_json

# Test extract_location with pincode
test_input = "226010"
print(f"Testing extract_location('{test_input}'):")
result = extract_location(test_input)
print(f"  Result: {result}")
print(f"  Type: {type(result)}")
print()

# Test with whitespace
test_input2 = " 226010 "
print(f"Testing extract_location('{test_input2}'):")
result2 = extract_location(test_input2)
print(f"  Result: {result2}")
print()

# Test JSON search
print("Testing search_clinics_in_json('226010'):")
clinics = search_clinics_in_json("226010")
print(f"  Found {len(clinics)} clinics")
for i, clinic in enumerate(clinics[:3], 1):
    print(f"  {i}. {clinic['name']}")

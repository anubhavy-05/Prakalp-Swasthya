# -*- coding: utf-8 -*-
"""
Test script for clinic finder with new JSON fallback
"""

import sys
sys.path.insert(0, 'src')

from clinic_finder import find_nearby_clinics, search_clinics_in_json, extract_location

def test_clinic_search():
    """Test various clinic search scenarios"""
    
    print("=" * 60)
    print("Testing Clinic Finder with JSON Fallback")
    print("=" * 60)
    
    # Test 1: Exact location key
    print("\n1. Testing exact location key: 'Lucknow_Gomti_Nagar_Patrakarpuram'")
    result = find_nearby_clinics("Lucknow_Gomti_Nagar_Patrakarpuram", "hindi")
    print(result)
    
    # Test 2: Partial location match
    print("\n2. Testing partial match: 'Patrakarpuram'")
    result = find_nearby_clinics("Patrakarpuram", "hindi")
    print(result)
    
    # Test 3: Pincode search
    print("\n3. Testing pincode: '226010'")
    result = find_nearby_clinics("226010", "hindi")
    print(result)
    
    # Test 4: Area name
    print("\n4. Testing area name: 'Gomti Nagar'")
    result = find_nearby_clinics("Gomti Nagar", "english")
    print(result)
    
    # Test 5: Direct JSON search
    print("\n5. Testing direct JSON search for 'Lucknow_Gomti_Nagar_Patrakarpuram'")
    clinics = search_clinics_in_json("Lucknow_Gomti_Nagar_Patrakarpuram")
    print(f"Found {len(clinics)} clinics")
    for i, clinic in enumerate(clinics[:3], 1):
        print(f"  {i}. {clinic['name']} - {clinic['address']}")

if __name__ == "__main__":
    test_clinic_search()

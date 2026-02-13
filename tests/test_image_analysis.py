# -*- coding: utf-8 -*-
"""
Image Analysis Test Script
Tests image upload, validation, and analysis features
"""

import os
from PIL import Image
import io
from image_analyzer import ImageAnalyzer


def create_test_image(width=800, height=600, color='red'):
    """Create a test image for testing"""
    img = Image.new('RGB', (width, height), color=color)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    return img_bytes.getvalue()


def test_image_validation():
    """Test image validation logic"""
    print("=" * 70)
    print("TESTING IMAGE VALIDATION")
    print("=" * 70)
    
    analyzer = ImageAnalyzer()
    
    # Test 1: Valid image
    print("\n📝 Test 1: Valid image (800x600)")
    test_img = create_test_image(800, 600)
    is_valid, message = analyzer.validate_image(test_img, 'image/jpeg')
    print(f"   Result: {'✅ PASS' if is_valid else '❌ FAIL'}")
    print(f"   Message: {message}")
    
    # Test 2: Too small image
    print("\n📝 Test 2: Too small image (50x50)")
    small_img = create_test_image(50, 50)
    is_valid, message = analyzer.validate_image(small_img, 'image/jpeg')
    print(f"   Result: {'✅ PASS - Correctly rejected' if not is_valid else '❌ FAIL'}")
    print(f"   Message: {message}")
    
    # Test 3: Too large file
    print("\n📝 Test 3: Large image file simulation")
    large_data = b'x' * (11 * 1024 * 1024)  # 11MB
    is_valid, message = analyzer.validate_image(large_data, 'image/jpeg')
    print(f"   Result: {'✅ PASS - Correctly rejected' if not is_valid else '❌ FAIL'}")
    print(f"   Message: {message}")


def test_image_preprocessing():
    """Test image preprocessing"""
    print("\n" + "=" * 70)
    print("TESTING IMAGE PREPROCESSING")
    print("=" * 70)
    
    analyzer = ImageAnalyzer()
    
    # Test different image sizes
    test_cases = [
        (800, 600, "Standard image"),
        (2000, 1500, "Large image - should resize"),
        (400, 300, "Small image - no resize"),
    ]
    
    for width, height, description in test_cases:
        print(f"\n📝 Test: {description} ({width}x{height})")
        test_img = create_test_image(width, height)
        processed = analyzer.preprocess_image(test_img)
        print(f"   Original size: {width}x{height}")
        print(f"   Processed size: {processed.size[0]}x{processed.size[1]}")
        print(f"   Color mode: {processed.mode}")
        print(f"   ✅ Preprocessing successful")


def test_image_quality_assessment():
    """Test image quality assessment"""
    print("\n" + "=" * 70)
    print("TESTING IMAGE QUALITY ASSESSMENT")
    print("=" * 70)
    
    analyzer = ImageAnalyzer()
    
    test_cases = [
        (1920, 1080, "Full HD"),
        (800, 600, "Standard"),
        (400, 300, "Low resolution"),
        (200, 150, "Very low resolution"),
    ]
    
    for width, height, description in test_cases:
        print(f"\n📝 Test: {description} ({width}x{height})")
        test_img = create_test_image(width, height)
        img = analyzer.preprocess_image(test_img)
        analysis = analyzer.analyze_image_basic(img)
        quality = analyzer._assess_image_quality(img)
        
        print(f"   Resolution: {analysis['resolution']}")
        print(f"   Quality Score: {quality}")
        print(f"   ✅ Assessment complete")


def test_skin_condition_analysis():
    """Test skin condition analysis"""
    print("\n" + "=" * 70)
    print("TESTING SKIN CONDITION ANALYSIS")
    print("=" * 70)
    
    analyzer = ImageAnalyzer()
    
    languages = ['hindi', 'english']
    
    for lang in languages:
        print(f"\n🗣️  Testing in {lang.upper()}:")
        print("-" * 70)
        
        test_img = create_test_image(800, 600)
        result = analyzer.analyze_skin_condition(test_img, lang)
        
        if result['success']:
            print("✅ Analysis successful")
            analysis = result['analysis']
            print(f"   Image quality: {analysis['image_quality']}")
            print(f"   Resolution: {analysis['resolution']}")
            print(f"   Analysis type: {analysis['analysis_type']}")
            print(f"\n   First 3 recommendations:")
            for i, rec in enumerate(analysis['recommendations'][:3], 1):
                print(f"   {i}. {rec[:60]}...")
        else:
            print(f"❌ Analysis failed: {result['error']}")


def test_image_request_detection():
    """Test detection of image-related queries"""
    print("\n" + "=" * 70)
    print("TESTING IMAGE REQUEST DETECTION")
    print("=" * 70)
    
    analyzer = ImageAnalyzer()
    
    test_messages = [
        ("Can I send a photo?", True),
        ("Photo bhejun?", True),
        ("Mere skin की picture dikhana hai", True),
        ("I have a headache", False),
        ("Mujhe bukhar hai", False),
        ("तस्वीर भेज सकता हूं?", True),
        ("Send image kar sakta hoon?", True),
    ]
    
    for message, expected in test_messages:
        detected = analyzer.detect_image_request(message)
        status = "✅" if detected == expected else "❌"
        print(f"{status} '{message[:40]}...' - Detected: {detected}, Expected: {expected}")


def test_instructions_generation():
    """Test instructions generation in multiple languages"""
    print("\n" + "=" * 70)
    print("TESTING INSTRUCTIONS GENERATION")
    print("=" * 70)
    
    analyzer = ImageAnalyzer()
    
    for lang in ['hindi', 'english']:
        print(f"\n🗣️  Instructions in {lang.upper()}:")
        print("-" * 70)
        instructions = analyzer.get_image_analysis_instructions(lang)
        print(instructions[:300] + "...")
        print("✅ Instructions generated")


def test_common_conditions_info():
    """Test common skin conditions info"""
    print("\n" + "=" * 70)
    print("TESTING COMMON SKIN CONDITIONS INFO")
    print("=" * 70)
    
    analyzer = ImageAnalyzer()
    
    for lang in ['hindi', 'english']:
        print(f"\n🗣️  Info in {lang.upper()}:")
        print("-" * 70)
        info = analyzer.get_common_skin_conditions_info(lang)
        print(info[:300] + "...")
        print("✅ Info generated")


def run_all_tests():
    """Run all image analysis tests"""
    print("\n" + "=" * 70)
    print("🖼️  SWASTHYAGUIDE IMAGE ANALYSIS TEST SUITE 🖼️")
    print("=" * 70)
    print("\nTesting image analysis features:")
    print("- Image validation")
    print("- Image preprocessing")
    print("- Quality assessment")
    print("- Skin condition analysis")
    print("- Request detection")
    print("- Instructions & info generation")
    print("\n" + "=" * 70)
    
    try:
        test_image_validation()
        test_image_preprocessing()
        test_image_quality_assessment()
        test_skin_condition_analysis()
        test_image_request_detection()
        test_instructions_generation()
        test_common_conditions_info()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS COMPLETED!")
        print("=" * 70)
        print("\n📊 Summary:")
        print("- Image Validation: TESTED")
        print("- Image Preprocessing: TESTED")
        print("- Quality Assessment: TESTED")
        print("- Skin Condition Analysis: TESTED")
        print("- Request Detection: TESTED")
        print("- Instructions Generation: TESTED")
        print("- Common Conditions Info: TESTED")
        print("\nℹ️  Note: This is basic testing without AI model integration.")
        print("For production, integrate with medical image analysis APIs.")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ ERROR during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()

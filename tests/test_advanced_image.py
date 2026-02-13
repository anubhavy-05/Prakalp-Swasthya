#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for advanced image analysis features
"""

import os
import sys
from PIL import Image
import io
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from image_analyzer import ImageAnalyzer


def create_test_image(color=(200, 100, 100), size=(512, 512)):
    """Create a test image with specific color"""
    # Create image with specified color
    img_array = np.zeros((size[1], size[0], 3), dtype=np.uint8)
    img_array[:, :] = color
    
    # Add some texture variation
    noise = np.random.randint(-20, 20, (size[1], size[0], 3), dtype=np.int16)
    img_array = np.clip(img_array.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Add some circular patterns (simulating skin condition)
    center_x, center_y = size[0] // 2, size[1] // 2
    y, x = np.ogrid[:size[1], :size[0]]
    mask = (x - center_x)**2 + (y - center_y)**2 <= 5000
    img_array[mask] = [220, 80, 80]  # Redder center
    
    img = Image.fromarray(img_array)
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr


def test_basic_validation():
    """Test basic image validation"""
    print("\n" + "=" * 60)
    print("🧪 TEST 1: Basic Image Validation")
    print("=" * 60)
    
    analyzer = ImageAnalyzer()
    
    # Create test image
    test_image = create_test_image()
    
    # Validate
    is_valid, message, metadata = analyzer.validate_image(test_image, 'image/png')
    
    print(f"\n✓ Validation Status: {is_valid}")
    print(f"✓ Message: {message}")
    if metadata:
        print(f"✓ Resolution: {metadata['size']}")
        print(f"✓ Format: {metadata['format']}")
        print(f"✓ File Size: {metadata['file_size'] / 1024:.2f} KB")
        print(f"✓ Image Hash: {metadata['image_hash'][:16]}...")
    
    return is_valid


def test_color_analysis():
    """Test advanced color analysis"""
    print("\n" + "=" * 60)
    print("🧪 TEST 2: Advanced Color Analysis")
    print("=" * 60)
    
    analyzer = ImageAnalyzer()
    
    # Create reddish test image (simulating inflammation)
    test_image = create_test_image(color=(220, 120, 120))
    
    # Preprocess
    original, enhanced = analyzer.preprocess_image(test_image, enhance=True)
    
    # Analyze colors
    color_analysis = analyzer.analyze_colors(enhanced)
    
    print("\n📊 Color Analysis Results:")
    print(f"  • Mean RGB: {[f'{x:.1f}' for x in color_analysis['mean_rgb']]}")
    print(f"  • Dominant Color: RGB{tuple(color_analysis['dominant_color'])}")
    print(f"  • Redness Score: {color_analysis['redness_score']:.2f}/100")
    print(f"  • Color Variance: {color_analysis['color_variance']:.2f}")
    
    print("\n🔥 Inflammation Indicators:")
    inflammation = color_analysis['inflammation_indicators']
    print(f"  • Red Dominant %: {inflammation['red_dominant_percentage']:.2f}%")
    print(f"  • Likely Inflamed: {inflammation['likely_inflamed']}")
    print(f"  • Severity Estimate: {inflammation['severity_estimate']}")
    
    return True


def test_texture_analysis():
    """Test texture analysis"""
    print("\n" + "=" * 60)
    print("🧪 TEST 3: Texture Analysis")
    print("=" * 60)
    
    analyzer = ImageAnalyzer()
    
    # Create test image
    test_image = create_test_image()
    original, enhanced = analyzer.preprocess_image(test_image, enhance=True)
    
    # Analyze texture
    texture_analysis = analyzer.analyze_texture(enhanced)
    
    print("\n🔬 Texture Analysis Results:")
    print(f"  • Smoothness: {texture_analysis['smoothness']:.4f}")
    print(f"  • Uniformity: {texture_analysis['uniformity']:.4f}")
    print(f"  • Entropy: {texture_analysis['entropy']:.4f}")
    print(f"  • Edge Density: {texture_analysis['edge_density']:.4f}")
    print(f"  • Texture Type: {texture_analysis['texture_type']}")
    
    return True


def test_comprehensive_analysis():
    """Test complete skin condition analysis"""
    print("\n" + "=" * 60)
    print("🧪 TEST 4: Comprehensive Skin Condition Analysis")
    print("=" * 60)
    
    analyzer = ImageAnalyzer()
    
    # Create test image with inflammatory characteristics
    test_image = create_test_image(color=(230, 110, 110))
    
    # Perform complete analysis
    result = analyzer.analyze_skin_condition(test_image, language='english')
    
    if result['success']:
        print("\n✓ Analysis Successful!")
        analysis = result['analysis']
        
        print(f"\n📋 Basic Info:")
        print(f"  • Quality: {analysis['image_quality']}")
        print(f"  • Resolution: {analysis['resolution']}")
        print(f"  • Confidence: {analysis['confidence_level']}")
        
        print(f"\n🎨 Visual Analysis:")
        visual = analysis['visual_analysis']
        print(f"  • Redness Score: {visual['color_metrics']['redness_score']:.1f}/100")
        print(f"  • Texture Type: {visual['texture_metrics']['texture_type']}")
        
        print(f"\n🩺 Condition Detection:")
        condition = analysis['condition_detection']
        findings = condition['findings']
        if findings:
            for i, finding in enumerate(findings, 1):
                print(f"  {i}. {finding['condition'].replace('_', ' ').title()}")
                print(f"     Confidence: {finding['confidence']}")
        else:
            print("  No specific conditions detected")
        
        print(f"\n📊 Severity Assessment:")
        severity = analysis['severity_assessment']
        print(f"  • Level: {severity['level'].upper()}")
        print(f"  • Urgency: {severity['urgency'].upper()}")
        print(f"  • Score: {severity['score']}/{severity['max_score']}")
        print(f"  • Description: {severity['description']}")
        
        print(f"\n📝 Next Steps:")
        for step in analysis['next_steps']:
            print(f"  {step}")
        
    else:
        print(f"\n✗ Analysis Failed: {result['error']}")
        return False
    
    return True


def test_report_generation():
    """Test report generation"""
    print("\n" + "=" * 60)
    print("🧪 TEST 5: Report Generation")
    print("=" * 60)
    
    analyzer = ImageAnalyzer()
    
    # Create test image
    test_image = create_test_image(color=(210, 100, 100))
    
    # Analyze
    result = analyzer.analyze_skin_condition(test_image, language='english')
    
    if result['success']:
        # Generate report
        report = analyzer.generate_analysis_report(result['analysis'], language='english')
        print("\n📄 Generated Report:")
        print(report)
        return True
    else:
        print(f"✗ Could not generate report: {result['error']}")
        return False


def test_history_tracking():
    """Test analysis history and comparison"""
    print("\n" + "=" * 60)
    print("🧪 TEST 6: History Tracking & Comparison")
    print("=" * 60)
    
    analyzer = ImageAnalyzer()
    
    # Analyze first image
    test_image1 = create_test_image(color=(200, 100, 100))
    result1 = analyzer.analyze_skin_condition(test_image1, language='english')
    
    # Analyze second image (worse condition)
    test_image2 = create_test_image(color=(240, 90, 90))
    result2 = analyzer.analyze_skin_condition(test_image2, language='english')
    
    print(f"\n✓ Analyzed {len(analyzer.analysis_history)} images")
    print(f"  Image 1 Severity: {analyzer.analysis_history[0]['severity']['level']}")
    print(f"  Image 2 Severity: {analyzer.analysis_history[1]['severity']['level']}")
    
    # Compare
    if len(analyzer.analysis_history) >= 2:
        comparison = analyzer.compare_with_history(result2['analysis']['metadata']['image_hash'])
        if comparison:
            print(f"\n📈 Comparison Results:")
            print(f"  • Trend: {comparison['trend'].upper()}")
            print(f"  • Severity Change: {comparison['severity_change']:+d}")
            print(f"  • Recommendation: {comparison['recommendation']}")
    
    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🚀 ADVANCED IMAGE ANALYZER TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Basic Validation", test_basic_validation),
        ("Color Analysis", test_color_analysis),
        ("Texture Analysis", test_texture_analysis),
        ("Comprehensive Analysis", test_comprehensive_analysis),
        ("Report Generation", test_report_generation),
        ("History Tracking", test_history_tracking)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' failed with error: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    total = len(results)
    passed = sum(1 for _, success in results if success)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

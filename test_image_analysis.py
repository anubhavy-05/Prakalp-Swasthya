# -*- coding: utf-8 -*-
"""
Test Medical Image Analysis with Hugging Face AI
This script tests the AI-powered image analysis feature
"""

import sys
from pathlib import Path
from src.image_analyzer import ImageAnalyzer

print("=" * 70)
print("🩺 TESTING MEDICAL IMAGE ANALYSIS WITH AI")
print("=" * 70)

# Initialize analyzer
analyzer = ImageAnalyzer()

# Check if AI is enabled
print("\n📊 CONFIGURATION CHECK:")
print(f"   - AI Enabled: {'✅ YES' if analyzer.ai_enabled else '❌ NO'}")
print(f"   - API Key: {analyzer.hf_api_key[:15] if analyzer.hf_api_key else 'Not configured'}...")
print(f"   - Supported formats: {', '.join(analyzer.supported_formats)}")

if not analyzer.ai_enabled:
    print("\n⚠️  AI analysis is disabled!")
    print("   Make sure HUGGINGFACE_API_KEY is set in your .env file")
    print("   Get your free token from: https://huggingface.co/settings/tokens")
    sys.exit(1)

# Test with a sample image (users can provide their own)
print("\n🖼️  IMAGE ANALYSIS TEST:")
print("=" * 70)

# Check if user provided an image path
if len(sys.argv) > 1:
    image_path = Path(sys.argv[1])
    
    if not image_path.exists():
        print(f"❌ Image not found: {image_path}")
        sys.exit(1)
    
    print(f"\n📂 Loading image: {image_path.name}")
    
    try:
        # Read image
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        print(f"   - Size: {len(image_data):,} bytes ({len(image_data) / 1024:.1f} KB)")
        
        # Analyze image
        print("\n🔬 Starting AI-powered analysis...")
        print("   (This may take 10-30 seconds depending on API response time)")
        
        result = analyzer.analyze_skin_condition(image_data, language='english')
        
        if result['success']:
            analysis = result['analysis']
            
            print("\n✅ ANALYSIS COMPLETE!")
            print("=" * 70)
            
            # AI Analysis Results
            if analysis.get('ai_analysis', {}).get('enabled'):
                ai = analysis['ai_analysis']
                print("\n🤖 AI ANALYSIS:")
                print(f"   Description: {ai['description']}")
                print(f"   Confidence: {ai['confidence']}")
                if ai.get('medical_keywords'):
                    print(f"   Keywords: {', '.join(ai['medical_keywords'][:10])}")
            
            # Condition Detection
            conditions = analysis.get('condition_detection', {})
            if conditions.get('findings'):
                print("\n🔍 DETECTED CONDITIONS:")
                for finding in conditions['findings']:
                    print(f"   - {finding['condition'].replace('_', ' ').title()}")
                    print(f"     Confidence: {finding['confidence']}")
                    if finding.get('source'):
                        print(f"     Source: {finding['source']}")
            
            # Severity
            severity = analysis.get('severity_assessment', {})
            print(f"\n⚠️  SEVERITY: {severity.get('level', 'unknown').upper()}")
            
            # Recommendations
            recommendations = analysis.get('recommendations', [])
            if recommendations:
                print("\n📋 RECOMMENDATIONS:")
                for rec in recommendations[:15]:  # Show first 15 lines
                    print(f"   {rec}")
            
            # Quality metrics
            print(f"\n📊 IMAGE QUALITY: {analysis.get('image_quality', 'N/A')}")
            print(f"   Resolution: {analysis.get('resolution', 'N/A')}")
            
        else:
            print(f"\n❌ ANALYSIS FAILED:")
            print(f"   Error: {result['error']}")
        
    except FileNotFoundError:
        print(f"❌ Cannot read image file: {image_path}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

else:
    # No image provided - show usage
    print("\n📖 USAGE:")
    print("   python test_image_analysis.py <path_to_image>")
    print("\nEXAMPLE:")
    print("   python test_image_analysis.py skin_rash.jpg")
    print("   python test_image_analysis.py C:\\Users\\Pictures\\medical_photo.png")
    
    print("\n💡 TIPS:")
    print("   - Use clear, well-lit photos")
    print("   - Focus on the affected area")
    print("   - Supported formats: JPG, PNG, WebP")
    print("   - Max size: 10MB")
    
    print("\n🧪 Want to test without an image?")
    print("   1. Take a photo of any skin condition (rash, cut, etc.)")
    print("   2. Save it to your computer")
    print("   3. Run: python test_image_analysis.py path/to/your/photo.jpg")

print("\n" + "=" * 70)
print("✅ Test script completed!")
print("=" * 70)

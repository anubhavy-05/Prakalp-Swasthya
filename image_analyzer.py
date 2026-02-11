# -*- coding: utf-8 -*-
"""
Image Analysis Module
Analyzes medical images for skin conditions, rashes, and basic diagnostics
"""

import base64
import io
import os
from typing import Dict, List, Optional, Tuple
from PIL import Image
import requests


class ImageAnalyzer:
    """Handles medical image analysis"""
    
    def __init__(self):
        """Initialize the image analyzer"""
        self.supported_formats = ['jpg', 'jpeg', 'png', 'webp']
        self.max_image_size = 10 * 1024 * 1024  # 10MB
        self.min_image_size = 1024  # 1KB
        
        # Skin condition categories
        self.skin_conditions = {
            'rash': ['redness', 'irritation', 'bumps', 'patches'],
            'acne': ['pimples', 'blackheads', 'whiteheads', 'spots'],
            'eczema': ['dry', 'scaly', 'itchy', 'inflamed'],
            'fungal': ['circular', 'ring', 'scaling', 'athlete'],
            'psoriasis': ['thick', 'silvery', 'scaly', 'plaques'],
            'burn': ['redness', 'blistering', 'peeling'],
            'insect_bite': ['swelling', 'red', 'bump', 'bite'],
            'allergy': ['hives', 'urticaria', 'welts', 'swelling']
        }
    
    def validate_image(self, image_data: bytes, content_type: str) -> Tuple[bool, str]:
        """
        Validate image format and size
        Returns: (is_valid, error_message)
        """
        # Check size
        if len(image_data) > self.max_image_size:
            return False, "Image too large. Please send an image smaller than 10MB."
        
        if len(image_data) < self.min_image_size:
            return False, "Image too small. Please send a clear image."
        
        # Check format
        try:
            image = Image.open(io.BytesIO(image_data))
            format_lower = image.format.lower() if image.format else ''
            
            if format_lower not in self.supported_formats:
                return False, f"Unsupported format. Please send: {', '.join(self.supported_formats)}"
            
            # Check dimensions
            width, height = image.size
            if width < 100 or height < 100:
                return False, "Image resolution too low. Please send a clearer image."
            
            return True, "Image valid"
            
        except Exception as e:
            return False, f"Invalid image file. Error: {str(e)}"
    
    def preprocess_image(self, image_data: bytes) -> Image.Image:
        """
        Preprocess image for analysis
        - Resize if too large
        - Enhance quality
        - Normalize
        """
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if too large (max 1024x1024 for processing)
        max_dimension = 1024
        if max(image.size) > max_dimension:
            ratio = max_dimension / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        return image
    
    def analyze_image_basic(self, image: Image.Image) -> Dict:
        """
        Basic image analysis without AI
        Analyzes image properties and provides general guidance
        """
        width, height = image.size
        
        # Basic image statistics
        analysis = {
            'resolution': f"{width}x{height}",
            'aspect_ratio': round(width / height, 2),
            'format': image.format,
            'quality_score': self._assess_image_quality(image)
        }
        
        return analysis
    
    def _assess_image_quality(self, image: Image.Image) -> str:
        """Assess image quality for medical analysis"""
        width, height = image.size
        total_pixels = width * height
        
        if total_pixels >= 1000000:  # 1MP+
            return "excellent"
        elif total_pixels >= 500000:  # 500K+
            return "good"
        elif total_pixels >= 200000:  # 200K+
            return "moderate"
        else:
            return "low"
    
    def analyze_skin_condition(self, image_data: bytes, language: str = 'english') -> Dict:
        """
        Analyze skin condition from image
        This is a basic implementation without AI model
        In production, you would integrate with medical AI APIs
        """
        # Validate image
        is_valid, message = self.validate_image(image_data, 'image/jpeg')
        if not is_valid:
            return {
                'success': False,
                'error': message,
                'analysis': None
            }
        
        # Preprocess image
        try:
            image = self.preprocess_image(image_data)
            basic_info = self.analyze_image_basic(image)
            
            # For demo purposes, provide general skin analysis guidance
            analysis = {
                'image_quality': basic_info['quality_score'],
                'resolution': basic_info['resolution'],
                'analysis_type': 'general_skin_assessment',
                'confidence': 'basic_analysis',
                'recommendations': self._get_general_skin_recommendations(language),
                'disclaimer': self._get_disclaimer(language)
            }
            
            return {
                'success': True,
                'error': None,
                'analysis': analysis
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error processing image: {str(e)}",
                'analysis': None
            }
    
    def _get_general_skin_recommendations(self, language: str) -> List[str]:
        """Get general recommendations for skin issues"""
        recommendations = {
            'hindi': [
                "🔍 Image received. Yahan kuch general guidance hai:",
                "",
                "📋 Basic skin care tips:",
                "• Affected area ko saaf aur sukha rakhein",
                "• Kharaab ya tight kapde avoid karein",
                "• Affected area ko zyada chhuyen nahi",
                "• Hydrated rahein - pani zyada piyein",
                "",
                "⚠️ Doctor se kab milein:",
                "• Agar condition 3-4 din mein behtar na ho",
                "• Agar dard, swelling, ya pus ho",
                "• Agar fever ya infection ke lakshan hon",
                "• Agar condition spread ho rahi ho",
                "",
                "🏥 Professional diagnosis ke liye dermatologist se zaroor milein."
            ],
            'english': [
                "🔍 Image received. Here's some general guidance:",
                "",
                "📋 Basic skin care tips:",
                "• Keep the affected area clean and dry",
                "• Avoid tight or irritating clothing",
                "• Don't scratch or touch the area excessively",
                "• Stay hydrated - drink plenty of water",
                "",
                "⚠️ When to see a doctor:",
                "• If condition doesn't improve in 3-4 days",
                "• If there's pain, swelling, or pus",
                "• If you develop fever or signs of infection",
                "• If the condition is spreading",
                "",
                "🏥 For professional diagnosis, please consult a dermatologist."
            ]
        }
        
        return recommendations.get(language, recommendations['english'])
    
    def _get_disclaimer(self, language: str) -> str:
        """Get medical disclaimer for image analysis"""
        disclaimers = {
            'hindi': """
⚠️ IMPORTANT DISCLAIMER:
Yeh automated image analysis hai aur professional medical diagnosis ka replacement NAHI hai. 
Accurate diagnosis ke liye qualified dermatologist ya doctor se milein.
Emergency mein turant medical help lein.
""",
            'english': """
⚠️ IMPORTANT DISCLAIMER:
This is an automated image analysis and is NOT a replacement for professional medical diagnosis.
Please consult a qualified dermatologist or doctor for accurate diagnosis.
Seek immediate medical help in case of emergency.
"""
        }
        
        return disclaimers.get(language, disclaimers['english'])
    
    def get_image_analysis_instructions(self, language: str) -> str:
        """Get instructions for sending medical images"""
        instructions = {
            'hindi': """
📸 IMAGE ANALYSIS INSTRUCTIONS:

Image bhejne se pehle:
1. ✅ Affected area ka clear photo lein
2. ✅ Achhe lighting mein photo lein
3. ✅ Photo focus mein hona chahiye
4. ✅ Area ko close-up se dikhayein
5. ✅ Multiple angles se photo helpful hai

Supported formats: JPG, PNG, WEBP
Maximum size: 10MB

Privacy: Aapki images secure aur confidential hain.

Image bhejne ke baad main basic guidance provide karunga.
But professional diagnosis ke liye doctor ko zaroor dikhaayein.
""",
            'english': """
📸 IMAGE ANALYSIS INSTRUCTIONS:

Before sending image:
1. ✅ Take a clear photo of the affected area
2. ✅ Ensure good lighting
3. ✅ Photo should be in focus
4. ✅ Show the area in close-up
5. ✅ Multiple angles are helpful

Supported formats: JPG, PNG, WEBP
Maximum size: 10MB

Privacy: Your images are secure and confidential.

After sending the image, I'll provide basic guidance.
However, please consult a doctor for professional diagnosis.
"""
        }
        
        return instructions.get(language, instructions['english'])
    
    def detect_image_request(self, text: str) -> bool:
        """Detect if user wants to send an image"""
        image_keywords = [
            'photo', 'picture', 'image', 'pic', 'photo bhejo', 'image send',
            'tasveer', 'photo dikhao', 'dekhna hai', 'rash dikha', 'skin dikha',
            'फोटो', 'तस्वीर', 'चित्र', 'ছবি', 'புகைப்படம்', 'ఫోటో', 'ਫੋਟੋ', 'ફોટો'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in image_keywords)
    
    def get_common_skin_conditions_info(self, language: str) -> str:
        """Provide information about common skin conditions"""
        info = {
            'hindi': """
📚 COMMON SKIN CONDITIONS:

1. 🔴 Rash (Daad/Kharish)
   - Red, itchy patches
   - Causes: Allergy, infection, heat

2. 🔴 Acne (Muhanse)
   - Pimples, blackheads
   - Common in teenagers

3. 🔴 Eczema (Khujli wali skin)
   - Dry, scaly, itchy skin
   - Chronic condition

4. 🔴 Fungal Infection (Fungal daad)
   - Circular, ring-like patches
   - Spreads easily

5. 🔴 Psoriasis
   - Thick, scaly patches
   - Chronic condition

6. 🔴 Burns
   - Heat, chemical, sun burns
   - Severity varies

Photo bhej kar main basic guidance de sakta hoon.
Lekin doctor se consultation zaroor karein.
""",
            'english': """
📚 COMMON SKIN CONDITIONS:

1. 🔴 Rash
   - Red, itchy patches
   - Causes: Allergy, infection, heat

2. 🔴 Acne
   - Pimples, blackheads
   - Common in teenagers

3. 🔴 Eczema
   - Dry, scaly, itchy skin
   - Chronic condition

4. 🔴 Fungal Infection
   - Circular, ring-like patches
   - Spreads easily

5. 🔴 Psoriasis
   - Thick, scaly patches
   - Chronic condition

6. 🔴 Burns
   - Heat, chemical, sun burns
   - Severity varies

You can send a photo for basic guidance.
However, please consult a doctor for proper diagnosis.
"""
        }
        
        return info.get(language, info['english'])


# Helper function for easy integration
def create_image_analyzer() -> ImageAnalyzer:
    """Factory function to create ImageAnalyzer instance"""
    return ImageAnalyzer()

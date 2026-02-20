# -*- coding: utf-8 -*-
"""
Voice Handler Module
Handles voice message processing: Speech-to-Text and Text-to-Speech
Supports multiple Indian languages for rural users
"""

import os
import logging
import tempfile
from pathlib import Path
from typing import Tuple, Optional
import requests

# Google Cloud Speech-to-Text and Text-to-Speech
try:
    from google.cloud import speech_v1p1beta1 as speech
    from google.cloud import texttospeech
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    logging.warning("Google Cloud libraries not available. Voice features will be limited.")

# Audio processing libraries
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    logging.warning("pydub not available. Audio conversion will be limited.")

logger = logging.getLogger(__name__)


class VoiceHandler:
    """
    Handle voice message processing for WhatsApp chatbot
    - Convert speech to text (multilingual support for Indian languages)
    - Convert text response to speech
    - Handle audio format conversions
    """
    
    # Language mapping: detected language -> Google Speech API language codes
    LANGUAGE_CODES = {
        'hindi': 'hi-IN',
        'english': 'en-IN',
        'bengali': 'bn-IN',
        'tamil': 'ta-IN',
        'telugu': 'te-IN',
        'marathi': 'mr-IN',
        'gujarati': 'gu-IN',
        'kannada': 'kn-IN',
        'malayalam': 'ml-IN',
        'punjabi': 'pa-IN',
        'hinglish': 'hi-IN'  # Use Hindi for Hinglish
    }
    
    def __init__(self):
        """Initialize Voice Handler with Google Cloud credentials"""
        self.google_available = GOOGLE_AVAILABLE
        self.pydub_available = PYDUB_AVAILABLE
        
        # Initialize clients
        if GOOGLE_AVAILABLE:
            try:
                # Set Google credentials from environment variable
                credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
                if credentials_path and os.path.exists(credentials_path):
                    self.speech_client = speech.SpeechClient()
                    self.tts_client = texttospeech.TextToSpeechClient()
                    logger.info("Google Cloud Speech services initialized successfully")
                else:
                    logger.warning("Google credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS environment variable.")
                    self.speech_client = None
                    self.tts_client = None
            except Exception as e:
                logger.error(f"Failed to initialize Google Cloud clients: {e}")
                self.speech_client = None
                self.tts_client = None
        else:
            self.speech_client = None
            self.tts_client = None
        
        # Create temp directory for audio processing
        self.temp_dir = Path(tempfile.gettempdir()) / 'swasthya_voice'
        self.temp_dir.mkdir(exist_ok=True)
        logger.info(f"Voice handler initialized. Temp dir: {self.temp_dir}")
    
    def download_voice_message(self, media_url: str, auth_tuple: Tuple[str, str]) -> Optional[bytes]:
        """
        Download voice message from WhatsApp/Twilio
        
        Args:
            media_url: URL of the voice message
            auth_tuple: (account_sid, auth_token) for Twilio authentication
            
        Returns:
            Audio data as bytes, or None if download fails
        """
        try:
            logger.info(f"Downloading voice message from: {media_url[:50]}...")
            response = requests.get(media_url, auth=auth_tuple, timeout=30)
            response.raise_for_status()
            
            audio_data = response.content
            logger.info(f"Voice message downloaded: {len(audio_data)} bytes")
            return audio_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download voice message: {e}")
            return None
    
    def convert_audio_format(self, audio_data: bytes, input_format: str = 'ogg', 
                           output_format: str = 'wav') -> Optional[bytes]:
        """
        Convert audio format (WhatsApp sends OGG, Google needs WAV/FLAC)
        
        Args:
            audio_data: Input audio data
            input_format: Input format (default: 'ogg' for WhatsApp)
            output_format: Output format (default: 'wav' for Google Speech)
            
        Returns:
            Converted audio data as bytes, or None if conversion fails
        """
        if not self.pydub_available:
            logger.warning("pydub not available. Returning original audio.")
            return audio_data
        
        try:
            # Create temporary files
            input_path = self.temp_dir / f"input.{input_format}"
            output_path = self.temp_dir / f"output.{output_format}"
            
            # Write input audio to temporary file
            with open(input_path, 'wb') as f:
                f.write(audio_data)
            
            # Convert using pydub
            logger.info(f"Converting audio: {input_format} -> {output_format}")
            audio = AudioSegment.from_file(str(input_path), format=input_format)
            
            # For Google Speech API, use mono 16-bit PCM WAV at 16kHz
            if output_format == 'wav':
                audio = audio.set_channels(1)  # Mono
                audio = audio.set_frame_rate(16000)  # 16kHz
                audio = audio.set_sample_width(2)  # 16-bit
            
            # Export converted audio
            audio.export(str(output_path), format=output_format)
            
            # Read converted audio
            with open(output_path, 'rb') as f:
                converted_data = f.read()
            
            # Clean up temporary files
            input_path.unlink(missing_ok=True)
            output_path.unlink(missing_ok=True)
            
            logger.info(f"Audio converted successfully: {len(converted_data)} bytes")
            return converted_data
            
        except Exception as e:
            logger.error(f"Audio conversion failed: {e}", exc_info=True)
            return None
    
    def transcribe_audio(self, audio_data: bytes, language_hint: str = 'hindi') -> Tuple[Optional[str], Optional[str]]:
        """
        Convert speech to text using Google Speech-to-Text API
        
        Args:
            audio_data: Audio data in WAV format
            language_hint: Expected language (hindi, english, etc.)
            
        Returns:
            Tuple of (transcribed_text, detected_language_code)
        """
        if not self.speech_client:
            logger.error("Google Speech client not initialized")
            return None, None
        
        try:
            # Get language code
            language_code = self.LANGUAGE_CODES.get(language_hint, 'hi-IN')
            
            # Configure recognition settings
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=language_code,
                # Enable automatic language detection for multiple Indian languages
                alternative_language_codes=[
                    'en-IN', 'hi-IN', 'bn-IN', 'ta-IN', 'te-IN', 
                    'mr-IN', 'gu-IN', 'kn-IN', 'ml-IN', 'pa-IN'
                ],
                enable_automatic_punctuation=True,
                model='latest_long',  # Best model for longer audio
                use_enhanced=True  # Enhanced model for better accuracy
            )
            
            audio = speech.RecognitionAudio(content=audio_data)
            
            logger.info(f"Sending audio to Google Speech API (language: {language_code})")
            
            # Perform recognition
            response = self.speech_client.recognize(config=config, audio=audio)
            
            # Extract transcribed text
            if not response.results:
                logger.warning("No speech detected in audio")
                return None, None
            
            # Get the best transcript
            transcript = response.results[0].alternatives[0].transcript
            detected_language = response.results[0].language_code if hasattr(response.results[0], 'language_code') else language_code
            
            logger.info(f"Speech transcribed successfully: '{transcript[:50]}...' (Language: {detected_language})")
            return transcript, detected_language
            
        except Exception as e:
            logger.error(f"Speech recognition failed: {e}", exc_info=True)
            return None, None
    
    def synthesize_speech(self, text: str, language: str = 'hindi', 
                         voice_gender: str = 'FEMALE') -> Optional[bytes]:
        """
        Convert text to speech using Google Text-to-Speech API
        
        Args:
            text: Text to convert to speech
            language: Language of the text
            voice_gender: Voice gender ('MALE' or 'FEMALE')
            
        Returns:
            Audio data as bytes (OGG format for WhatsApp), or None if synthesis fails
        """
        if not self.tts_client:
            logger.error("Google TTS client not initialized")
            return None
        
        try:
            # Get language code
            language_code = self.LANGUAGE_CODES.get(language, 'hi-IN')
            
            # Build the voice synthesis request
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Select voice parameters
            # For Hindi: hi-IN-Wavenet-A (Female), hi-IN-Wavenet-B (Male)
            # For English: en-IN-Wavenet-A (Female), en-IN-Wavenet-B (Male)
            voice_name = None
            if language_code == 'hi-IN':
                voice_name = 'hi-IN-Wavenet-D' if voice_gender == 'FEMALE' else 'hi-IN-Wavenet-C'
            elif language_code == 'en-IN':
                voice_name = 'en-IN-Wavenet-D' if voice_gender == 'FEMALE' else 'en-IN-Wavenet-C'
            
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name,
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE if voice_gender == 'FEMALE' 
                           else texttospeech.SsmlVoiceGender.MALE
            )
            
            # Select audio format - OGG for WhatsApp
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.OGG_OPUS,
                speaking_rate=0.95,  # Slightly slower for clarity
                pitch=0.0
            )
            
            logger.info(f"Generating speech: '{text[:50]}...' (Language: {language_code}, Voice: {voice_name})")
            
            # Perform the text-to-speech request
            response = self.tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            logger.info(f"Speech synthesized successfully: {len(response.audio_content)} bytes")
            return response.audio_content
            
        except Exception as e:
            logger.error(f"Speech synthesis failed: {e}", exc_info=True)
            return None
    
    def process_voice_message(self, media_url: str, auth_tuple: Tuple[str, str], 
                             language_hint: str = 'hindi') -> Tuple[Optional[str], Optional[str]]:
        """
        Complete pipeline: Download voice -> Convert -> Transcribe
        
        Args:
            media_url: URL of the voice message from WhatsApp
            auth_tuple: Twilio authentication credentials
            language_hint: Expected language
            
        Returns:
            Tuple of (transcribed_text, detected_language)
        """
        # Step 1: Download voice message
        audio_data = self.download_voice_message(media_url, auth_tuple)
        if not audio_data:
            return None, None
        
        # Step 2: Convert OGG to WAV
        wav_data = self.convert_audio_format(audio_data, input_format='ogg', output_format='wav')
        if not wav_data:
            logger.warning("Audio conversion failed, trying with original format")
            wav_data = audio_data
        
        # Step 3: Transcribe audio
        transcript, detected_language = self.transcribe_audio(wav_data, language_hint)
        
        return transcript, detected_language
    
    def get_error_message(self, error_type: str, language: str = 'hindi') -> str:
        """
        Get user-friendly error messages in the appropriate language
        
        Args:
            error_type: Type of error ('download', 'transcribe', 'unclear', etc.)
            language: User's language
            
        Returns:
            Error message string
        """
        messages = {
            'download': {
                'hindi': "🎤 आवाज़ संदेश डाउनलोड नहीं हो सका। कृपया दोबारा भेजें।",
                'english': "🎤 Could not download voice message. Please send again."
            },
            'transcribe': {
                'hindi': "🎤 आवाज़ स्पष्ट नहीं है। कृपया धीरे और साफ बोलें।",
                'english': "🎤 Voice is not clear. Please speak slowly and clearly."
            },
            'unclear': {
                'hindi': "🎤 आवाज़ नहीं सुनाई दी। कृपया दोबारा कोशिश करें।",
                'english': "🎤 Could not hear voice. Please try again."
            },
            'service_unavailable': {
                'hindi': "🎤 आवाज़ सेवा अभी उपलब्ध नहीं है। कृपया टेक्स्ट में लिखें।",
                'english': "🎤 Voice service currently unavailable. Please type your message."
            },
            'unsupported_language': {
                'hindi': "🎤 यह भाषा अभी समर्थित नहीं है। कृपया हिंदी या अंग्रेजी में बोलें।",
                'english': "🎤 This language is not supported yet. Please speak in Hindi or English."
            }
        }
        
        return messages.get(error_type, {}).get(language, messages[error_type]['hindi'])
    
    def get_voice_instructions(self, language: str = 'hindi') -> str:
        """
        Get instructions for using voice messages
        
        Args:
            language: User's language
            
        Returns:
            Instruction message
        """
        if language == 'hindi' or language == 'hinglish':
            return """🎤 *आवाज़ संदेश की सुविधा*

अब आप अपनी समस्या बोलकर भी बता सकते हैं!

*कैसे इस्तेमाल करें:*
1️⃣ WhatsApp की रिकॉर्डिंग बटन दबाएं
2️⃣ अपनी समस्या साफ और धीरे बोलें
3️⃣ संदेश भेजें

*समर्थित भाषाएं:*
• हिंदी
• अंग्रेजी
• बंगाली
• तमिल
• तेलुगु
• मराठी
• गुजराती
• और अन्य भारतीय भाषाएं

*उदाहरण:*
"मुझे बुखार और सिरदर्द है"
"Mujhe pet mein dard ho raha hai"

💡 *टिप्स:*
✅ शांत जगह पर बोलें
✅ स्पष्ट उच्चारण करें
✅ बहुत तेज़ या बहुत धीरे न बोलें

कोशिश करें! 🙏"""
        else:
            return """🎤 *Voice Message Feature*

You can now speak your problem instead of typing!

*How to Use:*
1️⃣ Press WhatsApp's recording button
2️⃣ Speak your problem clearly and slowly
3️⃣ Send the message

*Supported Languages:*
• Hindi
• English
• Bengali
• Tamil
• Telugu
• Marathi
• Gujarati
• Other Indian languages

*Example:*
"I have fever and headache"
"Mujhe bukhar aur sir dard hai"

💡 *Tips:*
✅ Speak in a quiet place
✅ Pronounce clearly
✅ Don't speak too fast or too slow

Try it! 🙏"""


# Initialize global voice handler instance
_voice_handler_instance = None

def get_voice_handler() -> VoiceHandler:
    """Get or create singleton voice handler instance"""
    global _voice_handler_instance
    if _voice_handler_instance is None:
        _voice_handler_instance = VoiceHandler()
    return _voice_handler_instance

"""
Text-to-Speech Module
Uses pyttsx3 for offline TTS
"""

import pyttsx3
from typing import Optional
from core.logger import setup_logger

logger = setup_logger("TTS")


class TextToSpeech:
    """Offline text-to-speech engine"""
    
    def __init__(self, config):
        self.config = config
        self.engine = None
        self._init_engine()
    
    def _init_engine(self):
        """Initialize TTS engine"""
        try:
            logger.info("Initializing TTS engine...")
            self.engine = pyttsx3.init()
            
            # Set voice properties
            self.engine.setProperty('rate', self.config.voice_rate)
            
            # Try to set voice (UK/US English)
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'english' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            
            logger.info("TTS engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TTS: {e}")
            raise
    
    def speak(self, text: str, async_mode: bool = False):
        """
        Convert text to speech
        
        Args:
            text: Text to speak
            async_mode: If True, speak asynchronously
        """
        if not text:
            return
        
        try:
            logger.info(f"Speaking: {text[:50]}...")
            self.engine.say(text)
            
            if not async_mode:
                self.engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS error: {e}")
    
    def set_rate(self, rate: int):
        """Set speech rate (words per minute)"""
        self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float):
        """Set volume (0.0 to 1.0)"""
        self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
    
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        voices = self.engine.getProperty('voices')
        return [{"id": v.id, "name": v.name, "languages": v.languages} for v in voices]

"""
Speech Recognition Module
Uses Whisper for offline speech-to-text
"""

import numpy as np
import sounddevice as sd
from typing import Optional
import whisper

from core.logger import setup_logger

logger = setup_logger("SpeechRecognition")


class SpeechRecognizer:
    """Offline speech recognition using OpenAI Whisper"""
    
    def __init__(self, config):
        self.config = config
        self.model = None
        self.is_listening = False
        self.sample_rate = 16000
    
    def load_model(self):
        """Load Whisper model (lazy loading)"""
        if self.model is None:
            logger.info(f"Loading Whisper model: {self.config.whisper_model}")
            self.model = whisper.load_model(self.config.whisper_model)
            logger.info("Whisper model loaded successfully")
    
    def record_audio(self, duration: int = 5) -> np.ndarray:
        """
        Record audio from microphone
        
        Args:
            duration: Recording duration in seconds
        
        Returns:
            Audio data as numpy array
        """
        logger.info(f"Recording for {duration} seconds...")
        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.float32
        )
        sd.wait()
        logger.info("Recording complete")
        return audio.flatten()
    
    def transcribe(self, audio: np.ndarray) -> str:
        """
        Transcribe audio to text
        
        Args:
            audio: Audio data as numpy array
        
        Returns:
            Transcribed text
        """
        if self.model is None:
            self.load_model()
        
        logger.info("Transcribing audio...")
        result = self.model.transcribe(audio, fp16=False)
        text = result["text"].strip()
        logger.info(f"Transcription: {text}")
        return text
    
    def listen(self, duration: int = 5) -> Optional[str]:
        """
        Listen and transcribe speech
        
        Args:
            duration: Listening duration in seconds
        
        Returns:
            Transcribed text or None if failed
        """
        try:
            audio = self.record_audio(duration)
            text = self.transcribe(audio)
            return text
        except Exception as e:
            logger.error(f"Speech recognition error: {e}")
            return None
    
    def start_continuous_listening(self, callback):
        """
        Start continuous listening mode with wake word detection
        (To be implemented)
        """
        # TODO: Implement wake word detection and continuous listening
        pass

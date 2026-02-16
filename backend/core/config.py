"""
Configuration management for YAAN
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel


class ServerConfig(BaseModel):
    """Server configuration"""
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = True
    workers: int = 1


class AIConfig(BaseModel):
    """AI model configuration"""
    model_name: str = "distilgpt2"  # Start with smaller model
    whisper_model: str = "base"  # tiny, base, small, medium, large
    max_tokens: int = 150
    temperature: float = 0.7
    use_gpu: bool = False  # Set to True if GPU available


class VoiceConfig(BaseModel):
    """Voice configuration"""
    wake_word: str = "hey yaan"
    voice_id: str = "en-us"  # TTS voice
    voice_rate: int = 150  # Words per minute
    sample_rate: int = 16000


class UserConfig(BaseModel):
    """User profile configuration"""
    name: str = "User"
    timezone: str = "UTC"
    language: str = "en"


class YAANConfig(BaseModel):
    """Main YAAN configuration"""
    server: ServerConfig = ServerConfig()
    ai: AIConfig = AIConfig()
    voice: VoiceConfig = VoiceConfig()
    user: UserConfig = UserConfig()
    data_dir: Path = Path("data")
    models_dir: Path = Path("models")
    logs_dir: Path = Path("logs")


def load_config(config_path: Optional[str] = None) -> YAANConfig:
    """
    Load configuration from file or environment
    
    Args:
        config_path: Path to config file (optional)
    
    Returns:
        YAANConfig instance
    """
    # TODO: Load from file if provided
    config = YAANConfig()
    
    # Create directories if they don't exist
    config.data_dir.mkdir(exist_ok=True)
    config.models_dir.mkdir(exist_ok=True)
    config.logs_dir.mkdir(exist_ok=True)
    
    # Override with environment variables
    if os.getenv("YAAN_HOST"):
        config.server.host = os.getenv("YAAN_HOST")
    if os.getenv("YAAN_PORT"):
        config.server.port = int(os.getenv("YAAN_PORT"))
    if os.getenv("YAAN_USER_NAME"):
        config.user.name = os.getenv("YAAN_USER_NAME")
    
    return config

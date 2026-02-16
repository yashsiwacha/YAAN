"""
Logging configuration for YAAN
"""

import sys
from pathlib import Path
from loguru import logger


def setup_logger(name: str = "YAAN", log_level: str = "INFO"):
    """
    Setup logger with custom formatting
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    # Remove default handler
    logger.remove()
    
    # Console handler with colors
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True
    )
    
    # File handler (rotating)
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger.add(
        log_dir / "yaan_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
        rotation="00:00",  # Rotate at midnight
        retention="7 days",  # Keep logs for 7 days
        compression="zip"  # Compress old logs
    )
    
    return logger

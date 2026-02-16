"""
YAAN - Your AI Assistant Network
Main Backend Server Entry Point
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from core.server import YAANServer
from core.config import load_config
from core.logger import setup_logger

# Setup logging
logger = setup_logger("YAAN")


def print_banner():
    """Display YAAN startup banner"""
    banner = """
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║   ██╗   ██╗ █████╗  █████╗ ███╗   ██╗   ║
    ║   ╚██╗ ██╔╝██╔══██╗██╔══██╗████╗  ██║   ║
    ║    ╚████╔╝ ███████║███████║██╔██╗ ██║   ║
    ║     ╚██╔╝  ██╔══██║██╔══██║██║╚██╗██║   ║
    ║      ██║   ██║  ██║██║  ██║██║ ╚████║   ║
    ║      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ║
    ║                                           ║
    ║     Your AI Assistant Network v0.1.0     ║
    ║          Offline • Private • Yours       ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝
    """
    print(banner)


async def main():
    """Main entry point for YAAN backend"""
    try:
        print_banner()
        logger.info("Starting YAAN Backend Server...")
        
        # Load configuration
        config = load_config()
        logger.info(f"Configuration loaded: {config.server.host}:{config.server.port}")
        
        # Initialize server
        server = YAANServer(config)
        
        # Start server
        await server.start()
        
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

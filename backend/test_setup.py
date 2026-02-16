"""
Simple test script to verify YAAN backend is working
Run this before starting the full server
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

print("🔧 Testing YAAN Components...")
print("-" * 50)

# Test imports
print("\n1. Testing imports...")
try:
    import core.config as config_module
    import core.logger as logger_module
    import nlp.command_processor as cmd_module
    print("   ✓ Core imports successful")
except Exception as e:
    print(f"   ✗ Import error: {e}")
    sys.exit(1)

# Test configuration
print("\n2. Testing configuration...")
try:
    config = config_module.load_config()
    print(f"   ✓ Config loaded")
    print(f"   - Server: {config.server.host}:{config.server.port}")
    print(f"   - User: {config.user.name}")
    print(f"   - AI Model: {config.ai.model_name}")
except Exception as e:
    print(f"   ✗ Config error: {e}")
    sys.exit(1)

# Test logger
print("\n3. Testing logger...")
try:
    logger = logger_module.setup_logger("Test")
    logger.info("Logger test successful")
    print("   ✓ Logger working")
except Exception as e:
    print(f"   ✗ Logger error: {e}")
    sys.exit(1)

# Test command processor
print("\n4. Testing command processor...")
try:
    import asyncio
    processor = cmd_module.CommandProcessor(config)
    
    async def test_commands():
        commands = [
            "hello",
            "what time is it",
            "system info"
        ]
        
        for cmd in commands:
            response = await processor.process(cmd)
            print(f"   '{cmd}' -> '{response[:50]}...'")
    
    asyncio.run(test_commands())
    print("   ✓ Command processor working")
except Exception as e:
    print(f"   ✗ Command processor error: {e}")
    sys.exit(1)

# Check optional dependencies
print("\n5. Checking optional dependencies...")
optional_deps = [
    ("whisper", "Speech recognition"),
    ("pyttsx3", "Text-to-speech"),
    ("torch", "AI models"),
]

for module, description in optional_deps:
    try:
        __import__(module)
        print(f"   ✓ {description} ({module}) available")
    except ImportError:
        print(f"   ⚠ {description} ({module}) not installed (optional)")

print("\n" + "=" * 50)
print("✅ All basic tests passed!")
print("=" * 50)
print("\nYou can now start the server with:")
print("  python main.py")

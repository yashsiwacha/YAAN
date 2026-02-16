"""Quick test for reminder/todo intent matching"""

import sys
import asyncio
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from nlp.command_processor import CommandProcessor
from core.config import load_config


async def main():
    config = load_config()
    processor = CommandProcessor(config)
    
    test_commands = [
        ("add todo: finish documentation", "create_todo"),
        ("show my todos", "show_todos"),
        ("show my reminders", "show_reminders"),
        ("complete todo 1", "complete_task"),
        ("delete reminder 2", "delete_task"),
        ("task summary", "task_summary"),
    ]
    
    print("\n🧪 Testing Intent Recognition\n" + "=" * 50 + "\n")
    
    for command, expected_intent in test_commands:
        result = await processor.process(command)
        # Check if the intent was matched correctly by looking at the log
        print(f"Command: '{command}'")
        print(f"Expected: {expected_intent}")
        print(f"Result: {result[:100]}...\n")
    
    print("✅ Test complete!")


if __name__ == "__main__":
    asyncio.run(main())

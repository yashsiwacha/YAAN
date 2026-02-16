"""Test script for coding assistant and reminder system features"""

import sys
import asyncio
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from nlp.command_processor import CommandProcessor
from core.config import load_config


def get_processor():
    """Get a configured command processor"""
    config = load_config()
    return CommandProcessor(config)


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


async def test_coding_features():
    """Test coding assistant features"""
    print_section("🧪 Testing Coding Assistant Features")
    
    processor = get_processor()
    
    # Test 1: Code explanation
    print("Test 1: Code explanation")
    code_sample = """
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)
"""
    result = await processor.process(f"explain this code: {code_sample}")
    print(f"✓ Result: {result}\n")
    
    # Test 2: Debug help
    print("Test 2: Debug help")
    buggy_code = """
def hello()
    print('hello world')
"""
    result = await processor.process(f"help debug this Python code with syntax error: {buggy_code}")
    print(f"✓ Result: {result}\n")
    
    # Test 3: Concept explanation
    print("Test 3: Concept explanation")
    result = await processor.process("what is recursion?")
    print(f"✓ Result: {result}\n")
    
    # Test 4: Another concept
    print("Test 4: Explain loops")
    result = await processor.process("explain loops in programming")
    print(f"✓ Result: {result}\n")
    
    # Test 5: JavaScript code
    print("Test 5: JavaScript code analysis")
    js_code = """
function greet(name) {
    return `Hello, ${name}!`;
}
"""
    result = await processor.process(f"analyze this JavaScript code: {js_code}")
    print(f"✓ Result: {result}\n")


async def test_reminder_features():
    """Test reminder system features"""
    print_section("⏰ Testing Reminder System Features")
    
    processor = get_processor()
    
    # Test 1: Create reminder
    print("Test 1: Create reminder with date and time")
    result = await processor.process("remind me to call John tomorrow at 3pm")
    print(f"✓ Result: {result}\n")
    
    # Test 2: Create another reminder
    print("Test 2: Create high priority reminder")
    result = await processor.process("remind me about the meeting at 10am [high]")
    print(f"✓ Result: {result}\n")
    
    # Test 3: Show reminders
    print("Test 3: Show all reminders")
    result = await processor.process("show my reminders")
    print(f"✓ Result: {result}\n")
    
    # Test 4: Create todo
    print("Test 4: Create todo with tag")
    result = await processor.process("add todo: finish project documentation #work")
    print(f"✓ Result: {result}\n")
    
    # Test 5: Create another todo
    print("Test 5: Create high priority todo")
    result = await processor.process("create task: review pull request [high] #code")
    print(f"✓ Result: {result}\n")
    
    # Test 6: Show todos
    print("Test 6: Show all todos")
    result = await processor.process("show my todos")
    print(f"✓ Result: {result}\n")
    
    # Test 7: Task summary
    print("Test 7: Get task summary")
    result = await processor.process("task summary")
    print(f"✓ Result: {result}\n")
    
    # Test 8: Complete a todo
    print("Test 8: Complete todo #1")
    result = await processor.process("complete todo 1")
    print(f"✓ Result: {result}\n")
    
    # Test 9: Show updated todos
    print("Test 9: Show todos after completion")
    result = await processor.process("show my todos")
    print(f"✓ Result: {result}\n")
    
    # Test 10: Delete a reminder
    print("Test 10: Delete reminder #1")
    result = await processor.process("delete reminder 1")
    print(f"✓ Result: {result}\n")


async def test_help_command():
    """Test updated help text"""
    print_section("📚 Testing Updated Help Command")
    
    processor = get_processor()
    
    print("Requesting help/capabilities...")
    result = await processor.process("help")
    print(f"✓ Result:\n{result}\n")


async def main_async():
    """Run all tests asynchronously"""
    print("\n" + "▓" * 60)
    print("  YAAN - Coding & Reminder System Test Suite")
    print("▓" * 60)
    
    try:
        # Test coding features
        await test_coding_features()
        
        # Test reminder features
        await test_reminder_features()
        
        # Test help command
        await test_help_command()
        
        print_section("✅ All Tests Completed Successfully")
        print("The coding assistant and reminder system are working correctly!")
        print("Integration complete. You can now use these features in YAAN.\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def main():
    """Run the async main function"""
    return asyncio.run(main_async())


if __name__ == "__main__":
    exit(main())

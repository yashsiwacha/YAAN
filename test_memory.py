"""
Test script for user memory system
"""

import sys
sys.path.insert(0, 'backend')

from pathlib import Path
from user.profile import UserProfile
from user.memory import UserMemory
from core.config import YAANConfig

# Initialize
config = YAANConfig()
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

profile = UserProfile(data_dir, "TestUser")
memory = UserMemory(profile)

print("=" * 50)
print("YAAN User Memory System Test")
print("=" * 50)

# Test 1: Analyze message with personal info
print("\n[Test 1] Analyzing message with personal info...")
message1 = "Hi! My name is Alex and I'm a software engineer from Seattle. I love Python programming."
memory.analyze_message(message1)
print(f"✓ Analyzed: {message1}")

# Test 2: Check what was learned
print("\n[Test 2] Checking learned information...")
print(f"User facts: {memory.user_facts}")
print(f"Interests: {memory.interests}")
print(f"Communication style: {memory.communication_style['formality']}")

# Test 3: Get memory summary
print("\n[Test 3] Memory summary:")
print(memory.get_memory_summary())

# Test 4: Get personalized greeting
print("\n[Test 4] Personalized greeting:")
print(memory.get_personalized_greeting())

# Test 5: Test memory retrieval
print("\n[Test 5] Testing memory retrieval...")
query1 = "What's my name?"
response1 = memory.get_relevant_memory(query1)
print(f"Q: {query1}")
print(f"A: {response1}")

# Test 6: Save memory
print("\n[Test 6] Saving memory to database...")
memory.save_memory()
print("✓ Memory saved")

# Test 7: Test with more messages
print("\n[Test 7] Analyzing more messages...")
messages = [
    "I really enjoy working with machine learning algorithms",
    "Hey, can you help me with some code?",
    "Thanks for your help!",
]

for msg in messages:
    memory.analyze_message(msg)
    print(f"✓ Analyzed: {msg}")

# Test 8: Check updated interests
print("\n[Test 8] Updated interests:")
top_interests = sorted(memory.interests.items(), key=lambda x: x[1], reverse=True)[:3]
for interest, count in top_interests:
    print(f"  • {interest}: {count} mentions")

# Test 9: Communication style detection
print("\n[Test 9] Communication style:")
print(f"  Formality: {memory.communication_style['formality']}")
print(f"  Verbosity: {memory.communication_style['verbosity']}")
print(f"  Emoji usage: {memory.communication_style['emoji_usage']}")
print(f"  Avg message length: {memory.communication_style['avg_message_length']} words")

# Test 10: Context for response
print("\n[Test 10] Context for personalized response:")
context = memory.get_context_for_response()
print(f"  User name: {context['user_name']}")
print(f"  Formality: {context['formality']}")
print(f"  Top interests: {[i[0] for i in context['top_interests']]}")

print("\n" + "=" * 50)
print("All tests completed successfully! ✓")
print("=" * 50)
print(f"\nMemory database location: {profile.db_path}")
print("You can now start the server and test the memory features in the chat!")

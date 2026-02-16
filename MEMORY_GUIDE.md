# YAAN User Memory System

YAAN now has an advanced memory system that learns about you and adapts to your communication style!

## What the AI Learns

### 1. **Personal Information**
- Your name (e.g., "My name is John")
- Location (e.g., "I live in New York")
- Occupation (e.g., "I work as a developer")
- Likes and preferences (e.g., "I like Python programming")
- Dislikes (e.g., "I don't like cold weather")

### 2. **Communication Style**
- **Formality Level**: Detects if you prefer casual ("hey", "yeah") or formal ("greetings", "thank you") language
- **Message Length**: Learns if you prefer brief or detailed responses
- **Emoji Usage**: Notices if you use emojis and adjusts accordingly
- **Common Phrases**: Tracks your frequently used expressions

### 3. **Interests & Topics**
The AI tracks what topics you discuss most frequently:
- Programming & Technology
- Work & Projects
- Entertainment
- Learning & Education
- Health & Fitness
- And more...

### 4. **Conversation Context**
- Remembers recent conversation topics
- Maintains session context for follow-up questions
- Recalls facts you've shared

## How to Use Memory Features

### Tell the AI About Yourself
Just chat naturally! The AI will automatically learn from statements like:
```
"My name is Sarah"
"I'm from California"
"I work as a data scientist"
"I love machine learning"
"I enjoy reading sci-fi books"
```

### Query What It Knows
Ask the AI what it remembers:
```
"What do you know about me?"
"What have you learned about me?"
"What are my interests?"
"My name?"
```

### Personalized Greetings
The AI will greet you based on your communication style:
- **Casual**: "Hey John!" or "What's up Sarah?"
- **Formal**: "Good day, Mr. Smith."
- **Neutral**: "Hello there!"

### Privacy Controls
Clear your data anytime:
```
"Forget everything about me"
"Clear my memory"
"Delete my data"
```

## Memory Storage

- All data is stored **locally** in `data/user_profile.db`
- **SQLite database** - no cloud, no external servers
- Includes conversation history, preferences, and learned patterns
- Fully private and under your control

## How It Works

1. **Analyze**: Every message you send is analyzed for:
   - Personal information
   - Communication patterns
   - Topic keywords
   - Sentiment and style

2. **Learn**: The AI updates its knowledge:
   - Stores facts in memory
   - Tracks topic frequency
   - Adjusts communication style
   - Builds your interest profile

3. **Personalize**: Responses are tailored based on:
   - Your name and known facts
   - Preferred formality level
   - Recent conversation context
   - Your interests

4. **Persist**: Everything is saved to disk:
   - Survives restarts
   - Builds over time
   - Improves with more interactions

## Example Interactions

### Learning Phase
**You**: "Hi! My name is Alex and I'm a software engineer from Seattle"
**YAAN**: "Nice to meet you, Alex! How can I help you today?"

*(YAAN now knows: name=Alex, occupation=software engineer, location=Seattle)*

### Using Memory
**You**: "What's my name?"
**YAAN**: "Your name is Alex."

**You**: "What do you know about me?"
**YAAN**: 
```
Here's what I've learned about you:

• Your name: Alex
• Location: Seattle
• Occupation: software engineer
• Communication style: casual
```

### Personalized Responses
After learning your style, YAAN adapts:
- Uses casual language if you do
- Keeps responses brief if you prefer
- References your interests in conversations
- Greets you by name

## Privacy & Security

✅ **Local Storage Only** - No data sent to external servers
✅ **Full Control** - Delete your data anytime
✅ **Transparent** - Ask what's stored at any time
✅ **Secure** - SQLite database on your machine
✅ **Optional** - Memory features enhance but don't limit functionality

## Files Created

- `data/user_profile.db` - SQLite database with your information
- Automatically created on first use
- Safe to delete if you want to start fresh

## Advanced Features

### Context-Aware Responses
The AI uses memory to:
- Answer follow-up questions
- Reference previous conversations
- Provide relevant suggestions based on interests
- Maintain conversation flow

### Learning Over Time
With each interaction, YAAN:
- Refines understanding of your preferences
- Improves response personalization
- Builds a more accurate profile
- Adapts to changes in your communication

### Session Memory
Current session tracking:
- Topics discussed today
- Recent questions and answers
- Temporary context for follow-ups

---

**Start chatting naturally and watch YAAN learn about you!** 🧠✨

# YAAN - Your AI Assistant Network

**Version 1.0** | A powerful, intelligent AI assistant with memory, coding help, task management, and proactive learning.

## ✨ What is YAAN?

YAAN is a conversational AI assistant that helps with:
- 💻 **Coding assistance** - Explain code, debug errors, learn concepts
- 🧠 **Smart memory** - Remembers your preferences and personal info
- ⏰ **Task management** - Reminders and todos with natural language
- 🎓 **Proactive learning** - Asks questions to understand you better
- 🎨 **Beautiful UI** - Modern web interface with syntax highlighting

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- 2GB+ RAM
- Windows/Mac/Linux

### Installation
```bash
# Clone the repository
git clone https://github.com/yashsiwacha/YAAN.git
cd YAAN

# Set up backend
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start YAAN
python main.py
```

### Access YAAN
Open your browser and navigate to: **http://localhost:8000**

## 🎯 Features (v1.0)

### 🧠 Intelligent Memory System
- Learns your name, location, occupation
- Remembers communication preferences
- Tracks interests by conversation topics
- Query: "What do you know about me?"
- Clear memory anytime: "Clear my memory"

### 💻 Coding Assistant
- **15+ Languages**: Python, JavaScript, TypeScript, Java, C++, C, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, SQL, HTML, CSS
- **Comprehensive Debugging**: Analyze any error with detailed explanations
  - 60+ error types across all languages
  - Automatic language detection
  - Error pattern matching
  - Code issue analysis (syntax, null checks, bounds, type mismatches)
  - Step-by-step debugging guidance
- **Explain code snippets** in any language
- **Debug errors** with intelligent error analysis
- **Learn programming concepts** (recursion, OOP, async, algorithms, etc.)
- **Code templates** for common patterns
- **Complexity analysis** (loops, conditionals, lines of code)
- **Syntax highlighting** in chat
- **Language-specific debugging tools** suggestions

### ⏰ Task Management
- Natural language reminders: "Remind me to call John tomorrow at 3pm"
- Todo lists with priorities: "Add todo: finish project #work [high]"
- Categories with hashtags (#work, #personal, #school)
- View/complete/delete tasks
- Task summary overview
- Persistent storage across sessions

### 🎓 Proactive Learning (NEW!)
- AI asks strategic questions to learn about you
- 25 questions across 5 categories:
  - Personal (name, location, interests)
  - Preferences (communication style)
  - Goals (career, learning)
  - Workflow (habits, routines)
  - Feedback (improvements)
- Smart timing: 30% chance after 5+ messages
- Max 2 questions per day, 5min intervals
- Enable/disable anytime
- View learning summary

### 🎨 Modern UI Features
- Settings panel (gear icon)
- Help & guide panel (? icon)
- Keyboard shortcuts (Ctrl+K, Ctrl+/)
- Code syntax highlighting
- Typing indicator
- Toast notifications
- Quick suggestion buttons
- Export conversations
- Dark theme optimized

## 📚 Usage Examples

### Memory & Personalization
```
You: "My name is John and I live in New York"
YAAN: ✅ I'll remember that!

You: "What do you know about me?"
YAAN: Here's what I know about you:
      - Name: John
      - Location: New York
```

### Coding Help
```
You: "explain this code: def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"
YAAN: [Detailed explanation of recursive Fibonacci function]

You: "what is polymorphism in C++?"
YAAN: [Comprehensive explanation with examples]
```

### Debug Any Error (15+ Languages)
```
You: "I'm getting: TypeError: unsupported operand type(s) for +: 'int' and 'str'
      Code: x = 5; y = '10'; result = x + y"

YAAN: ## 🐛 Debug Analysis
      
      TypeError (Python) - Wrong data type operation. 
      Can't add string + integer directly.
      
      Potential Issues: Mixing strings and numbers
      
      Fix: Use str(x) + y for concatenation 
           OR x + int(y) for math
      
      Detected language: PYTHON
```

### Task Management
```
You: "remind me to submit report tomorrow at 5pm #work"
YAAN: ✅ Reminder set: Submit report
      📅 Due: Tomorrow at 5:00 PM
      🏷️ Category: work

You: "show my todos"
YAAN: [Lists all todos with priorities and categories]
```

### Proactive Learning
```
YAAN: "I'd love to learn more about you! What's your preferred communication style - detailed or concise?"
You: "I prefer concise responses"
YAAN: ✅ Thanks! I'll keep my responses brief and to the point.
```

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Ctrl+K` | Clear chat |
| `Ctrl+/` | Toggle help |
| `Esc` | Close panels |

## 🔧 Commands Reference

### Memory Commands
- "What do you know about me?"
- "Clear my memory"
- "Forget about [topic]"

### Coding Commands
- "Explain this code: [code]"
- "What is [concept]?" (recursion, OOP, async, etc.)
- "Debug this error: [error message]"  
- "Fix this error: [error + code]"
- "Why am I getting [error type]?"
- "How do I [task] in [language]?"
- Supported: Python, JavaScript, TypeScript, Java, C++, C, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, SQL, HTML, CSS

### Task Commands
- "Remind me to [task] [when]"
- "Add todo: [task] #[category] [priority]"
- "Show my reminders/todos"
- "Complete todo [number]"
- "Delete reminder [number]"
- "Task summary"

### Learning Commands
- "Learning summary"
- "Stop asking questions"
- "Enable learning questions"

### General Commands
- "What time is it?"
- "Calculate [expression]"
- "Tell me a joke"
- "Help" or "What can you do?"

## 🏗️ Architecture

```
YAAN/
├── backend/
│   ├── core/              # Server & configuration
│   ├── nlp/               # AI engine, command processor
│   │   ├── ai_engine.py           # Main AI logic
│   │   ├── command_processor.py   # Intent matching (26 intents)
│   │   ├── coding_assistant.py    # Coding help
│   │   ├── reminder_system.py     # Task management
│   │   └── proactive_learning.py  # Learning system
│   ├── user/              # Memory & profile
│   ├── static/            # Web UI
│   └── data/              # SQLite databases
├── docs/                  # Documentation
└── PROJECT_STATUS.md      # Development tracking
```

## 🗄️ Databases

YAAN uses 4 SQLite databases:
- `user_profile.db` - Memory and preferences
- `reminders.db` - Tasks and todos
- `learning.db` - Questions and answers
- `debug_errors.db` - Common coding errors (400+)

## 📊 Project Stats

- **27 Intents** - Command recognition patterns (added debug_error)
- **45+ Features** - Fully implemented
- **6500+ Lines** - Production code
- **4 Databases** - SQLite storage
- **15+ Languages** - Comprehensive coding support
- **60+ Error Types** - Across all major languages
- **90%+ Test Coverage** - Comprehensive testing

## 🛠️ Technology Stack

### Backend
- **Python 3.12** - Core language
- **FastAPI** - Web framework
- **WebSocket** - Real-time communication
- **SQLite** - Data persistence
- **Regex NLP** - Pattern matching

### Frontend
- **HTML5/CSS3/JavaScript** - Web interface
- **Highlight.js** - Code syntax highlighting
- **Web Speech API** - Voice capabilities (future)

## 📖 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Get started in 5 minutes
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - Development progress
- [MEMORY_GUIDE.md](MEMORY_GUIDE.md) - Memory system details
- [GETTING_STARTED.md](GETTING_STARTED.md) - Detailed setup
- [ROADMAP.md](ROADMAP.md) - Future plans

## 🔄 Development Workflow

### Multi-System Development
This project uses [PROJECT_STATUS.md](PROJECT_STATUS.md) for tracking work across multiple development systems.

### Running Tests
```bash
cd backend
python tests/test_intent_matching.py
python tests/test_coding_and_reminders.py
```

### Making Changes
1. Update code
2. Run tests
3. Update PROJECT_STATUS.md
4. Commit with descriptive message
5. Push to GitHub

## 🚀 Planned Features (v1.1+)

- [ ] Full voice mode (Web Speech API)
- [ ] Weather API integration
- [ ] Desktop notifications
- [ ] Search conversation history
- [ ] Recurring reminders
- [ ] Theme customization
- [ ] Code snippet library
- [ ] Multi-language UI support

## 🔐 Privacy & Security

- ✅ All data stored locally
- ✅ No external API calls
- ✅ SQLite encryption ready
- ✅ Open source code
- ✅ Full user control

## 📝 License

MIT License - Free to use, modify, and distribute

## 🤝 Contributing

This is a personal learning project, but suggestions and feedback are welcome!

## 👨‍💻 Author

**Yash Siwach**  
GitHub: [@yashsiwacha](https://github.com/yashsiwacha)  
Project: [YAAN](https://github.com/yashsiwacha/YAAN)

---

**Version 1.0** | February 2026 | Made with ❤️ and ☕

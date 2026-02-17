# YAAN - Your AI Assistant Network

<div align="center">

![Version](https://img.shields.io/badge/version-v1-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-stable-success.svg)

**A powerful, intelligent AI assistant with memory, coding help, task management, and proactive learning.**

[Quick Start](#-quick-start) • [Features](#-features) • [Examples](#-usage-examples) • [Deployment](DEPLOYMENT.md) • [GitHub](https://github.com/yashsiwacha/YAAN)

</div>

---

## ✨ What is YAAN?

YAAN (Your AI Assistant Network) is a **production-ready, conversational AI assistant** designed to enhance your productivity and learning. Built with Python and FastAPI, YAAN provides intelligent assistance across multiple domains.

### 🎯 Core Capabilities

- 💻 **Advanced Coding Assistant** - Structured concept explanations, debug 60+ error types across 15+ languages
- 🧠 **Intelligent Memory System** - Learns and remembers your preferences, interests, and personal information  
- ⏰ **Smart Task Management** - Natural language reminders and todos with categories and priorities
- 🎓 **Proactive Learning Engine** - Asks strategic questions to understand you better over time
- 🎨 **Modern Web Interface** - Beautiful UI with syntax highlighting, keyboard shortcuts, and responsive design

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** (3.12 recommended)
- **2GB+ RAM** 
- **Windows, macOS, or Linux**

### Installation (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/yashsiwacha/YAAN.git
cd YAAN/backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Start YAAN
python main.py
```

**Access YAAN:** Open your browser → **http://localhost:8000**

**First Time?** Type "help" or "what can you do?" to get started!

## 📦 Deployment

YAAN supports multiple deployment methods for different use cases:

### One-Click Installation
```bash
# Windows
.\install.ps1

# Linux/Mac
./install.sh
```

### Docker Deployment
```bash
docker-compose up -d
```

### Production Deployment
- Linux systemd service
- Windows Service (NSSM)
- Cloud platforms (AWS, GCP, Azure)
- Nginx reverse proxy

**📘 [Full Deployment Guide →](DEPLOYMENT.md)**

For detailed instructions on all deployment methods, troubleshooting, and production configuration, see the [DEPLOYMENT.md](DEPLOYMENT.md) guide.

## 🎯 Features

### 💻 Advanced Coding Assistant

#### 🌟 Structured Concept Explanations (Flagship Feature)
YAAN provides **comprehensive, 5-section structured explanations** for programming concepts:

**Ask about any concept:**
- "What is dynamic programming?"
- "Explain recursion"
- "What is polymorphism?"
- "Explain async/await"

**Get structured responses with:**
1. **📖 Definition** - Clear explanation of the concept
2. **🎯 Use Case** - When and why to use it
3. **💻 Syntax** - Code examples with syntax highlighting
4. **✅ Uses** - Practical applications and scenarios
5. **🔑 Key Takeaways** - Important points to remember

#### 🐛 Comprehensive Error Debugging
- **60+ Error Types** across all major languages
- **15+ Supported Languages**: Python, JavaScript, TypeScript, Java, C++, C, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, SQL, HTML/CSS
- **Intelligent Error Analysis**:
  - Automatic language detection
  - Error pattern matching
  - Syntax error identification
  - Null/undefined checks
  - Type mismatch detection
  - Array bounds checking
- **Step-by-step debugging guidance** with code fixes
- **Language-specific tool suggestions** (debuggers, linters)

#### 📚 Additional Coding Features
- **Code Explanation** - Understand any code snippet in plain English
- **Template Generation** - Common patterns (loops, functions, classes)
- **Complexity Analysis** - Understand your code's structure
- **Multi-language Support** - Consistent experience across all languages

### 🧠 Intelligent Memory System

YAAN learns and remembers information about you across conversations:

**What YAAN Remembers:**
- 👤 **Personal Information** - Name, location, occupation
- 💬 **Communication Preferences** - Detailed vs concise, formal vs casual
- 🎯 **Interests & Hobbies** - Topics you discuss frequently
- 🎓 **Learning Goals** - Career aspirations, skills to learn
- 🔧 **Workflow & Habits** - Work patterns, routines

**Memory Commands:**
- "What do you know about me?" - View all stored information
- "Clear my memory" - Reset all data
- "Forget about [topic]" - Remove specific information

**Privacy First:** All data stored locally in SQLite, no external API calls.

### ⏰ Smart Task Management

Natural language task creation with intelligent parsing:

**Features:**
- 📅 **Smart Date Parsing** - "tomorrow", "next Friday", "in 2 hours"
- 🏷️ **Categories** - Use hashtags (#work, #personal, #school)
- ⚡ **Priority Levels** - [high], [medium], [low]
- ✅ **Todo Lists** - Track tasks with completion status
- 🔔 **Reminders** - Time-based notifications

**Examples:**
```
"Remind me to call John tomorrow at 3pm #personal"
"Add todo: finish project report #work [high]"
"Show my reminders"
"Complete todo 1"
```

### 🎓 Proactive Learning Engine

YAAN proactively asks questions to understand you better:

**Smart Learning System:**
- 25 strategic questions across 5 categories
- 30% chance to ask after 5+ messages
- Max 2 questions per day, 5-minute intervals
- Enable/disable anytime with "stop asking questions"
- View what YAAN has learned with "learning summary"

**Question Categories:**
1. Personal - Name, location, interests
2. Preferences - Communication style, response format
3. Goals - Career objectives, learning targets
4. Workflow - Habits, routines, work patterns
5. Feedback - Improvements, feature requests

### 🎨 Modern Web Interface

Beautiful, responsive UI with powerful features:

**UI Features:**
- ⚙️ **Settings Panel** - Configure preferences (gear icon)
- ❓ **Help & Guide** - Interactive help system (? icon)
- ⌨️ **Keyboard Shortcuts** - Ctrl+K (clear), Ctrl+/ (help)
- 🎨 **Code Highlighting** - Syntax highlighting with Highlight.js
- 💬 **Typing Indicator** - Real-time feedback
- 🔔 **Toast Notifications** - Success/error messages
- 💡 **Quick Suggestions** - One-click command buttons
- 📤 **Export Conversations** - Save chat history
- 🌙 **Dark Theme** - Optimized for long sessions



## � Usage Examples

### 🌟 Structured Concept Explanations

**Input:** `What is dynamic programming?`

**YAAN Output:**
```
📖 DEFINITION
Dynamic programming is a method for solving complex problems by breaking them 
down into simpler overlapping subproblems and storing their solutions.

🎯 USE CASE
When you have problems with overlapping subproblems and optimal substructure
(like Fibonacci, shortest path, longest common subsequence).

💻 SYNTAX
# Memoization (Top-Down)
def fib_memo(n, memo={}):
    if n in memo: return memo[n]
    if n <= 1: return n
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]

# Tabulation (Bottom-Up)
def fib_tab(n):
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

✅ USES
• Optimization problems (knapsack, coin change)
• Pathfinding algorithms (shortest path)
• String problems (edit distance, LCS)
• Game theory (min-max strategies)

🔑 KEY TAKEAWAYS
• Reduces time complexity by avoiding redundant calculations
• Two approaches: memoization (recursive) and tabulation (iterative)
• Time-space tradeoff: uses memory to save computation time
```

---

### 💻 Code Explanation

**Input:** `Explain this code: def factorial(n): return 1 if n <= 1 else n * factorial(n-1)`

**YAAN Output:**
```
This is a recursive function that calculates factorial:

1. Base case: Returns 1 when n <= 1
2. Recursive case: Multiplies n by factorial(n-1)
3. Works by breaking problem down to smaller subproblems

Example: factorial(5)
→ 5 * factorial(4)
→ 5 * 4 * factorial(3)
→ 5 * 4 * 3 * 2 * 1 = 120

Time Complexity: O(n)
Space Complexity: O(n) due to call stack
```

---

### 🐛 Error Debugging

**Input:** 
```
Debug this error:
TypeError: unsupported operand type(s) for +: 'int' and 'str'

Code:
x = 5
y = "10"
result = x + y
```

**YAAN Output:**
```
## 🐛 Debug Analysis

**Error Type:** TypeError (Python)
**Issue:** Cannot use + operator between int and str

**What's Wrong:**
You're trying to add a number (5) and a string ("10"). Python doesn't
know if you want mathematical addition or string concatenation.

**Potential Issues:**
✗ Mixing incompatible data types
✗ Missing type conversion

**Solutions:**

1️⃣ For String Concatenation:
result = str(x) + y  # "510"

2️⃣ For Mathematical Addition:
result = x + int(y)  # 15

3️⃣ Use f-strings (recommended):
result = f"{x}{y}"  # "510"

**Best Practice:** Always convert types explicitly before operations.

**Debugging Tools:** Use type() to check variable types: print(type(x), type(y))

Detected Language: PYTHON
```

---

### 🧠 Memory & Personalization

**Conversation:**
```
You: "My name is Alex and I work as a software engineer in Seattle"
YAAN: ✅ Got it! I'll remember that you're Alex, a software engineer in Seattle.

You: "I prefer concise explanations"
YAAN: ✅ Noted! I'll keep my responses brief.

You: "What do you know about me?"
YAAN: Here's what I know about you:
      👤 Name: Alex
      💼 Occupation: Software engineer
      📍 Location: Seattle
      💬 Communication: Prefers concise explanations
```

---

### ⏰ Task Management

**Natural Language Tasks:**
```
You: "Remind me to submit the project report tomorrow at 5pm #work [high]"
YAAN: ✅ Reminder created successfully!
      📋 Task: Submit the project report
      📅 Due: Tomorrow at 5:00 PM
      🏷️ Category: work
      ⚡ Priority: HIGH

You: "Add todo: buy groceries #personal"
YAAN: ✅ Todo added!

You: "Show my tasks"
YAAN: 📋 Your Reminders & Todos
      
      ⏰ REMINDERS:
      1. [HIGH] Submit project report (Tomorrow, 5:00 PM) #work
      
      ✅ TODOS:
      1. Buy groceries #personal
```

---

### 🎓 Proactive Learning

**YAAN asks questions over time:**
```
YAAN: "I'd love to learn more about you! What programming languages do you 
       use most often?"
You: "Mainly Python and JavaScript"
YAAN: ✅ Thanks for sharing! I'll remember that.

[Later in conversation...]

YAAN: "What's your preferred communication style - detailed explanations 
       or brief summaries?"
You: "Brief summaries please"
YAAN: ✅ Perfect! I'll keep things concise.
```



## ⌨️ Commands Reference

### 💻 Coding Commands
| Command | Example |
|---------|---------|
| Structured explanations | "What is recursion?", "Explain polymorphism" |
| Concept learning | "What is async/await?", "Explain OOP" |
| Code explanation | "Explain this code: [code]" |
| Error debugging | "Debug this error: [error]" |
| Fix errors | "Fix this: [error + code]" |
| How-to queries | "How do I sort an array in Python?" |
| Templates | "Show me a Python class template" |

**Supported Languages:** Python, JavaScript, TypeScript, Java, C++, C, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, SQL, HTML, CSS

### 🧠 Memory Commands
| Command | Description |
|---------|-------------|
| `What do you know about me?` | View all stored information |
| `Clear my memory` | Reset all data |
| `Forget about [topic]` | Remove specific information |

### ⏰ Task Commands
| Command | Example |
|---------|---------|
| Create reminder | `Remind me to [task] [when]` |
| Add todo | `Add todo: [task] #[category] [priority]` |
| View tasks | `Show my reminders`, `Show my todos` |
| Complete task | `Complete todo 1` |
| Delete task | `Delete reminder 2` |
| Task overview | `Task summary` |

**Priorities:** `[high]`, `[medium]`, `[low]`  
**Categories:** Use hashtags like `#work`, `#personal`, `#school`

### 🎓 Learning Commands
| Command | Description |
|---------|-------------|
| `Learning summary` | View what YAAN has learned |
| `Stop asking questions` | Disable proactive learning |
| `Enable learning questions` | Re-enable learning mode |

### 🔧 General Commands
| Command | Description |
|---------|-------------|
| `Help` | Show help guide |
| `What can you do?` | List all capabilities |
| `What time is it?` | Current time |
| `Calculate [expression]` | Math calculations |
| `Tell me a joke` | Get a random joke |

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Shift + Enter` | New line in input |
| `Ctrl + K` | Clear chat history |
| `Ctrl + /` | Toggle help panel |
| `Esc` | Close open panels |



## 🏗️ Architecture

```
YAAN/
├── backend/
│   ├── main.py                    # FastAPI server & WebSocket handler
│   ├── core/
│   │   ├── server.py              # Server configuration
│   │   └── config.py              # System settings
│   ├── nlp/
│   │   ├── ai_engine.py           # Main AI logic & response generator
│   │   ├── command_processor.py   # Intent matching (27 intents)
│   │   ├── coding_assistant.py    # Structured explanations & debugging
│   │   ├── reminder_system.py     # Task & reminder management
│   │   ├── proactive_learning.py  # Question engine
│   │   └── error_database.py      # 400+ common errors database
│   ├── user/
│   │   ├── memory_manager.py      # User profile & memory
│   │   └── user_profile.py        # Profile data model
│   ├── static/
│   │   ├── index.html             # Main UI
│   │   ├── styles.css             # Responsive design
│   │   └── app.js                 # WebSocket client & UI logic
│   └── data/                      # SQLite databases
│       ├── user_profile.db        # Memory & preferences
│       ├── reminders.db           # Tasks & todos
│       ├── learning.db            # Learning Q&A
│       └── debug_errors.db        # Error patterns
├── docs/                          # Documentation
├── tests/                         # Test suites
├── PROJECT_STATUS.md              # Development tracking
├── V2_ROADMAP.md                  # Future plans
└── README.md                      # This file
```

### 🔄 How It Works

1. **User Input** → WebSocket connection sends message to backend
2. **Intent Matching** → Command processor identifies user intent (27 patterns)
3. **AI Processing** → Appropriate module handles request:
   - `coding_assistant.py` → Code explanations & debugging
   - `memory_manager.py` → Store/retrieve user information
   - `reminder_system.py` → Task management
   - `proactive_learning.py` → Ask strategic questions
4. **Response Generation** → Format and send response with Markdown/code
5. **UI Rendering** → Display with syntax highlighting & formatting



## 🗄️ Data Storage

YAAN uses **4 SQLite databases** for persistent storage:

| Database | Purpose | Tables |
|----------|---------|--------|
| `user_profile.db` | User memory & preferences | profiles, memories |
| `reminders.db` | Tasks & todos | reminders, todos |
| `learning.db` | Questions & answers | questions, answers, asked_questions |
| `debug_errors.db` | Common coding errors | errors (400+ patterns) |

**Why SQLite?**
- ✅ Zero configuration required
- ✅ Serverless and self-contained
- ✅ ACID-compliant transactions
- ✅ Cross-platform compatibility
- ✅ Perfect for single-user applications

All data is stored locally on your machine - **no cloud, no external APIs**.

---

## 📊 Project Stats (v1)

<div align="center">

| Metric | Count |
|--------|-------|
| **Total Code Lines** | 7,700+ |
| **Features Implemented** | 46+ |
| **Intent Patterns** | 27 |
| **Programming Languages Supported** | 15+ |
| **Error Types Recognized** | 60+ |
| **Databases** | 4 |
| **Common Errors in DB** | 400+ |
| **Test Coverage** | 90%+ |
| **Documentation Files** | 10+ |

</div>

### 🏆 Production Ready
- ✅ Stable v1 release on GitHub
- ✅ Comprehensive documentation
- ✅ Extensive testing & debugging
- ✅ Real-world usage validated
- ✅ Performance optimized



## 🛠️ Technology Stack

### Backend
- **Python 3.12** - Core programming language
- **FastAPI** - Modern async web framework
- **WebSocket** - Real-time bidirectional communication
- **SQLite3** - Embedded database (4 databases)
- **Regex NLP** - Pattern-based intent matching (27 intents)

### Frontend  
- **HTML5/CSS3** - Modern web standards
- **Vanilla JavaScript** - No framework dependencies
- **Highlight.js** - Syntax highlighting for 15+ languages
- **Responsive Design** - Works on all screen sizes
- **WebSocket API** - Real-time messaging

### Development
- **Git** - Version control
- **GitHub** - Repository hosting
- **pytest** - Testing framework (90%+ coverage)
- **VS Code** - Primary development environment

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | Main documentation (this file) |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Deployment guide for all platforms |
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Development progress & v1 status |
| [V2_ROADMAP.md](V2_ROADMAP.md) | Future plans & v2.0 features |
| [QUICKSTART.md](QUICKSTART.md) | Get started in 5 minutes |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Detailed setup guide |
| [MEMORY_GUIDE.md](MEMORY_GUIDE.md) | Memory system details |

---

## 🚀 What's Next? (v2.0 Roadmap)

YAAN v2.0 is planned with major new features:

### 🌟 Flagship Feature: LeetCode Integration
- 500+ coding problems with solutions
- 20+ topics (Array, DP, Trees, Graphs, etc.)
- 15+ problem patterns (Two Pointers, Sliding Window, etc.)
- Daily challenge system
- Progress tracking & analytics
- Multi-language code generation

### 🎤 Additional Features
- Voice mode with Web Speech API
- Advanced learning system with spaced repetition
- Collaboration features (share solutions, compete)
- Enhanced pattern recognition
- Performance optimizations
- Extended language support

**Timeline:** 10 weeks (Feb 25 - May 1, 2026)  
**See:** [V2_ROADMAP.md](V2_ROADMAP.md) for complete specifications



## � Development & Testing

### Running Tests
```bash
# Navigate to backend
cd backend

# Run all tests
python tests/test_intent_matching.py
python tests/test_coding_and_reminders.py

# Or run specific test
pytest tests/test_memory.py -v
```

### Development Workflow
1. **Make Changes** - Edit code in your preferred editor
2. **Test Locally** - Run test suite to verify changes
3. **Update Docs** - Keep PROJECT_STATUS.md current
4. **Commit** - Use descriptive commit messages
5. **Push** - Sync with GitHub repository

### Multi-System Development
YAAN uses [PROJECT_STATUS.md](PROJECT_STATUS.md) to track development across multiple machines. Check this file for current progress and pending tasks.

### Code Structure
- Keep modules focused and single-purpose
- Follow Python PEP 8 style guidelines
- Add docstrings to all functions
- Update tests when adding features
- Document breaking changes

---

## 🔐 Privacy & Security

**Your Data, Your Control**

- ✅ **100% Local Storage** - All data stored in SQLite on your machine
- ✅ **No Cloud Services** - Zero external API calls or data transmission
- ✅ **No Telemetry** - No usage tracking or analytics
- ✅ **Open Source** - Full code transparency on GitHub
- ✅ **Encryption Ready** - SQLite supports encryption extensions
- ✅ **User Control** - Clear memory anytime with one command

**What YAAN Never Does:**
- ❌ Send your data to external servers
- ❌ Track your usage or behavior
- ❌ Require registration or login
- ❌ Connect to third-party APIs
- ❌ Store data outside your machine

---

## 📝 License

**MIT License** - Copyright © 2026 Yash Siwach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.

See [LICENSE](LICENSE) file for full terms.

---

## 🤝 Contributing

YAAN is a personal learning project, but contributions are welcome!

**Ways to Contribute:**
- 🐛 Report bugs via GitHub Issues
- 💡 Suggest features or improvements  
- 📖 Improve documentation
- 🧪 Add test cases
- ⭐ Star the repository

**Before Contributing:**
1. Check existing issues and PRs
2. Open an issue to discuss major changes
3. Follow existing code style
4. Add tests for new features
5. Update documentation

---

## 🔗 Links & Resources

- **GitHub Repository:** [github.com/yashsiwacha/YAAN](https://github.com/yashsiwacha/YAAN)
- **Latest Release:** [v1](https://github.com/yashsiwacha/YAAN/releases/tag/v1)
- **Stable Branch:** [v1](https://github.com/yashsiwacha/YAAN/tree/v1)
- **Development Branch:** [main](https://github.com/yashsiwacha/YAAN/tree/main)
- **Issues:** [Report bugs or request features](https://github.com/yashsiwacha/YAAN/issues)

---

## 👨‍💻 Author

**Yash Siwach**  
Software Engineer | AI Enthusiast

- GitHub: [@yashsiwacha](https://github.com/yashsiwacha)
- Project: [YAAN - Your AI Assistant Network](https://github.com/yashsiwacha/YAAN)

---

## 🙏 Acknowledgments

Built with passion using:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [SQLite](https://www.sqlite.org/) - Embedded SQL database
- [Highlight.js](https://highlightjs.org/) - Syntax highlighting library

Special thanks to the open-source community for excellent tools and documentation.

---

<div align="center">

**YAAN v1** | February 2026 | Made with ❤️ and ☕

[![GitHub](https://img.shields.io/badge/GitHub-yashsiwacha/YAAN-blue?logo=github)](https://github.com/yashsiwacha/YAAN)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Stable-success.svg)](https://github.com/yashsiwacha/YAAN/releases)

**[⬆ Back to Top](#yaan---your-ai-assistant-network)**

</div>

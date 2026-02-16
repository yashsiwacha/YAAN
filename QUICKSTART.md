# YAAN Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Python Dependencies

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

**Note:** First run will download AI models (~500MB-2GB depending on configuration).

### Step 2: Configure YAAN (Optional)

```bash
# Set your name
$env:YAAN_USER_NAME="Yash"

# Or edit backend/core/config.py
```

### Step 3: Start Backend Server

```bash
cd backend
python main.py
```

You should see:
```
╔═══════════════════════════════════════════╗
║   ██╗   ██╗ █████╗  █████╗ ███╗   ██╗   ║
║   YAAN - Your AI Assistant Network        ║
╚═══════════════════════════════════════════╝

Server running on http://127.0.0.1:8000
```

### Step 4: Launch Desktop Client (Optional)

**Prerequisites:**
- Java 17+
- JavaFX 17+

```bash
cd desktop

# Windows:
.\build.ps1
.\run.ps1

# Or compile manually:
javac -d bin src/*.java
java -cp bin YAANClient
```

### Step 5: Test YAAN

Open your browser: http://localhost:8000

Or use the desktop client to chat with YAAN!

**Try these commands:**
- "Hello YAAN"
- "What time is it?"
- "How's my system?"
- "Help"

## 🎤 Voice Mode (Coming Soon)

Voice features require additional setup:
- Microphone access
- ~2GB for Whisper model download

## 📱 Mobile Apps (Roadmap)

Mobile clients for Android and iOS are planned for future releases.

## 🔧 Troubleshooting

### Port 8000 Already in Use
```bash
# Change port in backend/core/config.py
server.port = 8001
```

### AI Models Not Downloading
```bash
# Manually download and place in models/ directory
# Check https://huggingface.co for model downloads
```

### Can't Connect Desktop Client
- Ensure backend is running first
- Check firewall settings
- Verify WebSocket connection to ws://localhost:8000/ws

## 📚 Documentation

See [README.md](README.md) for full documentation.

## 🤝 Need Help?

Check the logs in `backend/logs/` for detailed error messages.

---

**Happy coding with YAAN! 🚀**

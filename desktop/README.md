# YAAN Desktop - v2.0 (Electron)

**Status:** 🚀 v2.0 Development  
**Platform:** Electron + React  
**Target:** Windows & macOS  

---

## 🎯 v2.0 Migration

We're migrating from Java/JavaFX to **Electron + React** for v2.0:

### Why Electron?
- ✅ Single codebase for Windows & macOS
- ✅ Reuse existing web UI (HTML/CSS/JS)
- ✅ Better system integration
- ✅ Easier to maintain
- ✅ Modern development workflow
- ✅ Used by VS Code, Slack, Discord

### Migration Plan
1. Initialize Electron project
2. Port existing UI to React
3. Add desktop-specific features
4. Create installers

---

## 🚀 Quick Start (v2.0)

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+ (for backend)

### Initialize Project (First Time)

```bash
# Initialize npm
npm init -y

# Install Electron
npm install --save-dev electron electron-builder

# Install React
npm install react react-dom

# Install other dependencies
npm install electron-store axios socket.io-client
```

### Development

```bash
# Run in development mode
npm start

# Build for Windows
npm run build:win

# Build for macOS
npm run build:mac
```

---

## 📦 Features (v2.0 Roadmap)

**Windows-Specific:**
- ✅ System tray integration
- ✅ Start with Windows
- ✅ NSIS installer
- ✅ Windows notifications
- ✅ Jump list

**macOS-Specific:**
- ✅ Menu bar app
- ✅ Touch Bar support
- ✅ DMG installer
- ✅ Spotlight integration

**Both Platforms:**
- ✅ Global shortcuts (Ctrl/Cmd+Shift+Y)
- ✅ Auto-updates
- ✅ Native file dialogs
- ✅ Embedded Python backend
- ✅ Offline mode

---

## 🏗️ Project Structure (v2.0)

```
desktop/
├── package.json          # NEW: npm configuration
├── main.js              # NEW: Electron main process
├── preload.js           # NEW: Bridge script
├── renderer/            # NEW: React UI
│   ├── src/
│   ├── components/
│   └── App.jsx
├── assets/              # Icons & images
│   ├── icon.png
│   ├── icon.ico         # Windows
│   └── icon.icns        # macOS
├── build/               # Build outputs
└── src/                 # OLD: Java code (archived)
```

---

## 🔧 Tech Stack

**v2.0:**
- Electron 28+
- React 18
- Socket.IO Client
- Electron Store

**Backend:**
- FastAPI (shared with web)
- SQLite

---

## 📝 Development Status

**v1.0:** Java/JavaFX (archived)  
**v2.0:** Electron + React (in development)  
**Target Release:** April 2026

---

## 🎯 Next Steps

1. [ ] Create package.json
2. [ ] Set up Electron main process
3. [ ] Port UI to React
4. [ ] Test Python backend embedding
5. [ ] Add system tray
6. [ ] Create installers
7. [ ] Test on Windows & macOS

---

## 📚 Resources

- [NATIVE_APPS_PLAN.md](../NATIVE_APPS_PLAN.md) - Complete implementation guide
- [Electron Docs](https://www.electronjs.org/docs/latest/)
- [React Docs](https://react.dev/)

---

**Note:** Java/JavaFX code is archived in `src/` folder for reference.

## Usage
1. Start the YAAN backend server first
2. Launch the desktop client
3. It will automatically connect to localhost:8000
4. Start chatting with YAAN!

# YAAN v2.0 - Native App Development Plan

**Version:** 2.0.0  
**Status:** 🚀 Development Phase  
**Target Platforms:** Windows, macOS, Android, iOS  
**Target Release:** May 1, 2026

---

## 🎯 Vision

Transform YAAN into a **cross-platform native application** available on all major platforms:
- 🪟 **Windows** - Desktop app with system tray integration
- 🍎 **macOS** - Native Mac app with Touch Bar support
- 🤖 **Android** - Mobile app with Material Design
- 📱 **iOS** - iPhone/iPad app with native iOS design

---

## 🏗️ Architecture Decision

### Technology Stack

We'll use a **hybrid approach** for maximum efficiency:

#### Desktop Apps (Windows + macOS)
**Technology:** Electron + React  
**Why:**
- ✅ Single codebase for both Windows and macOS
- ✅ Native system integration (notifications, tray, shortcuts)
- ✅ Same web UI with enhanced desktop features
- ✅ Fast development (reuse existing HTML/CSS/JS)
- ✅ Auto-updates built-in
- ✅ Used by: VS Code, Slack, Discord, Spotify

**Alternative Considered:** Tauri (smaller, Rust-based)
- Pros: 10x smaller app size, faster
- Cons: Less mature ecosystem, steeper learning curve

#### Mobile Apps (Android + iOS)
**Technology:** React Native  
**Why:**
- ✅ Single codebase for both platforms
- ✅ True native performance and feel
- ✅ Access to device APIs (camera, notifications, biometrics)
- ✅ Can reuse business logic from web version
- ✅ Large community and libraries
- ✅ Used by: Facebook, Instagram, Discord, Shopify

**Alternative Considered:** Flutter
- Pros: Excellent performance, beautiful UI
- Cons: Dart language (new learning curve), less JavaScript ecosystem

#### Backend
**Technology:** FastAPI (existing)  
**Architecture:**
- Desktop: Embedded Python server OR connect to remote server
- Mobile: Connect to desktop server (WiFi) or cloud-optional

---

## 📁 Project Structure

```
YaanProject/
├── backend/                    # Existing FastAPI backend (shared)
│   ├── main.py
│   ├── nlp/
│   ├── user/
│   └── data/
│
├── desktop/                    # NEW: Electron desktop app
│   ├── package.json
│   ├── main.js                # Electron main process
│   ├── preload.js            # Bridge script
│   ├── renderer/             # React UI
│   │   ├── src/
│   │   ├── components/
│   │   └── App.jsx
│   ├── build/                # Build output
│   └── installer/            # Platform installers
│
├── mobile/                     # NEW: React Native mobile app
│   ├── package.json
│   ├── App.tsx
│   ├── android/              # Android native code
│   ├── ios/                  # iOS native code
│   ├── src/
│   │   ├── screens/
│   │   ├── components/
│   │   ├── navigation/
│   │   └── services/
│   └── assets/
│
├── shared/                     # NEW: Shared code (TypeScript)
│   ├── api/                  # API client
│   ├── types/                # TypeScript types
│   ├── utils/                # Utilities
│   └── constants/
│
├── docs/                       # Documentation
├── media/                      # Screenshots, videos
└── README.md
```

---

## 🪟 Desktop App (Electron) - Implementation

### Phase 1: Setup (Week 1)

**Install Dependencies:**
```bash
cd YaanProject
mkdir desktop
cd desktop

npm init -y
npm install electron electron-builder
npm install react react-dom
npm install electron-store  # For settings
npm install axios socket.io-client  # API communication
```

**Create Electron Main Process (`main.js`):**
```javascript
const { app, BrowserWindow, Tray, Menu, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let tray;
let pythonProcess;

// Start Python backend
function startBackend() {
    const pythonPath = path.join(__dirname, '../backend/venv/Scripts/python.exe');
    const mainPy = path.join(__dirname, '../backend/main.py');
    
    pythonProcess = spawn(pythonPath, [mainPy]);
    
    pythonProcess.stdout.on('data', (data) => {
        console.log(`Backend: ${data}`);
    });
}

// Create main window
function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        minWidth: 800,
        minHeight: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js')
        },
        icon: path.join(__dirname, 'assets/icon.png'),
        titleBarStyle: 'hiddenInset',  // macOS
        frame: true,
        backgroundColor: '#0a0a0a'
    });

    // Load local backend
    mainWindow.loadURL('http://localhost:8000');
    
    // System tray
    createTray();
    
    // Handle window close
    mainWindow.on('close', (event) => {
        if (!app.isQuitting) {
            event.preventDefault();
            mainWindow.hide();
        }
    });
}

// System tray integration
function createTray() {
    tray = new Tray(path.join(__dirname, 'assets/tray.png'));
    
    const contextMenu = Menu.buildFromTemplate([
        { label: 'Show YAAN', click: () => mainWindow.show() },
        { label: 'Hide', click: () => mainWindow.hide() },
        { type: 'separator' },
        { label: 'Quit', click: () => {
            app.isQuitting = true;
            app.quit();
        }}
    ]);
    
    tray.setContextMenu(contextMenu);
    tray.setToolTip('YAAN - Your AI Assistant');
    
    tray.on('click', () => {
        mainWindow.isVisible() ? mainWindow.hide() : mainWindow.show();
    });
}

// App lifecycle
app.whenReady().then(() => {
    startBackend();
    setTimeout(createWindow, 2000);  // Wait for backend startup
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('before-quit', () => {
    if (pythonProcess) {
        pythonProcess.kill();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

// Global shortcuts
app.whenReady().then(() => {
    const { globalShortcut } = require('electron');
    
    // Ctrl+Shift+Y to toggle YAAN
    globalShortcut.register('CommandOrControl+Shift+Y', () => {
        mainWindow.isVisible() ? mainWindow.hide() : mainWindow.show();
    });
});
```

**Package.json Scripts:**
```json
{
  "name": "yaan-desktop",
  "version": "2.0.0",
  "main": "main.js",
  "scripts": {
    "start": "electron .",
    "build": "electron-builder",
    "build:win": "electron-builder --win",
    "build:mac": "electron-builder --mac",
    "build:linux": "electron-builder --linux"
  },
  "build": {
    "appId": "com.yaan.assistant",
    "productName": "YAAN",
    "directories": {
      "output": "dist"
    },
    "files": [
      "**/*",
      "../backend/**/*",
      "!**/node_modules/*/{CHANGELOG.md,README.md}"
    ],
    "win": {
      "target": ["nsis", "portable"],
      "icon": "assets/icon.ico"
    },
    "mac": {
      "target": ["dmg", "zip"],
      "icon": "assets/icon.icns",
      "category": "public.app-category.productivity"
    },
    "nsis": {
      "oneClick": false,
      "allowToChangeInstallationDirectory": true,
      "createDesktopShortcut": true,
      "createStartMenuShortcut": true
    }
  }
}
```

### Desktop Features

**Windows-Specific:**
- ✅ System tray integration
- ✅ Start with Windows (startup registry)
- ✅ NSIS installer with custom UI
- ✅ Windows notifications
- ✅ Jump list with recent tasks

**macOS-Specific:**
- ✅ Menu bar app
- ✅ Touch Bar support (Mac Pro)
- ✅ DMG installer with custom background
- ✅ Native notifications
- ✅ Spotlight integration
- ✅ File draganddrop support

**Both Platforms:**
- ✅ Global keyboard shortcuts (Ctrl/Cmd+Shift+Y)
- ✅ Offline mode with local database
- ✅ Auto-updates
- ✅ Native file dialogs
- ✅ Deep linking (yaan:// protocol)

---

## 📱 Mobile App (React Native) - Implementation

### Phase 2: Setup (Week 2-3)

**Initialize React Native:**
```bash
cd YaanProject
npx react-native init YAANMobile --template react-native-template-typescript
cd YAANMobile
mv * ../mobile/
cd ..
rmdir YAANMobile
cd mobile
```

**Install Dependencies:**
```bash
npm install @react-navigation/native @react-navigation/stack
npm install react-native-screens react-native-safe-area-context
npm install axios socket.io-client
npm install react-native-gesture-handler react-native-reanimated
npm install @react-native-async-storage/async-storage
npm install react-native-push-notification
npm install react-native-biometrics
npm install react-native-qrcode-scanner
npm install react-native-voice  # For voice input
```

**App.tsx Structure:**
```typescript
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'react-native';

// Screens
import HomeScreen from './src/screens/HomeScreen';
import ChatScreen from './src/screens/ChatScreen';
import SettingsScreen from './src/screens/SettingsScreen';
import PairDeviceScreen from './src/screens/PairDeviceScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar barStyle="light-content" backgroundColor="#0a0a0a" />
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerStyle: {
            backgroundColor: '#0a0a0a',
          },
          headerTintColor: '#fff',
          cardStyle: { backgroundColor: '#0a0a0a' },
        }}
      >
        <Stack.Screen 
          name="Home" 
          component={HomeScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen 
          name="Chat" 
          component={ChatScreen}
          options={{ title: 'YAAN' }}
        />
        <Stack.Screen 
          name="Settings" 
          component={SettingsScreen} 
        />
        <Stack.Screen 
          name="PairDevice" 
          component={PairDeviceScreen}
          options={{ title: 'Pair Desktop' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

**API Service (`src/services/api.ts`):**
```typescript
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { io, Socket } from 'socket.io-client';

class YAANService {
  private baseURL: string = '';
  private socket: Socket | null = null;
  
  async setServer(url: string) {
    this.baseURL = url;
    await AsyncStorage.setItem('server_url', url);
    this.connect();
  }
  
  async loadServer() {
    const url = await AsyncStorage.getItem('server_url');
    if (url) {
      this.baseURL = url;
      this.connect();
    }
  }
  
  connect() {
    if (this.socket) {
      this.socket.disconnect();
    }
    
    this.socket = io(this.baseURL);
    
    this.socket.on('connect', () => {
      console.log('Connected to YAAN server');
    });
    
    this.socket.on('response', (data) => {
      // Handle real-time responses
    });
  }
  
  async sendMessage(message: string) {
    if (!this.socket) {
      throw new Error('Not connected to server');
    }
    
    this.socket.emit('message', { text: message });
  }
  
  async getServerInfo(ip: string) {
    const response = await axios.get(`http://${ip}:8000/api/server-info`);
    return response.data;
  }
}

export default new YAANService();
```

### Mobile Features

**Android-Specific:**
- ✅ Material Design 3 UI
- ✅ Android widgets (home screen)
- ✅ Quick Settings tile
- ✅ Firebase Cloud Messaging
- ✅ App shortcuts
- ✅ Picture-in-Picture mode

**iOS-Specific:**
- ✅ Native iOS design with SF Symbols
- ✅ Widgets (home screen, lock screen)
- ✅ Siri Shortcuts integration
- ✅ Apple Push Notifications
- ✅ Face ID / Touch ID authentication
- ✅ 3D Touch/Haptic Touch

**Both Platforms:**
- ✅ QR code scanning for device pairing
- ✅ Voice input with native APIs
- ✅ Push notifications for reminders
- ✅ Offline mode with local caching
- ✅ Biometric authentication (optional)
- ✅ Dark/Light theme
- ✅ Swipe gestures
- ✅ Share extension

---

## 🔄 Development Workflow

### Week 1-2: Desktop Foundation
- [ ] Set up Electron project
- [ ] Integrate existing web UI
- [ ] Add system tray
- [ ] Test Python backend embedding
- [ ] Create Windows installer
- [ ] Create macOS DMG

### Week 3-4: Desktop Features
- [ ] Global shortcuts
- [ ] Auto-updates
- [ ] Notifications
- [ ] File handling
- [ ] Platform-specific features
- [ ] Testing on both platforms

### Week 5-6: Mobile Foundation
- [ ] Set up React Native project
- [ ] Create navigation structure
- [ ] Build chat UI
- [ ] Implement API service
- [ ] QR code pairing
- [ ] Test on Android/iOS

### Week 7-8: Mobile Features
- [ ] Voice input
- [ ] Push notifications
- [ ] Offline mode
- [ ] Biometric auth
- [ ] Widgets
- [ ] Platform-specific features

### Week 9: Testing & Polish
- [ ] Cross-platform testing
- [ ] UI/UX refinements
- [ ] Performance optimization
- [ ] Bug fixes
- [ ] Beta testing

### Week 10: Release
- [ ] App store submissions
- [ ] Final documentation
- [ ] Marketing materials
- [ ] Launch! 🚀

---

## 📦 Distribution

### Desktop Apps

**Windows:**
- NSIS installer (.exe)
- Portable version (.exe)
- Microsoft Store (optional)
- Auto-updates via GitHub Releases

**macOS:**
- DMG installer
- ZIP archive
- Mac App Store (optional)
- Homebrew cask (optional)
- Auto-updates via GitHub Releases

### Mobile Apps

**Android:**
- Google Play Store
- APK direct download
- F-Droid (optional)
- Samsung Galaxy Store (optional)

**iOS:**
- Apple App Store
- TestFlight for beta testing
- (No sideloading for non-developers)

---

## 💰 Cost Considerations

### Development
- ✅ All tools are free (Electron, React Native)
- ✅ No licensing fees

### Distribution
- 🆓 Windows: Free
- 🆓 macOS: Free (self-distribution)
- 💵 Mac App Store: $99/year (Apple Developer)
- 💵 Google Play Store: $25 one-time
- 💵 Apple App Store: $99/year

**Total First Year:** $224 (if publishing to all stores)

---

## 📊 App Sizes (Estimated)

- **Desktop (Windows):** ~150-200 MB (includes Python runtime)
- **Desktop (macOS):** ~150-200 MB
- **Mobile (Android):** ~30-50 MB
- **Mobile (iOS):** ~30-50 MB

---

## 🎯 Success Metrics

- ✅ Windows app: 500+ downloads in month 1
- ✅ macOS app: 200+ downloads in month 1
- ✅ Android app: 1000+ installs in month 1
- ✅ iOS app: 500+ installs in month 1
- ✅ 4.5+ star rating on all platforms
- ✅ <5% crash rate
- ✅ <100ms response time

---

## 🚀 Quick Start Commands

### Desktop Development
```bash
cd desktop
npm install
npm start           # Run in development
npm run build:win   # Build Windows installer
npm run build:mac   # Build macOS DMG
```

### Mobile Development
```bash
cd mobile
npm install
npx react-native run-android   # Run on Android
npx react-native run-ios        # Run on iOS
```

---

**Status:** 🚀 Ready to start!  
**Timeline:** 10 weeks  
**Next Step:** Create desktop folder and initialize Electron

Let's build YAAN for everyone, everywhere! 🌍

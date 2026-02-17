# YAAN Mobile - v2.0 (React Native)

**Status:** 🚀 v2.0 Development  
**Platform:** React Native  
**Target:** Android & iOS  

---

## 🎯 v2.0 Launch

We're building **native mobile apps** for Android and iOS using React Native!

### Why React Native?
- ✅ Single codebase for both platforms
- ✅ True native performance
- ✅ Fast development (reuse logic from web)
- ✅ Large ecosystem & community
- ✅ Used by Facebook, Instagram, Discord

---

## 🚀 Quick Start (v2.0)

### Prerequisites
- Node.js 18+
- React Native CLI
- **Android:**  Android Studio, JDK 11+
- **iOS:** Xcode 14+ (macOS only)

### Initialize Project (First Time)

```bash
# Install React Native CLI
npm install -g react-native-cli

# Create project (done once)
npx react-native init YAANMobile --template react-native-template-typescript

# Install dependencies
npm install @react-navigation/native @react-navigation/stack
npm install react-native-screens react-native-safe-area-context
npm install axios socket.io-client
npm install @react-native-async-storage/async-storage
npm install react-native-qrcode-scanner
npm install react-native-voice
```

### Development

```bash
# Run on Android
npx react-native run-android

# Run on iOS (macOS only)
npx react-native run-ios

# Start Metro bundler
npx react-native start
```

---

## 📱 Features (v2.0 Roadmap)

### Android-Specific
- ✅ Material Design 3 UI
- ✅ Home screen widgets
- ✅ Quick Settings tile
- ✅ Firebase Cloud Messaging
- ✅ App shortcuts
- ✅ Picture-in-Picture

### iOS-Specific
- ✅ Native iOS design
- ✅ Widgets (home/lock screen)
- ✅ Siri Shortcuts
- ✅ Push Notifications
- ✅ Face ID / Touch ID
- ✅ Haptic feedback

### Cross-Platform
- ✅ QR code pairing with desktop
- ✅ Voice input
- ✅ Push notifications for reminders
- ✅ Offline mode
- ✅ Biometric authentication
- ✅ Dark/Light theme
- ✅ Swipe gestures
- ✅ Share extension

---

## 🏗️ Project Structure (v2.0)

```
mobile/
├── package.json
├── App.tsx                  # Main app entry
├── android/                 # Android native code
├── ios/                     # iOS native code
├── src/
│   ├── screens/            # App screens
│   │   ├── HomeScreen.tsx
│   │   ├── ChatScreen.tsx
│   │   ├── SettingsScreen.tsx
│   │   └── PairDeviceScreen.tsx
│   ├── components/         # Reusable components
│   ├── navigation/         # Navigation setup
│   ├── services/          # API & services
│   │   └── YAANService.ts
│   ├── types/             # TypeScript types
│   └── utils/             # Utilities
├── assets/                 # Images, fonts
└── __tests__/             # Tests
```

---

## 🔧 Tech Stack

- React Native 0.73+
- TypeScript
- React Navigation
- Socket.IO Client
- Async Storage
- React Native Voice

**Backend:**
- FastAPI (shared)
- WebSocket protocol

---

## 📝 Development Status

**Current:** Planning  
**Target Release:** May 2026  
**Version:** 2.0.0-alpha

---

## 🎯 Development Phases

### Phase 1: Foundation (Week 5)
- [ ] Initialize React Native project
- [ ] Set up navigation
- [ ] Create basic UI screens
- [ ] Implement API service

### Phase 2: Core Features (Week 6)
- [ ] Chat interface
- [ ] QR code pairing
- [ ] WebSocket connection
- [ ] Voice input

### Phase 3: Native Features (Week 7)
- [ ] Push notifications
- [ ] Biometric auth
- [ ] Offline mode
- [ ] Platform-specific features

### Phase 4: Polish (Week 8)
- [ ] UI/UX refinements
- [ ] Performance optimization
- [ ] Testing on real devices
- [ ] Bug fixes

---

## 🌐 Communication Flow

```
Mobile App
    ↓↑ (WebSocket)
Desktop Server (same WiFi)
    ↓↑
SQLite Database
```

**Pairing Process:**
1. Desktop shows QR code with server IP
2. Mobile scans QR code
3. Auto-connects to `http://192.168.1.x:8000`
4. Real-time sync begins!

---

## 📚 Resources

- [NATIVE_APPS_PLAN.md](../NATIVE_APPS_PLAN.md) - Complete implementation guide
- [React Native Docs](https://reactnative.dev/docs/getting-started)
- [React Navigation](https://reactnavigation.org/)

---

## 🔥 Next Steps

1. [ ] Set up development environment
2. [ ] Initialize React Native project
3. [ ] Create navigation structure
4. [ ] Build chat UI
5. [ ] Implement QR pairing
6. [ ] Test on Android & iOS

---

**Previous Plan:** Native Kotlin/Swift (archived)  
**Current Plan:** React Native (v2.0)  
**Status:** Ready to build! 🎉

## File Structure (Future)

```
mobile/
├── android/           # Android-specific code
│   ├── app/
│   └── build.gradle
├── ios/              # iOS-specific code
│   ├── YaanApp/
│   └── Podfile
├── shared/           # Shared code
│   ├── models/
│   └── services/
└── README.md
```

## Contributing

If you're interested in contributing to mobile development, please:
1. Ensure the backend is stable first
2. Follow the WebSocket API contract
3. Maintain privacy-first principles
4. Test thoroughly on both platforms

---

**Status:** Planning Phase  
**Updated:** February 2026

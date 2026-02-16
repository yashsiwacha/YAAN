# YAAN Mobile Apps

## Planned Features

### Android App
- Native Android client
- Voice integration with Android speech APIs
- Material Design UI
- Background service for always-on listening
- Widget support

### iOS App
- Native iOS client
- Siri integration
- iOS design guidelines
- Background audio processing
- Widget support

## Technology Stack (Planned)

### Option 1: React Native
- Single codebase for both platforms
- Fast development
- Good community support

### Option 2: Flutter
- Excellent performance
- Beautiful UI
- Strong typing with Dart

### Option 3: Native Development
- Kotlin for Android
- Swift for iOS
- Best performance
- Platform-specific features

## Development Priority

Mobile apps are scheduled for **Phase 4** of development, after:
1. ✅ Core backend (Phase 1)
2. ⏳ AI intelligence improvements (Phase 2)
3. ⏳ Automation features (Phase 3)
4. 📱 Mobile apps (Phase 4)

## Communication Protocol

Mobile apps will use the same WebSocket protocol as the desktop client:
- Connect to YAAN backend via WebSocket
- Send/receive JSON messages
- Real-time bidirectional communication

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

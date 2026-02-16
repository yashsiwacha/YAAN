# YAAN Desktop Client

Java-based cross-platform desktop client for YAAN.

## Requirements
- Java 17 or higher
- JavaFX 17+

## Setup

### Windows
```bash
# Install JavaFX (if not included in your JDK)
# Download from https://gluonhq.com/products/javafx/

# Compile
javac --module-path "C:\path\to\javafx-sdk\lib" --add-modules javafx.controls,javafx.fxml -d bin src/*.java

# Run
java --module-path "C:\path\to\javafx-sdk\lib" --add-modules javafx.controls,javafx.fxml -cp bin YAANClient
```

### macOS
```bash
# Install JavaFX
brew install openjdk@17
# Download JavaFX from https://gluonhq.com/products/javafx/

# Compile
javac --module-path /path/to/javafx-sdk/lib --add-modules javafx.controls,javafx.fxml -d bin src/*.java

# Run
java --module-path /path/to/javafx-sdk/lib --add-modules javafx.controls,javafx.fxml -cp bin YAANClient
```

## Dependencies

Add to your project:
- JavaFX 17+
- org.json (for JSON parsing)

You can download `json-20230227.jar` from Maven:
https://repo1.maven.org/maven2/org/json/json/20230227/json-20230227.jar

## Features
- Real-time WebSocket connection to backend
- Chat interface
- Voice input (coming soon)
- Cross-platform (Windows, Mac, Linux)
- Modern dark theme UI

## Usage
1. Start the YAAN backend server first
2. Launch the desktop client
3. It will automatically connect to localhost:8000
4. Start chatting with YAAN!

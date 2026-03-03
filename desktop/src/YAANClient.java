import java.util.Scanner;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

/**
 * YAAN Desktop Client (console fallback)
 * This version avoids JavaFX runtime requirements.
 */
public class YAANClient {

    private WebSocketClient wsClient;
    private boolean isConnected = false;

    public void start() {
        appendMessage("System", "Welcome to YAAN! Connecting to server...");
        connectToBackend();
        runInputLoop();
    }

    private void connectToBackend() {
        try {
            String serverUrl = "ws://localhost:8000/ws";
            wsClient = new WebSocketClient(serverUrl, this);
            wsClient.connect();
        } catch (Exception e) {
            appendMessage("System", "Failed to connect to backend: " + e.getMessage());
            updateStatus("Offline");
        }
    }

    private void sendMessage(String text) {
        if (text == null || text.trim().isEmpty() || !isConnected) {
            return;
        }

        String command = text.trim();
        appendMessage("You", command);
        wsClient.sendCommand(command);
    }

    private void runInputLoop() {
        try (Scanner scanner = new Scanner(System.in)) {
            appendMessage("System", "Type your message and press Enter. Type /exit to quit.");
            while (true) {
                String input = scanner.nextLine();
                if ("/exit".equalsIgnoreCase(input.trim())) {
                    close();
                    break;
                }
                sendMessage(input);
            }
        }
    }

    public void appendMessage(String sender, String message) {
        String timestamp = LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm:ss"));
        System.out.println(String.format("[%s] %s: %s", timestamp, sender, message));
    }

    public void onConnected() {
        isConnected = true;
        updateStatus("Online");
        appendMessage("System", "Connected to YAAN backend successfully!");
    }

    public void onDisconnected() {
        isConnected = false;
        updateStatus("Offline");
        appendMessage("System", "Disconnected from backend.");
    }

    public void onMessage(String message) {
        appendMessage("YAAN", message);
    }

    public void onError(String error) {
        appendMessage("Error", error);
    }

    private void updateStatus(String text) {
        appendMessage("Status", text);
    }

    public void close() {
        if (wsClient != null) {
            wsClient.close();
        }
    }

    public static void main(String[] args) {
        new YAANClient().start();
    }
}

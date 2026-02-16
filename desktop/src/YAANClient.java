import javafx.application.Application;
import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.stage.Stage;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

/**
 * YAAN Desktop Client
 * Cross-platform desktop interface for Your AI Assistant Network
 */
public class YAANClient extends Application {
    
    private TextArea chatArea;
    private TextField inputField;
    private Button sendButton;
    private Button voiceButton;
    private Label statusLabel;
    private WebSocketClient wsClient;
    private boolean isConnected = false;
    
    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("YAAN - Your AI Assistant");
        
        // Create UI components
        BorderPane root = new BorderPane();
        root.setStyle("-fx-background-color: #1e1e1e;");
        
        // Top bar with title and status
        HBox topBar = createTopBar();
        root.setTop(topBar);
        
        // Center - Chat area
        chatArea = new TextArea();
        chatArea.setEditable(false);
        chatArea.setWrapText(true);
        chatArea.setStyle(
            "-fx-control-inner-background: #2d2d2d; " +
            "-fx-text-fill: #ffffff; " +
            "-fx-font-size: 14px; " +
            "-fx-font-family: 'Consolas', 'Courier New', monospace;"
        );
        chatArea.setText("Welcome to YAAN!\nConnecting to server...\n\n");
        
        ScrollPane scrollPane = new ScrollPane(chatArea);
        scrollPane.setFitToWidth(true);
        scrollPane.setFitToHeight(true);
        root.setCenter(scrollPane);
        
        // Bottom - Input area
        HBox inputArea = createInputArea();
        root.setBottom(inputArea);
        
        // Create scene
        Scene scene = new Scene(root, 800, 600);
        primaryStage.setScene(scene);
        primaryStage.show();
        
        // Connect to backend
        connectToBackend();
        
        // Handle window close
        primaryStage.setOnCloseRequest(e -> {
            if (wsClient != null) {
                wsClient.close();
            }
            Platform.exit();
        });
    }
    
    private HBox createTopBar() {
        HBox topBar = new HBox(10);
        topBar.setPadding(new Insets(10));
        topBar.setStyle("-fx-background-color: #0078d4;");
        topBar.setAlignment(Pos.CENTER_LEFT);
        
        Label titleLabel = new Label("YAAN");
        titleLabel.setFont(Font.font("Arial", 24));
        titleLabel.setTextFill(Color.WHITE);
        
        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        
        statusLabel = new Label("● Connecting...");
        statusLabel.setTextFill(Color.YELLOW);
        statusLabel.setFont(Font.font("Arial", 12));
        
        topBar.getChildren().addAll(titleLabel, spacer, statusLabel);
        return topBar;
    }
    
    private HBox createInputArea() {
        HBox inputArea = new HBox(10);
        inputArea.setPadding(new Insets(10));
        inputArea.setStyle("-fx-background-color: #2d2d2d;");
        
        inputField = new TextField();
        inputField.setPromptText("Type your message or command...");
        inputField.setStyle(
            "-fx-background-color: #3d3d3d; " +
            "-fx-text-fill: #ffffff; " +
            "-fx-prompt-text-fill: #888888; " +
            "-fx-font-size: 14px;"
        );
        HBox.setHgrow(inputField, Priority.ALWAYS);
        
        // Send button
        sendButton = new Button("Send");
        sendButton.setStyle(
            "-fx-background-color: #0078d4; " +
            "-fx-text-fill: white; " +
            "-fx-font-size: 14px;"
        );
        sendButton.setDisable(true);
        
        // Voice button
        voiceButton = new Button("🎤 Voice");
        voiceButton.setStyle(
            "-fx-background-color: #107c10; " +
            "-fx-text-fill: white; " +
            "-fx-font-size: 14px;"
        );
        voiceButton.setDisable(true);
        
        // Event handlers
        sendButton.setOnAction(e -> sendMessage());
        inputField.setOnAction(e -> sendMessage());
        voiceButton.setOnAction(e -> startVoiceInput());
        
        inputArea.getChildren().addAll(inputField, voiceButton, sendButton);
        return inputArea;
    }
    
    private void connectToBackend() {
        try {
            String serverUrl = "ws://localhost:8000/ws";
            wsClient = new WebSocketClient(serverUrl, this);
            wsClient.connect();
        } catch (Exception e) {
            appendMessage("System", "Failed to connect to backend: " + e.getMessage());
            updateStatus("● Offline", Color.RED);
        }
    }
    
    private void sendMessage() {
        String text = inputField.getText().trim();
        if (text.isEmpty() || !isConnected) {
            return;
        }
        
        // Display user message
        appendMessage("You", text);
        
        // Send to backend
        wsClient.sendCommand(text);
        
        // Clear input
        inputField.clear();
    }
    
    private void startVoiceInput() {
        appendMessage("System", "Voice input feature coming soon!");
    }
    
    public void appendMessage(String sender, String message) {
        Platform.runLater(() -> {
            String timestamp = LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm:ss"));
            chatArea.appendText(String.format("[%s] %s: %s\n\n", timestamp, sender, message));
        });
    }
    
    public void onConnected() {
        Platform.runLater(() -> {
            isConnected = true;
            updateStatus("● Online", Color.GREEN);
            sendButton.setDisable(false);
            voiceButton.setDisable(false);
            appendMessage("System", "Connected to YAAN backend successfully!");
        });
    }
    
    public void onDisconnected() {
        Platform.runLater(() -> {
            isConnected = false;
            updateStatus("● Offline", Color.RED);
            sendButton.setDisable(true);
            voiceButton.setDisable(true);
            appendMessage("System", "Disconnected from backend.");
        });
    }
    
    public void onMessage(String message) {
        appendMessage("YAAN", message);
    }
    
    public void onError(String error) {
        appendMessage("Error", error);
    }
    
    private void updateStatus(String text, Color color) {
        Platform.runLater(() -> {
            statusLabel.setText(text);
            statusLabel.setTextFill(color);
        });
    }
    
    public static void main(String[] args) {
        launch(args);
    }
}

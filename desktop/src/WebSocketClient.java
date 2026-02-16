import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.WebSocket;
import java.nio.ByteBuffer;
import java.util.concurrent.CompletionStage;
import org.json.JSONObject;

/**
 * WebSocket client for YAAN backend communication
 */
public class WebSocketClient implements WebSocket.Listener {
    
    private WebSocket webSocket;
    private String serverUrl;
    private YAANClient client;
    private StringBuilder messageBuilder;
    
    public WebSocketClient(String serverUrl, YAANClient client) {
        this.serverUrl = serverUrl;
        this.client = client;
        this.messageBuilder = new StringBuilder();
    }
    
    public void connect() {
        try {
            HttpClient httpClient = HttpClient.newHttpClient();
            webSocket = httpClient.newWebSocketBuilder()
                .buildAsync(URI.create(serverUrl), this)
                .join();
        } catch (Exception e) {
            client.onError("Connection failed: " + e.getMessage());
        }
    }
    
    @Override
    public void onOpen(WebSocket webSocket) {
        client.onConnected();
        webSocket.request(1);
    }
    
    @Override
    public CompletionStage<?> onText(WebSocket webSocket, CharSequence data, boolean last) {
        messageBuilder.append(data);
        
        if (last) {
            String message = messageBuilder.toString();
            messageBuilder.setLength(0);
            
            try {
                JSONObject json = new JSONObject(message);
                String type = json.getString("type");
                
                if (type.equals("welcome") || type.equals("response")) {
                    String text = json.optString("message", json.optString("text", ""));
                    client.onMessage(text);
                }
            } catch (Exception e) {
                client.onError("Failed to parse message: " + e.getMessage());
            }
        }
        
        webSocket.request(1);
        return null;
    }
    
    @Override
    public CompletionStage<?> onClose(WebSocket webSocket, int statusCode, String reason) {
        client.onDisconnected();
        return null;
    }
    
    @Override
    public void onError(WebSocket webSocket, Throwable error) {
        client.onError("WebSocket error: " + error.getMessage());
    }
    
    public void sendCommand(String text) {
        if (webSocket != null) {
            try {
                JSONObject json = new JSONObject();
                json.put("type", "command");
                json.put("text", text);
                webSocket.sendText(json.toString(), true);
            } catch (Exception e) {
                client.onError("Failed to send message: " + e.getMessage());
            }
        }
    }
    
    public void close() {
        if (webSocket != null) {
            webSocket.sendClose(WebSocket.NORMAL_CLOSURE, "Client closing");
        }
    }
}

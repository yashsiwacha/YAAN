import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.WebSocket;
import java.util.concurrent.CompletionStage;

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
                String type = extractJsonString(message, "type");
                
                if ("welcome".equals(type) || "response".equals(type)) {
                    String text = extractJsonString(message, "message");
                    if (text == null || text.isEmpty()) {
                        text = extractJsonString(message, "text");
                    }
                    client.onMessage(text == null ? "" : text);
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
                String payload = "{\"type\":\"command\",\"text\":\"" + escapeJson(text) + "\"}";
                webSocket.sendText(payload, true);
            } catch (Exception e) {
                client.onError("Failed to send message: " + e.getMessage());
            }
        }
    }

    private String extractJsonString(String json, String key) {
        if (json == null || key == null) {
            return null;
        }

        String token = "\"" + key + "\"";
        int keyIndex = json.indexOf(token);
        if (keyIndex < 0) {
            return null;
        }

        int colonIndex = json.indexOf(':', keyIndex + token.length());
        if (colonIndex < 0) {
            return null;
        }

        int startQuote = json.indexOf('"', colonIndex + 1);
        if (startQuote < 0) {
            return null;
        }

        StringBuilder out = new StringBuilder();
        boolean escaped = false;
        for (int i = startQuote + 1; i < json.length(); i++) {
            char c = json.charAt(i);
            if (escaped) {
                switch (c) {
                    case '"':
                        out.append('"');
                        break;
                    case '\\':
                        out.append('\\');
                        break;
                    case '/':
                        out.append('/');
                        break;
                    case 'b':
                        out.append('\b');
                        break;
                    case 'f':
                        out.append('\f');
                        break;
                    case 'n':
                        out.append('\n');
                        break;
                    case 'r':
                        out.append('\r');
                        break;
                    case 't':
                        out.append('\t');
                        break;
                    default:
                        out.append(c);
                        break;
                }
                escaped = false;
            } else if (c == '\\') {
                escaped = true;
            } else if (c == '"') {
                return out.toString();
            } else {
                out.append(c);
            }
        }

        return null;
    }

    private String escapeJson(String value) {
        if (value == null) {
            return "";
        }

        return value
            .replace("\\", "\\\\")
            .replace("\"", "\\\"")
            .replace("\b", "\\b")
            .replace("\f", "\\f")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t");
    }
    
    public void close() {
        if (webSocket != null) {
            webSocket.sendClose(WebSocket.NORMAL_CLOSURE, "Client closing");
        }
    }
}

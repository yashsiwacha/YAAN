# Multi-Device Sync - Implementation Guide

## 🎯 Goal
Enable YAAN to sync across multiple devices (phone, laptop, tablet) on the same WiFi network with real-time updates.

## ✅ Current Architecture Advantages
YAAN is already 90% ready for this feature:
- ✅ SQLite databases (easily shared)
- ✅ WebSocket for real-time communication
- ✅ FastAPI backend
- ✅ No cloud dependencies

## 🔧 Implementation Steps

### 1. Change Server Binding (5 minutes)

**File:** `backend/main.py`

```python
# Current
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

# Change to
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

**What this does:**
- `127.0.0.1` = localhost only (current)
- `0.0.0.0` = all network interfaces (allows LAN access)

### 2. Display Server IP on UI (15 minutes)

**Add to backend API:**

```python
import socket

@app.get("/api/server-info")
async def get_server_info():
    """Get server IP address for device pairing"""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return {
        "ip": local_ip,
        "port": 8000,
        "url": f"http://{local_ip}:8000"
    }
```

**Add to UI (index.html):**

```html
<!-- Add to header -->
<div class="server-info" id="serverInfo">
    🌐 Server: <span id="serverIp">Loading...</span>
    <button onclick="copyServerUrl()">Copy URL</button>
</div>
```

```javascript
// Fetch and display server info
async function loadServerInfo() {
    const response = await fetch('/api/server-info');
    const data = await response.json();
    document.getElementById('serverIp').textContent = data.url;
}

function copyServerUrl() {
    const url = document.getElementById('serverIp').textContent;
    navigator.clipboard.writeText(url);
    showToast('Server URL copied!');
}
```

### 3. Test Multi-Device Access

**On Desktop:**
1. Start YAAN: `python main.py`
2. Note the IP shown in UI, e.g., `http://192.168.1.100:8000`

**On Mobile/Tablet:**
1. Connect to same WiFi
2. Open browser
3. Navigate to `http://192.168.1.100:8000`
4. Everything syncs automatically via shared SQLite!

## 🎨 QR Code Pairing (Optional Enhancement)

**Install QR code library:**
```bash
pip install qrcode[pil]
```

**Add endpoint:**
```python
import qrcode
import io
from fastapi.responses import StreamingResponse

@app.get("/api/qr-code")
async def generate_qr():
    """Generate QR code for easy mobile pairing"""
    local_ip = socket.gethostbyname(socket.gethostname())
    url = f"http://{local_ip}:8000"
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    return StreamingResponse(buf, media_type="image/png")
```

**Display in UI:**
```html
<div class="qr-pairing">
    <h3>Pair Mobile Device</h3>
    <img src="/api/qr-code" alt="Scan to connect" />
    <p>Scan with your phone to connect</p>
</div>
```

## 🔒 Security (Optional)

### Add PIN Protection

**Database:**
```sql
CREATE TABLE devices (
    id TEXT PRIMARY KEY,
    device_name TEXT,
    device_type TEXT,
    authorized BOOLEAN DEFAULT FALSE,
    pin_hash TEXT,
    last_seen TIMESTAMP
);
```

**Authentication:**
```python
import hashlib

def verify_pin(pin: str, stored_hash: str) -> bool:
    return hashlib.sha256(pin.encode()).hexdigest() == stored_hash

@app.post("/api/authorize-device")
async def authorize_device(device_id: str, pin: str):
    # Check PIN
    if not verify_pin(pin, get_stored_pin_hash()):
        raise HTTPException(401, "Invalid PIN")
    
    # Register device
    register_device(device_id)
    return {"status": "authorized"}
```

## 🌐 Network Discovery (Advanced)

### Using mDNS/Bonjour

**Install:**
```bash
pip install zeroconf
```

**Implement:**
```python
from zeroconf import ServiceInfo, Zeroconf
import socket

def register_service():
    """Register YAAN service for automatic discovery"""
    zeroconf = Zeroconf()
    ip = socket.inet_aton(socket.gethostbyname(socket.gethostname()))
    
    info = ServiceInfo(
        "_yaan._tcp.local.",
        "YAAN Assistant._yaan._tcp.local.",
        addresses=[ip],
        port=8000,
        properties={'version': '2.0'},
    )
    
    zeroconf.register_service(info)
    return zeroconf

# Start on server startup
zeroconf = register_service()
```

**Client Discovery:**
```javascript
// Mobile devices can discover YAAN automatically
// Without typing IP address
```

## 💡 How Sync Works

### Real-Time Sync Flow:

1. **Device A** connects to server via WebSocket
2. **Device B** connects to same server
3. Both use same SQLite databases
4. Any change broadcasts via WebSocket to all connected devices

**Example:**
```python
# In WebSocket handler
async def broadcast_update(message: dict):
    """Send update to all connected clients"""
    for connection in active_connections:
        await connection.send_json(message)

# When reminder is added
@app.post("/api/reminders")
async def add_reminder(reminder: Reminder):
    # Save to database
    save_reminder(reminder)
    
    # Broadcast to all devices
    await broadcast_update({
        "type": "reminder_added",
        "data": reminder.dict()
    })
```

## 📱 Mobile-Friendly Enhancements

### Add to index.html:
```html
<!-- Add manifest for PWA -->
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#667eea">
<meta name="apple-mobile-web-app-capable" content="yes">
```

### Create manifest.json:
```json
{
  "name": "YAAN Assistant",
  "short_name": "YAAN",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0a0a0a",
  "theme_color": "#667eea",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```

## 🧪 Testing Multi-Device Sync

### Test Checklist:
- [ ] Open YAAN on desktop
- [ ] Note the server IP
- [ ] Open same URL on phone
- [ ] Send message from phone → appears on desktop
- [ ] Add reminder on desktop → appears on phone
- [ ] Check memory sync
- [ ] Test with 3+ devices simultaneously
- [ ] Verify offline behavior
- [ ] Test reconnection after WiFi drop

## 📊 Benefits of This Implementation

✅ **Zero Configuration** - Works out of the box  
✅ **Complete Privacy** - No cloud, no external services  
✅ **Real-Time** - Instant sync via WebSocket  
✅ **No Additional Cost** - No server hosting fees  
✅ **Fast** - Local network = millisecond latency  
✅ **Secure** - Local WiFi only, optional PIN  
✅ **Offline Support** - Works when one device is offline  

## 🚀 Quick Start (for v2.0)

**Phase 1: Basic (Week 6, Day 1-2)**
- Change server binding to 0.0.0.0
- Add server IP display
- Test multi-device access

**Phase 2: QR Pairing (Week 6, Day 3)**
- Generate QR codes
- Add pairing UI
- Mobile testing

**Phase 3: Security (Week 7, Day 1-2)**
- Implement PIN protection
- Device authorization
- Security testing

**Phase 4: Polish (Week 7, Day 3)**
- Network status indicators
- Connection error handling
- UI improvements

## 🎯 v1.0 → v2.0 Changes Summary

```diff
# backend/main.py
- uvicorn.run("main:app", host="127.0.0.1", port=8000)
+ uvicorn.run("main:app", host="0.0.0.0", port=8000)

# New endpoints
+ /api/server-info
+ /api/qr-code
+ /api/authorize-device (optional)
+ /api/connected-devices

# UI additions
+ Server IP display
+ QR code modal
+ Device list in settings
+ Connection status indicator
```

## 📝 Notes

- **Firewall:** May need to allow port 8000
- **Router:** Most routers allow LAN access by default
- **Mobile Data:** Won't work (same WiFi required)
- **VPN:** May interfere with local network access
- **Performance:** No impact, same as single device

---

**Status:** Planned for v2.0  
**Estimated Time:** 8-12 hours (basic), 15-20 hours (with security)  
**Complexity:** Medium  
**Impact:** High - Game changing feature!

🎉 **Users can work seamlessly across all their devices!**

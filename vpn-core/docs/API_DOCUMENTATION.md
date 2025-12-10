# Nova-Link VPN Core API Documentation
**Member 1 Deliverable - Version 1.0**

## 🌐 Base URL
```
http://localhost:5000/api
```

## 📡 ENDPOINTS FOR MEMBER 2 (CLIENT APP)

### 1. Health Check
**GET** `/api/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "Nova-Link VPN Core API",
  "version": "1.0.0"
}
```

---

### 2. Get Server Information
**GET** `/api/server/info`

**Response:**
```json
{
  "server_public_key": "AedoWdmMIyWIwivBwoRL9475+2FQHmOOE/ksoJJGyGA=",
  "server_ip": "10.8.0.1",
  "server_port": 51820,
  "endpoint": "YOUR_SERVER_IP:51820"
}
```

**Usage for Member 2:**
- Use `server_public_key` to configure client connection
- Display `server_ip` and `server_port` in the UI

---

### 3. Register New Client
**POST** `/api/client/register`

**Request Body:**
```json
{
  "client_id": "user_123",
  "client_name": "John Doe"
}
```

**Response:**
```json
{
  "success": true,
  "client_id": "user_123",
  "ip_address": "10.8.0.2",
  "public_key": "CLIENT_PUBLIC_KEY_BASE64",
  "config_file": "path/to/config.conf"
}
```

**Usage for Member 2:**
- Call this when user first connects to VPN
- Store the `ip_address` and `public_key` for the user
- Use returned config to establish connection

---

### 4. Start VPN Tunnel
**POST** `/api/tunnel/start`

**Response:**
```json
{
  "success": true,
  "message": "VPN tunnel started successfully"
}
```

---

### 5. Stop VPN Tunnel
**POST** `/api/tunnel/stop`

**Response:**
```json
{
  "success": true,
  "message": "VPN tunnel stopped successfully"
}
```

---

### 6. Get Tunnel Status
**GET** `/api/tunnel/status`

**Response:**
```json
{
  "tunnel": {
    "status": "active",
    "active_peers": 2,
    "started_at": "2024-12-03T11:42:25.336",
    "details": "Tunnel is active with 2 connected peer(s)"
  },
  "ip_pool": {
    "total_ips": 253,
    "allocated": 2,
    "available": 251,
    "utilization": "0.8%"
  },
  "peers": [...],
  "server_public_key": "..."
}
```

**Usage for Member 2:**
- Use this to show connection status in UI
- Display number of active peers
- Show IP pool utilization

---

### 7. Unregister Client
**POST** `/api/client/unregister`

**Request Body:**
```json
{
  "client_id": "user_123"
}
```

**Response:**
```json
{
  "success": true
}
```

---

## 📡 ENDPOINTS FOR MEMBER 4 (BACKEND)

### 1. Allocate IP Address
**POST** `/api/ip/allocate`

**Request Body:**
```json
{
  "client_id": "user_456",
  "client_name": "Jane Smith"
}
```

**Response:**
```json
{
  "success": true,
  "client_id": "user_456",
  "ip_address": "10.8.0.3"
}
```

**Usage for Member 4:**
- Call this when a new user registers in your system
- Store the allocated IP in your database

---

### 2. Release IP Address
**POST** `/api/ip/release`

**Request Body:**
```json
{
  "client_id": "user_456"
}
```

---

### 3. List All IP Allocations
**GET** `/api/ip/list`

**Response:**
```json
{
  "allocations": [
    {
      "client_id": "user_123",
      "client_name": "John Doe",
      "ip_address": "10.8.0.2",
      "allocated_at": "2024-12-03T10:30:00",
      "status": "active"
    }
  ],
  "count": 1
}
```

---

### 4. Get IP Statistics
**GET** `/api/ip/stats`

**Response:**
```json
{
  "total_ips": 253,
  "allocated": 5,
  "available": 248,
  "utilization": "2.0%"
}
```

---

### 5. Add Peer to VPN
**POST** `/api/peer/add`

**Request Body:**
```json
{
  "client_id": "user_123",
  "public_key": "CLIENT_PUBLIC_KEY",
  "allowed_ip": "10.8.0.2/32"
}
```

---

### 6. Remove Peer from VPN
**POST** `/api/peer/remove`

**Request Body:**
```json
{
  "client_id": "user_123"
}
```

---

### 7. List Active Peers
**GET** `/api/peer/list`

**Response:**
```json
{
  "peers": [
    {
      "client_id": "user_123",
      "public_key": "...",
      "allowed_ip": "10.8.0.2/32",
      "added_at": "2024-12-03T10:30:00",
      "status": "active"
    }
  ],
  "count": 1
}
```

---

## 📡 ENDPOINTS FOR MEMBER 3 (SECURITY)

### Get Server Public Key
The server public key is available via:
1. **API:** `GET /api/server/info`
2. **File:** `vpn-core/keys/server_public.key`

Use this key for certificate generation and security configuration.

---

## 🔧 ERROR RESPONSES

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": "Error message here"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (missing parameters)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error

---

## 🧪 TESTING EXAMPLES

### Using cURL:
```bash
# Health check
curl http://localhost:5000/api/health

# Register client
curl -X POST http://localhost:5000/api/client/register \
  -H "Content-Type: application/json" \
  -d '{"client_id":"test_user","client_name":"Test User"}'
```

### Using Python:
```python
import requests

# Register client
response = requests.post('http://localhost:5000/api/client/register', 
    json={'client_id': 'user_123', 'client_name': 'John Doe'})
print(response.json())
```

### Using JavaScript (for Member 2):
```javascript
// Register client
const response = await fetch('http://localhost:5000/api/client/register', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        client_id: 'user_123',
        client_name: 'John Doe'
    })
});
const data = await response.json();
console.log(data);
```

---

## 📞 SUPPORT
For questions or issues, contact Member 1 or check the main project repository.
```

---
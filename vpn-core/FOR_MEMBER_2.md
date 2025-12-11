# Integration Guide for Member 2 (Client App)

## Quick Start

**API Base URL:** `http://localhost:5000/api`

## Essential Endpoints

### 1. Register New Client (When user first connects)
```javascript
const response = await fetch('http://localhost:5000/api/client/register', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        client_id: userId,      // Unique user ID from your app
        client_name: userName   // User's display name
    })
});
const data = await response.json();
// data.ip_address = "10.8.0.2"
// data.public_key = "user's public key"
```

### 2. Start VPN Connection
```javascript
const response = await fetch('http://localhost:5000/api/tunnel/start', {
    method: 'POST'
});
```

### 3. Check Connection Status (Update UI)
```javascript
const response = await fetch('http://localhost:5000/api/tunnel/status');
const status = await response.json();
// status.tunnel.status = "active"
// status.tunnel.active_peers = 2
```

### 4. Stop VPN Connection
```javascript
const response = await fetch('http://localhost:5000/api/tunnel/stop', {
    method: 'POST'
});
```

## Testing Your Integration

1. Start my API: `python -m api.app` in vpn-core folder
2. Your app calls the endpoints above
3. Check responses in browser DevTools

## Questions?
Contact me: [Your contact info]
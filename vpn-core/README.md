# Nova-Link VPN Core (Member 1)

## 🎯 Overview
This is the **VPN Core** component of the Nova-Link VPN project, responsible for:
- Setting up VPN software
- Handling connections
- Managing IP addresses

## 📁 Project Structure
```
vpn-core/
├── src/                    # Core Python modules
│   ├── vpn_server.py      # Main VPN server
│   ├── tunnel_manager.py  # Connection handler
│   ├── ip_allocator.py    # IP management
│   ├── peer_config.py     # Client config generator
│   └── utils.py           # Utility functions
├── api/                    # REST API
│   └── app.py             # Flask API server
├── config/                 # Configuration files
├── keys/                   # Cryptographic keys
├── logs/                   # Server logs
└── tests/                  # Unit tests
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run VPN Server (Standalone)
```bash
python src/vpn_server.py
```

### 3. Run API Server
```bash
python api/app.py
```

## 📡 API Endpoints

### Health Check
```
GET /api/health
```

### Server Info
```
GET /api/server/info
```

### Tunnel Control
```
POST /api/tunnel/start
POST /api/tunnel/stop
GET  /api/tunnel/status
```

### Client Management
```
POST /api/client/register
POST /api/client/unregister
```

### IP Management
```
POST /api/ip/allocate
POST /api/ip/release
GET  /api/ip/list
GET  /api/ip/stats
```

### Peer Management
```
POST /api/peer/add
POST /api/peer/remove
GET  /api/peer/list
```

## 🔧 Configuration

Edit `config/server_config.yaml` to customize:
- Server IP and port
- IP address pool
- DNS servers
- Security settings

## 🧪 Testing

Run unit tests:
```bash
python -m pytest tests/ -v
```

Test specific module:
```bash
python tests/test_ip_allocator.py
```

## 📚 Integration Guide

### For Member 2 (Client App)
Use these endpoints to connect:
- `POST /api/client/register` - Register new client
- `POST /api/tunnel/start` - Start VPN connection
- `GET /api/tunnel/status` - Check connection status

### For Member 3 (Security)
- Server public key: `keys/server_public.key`
- Use this key for certificate generation

### For Member 4 (Backend)
- `POST /api/ip/allocate` - When user registers
- `POST /api/peer/add` - To authorize connections
- `GET /api/ip/stats` - For monitoring

## 📝 Development Notes

This is a **Windows-compatible** VPN core using pure Python.
For production deployment, consider:
- Using actual WireGuard on Linux server
- Implementing proper authentication
- Adding rate limiting
- Setting up SSL/TLS for API

## 🐛 Troubleshooting

### API won't start
```bash
# Check if port 5000 is available
netstat -ano | findstr :5000
```

### Database errors
```bash
# Delete and recreate databases
del config\ip_pool.json
del config\peers.json
python src/vpn_server.py
```

## 📞 Support

For issues or questions, contact the team or check the main project documentation.
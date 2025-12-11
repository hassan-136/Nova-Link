"""
VPN Core API - Flask REST API
Exposes VPN Core functionality to other team members
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.vpn_server import VPNServer
from src.utils import setup_logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for Member 2's client app

# Initialize VPN Server
vpn_server = VPNServer()

# Setup logging
logger = setup_logging('../logs/api_server.log')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Nova-Link VPN Core API',
        'version': '1.0.0'
    })


@app.route('/api/server/info', methods=['GET'])
def server_info():
    """Get server information"""
    return jsonify({
        'server_public_key': vpn_server.server_keys['public_key'],
        'server_ip': '10.8.0.1',
        'server_port': 51820,
        'endpoint': 'YOUR_SERVER_IP:51820'
    })


@app.route('/api/tunnel/start', methods=['POST'])
def start_tunnel():
    """Start VPN tunnel"""
    logger.info("API: Starting tunnel...")

    success = vpn_server.start()

    if success:
        return jsonify({
            'success': True,
            'message': 'VPN tunnel started successfully'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Failed to start VPN tunnel'
        }), 500


@app.route('/api/tunnel/stop', methods=['POST'])
def stop_tunnel():
    """Stop VPN tunnel"""
    logger.info("API: Stopping tunnel...")

    success = vpn_server.stop()

    if success:
        return jsonify({
            'success': True,
            'message': 'VPN tunnel stopped successfully'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Failed to stop VPN tunnel'
        }), 500


@app.route('/api/tunnel/status', methods=['GET'])
def tunnel_status():
    """Get tunnel status"""
    status = vpn_server.get_status()
    return jsonify(status)


@app.route('/api/client/register', methods=['POST'])
def register_client():
    """Register a new VPN client"""
    data = request.json

    client_id = data.get('client_id')
    client_name = data.get('client_name', 'VPN Client')

    if not client_id:
        return jsonify({
            'success': False,
            'error': 'client_id is required'
        }), 400

    logger.info(f"API: Registering client {client_id}")

    result = vpn_server.register_client(client_id, client_name)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 500


@app.route('/api/client/unregister', methods=['POST'])
def unregister_client():
    """Unregister a VPN client"""
    data = request.json
    client_id = data.get('client_id')

    if not client_id:
        return jsonify({
            'success': False,
            'error': 'client_id is required'
        }), 400

    logger.info(f"API: Unregistering client {client_id}")

    result = vpn_server.unregister_client(client_id)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 500


@app.route('/api/ip/allocate', methods=['POST'])
def allocate_ip():
    """Allocate IP address for a client"""
    data = request.json
    client_id = data.get('client_id')
    client_name = data.get('client_name', 'Unknown')

    if not client_id:
        return jsonify({
            'success': False,
            'error': 'client_id is required'
        }), 400

    try:
        ip = vpn_server.ip_allocator.allocate_ip(client_id, client_name)
        return jsonify({
            'success': True,
            'client_id': client_id,
            'ip_address': ip
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ip/release', methods=['POST'])
def release_ip():
    """Release IP address"""
    data = request.json
    client_id = data.get('client_id')

    if not client_id:
        return jsonify({
            'success': False,
            'error': 'client_id is required'
        }), 400

    success = vpn_server.ip_allocator.release_ip(client_id)

    if success:
        return jsonify({
            'success': True,
            'message': f'IP released for client {client_id}'
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Client not found'
        }), 404


@app.route('/api/ip/list', methods=['GET'])
def list_ips():
    """List all IP allocations"""
    allocations = vpn_server.ip_allocator.list_allocations()
    return jsonify({
        'allocations': allocations,
        'count': len(allocations)
    })


@app.route('/api/ip/stats', methods=['GET'])
def ip_stats():
    """Get IP allocation statistics"""
    stats = vpn_server.ip_allocator.get_stats()
    return jsonify(stats)


@app.route('/api/peer/add', methods=['POST'])
def add_peer():
    """Add a peer to the VPN"""
    data = request.json

    client_id = data.get('client_id')
    public_key = data.get('public_key')
    allowed_ip = data.get('allowed_ip')

    if not all([client_id, public_key, allowed_ip]):
        return jsonify({
            'success': False,
            'error': 'client_id, public_key, and allowed_ip are required'
        }), 400

    success = vpn_server.tunnel_manager.add_peer(client_id, public_key, allowed_ip)

    if success:
        return jsonify({
            'success': True,
            'message': f'Peer {client_id} added successfully'
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to add peer'
        }), 500


@app.route('/api/peer/remove', methods=['POST'])
def remove_peer():
    """Remove a peer from the VPN"""
    data = request.json
    client_id = data.get('client_id')

    if not client_id:
        return jsonify({
            'success': False,
            'error': 'client_id is required'
        }), 400

    success = vpn_server.tunnel_manager.remove_peer(client_id)

    if success:
        return jsonify({
            'success': True,
            'message': f'Peer {client_id} removed successfully'
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to remove peer'
        }), 500


@app.route('/api/peer/list', methods=['GET'])
def list_peers():
    """List all active peers"""
    peers = vpn_server.tunnel_manager.list_peers()
    return jsonify({
        'peers': peers,
        'count': len(peers)
    })


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 NOVA-LINK VPN CORE API SERVER")
    print("=" * 60)
    print(f"📍 Running on: http://localhost:5000")
    print(f"📚 API Documentation: http://localhost:5000/api/health")
    print("=" * 60 + "\n")

    # Start the VPN server
    vpn_server.start()

    # Run Flask API
    app.run(host='0.0.0.0', port=5000, debug=True)
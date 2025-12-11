"""
VPN Tunnel Manager
Handles VPN tunnel lifecycle and peer connections
"""
import os
import logging
from datetime import datetime
from .utils import load_json, save_json, get_timestamp

logger = logging.getLogger(__name__)


class TunnelManager:
    def __init__(self, config_dir='../config'):
        """Initialize Tunnel Manager"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_dir = os.path.join(base_dir, config_dir)
        self.peers_file = os.path.join(self.config_dir, 'peers.json')

        # Create config directory
        os.makedirs(self.config_dir, exist_ok=True)

        # Load or initialize peers
        self.peers = load_json(self.peers_file)
        if not self.peers:
            self.peers = {'active_peers': [], 'tunnel_status': 'inactive'}
            self._save_peers()

        logger.info("TunnelManager initialized")

    def _save_peers(self):
        """Save peers configuration"""
        save_json(self.peers_file, self.peers)

    def start_tunnel(self):
        """Start VPN tunnel"""
        try:
            self.peers['tunnel_status'] = 'active'
            self.peers['started_at'] = get_timestamp()
            self._save_peers()

            logger.info("✅ VPN tunnel started successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to start tunnel: {e}")
            return False

    def stop_tunnel(self):
        """Stop VPN tunnel"""
        try:
            self.peers['tunnel_status'] = 'inactive'
            self.peers['stopped_at'] = get_timestamp()
            self._save_peers()

            logger.info("✅ VPN tunnel stopped successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to stop tunnel: {e}")
            return False

    def get_status(self):
        """Get current tunnel status"""
        status = self.peers.get('tunnel_status', 'inactive')
        active_peers = len(self.peers.get('active_peers', []))

        return {
            'status': status,
            'active_peers': active_peers,
            'started_at': self.peers.get('started_at', 'N/A'),
            'details': f"Tunnel is {status} with {active_peers} connected peer(s)"
        }

    def add_peer(self, client_id, public_key, allowed_ip):
        """Add a new peer to the tunnel"""
        try:
            peer = {
                'client_id': client_id,
                'public_key': public_key,
                'allowed_ip': allowed_ip,
                'added_at': get_timestamp(),
                'status': 'active'
            }

            if 'active_peers' not in self.peers:
                self.peers['active_peers'] = []

            self.peers['active_peers'].append(peer)
            self._save_peers()

            logger.info(f"✅ Added peer: {client_id} ({allowed_ip})")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to add peer: {e}")
            return False

    def remove_peer(self, client_id):
        """Remove a peer from the tunnel"""
        try:
            if 'active_peers' not in self.peers:
                return False

            self.peers['active_peers'] = [
                p for p in self.peers['active_peers']
                if p['client_id'] != client_id
            ]
            self._save_peers()

            logger.info(f"✅ Removed peer: {client_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to remove peer: {e}")
            return False

    def get_peer(self, client_id):
        """Get peer information"""
        if 'active_peers' not in self.peers:
            return None

        for peer in self.peers['active_peers']:
            if peer['client_id'] == client_id:
                return peer

        return None

    def list_peers(self):
        """List all active peers"""
        return self.peers.get('active_peers', [])


# Test the tunnel manager
if __name__ == '__main__':
    from .utils import setup_logging

    setup_logging('../logs/vpn_server.log')

    manager = TunnelManager()

    print("🧪 Testing Tunnel Manager...")

    # Start tunnel
    manager.start_tunnel()
    status = manager.get_status()
    print(f"Status: {status}")

    # Add peer
    manager.add_peer('client_001', 'dummy_public_key_123', '10.8.0.2/32')

    # List peers
    print("\n📋 Active Peers:")
    for peer in manager.list_peers():
        print(f"  {peer['client_id']}: {peer['allowed_ip']}")

    # Stop tunnel
    manager.stop_tunnel()
    print(f"Final status: {manager.get_status()}")
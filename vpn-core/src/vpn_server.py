"""
VPN Server - Main orchestrator
Coordinates all VPN Core components
"""
import os
import logging
from .utils import generate_keypair, setup_logging, save_json, load_json
from .ip_allocator import IPAllocator
from .tunnel_manager import TunnelManager
from .peer_config import PeerConfigGenerator


class VPNServer:
    def __init__(self):
        """Initialize VPN Server"""
        # Setup logging
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_file = os.path.join(base_dir, '../logs/vpn_server.log')
        self.logger = setup_logging(log_file)

        self.logger.info("=" * 50)
        self.logger.info("🚀 Nova-Link VPN Server Starting...")
        self.logger.info("=" * 50)

        # Initialize components
        self.ip_allocator = IPAllocator()
        self.tunnel_manager = TunnelManager()

        # Setup server keys
        self.keys_dir = os.path.join(base_dir, '../keys')
        os.makedirs(self.keys_dir, exist_ok=True)

        self.server_keys = self._load_or_generate_server_keys()
        self.peer_config_gen = PeerConfigGenerator(
            server_public_key=self.server_keys['public_key']
        )

        self.logger.info("✅ VPN Server initialized successfully")

    def _load_or_generate_server_keys(self):
        """Load existing server keys or generate new ones"""
        keys_file = os.path.join(self.keys_dir, 'server_keys.json')

        if os.path.exists(keys_file):
            self.logger.info("📂 Loading existing server keys...")
            return load_json(keys_file)
        else:
            self.logger.info("🔑 Generating new server keys...")
            private_key, public_key = generate_keypair()

            keys = {
                'private_key': private_key,
                'public_key': public_key
            }

            save_json(keys_file, keys)

            # Also save individual key files
            with open(os.path.join(self.keys_dir, 'server_private.key'), 'w') as f:
                f.write(private_key)
            with open(os.path.join(self.keys_dir, 'server_public.key'), 'w') as f:
                f.write(public_key)

            self.logger.info(f"✅ Server Public Key: {public_key}")
            return keys

    def register_client(self, client_id, client_name='VPN Client'):
        """Register a new VPN client"""
        try:
            self.logger.info(f"📝 Registering client: {client_id}")

            # Allocate IP address
            client_ip = self.ip_allocator.allocate_ip(client_id, client_name)
            self.logger.info(f"✅ Allocated IP: {client_ip}")

            # Generate client configuration
            config = self.peer_config_gen.generate_client_config(
                client_id, client_ip, client_name
            )

            # Add peer to tunnel
            self.tunnel_manager.add_peer(
                client_id,
                config['public_key'],
                f"{client_ip}/32"
            )

            self.logger.info(f"✅ Client {client_id} registered successfully")

            return {
                'success': True,
                'client_id': client_id,
                'ip_address': client_ip,
                'public_key': config['public_key'],
                'config_file': config['config_file']
            }

        except Exception as e:
            self.logger.error(f"❌ Failed to register client: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def unregister_client(self, client_id):
        """Unregister a VPN client"""
        try:
            self.logger.info(f"🗑️ Unregistering client: {client_id}")

            # Remove from tunnel
            self.tunnel_manager.remove_peer(client_id)

            # Release IP
            self.ip_allocator.release_ip(client_id)

            self.logger.info(f"✅ Client {client_id} unregistered successfully")
            return {'success': True}

        except Exception as e:
            self.logger.error(f"❌ Failed to unregister client: {e}")
            return {'success': False, 'error': str(e)}

    def start(self):
        """Start VPN server"""
        self.logger.info("▶️ Starting VPN tunnel...")
        success = self.tunnel_manager.start_tunnel()

        if success:
            self.logger.info("✅ VPN Server is running!")
        else:
            self.logger.error("❌ Failed to start VPN Server")

        return success

    def stop(self):
        """Stop VPN server"""
        self.logger.info("⏹️ Stopping VPN tunnel...")
        success = self.tunnel_manager.stop_tunnel()

        if success:
            self.logger.info("✅ VPN Server stopped")
        else:
            self.logger.error("❌ Failed to stop VPN Server")

        return success

    def get_status(self):
        """Get server status"""
        tunnel_status = self.tunnel_manager.get_status()
        ip_stats = self.ip_allocator.get_stats()
        peers = self.tunnel_manager.list_peers()

        return {
            'tunnel': tunnel_status,
            'ip_pool': ip_stats,
            'peers': peers,
            'server_public_key': self.server_keys['public_key']
        }


# Main execution
if __name__ == '__main__':
    server = VPNServer()

    print("\n" + "=" * 50)
    print("🧪 TESTING VPN SERVER")
    print("=" * 50 + "\n")

    # Start server
    print("1️⃣ Starting VPN Server...")
    server.start()

    # Register clients
    print("\n2️⃣ Registering clients...")
    result1 = server.register_client('client_001', 'Test Client 1')
    print(f"   Client 1 IP: {result1.get('ip_address')}")

    result2 = server.register_client('client_002', 'Test Client 2')
    print(f"   Client 2 IP: {result2.get('ip_address')}")

    # Get status
    print("\n3️⃣ Server Status:")
    status = server.get_status()
    print(f"   Tunnel Status: {status['tunnel']['status']}")
    print(f"   Active Peers: {status['tunnel']['active_peers']}")
    print(f"   IP Utilization: {status['ip_pool']['utilization']}")

    # Stop server
    print("\n4️⃣ Stopping VPN Server...")
    server.stop()

    print("\n✅ All tests completed!\n")
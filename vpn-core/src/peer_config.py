"""
Peer Configuration Generator
Generates WireGuard configuration files for clients
"""
import os
from .utils import generate_keypair, get_timestamp, save_json, load_json


class PeerConfigGenerator:
    def __init__(self, keys_dir='../keys', server_public_key=None):
        """Initialize peer configuration generator"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.keys_dir = os.path.join(base_dir, keys_dir)
        self.clients_dir = os.path.join(self.keys_dir, 'clients')

        # Create directories
        os.makedirs(self.keys_dir, exist_ok=True)
        os.makedirs(self.clients_dir, exist_ok=True)

        # Server configuration
        self.server_endpoint = "YOUR_SERVER_IP:51820"  # Will be configured
        self.server_public_key = server_public_key
        self.server_ip = "10.8.0.1"

    def generate_client_config(self, client_id, client_ip, client_name='VPN Client'):
        """Generate configuration file for a client"""
        # Generate client keys
        private_key, public_key = generate_keypair()

        # Save client keys
        client_key_file = os.path.join(self.clients_dir, f'{client_id}_keys.json')
        save_json(client_key_file, {
            'client_id': client_id,
            'client_name': client_name,
            'private_key': private_key,
            'public_key': public_key,
            'client_ip': client_ip,
            'generated_at': get_timestamp()
        })

        # Generate WireGuard config file
        config_content = f"""[Interface]
# Client: {client_name}
PrivateKey = {private_key}
Address = {client_ip}/24
DNS = 8.8.8.8, 8.8.4.4

[Peer]
# Server
PublicKey = {self.server_public_key or 'SERVER_PUBLIC_KEY_HERE'}
Endpoint = {self.server_endpoint}
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
"""

        # Save config file
        config_file = os.path.join(self.clients_dir, f'{client_id}.conf')
        with open(config_file, 'w') as f:
            f.write(config_content)

        return {
            'client_id': client_id,
            'private_key': private_key,
            'public_key': public_key,
            'config_file': config_file,
            'config_content': config_content
        }

    def get_client_public_key(self, client_id):
        """Get client's public key"""
        client_key_file = os.path.join(self.clients_dir, f'{client_id}_keys.json')
        keys = load_json(client_key_file)
        return keys.get('public_key') if keys else None


# Test the config generator
if __name__ == '__main__':
    generator = PeerConfigGenerator(server_public_key='EXAMPLE_SERVER_PUBLIC_KEY')

    print("🧪 Testing Peer Config Generator...")

    # Generate config for a client
    config = generator.generate_client_config(
        client_id='client_001',
        client_ip='10.8.0.2',
        client_name='Test Client'
    )

    print(f"✅ Generated config for {config['client_id']}")
    print(f"Public Key: {config['public_key'][:20]}...")
    print(f"Config file: {config['config_file']}")
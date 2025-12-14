"""
Utility functions for VPN Core
"""
import os
import json
import yaml
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization
import base64


def generate_keypair():
    """Generate WireGuard-style public/private keypair"""
    private_key = x25519.X25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Serialize keys to base64 (WireGuard format)
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    private_key_b64 = base64.b64encode(private_bytes).decode('utf-8')
    public_key_b64 = base64.b64encode(public_bytes).decode('utf-8')

    return private_key_b64, public_key_b64


def load_config(config_path):
    """Load YAML configuration file"""
    if not os.path.exists(config_path):
        return {}

    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def save_config(config_path, data):
    """Save data to YAML configuration file"""
    os.makedirs(os.path.dirname(config_path), exist_ok=True)

    with open(config_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)


def load_json(file_path):
    """Load JSON file"""
    if not os.path.exists(file_path):
        return {}

    with open(file_path, 'r') as f:
        return json.load(f)


def save_json(file_path, data):
    """Save data to JSON file"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def get_timestamp():
    """Get current timestamp"""
    return datetime.now().isoformat()


def setup_logging(log_file):
    """Setup logging configuration with UTF-8 support"""
    import logging
    import sys
    import io
    import os

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Force UTF-8 encoding for Windows console safely
    if sys.platform == 'win32':
        if not isinstance(sys.stdout, io.TextIOWrapper):
            sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
        if not isinstance(sys.stderr, io.TextIOWrapper):
            sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    return logging.getLogger(__name__)

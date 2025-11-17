#!/usr/bin/env python3
"""
VPN Client Main Entry Point
Secure VPN Solution - Client
"""

import sys
import signal
import argparse
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(_file_).parent.parent.parent))

from src.client.vpn_client import VPNClient
from src.client.config import ClientConfig
from src.shared.exceptions import VPNConnectionError, ConfigError

def signal_handler(signum, frame):
    """Handle interrupt signals"""
    print("\nReceived interrupt signal. Shutting down...")
    sys.exit(0)

def setup_argparse() -> argparse.Namespace:
    """Setup command line argument parsing"""
    parser = argparse.ArgumentParser(
        description="Secure VPN Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --config config/client_config.json
  python main.py --server 192.168.1.100 --port 5555 --key "my-secret-key"
        """
    )
    
    parser.add_argument(
        '--config', 
        '-c',
        type=str,
        default='config/client_config.json',
        help='Path to configuration file (default: config/client_config.json)'
    )
    
    parser.add_argument(
        '--server',
        '-s',
        type=str,
        help='VPN server hostname or IP address'
    )
    
    parser.add_argument(
        '--port',
        '-p',
        type=int,
        help='VPN server port'
    )
    
    parser.add_argument(
        '--key',
        '-k',
        type=str,
        help='Encryption key (base64 encoded)'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--debug',
        '-d',
        action='store_true',
        help='Enable debug logging'
    )
    
    return parser.parse_args()

def main():
    """Main client application entry point"""
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Parse arguments
    args = setup_argparse()
    
    try:
        # Load configuration
        config = ClientConfig(args.config)
        
        # Override config with command line arguments
        if args.server:
            config['server_host'] = args.server
        if args.port:
            config['server_port'] = args.port
        if args.key:
            config['encryption_key'] = args.key
        
        # Setup logging level
        if args.debug:
            config['log_level'] = 'DEBUG'
        elif args.verbose:
            config['log_level'] = 'INFO'
        
        print("=" * 50)
        print("Secure VPN Client Starting...")
        print(f"Server: {config['server_host']}:{config['server_port']}")
        print(f"Tunnel Device: {config['tun_device']}")
        print(f"Client IP: {config['client_ip']}")
        print("=" * 50)
        
        # Create and start VPN client
        with VPNClient(config) as client:
            if client.connect():
                print("VPN Connection established successfully!")
                print("Press Ctrl+C to disconnect")
                
                # Keep the main thread alive
                try:
                    while client.is_connected:
                        # You could add status monitoring here
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\nDisconnecting...")
            else:
                print("Failed to establish VPN connection")
                sys.exit(1)
                
    except ConfigError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except VPNConnectionError as e:
        print(f"VPN connection error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if _name_ == '_main_':
    import time
    main()
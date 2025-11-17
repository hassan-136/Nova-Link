import socket
import time
import logging
import threading
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from src.core.tunnel import TunnelManager
from src.core.crypto import CryptoManager
from src.shared.exceptions import VPNConnectionError, VPNConfigError
from src.client.config import ClientConfig

class VPNClient:
    """Main VPN Client class that manages the VPN connection"""
    
    def _init_(self, config: ClientConfig):
        self.config = config
        self.logger = self._setup_logging()
        self.tunnel_manager: Optional[TunnelManager] = None
        self.crypto_manager: Optional[CryptoManager] = None
        self.server_socket: Optional[socket.socket] = None
        self.is_connected = False
        self._stop_event = threading.Event()
        
        self.logger.info("VPN Client initialized")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the client"""
        logger = logging.getLogger('VPNClient')
        log_level = getattr(logging, self.config['log_level'].upper())
        logger.setLevel(log_level)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def connect(self) -> bool:
        """Establish VPN connection to server"""
        attempt = 0
        max_attempts = self.config['reconnect_attempts']
        
        while attempt < max_attempts and not self._stop_event.is_set():
            try:
                self.logger.info(f"Connection attempt {attempt + 1}/{max_attempts}")
                self._establish_connection()
                self.is_connected = True
                self.logger.info("VPN connection established successfully")
                return True
                
            except (VPNConnectionError, socket.error) as e:
                attempt += 1
                self.logger.error(f"Connection failed: {e}")
                
                if attempt < max_attempts:
                    self.logger.info(f"Retrying in {self.config['reconnect_delay']} seconds...")
                    time.sleep(self.config['reconnect_delay'])
                else:
                    self.logger.error("Max connection attempts reached")
                    break
        
        return False
    
    def _establish_connection(self) -> None:
        """Establish the actual VPN connection"""
        try:
            # Initialize crypto manager
            self.crypto_manager = CryptoManager(self.config['encryption_key'])
            self.logger.debug("Crypto manager initialized")
            
            # Initialize tunnel
            self.tunnel_manager = TunnelManager(
                tun_device=self.config['tun_device'],
                local_ip=self.config['client_ip'],
                peer_ip=self.config['server_tun_ip']
            )
            self.tunnel_manager.create_tunnel()
            self.logger.debug("Tunnel interface created")
            
            # Connect to server
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.settimeout(10)  # 10 second timeout
            
            self.logger.info(f"Connecting to server {self.config['server_host']}:{self.config['server_port']}")
            self.server_socket.connect((self.config['server_host'], self.config['server_port']))
            self.logger.info("Server connection established")
            
            # Start data forwarding
            self._start_forwarding()
            
        except Exception as e:
            self.cleanup()
            raise VPNConnectionError(f"Failed to establish connection: {e}")
    
    def _start_forwarding(self) -> None:
        """Start forwarding data between tunnel and socket"""
        # Thread for reading from tunnel and sending to server
        self.tunnel_to_socket_thread = threading.Thread(
            target=self._tunnel_to_socket_loop,
            daemon=True
        )
        
        # Thread for reading from socket and sending to tunnel
        self.socket_to_tunnel_thread = threading.Thread(
            target=self._socket_to_tunnel_loop,
            daemon=True
        )
        
        self.tunnel_to_socket_thread.start()
        self.socket_to_tunnel_thread.start()
        
        self.logger.info("Data forwarding started")
    
    def _tunnel_to_socket_loop(self) -> None:
        """Read from tunnel, encrypt and send to socket"""
        while not self._stop_event.is_set() and self.is_connected:
            try:
                # Read packet from tunnel
                packet = self.tunnel_manager.read_packet()
                if packet:
                    # Encrypt packet
                    encrypted_packet = self.crypto_manager.encrypt(packet)
                    
                    # Send to server
                    self.server_socket.send(encrypted_packet)
                    self.logger.debug(f"Sent encrypted packet: {len(packet)} bytes")
                    
            except socket.error as e:
                self.logger.error(f"Socket error in tunnel-to-socket: {e}")
                break
            except Exception as e:
                self.logger.error(f"Error in tunnel-to-socket: {e}")
                if not self._stop_event.is_set():
                    break
    
    def _socket_to_tunnel_loop(self) -> None:
        """Read from socket, decrypt and send to tunnel"""
        while not self._stop_event.is_set() and self.is_connected:
            try:
                # Receive data from server
                encrypted_data = self.server_socket.recv(self.config['buffer_size'])
                if not encrypted_data:
                    self.logger.warning("Server disconnected")
                    break
                
                # Decrypt packet
                decrypted_packet = self.crypto_manager.decrypt(encrypted_data)
                
                # Write to tunnel
                self.tunnel_manager.write_packet(decrypted_packet)
                self.logger.debug(f"Received and decrypted packet: {len(decrypted_packet)} bytes")
                
            except socket.timeout:
                continue
            except socket.error as e:
                self.logger.error(f"Socket error in socket-to-tunnel: {e}")
                break
            except Exception as e:
                self.logger.error(f"Error in socket-to-tunnel: {e}")
                if not self._stop_event.is_set():
                    break
    
    def disconnect(self) -> None:
        """Disconnect from VPN server"""
        self.logger.info("Disconnecting VPN client")
        self._stop_event.set()
        self.is_connected = False
        self.cleanup()
        self.logger.info("VPN client disconnected")
    
    def cleanup(self) -> None:
        """Clean up resources"""
        try:
            if self.server_socket:
                self.server_socket.close()
                self.server_socket = None
            
            if self.tunnel_manager:
                self.tunnel_manager.cleanup()
                self.tunnel_manager = None
            
            self.crypto_manager = None
            self.logger.debug("Resources cleaned up")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current client status"""
        return {
            "connected": self.is_connected,
            "server": f"{self.config['server_host']}:{self.config['server_port']}",
            "tunnel_device": self.config['tun_device'],
            "client_ip": self.config['client_ip']
        }
    
    def _enter_(self):
        """Context manager entry"""
        return self
    
    def _exit_(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
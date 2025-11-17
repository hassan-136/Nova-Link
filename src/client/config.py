import json
import os
from typing import Dict, Any
from src.shared.exceptions import ConfigError

class ClientConfig:
    """Handles client configuration loading and validation"""
    
    DEFAULT_CONFIG = {
        "server_host": "localhost",
        "server_port": 5555,
        "tun_device": "tun0",
        "client_ip": "10.0.0.2",
        "server_tun_ip": "10.0.0.1",
        "subnet_mask": "255.255.255.0",
        "encryption_key": "",
        "log_level": "INFO",
        "buffer_size": 4096,
        "reconnect_attempts": 3,
        "reconnect_delay": 5
    }
    
    def _init_(self, config_path: str = None):
        self.config_path = config_path
        self.config_data = self.DEFAULT_CONFIG.copy()
        if config_path and os.path.exists(config_path):
            self.load_config(config_path)
        self.validate_config()
    
    def load_config(self, config_path: str) -> None:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                self.config_data.update(user_config)
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON configuration: {e}")
        except Exception as e:
            raise ConfigError(f"Failed to load config: {e}")
    
    def validate_config(self) -> None:
        """Validate configuration parameters"""
        if not self.config_data["encryption_key"]:
            raise ConfigError("Encryption key is required")
        
        if not 1 <= self.config_data["server_port"] <= 65535:
            raise ConfigError("Server port must be between 1 and 65535")
        
        if len(self.config_data["encryption_key"]) < 16:
            raise ConfigError("Encryption key must be at least 16 characters")
    
    def get(self, key: str, default=None) -> Any:
        """Get configuration value"""
        return self.config_data.get(key, default)
    
    def _getitem_(self, key: str) -> Any:
        return self.config_data[key]
    
    def _setitem_(self, key: str, value: Any) -> None:
        self.config_data[key] = value
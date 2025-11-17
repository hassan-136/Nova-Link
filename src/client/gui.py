"""
Optional GUI for VPN Client using Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import logging
from typing import Optional

from src.client.vpn_client import VPNClient
from src.client.config import ClientConfig

class VPNClientGUI:
    """Simple GUI for VPN Client"""
    
    def _init_(self, root):
        self.root = root
        self.client: Optional[VPNClient] = None
        self.config: Optional[ClientConfig] = None
        self.is_connected = False
        
        self._setup_gui()
        self._setup_logging()
    
    def _setup_gui(self):
        """Setup the GUI elements"""
        self.root.title("Secure VPN Client")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Connection frame
        conn_frame = ttk.LabelFrame(main_frame, text="Connection Settings", padding="5")
        conn_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Server settings
        ttk.Label(conn_frame, text="Server:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.server_var = tk.StringVar(value="localhost")
        ttk.Entry(conn_frame, textvariable=self.server_var, width=20).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)
        
        ttk.Label(conn_frame, text="Port:").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.port_var = tk.StringVar(value="5555")
        ttk.Entry(conn_frame, textvariable=self.port_var, width=10).grid(row=0, column=3, sticky=(tk.W, tk.E), pady=2, padx=5)
        
        ttk.Label(conn_frame, text="Encryption Key:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.key_var = tk.StringVar()
        ttk.Entry(conn_frame, textvariable=self.key_var, width=30, show="*").grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=2, padx=5)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.connect_btn = ttk.Button(
            button_frame, 
            text="Connect", 
            command=self.connect_vpn,
            width=15
        )
        self.connect_btn.grid(row=0, column=0, padx=5)
        
        self.disconnect_btn = ttk.Button(
            button_frame, 
            text="Disconnect", 
            command=self.disconnect_vpn,
            state=tk.DISABLED,
            width=15
        )
        self.disconnect_btn.grid(row=0, column=1, padx=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="5")
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.status_var = tk.StringVar(value="Not connected")
        ttk.Label(status_frame, textvariable=self.status_var, foreground="red").grid(row=0, column=0, sticky=tk.W)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        conn_frame.columnconfigure(1, weight=1)
        conn_frame.columnconfigure(3, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
    
    def _setup_logging(self):
        """Setup logging to GUI text widget"""
        self.log_handler = TextHandler(self.log_text)
        self.log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger = logging.getLogger('VPNClient')
        logger.addHandler(self.log_handler)
    
    def connect_vpn(self):
        """Connect to VPN server"""
        try:
            # Create configuration
            config_data = {
                "server_host": self.server_var.get(),
                "server_port": int(self.port_var.get()),
                "tun_device": "tun0",
                "client_ip": "10.0.0.2",
                "server_tun_ip": "10.0.0.1",
                "encryption_key": self.key_var.get(),
                "log_level": "INFO"
            }
            
            self.config = ClientConfig()
            for key, value in config_data.items():
                self.config[key] = value
            
            # Connect in separate thread
            def connect_thread():
                try:
                    self.client = VPNClient(self.config)
                    if self.client.connect():
                        self.is_connected = True
                        self.root.after(0, self._update_connected_ui)
                    else:
                        self.root.after(0, lambda: messagebox.showerror("Connection Failed", "Failed to connect to VPN server"))
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Connection error: {e}"))
            
            threading.Thread(target=connect_thread, daemon=True).start()
            self._update_connecting_ui()
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid configuration: {e}")
    
    def disconnect_vpn(self):
        """Disconnect from VPN server"""
        def disconnect_thread():
            if self.client:
                self.client.disconnect()
            self.is_connected = False
            self.root.after(0, self._update_disconnected_ui)
        
        threading.Thread(target=disconnect_thread, daemon=True).start()
        self._update_disconnecting_ui()
    
    def _update_connecting_ui(self):
        """Update UI when connecting"""
        self.connect_btn.config(state=tk.DISABLED)
        self.disconnect_btn.config(state=tk.DISABLED)
        self.status_var.set("Connecting...")
    
    def _update_connected_ui(self):
        """Update UI when connected"""
        self.connect_btn.config(state=tk.DISABLED)
        self.disconnect_btn.config(state=tk.NORMAL)
        self.status_var.set("Connected")
        # Change status color to green
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label) and str(child.cget('textvariable')) == str(self.status_var):
                        child.config(foreground="green")
    
    def _update_disconnecting_ui(self):
        """Update UI when disconnecting"""
        self.connect_btn.config(state=tk.DISABLED)
        self.disconnect_btn.config(state=tk.DISABLED)
        self.status_var.set("Disconnecting...")
    
    def _update_disconnected_ui(self):
        """Update UI when disconnected"""
        self.connect_btn.config(state=tk.NORMAL)
        self.disconnect_btn.config(state=tk.DISABLED)
        self.status_var.set("Not connected")
        # Change status color to red
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label) and str(child.cget('textvariable')) == str(self.status_var):
                        child.config(foreground="red")

class TextHandler(logging.Handler):
    """Log handler that writes to a Tkinter text widget"""
    
    def _init_(self, text_widget):
        super()._init_()
        self.text_widget = text_widget
    
    def emit(self, record):
        msg = self.format(record)
        
        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.see(tk.END)
            self.text_widget.configure(state='disabled')
        
        self.text_widget.after(0, append)

def run_gui():
    """Run the GUI application"""
    root = tk.Tk()
    app = VPNClientGUI(root)
    root.mainloop()

if _name_ == '_main_':
    run_gui()
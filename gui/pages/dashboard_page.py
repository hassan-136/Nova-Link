import customtkinter as ctk
from tkinter import messagebox

class DashboardPage(ctk.CTkFrame):
    """
    The main VPN dashboard showing connection status, server selection,
    and controls for connecting/disconnecting.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        # Connection State Management
        self.is_connected = ctk.BooleanVar(value=False)
        self.current_server = ctk.StringVar(value="Alpha-01")

        # Define the available servers as per the request (non-geographic)
        self.available_servers = [
            "Alpha-01 (Low Latency)",
            "Beta-05 (High Throughput)",
            "Gamma-10 (Balanced)",
            "Delta-03 (Secure Core)"
        ]

        # Configure main grid for central alignment
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_dashboard_card()
        self._setup_connection_bindings()

    def _build_dashboard_card(self):
        # ---------- Main Dashboard Card (Themed) ----------
        card = ctk.CTkFrame(
            self,
            corner_radius=25,
            fg_color="#14263D",      # Darker interior color
            border_width=3,
            border_color="#00C4FF"
        )
        card.grid(row=0, column=0, padx=50, pady=50, sticky="")
        card.grid_columnconfigure(0, weight=1)

        # --- Header ---
        header = ctk.CTkLabel(
            card,
            text="Nova Link VPN Status",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#4FC3F7"
        )
        header.grid(row=0, column=0, pady=(40, 5), sticky="n")

        # --- Connection Status Indicator ---
        self.status_label = ctk.CTkLabel(
            card,
            text="DISCONNECTED",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#F44336" # Red for disconnected
        )
        self.status_label.grid(row=1, column=0, pady=(10, 30))

        # --- Server Selector Dropdown ---
        server_label = ctk.CTkLabel(
            card,
            text="Selected Server:",
            text_color="#B0BEC5"
        )
        server_label.grid(row=2, column=0, pady=(10, 5), padx=40, sticky="w")
        
        self.server_optionmenu = ctk.CTkOptionMenu(
            card,
            values=self.available_servers,
            variable=self.current_server,
            width=350,
            height=45,
            corner_radius=10,
            fg_color="#1E3A5F",
            button_color="#00C4FF",
            button_hover_color="#00B0E5",
            dropdown_fg_color="#1E3A5F"
        )
        self.server_optionmenu.grid(row=3, column=0, padx=40, pady=(0, 30), sticky="ew")

        # --- Connect/Disconnect Button ---
        self.connect_button = ctk.CTkButton(
            card,
            text="CONNECT",
            width=350,
            height=60,
            corner_radius=30,
            fg_color="#00C4FF",
            hover_color="#00B0E5",
            font=ctk.CTkFont(size=20, weight="bold"),
            command=self._toggle_connection
        )
        self.connect_button.grid(row=4, column=0, pady=(20, 40), padx=40, sticky="ew")

        # --- Logout Button (Footer) ---
        logout_btn = ctk.CTkButton(
            card,
            text="Logout",
            fg_color="transparent",
            hover_color="#1E2B3E",
            text_color="#B0BEC5",
            command=self._logout
        )
        logout_btn.grid(row=5, column=0, pady=(0, 20))

    def _setup_connection_bindings(self):
        """Sets up the trace for the connection state to update the UI."""
        self.is_connected.trace_add("write", self._update_ui_on_status_change)
        self.current_server.trace_add("write", self._server_selection_changed)

    def _update_ui_on_status_change(self, *args):
        """Updates colors, text, and state when connection status changes."""
        if self.is_connected.get():
            # State: CONNECTED
            self.status_label.configure(text="CONNECTED", text_color="#4CAF50") # Green
            self.connect_button.configure(text="DISCONNECT", fg_color="#F44336", hover_color="#D32F2F") # Red
            self.server_optionmenu.configure(state="disabled")
            messagebox.showinfo("VPN Status", f"Connected successfully to {self.current_server.get()}!")
        else:
            # State: DISCONNECTED
            self.status_label.configure(text="DISCONNECTED", text_color="#F44336") # Red
            self.connect_button.configure(text="CONNECT", fg_color="#00C4FF", hover_color="#00B0E5") # Blue
            self.server_optionmenu.configure(state="normal")
            messagebox.showinfo("VPN Status", "VPN connection terminated.")

    def _server_selection_changed(self, *args):
        """Handles logic when a new server is selected, only if currently disconnected."""
        if self.is_connected.get():
            # If connected, changing the selection does nothing until disconnected
            return
        
        print(f"Selected server changed to: {self.current_server.get()}")

    def _toggle_connection(self):
        """Switches the connection state and triggers the UI update."""
        if self.is_connected.get():
            # Currently connected, so disconnect
            print(f"Attempting to disconnect from {self.current_server.get()}...")
            # --- Actual disconnection logic would go here ---
            self.is_connected.set(False)
        else:
            # Currently disconnected, so connect
            server = self.current_server.get()
            print(f"Attempting to connect to {server}...")
            # --- Actual connection logic would go here (e.g., handshake, latency check) ---
            
            # Simulate a successful connection after a brief delay (or immediately for this demo)
            self.is_connected.set(True)

    def _logout(self):
        """Handles logout logic and returns to the Startup page."""
        if self.is_connected.get():
            self._toggle_connection() # Disconnect first
        
        # Clear any stored session tokens/data if needed
        messagebox.showinfo("Logout", "You have been securely logged out.")
        self.controller.show_page("StartupPage")
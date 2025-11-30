import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

class DashboardPage(ctk.CTkFrame):
    """Modern VPN Dashboard with premium design and interactive UI."""

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Connection State
        self.is_connected = ctk.BooleanVar(value=False)
        self.current_server = ctk.StringVar(value="Alpha-01")

        # Servers
        self.available_servers = [
            "Alpha-01 (Low Latency)",
            "Beta-05 (High Throughput)",
            "Gamma-10 (Balanced)",
            "Delta-03 (Secure Core)"
        ]

        # Grid Config
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_dashboard_card()
        self._setup_connection_bindings()

    def _build_dashboard_card(self):
        # ---------- Main Card ----------
        card = ctk.CTkFrame(
            self,
            corner_radius=25,
            fg_color="#0F1C2C",
            border_width=2,
            border_color="#00C4FF"
        )
        card.grid(row=0, column=0, padx=60, pady=60, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        # --- Header ---
        header = ctk.CTkLabel(
            card,
            text="Nova Link VPN",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#4FC3F7"
        )
        header.grid(row=0, column=0, pady=(30, 10))

        # --- Status Card with Icon ---
        status_frame = ctk.CTkFrame(
            card,
            corner_radius=20,
            fg_color="#1E3A5F",
            border_width=1,
            border_color="#4FC3F7"
        )
        status_frame.grid(row=1, column=0, padx=40, pady=20, sticky="ew")
        status_frame.grid_columnconfigure(1, weight=1)

        # Status Indicator Circle
        self.status_circle = ctk.CTkLabel(
            status_frame,
            text="●",
            font=ctk.CTkFont(size=22),
            text_color="#F44336"  # Default: disconnected
        )
        self.status_circle.grid(row=0, column=0, padx=(10, 20), pady=10)

        # Status Text
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="DISCONNECTED",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#F44336"
        )
        self.status_label.grid(row=0, column=1, sticky="w")

        # --- Server Selection ---
        server_label = ctk.CTkLabel(
            card,
            text="Choose Server:",
            text_color="#B0BEC5"
        )
        server_label.grid(row=2, column=0, padx=40, sticky="w")

        # OptionMenu
        self.server_optionmenu = ctk.CTkOptionMenu(
            card,
            values=self.available_servers,
            variable=self.current_server,
            width=350,
            height=45,
            corner_radius=12,
            fg_color="#1E3A5F",
            button_color="#00C4FF",
            button_hover_color="#00B0E5",
            dropdown_fg_color="#1E3A5F"
        )
        self.server_optionmenu.grid(row=3, column=0, padx=40, pady=15, sticky="ew")

        # --- Connect Button ---
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
        self.connect_button.grid(row=4, column=0, pady=(15, 25), padx=40, sticky="ew")

        # --- Extra Info (Latency / Load Placeholder) ---
        self.info_label = ctk.CTkLabel(
            card,
            text="Latency: -- ms | Load: --%",
            text_color="#B0BEC5"
        )
        self.info_label.grid(row=5, column=0, pady=(0, 20))

        # --- Logout Button ---
        logout_btn = ctk.CTkButton(
            card,
            text="Logout",
            fg_color="transparent",
            hover_color="#1E2B3E",
            text_color="#B0BEC5",
            command=self._logout
        )
        logout_btn.grid(row=6, column=0, pady=(0, 20))

    def _setup_connection_bindings(self):
        self.is_connected.trace_add("write", self._update_ui_on_status_change)
        self.current_server.trace_add("write", self._server_selection_changed)

    def _update_ui_on_status_change(self, *args):
        if self.is_connected.get():
            self.status_label.configure(text="CONNECTED", text_color="#4CAF50")
            self.status_circle.configure(text="●", text_color="#4CAF50")
            self.connect_button.configure(
                text="DISCONNECT", fg_color="#F44336", hover_color="#D32F2F"
            )
            self.server_optionmenu.configure(state="disabled")
            messagebox.showinfo("VPN Status", f"Connected to {self.current_server.get()}!")
        else:
            self.status_label.configure(text="DISCONNECTED", text_color="#F44336")
            self.status_circle.configure(text="●", text_color="#F44336")
            self.connect_button.configure(
                text="CONNECT", fg_color="#00C4FF", hover_color="#00B0E5"
            )
            self.server_optionmenu.configure(state="normal")
            messagebox.showinfo("VPN Status", "Disconnected from VPN.")

    def _server_selection_changed(self, *args):
        if self.is_connected.get():
            return
        print(f"Selected server changed to: {self.current_server.get()}")

    def _toggle_connection(self):
        if self.is_connected.get():
            print(f"Disconnecting from {self.current_server.get()}...")
            self.is_connected.set(False)
        else:
            print(f"Connecting to {self.current_server.get()}...")
            self.is_connected.set(True)

    def _logout(self):
        if self.is_connected.get():
            self._toggle_connection()
        messagebox.showinfo("Logout", "You have been logged out securely.")
        self.controller.show_page("StartupPage")

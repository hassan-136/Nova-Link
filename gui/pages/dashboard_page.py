import customtkinter as ctk
from tkinter import messagebox
from servers import SERVERS

class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # VPN state
        self.is_connected = ctk.BooleanVar(value=False)
        self.current_server = ctk.StringVar(value="No Servers")

        # Load servers from servers.py
        self.available_servers = self._load_servers()

        # Build UI
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_dashboard_card()
        self._setup_connection_bindings()

    def _load_servers(self):
        """Convert server objects into readable strings for OptionMenu."""
        if not SERVERS:
            return ["No servers available"]

        return [
            f"{srv['name']} ({srv['description']})" for srv in SERVERS
        ]

    def _get_server_object(self):
        """Return the dictionary of the selected server."""
        selected = self.current_server.get()
        for srv in SERVERS:
            text = f"{srv['name']} ({srv['description']})"
            if text == selected:
                return srv
        return None

    def _build_dashboard_card(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=25,
            fg_color="#0F1C2C",
            border_width=2,
            border_color="#00C4FF"
        )
        card.grid(row=0, column=0, padx=60, pady=60, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        # Header
        title = ctk.CTkLabel(
            card,
            text="Nova Link VPN",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#4FC3F7"
        )
        title.grid(row=0, column=0, pady=(30, 10))

        # Status Card
        status_frame = ctk.CTkFrame(
            card,
            corner_radius=20,
            fg_color="#1E3A5F",
            border_width=1,
            border_color="#4FC3F7"
        )
        status_frame.grid(row=1, column=0, padx=40, pady=20, sticky="ew")
        status_frame.grid_columnconfigure(1, weight=1)

        self.status_circle = ctk.CTkLabel(
            status_frame,
            text="●",
            font=ctk.CTkFont(size=22),
            text_color="#F44336"
        )
        self.status_circle.grid(row=0, column=0, padx=(10, 20), pady=10)

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="DISCONNECTED",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#F44336"
        )
        self.status_label.grid(row=0, column=1, sticky="w")

        # Server label
        server_label = ctk.CTkLabel(
            card,
            text="Choose Server:",
            text_color="#B0BEC5"
        )
        server_label.grid(row=2, column=0, padx=40, sticky="w")

        # Server dropdown
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

        # Connect button
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

        # Info label
        self.info_label = ctk.CTkLabel(
            card,
            text="Latency: -- ms | Load: --%",
            text_color="#B0BEC5"
        )
        self.info_label.grid(row=5, column=0, pady=(0, 20))

        # Logout button
        logout_btn = ctk.CTkButton(
            card,
            text="Logout",
            fg_color="transparent",
            hover_color="#1E2B3E",
            text_color="#B0BEC5",
            command=self._logout
        )
        logout_btn.grid(row=6, column=0, pady=(0, 20))

    # Bindings
    def _setup_connection_bindings(self):
        self.is_connected.trace_add("write", self._update_ui_on_status_change)
        self.current_server.trace_add("write", self._server_selection_changed)

    def _update_ui_on_status_change(self, *args):
        if self.is_connected.get():
            self.status_label.configure(text="CONNECTED", text_color="#4CAF50")
            self.status_circle.configure(text="●", text_color="#4CAF50")
            self.connect_button.configure(text="DISCONNECT", fg_color="#F44336")

            self.server_optionmenu.configure(state="disabled")

            srv = self._get_server_object()
            if srv:
                messagebox.showinfo("VPN Status", f"Connected to {srv['name']}!")

        else:
            self.status_label.configure(text="DISCONNECTED", text_color="#F44336")
            self.status_circle.configure(text="●", text_color="#F44336")
            self.connect_button.configure(text="CONNECT", fg_color="#00C4FF")

            self.server_optionmenu.configure(state="normal")
            messagebox.showinfo("VPN Status", "Disconnected from server.")

    def _server_selection_changed(self, *args):
        if self.is_connected.get():
            return
        print("Selected server:", self.current_server.get())

    def _toggle_connection(self):
        if self.current_server.get() == "No servers available":
            messagebox.showerror("Error", "No servers to connect to.")
            return

        self.is_connected.set(not self.is_connected.get())

    def _logout(self):
        if self.is_connected.get():
            self._toggle_connection()

        messagebox.showinfo("Logout", "You have been logged out.")
        self.controller.show_page("StartupPage")
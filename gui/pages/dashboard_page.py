import customtkinter as ctk
from tkinter import messagebox
import socket
import threading
from servers import SERVERS, SERVER_DETAILS

class DashboardPage(ctk.CTkFrame):
    """Modern VPN Dashboard with premium design and interactive UI."""

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Connection State
        self.is_connected = ctk.BooleanVar(value=False)
        self.current_server = ctk.StringVar(value="")

        # Servers
        self.available_servers = SERVERS
        if self.available_servers:
            self.current_server.set(self.available_servers[0])

        # Grid Config
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_dashboard_card()
        self._setup_connection_bindings()

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

        header = ctk.CTkLabel(
            card,
            text="Nova Link VPN",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#4FC3F7"
        )
        header.grid(row=0, column=0, pady=(30, 10))

        # Status Card
        status_frame = ctk.CTkFrame(
            card, corner_radius=20, fg_color="#1E3A5F",
            border_width=1, border_color="#4FC3F7"
        )
        status_frame.grid(row=1, column=0, padx=40, pady=20, sticky="ew")
        status_frame.grid_columnconfigure(1, weight=1)

        self.status_circle = ctk.CTkLabel(
            status_frame, text="●", font=ctk.CTkFont(size=22), text_color="#F44336"
        )
        self.status_circle.grid(row=0, column=0, padx=(10, 20), pady=10)

        self.status_label = ctk.CTkLabel(
            status_frame, text="DISCONNECTED", font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#F44336"
        )
        self.status_label.grid(row=0, column=1, sticky="w")

        # Server Selection
        server_label = ctk.CTkLabel(card, text="Choose Server:", text_color="#B0BEC5")
        server_label.grid(row=2, column=0, padx=40, sticky="w")

        self.server_optionmenu = ctk.CTkOptionMenu(
            card, values=self.available_servers, variable=self.current_server,
            width=350, height=45, corner_radius=12, fg_color="#1E3A5F",
            button_color="#00C4FF", button_hover_color="#00B0E5",
            dropdown_fg_color="#1E3A5F"
        )
        self.server_optionmenu.grid(row=3, column=0, padx=40, pady=15, sticky="ew")

        # Connect Button
        self.connect_button = ctk.CTkButton(
            card, text="CONNECT", width=350, height=60, corner_radius=30,
            fg_color="#00C4FF", hover_color="#00B0E5",
            font=ctk.CTkFont(size=20, weight="bold"),
            command=self._toggle_connection
        )
        self.connect_button.grid(row=4, column=0, pady=(15, 25), padx=40, sticky="ew")

    def _setup_connection_bindings(self):
        self.is_connected.trace_add("write", self._update_ui_on_status_change)

    def _update_ui_on_status_change(self, *args):
        if self.is_connected.get():
            self.status_label.configure(text="CONNECTED", text_color="#4CAF50")
            self.status_circle.configure(text="●", text_color="#4CAF50")
            self.connect_button.configure(text="DISCONNECT", fg_color="#F44336", hover_color="#D32F2F")
            self.server_optionmenu.configure(state="disabled")
            messagebox.showinfo("VPN Status", f"Connected to {self.current_server.get()}!")
        else:
            self.status_label.configure(text="DISCONNECTED", text_color="#F44336")
            self.status_circle.configure(text="●", text_color="#F44336")
            self.connect_button.configure(text="CONNECT", fg_color="#00C4FF", hover_color="#00B0E5")
            self.server_optionmenu.configure(state="normal")
            messagebox.showinfo("VPN Status", "Disconnected from VPN.")

    def _toggle_connection(self):
        if self.is_connected.get():
            # Disconnect
            if hasattr(self, "client_socket"):
                self.client_socket.close()
            self.is_connected.set(False)
        else:
            # Connect
            from servers import SERVER_DETAILS
            server_info = SERVER_DETAILS.get(self.current_server.get())
            if not server_info:
                messagebox.showerror("Connection Error", "Server info not found.")
                return

            host = server_info["host"]
            port = server_info["port"]
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((host, port))
                threading.Thread(target=self._receive_server_messages, daemon=True).start()
                self.is_connected.set(True)
            except Exception as e:
                messagebox.showerror("Connection Failed", f"Could not connect: {e}")

    def _receive_server_messages(self):
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print(f"[SERVER] {data.decode()}")
        except Exception as e:
            print("Server connection closed:", e)
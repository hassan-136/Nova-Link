import customtkinter as ctk
from tkinter import messagebox
import socket
import threading
import time
import tempfile
import subprocess
import sys
import os
from servers import SERVERS, SERVER_DETAILS

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#0A1A2B")  # Dark background
        self.controller = controller

        # Connection State
        self.is_connected = ctk.BooleanVar(value=False)
        self.current_server = ctk.StringVar(value=SERVERS[0] if SERVERS else "")

        # Grid Config
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_dashboard_card()
        self._setup_connection_bindings()

    # ------------------ UI BUILD ------------------ #
    def _build_dashboard_card(self):
        # ---------------- Left: Central Card ---------------- #
        card = ctk.CTkFrame(
            self,
            width=700,
            height=800,
            corner_radius=30,
            fg_color="transparent"
        )
        card.place(relx=0.0, rely=0.5, x=20, y=40, anchor="w")  # 20 pixels from left
        card.pack_propagate(False)

        # Header
        header = ctk.CTkLabel(
            card,
            text="🌐 Nova Link VPN",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#4FC3F7"
        )
        header.pack(pady=(30, 20))

        # Server Selection
        server_label = ctk.CTkLabel(
            card, text="Select Server:", font=ctk.CTkFont(size=16),
            text_color="#B0BEC5"
        )
        server_label.pack(anchor="w", padx=40, pady=(25, 25))

        self.server_optionmenu = ctk.CTkOptionMenu(
            card, values=SERVERS, variable=self.current_server,
            width=600, height=50, corner_radius=15,
            fg_color="#1E3A5F", button_color="#00C4FF", button_hover_color="#00B0E5",
            dropdown_fg_color="#1E3A5F", dropdown_text_color="#E0F7FA"
        )
        self.server_optionmenu.pack(padx=40, pady=(0, 25))

        # Connect Button
        self.connect_button = ctk.CTkButton(
            card, text="CONNECT", width=600, height=60, corner_radius=30,
            fg_color="#00C4FF", hover_color="#00B0E5",
            font=ctk.CTkFont(size=22, weight="bold"),
            command=self._toggle_connection
        )
        self.connect_button.pack(pady=(10, 20))

        # Logout Button
        self.logout_button = ctk.CTkButton(
            card, text="LOGOUT", width=600, height=60, corner_radius=30,
            fg_color="#F44336", hover_color="#D32F2F",
            font=ctk.CTkFont(size=22, weight="bold"),
            command=lambda: print("Logout clicked!")  # placeholder
        )
        self.logout_button.pack(pady=(0, 20))  # space before footer

        # Footer Note
        footer = ctk.CTkLabel(
            card, text="Secure & Private VPN Connection",
            font=ctk.CTkFont(size=14), text_color="#78909C"
        )
        footer.pack(pady=(0, 20))

        # ---------------- Right: Status / Info Section ---------------- #
        status_section = ctk.CTkFrame(
            self,
            width=650,
            height=800,
            corner_radius=30,
            fg_color="transparent"
        )
        status_section.place(relx=0.0, rely=0.5, x=740, y=40, anchor="w")  # position right of card
        status_section.pack_propagate(False)

        # Status Container (horizontal)
        status_container = ctk.CTkFrame(
            status_section,
            fg_color="transparent"
        )
        status_container.pack(pady=(50, 20))

        # Status Circle
        self.status_circle = ctk.CTkLabel(
            status_container,
            text="●",
            font=ctk.CTkFont(size=36),
            text_color="#F44336"
        )
        self.status_circle.pack(side="left", padx=(0, 15))

        # Status Label
        self.status_label = ctk.CTkLabel(
            status_container,
            text="DISCONNECTED",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#F44336"
        )
        self.status_label.pack(side="left")

        # Accessible Files Label
        self.files_label = ctk.CTkLabel(
            status_section,
            text="Accessible Files:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#B0BEC5"
        )
        self.files_label.pack(anchor="w", padx=10, pady=(30, 5))

        # Container for files
        self.files_container = ctk.CTkFrame(
            status_section,
            width=800,
            corner_radius=10,
            fg_color="transparent"
        )
        self.files_container.pack(padx=10, pady=(0, 20), fill="both", expand=True)

        # Hide files section initially
        self.files_label.pack_forget()
        self.files_container.pack_forget()

    # ------------------ CONNECTION BINDINGS ------------------ #
    def _setup_connection_bindings(self):
        self.is_connected.trace_add("write", self._update_ui_on_status_change)

    def _update_ui_on_status_change(self, *args):
        if self.is_connected.get():
            self.status_label.configure(text="CONNECTED", text_color="#4CAF50")
            self.status_circle.configure(text="●", text_color="#4CAF50")
            self.connect_button.configure(
                text="DISCONNECT", fg_color="#F44336", hover_color="#D32F2F"
            )
            self.server_optionmenu.configure(state="disabled")

            # Show files section
            self.files_label.pack(anchor="w", padx=10, pady=(30, 5))
            self.files_container.pack(padx=10, pady=(0, 20), fill="both", expand=True)

        else:
            self.status_label.configure(text="DISCONNECTED", text_color="#F44336")
            self.status_circle.configure(text="●", text_color="#F44336")
            self.connect_button.configure(
                text="CONNECT", fg_color="#00C4FF", hover_color="#00B0E5"
            )
            self.server_optionmenu.configure(state="normal")

            # Clear and hide files section
            for widget in self.files_container.winfo_children():
                widget.destroy()  # remove all file boxes
            self.files_label.pack_forget()
            self.files_container.pack_forget()

    # ------------------ CONNECT/DISCONNECT ------------------ #
    def _toggle_connection(self):
        if self.is_connected.get():
            # Disconnect
            if hasattr(self, "client_socket"):
                self.client_socket.close()
            self.is_connected.set(False)
        else:
            # Disable UI during connection
            self.connect_button.configure(state="disabled")
            self.server_optionmenu.configure(state="disabled")
            self.status_label.configure(text="CONNECTING...", text_color="#FFC107")
            self.status_circle.configure(text="●", text_color="#FFC107")

            def connect_thread():
                start_time = time.time()
                # Animated pulsing circle
                for i in range(6):  # ~3 seconds
                    color = "#FFC107" if i % 2 == 0 else "#FFEB3B"
                    self.status_circle.configure(text="●", text_color=color)
                    time.sleep(0.5)

                # Try actual connection
                server_info = SERVER_DETAILS.get(self.current_server.get())
                if not server_info:
                    self.connect_button.configure(state="normal")
                    self.server_optionmenu.configure(state="normal")
                    self.status_label.configure(text="DISCONNECTED", text_color="#F44336")
                    self.status_circle.configure(text="●", text_color="#F44336")
                    return

                host, port = server_info["host"], server_info["port"]
                try:
                    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.client_socket.connect((host, port))
                    threading.Thread(target=self._receive_server_messages, daemon=True).start()

                    # Ensure at least 3 seconds
                    elapsed = time.time() - start_time
                    if elapsed < 3:
                        time.sleep(3 - elapsed)

                    # Connected
                    self.is_connected.set(True)
                except Exception as e:
                    messagebox.showerror("Connection Error", f"Failed to connect:\n{e}")
                    self.status_label.configure(text="DISCONNECTED", text_color="#F44336")
                    self.status_circle.configure(text="●", text_color="#F44336")
                finally:
                    self.connect_button.configure(state="normal")
                    if not self.is_connected.get():
                        self.server_optionmenu.configure(state="normal")

            threading.Thread(target=connect_thread, daemon=True).start()

    def _receive_server_messages(self):
        try:
            while True:
                data = self.client_socket.recv(1024).decode(errors="ignore")
                if not data:
                    break

                # --------------------- FILE LIST HANDLING --------------------- #
                if data.startswith("FILE_LIST"):
                    files = data.replace("FILE_LIST", "").strip().split("\n")
                    self._display_file_buttons(files)
                    continue

                # --------------------- FILE DOWNLOAD HANDLING ---------------- #
                if data.startswith("FILE_SIZE:"):
                    filesize = int(data.split(":")[1])

                    # Send ACK to server
                    self.client_socket.sendall(b"ACK")

                    # Receive file bytes
                    file_bytes = b""
                    remaining = filesize

                    while remaining > 0:
                        chunk = self.client_socket.recv(min(4096, remaining))
                        if not chunk:
                            break
                        file_bytes += chunk
                        remaining -= len(chunk)

                    # Convert to text safely
                    try:
                        text = file_bytes.decode()
                    except:
                        text = file_bytes.decode("utf-8", errors="replace")

                    # Open popup UI viewer
                    self._show_file_viewer("Downloaded File", text)

                    continue

                print("[SERVER]:", data)

        except Exception as e:
            print("Receive error:", e)

    def _display_file_buttons(self, files):
        # Clear old file buttons
        for widget in self.files_container.winfo_children():
            widget.destroy()

        # Create a button for each file
        for filename in files:
            btn = ctk.CTkButton(
                self.files_container,
                text=filename,
                width=600,
                fg_color="#1E3A5F",
                hover_color="#00B0FF",
                command=lambda f=filename: self.client_socket.sendall(f"GET_FILE:{f}".encode())
            )
            btn.pack(pady=5)

    def _show_file_viewer(self, filename, content):
        viewer = ctk.CTkToplevel(self)
        viewer.title(f"Viewing: {filename}")
        viewer.geometry("700x600")
        viewer.configure(fg_color="#0A1A2B")

        title = ctk.CTkLabel(
            viewer,
            text=filename,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#4FC3F7"
        )
        title.pack(pady=10)

        # Scrollable textbox
        textbox = ctk.CTkTextbox(
            viewer,
            width=650,
            height=500,
            corner_radius=10,
            fg_color="#102437",
            text_color="#E0F7FA",
            font=ctk.CTkFont(size=14)
        )
        textbox.pack(pady=10, padx=10)

        textbox.insert("0.0", content)
        textbox.configure(state="disabled")  # Read-only
import customtkinter as ctk
from tkinter import messagebox
import socket
import threading
import time
import sys

# Configure appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

SERVERS = [
    "Alpha1 (Low Latency)"
]

SERVER_DETAILS = {
    "Alpha1 (Low Latency)": {"host": "10.159.187.143", "port": 5555}
}

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#0A1A2B")  # Dark background
        self.controller = controller
        self.client_socket = None
        self.stop_threads = False

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
        card.place(relx=0.0, rely=0.5, x=20, y=40, anchor="w")
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
            command=lambda: print("Logout clicked!")
        )
        self.logout_button.pack(pady=(0, 20))

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
        status_section.place(relx=0.0, rely=0.5, x=740, y=40, anchor="w")
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
        # Hidden by default

        # Container for files
        self.files_container = ctk.CTkScrollableFrame(
            status_section,
            width=600,
            height=400,
            corner_radius=10,
            fg_color="transparent"
        )
        # Hidden by default

    # ------------------ CONNECTION BINDINGS ------------------ #
    def _setup_connection_bindings(self):
        self.is_connected.trace_add("write", self._update_ui_on_status_change)

    def _update_ui_on_status_change(self, *args):
        if self.is_connected.get():
            self.status_label.configure(text="CONNECTED", text_color="#4CAF50")
            self.status_circle.configure(text="●", text_color="#4CAF50")
            self.connect_button.configure(
                text="DISCONNECT", fg_color="#F44336", hover_color="#D32F2F", state="normal"
            )
            self.server_optionmenu.configure(state="disabled")

            # Show files section
            self.files_label.pack(anchor="w", padx=10, pady=(30, 5))
            self.files_container.pack(padx=10, pady=(0, 20), fill="both", expand=True)
        else:
            self.status_label.configure(text="DISCONNECTED", text_color="#F44336")
            self.status_circle.configure(text="●", text_color="#F44336")
            self.connect_button.configure(
                text="CONNECT", fg_color="#00C4FF", hover_color="#00B0E5", state="normal"
            )
            self.server_optionmenu.configure(state="normal")

            # Clear and hide files section
            for widget in self.files_container.winfo_children():
                widget.destroy()
            self.files_label.pack_forget()
            self.files_container.pack_forget()

    # ------------------ CONNECT/DISCONNECT ------------------ #
    def _toggle_connection(self):
        if self.is_connected.get():
            # Disconnect Logic
            self.stop_threads = True
            if self.client_socket:
                try:
                    self.client_socket.close()
                except:
                    pass
            self.is_connected.set(False)
        else:
            # Connect Logic
            self.stop_threads = False
            threading.Thread(target=self._connect_process, daemon=True).start()

    def _connect_process(self):
        """Runs in a background thread to handle the connection attempt."""
        # 1. Animation
        for i in range(6):  # ~3 seconds pulsing
            if self.stop_threads: return
            color = "#FFC107" if i % 2 == 0 else "#FFEB3B"
            self.status_circle.configure(text="●", text_color=color)
            time.sleep(0.5)

        # 2. Update UI to 'Connecting'
        self.connect_button.configure(state="disabled", text="Connecting...")
        
        # 3. Try Socket Connection
        try:
            target = SERVER_DETAILS[self.current_server.get()]
            
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(5) # 5 second timeout
            self.client_socket.connect((target["host"], target["port"]))
            self.client_socket.settimeout(None) # Remove timeout for blocking recv

            # If successful:
            self.is_connected.set(True)
            
            # Start the listener thread for files/messages
            threading.Thread(target=self._receive_server_messages, daemon=True).start()

        except Exception as e:
            # Connection failed
            self.is_connected.set(False)
            messagebox.showerror(
                "Connection Failed",
                f"Could not connect to {target['host']}:{target['port']}\n\nError: {e}"
            )
        finally:
            self.connect_button.configure(state="normal")

    def _receive_server_messages(self):
        """Runs in background to listen for FILE_LIST or downloads."""
        try:
            while not self.stop_threads:
                # Basic receive
                data = self.client_socket.recv(1024).decode(errors="ignore")
                if not data:
                    break

                # --- PROTOCOL: FILE LIST ---
                if "FILE_LIST" in data:
                    # Example format: "FILE_LIST file1.txt\nfile2.py"
                    clean_data = data.replace("FILE_LIST", "").strip()
                    if clean_data:
                        files = clean_data.split("\n")
                        self.after(0, lambda f=files: self._display_file_buttons(f))
                    continue

                # --- PROTOCOL: DOWNLOAD START ---
                if data.startswith("FILE_SIZE:"):
                    try:
                        filesize = int(data.split(":")[1])
                        
                        # Send ACK to server so it knows to start sending bytes
                        self.client_socket.sendall(b"ACK")

                        # Read exact bytes
                        file_bytes = b""
                        remaining = filesize
                        
                        while remaining > 0 and not self.stop_threads:
                            chunk = self.client_socket.recv(min(4096, remaining))
                            if not chunk: break
                            file_bytes += chunk
                            remaining -= len(chunk)

                        # Show the file content
                        try:
                            content = file_bytes.decode('utf-8')
                        except:
                            content = file_bytes.decode('utf-8', errors='replace')
                            
                        self.after(0, lambda c=content: self._show_file_viewer("Downloaded File", c))

                    except ValueError:
                        print("Error parsing file size")
                    continue

        except OSError:
            pass # Socket closed
        except Exception as e:
            print(f"Receive error: {e}")
        finally:
            # If loop breaks (server disconnected), update UI
            if not self.stop_threads:
                self.after(0, lambda: self.is_connected.set(False))

    def _display_file_buttons(self, files):
        # Clear old file buttons
        for widget in self.files_container.winfo_children():
            widget.destroy()

        # Create a button for each file
        for filename in files:
            if not filename.strip(): continue
            btn = ctk.CTkButton(
                self.files_container,
                text=filename,
                width=500,
                fg_color="#1E3A5F",
                hover_color="#00B0FF",
                command=lambda f=filename: self._request_file(f)
            )
            btn.pack(pady=5)

    def _request_file(self, filename):
        if self.client_socket:
            try:
                # Protocol: GET_FILE:filename
                msg = f"GET_FILE:{filename}"
                self.client_socket.sendall(msg.encode())
            except Exception as e:
                print(f"Send error: {e}")

    def _show_file_viewer(self, filename, content):
        viewer = ctk.CTkToplevel(self)
        viewer.title(f"Viewing: {filename}")
        viewer.geometry("700x600")
        viewer.configure(fg_color="#0A1A2B")
        
        # Bring to front
        viewer.attributes('-topmost', True)
        viewer.after(100, lambda: viewer.attributes('-topmost', False))

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

# ------------------ MAIN APP WRAPPER ------------------ #
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Nova Link VPN Client")
        self.geometry("1400x900")
        
        # Initialize the Dashboard Page
        self.dashboard = DashboardPage(self, self)
        self.dashboard.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
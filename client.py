import customtkinter as ctk
from tkinter import messagebox
import socket
import threading
import time

# --- CONFIGURATION ---
# We connect to Localhost (127.0.0.1) because the SSH Tunnel 
# will forward this traffic to the real server.
SERVERS = ["Secure Tunnel Connection"]
SERVER_DETAILS = {
    "Secure Tunnel Connection": {"host": "127.0.0.1", "port": 6666}
}

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#0A1A2B")
        self.controller = controller
        self.client_socket = None

        self.is_connected = ctk.BooleanVar(value=False)
        self.current_server = ctk.StringVar(value=SERVERS[0])

        self._build_dashboard_card()
        self._setup_connection_bindings()

    def _build_dashboard_card(self):
        # Center Card
        card = ctk.CTkFrame(self, width=600, height=700, corner_radius=30, fg_color="transparent")
        card.place(relx=0.3, rely=0.5, anchor="center")
        
        ctk.CTkLabel(card, text="🌐 Nova Link VPN", font=("Arial", 32, "bold"), text_color="#4FC3F7").pack(pady=30)
        
        self.server_optionmenu = ctk.CTkOptionMenu(card, values=SERVERS, variable=self.current_server, width=400, fg_color="#1E3A5F")
        self.server_optionmenu.pack(pady=20)

        self.connect_button = ctk.CTkButton(card, text="CONNECT", width=400, height=50, fg_color="#00C4FF", font=("Arial", 18, "bold"), command=self._toggle_connection)
        self.connect_button.pack(pady=10)

        # Status Side Panel
        self.status_panel = ctk.CTkFrame(self, width=400, corner_radius=0, fg_color="#0F2439")
        self.status_panel.place(relx=0.7, rely=0.0, relheight=1.0, anchor="n")
        
        self.status_label = ctk.CTkLabel(self.status_panel, text="DISCONNECTED", font=("Arial", 20, "bold"), text_color="#F44336")
        self.status_label.pack(pady=50)

        self.files_container = ctk.CTkScrollableFrame(self.status_panel, label_text="Available Files", width=350, height=500, fg_color="transparent")
        # Hidden initially
        
    def _setup_connection_bindings(self):
        self.is_connected.trace_add("write", self._update_ui)

    def _update_ui(self, *args):
        if self.is_connected.get():
            self.status_label.configure(text="SECURE LINK ACTIVE", text_color="#4CAF50")
            self.connect_button.configure(text="DISCONNECT", fg_color="#F44336")
            self.files_container.pack(pady=20, fill="both", expand=True)
        else:
            self.status_label.configure(text="DISCONNECTED", text_color="#F44336")
            self.connect_button.configure(text="CONNECT", fg_color="#00C4FF")
            self.files_container.pack_forget()
            for widget in self.files_container.winfo_children(): widget.destroy()

    def _toggle_connection(self):
        if self.is_connected.get():
            if self.client_socket: self.client_socket.close()
            self.is_connected.set(False)
        else:
            threading.Thread(target=self._connect_thread, daemon=True).start()

    def _connect_thread(self):
        self.connect_button.configure(state="disabled", text="Connecting...")
        try:
            target = SERVER_DETAILS[self.current_server.get()]
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((target['host'], target['port']))
            
            self.is_connected.set(True)
            threading.Thread(target=self._listener_thread, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"Connection Failed.\nIs the Tunnel or Server running?\n\n{e}")
        finally:
            self.connect_button.configure(state="normal")

    def _listener_thread(self):
        try:
            while self.is_connected.get():
                data = self.client_socket.recv(1024).decode(errors='ignore')
                if not data: break
                
                if data.startswith("FILE_LIST"):
                    files = data.replace("FILE_LIST\n", "").split("\n")
                    self.after(0, lambda: self._update_file_list(files))
                elif data.startswith("FILE_SIZE:"):
                    self._handle_file_download(data)
        except:
            self.is_connected.set(False)

    def _update_file_list(self, files):
        for widget in self.files_container.winfo_children(): widget.destroy()
        for f in files:
            if f.strip():
                btn = ctk.CTkButton(self.files_container, text=f, fg_color="#1E3A5F", command=lambda x=f: self.client_socket.sendall(f"GET_FILE:{x}".encode()))
                btn.pack(pady=5, padx=5, fill="x")

    def _handle_file_download(self, header):
        size = int(header.split(":")[1])
        self.client_socket.sendall(b"ACK") # Ready to receive
        
        content = b""
        while len(content) < size:
            chunk = self.client_socket.recv(4096)
            if not chunk: break
            content += chunk
            
        try:
            text_content = content.decode('utf-8')
            self.after(0, lambda: self._show_file_popup(text_content))
        except:
            messagebox.showinfo("Download", "File downloaded (Binary file, cannot view in text box).")

    def _show_file_popup(self, content):
        top = ctk.CTkToplevel(self)
        top.geometry("600x500")
        top.title("File Viewer")
        box = ctk.CTkTextbox(top, text_color="white", fg_color="#102437")
        box.pack(fill="both", expand=True, padx=10, pady=10)
        box.insert("0.0", content)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x800")
        self.title("Nova Link Client")
        DashboardPage(self, self).pack(fill="both", expand=True)

if __name__ == "__main__":
    App().mainloop()
import threading
from gui.app import SecureVPNApp
from start_servers import start_all_servers

if __name__ == "__main__":
    # Run servers in background
    threading.Thread(target=start_all_servers, daemon=True).start()

    # Start GUI
    app = SecureVPNApp()
    app.mainloop()
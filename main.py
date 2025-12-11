<<<<<<< HEAD
from gui.app import SecureVPNApp

if __name__ == "__main__":
    app = SecureVPNApp()
=======
import threading
from gui.app import SecureVPNApp
from start_servers import start_all_servers

if __name__ == "__main__":
    # Run servers in background
    threading.Thread(target=start_all_servers, daemon=True).start()

    # Start GUI
    app = SecureVPNApp()
>>>>>>> c452dc3a4dbc162d039f7b3bf77efaae8372470a
    app.mainloop()
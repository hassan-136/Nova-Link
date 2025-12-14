import threading
from gui.app import SecureVPNApp

if __name__ == "__main__":
    # Start GUI
    app = SecureVPNApp()
    app.mainloop()
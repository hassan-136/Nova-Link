import psutil
import os

# List of server scripts to close
SERVERS_FOLDER = os.path.join(os.path.dirname(__file__), "servers")
SERVER_FILES = [f for f in os.listdir(SERVERS_FOLDER) if f.endswith("_server.py")]

def close_servers():
    print("[CLOSE SERVERS] Checking running Python processes...")
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if not cmdline:
                continue
            for server_file in SERVER_FILES:
                if server_file in cmdline:
                    print(f"[CLOSE SERVERS] Terminating {server_file} (PID: {proc.info['pid']})")
                    proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

if __name__ == "__main__":
    close_servers()
    print("[CLOSE SERVERS] Done.")
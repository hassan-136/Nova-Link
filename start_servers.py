import os
import subprocess
import time

# ---------- Start all servers in servers/ folder ----------
def start_all_servers():
    servers_folder = os.path.join(os.path.dirname(__file__), "servers")
    server_processes = []

    # Loop through all Python files in servers/ (exclude __pycache__)
    for filename in os.listdir(servers_folder):
        if filename.endswith("_server.py"):
            server_path = os.path.join(servers_folder, filename)
            print(f"[START SERVERS] Starting server: {filename}")
            # Start server as a subprocess
            proc = subprocess.Popen(["python", server_path])
            server_processes.append(proc)

    return server_processes

if __name__ == "__main__":
    server_processes = start_all_servers()
    print(f"[START SERVERS] {len(server_processes)} server(s) started.")

    try:
        # Keep the script alive while servers are running
        print("[START SERVERS] Press Ctrl+C to stop all servers...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[START SERVERS] Shutting down all servers...")
        for proc in server_processes:
            proc.terminate()
        print("[START SERVERS] All servers stopped.")
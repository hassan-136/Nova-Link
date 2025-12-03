import os
import subprocess

def start_all_servers():
    servers_folder = os.path.join(os.path.dirname(__file__), "servers")
    server_processes = []

    for filename in os.listdir(servers_folder):
        if filename.endswith("_server.py"):
            server_path = os.path.join(servers_folder, filename)
            print(f"[START SERVERS] Starting server: {filename}")

            proc = subprocess.Popen(
                ["python", server_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            server_processes.append(proc)

    print(f"[START SERVERS] {len(server_processes)} server(s) started.")
    return server_processes
import socket
import threading
import os

HOST = '127.0.0.1'  # localhost
PORT = 5555         # port for Alpha-01

clients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.sendall("Welcome to Alpha-01 VPN server!".encode())

    # Send alpha1.txt contents to client
    file_path = os.path.join(os.path.dirname(__file__), "alpha1.txt")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            file_data = f.read()
        conn.sendall(f"\n---Contents of alpha1.txt---\n{file_data}\n".encode())
    else:
        conn.sendall("alpha1.txt not found on server.".encode())

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            print(f"[{addr}] {message}")
            conn.sendall(f"Server received: {message}".encode())
    except ConnectionResetError:
        pass
    finally:
        print(f"[DISCONNECTED] {addr} disconnected.")
        conn.close()
        clients.remove(conn)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Alpha-01 server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
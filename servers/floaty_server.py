import socket
import threading
import os

HOST = '127.0.0.1'   # localhost
PORT = 6666          # port for Floaty server

clients = []

# Folder for Floaty server files
FILES_DIR = os.path.join(os.path.dirname(__file__), "floaty_files")


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.sendall(b"Welcome to Floaty VPN server!\n")

    # Send list of files inside floaty_files/
    if os.path.exists(FILES_DIR):
        files = os.listdir(FILES_DIR)
        files_list_str = "\n".join(files)
        conn.sendall(f"FILE_LIST\n{files_list_str}".encode())
    else:
        conn.sendall(b"FILE_LIST\n")  # no files available

    # Listen for client requests
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            command = data.decode().strip()

            # Request: Download file
            if command.startswith("GET_FILE:"):
                filename = command.split(":", 1)[1]
                filepath = os.path.join(FILES_DIR, filename)

                if os.path.exists(filepath):
                    filesize = os.path.getsize(filepath)
                    conn.sendall(f"FILE_SIZE:{filesize}".encode())

                    ack = conn.recv(1024)  # Wait for ACK from client

                    # Send file in chunks
                    with open(filepath, "rb") as f:
                        while chunk := f.read(4096):
                            conn.sendall(chunk)
                else:
                    conn.sendall(b"FILE_NOT_FOUND")

            else:
                # Generic echo response
                conn.sendall(f"Server received: {command}".encode())

    finally:
        conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Floaty server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    start_server()
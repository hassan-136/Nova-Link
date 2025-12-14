import socket
import threading
import select
import os
import time

# --- Configuration ---
HOST = '0.0.0.0'  # localhost
PORT = 5555         # One port for both Proxy and File Server
FILES_DIR = os.path.join(os.path.dirname(__file__), "alpha_files")

def handle_socks_proxy(client_socket, initial_data=None):
    """
    Handles the SOCKS5 Proxy logic.
    """
    remote = None
    try:
        # If we already read the header during detection, use it
        if initial_data:
            header = initial_data
        else:
            header = client_socket.recv(262)

        if not header or header[0] != 0x05:
            return

        # 1. Send SOCKS5 response: no authentication
        client_socket.sendall(b"\x05\x00")

        # 2. Receive connection request
        request = client_socket.recv(262)
        if not request or request[1] != 0x01:
            return

        # 3. Parse target address and port
        addr_type = request[3]
        target_addr = ""
        target_port = 0

        if addr_type == 0x01:  # IPv4
            target_addr = socket.inet_ntoa(request[4:8])
            target_port = int.from_bytes(request[8:10], "big")
        elif addr_type == 0x03:  # Domain name
            domain_len = request[4]
            target_addr = request[5:5 + domain_len].decode()
            target_port = int.from_bytes(request[5 + domain_len:7 + domain_len], "big")
        else:
            return

        # 4. Connect to target
        try:
            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.connect((target_addr, target_port))
        except Exception as e:
            print(f"[PROXY ERROR] Connection failed: {e}")
            return

        # 5. Send success response
        client_socket.sendall(b"\x05\x00\x00\x01" + socket.inet_aton("0.0.0.0") + (0).to_bytes(2, "big"))

        # 6. Relay data
        while True:
            r, w, e = select.select([client_socket, remote], [], [])
            
            if client_socket in r:
                data = client_socket.recv(4096)
                if len(data) == 0: break
                remote.sendall(data)
                
            if remote in r:
                data = remote.recv(4096)
                if len(data) == 0: break
                client_socket.sendall(data)

    except Exception as e:
        pass # SOCKS connection ended
    finally:
        client_socket.close()
        if remote:
            remote.close()

def handle_file_server(conn):
    """
    Handles the Alpha-01 File Server logic.
    """
    try:
        conn.sendall(b"Welcome to Alpha-01 VPN server! (File Mode)\n")

        # Send list of files
        if os.path.exists(FILES_DIR):
            files = os.listdir(FILES_DIR)
            files_list_str = "\n".join(files)
            conn.sendall(f"FILE_LIST\n{files_list_str}".encode())
        else:
            conn.sendall(b"FILE_LIST\nNo files available.")

        # Wait for client requests
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            command = data.decode().strip()
            
            if command.startswith("GET_FILE:"):
                filename = command.split(":", 1)[1]
                filepath = os.path.join(FILES_DIR, filename)
                
                if os.path.exists(filepath) and os.path.isfile(filepath):
                    filesize = os.path.getsize(filepath)
                    conn.sendall(f"FILE_SIZE:{filesize}".encode())
                    
                    # Wait for ACK ensures client is ready for stream
                    # (Simple timeout based ack or just wait for next packet)
                    # For this simple protocol, we assume client listens immediately after size.
                    time.sleep(0.1) 
                    
                    with open(filepath, "rb") as f:
                        while chunk := f.read(4096):
                            conn.sendall(chunk)
                else:
                    conn.sendall(b"FILE_NOT_FOUND")
            else:
                conn.sendall(f"Server received: {command}".encode())

    except Exception as e:
        print(f"[FILE SERVER ERROR] {e}")
    finally:
        conn.close()

def connection_dispatcher(conn, addr):
    """
    Decides if the client is a SOCKS user or a File Server user.
    """
    print(f"[NEW CONNECTION] {addr} checking protocol...")
    
    # Wait up to 0.5 seconds to see if client speaks first (SOCKS)
    # or if client is waiting for us to speak (File Server)
    try:
        readable, _, _ = select.select([conn], [], [], 0.5)
        
        if readable:
            # Client sent data immediately. Peek at it.
            # We use MSG_PEEK to look at data without removing it from buffer
            first_byte = conn.recv(1, socket.MSG_PEEK)
            
            if first_byte and first_byte[0] == 0x05:
                print(f"[PROTOCOL] SOCKS5 detected for {addr}")
                handle_socks_proxy(conn)
            else:
                # Client sent something, but it's not SOCKS5 (maybe a custom command?)
                # We default to file server logic, but consuming the buffer might be needed
                print(f"[PROTOCOL] Unknown/Text data detected for {addr}. Switching to File Mode.")
                handle_file_server(conn)
        else:
            # Timeout: Client is silent. 
            # This usually means the client is waiting for our "Welcome" message.
            print(f"[PROTOCOL] Client silent. Assuming File Server Client for {addr}")
            handle_file_server(conn)
            
    except Exception as e:
        print(f"[DISPATCH ERROR] {e}")
        conn.close()

def start_server():
    # Ensure file directory exists
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)
        
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(100)
    print(f"[LISTENING] Alpha-01 Hybrid Server (SOCKS5 + Files) on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=connection_dispatcher, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
# servers/floaty_server.py
import socket
import threading

HOST = '127.0.0.1'
PORT = 5556

def handle_client(conn, addr):
    print(f"[FLOATY SERVER] Connected by {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # Echo data back (placeholder)
            conn.sendall(data)
    except Exception as e:
        print(f"[FLOATY SERVER] Connection error: {e}")
    finally:
        conn.close()
        print(f"[FLOATY SERVER] Disconnected {addr}")

def start_server():
    print(f"[FLOATY SERVER] Starting on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("[FLOATY SERVER] Waiting for clients...")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
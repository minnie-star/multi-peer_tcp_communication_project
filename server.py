import socket
import threading
from crypto_utils import generate_rsa_keys, serialize_public_key, decrypt_aes_key, decrypt_message
from session_manager import SessionManager

HOST = '127.0.0.1'
PORT = 6000   

session_manager = SessionManager()
private_key, public_key = generate_rsa_keys()

def broadcast_message(sender_id, data):
    sender_nickname = session_manager.sessions[sender_id]["nickname"]
    aes_key = session_manager.sessions[sender_id]["aes_key"]

    for sid, peer in session_manager.sessions.items():
        if sid != sender_id and peer["aes_key"]:
            try:
                plaintext = decrypt_message(aes_key, data).decode()
                formatted = f"{sender_nickname}: {plaintext}"
                peer["conn"].sendall(formatted.encode())
            except Exception as e:
                print(f"Error broadcasting to {peer['nickname']}: {e}")

def handle_client(conn, addr):
    # First message from client is nickname
    nickname = conn.recv(1024).decode().strip()
    session_id = session_manager.register_peer(conn, addr, nickname)
    print(f"{nickname} connected from {addr}")

    try:
        # Send server public key
        conn.sendall(serialize_public_key(public_key))

        # Receive encrypted AES key
        encrypted_key = conn.recv(4096)
        aes_key = decrypt_aes_key(private_key, encrypted_key)
        session_manager.sessions[session_id]["aes_key"] = aes_key

        while True:
            data = conn.recv(4096)
            if not data:
                print(f"{nickname} disconnected")
                break
            session_manager.sessions[session_id]["last_message"] = data
            broadcast_message(session_id, data)
    finally:
        conn.close()
        session_manager.remove_peer(session_id)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()

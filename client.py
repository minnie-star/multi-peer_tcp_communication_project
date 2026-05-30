import socket
from crypto_utils import load_public_key, encrypt_aes_key, generate_aes_key, encrypt_message

HOST = '127.0.0.1'
PORT = 6000

def start_client():
    nickname = input("Enter your nickname: ")
    aes_key = generate_aes_key()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))

        # Send nickname first
        client.sendall(nickname.encode())

        # Receive server public key
        server_pub_pem = client.recv(4096)
        server_public_key = load_public_key(server_pub_pem)

        # Encrypt AES key with server’s public key
        encrypted_key = encrypt_aes_key(server_public_key, aes_key)
        client.sendall(encrypted_key)

        print("Connected! Type messages below:")

        while True:
            msg = input()
            ciphertext = encrypt_message(aes_key, msg)
            client.sendall(ciphertext)

            # Receive broadcasted messages
            try:
                response = client.recv(4096).decode()
                if response:
                    print(response)
            except:
                pass

if __name__ == "__main__":
    start_client()



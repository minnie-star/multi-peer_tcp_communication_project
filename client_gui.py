import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog
from crypto_utils import load_public_key, encrypt_aes_key, generate_aes_key, encrypt_message, decrypt_message

HOST = '127.0.0.1'
PORT = 6000

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Chat Client")

        # Chat display
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state='disabled')
        self.chat_area.pack(padx=10, pady=10)

        # Entry field
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(side=tk.LEFT, padx=10, pady=10)

        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5)

        # Nickname prompt
        self.nickname = simpledialog.askstring("Nickname", "Enter your nickname:")

        # Networking
        self.aes_key = generate_aes_key()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

        # Send nickname first
        self.client.sendall(self.nickname.encode())

        # Receive server public key
        server_pub_pem = self.client.recv(4096)
        server_public_key = load_public_key(server_pub_pem)

        # Encrypt AES key with server’s public key
        encrypted_key = encrypt_aes_key(server_public_key, self.aes_key)
        self.client.sendall(encrypted_key)

        # Start thread to listen for incoming messages
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self):
        msg = self.entry.get()
        if msg:
            ciphertext = encrypt_message(self.aes_key, msg)
            self.client.sendall(ciphertext)
            self.entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(4096)
                if data:
                    message = data.decode()
                    self.chat_area.config(state='normal')
                    self.chat_area.insert(tk.END, message + "\n")
                    self.chat_area.config(state='disabled')
                    self.chat_area.yview(tk.END)
            except:
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()

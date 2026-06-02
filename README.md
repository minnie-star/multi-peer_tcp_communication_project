# Multi-Peer TCP Communication Project

A secure, end-to-end encrypted communication system built with Python sockets, supporting multiple peers connected through a central server. Each peer registers with a nickname, exchanges encrypted messages, and communicates seamlessly with others in real time.

https://youtu.be/CZktSaq6K4o

---

## Features

- **Multi-Peer Messaging**: Connect multiple clients to a single server and chat securely.
- **Nickname Registration**: Each client identifies with a unique nickname for easy recognition.
- **End-to-End Encryption**:
  - RSA for secure key exchange
  - AES (CFB/GCM recommended) for message encryption
- **Session Management**: Track active peers and relay messages with sender identification.
- **REST API Integration**: Optional endpoints for listing peers and sending messages programmatically.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

---

## Project Structure
multi-peer_tcp_communication_project/
│
├── server.py          # TCP server handling peer connections and relaying messages
├── client.py          # TCP client for sending/receiving encrypted messages
├── crypto_utils.py    # RSA/AES encryption utilities
├── session_manager.py # Tracks active peers and sessions
├── rest_api.py        # Flask-based REST API for external interaction
└── README.md          # Project documentation


---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/minnie-star/multi-peer_tcp_communication_project.git
cd multi-peer_tcp_communication_project

pip install -r requirements.txt
python server.py
python client_gui.py

Configuration
Default Ports:

TCP Server: 6000
REST API: 8000
Change ports in server.py and rest_api.py if needed.

Usage Example
Start the server.
Launch two clients:
Client A registers as Alice
Client B registers as Bob
Alice sends: Hello Bob!
Bob receives: [Alice]: Hello Bob!

Security Notes
RSA ensures secure AES key exchange.
AES-GCM is recommended for authenticated encryption.
Avoid deprecated AES modes (e.g., CFB) for production use.

Roadmap
[ ] Add REST endpoints for sending/receiving messages
[ ] Upgrade to AES-GCM for stronger security
[ ] Implement persistent storage for chat history
[ ] Add WebSocket support for browser-based clients

Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to improve.

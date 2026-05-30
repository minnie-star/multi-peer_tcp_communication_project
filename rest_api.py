from flask import Flask, request, jsonify
from session_manager import SessionManager
from crypto_utils import encrypt_message, decrypt_message

app = Flask(__name__)
session_manager = SessionManager()

# REST endpoint to send a message to a peer
@app.route('/send/<session_id>', methods=['POST'])
def send_message(session_id):
    if session_id not in session_manager.sessions:
        return jsonify({"error": "Session not found"}), 404

    data = request.json
    message = data.get("message")

    peer = session_manager.sessions[session_id]
    conn = peer["conn"]
    aes_key = peer.get("aes_key")

    if not aes_key:
        return jsonify({"error": "AES key not established"}), 400

    ciphertext = encrypt_message(aes_key, message)
    conn.sendall(ciphertext)

    return jsonify({"status": "Message sent", "session_id": session_id})

# REST endpoint to list active peers
@app.route('/peers', methods=['GET'])
def list_peers():
    return jsonify({"active_sessions": list(session_manager.sessions.keys())})

# REST endpoint to fetch last received message from a peer
@app.route('/receive/<session_id>', methods=['GET'])
def receive_message(session_id):
    if session_id not in session_manager.sessions:
        return jsonify({"error": "Session not found"}), 404

    peer = session_manager.sessions[session_id]
    aes_key = peer.get("aes_key")
    last_message = peer.get("last_message")

    if not aes_key:
        return jsonify({"error": "AES key not established"}), 400
    if not last_message:
        return jsonify({"status": "No messages received yet"}), 200

    try:
        plaintext = decrypt_message(aes_key, last_message).decode()
        return jsonify({"session_id": session_id, "message": plaintext})
    except Exception as e:
        return jsonify({"error": f"Failed to decrypt message: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=8000, debug=True)


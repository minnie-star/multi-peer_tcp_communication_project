import uuid

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def register_peer(self, conn, addr, nickname):
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "conn": conn,
            "addr": addr,
            "nickname": nickname,
            "aes_key": None,
            "last_message": None
        }
        return session_id

    def remove_peer(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def get_peers(self):
        return self.sessions


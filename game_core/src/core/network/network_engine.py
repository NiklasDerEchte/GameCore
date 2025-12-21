from game_core import *

# pip install "python-socketio[client]"

import socketio

# Erstelle einen Client
sio = socketio.Client()


@sio.event
def connect():
    print("✅ Verbunden mit Server")
    # Direkt beim Connect eine Nachricht senden


@sio.event
def message(data):
    print("📨 Nachricht vom Server:", data)


@sio.event
def update(data):
    print("🔁 Update erhalten:", data)


@sio.event
def disconnect():
    print("❌ Verbindung getrennt")


sio.connect("http://localhost:5000")
# Optional: Verbindung offen halten
sio.wait()


class NetworkEngine(Engine):
    def __init__(self):
        pass


class SyncVar:
    def __init__(self):
        pass

    def sync(self):
        sio.emit("move", {"x": 42, "y": 99})
        # self.websocket_send({"type": "sync_var", "var": name, "value": value})

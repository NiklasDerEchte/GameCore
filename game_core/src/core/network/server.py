import socketio

# Create a SocketIO server instance
sio = socketio.Server(cors_allowed_origins='*', async_mode='eventlet')

# Create a WSGI app
app = socketio.WSGIApp(sio)

# Event handlers
@sio.event
def connect(sid, environ):
    print(f'Client connected: {sid}')

@sio.event
def disconnect(sid):
    print(f'Client disconnected: {sid}')

@sio.event
def message(sid, data):
    print(f'Message from {sid}: {data}')
    # Echo the message back
    sio.emit('response', data, to=sid)

@sio.event
def join_room(sid, room):
    sio.enter_room(sid, room)
    print(f'{sid} joined room {room}')

@sio.event
def leave_room(sid, room):
    sio.leave_room(sid, room)
    print(f'{sid} left room {room}')

# Run the server
if __name__ == '__main__':
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
    
# For Linux/Production with Gunicorn:
# gunicorn -k eventlet -w 1 -b 0.0.0.0:5000 game_core.src.core.network.server:app
import socketio
from config import origins


sio = socketio.AsyncServer(cors_allowed_origins=origins, async_mode='asgi')

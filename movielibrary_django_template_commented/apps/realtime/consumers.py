"""WebSocket consumer for movie events.

This is a minimal broadcast-only consumer:
- Clients connect
- Server can broadcast messages to the 'movies' group
- Clients receive JSON like {"type":"refetch","message":"refetch movies"}
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MoviesConsumer(AsyncWebsocketConsumer):
    # Group name used for broadcast
    group_name = "movies"

    async def connect(self):
        # Add this socket to the group and accept connection
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove socket from group when disconnected
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # No-op: you can add client → server messages here if you need them later.
        return

    async def refetch_movies(self, event):
        # Called when group_send sends {"type":"refetch_movies", ...}
        await self.send(text_data=json.dumps({
            "type": "refetch",
            "message": event.get("message", "refetch movies"),
        }))

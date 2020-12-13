import json
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        pass
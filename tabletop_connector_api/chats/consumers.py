import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        if self.scope["user"].is_authenticated():

            self.chat_id = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_name = "chat"
            self.room_group_name = f"{self.room_name}_{self.chat_id}"

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
            self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        handle = text_data_json["handle"]

        Message.objects.create(
            content=message,
            handle=handle,
            chat=self.chat_id,
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))

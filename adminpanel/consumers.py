from django.conf import settings
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer, AsyncConsumer, SyncConsumer
import json

class TimersConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)("timers", self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("timers", self.channel_name)

    def receive(self, text_data):
        print("receive")
        async_to_sync(self.channel_layer.group_send)(
            "timers",
            {
                "type": "timers.message",
                "text": text_data,
            },
        )

    def timers_message(self, event):
        self.send(text_data=event["content"])

from channels import Group

def websocket_receive(message):
    text = message.content.get('text')
    if text:
        Group("anything").add(message.reply_channel)
        message.reply_channel.send({"text": "You said: {}".format(text)})
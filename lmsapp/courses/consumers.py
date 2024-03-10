from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = "notifications" 
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        pass


    def send_notification(self, event):
        message = event.get('message', '')
        self.send(text_data=json.dumps({
            'message': message
        }))
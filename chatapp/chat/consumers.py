import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()  # Accept the WebSocket connection

        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': 'Welcome to the chat!'
        }))

    def receive(self,text_data):
        data = json.loads(text_data)
        message = data.get('message')

        print(f"Received message: {message}")

    
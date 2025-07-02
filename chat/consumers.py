import json
from channels.generic.websocket import AsyncWebsocketConsumer
from authentication.models import PrivateChat, User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    


    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        sender = self.scope['user']

        chat_type = data['chat_type']

        if chat_type == 'Private_chat':
            await self.private_chat_save(data, sender,message)
            receiver_id = data['receiver_id']
            private_room = self.room_group_name

            await self.channel_layer.group_send(
                private_room,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': sender.id,
                    'receiver_id': receiver_id
                }
            )
        elif chat_type == 'Group_chat':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': sender.id                  
                }
            )




    async def chat_message(self,event):
        await self.send(
            text_data=json.dumps({
                'message': event['message'],
                'sender_id': event['sender_id']
            })
        )



    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def private_chat_save(self,data, sender_id,message):
        receiver_id = data['receiver_id']
        receiver = await sync_to_async(User.objects.get)(id=receiver_id)


        await sync_to_async(PrivateChat.objects.create)(
            sender = sender_id,
            receiver = receiver,
            message = message
        )

        

    
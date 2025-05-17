import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message
from django.contrib.auth.models import User
import base64
import re

class ChatConsumer(AsyncWebsocketConsumer):
    # async def connect(self):
    #     self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
    #     await self.channel_layer.group_add(self.room_name, self.channel_name)
    #     await self.accept()

    async def connect(self):
        get_room_name = self.scope['url_route']['kwargs']['room_name']
        #replace invalid characters by _
        regex_name = re.sub(r'[^a-zA-Z0-9._-]', '_', get_room_name)
        self.room_name = f"room_{regex_name}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json
        event = {
            'type': 'send_message',
            'message': message,
        }
        await self.channel_layer.group_send(self.room_name, event)


    async def send_message(self, event):
        data = event['message']
        await self.create_message(data=data)
        response_data = {
            'sender': data['sender'],
            'message': data['message']
        }
        await self.send(text_data=json.dumps({'message': response_data}))


    @database_sync_to_async
    def create_message(self, data):
        get_room_by_name = Room.objects.get(room_name=data['room_name'])
        get_sender = User.objects.get(username=data['sender'])
        if not Message.objects.filter(message=data['message']).exists():
            new_message = Message(room=get_room_by_name, sender=get_sender, message=data['message'])
            new_message.save()


            
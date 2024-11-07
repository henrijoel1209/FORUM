import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        
        # Créez une salle unique en fonction des deux IDs d'utilisateur
        self.room_name = f"chat_{min(self.user.id, int(self.user_id))}_{max(self.user.id, int(self.user_id))}"
        
        # Rejoignez le groupe de la salle
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        recipient_id = data['recipient_id']

        await self.save_message(message, recipient_id)
        
        # Envoyer le message à l'autre utilisateur dans le groupe
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': self.user.id
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id']
        }))

    @database_sync_to_async
    def save_message(self, message, recipient_id):
        recipient = User.objects.get(id=recipient_id)
        Message.objects.create(sender=self.user, recipient=recipient, content=message)

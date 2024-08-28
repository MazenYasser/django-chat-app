from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
import json
from channels.db import database_sync_to_async 
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_name = self.scope["url_route"]["kwargs"]["user_name"]
        self.chat_group_name = f"chat_{self.chat_name}"
        current_user = self.scope["user"].pk
        authenticated_users = self.chat_name.split("_")[1:]
        
        if self.scope["user"].is_authenticated and str(current_user) in authenticated_users:
            # Add the connection to the group using the channel name
            await self.channel_layer.group_add(
                self.chat_group_name,
                self.channel_name  # Use self.channel_name here
            )
            await self.accept()
    
    async def disconnect(self, code):
        # Remove the connection from the group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name  # Use self.channel_name here
        )
    
    async def receive(self, text_data=None, bytes_data=None):
        from .serializers import MessageSerializer
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print("Recieved Message: ", message)
        print("Recieved JSON: ", text_data_json)
        # Save the message to the database
        serializer = MessageSerializer(data={
        'sender': text_data_json["sender"],
        'receiver': text_data_json["receiver"],
        'content': text_data_json["message"],
        })
        
        if await sync_to_async(serializer.is_valid)():
            await database_sync_to_async(serializer.save)()
            message = serializer.data
            await self.channel_layer.group_send(
                f"notification_{message["receiver"]}",
                {
                    "type": "notify_user",
                    "notification": "New message received",
                    "notification_type": "chat_message",
                    "sender": message["sender"],
                }
            )
        else:
            message = serializer.errors
            
        # Send the message to the group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                "type": "chat_message",
                "message": message
            }
        )
    
    async def chat_message(self, event):
        message = event["message"]
        
        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message
        }))
        
class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            # Mark user as online
            await self.set_user_online_status(True)
            
            self.notification_group_name = f"notification_{self.user.id}"
            await self.channel_layer.group_add(
                self.notification_group_name,
                self.channel_name
            )
            
            await self.accept()

    async def disconnect(self, code):
        # Mark user as offline
        await self.set_user_online_status(False)
        self.notification_group_name = f"notification_{self.user.id}"
        await self.channel_layer.group_discard(
                self.notification_group_name,
                self.channel_name
            )
    
    async def set_user_online_status(self, status):
        self.user.is_online = status
        await sync_to_async(self.user.save)()
        
    async def notify_user(self, event):
        notification = event['notification']
        notification_type = event['notification_type']
        sender = event['sender']
        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            "notification": notification,
            "notification_type": notification_type,
            "sender": sender
        }))
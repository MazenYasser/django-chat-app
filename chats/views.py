from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MessageSerializer
from .selectors import get_chat_messages, get_unread_messages, get_chat_unread_messages
from rest_framework.decorators import action
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import math

class ChatMessagesView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        receiver = kwargs.get('user_id')
        messages = get_chat_messages(user, receiver)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
class MarkChatMessagesAsReadView(APIView):
    
    def post(self, request, *args, **kwargs):
        user = request.user
        receiver = kwargs.get('user_id')
        messages = get_chat_unread_messages(user, receiver)
        for message in messages:
            message.is_read = True
            message.save()
        channel_layer = get_channel_layer()
        print("user.pk: ", user.pk,)
        print("user: ", user)
        print("receiver: ", receiver)
        print(f"private_{min(user.pk, int(receiver))}_{max(user.pk, int(receiver))}")
        async_to_sync(channel_layer.group_send)(
            f"chat_private_{min(user.pk, int(receiver))}_{max(user.pk, int(receiver))}",
            {
                "type": "read_receipt",
                "message": "All messages marked as read"
            }
        )
        return Response({"message": "All messages marked as read"})
    
class UnreadMessagesView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        messages = get_unread_messages(user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
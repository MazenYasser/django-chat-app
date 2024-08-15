from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MessageSerializer
from .selectors import get_chat_messages, get_unread_messages
from rest_framework.decorators import action

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
        messages = get_chat_messages(user, receiver)
        for message in messages:
            message.is_read = True
            message.save()
        return Response({"message": "All messages marked as read"})
    
class UnreadMessagesView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        messages = get_unread_messages(user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
from rest_framework import serializers
from .models import Message
from users.models import User
from datetime import datetime
import pdb


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["sender", "receiver", "content"]

class MessageLogSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField('get_sender_name')

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"
    
    class Meta:
        model = Message
        fields = ["sender", "sender_name", "receiver", "content", "timestamp", "is_read"]
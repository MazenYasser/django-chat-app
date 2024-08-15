from rest_framework import serializers
from .models import Message
from users.models import User

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["sender", "receiver", "content"]
from rest_framework import serializers
from .models import User, Friend, FriendRequest

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name", "email"]
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]

class SendFriendRequestSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        current_user = self.context["request"].user
        friend_request = FriendRequest.objects.create(
            from_user=current_user,
            to_user=User.objects.get(username=validated_data["to_user"]),
        )
        return friend_request

    class Meta:
        model = FriendRequest
        fields = ["to_user"]


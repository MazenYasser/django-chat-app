from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from yaml import serialize
from .models import User, Friend, FriendRequest
from .selectors import *
from .serializers import UserRegistrationSerializer, SendFriendRequestSerializer, UserSerializer



class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerializer
        elif self.action == "get_friend_list":
            return UserSerializer
        elif self.action == "send_friend_request":
            return SendFriendRequestSerializer
        else:
            return UserSerializer

    
    def create(self, request, *args, **kwargs):
        user_data = request.POST
        serializer = self.get_serializer(user_data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        
    @action(methods=["GET"], detail=True, url_path="friends")
    def get_friend_list(self, request, *args, **kwargs):
        friends_list = get_friend_list(request.user)
        serializer = UserSerializer(friends_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=True, url_path="friend-request")
    def send_friend_request(self, request, *args, **kwargs):
        sender = request.user
        recpient_name = request.data.get("to_user")
        
        try:
            recipent = get_user_by_username(recpient_name)
        except User.DoesNotExist:
            return Response({"message": "User with name " + recpient_name + " does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if recipent == sender:
            return Response({"message": "Cannot send friend request to yourself!"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data={"to_user": recipent.pk})

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Friend request sent to " + recpient_name}, status=status.HTTP_200_OK)
            
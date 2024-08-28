from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import User, StatusChoices

from .selectors import *
from .serializers import *

from django.contrib.auth.hashers import make_password


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

    @action(methods=["GET"], detail=False, url_path="user-data")
    def get_user_data(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response({"message": "You are not logged in"}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
    def create(self, request, *args, **kwargs):
        user_data = request.data
        password = request.data["password"]
        hashed_password = make_password(password)
        request.data["password"] = hashed_password
        serializer = self.get_serializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(methods=["GET"], detail=False, url_path="friends")
    def get_friend_list(self, request, *args, **kwargs):
        friends_list = get_friend_list(request.user)
        serializer = UserSerializer(friends_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, url_path="friend-request")
    def send_friend_request(self, request, *args, **kwargs):
        sender = request.user
        recpient_name = request.data.get("to_user")
        
        try:
            recipent = get_user_by_username(recpient_name)
        except User.DoesNotExist:
            return Response({"message": "User with name " + recpient_name + " does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        if recipent == sender:
            return Response({"message": "Cannot send friend request to yourself!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if recipent in get_friend_list(sender):
            return Response({"message": "You are already friends with " + recpient_name}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data={"to_user": recipent.pk})

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Friend request sent to " + recpient_name}, status=status.HTTP_201_CREATED)

class FriendRequestViewset(ModelViewSet):
    serializer_class = UpdateFriendRequestSerializer
    queryset = FriendRequest.objects.all()
    
    def patch(self, request):
        friend_request = get_friend_request_by_id(request.data.get("friend_request_id"))
        if not friend_request:
            return Response({"message": "Friend request does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        if friend_request.status == StatusChoices.ACCEPTED:
            return Response({"message": "Friend request already accepted"}, status=status.HTTP_400_BAD_REQUEST)
        
        new_request_status = request.data.get("status")
        friend_request.status = new_request_status
        friend_request.save()
        
        return Response({"message": "Friend request is" + str(new_request_status).lower()}, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        friend_request_list = get_pending_friend_requests(request.user)
        serializer = FriendRequestSerializer(friend_request_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
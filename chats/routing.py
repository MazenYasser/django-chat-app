from django.urls import re_path

from chats.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r"chat/(?P<user_name>\w+)/$", ChatConsumer.as_asgi(), name="chat")
]
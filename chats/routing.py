from django.urls import re_path, path

from chats.consumers import ChatConsumer, StatusConsumer

websocket_urlpatterns = [
    re_path(r"chat/(?P<user_name>\w+)/$", ChatConsumer.as_asgi(), name="chat"),
    re_path(r"status/$", StatusConsumer.as_asgi(), name="status"),
]
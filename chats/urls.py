from django.urls import path
from .views import ChatMessagesView, MarkChatMessagesAsReadView, UnreadMessagesView

urlpatterns = [
    path("chat/<str:user_id>/", ChatMessagesView.as_view(), name="chat"),
    path("chat/<str:user_id>/mark-all-as-read/", MarkChatMessagesAsReadView.as_view(), name="mark-all-as-read"),
    path("unread-messages/", UnreadMessagesView.as_view(), name="unread-messages"),
]

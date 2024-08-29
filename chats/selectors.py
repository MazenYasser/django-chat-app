from .models import Message
from django.db.models import Q

def get_chat_messages(user, receiver):
    return Message.objects.filter(
        (Q(sender=user, receiver=receiver) | Q(sender=receiver, receiver=user))
    ).order_by('timestamp')

def get_unread_messages(user):
    return Message.objects.filter(receiver=user, is_read=False).order_by('timestamp')

def get_chat_unread_messages(user, receiver):
    return Message.objects.filter(
        (Q(sender=user, receiver=receiver, is_read=False) | Q(sender=receiver, receiver=user, is_read=False))
    ).order_by('timestamp')


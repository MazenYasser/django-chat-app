from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FriendRequest, Friend

@receiver(post_save, sender=FriendRequest)
def create_friendship(sender, instance, created, **kwargs):
    if not created and instance.accepted:
        Friend.objects.get_or_create(friend_1=instance.from_user, friend_2=instance.to_user)
        Friend.objects.get_or_create(friend_1=instance.to_user, friend_2=instance.from_user)



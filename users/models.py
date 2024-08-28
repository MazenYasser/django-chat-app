from enum import Enum
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import transaction

class StatusChoices(models.TextChoices):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
        
        
class User(AbstractUser):
    is_online = models.BooleanField(default=False)
    friends = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="friends_with", through="Friend")

class Friend(models.Model):
    friend_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    friend_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Friendship started at: {self.timestamp} | {self.friend_1} - {self.friend_2}"

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_sender")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_receiver")
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default="PENDING")
    
    
    @transaction.atomic
    def save(self, *args, **kwargs):    
        if self.status == StatusChoices.ACCEPTED:
            Friend.objects.get_or_create(friend_1=self.from_user, friend_2=self.to_user)
            Friend.objects.get_or_create(friend_1=self.to_user, friend_2=self.from_user)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Friend request sent at: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | {self.from_user} - {self.to_user}"

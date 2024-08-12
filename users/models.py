from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_online = models.BooleanField(default=False)
    friends = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="friends_with", through="Friend")

class Friend(models.Model):
    friend_1 = models.ForeignKey(User, on_delete=models.SET("Deleted User"), related_name="from_user")
    friend_2 = models.ForeignKey(User, on_delete=models.SET("Deleted User"), related_name="to_user")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Friendship started at: {self.timestamp} | {self.from_user} - {self.to_user}"

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.SET("Deleted User"), related_name="request_sender")
    to_user = models.ForeignKey(User, on_delete=models.SET("Deleted User"), related_name="request_receiver")
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Friend request sent at: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | {self.from_user} - {self.to_user}"

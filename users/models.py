from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_online = models.BooleanField(default=False)
    friends = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="friends_with", through="Friend")

class Friend(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.SET("Deleted User"), related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.SET("Deleted User"), related_name="to_user")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Friendship started at: {self.timestamp} | {self.from_user} - {self.to_user}"

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.SET("Deleted User"), related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.SET("Deleted User"), related_name="to_user")
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Friend request sent at: {self.timestamp} | {self.from_user} - {self.to_user}"

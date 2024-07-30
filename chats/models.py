from django.db import models

class Message(models.Model):
    sender = models.ForeignKey('users.User', on_delete=models.SET("Deleted User"), related_name='sender')
    receiver = models.ForeignKey('users.User', on_delete=models.SET("Deleted User"), related_name='receiver')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} | {self.sender.username}: {self.content} >> {self.receiver.username}"
    
    
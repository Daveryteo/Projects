# I wrote this code

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chat(models.Model):
    chat = models.CharField(max_length=255, unique=True, blank=False)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.chat

class ChatDetails(models.Model):
    content = models.CharField(max_length=10000)
    timeposted = models.DateTimeField(auto_now=True)
    chatroom = models.ForeignKey(Chat, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Message from {self.users} in {self.chatroom} at {self.timeposted}: {self.content}"

# end of code I wrote

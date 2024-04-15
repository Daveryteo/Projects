# I wrote this code

from django.db import models
from userprofile.models import *

# Create your models here.

class Friend(models.Model):
    user = models.OneToOneField(User, related_name='friend_user', on_delete=models.CASCADE, null=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    def __str__(self):
        return self.user.username

    def add_friend(self, added):
        if not added in self.friends.all():
            self.friends.add(added)
            self.save()

    # helps to remove friend from friends list
    def remove_friends(self, removed):
        if removed in self.friends.all():
            self.friends.remove(removed)
            self.save()

    def unfriend(self, unfriend):
        self.remove_friends(unfriend)
        friends_list = Friend.objects.get(user=unfriend)
        friends_list.remove_friends(self.user)


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    pending_req = models.BooleanField(blank=True, null=False, default=True)
    timesent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        # get the user that received the friend request
        # check if received friend request, we add the receiver to sender's friends list
        # get the senders info then add sender to receiver's friends list
        # change pending friend request to false
        Receiver = Friend.objects.get(user=self.receiver)
        if Receiver:
            Receiver.add_friend(self.sender)
            Sender = Friend.objects.get(user=self.sender)
            Sender.add_friend(self.receiver)
            self.pending_req = False
            self.save()

    # if friend request decline or cancel just change pending to false
    def decline(self):
        self.pending_req = False
        self.save()

    def cancel(self):
        self.pending_req = False
        self.save()
# I wrote this code

from rest_framework import serializers
from .models import *
from userprofile.serializers import *


class FriendSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    friends = UserSerializer(many=True)
    class Meta:
        model = Friend
        fields = ['pk', 'user','friends']


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()
    class Meta:
        model = FriendRequest
        fields = ['pk', 'sender', 'receiver', 'pending_req', 'timesent']

# end of code I wrote

# I wrote this code

from rest_framework import serializers
from .models import *
from userprofile.serializers import *

class ChatSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Chat
        fields = ['pk', 'chat', 'users']

class ChatDetails(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    chat = ChatSerializer

    class Meta:
        model = ChatDetails
        fields = ['pk', 'content', 'timeposted', 'chatroom', 'users']

# end of code I wrote

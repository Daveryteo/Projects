# I wrote this code

from rest_framework import serializers
from .models import *
from userprofile.serializers import *

class UserPostSerializer(serializers.ModelSerializer):

    #get the user data and format it using the model and fields
    users = UserSerializer()
    class Meta:
        model = Posts
        fields = ['pk', 'users', 'content','images','timeposted']

# end of code I wrote
# I wrote this code

from .models import *
from .serializers import *

from rest_framework import generics
from rest_framework import mixins

class FriendDetails(generics.ListAPIView, mixins.RetrieveModelMixin):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class FriendRequest(generics.ListAPIView, mixins.RetrieveModelMixin):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# end of code I wrote

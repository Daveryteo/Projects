# I wrote this code

from .models import *
from .serializers import *

from rest_framework import generics
from rest_framework import mixins


class ChatList(generics.GenericAPIView, mixins.RetrieveModelMixin):

    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# end of code I wrote

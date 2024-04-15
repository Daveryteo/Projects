# I wrote this code

from .models import *
from .forms import *
from .serializers import *

from rest_framework import generics
from rest_framework import mixins


class PostsList(generics.GenericAPIView, mixins.RetrieveModelMixin):

    # get model table and serializer class
    queryset = Posts.objects.all()
    serializer_class = UserPostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class NewPost(generics.GenericAPIView, mixins.CreateModelMixin):

    # get model table, serializer class and form class
    queryset = Posts.objects.all()
    serializer_class = UserPostSerializer
    form_class = NewPostForm

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# end of code I wrote
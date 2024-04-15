# I wrote this code

from .forms import *
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework import mixins


class UserList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserAccountSerializer


class CreateUser(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    form_class = UserForm

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetails(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserAccountSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# end of code I wrote

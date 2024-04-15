# I wrote this code

from django import forms
from .models import *

class ChatForm(forms.ModelForm):
    chat = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Chatroom name', 'label': 'Create a new chatroom'}))

    class Meta:
        model = Chat
        fields = ['chat']

# end of code I wrote

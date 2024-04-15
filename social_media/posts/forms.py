# I wrote this code

from django import forms
from .models import *

# create form for new posts which has a text and image field
class NewPostForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'placeholder':'What is happening?!',
                                                           'style': 'min-width: 100%',
                                                           'row': '5'}))
    images = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Posts
        fields = ['content', 'images']

# end of code I wrote
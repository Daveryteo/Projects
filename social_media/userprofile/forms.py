# I wrote this code

from django import forms
from django.forms import ModelForm, EmailInput, TextInput, PasswordInput
from .models import *
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'username': TextInput(attrs={'id': "username", 'class': "form-control", 'placeholder': 'Username'}),
            'username.label_tag': TextInput(attrs={'class': "small mb-1", 'value': 'Username'}),
            'first_name': TextInput(attrs={'class': "form-control", 'placeholder': 'First Name'}),
            'last_name': TextInput(attrs={'class': "form-control", 'placeholder': 'Last Name'}),
            'email': EmailInput(attrs={'class': "form-control", 'placeholder': 'Email Address'}),
            'password': PasswordInput(attrs={'class': "form-control", 'placeholder': 'Password'})
        }


# update user info form for user model in django
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=256, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=128, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=128, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


# form for the user profile on top of the user model
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('pfp', 'dob')


# update form for the user profile
class UpdateUserProfileForm(forms.ModelForm):
    pfp = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    dob = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y', attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = UserProfile
        fields = ['pfp', 'dob']


# end of code I wrote

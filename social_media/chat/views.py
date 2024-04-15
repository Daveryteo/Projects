# I wrote this code

from django.contrib import messages
from django.shortcuts import render, redirect

from .models import *
from .forms import *
from userprofile.models import *
from userprofile.forms import *

# Create your views here.
def chat(request):
    context = {}
    if request.user.is_authenticated:
        if request.method == "POST":
            chatform = ChatForm(request.POST)
            if chatform.is_valid():
                chatform.save()
                chatroom = request.POST['chatroom']
                messages.success(request, 'Chatroom created successfully')
                return redirect('/chat/' + chatroom)
            else:
                messages.error(request, 'There was an error when creating the chatroom')
                return redirect('chat')
        else:
            profile_form = UpdateUserProfileForm(instance=request.user.profile)
            chats = Chat.objects.all()
            chatform = ChatForm()
            context['profile_form'] = profile_form
            context['navbar'] = "chat"
            context['chat_name'] = chats
            context['chatForm'] = chatform
        return render(request, 'chat.html', context)
    else:
        messages.error(request, 'Please login first')
        return redirect('user_login')



def chatroom(request, chat_name):
    context = {}
    if request.user.is_authenticated:
        if request.method == "GET":
            profile_form = UpdateUserProfileForm(instance=request.user.profile)
            context['profile_form'] = profile_form
            context['navbar'] = "chat"
            context['chat_name'] = chat_name
        return render(request, 'chatroom.html', context)
    else:
        messages.error(request, 'Please login first')
        return redirect('user_login')



def deleteChat(request, chat_name):
    # if user wants to delete the chatroom
    try:
        chatroom = Chat.objects.get(chat=chat_name)
        chatroom.delete()
        messages.success(request, 'Chat deleted successfully')
        return redirect('chat')
    except:
        messages.error(request, 'Error deleting chat')
        return redirect('chat')

# end of code I wrote

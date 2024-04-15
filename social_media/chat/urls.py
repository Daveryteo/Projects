# I wrote this code

from django.urls import path, include
from . import views, api

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('chat/<str:chat_name>', views.chatroom, name='chatroom'),
    path('chat/deleteChat/<str:chat_name>', views.deleteChat, name='deleteChat'),
    path('api/chat/<int:pk>', api.ChatList.as_view(), name='chat_api')
]



# end of code I wrote

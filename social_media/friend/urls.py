# I wrote this code

from django.urls import include, path
from . import views
from . import api

urlpatterns = [
    path('friendDetails/<str:username>', views.friend_details, name='friend_details'),
    path('sendRequest/', views.send_request, name="send_request"),
    path('cancelRequest/', views.cancel_request, name="cancel_request"),
    path('removeFriend/', views.remove_friend, name="remove_friend"),
    path('acceptRequest/<req_id>/', views.accept_request, name="accept_request"),
    path('declineRequest/<req_id>/', views.decline_request, name="decline_request"),
    path('api/friendlist/<int:pk>/', api.FriendDetails.as_view(), name='friend_api'),
    path('api/friendrequest/<int:pk>/', api.FriendRequest.as_view(), name='friend_request_api'),
]

# end of code I wrote

# I wrote this code

from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import api

urlpatterns = [
    path('register', views.register_user, name='register'),
    path('login', views.login_user, name='login_user'),
    path('profile', views.user_profile, name='user_profile'),
    path('editProfile', views.edit_user_profile, name='edit_user_profile'),
    path('search', views.user_search, name='user_search'),
    path('logout', views.user_logout, name='user_logout'),
    path('acceptRequest/<req_id>/', views.accept_request, name="accept_request"),
    path('declineRequest/<req_id>/', views.decline_request, name="decline_request"),
    path('api/user/', api.UserList.as_view(), name='users_api'),
    path('api/user/<int:pk>/', api.UserDetails.as_view(), name='user_detail_api'),
    path('api/createuser/', api.CreateUser.as_view(), name='create_user_api'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# end of code I wrote
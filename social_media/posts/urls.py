# I wrote this code

from django.urls import include, path
from . import views
from . import api

urlpatterns = [
    path('', views.homepage, name='home'),
    path('api/newpost/', api.NewPost.as_view(), name='create_post_api'),
    path('api/posts/<int:pk>/', api.PostsList.as_view(), name='user_post_api'),
]

# end of code I wrote
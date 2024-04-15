"""socialmedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# I wrote this code
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = [
    path('', include('userprofile.urls')),
    path('', include('posts.urls')),
    path('', include('chat.urls')),
    path('', include('friend.urls')),
    path('admin/', admin.site.urls),
    path('apischema/', get_schema_view(
        title="Social Media",
        description="API for interacting with user records",
        version="1.0.0"
    ), name='openapi-schema'),
    path('swaggerdocs/', TemplateView.as_view(
                template_name='swagger-docs.html',
                extra_context={'schema_url':'openapi-schema'}
            ), name='swagger-ui'),
]

urlpatterns += staticfiles_urlpatterns()

# end of code I wrote

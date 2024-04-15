# I wrote this code

from django.contrib import admin
from .models import *

# Register your models here.
class PostsAdmin(admin.ModelAdmin):
    list_display=('id', 'users', 'content', 'images', 'timeposted')

admin.site.register(Posts, PostsAdmin)

# end of code I wrote
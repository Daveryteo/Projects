# I wrote this code

from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'pfp', 'dob')

admin.site.register(UserProfile, UserAdmin)

# end of code I wrote
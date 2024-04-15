# I wrote this code

from django.db import models
from userprofile.models import *


# Create your models here.
class Posts(models.Model):
    content = models.CharField(max_length=10000)
    # if there is image, we store in the file PostsImage
    images = models.ImageField(null=True, upload_to='PostsImage', blank=True)
    # helps to sort all the users posts in the homepage
    timeposted = models.DateTimeField(auto_now=True)
    users = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="user")

# end of code I wrote

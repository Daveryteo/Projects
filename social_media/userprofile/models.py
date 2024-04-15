# I wrote this code

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    pfp = models.ImageField(default='user.png', upload_to='profilePicture', null=True, blank=True)
    dob = models.DateField(null=True, blank=True)


    def __unicode__(self):
        return self.user.username

# end of code I wrote
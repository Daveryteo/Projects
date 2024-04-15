# I wrote this code

from django.shortcuts import render
from .models import *
from .forms import *
from userprofile.models import *
from userprofile.forms import *
from friend.models import *

import os
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def homepage(request, *args, **kwargs):
    context = {}
    current_user = request.user

    # check if request method is post and that the user is authenticated and get the post form
    if current_user.is_authenticated and request.method == "POST":
        postForm = NewPostForm(request.POST, request.FILES)

        # check if the post_form is valid and get the cleaned data
        if postForm.is_valid():
            content = postForm.cleaned_data.get("content")

            # we check if there is any image uploaded
            try:
                # request for file upload where the input name is 'postImage'
                request_file = request.FILES['PostsImage']

                url = os.path.join(settings.MEDIA_ROOT)
                storage = FileSystemStorage(location=url)
                file = storage.save(f"PostsImage/{str(request_file)}", request_file)

                # create a Posts object with the content, image and user information
                new_post = Posts.objects.create(content=content, images=file, users=current_user)
                messages.success(request, 'Your post has been successfully posted!')
                return HttpResponseRedirect("/")
            except:
                # if there is no image uploaded, create the Posts with only the content and user
                new_post = Posts.objects.create(content=content, users=current_user)

                messages.success(request, 'Your post has been successfully posted!')
                return HttpResponseRedirect("/")

    # if the user is authenticated
    if current_user.is_authenticated:
        # get the profile form from userprofile app
        profileForm = UpdateUserProfileForm(instance=current_user.profile)
        context['profile_form'] = profileForm

        friend_list = []
        try:
            # get the friends of the currentUser
            current_user_friend_list = Friend.objects.get(user=current_user)
            # append each friend object to the friend_list
            for friend in current_user_friend_list.friends.all():
                friend_list.append(friend)
        except Friend.DoesNotExist:
            pass

        # if there are friend in the friend_list, display currentUser's post and their friends' posts
        if friend_list != []:
            # include currentUser to list before filtering
            friend_list.append(current_user)

            # filter UserPost based on if user is in the friend_list
            # order by timestamp and reverse filtered result so that posts are correctly displayed on the home page
            # (new post displayed before old post)
            posts = reversed(Posts.objects.filter(user__in=friend_list).order_by('timeposted'))
            context['posts'] = posts

            # filter UserAccount based on if user is in the friend_list
            # this is to get the profile image of friends
            profile = UserProfile.objects.filter(user__in=friend_list)
            context['profile'] = profile

        # else if friend_list is empty
        else:
            # display own posts only
            # order by timestamp and reverse filtered result so that posts are correctly displayed on the home page
            # (new post displayed before old post)
            posts = reversed(Posts.objects.filter(users=current_user).order_by('timeposted'))
            context['posts'] = posts

            # filter UserAccount based on if user is in the friend_list
            # this is to get the profile image of friends
            profile = UserProfile.objects.get(user=current_user)
            context['profile'] = profile

        context['navbar'] = "home"
    return render(request, "homepage.html", context)


# end of code I wrote
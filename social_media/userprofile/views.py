# I wrote this code

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import *
from friend.models import *
from .forms import *
from posts.forms import *
from posts.models import *


def request_exists(sender, receiver):
    try:
        return FriendRequest.objects.get(sender=sender, receiver=receiver, pending_req=True)
    except FriendRequest.DoesNotExist:
        return False

def register_user(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # commit=false allows me to get the model object but does not save it,
            # so I can add the user data that was collected from user form and save it
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
            messages.success(request, user.username + 'has been successfully registered')
            return redirect('login_user')
        else:
            messages.error(request, 'Error registering please try again')
    else:
        user_form = UserForm()
    return render(request, 'register.html', {'user_form': user_form, 'registered': registered})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Inactive user contact admin')
                return redirect('user_login')
        else:
            messages.error(request, 'Invalid username/password')
            return redirect('user_login')
    else:
        return render(request, 'login.html')


@login_required
def user_profile(request):
    context = {}
    user = request.user

    if user.is_authenticated and request.method == 'GET':
        user_form = UpdateUserForm(instance=user)
        profile_form = UpdateUserProfileForm(instance=user.profile)
        posts = Posts.objects.filter(user=user)

        try:
            friend = Friend.objects.get(user=user)
        except Friend.DoesNotExist:
            friend_list = Friend(user=user)
            friend_list.save()

        # save the current user's friends list and filter the UserProfile to get friends' profile
        friend_list = friend.friends.all()
        context['friend_list'] = friend_list
        profile = UserProfile.objects.filter(user__in=friend_list)
        context['profile'] = profile
        friend_requests = None

        try:
            # get all friend requests that are still pending
            friend_requests = FriendRequest.objects.filter(receiver=user, pending_req=True)
            pfp_list = []
            sender_list = []

            for username in friend_requests:
                sender = User.objects.get(username=username)
                profile_friend = UserProfile.objects.get(user=sender)
                if profile_friend.image:
                    profile_friend_img = profile_friend.image.url
                    pfp_list.append(profile_friend_img)
                else:
                    pfp_list.append(None)
                if request_exists(sender=sender, receiver=user):
                    sender_id = request_exists(sender=sender, receiver=user).id
                    sender_list.append(sender_id)

            sender_info = zip(friend_requests, pfp_list, sender_list)
            context['sender_info'] = sender_info
        except:
            pass

        context['friend_requests'] = friend_requests
        context['user'] = user
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        context['posts'] = posts
    else:
        messages.error(request, 'Please login first')
        return redirect('user_login')
    return render(request, 'profile.html', context)


@login_required
def edit_user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=request.user)
            profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Profile update successful')
                return redirect('editProfile')
            else:
                messages.error(request, 'Error updating profile')
        else:
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateUserProfileForm(instance=request.user.profile)
    else:
        messages.error(request, 'Please login first')
        return redirect('user_login')

    return render(request, 'editprofile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def user_search(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            search = request.POST['query']
            if search:
                result = User.objects.filter(username__contains=search)
                pfp_list = []
                for user in result:
                    profile_friend = UserProfile.objects.get(user=user)
                    if profile_friend.image:
                        profile_friend_img = profile_friend.image.url
                        pfp_list.append(profile_friend_img)
                    else:
                        pfp_list.append(None)
                search_result = zip(result, pfp_list)
            else:
                return render(request, 'search.html')
    else:
        messages.error(request, 'Please login first')
        return redirect('user_login')
    return render(request, "search.html", {'search_result': search_result})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect("/")


@login_required
def accept_request(request, *args, **kwargs):
    current_user = request.user
    if request.method == "GET" and current_user.is_authenticated:
        req_id = kwargs.get("req_id")

        if req_id:
            friend_request = FriendRequest.objects.get(pk=req_id)
            try:
                friend_request.accept()
                messages.success(request, "Accepted friend request")
            except Exception as e:
                messages.error(request, "Error accepting friend request")
        else:
            messages.error(request, "Request does not exist")
    return HttpResponse


@login_required
def decline_request(request, *args, **kwargs):
    current_user = request.user
    if request.method == "GET" and current_user.is_authenticated:
        req_id = kwargs.get("req_id")
        if req_id:
            friend_request = FriendRequest.objects.get(pk=req_id)
            try:
                friend_request.decline()
                messages.success(request, "Friend request declined")
            except Exception as e:
                messages.error(request, "Error declining friend request")
        else:
            messages.error(request, "Request does not exist")
    return HttpResponse

# end of code I wrote

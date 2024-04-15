# I wrote this code

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import *
from userprofile.models import *
from userprofile.forms import *
from posts.models import *


# check if requests exists
def request_exists(sender, receiver):
    try:
        return FriendRequest.objects.get(sender=sender, receiver=receiver, pending_req=True)
    except FriendRequest.DoesNotExist:
        return False


def friend_details(request, username):
    context = {}
    user = request.user

    if user.is_authenticated:
        # get current user info and friends by using the username
        if request.method == "GET":
            current_user = User.objects.get(username=username)
            profile = UserProfile.objects.get(user=current_user)
            profile_form = UserProfileForm(instance=user.profile)
            posts = Posts.objects.filter(user=current_user)
            try:
                friend = Friend.objects.get(user=current_user)
            except Friend.DoesNotExist:
                friend = Friend(user=current_user)
                friend.save()

            # save the current user's friends list and filter the UserProfile to get friends' profile
            friend_list = friend.friends.all()
            context['friend_list'] = friend_list
            friend_profile = UserProfile.objects.filter(user__in=friend_list)
            context['friend_profile'] = friend_profile

            is_self = False
            # is_friend is to check if the user is already friends with current_user
            is_friend = False
            # request_state created to help track the state of the request
            # 0: request to user already exists, 1: request from user already exists, 2: user does not exists
            request_state = 0

            # check if user is friends with the current_user
            if friend_list.filter(pk=user.id):
                is_friend = True
            else:
                is_friend = False
                if request_exists(sender=current_user, receiver=user):
                    request_state = 0
                    context['request_id'] = request_exists(sender=current_user, receiver=user).id
                elif request_exists(sender=user, receiver=current_user):
                    request_state = 1
                else:
                    request_state = 2

            context['is_self'] = is_self
            context['is_friend'] = is_friend
            context['request_status'] = request_state
            context['user'] = current_user
            context['profile'] = profile
            context['profile_form'] = profile_form
            context['posts'] = posts
    else:
        messages.error(request, 'Please sign in before viewing profiles')
        return redirect('user_login')

    return render(request, 'friends.html', context)


def send_request(request):
    current_user = request.user

    if request.method == "POST" and current_user.is_authenticated:
        user_id = request.POST.get("receiverID")

        if user_id:
            receiver = User.objects.get(pk=user_id)
            # check if there is any friend requests if there is none send friend request
            try:
                friend_requests = FriendRequest.objects.filter(sender=current_user, receiver=receiver)
                # for all requests check if friend request is pending if not send the request
                try:
                    for req in friend_requests:
                        if req.pending_req:
                            messages.info(request, "You already have a pending friend request")
                    friend_request = FriendRequest(sender=current_user, receiver=receiver)
                    friend_request.save()
                    messages.success(request, "Friend request sent")
                except Exception as e:
                    messages.error(request, "Error sending friend request")
            except FriendRequest.DoesNotExist:
                friend_request = FriendRequest(sender=current_user, receiver=receiver)
                friend_request.save()
                messages.success(request, "Friend request sent")
        else:
            messages.error(request, "User does not exist")
    return HttpResponse


def cancel_request(request):
    current_user = request.user
    if request.method == "POST" and current_user.is_authenticated:
        user_id = request.POST.get("receiverID")


        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                cancelReq = FriendRequest.objects.filter(sender=current_user, receiver=receiver, pending_req=True)
                cancelReq.first().cancel()
                messages.success(request, "Cancelled friend request")

            except Exception as e:
                messages.error(request, "No friend request sent")
        else:
            messages.error(request, "User does not exist")
    return HttpResponse


def remove_friend(request):
    current_user = request.user

    if request.method == "POST" and current_user.is_authenticated:
        user_id = request.POST.get("receiverID")

        if user_id:
            try:
                RemoveFriend = User.objects.get(pk=user_id)
                self_friend_list = Friend.objects.get(user=current_user)
                self_friend_list.unfriend(RemoveFriend)
                messages.success(request, RemoveFriend.username + " has been removed")
            except Exception as e:
                messages.error(request, "Error removing friend")
        else:
            messages.error(request, "Friend does not exist")
    return HttpResponse


def accept_request(request, *args, **kwargs):
    current_user = request.user
    if request.method == "GET" and current_user.is_authenticated:
        req_id = kwargs.get("req_id")

        if req_id:
            friend_request = FriendRequest.objects.get(pk=req_id)
            try:
                friend_request.accept()
                messages.success(request, "Friend request has been accepted")
            except Exception as e:
                messages.error(request, "Error accepting friend request")
        else:
            messages.error(request, "Request does not exist")
    return HttpResponse


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

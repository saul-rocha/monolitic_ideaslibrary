from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from ..models import Profile, Post, Follower
from itertools import chain
import random
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def home(request):
    # user_profile = Profile.objects.get(user=request.user)

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    # retorna a foto do perfil

    user_following_list = []
    feed = []

    user_following = Follower.objects.filter(
        follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_list = Post.objects.filter(user=usernames)
        feed.append(feed_list)

    feed_list = list(chain(*feed))

    # sujestoes de usuarios para seguir
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_sugestion_list = [x for x in list(all_users) if (
        x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestion_list = [x for x in list(
        new_sugestion_list) if (x not in list(current_user))]

    random.shuffle(final_suggestion_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestion_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_list = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_list)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'home.html', {'user_profile': user_profile, 'posts': feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})


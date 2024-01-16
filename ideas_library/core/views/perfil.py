from django.shortcuts import render
from django.contrib.auth.models import User
from ..models import Profile, Post, Follower

from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def perfil(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if Follower.objects.filter(follower=follower, user=user).first():
        button_text = 'Deixar de seguir'
        color = 'vermelho'
    else:
        button_text = 'Seguir'
        color = 'verde'

    user_followers = len(Follower.objects.filter(user=pk))
    user_following = len(Follower.objects.filter(follower=pk))
    # print(user_following)

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
        'outro': request.user.username != pk,
        'color': color
    }

    return render(request, 'perfil.html', context)

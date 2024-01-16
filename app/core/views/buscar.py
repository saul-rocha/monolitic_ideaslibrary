from django.shortcuts import render
from django.contrib.auth.models import User
from ..models import Profile
from itertools import chain
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def buscar(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_list = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_list)

        username_profile_list = list(chain(*username_profile_list))

    return render(request, 'buscar.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

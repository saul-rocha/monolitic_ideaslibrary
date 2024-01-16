from django.shortcuts import render, redirect
from ..models import Follower

from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def seguir(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if Follower.objects.filter(follower=follower, user=user).first():
            delete_follower = Follower.objects.get(
                follower=follower, user=user)
            delete_follower.delete()

        else:
            Follower.objects.create(follower=follower, user=user)

        return redirect('/perfil/'+user)

    else:
        return redirect('/')

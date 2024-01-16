from django.shortcuts import render, redirect
from ..models import Profile

from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimage

            user_profile.profileimage = image
            user_profile.save()

        if request.FILES.get('image') != None:

            image = request.FILES.get('image')
            user_profile.profileimage = image
            user_profile.save()

        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})





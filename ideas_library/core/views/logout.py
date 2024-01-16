
from django.shortcuts import redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')
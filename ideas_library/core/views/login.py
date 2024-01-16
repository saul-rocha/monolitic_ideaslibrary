from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/home')
        else:
            messages.info(request, 'Usuário ou senha incorretos')
            return redirect('login')
    else:
        return render(request, 'login.html')
    


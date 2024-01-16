from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from ..models import Profile


def cadastro(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email já existe')
                return redirect('cadastro')
            elif User.objects.filter(username=user).exists():
                messages.info(request, 'Nome de usuário já existe!')
                return redirect('cadastro')
            else:
                user = User.objects.create_user(
                    username=user, email=email, password=password)
                user.save()

                # redirecionar para configs
                user_login = auth.authenticate(
                    username=user, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=user)
                new_profile = Profile.objects.create(
                    user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Senhas não coincidem!')
            return redirect('cadastro')
    else:
        return render(request, 'cadastro.html')
    # forms
    # def cadastro(request):
    #     if request.method == 'POST':
    #         form_usuario = UserCreationForm(request.POST)
    #         form_perfil = CadastroForm(request.POST)

    #         if form_usuario.is_valid() and form_perfil.is_valid():
    #             # Salvar o usuário
    #             user = form_usuario.save()

    #             # Atualizar o perfil associado ao usuário
    #             perfil = form_perfil.save(commit=False)
    #             perfil.user = user
    #             perfil.save()

    #             # Redirecione para a página inicial após o registro
    #             return redirect('index')
    #     else:
    #         form_usuario = UserCreationForm()
    #         form_perfil = CadastroForm()

    #     return render(request, 'cadastro.html', {'form_usuario': form_usuario, 'form_perfil': form_perfil})

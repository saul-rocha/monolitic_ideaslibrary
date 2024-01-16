from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile, Post, Avaliation, Comentario, Follower
from django.shortcuts import get_object_or_404


from django.contrib.auth.decorators import login_required


def index(request):
    # pega todos os posts
    posts = Post.objects.order_by("created_at").all()

    # condição para verificar se o usuario está logado
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
        # retorna a foto do perfil

        return render(request, 'index.html', {'user_profile': user_profile, 'posts': posts})
    else:
        # retona a pagina normalmente
        return render(request, 'index.html', {'posts': posts})


@login_required(login_url='login')
def recomendar(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        livro = request.POST.get('livro')
        review = request.POST.get('review')
        link = request.POST.get('link')

        new_post = Post.objects.create(
            user=user, image=image, nm_livro=livro, review=review, link=link)
        new_post.save()

        return redirect('/')
    else:
        return render(request, 'recomendar.html')


# def calculate_new_average(avaliation):
#     ratings = Post.objects.filter(item=avaliation)
#     average = sum([rating.value for rating in ratings]) / len(ratings)

#     return average


@login_required(login_url='login')
def avaliacao(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    aval_filter = Avaliation.objects.filter(
        post_id=post_id, username=username).first()

    if aval_filter == None:
        new_aval = Avaliation.objects.create(
            post_id=post_id, username=username)
        new_aval.save()
        post.avaliation = post.avaliation + 1
        post.save()
        return redirect('/')
    else:
        aval_filter.delete()
        post.avaliation = post.avaliation - 1
        post.save()
        return redirect('/')


@login_required(login_url='login')
def comentario(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        comentario_texto = request.POST.get('comentario')
        comentario = Comentario.objects.create(
            post=post, username=username, comentario=comentario_texto)
        comentario.save()
        return redirect('recomendacao', pk=post_id)
    else:
        return redirect('/')


@login_required(login_url='login')
def perfil(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
    }
    return render(request, 'perfil.html', context)


@login_required(login_url='login')
def seguir(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if Follower.objects.filter(follower=follower, user=user).first():
            delete_follower = Follower.objects.get(
                follower=follower, user=user)
            delete_follower.delete()
            return redirect('/perfil/' + user)

        else:
            new_follower = Follower.objects.create(
                follower=follower, user=user)
            new_follower.save()
            return redirect('/perfil/' + user)

    else:
        return redirect('/')


@login_required(login_url='login')
def recomendacao(request, pk):
    post = Post.objects.get(id=pk)
    comentarios = Comentario.objects.filter(post=post)
    user_profile = Profile.objects.get(username=post.user)  # Adicionado

    context = {
        'post': post,
        'comentarios': comentarios,
        'user_profile': user_profile,  # Adicionado
    }
    return render(request, 'recomendacao.html', context)


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

# < --------- PAREI AQUI


def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Usuário ou senha incorretos')
            return redirect('login')
    else:
        return render(request, 'login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('index')


@login_required(login_url='/login/')
def home(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, 'home.html', {'user': user_profile.user})

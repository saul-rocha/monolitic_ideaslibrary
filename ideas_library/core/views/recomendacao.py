from django.shortcuts import render
from ..models import Profile, Post, Comentario
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def recomendacao(request, pk):
    post = Post.objects.get(id=pk)
    comentarios = Comentario.objects.filter(post=post)
    user_object = User.objects.get(username=post.user)
    user_profile = Profile.objects.get(user=user_object)
    
    context = {
        'post': post,
        'comentarios': comentarios,
        'user_profile': user_profile,  # Adicionado
        'ehDoUser': post.user == request.user.username,
        'qntComentarios': len(comentarios)
    }
    return render(request, 'recomendacao.html', context)


@login_required(login_url='login')
def recomendacoes(request):
    posts = Post.objects.all()
    context = {'posts': posts, 'qnt': len(posts)}
    return render(request, 'recomendacoes.html', context)

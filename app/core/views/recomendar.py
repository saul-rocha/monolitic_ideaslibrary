from django.shortcuts import render, redirect
from ..models import Post

from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def recomendar(request):

    if request.method == 'POST':

        if request.FILES.get('image_upload') == None:
            image = Post().image
        else:
            image = request.FILES.get('image_upload')

        user = request.user.username
        livro = request.POST.get('livro')
        review = request.POST.get('review')
        link = request.POST.get('link')

        Post.objects.create(
            user=user, image=image, nm_livro=livro, review=review, link=link)

        return redirect('/recomendacoes')
    
    else:
        return render(request, 'recomendar.html')

from django.shortcuts import redirect
from ..models import Post, Comentario
from django.shortcuts import get_object_or_404


from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def comentario(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        comentario_texto = request.POST.get('comentario')
        Comentario.objects.create(
            post=post, username=username, comentario=comentario_texto)

        return redirect('recomendacao', pk=post_id)
    else:
        return redirect('/')

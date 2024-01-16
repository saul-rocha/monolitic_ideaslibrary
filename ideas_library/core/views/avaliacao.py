from django.shortcuts import get_object_or_404, redirect
from django.db.models import F
from ..models import Post, Avaliation
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def avaliacao(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = get_object_or_404(Post, id=post_id)

    aval_filter = Avaliation.objects.filter(post_id=post_id, username=username).first()

    print(aval_filter)

    if not aval_filter:
        Avaliation.objects.create(post_id=post_id, username=username)
        post.avaliation = F('avaliation') + 1
        post.save()
    else:
        aval_filter.delete()
        post.avaliation = F('avaliation') - 1
        post.save()

    return redirect(f'/recomendacao/{post_id}')
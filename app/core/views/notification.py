from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from notifications.models import Notification
from ..models import Post, Follower, Comentario, Avaliation
from django.contrib.auth.models import User
from django.shortcuts import render

# noficação de Postagem


@receiver(post_save, sender=Post)
def post_save_notification(sender, instance, **kwargs):

    # Obtém os seguidores do usuário que fez a postagem
    followers = Follower.objects.filter(user=instance.user)
    followers = followers.values_list('follower', flat=True)
    print(followers)
    for follower in followers:

        # Cria uma mensagem para a notificação
        message = f'{instance.user} fez uma nova postagem: "{instance.nm_livro}"'

        follower_receptor = User.objects.get(username=follower)
        ator = User.objects.get(username=instance.user)
        # Cria a notificação para cada seguidor
        Notification.objects.create(

            recipient=follower_receptor,
            actor=ator,  # Define o usuário que fez a postagem como o "ator"
            verb='postagem',
            target=instance,
            description=message
        )


@receiver(post_save, sender=Comentario)
def comment_save_notification(sender, instance, **kwargs):

    post = instance.post

    receptor = User.objects.get(username=post.user)
    ator = User.objects.get(username=instance.username)

    # Cria uma mensagem para a notificação
    message = '{} comentou seu post do livro {}'.format(ator,
                                                        post.nm_livro)

    # Cria a notificação para cada seguidor
    Notification.objects.create(

        recipient=receptor,
        actor=ator,  # Define o usuário que fez a postagem como o "ator"
        verb='comentario',
        target=instance,
        description=message
    )


@receiver(post_save, sender=Avaliation)
def avaliation_save_notification(sender, instance, **kwargs):

    post = Post.objects.get(id=instance.post_id)

    # Cria uma mensagem para a notificação
    message = '{} curtiu seu post: {}'.format(instance.username, post.nm_livro)

    receptor = User.objects.get(username=post.user)
    ator = User.objects.get(username=instance.username)
    # Cria a notificação para cada seguidor
    Notification.objects.create(

        recipient=receptor,
        actor=ator,  # Define o usuário que fez a postagem como o "ator"
        verb='avaliation',
        target=instance,
        description=message
    )


@receiver(post_delete, sender=Avaliation)
def unavaliation_save_notification(sender, instance, **kwargs):

    post = Post.objects.get(id=instance.post_id)

    # Cria uma mensagem para a notificação
    message = '{} descurtiu seu post: {}'.format(
        instance.username, post.nm_livro)

    receptor = User.objects.get(username=post.user)
    ator = User.objects.get(username=instance.username)
    # Cria a notificação para cada seguidor
    Notification.objects.create(

        recipient=receptor,
        actor=ator,  # Define o usuário que fez a postagem como o "ator"
        verb='avaliation',
        target=instance,
        description=message
    )


@receiver(post_save, sender=Follower)
def follow_save_notification(sender, instance, **kwargs):

    # Cria uma mensagem para a notificação
    message = '{} começou a te seguir'.format(instance.follower)

    receptor = User.objects.get(username=instance.user)
    ator = User.objects.get(username=instance.follower)
    # Cria a notificação para cada seguidor
    Notification.objects.create(

        recipient=receptor,
        actor=ator,  # Define o usuário que fez a postagem como o "ator"
        verb='seguir',
        target=instance,
        description=message
    )


@receiver(post_delete, sender=Follower)
def unfollow_notification(sender, instance, **kwargs):
    # Cria uma mensagem para a notificação
    message = '{} deixou de te seguir'.format(instance.follower)

    receptor = User.objects.get(username=instance.user)
    ator = User.objects.get(username=instance.follower)
    # Cria a notificação para cada seguidor
    Notification.objects.create(
        recipient=receptor,
        actor=ator,  # Define o usuário que fez a postagem como o "ator"
        verb='deixar de seguir',
        target=instance,
        description=message
    )


def notifications(request):
    # Obtém as notificações do usuário atual
    # notifications = Notification.objects.filter(recipient=request.user, unread=True)
    notifications = Notification.objects.filter(recipient=request.user)

    nao_lidas = [ x for x in notifications if x.unread ]
    lidas = [ x for x in notifications if not x.unread ]
    
    notificacoes = {
        'lidas': {
            'qnt': len(lidas),
            'notificacoes': lidas
        },
        'nao_lidas': {
            'qnt': len(nao_lidas),
            'notificacoes': nao_lidas
        }
    }

    # Marca todas as notificações não lidas como lidas
    for notification in notifications:
        notification.unread = False
        notification.save()

    return render(request, 'notifications.html', {'notifications': notifications, 'notificacoes': notificacoes})

from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, blank=True)
    id_user = models.IntegerField(null=True)
    # bio = models.TextField(blank=True)
    profileimage = models.ImageField(
        upload_to='profile_images', default='do-utilizador.png')
    # location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    nm_livro = models.CharField(max_length=100, default='')
    review = models.TextField(blank=False)
    link = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='post_images',
                              default='conhecimento.png')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    avaliation = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class Avaliation(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Comentario(models.Model):

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    comentario = models.TextField()

    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.username


class Follower(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user

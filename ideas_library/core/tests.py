from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Follower
from notifications.models import Notification


class NotificationTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='12345')
        self.user2 = User.objects.create_user(
            username='user2', password='12345')
        self.post = Post.objects.create(
            user=self.user1, nm_livro='Livro Teste')

        Follower.objects.create(user=self.user1, follower=self.user2)

    def test_post_save_notification(self):
        self.post.save()

        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.recipient, self.user2)
        self.assertEqual(notification.actor, self.user1)
        self.assertEqual(notification.target, self.post)
        self.assertEqual(notification.verb, 'fez uma nova postagem')
        self.assertEqual(notification.description,
                         'user1 fez uma nova postagem: "Livro Teste"')

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    def follow(self, user):
        if user != self:  # Prévenir l'utilisateur de se suivre lui-même
            self.following.add(user)

    def unfollow(self, user):
        self.following.remove(user)

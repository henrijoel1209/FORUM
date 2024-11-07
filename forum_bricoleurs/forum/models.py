from django.db import models
from django.conf import settings
from notifications.signals import notify

class Subscription(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscriptions', on_delete=models.CASCADE)
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscribers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='disliked_posts')

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            for follower in self.author.subscribers.all():
                notify.send(
                    self.author,
                    recipient=follower.subscriber,
                    verb='a publié un nouveau post',
                    target=self
                )

class Step(models.Model):
    post = models.ForeignKey(Post, related_name='steps', on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    description = models.TextField(default='Entrez votre description ici')  # Valeur par défaut
    image = models.ImageField(upload_to='steps/', null=True, blank=True)  # Champ image

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

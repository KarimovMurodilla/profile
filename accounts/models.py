from django.db import models

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bio = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.username


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    commentator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='commentators')
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title